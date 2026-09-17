import streamlit as st


def show_ai_results(ai_text, lab_advice):
    """Zeigt die KI-Interpretation und den Laborberater an."""

    if ai_text:
        st.subheader("🧠 KI-Interpretation")
        st.info(ai_text)

    if lab_advice:
        st.subheader("🧪 KI-Laborberater")
        st.success(lab_advice)