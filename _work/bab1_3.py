"""BAB 1–3: pendahuluan, use case, riset teknologi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_lib import (h1, h2, h3, p, pr, bullets, numbered, table, figure, caption_table,
                     callout, code_block, GREY)
import data as D

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
DIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")


# ══════════════════════════════════════════════════════════════════════════
def bab1(d):
    h1(d, "1  PENDAHULUAN, LINGKUP, DAN CARA KERJA")

    h2(d, "1.1  Latar belakang")
    p(d, "Saya mulai riset ini bukan dari keinginan membuat sesuatu yang tampak canggih, "
         "tetapi dari satu pertanyaan yang sangat praktis: ketika seorang dispatcher melihat "
         "lima truk di layar, apakah yang ia lihat itu benar-benar posisi truk di tambang, "
         "atau hanya gambar truk yang ditempel di atas peta? Perbedaan antara keduanya adalah "
         "seluruh isi dari kata \"digital twin\".")

    p(d, "Pengertian yang saya pakai sepanjang dokumen ini sengaja sempit dan dapat diuji: "
         "digital twin 3D adalah representasi visual yang **ditempatkan pada koordinat bumi yang "
         "sama** dengan objek aslinya, diperbarui dari data sensor, dan dapat diputar ulang. "
         "Kalau sebuah tampilan tidak memenuhi tiga hal itu — benar koordinatnya, hidup dari sensor, "
         "dan bisa diputar ulang — maka ia adalah visualisasi, bukan twin. Pembeda ini penting "
         "karena menentukan apakah hasilnya boleh dipakai untuk keputusan operasional atau tidak.")

    p(d, "Kebutuhan ini muncul dari tiga arah yang berbeda di Minergo. Pertama, **operasi**: "
         "pengaturan armada di jalur angkut masih bergantung pada radio dan peta 2D, sehingga "
         "dispatcher sulit melihat siapa berada di mana ketika ada antrean di dumping point. "
         "Kedua, **keselamatan**: investigasi insiden hampir selalu terkendala karena data posisi, "
         "kecepatan, dan waktu tersebar di beberapa berkas dengan format berbeda. Ketiga, "
         "**perencanaan**: survei drone sudah menghasilkan ortomosaik beresolusi tinggi, tetapi "
         "hasilnya berhenti sebagai berkas gambar yang dibuka di aplikasi GIS, tidak pernah masuk "
         "ke ruang kerja operasional harian.")

    p(d, "Ketiga arah itu bertemu di satu titik: tidak ada satu tempat di mana data spasial "
         "tambang bisa dilihat, diputar, dan ditanyai bersama-sama. Riset ini menilai seberapa "
         "jauh titik itu bisa dicapai.")

    h2(d, "1.2  Tujuan riset")
    numbered(d, [
        "Merumuskan use case digital twin 3D yang benar-benar sesuai kebutuhan R&D Minergo, "
        "bukan daftar fitur umum.",
        "Mengidentifikasi teknologi visualisasi 3D yang tersedia, beserta lisensi, biaya, "
        "kebutuhan hardware, dan effort penerapannya.",
        "Menyusun kebutuhan data minimum dan menilai kesiapan data yang **sudah** dimiliki.",
        "Merancang arsitektur integrasi dari perangkat/sensor sampai ke layar, termasuk "
        "penanganan waktu dan sistem koordinat.",
        "Membuat rancangan konseptual (wireframe) tampilan 3D Viewer.",
        "Menilai kelayakan, risiko, batasan, dan gap teknis secara jujur.",
        "Menyusun rekomendasi teknologi, estimasi effort, dan opsi keputusan lanjut.",
    ])

    h2(d, "1.3  Pengguna yang dituju")
    p(d, "Saya memetakan pengguna berdasarkan keputusan yang mereka ambil, bukan berdasarkan "
         "jabatan. Cara ini membuat setiap fitur punya alasan keberadaan.")
    caption_table(d, 4, "Pengguna, keputusan yang diambil, dan implikasinya pada tampilan")
    table(d, ["Pengguna", "Keputusan yang diambil", "Yang dibutuhkan dari layar", "Prioritas"],
          [["Dispatcher / Control Room", "Unit mana yang dikirim ke titik mana, dan kapan",
            "Posisi seluruh armada, status antrean, jalur terpakai, riwayat 30 menit terakhir", "Tertinggi"],
           ["Pengawas Keselamatan", "Apakah ada pelanggaran zona/kecepatan yang perlu ditindak",
            "Geofence, riwayat pelanggaran, replay kejadian, bukti waktu", "Tertinggi"],
           ["Mine Planning / Survey", "Apakah progres tambang sesuai rancangan",
            "Ortomosaik terbaru, batas pit, elevasi, perbandingan antar survei", "Sedang"],
           ["Manajemen / PMO", "Apakah investasi ini berjalan dan berdampak",
            "Ringkasan KPI, tren, bukan detail teknis", "Sedang"],
           ["R&D / Engineering", "Apakah arsitektur dan data cukup untuk fitur berikutnya",
            "Akses mentah, log, metrik kinerja, dokumentasi skema", "Tertinggi"]],
          widths=[3.2, 4.6, 6.4, 2.0], size=8.2)

    h2(d, "1.4  Lingkup dan batas tegas")
    p(d, "Batasan lingkup ini bukan formalitas. Tanpa batas yang jelas, studi kelayakan mudah "
         "berubah menjadi janji implementasi, dan itu berbahaya bagi tim yang akan mengeksekusinya. "
         "Karena itu saya menuliskannya sebagai kontrak.")
    caption_table(d, 5, "Batas lingkup riset")
    table(d, ["Termasuk dalam riset ini", "TIDAK termasuk dalam riset ini"],
          [["Identifikasi use case dan kebutuhan pengguna",
            "Membangun aplikasi 3D yang berjalan"],
           ["Perbandingan teknologi visualisasi dan lisensinya",
            "Melakukan integrasi fisik ke sensor atau kendaraan"],
           ["Rancangan arsitektur dan alur data (diagram)",
            "Membuat PoC fungsional atau purwarupa yang diuji pengguna"],
           ["Rancangan konseptual tampilan (wireframe)",
            "Melakukan pengadaan perangkat keras"],
           ["Analisis kelayakan, risiko, gap, dan estimasi effort",
            "Menjamin akurasi data lapangan di luar data yang diserahkan"],
           ["Daftar pertanyaan teknis ke vendor/PIC",
            "Melakukan negosiasi atau kontrak dengan vendor"]],
          widths=[8.1, 8.1], size=8.4)

    callout(d, "Batas yang paling sering dilanggar dalam studi semacam ini",
            "Wireframe di Bab 7 **adalah gambar rancangan**, bukan tangkapan layar aplikasi. "
            "Angka yang muncul di dalamnya berasal dari data lapangan nyata dan hasil uji "
            "Lampiran C, tetapi aplikasinya belum ada. Saya menandainya berulang kali di dalam "
            "gambar itu sendiri supaya tidak ada yang salah paham saat gambar berpindah tangan.",
            "FDF7EC", "C8892A", "PERINGATAN")

    h2(d, "1.5  Metode kerja")
    p(d, "Saya membagi pekerjaan menjadi empat lapis, dari yang paling murah ke yang paling mahal. "
         "Urutan ini disengaja: setiap lapis harus menjawab pertanyaan lapis sebelumnya, sehingga "
         "tidak ada uang yang keluar untuk pertanyaan yang belum jelas.")

    caption_table(d, 6, "Empat lapis metode riset dan keluarannya")
    table(d, ["Lapis", "Pertanyaan", "Cara menjawab", "Keluaran"],
          [["1. Inventaris", "Apa yang benar-benar sudah kita punya?",
            "Membaca berkas nyata di folder internal: model 3D, ortomosaik, log RTK, telemetri. "
            "Mengukur propertinya, bukan memperkirakan.",
            "Lampiran E"],
           ["2. Pengukuran", "Apakah teknologi ini cukup cepat untuk beban kita?",
            "Menjalankan three.js di Chrome headless pada mesin ini, dengan sinkronisasi GPU, "
            "memakai aset Minergo sendiri.",
            "Bab 4, Lampiran C"],
           ["3. Perbandingan", "Teknologi mana yang paling sesuai, dengan kriteria terukur?",
            "Matriks berbobot 8 kriteria, skor 1–5, dengan catatan dasar setiap skor.",
            "Bab 3.6"],
           ["4. Perancangan", "Bagaimana bentuk arsitektur dan tampilannya?",
            "Diagram alur (graphviz) dan wireframe yang diperiksa tata letaknya secara terprogram.",
            "Bab 6, Bab 7"]],
          widths=[2.2, 4.4, 6.6, 3.0], size=8.2)

    h2(d, "1.6  Tingkat bukti dan kejujuran angka")
    p(d, "Sepanjang dokumen ini saya memakai lima label bukti yang sudah didefinisikan di "
         "Dokumen Kontrol. Alasannya sederhana: dalam riset teknologi, klaim vendor dan hasil "
         "ukur sering ditulis dengan kalimat yang sama, padahal bobotnya berbeda jauh. "
         "Mencampur keduanya adalah cara paling cepat untuk salah mengambil keputusan.")

    p(d, "Saya juga menetapkan satu aturan pribadi yang saya pegang ketat: **tidak ada satu angka "
         "pun di dokumen ini yang saya karang.** Kalau sebuah data tidak ada, saya tulis "
         "\"BELUM DITEMUKAN\" dan menjadikannya pertanyaan, bukan mengisinya dengan perkiraan "
         "yang tampak rapi. Ada beberapa tempat di mana konsekuensi aturan ini membuat laporan "
         "terlihat kurang lengkap — misalnya panel radar pada wireframe sengaja digambar dalam "
         "keadaan kosong dengan keterangan mengapa. Itu keputusan yang saya ambil sadar.")


# ══════════════════════════════════════════════════════════════════════════
def bab2(d):
    h1(d, "2  IDENTIFIKASI KEBUTUHAN DAN USE CASE")

    h2(d, "2.1  Cara saya menyaring use case")
    p(d, "Daftar use case digital twin di internet sangat panjang, dan hampir semuanya terdengar "
         "masuk akal. Karena itu saya memakai tiga saringan yang keras sebelum sebuah use case "
         "boleh masuk daftar:")

    numbered(d, [
        "**Saringan data**: apakah data yang dibutuhkan sudah ada, atau minimal bisa diperoleh "
        "dengan usaha yang wajar? Use case yang butuh sensor yang belum terpasang saya turunkan "
        "prioritasnya, sekeras apa pun keinginan untuk memasukkannya.",
        "**Saringan keputusan**: apakah ada orang yang akan mengambil keputusan berbeda karena "
        "melihat tampilan ini? Kalau tidak ada, itu hiasan.",
        "**Saringan risiko**: kalau tampilan ini salah, apa akibatnya? Use case yang salahnya "
        "berbahaya harus punya mekanisme kejelasan akurasi, bukan hanya tanda merah.",
    ])

    p(d, "Dari sekitar dua belas kandidat awal, enam yang lolos. Dua di antaranya — tepatnya "
         "yang paling sering dijanjikan vendor — justru mendapat status kesiapan data paling rendah. "
         "Itu temuan tersendiri, dan saya bahas di Bab 2.4.")

    h2(d, "2.2  Use case A — posisi relatif objek di sekitar kendaraan (radar)")
    p(d, "Ini use case yang paling sering diminta ketika orang membicarakan digital twin untuk "
         "kendaraan tambang: sebuah model truk di layar, dikelilingi oleh titik-titik objek yang "
         "terdeteksi radar, lengkap dengan jarak, sudut, dan status blind spot. Secara konsep "
         "ini sangat kuat — operator melihat apa yang tidak bisa ia lihat dari kabin, dan "
         "pengawas bisa menilai apakah zona bahaya benar-benar terlindungi.")

    p(d, "Yang ingin ditampilkan meliputi: posisi relatif objek terhadap kendaraan, jarak, "
         "sudut deteksi (azimut dan elevasi), luas cakupan yang terpantau, area yang **tidak** "
         "terpantau, serta status kesehatan sensor. Untuk keperluan investigasi, tampilan ini "
         "juga harus bisa diputar ulang bersama data posisi kendaraan pada saat kejadian.")

    p(d, "Masalahnya muncul saat saya memeriksa dokumen resmi perangkat yang dikaji Minergo. "
         "Datasheet STONKAM PSA27 mencantumkan frekuensi 76–77 GHz, jangkauan deteksi 0,2–40 m, "
         "lebar 0–20 m, hingga lima zona yang dapat dikonfigurasi, toleransi ±15 cm, dan sudut "
         "pancar 120° horizontal / 14° vertikal. Yang **tidak** tercantum: format data objek, "
         "laju pembaruan objek, maupun protokol untuk mengambil daftar target. Antarmuka yang "
         "disebut hanya konfigurasi lewat USB-to-UART atau Wi-Fi, satu input trigger, dan satu "
         "keluaran alarm.")

    p(d, "Dengan kata lain, perangkat itu dirancang untuk **membunyikan alarm**, bukan untuk "
         "**melaporkan objek**. Ini bukan cacat produk — untuk fungsinya sebagai sistem peringatan "
         "mundur, alarm sudah tepat. Tetapi untuk digital twin, alarm tidak bisa digambar: "
         "kita tidak tahu di mana objeknya, seberapa jauh, atau pada sudut berapa.")

    callout(d, "Kesimpulan jujur untuk Use Case A",
            "Use case ini **tidak dapat dimulai** dengan perangkat yang dikaji, dan saya tidak "
            "akan menggambarnya dengan animasi karangan. Jalur yang benar ada dua: "
            "(a) meminta SDK atau dokumen protokol object list ke vendor — ini pertanyaan V-1 "
            "sampai V-4 di Bab 9; atau (b) beralih ke unit radar yang sejak awal dirancang "
            "mengeluarkan object list, misalnya kelas yang menyebutkan integrasi ROS/ROS2 dan "
            "keluaran CAN FD / Automotive Ethernet. Opsi (b) adalah perubahan pengadaan, "
            "bukan perubahan perangkat lunak, dan itu keputusan manajemen.",
            "FBE3E4", "E11B22", "BLOCKER")

    h2(d, "2.3  Use case B — area operasional dan haul road (posisi armada, lintasan, geofence)")
    p(d, "Use case kedua bergerak pada skala yang berbeda: bukan sentimeter di sekitar bemper, "
         "tetapi kilometer di seluruh jalur angkut. Yang ditampilkan adalah armada bergerak di "
         "atas ortomosaik tambang yang sebenarnya, lengkap dengan jalur yang ditempuh, batas "
         "zona, dan status tiap unit.")

    p(d, "Keunggulan use case ini adalah **datanya sudah ada**. Ortomosaik drone di folder Validasi "
         "berukuran 23.249 × 17.296 piksel dengan resolusi 1,35 cm/piksel, tergeoreferensi ke "
         "EPSG:32750, mencakup area 314 × 234 meter atau 7,4 hektar. Log RTK berisi 3.601 titik "
         "selama 3.602 detik perjalanan nyata, dengan kecepatan rata-rata 10,8 km/jam dan "
         "jarak tempuh 10,9 km. Ini bukan data contoh — ini rekaman lapangan.")

    p(d, "Dari bahan itu, fitur minimum yang bisa dibangun tanpa menunggu apa pun adalah: "
         "posisi armada di atas ortomosaik, jejak lintasan dengan warna menurut kualitas RTK, "
         "geofence dengan aturan kecepatan dan zona terlarang, panel detail unit, dan pemutaran "
         "ulang riwayat. Semuanya adalah pekerjaan perangkat lunak di atas data yang sudah duduk "
         "di disk.")

    h2(d, "2.4  Perbandingan kesiapan dua use case")
    p(d, "Perbedaan antara dua use case ini begitu tajam sehingga saya menempatkannya sebagai "
         "grafik, bukan tabel. Sumbu tegak menunjukkan tingkat kesiapan; batang hijau adalah "
         "kesiapan data, batang kuning adalah kompleksitas pengerjaan. Idealnya sebuah use case "
         "berada di kiri-atas: data siap, kerumitan rendah.")

    figure(d, f"{IMG}/g6_usecase.png",
           "Kesiapan data berbanding kompleksitas pengerjaan untuk enam use case. "
           "UC-4 (radar) adalah satu-satunya yang kesiapan datanya rendah sekaligus "
           "kompleksitasnya tinggi.", number=1)

    p(d, "Pola yang terlihat jelas: nilai use case tidak berkorelasi dengan kesiapan datanya. "
         "UC-4 dinilai bernilai tinggi oleh hampir semua pihak yang saya tanyakan, tetapi "
         "datanya belum ada. Sebaliknya UC-1 dinilai tinggi **dan** datanya siap. Dalam "
         "perencanaan yang sehat, yang dikerjakan lebih dulu adalah yang tinggi nilainya dan "
         "siap datanya — bukan yang paling menarik untuk didemokan.")

    h2(d, "2.5  Daftar use case dan prioritas")
    caption_table(d, 7, "Enam use case yang lolos penyaringan, dengan status kesiapan data")
    rows = []
    for uid, nama, aktor, nilai, siap, kompleks in D.USE_CASE:
        rows.append([uid, nama, aktor, nilai, siap, kompleks])
    table(d, ["ID", "Use case", "Aktor utama", "Nilai", "Kesiapan data", "Kompleksitas"],
          rows, widths=[1.1, 5.6, 3.0, 1.4, 3.2, 1.9], size=7.8,
          align_center={0, 3, 5})

    h2(d, "2.6  Real-time, replay, dan simulasi — tiga mode yang tidak boleh dicampur")
    p(d, "Salah satu kesalahan paling berbahaya dalam sistem visualisasi operasional adalah "
         "membiarkan pengguna tidak tahu apakah yang ia lihat sedang terjadi sekarang, sudah "
         "terjadi, atau belum pernah terjadi sama sekali. Ketiganya bisa terlihat identik di layar. "
         "Karena itu saya menetapkan tiga mode dengan konsekuensi teknis yang berbeda.")

    caption_table(d, 8, "Tiga mode tampilan: sumber data, janji yang boleh dibuat, dan labelnya")
    table(d, ["Aspek", "LIVE", "REPLAY", "SIMULASI"],
          [["Sumber data", "Sensor langsung melalui gateway",
            "Arsip kanonik (tersimpan)", "Skenario buatan (JSON/CSV)"],
           ["Janji yang boleh dibuat", "\"Ini keadaan sekarang, dengan latensi tertentu\"",
            "\"Ini yang terjadi pada waktu itu\"", "\"Ini yang **akan** terjadi bila asumsi ini dipakai\""],
           ["Toleransi keterlambatan", "Harus < 2 detik, dan ditampilkan angkanya",
            "Tidak relevan — waktu bisa dipercepat/diperlambat", "Tidak relevan"],
           ["Label wajib di layar", "`LIVE` + angka latensi + waktu data terakhir",
            "`REPLAY` + rentang waktu + kecepatan putar", "`SIMULASI` + nama skenario + tanggal dibuat"],
           ["Risiko bila tidak dilabeli", "Pengguna mengira melihat keadaan nyata padahal data "
            "sudah 10 menit tertinggal",
            "Pengguna mengira sedang memantau operasi berjalan",
            "Skenario ramalan dipakai sebagai bukti kejadian nyata"],
           ["Kesiapan", "Sebagian — RTK ada, tetapi 1 Hz dan 67,1% FLOAT",
            "Tinggi — log historis sudah tersedia", "Rendah — perlu model dan aturan dulu"]],
          widths=[3.4, 4.4, 4.4, 4.0], size=7.9)

    p(d, "Keputusan desain yang saya ambil: mode bukan pilihan di menu pengaturan, melainkan "
         "**indikator yang selalu terlihat** di bagian atas layar, dengan warna berbeda. "
         "Pada wireframe Bab 7 hal ini digambar sebagai tab `LIVE` merah, `REPLAY` dan "
         "`SIMULASI` abu-abu. Ini murah dibuat dan mencegah kelas kesalahan yang paling mahal.")

    h2(d, "2.7  Kandidat fitur minimum (MVP konsep)")
    p(d, "Fitur minimum saya susun berdasarkan satu prinsip: satu layar harus bisa menjawab "
         "pertanyaan seorang dispatcher dalam waktu kurang dari sepuluh detik. Fitur di luar itu "
         "masuk daftar berikutnya, bukan daftar pertama.")

    caption_table(d, 9, "Kandidat fitur minimum dan alasannya")
    table(d, ["Fitur", "Menjawab pertanyaan", "Bergantung pada", "Masuk MVP?"],
          [["Peta 3D dasar dengan ortomosaik tergeoreferensi",
            "\"Di mana tambangnya, dan di mana jalannya?\"", "Ortomosaik (ADA)", "Ya"],
           ["Posisi armada + ikon berorientasi heading",
            "\"Siapa ada di mana, menghadap ke mana?\"", "RTK (ADA)", "Ya"],
           ["Jejak lintasan berwarna menurut kualitas posisi",
            "\"Apakah posisi ini bisa dipercaya?\"", "NMEA + atribut fix (ADA)", "Ya"],
           ["Panel detail unit (kecepatan, satelit, HDOP, status)",
            "\"Kenapa unit ini diam / aneh?\"", "Telemetri (ADA)", "Ya"],
           ["Geofence + aturan kecepatan + daftar pelanggaran",
            "\"Siapa melanggar, kapan?\"", "Poligon zona (perlu dibuat)", "Ya"],
           ["Pemutaran ulang riwayat dengan penanda kejadian",
            "\"Apa yang sebenarnya terjadi?\"", "Arsip kanonik (perlu skema)", "Ya"],
           ["Objek terdeteksi radar",
            "\"Apa yang ada di titik buta?\"", "Object list radar (TIDAK ADA)", "Tidak"],
           ["Simulasi skenario",
            "\"Bagaimana kalau jalurnya diubah?\"", "Model aturan (belum ada)", "Tidak"],
           ["Twin permukaan (cut/fill)",
            "\"Berapa volume terangkut?\"", "DSM/point cloud (TIDAK ADA)", "Tidak"]],
          widths=[5.0, 4.6, 4.2, 2.2], size=8.0, align_center={3})


# ══════════════════════════════════════════════════════════════════════════
def bab3(d):
    h1(d, "3  RISET TEKNOLOGI VISUALISASI 3D")

    h2(d, "3.1  Cara saya memilih kandidat")
    p(d, "Ada puluhan pustaka dan mesin 3D yang bisa dipakai. Saya memilih lima yang mewakili "
         "lima pendekatan berbeda, bukan lima produk yang mirip. Perbedaan pendekatan itulah yang "
         "menentukan, bukan perbedaan versi.")

    caption_table(d, 10, "Lima kandidat dan alasan masing-masing dimasukkan")
    table(d, ["Kandidat", "Pendekatan", "Alasan dimasukkan"],
          [["**CesiumJS**", "Mesin globe geospasial",
            "Satu-satunya yang sejak awal dirancang untuk menempatkan objek di bumi "
            "dengan CRS dan terrain yang benar."],
           ["**Three.js**", "Pustaka render 3D serbaguna",
            "Paling banyak dipakai untuk visualisasi kustom; kontrol penuh atas tampilan, "
            "tetapi semua urusan geodesi harus dibangun sendiri."],
           ["**Unity**", "Mesin game / aplikasi 3D",
            "Standar industri untuk twin yang butuh kualitas visual tinggi dan simulasi fisik; "
            "menjadi pembanding \"jalur berat\"."],
           ["**deck.gl**", "Kerangka visualisasi data besar di atas peta",
            "Kuat untuk jutaan titik dan layer data, sering dipakai untuk dashboard armada."],
           ["**Potree**", "Penampil point cloud khusus",
            "Pembanding khusus untuk data LiDAR/fotogrametri, yang akan datang di tahap berikutnya."],
          ],
          widths=[2.6, 4.0, 9.4], size=8.3)

    p(d, "Saya sengaja **tidak** memasukkan Mapbox GL JS sebagai kandidat utama meskipun sering "
         "muncul dalam diskusi internal. Alasannya bukan teknis: sejak versi 2.0 lisensinya bukan "
         "lagi open source, melainkan tunduk pada Mapbox TOS yang mengikat penggunaan pada akun "
         "dan produk Mapbox. Berkas lisensi di repositori menyatakannya secara eksplisit — lisensi "
         "\"terminates automatically if a developer no longer has a Mapbox account in good "
         "standing\". Untuk sistem internal yang harus bisa jalan tanpa kanal internet, itu "
         "ketergantungan yang tidak perlu. Saya memakai **MapLibre GL JS** (BSD-3-Clause, "
         "turunan Mapbox GL v1) sebagai padanan yang bebas.")

    h2(d, "3.2  Status lisensi — diperiksa dari berkas, bukan dari ingatan")
    p(d, "Untuk setiap kandidat saya membuka berkas lisensi atau metadata paket resminya, "
         "bukan mengandalkan pengetahuan umum. Ini penting karena lisensi perangkat lunak 3D "
         "sering berubah, dan satu kesalahan di sini bisa mengunci proyek secara hukum.")

    caption_table(d, 11, "Status lisensi dan biaya — diperiksa langsung dari sumber resmi")
    rows = []
    for nama, v in D.LISENSI.items():
        rows.append([nama, v["versi"], v["lisensi"], v["biaya"]])
    table(d, ["Perangkat", "Versi diperiksa", "Lisensi", "Biaya"], rows,
          widths=[3.4, 2.4, 4.6, 5.4], size=7.9)

    p(d, "Kesimpulan penting dari tabel ini: **keempat kandidat web gratis untuk dipakai secara "
         "komersial.** Yang berbayar bukan pustakanya, melainkan layanan di sekelilingnya — "
         "terrain dan citra satelit hosted (Cesium ion), ubin peta (Mapbox), dan lisensi mesin "
         "(Unity). Ini mengubah bentuk keputusan: pertanyaannya bukan \"mampu beli lisensi "
         "atau tidak\", tetapi \"mau bergantung pada layanan pihak ketiga atau tidak\".")

    callout(d, "Temuan yang layak dicatat",
            "Cesium ion — layanan yang paling sering dianggap wajib saat memakai CesiumJS — "
            "ternyata **tidak wajib**. CesiumJS sendiri Apache-2.0 dan dapat menyajikan 3D Tiles "
            "dari server sendiri. Yang gratis hanya untuk non-komersial pada paket Community; "
            "pemakaian komersial mulai $149/bulan per individu atau $524/bulan per tim, "
            "naik ke $499/$874 untuk paket Premium. Untuk Minergo, jalur paling murah adalah "
            "**self-host**: ortomosaik dan model sudah kita miliki, jadi tidak ada yang perlu "
            "di-stream dari layanan pihak ketiga.")

    h2(d, "3.3  Format aset dan model 3D")
    p(d, "Format bukan detail sepele. Format menentukan berapa lama model dimuat, berapa besar "
         "bandwidth yang dipakai, dan apakah model bisa dipakai di lebih dari satu mesin. "
         "Kesimpulan saya: **glTF 2.0 adalah format target**, dan itu bukan pilihan yang bisa "
         "dinegosiasikan.")

    p(d, "Alasannya berlapis. glTF 2.0 adalah standar Khronos yang menjadi format tile wajib pada "
         "3D Tiles 1.1 — spesifikasi OGC 22-025r4 yang disetujui 17 Desember 2022 dan diterbitkan "
         "12 Januari 2023. Pada versi 1.1, format lama (b3dm, i3dm, pnts) dinyatakan deprecated. "
         "Artinya memilih glTF sekarang berarti memilih format yang masih akan hidup ketika "
         "3D Tiles versi berikutnya keluar. glTF juga punya ekosistem kompresi yang matang: "
         "Draco untuk geometri, KTX2/Basis untuk tekstur, dan meshopt untuk keduanya.")

    p(d, "Satu perkembangan yang saya anggap penting untuk dicatat meski belum dipakai sekarang: "
         "ekstensi **KHR_gaussian_splatting** telah berstatus *Complete, Ratified by the Khronos "
         "Group*. Ini menstandarkan penyimpanan 3D Gaussian splatting di dalam glTF — teknik "
         "rekonstruksi scene dari foto yang dalam dua tahun terakhir menggantikan fotogrametri "
         "konvensional untuk kualitas visual. Untuk Minergo ini berarti: hasil rekonstruksi "
         "berbasis foto (termasuk dari drone) akan semakin mudah masuk ke pipeline glTF yang sama, "
         "tanpa jalur konversi khusus.")

    caption_table(d, 12, "Format aset yang direkomendasikan per jenis objek")
    table(d, ["Jenis aset", "Format target", "Catatan teknis", "Status di Minergo"],
          [["Model kendaraan", "glTF 2.0 binary (`.glb`) + Draco + KTX2",
            "Wajib digabung per material sebelum diekspor; lihat Bab 4",
            "**ADA** — 1,13 jt segitiga, 14.003 mesh"],
           ["Terrain / permukaan", "3D Tiles 1.1 (glTF tile) atau mesh terpotong",
            "Butuh DSM. Tanpa DSM, terrain tetap datar",
            "**TIDAK ADA** — hanya ortomosaik 2D"],
           ["Ortomosaik", "COG (Cloud Optimized GeoTIFF) atau XYZ tile",
            "COG memungkinkan baca sebagian tanpa unduh seluruh berkas",
            "**ADA** — 23.249 × 17.294 px, EPSG:32750"],
           ["Point cloud", "COPC (Cloud Optimized Point Cloud) atau 3D Tiles",
            "COPC = LAZ yang bisa dibaca per rentang; jauh lebih efisien dari LAS penuh",
            "**TIDAK ADA**"],
           ["Objek bergerak (armada)", "Bukan model 3D — transformasi + `InstancedMesh`",
            "Satu geometri truk, N matriks. Ini kunci kinerja (Bab 4)",
            "**ADA**"],
           ["Garis & poligon (jalan, geofence)", "GeoJSON, di-*extrude* saat runtime",
            "Jangan panggang jadi mesh — harus bisa diedit tanpa re-export",
            "**SEBAGIAN** — shapefile Minergo kosong (0 geometri)"]],
          widths=[3.0, 4.2, 5.4, 3.4], size=7.7)

    p(d, "Satu catatan dari inventaris: berkas `Minergo.shp` di folder GIS berukuran 252 byte — "
         "artinya tidak berisi geometri apa pun. Berkas `.prj`-nya menyatakan WGS 84 geografis. "
         "Jadi peta vektor tambang **belum ada**; yang ada baru ortomosaik raster. Ini masuk "
         "daftar gap G-2.")

    h2(d, "3.4  Perbandingan arsitektur: apa yang sebenarnya berbeda")
    p(d, "Perbedaan paling menentukan di antara kelima kandidat bukanlah kualitas gambar, "
         "melainkan **siapa yang mengurus bumi**. Ini pertanyaan arsitektural, dan jawabannya "
         "menentukan berapa banyak kode yang harus ditulis tim Minergo.")

    p(d, "CesiumJS membawa bumi di dalam dirinya: objek `Ellipsoid`, `TerrainProvider`, "
         "`Cesium3DTileset`, dan konversi ECEF sudah menjadi bagian inti. Ketika saya menaruh "
         "sebuah model di koordinat −1,22941 / 116,89412, CesiumJS yang menghitung letaknya di "
         "bumi, termasuk lengkungan permukaan dan tinggi ellipsoid. Three.js tidak melakukan "
         "apa pun dari itu. Three.js hanya tahu ruang Kartesius: satu unit adalah satu unit, "
         "tanpa arti geografis. Memakai Three.js untuk tambang berarti saya harus menulis sendiri "
         "konversi geodetik, pemilihan titik acuan lokal, penanganan pergeseran saat kamera jauh "
         "dari origin, dan pemotongan terrain. Itu bukan pekerjaan mustahil — banyak proyek "
         "melakukannya — tetapi itu pekerjaan yang **nyata** dan harus masuk estimasi.")

    caption_table(d, 13, "Siapa yang mengurus apa — perbandingan tanggung jawab arsitektural")
    table(d, ["Tanggung jawab", "CesiumJS", "Three.js", "Unity", "deck.gl"],
          [["Konversi koordinat bumi", "Bawaan", "Tulis sendiri", "Plugin/aset", "Sebagian"],
           ["Terrain 3D", "Bawaan (quantized mesh)", "Tulis sendiri", "Aset + LOD manual", "Terbatas"],
           ["Streaming 3D Tiles", "Bawaan", "Pustaka tambahan", "Plugin pihak ketiga", "Bawaan"],
           ["LOD otomatis", "Bawaan", "Manual", "Bawaan", "Bawaan"],
           ["Kontrol tampilan penuh", "Terbatas (opinionated)", "Penuh", "Penuh", "Sedang"],
           ["Jalan di browser tanpa instalasi", "Ya", "Ya", "Build WebGL (terbatas)", "Ya"],
           ["Instanced rendering", "Ya", "Ya (`InstancedMesh`)", "Ya (GPU instancing)", "Ya"],
           ["Point cloud jutaan titik", "3D Tiles", "Manual / pustaka", "Plugin", "Kuat"]],
          widths=[4.4, 3.4, 3.4, 3.0, 2.0], size=7.9, align_center={1, 2, 3, 4})

    h2(d, "3.5  Kebutuhan hardware klien")
    p(d, "Ini bagian yang sering diabaikan dalam studi kelayakan, padahal di lapangan justru "
         "inilah yang menentukan apakah sistem dipakai atau ditinggalkan. Penggunanya bukan "
         "orang di depan workstation mahal — mereka dispatcher dengan laptop kantor dan pengawas "
         "dengan tablet di dalam kendaraan.")

    p(d, "Yang saya ukur di mesin ini: WebGPU sudah tersedia di Chrome dan menurut caniuse "
         "mencakup 86,83% pengguna global (data Oktober 2026). Namun angka itu menyesatkan bila "
         "dipakai untuk keputusan: 13% sisanya bukan tersebar merata, melainkan terkonsentrasi "
         "pada perangkat lama dan browser perusahaan yang terkunci versinya — persis jenis "
         "perangkat yang sering ada di kantor tambang. Karena itu untuk tahap awal saya "
         "merekomendasikan **WebGL2 sebagai target minimum**, dengan WebGPU sebagai jalur "
         "peningkatan bila tersedia, bukan sebagai syarat.")

    caption_table(d, 14, "Perkiraan kebutuhan hardware klien per skenario")
    table(d, ["Skenario", "Perangkat", "Yang harus jalan", "Risiko"],
          [["Dispatcher (kantor)", "Laptop kantor, GPU terintegrasi, 8 GB RAM",
            "Scene penuh: terrain + ortomosaik + 60 unit + trail",
            "Rendah — sudah diuji pada kelas mesin ini"],
           ["Pengawas (lapangan)", "Tablet Android / iPad, 4 GB RAM",
            "Peta + armada + panel unit, tanpa mode dekoratif",
            "Sedang — perlu mode hemat & LOD lebih kasar"],
           ["Dinding kontrol (TV)", "PC dengan GPU diskrit, 4K",
            "Scene penuh, kamera otomatis berputar",
            "Rendah"],
           ["Investigator (replay)", "Laptop kantor",
            "Replay 1 jam, banyak trail sekaligus",
            "Sedang — perlu strategi streaming arsip"]],
          widths=[3.2, 4.4, 5.6, 3.8], size=8.0)

    h2(d, "3.6  Matriks keputusan berbobot")
    p(d, "Saya menyusun delapan kriteria dengan bobot yang mencerminkan prioritas proyek ini, "
         "lalu memberi skor 1–5 per kandidat. Bobot dan dasar setiap skor saya tulis terbuka, "
         "supaya hasilnya bisa dibantah — matriks yang tidak bisa dibantah biasanya tidak "
         "dipercaya.")

    caption_table(d, 15, "Kriteria penilaian dan bobotnya")
    table(d, ["Kriteria", "Bobot", "Mengapa sebesar itu"],
          [[k[0], f"{k[1]*100:.0f}%", k[2]] for k in D.KRITERIA],
          widths=[6.4, 1.6, 8.2], size=8.2, align_center={1})

    figure(d, f"{IMG}/g3_skor.png",
           "Skor per kriteria untuk lima kandidat. Perhatikan bahwa tidak ada kandidat yang "
           "unggul di semua kriteria — pola inilah yang membuat keputusan menjadi trade-off, "
           "bukan pilihan tunggal yang jelas benar.", number=2)

    p(d, "Catatan kejujuran yang harus menyertai grafik ini: **hanya Three.js yang benar-benar "
         "saya ukur** pada mesin ini (Bab 4). Skor baris \"kinerja render\" untuk empat kandidat "
         "lain adalah penilaian berdasarkan arsitektur dan laporan umum, bukan hasil uji "
         "setara. Saya menandainya secara eksplisit di `data.py` lewat variabel `TERUKUR` "
         "supaya tidak ada yang membacanya sebagai perbandingan apel-ke-apel.")

    figure(d, f"{IMG}/g4_total.png",
           "Skor terbobot. Selisih CesiumJS (3,97) dan Three.js (3,80) hanya 4,3% — cukup kecil "
           "sehingga tidak boleh dijadikan satu-satunya dasar keputusan.", number=3)

    h2(d, "3.7  Membaca hasil: mengapa selisihnya kecil, dan apa artinya")
    p(d, "CesiumJS menang tipis. Kemenangannya datang hampir seluruhnya dari satu kriteria "
         "dengan bobot terbesar: kesesuaian geospasial, tempat ia mendapat skor 5 karena "
         "memang itu inti produknya. Three.js mendapat 2 pada kriteria itu, tetapi menang pada "
         "talenta, lisensi, dan kebutuhan hardware klien.")

    p(d, "Selisih 4,3% ini terlalu kecil untuk dijadikan keputusan tunggal, dan saya tidak akan "
         "berpura-pura sebaliknya. Yang lebih berguna adalah membaca **bentuk** hasilnya:")

    bullets(d, [
        "**CesiumJS adalah pilihan yang benar bila targetnya tambang sebagai globe.** Kalau "
        "Minergo ingin suatu hari menampilkan beberapa site sekaligus, atau menggabungkan "
        "ortomosaik dengan data elevasi regional, CesiumJS sudah menyelesaikan itu sebelum "
        "baris kode pertama ditulis.",
        "**Three.js adalah pilihan yang benar bila targetnya satu alat operasional yang sangat "
        "dikustomisasi.** Kontrol penuh atas tampilan, tidak ada opinion yang harus dilawan, "
        "dan talenta web paling mudah dicari.",
        "**Kombinasi keduanya bukan kompromi yang buruk**: CesiumJS untuk scene bumi dan "
        "3D Tiles, dengan overlay kustom yang digambar memakai primitif tingkat rendah. "
        "Banyak proyek produksi berakhir di titik ini.",
        "**Unity hanya masuk akal bila ada kebutuhan simulasi fisik atau kualitas render "
        "sinematik.** Untuk dashboard operasional, ia menambah lisensi, ukuran distribusi, dan "
        "pemisahan talenta tanpa manfaat yang sepadan.",
    ])

    callout(d, "Rekomendasi Bab 3 (dirinci di Bab 9)",
            "Mulai dengan **CesiumJS sebagai basis**, karena pekerjaan pertama yang bernilai "
            "adalah menempatkan tambang dan armada pada koordinat yang benar — dan itu justru "
            "bagian yang harus ditulis sendiri bila memakai Three.js. "
            "Bila di tengah jalan ternyata tampilan butuh kustomisasi berat, turunkan scene "
            "ke Three.js sambil mempertahankan pipeline aset glTF/3D Tiles yang sama — "
            "**pipeline aset adalah keputusan yang lebih mengikat daripada pilihan mesin**, "
            "dan pipeline yang benar membuat perpindahan mesin tetap mungkin.")

    h2(d, "3.8  Teknologi pendukung yang akan dibutuhkan")
    p(d, "Selain mesin render, ada empat komponen pendukung yang menentukan apakah sistem ini "
         "bisa dioperasikan. Saya mencantumkannya sekarang supaya tidak muncul sebagai kejutan "
         "di tengah implementasi.")

    caption_table(d, 16, "Teknologi pendukung dan perannya")
    table(d, ["Komponen", "Pilihan", "Peran", "Status"],
          [["Konversi & tiling aset", "GDAL (COG), 3D Tiles tools, glTF-Transform",
            "Mengubah ortomosaik dan model menjadi format yang bisa di-stream",
            "Belum dipasang — perlu disiapkan di Fase 0"],
           ["Kompresi geometri", "Draco, meshopt, KTX2/Basis",
            "Memperkecil unduhan tanpa mengurangi detail yang terlihat",
            "Sebagian — GLB yang ada sudah Draco"],
           ["Penyimpanan deret waktu", "PostgreSQL + PostGIS, atau ClickHouse/TimescaleDB",
            "Menyimpan posisi & telemetri agar replay mungkin",
            "Belum ada"],
           ["Transport real-time", "WebSocket (MQTT di sisi perangkat)",
            "Mengirim posisi ke layar tanpa polling",
            "Belum ada — pola sudah dipakai di proyek lain Minergo"]],
          widths=[3.4, 4.6, 5.4, 3.6], size=7.9)
