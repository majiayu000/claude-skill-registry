---
name: codex-skills-index
description: Entry point for Codex-discoverable skills used by the Run-Smart AI coach.
metadata:
  short-description: Catalog of AI skills, contracts, telemetry, and guardrails for Run-Smart.
---

## Purpose
Defines the shared conventions, contracts, safety posture, and telemetry used by all Run-Smart AI skills. This index allows Codex to discover available skills and the rules they follow.

## When Codex should use it
- Before invoking any Run-Smart skill to understand shared schemas, safety guidance, and telemetry.
- When onboarding a new skill to ensure compliance with common contracts.

## Invocation guidance
1. Load shared references in `_index/references/` (contracts, telemetry, conventions, smoke-tests).
2. Select the appropriate skill directory based on the user’s need (plan generation, adjustment, insights, etc.).
3. Validate request/response payloads against the schemas in `contracts.md` and skill-specific schemas.

## Shared components
- **Contracts:** `_index/references/contracts.md`
- **Telemetry:** `_index/references/telemetry.md`
- **Conventions:** `_index/references/conventions.md`
- **Smoke tests:** `_index/references/smoke-tests.md`

## Safety & guardrails
- No medical diagnosis. If pain/dizziness/severe symptoms appear, advise stopping activity and consulting a qualified professional.
- Prefer conservative adjustments under uncertainty.
- Emit `SafetyFlag` objects when thresholds are crossed and log via `ai_safety_flag_raised`.

## Integration points
- Skills are invoked from chat flows (`v0/app/api/chat/route.ts`, `v0/lib/enhanced-ai-coach.ts`), plan generation APIs (`v0/app/api/generate-plan/route.ts`), background jobs (plan adjustment), and post-run screens.

## Telemetry events (standard)
- `ai_skill_invoked`
- `ai_plan_generated`
- `ai_adjustment_applied`
- `ai_insight_created`
- `ai_safety_flag_raised`
- `ai_user_feedback`
