import pandas as pd
import streamlit as st

from comparison import (
    analyze_experiment,
    show_experiment_comparison_plot,
)
from comparison_analysis import build_comparison_summary
from comparison_report import create_comparison_pdf


def show_comparison_panel():
    st.header("📊 Vergleich mehrerer Experimente")

    comparison_files = st.file_uploader(
        "Mehrere Excel-Dateien auswählen",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        key="comparison_files",
    )

    if not comparison_files:
        return

    results = []

    for file in comparison_files:
        try:
            results.append(analyze_experiment(file))
        except Exception as error:
            st.error(f"{file.name}: {error}")

    if not results:
        return
    if len(results) < 2:
        st.warning(
        "Bitte mindestens zwei gültige Experimente hochladen, "
        "um einen Vergleich durchzuführen."
    )
    return
    

    comparison_df = pd.DataFrame(
        [
            {
                "Datei": result["Datei"],
                "Vmax": result["Vmax"],
                "Km": result["Km"],
                "R²": result["R²"],
            }
            for result in results
        ]
    )

    st.dataframe(comparison_df, width="stretch")

    summary = build_comparison_summary(comparison_df)

    best_vmax = summary["best_vmax"]
    best_km = summary["best_km"]
    best_r2 = summary["best_r2"]

    st.subheader("📌 Kurzes Fazit")

    same_experiment = best_vmax["Datei"] == best_km["Datei"]

    if same_experiment:
        st.success(
            f"{best_vmax['Datei']} schneidet insgesamt am stärksten ab: "
            "Es erreicht die höchste maximale Reaktionsgeschwindigkeit "
            "und arbeitet gleichzeitig schon bei wenig Substrat effizient."
        )
    else:
        st.info(
            f"Wenn maximale Leistung wichtig ist, ist "
            f"{best_vmax['Datei']} besser geeignet. "
            f"Wenn wenig Substrat vorhanden ist, ist "
            f"{best_km['Datei']} günstiger."
        )

    if best_r2["R²"] >= 0.98:
        st.write(
            f"Die beste Modellanpassung hat {best_r2['Datei']} "
            f"(R² = {best_r2['R²']:.4f})."
        )
    elif best_r2["R²"] >= 0.95:
        st.write(
            f"Die beste Modellanpassung ist insgesamt gut "
            f"({best_r2['Datei']}, R² = {best_r2['R²']:.4f})."
        )
    else:
        st.warning(
            "Auch die beste Modellanpassung ist nicht optimal. "
            "Die Ergebnisse sollten vorsichtig interpretiert werden."
        )

    st.subheader("🧠 Einfach erklärt")

    st.write(
        f"🚀 **Höchste Vmax:** {best_vmax['Datei']} "
        f"mit {best_vmax['Vmax']:.2f}. "
        "Dieses Experiment erreicht die höchste maximale Reaktionsgeschwindigkeit."
    )

    st.write(
        f"🎯 **Kleinster Km:** {best_km['Datei']} "
        f"mit {best_km['Km']:.2f}. "
        "Dieses Experiment arbeitet schon bei geringerer Substratkonzentration effizient."
    )

    st.write(
        f"📈 **Bestes R²:** {best_r2['Datei']} "
        f"mit {best_r2['R²']:.4f}. "
        "Hier passen Modell und Messdaten am besten zusammen."
    )

    vmax_diff = comparison_df["Vmax"].max() - comparison_df["Vmax"].min()
    km_diff = comparison_df["Km"].max() - comparison_df["Km"].min()

    st.info(
        f"""
**Vergleichszusammenfassung**

• Unterschied Vmax: {vmax_diff:.2f}

• Unterschied Km: {km_diff:.2f}

• Anzahl Experimente: {len(comparison_df)}
"""
    )

    csv_data = comparison_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Vergleich als CSV herunterladen",
        data=csv_data,
        file_name="experimentvergleich.csv",
        mime="text/csv",
    )

    st.bar_chart(
        comparison_df.set_index("Datei")[["Vmax", "Km"]]
    )

    st.subheader("📈 Gemeinsamer Michaelis-Menten-Vergleich")

    comparison_plot_image = show_experiment_comparison_plot(results)

    comparison_pdf_path = create_comparison_pdf(
        comparison_df,
        summary,
        comparison_plot_image,
    )

    with open(comparison_pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label="📄 Vergleichs-PDF herunterladen",
        data=pdf_bytes,
        file_name="experimentvergleich.pdf",
        mime="application/pdf",
    )

    st.subheader("👀 So liest du den Vergleich")

    st.write(
        "• Eine Kurve, die weiter oben liegt, erreicht eine höhere "
        "Reaktionsgeschwindigkeit."
    )

    st.write(
        "• Ein höheres Vmax bedeutet: Das Enzym kann insgesamt mehr leisten."
    )

    st.write(
        "• Ein kleinerer Km bedeutet: Das Enzym arbeitet schon bei weniger "
        "Substrat effizient."
    )

    st.write(
        "• Ein R² nahe 1 bedeutet: Die Messdaten passen sehr gut zum Modell."
    )

    st.info(
        f"Für maximale Leistung ist {best_vmax['Datei']} am stärksten. "
        f"Bei niedriger Substratkonzentration ist {best_km['Datei']} günstiger."
    )