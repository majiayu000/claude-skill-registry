---
name: workflow-rechtsquellen-livecheck
description: "Rechtsquellen-Livecheck im Plugin verlagsredaktion: zwingt vor tragenden Aussagen zum aktuellen Quellencheck bei Gesetzen, Behörden, Gerichten und Formularen."
---

# Rechtsquellen-Livecheck

## Aufgabe
Dieser Workflow-Skill erzwingt vor Drucklegung den Live-Check aller Fundstellen: Norm-Stand, Aktenzeichen, Randnummer, Zeitschriften-Seite, Auflage und Erscheinungsjahr.

## Pflichtquellen Verlagsredaktion
- **Normen:** `gesetze-im-internet.de` (Bundesrecht), Landesrecht-Portale; Fassungsstand exakt belegen (Bekanntmachung BGBl., letzte Änderung).
- **Rechtsprechung:** `bundesgerichtshof.de`, `bverfg.de`, `bverwg.de`, `bag.bund.de`, `bsg.bund.de`, `bundesfinanzhof.de`; ECLI-Permalinks für EuGH / EuG (`curia.europa.eu`).
- **Zeitschriften:** Seitenzitate exakt; bei Bedarf Erstseite + zitierte Seite; bei Heftzitierung Heftnummer.
- **Kommentare:** Bearbeiter, Werk, Auflage, Jahr, Norm, Randnummer; bei mehreren Auflagen pro Bearbeiter aktuelle Auflage prüfen.
- **Gesetzgebungsmaterialien:** Bundestags-Drs. (`dipbt.bundestag.de`), Bundesrats-Drs.; Begründung mit Zeilen-/Randnummer.

## Zitierregeln nach `references/zitierweise.md`
- Rspr. vor Lit., neueste zuerst.
- Bei BGH/BVerfG: Gericht, Senat (optional), Entscheidungsform, Datum, Aktenzeichen, Fundstelle, Randnummer.
- Bei EuGH/EuG: Gericht, Datum, Rechtssache, ECLI, Randnummer.
- Keine Komma-Zahlen in `description` (Frontmatter) und in technischen Skill-Metadaten.

## Anti-Halluzinations-Regeln
- Keine Aktenzeichen, Aufsatz- oder Kommentarfundstellen aus Modellwissen. Jede Fundstelle wird in der jeweiligen Datenbank verifiziert.
- Falsche Fußnote wirkt im Publikationsbetrieb wie Lügengeschichte; Vertrauen einmal verloren.

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
