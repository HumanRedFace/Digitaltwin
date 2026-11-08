#!/usr/bin/env python3
"""
Cek teks keluar dari KARTU (bukan hanya dari kanvas).
Kartu didefinisikan ulang di sini dengan koordinat yang sama seperti wireframe.py,
lalu setiap label dicocokkan ke kartu yang memuat titik tengahnya.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import wireframe as W

# kartu pada panel desktop (koordinat axes 0..1) — disalin dari wireframe.py
KARTU_DESKTOP = {
    "topbar":        (0.006, 0.930, 0.988, 0.062),
    "sidebar":       (0.006, 0.060, 0.128, 0.862),
    "viewport":      (0.140, 0.148, 0.612, 0.774),
    "armada":        (0.760, 0.700, 0.234, 0.222),
    "peringatan":    (0.760, 0.402, 0.234, 0.286),
    "radar":         (0.760, 0.230, 0.234, 0.158),
    "performa":      (0.760, 0.148, 0.234, 0.072),
    "timeline":      (0.140, 0.060, 0.854, 0.076),
    "kualitas":      (0.014, 0.075, 0.112, 0.088),
    "tooltip":       (0.140 + 0.34, 0.148 + 0.56, 0.205, 0.115),
}


def audit(make_fn, nama, cards, tol=0.004):
    cap = {}
    orig = matplotlib.figure.Figure.savefig
    def fake(self, *a, **k): cap["fig"] = self
    matplotlib.figure.Figure.savefig = fake
    try: make_fn("/tmp/_f.png")
    finally: matplotlib.figure.Figure.savefig = orig
    fig = cap["fig"]
    r = fig.canvas.get_renderer()
    Wpx, Hpx = fig.get_size_inches()[0] * fig.dpi, fig.get_size_inches()[1] * fig.dpi

    ax = fig.axes[0]
    issues = 0
    print(f"\n=== {nama}")
    for t in ax.texts:
        s = t.get_text().strip()
        if not s: continue
        bb = t.get_window_extent(renderer=r)
        mx, my = (bb.x0 + bb.x1) / 2 / Wpx, (bb.y0 + bb.y1) / 2 / Hpx
        host = None
        for k, (x, y, w, h) in cards.items():
            if x <= mx <= x + w and y <= my <= y + h:
                if host is None or (w * h) < (cards[host][2] * cards[host][3]):
                    host = k
        if host is None:
            continue
        x, y, w, h = cards[host]
        if bb.x1 / Wpx > x + w - tol or bb.x0 / Wpx < x + tol:
            issues += 1
            print(f"  !! '{s[:44]}' keluar horizontal dari kartu '{host}': "
                  f"teks [{bb.x0/Wpx:.3f},{bb.x1/Wpx:.3f}] kartu [{x:.3f},{x+w:.3f}]")
        if bb.y1 / Hpx > y + h + tol or bb.y0 / Hpx < y - tol:
            issues += 1
            print(f"  !! '{s[:44]}' keluar vertikal dari kartu '{host}': "
                  f"teks [{bb.y0/Hpx:.3f},{bb.y1/Hpx:.3f}] kartu [{y:.3f},{y+h:.3f}]")
    print(f"  masalah: {issues}")
    plt.close(fig)
    return issues


if __name__ == "__main__":
    n = audit(W.panel_desktop, "desktop: teks vs kartu", KARTU_DESKTOP)
    print("\nTOTAL:", n)
