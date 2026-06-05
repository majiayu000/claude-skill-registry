---
name: workflow-kaltstart-und-routing
description: "Kaltstart und Routing im Plugin subsumtions-pruefer: führt vom ersten Satz oder Dokument in den passenden Arbeitsweg, erkennt Rolle, Ziel, Risiko und Anschluss-Skills."
---

# Kaltstart und Routing

## Aufgabe

Dieser Workflow-Skill führt den Nutzer vom ersten Satz oder Dokument in den passenden Arbeitsweg. Er erkennt Rolle, Ziel, Risiko und wählt den geeigneten Anschluss-Skill aus dem Plugin.

## Routing-Logik

```
Erster Satz / Dokument erhalten
├─ Klausur / Hausarbeit / Probelösung → kandidatenloesung-subsumtion-pruefen
├─ Subsumtion mit Fehler → subsumtions-rewrite-klausurton, workflow-fristen-und-risikoampel
├─ Neuer Mandantenfall, keine Akten → spezial-interaktiver-erstpruefung-und-mandatsziel
├─ Mandantenfall mit Akten → workflow-dokumentenintake → dann Fallbild
├─ Frist-Notfall (< 30 Tage) → workflow-fristen-und-risikoampel (Sofortampel)
├─ Beweisfrage → spezial-subsumtions-tatbestand-beweis-und-belege
├─ Europarecht-Bezug → de-eu-recht-abgrenzung → einschlaegige-normen-vorschlagen-eu
├─ Internationaler Bezug → spezial-rechtsberatung-internationaler-bezug-und-schnittstellen
├─ Mehrere Parteien → spezial-pruefen-mehrparteien-konflikt-und-interessen
├─ Behörde / Register → spezial-vier-behoerden-gericht-und-registerweg
├─ Verhandlung / Vergleich → spezial-schema-verhandlung-vergleich-und-eskalation
├─ Rechtsfolge berechnen → spezial-rechtsfolgen-zahlen-schwellen-und-berechnung
├─ Schriftsatz / Memo erstellen → spezial-schritt-schriftsatz-brief-und-memo-bausteine
└─ Ausgabe in Alltagssprache → output-alltagssprache-de
```

## Kaltstart — Fünf Kernfragen

1. **Wer fragt?** (Anwalt, Richter, Klausurkandidat, Mandant, Behördenmitarbeiter)
2. **Was ist das Ziel?** (Anspruch, Abwehr, Gutachten, Schriftsatz, Information, Berechnung)
3. **Was ist die kritische Frist?** (Verjährung, Klagefrist, Widerspruchsfrist — Datum?)
4. **Was liegt vor?** (Sachverhalt, Akten, Urteil, Schriftsatz, nichts)
5. **Was ist der gewünschte Output?** (Memo, Schriftsatz, Klausurgutachten, Brief, Tabelle, Alltagssprache)

## Kaltstart-Arbeitssequenz

Wenn Unterlagen vorhanden sind, arbeite zuerst aus den Unterlagen:
1. Dokument einlesen (→ workflow-dokumentenintake)
2. Fallbild erstellen (Parteien, Ziel, Frist, TBM)
3. Routing zu Spezialskill
4. Sofortampel (Fristen, Beweis, Risiko)

Wenn keine Unterlagen vorhanden sind:
1. Fünf Kernfragen stellen (nur die, die die nächste Weiche bestimmen)
2. Fallbild aus Antworten erstellen
3. Routing zu Spezialskill

## Sonderfall: Frist-Notfall

Wenn eine Frist innerhalb von 30 Tagen abläuft:
1. Sofort → workflow-fristen-und-risikoampel
2. Verjährungshemmung prüfen (§§ 203–213 BGB): Klageerhebung, Güteantrag, Mahnbescheid, Verhandlungen
3. Mandant informieren und Aktennotiz erstellen

## Subsumtion — Wenn-Dann-Logik

- **Vier-Schritt-Schema:** Obersatz (Norm), Definition (Auslegung des TBM), Subsumtion (konkreter Sachverhalt unter Definition), Ergebnis.
- **Obersatz:** "Anspruchsteller könnte gegen Anspruchsgegner einen Anspruch auf X aus § Y haben." Nicht "hat", solange noch zu prüfen.
- **Definition vor Subsumtion:** Jedes streitige Merkmal mit Definition aus Rspr./Lit. unterlegen.
- **Subsumtion = konkrete Tatsachen unter abstrakte Definition.**
- **Zwischen- und Gesamtergebnis:** Jedes TBM mit Zwischenergebnis abschließen.
- **Falle:** Zirkelschluss — die Definition muss aus einer Quelle gespeist sein, nicht aus dem zu prüfenden Sachverhalt.

## Output-Standard

- Kurzbild: worum es geht, was gesichert ist, was offen ist.
- Routing-Empfehlung: Welcher Skill als nächstes?
- Sofortampel (Fristen, Beweis).
- Konkreter nächster Schritt mit Frist, Zuständigkeit und Unterlagen.

## Quellenregel

- Aktuelle Normen live prüfen: gesetze-im-internet.de.
- Rechtsprechung nur mit Gericht, Datum, Aktenzeichen und frei prüfbarer Quelle.
- Keine Blindzitate. Paywall-Literatur nur mit Nutzerquelle.
- Unsicherheiten und Annahmen ausdrücklich markieren.

## Qualitäts-Hardening

- Arbeite aktennah: Tatsachen, Belege, Fristen, Zuständigkeit und gewünschtes Arbeitsprodukt zuerst klären.
- Keine Rechtsprechung aus Modellwissen zitieren. Jede Entscheidung vor Ausgabe absichern.
- Wenn eine Quelle, Randnummer, Behördenpraxis oder Frist nicht sicher geprüft ist, sichtbar als Prüfpunkt markieren.
- Ergebnisse so liefern, dass sie sofort weiterverwendbar sind: Kurzbild, Prüfpfad, Risikoampel, Lückenliste und konkrete nächste Schritte.
