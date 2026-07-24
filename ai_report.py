from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_report(vmax, km, r2, notes):

    prompt = f"""
Du bist Biochemiker.

Analysiere folgende Michaelis-Menten-Auswertung.

Vmax:
{vmax:.2f}

Km:
{km:.2f}

R²:
{r2:.4f}

Zusätzliche Labornotizen:
{notes}

Schreibe eine wissenschaftliche Interpretation
mit ungefähr 150 Wörtern.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
def ask_ai(question, df, vmax, km, r2, notes):
    prompt = f"""
Du bist ein erfahrener Biochemiker.

Messdaten:

{df.to_string(index=False)}

Vmax: {vmax:.2f}
Km: {km:.2f}
R²: {r2:.4f}

Labornotizen:
{notes}

Frage des Benutzers:
{question}

Beantworte die Frage wissenschaftlich, präzise und leicht verständlich.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content