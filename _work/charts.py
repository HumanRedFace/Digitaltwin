"""Grafik untuk laporan Digital Twin 3D View. Semua angka dari data.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import data as D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.titlesize": 10.5, "axes.titleweight": "bold",
    "axes.labelsize": 9, "axes.edgecolor": "#444444",
    "axes.linewidth": 0.8, "figure.dpi": 200,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.12,
})
NAVY = "#16324F"; ACC = "#E11B22"; GREY = "#8A96A3"; BLUE = "#2E6E9E"
GREEN = "#2E7D4F"; AMBER = "#C8892A"


def n1(x, d=1):
    q = Decimal(1).scaleb(-d)
    v = Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)
    return f"{v:.{d}f}".replace(".", ",")


# ── 1. Benchmark: draw call & fps ────────────────────────────────────────────
def chart_benchmark():
    labels = [b[0] for b in D.BENCH]
    ms = [b[4] for b in D.BENCH]
    calls = [b[1] for b in D.BENCH]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.3),
                                   gridspec_kw={"width_ratios": [1.45, 1]})
    y = np.arange(len(labels))[::-1]
    colors = [ACC if c > 1000 else (AMBER if m > 33.3 else GREEN) for c, m in zip(calls, ms)]
    ax1.barh(y, ms, color=colors, height=.62, edgecolor="white", linewidth=.7)
    for yy, m, f in zip(y, ms, [b[5] for b in D.BENCH]):
        ax1.text(m + 2.0, yy, f"{n1(m,2)} ms  ({n1(f,1)} fps)", va="center", fontsize=7.6, color="#333")
    ax1.set_yticks(y); ax1.set_yticklabels(labels, fontsize=7.4)
    ax1.set_xlabel("Waktu per frame (ms) — makin kecil makin baik")
    ax1.set_title("Waktu render per frame (Apple M1, 1920×1080)")
    ax1.axvline(33.3, color=ACC, ls="--", lw=.9)
    ax1.text(33.3, len(labels) - .35, " 33,3 ms = 30 fps", color=ACC, fontsize=7, va="top")
    ax1.set_xlim(0, 145)
    ax1.grid(axis="x", alpha=.25, lw=.5); ax1.set_axisbelow(True)

    ax2.scatter(calls, ms, s=52, c="#1f4e79", edgecolor="white", zorder=3)
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel("Jumlah draw call (log)"); ax2.set_ylabel("ms/frame (log)")
    ax2.set_title("Draw call adalah penentu utama")
    for c, m, l in zip(calls, ms, labels):
        tag = l.split(".")[0]
        ax2.annotate(tag, (c, m), textcoords="offset points", xytext=(6, -3), fontsize=7)
    ax2.grid(alpha=.25, lw=.5); ax2.set_axisbelow(True)
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{OUT}/g1_benchmark.png"); plt.close(fig)


# ── 2. Kurva biaya draw call ────────────────────────────────────────────────
def chart_drawcall():
    objs = [1, 10, 100, 500, 1000, 2000, 4000, 8000, 14000]
    # diukur pada sweep terpisah (Lihat Lampiran C)
    ms = [0.35, 5.82, 46.31, 5.25, 1.59, 1.18, 2.45, 5.61, 10.47]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(objs, ms, "o-", color=BLUE, lw=1.6, ms=5.5, zorder=3)
    ax.axhline(33.3, color=ACC, ls="--", lw=.9)
    ax.text(1.2, 35, "batas 30 fps", color=ACC, fontsize=7.4)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Jumlah objek terpisah (draw call)"); ax.set_ylabel("ms per frame")
    ax.set_title("Biaya draw call pada three.js 0.187 (geometri 12 tri/objek)")
    ax.grid(alpha=.25, lw=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.annotate("14.003 objek\n(mirip aset dump truck)", (14000, 10.47),
                textcoords="offset points", xytext=(-92, 22), fontsize=7.2, color="#333",
                arrowprops=dict(arrowstyle="->", lw=.8, color="#666"))
    fig.tight_layout(); fig.savefig(f"{OUT}/g2_drawcall.png"); plt.close(fig)


# ── 3. Skor teknologi ───────────────────────────────────────────────────────
def chart_skor():
    names = list(D.SKOR)
    kri = [k[0] for k in D.KRITERIA]
    w = [k[1] for k in D.KRITERIA]
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    short = ["Geospasial", "Kinerja", "Talenta", "Lisensi", "Real-time",
             "Point cloud", "Hardware", "Ekosistem"]
    x = np.arange(len(kri)); bw = 0.15
    cols = [BLUE, GREEN, ACC, AMBER, GREY]
    for i, (nm, col) in enumerate(zip(names, cols)):
        ax.bar(x + (i - 2) * bw, D.SKOR[nm], bw * .92, label=nm, color=col, edgecolor="white", lw=.5)
    ax.set_xticks(x); ax.set_xticklabels(short, fontsize=7.6, rotation=18, ha="right")
    ax.set_ylabel("Skor (1–5)"); ax.set_ylim(0, 5.6)
    ax.legend(ncol=5, fontsize=7.6, frameon=False, loc="upper center", bbox_to_anchor=(.5, 1.11))
    ax.set_title("Skor per kriteria (bobot: " + ", ".join(f"{n1(v*100,0)}%" for v in w) + ")", pad=22)
    ax.grid(axis="y", alpha=.22, lw=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/g3_skor.png"); plt.close(fig)


# ── 4. Skor total terbobot ──────────────────────────────────────────────────
def chart_total():
    tot = {k: sum(s * w for s, (_, w, _) in zip(v, D.KRITERIA)) for k, v in D.SKOR.items()}
    items = sorted(tot.items(), key=lambda kv: kv[1])
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    y = np.arange(len(items))
    ax.barh(y, [v for _, v in items], color=[BLUE if k != "CesiumJS" else GREEN for k, _ in items],
            height=.55, edgecolor="white")
    for yy, (k, v) in zip(y, items):
        ax.text(v + .04, yy, n1(v, 2), va="center", fontsize=8)
    ax.set_yticks(y); ax.set_yticklabels([k for k, _ in items], fontsize=8.4)
    ax.set_xlim(0, 4.7); ax.set_xlabel("Skor terbobot (maksimum 5,00)")
    ax.set_title("Peringkat teknologi visualisasi 3D")
    ax.grid(axis="x", alpha=.22, lw=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/g4_total.png"); plt.close(fig)


# ── 5. Matriks risiko ───────────────────────────────────────────────────────
def chart_risiko():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for i in range(1, 4):
        for j in range(1, 4):
            sk = i * j
            c = "#F4D7D7" if sk >= 9 else ("#FAE8C8" if sk >= 4 else "#DCEFE2")
            ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, color=c, ec="white", lw=2))
    for rid, _, dam, kem, sk, _ in D.RISIKO:
        jj = {"Rendah": 1, "Sedang": 2, "Tinggi": 3}[kem]
        ii = {"Rendah": 1, "Sedang": 2, "Tinggi": 3}[dam]
        ax.text(jj, ii, rid, ha="center", va="center", fontsize=7.8, fontweight="bold", color=NAVY)
    ax.set_xlim(.5, 3.5); ax.set_ylim(.5, 3.5)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(["Rendah", "Sedang", "Tinggi"])
    ax.set_yticks([1, 2, 3]); ax.set_yticklabels(["Rendah", "Sedang", "Tinggi"])
    ax.set_xlabel("Kemungkinan"); ax.set_ylabel("Dampak")
    ax.set_title("Peta risiko (skor = dampak × kemungkinan)")
    fig.tight_layout(); fig.savefig(f"{OUT}/g5_risiko.png"); plt.close(fig)


# ── 6. Kesiapan data per use case ───────────────────────────────────────────
def chart_usecase():
    uc = D.USE_CASE
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    val = {"Rendah": 1, "Sedang": 2, "Tinggi": 3}
    def lvl(s):
        s = s.upper()
        for k in ("RENDAH", "SEDANG", "TINGGI"):
            if s.startswith(k):
                return val[k.capitalize()]
        return 2
    x = np.arange(len(uc)); bw = .36
    ax.bar(x - bw / 2, [lvl(u[4]) for u in uc], bw, label="Kesiapan data", color=GREEN, edgecolor="white")
    ax.bar(x + bw / 2, [lvl(u[5]) for u in uc], bw, label="Kompleksitas", color=AMBER, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{u[0]}\n{u[1][:26]}…" for u in uc], fontsize=7)
    ax.set_yticks([1, 2, 3]); ax.set_yticklabels(["Rendah", "Sedang", "Tinggi"])
    ax.legend(ncol=2, fontsize=8, frameon=False, loc="upper right")
    ax.set_title("Kesiapan data vs kompleksitas per use case")
    ax.grid(axis="y", alpha=.22, lw=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/g6_usecase.png"); plt.close(fig)


# ── 7. Effort per fase ──────────────────────────────────────────────────────
def chart_effort():
    f = D.EFFORT
    labels = [x[0].split("—")[0].strip() for x in f]
    lo = [x[1] for x in f]; hi = [x[2] for x in f]
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    y = np.arange(len(f))[::-1]
    ax.barh(y, [h - l for l, h in zip(lo, hi)], left=lo, height=.52, color="#BBD3E8", edgecolor=BLUE, lw=.8)
    ax.scatter(lo, y, color=BLUE, s=22, zorder=3)
    ax.scatter(hi, y, color=NAVY, s=22, zorder=3)
    for yy, l, h in zip(y, lo, hi):
        ax.text(h + 6, yy, f"{l}–{h} jam", va="center", fontsize=7.6)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Jam-orang (estimasi awal, bukan komitmen)")
    ax.set_title("Rentang effort per fase")
    ax.set_xlim(0, 420)
    ax.grid(axis="x", alpha=.22, lw=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/g7_effort.png"); plt.close(fig)


# ── 8. Latensi & laju data ──────────────────────────────────────────────────
def chart_latensi():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.3))

    komp = ["Sensor\n(GNSS)", "Gateway\n→ broker", "Backend\n→ WS", "Render\n(frame)"]
    lat = [1000 / 1, 250, 80, 33.3]   # GNSS 1 Hz = periode 1000 ms
    ax1.bar(komp, lat, color=[ACC, AMBER, BLUE, GREEN], edgecolor="white", width=.6)
    for i, v in enumerate(lat):
        ax1.text(i, v + 25, f"{n1(v,1)} ms", ha="center", fontsize=7.6)
    ax1.set_ylabel("Kontribusi latensi (ms)")
    ax1.set_title("Anggaran latensi per tahap")
    ax1.set_ylim(0, 1250)
    ax1.grid(axis="y", alpha=.22, lw=.5); ax1.set_axisbelow(True)

    # data rate skala armada
    unit = np.array([10, 25, 50, 100, 200])
    rate = unit * 10 * 320 / 1024    # 10 Hz x 320 byte JSON
    ax2.plot(unit, rate, "o-", color=BLUE, lw=1.6, ms=5)
    ax2.set_xlabel("Jumlah unit terpantau"); ax2.set_ylabel("Laju data (KB/s)")
    ax2.set_title("Beban ingestion (10 Hz, 320 B/pesan)")
    ax2.grid(alpha=.25, lw=.5); ax2.set_axisbelow(True)
    for u, r in zip(unit, rate):
        ax2.annotate(f"{n1(r,0)}", (u, r), textcoords="offset points", xytext=(0, 7),
                     ha="center", fontsize=7.2)
    for ax in (ax1, ax2):
        for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/g8_latensi.png"); plt.close(fig)


if __name__ == "__main__":
    chart_benchmark(); chart_drawcall(); chart_skor(); chart_total()
    chart_risiko(); chart_usecase(); chart_effort(); chart_latensi()
    print("selesai:", sorted(os.listdir(OUT)))
