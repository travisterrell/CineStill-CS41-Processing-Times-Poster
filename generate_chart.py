from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ====== Tweakables ======
OUTPUT = "CineStill_CS41_Processing_Times_Chart.pdf"
TOP_MARGIN_PT = 60
BLOCK_SPACING_PT = 32        # space between step blocks
# ========================

doc = SimpleDocTemplate(OUTPUT, pagesize=letter, topMargin=TOP_MARGIN_PT)

title_style   = ParagraphStyle(name="Title",     fontSize=26, leading=30, alignment=1, spaceAfter=0)
subtitle_style= ParagraphStyle(name="Subtitle",  fontSize=18, leading=22, alignment=1, spaceAfter=26)
step_title    = ParagraphStyle(name="StepTitle", fontSize=22, leading=26, textColor=colors.white, alignment=1)
time_style    = ParagraphStyle(name="Time",      fontSize=40, leading=44, alignment=1, spaceAfter=6, textColor=colors.black)
text_style    = ParagraphStyle(name="Text",      fontSize=14, leading=18, alignment=1, textColor=colors.black)

elements = []
elements.append(Paragraph("CineStill Cs41 Process Reference", title_style))
elements.append(Paragraph("(39 °C / 102 °F)", subtitle_style))
elements.append(Spacer(1, 6))

steps = [
    ("Step 1: Developer", "3:30",
     "Roll 2 = 3:38 &nbsp;|&nbsp; Roll 3 = 3:46 &nbsp;|&nbsp; Roll 4 = 3:55",
    #  "Push +1 = 4:00  Push +2 = 4:30  Pull −1 = 3:00  Pull −2 = 2:30",
    #  "+1 = 4:00, +2 = 4:30, −1 = 3:00, −2 = 2:30",
    None,
     colors.HexColor("#C0392B")),
    ("Step 2: Bleach / Fix", "8:00",
     "Agitate 10 sec every 30 sec", None,
     colors.HexColor("#884EA0")),
    ("Step 3: Wash / Rinse", "3:00",
     "Running water; 7 changes or continuous flow", None,
     colors.HexColor("#2471A3")),
    ("Step 4: Stabilizer", "1:00",
     "Do not rinse afterwards", None,
     colors.HexColor("#229954")),
]

for title, t, line1, line2, bg in steps:
    data = [
        [Paragraph(title, step_title)],
        [Paragraph(f"<b>{t}</b>", time_style)],
        [Paragraph(line1, text_style) if line1 else Paragraph("", text_style)],
    ]
    if line2:
        data.append([Paragraph(line2, text_style)])
    table = Table(data, colWidths=[450])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), bg),
        ('BOX', (0,0), (-1,-1), 1.5, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,1), (-1,1), 0.8, colors.black),  # divider under the big time
    ]
    if line1:
        style_cmds.append(('LINEBELOW', (0,2), (-1,2), 0.8, colors.black))  # divider between reuse & push/pull
    table.setStyle(TableStyle(style_cmds))
    elements.append(table)
    elements.append(Spacer(1, BLOCK_SPACING_PT))

doc.build(elements)
print(f"Written: {OUTPUT}")