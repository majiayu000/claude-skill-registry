---
name: workflow-dokumentenintake
description: "Dokumentenintake im Plugin subsumtions-pruefer: liest Uploads, sortiert Dokumentarten, markiert Fristen und baut eine knappe Arbeitsakte."
---

# Dokumentenintake

## Aufgabe

Dieser Workflow-Skill liest Sachverhalte, Gutachten, Schriftsätze, Urteile und Vermerke ein und sortiert sie nach Subsumtions-Bausteinen: Obersatz (Norm), Definition des Tatbestandsmerkmals, Subsumtion (konkrete Tatsachen unter Definition), Schlussfolgerung. Ergebnis ist eine knappe Arbeitsakte, die direkt für die weitere Prüfung genutzt werden kann.

## Dokumentenarten und Intake-Logik

### Sachverhalt
- **Auftrag:** Tatsachenmaterial mit Subsumtionsbedarf.
- **Intake-Schritte:** Wer, Was, Wann, Wo, Beweise. Relevante Tatsachen markieren; irrelevante ausblenden.
- **Prüffrage:** Sind alle Tatsachen zeitlich geordnet? Gibt es Widersprüche?

### Vorgutachten / Memo
- **Auftrag:** Ist die Subsumtion sauber? Ist die Definition mit Quelle belegt?
- **Intake-Schritte:** Obersatz identifizieren; Definition prüfen (Quelle vorhanden?); Subsumtion vs. Wiederholung abgrenzen.
- **Anti-Muster:** Definition wiederholen statt subsumieren; Tatsachen umformulieren statt unter Definition zu prüfen.

### Klausurlösung / Kandidatenlösung
- **Auftrag:** Subsumtion vs. bloße Wiederholung der Definition prüfen.
- **Intake-Schritte:** Vier-Schritt-Schema anwenden; Fehlerklassen identifizieren (Sprung-Subsumtion, Zirkelschluss, fehlende Definition).
- **Prüffrage:** Wo fehlt das Zwischenergebnis? Wo steht Konjunktiv im Schluss?

### Urteil / Beschluss
- **Auftrag:** Tatbestand (§ 313 ZPO) liefert Tatsachen; Entscheidungsgründe liefern juristische Würdigung mit Subsumtion.
- **Intake-Schritte:** Tatbestand → Tatsachenextraktion; Entscheidungsgründe → Normprüfung und Subsumtion.
- **Prüffrage:** Welche TBM sind streitig geblieben? Welche Einreden wurden behandelt?

### Bescheid / Verwaltungsakt
- **Auftrag:** Ermächtigungsgrundlage, Tatbestand, Rechtsfolge, Nebenbestimmungen.
- **Intake-Schritte:** Ermächtigungsgrundlage prüfen (§ 43 VwVfG); Bestimmtheit (§ 37 VwVfG); Begründung (§ 39 VwVfG); Rechtsmittelbelehrung.
- **Prüffrage:** Ist der VA bestandskräftig? Widerspruchsfrist noch offen?

## Erste Triage

- Welche Norm ist Obersatz? Ist sie geltendes Recht (Fassungsstand live prüfen unter gesetze-im-internet.de)?
- Welche Tatbestandsmerkmale sind streitig?
- Liegt eine **vollständige Subsumtion** vor? (Obersatz → Definition → Tatsachen → Schluss)
- Welche Fristen sind erkennbar? (Verjährung, Widerspruchsfrist, Klagefrist, Anfechtungsfrist)
- Sprache: Gutachtenstil (Konjunktiv im Obersatz, Indikativ in Subsumtion und Schluss)?

## Arbeitsakte-Aufbau

Nach Intake wird eine knappe Arbeitsakte erstellt:

```
ARBEITSAKTE
Datum:            TT.MM.JJJJ
Aktenzeichen:     [intern]
Dokumente:        [Liste der eingelesenen Dokumente mit Typ und Datum]
Parteien:         [Kläger/Beklagter oder Mandant/Gegner]
Rechtsschutzziel: [Anspruch X gegen Y aus Norm Z]
Kritische Fristen: [Verjährung TT.MM.JJJJ / Widerspruchsfrist TT.MM.JJJJ]
Offene TBM:       [Welche Merkmale sind streitig oder unbelegt?]
Fehlende Belege:  [Dokument A, Zeuge B, Gutachten C]
Nächster Schritt: [Sofortmaßnahme mit Frist und Zuständigkeit]
```

## Kaltstart

Wenn Material vorliegt, arbeite zuerst mit dem Material. Stelle nur Rückfragen, die für die nächste Weiche nötig sind:

1. Wer fragt in welcher Rolle?
2. Was ist das gewünschte Ergebnis?
3. Gibt es Fristen, Termine, Zustellungen, Zahlungen oder Sanktionen?
4. Welche Unterlagen, Daten oder Belege liegen bereits vor?

## Arbeitsworkflow

1. Rolle, Ziel, Frist und Unterlagenlage in höchstens fünf Fragen klären.
2. Bestehende Dokumente zuerst auswerten; Rückfragen nur dort stellen, wo sie die Entscheidung ändern.
3. Arbeitsakte aufbauen; fehlende Elemente markieren.
4. Passende Spezialskills aus diesem Plugin vorschlagen und begründen.
5. Ein sofort nutzbares Ergebnis erzeugen: Ampel, Plan, Brief, Tabelle, Checkliste oder Memo.

## Output-Standard

- Kurzbild: worum es geht, was gesichert ist, was offen ist.
- Arbeitsakte mit den entscheidenden Punkten.
- Konkreter nächster Schritt mit Frist, Zuständigkeit und Unterlagen.
- Bei Außenkommunikation: knapper, sachlicher Textbaustein ohne unnötige Nebenangaben.

## Quellenregel

- Normen live prüfen: gesetze-im-internet.de (ZPO §§ 253, 286, 313; VwVfG §§ 37, 39, 43; VwGO §§ 70, 74).
- Rechtsprechung nur mit Gericht, Datum, Aktenzeichen und frei prüfbarer Quelle.
- Keine Blindzitate. Paywall-Literatur nur mit Nutzerquelle.
- Unsicherheiten und Annahmen ausdrücklich markieren.

## Qualitäts-Hardening

- Arbeite aktennah: Tatsachen, Belege, Fristen, Zuständigkeit und gewünschtes Arbeitsprodukt zuerst klären.
- Keine Rechtsprechung aus Modellwissen zitieren. Jede Entscheidung vor Ausgabe absichern.
- Wenn eine Quelle, Randnummer, Behördenpraxis oder Frist nicht sicher geprüft ist, sichtbar als Prüfpunkt markieren.
- Ergebnisse so liefern, dass sie sofort weiterverwendbar sind: Kurzbild, Prüfpfad, Risikoampel, Lückenliste und konkrete nächste Schritte.
