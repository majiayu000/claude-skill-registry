---
name: specsafe-spec
description: Generate detailed spec from PRD
argument-hint: "[spec-id]"
disable-model-invocation: true
---

Convert PRD to comprehensive specification:
- Read PRD from specs/drafts/SPEC-ID.md
- Create functional requirements (FR-XXX)
- Create technical requirements (TR-XXX)
- Define scenarios (Given/When/Then)
- Write acceptance criteria
- Add architecture notes

Move to specs/active/SPEC-ID.md and update PROJECT_STATE.md (DRAFT → SPEC).
