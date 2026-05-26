---
name: vaf-feldinventar
description: "Erstellt ein Feldinventar mit Pflichtfeld, Quelle, Beispielwert, Risiko, Rückfrage und Einfügeort für den Vertragsgenerator."
---

# Feldinventar

## Aufgabe

Der Skill baut die zentrale Datenmatrix für den Vertrag. Er arbeitet freistehend innerhalb des Vertragsausfüller-Plugins und setzt keine anderen Plugins voraus.

## Startet bei

- hochgeladener Word-Vorlage oder altem Vertrag
- Term Sheet, E-Mail, Tabelle oder Freitext mit Eckdaten
- Wunsch nach neuem Vertragsentwurf
- Wunsch nach Redline oder Track Changes

## Workflow

1. Alle Platzhalter und erkannten Variablen als Tabelle erfassen.
2. Pflichtfelder, optionale Felder, abgeleitete Werte und juristische Prüfwerte trennen.
3. Konflikte zwischen Vorlage, Altvertrag und Term Sheet markieren.
4. Ein Feld erst als freigegeben behandeln, wenn Wert, Quelle und Plausibilität klar sind.

## Ausgabe

- Vertragsdatenmatrix
- Rückfragenliste
- Ausfüllprotokoll
- Entwurfs- oder Prüfvermerk
- klare Stopper vor Track Changes, falls noch keine ausdrückliche Bestätigung vorliegt

## Leitplanken

- Originaldateien werden nie überschrieben.
- Track Changes, Redline oder Vergleichsfassung nur nach ausdrücklicher Rückfrage und Bestätigung.
- Offene Werte bleiben sichtbar; sie werden nicht erfunden.
- Juristische Wahlentscheidungen werden erklärt und protokolliert.
