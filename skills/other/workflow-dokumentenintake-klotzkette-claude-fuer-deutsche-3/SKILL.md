---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin prozessrecht: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe
Dieser Workflow-Skill liest Klagen, Klageerwiderungen, Repliken, Beschlüsse, Urteile und Anlagenkonvolute in das Plugin `prozessrecht` ein, sortiert sie nach ZPO-Struktur und markiert prozessrechtliche Klippen (Fristen, Zustellungen, Säumnis, Beweismittel).

## Dokumentenarten
- **Klage / Antrag:** Anträge (§ 253 Abs. 2 Nr. 2 ZPO), Klagegrund, Beweisangebote; Streitwert.
- **Klageerwiderung / Replik:** Erklärung nach § 138 ZPO, Bestreiten mit Nichtwissen (§ 138 Abs. 4 ZPO), Beweisangebote.
- **Verfügung Gericht / Hinweis (§ 139 ZPO):** Eingangsbestätigung, Aufklärungshinweise, Auflagen, Frist.
- **Beschluss / Urteil:** Rubrum, Tenor, Tatbestand (§ 313 Abs. 1 Nr. 4 ZPO), Entscheidungsgründe (Nr. 5), Rechtsmittelbelehrung.
- **Sitzungsprotokoll (§ 159 ZPO):** wesentliche Erklärungen, Beweisaufnahme, ggf. § 162 ZPO Vorhalt.

## Erste Triage
- **Fristen:** Klageerwiderungsfrist (§ 277 ZPO), Berufungsfrist (§ 517 ZPO: einen Monat), Berufungsbegründung (§ 520 ZPO: zwei Monate), Revision (§ 548 ZPO).
- **Zuständigkeit:** sachlich (GVG), örtlich (§§ 12-37 ZPO), funktionell (Einzelrichter/Kammer).
- **Beweismaß:** § 286 ZPO (volle Überzeugung) vs. § 287 ZPO (überwiegende Wahrscheinlichkeit bei Schadenshöhe / Kausalität bei Folgeschäden).
- **Beweisangebote zulässig?** Strengbeweis (§§ 355-484 ZPO), Freibeweis nur bei prozessualen Tatsachen.

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
