---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin liquiditaetsplanung: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe
Dieser Workflow-Skill für `liquiditaetsplanung` Dokumentenintake im Plugin liquiditaetsplanung: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte.. Er ist dazu da, den Nutzer schneller und sicherer in die richtige Bearbeitung zu führen.

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

## Dokumenten-Intake Liquiditätsplanung
- **Cash-In-Daten:**
  - **OPOS Debitoren** mit Fälligkeitsstruktur (Aging-Report) — Basis für Cash-In direkte Methode.
  - Auftragsbestand, Umsatzprognose, Kundenbestätigungen, Anzahlungen.
  - Erstattungen Finanzamt (Vorsteuer, Lohnsteuer), Versicherungsleistungen.
- **Cash-Out-Daten:**
  - **OPOS Kreditoren** mit Fälligkeit — Basis für Cash-Out direkte Methode.
  - Lohnabrechnung mit Auszahlungsterminen, Lohnsteuer- und SV-Abgaben (§ 266a StGB!).
  - Steuerverbindlichkeiten Finanzamt mit Fälligkeiten (USt-Voranmeldung, KSt-Vorauszahlung).
  - Miet- und Pachtverpflichtungen (§ 535 BGB), Dauerlieferverträge.
  - Tilgung und Zinsen für Kreditverbindlichkeiten, Leasingraten.
- **Liquiditätsreserven:**
  - Bank- und Kassenbestände, Tagesgeld, Festgeld.
  - Offene Kreditlinien (Kontokorrent), Factoring-Linien.
  - Stille Reserven, freie Vermögensgegenstände, die kurzfristig veräußerbar sind.
- **Kovenanten-Tracking:**
  - Bankvertrag mit Kovenanten (Working Capital, EBITDA, Debt-Service-Coverage, Equity Ratio).
  - Quartalsweise Compliance-Bestätigung an Bank.
- **Sanierungsmaßnahmen mit Liquiditätswirkung:**
  - Stundungsvereinbarungen, Forderungsverzichte (mit Besserungsschein), Gesellschafterdarlehen, Patronate.
  - Rangrücktrittsvereinbarungen § 39 Abs. 2 InsO.

## Plausibilitätsprüfung beim Intake
- Saldenkonsistenz: Anfangsbestand + Cash-In − Cash-Out = Endbestand.
- Sensitivität: Best-/Base-/Worst-Case explizit ausgewiesen?
- Annahmen-Dokumentation: woher kommen Umsatzprognose und Kostenstruktur?
- Vergleich mit Vergangenheit (BWA, letzte 12 Monate) — Plausibilitätscheck Working Capital.
