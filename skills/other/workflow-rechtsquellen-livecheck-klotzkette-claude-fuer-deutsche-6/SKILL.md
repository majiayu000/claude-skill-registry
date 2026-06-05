---
name: workflow-rechtsquellen-livecheck
description: "Rechtsquellen-Livecheck im Plugin patentrecherche: zwingt vor tragenden Aussagen zum aktuellen Quellencheck bei Gesetzen, Behörden, Gerichten und Formularen."
---

# Rechtsquellen-Livecheck

## Aufgabe
Dieser Workflow-Skill zwingt vor jeder Bewertung in der Patentrecherche zum Live-Check der relevanten Register und der einschlägigen Norm-/Rechtsprechungs-Quellen.

## Pflichtquellen Patentrecherche
- **Patentregister:** `register.dpma.de` (DPMA), `register.epo.org` (EPO), `worldwide.espacenet.com`, `patentscope.wipo.int` (PCT), `patents.google.com`, USPTO Patent Public Search, JPlatPat, CNIPA.
- **Gesetze:** PatG, GebrMG, EPÜ, PCT, UPC-Agreement -- `gesetze-im-internet.de` (DE), `epo.org/law-practice/legal-texts/epc.html` (EPÜ), `wipo.int` (PCT).
- **Klassifikationen:** IPC und CPC unter `worldwide.espacenet.com/patent/cpc-browser` und `wipo.int/classifications/ipc`.
- **Rechtsprechung:** BPatG (`bpatg.de`), BGH-Patentsenat (`bundesgerichtshof.de`), EPA-Beschwerdekammern (`epo.org/law-practice/case-law-appeals.html`), EuGH (`curia.europa.eu` -- C-/T-Nummer mit ECLI), UPC (`unifiedpatentcourt.org`).
- **Non-Patent-Literature (NPL):** Google Scholar, IEEE Xplore, ACM Digital Library, PubMed -- für Validity-Search wichtig (Konferenzbeiträge können neuheitsschädlich sein).

## Anti-Halluzinations-Regeln
- Patentnummern nie ergänzen oder ändern -- jede Nummer im Register live verifizieren.
- "EP 1 234 567 A1" hat A1/A2/A3/B1/B2 Veröffentlichungstyp -- Statuscode prüfen, sonst falsch zitiert.
- Erteilungsstatus, Validierungen pro Land und Rechtsmittelstatus separat prüfen.
- Bei UPC: Opt-out-Status individuell prüfen (Übergangszeit).

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
