import numpy as np
from scipy.optimize import curve_fit


def michaelis_menten(substrat, vmax, km):
    """
    Berechnet die Michaelis-Menten-Gleichung.
    """
    return (vmax * substrat) / (km + substrat)


def fit_michaelis_menten(df):
    """
    Berechnet Km und Vmax aus den Messdaten.
    """
    x = df["Substrat"].values
    y = df["Geschwindigkeit"].values

    parameter, _ = curve_fit(
        michaelis_menten,
        x,
        y,
        p0=[max(y), np.median(x)]
    )

    vmax, km = parameter

    return vmax, km
def calculate_r2(df, vmax, km):
    """
    Berechnet das Bestimmtheitsmaß R².
    """

    x = df["Substrat"].values
    y = df["Geschwindigkeit"].values

    y_fit = michaelis_menten(x, vmax, km)

    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    r2 = 1 - ss_res / ss_tot

    return r2