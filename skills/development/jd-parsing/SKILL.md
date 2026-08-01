---
name: jd-parsing
description: 'description: Pflege das Parsing von Job Descriptions (JD); verwenden
  bei neuen Feldern, Headern oder Parsing-Regeln.'
---

﻿---
name: jd-parsing
description: Pflege das Parsing von Job Descriptions (JD); verwenden bei neuen Feldern, Headern oder Parsing-Regeln.
---

# Skill: jd-parsing

## Zweck
Extrahiere strukturierte Anforderungen aus Job Descriptions fuer Matching und Analyse.

## Wann anwenden
- Wenn neue JD-Felder benoetigt werden.
- Wenn DE/EN-Header oder Parsing-Regeln erweitert werden.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-006 und bestehende Tests.
2) Aktualisiere `src/core/jd_parser.py`.
3) Passe Tests in `tests/unit/test_jd_parser.py` an.
4) Pruefe, dass fehlende Felder sauber behandelt werden.

## Lernperspektive
- Warum so? Regelbasierte Parsing-Logik ist nachvollziehbar und testbar.
- Alternativen: ML-basierte Klassifikation oder externe Parser.
- Warum nicht hier? Reduziert Explainability und erhoeht Abhaengigkeiten.

## Repo-Referenzen
- `src/core/jd_parser.py`
- `tests/unit/test_jd_parser.py`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Ausgabe deckt definierte JD-Felder ab.
- Tests enthalten DE/EN Beispiele.
- Parsing faellt kontrolliert bei fehlenden Inputs.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | JD-Parsing (DE/EN) implementieren | erledigt |