---
name: workflow-anschluss-skills-router
description: "Anschluss-Skills Router im Plugin patentrecherche: schlägt nach der ersten Prüfung die passenden Spezialskills aus demselben Plugin vor."
---

# Anschluss-Skills Router

## Aufgabe
Dieser Workflow-Skill leitet nach Sichtung in die passenden Patentrecherche-Spezialskills weiter: Suchstrategie, Klassifikationsanalyse, Volltextrecherche, Family-Watch, Wettbewerber-Monitoring, Validity-Suche.

## Routing nach Rechercheart
- **Stand der Technik (Patentability):** Anspruchsmerkmale -> Keywords, IPC/CPC-Klassen, Synonym-Hierarchie; Datenbanken Espacenet, DEPATISnet, Google Patents, Patentscope.
- **Freedom-to-Operate (FTO):** Anspruchssatz fremder Patente -> merkmalsweise Verletzungsmatrix; Schutzregionen klären; Validity-Reserve hinterlegen.
- **Validity-Search (Nichtigkeitsangriff):** harte Suche auf Vorveröffentlichungen vor Prioritätstag des Angriffsziels; Non-Patent-Literature (Konferenzbeiträge, Master-/Doktorarbeiten) explizit prüfen.
- **Family-Watch / Wettbewerber-Monitoring:** Patentfamilien laufend monitoren (INPADOC, Espacenet family); Statusupdates RSS/Alert.
- **Standard / SEP:** ETSI/3GPP/IEEE-Datenbanken; SEP-Datenbanken (DARTS-IP, IPlytics) beachten.

## Anti-Muster
- Nur Englisch suchen, deutsche/asiatische Patente übersehen.
- IPC/CPC ignorieren -- erheblicher Recall-Verlust.
- Stichtag falsch wählen (Anmeldetag vs. Prioritätstag).
- "Erschöpfende" Suche ohne dokumentierte Suchstrategie -- nicht prüfbar.

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
