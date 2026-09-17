from __future__ import annotations

import pandas as pd


def build_scientific_assessment(
    df: pd.DataFrame,
    vmax: float,
    km: float,
    r2: float,
    quality_score: int | float,
    quality_comments: list[str],
    outlier_comments: list[str],
    measurement_recommendations: list[str],
    replicate_precision_df: pd.DataFrame,
) -> dict[str, object]:
    """Erstellt eine strukturierte wissenschaftliche Bewertung."""

    strengths = []
    weaknesses = []
    recommendations = []

    if r2 >= 0.98:
        strengths.append(
            f"Sehr gute Anpassung an das Michaelis-Menten-Modell "
            f"(R² = {r2:.4f})."
        )
    elif r2 >= 0.95:
        strengths.append(
            f"Gute Anpassung an das Michaelis-Menten-Modell "
            f"(R² = {r2:.4f})."
        )
    else:
        weaknesses.append(
            f"Die Modellanpassung ist eingeschränkt "
            f"(R² = {r2:.4f})."
        )

    if len(df) >= 8:
        strengths.append(
            f"Der Datensatz enthält {len(df)} gültige Messpunkte."
        )
    elif len(df) >= 6:
        strengths.append(
            f"Der Datensatz enthält eine ausreichende Anzahl "
            f"von {len(df)} Messpunkten."
        )
    else:
        weaknesses.append(
            f"Der Datensatz enthält nur {len(df)} gültige Messpunkte."
        )

    if quality_score >= 8:
        confidence = "hoch"
    elif quality_score >= 5:
        confidence = "mittel"
    else:
        confidence = "niedrig"

    for comment in quality_comments:
        normalized = comment.lower()

        if (
            "zu wenige" in normalized
            or "schwach" in normalized
            or "nicht" in normalized
        ):
            weaknesses.append(comment)
        else:
            strengths.append(comment)

    meaningful_outliers = [
        comment
        for comment in outlier_comments
        if "keine auffälligen" not in comment.lower()
    ]

    if meaningful_outliers:
        weaknesses.extend(meaningful_outliers)
        recommendations.append(
            "Auffällige Messpunkte sollten als technische oder "
            "biologische Replikate erneut gemessen werden."
        )
    else:
        strengths.append(
            "Es wurden keine auffälligen Messpunkte anhand des "
            "aktuellen Schwellenwerts erkannt."
        )

    recommendations.extend(measurement_recommendations)
    if not replicate_precision_df.empty:
        high_cv_replicates = replicate_precision_df[
        replicate_precision_df["CV (%)"] >= 10
    ]

    if not high_cv_replicates.empty:
        weaknesses.append(
            "Einige Replikatmessungen zeigen eine erhöhte Streuung "
            "(CV ≥ 10 %)."
        )

        recommendations.append(
            "Replikate mit erhöhter Streuung sollten überprüft "
            "oder erneut gemessen werden."
        )
    else:
        strengths.append(
            "Die Replikatmessungen zeigen eine gute Übereinstimmung."
        )

    summary = (
        f"Die Daten ergeben Vmax = {vmax:.2f}, Km = {km:.2f} "
        f"und R² = {r2:.4f}. Das Vertrauen in die aktuelle "
        f"Parameterschätzung ist {confidence}."
    )

    return {
        "summary": summary,
        "strengths": _remove_duplicates(strengths),
        "weaknesses": _remove_duplicates(weaknesses),
        "recommendations": _remove_duplicates(recommendations),
        "confidence": confidence,
    }


def _remove_duplicates(items: list[str]) -> list[str]:
    """Entfernt doppelte Texte und behält die Reihenfolge bei."""

    seen = set()
    unique_items = []

    for item in items:
        clean_item = str(item).strip()

        if clean_item and clean_item not in seen:
            seen.add(clean_item)
            unique_items.append(clean_item)

    return unique_items     