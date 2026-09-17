import pandas as pd

from analysis import calculate_r2, fit_michaelis_menten
from io import BytesIO

def analyze_experiment(uploaded_file):
    df = pd.read_excel(uploaded_file)

    required_columns = {"Substrat", "Geschwindigkeit"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Die Datei muss die Spalten "
            "'Substrat' und 'Geschwindigkeit' enthalten."
        )

    df = df[["Substrat", "Geschwindigkeit"]].copy()

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
        raise ValueError(
            "Es werden mindestens 4 gültige Messpunkte benötigt."
        )

    vmax, km = fit_michaelis_menten(df)
    r2 = calculate_r2(df, vmax, km)

    return {
    "Datei": uploaded_file.name,
    "Vmax": vmax,
    "Km": km,
    "R²": r2,
    "Daten": df,
}
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def show_experiment_comparison_plot(results):
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for result in results:
        df = result["Daten"]
        vmax = result["Vmax"]
        km = result["Km"]
        label = result["Datei"]

        substrate = df["Substrat"].to_numpy()

        x_fit = np.linspace(
            0,
            substrate.max() * 1.05,
            300,
        )

        y_fit = (vmax * x_fit) / (km + x_fit)

        ax.scatter(
            df["Substrat"],
            df["Geschwindigkeit"],
            s=45,
            alpha=0.8,
        )

        ax.plot(
            x_fit,
            y_fit,
            linewidth=2,
            label=(
                f"{label} "
                f"(Vmax={vmax:.2f}, Km={km:.2f})"
            ),
        )

    ax.set_title(
        "Vergleich der Michaelis-Menten-Kurven",
        fontsize=15,
    )
    ax.set_xlabel("Substratkonzentration")
    ax.set_ylabel("Reaktionsgeschwindigkeit")

    ax.grid(True, alpha=0.3)

    ax.legend(
        title="Experimente",
        fontsize=9,
    )

    fig.tight_layout()

    st.pyplot(fig)
    image_buffer = BytesIO()

    fig.savefig(
        image_buffer,
        format="png",
        dpi=200,
        bbox_inches="tight",
    )

    image_buffer.seek(0)
    plt.close(fig)
    return image_buffer