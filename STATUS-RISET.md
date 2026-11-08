# STATUS RISET — Digital Twin 3D View (Minergo R&D)

> **Baca berkas ini dulu sebelum mengerjakan apa pun pada proyek ini.**
> Ia mencatat apa yang sudah selesai, apa yang belum, keputusan yang sudah
> diambil, jebakan yang sudah ditemukan, dan perintah persis untuk melanjutkan.
>
> Terakhir diperbarui: 8 November 2026 — akhir sesi 2 (QA tahap 2 + perbaikan bug).

---

## 1. Status satu baris

Dokumen **selesai, sudah dibangun ulang, dan seluruh QA terukur lulus 0 temuan.**
Yang belum: pemadatan 5 halaman yang berakhir terlalu dini, dan pemeriksaan visual
dengan mata (Vision API terkunci 429 sepanjang dua sesi).

---

## 2. Berkas hasil (deliverable)

| Berkas | Ukuran | Keterangan |
|---|---|---|
| `Digital Twin 3D View - Riset Kelayakan.docx` | 1,6 MB | sumber |
| `Digital Twin 3D View - Riset Kelayakan.pdf` | 2,1 MB | hasil ekspor LibreOffice |

Lokasi: `/Users/mvmho11/Documents/Digitaltwin/`

Isi: Bab 1–9 + Lampiran A–E · 52 halaman · 16.919 kata · 9 gambar (Gambar 1–9
lengkap) · 39 tabel (Tabel 1–39 lengkap).
Nomor dokumen: MNG-RND-DT-2026-001 rev A.

---

## 3. Peta berkas kerja (folder `_work/`)

### Pembangun dokumen — urutan pemanggilan
| Berkas | Isi |
|---|---|
| `build_all.py` | **titik masuk.** Build → ekspor PDF → ukur halaman → build ulang sampai konvergen |
| `build.py` | merakit seluruh bab jadi satu .docx |
| `doc_lib.py` | pustaka tata letak: `p`, `pr`, `table`, `figure`, `callout`, `code_block`, footer |
| `bab_awal.py` | sampul, dokumen kontrol, ringkasan eksekutif, daftar isi |
| `bab1_3.py` | Bab 1–3 (pendahuluan, use case, riset teknologi) |
| `bab4_6.py` | Bab 4–6 (pengukuran render, data & integrasi, arsitektur) |
| `bab7_9.py` | Bab 7–9 (wireframe, kelayakan & risiko, rekomendasi) |
| `lampiran.py` | Lampiran A–E |
| `data.py` | **satu-satunya sumber angka.** Semua temuan terukur ada di sini |
| `charts.py` | grafik matplotlib (8 berkas di `img/`) |
| `wireframe.py` | wireframe viewer desktop + mobile (matplotlib) |
| `measure_toc.py` | **mengukur** nomor halaman nyata dari PDF untuk mengisi daftar isi |

### Gambar
- `img/g1..g8_*.png` — 8 grafik dari `charts.py` (dibuat `figure.dpi=200`).
- `diagrams/{arsitektur,alur_data,koordinat}.png` — diagram graphviz, **300 DPI**
  (diregenerasi sesi 2 dengan `/opt/homebrew/bin/dot -Tpng -Gdpi=300`).
- `wireframe/{wireframe_desktop,wireframe_mobile}.png`

### Skrip QA — semua berbasis pengukuran, tidak ada yang "kira-kira"
| Skrip | Memeriksa | Hasil terakhir |
|---|---|---|
| `qa_pdf.py` | halaman kosong, teks terpotong, gambar keluar kolom, entri TOC | 0 / 0 / 0 |
| `qa_toc.py` | verifikasi independen 73 entri daftar isi | 73/73 |
| `qa_teks.py` | karakter asing, markup bocor, placeholder, konsistensi angka | 0 masalah |
| `qa_paginasi.py` | keterisian halaman, baris piatu, judul menggantung | 0 temuan |
| `qa_struktur.py` | jarak keterangan↔objek, tepi kolom, tabel terbelah | 0 temuan |
| `qa_overlap.py` | kata saling menimpa, teks di atas gambar | 0 |
| `qa_estetika.py` | kepadatan tinta, ruang kosong, berat visual kiri-kanan | lihat §6.2 |
| `qa_kontras.py` | kontras piksel pada label wireframe | dipakai sekali |
| `qa_kartu.py` | teks keluar dari kartu di wireframe | dipakai sekali |
| `qa_wireframe.py` | teks tumpang-tindih di wireframe | dipakai sekali |
| `qa_diagram.py` | node graphviz bertumpuk / keluar kanvas | dipakai sekali |

---

## 4. Cara membangun ulang

```bash
cd /Users/mvmho11/Documents/Digitaltwin/_work
/Users/mvmho11/miniconda3/bin/python3.13 build_all.py
```

Dua-pass konvergen: bangun → ekspor PDF → ukur letak tiap judul → isi nomor
halaman → bangun lagi, maksimal 3 iterasi, berhenti saat "KONVERGEN".

Lingkungan:
- Python: `/Users/mvmho11/miniconda3/bin/python3.13` — satu-satunya yang punya
  numpy/scipy/PIL/PyMuPDF di mesin ini.
- LibreOffice: `/Applications/LibreOffice.app/Contents/MacOS/soffice`.
- Graphviz: `/opt/homebrew/bin/dot`.
- Font: Georgia + Courier New (tertanam sebagai subset di PDF).

---

## 5. Hasil QA terakhir — semua lulus

| Pemeriksaan | Hasil |
|---|---|
| Halaman kosong | 0 |
| Teks terpotong (ukur per KATA) | 0 |
| Gambar keluar kolom | 0 |
| Kata saling menimpa | 0 |
| Teks di atas gambar | 0 |
| Keterangan jauh dari objek | 0 (semua 3,6–4,5 pt dari objeknya) |
| Tepi kolom menyimpang | 0 |
| Tabel terbelah tanpa header ulang | 0 (hal 14→15 header berulang) |
| Markup bocor / karakter asing / placeholder | 0 |
| Paragraf duplikat | 0 |
| Daftar isi | 73/73 cocok |
| DPI efektif semua gambar | 215–300 DPI (semua ≥200) |
| Gambar 1–9 / Tabel 1–39 | lengkap |

Rata-rata kepadatan tinta 9,06% — wajar untuk laporan padat teks (khas 6–12%).

---

## 6. Yang BELUM selesai

### 6.1 Pemeriksaan visual belum pernah dilakukan
Sepanjang dua sesi, Vision API selalu 429 (rate limit). **Tidak ada satu pun
halaman yang pernah dinilai dengan mata.** Semua QA di atas bersifat pengukuran
terprogram — sangat ketat untuk hal terukur (posisi, luapan, nomor halaman), tetapi
tidak menangkap cacat rasa: ritme spasi, keseimbangan warna, hierarki tipografi.

Semua halaman sudah dirender ke `_work/render/p01..p52.png` (110 dpi). Mulai dari
p01 (sampul), p03 (ringkasan), p17–18 (matriks skor), p32 & p34 (wireframe).

### 6.2 Halaman berakhir terlalu dini
Diukur dari kepadatan tinta dan keterisian kolom:

| Halaman | Tinta | Keterisian | Isi |
|---|---|---|---|
| 4 | <2% | 14,7% | lanjutan ringkasan eksekutif + callout "KEPUTUSAN DIMINTA" |
| 31 | <2% | 26,5% | lanjutan daftar "yang sengaja tidak dimasukkan" |
| 13 | 5% | 48,8% | akhir 2.7 (tabel kandidat fitur MVP) |
| 43 | 5% | 49,9% | akhir 9.6 Penutup |
| 45 | 4,5% | 50,4% | Tabel A-3 statistik log RTK |

Penyebab: `h1()` memaksa `page_break_before`, jadi sisa ruang halaman sebelumnya
terbuang; ditambah `keep_together` pada tabel besar yang tidak boleh terbelah.

Opsi (pilih sadar, jangan asal):
- Perkecil `space_before` heading level 1, atau
- longgarkan ambang `keep_together` untuk tabel > 6 baris supaya boleh terbelah
  dengan header berulang, atau
- pindahkan callout "KEPUTUSAN DIMINTA" ke halaman 3 yang masih lapang.

Catatan: halaman 32 dan 34 terdeteksi "SANGAT PADAT" karena berisi wireframe
berlatar gelap (±97% piksel gelap). Itu **bukan** cacat — kepadatan tinta pada
halaman bergambar gelap memang tinggi.

### 6.3 Halaman 5 dinilai "berat sebelah"
Tabel daftar isi memenuhi kolom; kolom nomor halaman di kanan sempit. Ini akibat
wajar dari struktur tabel TOC, bukan cacat cetak. Diabaikan kecuali terlihat janggal
secara visual.

### 6.4 Belum ada pemeriksaan konsistensi istilah
Belum ada skrip yang mendeteksi istilah sama ditulis berbeda (mis. "dump truck" vs
"dumptruck", "haul road" vs "jalan angkut"). Mudah ditambahkan ke `qa_teks.py`.

---

## 7. Bug yang SUDAH ditemukan dan diperbaiki — jangan terulang

Ini bagian terpenting berkas ini. Masing-masing pernah lolos dari QA lama.

### 7.1 Daftar isi menunjuk halaman salah untuk Lampiran C dan E  ← paling serius
**Gejala:** TOC menulis Lampiran C = hal 32 (seharusnya 48) dan Lampiran E = hal 9
(seharusnya 52). `qa_toc.py` tetap melaporkan "73/73 cocok".

**Sebab:** `measure_toc.py` dan `qa_toc.py` sama-sama mencocokkan judul dengan
`line.startswith(judul)` terhadap **semua** baris teks. Akibatnya:
- hal 32 memuat kalimat badan `"Lampiran C (88 fps, 3 draw call). Aplikasinya..."`
- hal 9 memuat sel tabel `"Lampiran E"`

Keduanya lebih awal daripada judul aslinya, jadi menang dalam pencarian.

**Perbaikan:** pencocokan sekarang hanya terhadap baris berformat JUDUL (tebal dan
≥ 11,5 pt). Judul asli 15 pt tebal; teks badan 8–9 pt biasa.

**Pelajaran:** verifikator yang memakai aturan pencocokan sama dengan pembangun
tidak bisa menemukan bug pencocokan. Filter format judul wajib dipakai di kedua
sisi.

### 7.2 Metrik "monoton naik" TOC tidak bermakna
`qa_pdf.py` dulu mengumpulkan semua baris berakhir angka — termasuk baris footer
`MNG-RND-DT-2026-001 rev A | 7 / 52`. Jadi yang diukur nomor footer, dan tahun
"2026" sempat muncul sebagai nomor halaman (`rentang 1 .. 2026`). Sekarang: hanya
blok di atas area footer, dan hanya nilai 1..page_count.

### 7.3 Gambar 5 hanya 130 DPI
`diagrams/koordinat.png` diekspor tanpa `-Gdpi`, jadi hanya 796×913 px sementara
8 gambar lain 210–300 DPI. Pada cetak akan tampak kabur. Sudah diregenerasi ke
300 DPI; sekarang 261 DPI efektif di PDF.

### 7.4 Jebakan pengukuran (positif palsu) — WAJIB diingat

| Jebakan | Akibat kalau salah | Cara benar |
|---|---|---|
| Ukur luapan per **blok** | 4 "tabrakan" palsu di hal 8/27/37/42 karena bbox blok memuat spasi justify | ukur per **kata** |
| Halaman lanjutan TOC tidak berjudul | sub-bab mencocokkan dirinya sendiri → nomor palsu | kenali dari pola entri (baris terakhir angka 1–3 digit) |
| Sel tabel diukur sebagai paragraf | puluhan "tepi kiri menyimpang" palsu | hanya blok yang mengisi kolom penuh (lebar ≥458 pt dan x1 ≈ 527,25 pt) |
| Keterangan di puncak halaman | dianggap terpisah dari gambar | sah bila gambar/tabel ada di halaman yang sama |
| `page` di loop kedua | merujuk halaman terakhir loop pertama | pakai `doc[i-1]` |

---

## 8. Temuan riset inti — jangan diteliti ulang

Ambil angka dari `data.py`, jangan hitung ulang.

| Temuan | Angka | Tingkat bukti |
|---|---|---|
| Model dump truck Minergo | 14.003 mesh, 1,13 juta segitiga | TERVERIFIKASI |
| Render apa adanya | 14,3 fps | TERVERIFIKASI |
| Render setelah digabung per material | 116,8 fps (geometri identik) | TERVERIFIKASI |
| Penyebab utama lambat | draw call, bukan jumlah segitiga | TERVERIFIKASI |
| Scene target (60 truk + 1 juta titik) | 88,2 fps · 11,34 ms/frame, GPU terintegrasi M1 | TERVERIFIKASI |
| Log RTK 28 Okt 2026 | 3.601 titik, 1 jam, 10.891 m | TERVERIFIKASI |
| Kualitas solusi RTK | 32,9% FIX (1.184) / 67,1% FLOAT (2.417) | TERVERIFIKASI |
| Jarak antar sampel FIX | 3,03 m (laju 1 Hz) | TERVERIFIKASI |
| Ortomosaik | 7,4 ha, 1,35 cm/piksel | TERVERIFIKASI |
| Skor teknologi | CesiumJS 3,97 vs Three.js 3,80 dari 5,00 | ASUMSI berbobot |
| Estimasi effort | 720–1.220 jam-orang | ASUMSI |
| Radar STONKAM PSA27 / CISBO C95M | hanya alarm LED+buzzer, **0 dokumen protokol** | BELUM DITEMUKAN |

### Batas yang tidak boleh dilanggar
Laporan secara sadar **tidak** menggambar objek radar. Panel radar di wireframe
sengaja kosong dengan keterangan alasannya, karena perangkat yang dikaji hanya
mengeluarkan alarm biner, bukan daftar objek berkoordinat. Menambahkan animasi
karangan = klaim palsu di depan manajemen dan berbahaya untuk keputusan
keselamatan. **Jangan "memperbaiki" panel kosong itu.**

Batasan lain: dari CAN mentah tidak bisa dibedakan sein kiri vs kanan. Jangan
menyimpulkan sebaliknya.

---

## 9. Kebutuhan yang diminta (untuk verifikasi cakupan)

17 langkah kerja A–E semuanya tercakup:
- A (1–3) identifikasi kebutuhan + 2 use case → Bab 2
- B (4–5) perbandingan ≥3 teknologi + format aset → Bab 3
- C (6–9) data dictionary, inventaris sumber, opsi integrasi radar, waktu & koordinat → Bab 5
- D (10–14) diagram alur, wireframe, live/playback, risiko, effort → Bab 6–8
- E (15–17) sumber + matriks validasi, gap & pertanyaan vendor, usulan keputusan → Bab 8–9 + Lampiran D

7 keluaran yang diminta juga lengkap: dokumen, matriks ≥3 teknologi, daftar use case
+ kebutuhan data, diagram arsitektur, wireframe, analisis kelayakan, rekomendasi +
roadmap + estimasi effort.

---

## 10. Pertanyaan terbuka ke vendor (belum terjawab, tercatat di Bab 9.5)

| ID | Pihak | Pertanyaan | Menentukan |
|---|---|---|---|
| V-1 | STONKAM | Apakah PSA27 menyediakan object list terstruktur? | apakah UC-4 mungkin sama sekali |
| V-2 | STONKAM | Laju pembaruan objek (Hz) & jumlah objek bersamaan? | objek bisa digambar mulus atau hanya berkedip |
| V-3 | CISBO | Apakah C95M dapat mengeluarkan data target selain alarm? | apakah radar CISBO bisa dipakai |
| V-4 | CISBO | Klarifikasi jangkauan: halaman resmi 5 m × 6 m vs klaim 120 m | salah pakai = salah desain |
| V-5 | Quectel / mitra RTK | Apakah LC29H dapat dikonfigurasi ke laju lebih tinggi? | mengurangi lompatan 3 m antar posisi |
| V-6 | PIC Survey | Apakah tersedia DSM/point cloud dari survei drone? | apakah twin permukaan (cut/fill) mungkin |
| V-7 | IT / OT | Apakah diizinkan menyajikan viewer 3D on-premis? | apakah arsitektur on-premise dapat disetujui |

---

## 11. Aturan kerja proyek ini

1. **Lingkup riset dan konsep saja.** Tidak membangun aplikasi 3D, tidak integrasi
   sensor fisik, tidak PoC fungsional. Kalau diminta melampaui ini, konfirmasi dulu.
2. **Pisahkan fakta terverifikasi / klaim vendor / asumsi / belum ditemukan.**
   Setiap temuan penting mencantumkan sumber. Tidak ada angka tanpa label.
3. **Jangan mengarang data.** Lebih baik "tidak tersedia" daripada animasi atau
   angka karangan.
4. **Angka hanya dari `data.py`.** Jangan mengetik ulang angka di modul bab.
5. **QA harus terukur.** Kalau menambah pemeriksaan, tulis skripnya. Jangan
   mengandalkan pembacaan visual saja — dan jangan percaya skrip yang belum diuji
   bisa gagal.
6. **Setiap perubahan isi → jalankan `build_all.py`**, karena daftar isi diukur
   ulang dari PDF nyata setiap pass.

---

## 12. Log sesi

**Sesi 1 — 8 Nov 2026 (15:19–16:10)**
Riset dari nol: inventaris aset, riset teknologi + lisensi, riset integrasi
radar/telemetri/GNSS, pengukuran render nyata (puppeteer + three.js), diagram
arsitektur/koordinat/alur data, wireframe desktop + mobile, 8 grafik, tabel
benchmarking, tulis Bab 1–9 + Lampiran A–E, render .docx + PDF, QA layout/TOC/teks.
Daftar isi awalnya salah total (angka manual sampai 81 untuk PDF 53 halaman).
Hasil: 52 halaman, 16.919 kata.

**Sesi 2 — 8 Nov 2026 (18:xx) — QA tahap 2**
Menambahkan `qa_overlap.py`, `qa_paginasi.py`, `qa_struktur.py`, `qa_estetika.py`.
Empat cacat ditemukan dan diperbaiki:
1. **TOC salah halaman untuk Lampiran C (32→48) dan E (9→52)** — akar masalah
   pencocokan `startswith`; diperbaiki di `measure_toc.py` + `qa_toc.py`.
2. **Gambar 5 hanya 130 DPI** → regenerasi 300 DPI, sekarang 261 DPI.
3. **`qa_pdf.py` mengukur nomor footer, bukan entri TOC** — diperbaiki.
4. **Lima positif palsu di skrip QA sendiri** (ukur per blok, sel tabel, `page`
   bocor antar loop) — diperbaiki; QA sekarang 0 temuan.
PDF dibangun ulang dan konvergen; TOC terverifikasi 73/73 dengan verifikator yang
sudah benar. Vision API tetap 429 sepanjang sesi.

---

## 13. Langkah pertama saat melanjutkan

```bash
cd /Users/mvmho11/Documents/Digitaltwin/_work

# 1. Pastikan kondisi awal masih sehat (harus 0 temuan)
for s in qa_pdf qa_toc qa_teks qa_paginasi qa_struktur qa_overlap; do
  echo "### $s"; /Users/mvmho11/miniconda3/bin/python3.13 "$s.py" 2>&1 | tail -4
done

# 2. Kalau mengubah isi/layout, bangun ulang (wajib)
/Users/mvmho11/miniconda3/bin/python3.13 build_all.py

# 3. Periksa DPI gambar (harus >=200)
/Users/mvmho11/miniconda3/bin/python3.13 -c "
import fitz
d=fitz.open('../Digital Twin 3D View - Riset Kelayakan.pdf')
seen={}
for pg in range(1,d.page_count+1):
    p=d[pg-1]
    for im in p.get_images(full=True):
        for r in p.get_image_rects(im[0]):
            seen.setdefault(im[0],(pg,im[2],im[3],r.width))
for k,(pg,w,h,wpt) in sorted(seen.items(), key=lambda z:z[1][0]):
    print(f'hal {pg:>2}  {w}x{h}  {w/(wpt/72):4.0f} dpi')
"

# 4. Kalau vision sudah pulih, nilai halaman dengan mata
ls render/ | head
```

Urutan kerja yang disarankan:
1. §6.1 pemeriksaan visual (butuh vision; paling cepat memberi nilai tambah).
2. §6.2 pemadatan halaman 4, 13, 31, 43, 45 — perbaikan terakhir.
3. §6.4 konsistensi istilah, kalau diminta.
