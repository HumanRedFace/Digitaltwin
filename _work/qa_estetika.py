#!/usr/bin/env python3
"""QA estetika terukur (pengganti sementara vision): keseimbangan ruang putih,
kepadatan tinta, dan berat visual kiri-kanan per halaman.

Tidak menilai rasa, tetapi menangkap cacat yang biasanya baru terlihat mata:
halaman yang terlalu kosong, halaman yang terlalu padat, dan halaman yang
bobotnya berat sebelah (mis. gambar menumpuk di kiri, teks kosong di kanan).
"""
import sys
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"
DPI = 96
PH = 841.89
FOOT = PH - 55

doc = fitz.open(PDF)
print(f"PDF : {PDF}\nhal : {doc.page_count}\n")
print("hal  tinta%  ruang-kosong%  berat-kiri%  catatan")

rows = []
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY)
    w, h = pix.width, pix.height
    buf = pix.samples
    total = w * h
    gelap = 0
    kiri = 0
    kanan = 0
    for y in range(h):
        row = buf[y * w:(y + 1) * w]
        for x in range(w):
            if row[x] < 200:          # piksel bertinta
                gelap += 1
                if x < w // 2:
                    kiri += 1
                else:
                    kanan += 1
    tinta = 100.0 * gelap / total
    berat_kiri = 100.0 * kiri / gelap if gelap else 0.0
    cat = []
    if tinta < 1.5:
        cat.append("SANGAT KOSONG")
    elif tinta < 3.0:
        cat.append("kosong")
    if tinta > 18:
        cat.append("SANGAT PADAT")
    if gelap > 5000 and (berat_kiri < 32 or berat_kiri > 68):
        cat.append("berat sebelah")
    print(f"{i:>3}  {tinta:5.2f}  {100-tinta:12.2f}  {berat_kiri:10.1f}  {' '.join(cat)}")
    rows.append((i, tinta, berat_kiri, cat))

print()
kosong = [r for r in rows if r[1] < 3.0]
padat = [r for r in rows if r[1] > 18]
sebelah = [r for r in rows if "berat sebelah" in r[3]]
print(f"Halaman terlalu kosong (<3% tinta) : {len(kosong)}  {[r[0] for r in kosong]}")
print(f"Halaman terlalu padat  (>18% tinta): {len(padat)}  {[r[0] for r in padat]}")
print(f"Halaman berat sebelah             : {len(sebelah)}  {[r[0] for r in sebelah]}")
rata = sum(r[1] for r in rows) / len(rows)
print(f"Rata-rata kepadatan tinta         : {rata:.2f}%  (khas 6-12% untuk laporan padat teks)")
doc.close()
