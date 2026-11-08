#!/usr/bin/env python3
"""QA paginasi: keterisian halaman, baris yatim/piatu, judul menggantung,
gambar terpisah dari keterangannya, tabel terpotong antar halaman.

Tujuan: temukan halaman yang "berakhir dini" (isi berhenti jauh di atas dasar
kolom) dan elemen yang terbelah di batas halaman — dua cacat yang tidak
terdeteksi oleh qa_pdf.py (yang hanya memeriksa luapan ke margin).
"""
import re
import sys
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"

PH = 841.89
TOP, BOT = 56.7, PH - 68.03        # batas kolom teks
FOOT = PH - 55

doc = fitz.open(PDF)
hal = []

print(f"PDF : {PDF}\nhal : {doc.page_count}\n")

print("KETERISIAN PER HALAMAN")
print("hal  isi-sampai  terpakai  kata  catatan")
for i, page in enumerate(doc, start=1):
    ws = [w for w in page.get_text("words") if w[1] < FOOT and w[4].strip()]
    if not ws:
        print(f"{i:>3}  {'-':>9}  {'-':>8}  {0:>4}  KOSONG")
        continue
    bot = max(w[3] for w in ws)
    pakai = 100 * (bot - TOP) / (BOT - TOP)
    cat = ""
    if pakai < 55:
        cat = "<<< BERAKHIR DINI"
    elif pakai < 68:
        cat = "< agak pendek"
    print(f"{i:>3}  {bot:9.1f}  {pakai:7.1f}%  {len(ws):>4}  {cat}")
    hal.append((i, pakai, bot))

print("\n\nBARIS YATIM/PIATU DAN JUDUL MENGGANTUNG")

# kumpulkan baris per halaman
lines_by_page = {}
for i, page in enumerate(doc, start=1):
    d = page.get_text("dict")
    out = []
    for blk in d["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk["lines"]:
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if not txt:
                continue
            size = max(s["size"] for s in ln["spans"])
            bold = any("Bold" in s["font"] for s in ln["spans"])
            out.append((fitz.Rect(ln["bbox"]), txt, size, bold))
    lines_by_page[i] = sorted(out, key=lambda r: r[0].y0)

JUDUL = re.compile(r"^(\d+(\.\d+)*|[A-E](\.\d+)*)\s+[A-Z]")

problems = []
for i in range(1, doc.page_count + 1):
    cur = [l for l in lines_by_page.get(i, []) if l[0].y1 < FOOT]
    nxt = [l for l in lines_by_page.get(i + 1, []) if l[0].y1 < FOOT]
    if not cur or not nxt:
        continue

    # 1. judul di baris terakhir halaman (isinya di halaman berikut)
    last = cur[-1]
    if last[2] >= 11.5 and last[3] and JUDUL.match(last[1]):
        problems.append((i, "JUDUL MENGGANTUNG", last[1][:58]))

    # 2. baris piatu: satu baris terakhir paragraf sendirian di atas halaman baru
    #    deteksi: baris pertama halaman baru, lalu celah vertikal besar sesudahnya
    if len(nxt) >= 2:
        gap = nxt[1][0].y0 - nxt[0][0].y1
        if gap > 12 and nxt[0][0].y1 < TOP + 20:
            problems.append((i + 1, "BARIS PIATU", nxt[0][1][:58]))

    # 3. keterangan gambar/tabel terpisah dari objeknya.
    #    Keterangan di baris pertama halaman BUKAN cacat bila objeknya juga ada di
    #    halaman itu (gambar/tabel menempel puncak halaman). Hanya laporkan bila
    #    tidak ada objek apa pun di halaman tersebut.
    #    CATATAN: harus memakai doc[i-1], bukan 'page' — 'page' di sini masih
    #    merujuk halaman terakhir dari loop pertama.
    hal_ini = doc[i - 1]
    ada_gambar = any(True for im in hal_ini.get_images(full=True)
                     for _ in hal_ini.get_image_rects(im[0]))
    ada_garis = any(d["rect"].width > 380 for d in hal_ini.get_drawings())
    for j, l in enumerate(cur):
        if re.match(r"^(Gambar|Tabel)\s+\d+\.", l[1]) and j == 0:
            if ada_gambar or ada_garis:
                continue        # objeknya ada di halaman ini juga — wajar
            problems.append((i, "KETERANGAN DI PUNCAK HALAMAN", l[1][:58]))

seen = set()
uniq = []
for p in problems:
    k = (p[0], p[1])
    if k in seen:
        continue
    seen.add(k)
    uniq.append(p)

for p in uniq:
    print(f"   hal {p[0]:>2}  {p[1]:<32} | {p[2]}")
print(f"\ntotal temuan: {len(uniq)}")

# ringkasan: berapa halaman yang bisa dihemat bila isi dipadatkan
hemat = sum(1 for h in hal if h[1] < 55)
print(f"\nHalaman terpakai < 55%: {hemat}  — kandidat pemadatan")
print(f"Halaman total: {doc.page_count}")
doc.close()
