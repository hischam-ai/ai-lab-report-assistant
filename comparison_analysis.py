import pandas as pd


def build_comparison_summary(comparison_df: pd.DataFrame) -> dict:
    """
    Erstellt eine automatische Zusammenfassung mehrerer Experimente.
    """

    best_vmax = comparison_df.loc[
        comparison_df["Vmax"].idxmax()
    ]

    best_km = comparison_df.loc[
        comparison_df["Km"].idxmin()
    ]

    best_r2 = comparison_df.loc[
        comparison_df["R²"].idxmax()
    ]

    return {
        "best_vmax": best_vmax,
        "best_km": best_km,
        "best_r2": best_r2,
    }