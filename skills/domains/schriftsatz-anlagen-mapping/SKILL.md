---
name: schriftsatz-anlagen-mapping
description: "Schriftsatzstellen, Tatsachenbehauptungen, Beweisangebote und Anlagen in eine Matrix bringen; erkennt fehlende, doppelte und nur scheinbar belegte Anlagen."
---

# Schriftsatz-Anlagen-Mapping

## Zweck

Dieser Skill liest den Schriftsatz als Landkarte. Jede erhebliche Behauptung bekommt eine Belegstelle; jede Anlage bekommt eine Funktion. Das verhindert die verbreitete Krankheit: viele Anlagen, aber kein tragender Vortrag.

## Mindestinput

- Schriftsatzentwurf oder Auszug.
- Vorläufiges Anlagenverzeichnis oder Dateiliste.
- Angabe, ob geprüft oder neu nummeriert werden soll.

## Arbeitsablauf

1. Extrahiere alle Anlagenzitate und Beweisangebote.
2. Formuliere den Tatsachenkern jeder Beweisstelle.
3. Ordne vorhandene Dateien zu und markiere unklare Zuordnungen.
4. Prüfe, ob der Tatsachenvortrag im Schriftsatz selbst steht.
5. Erzeuge Lücken-, Doppelungs- und Überhangliste.

## Ausgabe

- Belegmatrix als Tabelle.
- Liste „zitiert, aber Datei fehlt“.
- Liste „Datei vorhanden, aber nicht eingeführt“.
- Korrekturvorschläge für Schriftsatzanker.

## Typische Fehler, die du aktiv suchst

- Unklare Anlagenfunktion: Die Datei existiert, aber niemand sagt, welche Tatsache sie beweist.
- Nummerierung folgt dem Ordner, nicht dem Schriftsatz.
- Der Schriftsatz versteckt entscheidenden Vortrag in der Anlage.
- Dateiname, Stempel oder Anlagenverzeichnis widersprechen einander.

## Anschluss-Skills

- `anlagen-zu-schriftsaetzen` für den Hauptworkflow.
- `anlagen-qualitygate-finalcheck` vor Versand.
- `schriftsatz-anlagen-mapping` für Belegmatrix und Lückenliste.

## Quellen- und Vorsichtsregel

Bei tragenden Aussagen zu Form, elektronischer Einreichung oder prozessualer Verwertbarkeit aktuelle amtliche Quellen prüfen: ZPO, BRAO, ERVV, ERVB und gerichtliche Hinweise. Keine BeckRS-/juris-/Literatur-Blindzitate. Rechtsprechung nur mit Gericht, Entscheidungsform, Datum, Aktenzeichen und frei prüfbarer Quelle nennen.
