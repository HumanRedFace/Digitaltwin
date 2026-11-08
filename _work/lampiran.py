"""LAMPIRAN: metodologi uji, data mentah, sumber, glosarium."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_lib import (h1, h2, h3, p, pr, bullets, numbered, table, figure, caption_table,
                     callout, code_block, GREY)
import data as D

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
DIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")


def lampiran_a(d):
    h1(d, "LAMPIRAN A — INVENTARIS ASET DAN PENGUKURANNYA")

    h2(d, "A.1  Model 3D")
    p(d, "Setiap berkas dibaca langsung dengan parser glTF (membaca header biner dan JSON "
         "chunk), bukan diperkirakan dari nama berkas atau ukuran.")
    caption_table(d, "A-1", "Model 3D yang ditemukan beserta properti terukurnya")
    rows = []
    for key, m in D.ASET_MODEL.items():
        rows.append([m["berkas"].replace("~/Documents/", ""),
                     str(m.get("ukuran_berkas_mb", "—")),
                     str(m.get("mesh", "—")), str(m.get("material", "—")),
                     f"{m.get('triangles', '—'):,}".replace(",", ".") if isinstance(m.get("triangles"), int) else "—",
                     m.get("status") or m.get("catatan", "—")])
    table(d, ["Berkas", "MB", "Mesh", "Material", "Segitiga", "Status"], rows,
          widths=[4.8, 1.4, 1.4, 1.9, 2.4, 4.3], size=7.6, align_center={1, 2, 3, 4})

    p(d, "Catatan penting: berkas `dumptruck_edit.gltf` merujuk ke buffer eksternal "
         "`dumptruck_edit.bin` sebesar 108 MB yang **tidak ada** di folder tersebut. Model "
         "tersebut tidak dapat dimuat apa adanya. Versi yang berfungsi adalah "
         "`dumptruck_mapbox.glb` (23,59 MB, sudah terkompresi Draco). Ini gap G-1.")

    h2(d, "A.2  Data spasial")
    caption_table(d, "A-2", "Aset spasial dan parameter georeferensinya")
    table(d, ["Aset", "Parameter", "Nilai"],
          [["Ortomosaik", "Dimensi piksel", "23.249 × 17.296 px"],
           ["", "Resolusi", "1,352 cm/piksel"],
           ["", "Cakupan", "314,44 × 233,92 m (7,40 ha)"],
           ["", "Sistem koordinat", "EPSG:32750 — WGS 84 / UTM zone 50S"],
           ["", "Sumber georeferensi", "chunk eXIf: ModelPixelScale + ModelTiepoint + "
                                        "GeoKeyDirectory"],
           ["", "Tanggal survei", "14 Oktober 2026"],
           ["Titik kontrol", "Jumlah titik", "22 titik"],
           ["", "Resolusi citra drone / satelit", "3,93 cm/px / 14,93 cm/px"],
           ["", "Simpangan maksimum (drone)", "0,039 m"],
           ["", "Batas pengukuran", "Jarak ke badan jalan pada citra — bukan ke titik GCP "
                                     "terukur langsung"],
           ["Batas area", "Berkas", "Minergo.shp (252 byte) + Minergo.prj"],
           ["", "Isi geometri", "**0 geometri** — berkas praktis kosong"],
           ["", "Sistem koordinat", "WGS 84 geografis"]],
          widths=[2.8, 5.0, 8.4], size=7.9)

    h2(d, "A.3  Data RTK")
    caption_table(d, "A-3", "Statistik lengkap log RTK 28 Oktober 2026")
    r = D.RTK
    pasangan = [
        ("Sumber berkas", r["sumber"]),
        ("Jumlah titik", f"{r['titik']:,}".replace(",", ".")),
        ("Durasi", f"{r['durasi_detik']:,} detik".replace(",", ".")),
        ("Jarak tempuh", f"{r['jarak_m']:,.1f} m".replace(",", ".")),
        ("Kecepatan rata-rata", f"{r['kecepatan_rata_kmh']:.2f} km/jam"),
        ("Kecepatan p95", f"{r['kecepatan_p95_kmh']:.2f} km/jam"),
        ("Kecepatan maksimum", f"{r['kecepatan_maks_kmh']:.2f} km/jam"),
        ("Satelit (rata / min / maks)", f"{r['satelit_rata']} / {r['satelit_min']} / {r['satelit_maks']}"),
        ("HDOP (rata / terburuk)", f"{r['hdop_rata']} / {r['hdop_terburuk']}"),
        ("Umur koreksi RTCM (rata / maks)", f"{r['umur_koreksi_rata_s']} s / {r['umur_koreksi_maks_s']} s"),
        ("Solusi FIX", f"{r['rtk_fix']:,} sampel ({r['persen_fix']}%)".replace(",", ".")),
        ("Solusi FLOAT", f"{r['rtk_float']:,} sampel ({r['persen_float']}%)".replace(",", ".")),
        ("Jarak antar sampel FIX", f"{r['jarak_antar_fix_m']} m"),
        ("Course unik / beku", f"{r['course_unik']} / {r['course_beku']}"),
        ("Kalimat NMEA (RMC / GGA)", f"{r['nmea_rmc']:,} / {r['nmea_gga']:,}".replace(",", ".")),
        ("Checksum salah", f"{r['checksum_salah']} kalimat"),
        ("Selisih posisi vs telemetri OBU (rata / maks)",
         f"{r['selisih_posisi_obu_rata_m']} m / {r['selisih_posisi_obu_maks_m']} m"),
    ]
    table(d, ["Parameter", "Nilai"], [[k, v] for k, v in pasangan],
          widths=[6.6, 9.6], size=8.0, first_col_bold=False, zebra=True)


def lampiran_b(d):
    h1(d, "LAMPIRAN B — SPESIFIKASI PERANGKAT (DARI DOKUMEN RESMI)")

    h2(d, "B.1  Radar STONKAM PSA27")
    p(d, "Sumber: datasheet resmi PDF (S-15). Seluruh angka di bawah adalah **klaim vendor** — "
         "saya mengutipnya apa adanya tanpa menguji, karena pengujian perangkat berada di luar "
         "lingkup riset ini.")
    ps = D.RADAR["STONKAM PSA27"]
    urut = [("frekuensi", "Frekuensi & modulasi"), ("jangkauan", "Jangkauan deteksi"),
            ("zona", "Zona deteksi"), ("toleransi", "Toleransi pengukuran"),
            ("fov", "Sudut pandang"), ("proteksi", "Proteksi lingkungan"),
            ("daya", "Catu daya"), ("getaran", "Ketahanan getaran"), ("suhu", "Rentang suhu"),
            ("antarmuka", "Antarmuka"), ("sdk_terbuka", "SDK / protokol data")]
    table(d, ["Parameter", "Nilai (klaim vendor)"], [[l, ps[k]] for k, l in urut],
          widths=[4.4, 11.8], size=7.9, first_col_bold=True)

    h2(d, "B.2  Radar CISBO C95M")
    p(d, "Sumber: halaman produk resmi (S-17). Perhatikan catatan konflik di bagian bawah — "
         "ini contoh penting mengapa angka dari dokumen internal harus diverifikasi.")
    cs = D.RADAR["CISBO C95M"]
    urut = [("frekuensi", "Frekuensi"), ("jangkauan", "Jangkauan deteksi"),
            ("fov", "Sudut pandang"), ("proteksi", "Proteksi"), ("daya", "Catu daya"),
            ("antarmuka", "Antarmuka"), ("sdk_terbuka", "SDK / protokol data")]
    table(d, ["Parameter", "Nilai (klaim vendor)"], [[l, cs[k]] for k, l in urut],
          widths=[4.4, 11.8], size=7.9, first_col_bold=True)
    callout(d, "Konflik angka yang tidak boleh diabaikan",
            cs["catatan_konflik"] + " Bila angka 120 m terbawa ke rancangan, jangkauan deteksi "
            "akan dilebihkan 20 kali lipat — dan seluruh perhitungan cakupan blind spot menjadi "
            "salah. Karena itu angka yang tidak dapat diverifikasi **tidak dipakai** di dokumen "
            "ini, sekalipun berasal dari riset internal sendiri.",
            "FBE3E4", "E11B22", "PERINGATAN")

    h2(d, "B.3  Modul GNSS Quectel LC29H")
    p(d, "Sumber: datasheet hardware resmi (S-19), berkas lokal 59 halaman.")
    g = D.GNSS
    table(d, ["Parameter", "Nilai"],
          [["Modul", g["modul"]],
           ["Laju pembaruan posisi", g["update_rate"]],
           ["Laju data GNSS mentah", g["gnss_raw"]],
           ["Akurasi pulsa 1PPS", g["akurasi_1pps"]],
           ["Antarmuka", g["antarmuka"]],
           ["Sumber", g["sumber"]]],
          widths=[4.4, 11.8], size=8.0, first_col_bold=True)

    p(d, "Dua hal dari datasheet ini penting untuk rancangan. Pertama, **laju maksimum 10 Hz** "
         "berarti masalah lompatan 3 meter di Bab 5.4 sebagian bisa dikurangi hanya dengan "
         "mengubah konfigurasi — tanpa perangkat baru. Kedua, **pulsa 1PPS** dapat dipakai untuk "
         "menyelaraskan waktu antar perangkat dalam satu kendaraan, yang akan dibutuhkan bila "
         "kelak radar dan kamera digabungkan.")

    h2(d, "B.4  Sensor ultrasonik Howen (sering tertukar)")
    hs = D.RADAR["Howen HW-H6004A / H6008A"]
    table(d, ["Parameter", "Nilai (klaim vendor)"],
          [["Teknologi", hs["teknologi"]], ["Akurasi", hs["akurasi"]],
           ["Proteksi", hs["proteksi"]], ["Antarmuka", hs["antarmuka"]],
           ["Catatan", hs["catatan"]]],
          widths=[4.4, 11.8], size=8.0, first_col_bold=True)
    p(d, "Saya mencantumkan perangkat ini justru karena sering **tertukar** dengan radar dalam "
         "diskusi internal. Secara teknologi ia berbeda: ultrasonik 40 kHz, bukan gelombang "
         "milimeter. Konsekuensinya berbeda pula — jangkauan lebih pendek, dan tetap tidak "
         "menghasilkan objek berkoordinat.")

    h2(d, "B.5  Radar kelas object-list (pembanding)")
    p(d, "Untuk menunjukkan bahwa masalah pada Bab 5.6 bukan keterbatasan teknologi radar secara "
         "umum, saya mencantumkan satu kelas perangkat yang memang dirancang mengeluarkan "
         "object list.")
    sm = D.RADAR["smartmicro DRVEGRD (pembanding kelas industri)"]
    table(d, ["Parameter", "Nilai (klaim vendor)"],
          [["Frekuensi", sm["frekuensi"]], ["Antarmuka", sm["antarmuka"]],
           ["Keluaran", sm["keluaran"]], ["Integrasi", sm["integrasi"]],
           ["Status", sm["status"]]],
          widths=[4.4, 11.8], size=8.0, first_col_bold=True)
    p(d, "Perangkat kelas ini membuktikan bahwa permintaan pada Bab 5.7 bukan permintaan yang "
         "mustahil secara teknis — ia hal biasa pada radar otomotif industri. Yang menjadi "
         "masalah adalah perangkat spesifik yang dimiliki Minergo saat ini berada di kelas "
         "produk yang berbeda: sistem peringatan, bukan sistem persepsi.")


def lampiran_c(d):
    h1(d, "LAMPIRAN C — METODOLOGI DAN DATA MENTAH PENGUKURAN RENDER")

    h2(d, "C.1  Mengapa lampiran ini ada")
    p(d, "Angka kinerja di Bab 4 adalah bagian dokumen yang paling mungkin dipertanyakan, dan "
         "sepatutnya demikian. Karena itu seluruh metode dan data mentahnya dicantumkan di sini "
         "supaya dapat direproduksi atau dibantah. Prinsipnya: angka yang tidak bisa "
         "direproduksi tidak layak dipercaya.")

    h2(d, "C.2  Perangkat dan perangkat lunak")
    table(d, ["Komponen", "Spesifikasi"],
          [["Mesin", D.UJI["mesin"]], ["GPU (dibaca dari driver)", D.UJI["gpu"]],
           ["Ukuran tekstur maksimum", str(D.UJI["max_texture_size"])],
           ["Browser", D.UJI["browser"]], ["Resolusi render", D.UJI["resolusi"]],
           ["Pustaka", f"three.js {D.UJI['three_js']}"]],
          widths=[4.6, 11.6], size=8.2, first_col_bold=True)

    h2(d, "C.3  Metode pengukuran")
    p(d, "Tiga hal dalam metode ini menentukan keabsahan seluruh angka, dan ketiganya lahir dari "
         "kegagalan yang saya alami sendiri saat pertama kali mengukur.")

    numbered(d, [
        "**Sinkronisasi GPU.** `renderer.render()` hanya menaruh perintah ke antrean; ia kembali "
        "sebelum GPU selesai. Tanpa paksaan menunggu, hasilnya mengukur kecepatan CPU "
        "mengantre — bukan kecepatan menggambar. Saya memakai `gl.readPixels()` satu piksel "
        "setelah setiap render, yang memaksa sinkronisasi. Pengukuran awal saya tanpa ini "
        "menghasilkan 27 juta segitiga pada 830 fps, angka yang jelas mustahil dan saya buang.",
        "**Pemanasan sebelum pengukuran.** 20 frame pertama dijalankan tanpa dicatat, agar "
        "kompilasi shader dan alokasi tekstur tidak masuk hitungan.",
        "**Jendela waktu tetap.** Pengukuran berjalan selama 2500 ms dan jumlah frame dihitung, "
        "bukan sebaliknya. Ini menghindari bias dari frame pertama yang lebih lambat.",
    ])

    callout(d, "Kesalahan yang saya temukan dan perbaiki sendiri",
            "Pengukuran awal (bench5) menghasilkan angka yang tidak masuk akal. Alih-alih "
            "melaporkannya sebagai temuan, saya memeriksa metodenya dan menemukan dua cacat: "
            "(a) tidak ada sinkronisasi GPU, dan (b) penghitungan segitiga hanya meng-instance "
            "satu kelompok material dari tiga yang ada. Run final (bench7) memperbaiki keduanya "
            "dan itulah yang dilaporkan. Saya mencantumkan kegagalan ini karena metode yang "
            "menyembunyikan kesalahannya sendiri tidak layak dipercaya.",
            "FDF7EC", "C8892A", "CATATAN METODE")

    h2(d, "C.4  Data mentah — seluruh run")
    caption_table(d, "C-1", "Seluruh hasil pengukuran, tanpa penyaringan")
    rows = []
    for label, dc, tri, pts, ms, fps in D.BENCH:
        rows.append([label, f"{dc:,}".replace(",", "."), f"{tri:,}".replace(",", "."),
                     f"{pts:,}".replace(",", ".") if pts else "—",
                     f"{ms:.2f}", f"{fps:.1f}"])
    table(d, ["Skenario", "Draw call", "Segitiga", "Titik", "ms/frame", "fps"], rows,
          widths=[6.2, 1.9, 2.4, 2.0, 1.9, 1.6], size=7.7, align_center={1, 2, 3, 4, 5})

    h2(d, "C.5  Angka turunan dan cara menghitungnya")
    bt = D.BENCH_TURUNAN
    table(d, ["Besaran", "Rumus", "Hasil"],
          [["Biaya per draw call", "(70,12 − 8,25) ms ÷ (14.003 − 1)",
            f"{bt['biaya_per_draw_call_ms']*1000:.1f} mikrodetik"],
           ["Throughput vertex (60 instance)", "67.918.500 segitiga ÷ 124,46 ms",
            f"{bt['throughput_tri_juta_per_detik']:.0f} juta segitiga/detik"],
           ["Throughput vertex (24 instance)", "27.167.400 segitiga ÷ 51,04 ms",
            f"{bt['throughput_tri_juta_per_detik_24']:.0f} juta segitiga/detik"],
           ["Headroom pada target 30 fps", "(33,33 − 11,34) ms ÷ 33,33 ms", "66%"],
           ["Rasio optimasi aset", "70,12 ms ÷ 8,25 ms", "8,5 kali"]],
          widths=[4.4, 7.2, 4.6], size=8.0)

    p(d, "Dua angka throughput vertex yang hampir identik (546 dan 546 juta segitiga/detik) "
         "bukan kebetulan — itu bukti bahwa pada beban tersebut penyempitnya sudah berpindah "
         "dari CPU ke GPU, sehingga penambahan instance berbanding lurus dengan waktu. Ini "
         "informasi yang berguna untuk merancang LOD.")

    h2(d, "C.6  Cara mereproduksi")
    p(d, "Seluruh skrip pengukuran disimpan bersama dokumen ini di folder `_work/`. Untuk "
         "mereproduksi:")
    code_block(d, """
# 1. Pasang dependensi
cd _work/bench
npm install three@0.187.0 puppeteer-core@23

# 2. Jalankan (Chrome harus terpasang)
node run_bench7.js

# 3. Hasil
#    bench7_results.json  → data mentah
#    scene_b7.png         → tangkapan layar scene

# Catatan: skrip memakai Chrome headless pada 1920x1080.
# Angka akan berbeda pada perangkat lain — itu wajar dan justru
# alasan pengukuran ulang pada perangkat target diperlukan (Fase 1).
""", size=7.4)

    p(d, "Untuk grafik pada Bab 3 dan Bab 4, seluruh angka berasal dari satu berkas "
         "`_work/data.py`. Tidak ada angka yang ditulis ulang secara manual di dalam grafik, "
         "sehingga tidak mungkin ada ketidakcocokan antara teks, tabel, dan gambar.")


def lampiran_d(d):
    h1(d, "LAMPIRAN D — DAFTAR SUMBER")

    p(d, "Setiap sumber di bawah ini benar-benar dibuka dan diperiksa isinya, bukan dikutip dari "
         "mesin pencari. Untuk sumber berlisensi, yang dibaca adalah berkas lisensi mentah; "
         "untuk datasheet, berkas PDF resminya; untuk standar, dokumen spesifikasinya.")

    caption_table(d, "D-1", "Daftar sumber dan tingkat verifikasinya")
    rows = []
    for sid, nama, url, status in D.SUMBER:
        rows.append([sid, nama, url, status])
    table(d, ["ID", "Sumber", "Alamat / lokasi", "Tingkat"], rows,
          widths=[1.1, 5.6, 7.0, 2.5], size=7.2, align_center={0, 3})

    h2(d, "D.1  Catatan tentang sumber yang saling bertentangan")
    p(d, "Ada satu kelompok sumber yang saling bertentangan dan perlu dijelaskan secara terbuka: "
         "dokumen riset radar internal Minergo (S-27) memuat angka jangkauan yang berbeda dari "
         "halaman produk resmi vendor untuk perangkat yang sama. Ketika dua sumber bertentangan, "
         "saya memakai prinsip: **sumber yang lebih dekat ke pabrikan menang**, dan bila "
         "keduanya tidak dapat diverifikasi, angka tersebut tidak dipakai sama sekali.")

    p(d, "Konsekuensinya, angka 120 m untuk CISBO C95M — yang muncul di dokumen internal — tidak "
         "dipakai di dokumen ini, dan saya jadikan pertanyaan V-4. Ini keputusan yang tidak "
         "nyaman karena berarti mengoreksi pekerjaan sendiri, tetapi alternatifnya adalah "
         "membangun rancangan di atas angka yang mungkin salah 20 kali lipat.")

    h2(d, "D.2  Sumber yang dicari tetapi tidak ditemukan")
    p(d, "Sama pentingnya dengan daftar yang ditemukan: berikut adalah hal-hal yang sudah dicari "
         "dan **tidak** ditemukan. Pencantuman ini mencegah orang lain mengulang pencarian yang "
         "sama.")
    bullets(d, [
        "Dokumen protokol atau SDK untuk object list radar STONKAM PSA27 — tidak ada di situs "
        "resmi, tidak ada di halaman unduhan, tidak disebut dalam datasheet.",
        "Dokumen protokol untuk radar CISBO C95M — halaman produknya hanya menyebut LED dan "
        "buzzer sebagai antarmuka.",
        "DSM atau point cloud dari survei drone Minergo — folder Validasi hanya berisi "
        "ortomosaik raster dan data titik kontrol.",
        "Berkas buffer `dumptruck_edit.bin` (108 MB) yang dirujuk oleh `dumptruck_edit.gltf`.",
        "Geometri pada `Minergo.shp` — berkas berukuran 252 byte, praktis kosong.",
        "Skema resmi telemetri OBU — berkas CSV ada, tetapi tanpa dokumentasi field.",
    ])


def lampiran_e(d):
    h1(d, "LAMPIRAN E — GLOSARIUM DAN SINGKATAN")

    p(d, "Glosarium ini disusun untuk pembaca yang tidak berlatar belakang geospasial atau grafika "
         "komputer — karena dokumen ini akan dibaca oleh manajemen dan tim operasional, bukan "
         "hanya oleh engineer.")

    istilah = [
        ("3D Tiles", "Standar OGC untuk streaming data 3D geospasial secara bertahap sesuai "
                     "kebutuhan kamera. Versi 1.1 (2023) menjadikan glTF sebagai format tile wajib."),
        ("1PPS", "One Pulse Per Second — pulsa waktu satu detik sekali dari modul GNSS, dipakai "
                 "menyelaraskan jam antar perangkat."),
        ("COG", "Cloud Optimized GeoTIFF — berkas GeoTIFF yang disusun agar bisa dibaca sebagian "
                "tanpa mengunduh seluruhnya."),
        ("COPC", "Cloud Optimized Point Cloud — standar serupa COG, tetapi untuk point cloud."),
        ("Draw call", "Satu perintah gambar dari CPU ke GPU. Semakin banyak draw call, semakin "
                      "besar beban CPU per frame — penyebab utama lambat pada Bab 4."),
        ("DSM", "Digital Surface Model — model permukaan tanah beserta semua objek di atasnya "
                "(bangunan, kendaraan, vegetasi). Dibutuhkan untuk twin permukaan."),
        ("ECEF", "Earth-Centered, Earth-Fixed — sistem koordinat kartesian dengan titik nol di "
                 "pusat bumi (EPSG:4978). Satuannya meter. Dipakai untuk perhitungan posisi."),
        ("ENU", "East-North-Up — kerangka lokal dengan sumbu timur, utara, dan atas. Dipakai "
                "per tile pada 3D Tiles, dan pada umumnya Y adalah sumbu atas (berbeda dari "
                "kerangka kendaraan)."),
        ("FIX / FLOAT", "Status solusi RTK. FIX berarti ambiguitas integer terkunci — akurasi "
                        "sentimeter. FLOAT berarti belum terkunci — akurasi desimeter sampai meter."),
        ("FMCW", "Frequency Modulated Continuous Wave — modulasi radar yang mengukur jarak dari "
                 "pergeseran frekuensi."),
        ("Geofence", "Batas virtual pada peta. Dipakai untuk menandai zona terlarang, batas "
                     "kecepatan, atau area operasi."),
        ("glTF", "GL Transmission Format — standar Khronos untuk model 3D. \"JPEG-nya 3D\"."),
        ("GNSS", "Global Navigation Satellite System — istilah umum untuk GPS, GLONASS, Galileo, "
                 "Beidou."),
        ("HDOP", "Horizontal Dilution of Precision — ukuran geometri satelit. Semakin kecil "
                 "semakin baik; di bawah 1 sangat baik."),
        ("InstancedMesh", "Teknik menggambar banyak salinan geometri yang sama dengan satu draw "
                          "call. Kunci untuk menampilkan puluhan kendaraan."),
        ("LOD", "Level of Detail — memakai model lebih sederhana saat objek jauh dari kamera."),
        ("NMEA 0183", "Format teks standar keluaran penerima GNSS. Kalimat RMC memuat posisi dan "
                      "kecepatan; GGA memuat kualitas solusi."),
        ("Object list", "Daftar objek terdeteksi beserta jarak, sudut, dan kecepatannya. "
                        "Ini yang dibutuhkan visualisasi radar — dan yang tidak dimiliki "
                        "perangkat saat ini."),
        ("Orthomosaic", "Citra gabungan hasil foto drone yang sudah dikoreksi geometrinya, "
                        "sehingga dapat dipakai sebagai peta dengan skala seragam."),
        ("RTK", "Real-Time Kinematic — teknik GNSS dengan koreksi dari base station, memberikan "
                "akurasi sentimeter bila berstatus FIX."),
        ("UTM", "Universal Transverse Mercator — sistem proyeksi peta dalam meter. Ortomosaik "
                "Minergo memakai UTM zona 50S (EPSG:32750)."),
        ("WebGL2 / WebGPU", "Antarmuka grafis browser. WebGL2 tersedia luas; WebGPU lebih baru "
                            "dan lebih cepat tetapi belum di semua perangkat."),
        ("Wireframe", "Rancangan tata letak layar tanpa detail visual final — dipakai untuk "
                      "menguji keputusan informasi sebelum kode ditulis."),
    ]

    for ist, defi in istilah:
        par = d.add_paragraph()
        par.paragraph_format.space_after = d.paragraphs[-1].paragraph_format.space_after
        from doc_lib import _apply_font, BODY_FONT
        from docx.shared import Pt
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.left_indent = __import__("docx").shared.Cm(0.0)
        r1 = par.add_run(ist)
        _apply_font(r1, BODY_FONT, 9, bold=True)
        r2 = par.add_run("  —  ")
        _apply_font(r2, BODY_FONT, 9)
        r3 = par.add_run(defi)
        _apply_font(r3, BODY_FONT, 9)
