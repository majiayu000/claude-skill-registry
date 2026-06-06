---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin memorandums-ersteller: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe
Dieser Workflow-Skill liest die Memo-Anfrage des Mandanten, die zugrundeliegenden Verträge, Bescheide, Korrespondenzen und Vorgutachten ein und bereitet die Struktur des Memos (Sachverhalt, Frage, Kurzantwort, Bewertung, Risiken, Quellen) vor.

## Dokumentenarten erkennen
- **Mandatsauftrag / Memo-Anfrage:** Was wird gefragt? (Ja/Nein, Risikoanalyse, Strategieoption, Stellungnahme zu Vorgutachten?)
- **Faktenmaterial:** Verträge, AGB, Korrespondenz, Bescheide, Term Sheet, Letter of Intent.
- **Vorgutachten / Stellungnahmen Dritter:** mit Kennzeichnung wessen Sicht; Memo-Verfasser muss eigene Bewertung machen.
- **Begleitende Anlagen:** Bilanzen, Datenraum-Exporte, Behördenakten, Polizei-/Staatsanwaltschaftsakten.

## Erste Triage
- **Adressat:** Mandant (operativ), Geschäftsführung, Aufsichtsrat, externe Investoren, Behörde? Memo-Tonalität und -Tiefe richten sich danach.
- **Rechtsgebiete:** mono-thematisch oder Schnittstellenmemo (z. B. Steuer + Gesellschaftsrecht + Arbeit)?
- **Standardstruktur Memo (vgl. CLAUDE.md):** Sachverhalt, Frage(n), Kurzantwort (1 Satz), rechtliche Bewertung im Gutachtenstil, Gesamtergebnis, Risiken/offene Punkte, Quellenverzeichnis.
- **Vertraulichkeit:** Privileged & confidential? Legal-privilege-Reichweite EU-grenzüberschreitend prüfen.

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
