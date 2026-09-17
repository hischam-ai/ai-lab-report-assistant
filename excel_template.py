from io import BytesIO

import pandas as pd


def create_excel_template():
    """Erstellt eine einfache Excel-Vorlage für Michaelis-Menten-Messdaten."""

    template_df = pd.DataFrame(
        {
            "Substrat": [0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
            "Geschwindigkeit": [0.5, 0.9, 1.8, 3.0, 4.2, 5.4],
        }
    )

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        template_df.to_excel(
            writer,
            index=False,
            sheet_name="Messdaten",
        )

    output.seek(0)

    return output