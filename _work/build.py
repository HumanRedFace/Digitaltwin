#!/usr/bin/env python3
"""Bangun laporan .docx + ekspor PDF + QA layout."""
import sys, os, subprocess, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_lib as L
import bab_awal, bab1_3, bab4_6, bab7_9, lampiran

OUTDIR = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(OUTDIR, "..", "Digital Twin 3D View - Riset Kelayakan.docx")
PDF = os.path.join(OUTDIR, "..", "Digital Twin 3D View - Riset Kelayakan.pdf")


def _toc_entries():
    """Ambil entri Daftar Isi. Bila toc_pages.json ada (hasil pengukuran PDF),
    pakai nomor halaman NYATA; bila belum ada, pakai nomor perkiraan."""
    import json
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toc_pages.json")
    if os.path.exists(path):
        try:
            data = json.load(open(path))
            if data and all(isinstance(r, list) and len(r) == 3 for r in data):
                return [(int(lv), str(j), int(h) if h else 1) for lv, j, h in data]
        except Exception:
            pass
    return [
        (1, "DOKUMEN KONTROL", 2),
        (1, "RINGKASAN EKSEKUTIF", 3),
        (1, "DAFTAR ISI", 5),
    ]


def build_docx():
    d = L.setup_document()
    bab_awal.cover(d)

    # ── dokumen kontrol: h1() sudah memaksa page break, jadi tanpa paragraf kosong ──
    bab_awal.dokumen_kontrol(d)

    bab_awal.ringkasan_eksekutif(d)

    entries = _toc_entries()
    bab_awal.daftar_isi(d, entries)

    bab1_3.bab1(d)
    bab1_3.bab2(d)
    bab1_3.bab3(d)
    bab4_6.bab4(d)
    bab4_6.bab5(d)
    bab4_6.bab6(d)
    bab7_9.bab7(d)
    bab7_9.bab8(d)
    bab7_9.bab9(d)
    lampiran.lampiran_a(d)
    lampiran.lampiran_b(d)
    lampiran.lampiran_c(d)
    lampiran.lampiran_d(d)
    lampiran.lampiran_e(d)

    for s in d.sections:
        L.add_footer_page_numbers(s, "MNG-RND-DT-2026-001 rev A")
    d.save(DOCX)
    return DOCX


if __name__ == "__main__":
    f = build_docx()
    print("docx:", f, os.path.getsize(f), "bytes")
