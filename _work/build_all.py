#!/usr/bin/env python3
"""
Build laporan lengkap dengan Daftar Isi yang nomor halamannya DIUKUR dari PDF nyata.
Iterasi dua pass sampai nomor halaman stabil (konvergen), lalu verifikasi.
"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

WORK = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(WORK)
DOCX = os.path.join(BASE, "Digital Twin 3D View - Riset Kelayakan.docx")
PDF = os.path.join(BASE, "Digital Twin 3D View - Riset Kelayakan.pdf")
SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
PY = "/Users/mvmho11/miniconda3/bin/python3.13"
TOCJSON = os.path.join(WORK, "toc_pages.json")


def to_pdf():
    if os.path.exists(PDF):
        os.remove(PDF)
    subprocess.run([SOFFICE, "--headless", "--norestore", "--convert-to", "pdf",
                    "--outdir", BASE, DOCX],
                   check=True, capture_output=True, timeout=600)


def measure():
    r = subprocess.run([PY, os.path.join(WORK, "measure_toc.py"), PDF, TOCJSON],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ukur TOC gagal:\n" + r.stderr[-2000:])
    return json.load(open(TOCJSON))


def main():
    import build

    # Pass 0: tanpa TOC terukur → dapat struktur dasar
    if os.path.exists(TOCJSON):
        os.remove(TOCJSON)
    print("[pass 0] build awal + ekspor PDF ...")
    build.build_docx()
    to_pdf()
    prev = measure()
    print(f"          {len(prev)} judul, {sum(1 for r in prev if r[2] is None)} tidak ditemukan")

    for it in range(1, 4):
        print(f"[pass {it}] build dengan nomor halaman hasil ukur ...")
        build.build_docx()
        to_pdf()
        cur = measure()
        beda = [(a[1], a[2], b[2]) for a, b in zip(prev, cur) if a[2] != b[2]]
        print(f"          selisih dari pass sebelumnya: {len(beda)}")
        for j, x, y in beda[:8]:
            print(f"            {j[:52]:54s} {x} -> {y}")
        if not beda:
            print("          KONVERGEN — nomor halaman stabil")
            break
        prev = cur
    else:
        print("PERINGATAN: belum konvergen setelah 3 iterasi")

    hilang = [r for r in cur if r[2] is None]
    print(f"\njudul tanpa halaman: {len(hilang)}")
    for r in hilang:
        print("   ", r[1])
    print(f"\ndocx: {DOCX}  ({os.path.getsize(DOCX):,} bytes)")
    print(f"pdf : {PDF}  ({os.path.getsize(PDF):,} bytes)")


if __name__ == "__main__":
    main()
