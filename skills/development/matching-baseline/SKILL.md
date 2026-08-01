---
name: matching-baseline
description: 'name: matching-baseline'
---

﻿---
name: matching-baseline
description: Pflege das regelbasierte CV<->JD Matching inkl. Explainability; verwenden bei Anpassung der Scoring-Logik, Gewichtung oder Match-Outputs.
---

# Skill: matching-baseline

## Zweck
Liefere nachvollziehbares, deterministisches Matching zwischen CV und JD.

## Wann anwenden
- Wenn Scoring-Regeln, Gewichtungen oder Match-Ausgaben angepasst werden.
- Wenn Explainability erweitert werden soll.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-007 und ADR-002.
2) Aktualisiere `src/core/matcher.py`.
3) Passe Tests in `tests/unit/test_matcher.py` an.
4) Pruefe, dass Match-Ergebnisse Gap/Match pro Kriterium enthalten.

## Lernperspektive
- Warum so? Regelbasiertes Matching ermoeglicht transparente Erklaerungen.
- Alternativen: ML-Matching (ADR-002 Plan).
- Warum nicht hier? ML ist erst nach stabiler Baseline geplant und erhoeht Komplexitaet.

## Repo-Referenzen
- `src/core/matcher.py`
- `tests/unit/test_matcher.py`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Matching ist deterministisch.
- Breakdown erklaert Score nachvollziehbar.
- Tests decken typische und fehlende Felder ab.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | Baseline Matching mit Explainability implementieren | erledigt |