import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO

from analysis import michaelis_menten


def show_measurement_plot(
    df: pd.DataFrame,
    vmax: float,
    km: float,
) -> BytesIO:
    """Zeigt den Fit an und gibt das Diagramm als PNG zurück."""

    x = df["Substrat"].to_numpy()
    y = df["Geschwindigkeit"].to_numpy()

    x_curve = np.linspace(0, x.max(), 200)
    y_curve = michaelis_menten(x_curve, vmax, km)

    fig, ax = plt.subplots()

    ax.scatter(x, y, label="Messdaten")
    ax.plot(x_curve, y_curve, label="Michaelis-Menten-Fit")

    ax.set_xlabel("Substrat")
    ax.set_ylabel("Geschwindigkeit")
    ax.set_title("Michaelis-Menten-Kurve")
    ax.legend()
    ax.grid(True)

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
import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def show_lineweaver_burk_plot(df):
    filtered_df = df[
        (df["Substrat"] > 0)
        & (df["Geschwindigkeit"] > 0)
    ].copy()

    if len(filtered_df) < 2:
        st.warning(
            "Für den Lineweaver-Burk-Plot werden mindestens "
            "zwei positive Messpunkte benötigt."
        )
        return None

    x = 1 / filtered_df["Substrat"].to_numpy()
    y = 1 / filtered_df["Geschwindigkeit"].to_numpy()

    slope, intercept = np.polyfit(x, y, 1)

    x_fit = np.linspace(x.min(), x.max(), 200)
    y_fit = slope * x_fit + intercept

    fig, ax = plt.subplots()

    ax.scatter(x, y, label="Messdaten")
    ax.plot(x_fit, y_fit, label="Lineweaver-Burk-Fit")

    ax.set_title("Lineweaver-Burk-Plot")
    ax.set_xlabel("1 / Substrat")
    ax.set_ylabel("1 / Geschwindigkeit")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    image_buffer = io.BytesIO()
    fig.savefig(
        image_buffer,
        format="png",
        bbox_inches="tight",
        dpi=150,
    )
    image_buffer.seek(0)

    plt.close(fig)

    return image_buffer
import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def show_lineweaver_burk_plot(df):
    filtered_df = df[
        (df["Substrat"] > 0)
        & (df["Geschwindigkeit"] > 0)
    ].copy()

    if len(filtered_df) < 2:
        st.warning(
            "Für den Lineweaver-Burk-Plot werden mindestens "
            "zwei positive Messpunkte benötigt."
        )
        return None

    x = 1 / filtered_df["Substrat"].to_numpy()
    y = 1 / filtered_df["Geschwindigkeit"].to_numpy()

    slope, intercept = np.polyfit(x, y, 1)

    y_pred = slope * x + intercept

    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    if ss_tot == 0:
        r2_lb = 1.0
    else:
        r2_lb = 1 - (ss_res / ss_tot)

    if intercept <= 0 or slope <= 0:
        st.warning(
            "Aus dem Lineweaver-Burk-Fit konnten keine "
            "physikalisch sinnvollen Parameter berechnet werden."
        )
        vmax_lb = None
        km_lb = None
    else:
        vmax_lb = 1 / intercept
        km_lb = slope / intercept

    x_left = min(x.min(), -intercept / slope) if slope != 0 else x.min()
    x_right = x.max()

    margin = 0.1 * (x_right - x_left)
    x_fit = np.linspace(
        x_left - margin,
        x_right + margin,
        300,
    )
    y_fit = slope * x_fit + intercept

    fig, ax = plt.subplots()

    ax.scatter(x, y, label="Messdaten")
    ax.plot(x_fit, y_fit, label="Lineweaver-Burk-Fit")

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if slope != 0:
        x_intercept = -intercept / slope
        ax.scatter(
            [x_intercept],
            [0],
            marker="x",
            label="x-Achsenabschnitt",
        )

    ax.scatter(
        [0],
        [intercept],
        marker="x",
        label="y-Achsenabschnitt",
    )

    ax.set_title("Lineweaver-Burk-Plot")
    ax.set_xlabel("1 / Substrat")
    ax.set_ylabel("1 / Geschwindigkeit")
    ax.legend()
    ax.grid(True)

    equation_text = (
        f"y = {slope:.4f}x + {intercept:.4f}\n"
        f"R² = {r2_lb:.4f}"
    )

    if vmax_lb is not None and km_lb is not None:
        equation_text += (
            f"\nVmax = {vmax_lb:.2f}"
            f"\nKm = {km_lb:.2f}"
        )

    ax.text(
        0.98,
        0.05,
        equation_text,
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="bottom",
        bbox={
            "boxstyle": "round",
            "alpha": 0.8,
        },
    )

    st.pyplot(fig)

    image_buffer = io.BytesIO()
    fig.savefig(
        image_buffer,
        format="png",
        bbox_inches="tight",
        dpi=150,
    )
    image_buffer.seek(0)

    plt.close(fig)

    return image_buffer


def show_residual_plot(df, vmax, km):
    """
    Zeigt die Residuen des Michaelis-Menten-Fits.
    """

    x = df["Substrat"].to_numpy(dtype=float)
    y = df["Geschwindigkeit"].to_numpy(dtype=float)

    y_fit = michaelis_menten(x, vmax, km)
    residuals = y - y_fit

    fig, ax = plt.subplots()

    ax.scatter(x, residuals, label="Residuen")
    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("Residuenanalyse")
    ax.set_xlabel("Substrat")
    ax.set_ylabel("Residuum")
    ax.grid(True)
    ax.legend()

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