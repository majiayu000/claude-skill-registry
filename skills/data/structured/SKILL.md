---
name: structured
description: "Strukturierte Analyse in 3 Schritten. Run '/structured', 'strukturiert analysieren', oder 'constraint cascade'."
---

# Structured Skill (Constraint Cascade)

Strukturierte Analyse in drei klaren Schritten: Fakten sammeln, verdichten, entscheiden. Basiert auf Anthropic's "Constraint Cascade" Best Practice.

## Wann ausfuehren

- Bei komplexen Analyseaufgaben
- Wenn User sagt "structured", "strukturiert analysieren", oder "/structured"
- Bei Entscheidungen die auf Daten basieren sollen
- Wenn Uebersicht ueber ein Thema noetig ist

## Workflow

### Phase 1: Analyse (Fakten sammeln)

**Ziel:** Alle relevanten Informationen zusammentragen

```
## Phase 1: Analyse

### Fakten
- [Fakt 1]: [Quelle/Beleg]
- [Fakt 2]: [Quelle/Beleg]
- [Fakt 3]: [Quelle/Beleg]
...

### Daten
| Metrik | Wert | Zeitraum |
|--------|------|----------|
| [Metrik 1] | [Wert] | [Zeitraum] |
| [Metrik 2] | [Wert] | [Zeitraum] |

### Kontext
- [Relevanter Kontext 1]
- [Relevanter Kontext 2]

### Offene Fragen
- [Frage die noch geklaert werden muss]
```

**Methoden:**
- Codebase durchsuchen (Grep, Glob, Read)
- Web-Recherche wenn noetig (WebSearch)
- Bestehende Dokumentation lesen
- User nach fehlenden Infos fragen

### Phase 2: Zusammenfassung (Verdichten)

**Ziel:** Die wichtigsten Erkenntnisse destillieren

```
## Phase 2: Zusammenfassung

### Kernerkenntnisse
1. **[Erkenntnis 1]:** [Ein Satz Erklaerung]
2. **[Erkenntnis 2]:** [Ein Satz Erklaerung]
3. **[Erkenntnis 3]:** [Ein Satz Erklaerung]

### Muster & Trends
- [Muster 1]
- [Trend 1]

### Risiken
| Risiko | Wahrscheinlichkeit | Impact |
|--------|-------------------|--------|
| [Risiko 1] | Hoch/Mittel/Niedrig | Hoch/Mittel/Niedrig |
| [Risiko 2] | ... | ... |

### Chancen
- [Chance 1]
- [Chance 2]
```

**Regeln:**
- Maximal 5 Kernerkenntnisse
- Jede Erkenntnis in einem Satz
- Priorisieren, nicht alles auflisten

### Phase 3: Entscheidung (Handlungsempfehlung)

**Ziel:** Konkrete, umsetzbare Empfehlung

```
## Phase 3: Entscheidung

### Empfehlung
**[Klare Empfehlung in einem Satz]**

### Begruendung
[2-3 Saetze warum diese Empfehlung]

### Aktionsplan
| Schritt | Aktion | Verantwortlich | Deadline |
|---------|--------|----------------|----------|
| 1 | [Aktion] | [Wer] | [Wann] |
| 2 | [Aktion] | [Wer] | [Wann] |
| 3 | [Aktion] | [Wer] | [Wann] |

### Erfolgskriterien
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]
- [ ] [Kriterium 3]

### Alternative (falls Empfehlung nicht moeglich)
[Plan B in einem Satz]
```

## Beispiel-Ablauf

### User Request
"Analysiere ob wir auf Astro 5 upgraden sollten"

### Phase 1: Analyse

**Fakten:**
- Aktuelle Version: Astro 4.x (package.json)
- Astro 5 released: Dezember 2024
- Breaking Changes: Content Collections API geaendert
- Migration Guide verfuegbar: ja

**Daten:**
| Metrik | Wert | Quelle |
|--------|------|--------|
| Breaking Changes | 3 major | Astro Docs |
| Migration Aufwand | ~2-4h | Erfahrungswerte |
| Performance Verbesserung | ~15% | Benchmarks |

**Kontext:**
- Projekt nutzt Content Collections intensiv
- Keine kritischen Features in Astro 5 noetig
- Team hat Kapazitaet naechste Woche

### Phase 2: Zusammenfassung

**Kernerkenntnisse:**
1. **Upgrade ist machbar:** Migration Guide ist gut dokumentiert
2. **Aufwand ueberschaubar:** ~2-4 Stunden fuer dieses Projekt
3. **Kein Druck:** Aktuelle Version funktioniert, keine Security Issues

**Risiken:**
| Risiko | Wahrscheinlichkeit | Impact |
|--------|-------------------|--------|
| Unerwartete Bugs | Niedrig | Mittel |
| Plugin-Inkompatibilitaet | Mittel | Niedrig |

**Chancen:**
- Bessere Performance
- Zukunftssicherheit
- Neue Features nutzbar

### Phase 3: Entscheidung

**Empfehlung:**
**Upgrade auf Astro 5 in der naechsten ruhigen Woche durchfuehren**

**Begruendung:**
Der Aufwand ist gering, das Risiko niedrig, und laenger warten macht die Migration nur komplizierter. Keine dringenden Features blockieren das Upgrade.

**Aktionsplan:**
| Schritt | Aktion | Verantwortlich | Deadline |
|---------|--------|----------------|----------|
| 1 | Branch erstellen | Dev | Tag 1 |
| 2 | Dependencies updaten | Dev | Tag 1 |
| 3 | Content Collections migrieren | Dev | Tag 1 |
| 4 | Testen | QA | Tag 2 |
| 5 | Merge & Deploy | Dev | Tag 2 |

**Erfolgskriterien:**
- [ ] Alle Seiten rendern korrekt
- [ ] Keine Console Errors
- [ ] Build Zeit <= vorher
- [ ] Lighthouse Score >= vorher

**Alternative:**
Bei Problemen: Auf Astro 4.x bleiben bis 5.1 erscheint.

## Wichtige Regeln

- **ALLE 3 Phasen** durchlaufen (nicht abkuerzen)
- **Phase 1** ist die laengste - gruendlich recherchieren
- **Phase 2** ist die kuerzeste - nur das Wichtigste
- **Phase 3** MUSS eine klare Empfehlung haben
- **NIEMALS** "es kommt drauf an" als Empfehlung

## Wann verkuerzen

Bei einfachen Fragen kann Phase 1 kuerzer sein:
- Wenige Fakten noetig
- Kontext ist klar
- Keine Recherche noetig

Aber: **Immer alle 3 Phasen durchlaufen**

## Typische Nutzung

User: `/structured Welches Testing Framework sollten wir nutzen?`

Response:
1. **Analyse:** Optionen recherchieren, Anforderungen sammeln
2. **Zusammenfassung:** Top 3 Optionen mit Vor/Nachteilen
3. **Entscheidung:** Konkrete Empfehlung mit Aktionsplan
