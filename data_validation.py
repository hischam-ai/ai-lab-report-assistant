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

    if df.empty:
        return False, "Die Excel-Datei enthält keine gültigen Messwerte."

    if (df["Substrat"] < 0).any():
        return False, "Die Substratkonzentration darf keine negativen Werte enthalten."

    if (df["Geschwindigkeit"] < 0).any():
        return False, "Die Reaktionsgeschwindigkeit darf keine negativen Werte enthalten."
    if (df["Geschwindigkeit"] == 0).all():
        return False, (
        "Alle Reaktionsgeschwindigkeiten sind 0. "
        "Eine Michaelis-Menten-Auswertung ist damit nicht möglich."
    )
    if len(df) < 4:
        return False, "Es werden mindestens 4 gültige Messpunkte benötigt."
    if df["Substrat"].nunique() < 2:
        return False, (
            "Es werden mindestens 2 unterschiedliche "
            "Substratkonzentrationen benötigt."
        )
    return True, None