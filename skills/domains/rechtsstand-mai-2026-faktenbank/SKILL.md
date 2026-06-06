---
name: rechtsstand-mai-2026-faktenbank
description: "Faktenbank und Quellen-Gate für aktuelle mietrechtliche und WEG-rechtliche Aussagen mit Stand 29.05.2026. Nutze diesen Skill vor Ausgaben zu Mietpreisbremse, Mieterhöhung, Betriebskosten, Kündigung, Kaution, Steckersolargeräten, virtueller Eigentümerversammlung, WEG-Beschlussklage und baulichen Veränderungen."
---

# Rechtsstand Mai 2026 — Faktenbank Mietrecht und WEG

## Zweck

Dieser Skill ist das Quellen-Gate des Mietrecht-Plugins. Er wird geladen, wenn aktuelle Rechtslage, Mietpreisbremse, WEG-Reform, Betriebskosten, Kündigung, Kaution, bauliche Veränderung oder gerichtliche Durchsetzung relevant sind.

Stand dieser Faktenbank: **29.05.2026**. Bei konkreten Mietspiegeln, Landesverordnungen und Rechtsprechung immer live prüfen.

## Quellenregel

- Keine BeckRS-, juris-, Kommentar-, Handbuch- oder Aufsatzfundstellen aus Modellwissen.
- Rechtsprechung nur mit Gericht, Entscheidungsform, Datum, Aktenzeichen und freiem/amtlichem Link.
- Mietspiegel nur aus amtlicher kommunaler Quelle oder aus `references/mietspiegel-quellen.md`.
- Landesverordnungen zur Mietpreisbremse/Kappungsgrenze immer für Bundesland, Gemeinde und Zeitpunkt prüfen.

## Verifizierte Rechtsstandsanker

| Thema | Gesicherter Anker | Praktische Aussage | Freie Quelle |
|---|---|---|---|
| Mietpreisbremse | § 556d BGB; BGH, Urteil vom 18.12.2024, VIII ZR 16/23 | Mietpreisbremse immer dreistufig prüfen: Gebiet/Verordnung, Ausgangsmiete und Ausnahmen, dann Rüge/Rückforderung. Verfassungs- und Verordnungsfragen nicht aus Modellwissen behaupten. | https://www.gesetze-im-internet.de/bgb/__556d.html / https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&nr=140461 |
| Modernisierung und Mietpreisbremse | BGH, Urteil vom 27.11.2024, VIII ZR 36/23 | Modernisierungsausnahmen sauber nach Vor-/Nachmaßnahmen, Informationslage und konkreter Berechnung trennen; umfassende Modernisierung nicht pauschal unterstellen. | https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&nr=140073 |
| Steckersolargeräte Miete | § 554 BGB | Mieter können eine bauliche Veränderung für Steckersolargeräte verlangen; Interessenabwägung, Zumutbarkeit, technische Sicherheit und Rückbau dokumentieren. | https://www.gesetze-im-internet.de/bgb/__554.html |
| Steckersolargeräte WEG | § 20 Abs. 2 WEG | Wohnungseigentümer haben einen Anspruch auf angemessene bauliche Veränderungen u. a. für Steckersolargeräte; Ausführung bleibt ordnungsmäßig zu beschließen. | https://www.gesetze-im-internet.de/woeigg/__20.html |
| Virtuelle Eigentümerversammlung | § 23 Abs. 1a WEG; § 48 Abs. 6 WEG | Rein virtuelle Versammlung nur aufgrund Beschlusses mit qualifizierter Mehrheit und befristeter Wirkung; bis Ende 2028 Übergangsrecht mit Präsenzversammlung beachten. | https://www.gesetze-im-internet.de/woeigg/__23.html / https://www.gesetze-im-internet.de/woeigg/__48.html |
| Verwalterabberufung | § 26 Abs. 3 WEG | Verwalter kann jederzeit abberufen werden; der Verwaltervertrag endet spätestens sechs Monate nach Abberufung. "Nur bei wichtigem Grund" ist seit WEMoG falsch. | https://www.gesetze-im-internet.de/woeigg/__26.html |
| WEG bauliche Veränderung | BGH, Urteil vom 28.03.2025, V ZR 105/24 | Bei baulichen Veränderungen § 20 WEG und Kostenfolge § 21 WEG getrennt prüfen; § 20 Abs. 4 WEG bleibt Grenze bei grundlegender Umgestaltung/unbilliger Benachteiligung. | https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&nr=141815 |
| WEG Störerhaftung bei Mietern | BGH, Urteil vom 21.03.2025, V ZR 1/24 | Vermietende Wohnungseigentümer können gegenüber der Gemeinschaft als mittelbare Handlungsstörer haften, wenn ihr Mieter unzulässig in Gemeinschaftseigentum eingreift. | https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/document.py?Gericht=bgh&nr=141725 |

## Workflow-Gate

1. **Rolle klären:** Mieter, Vermieter, WEG-Eigentümer, Gemeinschaft, Verwalter, Beirat.
2. **Objekt klären:** Wohnraum, Gewerbe, Mischmiete, Wohnungseigentum, Sonder-/Gemeinschaftseigentum.
3. **Eilfristen zuerst:** Kündigung, Räumung, Mieterhöhung, WEG-Beschlussklage (§ 45 WEG: Klage 1 Monat, Begründung 2 Monate), Betriebskostenfrist.
4. **Quelle auswählen:** Mietspiegel/Landesverordnung, BGB, WEG, BetrKV, BGH/Amts-/Landgericht nur wenn frei geprüft.
5. **Output anschließen:** `mieterhoehung-pruefen-widersprechen`, `mietsenkungsverlangen`, `nebenkostenabrechnung-pruefen`, `mahnung-zahlungsverzug-mieter`, `weg-beschluss-anfechten`, `klageentwurf-amtsgericht`.

## Kurzkorrekturen für bestehende Workflows

- WEG-Sachen nach §§ 43 ff. WEG gehen erstinstanzlich grundsätzlich zum Amtsgericht der Belegenheit; nicht nach allgemeiner Streitwertlogik zum Landgericht springen.
- Bauliche Veränderungen: Beschluss/Anspruch, ordnungsmäßige Ausführung, Grenzen des § 20 Abs. 4 WEG und Kostenverteilung § 21 WEG getrennt prüfen.
- Schonfristzahlung heilt die fristlose Kündigung wegen Zahlungsverzugs, nicht automatisch eine hilfsweise ordentliche Kündigung; konkrete BGH-Linie live verifizieren.
- Mietpreisbremse nie ohne lokale Landesverordnung, Mietspiegel und Ausnahmen prüfen.
