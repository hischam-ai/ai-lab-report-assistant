# LabMind AI – Lab Report Assistant

Eine Streamlit-App zur Auswertung von Enzymkinetik-Messdaten nach Michaelis-Menten.

Die App liest Excel-Messdaten ein, berechnet kinetische Parameter, visualisiert die Ergebnisse und erstellt einen PDF-Laborbericht.

## Projekt starten

Voraussetzung: Python und `uv` sind installiert.

```bash
uv sync
uv run streamlit run main.py
```

## Messdaten

Die Excel-Datei benötigt zwei Spalten:

- `Substrat`
- `Geschwindigkeit`

In der App kann eine passende Excel-Vorlage heruntergeladen werden.

## Testdaten

Im Ordner `testdaten/` liegt eine Excel-Datei mit Wiederholungsmessungen:

`testdaten/mit_replikaten.xlsx`

## Funktionen

- Michaelis-Menten-Auswertung mit Berechnung von Vmax, Km und R²
- Michaelis-Menten-Kurve und Lineweaver-Burk-Darstellung
- Bewertung der Datenqualität
- Analyse von Wiederholungsmessungen (Replikaten) mit CV-Werten
- Darstellung der Parameterunsicherheit
- KI-gestützte Interpretation der Messergebnisse
- Erstellung eines PDF-Laborberichts

## PDF-Bericht

Der PDF-Bericht enthält die kinetischen Parameter, Diagramme,
Messdaten, Qualitätsbewertung und ein zusammenfassendes Fazit.

Wenn Wiederholungsmessungen vorhanden sind, wird zusätzlich
die Präzision der Replikate dargestellt.