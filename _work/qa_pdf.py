#!/usr/bin/env python3
"""QA layout PDF: halaman kosong, isi terpotong, gambar keluar kolom, header/footer terpisah."""
import sys, os
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"

PW, PH = 595.28, 841.89
M = 68.03
COL_R = PW - M          # 527.25 tepi kanan kolom teks
FOOT_TOP = PH - 55      # blok di bawah ini = footer (memang di margin)
TOL = 4.0               # toleransi pembulatan twip LibreOffice

doc = fitz.open(PDF)
print(f"PDF : {os.path.basename(PDF)}")
print(f"hal : {doc.page_count}   ukuran {doc[0].rect.width:.1f} x {doc[0].rect.height:.1f} pt")
print(f"kolom teks: x {M:.1f} .. {COL_R:.1f} pt (lebar {COL_R-M:.1f} pt)\n")

blank, clipped, imgs_bad = [], [], []
chars = []
footer_hits = 0

for i, page in enumerate(doc, start=1):
    txt = page.get_text("text")
    n = len(txt.strip())
    chars.append(n)
    if n < 40 and not page.get_images():
        blank.append(i)

    # ukur per KATA, bukan per blok: bbox blok menyertakan spasi di ujung baris
    # yang direntangkan oleh perataan justify — itu artefak ukur, bukan luapan nyata.
    for w in page.get_text("words"):
        x0, y0, x1, y1, word = w[0], w[1], w[2], w[3], w[4]
        if y0 > FOOT_TOP:
            footer_hits += 1 if word else 0
            continue
        if x1 > COL_R + TOL or x0 < M - TOL or y1 > PH - M + TOL:
            clipped.append((i, round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1), word[:46]))

    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if r.x1 > COL_R + TOL or r.x0 < M - TOL:
                imgs_bad.append((i, round(r.x0, 1), round(r.x1, 1),
                                 round(r.y0, 1), round(r.y1, 1)))

print(f"HALAMAN KOSONG      : {blank if blank else 'TIDAK ADA  (lulus)'}")
print(f"TEKS TERPOTONG      : {len(clipped)}")
for c in clipped[:12]:
    print(f"   hal {c[0]}: x[{c[1]},{c[2]}] y[{c[3]},{c[4]}] | {c[5]}")
print(f"GAMBAR KELUAR KOLOM : {len(imgs_bad)}")
for c in imgs_bad[:12]:
    print(f"   hal {c[0]}: x[{c[1]},{c[2]}] lebar {c[2]-c[1]:.1f} pt "
          f"(maks {COL_R-M:.1f}) y[{c[3]},{c[4]}]")
print(f"\nblok footer terdeteksi: {footer_hits}  (normal: 1 per halaman)")

miskin = sorted(range(len(chars)), key=lambda k: chars[k])[:5]
print("\nHALAMAN TEKS TERSEDIKIT:")
for k in miskin:
    print(f"   hal {k+1}: {chars[k]} karakter")

# cek daftar isi: apakah nomor halaman di TOC masuk akal (monoton naik)
# CATATAN: versi lama membaca SEMUA baris berakhir angka — termasuk baris footer
# "MNG-RND-DT-2026-001 rev A | 7 / 52", sehingga yang terukur nomor footer, bukan
# entri TOC, dan metrik monoton jadi tak bermakna. Sekarang: hanya blok di dalam
# kolom teks (di atas footer) dan hanya entri yang berakhir angka 1..page_count.
toc_hal = []
for i, page in enumerate(doc, start=1):
    if i > 12:
        break
    entri = 0
    for b in page.get_text("blocks"):
        if b[6] != 0 or b[1] > FOOT_TOP:      # lewati gambar & baris footer
            continue
        baris = [s.strip() for s in b[4].strip().splitlines() if s.strip()]
        if len(baris) < 2:
            continue
        akhir = baris[-1]
        if akhir.isdigit():
            v = int(akhir)
            if 1 <= v <= doc.page_count and len(baris[0]) > 4:
                toc_hal.append(v)
                entri += 1
    if entri:
        print(f"   TOC hal {i}: {entri} entri", end="")
print()
if len(toc_hal) > 5:
    naik = sum(1 for a, b in zip(toc_hal, toc_hal[1:]) if b >= a)
    print(f"\nTOC: {len(toc_hal)} entri nomor halaman, {naik}/{len(toc_hal)-1} monoton naik")
    print(f"     rentang: {min(toc_hal)} .. {max(toc_hal)}   (total PDF {doc.page_count})")
    turun = [(a, b) for a, b in zip(toc_hal, toc_hal[1:]) if b < a]
    if turun:
        print(f"     TURUN di {len(turun)} titik (normal: pindah antar bab): {turun[:6]}")

doc.close()
