#!/usr/bin/env python3
"""QA tambahan: kata saling menimpa, teks menimpa gambar, halaman berakhir dini.

Ukur per KATA, bukan per blok. bbox blok menyertakan spasi di ujung baris yang
direntangkan justify, sehingga dua sel tabel bersebelahan selalu tampak
beririsan padahal tidak. bbox kata ketat, jadi irisan di level kata = tabrakan
cetak yang nyata.
"""
import sys
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"

PW, PH = 595.28, 841.89
M_BOT = 68.03
MIN_AREA = 6.0        # pt^2 — di bawah ini masih sentuhan antar-glyph normal
FOOT_TOP = PH - 55


def area(a, b):
    x0 = max(a.x0, b.x0)
    y0 = max(a.y0, b.y0)
    x1 = min(a.x1, b.x1)
    y1 = min(a.y1, b.y1)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    return (x1 - x0) * (y1 - y0)


doc = fitz.open(PDF)
print(f"PDF : {PDF}\nhal : {doc.page_count}\n")

clashes = []
on_img = []
early = []

for i, page in enumerate(doc, start=1):
    words = [w for w in page.get_text("words") if w[1] < FOOT_TOP and w[4].strip()]
    rects = [(fitz.Rect(w[:4]), w[4], w[5]) for w in words]

    for a in range(len(rects)):
        ra, wa, ba = rects[a]
        for b in range(a + 1, len(rects)):
            rb, wb, bb = rects[b]
            if ba == bb:
                continue                       # kata dalam sel/blok yang sama
            if rb.y0 > ra.y1 or ra.y0 > rb.y1:
                continue                       # cepat: tidak sebaris
            ar = area(ra, rb)
            if ar > MIN_AREA:
                clashes.append((i, round(ar, 1), wa, wb))

    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            for rect, w, _blk in rects:
                if area(rect, r) > MIN_AREA:
                    on_img.append((i, w, round(r.y0, 1), round(r.y1, 1)))

    if rects:
        bottom = max(r.y1 for r, _w, _b in rects)
        ruang = (PH - M_BOT) - bottom
        if ruang > 150:
            early.append((i, round(ruang, 1)))

print(f"KATA SALING MENIMPA   : {len(clashes)}")
for c in clashes[:20]:
    print(f"   hal {c[0]:>2}  {c[1]:>6} pt2  {c[2]!r} <> {c[3]!r}")

print(f"\nKATA DI ATAS GAMBAR   : {len(on_img)}")
for o in on_img[:12]:
    print(f"   hal {o[0]:>2}  {o[1]!r}  gambar y[{o[2]},{o[3]}]")

# Catatan: pengukuran "halaman berakhir dini" sengaja TIDAK diulang di sini.
# Tugas itu milik qa_paginasi.py, yang mengukur keterisian kolom dan menghitungnya
# relatif terhadap tinggi kolom teks. Versi lama skrip ini mencetak jumlah pt ruang
# kosong tanpa konteks (mis. hal 1 sampul memang pendek) sehingga terbaca sebagai
# 19 cacat padahal bukan — itu menyesatkan.
print(f"\nHalaman: {doc.page_count}   (untuk keterisian halaman lihat qa_paginasi.py)")
doc.close()
