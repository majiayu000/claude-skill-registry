---
name: kaltstart-triage
description: "Einstieg, Kaltstart und Fallrouting im Beamtenrecht-Plugin: klärt Status, Dienstherr, Bundesland, Frist, Ziel, Unterlagen, Anfänger-/Profi-Modus und schlägt passende Fachmodule vor."
---

# Allgemein

## Aktenstart statt Formularstart

Wenn zu **Kaltstart Triage** bereits Unterlagen, ein Ordner, ein ZIP, ein PDF-Buendel, E-Mails, Screenshots, Tabellen oder Entwuerfe vorliegen, lies diese zuerst aus. Bilde fuer **Beamtenrecht** eine Arbeitshypothese zu Beteiligten, Rolle des Nutzers, Verfahrensstand, Fristen, Betrags-/Datumslogik, Belegen und naechstem sinnvollen Output. Frage nicht routinemaessig nach Angaben, die sich aus der Akte ergeben.

Starte dann mit einer knappen Rueckmeldung:

```text
Ich habe aus der Akte vorlaeufig erkannt: [...]
Unsicher sind noch: [...]
Als naechsten Schritt schlage ich vor: [...]
```

Stelle danach hoechstens drei Rueckfragen und nur zu echten Luecken oder Widerspruechen. Wenn keine Akte vorliegt, bitte zuerst um Upload der wichtigsten Unterlagen statt ein langes Interview zu beginnen.

## Pflichtfragen

- Welcher Status liegt vor: Beamter, Richter, Bewerber, Anwärter, Tarifbeschäftigter, Wahlbeamter oder Mischfall?
- Welcher Dienstherr und welches Bundesland sind betroffen?
- Gibt es einen Bescheid, eine Beurteilung, eine Ausschreibung, einen Auswahlvermerk oder eine Verfügung mit Datum und Zugang?
- Welche Frist läuft und welches Ergebnis soll erreicht werden?
- Welche Unterlagen fehlen noch: Personalakte, Beurteilungsbeiträge, amtsärztliches Gutachten, Berechnungsblatt, Beteiligungsvermerk, Versorgungsauskunft, Beihilfebescheid, PKV-Schreiben, Auswahlvermerk?

## Prüfprogramm

1. **Status und Rechtsquelle:** Bundesrecht, Landesrecht oder Richterrecht trennen; Normen live gegen amtliche Quellen prüfen.
2. **Eingriff und Ziel:** Verwaltungsakt, dienstliche Weisung, Auswahlentscheidung, Realakt oder bloße Kommunikation einordnen.
3. **Materielle Prüfung:** Tatbestand, Ermessen, Beteiligung, Begründung, Gleichbehandlung, Fürsorge und Verhältnismäßigkeit prüfen.
4. **Verfahren:** Anhörung, Akteneinsicht, Frist, Widerspruch, Klageart, Eilrechtsschutz und Glaubhaftmachung klären.
5. **Pension/Beihilfe-Sonderroute:** Bei Ruhestand, Krankheit, Pflege, Heilfürsorge oder gesetzlicher Rente sofort in die Versorgungsskills routen; bei Bewerbungs- oder Beförderungsstreit die Konkurrentenschutzskills mit Eilrechtsschutz vorschalten.
6. **Output:** Eine klare Handlungsempfehlung, einen Entwurf oder eine Risikomatrix erzeugen.

## Erweiterte Spezialrouten

- **Pension und Versorgung:** `pensionierung-gesamtcheck-ruhegehalt-beihilfe-pkv`, `versorgungsakte-dokumentenintake-und-berechnung`, `pension-und-gesetzliche-rente-55-beamtvg`.
- **Krankheitskosten:** `krankheitskosten-beihilfe-pkv-widerspruch`, `pflege-beihilfe-pflegeversicherung-beamte`, `heilfürsorge-ruhestand-pkv-anwartschaft`.
- **Konkurrentenschutz:** `konkurrentenschutz-sofortprogramm-einzelgerechtigkeit`, `konkurrentenschutz-auswahlvermerk-und-akteneinsicht`, `konkurrentenschutz-nach-ernennung-schadensersatz`.
