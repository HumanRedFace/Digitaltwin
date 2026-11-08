#!/usr/bin/env python3
"""QA struktur: header tabel yatim, keterangan jauh dari objeknya,
tabel terbelah tanpa header ulang, dan konsistensi tepi kiri teks.

Melengkapi qa_pdf.py (luapan margin) dan qa_paginasi.py (keterisian halaman).
Yang diperiksa di sini adalah relasi antara elemen dan keterangannya.
"""
import re
import sys
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"
PH = 841.89
FOOT = PH - 55
CAP = re.compile(r"^(Gambar|Tabel)\s+([0-9A-E][\w-]*)\.\s")

doc = fitz.open(PDF)
print(f"PDF : {PDF}\nhal : {doc.page_count}\n")

issues = []

# ── 1. keterangan gambar/tabel: jarak ke objek terdekat ────────────────────
print("JARAK KETERANGAN KE OBJEKNYA")
for i, page in enumerate(doc, start=1):
    caps = []
    for b in page.get_text("blocks"):
        if b[6] != 0:
            continue
        t = b[4].strip()
        if CAP.match(t):
            caps.append((fitz.Rect(b[:4]), t[:52]))
    if not caps:
        continue

    imgs = [r for im in page.get_images(full=True) for r in page.get_image_rects(im[0])]
    # garis tabel: gambar vektor yang membentang horizontal
    tbls = [d["rect"] for d in page.get_drawings() if d["rect"].width > 380]

    for cr, ctxt in caps:
        best, kind = 1e9, "-"
        for r in imgs:
            gap = min(abs(cr.y0 - r.y1), abs(r.y0 - cr.y1))
            if gap < best:
                best, kind = gap, "gambar"
        for r in tbls:
            gap = min(abs(cr.y0 - r.y1), abs(r.y0 - cr.y1))
            if gap < best:
                best, kind = gap, "tabel"
        flag = ""
        if best > 24:
            flag = "  <<< JAUH / TIDAK ADA PASANGAN"
            issues.append((i, "keterangan jauh dari objek", f"{ctxt} ({kind} {best:.0f}pt)"))
        print(f"   hal {i:>2}  {kind:<7} {best:6.1f} pt  {ctxt}{flag}")

# ── 2. tepi kiri teks: konsistensi kolom ──────────────────────────────────
# Toleransi 1 pt: pembulatan twip LibreOffice menghasilkan 68,2 / 68,3 / 68,6
# untuk paragraf yang sama rata kirinya. Itu bukan cacat.
# Hanya blok yang LEBAR (paragraf badan, > 200 pt) yang diukur — sel tabel juga
# punya tepi kiri sendiri (118, 301, 443 pt) dan bukan cacat kolom.
TEPI_NOMINAL = 68.03
TEPI_TOL = 1.0
LEBAR_MIN = 450.0     # paragraf badan = 461,6 pt; blok tabel <= 448,4 pt
print(f"\n\nTEPI KIRI PARAGRAF BADAN (nominal {TEPI_NOMINAL:.2f} pt, toleransi {TEPI_TOL} pt)")


def dalam_kotak(page, blok_rect):
    """True bila blok berada di dalam kotak berwarna (tabel/callout/code block).

    Teks di dalam sel punya tepi kiri sendiri karena margin sel (74,7 / 72,2 pt),
    jadi tidak boleh diukur sebagai tepi kolom badan.
    """
    cx, cy = (blok_rect.x0 + blok_rect.x1) / 2, (blok_rect.y0 + blok_rect.y1) / 2
    for d in page.get_drawings():
        if not (d.get("fill") or d.get("color")):
            continue
        r = d["rect"]
        if r.x0 - 1 <= cx <= r.x1 + 1 and r.y0 - 1 <= cy <= r.y1 + 1 and r.width > 40:
            return True
    return False


COL_R = 595.28 - 68.03        # tepi kanan kolom teks = 527,25 pt
for i, page in enumerate(doc, start=1):
    xs = {}
    for b in page.get_text("blocks"):
        if b[6] != 0 or not b[4].strip():
            continue
        if b[1] > FOOT:
            continue
        r = fitz.Rect(b[:4])
        # Hanya paragraf yang MENGISI kolom penuh. Keterangan gambar (tengah),
        # sel tabel (lebar 450 pt) dan teks callout punya tepi sendiri dan bukan
        # cacat kolom — mencampurnya menghasilkan puluhan positif palsu.
        if r.width < 458 or abs(r.x1 - COL_R) > 2.0:
            continue
        x = round(r.x0, 1)
        xs[x] = xs.get(x, 0) + 1
    aneh = {x: n for x, n in xs.items() if abs(x - TEPI_NOMINAL) > TEPI_TOL}
    if aneh:
        issues.append((i, "tepi kiri menyimpang", str(aneh)))
        print(f"   hal {i:>2}  {aneh}")
print("   (kosong = konsisten)")

# ── 3. tabel terbelah antar halaman: header harus berulang ────────────────
print("\n\nTABEL TERBELAH ANTAR HALAMAN")
for i in range(1, doc.page_count):
    a, b = doc[i - 1], doc[i]
    ga = [d["rect"] for d in a.get_drawings() if d["rect"].width > 380]
    gb = [d["rect"] for d in b.get_drawings() if d["rect"].width > 380]
    if not ga or not gb:
        continue
    bawah = max(r.y1 for r in ga)
    atas = min(r.y0 for r in gb)
    tb = b.get_text("text").splitlines()
    head = " / ".join(t.strip() for t in tb[2:4] if t.strip())[:70]
    # Terbelah = garis tabel mencapai dasar halaman A DAN berlanjut di puncak B.
    # Tabel daftar isi (hal 5->6) selalu "terbelah" menurut definisi ini tetapi
    # itu bukan tabel data — dikecualikan. Header berulang diverifikasi terpisah
    # dengan membandingkan baris pertama kedua halaman.
    if bawah > FOOT - 26 and atas < 110:
        if "DAFTAR ISI" in a.get_text("text") or "DAFTAR ISI" in b.get_text("text"):
            continue
        # apakah header benar-benar berulang?
        hdr_a = [l.strip() for l in a.get_text("text").splitlines() if l.strip()]
        hdr_b = [l.strip() for l in tb if l.strip()]
        ulang = any(x in hdr_b[:4] for x in hdr_a if len(x) > 12)
        status = "header berulang OK" if ulang else "HEADER TIDAK BERULANG"
        print(f"   hal {i:>2}->{i+1}: {status}  | puncak hal {i+1} = {head!r}")
        if not ulang:
            issues.append((i, "tabel terbelah tanpa header ulang", head))
if not any("terbelah" in x[1] for x in issues):
    print("   tidak ada")

print(f"\n\nTOTAL TEMUAN STRUKTUR: {len(issues)}")
for x in issues:
    print(f"   hal {x[0]:>2}  {x[1]:<32} {x[2]}")
doc.close()
