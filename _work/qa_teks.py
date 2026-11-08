#!/usr/bin/env python3
"""Audit teks laporan: karakter asing, markup bocor, placeholder, dan konsistensi angka."""
import sys, re
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"

doc = fitz.open(PDF)
full = "\n".join(p.get_text("text") for p in doc)

masalah = 0

# 1. markup yang bocor ke dokumen (**tebal** atau `kode`)
bocor = re.findall(r"\*\*[^*\n]{1,60}\*\*", full)
print(f"1. markup '**' bocor        : {len(bocor)}")
for b in bocor[:8]:
    print("     ", b[:70])
masalah += len(bocor)

back = re.findall(r"`[^`\n]{1,50}`", full)
print(f"2. markup '`' bocor         : {len(back)}")
for b in back[:8]:
    print("     ", b[:70])
masalah += len(back)

# 2. karakter CJK / kontrol
cjk = [(ch, i) for i, ch in enumerate(full) if '\u4e00' <= ch <= '\u9fff']
print(f"3. karakter CJK             : {len(cjk)}")
for ch, i in cjk[:5]:
    print("     ", repr(full[max(0, i-40):i+20]))
masalah += len(cjk)

# 3. placeholder / TODO (word boundary; "METODOLOGI" bukan TODO)
ph = re.findall(r"\b(TODO|TBD|FIXME|XXX)\b|lorem ipsum|Lorem ipsum", full)
print(f"4. placeholder/TODO         : {len(ph)}")
for p in set(ph):
    print("     ", p)
masalah += len(ph)

# 4. "None" / "nan" (brace diabaikan — blok kode JSON memang pakai kurung kurawal)
none_hit = re.findall(r"\bNone\b|\bnan\b|\bundefined\b", full)
print(f"5. 'None'/'nan'/'undefined' : {len(none_hit)}")
for n in set(none_hit):
    idx = full.find(n)
    print("     ", repr(full[max(0, idx-50):idx+30]))
masalah += len(none_hit)

# 5. angka penting harus muncul (konsistensi lintas bab)
harus = {
    "88,2 fps": "hasil scene target",
    "11,34": "ms/frame",
    "14.003": "jumlah draw call",
    "1.131.975": "segitiga model",
    "32,9%": "persen FIX",
    "1,35": "cm/px ortomosaik",
    "3,97": "skor Cesium",
    "3,80": "skor Three.js",
    "8,5 kali": "rasio optimasi",
}
print("6. angka kunci:")
for k, ket in harus.items():
    n = full.count(k)
    status = "OK" if n >= 1 else "HILANG"
    if n < 1:
        masalah += 1
    print(f"     {k:12s} ({ket:22s}) muncul {n}x  {status}")

# 6. label bukti harus dipakai
print("7. label tingkat bukti:")
for lab in ("TERVERIFIKASI", "KLAIM VENDOR", "ASUMSI", "BELUM DITEMUKAN", "TIDAK ADA"):
    n = full.upper().count(lab)
    print(f"     {lab:18s} {n}x")

# 7. duplikasi paragraf persis
paras = [re.sub(r"\s+", " ", p).strip() for p in full.split("\n\n") if len(p.strip()) > 120]
dobel = len(paras) - len(set(paras))
print(f"8. paragraf duplikat        : {dobel}")
masalah += dobel

print(f"\nTOTAL MASALAH: {masalah}")
doc.close()
