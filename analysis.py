import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import t


def michaelis_menten(substrat, vmax, km):
    """Berechnet die Michaelis-Menten-Gleichung."""

    substrat = np.asarray(substrat, dtype=float)
    return (vmax * substrat) / (km + substrat)


def fit_michaelis_menten(df):
    """Berechnet Vmax und Km aus den Messdaten."""

    x = df["Substrat"].to_numpy(dtype=float)
    y = df["Geschwindigkeit"].to_numpy(dtype=float)

    parameter, _ = curve_fit(
        michaelis_menten,
        x,
        y,
        p0=[max(y), np.median(x)],
        bounds=(0, np.inf),
        maxfev=10000,
    )

    vmax, km = parameter
    return float(vmax), float(km)


def calculate_r2(df, vmax, km):
    """Berechnet das Bestimmtheitsmaß R²."""

    x = df["Substrat"].to_numpy(dtype=float)
    y = df["Geschwindigkeit"].to_numpy(dtype=float)

    y_fit = michaelis_menten(x, vmax, km)

    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    if ss_tot == 0:
        return 0.0

    r2 = 1 - ss_res / ss_tot
    return float(r2)


def calculate_parameter_statistics(
    df,
    confidence_level=0.95,
):
    """
    Berechnet Parameter, Standardfehler, RMSE und Konfidenzintervalle.

    Die Funktion führt den Michaelis-Menten-Fit erneut aus, damit die
    Kovarianzmatrix von scipy.optimize.curve_fit verwendet werden kann.
    """

    if not 0 < confidence_level < 1:
        raise ValueError(
            "Das Konfidenzniveau muss zwischen 0 und 1 liegen."
        )

    x = df["Substrat"].to_numpy(dtype=float)
    y = df["Geschwindigkeit"].to_numpy(dtype=float)

    if len(x) < 4:
        raise ValueError(
            "Für die Statistik werden mindestens 4 Messpunkte benötigt."
        )

    parameter, covariance = curve_fit(
        michaelis_menten,
        x,
        y,
        p0=[max(y), np.median(x)],
        bounds=(0, np.inf),
        maxfev=10000,
    )

    vmax, km = parameter
    y_fit = michaelis_menten(x, vmax, km)
    residuals = y - y_fit

    degrees_of_freedom = len(y) - len(parameter)

    if degrees_of_freedom <= 0:
        raise ValueError(
            "Zu wenige Freiheitsgrade für eine Unsicherheitsanalyse."
        )

    rmse = np.sqrt(
        np.sum(residuals ** 2) / degrees_of_freedom
    )

    variances = np.diag(covariance)

    if np.any(variances < 0) or not np.all(np.isfinite(variances)):
        raise ValueError(
            "Die Parameterunsicherheit konnte nicht stabil berechnet werden."
        )

    standard_errors = np.sqrt(variances)
    vmax_standard_error, km_standard_error = standard_errors

    alpha = 1 - confidence_level
    t_critical = t.ppf(
        1 - alpha / 2,
        degrees_of_freedom,
    )

    vmax_margin = t_critical * vmax_standard_error
    km_margin = t_critical * km_standard_error

    return {
        "vmax": float(vmax),
        "km": float(km),
        "rmse": float(rmse),
        "degrees_of_freedom": int(degrees_of_freedom),
        "confidence_level": float(confidence_level),
        "vmax_standard_error": float(vmax_standard_error),
        "km_standard_error": float(km_standard_error),
        "vmax_confidence_interval": (
            float(vmax - vmax_margin),
            float(vmax + vmax_margin),
        ),
        "km_confidence_interval": (
            float(km - km_margin),
            float(km + km_margin),
        ),
        "residuals": residuals.tolist(),
        "predicted_values": y_fit.tolist(),
    }