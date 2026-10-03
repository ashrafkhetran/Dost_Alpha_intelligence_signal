"""Document export helpers."""

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _inline(text: str) -> str:
    """Escape text for ReportLab and turn bare URLs into clickable links."""
    import re

    safe = escape(text.replace("**", ""))
    return re.sub(r"(https?://[^\s<]+)", r'<link href="\1" color="#5336A5">\1</link>', safe)


def render_brief_pdf(title: str, markdown: str, footer: str = "DOST ALPHA  |  Illustrative sample briefing") -> bytes:
    """Render a printable executive briefing PDF."""
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.7 * inch,
        title=title,
        author="DOST ALPHA",
    )
    base_styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "BriefTitle",
        parent=base_styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#5336A5"),
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        spaceAfter=18,
    )
    heading_style = ParagraphStyle(
        "BriefHeading",
        parent=base_styles["Heading2"],
        textColor=colors.HexColor("#25243A"),
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "BriefBody",
        parent=base_styles["BodyText"],
        textColor=colors.HexColor("#465066"),
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        spaceAfter=6,
    )
    story = [Paragraph(escape(title), title_style)]
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 3))
        elif stripped.startswith("#"):
            story.append(Paragraph(_inline(stripped.lstrip("#").strip()), heading_style))
        elif stripped.startswith(("- ", "* ")):
            story.append(Paragraph(f"&bull;&nbsp; {_inline(stripped[2:])}", body_style))
        elif stripped[:1].isdigit() and ". " in stripped[:4]:
            item = stripped.split(". ", 1)[1]
            story.append(Paragraph(f"&bull;&nbsp; {_inline(item)}", body_style))
        else:
            story.append(Paragraph(_inline(stripped), body_style))

    def draw_footer(canvas, _document) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
        canvas.line(0.75 * inch, 0.55 * inch, 7.75 * inch, 0.55 * inch)
        canvas.setFillColor(colors.HexColor("#768198"))
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.75 * inch, 0.38 * inch, footer)
        canvas.drawRightString(7.75 * inch, 0.38 * inch, str(canvas.getPageNumber()))
        canvas.restoreState()

    document.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return buffer.getvalue()
