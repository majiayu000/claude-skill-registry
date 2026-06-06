---
name: output-fremdsprachig-en-fr
description: "Gibt das Subsumtionsergebnis auf Englisch oder Franzoesisch aus. Enthaelt obligatorischen Hinweis auf nicht-amtliche Übersetzung und Abweichung von deutschen Originalnormen. Nuetzlich für internationale Mandanten, grenzüberschreitende Sachverhalte und EU-Verfahren."
---

# Output: Fremdsprachig (Englisch und Französisch)

## Zweck

Für internationale Mandanten, grenzüberschreitende Sachverhalte und EU-rechtliche Verfahren ist eine englische oder französische Ausgabe des Subsumtionsergebnisses hilfreich. Dieser Skill erzeugt Ausgaben in beiden Sprachen und kennzeichnet sie ausdrücklich als nicht-amtliche Übersetzungen.

## Triage zu Beginn

1. Welche Sprache wird benötigt? (Englisch / Französisch / zweisprachig)
2. Hat der Sachverhalt einen EU-Bezug? → Französisch empfohlen als EU-Amtssprache
3. Ist das Dokument für eine internationale Schiedsklausel bestimmt? → Englisch ICC/DIS-Standard
4. Ist eine notariell beglaubigte Übersetzung erforderlich? → Hinweis: diese Ausgabe ist nicht beglaubigt
5. Sind Fristen oder Verfahrenshandlungen im Ausland relevant? → Zustellungsregeln und Fristberechnung im Zielland separat prüfen

## Obligatorischer Hinweis (Pflicht in jeder fremdsprachigen Ausgabe)

Jedes Ausgabedokument in englischer oder französischer Sprache beginnt mit:

**Englisch:**
> **Non-official translation — for information purposes only:** This document is a non-official translation of a legal analysis conducted under German law and/or European Union law. The original German or French text of the applicable statutes, regulations and judgments is authoritative. This translation does not constitute legal advice and has not been prepared by a licensed attorney. It is a mechanical analysis based solely on information provided by the user.

**Französisch:**
> **Traduction non officielle — à titre informatif uniquement:** Ce document est une traduction non officielle d'une analyse juridique effectuée en vertu du droit allemand et/ou du droit de l'Union européenne. Le texte original allemand ou français des lois, règlements et jugements applicables fait foi. Cette traduction ne constitue pas un avis juridique et n'a pas été rédigée par un avocat agréé.

## Terminologie — Englisch

| Deutsch | Englisch |
|---------|---------|
| Tatbestandsmerkmal | constituent element / element of the offence |
| Subsumtion | subsumption / legal classification |
| Anspruchsgrundlage | legal basis / cause of action |
| Schadensersatz | damages / compensation |
| Treu und Glauben | good faith |
| Bereicherungsrecht | unjust enrichment |
| einstweilige Verfügung | interim injunction / preliminary injunction |
| Vorabentscheidungsersuchen | request for a preliminary ruling |
| Verhältnismäßigkeit | proportionality |
| Verwaltungsakt | administrative act / administrative decision |
| Beweislast | burden of proof |
| Darlegungslast | burden of pleading / burden of production |
| Anscheinsbeweis | prima facie evidence |

## Terminologie — Französisch

| Deutsch | Französisch |
|---------|------------|
| Tatbestandsmerkmal | élément constitutif |
| Subsumtion | subsomption |
| Anspruchsgrundlage | fondement juridique |
| Schadensersatz | dommages-intérêts |
| Treu und Glauben | bonne foi |
| einstweilige Verfügung | ordonnance de référé / mesure provisoire |
| Vorabentscheidungsersuchen | renvoi préjudiciel |
| Verhältnismäßigkeit | proportionnalité |
| Beweislast | charge de la preuve |

## Struktur der fremdsprachigen Ausgabe

Die fremdsprachige Ausgabe folgt derselben Struktur wie die deutsche Ausgabe (Vier-Schritt-Schema: Obersatz, Definition, Subsumtion, Ergebnis). Rechtsbegriffe werden beim ersten Auftreten in eckigen Klammern mit dem deutschen Originalterm versehen: "legal basis [Anspruchsgrundlage]".

Bei EU-Rechtsbegriffen gilt die Terminologie der amtlichen Sprachfassung (eur-lex.europa.eu) als maßgebend.

## Sprachauswahl

Das System fragt am Anfang:
- (A) Englisch / English
- (B) Französisch / Français
- (C) Zweisprachig Deutsch-Englisch (parallele Spalten)
- (D) Dreisprachig Deutsch-Englisch-Französisch

Für Sachverhalte mit Bezug zu EU-Institutionen (EuGH, Kommission, Rat) empfiehlt das System Französisch als primäre EU-Arbeitssprache zusätzlich zur englischen Fassung.

## Besondere Hinweise bei internationalen Sachverhalten

- Schiedsverfahren: Sprachregelung in der Schiedsklausel beachten (§ 1045 ZPO; ICC-Regeln; DIS-Regeln)
- Gerichtsstand und Zustellungsfragen: EuGVVO (VO 1215/2012), HZÜ, EuZVO — live prüfen
- Ausländisches Recht wird nicht angewendet; bei Kollisionsrechtsfragen Verweis auf IPR (EGBGB, Rom I-VO, Rom II-VO)

## Quellenregel

- Rechtsprechung nur mit Gericht, Datum, Aktenzeichen und frei prüfbarer Quelle (curia.europa.eu für EuGH; dejure.org; bgh.de).
- Keine BeckRS-, juris-, Kommentar-, Handbuch- oder Aufsatz-Blindzitate aus Modellwissen.
- EU-Normtext live prüfen: eur-lex.europa.eu.

## Qualitäts-Hardening

- Arbeite aktennah: Tatsachen, Belege, Fristen, Zuständigkeit und gewünschtes Arbeitsprodukt zuerst klären.
- Keine Rechtsprechung aus Modellwissen zitieren. Jede Entscheidung vor Ausgabe absichern.
- Keine BeckRS-, juris-, Kommentar-, Handbuch- oder Aufsatz-Blindzitate. Literatur nur verwenden, wenn der Nutzer sie bereitstellt.
- Wenn eine Quelle, Randnummer, Behördenpraxis oder Frist nicht sicher geprüft ist, sichtbar als Prüfpunkt markieren und keine Scheinpräzision erzeugen.
- Ergebnisse so liefern, dass sie sofort weiterverwendbar sind: Kurzbild, Prüfpfad, Risikoampel, Lückenliste und konkrete nächste Schritte.
- Normtext live prüfen: gesetze-im-internet.de (Bund), eur-lex.europa.eu (EU-Recht).
