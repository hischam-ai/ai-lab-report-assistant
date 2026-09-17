import pandas as pd


def clean_measurement_data(df):
    """Bereinigt die Messdaten und wandelt die Messwerte in Zahlen um."""

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

    return df


def validate_measurement_data(df):
    """Prüft die bereinigten Messdaten auf grundlegende Fehler."""

    if (df["Substrat"] < 0).any():
        return False, "Die Substratkonzentration darf keine negativen Werte enthalten."

    if (df["Geschwindigkeit"] < 0).any():
        return False, "Die Reaktionsgeschwindigkeit darf keine negativen Werte enthalten."

    if len(df) < 4:
        return False, "Es werden mindestens 4 gültige Messpunkte benötigt."

    return True, None