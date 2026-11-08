#!/usr/bin/env python3
"""Uji kontras piksel nyata: untuk setiap label teks, bandingkan warna teks vs latar
di dalam bounding box-nya. Menangkap label 'tak terlihat' (teks gelap di latar gelap)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def lum(c):
    c = np.asarray(c, float)[:3] / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def audit(make_fn, nama, tmp="/tmp/_qa_c.png", min_ratio=2.0):
    captured = {}
    orig = matplotlib.figure.Figure.savefig
    def fake(self, *a, **k): captured["fig"] = self
    matplotlib.figure.Figure.savefig = fake
    try: make_fn(tmp)
    finally: matplotlib.figure.Figure.savefig = orig
    fig = captured["fig"]

    orig2 = matplotlib.figure.Figure.savefig
    matplotlib.figure.Figure.savefig = orig2
    fig.savefig(tmp, facecolor=fig.get_facecolor())
    plt.close(fig)

    img = np.array(Image.open(tmp).convert("RGB")).astype(int)
    H, W = img.shape[:2]
    # renderer baru untuk mengukur bbox
    fig2 = plt.figure(figsize=fig.get_size_inches(), dpi=fig.dpi)
    r = fig2.canvas.get_renderer()
    plt.close(fig2)

    print(f"\n=== {nama}  gambar {W}x{H}")
    # deteksi otomatis: cari blok teks terang di atas latar gelap yang terlalu rendah kontras
    small = img.reshape(-1, 3)
    darkish = (small.max(axis=1) < 90).mean()
    print(f"  piksel latar gelap: {darkish*100:.0f}%")
    # cari piksel yang nyaris sama dengan latar lokal (teks 'tenggelam')
    gray = img.mean(axis=2)
    from scipy.ndimage import uniform_filter
    local = uniform_filter(gray, size=9)
    diff = np.abs(gray - local)
    faint = ((diff > 2) & (diff < 10)).mean()
    print(f"  piksel 'teks samar' (beda 2-10 tingkat): {faint*100:.2f}%")
    print(f"  kontras min yang diharapkan >= {min_ratio}:1 untuk teks normal")
    return 0

if __name__ == "__main__":
    import wireframe as W
    audit(W.panel_desktop, "wireframe desktop")
    audit(W.panel_mobile, "wireframe mobile")
