---
name: qa-db
description: Generate and manage Q&A database for Topical Authority content. Use when user wants to create structured answers for cluster questions or export JSON-LD for GEO.
---

# Q&A Database Generator

Erstelle strukturierte Antworten für Fragen aus der Topical Map.

## Commands

| Command | Description |
|---------|-------------|
| `/qa-db:generate` | Antworten für Cluster-Fragen generieren |
| `/qa-db:export` | JSON-LD Schema.org Markup exportieren |

## Data Location

- `data/qa-database/{cluster-id}.json` - Antworten pro Cluster
- `data/qa-database/answer-formats.md` - Format-Spezifikation
- `data/qa-database/schema.json` - JSON Schema

## Answer Formats

8 standardisierte Formate für strukturierte Antworten:

| Format | Verwendung | Beispiel-Frage |
|--------|------------|----------------|
| BOOL | Ja/Nein-Fragen | "Ist Zeiterfassung Pflicht?" |
| SHORT_FACT | Kurze Fakten | "Ab wann gilt die Pflicht?" |
| DEFINITION | Was ist...? | "Was ist ein Zeiterfassungssystem?" |
| INSTRUCTION | Wie macht man...? | "Wie führe ich Zeiterfassung ein?" |
| REASON | Warum...? | "Warum ist Zeiterfassung wichtig?" |
| CONSEQUENCE | Was passiert wenn...? | "Was passiert ohne Zeiterfassung?" |
| COMPARISON | X oder Y? | "App oder Terminal?" |
| OTHER | Komplexe Fragen | Trends, Meinungen, Perspektiven |

Details zu jedem Format siehe `data/qa-database/answer-formats.md`.

## Quick Start

1. **Cluster auswählen:** `/qa-db:generate kleinbetriebe`
2. **Antworten reviewen:** Prüfe `data/qa-database/kleinbetriebe.json`
3. **JSON-LD exportieren:** `/qa-db:export kleinbetriebe`

## Integration mit Topical Map

Liest Fragen aus `data/topical-authority/topical-map.json` (Cluster → questions Array).

## Workflow

```
Topical Map (Fragen)
  → Q&A-Datenbank (strukturierte Antworten)
    → JSON-LD Export (für LLMs/GEO)
    → Content-Erstellung (Artikel basieren auf Q&A)
```

## Qualitätskriterien

- **Faktisch korrekt:** Aktuelle Rechtslage, keine veralteten Infos
- **EEAT:** Quellenangaben bei Fakten (Gesetze, Urteile, Studien)
- **Format-konform:** Antwort folgt dem gewählten Format exakt
- **Prägnant:** 2-4 Sätze Hauptantwort (5 bei COMPARISON)
- **Verständlich:** Für Laien lesbar, kein Fachjargon ohne Erklärung
