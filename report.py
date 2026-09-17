from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    Image,
    PageBreak,
    KeepTogether,
)


def _register_unicode_font() -> str:
    """Registriert eine Unicode-Schrift und gibt ihren ReportLab-Namen zurück."""

    font_candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    ]

    for font_path in font_candidates:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont("LabUnicode", str(font_path)))
            return "LabUnicode"

    return "Helvetica"

def add_header_and_page_number(canvas, doc):
    """Fügt Kopfzeile und Seitenzahl ein."""

    canvas.saveState()

    page_width, page_height = A4
    page_num = canvas.getPageNumber()

    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(
        1.8 * cm,
        page_height - 1 * cm,
        "LabMind AI",
    )

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        page_width - 1.8 * cm,
        page_height - 1 * cm,
        "Automatische Enzymkinetik-Auswertung",
    )

    canvas.setStrokeColor(colors.HexColor("#B7C3D0"))
    canvas.setLineWidth(0.5)
    canvas.line(
        1.8 * cm,
        page_height - 1.15 * cm,
        page_width - 1.8 * cm,
        page_height - 1.15 * cm,
    )

    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(
        page_width - 1.8 * cm,
        1 * cm,
        f"Seite {page_num}",
    )

    canvas.restoreState()
def create_pdf_report(
    df: pd.DataFrame,
    vmax: float,
    km: float,
    r2: float,
    plot_image: BytesIO,
    lineweaver_image: BytesIO,
    project_name: str,
    sample_name: str,
    notes: str,
    ai_text: str,
    lab_advice: str,
    quality_score: int | float | None = None,
    quality_comments: list[str] | None = None,
    statistics: dict | None = None,
    replicate_precision_df: pd.DataFrame | None = None,
    replicate_precision_comments: list[str] | None = None,
) -> bytes:
    """Erstellt einen professionellen PDF-Bericht im Arbeitsspeicher."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title=project_name or "Lab Report Assistant",
        author="Lab Report Assistant",
    )

    font_name = _register_unicode_font()
    styles = getSampleStyleSheet()

    for style_name in ("Title", "Normal", "Heading1", "Heading2", "BodyText"):
        styles[style_name].fontName = font_name

    styles["Title"].fontSize = 22
    styles["Title"].leading = 27
    styles["Heading2"].spaceBefore = 8
    styles["Heading2"].spaceAfter = 6
    styles["BodyText"].leading = 15

    elements = []

    elements.append(Paragraph("LabMind AI", styles["Title"]))
    elements.append(
        Paragraph(
            "Automatische Enzymkinetik-Auswertung",
            styles["Heading2"],
        )
    )
    elements.append(Spacer(1, 0.7 * cm))

    date_text = datetime.now().strftime("%d.%m.%Y")

    metadata_data = [
        ["Projekt", project_name or "–"],
        ["Probe", sample_name or "–"],
        ["Auswertungsdatum", date_text],
        ["Notizen", notes.strip() if notes and notes.strip() else "–"],
    ]

    metadata_table = Table(
        metadata_data,
        colWidths=[4.2 * cm, 11.5 * cm],
    )
    metadata_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F6")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C3D0")),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(metadata_table)
    elements.append(Spacer(1, 0.65 * cm))
    if statistics is not None:
     elements.append(
        Paragraph("Parameterunsicherheit", styles["Heading2"])
    )

    vmax_ci = statistics["vmax_confidence_interval"]
    km_ci = statistics["km_confidence_interval"]

    statistics_data = [
        ["Kennzahl", "Wert"],
        [
            "Standardfehler Vmax",
            f"{statistics['vmax_standard_error']:.4f}",
        ],
        [
            "Standardfehler Km",
            f"{statistics['km_standard_error']:.4f}",
        ],
        [
            "RMSE",
            f"{statistics['rmse']:.4f}",
        ],
        [
            "Freiheitsgrade",
            str(statistics["degrees_of_freedom"]),
        ],
        [
            "95-%-KI Vmax",
            f"{vmax_ci[0]:.4f} – {vmax_ci[1]:.4f}",
        ],
        [
            "95-%-KI Km",
            f"{km_ci[0]:.4f} – {km_ci[1]:.4f}",
        ],
    ]

    statistics_table = Table(
        statistics_data,
        colWidths=[7.8 * cm, 7.8 * cm],
    )

    statistics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9AA8B5")),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(statistics_table)
    elements.append(Spacer(1, 0.65 * cm))

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
        colWidths=[7.8 * cm, 7.8 * cm],
    )
    parameter_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9AA8B5")),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.append(parameter_table)
    elements.append(Spacer(1, 0.65 * cm))

    plot_image.seek(0)

    michaelis_menten_section = KeepTogether(
        [
            Paragraph(
                "Michaelis-Menten-Kurve",
                    styles["Heading2"],
            ),
            Spacer(1, 0.25 * cm),
            Image(
                plot_image,
                width=16.2 * cm,
                height=9.7 * cm,
            ),
        ]
    )

    elements.append(michaelis_menten_section)


    elements.append(
        Paragraph("Lineweaver-Burk-Darstellung", styles["Heading2"])
)
    lineweaver_image.seek(0)
    elements.append(
        Image(
            lineweaver_image,
            width=14.5 * cm,
            height=8.7 * cm,
        )

    )
    elements.append(Spacer(1, 0.6 * cm))
    elements.append(PageBreak())
    elements.append(Paragraph("Messdaten", styles["Heading2"]))

    measurement_data = [["Substrat", "Geschwindigkeit"]]
    for _, row in df.iterrows():
        measurement_data.append(
            [
                f"{row['Substrat']:.4g}",
                f"{row['Geschwindigkeit']:.4g}",
            ]
        )

    measurement_table = Table(
        measurement_data,
        colWidths=[7.8 * cm, 7.8 * cm],
        repeatRows=1,
    )
    measurement_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#9AA8B5")),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(measurement_table)
    elements.append(Spacer(1, 0.7 * cm))

    if quality_score is not None:
        elements.append(Paragraph("Datenqualität", styles["Heading2"]))

        if quality_score >= 9:
            quality_color = colors.HexColor("#DFF3E4")
            quality_label = "Sehr gut"
        elif quality_score >= 6:
            quality_color = colors.HexColor("#FFF2CC")
            quality_label = "Verbesserungsfähig"
        else:
            quality_color = colors.HexColor("#F8D7DA")
            quality_label = "Kritisch"

        quality_summary = Table(
            [[
                Paragraph(
                    f"<b>Qualitäts-Score:</b> {quality_score:g}/10 "
                    f"({quality_label})",
                    styles["Normal"],
                )
            ]],
            colWidths=[15.6 * cm],
        )
        quality_summary.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), quality_color),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#AAB4BE")),
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ]
            )
        )

        elements.append(quality_summary)
        elements.append(Spacer(1, 0.35 * cm))

        for comment in quality_comments or []:
            clean_comment = str(comment).strip()
            if clean_comment:
                elements.append(
                    Paragraph(f"• {clean_comment}", styles["BodyText"])
                )

        elements.append(Spacer(1, 0.55 * cm))
        if replicate_precision_df is not None and not replicate_precision_df.empty:
     

         replicate_table_data = [
        [
            "Substrat",
            "Anzahl",
            "Mittelwert",
            "Standardabw.",
            "CV (%)",
        ]
    ]

    for _, row in replicate_precision_df.iterrows():
        replicate_table_data.append(
            [
                f"{row['Substrat']:.2f}",
                str(int(row["Anzahl Messungen"])),
                f"{row['Mittelwert']:.3f}",
                f"{row['Standardabweichung']:.3f}",
                f"{row['CV (%)']:.1f}",
            ]
        )

    replicate_table = Table(
        replicate_table_data,
        colWidths=[2.4 * cm, 2.2 * cm, 2.7 * cm, 3.2 * cm, 2.0 * cm],
    )

    replicate_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(
    KeepTogether(
        [
            Paragraph("Präzision der Replikate", styles["Heading2"]),
            Spacer(1, 0.25 * cm),
            replicate_table,
        ]
    )
)
    elements.append(Spacer(1, 0.55 * cm))
    if replicate_precision_comments:
        for comment in replicate_precision_comments:
            elements.append(
            Paragraph(f"• {comment}", styles["BodyText"])
        )

    elements.append(Spacer(1, 0.55 * cm))

    if r2 >= 0.98:
        fit_text = "eine sehr gute Modellanpassung"
    elif r2 >= 0.95:
        fit_text = "eine gute Modellanpassung"
    else:
        fit_text = "eine eingeschränkte Modellanpassung"

    if quality_score is not None and quality_score >= 8:
        quality_text = "Die Datenqualität ist insgesamt gut."
    elif quality_score is not None and quality_score >= 5:
        quality_text = "Die Datenqualität ist grundsätzlich brauchbar, kann aber verbessert werden."
    else:
        quality_text = "Die Datenqualität sollte vor einer abschließenden Interpretation kritisch geprüft werden."
    replicate_conclusion = ""

    if  replicate_precision_comments:
        replicate_conclusion = (
            "Die Replikat-Analyse zeigt erhöhte Streuungen bei einzelnen "
            "Substratkonzentrationen. Die Reproduzierbarkeit dieser Messungen "
            "sollte daher überprüft und gegebenenfalls durch weitere "
            "Wiederholungsmessungen verbessert werden. "
        )
        conclusion_text = (
            f"Die Michaelis-Menten-Auswertung zeigt {fit_text} "
            f"mit R² = {r2:.4f}. "
            f"Die geschätzten Parameter betragen Vmax = {vmax:.2f} "
            f"und Km = {km:.2f}. "
        f"{quality_text} "
        f"{replicate_conclusion}"
        "Zusätzliche Messpunkte im Bereich um Km können die "
        "Parameterschätzung weiter verbessern."
        )

        elements.append(Paragraph("Fazit", styles["Heading2"]))



        elements.append(
                Paragraph(
                    conclusion_text,
                    styles["BodyText"],
                )
    )

        document.build(
        elements,
        onFirstPage=add_header_and_page_number,
        onLaterPages=add_header_and_page_number,
    )

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes