---
name: allgemein
description: "Einstieg und Orientierung für das Mietrecht-Plugin: Wohnraum- und Gewerberaummiete für Vermieter und Mieter, amtliche Mietspiegel-Quellen, Mieterhoehung, Mietsenkung, Nebenkostenprüfung und -erstellung, Kündigung, Kautionsrückforderung und Klageentwurf."
---

# Mietrecht — Allgemein

## Worum geht es?

Dieses Plugin unterstuetzt Mieter, Vermieter, Hausverwaltungen und deren Anwaelte bei allen praxisrelevanten Fragen des deutschen Mietrechts. Es deckt Wohnraummiete und Gewerberaummiete ab: Mieterhoehungsverlangen, Mietsenkungsverlangen nach Mietpreisbremse, Nebenkostenpruefung, Kuendigungsrecht (Eigenbedarf, Zahlungsverzug), Kautionsrueckforderung, WEG-Beschlussanfechtung und Klageentwurf zum Amtsgericht.

Ein Alleinstellungsmerkmal ist die Einbindung offizieller Mietspiegel-Quellen fuer Bundeslaender, Top- und Universitaetsstaedte. Es werden ausschliesslich amtliche Quellen verwendet; keine Schaetzdaten oder Onlineportale.

## Wann brauchen Sie diese Skill?

- Sie sind Vermieter und wollen ein Mieterhoehungsverlangen auf ortsuebliche Vergleichsmiete erstellen.
- Sie sind Mieter und haben ein Mieterhoehungsverlangen erhalten und wollen pruefen, ob Sie Widerspruch einlegen koennen.
- Sie pruefen eine Betriebskostenabrechnung auf Formfehler, Umlagefaehigkeit und rechnerische Richtigkeit.
- Sie benoetigen als Vermieter ein Kuendigungsschreiben wegen Eigenbedarfs oder Zahlungsverzugs.
- Sie wollen eine Beschlussanfechtungsklage gegen einen WEG-Beschluss vorbereiten.

## Fachbegriffe (kurz erklaert)

- **Ortsuebliche Vergleichsmiete** — Die uebliche Miete fuer Wohnungen vergleichbarer Art, Groesse, Ausstattung und Lage; Massstab fuer Mieterhoehungen nach § 558 BGB.
- **Kappungsgrenze** — Maximale prozentuale Erhoehung innerhalb von drei Jahren; regelmaessig 20 %, in Spannungsgebieten 15 %.
- **Mietpreisbremse** — §§ 556d ff. BGB; Neuvermietungsmiete darf in Gebieten mit angespanntem Wohnungsmarkt die ortsuebliche Vergleichsmiete um nicht mehr als 10 % uebersteigen.
- **Qualifizierter Mietspiegel** — Mietspiegel, der nach wissenschaftlichen Grundsaetzen erstellt und anerkannt wurde (§ 558d BGB); hat Vermutungswirkung.
- **Betriebskosten** — Laufende Kosten des Gebaeudebetriebs, die nach Betriebskostenverordnung (BetrKV) umlagefaehig sind.
- **Schonfristzahlung** — Zahlung aller Mietruckstaende durch den Mieter innerhalb von zwei Monaten nach Zustellung der Raeumungsklage; heilt fristlose Kuendigung (§ 569 Abs. 3 BGB).
- **WEG** — Wohnungseigentuemergemeindschaft; geregelt im Wohnungseigentumsgesetz (WEG) in der Fassung nach der Reform 2020.

## Rechtsgrundlagen

- §§ 535-580 BGB — Mietvertrag allgemein
- §§ 556-556g BGB — Betriebskosten und Mietpreisbremse
- §§ 558-558e BGB — Mieterhoehung auf ortsuebliche Vergleichsmiete
- § 558d BGB — Qualifizierter Mietspiegel
- §§ 543, 569 BGB — Ausserordentliche Kuendigung
- § 573 BGB — Ordentliche Kuendigung durch Vermieter (Eigenbedarf)
- § 573c BGB — Kuendigungsfristen
- § 551 BGB — Begrenzung und Anlage der Mietkaution
- §§ 44 ff. WEG — Beschlussanfechtung und -klage (nach WEG-Reform 2020)
- § 29a ZPO — Ausschliessliche Zustaendigkeit Amtsgericht bei Wohnraum

## Schritt-fuer-Schritt: Einstieg ins Plugin

1. Mandantenkonstellation klaeren: Vermieter oder Mieter, Wohnraum oder Gewerbe, Bestandsmiete oder Neuabschluss.
2. Phase des Mandats bestimmen: Mieterhoehung, Nebenkostenstreit, Kuendigung, Kaution, WEG oder Klage.
3. Passenden Skill auswaehlen (siehe Skill-Tour).
4. Eilfristen pruefen: WEG-Anfechtungsklage (§ 45 WEG: ein Monat), Kuendigungsfristen (§ 573c BGB), Mieterhoehungs-Zustimmungsfrist (zwei Monate § 558b BGB).
5. Anschluss-Skill bestimmen: nach Mietspiegel-Ermittlung typischerweise Mieterhoehungsverlangen oder Widerspruch; nach Kuendigung ggf. Klageentwurf.

## Skill-Tour (was gibt es hier?)

**Einstieg und Triage**

- `mandat-triage-mietrecht` — Eingangs-Abfrage: Mandantenrolle, Gegenstandsart, Sachgebiet und Fristen-Sofort-Check.

**Datenerhebung**

- `lage-und-ausstattung-erheben` — Strukturierte Datenerhebung fuer Mietspiegel-Einordnung: Adresse, Baujahr, Wohnflaeche, Ausstattungsmerkmale.
- `mietspiegel-quellen` — Prueft ortsuebliche Vergleichsmiete anhand amtlicher Mietspiegel-Quellen pro Bundesland und Stadttyp.

**Mieterhoehung (Vermieter)**

- `mieterhoehungsverlangen-erstellen` — Mieterhoehungsverlangen nach § 558a BGB mit Begruendung durch Mietspiegel oder Vergleichswohnungen.

**Mieterhoehung (Mieter)**

- `mieterhoehung-pruefen-widersprechen` — Mieterhoehungsverlangen auf Form, Frist, Kappungsgrenze und Begruendung pruefen; Widerspruchs- oder Teilzustimmungs-Entwurf.
- `mietsenkungsverlangen` — Miete auf Mietpreisbremse (§§ 556d ff. BGB), § 5 WiStG und § 291 StGB pruefen; qualifizierte Ruege erstellen.

**Nebenkostenabrechnung**

- `nebenkostenabrechnung-erstellen` — Rechtssichere Betriebskostenabrechnung fuer Vermieter nach § 556 BGB und BetrKV.
- `nebenkostenabrechnung-pruefen` — Betriebskostenabrechnung auf Frist, Form, Umlagefaehigkeit, Verteilerschluessel und HeizkostenV pruefen.

**Kuendigung**

- `mahnung-zahlungsverzug-mieter` — Mahnung und fristlose Kuendigung wegen Zahlungsverzugs nach § 543 Abs. 2 Nr. 3 BGB; gestuftes Schreibenpaket.
- `eigenbedarfskuendigung-erstellen` — Ordentliche Kuendigung wegen Eigenbedarfs nach § 573 Abs. 2 Nr. 2 BGB mit konkreter Begruendung und Fristen.

**Kaution**

- `mietkaution-rueckforderung` — Prueft Rueckforderungsanspruch: Hoechstgrenze, Anlagepflicht, Abrechnungsfrist, Einbehalt und Verjaehrung.

**Kommunikation und WEG**

- `mieteranfragen-beantworten` — Beantwortung von Mieteranfragen sachlich und rechtlich korrekt fuer Vermieter und Hausverwaltungen.
- `weg-beschluss-anfechten` — Prueft Beschlussanfechtungs- und Nichtigkeitsklage nach §§ 44 ff. WEG 2020 mit Monatsfrist.

**Klage**

- `klageentwurf-amtsgericht` — Klageschrift zum Amtsgericht in Mietsachen: Zustaendigkeit, Streitwert, Antraege und Beweisangebote.

## Worauf besonders achten

- **Ausschliesslich amtliche Mietspiegel verwenden.** Das Plugin nutzt nur offiziell anerkannte Quellen; Onlineportale sind keine zulaessige Begruendung fuer Mieterhoehungsverlangen.
- **Kappungsgrenze gilt relativ zum letzten Mieterhoehungsverlangen.** Dreijahresfrist und prozentuale Grenze sind getrennt zu pruefen; Kappungsgrenze in Spannungsgebieten 15 % nach Landesrecht.
- **Kuendigungsbegruendung bei Eigenbedarf muss konkret sein.** Zu abstrakte Begruendungen fuehren zur Unwirksamkeit der Kuendigung; Skill `eigenbedarfskuendigung-erstellen` sichert den Mindestinhalt.
- **WEG-Anfechtungsfrist laeuft hart.** Ein Monat nach Beschlussfassung (§ 45 WEG); danach nur noch Nichtigkeitsklage bei gravierenden Maengeln.
- **Nebenkostenabrechnung muss innerhalb von 12 Monaten zugehen.** Spaeterer Zugang fuehrt zur Unwirksamkeit der Abrechnung und Verlust von Nachzahlungsanspruechen.

## Typische Fehler

- Mieterhoehungsverlangen wird ohne ordnungsgemaesse Begruendung versandt; Mieter kann Zustimmung verweigern und Klage ist unbegrendet.
- Fristlose Kuendigung wird ausgesprochen ohne hilfsweise ordentliche Kuendigung; hilfsweise Kuendigung sichert Rueckfall ab.
- Betriebskostenabrechnung enthaelt nicht umlagefaehige Positionen (z.B. Verwaltungskosten); Mieter kann Rueckforderung geltend machen.
- Mietkaution wird nicht getrennt vom Vermoegen des Vermieters angelegt; bei Insolvenz des Vermieters geht Mieter leer aus.
- WEG-Anfechtungsfrist wird verpasst; nur Nichtigkeitsklage bei sehr schweren Maengeln verbleibt als Option.

## Querverweise

- `subsumtions-pruefer` — Fuer vertiefte Normanwendung bei Einzelfragen (z.B. Tatbestandsmerkmale § 543 BGB).
- `gesellschaftsrecht` — Wenn Vermieter eine GmbH oder AG ist und gesellschaftsrechtliche Fragen relevant werden.
- `mittelstand-corporate-ma` — Wenn Gewerberaummiete im Kontext einer Unternehmenstransaktion steht (Change of Control, Betriebsuebergang).

## Quellen und Aktualitaet

- Stand: 05/2026
- Gesetzesfassungen zum Stand-Datum (BGB, BetrKV, HeizkostenV, WEG, ZPO, WiStG)

<!-- AUDIT 27.05.2026 | welle 5a | neuer allgemein-Skill (Pattern: selbstvertreter-orientierung) -->
