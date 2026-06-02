---
name: workflow-redteam-qualitygate
description: "Red-Team Qualitygate im Plugin common-law-kompass: prüft das Ergebnis auf Halluzinationen, Fristenfehler, Zuständigkeit, Quellen, Beweise und Ton."
---

# Red-Team Qualitygate

## Aufgabe
Dieser Workflow-Skill für `common-law-kompass` Red-Team Qualitygate im Plugin common-law-kompass: prüft das Ergebnis auf Halluzinationen, Fristenfehler, Zuständigkeit, Quellen, Beweise und Ton.. Er ist dazu da, den Nutzer schneller und sicherer in die richtige Bearbeitung zu führen.

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

## Red-Team-Checks für Common-Law-Berührung

- **False Friends:** "Indemnity" ist keine Schadensersatzhaftung deutschen Stils, sondern eine vertragliche Freistellung, oft unabhängig vom Verschulden — Abgrenzung zu § 280 BGB klären.
- **Consideration:** Keine Vertragsbindung ohne consideration im US/UK-Recht (ausgenommen deed/seal-Konstruktionen); deutsche Verträge erfüllen das oft nicht ausdrücklich, aber als implied bargain.
- **Discovery (US Federal: FRCP 26–37):** Erheblich weiter als deutsche Beweiserhebung (§§ 142, 144 ZPO, § 810 BGB); "fishing expedition"-Verbot beachten; § 1782 USC für Hilfe aus US-Gerichten an ausländische Verfahren.
- **Verbot der Präjudizienbindungs-Übertragung:** Deutsche Anwälte dürfen "binding precedent" nicht in deutsche Argumentation überspielen — in Deutschland gibt es keine stare-decisis-Wirkung (Ausnahme § 31 BVerfGG).
- **Keine erfundenen Aktenzeichen:** US-Federal-Cite-Format (z. B. "_F.3d_") nur bei verifizierter Reporter-Fundstelle; Neutral-Citation (z. B. [2023] UKSC 12) auf bailii prüfen.
- **Rechtsdienstleistungsverbot:** Beratung zu US/UK-Recht durch deutsche Anwälte ohne Zulassung dort grds. unzulässig — local counsel hinzuziehen (§ 4 EuRAG, RDG-Restrisiko).

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
