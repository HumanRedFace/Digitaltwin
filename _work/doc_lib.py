"""Helper pembangun .docx — dipakai semua modul bab."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── geometri halaman (A4, margin 2,4 cm seperti skill) ─────────────────────
USABLE_CM = 16.20
FIG_SAFE_CM = 15.50
MARGIN_CM = 2.40

NAVY = RGBColor(0x16, 0x32, 0x4F)
ACC = RGBColor(0xE1, 0x1B, 0x22)
GREY = RGBColor(0x5A, 0x6B, 0x7B)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x2E, 0x7D, 0x4F)
AMBER = RGBColor(0x9A, 0x6A, 0x10)

BODY_FONT = "Georgia"
MONO_FONT = "Courier New"


def _apply_font(run, name, size=None, bold=None, color=None, italic=None):
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    run.font.name = name
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    run._element.get_or_add_rPr().append(rf)


def setup_document():
    d = Document()
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.orientation = WD_ORIENT.PORTRAIT
        s.top_margin = s.bottom_margin = Cm(MARGIN_CM)
        s.left_margin = s.right_margin = Cm(MARGIN_CM)
    st = d.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(10)
    st.font.color.rgb = BLACK
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), BODY_FONT)
    st.element.get_or_add_rPr().append(rf)
    pf = st.paragraph_format
    pf.space_after = Pt(5)
    pf.line_spacing = 1.14
    for lvl, size in ((1, 15), (2, 12), (3, 10.5)):
        h = d.styles[f"Heading {lvl}"]
        h.font.name = BODY_FONT
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = NAVY
        rf2 = OxmlElement("w:rFonts")
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf2.set(qn(a), BODY_FONT)
        h.element.get_or_add_rPr().append(rf2)
        h.paragraph_format.space_before = Pt(12 if lvl == 1 else 9)
        h.paragraph_format.space_after = Pt(5)
        h.paragraph_format.keep_with_next = True
    return d


def h1(d, teks, pb=True):
    p = d.add_heading(teks, 1)
    if pb:
        p.paragraph_format.page_break_before = True
    return p


def h2(d, teks):
    return d.add_heading(teks, 2)


def h3(d, teks):
    return d.add_heading(teks, 3)


def p(d, teks, size=10, bold=False, italic=False, color=None, align="just",
      space_after=5, indent_first=False):
    par = d.add_paragraph()
    par.alignment = {"just": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                     "center": WD_ALIGN_PARAGRAPH.CENTER,
                     "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    par.paragraph_format.space_after = Pt(space_after)
    if indent_first:
        par.paragraph_format.first_line_indent = Cm(0.6)
    if bold or italic or color:
        # gaya eksplisit: satu run, tanpa parsing markup
        r = par.add_run(teks)
        _apply_font(r, BODY_FONT, size, bold, color, italic)
    else:
        # parsing **tebal** / `mono` supaya markup tidak bocor ke dokumen
        _rich(par, teks, size)
    return par


def _rich(par, teks, size):
    """Dukung **tebal** dan `kode` di dalam satu paragraf."""
    import re
    for tok in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", teks):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = par.add_run(tok[2:-2])
            _apply_font(r, BODY_FONT, size, bold=True)
        elif tok.startswith("`") and tok.endswith("`"):
            r = par.add_run(tok[1:-1])
            _apply_font(r, MONO_FONT, size - 1.2)
        else:
            r = par.add_run(tok)
            _apply_font(r, BODY_FONT, size)


def pr(d, teks, size=10, align="just", space_after=5):
    """Paragraf dengan markup **tebal** / `mono`."""
    par = d.add_paragraph()
    par.alignment = {"just": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                     "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
    par.paragraph_format.space_after = Pt(space_after)
    _rich(par, teks, size)
    return par


def bullets(d, items, size=9.5, style="List Bullet"):
    for it in items:
        par = d.add_paragraph(style=style)
        par.paragraph_format.space_after = Pt(2)
        par.paragraph_format.left_indent = Cm(0.65)
        _rich(par, it, size)


def numbered(d, items, size=9.5):
    bullets(d, items, size, style="List Number")


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def cell_margins(cell, top=50, bottom=50, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for k, v in (("top", top), ("start", left), ("bottom", bottom), ("end", right)):
        e = OxmlElement(f"w:{k}")
        e.set(qn("w:w"), str(v))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tcPr.append(mar)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def table(d, header, rows, widths=None, size=8.4, header_bg="16324F",
          keep_together=None, align_center=None, first_col_bold=False,
          zebra=True, bold_rows=()):
    n = len(header)
    t = d.add_table(rows=1, cols=n)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    widths = widths or [USABLE_CM / n] * n
    scale = USABLE_CM / sum(widths)
    widths = [w * scale for w in widths]

    hdr = t.rows[0]
    repeat_header(hdr)
    for i, htxt in enumerate(header):
        c = hdr.cells[i]
        c.width = Cm(widths[i])
        shade(c, header_bg)
        cell_margins(c)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        par = c.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = Pt(1)
        r = par.add_run(htxt)
        _apply_font(r, BODY_FONT, size, bold=True, color=WHITE)

    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        no_split(t.rows[-1])
        for i, val in enumerate(row):
            c = cells[i]
            c.width = Cm(widths[i])
            cell_margins(c)
            c.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if zebra and ri % 2 == 1:
                shade(c, "F2F5F8")
            par = c.paragraphs[0]
            par.paragraph_format.space_after = Pt(1)
            if align_center and i in align_center:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _rich(par, str(val), size)
            if (first_col_bold and i == 0) or ri in bold_rows:
                for r in par.runs:
                    r.bold = True

    if keep_together is None:
        keep_together = len(rows) <= 6
    if keep_together:
        for row in t.rows[:-1]:
            for c in row.cells:
                for par in c.paragraphs:
                    par.paragraph_format.keep_with_next = True
                    par.paragraph_format.keep_together = True
    return t


def figure(d, path, caption, width_cm=None, number=None):
    # Selalu dibatasi ke FIG_SAFE_CM supaya tidak pernah melewati tepi kolom,
    # sekalipun pemanggil meminta lebih lebar.
    if width_cm is None:
        width_cm = FIG_SAFE_CM
    width_cm = min(width_cm, FIG_SAFE_CM)
    par = d.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(2)
    par.paragraph_format.keep_with_next = True
    par.paragraph_format.left_indent = Cm(0)
    par.paragraph_format.right_indent = Cm(0)
    par.paragraph_format.first_line_indent = Cm(0)
    par.add_run().add_picture(path, width=Cm(width_cm))
    cp = d.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_after = Pt(10)
    label = f"Gambar {number}. " if number else ""
    r = cp.add_run(label + caption)
    _apply_font(r, BODY_FONT, 8.2, italic=True, color=GREY)
    return par


def caption_table(d, num, teks):
    cp = d.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(6)
    cp.paragraph_format.space_after = Pt(3)
    cp.paragraph_format.keep_with_next = True
    r = cp.add_run(f"Tabel {num}. {teks}")
    _apply_font(r, BODY_FONT, 8.2, italic=True, color=GREY)


def callout(d, judul, isi, warna="EEF3F8", garis="2E6E9E", ikon="CATATAN"):
    t = d.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.autofit = False
    c = t.rows[0].cells[0]
    c.width = Cm(USABLE_CM)
    shade(c, warna)
    cell_margins(c, 90, 90, 130, 130)
    par = c.paragraphs[0]
    par.paragraph_format.space_after = Pt(2)
    r = par.add_run(f"{ikon} — {judul}")
    _apply_font(r, BODY_FONT, 8.6, bold=True, color=RGBColor.from_string(garis))
    par2 = c.add_paragraph()
    par2.paragraph_format.space_after = Pt(0)
    _rich(par2, isi, 9)
    d.add_paragraph().paragraph_format.space_after = Pt(3)
    return t


def code_block(d, code, size=7.6):
    t = d.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.autofit = False
    c = t.rows[0].cells[0]
    c.width = Cm(USABLE_CM)
    shade(c, "F5F7FA")
    cell_margins(c, 70, 70, 110, 110)
    par = c.paragraphs[0]
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.line_spacing = 1.0
    lines = code.strip("\n").split("\n")
    for i, ln in enumerate(lines):
        if i:
            par.add_run().add_break()
        r = par.add_run(ln if ln else " ")
        _apply_font(r, MONO_FONT, size)
    d.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def add_footer_page_numbers(section, teks_kiri):
    footer = section.footer
    par = footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(teks_kiri + "   |   ")
    _apply_font(r, BODY_FONT, 8, color=GREY)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "16")
    rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t"); t.text = "1"
    run.append(t)
    fld.append(run)
    par._p.append(fld)
    r2 = par.add_run(" / ")
    _apply_font(r2, BODY_FONT, 8, color=GREY)
    fld2 = OxmlElement("w:fldSimple")
    fld2.set(qn("w:instr"), "NUMPAGES")
    run2 = OxmlElement("w:r")
    rpr2 = OxmlElement("w:rPr")
    sz2 = OxmlElement("w:sz"); sz2.set(qn("w:val"), "16")
    rpr2.append(sz2)
    run2.append(rpr2)
    t2 = OxmlElement("w:t"); t2.text = "1"
    run2.append(t2)
    fld2.append(run2)
    par._p.append(fld2)


def hrule(d, warna="D0D7DE"):
    par = d.add_paragraph()
    par.paragraph_format.space_before = Pt(2)
    par.paragraph_format.space_after = Pt(6)
    pPr = par._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), warna)
    pbdr.append(bottom)
    pPr.append(pbdr)
