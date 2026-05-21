---
name: tabellenpruefung
description: "Tabellarisches Vertragsreview als Prompt-Matrix — pro Spalte ein Extraktionsprompt (was wird gefragt), pro Zeile ein dokumentspezifischer Prompt (wie wird dieses Dokument behandelt). Eine Zeile pro Dokument, eine Spalte pro Datenpunkt, jede Zelle mit wörtlichem Quellenzitat und Fundstelle. Geeignet für M&A-Due-Diligence (Change-of-Control, Abtretungsverbote, MAC-Klauseln in vielen Zielgesellschaftsverträgen), Vendor-Vertragsaudits und jeden anderen Stapeldurchlauf. Lädt bei „tabellarisches Review\", „Review-Raster\", „Prompt-Tabelle\", „Felder aus Verträgen extrahieren\", „Dokumente auf X, Y, Z prüfen\" oder bei Verweis auf einen Dokumentenordner mit Vergleichsauftrag."
---

# Tabellarisches Vertragsreview als Prompt-Matrix

## Zweck

Sie haben einen Stapel Dokumente und eine Liste von Fragen, die für jedes Dokument konsistent beantwortet werden müssen. Das Ergebnis ist eine Tabelle: **Dokumentenzeilen × Datenpunktspalten**, jede Zelle rückverfolgbar bis auf die exakten Wörter im Quelltext.

**Die Prompt-Matrix:**
- **Prompt pro Spalte** (Spaltenprompt) = die Frage, die für *alle* Dokumente gestellt wird. „Welche Kündigungsfrist gilt? Wörtliches Zitat mit Fundstelle."
- **Prompt pro Zeile** (Zeilenprompt) = die *dokumentspezifische* Anweisung, die das Lesen dieses einen Dokuments steuert. „Dieser Vertrag ist ein Konzernvertrag — § 311 AktG zusätzlich prüfen." Oder: „Anlage 7 liegt nur in geänderter Fassung vor — Originalfassung anfordern."

Der Wert der Matrix: gleiche Fragen für alle Dokumente (Vergleichbarkeit), aber gezielte Sonderbehandlung dort, wo ein Dokument abweicht (Genauigkeit).

Dies ist **keine** Problemerkennung. `/gesellschaftsrecht:dd-findings-extraktion` findet die 30 Probleme in 2.000 Dokumenten. Dieser Skill beantwortet die gleichen 15 Fragen für alle 2.000 Dokumente.

Dies ersetzt **nicht** das Lesen des Dokuments. Jede Zelle ist ein **Hinweis, der der Verifikation bedarf**, kein abschließender Befund.

## Eingaben

- **Dokumentenquelle**: Datenraum-Ordner (VDR), lokaler Pfad, SharePoint-Bibliothek, Liste von Dateipfaden
- **Spaltenprompts** (Schema): natürlichsprachig vom Nutzer beschrieben oder als `review-schema.yaml` hochgeladen
- **Zeilenprompts** (optional): pro Dokument zusätzliche Anweisungen — als `zeilen-prompts.yaml`, als Übersichtstabelle vom Nutzer eingegeben oder leer (dann nur Spaltenprompts)
- **Ausgabeformat**: Excel (`.xlsx`) oder CSV
- **Praxisprofil** (CLAUDE.md): Due-Diligence-Struktur, Wesentlichkeitsschwellen, Hausformat

## Rechtlicher Rahmen

**M&A Due Diligence:**
- §§ 311 Abs. 2, 241 Abs. 2 BGB (vorvertragliche Aufklärungspflichten)
- §§ 443, 444 BGB (Garantien, Haftungsausschluss)
- § 442 BGB (Kenntnis des Käufers, Ausschluss der Gewährleistung)
- BGH, Urt. v. 27.03.2009 – V ZR 30/08, NJW 2009, 2064 Rn. 25 (Due-Diligence-Pflicht des Käufers; Kenntnis von Mängeln)

**Change-of-Control:**
- BGH, Urt. v. 29.04.2008 – KZR 2/07, NJW 2008, 3055 Rn. 18 (Kündigung bei mittelbarem Kontrollwechsel)
- BGH, Urt. v. 10.11.2016 – I ZR 193/15, NJW-RR 2017, 877 Rn. 14 (Vertragsübernahme ohne Schuldnerzustimmung)

**Abtretungsverbote:**
- § 399 BGB (Abtretungsausschluss durch Parteivereinbarung)
- § 354a HGB (Unwirksamkeit im kaufmännischen Verkehr)
- BGH, Urt. v. 14.11.1991 – IX ZR 31/91, NJW 1992, 1026

**MAC-Klauseln:**
- §§ 313, 314 BGB (Wegfall der Geschäftsgrundlage; außerordentliche Kündigung) als gesetzlicher Hintergrund

**Kommentarliteratur:**
- Westermann, in: MüKoBGB, 9. Aufl. 2022, § 453 Rn. 12 (Unternehmenskauf, Due Diligence)
- Bayer, in: Lutter/Hommelhoff, GmbHG, 21. Aufl. 2023, § 15 Rn. 5 (Abtretung GmbH-Anteile)
- Hopt, in: Baumbach/Hopt, HGB, 41. Aufl. 2024, § 354a Rn. 1 (Abtretungsverbot)

## Ablauf

### Schritt 0 — Was und Wo

Klären:
1. **Dokumente.** Wo? Wie viele? Bei mehr als 200: Warnung, dass das Zeit braucht; Vorschlag, mit einem wesentlichkeitsgefilterten Teilbestand zu beginnen.
2. **Spalten.** Welche Fragen? (siehe Schritt 1)
3. **Zeilen-Sonderbehandlung.** Gibt es Dokumente, die besonders gelesen werden müssen? Konzernverträge, Anlagen mit fehlender Originalfassung, gemischtsprachige Verträge? (siehe Schritt 2)
4. **Ausgabe.** Excel oder CSV.

### Schritt 1 — Spaltenprompts definieren

Spaltenliste in ein getyptes Schema überführen. Für jede Spalte: `id`, `label`, `typ`, `prompt`, `optionen` (bei `klassifizieren`).

**Spaltentypensystem:**

| Typ | Was zurückkommt | Verwendung |
|---|---|---|
| `wörtlich` | Exaktes Zitat | Definitionen, operative Klauselformulierungen |
| `klassifizieren` | Ein Wert aus fester Liste | Ja/Nein, Klauselvarianten |
| `datum` | ISO-Datum | Abschluss, Ablauf, Kündigungsfrist |
| `dauer` | Zahl + Einheit | Vertragslaufzeit, Kündigungsfrist |
| `betrag` | Zahl + Währungscode | Haftungsobergrenzen, Schwellenwerte |
| `zahl` | Bloße Zahl | Anzahlen, Prozente |
| `frei` | Kurze Freitextzusammenfassung | Sparsam — erzeugt Inkonsistenz |

**Wörtlichkeitsregel:** Jede Nicht-`wörtlich`-Spalte erfasst auch das exakte Quellzitat als Begleitfeld. Die Antwort in der Zelle ist die Interpretation; das Zitat ist der Beweis.

**Beispiel-Schema (Spaltenprompts) als `review-schema.yaml`:**

```yaml
spalten:
  - id: gegenpartei
    label: Gegenpartei
    typ: wörtlich
    prompt: >
      Wer ist die Gegenpartei dieses Vertrags? Genaue Firmierung mit Rechtsform,
      wie sie im Rubrum oder im ersten Absatz steht. Exaktes Zitat.

  - id: wirksamkeitsdatum
    label: Wirksamkeitsdatum
    typ: datum
    prompt: >
      Wann tritt der Vertrag in Kraft? Suche im Unterschriftenblock oder
      in einer „Wirksamkeitsdatum"-Klausel. Falls Unterschriften an
      verschiedenen Tagen: das spätere. ISO-Format JJJJ-MM-TT.

  - id: change_of_control
    label: Change-of-Control
    typ: klassifizieren
    optionen:
      - zustimmungserforderlich
      - kündigungsrecht_bei_coc
      - keine_regelung
      - sonstige
    prompt: >
      Hat die Gegenpartei ein Sonderrecht bei Kontrollwechsel beim Mandanten?
      Auch mittelbaren Kontrollwechsel beachten (BGH KZR 2/07). Wörtliches
      Zitat der einschlägigen Klausel als Begleitfeld.

  - id: abtretung
    label: Abtretung
    typ: klassifizieren
    optionen:
      - frei_übertragbar
      - zustimmungserforderlich
      - abtretungsverbot_absolut
      - abtretungsverbot_354a_HGB_vorbehalt
      - keine_regelung
    prompt: >
      Welche Regelung zur Abtretung? Bei absolutem Verbot zwischen Kaufleuten
      § 354a HGB-Vorbehalt prüfen (BGH NJW 1992, 1026).

  - id: haftungsobergrenze
    label: Haftungsobergrenze
    typ: betrag
    prompt: >
      Welche betragsmäßige Haftungsobergrenze ist vereinbart? In EUR.
      Mehrere Limits (z. B. pro Schadensfall vs. aggregat) separat erfassen.
```

### Schritt 2 — Zeilenprompts definieren (das Neue an dieser Matrix)

Spaltenprompts sind generisch. Bei Stapel-Reviews gibt es aber oft Dokumente, die anders behandelt werden müssen — entweder weil sie inhaltlich abweichen oder weil dem Reviewer schon etwas zu diesem Dokument bekannt ist.

Drei typische Quellen für Zeilenprompts:

1. **Dokumenttyp-spezifisch.** Konzernvertrag → § 311 AktG zusätzlich prüfen; Mietvertrag → Mietpreisbremse (§ 556d BGB) prüfen; Rahmenvertrag → auf Einzelverträge verweisen; AGB → §§ 305 ff. BGB.
2. **Mandanten-/Mandatsspezifisch.** „Vertrag X ist der Hauptliefervertrag — bei jeder unklaren Klausel zur Hauptverhandlung mit dem Lead-Counsel eskalieren."
3. **Dokument-spezifisch.** „Anlage 7 liegt nur in geänderter Fassung vor — bei Streitstand zur Originalfassung kommentieren." „Dieser Vertrag ist auf Englisch geschrieben — bei Mehrdeutigkeit auf den englischen Urtext zurückgreifen."

**Beispiel `zeilen-prompts.yaml`:**

```yaml
zeilen:
  - dokument: "Lieferanten-MSA — Alpha GmbH.pdf"
    typ: rahmenvertrag
    prompt: >
      Hauptliefervertrag, Konzernvertrag im Sinne der §§ 15 ff. AktG.
      Zusätzlich prüfen: § 311 AktG (Beherrschungsvertrag), § 308 AktG
      (Weisungsrecht). Bei unklarer CoC-Klausel zum Lead-Counsel
      eskalieren.

  - dokument: "Mietvertrag Hauptniederlassung Berlin.pdf"
    typ: gewerberaummietvertrag
    prompt: >
      Gewerberaum, kein Wohnraum (§ 535 ff. BGB allgemein, nicht §§ 549 ff.).
      Indexmietklausel auf Einhaltung § 557b BGB prüfen.
      Konkurrenzschutzklausel separat erfassen, falls vorhanden.

  - dokument: "Vendor Agreement Beta Ltd (EN).pdf"
    typ: internationaler_vertrag
    prompt: >
      Englischsprachiger Vertrag, vermutlich English law. Bei
      Rechtswahlklausel: deutsch oder englisch? Bei Zuständigkeitsklausel:
      Schiedsverfahren oder ordentliche Gerichtsbarkeit?
      Wörtliche Zitate auf Englisch belassen, deutsche Erläuterung
      in `notizen`.

  - dokument: "Anlage K7 — Nachtrag 2024.pdf"
    typ: anlage_nachtrag
    prompt: >
      Nur Nachtrag — Hauptvertrag (Anlage K6) zur Vollständigkeit
      mitlesen. CoC-Klausel ist im Hauptvertrag, nicht hier.

  - dokument: "*"  # Wildcard für alle nicht spezifisch genannten
    typ: standard
    prompt: >
      Standardvertrag, keine Sonderbehandlung. Spaltenprompts wörtlich
      anwenden.
```

### Schritt 3 — Prompt-Matrix anzeigen und bestätigen

Vor dem Probedurchlauf die zusammengesetzte Matrix dem Nutzer zeigen. Beispiel:

```markdown
## Prompt-Matrix — Probedurchlauf

**Dokumente:** 4 (von 80 im VDR)
**Spalten:** 5
**Zeilenprompts:** 4 spezifisch + 1 Wildcard (Standard)

| Dokument | Zeilenprompt-Typ | Gegenpartei (Spalte) | CoC (Spalte) | … |
|---|---|---|---|---|
| Lieferanten-MSA Alpha | rahmenvertrag | wörtlich | klassifizieren | … |
| Mietvertrag Berlin | gewerberaummietvertrag | wörtlich | klassifizieren | … |
| Vendor Agreement Beta | internationaler_vertrag | wörtlich | klassifizieren | … |
| Anlage K7 Nachtrag | anlage_nachtrag | wörtlich | klassifizieren | … |
```

Nutzer bestätigt oder korrigiert. Erst dann Probedurchlauf.

### Schritt 4 — Probedurchlauf (3–5 Dokumente)

Nicht 200 Dokumente mit einem ungeprüften Schema durchlaufen.

Probedurchlauf zeigt:
- Spalten, bei denen die meisten Antworten `unklar` sind → Spaltenprompt mehrdeutig, umformulieren
- `klassifizieren`-Optionen, die nicht passen → Optionen ergänzen oder auf `frei` wechseln
- Zeilenprompts, die zu generisch sind → schärfen
- Konflikte zwischen Spalten- und Zeilenprompt → Vorrangregel klären (Standard: Zeilenprompt ergänzt, ersetzt nicht — der Spaltenprompt bleibt die Hauptfrage)

Schema + Zeilenprompts anpassen, Probedurchlauf wiederholen.

### Schritt 5 — Vollständiger Durchlauf

Ein Unteragent pro Dokument, parallel. Jeder Unteragent erhält:
- Das Dokument
- Alle Spaltenprompts (universell)
- Den zutreffenden Zeilenprompt (oder den Wildcard-Standard)

Jeder Unteragent gibt eine strukturierte Zeile zurück: für jede Spalte `{wert, zustand, zitat, fundstelle}`:
- `wert` — die getypte Antwort (oder null bei `zustand ≠ beantwortet`)
- `zustand` — `beantwortet | nicht_vorhanden | unklar | prüfung_erforderlich`
- `zitat` — wörtlicher Begleittext (kein Paraphrase, keine Auslassungszeichen zwischen nicht zusammenhängendem Text)
- `fundstelle` — Abschnittsnummer, Überschrift, Seite

**Wörtlichkeitsregel** — mechanisch, keine Empfehlung:
- `zitat` MUSS zeichengenaue Kopie zusammenhängenden Texts sein
- NICHT aus Abschnittsüberschrift plus erwartetem Standardtext zusammensetzen
- NICHT paraphrasieren und als wörtlich bezeichnen
- NICHT aus Erinnerung rekonstruieren
- Bei nicht findbarem exaktem Text: `zustand: prüfung_erforderlich`, `wert: null`, `notizen: "zitat_nicht_verfügbar: <Grund>"`

**Zusätzliche Felder bei aktivem Zeilenprompt:**
- `zeilenprompt_befolgt` — Bool: hat der Unteragent die Zeilen-Sonderanweisung beachtet?
- `zeilenprompt_notiz` — was wurde aufgrund des Zeilenprompts zusätzlich erfasst (z. B. „§ 311 AktG geprüft, keine relevante Klausel")

### Schritt 6 — Normalisierung

Spaltenweise gesamte Tabelle prüfen:
- `klassifizieren`: Ausreißer prüfen. Bei 195/200 `zustimmungserforderlich` und 5/200 `frei_übertragbar` → die 5 manuell anschauen.
- `datum`/`dauer`/`betrag`: Formatkonsistenz. Unplausible Werte (99-jährige Laufzeit, 1-EUR-Haftungsdeckelung) auf `prüfung_erforderlich`.
- Zitate: Stichprobe (3–5 Zeilen pro Spalte oder 10 %, je größer) — Quelldokument an `fundstelle` wieder öffnen, Zitat zeichengenau vergleichen. Bei Abweichung: ganze Spalte ausweiten.

### Schritt 7 — Ausgabe

**Markdown** (immer, für die Sitzung):

```markdown
| Dokument | Zeilenprompt | Gegenpartei | Wirksamkeit | CoC | Abtretung | Haftungsobergrenze | ⚠️ Flags |
|---|---|---|---|---|---|---|---|
| Lieferanten-MSA Alpha | rahmenvertrag | Alpha GmbH | 2023-04-01 | zustimmungserforderlich | zustimmungserforderlich | 12 Mio EUR | — |
| Mietvertrag Berlin | gewerberaummietvertrag | Vermieter XY GbR | 2020-11-15 | keine_regelung | absolut (§ 354a HGB-Vorbehalt) | unbegrenzt | ⚠️ Indexmiete prüfen |
| Vendor Agreement Beta | internationaler_vertrag | Beta Ltd | 2024-01-12 | kündigungsrecht_bei_coc | frei_übertragbar | 5 Mio EUR | ⚠️ englisches Recht |
| Anlage K7 Nachtrag | anlage_nachtrag | (s. K6) | 2024-09-20 | (s. K6) | (s. K6) | (s. K6) | — |
```

**Excel** (`.xlsx`) oder **CSV**:
- Jede Datenspalte mit verdeckter Quellspalte gepaart (Zitat + Fundstelle)
- Zellkommentare zeigen das Zitat beim Überfahren (Excel)
- Farbcodierung nach `zustand`: weiß = beantwortet, gelb = unklar/prüfung_erforderlich, grau = nicht_vorhanden
- Zusätzliche Spalte „Zeilenprompt" sichtbar (Dokumenttyp)
- Spalte „Zeilenprompt-Notiz" für die Notiz aus Schritt 5
- `Geprüft`-Spalte pro Datenspalte, vom Reviewer abzuhaken
- `_Schema`-Tabellenblatt mit Spalten- und Zeilenprompt-Definitionen — selbstdokumentierend

Arbeitsergebnis-Kopfzeile aus CLAUDE.md voranstellen plus:

> Dieses Review basiert auf Quelldokumenten, die privilegiert, vertraulich oder beides sein können. Es teilt den Schutzstatus der Quellen — Verteilung über den Vertraulichkeitskreis hinaus kann das Mandatsgeheimnis (§ 43a Abs. 2 BRAO) beeinträchtigen.

### Schritt 8 — Zusammenfassung

- Dokumentenanzahl, Spaltenanzahl, abgeschlossene Zeilen
- Pro Spalte: Anzahl `nicht_vorhanden`, `unklar`, `prüfung_erforderlich`
- Pro Zeilenprompt-Typ: wie viele Dokumente fielen darunter
- Spalten, bei denen die Normalisierung > 10 % der Zeilen flaggte
- Speicherort der Ausgabedateien
- Hinweis: Jede Zelle ist ein Hinweis, kein Befund. Verifikation erforderlich.

## Ausgabeformat

Strukturierte Tabelle (Markdown sitzungsintern + Excel/CSV als Dateien) + `review-schema.yaml` + `zeilen-prompts.yaml` + einseitige Zusammenfassung. Arbeitsergebnis-Kopfzeile und Verteilungshinweis oben.

## Beispiel — kompakte Prompt-Matrix für M&A-DD

**Szenario:** GmbH-Anteilskauf, 8 Zielgesellschaftsverträge. Aufgabe: CoC, Abtretung, Mindestlaufzeit, Haftungsobergrenze extrahieren.

**Spaltenprompts** (universell, gleiche Frage an jeden Vertrag):

| Spalte | Typ | Spaltenprompt (Kurzfassung) |
|---|---|---|
| Gegenpartei | wörtlich | „Wer ist die Gegenpartei? Genaue Firmierung mit Rechtsform aus dem Rubrum." |
| Wirksamkeitsdatum | datum | „Wann tritt der Vertrag in Kraft? Bei verschiedenen Unterschriftsdaten: das spätere." |
| CoC | klassifizieren | „Sonderrecht bei Kontrollwechsel? Auch mittelbaren Kontrollwechsel (BGH KZR 2/07) prüfen." |
| Abtretung | klassifizieren | „Welche Abtretungsregelung? Bei Verbot zwischen Kaufleuten § 354a HGB prüfen." |
| Haftungsobergrenze | betrag | „Betragsmäßige Haftungsobergrenze in EUR. Mehrere Limits separat." |

**Zeilenprompts** (dokumentspezifisch, ergänzt zu Spaltenprompts):

| Zeile (Dokument) | Zeilenprompt |
|---|---|
| Lieferanten-MSA — Alpha GmbH | „Hauptliefervertrag, Konzernvertrag — zusätzlich § 311 AktG (Beherrschung) prüfen. Bei unklarer CoC zum Lead-Counsel eskalieren." |
| Mietvertrag Hauptniederlassung Berlin | „Gewerberaum (§ 535 BGB, nicht §§ 549 ff.). Indexmietklausel auf § 557b BGB prüfen. Konkurrenzschutzklausel separat." |
| Vendor Agreement Beta Ltd (EN) | „Englischsprachiger Vertrag. Rechtswahl und Gerichtsstand klären. Englische Zitate belassen, deutsche Notiz." |
| Anlage K7 Nachtrag | „Nur Nachtrag — Hauptvertrag (Anlage K6) mitlesen. CoC steht im Hauptvertrag." |
| Lizenzvertrag — Gamma SaaS | „SaaS-Vertrag — zusätzlich auf Sub-Auftragsverarbeitung (Art. 28 IV DSGVO) prüfen, da personenbezogene Daten verarbeitet werden." |
| Vertriebsvertrag — Delta GmbH | „Handelsvertreter (§§ 84 ff. HGB) oder Vertragshändler? Klassifikation in Notizen." |
| Joint-Venture-Vertrag — Epsilon AG | „Gleichberechtigte Beteiligung 50:50 — Patt-Regelungen und Deadlock-Klausel separat erfassen, falls vorhanden." |
| Wildcard (alle anderen) | „Standardvertrag, keine Sonderbehandlung. Spaltenprompts wörtlich." |

**Ergebnis** (Auszug):

| Dokument | Zeilen­prompt­typ | Gegenpartei | CoC | Abtretung | Haftungs­obergrenze | Zeilen­prompt-Notiz |
|---|---|---|---|---|---|---|
| Alpha-MSA | rahmenvertrag | Alpha GmbH | zustimmungserforderlich | zustimmungserforderlich | 12 Mio EUR | § 311 AktG geprüft — keine Beherrschungsklausel; CoC eindeutig |
| Berlin-Miete | gewerberaummietvertrag | Vermieter XY GbR | keine_regelung | absolut (§ 354a HGB-Vorbehalt) | unbegrenzt | Indexmiete § 5(2): Klausel ⚠️ § 557b BGB-konform? prüfen |
| Beta-Vendor | internationaler_vertrag | Beta Ltd | kündigungsrecht_bei_coc | frei_übertragbar | 5 Mio EUR | English law, LCIA-Schiedsverfahren — Zuständigkeitsfrage geklärt |
| K7-Nachtrag | anlage_nachtrag | (s. K6) | (s. K6) | (s. K6) | (s. K6) | Verweis auf K6 — separat zu lesen |
| Gamma-SaaS | (eigener) | Gamma GmbH | zustimmungserforderlich | zustimmungserforderlich | 100% Jahresvergütung | Art. 28 IV DSGVO: Sub-AV-Erlaubnis ohne Vorabzustimmung ⚠️ |

## Risiken und typische Fehler

- **Dokumente überspringen.** Jedes vom Nutzer benannte Dokument bekommt eine Zeile. Nicht lesbares Dokument: Zeile mit `prüfung_erforderlich`.
- **Paraphrase als Zitat ausgeben.** Beweiskette = Kernwert. Wörtlichkeitsregel mechanisch.
- **Zeilenprompt überschreibt Spaltenprompt.** Standard: Zeilenprompt **ergänzt**. Wenn der Spaltenprompt fragt „Was ist die Kündigungsfrist?", darf der Zeilenprompt nicht implizieren „Bei diesem Vertrag schauen wir keine Kündigungsfrist an". Bei Konflikt rückfragen.
- **Schema nicht probetesten.** Vollständigkeitsdurchlauf mit fehlerhaftem Schema = verworfene Arbeit. Immer 3–5 Dokumente zuerst.
- **Konfidenzwerte erfinden.** Kein numerischer Konfidenzwert. Stattdessen: `unklar` / `prüfung_erforderlich`-Zustände + verbatim Zitate als Konfidenz-Signal.
- **§ 354a HGB ignorieren.** Abtretungsverbote zwischen Kaufleuten ggf. unwirksam — in Schema-Notizen vermerken.
- **Zeilenprompt aus Erinnerung statt aus Fakten.** Wenn der Reviewer behauptet „dieser Vertrag ist ein Konzernvertrag" — Faktenlage muss aus dem Dokument belegt sein, nicht aus Vermutung.

## Quellenpflicht

Jede rechtliche Beurteilung im Schema-Aufbau und in der Normalisierung mit Norm belegen:
- Abtretungsverbote: `§ 399 BGB`, `§ 354a HGB`
- Change-of-Control: `BGH, Urt. v. 29.04.2008 – KZR 2/07, NJW 2008, 3055 Rn. 18`
- Due-Diligence-Pflichten: `BGH, Urt. v. 27.03.2009 – V ZR 30/08, NJW 2009, 2064 Rn. 25`
- Konzernrecht bei Zeilenprompt: `§§ 15 ff., 308, 311 AktG`
- Gewerberaummiete: `Häublein, in: MüKoBGB, 9. Aufl. 2023, § 535 Rn. 1` (zit.)
- Indexmietklausel: `§ 557b BGB`
- AGB-Kontrolle bei Stapel: `§§ 305 ff. BGB`
- Sub-AV: `Art. 28 Abs. 4 DSGVO`
- Kommentare: `Hopt, in: Baumbach/Hopt, HGB, 41. Aufl. 2024, § 354a Rn. 1`

Hinweis: Dieser Skill ersetzt keine anwaltliche Beratung im konkreten Einzelfall. Jede Zelle der Matrix ist ein Hinweis, der vor Verwendung in einer Garantie, einem Anhang oder einem Memo zu verifizieren ist.
