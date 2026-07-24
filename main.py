import streamlit as st 
import pandas as pd

from plots import show_measurement_plot
from analysis import fit_michaelis_menten, calculate_r2
from report import create_pdf_report
from ai_report import generate_ai_report, ask_ai

st.set_page_config(
    page_title="Lab Report Assistant",
    page_icon="🧪",
)

st.title("🧪 Lab Report Assistant")
st.write(
    "Excel-Daten analysieren, Michaelis-Menten-Parameter berechnen "
    "und Laborberichte vorbereiten."
)
project_name = st.text_input(
    "Projektname",
    value="Michaelis-Menten-Auswertung",
)

sample_name = st.text_input(
    "Probenname",
    value="Probe 1",
)

notes = st.text_area(
    "Notizen",
    placeholder="Temperatur, pH-Wert, Enzymkonzentration ...",
)
uploaded_file = st.file_uploader(
    "Excel-Datei hochladen",
    type=["xlsx", "xls"],
)
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        required_columns = {"Substrat", "Geschwindigkeit"}

        if not required_columns.issubset(df.columns):
            st.error(
                "Die Excel-Datei muss die Spalten "
                "'Substrat' und 'Geschwindigkeit' enthalten."
            )
            st.stop()

        df = df[["Substrat", "Geschwindigkeit"]].dropna()

        df["Substrat"] = pd.to_numeric(
            df["Substrat"],
            errors="coerce",
        )

        df["Geschwindigkeit"] = pd.to_numeric(
            df["Geschwindigkeit"],
            errors="coerce",
        )

        df = df.dropna()

        if len(df) < 4:
            st.error("Es werden mindestens 4 gültige Messpunkte benötigt.")
            st.stop()

        st.success("Datei erfolgreich geladen!")

        st.subheader("Vorschau der Daten")
        st.dataframe(df)

        vmax, km = fit_michaelis_menten(df)
        r2 = calculate_r2(df, vmax, km)

        plot_image = show_measurement_plot(df, vmax, km)

        with st.spinner("🤖 KI analysiert die Versuchsdaten..."):
            ai_text = generate_ai_report(
                vmax,
                km,
                r2,
                notes,
            )

        st.subheader("Michaelis-Menten-Parameter")

        col1, col2 = st.columns(2)
        col1.metric("Vmax", f"{vmax:.2f}")
        col2.metric("Km", f"{km:.2f}")

        st.metric("R²", f"{r2:.4f}")

        st.subheader("🤖 KI-Interpretation")
        st.info(ai_text)

        st.subheader("💬 Frage die KI")

        question = st.text_input(
            "Stelle eine Frage zu deinen Messdaten"
        )

        if question:
            with st.spinner("KI beantwortet deine Frage..."):
                answer = ask_ai(
                    question,
                    df,
                    vmax,
                    km,
                    r2,
                    notes,
                )

            st.success(answer)

        pdf_report = create_pdf_report(
            df,
            vmax,
            km,
            r2,
            plot_image,
            project_name,
            sample_name,
            notes,
        )

        st.download_button(
            label="📄 PDF-Bericht herunterladen",
            data=pdf_report,
            file_name="michaelis_menten_report.pdf",
            mime="application/pdf",
        )

    except Exception as error:
        st.error(f"Die Datei konnte nicht ausgewertet werden: {error}")