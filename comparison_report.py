from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

def create_comparison_pdf(
    comparison_df,
    summary,
    plot_image,
    output_path="experimentvergleich.pdf",
)   :   
    """
    Erstellt einen PDF-Bericht für den Vergleich mehrerer Experimente.
    """

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []

    # Titel
    elements.append(
        Paragraph(
            "📊 Vergleich mehrerer Experimente",
            styles["Heading1"],
        )
    )
    elements.append(Spacer(1, 0.5 * cm))

    # Vergleichstabelle
    elements.append(
        Paragraph(
            "Parametervergleich",
            styles["Heading2"],
        )
    )

    table_data = [
        ["Datei", "Vmax", "Km", "R²"]
    ]

    for _, row in comparison_df.iterrows():
        table_data.append(
            [
                str(row["Datei"]),
                f"{row['Vmax']:.4f}",
                f"{row['Km']:.4f}",
                f"{row['R²']:.4f}",
            ]
        )

    comparison_table = Table(
        table_data,
        colWidths=[
            7 * cm,
            3 * cm,
            3 * cm,
            3 * cm,
        ],
    )

    comparison_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#DCE6F1"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#AAB7C4"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(comparison_table)
    elements.append(Spacer(1, 0.6 * cm))
    best_vmax = summary["best_vmax"]
    best_km = summary["best_km"]
    best_r2 = summary["best_r2"]

    elements.append(
        Paragraph(
            "Kurzes Fazit",
            styles["Heading2"],
        )
    )

    conclusion = (
        f"Für maximale Reaktionsgeschwindigkeit ist "
        f"<b>{best_vmax['Datei']}</b> am stärksten. "
        f"Bei niedriger Substratkonzentration ist "
        f"<b>{best_km['Datei']}</b> günstiger. "
        f"Die beste Modellanpassung zeigt "
        f"<b>{best_r2['Datei']}</b> "
        f"mit R² = {best_r2['R²']:.4f}."
    )

    elements.append(
        Paragraph(
            conclusion,
            styles["BodyText"],
        )
    )

    elements.append(Spacer(1, 0.7 * cm))
    elements.append(
        Paragraph(
            "Michaelis-Menten-Vergleich",
            styles["Heading2"],
        )
    )

    plot_image.seek(0)

    elements.append(
        Image(
            plot_image,
            width=16 * cm,
            height=9.5 * cm,
        )
    )

    elements.append(Spacer(1, 0.5 * cm))
    doc.build(elements)

    return output_path