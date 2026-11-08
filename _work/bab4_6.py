"""BAB 4–6: pengukuran kinerja, kebutuhan & integrasi data, arsitektur."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_lib import (h1, h2, h3, p, pr, bullets, numbered, table, figure, caption_table,
                     callout, code_block, GREY, USABLE_CM)
import data as D

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
DIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")


# ══════════════════════════════════════════════════════════════════════════
def bab4(d):
    h1(d, "4  PENGUKURAN KINERJA RENDER (HASIL UJI NYATA)")

    h2(d, "4.1  Mengapa saya mengukur sendiri")
    p(d, "Setiap mesin 3D mengklaim mampu menangani \"jutaan objek\" atau \"scene kompleks\". "
         "Kalimat itu tidak salah, tetapi juga tidak memberi informasi: kompleks menurut siapa, "
         "pada perangkat apa, dengan ukuran frame berapa. Karena keputusan teknologi di Bab 3 "
         "memakai kriteria kinerja dengan bobot 18%, angka itu harus punya dasar. Saya memilih "
         "mengukur sendiri di mesin yang tersedia daripada mengutip benchmark pihak lain, "
         "karena benchmark publik biasanya memakai scene yang tidak menyerupai tambang.")

    p(d, "Yang saya ukur bukanlah \"apakah three.js cepat\". Yang saya ukur adalah pertanyaan yang "
         "akan menentukan arsitektur: **berapa batas praktis scene tambang pada perangkat kelas "
         "laptop, dan apa yang menjadi penyempitannya?** Jawaban atas pertanyaan kedua itulah yang "
         "paling berguna, karena ia menentukan pekerjaan mana yang harus didisiplinkan.")

    callout(d, "Metode — dan mengapa metodenya penting",
            "Pengukuran dilakukan dengan three.js 0.187.0 di Chrome headless melalui "
            "puppeteer-core 23.11.1, resolusi 1920×1080, devicePixelRatio 1. "
            "Setiap frame diukur dengan `renderer.render(scene, camera)` yang diikuti "
            "`gl.readPixels()` satu piksel. Panggilan readPixels memaksa CPU menunggu GPU "
            "selesai, sehingga yang terukur adalah **waktu penyelesaian nyata**, bukan waktu "
            "antrean perintah. Tanpa sinkronisasi ini, pengukuran awal saya sempat menghasilkan "
            "angka 27 juta segitiga pada 830 fps — angka yang saya buang karena mustahil.",
            "EEF3F8", "2E6E9E", "METODE")

    caption_table(d, 17, "Lingkungan pengukuran")
    table(d, ["Parameter", "Nilai"],
          [["Mesin", D.UJI["mesin"]],
           ["GPU", D.UJI["gpu"]],
           ["Browser", D.UJI["browser"]],
           ["Resolusi render", D.UJI["resolusi"]],
           ["Versi three.js", D.UJI["three_js"]],
           ["Metode", D.UJI["metode_ukur"]],
           ["Catatan", D.UJI["catatan"]]],
          widths=[3.6, 12.6], size=8.2, first_col_bold=True)

    h2(d, "4.2  Temuan utama: draw call, bukan segitiga")
    p(d, "Model dump truck yang saya pakai adalah model yang benar-benar ada di folder Minergo: "
         "`dumptruck_mapbox.glb`, 23,59 MB, 1.131.975 segitiga, tiga material, tiga tekstur. "
         "Secara jumlah segitiga, model ini tergolong berat tetapi wajar untuk kendaraan tambang "
         "yang detail. Yang tidak wajar adalah strukturnya: **14.003 mesh node terpisah**.")

    p(d, "Setiap mesh node menjadi satu draw call. Empat belas ribu draw call berarti CPU harus "
         "menyiapkan empat belas ribu perintah gambar untuk setiap frame — dan itu pekerjaan yang "
         "harus selesai dalam 16 milidetik bila ingin 60 fps. Hasilnya bisa ditebak, tetapi saya "
         "tetap mengukurnya supaya angkanya bisa dipakai:")

    caption_table(d, 18, "Hasil pengukuran — model dump truck yang sama, tiga cara memuat")
    rows = []
    for label, dc, tri, pts, ms, fps in D.BENCH[:3]:
        rows.append([label, f"{dc:,}".replace(",", "."), f"{tri:,}".replace(",", "."),
                     f"{ms:.2f}", f"{fps:.1f}"])
    table(d, ["Skenario", "Draw call", "Segitiga", "ms/frame", "fps"], rows,
          widths=[7.0, 2.4, 2.6, 2.2, 2.0], size=8.4, align_center={1, 2, 3, 4})

    p(d, "Baris pertama dan ketiga memuat **geometri yang identik** — 1.131.975 segitiga, "
         "material yang sama, tekstur yang sama. Bedanya hanya struktur: yang pertama memuat "
         "14.003 mesh, yang ketiga memuat satu mesh hasil penggabungan. Hasilnya 14,3 fps "
         "berbanding 121,2 fps — **8,5 kali lebih cepat tanpa mengurangi satu segitiga pun**.")

    p(d, "Dari dua angka itu saya menurunkan biaya per draw call: (70,12 − 8,25) ms dibagi "
         "(14.003 − 1) draw call menghasilkan sekitar **4,4 mikrodetik per draw call**. Angka ini "
         "kecil per satuannya, dan justru itulah pelajarannya: satu draw call tidak terasa, "
         "tetapi empat belas ribu dijumlahkan menjadi 62 milidetik — empat kali lipat anggaran "
         "satu frame pada 60 fps.")

    figure(d, f"{IMG}/g1_benchmark.png",
           "Kiri: fps per skenario pada skala logaritmik, dengan garis putus-putus sebagai "
           "batas 30 fps. Kanan: waktu per frame. Perhatikan bahwa penurunan tajam terjadi "
           "saat jumlah mesh naik, bukan saat jumlah segitiga naik.", number=4)

    h2(d, "4.3  Uji instancing — batas sebenarnya bukan 1 juta segitiga")
    p(d, "Setelah struktur dirapikan, pertanyaan berikutnya adalah berapa banyak kendaraan yang "
         "bisa ditampilkan. Di tambang, satu scene bisa berisi 40–70 unit. Saya menguji dengan "
         "`InstancedMesh`: satu geometri truk, digambar berkali-kali dengan matriks berbeda. "
         "Ini cara yang benar untuk armada, karena semua truk HD memang berbagi model yang sama.")

    caption_table(d, 19, "Hasil uji instancing — satu geometri, N instance")
    rows = []
    for label, dc, tri, pts, ms, fps in D.BENCH[3:6]:
        rows.append([label, f"{dc}", f"{tri:,}".replace(",", "."), f"{ms:.2f}", f"{fps:.1f}"])
    table(d, ["Skenario", "Draw call", "Segitiga dirender", "ms/frame", "fps"], rows,
          widths=[6.6, 2.2, 3.4, 2.2, 2.0], size=8.4, align_center={1, 2, 3, 4})

    p(d, "Angka ini memberi dua batas yang sangat berguna. Pada 24 instance (27,2 juta segitiga), "
         "masih tercapai 19,6 fps. Pada 60 instance (67,9 juta segitiga), turun ke 8,0 fps. "
         "Dari sini throughput vertex dapat dihitung: sekitar 546 juta segitiga/detik pada beban "
         "24 instance, dan 546 juta juga pada beban 60 instance — konsisten, yang berarti pada "
         "titik ini penyempitannya sudah berpindah dari CPU ke GPU.")

    p(d, "Implikasi praktisnya jelas dan penting untuk anggaran: **menampilkan 60 truk HD "
         "berdetail penuh secara serentak tidak mungkin di perangkat kelas ini** (8 fps). "
         "Tetapi itu bukan masalah, karena secara operasional juga tidak perlu. Yang perlu "
         "adalah 60 truk yang **terlihat benar** dari jarak kamera operasional — dan untuk itu "
         "model perlu punya tingkat detail (LOD) rendah. Inilah sebabnya Bab 7 menggambar truk "
         "sebagai blok sederhana, bukan model 1,13 juta segitiga.")

    h2(d, "4.4  Scene target — angka yang saya pakai untuk keputusan")
    p(d, "Pengukuran yang paling relevan bukanlah model tunggal, melainkan campuran yang "
         "menyerupai layar sungguhan: terrain, ortomosaik, 60 unit armada, dan satu juta titik "
         "untuk jejak lintasan. Saya menyusun scene itu dan mengukurnya.")

    caption_table(d, 20, "Scene target realistis — komposisi dan hasil")
    rows = []
    label, dc, tri, pts, ms, fps = D.BENCH[6]
    rows.append(["Scene target (60 truk + 1 jt titik + terrain)", str(dc),
                 f"{tri:,}".replace(",", "."), f"{pts:,}".replace(",", "."),
                 f"{ms:.2f}", f"{fps:.1f}"])
    table(d, ["Skenario", "Draw call", "Segitiga", "Titik", "ms/frame", "fps"], rows,
          widths=[5.4, 1.9, 2.2, 2.2, 1.9, 1.7], size=8.4, align_center={1, 2, 3, 4, 5})

    p(d, "Hasilnya **88,2 fps** atau 11,34 ms per frame. Angka ini penting karena dua hal. "
         "Pertama, ia berada jauh di atas batas 30 fps yang saya tetapkan sebagai anggaran. "
         "Kedua, ia dicapai **tanpa** memakai WebGPU, tanpa GPU diskrit, dan tanpa trik "
         "dekoratif — hanya WebGL2 biasa pada GPU terintegrasi laptop.")

    p(d, "Dengan target 30 fps (33,3 ms per frame), tersisa 21,99 ms atau **66% headroom** untuk "
         "pekerjaan lain: memperbarui posisi, menggambar panel UI, dekode data jaringan, dan "
         "animasi. Headroom sebesar ini bukan kemewahan — ia adalah ruang untuk fitur yang belum "
         "direncanakan, dan dalam proyek nyata ruang itu selalu terpakai.")

    callout(d, "Angka yang saya pakai untuk keputusan",
            "Scene target berjalan **88,2 fps (11,34 ms/frame)** pada GPU terintegrasi kelas "
            "laptop. Anggaran yang saya tetapkan: **30 fps minimum** pada perangkat dispatcher, "
            "dengan headroom 66%. Untuk tablet lapangan, target diturunkan ke 30 fps dengan LOD "
            "lebih kasar dan mode 2D sebagai fallback. Angka ini adalah **batas bawah** — "
            "perangkat dengan GPU diskrit akan lebih cepat.",
            "F2F8F4", "2E7D4F", "HASIL")

    h2(d, "4.5  Pelajaran yang mengubah prioritas pekerjaan")
    p(d, "Dari seluruh pengukuran ini, ada empat kesimpulan yang saya bawa ke Bab 6 dan Bab 9. "
         "Keempatnya bukan kesimpulan tentang three.js, melainkan tentang **pekerjaan yang harus "
         "dilakukan siapa pun yang membangun visualisasi tambang, dengan mesin apa pun**.")

    bullets(d, [
        "**Pipeline aset lebih menentukan daripada pilihan mesin.** Selisih antara model "
        "apa adanya dan model yang dirapikan adalah 8,5 kali. Selisih antar mesin render di "
        "kelas yang sama jauh lebih kecil dari itu. Konsekuensinya: pekerjaan pertama yang "
        "berharga bukan memilih mesin, tetapi membangun pipeline konversi aset yang disiplin.",
        "**Angka \"jumlah objek\" pada brosur hampir selalu menyesatkan.** Yang menentukan "
        "adalah berapa draw call, berapa material, dan berapa tekstur — bukan berapa objek.",
        "**Detail model harus mengikuti jarak kamera, bukan kebanggaan artistik.** Truk "
        "berdetail 1,13 juta segitiga hanya masuk akal bila kamera mendekat. Untuk pandangan "
        "seluruh pit, LOD rendah sudah cukup dan itulah yang membuat 60 unit mungkin.",
        "**Sinkronisasi GPU wajib dalam setiap pengukuran render.** Tanpa itu hasilnya bisa "
        "salah hingga dua orde besaran, dan keputusan yang dibangun di atasnya akan salah.",
    ])

    p(d, "Satu hal yang perlu saya nyatakan terus terang: pengukuran ini dilakukan pada satu "
         "mesin, dengan satu model, dan satu komposisi scene. Ia cukup untuk menjawab "
         "\"apakah mungkin\" dan \"apa penyempitannya\", tetapi tidak cukup untuk menjanjikan "
         "angka fps pada perangkat tertentu di lapangan. Untuk itu diperlukan uji pada perangkat "
         "target yang sebenarnya — dan itu pekerjaan Fase 1, bukan pekerjaan riset ini.")


# ══════════════════════════════════════════════════════════════════════════
def bab5(d):
    h1(d, "5  KEBUTUHAN DATA DAN METODE INTEGRASI")

    h2(d, "5.1  Skema kanonik — satu baris, satu sampel")
    p(d, "Masalah terbesar yang saya temukan bukanlah kekurangan data, melainkan **keragaman "
         "format**. Log RTK keluar sebagai NMEA, telemetri kendaraan keluar sebagai CSV, "
         "ortomosaik sebagai GeoTIFF, dan masing-masing punya cara sendiri menyebut waktu, "
         "satuan, dan kualitas. Selama formatnya beragam, setiap fitur baru harus menulis "
         "pembaca sendiri — dan itu sumber bug yang tak habis.")

    p(d, "Karena itu saya mengusulkan satu skema kanonik. Prinsipnya sederhana: **satu baris "
         "adalah satu sampel dari satu sumber pada satu waktu**, dengan satuan SI, waktu UTC, "
         "dan kualitas yang selalu ikut. Semua adapter bertugas mengubah format asli ke bentuk "
         "ini; tidak ada bagian lain dari sistem yang boleh tahu format asli.")

    code_block(d, """
{
  "ts_utc":        "2026-10-28T10:41:02.113Z",   // waktu sumber, UTC, ISO-8601
  "ts_ingest":     "2026-10-28T10:41:02.488Z",   // waktu diterima gateway
  "source":        "rtk-lite-01",                // identitas perangkat
  "asset_id":      "HD-033",                     // unit yang diukur (boleh null)
  "kind":          "position",                   // position|telemetry|detection|video

  "pos": {                                        // EPSG:4978, meter
    "ecef":        [-2377291.482, 5397071.113, -2291004.771],
    "crs_src":     "EPSG:4326"
  },
  "quality": {
    "fix":         "FLOAT",                      // NONE|SINGLE|FLOAT|FIX
    "satellites":  41,
    "hdop":        0.44,
    "corr_age_s":  1.2
  },
  "motion": {
    "speed_mps":   7.61,                         // SI, bukan km/h
    "course_deg":  318.4,
    "course_valid": false                        // false bila kecepatan ~0
  },
  "payload": {}                                   // khusus kind=detection / telemetry
}
""", size=7.0)

    p(d, "Beberapa keputusan di dalam skema ini perlu penjelasan, karena tampak sepele tetapi "
         "berdampak besar:")

    bullets(d, [
        "**Posisi disimpan sebagai ECEF (EPSG:4978), bukan lat/lon.** Alasannya matematis: "
        "interpolasi dan perhitungan jarak pada lat/lon salah kecuali memakai rumus geodetis. "
        "Dalam ECEF, semuanya adalah vektor meter biasa. Konversi ke lat/lon hanya dilakukan "
        "saat ditampilkan.",
        "**Dua cap waktu, bukan satu.** `ts_utc` adalah waktu kejadian di sumber; `ts_ingest` "
        "adalah waktu data diterima. Selisihnya adalah latensi, dan latensi itulah yang harus "
        "ditampilkan kepada pengguna — bukan disembunyikan.",
        "**course_valid wajib ada.** Ini pelajaran langsung dari data: 1.146 dari 3.601 sampel "
        "punya course yang membeku karena kecepatan mendekati nol. Memakai course beku untuk "
        "mengarahkan model 3D akan membuat truk menghadap arah yang salah.",
        "**Kualitas bukan opsional.** Tanpa `fix`, `hdop`, dan `corr_age`, pengguna tidak bisa "
        "membedakan posisi yang akurat 2 cm dari posisi yang meleset 3 meter.",
        "**Satuan SI.** Kecepatan dalam m/s, bukan km/h. Konversi ke km/h hanya untuk tampilan. "
        "Ini mencegah kelas bug satuan yang sudah pernah terjadi di proyek sebelumnya.",
    ])

    h2(d, "5.2  Sistem koordinat — tiga kerangka yang tidak boleh dicampur")
    p(d, "Ini bagian yang paling sering salah dalam proyek digital twin, dan kesalahannya sering "
         "baru terlihat setelah sistem dipakai berbulan-bulan. Ada tiga kerangka koordinat yang "
         "hidup bersamaan, dan masing-masing punya aturan sendiri.")

    figure(d, f"{DIA}/koordinat.png",
           "Tiga kerangka koordinat: global geodetik (disimpan), global kartesian (dihitung), "
           "dan relatif kendaraan (tempat model dan objek sensor hidup).", number=5)

    p(d, "**Kerangka pertama** adalah global geodetik — latitudo, longitudo, tinggi. Ini yang "
         "dipakai manusia dan yang keluar dari NMEA. **Kerangka kedua** adalah global kartesian: "
         "ECEF (EPSG:4978) untuk perhitungan, atau UTM 50S (EPSG:32750) untuk peta datar. "
         "Ortomosaik Minergo berada di UTM 50S, jadi konversi ini nyata dan harus benar. "
         "**Kerangka ketiga** adalah relatif kendaraan: tempat model 3D dipasang, dan tempat "
         "objek radar dinyatakan.")

    p(d, "Aturan yang saya tetapkan, dan yang harus dipatuhi oleh siapa pun yang melanjutkan "
         "pekerjaan ini:")

    numbered(d, [
        "Posisi armada **disimpan** dalam EPSG:4978. Tidak ada penyimpanan lat/lon di basis data "
        "operasional.",
        "Model 3D kendaraan **selalu** berada di kerangka kendaraan (X maju, Y kiri, Z atas, "
        "ISO 8855), lalu dipasang ke dunia lewat matriks posisi dan heading.",
        "Objek radar **selalu** relatif terhadap sensor, bukan terhadap dunia. Mengubahnya "
        "menjadi global membutuhkan heading yang valid — dan heading tidak selalu valid (R-6).",
        "Ortomosaik dan terrain memakai UTM 50S pada sumbernya, lalu dikonversi ke ENU lokal "
        "per tile. Jangan mencampur UTM dengan ECEF secara langsung.",
        "Setiap kali ada perbedaan posisi antar sumber, selisihnya **diukur dan dicatat**, "
        "tidak dirata-ratakan diam-diam.",
    ])

    p(d, "Poin terakhir itu bukan teori. Pada data lapangan yang saya periksa, posisi dari log "
         "RTK dan posisi dari log telemetri unit berbeda rata-rata **1,27 meter**, dengan selisih "
         "maksimum **7,27 meter**. Bila kedua sumber digambar tanpa penjelasan, pengguna akan "
         "melihat dua truk untuk satu kendaraan — dan menyimpulkan sistemnya rusak. Padahal yang "
         "terjadi adalah dua metode penentuan posisi yang berbeda akurasi. Selisih ini harus "
         "ditampilkan sebagai atribut, misalnya \"posisi RTK\" versus \"posisi GNSS unit\".")

    h2(d, "5.3  Data yang sudah ada — hasil inventaris")
    p(d, "Ini bagian yang paling melegakan dari seluruh riset. Bahan baku digital twin sudah "
         "cukup banyak; yang belum adalah sambungannya.")

    caption_table(d, 21, "Inventaris aset nyata yang ditemukan di folder Minergo")
    table(d, ["Aset", "Properti terukur", "Status", "Dipakai untuk"],
          [["Ortomosaik drone", "23.249 × 17.296 px · 1,35 cm/px · EPSG:32750 · 7,4 ha · "
                                "survei 14 Okt 2026", "**SIAP**", "Permukaan dasar peta 3D"],
           ["Log RTK (28 Okt 2026)", "3.601 titik · 3.602 s · 10,9 km · 32,9% FIX",
            "**SIAP**", "Posisi armada, trail, replay"],
           ["Model dump truck", "1.131.975 tri · 14.003 mesh · 23,59 MB GLB (Draco)",
            "**SIAP setelah dirapikan**", "Model armada (dengan LOD)"],
           ["Model excavator", "6.452 tri · 26 mesh · 40 KB", "**SIAP**", "Model alat berat"],
           ["Telemetri unit (OBU)", "CSV per perjalanan · kecepatan, posisi, status",
            "**SEBAGIAN** — belum berskema", "Panel unit, analitik"],
           ["Batas area (shapefile)", "252 byte · 0 geometri · WGS 84", "**KOSONG**",
            "Geofence (harus dibuat ulang)"],
           ["DSM / point cloud drone", "Tidak ada berkas", "**TIDAK ADA**", "Terrain 3D sejati"],
           ["Object list radar", "Tidak ada dokumen protokol", "**TIDAK ADA**",
            "Use Case A (radar)"]],
          widths=[3.2, 5.6, 3.2, 4.0], size=7.8)

    h2(d, "5.4  Kualitas data lapangan — apa yang angka katakan")
    p(d, "Ini bagian yang paling tidak nyaman, dan karena itu paling penting. Data RTK yang saya "
         "periksa adalah rekaman perjalanan nyata selama satu jam. Dari 3.601 sampel, hanya "
         "**1.184 (32,9%) berstatus FIX**; sisanya 2.417 sampel (67,1%) berstatus **FLOAT**. "
         "Satelit rata-rata 48 dan HDOP 0,40 — angka yang bagus. Jadi masalahnya bukan geometri "
         "satelit, melainkan hilangnya solusi integer ambiguity, yang khas terjadi di lingkungan "
         "tambang karena multipath dari tebing dan kendaraan besar.")

    p(d, "Apa artinya bagi digital twin? FIX berarti akurasi sentimeter. FLOAT berarti akurasi "
         "desimeter sampai meter. Untuk menampilkan posisi armada di peta, keduanya cukup. "
         "Untuk **menegakkan geofence keselamatan**, FLOAT tidak cukup — truk bisa terlihat "
         "di dalam zona padahal berada 2 meter di luarnya. Karena itu kelas akurasi harus "
         "tampil di layar, dan aturan keselamatan tidak boleh memakai sampel FLOAT tanpa "
         "penanda.")

    caption_table(d, 22, "Statistik log RTK nyata — 3.601 sampel, 28 Oktober 2026")
    table(d, ["Metrik", "Nilai", "Implikasi bagi desain"],
          [["Durasi / jarak", "3.602 s / 10.891 m",
            "Cukup untuk satu siklus haul penuh — layak dijadikan data replay contoh"],
           ["Kecepatan rata-rata / p95 / maks", "10,82 / 27,49 / 35,79 km/jam",
            "Kecepatan p95 masih di bawah batas 40 km/jam pada umumnya jalur angkut"],
           ["Laju sampel", "1 Hz (3.601 sampel dalam 3.602 s)",
            "**Penyempit utama** — lihat perhitungan di bawah"],
           ["Jarak antar sampel pada FIX", "3,03 m",
            "Pada 30 fps, posisi hanya berubah sekali setiap 30 frame; interpolasi wajib"],
           ["Status solusi", "32,9% FIX · 67,1% FLOAT", "Kelas akurasi harus tampil di UI"],
           ["Satelit / HDOP", "48,4 rata-rata · HDOP 0,40",
            "Geometri satelit baik; FLOAT bukan disebabkan jumlah satelit"],
           ["Umur koreksi RTCM", "1,11 s rata-rata · 10,0 s maksimum",
            "Koreksi sempat putus hingga 10 detik — indikator jaringan perlu ada di UI"],
           ["Course beku", "1.146 dari 3.601 sampel",
            "Heading tidak boleh dipakai saat kecepatan ≈ 0 (risiko R-6)"],
           ["Checksum NMEA salah", "4 dari 3.605 kalimat",
            "Kecil, tetapi harus ditangani — bukan diabaikan"]],
          widths=[4.2, 4.6, 7.2], size=7.9)

    p(d, "Dari angka ini muncul satu perhitungan yang sangat menentukan pengalaman pengguna. "
         "Pada laju 1 Hz dan kecepatan rata-rata 10,8 km/jam (3,0 m/s), posisi truk melompat "
         "sekitar **3,03 meter setiap sampel**. Bila data digambar apa adanya, truk akan tampak "
         "berpindah secara tersentak sekali per detik. Pada 30 fps, itu berarti 30 frame dengan "
         "posisi diam lalu satu lompatan.")

    p(d, "Solusinya bukan menaikkan laju sensor lebih dulu — meskipun itu juga perlu (LC29H "
         "mendukung maksimum 10 Hz menurut datasheet-nya, sementara konfigurasi sekarang 1 Hz). "
         "Solusi yang lebih murah adalah **interpolasi di sisi klien** dengan buffer kecil: "
         "tampilkan posisi pada waktu `sekarang − latensi`, dan gerakkan secara halus menuju "
         "sampel berikutnya. Ini membuat gerakan terlihat kontinu tanpa menambah bandwidth, "
         "dengan konsekuensi bahwa yang terlihat adalah posisi **perkiraan**, bukan posisi "
         "terukur terakhir. Karena itu label latensi wajib ada.")

    h2(d, "5.5  Sinkronisasi waktu")
    p(d, "Ketika satu layar menampilkan posisi kendaraan, objek radar, dan video secara "
         "bersamaan, ketiganya harus berada pada waktu yang sama. Tanpa itu, replay insiden "
         "akan menampilkan objek yang belum ada saat tabrakan terjadi — dan kesimpulan "
         "investigasinya salah.")

    caption_table(d, 23, "Kebutuhan presisi waktu per jenis data")
    table(d, ["Data", "Presisi yang dibutuhkan", "Alasan", "Sarana"],
          [["Posisi armada", "±100 ms", "Pada 36 km/jam, 100 ms = 1 m pergeseran",
            "NTP di gateway (cukup)"],
           ["Objek radar", "±10 ms", "Objek bergerak cepat; salah waktu = salah posisi relatif",
            "PTP atau 1PPS dari modul GNSS"],
           ["Video (MDVR)", "±40 ms (1 frame)", "Untuk membuktikan urutan kejadian",
            "Timestamp JT808 + sinkronisasi berkala"],
           ["Telemetri mesin", "±500 ms", "Perubahan RPM/beban relatif lambat",
            "NTP di gateway"],
           ["Ortomosaik / peta", "Tidak relevan", "Data statis, ditandai tanggal survei",
            "Metadata tanggal di UI"]],
          widths=[3.2, 3.8, 5.4, 3.6], size=8.0)

    p(d, "Modul GNSS yang dipakai Minergo punya keunggulan yang jarang dimanfaatkan: output "
         "**1PPS dengan akurasi tipikal 100 ns** menurut datasheet LC29H. Pulsa ini bisa dipakai "
         "untuk menyelaraskan pencatatan waktu antar perangkat di satu kendaraan, tanpa "
         "memerlukan server PTP. Untuk tahap sekarang ini belum perlu, tetapi penting dicatat "
         "sebagai jalur yang sudah tersedia di perangkat yang ada.")

    h2(d, "5.6  Integrasi radar — di mana persisnya terhenti")
    p(d, "Saya perlu menjelaskan bagian ini dengan sangat spesifik, karena inilah perbedaan antara "
         "\"belum dikerjakan\" dan \"tidak bisa dikerjakan dengan perangkat ini\".")

    p(d, "Datasheet STONKAM PSA27 menyebutkan: frekuensi 76–77 GHz FMCW, jangkauan deteksi "
         "0,2–40 m, lebar pemantauan 0–20 m, hingga lima zona yang dapat dikonfigurasi, "
         "toleransi ±15 cm, sudut 120° horizontal dan 14° vertikal, proteksi IP69K, dan daya "
         "10–32 VDC. Semua ini adalah spesifikasi **deteksi**. Yang tidak ada dalam dokumen itu "
         "adalah spesifikasi **pelaporan**: format pesan objek, laju pembaruan objek, jumlah "
         "target maksimum, dan struktur protokol. Antarmuka yang disebut hanyalah konfigurasi "
         "(USB-to-UART atau Wi-Fi), satu input trigger, dan satu keluaran alarm.")

    p(d, "CISBO C95M lebih singkat lagi: 77 GHz, jangkauan 5 m × 6 m, FOV 180° horizontal, "
         "daya 9–36 VDC, dan antarmuka berupa **LED dan buzzer 80–100 dB**. Tidak ada klaim "
         "keluaran data.")

    p(d, "Kesimpulannya bukan bahwa perangkat ini buruk. Untuk fungsi aslinya — memperingatkan "
         "pengemudi akan halangan saat mundur — alarm adalah keluaran yang tepat, murah, dan "
         "andal. Masalahnya adalah **jenis keluaran yang berbeda dari yang dibutuhkan visualisasi**. "
         "Alarm bersifat biner: ada halangan, atau tidak. Visualisasi membutuhkan vektor: "
         "di mana, sejauh apa, pada sudut berapa.")

    caption_table(d, 24, "Perbandingan kontrak data — yang dibutuhkan vs yang tersedia")
    table(d, ["Yang dibutuhkan visualisasi", "PSA27", "C95M", "Radar kelas object-list"],
          [["Jarak objek (m)", "Tidak tersedia", "Tidak tersedia", "Ya"],
           ["Sudut azimut (°)", "Tidak tersedia", "Tidak tersedia", "Ya"],
           ["Kecepatan relatif", "Tidak tersedia", "Tidak tersedia", "Ya"],
           ["Jumlah objek bersamaan", "Tidak tersedia", "Tidak tersedia", "Ya (biasanya 20–64)"],
           ["Laju pembaruan objek", "Tidak tersedia", "Tidak tersedia", "Ya (10–20 Hz)"],
           ["Alarm biner / zona", "**Ya**", "**Ya**", "Ya"],
           ["Dokumen protokol publik", "**TIDAK DITEMUKAN**", "**TIDAK DITEMUKAN**",
            "Sebagian (NDA)"],
           ["Antarmuka data", "USB-UART (konfigurasi), alarm", "LED + buzzer",
            "CAN FD / Ethernet / UART"]],
          widths=[4.6, 3.6, 3.4, 4.4], size=7.9)

    callout(d, "Batas yang saya tolak untuk dilewati",
            "Saya bisa saja menggambar panel radar yang tampak meyakinkan di wireframe — "
            "beberapa titik oranye bergerak di sekitar truk — dan tidak ada yang akan tahu "
            "bedanya sampai integrasi sebenarnya dimulai. Saya memilih tidak melakukannya. "
            "Panel radar pada wireframe Bab 7 digambar **kosong dengan keterangan** alasan "
            "ketidaktersediaannya, dan itu justru menyampaikan informasi yang lebih berguna "
            "kepada pengambil keputusan daripada animasi palsu: bahwa ada pekerjaan pengadaan "
            "atau negosiasi vendor yang harus diselesaikan lebih dulu.",
            "FBE3E4", "E11B22", "KEPUTUSAN")

    h2(d, "5.7  Kontrak data yang harus diminta ke vendor")
    p(d, "Bila jalur yang dipilih adalah tetap memakai perangkat yang ada, berikut adalah "
         "spesifikasi minimum yang harus diminta. Saya tuliskan dalam bentuk yang bisa langsung "
         "dikirim sebagai surat, karena dokumen ini akan dipakai untuk itu.")

    code_block(d, """
Permintaan informasi teknis — integrasi data radar ke sistem visualisasi

Untuk setiap model radar yang kami gunakan, kami memerlukan:

 1. Daftar perintah/protokol untuk membaca OBJECT LIST (bukan hanya status alarm),
    termasuk format frame, checksum, dan contoh byte stream nyata.

 2. Spesifikasi object list:
      - jumlah target maksimum per frame
      - laju pembaruan (Hz)
      - besaran yang dilaporkan per target (jarak, azimut, elevasi,
        kecepatan relatif, RCS, ID pelacakan)
      - resolusi dan akurasi masing-masing besaran

 3. Apakah tersedia SDK, driver, atau contoh kode (C/C++/Python)?
    Apakah tersedia di bawah NDA? Berapa lama prosesnya?

 4. Antarmuka fisik yang tersedia untuk data (bukan konfigurasi):
    UART / CAN / CAN FD / Ethernet? Pinout dan level tegangan?

 5. Konfirmasi jangkauan dan FOV untuk model yang kami miliki, dalam dokumen
    resmi bertanda tangan — bukan halaman pemasaran.

 6. Apakah perangkat dapat mengeluarkan data mentah (raw ADC/cube) selain
    object list? Bila ya, dengan antarmuka apa dan laju berapa?
""", size=7.2)


# ══════════════════════════════════════════════════════════════════════════
def bab6(d):
    h1(d, "6  ARSITEKTUR YANG DIUSULKAN")

    h2(d, "6.1  Prinsip perancangan")
    p(d, "Arsitektur ini saya susun dengan lima prinsip yang lahir langsung dari temuan "
         "sebelumnya — bukan dari pola umum. Setiap prinsip menjawab satu masalah yang sudah "
         "terbukti ada, bukan masalah yang dibayangkan.")

    caption_table(d, 25, "Prinsip arsitektur dan masalah nyata yang diaturnya")
    table(d, ["Prinsip", "Masalah yang dijawab", "Konsekuensi konkret"],
          [["**Pisahkan bidang data dari bidang tampilan**",
            "67,1% sampel RTK berstatus FLOAT, dan laju 1 Hz; tampilan tidak boleh mengikuti "
            "data mentah apa adanya",
            "Ada lapisan normalisasi dan buffer; klien menerima data yang sudah berskema"],
           ["**Satu skema kanonik, banyak adapter**",
            "Format sumber beragam: NMEA, CSV, GeoTIFF, JSON",
            "Setiap sumber punya adapter kecil; tidak ada logika format di dalam viewer"],
           ["**Tandai ketidakpastian, jangan sembunyikan**",
            "Kelas akurasi berbeda jauh antar sampel",
            "Kualitas adalah field wajib; UI menampilkannya; trail diberi warna menurut kualitas"],
           ["**Mode adalah status, bukan setelan**",
            "Risiko pengguna salah membaca live sebagai replay atau sebaliknya",
            "Indikator mode selalu tampil, tidak bisa disembunyikan"],
           ["**Pekerjaan berat di server, bukan di klien**",
            "Tablet lapangan dengan 4 GB RAM",
            "Tiling, LOD, dan agregasi dilakukan sekali di server, bukan per klien"]],
          widths=[4.4, 5.6, 6.2], size=8.0)

    h2(d, "6.2  Diagram arsitektur")
    p(d, "Diagram berikut menunjukkan empat lapis sistem, dari sensor di lapangan sampai viewer "
         "di browser. Yang perlu diperhatikan adalah dua garis putus-putus merah: keduanya "
         "menandai sambungan yang **belum ada kontrak datanya**, dan sengaja digambar begitu "
         "supaya celahnya terlihat, bukan tersembunyi.")

    figure(d, f"{DIA}/arsitektur.png",
           "Arsitektur empat lapis. Kotak merah (radar) adalah satu-satunya sumber yang belum "
           "punya kontrak data; kotak kuning (survei drone) adalah sumber batch, bukan streaming.",
           number=6, width_cm=16.0)

    h2(d, "6.3  Penjelasan setiap lapis")
    h3(d, "Lapis 1 — sumber data")
    p(d, "Lima sumber, dengan sifat yang berbeda dan karena itu harus diperlakukan berbeda. "
         "**GNSS/RTK** mengeluarkan NMEA pada 1 Hz. **Telemetri unit** keluar sebagai CSV per "
         "perjalanan — bukan streaming, melainkan berkas yang diunduh setelah perjalanan selesai. "
         "**Kamera/MDVR** mengeluarkan video dengan timestamp JT808. **Radar** mengeluarkan "
         "alarm biner. **Survei drone** menghasilkan ortomosaik yang diperbarui berkala, "
         "bukan setiap detik.")

    p(d, "Perbedaan sifat ini penting: tiga sumber bersifat streaming (GNSS, kamera, radar "
         "bila kelak ada), satu sumber semi-batch (telemetri), dan satu sumber batch (drone). "
         "Menyamakan perlakuan terhadap kelimanya akan menghasilkan arsitektur yang boros.")

    h3(d, "Lapis 2 — ingestion dan normalisasi")
    p(d, "Gateway tepi bertugas tiga hal yang tidak boleh diserahkan ke server pusat: memberi "
         "cap waktu saat data **tiba** (bukan saat diproses), menyangga data ketika jaringan "
         "hilang, dan mengirim ulang secara berurutan ketika jaringan kembali. Di tambang, "
         "jaringan hilang adalah keadaan normal, bukan pengecualian.")

    p(d, "Adapter bertugas mengubah format asli menjadi skema kanonik Bab 5.1. Satu adapter per "
         "sumber, masing-masing kecil dan dapat diuji sendiri. Ini pekerjaan yang tampak "
         "membosankan tetapi menentukan: bila adapter benar, seluruh sistem di atasnya menjadi "
         "sederhana; bila adapter bocor, kompleksitasnya menyebar ke mana-mana.")

    h3(d, "Lapis 3 — backend")
    p(d, "Empat komponen dengan tanggung jawab yang sengaja dipisah. **Penyimpanan deret waktu** "
         "menyimpan posisi dan telemetri — ini yang membuat replay mungkin. **Penyimpanan geo "
         "dan aset** menyimpan geofence, geometri haul road, dan tile 3D. **Mesin aturan** "
         "mengevaluasi kondisi (kecepatan melebihi batas di dalam zona, keluar geofence, idle "
         "terlalu lama) dan mengeluarkan event. **Layanan real-time** menyebarkan data ke klien "
         "lewat WebSocket, dan melayani query replay lewat REST.")

    p(d, "Pemisahan mesin aturan dari layanan real-time bukan formalitas arsitektur. Alasannya "
         "operasional: aturan keselamatan berubah lebih sering daripada kode penyajian, dan "
         "aturan yang salah harus bisa diperbaiki tanpa menyentuh jalur data. Selain itu, mesin "
         "aturan bisa diuji dengan data historis — \"apakah aturan baru ini akan menandai "
         "kejadian bulan lalu?\" — dan itu kemampuan yang sangat berharga untuk validasi.")

    h3(d, "Lapis 4 — viewer 3D")
    p(d, "Viewer adalah lapisan yang paling terlihat, tetapi dalam arsitektur ini justru yang "
         "paling tipis logikanya. Ia menerima tile dari server, posisi dari WebSocket, dan "
         "menggambar. Semua kecerdasan ada di lapis 2 dan 3. Prinsip ini menjaga viewer tetap "
         "bisa diganti — dan pada kenyataannya ia **akan** diganti, karena teknologi render "
         "berubah lebih cepat daripada skema data.")

    h2(d, "6.4  Tiga jalur data: live, replay, simulasi")
    p(d, "Ketiga mode di Bab 2.6 bukan tiga tampilan, melainkan tiga jalur data yang berbeda. "
         "Menggambarnya terpisah membuat konsekuensi teknisnya terlihat jelas.")

    figure(d, f"{DIA}/alur_data.png",
           "Tiga jalur data. Jalur LIVE dan REPLAY berbagi viewer yang sama; jalur SIMULASI "
           "memakai viewer yang sama tetapi sumber datanya skenario buatan, dan wajib berlabel.",
           number=7)

    p(d, "Perhatikan bahwa jalur LIVE menulis ke arsip. Ini keputusan yang disengaja: replay "
         "tidak dibangun sebagai fitur terpisah, melainkan sebagai **konsekuensi** dari "
         "penyimpanan yang benar. Bila jalur live menyimpan data kanonik secara konsisten, "
         "replay hampir gratis. Bila tidak, replay harus dibangun ulang dengan cara khusus — "
         "dan itulah yang biasanya terjadi pada proyek yang tidak merancangnya dari awal.")

    h2(d, "6.5  Di mana komponen diletakkan (on-premise)")
    p(d, "Satu persyaratan yang saya anggap tidak bisa dinegosiasikan: **sistem harus berjalan "
         "tanpa internet publik.** Alasannya bukan paranoia, melainkan kenyataan operasional — "
         "jaringan tambang sering terputus, dan koordinat serta data produksi tidak seharusnya "
         "keluar dari jaringan perusahaan. Ini juga risiko R-8.")

    caption_table(d, 26, "Penempatan komponen dan ketergantungan pada internet")
    table(d, ["Komponen", "Lokasi", "Butuh internet publik?", "Catatan"],
          [["Gateway tepi", "Di site, dekat perangkat", "Tidak", "Harus tahan putus jaringan"],
           ["Backend & basis data", "Server on-premise", "Tidak", "Akses via VPN untuk tim pusat"],
           ["Tile 3D & ortomosaik", "Server file on-premise", "Tidak", "Di-generate sekali di server"],
           ["Viewer (browser)", "Disajikan dari server lokal", "Tidak", "Tanpa CDN, tanpa token"],
           ["Peta dasar (bila perlu)", "Tile lokal (self-host)", "Tidak", "MapLibre + tile sendiri"],
           ["Font / pustaka JS", "Di-bundle, bukan CDN", "Tidak", "Build statis"]],
          widths=[3.6, 4.4, 3.2, 5.0], size=8.0)

    p(d, "Poin terakhir terlihat sepele tetapi sering menjatuhkan sistem di lapangan: aplikasi "
         "yang memuat font atau pustaka dari CDN akan kehilangan tampilannya ketika internet "
         "putus, dan gejalanya sulit didiagnosis karena kodenya benar. Semua dependensi harus "
         "di-bundle dalam build.")

    h2(d, "6.6  Yang sengaja tidak saya masukkan ke arsitektur")
    p(d, "Sama pentingnya dengan apa yang ada: beberapa hal populer yang sengaja saya tinggalkan, "
         "dengan alasan.")

    bullets(d, [
        "**Microservices.** Untuk beban satu tambang dengan puluhan unit, empat komponen yang "
        "disebut di atas cukup sebagai satu atau dua proses. Memecahnya menjadi belasan layanan "
        "menambah biaya operasional tanpa manfaat.",
        "**Kubernetes.** Satu server on-premise tidak membutuhkan orkestrasi klaster. "
        "Docker Compose sudah memadai dan jauh lebih mudah dirawat oleh tim kecil.",
        "**Event streaming platform (Kafka dan sejenisnya).** Untuk 60 unit pada 1–10 Hz, "
        "yaitu ratusan pesan per detik, broker ringan atau bahkan WebSocket langsung sudah cukup. "
        "Kafka berguna pada skala ribuan perangkat.",
        "**WebGPU sebagai syarat.** Dukungan 86,83% berarti 13% perangkat gagal, dan itu "
        "terlalu banyak untuk perangkat kantor. WebGL2 dulu, WebGPU sebagai peningkatan.",
        "**Digital twin permukaan (cut/fill).** Menggiurkan dan sering diminta, tetapi butuh "
        "DSM/point cloud yang belum ada. Memasukkannya ke arsitektur sekarang berarti "
        "merancang untuk data yang tidak dimiliki.",
    ])

    p(d, "Daftar ini bukan penolakan terhadap teknologi tersebut. Ini penundaan yang sadar: "
         "setiap komponen yang tidak dimasukkan adalah satu hal yang tidak perlu dirawat, "
         "diperbarui, dan dipelajari oleh tim yang kecil. Arsitektur yang baik untuk Minergo "
         "bukan arsitektur yang paling lengkap, melainkan yang paling mudah dioperasikan oleh "
         "tiga orang.")
