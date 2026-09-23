# Abbildungsplan Buch

Stand 2026-09-23. Ziel: Abbildungen dort, wo ein Modell, ein Ablauf oder eine Beziehung schneller zu sehen als zu lesen ist. Kein Schmuck, keine doppelte Tabelle.

## Technik

- **Diagramme mit Text** (Modelle, Prozesse, Raster): handgebaute SVG in `figures-src/`, gebaut mit `uv run scripts/build_figures.py` nach `images/`. Geist ist eingebettet, Farben aus der Buchpalette (Papier, Tinte, Ochre, Terracotta, Schiefer). Gründe: gestochen scharfe deutsche Beschriftung, barrierearm (`<title>`/`<desc>` plus `fig-alt`), in Folien und Lernplattform wiederverwendbar, jederzeit textlich korrigierbar.
- **Datengrafiken** (Rechenbeispiele): ebenfalls SVG im selben Stil, nach den Regeln des dataviz-Skills (direkte Beschriftung, keine Legende, wenige Farben).
- **KI-Bilder** (Gemini): nur für Analogien ohne Text. Für Lernabbildungen ungeeignet, weil deutsche Beschriftung und Pfeile unzuverlässig sind. Die Folien haben bereits Hero-Bilder; im Buch vorerst keine.
- Quellen erzeugen: `uv run scripts/generate_figure_sources.py` (Welle 1; das Value Proposition Canvas ist handgeschrieben), danach `uv run scripts/build_figures.py`.
- Folien: `build_figures.py` schreibt zusätzlich nach `slides/images/`; jedes betroffene Deck hat eine eigene Abbildungsfolie mit Aussage-Überschrift und Sprechernotiz.
- Einbindung: `![Bildunterschrift](../images/<name>.svg){#fig-<name> fig-alt="..."}`.

## Welle 1 (Kernmodelle, erstellt am 2026-09-23)

| # | Kapitel | Abbildung | Didaktischer Zweck |
|---|---|---|---|
| 1 | 02 Value Proposition Canvas | Quadrat und Kreis mit Fit-Pfeilen, Reihenfolge 1/2 | **Beispiel, erstellt** |
| 2 | 01 Was Marketing ist | Kundenreise: Fremde → Besucher → Interessenten → Kunden → Fürsprecher, darunter die Aufgaben Anwerben, Überzeugen, Gewinnen, Binden | Stationen als Weg statt als Tabelle |
| 3 | 11 Online-Werbemarkt | Planungsprozess in acht Schritten als Kreislauf mit Rückkopplung vom Controlling | zeigt die Schleifen, die der Text betont |
| 4 | 11 Online-Werbemarkt | Marktakteure: Werbungtreibende, Agentur, DSP, Ad Exchange, SSP, Publisher; Plattformen als geschlossenes System daneben | ordnet die Abkürzungen räumlich |
| 5 | 02 Empathy Map | Vier Felder um die Person (Sehen, Hören, Denken und Fühlen, Sagen und Tun), darunter Pains und Gains als Brücke zum Kundenprofil | Strukturbild des Werkzeugs |
| 6 | 02 Business Model Canvas | Neun Bausteine im Raster, linke Seite (Effizienz) und rechte Seite (Wert) getönt | Aufbau plus Lesart links/rechts |
| 7 | 03 Segmentierung und Targeting | STP als drei Schritte: Markt aufteilen, Segmente wählen, Position bestimmen | Einordnung der drei Kapitel des Moduls |
| 8 | 04 Von Zielen zu Kennzahlen | Kennzahlenbaum am Webinar-Beispiel: Ziel → Ergebnisindikator → Frühindikatoren | Ziel-Kennzahl-Beziehung sichtbar |
| 9 | 07 Funktionsweise und Auktionen | Rechenbeispiel Anzeigenrang: drei Anbietende, Gebot × Qualität, Position und tatsächlicher Klickpreis | „höchstes Gebot gewinnt nicht“ auf einen Blick |
| 10 | 07 Kampagnenstruktur | Konto → Kampagnen → Anzeigengruppen → Keywords und Anzeigen | Hierarchie |
| 11 | 09 Kennzahlen und Kennzahlensysteme | Ein Kostenblock (2.000 €), vier Nenner: CPC, Kosten je Bestellung, Medien-CAC, ROAS (Zahlen aus dem Kapitelbeispiel) | Zähler/Nenner sauber trennen |
| 12 | 09 Attribution und Dashboards | Touchpoint-Kette plus Balken: dieselben 100 Käufe unter Last-Click und gleichmäßiger Verteilung | Zurechnung ist Verteilung, keine Zusatzwirkung |

## Welle 2 (erstellt am 2026-09-23)

| Kapitel | Abbildung |
|---|---|
| 01 Marketing-Mix | Vier P gegenüber vier C |
| 03 Positionierung | Positionierungskarte mit zwei Achsen und fiktiven Wettbewerbern |
| 06 Core Web Vitals | LCP, INP, CLS als drei Momente eines Besuchs, ohne Schwellenwerte (Kapitel verlangt Nachschlagen) |
| 06 Keyword-Recherche | Suchintentionen als vier Felder mit Beispielsuchen |
| 07 Quality Score | Drei Komponenten mit je einem Hebel |
| 08 LinkedIn-Grundlagen | Markenaufbau und Aktivierung im Gleichgewicht |
| 09 GA4-Tracking | Event → Parameter → Schlüsselereignis |
| 10 Prompting-Grundlagen | Vier Bausteine eines Prompts |
| 10 COMPASS-Framework | Sieben Komponenten |
| 10 KI-Werkzeuge und Agenten | Chat (eine Antwort) gegenüber Agent (Schleife aus Planen, Handeln, Prüfen) |
| 11 Recht | Entscheidungsweg Einwilligung beim Tracking |

Vor jeder Abbildung wird das Kapitel vollständig gelesen; Beschriftungen übernehmen die Begriffe des Kapiteltexts.
