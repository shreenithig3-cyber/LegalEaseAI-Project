import io
import re
import html

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT


# -----------------------------------
# Filename helper
# -----------------------------------

def export_filename(document_type, extension):
    """
    Creates a safe filename for downloaded documents.
    """

    name = str(document_type).strip()

    if not name:
        name = "LegalEase_Document"

    # Replace characters that are unsafe in Windows filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)

    # Replace multiple spaces with underscore
    name = re.sub(r'\s+', '_', name)

    return f"{name}.{extension}"


# -----------------------------------
# Plain text export
# -----------------------------------

def format_txt(document):
    """
    Converts document content into UTF-8 text bytes.
    """

    if document is None:
        document = ""

    return str(document).encode("utf-8")


# -----------------------------------
# HTML preview
# -----------------------------------

def format_html_preview(document):
    """
    Converts plain document text into simple HTML
    for displaying inside Streamlit.
    """

    if document is None:
        document = ""

    text = str(document)

    # Escape HTML characters for safety
    text = html.escape(text)

    lines = text.splitlines()

    output = []

    for line in lines:

        line = line.strip()

        if not line:
            output.append('<div class="blank"></div>')
            continue

        # Convert simple headings
        if line.startswith("# "):
            heading = line[2:].strip()
            output.append(
                f"<h3>{heading}</h3>"
            )

        # Convert bullet points
        elif line.startswith("- "):
            bullet = line[2:].strip()
            output.append(
                f'<div class="bullet">• {bullet}</div>'
            )

        elif line.startswith("* "):
            bullet = line[2:].strip()
            output.append(
                f'<div class="bullet">• {bullet}</div>'
            )

        else:
            output.append(
                f"<p>{line}</p>"
            )

    return "\n".join(output)


# -----------------------------------
# DOCX export
# -----------------------------------

def format_docx(document, document_type="Legal Document"):
    """
    Creates a DOCX document and returns it as bytes.
    """

    if document is None:
        document = ""

    doc = Document()

    # Title
    title = doc.add_heading(
        str(document_type),
        level=1
    )

    # Document content
    text = str(document)

    for line in text.splitlines():

        line = line.strip()

        if not line:
            doc.add_paragraph("")
            continue

        # Heading
        if line.startswith("# "):

            heading = line[2:].strip()

            doc.add_heading(
                heading,
                level=2
            )

        # Bullet point
        elif line.startswith("- "):

            bullet = line[2:].strip()

            doc.add_paragraph(
                bullet,
                style="List Bullet"
            )

        elif line.startswith("* "):

            bullet = line[2:].strip()

            doc.add_paragraph(
                bullet,
                style="List Bullet"
            )

        else:

            doc.add_paragraph(line)

    # Save document into memory
    buffer = io.BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# -----------------------------------
# PDF export
# -----------------------------------

def format_pdf(document, document_type="Legal Document"):
    """
    Creates a PDF document and returns it as bytes.
    """

    if document is None:
        document = ""

    buffer = io.BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    body_style = styles["BodyText"]

    body_style.alignment = TA_LEFT

    story = []

    # Title
    story.append(
        Paragraph(
            html.escape(str(document_type)),
            title_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Content
    text = str(document)

    for line in text.splitlines():

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 8)
            )
            continue

        # Heading
        if line.startswith("# "):

            heading = line[2:].strip()

            story.append(
                Paragraph(
                    f"<b>{html.escape(heading)}</b>",
                    body_style
                )
            )

            story.append(
                Spacer(1, 8)
            )

        # Bullet
        elif line.startswith("- "):

            bullet = line[2:].strip()

            story.append(
                Paragraph(
                    f"• {html.escape(bullet)}",
                    body_style
                )
            )

        elif line.startswith("* "):

            bullet = line[2:].strip()

            story.append(
                Paragraph(
                    f"• {html.escape(bullet)}",
                    body_style
                )
            )

        else:

            story.append(
                Paragraph(
                    html.escape(line),
                    body_style
                )
            )

        story.append(
            Spacer(1, 5)
        )

    pdf.build(story)

    buffer.seek(0)

    return buffer.getvalue()