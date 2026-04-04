---
name: vkc-visa-assessment-engine
description: Design and implement the Viet K-Connect visa assessment engine (DB-driven ruleset JSON schema + versioning + effective dates). No hardcoded rules in code. Use for building /api/visa/assess and admin ruleset management. (키워드= 비자 평가, 룰셋, 규칙 엔진, DB-driven, 버전/적용일, /api/visa/assess)
metadata:
  short-description: Visa assessment engine (DB-driven)
---

# VKC Visa Assessment Engine (P1)

## Goal

Provide “비자변경 가능성(%)” outputs at scale (cover target-customer visas) while keeping maintenance **data-driven**:

- rules/weights live in DB (versioned + effective dates)
- code is a stable evaluator + storage + admin activation workflow

## Non‑negotiable

- **No hardcoding rules** in TypeScript. Rules belong to DB rows as JSON.

## Core data model (minimum)

- `visa_catalog`: visa codes / labels / categories
- `visa_transition_rules`: `fromVisa`→`toVisa` ruleset JSON + `version` + `effectiveFrom` + `status(pending|active)`
- `visa_assessment_models`: score→percent mapping / weights JSON + version + status
- `visa_assessments`: user assessment history (`probabilityPercent`, `grade`, `missing`, `risks`, `createdAt`)

## Required interfaces

- Ruleset JSON schema (validate before activation)
  - `.codex/skills/vkc-visa-assessment-engine/references/ruleset-schema.json`
- API response schema (persist + return)
  - `.codex/skills/vkc-visa-assessment-engine/references/response-schema.json`

## API + admin workflow (recommended)

- User:
  - `POST /api/visa/assess` (auth + 1/day + save `visa_assessments`)
- Admin:
  - Manage `visa_catalog`
  - Create/update `visa_transition_rules` (pending)
  - Activate a ruleset version (switch to active)
  - Manage `visa_assessment_models` version and activation

## STEP3 visa registry (SoT)

- “전체 커버” visa code registry lives in: `docs/STEP3_SOT_RESOURCES.md`
- Implementation rule: registry is complete first → rulesets are filled in iteratively (v1→vN)
