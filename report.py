from io import BytesIO
from datetime import datetime

import pandas as pd
from ai_report import generate_ai_report
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def create_pdf_report(
    df: pd.DataFrame,
    vmax: float,
    km: float,
    r2: float,
    plot_image: BytesIO,
    project_name,
    sample_name,
    notes,
) -> bytes:
    """Erstellt einen einfachen PDF-Bericht im Arbeitsspeicher."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("Lab Report Assistant", styles["Title"])
    )
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(
    Paragraph(f"<b>Projekt:</b> {project_name}", styles["Normal"])
    )

    elements.append(
    Paragraph(f"<b>Probe:</b> {sample_name}", styles["Normal"])
    )

    if notes.strip():
        elements.append(
    Paragraph(f"<b>Notizen:</b> {notes}", styles["Normal"])
    )

    elements.append(Spacer(1, 0.5 * cm))
    date_text = datetime.now().strftime("%d.%m.%Y")
    elements.append(
    Paragraph(f"Auswertungsdatum: {date_text}", styles["Normal"])
    )
    elements.append(Spacer(1, 0.7 * cm))

    elements.append(
    Paragraph("Michaelis-Menten-Parameter", styles["Heading2"])
    )

    parameter_data = [
        ["Parameter", "Wert"],
        ["Vmax", f"{vmax:.2f}"],
        ["Km", f"{km:.2f}"],
        ["R²", f"{r2:.4f}"],
    ]

    parameter_table = Table(
        parameter_data,
        colWidths=[7 * cm, 7 * cm],
    )

    parameter_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    elements.append(parameter_table)
    elements.append(Spacer(1, 0.7 * cm))

    elements.append(
        Paragraph("Michaelis-Menten-Kurve", styles["Heading2"])
    )

    plot_image.seek(0)

    plot = Image(
    plot_image,
    width=16 * cm,
    height=10 * cm,
)

    elements.append(plot)
    elements.append(Spacer(1, 0.7 * cm))

    elements.append(
        Paragraph("Messdaten", styles["Heading2"])
)
    measurement_data = [
        ["Substrat", "Geschwindigkeit"]
    ]

    for _, row in df.iterrows():
        measurement_data.append(
            [
                f"{row['Substrat']:.4g}",
                f"{row['Geschwindigkeit']:.4g}",
            ]
        )

    measurement_table = Table(
        measurement_data,
        colWidths=[7 * cm, 7 * cm],
    )

    measurement_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(measurement_table)
    elements.append(Spacer(1, 0.7 * cm))

    interpretation = generate_ai_report(
    vmax,
    km,
    r2,
    notes,
)

    elements.append(
        Paragraph("Automatische Zusammenfassung", styles["Heading2"])
    )
    elements.append(
        Paragraph(interpretation, styles["BodyText"])
    )

    document.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes