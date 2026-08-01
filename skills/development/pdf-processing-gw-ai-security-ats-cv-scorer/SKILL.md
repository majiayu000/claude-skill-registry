---
name: pdf-processing-gw-ai-security-ats-cv-scorer
description: 'description: Implementiere oder aendere PDF-Upload-Validierung und Textextraktion;
  verwenden bei Anpassungen an Upload-Regeln, Parsing oder Fehlerbehandlung.'
---

﻿---
name: pdf-processing
description: Implementiere oder aendere PDF-Upload-Validierung und Textextraktion; verwenden bei Anpassungen an Upload-Regeln, Parsing oder Fehlerbehandlung.
---

# Skill: pdf-processing

## Zweck
Stelle eine deterministische, robuste PDF-Validierung und Textextraktion sicher.

## Wann anwenden
- Wenn Upload-Regeln (Typ/Size) geaendert werden.
- Wenn die Extraktion verbessert oder Fehlerbehandlung erweitert wird.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-001/FR-002 und die Traceability.
2) Aktualisiere `src/utils/validation.py` oder `src/core/pdf_processor.py`.
3) Passe Tests in `tests/integration/` und `tests/unit/` an.
4) Pruefe, dass deterministisches Verhalten und Fehlerpfade getestet sind.

## Lernperspektive
- Warum so? Determinismus und klare Fehlerpfade sind zentral fuer Nachvollziehbarkeit.
- Alternativen: OCR oder externe Parsing-APIs.
- Warum nicht hier? Externe Abhaengigkeiten und OCR stehen explizit nicht im Scope (FR-002).

## Repo-Referenzen
- `src/utils/validation.py`
- `src/core/pdf_processor.py`
- `tests/unit/test_pdf_processor.py`
- `tests/integration/test_upload_validation.py`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Upload-Validierung entspricht FR-001.
- Extraktion ist deterministisch und testbar.
- Fehlerbehandlung liefert klare Rueckgaben, kein Crash.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | PDF-Upload-Validierung und Textextraktion umsetzen | erledigt |