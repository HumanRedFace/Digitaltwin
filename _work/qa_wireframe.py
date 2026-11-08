#!/usr/bin/env python3
"""
QA tata letak wireframe TANPA vision: memakai bounding box teks asli dari renderer
matplotlib. Mendeteksi (a) teks yang tumpang tindih, (b) teks yang keluar dari kanvas.
Jalankan dengan mengimpor modul wireframe dan menangkap figure-nya.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import wireframe as W


def audit(make_fn, nama, pad_px=1.0, min_area=14):
    fig = plt.figure()
    plt.close(fig)
    # tangkap figure yang dibuat fungsi: monkeypatch savefig
    captured = {}
    orig = matplotlib.figure.Figure.savefig

    def fake(self, *a, **k):
        captured["fig"] = self
    matplotlib.figure.Figure.savefig = fake
    try:
        make_fn("/tmp/_qa.png")
    finally:
        matplotlib.figure.Figure.savefig = orig

    fig = captured["fig"]
    r = fig.canvas.get_renderer()
    W_px = fig.get_size_inches()[0] * fig.dpi
    H_px = fig.get_size_inches()[1] * fig.dpi

    texts = []
    for ax in fig.axes:
        for t in ax.texts:
            s = t.get_text()
            if not s.strip():
                continue
            try:
                bb = t.get_window_extent(renderer=r)
            except Exception:
                continue
            texts.append(dict(s=s.replace("\n", " | "), bb=bb, size=t.get_fontsize()))

    print(f"\n=== {nama} — {len(texts)} label teks, kanvas {W_px:.0f}x{H_px:.0f} px")

    # 1) keluar kanvas
    out = 0
    for t in texts:
        b = t["bb"]
        if b.x0 < -pad_px or b.y0 < -pad_px or b.x1 > W_px + pad_px or b.y1 > H_px + pad_px:
            out += 1
            print(f"  !! KELUAR KANVAS: '{t['s'][:48]}'  x[{b.x0:.0f},{b.x1:.0f}] y[{b.y0:.0f},{b.y1:.0f}]")

    # 2) tumpang tindih teks
    coll = 0
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i]["bb"], texts[j]["bb"]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 1.5 and oy > 1.5:
                area = ox * oy
                smaller = min((a.x1 - a.x0) * (a.y1 - a.y0), (b.x1 - b.x0) * (b.y1 - b.y0))
                if area > min_area and area > 0.18 * smaller:
                    coll += 1
                    print(f"  !! TUMPANG-TINDIH {area:.0f}px2: '{texts[i]['s'][:34]}'  <->  '{texts[j]['s'][:34]}'")

    print(f"  hasil: keluar-kanvas={out}, tumpang-tindih={coll}")
    plt.close(fig)
    return out + coll


if __name__ == "__main__":
    bad = 0
    bad += audit(W.panel_desktop, "wireframe desktop")
    bad += audit(W.panel_mobile, "wireframe mobile")
    print("\nTOTAL MASALAH:", bad)
    sys.exit(0)
