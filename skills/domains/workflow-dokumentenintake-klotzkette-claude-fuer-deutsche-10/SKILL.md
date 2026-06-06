---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin rechtsberatungsstelle: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe
Dieser Workflow-Skill liest typische Unterlagen von Rechtsuchenden in einer niedrigschwelligen Rechtsberatungsstelle ein: Bescheide (Jobcenter, Sozialamt, Ausländerbehörde, BAföG, Wohngeld), Mietvertrag, Lohnabrechnung, Mahnbescheide, Vollstreckungsbescheide, Bußgeldbescheide.

## Dokumentenarten
- **Verwaltungsbescheid:** Adressat, Datum, Rechtsbehelfsbelehrung; Widerspruchsfrist 1 Monat (§ 70 VwGO / § 84 SGG).
- **Mahnbescheid (§ 692 ZPO):** Widerspruch 2 Wochen ab Zustellung (§ 694 ZPO); Vollstreckungsbescheid: Einspruch 2 Wochen (§ 700 ZPO).
- **Bußgeldbescheid:** Einspruch 2 Wochen ab Zustellung (§ 67 OWiG).
- **Kündigung (Miete, Arbeit):** Klagefrist Kündigungsschutzklage 3 Wochen ab Zugang (§ 4 KSchG); Mietrecht: Räumungsfrist je nach Lage.
- **Lohnabrechnung / Sozialversicherung:** Indizien für Verdienstausfall, BAföG, Wohngeld, Bürgergeld.
- **Mahnschreiben / Inkasso:** Verzug, Inkassokostenklauseln (§ 13a RDG), Ratenzahlung.

## Erste Triage
- **Beratungsberechtigung:** Beratungshilfeschein des Amtsgerichts (BerHG) oder Prozesskostenhilfe (§§ 114 ff. ZPO)?
- **Fristen:** Welche harte Frist läuft? Sofortige Eintragung in Fristenkalender.
- **Rolle der Beratungsstelle:** allgemeine Information vs. Vertretung (RDG-Grenzen für Nicht-Anwälte beachten).
- **Sprachbarrieren / Behinderung:** ggf. Dolmetscher, Leichte Sprache, Begleitperson.
- **Vertraulichkeit:** datensparsame Aufnahme; AVV bei genutzter Software.

## Kaltstart
Wenn Material vorliegt, arbeite zuerst mit dem Material. Stelle nur Rückfragen, die für die nächste Weiche nötig sind:

1. Wer fragt in welcher Rolle?
2. Was ist das gewünschte Ergebnis?
3. Gibt es Fristen, Termine, Zustellungen, Zahlungen oder Sanktionen?
4. Welche Unterlagen, Daten oder Belege liegen bereits vor?

## Arbeitsworkflow
1. Rolle, Ziel, Frist und Unterlagenlage in höchstens fünf Fragen klären.
2. Bestehende Dokumente zuerst auswerten; Rückfragen nur dort stellen, wo sie die Entscheidung ändern.
3. Passende Spezialskills aus diesem Plugin vorschlagen und begründen.
4. Ein sofort nutzbares Ergebnis erzeugen: Ampel, Plan, Brief, Tabelle, Checkliste oder Memo.

## Output-Standard
- Kurzbild: worum es geht, was gesichert ist, was offen ist.
- Prüf- oder Bearbeitungsmatrix mit den entscheidenden Punkten.
- Konkreter nächster Schritt mit Frist, Zuständigkeit und Unterlagen.
- Bei Außenkommunikation: knapper, sachlicher Textbaustein ohne unnötige Nebenangaben.

## Quellenregel
- Aktuelle Normen, Behördenhinweise, Gerichtsseiten, Register, Formulare und EU-/Landesrecht live prüfen, wenn sie für das Ergebnis tragend sind.
- Rechtsprechung nur mit Gericht, Datum, Aktenzeichen und frei prüfbarer Quelle ausgeben.
- Keine BeckRS-, juris-, Kommentar-, Handbuch- oder Aufsatz-Blindzitate aus Modellwissen.
- Unsicherheiten und Annahmen ausdrücklich markieren.
