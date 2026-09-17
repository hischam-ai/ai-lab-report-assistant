from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_lab_advice(
    df,
    vmax,
    km,
    r2,
    notes,
    outlier_comments=None,
    measurement_recommendations=None,
):

    prompt = f"""
Du bist ein erfahrener Biochemiker und Laborleiter.

Analysiere folgende Enzymkinetik.

Messdaten:
{df.to_string(index=False)}

Vmax: {vmax:.2f}
Km: {km:.2f}
R²: {r2:.4f}

Labornotizen:
{notes}

Auffällige Messpunkte:
{chr(10).join(outlier_comments) if outlier_comments else "Keine"}

Empfohlene zusätzliche Messpunkte:
{chr(10).join(measurement_recommendations) if measurement_recommendations else "Keine"}

Gib ausschließlich praktische Empfehlungen.

Gib ausschließlich praktische Empfehlungen.

Zum Beispiel:

- Welche Messungen fehlen?
- Sollte man weitere Messpunkte aufnehmen?
- Gibt es Hinweise auf Ausreißer?
- Sind weitere Replikate sinnvoll?
- Sind Einheiten oder Enzymkonzentration notwendig?
- Wie könnte man den Versuch verbessern?

Schreibe maximal 6 Stichpunkte.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response.choices[0].message.content
def evaluate_data_quality(df, vmax, km, r2, replicate_precision_df=None):
    score = 10
    comments = []

    # R² bewerten
    if r2 < 0.95:
        score -= 3
        comments.append("Schwache Modellanpassung.")
    elif r2 < 0.98:
        score -= 1
        comments.append("Gute Modellanpassung.")
    else:
        comments.append("Sehr gute Modellanpassung.")

    # Anzahl Messpunkte
    if len(df) < 6:
        score -= 2
        comments.append("Zu wenige Messpunkte.")
    else:
        comments.append("Ausreichende Anzahl an Messpunkten.")

    # Bereich um Km prüfen
    around_km = df[
        (df["Substrat"] > km * 0.5) &
        (df["Substrat"] < km * 1.5)
    ]

    if len(around_km) < 2:
        score -= 2
        comments.append("Zu wenige Messpunkte im Bereich um Km.")
    else:
        comments.append("Km-Bereich gut abgedeckt.")
            # Präzision der Replikate bewerten
    if replicate_precision_df is not None and not replicate_precision_df.empty:
        high_cv = replicate_precision_df["CV (%)"] >= 10

        if high_cv.any():
            score -= 1
            comments.append(
                "Erhöhte Streuung bei einzelnen Replikaten."
            )
        else:
            comments.append(
                "Gute Übereinstimmung der Replikate."
            )

    score = max(score, 0)

    return score, comments