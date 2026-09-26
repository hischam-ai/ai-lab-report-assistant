# LabMind AI – Lab Report Assistant

LabMind AI ist eine Streamlit-Anwendung zur automatisierten Auswertung von Enzymkinetik-Messdaten nach dem Michaelis-Menten-Modell.

Die App liest Messdaten aus Excel-Dateien ein, berechnet kinetische Parameter, visualisiert die Ergebnisse, bewertet die Datenqualität und erstellt einen strukturierten PDF-Laborbericht.

## Funktionen

- Berechnung von Vmax, Km und R²
- Michaelis-Menten-Kurve mit Messdaten und Fit
- Lineweaver-Burk-Darstellung
- Bewertung der Datenqualität
- Darstellung der Parameterunsicherheit
- Analyse von Wiederholungsmessungen (Replikaten)
- Berechnung von Mittelwert, Standardabweichung und CV
- Validierung und Bereinigung hochgeladener Messdaten
- KI-gestützte Interpretation der Messergebnisse
- Automatische Erstellung eines PDF-Laborberichts

## Messdaten

Die Excel-Datei benötigt die beiden Spalten:

- `Substrat`
- `Geschwindigkeit`

Für eine Auswertung werden mindestens vier gültige Messpunkte und mindestens zwei unterschiedliche Substratkonzentrationen benötigt.

Ungültige oder fehlende Messwerte werden erkannt und beim Einlesen entsprechend behandelt.

Eine passende Excel-Vorlage kann direkt in der App heruntergeladen werden.

## Testdaten

Im Ordner `testdaten/` befindet sich unter anderem eine Testdatei mit Wiederholungsmessungen:

`testdaten/mit_replikaten.xlsx`

Damit können die Michaelis-Menten-Auswertung und die Replikat-Analyse direkt getestet werden.

## PDF-Bericht

Der automatisch erzeugte PDF-Bericht enthält unter anderem:

- kinetische Parameter
- Parameterunsicherheit
- Michaelis-Menten-Kurve
- Lineweaver-Burk-Darstellung
- verwendete Messdaten
- Bewertung der Datenqualität
- zusammenfassendes Fazit

Wenn Wiederholungsmessungen vorhanden sind, enthält der Bericht zusätzlich eine Analyse der Replikat-Präzision mit CV-Werten.

## Projekt starten

Voraussetzungen:

- Python
- `uv`

Abhängigkeiten installieren:

```bash
uv sync