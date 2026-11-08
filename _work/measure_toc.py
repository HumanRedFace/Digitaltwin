#!/usr/bin/env python3
"""
Ukur nomor halaman nyata dari PDF hasil ekspor, untuk mengisi Daftar Isi.
Dicocokkan berdasarkan judul bab/sub-bab yang benar-benar muncul di halaman.
"""
import sys, os, json, re
import fitz

PDF = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/toc_pages.json"

doc = fitz.open(PDF)

# kumpulkan (halaman -> daftar judul) untuk pencocokan.
# PENTING: hanya baris yang benar-benar berformat JUDUL yang boleh dianggap judul
# (tebal, >= 11,5 pt). Tanpa filter ini, kalimat badan seperti "Lampiran C (88 fps,
# 3 draw call) ..." di hal 32 dan sel tabel "Lampiran E" di hal 9 akan menang atas
# judul sebenarnya, dan Daftar Isi menunjuk halaman yang salah.
SIZE_JUDUL = 11.5


def judul_di_halaman(page):
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for ln in blk["lines"]:
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            teks = "".join(s["text"] for s in spans).strip()
            if not teks or teks.startswith("MNG-RND-DT-2026-001"):
                continue
            size = max(s["size"] for s in spans)
            tebal = any("Bold" in s["font"] for s in spans)
            if tebal and size >= SIZE_JUDUL:
                out.append(teks)
    return out


halaman = [(i, judul_di_halaman(page)) for i, page in enumerate(doc, start=1)]

print(f"PDF {doc.page_count} halaman\n")

# judul yang dicari: diambil dari struktur laporan (harus sama persis dengan heading)
JUDUL = [
    ("DOKUMEN KONTROL", 1),
    ("RINGKASAN EKSEKUTIF", 1),
    ("DAFTAR ISI", 1),
    ("1  PENDAHULUAN, LINGKUP, DAN CARA KERJA", 1),
    ("1.1  Latar belakang", 2),
    ("1.2  Tujuan riset", 2),
    ("1.3  Pengguna yang dituju", 2),
    ("1.4  Lingkup dan batas tegas", 2),
    ("1.5  Metode kerja", 2),
    ("1.6  Tingkat bukti dan kejujuran angka", 2),
    ("2  IDENTIFIKASI KEBUTUHAN DAN USE CASE", 1),
    ("2.1  Cara saya menyaring use case", 2),
    ("2.2  Use case A", 2),
    ("2.3  Use case B", 2),
    ("2.4  Perbandingan kesiapan dua use case", 2),
    ("2.5  Daftar use case dan prioritas", 2),
    ("2.6  Real-time, replay, dan simulasi", 2),
    ("2.7  Kandidat fitur minimum", 2),
    ("3  RISET TEKNOLOGI VISUALISASI 3D", 1),
    ("3.1  Cara saya memilih kandidat", 2),
    ("3.2  Status lisensi", 2),
    ("3.3  Format aset dan model 3D", 2),
    ("3.4  Perbandingan arsitektur", 2),
    ("3.5  Kebutuhan hardware klien", 2),
    ("3.6  Matriks keputusan berbobot", 2),
    ("3.7  Membaca hasil", 2),
    ("3.8  Teknologi pendukung", 2),
    ("4  PENGUKURAN KINERJA RENDER", 1),
    ("4.1  Mengapa saya mengukur sendiri", 2),
    ("4.2  Temuan utama", 2),
    ("4.3  Uji instancing", 2),
    ("4.4  Scene target", 2),
    ("4.5  Pelajaran yang mengubah prioritas", 2),
    ("5  KEBUTUHAN DATA DAN METODE INTEGRASI", 1),
    ("5.1  Skema kanonik", 2),
    ("5.2  Sistem koordinat", 2),
    ("5.3  Data yang sudah ada", 2),
    ("5.4  Kualitas data lapangan", 2),
    ("5.5  Sinkronisasi waktu", 2),
    ("5.6  Integrasi radar", 2),
    ("5.7  Kontrak data yang harus diminta", 2),
    ("6  ARSITEKTUR YANG DIUSULKAN", 1),
    ("6.1  Prinsip perancangan", 2),
    ("6.2  Diagram arsitektur", 2),
    ("6.3  Penjelasan setiap lapis", 2),
    ("6.4  Tiga jalur data", 2),
    ("6.5  Di mana komponen diletakkan", 2),
    ("6.6  Yang sengaja tidak saya masukkan", 2),
    ("7  KONSEP TAMPILAN", 1),
    ("7.1  Dasar perancangan", 2),
    ("7.2  Layar desktop", 2),
    ("7.3  Layar tablet", 2),
    ("7.4  Hierarki informasi", 2),
    ("7.5  Elemen yang sengaja tidak digambar", 2),
    ("8  ANALISIS KELAYAKAN DAN RISIKO", 1),
    ("8.1  Kerangka penilaian", 2),
    ("8.2  Apa yang layak dikerjakan sekarang", 2),
    ("8.3  Apa yang belum layak", 2),
    ("8.4  Risiko", 2),
    ("8.5  Dua risiko yang paling menentukan", 2),
    ("8.6  Gap teknis yang harus ditutup", 2),
    ("8.7  Kesimpulan kelayakan", 2),
    ("9  REKOMENDASI DAN LANGKAH LANJUT", 1),
    ("9.1  Rekomendasi teknologi", 2),
    ("9.2  Peta jalan bertahap", 2),
    ("9.3  Estimasi effort", 2),
    ("9.4  Keputusan yang saya minta", 2),
    ("9.5  Pertanyaan terbuka", 2),
    ("9.6  Penutup", 2),
    ("LAMPIRAN A", 1),
    ("LAMPIRAN B", 1),
    ("LAMPIRAN C", 1),
    ("LAMPIRAN D", 1),
    ("LAMPIRAN E", 1),
]

def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


# ── deteksi halaman Daftar Isi ──────────────────────────────────────────────
# Halaman TOC = memuat judul "DAFTAR ISI" ATAU banyak entri berformat
# "<judul>\\n<angka>" (blok teks yang baris terakhirnya angka 1-3 digit).
# Halaman lanjutan TOC tidak punya judulnya, jadi harus dikenali dari pola entri.
toc_pages = set()
for i, page in enumerate(doc, start=1):
    blok = page.get_text("blocks")
    entri_toc = 0
    for b in blok:
        baris = [s.strip() for s in b[4].strip().splitlines() if s.strip()]
        if len(baris) >= 2 and re.fullmatch(r"\d{1,3}", baris[-1]) and len(baris[0]) > 4:
            entri_toc += 1
    ada_judul = any("daftar isi" in b[4].strip().lower() for b in blok)
    if entri_toc >= 5 or (ada_judul and entri_toc >= 2):
        toc_pages.add(i)
print(f"halaman Daftar Isi terdeteksi: {sorted(toc_pages)}\n")

hasil = []
for judul, level in JUDUL:
    target = norm(judul)
    # "DAFTAR ISI" menunjuk ke halaman TOC itu sendiri, yang justru dikecualikan
    # dari pencarian — jadi nilainya diisi langsung dari halaman TOC pertama.
    if target == "daftar isi":
        hal = min(toc_pages) if toc_pages else None
        hasil.append([level, judul, hal])
        print(f"{judul[:62]:64s} -> hal {hal} (halaman TOC)")
        continue
    found = None
    for i, lines in halaman:
        if i < 2 or i in toc_pages:
            continue
        for ln in lines:
            if norm(ln).startswith(target):
                found = i
                break
        if found:
            break
    hasil.append([level, judul, found])
    print(f"{'  ' if level==2 else ''}{judul[:62]:64s} -> hal {found if found else 'TIDAK DITEMUKAN'}")

json.dump(hasil, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"\ndisimpan: {OUT}")
doc.close()
