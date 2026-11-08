#!/usr/bin/env python3
"""
Wireframe konseptual 3D Viewer — digambar sebagai gambar raster (bukan mockup HTML),
supaya bisa langsung masuk .docx dan tidak menimbulkan klaim "aplikasi sudah jadi".

Panel 1 : desktop 1920x1080 — mode LIVE
Panel 2 : tablet/mobile 900x1600 — mode LIVE (kolom kanan dilipat)
Semua angka yang muncul di layar berasal dari data.py / data lapangan nyata.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np
import data as D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wireframe")
os.makedirs(OUT, exist_ok=True)

# ── palet (mengikuti identitas Minergo: merah #E11B22, dasar gelap) ─────────
BG      = "#0E1116"
PANEL   = "#161B22"
PANEL2  = "#1C232C"
STROKE  = "#2B3542"
TXT     = "#E6EDF3"
TXT2    = "#8B97A5"
ACCENT  = "#E11B22"
OK      = "#3FB950"
WARN    = "#D29922"
INFO    = "#58A6FF"
TERRAIN = "#3B4A3F"
ROAD    = "#6B5B45"

plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 200})


def box(ax, x, y, w, h, fc=PANEL, ec=STROKE, lw=1.0, r=0.010, z=2, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha,
                       transform=ax.transAxes, clip_on=False)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=8, color=TXT, weight="normal", ha="left", va="center",
        z=6, family="DejaVu Sans", ls=0):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=size, color=color,
            fontweight=weight, ha=ha, va=va, zorder=z, family=family, linespacing=ls)


def chip(ax, x, y, w, h, label, fc, tc="#08131A", size=6.4):
    box(ax, x, y, w, h, fc=fc, ec="none", r=0.014, z=7)
    txt(ax, x + w / 2, y + h / 2, label, size=size, color=tc, weight="bold",
        ha="center", z=8)


def scene3d(ax, box_xywh, horizon=0.62, tint="#1A222B"):
    """Gambar latar scene 3D semu: langit, terrain, haul road, armada."""
    x0, y0, w, h = box_xywh
    # langit
    ax.add_patch(Rectangle((x0, y0 + h * horizon), w, h * (1 - horizon),
                           transform=ax.transAxes, fc="#131A22", ec="none", zorder=1, clip_on=False))
    # terrain (poligon bergelombang)
    xs = np.linspace(x0, x0 + w, 220)
    base = y0 + h * horizon
    yy = base + 0.028 * h * np.sin(np.linspace(0, 7.2, 220)) + 0.014 * h * np.sin(np.linspace(0, 21, 220))
    verts = [(x0, y0)] + list(zip(xs, yy)) + [(x0 + w, y0)]
    ax.add_patch(Polygon(verts, transform=ax.transAxes, fc=TERRAIN, ec="none", zorder=1.4, clip_on=False))
    # haul road: pita perspektif
    road = [(x0 + w * 0.06, y0 + h * 0.02), (x0 + w * 0.30, base + h * 0.01),
            (x0 + w * 0.60, base + h * 0.02), (x0 + w * 0.98, y0 + h * 0.0),
            (x0 + w * 0.98, y0 + h * 0.07), (x0 + w * 0.60, base + h * 0.09),
            (x0 + w * 0.30, base + h * 0.07), (x0 + w * 0.06, y0 + h * 0.10)]
    ax.add_patch(Polygon(road, transform=ax.transAxes, fc=ROAD, ec="none", zorder=1.6,
                         clip_on=False, alpha=.92))
    # garis tengah jalan
    ax.plot([x0 + w * .06, x0 + w * .30, x0 + w * .60, x0 + w * .97],
            [y0 + h * .062, base + h * .05, base + h * .058, y0 + h * .035],
            transform=ax.transAxes, color="#9A8A6A", lw=.8, ls=(0, (5, 4)), zorder=1.7, alpha=.5)
    # grid permukaan (isyarat "ini 3D, bukan citra 2D")
    for i in range(1, 9):
        t = i / 9
        ax.plot([x0 + w * (0.30 + t * 0.62), x0 + w * (0.30 + t * 0.30)],
                [base + h * 0.012, y0 + h * 0.006],
                transform=ax.transAxes, color="#FFFFFF", lw=.35, alpha=.06, zorder=1.8)


def truck(ax, cx, cy, s, color="#E8A33D", label=None, sub=None, warn=False, z=4):
    """Ikon truk angkut tampak atas-miring, digambar sebagai blok 3D sederhana."""
    w, h = s * 1.55, s * 0.95
    # bayangan
    ax.add_patch(Rectangle((cx - w / 2 + s * .10, cy - h / 2 - s * .08), w, h,
                           transform=ax.transAxes, fc="#000000", ec="none", alpha=.35, zorder=z - .2))
    # bak
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w * .66, h,
                           transform=ax.transAxes, fc=color, ec="#00000055", lw=.6, zorder=z))
    # kabin
    ax.add_patch(Rectangle((cx + w * .18, cy - h * .34), w * .30, h * .68,
                           transform=ax.transAxes, fc="#C4842C", ec="#00000055", lw=.6, zorder=z))
    # arah hadap
    ax.add_patch(Polygon([(cx + w * .50, cy), (cx + w * .40, cy + h * .16),
                          (cx + w * .40, cy - h * .16)], transform=ax.transAxes,
                         fc="#FFFFFF", ec="none", alpha=.75, zorder=z + .1))
    if warn:
        ax.add_patch(Circle((cx, cy), s * 1.15, transform=ax.transAxes, fc="none",
                            ec=ACCENT, lw=1.4, alpha=.85, zorder=z + .2))
    if label:
        txt(ax, cx, cy + s * .78, label, size=6.4, color=TXT, weight="bold", ha="center", z=z + .3)
    if sub:
        txt(ax, cx, cy - s * .82, sub, size=5.6, color=TXT2, ha="center", z=z + .3)


# ══════════════════════════════════════════════════════════════════════════
# PANEL 1 — DESKTOP
# ══════════════════════════════════════════════════════════════════════════
def panel_desktop(path):
    fig = plt.figure(figsize=(13.2, 7.45))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec="none", zorder=0))

    # ── top bar ────────────────────────────────────────────────────────────
    box(ax, 0.006, 0.930, 0.988, 0.062, fc=PANEL, r=0.008, z=3)
    txt(ax, 0.022, 0.961, "MINERGO", size=11.5, weight="bold", z=6)
    txt(ax, 0.078, 0.961, "DIGITAL TWIN 3D", size=11.5, color=TXT2, z=6)
    txt(ax, 0.078, 0.941, "R&D — konsep, bukan implementasi", size=5.8, color=TXT2, z=6)
    # tab mode (WAJIB terlihat)
    chip(ax, 0.300, 0.941, 0.052, 0.038, "LIVE", ACCENT)
    box(ax, 0.356, 0.941, 0.058, 0.038, fc="#10161D", r=0.010, z=7)
    txt(ax, 0.385, 0.960, "REPLAY", size=6.4, color=TXT2, ha="center", z=8)
    box(ax, 0.418, 0.941, 0.068, 0.038, fc="#10161D", r=0.010, z=7)
    txt(ax, 0.452, 0.960, "SIMULASI", size=6.4, color=TXT2, ha="center", z=8)
    # status kanan
    chip(ax, 0.700, 0.947, 0.075, 0.026, "● LATENCY 840 ms", "#132A1B", size=5.6)
    ax.patches[-1].set_edgecolor(STROKE)
    txt(ax, 0.700, 0.947, "●", size=6, color=OK, z=9)
    txt(ax, 0.783, 0.960, "SITE  PIT A — HAUL ROAD 07", size=6.2, color=TXT2, z=8)
    txt(ax, 0.972, 0.960, "R. Pratama", size=6.6, z=8, ha="right")
    txt(ax, 0.972, 0.942, "Dispatcher", size=5.6, color=TXT2, z=8, ha="right")

    # ── sidebar kiri ───────────────────────────────────────────────────────
    box(ax, 0.006, 0.060, 0.128, 0.862, fc=PANEL, r=0.008, z=3)
    items = [("Peta 3D", True), ("Armada", False), ("Geofence", False),
             ("Replay", False), ("Radar", False), ("Lapisan", False), ("Setelan", False)]
    yy = 0.884
    for name, active in items:
        if active:
            box(ax, 0.014, yy - 0.026, 0.112, 0.040, fc="#2A1519", ec="#5A2027", r=0.010, z=4)
            ax.add_patch(Rectangle((0.014, yy - 0.026), 0.004, 0.040, transform=ax.transAxes,
                                   fc=ACCENT, ec="none", zorder=5))
        txt(ax, 0.032, yy - 0.006, name, size=7.2, color=TXT if active else TXT2,
            weight="bold" if active else "normal", z=6)
        yy -= 0.052
    txt(ax, 0.020, 0.545, "LAPISAN", size=5.8, color=TXT2, weight="bold", z=6)
    layers = [("Ortomosaik drone", OK), ("Haul road", OK), ("Geofence", OK),
              ("Trail 30 mnt", OK), ("Model armada", OK), ("Objek radar", WARN),
              ("Point cloud", "#4A5563")]
    yy = 0.512
    for name, c in layers:
        ax.add_patch(Circle((0.026, yy), 0.0038, transform=ax.transAxes, fc=c, ec="none", zorder=6))
        txt(ax, 0.040, yy, name, size=6.4, color=TXT if c != "#4A5563" else TXT2, z=6)
        yy -= 0.031
    # status data
    box(ax, 0.014, 0.075, 0.112, 0.088, fc="#10161D", r=0.008, z=4)
    txt(ax, 0.022, 0.148, "KUALITAS DATA", size=5.4, color=TXT2, weight="bold", z=6)
    txt(ax, 0.022, 0.128, "RTK FIX", size=6.0, color=TXT2, z=6)
    txt(ax, 0.118, 0.128, "32,9%", size=6.2, color=WARN, ha="right", z=6)
    txt(ax, 0.022, 0.110, "RTK FLOAT", size=6.0, color=TXT2, z=6)
    txt(ax, 0.118, 0.110, "67,1%", size=6.2, color=ACCENT, ha="right", z=6)
    txt(ax, 0.022, 0.090, "Satelit", size=6.0, color=TXT2, z=6)
    txt(ax, 0.118, 0.090, "48", size=6.2, color=TXT, ha="right", z=6)

    # ── viewport 3D ────────────────────────────────────────────────────────
    VX, VY, VW, VH = 0.140, 0.148, 0.612, 0.774
    box(ax, VX, VY, VW, VH, fc="#0B1015", ec=STROKE, r=0.006, z=2)
    scene3d(ax, (VX, VY, VW, VH), horizon=0.66)
    # label viewport
    txt(ax, VX + 0.012, VY + VH - 0.024, "PIT A · HAUL ROAD 07 · 60 unit", size=6.6,
        color=TXT, weight="bold", z=9)
    txt(ax, VX + 0.012, VY + VH - 0.042,
        "Ortomosaik 1,35 cm/px · EPSG:32750 · survei 14 Okt 2026", size=5.6, color=TXT2, z=9)

    # geofence poligon
    gf = [(VX + .06, VY + .16), (VX + .27, VY + .30), (VX + .50, VY + .34),
          (VX + .55, VY + .18), (VX + .30, VY + .10)]
    ax.add_patch(Polygon(gf, transform=ax.transAxes, fc=ACCENT, ec=ACCENT,
                         lw=1.2, alpha=.10, zorder=3, ls="--", clip_on=False))
    ax.add_patch(Polygon(gf, transform=ax.transAxes, fc="none", ec=ACCENT,
                         lw=1.1, alpha=.75, zorder=3.1, ls=(0, (4, 3)), clip_on=False))
    txt(ax, VX + .10, VY + .315, "GEOFENCE — SPEED ≤ 25 km/h", size=5.5, color=ACCENT, z=9)

    # armada
    truck(ax, VX + .20, VY + .38, .016, label="HD-018", sub="FIX · 18 km/h")
    truck(ax, VX + .33, VY + .30, .014, color="#E8A33D", label="HD-021", sub="FLOAT · 24 km/h")
    truck(ax, VX + .46, VY + .22, .013, label="HD-007", sub="FIX · 0 km/h")
    truck(ax, VX + .27, VY + .52, .013, color="#C9D1D9", label="LV-014", sub="FIX · 31 km/h")
    # unit bermasalah
    truck(ax, VX + .40, VY + .44, .012, color="#E8A33D", label="HD-033",
          sub="FLOAT · 27 km/h", warn=True)
    txt(ax, VX + .40, VY + .44 - .030, "di luar geofence", size=5.2, color=ACCENT,
        ha="center", weight="bold", z=9)
    # excavator
    ax.add_patch(Rectangle((VX + .15, VY + .20), .026, .020, transform=ax.transAxes,
                           fc="#7B8CA0", ec="#00000055", lw=.6, zorder=4))
    txt(ax, VX + .163, VY + .233, "EX-05", size=5.6, color=TXT, ha="center", weight="bold", z=6)

    # kompas + skala
    ax.add_patch(Circle((VX + VW - 0.036, VY + VH - 0.044), 0.018, transform=ax.transAxes,
                        fc="#0E1116", ec=STROKE, lw=.8, zorder=8))
    ax.add_patch(Polygon([(VX + VW - 0.036, VY + VH - 0.028), (VX + VW - 0.041, VY + VH - 0.050),
                          (VX + VW - 0.031, VY + VH - 0.050)], transform=ax.transAxes,
                         fc=ACCENT, ec="none", zorder=9))
    txt(ax, VX + VW - 0.036, VY + VH - 0.056, "N", size=5.4, color=TXT2, ha="center", z=9)
    ax.plot([VX + VW - 0.115, VX + VW - 0.045], [VY + 0.020, VY + 0.020],
            transform=ax.transAxes, color=TXT2, lw=1.4, zorder=8)
    txt(ax, VX + VW - 0.080, VY + 0.032, "50 m", size=5.4, color=TXT2, ha="center", z=8)

    # tooltip unit
    box(ax, VX + .34, VY + .56, .205, .115, fc="#0F1520", ec=INFO, r=0.008, z=10, alpha=.97)
    txt(ax, VX + .352, VY + .655, "HD-033 · CAT 785D", size=6.8, weight="bold", z=11)
    rows = [("Posisi", "−1,22941 / 116,89412"),
            ("Kecepatan", "27,4 km/h"),
            ("Heading", "318°  (course beku 1,1 s)"),
            ("Kualitas", "RTK FLOAT · 41 sat · HDOP 0,44"),
            ("Status", "Di luar geofence · zona bahaya")]
    yy = VY + .634
    for k, v in rows:
        txt(ax, VX + .352, yy, k, size=5.6, color=TXT2, z=11)
        txt(ax, VX + .425, yy, v, size=5.6, color=TXT
            if k != "Status" else ACCENT, z=11,
            weight="bold" if k == "Status" else "normal")
        yy -= .019
    txt(ax, VX + .352, VY + .568, "Klik → fokus kamera · buka replay 5 mnt sebelum kejadian",
        size=5.0, color=TXT2, z=11)

    # ── kolom kanan ────────────────────────────────────────────────────────
    RX, RW = 0.760, 0.234
    # kartu 1: ringkasan armada
    box(ax, RX, 0.700, RW, 0.222, fc=PANEL, r=0.008, z=3)
    txt(ax, RX + .012, 0.904, "ARMADA AKTIF", size=6.6, weight="bold", z=6)
    txt(ax, RX + RW - .012, 0.904, "60 / 64", size=6.6, color=OK, ha="right", weight="bold", z=6)
    kpi = [("Mengangkut", "38", OK), ("Antre", "11", INFO),
           ("Perawatan", "4", WARN), ("Idle > 10 mnt", "7", ACCENT)]
    yy = 0.872
    for label, val, c in kpi:
        ax.add_patch(Rectangle((RX + .012, yy - .008), .004, .016, transform=ax.transAxes,
                               fc=c, ec="none", zorder=5))
        txt(ax, RX + .024, yy, label, size=6.2, color=TXT2, z=6)
        txt(ax, RX + RW - .012, yy, val, size=6.6, color=c, ha="right", weight="bold", z=6)
        yy -= 0.034

    # kartu 2: peringatan
    box(ax, RX, 0.402, RW, 0.286, fc=PANEL, r=0.008, z=3)
    txt(ax, RX + .012, 0.670, "PERINGATAN", size=6.6, weight="bold", z=6)
    chip(ax, RX + RW - .050, 0.660, .038, .019, "3 BARU", ACCENT, size=5.2)
    alerts = [
        (ACCENT, "Pelanggaran geofence", "HD-033 keluar zona · 27 km/h", "10:42:11"),
        (WARN,   "Kecepatan > batas", "HD-021 · 34 km/h di tikungan", "10:41:02"),
        (INFO,   "Kualitas posisi turun", "HD-007 FLOAT 48 s (sat 29)", "10:38:55"),
    ]
    yy = 0.630
    for c, title, desc, t in alerts:
        ax.add_patch(Rectangle((RX + .012, yy - .052), .003, .058, transform=ax.transAxes,
                               fc=c, ec="none", zorder=5))
        txt(ax, RX + .022, yy - .006, title, size=6.2, weight="bold", color=TXT, z=6)
        txt(ax, RX + .022, yy - .026, desc, size=5.5, color=TXT2, z=6)
        txt(ax, RX + .022, yy - .044, t, size=5.2, color=TXT2, z=6)
        yy -= 0.076

    # kartu 3: radar (jujur — belum ada)
    box(ax, RX, 0.230, RW, 0.158, fc="#1A1410", ec="#4A3520", r=0.008, z=3)
    txt(ax, RX + .012, 0.368, "OBJEK TERDETEKSI RADAR", size=6.6, weight="bold", color=WARN, z=6)
    chip(ax, RX + RW - .076, 0.358, .064, .019, "BELUM ADA", "#4A3520", tc=WARN, size=5.2)
    txt(ax, RX + .012, 0.342,
        "Radar PSA27/C95M hanya mengeluarkan\nstatus alarm (LED/buzzer), bukan daftar\nobjek berkoordinat.",
        size=5.6, color=TXT2, z=6, va="top")
    txt(ax, RX + .012, 0.264,
        "Panel ini aktif hanya bila vendor\nmenyediakan SDK / object list.",
        size=5.6, color=WARN, z=6, va="top")
    txt(ax, RX + .012, 0.240, "Lihat risiko R-1 · pertanyaan V-1, V-3",
        size=5.0, color=TXT2, z=6)

    # kartu 4: performa
    box(ax, RX, 0.148, RW, 0.072, fc=PANEL, r=0.008, z=3)
    txt(ax, RX + .012, 0.204, "PERFORMA VIEWER", size=5.8, weight="bold", color=TXT2, z=6)
    txt(ax, RX + .012, 0.182, "88 fps", size=9.5, weight="bold", color=OK, z=6)
    txt(ax, RX + .058, 0.182, "60 truk + 1 jt titik", size=5.4, color=TXT2, z=6)
    txt(ax, RX + .012, 0.162, "3 draw call · 11,3 ms/frame · uji nyata",
        size=5.2, color=TXT2, z=6)

    # ── timeline bawah ─────────────────────────────────────────────────────
    box(ax, 0.140, 0.060, 0.854, 0.076, fc=PANEL, r=0.008, z=3)
    txt(ax, 0.152, 0.118, "TIMELINE — 30 MENIT TERAKHIR", size=5.8, color=TXT2,
        weight="bold", z=6)
    chip(ax, 0.760, 0.108, 0.038, 0.019, "1×", ACCENT, size=5.4)
    box(ax, 0.802, 0.108, 0.032, 0.019, fc="#10161D", r=0.010, z=7)
    txt(ax, 0.818, 0.1175, "2×", size=5.4, color=TXT2, ha="center", z=8)
    box(ax, 0.838, 0.108, 0.032, 0.019, fc="#10161D", r=0.010, z=7)
    txt(ax, 0.854, 0.1175, "8×", size=5.4, color=TXT2, ha="center", z=8)
    # track
    ax.plot([0.152, 0.968], [0.088, 0.088], transform=ax.transAxes, color=STROKE, lw=4,
            solid_capstyle="round", zorder=5)
    # segmen kualitas (FIX hijau / FLOAT kuning) — mencerminkan 32,9% vs 67,1%
    np.random.seed(7)
    x = 0.152
    while x < 0.966:
        wseg = np.random.uniform(0.006, 0.030)
        c = OK if np.random.rand() < 0.33 else WARN
        ax.plot([x, min(x + wseg, 0.968)], [0.088, 0.088], transform=ax.transAxes,
                color=c, lw=4, solid_capstyle="butt", zorder=6, alpha=.85)
        x += wseg
    # penanda kejadian
    for xx, c in [(0.412, ACCENT), (0.607, WARN)]:
        ax.plot([xx, xx], [0.074, 0.100], transform=ax.transAxes, color=c, lw=1.5, zorder=7)
    txt(ax, 0.412, 0.070, "▲ geofence", size=5.0, color=ACCENT, ha="center", z=8)
    txt(ax, 0.607, 0.070, "▲ kecepatan", size=5.0, color=WARN, ha="center", z=8)
    for lab, xx in [("10:12", 0.152), ("10:22", 0.425), ("10:32", 0.700), ("10:42", 0.955)]:
        txt(ax, xx, 0.100, lab, size=5.0, color=TXT2, ha="center", z=8)

    # footer
    txt(ax, 0.140, 0.034,
        "WIREFRAME KONSEP — bukan tangkapan layar aplikasi. Angka pada layar berasal dari data lapangan nyata "
        "(RTK 28-10-2026, ortomosaik 14-10-2026) dan hasil uji render Lampiran C.",
        size=5.4, color=TXT2, z=6)
    txt(ax, 0.994, 0.034, "MNG-RND-DT-2026-001  ·  rev A", size=5.2, color=TXT2, ha="right", z=6)

    fig.savefig(path, facecolor=BG)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════
# PANEL 2 — TABLET / MOBILE
# ══════════════════════════════════════════════════════════════════════════
def panel_mobile(path):
    fig = plt.figure(figsize=(5.1, 9.2))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=BG, ec="none", zorder=0))
    box(ax, 0.010, 0.010, 0.980, 0.980, fc=BG, ec="#2B3542", r=0.030, z=1)

    # header ringkas
    box(ax, 0.022, 0.930, 0.956, 0.052, fc=PANEL, r=0.016, z=3)
    txt(ax, 0.044, 0.956, "MINERGO 3D", size=9, weight="bold", z=6)
    chip(ax, 0.360, 0.940, 0.120, 0.032, "LIVE", ACCENT, size=7)
    txt(ax, 0.560, 0.956, "Pit A", size=7, color=TXT2, z=6)
    ax.add_patch(Circle((0.930, 0.956), 0.016, transform=ax.transAxes, fc="#222B36",
                        ec=STROKE, lw=.7, zorder=6))
    txt(ax, 0.930, 0.956, "☰", size=7.5, color=TXT, ha="center", z=7)

    # viewport — mengisi hampir seluruh layar (keputusan desain: peta dulu)
    VX, VY, VW, VH = 0.022, 0.300, 0.956, 0.618
    box(ax, VX, VY, VW, VH, fc="#0B1015", ec=STROKE, r=0.012, z=2)
    scene3d(ax, (VX, VY, VW, VH), horizon=0.58)
    gf = [(VX + .08, VY + .13), (VX + .34, VY + .28), (VX + .70, VY + .32),
          (VX + .80, VY + .14), (VX + .40, VY + .06)]
    ax.add_patch(Polygon(gf, transform=ax.transAxes, fc=ACCENT, ec=ACCENT, lw=1.0,
                         alpha=.10, zorder=3, clip_on=False))
    ax.add_patch(Polygon(gf, transform=ax.transAxes, fc="none", ec=ACCENT, lw=1.0,
                         alpha=.7, zorder=3.1, ls=(0, (4, 3)), clip_on=False))
    truck(ax, VX + .26, VY + .38, .036, label="HD-018", sub="FIX · 18")
    truck(ax, VX + .62, VY + .30, .032, label="HD-021", sub="FLOAT · 24")
    truck(ax, VX + .46, VY + .52, .030, color="#E8A33D", label="HD-033", sub="27 · luar zona", warn=True)
    txt(ax, VX + .020, VY + VH - 0.030, "Pit A · Haul Road 07", size=7, weight="bold", z=9)
    txt(ax, VX + .020, VY + VH - 0.052, "Ortomosaik 1,35 cm/px · 14 Okt 2026",
        size=5.4, color=TXT2, z=9)

    # kartu unit terpilih — sheet dari bawah
    box(ax, 0.022, 0.108, 0.956, 0.180, fc=PANEL, r=0.020, z=4)
    ax.add_patch(Rectangle((0.470, 0.272), 0.060, 0.005, transform=ax.transAxes,
                           fc=STROKE, ec="none", zorder=6))
    txt(ax, 0.044, 0.250, "HD-033", size=9.5, weight="bold", z=6)
    txt(ax, 0.150, 0.250, "CAT 785D", size=6.4, color=TXT2, z=6)
    chip(ax, 0.780, 0.240, 0.175, 0.026, "LUAR GEOFENCE", ACCENT, size=6)
    # 4 metrik
    mets = [("27,4", "km/h", WARN), ("318°", "heading", TXT), ("41", "satelit", OK), ("0,44", "HDOP", OK)]
    xx = 0.048
    for val, lab, c in mets:
        txt(ax, xx, 0.206, val, size=9.5, color=c, weight="bold", z=6)
        txt(ax, xx, 0.186, lab, size=5.6, color=TXT2, z=6)
        xx += 0.235
    txt(ax, 0.044, 0.164, "RTK FLOAT · course beku 1,1 s · umur koreksi 1,2 s",
        size=5.6, color=TXT2, z=6)
    # aksi
    box(ax, 0.044, 0.120, 0.440, 0.030, fc="#222B36", ec=STROKE, r=0.014, z=6)
    txt(ax, 0.264, 0.135, "Fokus kamera", size=6.4, color=TXT, ha="center", z=7)
    box(ax, 0.508, 0.120, 0.440, 0.030, fc=ACCENT, ec="none", r=0.014, z=6)
    txt(ax, 0.728, 0.135, "Replay 5 mnt", size=6.4, color="#FFFFFF", ha="center",
        weight="bold", z=7)

    # timeline ringkas
    box(ax, 0.022, 0.030, 0.956, 0.068, fc=PANEL, r=0.016, z=3)
    txt(ax, 0.044, 0.080, "30 MENIT", size=5.4, color=TXT2, weight="bold", z=6)
    ax.plot([0.150, 0.950], [0.064, 0.064], transform=ax.transAxes, color=STROKE, lw=5,
            solid_capstyle="round", zorder=5)
    np.random.seed(11); x = 0.150
    while x < 0.948:
        w = np.random.uniform(0.010, 0.040)
        ax.plot([x, min(x + w, 0.950)], [0.064, 0.064], transform=ax.transAxes,
                color=OK if np.random.rand() < 0.33 else WARN, lw=5, zorder=6,
                solid_capstyle="butt", alpha=.85)
        x += w
    ax.plot([0.700, 0.700], [0.048, 0.080], transform=ax.transAxes, color=ACCENT, lw=1.6, zorder=7)
    txt(ax, 0.700, 0.040, "geofence", size=5.0, color=ACCENT, ha="center", z=8)
    txt(ax, 0.044, 0.044, "10:12", size=5.0, color=TXT2, z=8)
    txt(ax, 0.944, 0.044, "10:42", size=5.0, color=TXT2, ha="right", z=8)

    fig.savefig(path, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    panel_desktop(os.path.join(OUT, "wireframe_desktop.png"))
    panel_mobile(os.path.join(OUT, "wireframe_mobile.png"))
    print("wireframe dibuat:", sorted(os.listdir(OUT)))
