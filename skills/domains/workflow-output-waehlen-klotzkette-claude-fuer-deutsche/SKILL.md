---
name: workflow-output-waehlen
description: "Output wählen im Plugin patentrecherche: entscheidet zwischen Memo, Schriftsatz, Tabelle, Brief, Checkliste, Vermerk, Redline oder Mandantenübersetzung."
---

# Output wählen

## Aufgabe
Dieser Workflow-Skill bestimmt das Output-Format der Patentrecherche: Stand-der-Technik-Report, FTO-Memo, Validity-Search-Report, Suchprotokoll, Claim Chart, Wettbewerber-Monitor.

## Output-Typen
- **Suchprotokoll:** Datenbank, Datum, Suchstring, Filter (IPC/CPC, Anmelder, Datumsbereich), Trefferzahl, ausgewählte Treffer, Begründung der Auswahl/Aussonderung.
- **Stand-der-Technik-Report:** Anmeldungsthema, Suchstrategie, geprüfte Datenbanken, gefundene D1/D2/...-Dokumente mit Volltextzitaten und Übersetzungen.
- **FTO-Memo:** Produkt -> Anspruchsmerkmale fremder Patente; merkmalsweise Verletzungs-Matrix (Erfüllt / Nicht erfüllt / Unklar) je Schutzrecht.
- **Validity-Search-Report:** harte Suche auf Vorveröffentlichungen vor Prio-Tag; je gefundene Stelle: Quelle, Datum, technisches Merkmal, Vergleich zur Anspruchsfassung.
- **Claim Chart (Patent vs. Stand der Technik / vs. Angriffsziel):** Spalten Anspruchsmerkmal, Fundstelle, wörtliche Stelle, Bewertung, Anmerkung.
- **Family Watch:** Patentfamilien-Liste mit Status, nächster Frist, Ländern, Anmeldern.

## Methodik
- Suchstrategie immer in Volltext speichern (für Reproduzierbarkeit); idealerweise Boolean-Strings mit IPC/CPC-Klassen.
- Bei NPL (Non-Patent-Literature): Konferenzbeitrag, Master-/Doktorarbeit, Whitepaper, GitHub-Commits als mögliche Vorveröffentlichung dokumentieren.

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
