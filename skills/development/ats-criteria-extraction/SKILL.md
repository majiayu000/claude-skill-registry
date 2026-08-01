---
name: ats-criteria-extraction
description: 'name: ats-criteria-extraction'
---

﻿---
name: ats-criteria-extraction
description: Pflege die Extraktion von ATS-Kriterien aus CVs; verwenden bei Anpassungen an Kontakt-, Erfahrung- oder Bildungsextraktion.
---

# Skill: ats-criteria-extraction

## Zweck
Extrahiere recruiter-relevante Kriterien nachvollziehbar aus CV-Text.

## Wann anwenden
- Wenn Felder oder Regeln fuer ATS-Kriterien angepasst werden.
- Wenn neue Extraktionsfelder hinzugefuegt werden.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-005 und bestehende Tests.
2) Aktualisiere `src/core/ats_criteria_extractor.py`.
3) Passe Tests in `tests/unit/test_ats_criteria.py` an.
4) Stelle sicher, dass fehlende Felder als "not found" markiert werden.

## Lernperspektive
- Warum so? Regelbasierte Kriterien sind erklaerbar und nachvollziehbar.
- Alternativen: LLM-Extraktion oder ML-Modelle.
- Warum nicht hier? Black-Box-Extraktion ist schwer auditierbar und passt nicht zur Case-Study-Ausrichtung.

## Repo-Referenzen
- `src/core/ats_criteria_extractor.py`
- `tests/unit/test_ats_criteria.py`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Alle Pflichtfelder werden extrahiert oder als fehlend markiert.
- Tests decken DE/EN Beispiele ab.
- Keine Exceptions bei unvollstaendigen CVs.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | ATS-Kriterien aus CV extrahieren | erledigt |