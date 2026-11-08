"""BAB AWAL: cover, dokumen kontrol, ringkasan eksekutif, daftar isi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from doc_lib import (h1, h2, h3, p, pr, bullets, numbered, table, figure, caption_table,
                     callout, code_block, shade, cell_margins, USABLE_CM, NAVY, ACC, GREY,
                     BLACK, WHITE, GREEN, AMBER, _apply_font, hrule, BODY_FONT)
import data as D


def cover(d):
    # blok atas
    t = d.add_table(rows=1, cols=1); t.style = "Table Grid"; t.autofit = False
    c = t.rows[0].cells[0]; c.width = Cm(USABLE_CM)
    shade(c, "16324F"); cell_margins(c, 260, 260, 240, 240)
    par = c.paragraphs[0]; par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    par.paragraph_format.space_after = Pt(2)
    r = par.add_run("MINERGO SYSTEMS  ·  DIVISI R&D")
    _apply_font(r, BODY_FONT, 9.5, bold=True, color=RGBColor(0xA8, 0xC0, 0xD6))
    par2 = c.add_paragraph(); par2.paragraph_format.space_after = Pt(0)
    r2 = par2.add_run("Riset Kelayakan")
    _apply_font(r2, BODY_FONT, 11, color=RGBColor(0xD8, 0xE4, 0xEE))

    d.add_paragraph().paragraph_format.space_after = Pt(24)

    h = d.add_paragraph()
    h.paragraph_format.space_after = Pt(4)
    r = h.add_run("Digital Twin 3D View")
    _apply_font(r, BODY_FONT, 30, bold=True, color=NAVY)

    h2p = d.add_paragraph()
    h2p.paragraph_format.space_after = Pt(2)
    r = h2p.add_run("Visualisasi 3D Lingkungan Operasional, Armada, dan Objek Terdeteksi Sensor")
    _apply_font(r, BODY_FONT, 14, color=RGBColor(0x33, 0x44, 0x55))

    sp = d.add_paragraph()
    sp.paragraph_format.space_after = Pt(18)
    r = sp.add_run("Kajian teknologi, kebutuhan data, metode integrasi, dan arsitektur "
                   "untuk kebutuhan R&D Minergo — lingkup riset dan konsep, bukan implementasi aplikasi.")
    _apply_font(r, BODY_FONT, 11, italic=True, color=GREY)

    hrule(d)

    # kartu identitas dokumen
    info = [
        ("Nomor dokumen", "MNG-RND-DT-2026-001"),
        ("Versi / status", "rev A — draf untuk review teknis & PMO"),
        ("Tanggal", "8 November 2026"),
        ("Disusun oleh", "R&D Minergo — riset & arsitektur"),
        ("Jenis dokumen", "Studi kelayakan (feasibility study) + rancangan konseptual"),
        ("Lingkup", "Riset, perbandingan teknologi, arsitektur, wireframe"),
        ("Di luar lingkup", "Pembangunan aplikasi 3D, integrasi sensor fisik, PoC fungsional"),
        ("Klasifikasi", "Internal — R&D"),
    ]
    t2 = d.add_table(rows=0, cols=2); t2.style = "Table Grid"; t2.autofit = False
    for k, v in info:
        cells = t2.add_row().cells
        cells[0].width = Cm(4.6); cells[1].width = Cm(11.6)
        shade(cells[0], "F2F5F8"); cell_margins(cells[0]); cell_margins(cells[1])
        par = cells[0].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
        r = par.add_run(k); _apply_font(r, BODY_FONT, 8.6, bold=True, color=NAVY)
        par2 = cells[1].paragraphs[0]; par2.paragraph_format.space_after = Pt(0)
        r2 = par2.add_run(v); _apply_font(r2, BODY_FONT, 8.6)

    d.add_paragraph().paragraph_format.space_after = Pt(14)
    p(d, "Dokumen ini menjawab satu pertanyaan pokok: sejauh mana Minergo dapat "
         "merepresentasikan tambangnya dalam bentuk digital twin 3D — dengan data yang benar-benar "
         "sudah dimiliki hari ini, dan dengan biaya serta risiko yang terukur.", size=10.5, italic=True)


def dokumen_kontrol(d):
    h1(d, "DOKUMEN KONTROL")
    caption_table(d, 1, "Riwayat revisi dokumen")
    table(d, ["Versi", "Tanggal", "Penulis", "Deskripsi perubahan", "Status"],
          [["A", "8 Nov 2026", "R&D Minergo",
            "Rilis awal: identifikasi use case, perbandingan 5 teknologi, arsitektur, "
            "wireframe, analisis kelayakan dan risiko", "Draf untuk review"]],
          widths=[1.5, 2.4, 3.0, 7.2, 2.1], align_center={0, 1, 4}, size=8.4)

    caption_table(d, 2, "Konvensi penandaan tingkat bukti — dipakai konsisten di seluruh dokumen")
    table(d, ["Label", "Arti", "Cara pembaca memakainya"],
          [["**TERVERIFIKASI**",
            "Diukur langsung di mesin ini, dibaca dari berkas nyata milik Minergo, "
            "atau dikutip dari dokumen standar/datasheet resmi.",
            "Boleh dipakai sebagai dasar keputusan."],
           ["**KLAIM VENDOR**",
            "Angka berasal dari brosur/datasheet/halaman resmi vendor, belum diuji sendiri.",
            "Dipakai untuk menyaring, **bukan** untuk menjanjikan kinerja."],
           ["**ASUMSI**",
            "Perkiraan tim riset yang belum diverifikasi — misalnya estimasi effort.",
            "Wajib divalidasi sebelum jadi komitmen anggaran."],
           ["**BELUM DITEMUKAN**",
            "Sudah dicari dan tidak ada: dokumen, SDK, atau data tidak tersedia.",
            "Menjadi daftar pertanyaan ke vendor/PIC (Bab 9)."],
           ["**TIDAK ADA**",
            "Terkonfirmasi tidak ada pada perangkat/data saat ini.",
            "Menjadi blocker yang harus diselesaikan lebih dulu."]],
          widths=[3.2, 7.4, 5.6], size=8.4)

    callout(d, "Cara membaca angka kinerja di dokumen ini",
            "Semua angka fps/ms pada Bab 4 dan Lampiran C **diukur sendiri** memakai three.js 0.187.0 "
            "di Chrome headless pada MacBook M1 (GPU terintegrasi), resolusi 1920×1080. "
            "Metodenya: `render()` diikuti `gl.readPixels()` 1 piksel sebagai sinkronisasi GPU — "
            "tanpa ini, angka fps akan menipu karena hanya mengukur antrean CPU. "
            "Angka pada GPU diskrit akan lebih tinggi; angka ini sengaja dipakai sebagai **batas bawah**.",
            "EEF3F8", "2E6E9E", "METODE")


def ringkasan_eksekutif(d):
    h1(d, "RINGKASAN EKSEKUTIF")

    p(d, "Riset ini berangkat dari satu kenyataan yang saya temukan saat membuka berkas-berkas "
         "internal: Minergo **sudah memiliki** bahan baku digital twin yang cukup serius — "
         "ortomosaik drone tergeoreferensi resolusi 1,35 cm/piksel, log RTK 3.601 titik selama satu jam "
         "perjalanan nyata, model 3D dump truck 1,13 juta segitiga, dan riwayat telemetri unit. "
         "Yang belum ada bukanlah bahan bakunya, melainkan **sambungan** antar bahan itu, "
         "satu skema data yang seragam, dan satu keputusan teknologi yang diuji — bukan dipilih karena tren.")

    p(d, "Karena itu saya membagi pekerjaan ini menjadi dua: mengukur apa yang bisa diukur, dan "
         "menuliskan dengan jujur apa yang tidak bisa. Hasil pengukuran render di mesin ini "
         "menunjukkan satu temuan yang mengubah arah rekomendasi: **model dump truck yang ada "
         "memuat 14.003 mesh terpisah**. Dimuat apa adanya, ia hanya berjalan "
         "14,3 fps. Setelah digabung per material, dengan jumlah segitiga yang sama persis, "
         "ia berjalan 116,8 fps — delapan kali lebih cepat tanpa mengurangi detail sedikit pun. "
         "Artinya kelayakan visualisasi 3D bukan soal membeli GPU, tetapi soal disiplin pipeline aset.")

    caption_table(d, 3, "Ringkasan temuan pokok per aspek")
    table(d, ["Aspek", "Hasil utama", "Angka kunci", "Status"],
          [["Kesiapan data", "Ortomosaik, RTK, model 3D, dan telemetri sudah ada; "
                             "DSM/point cloud drone dan data objek radar belum",
            "7,4 ha terpetakan · 3.601 titik RTK",
            "**SEBAGIAN**"],
           ["Kinerja render", "Scene realistis (60 truk + 1 juta titik + terrain) "
                              "berjalan jauh di atas kebutuhan 30 fps",
            "88,2 fps · 11,34 ms/frame",
            "**TERVERIFIKASI**"],
           ["Penyebab utama lambat", "Jumlah draw call, bukan jumlah segitiga",
            "14.003 draw call = 70,12 ms; 3 draw call = 8,56 ms",
            "**TERVERIFIKASI**"],
           ["Kualitas posisi", "Hanya 32,9% sampel RTK berstatus FIX pada log nyata; "
                               "sisanya FLOAT",
            "1.184 FIX · 2.417 FLOAT",
            "**TERVERIFIKASI**"],
           ["Resolusi posisi", "Dengan laju 1 Hz dan kecepatan rata-rata 10,8 km/h, "
                               "posisi melompat ±3 m antar sampel",
            "3,03 m per sampel",
            "**TERVERIFIKASI**"],
           ["Data radar", "Radar yang dikaji hanya mengeluarkan status alarm; "
                          "daftar objek berkoordinat tidak tersedia",
            "0 dokumen protokol ditemukan",
            "**BELUM DITEMUKAN**"],
           ["Rekomendasi teknologi", "CesiumJS unggul tipis secara skor terbobot karena "
                                     "geospasial; Three.js unggul bila dibangun bertahap",
            "3,97 vs 3,80 dari 5,00",
            "**ASUMSI berbobot**"],
           ["Estimasi effort", "Fondasi + viewer armada layak dimulai lebih dulu",
            "720–1.220 jam-orang total",
            "**ASUMSI**"]],
          widths=[3.0, 7.0, 3.4, 2.8], size=8.2)

    h2(d, "Kesimpulan singkat")

    p(d, "Digital twin 3D **layak dikerjakan sekarang**, tetapi bukan dalam bentuk yang biasanya "
         "dibayangkan orang. Yang layak lebih dulu adalah **peta operasional 3D yang hidup**: "
         "armada bergerak di atas ortomosaik drone yang sebenarnya, dengan lintasan, geofence, "
         "dan riwayat yang bisa diputar ulang. Itu seluruhnya bisa dibangun dari data yang "
         "sudah ada di folder Minergo hari ini.")

    p(d, "Yang **belum** layak dijanjikan adalah menampilkan objek yang terdeteksi radar. "
         "Bukan karena teknologinya sulit, tetapi karena radar yang dikaji (STONKAM PSA27, "
         "CISBO C95M) menurut dokumen resminya hanya mengeluarkan **alarm LED dan buzzer** — "
         "bukan daftar objek berkoordinat. Tanpa kontrak data dari vendor, tidak ada yang bisa "
         "digambar. Saya menolak menutupi celah ini dengan animasi karangan, karena itu akan "
         "menjadi klaim palsu di depan manajemen dan berbahaya bila dipakai untuk keputusan "
         "keselamatan.")

    callout(d, "Tiga keputusan yang saya minta dari review ini",
            "1. **Setujui** pengerjaan Fase 0–1 (fondasi koordinat + viewer armada) sebagai "
            "langkah nyata berikutnya. "
            "2. **Setujui** pengiriman surat permintaan SDK/object list ke STONKAM dan CISBO "
            "sebelum Fase 4 dimasukkan ke anggaran. "
            "3. **Tetapkan** apakah target akhirnya browser (Three.js/CesiumJS) atau aplikasi "
            "desktop (Unity) — keputusan ini mengunci talenta dan lisensi selama beberapa tahun.",
            "FDF7EC", "C8892A", "KEPUTUSAN DIMINTA")


def daftar_isi(d, entries):
    """Daftar isi dua kolom: judul (dengan indentasi per level) + nomor halaman."""
    h1(d, "DAFTAR ISI")
    t = d.add_table(rows=0, cols=2); t.style = "Table Grid"; t.autofit = False
    for level, judul, hal in entries:
        cells = t.add_row().cells
        cells[0].width = Cm(14.0); cells[1].width = Cm(2.2)
        for c in cells:
            cell_margins(c, 40, 40, 70, 70)
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
        # kolom 1: judul, diindentasi menurut level
        par = cells[0].paragraphs[0]
        par.paragraph_format.left_indent = Cm({1: 0.0, 2: 0.45, 3: 0.90}.get(level, 0.0))
        r = par.add_run(judul)
        _apply_font(r, BODY_FONT, 8.8 if level == 1 else 8.4,
                    bold=(level == 1), color=NAVY if level == 1 else BLACK)
        # kolom 2: nomor halaman, rata kanan
        par2 = cells[1].paragraphs[0]
        par2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = par2.add_run(str(hal))
        _apply_font(r2, BODY_FONT, 8.6, bold=(level == 1),
                    color=NAVY if level == 1 else BLACK)
    d.add_paragraph()
    p(d, "Nomor halaman di atas mengacu pada berkas PDF yang menyertai dokumen ini. "
         "Bila dibuka di Word, nomor halaman dapat bergeser sedikit karena perbedaan "
         "mesin tata letak.", size=8.2, italic=True, color=GREY)
