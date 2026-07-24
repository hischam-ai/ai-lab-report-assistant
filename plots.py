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