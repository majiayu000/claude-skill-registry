---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin kanzlei-builder-hub: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe
Dieser Workflow-Skill liest Skill-Spezifikationen, Plugin-Manifeste (`plugin.json`), SKILL.md-Vorlagen, Frontmatter-Beispiele und Mandantenanforderungen in den Builder-Hub ein. Er trennt die fachliche Anforderung vom technischen Skill-Gerüst.

## Dokumentenarten
- **Skill-Spezifikation (Fachseite):** beschreibt Anwendungsfall, Eingaben, Ablauf, Output.
- **`plugin.json`** mit `name`, `version`, `description` -- keine Komma-Zahlen.
- **SKILL.md-Vorlage:** Frontmatter mit `name` und `description` (max. 1024 Zeichen); Inhalt strukturiert nach Repo-Konvention (Zweck, Eingaben, Ablauf, Quellen, Output, Beispiele).
- **References:** zitierweise.md, methodik-*.md, ggf. weitere Querverweise unter `references/`.

## Erste Triage
- Ist die fachliche Aufgabenstellung klar oder noch Mandanteninterview erforderlich?
- Welches Plugin? Existiert es schon (Pluralfehler vermeiden) oder ist es neu anzulegen?
- Welcher Skill-Name (ASCII, Kebab-Case, max. 64 Zeichen)?
- Welche Querverweise zu vorhandenen Skills und References werden benötigt?

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
