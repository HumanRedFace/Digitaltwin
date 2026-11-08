"""BAB 7–9: wireframe, kelayakan & risiko, rekomendasi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_lib import (h1, h2, h3, p, pr, bullets, numbered, table, figure, caption_table,
                     callout, code_block, GREY)
import data as D

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
WF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wireframe")
DIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")


# ══════════════════════════════════════════════════════════════════════════
def bab7(d):
    h1(d, "7  KONSEP TAMPILAN (WIREFRAME)")

    h2(d, "7.1  Dasar perancangan")
    p(d, "Wireframe ini bukan gambar hiasan sebelum aplikasi dibuat. Ia adalah alat uji "
         "keputusan: dengan menggambar layar secara spesifik, menjadi jelas informasi apa yang "
         "harus tersedia, siapa yang harus menyediakannya, dan apa yang terjadi bila tidak ada. "
         "Beberapa keputusan di Bab 5 dan Bab 6 lahir justru dari proses menggambar ini — "
         "misalnya keharusan menampilkan kelas akurasi, dan keputusan menampilkan panel radar "
         "dalam keadaan kosong.")

    p(d, "Tiga aturan yang saya pegang dalam menggambar:")

    numbered(d, [
        "**Setiap angka di layar harus punya sumber.** Bila sebuah angka tidak bisa dihitung "
        "dari data yang ada, ia tidak boleh muncul. Itulah sebabnya panel radar kosong.",
        "**Ketidakpastian harus terlihat, bukan tersembunyi.** Warna trail menunjukkan kualitas "
        "posisi; label latensi selalu tampil; mode (LIVE/REPLAY/SIMULASI) tidak bisa "
        "disembunyikan.",
        "**Ponsel bukan versi kecil dari desktop.** Pada layar kecil, kolom kanan tidak "
        "dilipat menjadi ikon-ikon kecil — ia diganti dengan lembar bawah yang muncul saat "
        "unit dipilih. Prioritasnya peta, bukan panel.",
    ])

    callout(d, "Apa yang sedang dilihat pembaca",
            "Gambar pada bab ini adalah **rancangan**, bukan tangkapan layar aplikasi yang sudah "
            "jadi. Angka yang muncul di dalamnya diambil dari data lapangan nyata: RTK 28 Oktober "
            "2026 (kecepatan 27,4 km/h, 41 satelit, HDOP 0,44, status FLOAT, course beku 1,1 s), "
            "ortomosaik 14 Oktober 2026 (1,35 cm/px), dan hasil uji render Lampiran C "
            "(88 fps, 3 draw call). Aplikasinya belum dibangun — itu di luar lingkup riset ini.",
            "FDF7EC", "C8892A", "PERINGATAN")

    h2(d, "7.2  Layar desktop — mode LIVE")
    p(d, "Tata letak desktop mengikuti satu prinsip: **peta adalah raja**. Viewport 3D menempati "
         "sekitar 61% lebar layar, dan semua panel lain adalah pendukung yang bisa dipindai dalam "
         "satu pandangan tanpa mengalihkan perhatian dari peta.")

    figure(d, f"{WF}/wireframe_desktop.png",
           "Wireframe desktop 1920×1080, mode LIVE. Panel kiri: navigasi dan lapisan. "
           "Tengah: viewport 3D dengan armada, geofence, dan tooltip unit. "
           "Kanan: ringkasan armada, peringatan, panel radar (kosong), dan performa. "
           "Bawah: timeline 30 menit dengan penanda kejadian.", number=8, width_cm=16.0)

    h3(d, "Keputusan desain pada layar desktop")
    caption_table(d, 27, "Keputusan desain desktop dan alasannya")
    table(d, ["Elemen", "Keputusan", "Alasan"],
          [["Tab mode", "LIVE berwarna merah, selalu di kiri atas; tidak bisa disembunyikan",
            "Mencegah kesalahan paling mahal: mengira melihat keadaan sekarang padahal bukan"],
           ["Indikator latensi", "`● LATENCY 840 ms` di bar atas, dengan titik hijau/kuning/merah",
            "Angka konkret lebih jujur daripada ikon \"terhubung\""],
           ["Warna trail", "Hijau untuk FIX, kuning untuk FLOAT",
            "Pengguna melihat sendiri di mana posisi bisa dipercaya, tanpa membaca tabel"],
           ["Label unit", "Kode unit + status kualitas + kecepatan, dalam satu baris",
            "Menjawab \"siapa itu dan bisakah dipercaya\" tanpa klik"],
           ["Penanda masalah", "Lingkaran merah pada unit yang melanggar geofence, "
                               "dengan teks di bawahnya",
            "Tidak bergantung pada warna saja — penting untuk pengguna buta warna"],
           ["Panel radar", "Kosong, dengan keterangan mengapa",
            "Kejujuran lebih berguna daripada animasi yang tidak bisa diwujudkan"],
           ["Timeline", "Segmen berwarna menurut kualitas RTK",
            "Memperlihatkan bahwa kualitas berubah sepanjang waktu, bukan seragam"],
           ["Skala & kompas", "Keduanya kecil di sudut, tidak mencolok",
            "Dibutuhkan untuk orientasi, tetapi tidak boleh bersaing dengan data"]],
          widths=[3.0, 6.4, 6.8], size=7.9)

    p(d, "Satu elemen yang mungkin terlihat aneh: panel **PERFORMA VIEWER** di kanan bawah "
         "menampilkan \"88 fps · 3 draw call · 11,3 ms/frame\". Menampilkan metrik teknis kepada "
         "dispatcher memang tidak lazim. Saya memasukkannya karena dua alasan: pertama, ia "
         "memungkinkan pengguna melaporkan masalah kinerja dengan angka, bukan dengan kalimat "
         "\"aplikasinya lambat\"; kedua, ia adalah pengingat permanen bagi tim pengembang bahwa "
         "anggaran render itu nyata dan terukur.")

    h2(d, "7.3  Layar tablet — mode LIVE")
    p(d, "Untuk perangkat lapangan, tata letaknya berubah secara mendasar. Bukan karena layarnya "
         "kecil, tetapi karena **situasinya berbeda**: pengawas berdiri di luar, sering dengan "
         "sarung tangan, dan tidak sedang menganalisis — ia sedang memverifikasi satu hal "
         "tentang satu unit.")

    figure(d, f"{WF}/wireframe_mobile.png",
           "Wireframe tablet/telepon, mode LIVE. Peta mengisi hampir seluruh layar; "
           "detail unit muncul sebagai lembar bawah saat unit disentuh, "
           "dengan empat metrik besar dan dua aksi.", number=9, width_cm=8.4)

    caption_table(d, 28, "Perbedaan keputusan desain desktop vs perangkat lapangan")
    table(d, ["Aspek", "Desktop", "Tablet / telepon", "Alasan perbedaan"],
          [["Porsi peta", "61% lebar", "≈93% lebar", "Lapangan: peta adalah satu-satunya hal "
                                                     "yang penting"],
           ["Detail unit", "Panel kanan permanen", "Lembar bawah saat dipilih",
            "Tidak ada ruang untuk panel permanen"],
           ["Jumlah metrik", "Lima baris + tabel", "Empat angka besar",
            "Dibaca sambil berdiri, sering di bawah matahari"],
           ["Ukuran sentuh", "Klik presisi", "Target ≥ 44 px",
            "Sarung tangan dan gerakan tangan"],
           ["Timeline", "Penuh dengan penanda", "Ringkas, hanya posisi waktu",
            "Navigasi replay dilakukan di tempat duduk, bukan di lapangan"],
           ["Panel radar", "Ada (kosong, dengan keterangan)", "Tidak ada",
            "Tidak berguna bila tidak ada data; menghemat ruang"]],
          widths=[2.8, 4.2, 4.2, 5.0], size=7.9)

    h2(d, "7.4  Hierarki informasi")
    p(d, "Satu pertanyaan yang saya ajukan pada diri sendiri saat menggambar: bila pengguna hanya "
         "melihat layar selama tiga detik, apa yang harus ia dapat? Jawabannya menentukan urutan "
         "prioritas visual. Saya menyusunnya menjadi tiga lapis.")

    caption_table(d, 29, "Hierarki informasi — tiga lapis perhatian")
    table(d, ["Lapis", "Isi", "Waktu baca", "Perlakuan visual"],
          [["1 — Sekilas", "Mode (LIVE/REPLAY), jumlah unit aktif, ada/tidak peringatan, "
                           "lokasi unit bermasalah",
            "< 1 detik", "Warna jenuh, ukuran besar, posisi tetap"],
           ["2 — Pemindaian", "Posisi & heading tiap unit, status kualitas, kecepatan, "
                              "batas geofence",
            "2–5 detik", "Ukuran sedang, warna terkendali"],
           ["3 — Pendalaman", "HDOP, jumlah satelit, umur koreksi, riwayat lintasan, "
                              "detail telemetri",
            "> 5 detik, perlu klik", "Abu-abu, ukuran kecil, di panel"]],
          widths=[3.0, 7.4, 2.8, 3.0], size=8.0)

    p(d, "Kesalahan yang paling sering terjadi dalam dashboard operasional adalah menempatkan "
         "informasi lapis 3 di area lapis 1 — misalnya menampilkan HDOP dengan huruf besar di "
         "tengah layar. Informasi itu penting, tetapi bukan untuk tiga detik pertama. Ia harus "
         "tersedia, bukan menonjol.")

    h2(d, "7.5  Elemen yang sengaja tidak digambar")
    p(d, "Beberapa fitur yang sering muncul dalam demo digital twin sengaja tidak saya masukkan, "
         "dan alasannya perlu dicatat supaya tidak dianggap kelalaian.")

    bullets(d, [
        "**Animasi roda berputar dan suspensi.** Menghabiskan anggaran render untuk hal yang "
        "tidak menambah keputusan apa pun. Pada pandangan operasional (kamera jauh), detail ini "
        "tidak terlihat.",
        "**Efek bayangan real-time dan refleksi.** Indah untuk pemasaran, mahal untuk perangkat "
        "lapangan. Bayangan statis sederhana sudah cukup untuk memberi kesan kedalaman.",
        "**Panah animasi arus lalu lintas.** Terlihat mengesankan di presentasi, tetapi "
        "menutupi data sebenarnya. Bila ingin menunjukkan arah, gunakan heading unit yang nyata.",
        "**Panel radar berisi titik objek.** Inilah yang paling sering diminta, dan justru yang "
        "paling tidak bisa dipertanggungjawabkan dengan perangkat saat ini.",
        "**Grafik 3D batang untuk KPI.** Tiga dimensi pada grafik batang selalu mengurangi "
        "keterbacaan dibanding dua dimensi. Untuk KPI, gunakan grafik 2D.",
    ])

    p(d, "Ada satu benang merah dalam daftar ini: semua yang saya tinggalkan adalah hal yang "
         "**menambah kesan** tanpa menambah **informasi**. Dalam sistem operasional, kesan yang "
         "berlebihan justru berbahaya karena membuat orang percaya pada tampilan lebih dari yang "
         "seharusnya.")


# ══════════════════════════════════════════════════════════════════════════
def bab8(d):
    h1(d, "8  ANALISIS KELAYAKAN DAN RISIKO")

    h2(d, "8.1  Kerangka penilaian")
    p(d, "Kelayakan saya nilai pada lima dimensi yang terpisah, karena sebuah proyek bisa layak "
         "secara teknis tetapi tidak layak secara operasional — dan itu kejadian yang sangat "
         "umum. Menilai kelima dimensi secara terpisah memaksa saya menyebutkan di mana "
         "sebenarnya kekuatannya dan di mana kelemahannya.")

    caption_table(d, 30, "Penilaian kelayakan per dimensi")
    table(d, ["Dimensi", "Penilaian", "Dasar", "Catatan"],
          [["**Teknis**", "LAYAK",
            "Scene target 88,2 fps pada GPU terintegrasi; seluruh format aset standar "
            "(glTF, 3D Tiles, COG); pustaka yang dipakai berlisensi bebas",
            "Satu-satunya komponen yang tidak layak secara teknis adalah data radar — "
            "dan itu masalah kontrak data, bukan kemampuan render"],
           ["**Data**", "LAYAK SEBAGIAN",
            "Ortomosaik, RTK, model 3D, dan telemetri tersedia dan terukur. "
            "DSM, point cloud, geofence, dan object list radar tidak ada",
            "Cukup untuk memulai; tidak cukup untuk seluruh use case"],
           ["**Operasional**", "LAYAK dengan syarat",
            "Data 1 Hz dan 67,1% FLOAT membatasi ketepatan; interpolasi + label kualitas "
            "membuatnya dapat dipakai untuk pemantauan, bukan untuk keputusan hukum",
            "Perlu kesepakatan tertulis tentang apa yang boleh disimpulkan dari tampilan"],
           ["**Biaya**", "LAYAK",
            "Seluruh pustaka inti gratis. Biaya utama adalah jam-orang dan satu server on-premise",
            "Risiko biaya ada pada layanan hosted (Cesium ion, Mapbox) — dihindari dengan self-host"],
           ["**SDM & perawatan**", "PERLU PERHATIAN",
            "Butuh kompetensi web 3D + geospasial + backend data. Tim kecil bisa, "
            "tetapi menjadi bottleneck bila hanya satu orang",
            "Risiko kebergantungan pada satu orang (bus factor) harus dikelola"]],
          widths=[2.8, 2.8, 6.6, 4.0], size=7.9)

    h2(d, "8.2  Apa yang layak dikerjakan sekarang")
    p(d, "Berdasarkan penilaian di atas, ada pekerjaan yang bisa dimulai tanpa menunggu keputusan "
         "atau pengadaan apa pun. Ini penting: studi kelayakan yang berakhir dengan \"tunggu\" "
         "adalah studi yang gagal.")

    caption_table(d, 31, "Pekerjaan yang layak dimulai sekarang, tanpa prasyarat")
    table(d, ["Pekerjaan", "Prasyarat", "Keluaran", "Risiko"],
          [["Konversi ortomosaik ke tile yang bisa di-stream",
            "Tidak ada — berkas sudah ada", "Peta dasar 3D yang bisa dibuka di browser", "Rendah"],
           ["Pipeline aset model 3D (merge + LOD + Draco/KTX2)",
            "Tidak ada — model sudah ada", "Model armada yang ringan dan siap instancing", "Rendah"],
           ["Skema kanonik + adapter NMEA/CSV",
            "Tidak ada", "Data lapangan yang seragam dan bisa diputar ulang", "Rendah"],
           ["Viewer armada dasar (posisi + heading + trail)",
            "Tiga hal di atas", "Demo UC-1 yang bisa dinilai pengguna", "Rendah"],
           ["Pembuatan geofence dari citra",
            "Butuh waktu surveyor, bukan pengadaan", "Poligon zona yang bisa dipakai aturan", "Rendah"],
           ["Uji beban pada perangkat target sebenarnya",
            "Satu laptop & satu tablet milik perusahaan", "Angka fps nyata di lapangan",
            "Rendah"]],
          widths=[5.4, 4.2, 4.4, 2.2], size=7.9)

    h2(d, "8.3  Apa yang belum layak, dan prasyaratnya")
    p(d, "Sebaliknya, ada pekerjaan yang tampak paling menarik tetapi harus menunggu. Menuliskan "
         "prasyaratnya membuat penundaan ini dapat ditindaklanjuti, bukan sekadar ditunda.")

    caption_table(d, 32, "Pekerjaan yang belum layak dan prasyarat yang harus dipenuhi")
    table(d, ["Pekerjaan", "Mengapa belum layak", "Prasyarat yang harus selesai lebih dulu"],
          [["Objek terdeteksi radar (UC-4)",
            "Perangkat yang ada hanya mengeluarkan alarm biner; tidak ada object list",
            "Dokumen protokol / SDK dari vendor (V-1 s.d. V-4), **atau** pengadaan unit "
            "ber-object-list"],
           ["Twin permukaan / cut-fill (UC-6)",
            "Tidak ada DSM maupun point cloud; ortomosaik hanya 2D",
            "Survei drone dengan overlap memadai + pengolahan ke LAS/COPC (V-6)"],
           ["Simulasi skenario (UC-5)",
            "Belum ada model aturan maupun data historis yang cukup untuk kalibrasi",
            "Skema kanonik berjalan minimal 3 bulan agar ada data pembanding"],
           ["Peringatan keselamatan otomatis berbasis posisi",
            "67,1% sampel FLOAT; kesalahan posisi bisa > 1 m",
            "Kenaikan fix rate (perbaikan lokasi antena/base) **atau** kesepakatan bahwa "
            "peringatan bersifat indikatif"],
           ["Multi-site / globe",
            "Belum ada kebutuhan yang terverifikasi; menambah kompleksitas signifikan",
            "Keputusan bisnis, bukan keputusan teknis"]],
          widths=[4.2, 5.8, 6.2], size=7.9)

    h2(d, "8.4  Risiko — daftar dan penilaian")
    p(d, "Saya menilai risiko dengan perkalian dampak dan kemungkinan (skala 1–3), sehingga skor "
         "9 adalah yang tertinggi. Yang penting bukan angkanya, melainkan **mitigasinya**: "
         "risiko yang tidak punya mitigasi jelas seharusnya menghentikan proyek, bukan hanya "
         "dicatat.")

    caption_table(d, 33, "Daftar risiko teknis dan operasional")
    rows = []
    for rid, risiko, dampak, kemungkinan, skor, mitigasi in D.RISIKO:
        rows.append([rid, risiko, dampak, kemungkinan, str(skor), mitigasi])
    table(d, ["ID", "Risiko", "Dampak", "Kemungkinan", "Skor", "Mitigasi"],
          rows, widths=[1.2, 5.2, 1.9, 2.2, 1.2, 6.5], size=7.4, align_center={0, 2, 3, 4})

    h2(d, "8.5  Dua risiko yang paling menentukan")
    p(d, "Dari sepuluh risiko di atas, dua mendapat skor tertinggi (9) dan keduanya layak "
         "dibahas lebih panjang karena sifatnya berbeda: satu berasal dari luar kendali tim, "
         "satu sepenuhnya di dalam kendali tim.")

    h3(d, "R-1 — Kontrak data radar tidak tersedia")
    p(d, "Ini risiko eksternal. Mitigasinya bukan pekerjaan teknis, melainkan pengadaan dan "
         "negosiasi. Yang bisa dilakukan tim R&D sekarang hanyalah menyiapkan surat permintaan "
         "(Bab 5.7) dan menyiapkan jalur mundur: bila vendor tidak bisa menyediakan object list, "
         "pilihannya adalah mengganti unit radar dengan kelas yang menyediakannya — dan itu "
         "keputusan manajemen, dengan konsekuensi biaya pengadaan dan sertifikasi ulang.")

    p(d, "Yang tidak boleh dilakukan adalah menganggap risiko ini akan hilang sendiri setelah "
         "integrasi dimulai. Pengalaman umum menunjukkan sebaliknya: tanpa dokumen protokol, tim "
         "akan menghabiskan berminggu-minggu mencoba menebak format melalui eksperimen, dan "
         "sering tidak berhasil karena datanya memang tidak dikeluarkan.")

    h3(d, "R-2 — Draw call meledak karena model tidak dioptimasi")
    p(d, "Ini risiko internal, dan justru karena itu paling bisa dikendalikan — sekaligus paling "
         "sering terjadi. Angka pengukurannya sudah saya dapat: 14.003 draw call menghasilkan "
         "14,3 fps, sementara 3 draw call menghasilkan 116,8 fps untuk geometri yang sama. "
         "Selisihnya 8,5 kali.")

    p(d, "Mitigasinya bukan \"hati-hati saat mengimpor model\", melainkan **pipeline yang "
         "memaksa**. Setiap aset yang masuk harus melewati pemeriksaan otomatis: berapa draw "
         "call, berapa material, berapa tekstur, berapa segitiga. Aset yang melewati ambang "
         "ditolak secara otomatis, bukan diberi peringatan yang bisa diabaikan. Ini keputusan "
         "proses, dan nilainya lebih besar daripada keputusan teknologi mana pun dalam dokumen ini.")

    callout(d, "Mengapa R-2 lebih penting daripada pilihan mesin",
            "Selisih kinerja antara mesin render yang berbeda di kelas yang sama biasanya berada "
            "dalam kisaran 1,5–2 kali. Selisih antara aset yang dioptimasi dan tidak dioptimasi "
            "yang saya ukur adalah **8,5 kali**. Artinya: tim yang memilih mesin terbaik tetapi "
            "mengabaikan pipeline aset akan kalah dari tim yang memilih mesin biasa tetapi "
            "membangun pipeline yang disiplin. Ini temuan yang saya anggap paling berharga dari "
            "seluruh riset ini.",
            "EEF3F8", "2E6E9E", "TEMUAN")

    h2(d, "8.6  Gap teknis yang harus ditutup")
    caption_table(d, 34, "Gap teknis terverifikasi dan cara menutupnya")
    rows = []
    for gid, gap, dampak, cara in D.GAP:
        rows.append([gid, gap, dampak, cara])
    table(d, ["ID", "Gap", "Dampak bila tidak ditutup", "Cara menutup"],
          rows, widths=[1.2, 4.8, 4.6, 5.6], size=7.6, align_center={0})

    h2(d, "8.7  Kesimpulan kelayakan")
    p(d, "Digital twin 3D untuk Minergo **layak**, dengan tiga pembatasan yang harus diterima "
         "secara sadar:")

    numbered(d, [
        "**Layak untuk pemantauan dan investigasi, belum layak untuk keputusan keselamatan "
        "otomatis.** Kualitas posisi (67,1% FLOAT, 1 Hz) cukup untuk melihat dan memutar ulang, "
        "tidak cukup untuk menegakkan aturan yang berakibat hukum.",
        "**Layak untuk armada dan area, belum layak untuk objek radar.** Perbedaan ini bukan "
        "soal teknologi render, melainkan ketersediaan kontrak data dari perangkat.",
        "**Layak dengan tim kecil, tetapi tidak layak dengan satu orang.** Kompetensi yang "
        "dibutuhkan mencakup web 3D, geospasial, dan backend data — tiga bidang yang jarang "
        "dikuasai satu orang secara mendalam.",
    ])

    p(d, "Dengan tiga pembatasan itu diterima dan dituliskan, sisa pekerjaannya adalah pekerjaan "
         "rekayasa biasa: jelas, terukur, dan bisa dipecah menjadi sprint. Itu posisi yang baik "
         "untuk memulai — jauh lebih baik daripada proyek yang dijanjikan bisa melakukan "
         "segalanya sejak hari pertama.")


# ══════════════════════════════════════════════════════════════════════════
def bab9(d):
    h1(d, "9  REKOMENDASI DAN LANGKAH LANJUT")

    h2(d, "9.1  Rekomendasi teknologi")
    p(d, "Rekomendasi ini saya susun sebagai keputusan berlapis, bukan satu pilihan tunggal. "
         "Alasannya: keputusan yang paling mengikat bukanlah mesin render, melainkan pipeline "
         "aset dan skema data — dan keduanya tetap sama apa pun mesin yang dipilih.")

    caption_table(d, 35, "Rekomendasi teknologi per lapis, dengan tingkat keyakinan")
    table(d, ["Lapis", "Rekomendasi", "Keyakinan", "Alasan pokok"],
          [["Format aset", "**glTF 2.0 (.glb) + Draco + KTX2**", "Tinggi",
            "Standar Khronos; format tile wajib 3D Tiles 1.1; ekosistem kompresi matang"],
           ["Tile geospasial", "**3D Tiles 1.1**, di-self-host", "Tinggi",
            "Standar OGC; CesiumJS dan 3d-tiles-renderer sama-sama membacanya"],
           ["Peta raster", "**COG (Cloud Optimized GeoTIFF)** + tile XYZ lokal", "Tinggi",
            "Bisa dibaca sebagian; tidak perlu unduh 400 MB untuk melihat satu area"],
           ["Mesin render", "**CesiumJS** sebagai basis", "Sedang",
            "Skor terbobot tertinggi (3,97); menyelesaikan geodesi & 3D Tiles tanpa kode tambahan"],
           ["Alternatif mesin", "**Three.js + 3d-tiles-renderer**", "Sedang",
            "Skor 3,80; lebih fleksibel & talenta lebih mudah; geodesi harus ditulis sendiri"],
           ["Peta dasar vektor", "**MapLibre GL JS** (BSD-3)", "Tinggi",
            "Bebas lisensi; Mapbox GL JS sejak v2.0 proprietary"],
           ["Basis data deret waktu", "**PostgreSQL + PostGIS**", "Sedang",
            "Sudah umum, satu basis data untuk waktu & geometri; TimescaleDB bila volume naik"],
           ["Transport real-time", "**WebSocket** (MQTT di sisi perangkat)", "Tinggi",
            "Cukup untuk ratusan pesan/detik; tidak perlu Kafka"],
           ["Penyajian", "**On-premise, tanpa CDN, tanpa token pihak ketiga**", "Tinggi",
            "Risiko R-8; jaringan tambang tidak selalu tersedia"]],
          widths=[3.0, 4.6, 2.0, 6.6], size=7.9)

    h3(d, "Mengapa CesiumJS, meskipun selisihnya tipis")
    p(d, "Selisih 3,97 berbanding 3,80 hanya 4,3% — cukup kecil sehingga keputusannya harus "
         "dijelaskan, bukan hanya diumumkan. Ada tiga alasan yang menurut saya membenarkan "
         "pilihan CesiumJS untuk **pekerjaan pertama**:")

    numbered(d, [
        "Pekerjaan pertama yang bernilai adalah menempatkan tambang dan armada pada koordinat "
        "yang benar. Itu justru bagian yang harus ditulis sendiri bila memakai Three.js — "
        "dan bagian itu bukan pekerjaan sepele: konversi geodetik, pemilihan origin lokal, "
        "penanganan presisi saat kamera jauh, serta terrain.",
        "Ortomosaik Minergo berada di UTM 50S dan harus tampil tepat di atas permukaan. "
        "CesiumJS menangani konversi dan penempatan ini secara bawaan.",
        "Bila kelak dibutuhkan tampilan multi-site atau data elevasi regional, CesiumJS sudah "
        "siap; Three.js memerlukan penulisan ulang lapisan bumi.",
    ])

    p(d, "Namun saya menambahkan satu syarat yang penting: **pipeline aset harus dibangun "
         "netral-mesin.** Artinya, konversi ke glTF/3D Tiles dilakukan oleh alat terpisah "
         "(glTF-Transform, GDAL, alat tiling), bukan di dalam kode aplikasi. Dengan begitu, "
         "bila di tengah jalan CesiumJS ternyata terlalu membatasi tampilan, perpindahan ke "
         "Three.js hanya mengganti lapisan render — bukan membangun ulang seluruh sistem.")

    h2(d, "9.2  Peta jalan bertahap")
    p(d, "Urutan fase disusun berdasarkan satu aturan: **setiap fase harus menghasilkan sesuatu "
         "yang bisa dinilai pengguna**, bukan hanya kemajuan teknis. Fase yang tidak menghasilkan "
         "apa pun yang bisa dilihat berisiko kehilangan dukungan sebelum selesai.")

    caption_table(d, 36, "Peta jalan bertahap dan keluarannya")
    rows = []
    for sprint, durasi, isi, keluar in D.ROADMAP:
        rows.append([sprint, durasi, isi, keluar])
    table(d, ["Tahap", "Durasi", "Isi", "Keluaran yang bisa dinilai"],
          rows, widths=[2.2, 2.2, 7.6, 4.2], size=7.9, align_center={1})

    p(d, "Perhatikan bahwa Fase 4 (radar) ditempatkan **setelah** tiga fase yang tidak "
         "bergantung padanya. Ini keputusan yang disengaja: bila kontrak data radar ternyata "
         "tidak diperoleh, tiga fase pertama tetap menghasilkan sistem yang berguna, dan "
         "proyek tidak berhenti total. Ini pola yang dalam manajemen risiko disebut mengurangi "
         "ketergantungan pada jalur kritis tunggal.")

    h2(d, "9.3  Estimasi effort")
    p(d, "Angka di bawah adalah **asumsi**, bukan komitmen. Dasarnya adalah pengalaman umum "
         "proyek sejenis, bukan pengukuran — dan saya menandainya begitu supaya tidak dipakai "
         "sebagai dasar kontrak.")

    caption_table(d, 37, "Estimasi effort per fase (jam-orang) — ASUMSI")
    rows = []
    total_lo, total_hi = 0, 0
    for fase, lo, hi, tim in D.EFFORT:
        rows.append([fase, f"{lo}–{hi}", tim])
        total_lo += lo
        total_hi += hi
    rows.append(["**Total**", f"**{total_lo}–{total_hi}**", "—"])
    table(d, ["Fase", "Jam-orang", "Komposisi tim"], rows,
          widths=[8.6, 3.2, 4.4], size=8.0, align_center={1})

    p(d, f"Total {total_lo}–{total_hi} jam-orang. Bila dikerjakan dua orang penuh waktu "
         f"(sekitar 160 jam-orang per bulan), rentangnya setara 4,5 sampai 7,6 bulan — "
         f"dengan asumsi tidak ada gangguan prioritas lain. Untuk konteks: tiga fase pertama "
         f"(fondasi, viewer, geofence) hanya {sum(e[1] for e in D.EFFORT[:3])}–"
         f"{sum(e[2] for e in D.EFFORT[:3])} jam-orang, yaitu sekitar sepertiga dari total, "
         f"dan sudah menghasilkan sistem yang bisa dipakai.")

    callout(d, "Cara membaca estimasi ini",
            "Angka jam-orang di atas **tidak** termasuk: pengadaan perangkat, survei drone "
            "tambahan, sertifikasi keamanan, pelatihan pengguna, dan perawatan setelah rilis. "
            "Dalam pengalaman umum, keempat hal itu menambah 30–50% dari biaya pengembangan. "
            "Angka ini juga mengasumsikan tim sudah menguasai stack web; bila harus belajar "
            "dari nol, tambahkan 20–30%.",
            "FDF7EC", "C8892A", "CATATAN")

    h2(d, "9.4  Keputusan yang saya minta")
    p(d, "Dokumen riset yang berakhir tanpa permintaan keputusan adalah dokumen yang akan "
         "didiamkan. Karena itu saya menutup dengan empat keputusan spesifik, masing-masing "
         "dengan pemilik yang jelas.")

    caption_table(d, 38, "Keputusan yang diminta, pemilik, dan tenggat yang diusulkan")
    table(d, ["No", "Keputusan", "Pemilik", "Tenggat usulan", "Konsekuensi bila ditunda"],
          [["K-1", "Menyetujui Fase 0–1 (fondasi koordinat + viewer armada) sebagai langkah "
                   "berikutnya", "Kepala R&D + PMO", "2 minggu",
            "Tidak ada kemajuan; tim kehilangan momentum dan data tetap tidak terpakai"],
           ["K-2", "Mengirim surat permintaan SDK/object list ke STONKAM dan CISBO",
            "Procurement + R&D", "1 minggu",
            "UC-4 tidak bisa dimulai; bila ditunda terlalu lama, Fase 4 harus dikeluarkan "
            "dari anggaran tahun ini"],
           ["K-3", "Menetapkan target platform: browser (CesiumJS/Three.js) atau desktop (Unity)",
            "Kepala R&D", "3 minggu",
            "Perekrutan dan pelatihan tidak bisa dimulai; risiko R-7 meningkat"],
           ["K-4", "Menyepakati batas penggunaan: pemantauan & investigasi, bukan keputusan "
                   "hukum otomatis", "Manajemen + Safety", "3 minggu",
            "Risiko tampilan dipakai melebihi kemampuannya — risiko reputasi dan hukum"]],
          widths=[1.1, 5.4, 3.0, 2.2, 4.5], size=7.7, align_center={0, 3})

    h2(d, "9.5  Pertanyaan terbuka untuk vendor dan PIC")
    p(d, "Daftar ini adalah keluaran langsung dari gap yang tidak bisa diselesaikan tim R&D "
         "sendiri. Setiap pertanyaan disertai alasan mengapa jawabannya menentukan.")

    caption_table(d, 39, "Pertanyaan terbuka dan dampaknya bila tidak terjawab")
    dampak = {
        "V-1": "Menentukan apakah UC-4 mungkin sama sekali",
        "V-2": "Menentukan apakah objek bisa digambar mulus atau hanya berkedip",
        "V-3": "Menentukan apakah radar CISBO bisa dipakai untuk visualisasi",
        "V-4": "Angka 120 m tidak dapat diverifikasi; salah pakai = salah rancangan",
        "V-5": "Menaikkan laju sampel mengurangi lompatan 3 m antar posisi",
        "V-6": "Menentukan apakah twin permukaan (cut/fill) mungkin",
        "V-7": "Menentukan apakah arsitektur on-premise dapat disetujui",
    }
    rows = []
    for vid, pihak, pertanyaan in D.PERTANYAAN_VENDOR:
        rows.append([vid, pihak, pertanyaan, dampak.get(vid, "—")])
    table(d, ["ID", "Pihak", "Pertanyaan", "Menentukan"],
          rows, widths=[1.1, 2.6, 8.0, 4.5], size=7.6, align_center={0})

    h2(d, "9.6  Penutup")
    p(d, "Saya menutup dokumen ini dengan satu pengamatan yang menurut saya paling penting, "
         "dan yang mungkin tidak diharapkan dari sebuah studi kelayakan teknologi.")

    p(d, "Temuan terbesar dari riset ini bukanlah tentang mesin 3D mana yang lebih baik, atau "
         "tentang berapa fps yang bisa dicapai. Temuan terbesarnya adalah bahwa **selisih antara "
         "aset yang dirapikan dan tidak dirapikan (8,5 kali) jauh lebih besar daripada selisih "
         "antar mesin render (1,5–2 kali)**, dan bahwa **bahan baku digital twin sudah ada di "
         "folder Minergo hari ini** — ortomosaik tergeoreferensi, log RTK satu jam perjalanan "
         "nyata, model kendaraan berdetail tinggi, dan riwayat telemetri.")

    p(d, "Artinya, hambatan utama bukanlah teknologi yang belum dibeli atau perangkat keras yang "
         "belum tersedia. Hambatannya adalah pekerjaan yang membosankan dan tidak terlihat: "
         "mendefinisikan skema data, merapikan aset, membangun pipeline konversi, dan menulis "
         "adapter. Pekerjaan itu tidak menghasilkan demo yang mengesankan, tetapi justru itulah "
         "yang menentukan apakah sistem ini akan berfungsi atau hanya akan menjadi presentasi "
         "yang bagus.")

    p(d, "Satu hal terakhir, tentang apa yang saya sengaja tidak lakukan. Sepanjang dokumen ini "
         "ada beberapa tempat di mana saya bisa membuat laporan terlihat lebih lengkap: "
         "mengisi panel radar dengan animasi, mengisi kolom DSM dengan perkiraan, atau "
         "menuliskan angka fps yang belum diukur. Saya memilih tidak melakukannya, dan "
         "menandai setiap tempat itu sebagai celah yang harus ditutup. Bukan karena kerendahan "
         "hati, tetapi karena keputusan yang dibangun di atas angka karangan akan gagal di "
         "lapangan — dan kegagalan itu akan terjadi setelah anggaran habis, bukan sebelum.")

    hrule_close(d)


def hrule_close(d):
    from doc_lib import hrule, p as para, GREY
    hrule(d)
    para(d, "Dokumen ini disusun berdasarkan data yang tersedia di lingkungan R&D Minergo per "
            "8 November 2026, ditambah pengukuran mandiri dan dokumen vendor resmi. Seluruh "
            "angka yang ditandai TERVERIFIKASI dapat direproduksi dengan skrip pada Lampiran C. "
            "Angka yang ditandai KLAIM VENDOR atau ASUMSI tidak boleh dipakai sebagai dasar "
            "komitmen tanpa validasi lanjutan.",
         size=8.4, italic=True, color=GREY)
