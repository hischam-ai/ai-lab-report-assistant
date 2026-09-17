import streamlit as st

from ai_report import ask_ai, generate_ai_report
from analysis import (
    calculate_parameter_statistics,
    calculate_r2,
    fit_michaelis_menten,
)
from components.quality_panel import show_quality_panel
from lab_advisor import evaluate_data_quality, generate_lab_advice
from plots import (
    show_lineweaver_burk_plot,
    show_measurement_plot,
    show_residual_plot,
)

from quality_analysis import (
    analyze_replicate_precision,
    detect_outliers,
    detect_replicates,
    summarize_measurement_recommendations,
    summarize_outliers,
    summarize_replicate_precision,
    
)
from components.pdf_panel import show_pdf_download
from components.parameter_panel import show_parameter_panel
from components.ai_panel import show_ai_results
from components.upload_panel import show_upload_panel
from components.scientist_panel import show_scientist_panel
from components.comparison_panel import show_comparison_panel
from scientist_analysis import build_scientific_assessment

st.set_page_config(
    page_title="Lab Report Assistant",
    page_icon="🧪",
)

st.title("🧪 Lab Report Assistant")
st.write(
    "Excel-Daten analysieren, Michaelis-Menten-Parameter berechnen "
    "und Laborberichte vorbereiten."
)

single_tab, comparison_tab = st.tabs(
    [
        "🧪 Einzelanalyse",
        "📊 Experimentvergleich",
    ]
)

with single_tab:
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

    df = show_upload_panel()

    if df is not None:
        try:
            vmax, km = fit_michaelis_menten(df)
            r2 = calculate_r2(df, vmax, km)
            statistics = calculate_parameter_statistics(df)

            plot_image = show_measurement_plot(df, vmax, km)

            st.subheader("📈 Lineweaver-Burk")
            lineweaver_image = show_lineweaver_burk_plot(df)
            st.subheader("📉 Residuenanalyse")
            show_residual_plot(
                df,
                vmax,
                km,
            )

            if "ai_text" not in st.session_state:
                st.session_state.ai_text = None

            if "lab_advice" not in st.session_state:
                st.session_state.lab_advice = None

            replicate_df = detect_replicates(df)
            replicate_precision_df = analyze_replicate_precision(df)
            quality_score, quality_comments = evaluate_data_quality(
                df,
                vmax,
                km,
                r2,
                replicate_precision_df,
            )

            outlier_df = detect_outliers(
                df,
                vmax,
                km,
            )

            outlier_comments = summarize_outliers(outlier_df)

            measurement_recommendations = summarize_measurement_recommendations(
                df,
                km,
            )
            
            replicate_precision_comments = summarize_replicate_precision(
            replicate_precision_df
)
            scientific_assessment = build_scientific_assessment(
                df,
                vmax,
                km,
                r2,
                quality_score,
                quality_comments,
                outlier_comments,
                measurement_recommendations,
                replicate_precision_df,
            )

            if st.button("🔬 Analyse starten", type="primary"):
                with st.spinner("🤖 KI analysiert die Versuchsdaten..."):
                    st.session_state.ai_text = generate_ai_report(
                        vmax,
                        km,
                        r2,
                        notes,
                    )

                    st.session_state.lab_advice = generate_lab_advice(
                        df,
                        vmax,
                        km,
                        r2,
                        notes,
                        outlier_comments,
                        measurement_recommendations,
                    )

            ai_text = st.session_state.ai_text
            lab_advice = st.session_state.lab_advice

            show_parameter_panel(
                vmax,
                km,
                r2,
                statistics,
            )

            show_quality_panel(
                quality_score,
                quality_comments,
                outlier_comments,
                measurement_recommendations,
                outlier_df,
                replicate_df,
                replicate_precision_df,
                replicate_precision_comments,
            )

            show_scientist_panel(scientific_assessment)
            show_ai_results(ai_text, lab_advice)

            if ai_text:
                st.subheader("💬 Frage die KI")

                question = st.text_input(
                    "Stelle eine Frage zu deinen Messdaten",
                    key="ai_question",
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

              

            else:
                st.info(
                    "Klicke auf „Analyse starten“, "
                    "um eine KI-Interpretation und Laborberatung zu erstellen."
                )
            show_pdf_download(
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
        except Exception as error:
            st.error(
                f"Die Datei konnte nicht ausgewertet werden: {error}"
            )


with comparison_tab:
    show_comparison_panel()