import pandas as pd
import streamlit as st
from excel_template import create_excel_template
from data_validation import clean_measurement_data, validate_measurement_data


def show_upload_panel():
    """Lädt eine Excel-Datei, prüft sie und gibt bereinigte Messdaten zurück."""
    st.info(
    "📋 Erwartetes Dateiformat: Excel-Datei mit den Spalten "
    "'Substrat' und 'Geschwindigkeit'. "
    "Es werden mindestens 4 gültige Messpunkte benötigt."
)
    template_file = create_excel_template()

    st.download_button(
    label="📥 Excel-Vorlage herunterladen",
    data=template_file,
    file_name="michaelis_menten_vorlage.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
    uploaded_file = st.file_uploader(
        "Excel-Datei hochladen",
        type=["xlsx", "xls"],
    )

    if uploaded_file is None:
        return None

    try:
        if uploaded_file.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif uploaded_file.name.lower().endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Bitte eine gültige Excel-Datei (.xlsx oder .xls) hochladen.")
            return None

    except Exception:
        st.error(
        "Die Excel-Datei konnte nicht gelesen werden. "
        "Bitte prüfe, ob die Datei eine gültige und nicht beschädigte Excel-Datei ist."
    )
        return None
    df.columns = df.columns.astype(str).str.strip()
    required_columns = {"Substrat", "Geschwindigkeit"}

    if not required_columns.issubset(df.columns):
        st.error(
            "Die Excel-Datei muss die Spalten "
            "'Substrat' und 'Geschwindigkeit' enthalten."
        )
        return None

    df = clean_measurement_data(df)

    is_valid, error_message = validate_measurement_data(df)

    if not is_valid:
        st.error(error_message)
        return None
        

   

    st.success("Datei erfolgreich geladen!")
    st.subheader("Vorschau der Daten")
    st.dataframe(df, width="stretch")

    return df