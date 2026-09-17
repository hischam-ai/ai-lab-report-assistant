import pandas as pd
import streamlit as st


def show_quality_panel(
    quality_score: int | float,
    quality_comments: list[str],
    outlier_comments: list[str],
    measurement_recommendations: list[str],
    outlier_df: pd.DataFrame,
    replicate_df: pd.DataFrame,
    replicate_precision_df: pd.DataFrame,
    replicate_precision_comments: list[str],
) -> None:
    """Zeigt Datenqualität, Ausreißer und Messpunkt-Empfehlungen an."""

    st.subheader("📊 Datenqualität")

    if quality_score >= 8:
        st.success(f"Qualitäts-Score: {quality_score}/10")
    elif quality_score >= 5:
        st.warning(f"Qualitäts-Score: {quality_score}/10")
    else:
        st.error(f"Qualitäts-Score: {quality_score}/10")

    for comment in quality_comments:
        st.write(f"• {comment}")

    st.subheader("🔎 Ausreißer-Analyse")

    for comment in outlier_comments:
        st.write(f"• {comment}")

    st.subheader("🧪 Vorschläge für weitere Messungen")

    for recommendation in measurement_recommendations:
        st.write(f"• {recommendation}")
    st.subheader("🔁 Replikat-Analyse")

    if replicate_df.empty:
        st.info("Keine mehrfach gemessenen Substratkonzentrationen gefunden.")
    else:
        st.success(
            f"{len(replicate_df)} Substratkonzentration(en) wurden mehrfach gemessen."
        )

        st.dataframe(
            replicate_df,
            width="stretch",
        )
    st.markdown("**Präzision der Replikate**")

    if not replicate_precision_df.empty:
        st.dataframe(
            replicate_precision_df.round(3),
            width="stretch",
        )

    for comment in replicate_precision_comments:
        st.write(f"• {comment}")

    with st.expander("Detaillierte Abweichungen anzeigen"):
        display_outliers = outlier_df.copy()

        display_outliers["Erwartete Geschwindigkeit"] = (
            display_outliers["Erwartete Geschwindigkeit"].round(4)
        )

        display_outliers["Absolute Abweichung"] = (
            display_outliers["Absolute Abweichung"].round(4)
        )

        display_outliers["Abweichung (%)"] = (
            display_outliers["Abweichung (%)"].round(1)
        )

        st.dataframe(
            display_outliers[
                [
                    "Messpunkt",
                    "Substrat",
                    "Geschwindigkeit",
                    "Erwartete Geschwindigkeit",
                    "Abweichung (%)",
                    "Ausreißer",
                ]
            ],
            width="stretch",
        )