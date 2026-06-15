from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import os


# ======================
# BUILD PDF REPORT
# ======================

def build_pdf(df, output_path):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    elements = []

    # TITLE

    title = Paragraph(
        "AI-Based Predictive Credit Scoring Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    # SUBTITLE

    subtitle = Paragraph(
        f"Total Records: {len(df)}",
        styles["Normal"]
    )

    elements.append(subtitle)

    elements.append(
        Spacer(1, 12)
    )

    # TABLE DATA

    data = [list(df.columns)]

    for row in df.values.tolist():

        data.append(
            [str(item) for item in row]
        )

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkblue
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.beige
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )

        ])

    )

    elements.append(table)

    doc.build(elements)

    return output_path