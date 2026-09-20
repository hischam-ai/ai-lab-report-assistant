from io import BytesIO

import pandas as pd
import streamlit as st
import traceback

from report import create_pdf_report


def show_pdf_download(
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
    quality_score: int | float,
    quality_comments: list[str],
    statistics,
    replicate_precision_df: pd.DataFrame,
    replicate_precision_comments: list[str],
) -> None:
    """Erstellt den PDF-Bericht und zeigt den Download-Button an."""

    try:
        pdf_report = create_pdf_report(
            df,
            vmax,
            km,
            r2,
            plot_image,
        lineweaver_image,
        project_name,
        sample_name,
        notes,
        ai_text,
        lab_advice,
        quality_score,
        quality_comments,
        statistics,
        replicate_precision_df,
        replicate_precision_comments,
    
    )
        print("PDF-RÜCKGABE:", type(pdf_report), len(pdf_report) if pdf_report is not None else None)

    except Exception:
        st.error("Fehler beim Erstellen des PDF-Berichts:")
        st.code(traceback.format_exc())
        return
    st.download_button(
        label="📄 PDF-Bericht herunterladen",
        data=pdf_report,
        file_name="michaelis_menten_report.pdf",
        mime="application/pdf",
    )