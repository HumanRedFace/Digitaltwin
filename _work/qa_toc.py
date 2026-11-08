#!/usr/bin/env python3
"""Verifikasi independen Daftar Isi: baca entri TOC dari PDF, lalu cek apakah
setiap judul benar-benar berada di halaman yang disebutkan."""
import sys, re
import fitz

PDF = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/mvmho11/Documents/Digitaltwin/Digital Twin 3D View - Riset Kelayakan.pdf"

doc = fitz.open(PDF)
N = doc.page_count


def is_toc_page(page):
    blok = page.get_text("blocks")
    entri = 0
    for b in blok:
        baris = [s.strip() for s in b[4].strip().splitlines() if s.strip()]
        if len(baris) >= 2 and re.fullmatch(r"\d{1,3}", baris[-1]) and len(baris[0]) > 4:
            entri += 1
    ada = any("daftar isi" in b[4].strip().lower() for b in blok)
    return entri >= 5 or (ada and entri >= 2)


toc_pages = {i for i, p in enumerate(doc, start=1) if is_toc_page(p)}
print(f"halaman TOC: {sorted(toc_pages)}")

# baca entri: blok "judul\nangka" pada halaman TOC
entri = []
for i in sorted(toc_pages):
    for b in doc[i - 1].get_text("blocks"):
        baris = [s.strip() for s in b[4].strip().splitlines() if s.strip()]
        if len(baris) >= 2 and re.fullmatch(r"\d{1,3}", baris[-1]) and len(baris[0]) > 4:
            entri.append((" ".join(baris[:-1]), int(baris[-1])))
        # judul panjang yang wrap: blok judul terpisah dari blok angka
    # tangani blok judul multiline + blok angka terpisah (y sejajar)
    judul_blok = [b for b in doc[i - 1].get_text("blocks")
                  if re.search(r"[A-Za-z]", b[4]) and b[0] < 420 and len(b[4].strip()) > 4
                  and not b[4].strip().upper().startswith("DAFTAR ISI")
                  and not b[4].strip().startswith("MNG-")]
    angka_blok = [b for b in doc[i - 1].get_text("blocks")
                  if re.fullmatch(r"\d{1,3}", b[4].strip())]
    for jb in judul_blok:
        jy = (jb[1] + jb[3]) / 2
        cocok = [ab for ab in angka_blok if abs((ab[1] + ab[3]) / 2 - jy) < 8]
        if cocok:
            t = " ".join(jb[4].split())
            entri.append((t, int(cocok[0][4].strip())))

# dedupe
seen, uniq = set(), []
for t, h in entri:
    if (t, h) not in seen:
        seen.add((t, h)); uniq.append((t, h))
entri = uniq
print(f"entri terbaca: {len(entri)}\n")


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def judul_di_halaman(page, toc_pages):
    """Baris yang berformat JUDUL saja: tebal dan >= 11,5 pt.

    Tanpa filter ini, verifikasi selalu LULUS secara palsu: kalimat badan
    "Lampiran C (88 fps, 3 draw call) ..." di hal 32 dan sel tabel "Lampiran E"
    di hal 9 dicocokkan sebagai judul, sehingga nomor halaman yang salah di
    Daftar Isi terlihat "cocok".
    """
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
            if max(s["size"] for s in spans) >= 11.5 and any("Bold" in s["font"] for s in spans):
                out.append(teks)
    return out


salah, benar = [], 0
for judul, hal in entri:
    t = norm(judul)
    if len(t) < 5 or t == "daftar isi":
        continue
    key = t[:46]
    ketemu = None
    for i, page in enumerate(doc, start=1):
        if i in toc_pages or i == 1:
            continue
        for ln in judul_di_halaman(page, toc_pages):
            if norm(ln).startswith(key):
                ketemu = i
                break
        if ketemu:
            break
    if ketemu is None:
        salah.append((judul, hal, "TIDAK KETEMU"))
    elif ketemu != hal:
        salah.append((judul, hal, ketemu))
    else:
        benar += 1

total = benar + len(salah)
print(f"COCOK    : {benar}/{total}")
if salah:
    print(f"MISMATCH : {len(salah)}")
    for j, a, b in salah:
        print(f"   '{j[:56]}'  TOC={a}  aktual={b}")
else:
    print("SEMUA nomor halaman Daftar Isi cocok dengan lokasi judul sebenarnya.")

doc.close()
