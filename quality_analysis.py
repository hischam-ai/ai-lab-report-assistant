import numpy as np
import pandas as pd


def michaelis_menten_velocity(
    substrate: np.ndarray,
    vmax: float,
    km: float,
) -> np.ndarray:
    """Berechnet die erwartete Geschwindigkeit nach Michaelis-Menten."""

    substrate = np.asarray(substrate, dtype=float)
    return vmax * substrate / (km + substrate)

def detect_replicates(df: pd.DataFrame) -> pd.DataFrame:
    """Erkennt mehrfach gemessene Substratkonzentrationen."""

    if "Substrat" not in df.columns:
        raise ValueError(
            "Der DataFrame muss die Spalte 'Substrat' enthalten."
        )

    replicate_counts = (
        df.groupby("Substrat")
        .size()
        .reset_index(name="Anzahl Messungen")
    )

    return replicate_counts[
        replicate_counts["Anzahl Messungen"] > 1
    ].reset_index(drop=True)
def detect_outliers(
    df: pd.DataFrame,
    vmax: float,
    km: float,
    relative_threshold: float = 0.25,
) -> pd.DataFrame:
    """
    Erkennt auffällige Messpunkte anhand ihrer Abweichung vom Modell.

    Ein Messpunkt gilt als auffällig, wenn seine relative Abweichung
    mindestens dem angegebenen Schwellenwert entspricht.
    """

    required_columns = {"Substrat", "Geschwindigkeit"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Der DataFrame muss die Spalten "
            "'Substrat' und 'Geschwindigkeit' enthalten."
        )

    if relative_threshold <= 0:
        raise ValueError("Der Schwellenwert muss größer als 0 sein.")

    result = df[["Substrat", "Geschwindigkeit"]].copy()

    result["Erwartete Geschwindigkeit"] = michaelis_menten_velocity(
        result["Substrat"].to_numpy(),
        vmax,
        km,
    )

    result["Absolute Abweichung"] = (
        result["Geschwindigkeit"]
        - result["Erwartete Geschwindigkeit"]
    ).abs()

    denominator = result["Erwartete Geschwindigkeit"].abs().replace(0, np.nan)

    result["Relative Abweichung"] = (
        result["Absolute Abweichung"] / denominator
    )

    result["Abweichung (%)"] = result["Relative Abweichung"] * 100

    result["Ausreißer"] = (
        result["Relative Abweichung"] >= relative_threshold
    )

    result.insert(0, "Messpunkt", range(1, len(result) + 1))

    return result


def summarize_outliers(outlier_df: pd.DataFrame) -> list[str]:
    """Erstellt kurze, verständliche Hinweise zu auffälligen Messpunkten."""

    if "Ausreißer" not in outlier_df.columns:
        raise ValueError(
            "Die Tabelle muss zuvor mit detect_outliers() erzeugt werden."
        )

    flagged = outlier_df[outlier_df["Ausreißer"]]

    if flagged.empty:
        return [
            "Keine auffälligen Messpunkte anhand des aktuellen "
            "Abweichungsschwellenwerts erkannt."
        ]

    comments = []

    for _, row in flagged.iterrows():
        comments.append(
            "Messpunkt "
            f"{int(row['Messpunkt'])} bei Substrat = "
            f"{row['Substrat']:.4g} weicht um "
            f"{row['Abweichung (%)']:.1f} % vom Modell ab."
        )

    return comments



def suggest_measurement_points(
    df: pd.DataFrame,
    km: float,
) -> list[float]:
    """
    Schlägt zusätzliche Substratkonzentrationen vor.

    Die Vorschläge konzentrieren sich auf:
    - den Bereich unterhalb von Km,
    - den Bereich direkt um Km,
    - den Sättigungsbereich oberhalb von Km.
    """

    if km <= 0:
        raise ValueError("Km muss größer als 0 sein.")

    if "Substrat" not in df.columns:
        raise ValueError(
            "Der DataFrame muss die Spalte 'Substrat' enthalten."
        )

    existing_values = pd.to_numeric(
        df["Substrat"],
        errors="coerce",
    ).dropna().to_numpy(dtype=float)

    if len(existing_values) == 0:
        raise ValueError("Es wurden keine gültigen Substratwerte gefunden.")

    candidates = np.array(
        [
            0.25 * km,
            0.5 * km,
            0.75 * km,
            1.0 * km,
            1.5 * km,
            2.0 * km,
            4.0 * km,
        ],
        dtype=float,
    )

    suggestions = []

    for candidate in candidates:
        distance = np.abs(existing_values - candidate)

        tolerance = max(0.12 * candidate, 1e-9)

        if not np.any(distance <= tolerance):
            suggestions.append(float(candidate))

    suggestions = sorted(set(round(value, 4) for value in suggestions))

    return suggestions[:5]


def summarize_measurement_recommendations(
    df: pd.DataFrame,
    km: float,
) -> list[str]:
    """Erstellt verständliche Empfehlungen für zusätzliche Messpunkte."""

    suggestions = suggest_measurement_points(df, km)

    if not suggestions:
        return [
            "Der relevante Substratbereich um Km ist bereits gut abgedeckt."
        ]

    formatted_values = ", ".join(f"{value:.4g}" for value in suggestions)

    comments = [
        "Zusätzliche Messungen werden bei folgenden "
        f"Substratkonzentrationen empfohlen: {formatted_values}.",
    ]

    existing_values = pd.to_numeric(
        df["Substrat"],
        errors="coerce",
    ).dropna()

    below_km = int((existing_values < 0.5 * km).sum())
    around_km = int(
        (
            (existing_values >= 0.5 * km)
            & (existing_values <= 1.5 * km)
        ).sum()
    )
    above_km = int((existing_values > 2.0 * km).sum())

    if below_km < 2:
        comments.append(
            "Im niedrigen Substratbereich fehlen Messpunkte. "
            "Diese helfen bei der Bestimmung des Kurvenanstiegs."
        )

    if around_km < 3:
        comments.append(
            "Im Bereich um Km sollten mehrere Messpunkte liegen, "
            "da dieser Bereich besonders wichtig für die Km-Schätzung ist."
        )

    if above_km < 2:
        comments.append(
            "Im Sättigungsbereich oberhalb von 2 × Km fehlen Messpunkte. "
            "Diese verbessern die Schätzung von Vmax."
        )

    return comments
def analyze_replicate_precision(df: pd.DataFrame) -> pd.DataFrame:
    """Berechnet die Präzision mehrfach gemessener Substratkonzentrationen."""

    replicates = (
        df.groupby("Substrat")["Geschwindigkeit"]
        .agg(["count", "mean", "std"])
        .reset_index()
    )

    replicates = replicates[replicates["count"] > 1].copy()

    replicates["CV (%)"] = (
        replicates["std"] / replicates["mean"].abs() * 100
    )

    replicates = replicates.rename(
        columns={
            "count": "Anzahl Messungen",
            "mean": "Mittelwert",
            "std": "Standardabweichung",
        }
    )

    return replicates
def summarize_replicate_precision(
    replicate_df: pd.DataFrame,
) -> list[str]:
    """Erstellt eine verständliche Bewertung der Replikat-Präzision."""

    comments = []

    if replicate_df.empty:
        return ["Keine Replikate für eine Präzisionsbewertung vorhanden."]

    for _, row in replicate_df.iterrows():
        substrate = row["Substrat"]
        cv = row["CV (%)"]

        if cv < 5:
            assessment = "sehr geringe Streuung"
        elif cv < 10:
            assessment = "geringe Streuung"
        elif cv < 20:
            assessment = "erhöhte Streuung"
        else:
            assessment = "hohe Streuung"

        comments.append(
            f"Substrat {substrate:g}: CV = {cv:.1f} % – {assessment}."
        )

    return comments