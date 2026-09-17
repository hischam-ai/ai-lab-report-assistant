import streamlit as st


def show_parameter_panel(vmax, km, r2, statistics=None):
    """Zeigt die berechneten Michaelis-Menten-Parameter an."""

    st.subheader("📈 Michaelis-Menten-Parameter")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Vmax", f"{vmax:.2f}")

    with col2:
        st.metric("Km", f"{km:.2f}")

    st.metric("R²", f"{r2:.4f}")

    if statistics is None:
        return

    st.markdown("### 📊 Parameterunsicherheit")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Standardfehler Vmax",
            f"{statistics['vmax_standard_error']:.4f}",
        )

        ci = statistics["vmax_confidence_interval"]
        st.caption(
            f"95-%-KI: {ci[0]:.4f} bis {ci[1]:.4f}"
        )

    with col2:
        st.metric(
            "Standardfehler Km",
            f"{statistics['km_standard_error']:.4f}",
        )

        ci = statistics["km_confidence_interval"]
        st.caption(
            f"95-%-KI: {ci[0]:.4f} bis {ci[1]:.4f}"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("RMSE", f"{statistics['rmse']:.4f}")

    with col2:
        st.metric(
            "Freiheitsgrade",
            statistics["degrees_of_freedom"],
        )