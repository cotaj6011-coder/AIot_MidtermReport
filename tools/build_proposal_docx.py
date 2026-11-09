from pathlib import Path
import re
import sys

sys.path.insert(0, r"C:\Users\Justin\AppData\Local\Temp\codex_docx_deps")

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proposal" / "proposal.md"
OUTPUT = ROOT / "proposal" / "智慧停車AI_Agent_Proposal.docx"

FONT = "Microsoft JhengHei"
MONO = "Consolas"
NAVY = "17365D"
LIGHT_BLUE = "DCE6F1"
PALE_BLUE = "EEF4FA"
LIGHT_GRAY = "D9D9D9"
TEXT = "111111"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_border(cell, color=LIGHT_GRAY, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_run_font(run, name=FONT, size=None, bold=None, color=TEXT):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)


def add_inline(paragraph, text, size=11):
    pattern = re.compile(r"(\*\*.*?\*\*|`.*?`)")
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            set_run_font(paragraph.add_run(text[pos:match.start()]), size=size)
        token = match.group(0)
        if token.startswith("**"):
            set_run_font(paragraph.add_run(token[2:-2]), size=size, bold=True)
        else:
            set_run_font(paragraph.add_run(token[1:-1]), name=MONO, size=max(9, size - 1), color="333333")
        pos = match.end()
    if pos < len(text):
        set_run_font(paragraph.add_run(text[pos:]), size=size)


def style_table(table, header=True, font_size=9):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for r_idx, row in enumerate(table.rows):
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(OxmlElement("w:cantSplit"))
        if r_idx == 0 and header:
            set_repeat_table_header(row)
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)
            set_cell_border(cell)
            if r_idx == 0 and header:
                set_cell_shading(cell, NAVY)
            elif r_idx % 2 == 0:
                set_cell_shading(cell, PALE_BLUE)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.05
                for run in p.runs:
                    set_run_font(run, size=font_size, bold=(r_idx == 0 and header), color=("FFFFFF" if r_idx == 0 and header else TEXT))


def add_markdown_table(doc, rows):
    if len(rows) < 2:
        return
    data = []
    for idx, raw in enumerate(rows):
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if idx == 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        data.append(cells)
    cols = max(len(r) for r in data)
    table = doc.add_table(rows=len(data), cols=cols)
    table.style = "Table Grid"
    usable = 6.8
    widths = [usable / cols] * cols
    if cols == 4:
        widths = [1.35, 0.9, 2.6, 1.95]
    elif cols == 5:
        widths = [0.45, 1.25, 1.1, 2.65, 1.35]
    elif cols == 8:
        widths = [0.4, 0.45, 0.85, 0.95, 1.05, 1.1, 1.05, 0.95]
    for r_idx, row in enumerate(data):
        for c_idx in range(cols):
            cell = table.cell(r_idx, c_idx)
            cell.width = Inches(widths[c_idx])
            text = row[c_idx] if c_idx < len(row) else ""
            p = cell.paragraphs[0]
            add_inline(p, text, size=8.3 if cols >= 7 else 9)
    style_table(table, header=True, font_size=8.3 if cols >= 7 else 9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_architecture_diagram(doc):
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(caption.add_run("圖 1  智慧停車 AI Agent 八模組架構"), size=10, bold=True)
    steps = [
        "① User and GIS Interface", "② Agent Orchestrator",
        "③ Data Connectors", "④ Data Quality and Storage",
        "⑤ Prediction Engine", "⑥ Domain Decision Engine",
        "⑦ Recommendation Agent", "⑧ Output and Evaluation",
    ]
    table = doc.add_table(rows=4, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i in range(4):
        left = table.cell(i, 0)
        arrow = table.cell(i, 1)
        right = table.cell(i, 2)
        for cell, text in ((left, steps[i * 2]), (right, steps[i * 2 + 1])):
            set_cell_shading(cell, LIGHT_BLUE if i % 2 == 0 else PALE_BLUE)
            set_cell_border(cell, color="9FBAD0", size="8")
            set_cell_margins(cell, top=130, bottom=130)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_run_font(p.add_run(text), size=10, bold=True, color=NAVY)
        set_cell_border(arrow, color="FFFFFF", size="0")
        p = arrow.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p.add_run("→"), size=16, bold=True, color=NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_flowchart_diagram(doc):
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(caption.add_run("圖 2  推薦流程與失效處理"), size=10, bold=True)
    stages = [
        ("輸入", "目的地、抵達時間、預算與步行限制"),
        ("候選與資料", "搜尋附近資源並取得即時與歷史資料"),
        ("品質決策", "檢查欄位、資料時間、缺失、故障與服務狀態"),
        ("預測", "使用已驗證模型；不可用時採標示清楚的基準"),
        ("領域決策", "套用容量、費率、距離、偏好與風險規則"),
        ("輸出與驗證", "顯示推薦證據並保存預測供事後比較"),
    ]
    table = doc.add_table(rows=len(stages), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (stage, desc) in enumerate(stages):
        c0, c1 = table.cell(i, 0), table.cell(i, 1)
        set_cell_shading(c0, NAVY)
        set_cell_shading(c1, "FFFFFF" if i % 2 == 0 else PALE_BLUE)
        for c in (c0, c1):
            set_cell_border(c)
            set_cell_margins(c, top=110, bottom=110)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p0.add_run(stage), size=9.5, bold=True, color="FFFFFF")
        p1 = c1.paragraphs[0]
        add_inline(p1, desc, size=9.5)
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(note.add_run("失效路徑：資料過期或無有效候選時，系統說明限制並回傳調整選項。"), size=9, color="555555")


def add_architecture_diagram(doc):
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(caption.add_run("Figure 1  Agent planning and tool architecture"), size=10, bold=True)
    rows = [
        ("Main 1", "User / GIS -> Planner -> Tool Selection"),
        ("Main 2", "Connectors -> Schema / Freshness / Quality Gate"),
        ("Valid", "Past-only Features -> Model / Baseline -> Risk Rules"),
        ("Output", "Top-k -> Evidence -> Arrival Verification"),
        ("Retry loop", "Retryable error -> Retry / Replan -> Planner"),
        ("Human loop", "Low confidence / unrecoverable -> Human Review -> Planner"),
    ]
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    for i, (stage, path) in enumerate(rows):
        table.cell(i, 0).text = stage
        table.cell(i, 1).text = path
    style_table(table, header=False, font_size=9.2)
    for row in table.rows:
        set_cell_shading(row.cells[0], NAVY)
        for run in row.cells[0].paragraphs[0].runs:
            set_run_font(run, size=9.2, bold=True, color="FFFFFF")
    note = doc.add_paragraph("Every tool call is logged as evidence. The agent abstains when no valid source remains.")
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_flowchart_diagram(doc):
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(caption.add_run("Figure 2  Decision loop exception and human interaction"), size=10, bold=True)
    stages = [
        ("Plan", "Parse objective and success criteria"),
        ("Select", "Choose a tool by capability and health"),
        ("Call", "Retryable error -> Retry / Replan -> Select"),
        ("Validate", "Schema time capacity; no alternative -> Human Review"),
        ("Predict", "Validated model; otherwise Persistence baseline"),
        ("Decide", "Use each observation's own quality; low confidence -> Human Review"),
        ("Explain", "Top-k sources timestamps errors and limits"),
        ("Verify", "Arrival check; drift or calibration failure -> Plan"),
    ]
    table = doc.add_table(rows=len(stages), cols=2)
    table.style = "Table Grid"
    for i, (stage, desc) in enumerate(stages):
        table.cell(i, 0).text = stage
        table.cell(i, 1).text = desc
    style_table(table, header=False, font_size=9.0)
    for row in table.rows:
        set_cell_shading(row.cells[0], NAVY)
        for run in row.cells[0].paragraphs[0].runs:
            set_run_font(run, size=9.0, bold=True, color="FFFFFF")


def configure_styles(doc):
    styles = doc.styles
    for style_name in ("Normal", "Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3", "Heading 4"):
        style = styles[style_name]
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        style.font.color.rgb = RGBColor(0, 0, 0)
    styles["Normal"].font.size = Pt(11)
    styles["Normal"].paragraph_format.line_spacing = 1.25
    styles["Normal"].paragraph_format.space_after = Pt(6)
    styles["Title"].font.size = Pt(23)
    styles["Title"].font.bold = True
    styles["Title"].paragraph_format.space_after = Pt(14)
    title_ppr = styles["Title"].element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)
    styles["Subtitle"].font.size = Pt(12)
    styles["Subtitle"].font.italic = False
    styles["Heading 1"].font.size = Pt(17)
    styles["Heading 1"].font.bold = True
    styles["Heading 1"].paragraph_format.space_before = Pt(14)
    styles["Heading 1"].paragraph_format.space_after = Pt(7)
    styles["Heading 1"].paragraph_format.keep_with_next = True
    styles["Heading 2"].font.size = Pt(14)
    styles["Heading 2"].font.bold = True
    styles["Heading 2"].paragraph_format.space_before = Pt(11)
    styles["Heading 2"].paragraph_format.space_after = Pt(5)
    styles["Heading 2"].paragraph_format.keep_with_next = True
    styles["Heading 3"].font.size = Pt(12)
    styles["Heading 3"].font.bold = True
    styles["Heading 3"].paragraph_format.space_before = Pt(8)
    styles["Heading 3"].paragraph_format.space_after = Pt(4)
    styles["Heading 3"].paragraph_format.keep_with_next = True
    styles["Heading 4"].font.size = Pt(11)
    styles["Heading 4"].font.bold = True
    styles["Heading 4"].paragraph_format.space_before = Pt(6)
    styles["Heading 4"].paragraph_format.space_after = Pt(3)
    styles["Heading 4"].paragraph_format.keep_with_next = True


def add_footer(doc):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p.add_run("智慧停車 AI Agent Proposal"), size=8, color="666666")


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    configure_styles(doc)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(title.add_run("智慧停車 AI Agent"), size=23, bold=True)
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(subtitle.add_run("臺中市剩餘車位預測與推薦 Proposal"), size=16, bold=True)
    english = doc.add_paragraph()
    english.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(english.add_run("Smart Parking AI Agent for Parking Availability Prediction and Recommendation in Taichung City"), size=10, color="555555")
    doc.add_paragraph()
    meta = doc.add_table(rows=3, cols=2)
    meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row, left, right in ((0, "課程", "物聯網應用與資料分析"), (1, "文件", "Final Project Proposal"), (2, "日期", "2026 年 11 月")):
        meta.cell(row, 0).text = left
        meta.cell(row, 1).text = right
    style_table(meta, header=False, font_size=10)
    doc.add_page_break()

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 2
    table_rows = []
    in_code = False
    code_lang = ""
    code_lines = []
    last_heading = ""
    while i < len(lines):
        line = lines[i]
        if line.startswith("英文題目："):
            i += 1
            continue
        if line.startswith("```"):
            if not in_code:
                if table_rows:
                    add_markdown_table(doc, table_rows)
                    table_rows = []
                in_code = True
                code_lang = line[3:].strip()
                code_lines = []
            else:
                if code_lang == "mermaid":
                    if "Architecture" in last_heading:
                        add_architecture_diagram(doc)
                    else:
                        add_flowchart_diagram(doc)
                else:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.2)
                    p.paragraph_format.right_indent = Inches(0.2)
                    p.paragraph_format.space_after = Pt(8)
                    for idx, code_line in enumerate(code_lines):
                        run = p.add_run(code_line + ("\n" if idx < len(code_lines) - 1 else ""))
                        set_run_font(run, name=MONO, size=8.5, color="222222")
                in_code = False
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if line.startswith("|"):
            table_rows.append(line)
            i += 1
            continue
        if table_rows:
            add_markdown_table(doc, table_rows)
            table_rows = []
        if not line.strip():
            i += 1
            continue
        heading = re.match(r"^(#{2,4})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1)) - 1
            text = heading.group(2).replace(" and ", " and ")
            last_heading = text
            if "Article Summary Table" in text or "System Architecture" in text:
                doc.add_page_break()
            p = doc.add_paragraph(style=f"Heading {level}")
            add_inline(p, text, size={1: 17, 2: 14, 3: 12}.get(level, 11))
            i += 1
            continue
        if re.match(r"^\d+\.\s+", line):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.22)
            p.paragraph_format.first_line_indent = Inches(-0.22)
            add_inline(p, line, size=11)
            i += 1
            continue
        if line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, line[2:], size=11)
            i += 1
            continue
        if line.startswith("$$"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_run_font(p.add_run(line.strip("$").strip()), name=MONO, size=10)
            i += 1
            continue
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_inline(p, line, size=11)
        i += 1
    if table_rows:
        add_markdown_table(doc, table_rows)
    add_footer(doc)
    doc.core_properties.title = "智慧停車 AI Agent 臺中市剩餘車位預測與推薦 Proposal"
    doc.core_properties.subject = "Final Project Proposal"
    doc.core_properties.keywords = "Smart Parking, AI Agent, Taichung, Parking Prediction"
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
