"""
Sumber tunggal angka untuk seluruh laporan Digital Twin 3D View.
Setiap angka di sini berasal dari: (a) pengukuran langsung di mesin ini,
(b) berkas milik Minergo di ~/Documents, atau (c) dokumen vendor resmi.
Tidak ada angka yang dikarang. Label sumber dipakai di laporan.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. LINGKUNGAN UJI (terverifikasi: dibaca dari WEBGL_debug_renderer_info)
# ─────────────────────────────────────────────────────────────────────────────
UJI = {
    "mesin": "MacBook Apple M1, macOS 26.2",
    "gpu": "ANGLE (Apple, ANGLE Metal Renderer: Apple M1, Unspecified Version)",
    "max_texture_size": 16384,
    "browser": "Google Chrome headless (puppeteer-core 23.11.1)",
    "resolusi": "1920 x 1080, devicePixelRatio 1",
    "three_js": "0.187.0",
    "metode_ukur": (
        "render() + gl.readPixels(1 piksel) sebagai sinkronisasi GPU, "
        "jendela 2500 ms, 20 frame pemanasan"
    ),
    "catatan": (
        "GPU terintegrasi kelas laptop. Angka GPU diskrit/desktop akan lebih tinggi; "
        "ini sengaja dipakai sebagai batas bawah yang konservatif."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. ASET YANG BENAR-BENAR ADA (terverifikasi: dibaca dari berkas)
# ─────────────────────────────────────────────────────────────────────────────
ASET_MODEL = {
    "dumptruck_gltf": {
        "berkas": "~/Documents/HD_3D/HD/dumptruck_edit.gltf",
        "ukuran_berkas_mb": 18.13,
        "buffer_eksternal": "dumptruck_edit.bin (108 MB) — TIDAK ADA di folder",
        "status": "RUSAK / tidak dapat dimuat apa adanya",
        "mesh": 14003, "node": 14003, "material": 3, "tekstur": 3,
        "triangles": 1131975,
        "generator": "Khronos glTF Blender I/O v5.2.39",
    },
    "dumptruck_glb": {
        "berkas": "~/Documents/Testing_3D/HD/dumptruck_mapbox.glb",
        "ukuran_berkas_mb": 23.59,
        "status": "VALID (glTF 2.0 + KHR_draco_mesh_compression)",
        "mesh": 14003, "node": 14003, "material": 3, "tekstur": 3,
        "triangles": 1131975,
        "dimensi_m": (12.35, 7.74, 7.18),
        "generator": "glTF-Transform v4.5.0",
        "catatan_draw_call": "14.003 mesh node = 14.003 draw call bila dimuat apa adanya",
    },
    "excavator_gltf": {
        "berkas": "~/Documents/Testing_3D/Excavator/Excavator.gltf",
        "ukuran_berkas_mb": 0.04,
        "status": "VALID",
        "mesh": 26, "node": 27, "material": 6, "tekstur": 0,
        "triangles": 6452,
        "catatan": "Contoh model ringan yang sudah 'siap web' (6.452 tri).",
    },
    "tekstur_diffuse": {
        "berkas": "CatterPillar_Trcuk_Diffuse.png",
        "piksel": (3125, 3125),
        "ukuran_mb": 17.88,
        "catatan": "Tekstur 3125x3125 PNG belum dikompresi (kandidat KTX2/Basis).",
    },
    "tekstur_normal": {
        "berkas": "CatterPillar_Trcuk_Normal.png",
        "piksel": (1024, 1024),
        "ukuran_mb": 1.75,
    },
}

ASET_PETA = {
    "orthomosaic": {
        "berkas": "~/Documents/Validasi/map/orthomosaic_web.jpg",
        "piksel": (23249, 17296),
        "resolusi_m_px": 0.0135248,
        "resolusi_cm_px": 1.35248,
        "cakupan_m": (314.44, 233.92),
        "luas_ha": 7.4,
        "crs": "EPSG:32750 (WGS 84 / UTM zone 50S)",
        "sumber_georef": "chunk eXIf di dalam orthomosaic.png (ModelPixelScale + ModelTiepoint + GeoKeyDirectory)",
        "status": "TERVERIFIKASI — orthomosaic drone nyata, sudah tergeoreferensi",
    },
    "titik_rtk": {
        "berkas": "~/Documents/Validasi/_work/galat_titik.json",
        "jumlah_titik": 22,
        "resolusi_citra_dron_cm": 3.93,
        "resolusi_citra_satelit_cm": 14.93,
        "titik_di_atas_jalan_dron": 20,
        "titik_di_atas_jalan_satelit": 11,
        "simpangan_maks_dron_m": 0.039,
        "batas": "jarak ke BADAN JALAN pada citra, bukan ke titik GCP terukur",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. DATA RTK NYATA (terverifikasi: ~/Documents/RTK_Baru/apps/rtk-simulator/data.json)
# ─────────────────────────────────────────────────────────────────────────────
RTK = {
    "sumber": "rtk-raw-2026-10-28-RTK-Lite.txt + obu-log-20261028-180119-PDS.csv",
    "tanggal": "2026-10-28",
    "titik": 3601,
    "durasi_detik": 3602,
    "jarak_m": 10891.3,
    "kecepatan_rata_kmh": 10.82,
    "kecepatan_maks_kmh": 35.79,
    "kecepatan_p95_kmh": 27.49,
    "satelit_rata": 48.4, "satelit_min": 34, "satelit_maks": 53,
    "hdop_rata": 0.4, "hdop_terburuk": 0.56,
    "umur_koreksi_rata_s": 1.11, "umur_koreksi_maks_s": 10.0,
    "persen_fix": 32.9, "persen_float": 67.1,
    "rtk_fix": 1184, "rtk_float": 2417,
    "course_unik": 971, "course_beku": 1146,
    "nmea_rmc": 3604, "nmea_gga": 3601, "checksum_salah": 4,
    "jarak_antar_fix_m": 3.03,
    "selisih_posisi_obu_rata_m": 1.27,
    "selisih_posisi_obu_maks_m": 7.27,
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. HASIL PENGUKURAN RENDER (terverifikasi: dijalankan di mesin ini)
# ─────────────────────────────────────────────────────────────────────────────
BENCH = [
    # label, draw_calls, triangles, points, ms_per_frame, fps
    ("A. GLB as-delivered (14.003 mesh)",        14003, 1131975, 0,       70.12, 14.3),
    ("B. Digabung per material",                     3, 1131975, 0,        8.56, 116.8),
    ("C. Satu mesh, satu material",                  1, 1131975, 0,        8.25, 121.2),
    ("D1. Instanced x1 (truk HD)",                   1, 1131975, 0,        8.30, 120.4),
    ("D2. Instanced x24 (truk HD)",                  1, 27167400, 0,      51.04, 19.6),
    ("D3. Instanced x60 (truk HD)",                  1, 67918500, 0,       124.46, 8.0),
    ("E. Scene target: 60 truk + 1 jt titik + terrain", 3, 105200, 1000000, 11.34, 88.2),
]

BENCH_TURUNAN = {
    # biaya per draw call = (ms A - ms C) / (calls A - calls C)
    "biaya_per_draw_call_ms": (70.12 - 8.25) / (14003 - 1),
    "throughput_tri_juta_per_detik": 67918500 / 124.46 / 1e6,
    "throughput_tri_juta_per_detik_24": 27167400 / 51.04 / 1e6,
}

# target anggaran render yang dipakai di seluruh laporan
ANGGARAN_RENDER = {
    "fps_target": 30,
    "ms_per_frame_30fps": 1000 / 30,
    "ms_per_frame_60fps": 1000 / 60,
    "headroom_persen": 40,   # sisa untuk UI, dekode, jaringan
}

# ─────────────────────────────────────────────────────────────────────────────
# 5. DOKUMEN VENDOR (terverifikasi dari datasheet/halaman resmi)
# ─────────────────────────────────────────────────────────────────────────────
RADAR = {
    "STONKAM PSA27": {
        "frekuensi": "76.00–77.00 GHz, FMCW",
        "jangkauan": "0,2–40 m (panjang), lebar 0–20 m",
        "zona": "hingga 5 zona deteksi, dapat dikonfigurasi",
        "toleransi": "±15 cm",
        "fov": "120° horizontal, 14° vertikal",
        "proteksi": "IP69K (sensor), IP66 (control box)",
        "daya": "10–32 VDC",
        "antarmuka": "konfigurasi via USB-to-UART atau Wi-Fi 2,4 GHz; trigger input x1; alarm output x1; video AHD/1080P",
        "getaran": "ISO 16750-3 2012 (5,9 G)",
        "suhu": "−40…+85 °C (sensor), −20…+70 °C (control box)",
        "sdk_terbuka": "TIDAK DITEMUKAN",
        "status": "KLAIM VENDOR (datasheet resmi)",
    },
    "CISBO C95M": {
        "frekuensi": "77 GHz",
        "jangkauan": "panjang 5 m, lebar 6 m",
        "fov": "180° horizontal",
        "proteksi": "IP69K",
        "daya": "9–36 VDC, ≤400 mA",
        "antarmuka": "LED + buzzer 80–100 dB",
        "sdk_terbuka": "TIDAK DITEMUKAN",
        "status": "KLAIM VENDOR (halaman produk resmi)",
        "catatan_konflik": (
            "Dokumen riset internal sebelumnya menulis 120 m / 100 m dan FOV 150°. "
            "Halaman produk resmi saat ini menulis 5 m x 6 m dan H180°. Angka 120 m "
            "TIDAK dapat diverifikasi — jangan dipakai."
        ),
    },
    "Howen HW-H6004A / H6008A": {
        "teknologi": "ULTRASONIK 40 kHz (bukan radar)",
        "akurasi": "1 cm (klaim)",
        "proteksi": "IP67",
        "antarmuka": "kabel sinyal 232",
        "status": "KLAIM VENDOR (datasheet)",
        "catatan": "Sering tertukar dengan radar. Tidak menghasilkan objek terdeteksi berkoordinat.",
    },
    "smartmicro DRVEGRD (pembanding kelas industri)": {
        "frekuensi": "77/79 GHz (keluarga DRVEGRD)",
        "antarmuka": "Automotive Ethernet + CAN FD",
        "keluaran": "dari raw data sampai object list",
        "integrasi": "ROS, ROS2, Autoware",
        "status": "KLAIM VENDOR (situs resmi) — kontrak datanya tidak dipublikasikan terbuka",
    },
}

GNSS = {
    "modul": "Quectel LC29H (dipakai di RTK_Baru)",
    "update_rate": "1 Hz default, maksimum 10 Hz",
    "gnss_raw": "hingga 10 Hz",
    "akurasi_1pps": "tipikal 100 ns",
    "antarmuka": "UART (NMEA/RTCM/PAIR), I2C",
    "sumber": "Quectel_LC29H_Series_Hardware_Design_V1.0.pdf, hlm. 1–4",
    "status": "TERVERIFIKASI (datasheet)",
}

# ─────────────────────────────────────────────────────────────────────────────
# 6. LISENSI & BIAYA (terverifikasi dari berkas lisensi / halaman harga resmi)
# ─────────────────────────────────────────────────────────────────────────────
LISENSI = {
    "three.js":        {"versi": "0.187.0", "lisensi": "MIT", "biaya": "gratis", "status": "TERVERIFIKASI (berkas LICENSE)"},
    "CesiumJS":        {"versi": "1.147.0", "lisensi": "Apache-2.0", "biaya": "gratis", "status": "TERVERIFIKASI (berkas LICENSE.md)"},
    "Cesium ion":      {"versi": "layanan", "lisensi": "komersial", "biaya": "Community gratis (non-komersial); Commercial $149/bln (individu) / $524/bln (tim); Premium $499 / $874", "status": "TERVERIFIKASI (halaman harga)"},
    "Unity":           {"versi": "6.x", "lisensi": "proprietary", "biaya": "Personal gratis (<$200K pendapatan/pendanaan); Pro $210/bln atau dari $2.310/thn; Industry = harga khusus", "status": "TERVERIFIKASI (halaman harga)"},
    "MapLibre GL JS":  {"versi": "5.x", "lisensi": "BSD-3-Clause", "biaya": "gratis", "status": "TERVERIFIKASI (berkas LICENSE)"},
    "Mapbox GL JS":    {"versi": "3.34.2", "lisensi": "Mapbox TOS (bukan open source sejak v2.0)", "biaya": "per MAU / per peta", "status": "TERVERIFIKASI (berkas LICENSE.txt)"},
    "deck.gl":         {"versi": "9.4.1", "lisensi": "MIT", "biaya": "gratis", "status": "TERVERIFIKASI (npm metadata)"},
    "Potree":          {"versi": "1.x", "lisensi": "BSD-2-Clause", "biaya": "gratis", "status": "TERVERIFIKASI (berkas LICENSE)"},
    "3d-tiles-renderer":{"versi": "0.5.4", "lisensi": "Apache-2.0", "biaya": "gratis", "status": "TERVERIFIKASI (npm metadata)"},
}

STANDAR = {
    "3D Tiles 1.1": "OGC Community Standard, dokumen 22-025r4, disetujui 2022-12-17, terbit 2023-01-12",
    "glTF 2.0": "Khronos, format tile wajib pada 3D Tiles 1.1 (menggantikan b3dm/i3dm/pnts)",
    "KHR_gaussian_splatting": "Ratified oleh Khronos Group (status: Complete)",
    "EPSG:4978": "WGS 84 geosentrik (ECEF), satuan meter",
    "EPSG:32750": "WGS 84 / UTM zone 50S, satuan meter (dipakai orthomosaic)",
    "WebGPU": "W3C Working Draft; dukungan global 86,83% (caniuse, data Okt 2026)",
    "COPC": "Cloud Optimized Point Cloud 1.0 — LAZ yang dapat dibaca per rentang",
}

# ─────────────────────────────────────────────────────────────────────────────
# 7. MATRIKS KEPUTUSAN TEKNOLOGI (bobot x skor; dasar skor di Bab 3)
# ─────────────────────────────────────────────────────────────────────────────
KRITERIA = [
    # (nama, bobot, keterangan)
    ("Kesesuaian geospasial (CRS, terrain, 3D Tiles)", 0.22, "harus menempatkan aset 1:1 di koordinat global"),
    ("Kinerja render scene tambang",                   0.18, "diukur di Bab 4, bukan klaim vendor"),
    ("Ketersediaan talenta & kurva belajar",           0.14, "R&D internal, bahasa Indonesia/JS"),
    ("Lisensi & biaya jangka panjang",                 0.13, "biaya per pengguna / per stream"),
    ("Integrasi data real-time (WS/MQTT/REST)",        0.12, "latensi & kemudahan ingestion"),
    ("Dukungan point cloud / fotogrametri",            0.10, "orthomosaic + LiDAR drone"),
    ("Kebutuhan hardware klien",                       0.07, "harus jalan di laptop & tablet"),
    ("Kematangan ekosistem & dukungan",                0.04, "dokumentasi, komunitas, contoh"),
]

# skor 1..5, dibahas per kriteria di Bab 3.6
# PENTING: hanya Three.js yang DIUKUR pada mesin ini (Lampiran C).
# Skor baris "Kinerja render" untuk engine lain adalah PENILAIAN, bukan pengukuran.
SKOR = {
    "Three.js":  [2, 4, 5, 5, 4, 3, 5, 4],
    "CesiumJS":  [5, 3, 4, 4, 4, 4, 3, 4],
    "Unity":     [3, 4, 3, 2, 3, 3, 2, 5],
    "deck.gl":   [3, 3, 3, 5, 4, 3, 3, 3],
    "Potree":    [3, 3, 3, 5, 2, 5, 4, 2],
}

# engine yang benar-benar diukur (indeks kriteria "Kinerja render" = 1)
TERUKUR = {"Three.js"}

# dasar skor per sel, dipakai sebagai catatan kaki tabel di Bab 3.6
DASAR_SKOR = {
    "Kesesuaian geospasial (CRS, terrain, 3D Tiles)": "CesiumJS: inti produk (Ellipsoid, Terrain, 3D Tiles). Three.js: TIDAK ADA dukungan CRS — proyeksi & terrain harus dibangun sendiri (terbukti saat uji). deck.gl: ada Tile3DLayer tetapi bukan scene graph bumi.",
    "Kinerja render scene tambang": "Three.js: TERUKUR 88,2 fps pada scene target (Bab 4). Lainnya: PENILAIAN, belum diukur — jangan dibaca sebagai hasil uji.",
    "Ketersediaan talenta & kurva belajar": "Three.js/JS: talenta web paling luas. CesiumJS: butuh pemahaman geodesi. Unity: butuh C#/engine 3D, talenta berbeda.",
    "Lisensi & biaya jangka panjang": "Three.js MIT, CesiumJS Apache-2.0, deck.gl/Potree MIT/BSD (gratis). Unity: Pro $210/bln setelah ambang pendapatan. Cesium ion: $149–$874/bln bila memakai layanan hosted.",
    "Integrasi data real-time (WS/MQTT/REST)": "Semua engine web setara (JS). Unity butuh jembatan native/WebGL.",
    "Dukungan point cloud / fotogrametri": "Potree: khusus point cloud (terbaik). CesiumJS: 3D Tiles point cloud. Three.js: manual. deck.gl: layer titik 2D.",
    "Kebutuhan hardware klien": "Three.js/deck.gl: WebGL2, jalan di tablet. CesiumJS: lebih berat (terrain+imagery). Unity: build desktop/mobile, tidak di browser.",
    "Kematangan ekosistem & dukungan": "Unity: komersial penuh. CesiumJS/Three.js: besar & aktif. Potree: komunitas kecil, rilis jarang (push terakhir Jan 2026).",
}


# ─────────────────────────────────────────────────────────────────────────────
# 8. USE CASE & PRIORITAS
# ─────────────────────────────────────────────────────────────────────────────
USE_CASE = [
    # id, nama, aktor, nilai, kesiapan data, kompleksitas
    ("UC-1", "Posisi & pergerakan armada di haul road (peta 3D + trail)",
     "Dispatcher, Mine Planning", "Tinggi", "Tinggi (RTK + orthomosaic ada)", "Rendah"),
    ("UC-2", "Geofence & pelanggaran zona (speed, dumping, restricted)",
     "Safety, Dispatch", "Tinggi", "Tinggi", "Rendah"),
    ("UC-3", "Replay historis insiden (post-mortem kecelakaan/ near-miss)",
     "Safety, Investigasi", "Tinggi", "Sedang (log ada, belum seragam)", "Sedang"),
    ("UC-4", "Blind spot & objek terdeteksi radar di sekitar unit",
     "Operator, Safety", "Tinggi", "RENDAH — kontrak data radar belum ada", "Tinggi"),
    ("UC-5", "Simulasi skenario (layout jalan, kecepatan, titik buta)",
     "Mine Planning, R&D", "Sedang", "Rendah (perlu model & aturan)", "Tinggi"),
    ("UC-6", "Digital twin permukaan & progres tambang (cut/fill dari drone)",
     "Survey, Planning", "Sedang", "Sedang (ortho ada, DSM/point cloud belum)", "Sedang"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 9. RISIKO
# ─────────────────────────────────────────────────────────────────────────────
RISIKO = [
    # id, risiko, dampak, kemungkinan, skor, mitigasi
    ("R-1", "Kontrak data radar tidak tersedia (hanya alarm LED/buzzer)",
     "Tinggi", "Tinggi", 9, "Minta SDK/protokol ke vendor; siapkan jalur mundur: radar diganti unit ber-object-list"),
    ("R-2", "Draw call meledak karena model tidak dioptimasi",
     "Tinggi", "Tinggi", 9, "Pipeline optimasi wajib: merge per material + InstancedMesh (terbukti 8x)"),
    ("R-3", "Akurasi RTK tidak konsisten (67,1% FLOAT pada log nyata)",
     "Sedang", "Tinggi", 6, "Tampilkan kelas akurasi di UI; jangan jadikan FLOAT dasar keputusan geofence kritis"),
    ("R-4", "Sinkronisasi waktu 1 Hz membuat posisi melompat 3 m",
     "Sedang", "Tinggi", 6, "Interpolasi + timestamp sumber; target 5–10 Hz atau dead-reckoning IMU"),
    ("R-5", "Latensi ingestion > 2 s membuat tampilan tidak dapat dipakai untuk peringatan",
     "Sedang", "Sedang", 4, "Pisahkan jalur peringatan (edge) dari jalur visualisasi (server)"),
    ("R-6", "Lisensi Cesium ion / Mapbox membengkak saat pengguna bertambah",
     "Sedang", "Sedang", 4, "Self-host aset (3D Tiles statis) + MapLibre/terrain lokal"),
    ("R-7", "Ketergantungan vendor engine (Unity) mengunci tim",
     "Sedang", "Sedang", 4, "Pilih stack web terbuka lebih dulu; Unity hanya bila butuh desktop berat"),
    ("R-8", "Keamanan data: koordinat & produksi keluar dari jaringan perusahaan",
     "Tinggi", "Sedang", 6, "On-premise, tanpa CDN publik, tanpa token pihak ketiga di klien"),
    ("R-9", "Hardware klien di lapangan (tablet) tidak mampu render",
     "Sedang", "Sedang", 4, "Anggaran render 30 fps, LOD, mode 2D fallback"),
    ("R-10", "Data drone tidak rutin diperbarui → twin cepat kedaluwarsa",
     "Sedang", "Tinggi", 6, "Jadwal survei + tanggal data ditampilkan di UI"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 10. ESTIMASI EFFORT (jam-orang; ASUMSI, bukan komitmen)
# ─────────────────────────────────────────────────────────────────────────────
EFFORT = [
    ("Fase 0 — Fondasi data & koordinat", 60, 90, "1 dev + 0,2 surveyor"),
    ("Fase 1 — Viewer 3D + armada (UC-1)", 120, 180, "1 dev frontend + 1 dev backend"),
    ("Fase 2 — Geofence & peringatan (UC-2)", 80, 120, "1 dev backend"),
    ("Fase 3 — Replay historis (UC-3)", 100, 150, "1 dev full-stack"),
    ("Fase 4 — Integrasi radar / objek terdeteksi (UC-4)", 160, 320, "1 dev + dukungan vendor"),
    ("Fase 5 — Simulasi (UC-5) & twin permukaan (UC-6)", 200, 360, "2 dev"),
]

ROADMAP = [
    ("Sprint 0", "2 minggu", "Audit aset, konversi model, uji beban nyata", "Keputusan stack final"),
    ("Sprint 1", "4 minggu", "Orthomosaic + RTK live di viewer 3D", "Demo UC-1"),
    ("Sprint 2", "3 minggu", "Trail, replay 1 jam, panel kendaraan", "Demo UC-3 dasar"),
    ("Sprint 3", "3 minggu", "Geofence + aturan kecepatan", "Demo UC-2"),
    ("Sprint 4", "6 minggu", "Radar (bergantung kontrak data vendor)", "Demo UC-4 / atau parkir"),
]

GAP = [
    ("G-1", "Berkas buffer dumptruck_edit.bin (108 MB) hilang", "Model .gltf tidak bisa dimuat; pakai .glb",
     "Ekspor ulang dari .blend di ~/Documents/HD_3D/dumptruck_edit.blend"),
    ("G-2", "Belum ada DSM / point cloud hasil drone", "Twin masih datar (orthomosaic 2D)",
     "Terbangkan ulang dengan overlap 75/65 dan olah ke LAS/COPC"),
    ("G-3", "Kontrak data radar (SDK/protokol) tidak ada", "UC-4 tidak bisa dimulai",
     "Surat permintaan SDK ke STONKAM/CISBO; atau uji unit ber-object-list"),
    ("G-4", "Log telemetri belum berskema seragam", "Replay & analitik sulit",
     "Definisikan skema kanonik (Bab 5.1) + adapter per sumber"),
    ("G-5", "Belum ada acuan waktu tunggal (PTP/NTP) di unit", "Sinkronisasi multi-sensor tidak ketat",
     "Aktifkan NTP/PTP di gateway; cap waktu di titik masuk"),
    ("G-6", "Heading armada tidak stabil (1146 dari 3601 course beku)", "Orientasi model 3D bisa salah arah",
     "Fusi course + IMU; jangan pakai course saat kecepatan ~0"),
]

PERTANYAAN_VENDOR = [
    ("V-1", "STONKAM", "Apakah PSA27 menyediakan object list terstruktur (jarak, sudut, kecepatan) via UART/CAN, dan di mana dokumen protokolnya?"),
    ("V-2", "STONKAM", "Berapa laju pembaruan objek (Hz) dan berapa jumlah target maksimum yang dilaporkan?"),
    ("V-3", "CISBO", "Apakah C95M dapat mengeluarkan data target selain status alarm LED? Format dan lajunya?"),
    ("V-4", "CISBO", "Klarifikasi jangkauan: halaman resmi menulis 5 m x 6 m, dokumen lama menyebut 120 m. Mana yang benar untuk C95M?"),
    ("V-5", "Quectel / mitra RTK", "Apakah LC29H dapat dikonfigurasi ke 5–10 Hz tanpa kehilangan fix rate pada kondisi tambang?"),
    ("V-6", "PIC Survey", "Apakah tersedia DSM/point cloud dari survei drone terakhir, atau hanya orthomosaic?"),
    ("V-7", "IT / OT", "Apakah diizinkan menyajikan viewer 3D on-premise tanpa CDN dan tanpa token pihak ketiga?"),
]

SUMBER = [
    ("S-01", "three.js LICENSE (MIT)", "https://raw.githubusercontent.com/mrdoob/three.js/dev/LICENSE", "TERVERIFIKASI"),
    ("S-02", "CesiumJS LICENSE.md (Apache-2.0)", "https://raw.githubusercontent.com/CesiumGS/cesium/main/LICENSE.md", "TERVERIFIKASI"),
    ("S-03", "OGC 3D Tiles 1.1, dok. 22-025r4", "https://docs.ogc.org/cs/22-025r4/22-025r4.html", "TERVERIFIKASI"),
    ("S-04", "OGC 3D Tiles (halaman standar)", "https://www.ogc.org/standards/3dtiles/", "TERVERIFIKASI"),
    ("S-05", "Cesium ion — halaman harga", "https://cesium.com/platform/cesium-ion/pricing/", "TERVERIFIKASI"),
    ("S-06", "Unity — halaman harga", "https://unity.com/pricing", "TERVERIFIKASI"),
    ("S-07", "Mapbox GL JS LICENSE.txt (Mapbox TOS)", "https://raw.githubusercontent.com/mapbox/mapbox-gl-js/main/LICENSE.txt", "TERVERIFIKASI"),
    ("S-08", "MapLibre GL JS LICENSE.txt (BSD-3)", "https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/LICENSE.txt", "TERVERIFIKASI"),
    ("S-09", "Potree LICENSE (BSD-2)", "https://raw.githubusercontent.com/potree/potree/master/LICENSE", "TERVERIFIKASI"),
    ("S-10", "Khronos glTF 2.0", "https://www.khronos.org/gltf/", "TERVERIFIKASI"),
    ("S-11", "KHR_gaussian_splatting (status: Ratified)", "https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_gaussian_splatting/README.md", "TERVERIFIKASI"),
    ("S-12", "COPC — Cloud Optimized Point Cloud 1.0", "https://copc.io/", "TERVERIFIKASI"),
    ("S-13", "EPSG:4978 WGS 84 geosentrik", "https://epsg.io/4978", "TERVERIFIKASI"),
    ("S-14", "WebGPU — caniuse (86,83% global, Okt 2026)", "https://caniuse.com/webgpu", "TERVERIFIKASI"),
    ("S-15", "STONKAM PSA27 — datasheet PDF resmi", "https://www.stonkam.com/storage/file/20260807/1786081641652919.pdf", "KLAIM VENDOR"),
    ("S-16", "STONKAM PSA27 — halaman produk", "https://www.stonkam.com/millimeter-wave-radar/7inch-Radar-Detection-System-PSA27", "KLAIM VENDOR"),
    ("S-17", "CISBO C95M — halaman produk resmi", "https://www.szcisbo.com/truck-bsd-blind-spot-detection-system-with-77ghz-millimeter-wave-radar-c95m", "KLAIM VENDOR"),
    ("S-18", "smartmicro — automotive radar (Ethernet/CAN FD, ROS/ROS2)", "https://www.smartmicro.com/automotive-radar", "KLAIM VENDOR"),
    ("S-19", "Quectel LC29H Hardware Design V1.0 (lokal, 59 hlm)", "~/Documents/RTK_Baru/dokumen/Quectel_LC29H_Series_Hardware_Design_V1.0.pdf", "TERVERIFIKASI"),
    ("S-20", "Howen HW-H6004A/H6008A datasheet (ultrasonik)", "~/Documents/Riset_Jarak/HW-H6004A, HW-H6008A_Datasheet.pdf", "KLAIM VENDOR"),
    ("S-21", "Data RTK nyata 28-10-2026 (3.601 titik)", "~/Documents/RTK_Baru/apps/rtk-simulator/data.json", "TERVERIFIKASI"),
    ("S-22", "Orthomosaic drone + VRT georef", "~/Documents/Validasi/map/orthomosaic_georef.vrt", "TERVERIFIKASI"),
    ("S-23", "Galat titik RTK vs citra", "~/Documents/Validasi/_work/galat_titik.json", "TERVERIFIKASI"),
    ("S-24", "Model 3D dump truck (glTF/GLB)", "~/Documents/HD_3D/, ~/Documents/Testing_3D/", "TERVERIFIKASI"),
    ("S-25", "Pengukuran render three.js 0.187.0 di mesin ini", "bench7 (lihat Lampiran C)", "TERVERIFIKASI"),
    ("S-26", "3D Gaussian Splatting (Kerbl dkk., 2023)", "https://arxiv.org/abs/2308.04079", "TERVERIFIKASI"),
    ("S-27", "Dokumen riset internal radar (pembanding)", "~/Documents/Riset_Jarak/Riset Radar Deteksi Kendaraan Tambang.docx", "ASUMSI — memuat angka yang tidak cocok dengan sumber vendor"),
]
