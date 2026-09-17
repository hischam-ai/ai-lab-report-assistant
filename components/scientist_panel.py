import streamlit as st


def show_scientist_panel(assessment):
    """Zeigt die wissenschaftliche Bewertung."""

    st.subheader("🧪 AI Scientist")

    confidence = assessment["confidence"]

    if confidence == "hoch":
        st.success(f"Vertrauen in die Parameterschätzung: {confidence}")
    elif confidence == "mittel":
        st.warning(f"Vertrauen in die Parameterschätzung: {confidence}")
    else:
        st.error(f"Vertrauen in die Parameterschätzung: {confidence}")

    st.markdown("### 📋 Wissenschaftliche Zusammenfassung")
    st.info(assessment["summary"])

    st.markdown("### ✅ Stärken")
    for item in assessment["strengths"]:
        st.write(f"• {item}")

    st.markdown("### ⚠️ Schwächen")
    for item in assessment["weaknesses"]:
        st.write(f"• {item}")

    st.markdown("### 💡 Empfehlungen")
    for item in assessment["recommendations"]:
        st.write(f"• {item}")