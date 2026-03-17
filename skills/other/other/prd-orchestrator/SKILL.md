---
name: prd-orchestrator
description: Orchestrate a one-line requirement or requirement document into a full PRD set, sub-PRDs, per-PRD plans, and an execution runner for codex exec. Use when the user invokes $prd-orchestrator to turn requirements into ordered, executable PRDs and plans.
---

# PRD Orchestrator

## Overview
Turn a one-line requirement or requirement document/path into a complete, ordered PRD and Plan bundle that can be executed by codex exec. This skill produces mother PRD, verify tooling PRD, ordered sub-PRDs, per-PRD plans, a runner script, and reporting schema.

## How to invoke
- $prd-orchestrator <one-line requirement>
- $prd-orchestrator <full requirement text>
- $prd-orchestrator <path/to/requirements.md>

## Working agreements / Rules
- Always follow the merged instruction chain from AGENTS and rules.
- Global layer (in priority order):
  - $CODEX_HOME/AGENTS.override.md (if exists and non-empty), else $CODEX_HOME/AGENTS.md
  - $CODEX_HOME/rules/**
- Project layer (current repo tree):
  - <repo>/AGENTS.override.md or <repo>/AGENTS.md
  - Any nested AGENTS.override.md or AGENTS.md in subdirectories
  - <repo>/rules/** and any nested rules/ directories
- Conflict resolution: more specific scope overrides more general (subdir > repo > global).
- If rules restrict command execution (prompt/allow/forbidden), obey strictly.

## Inputs
- A single sentence requirement, or
- A requirement document text or file path.

## Outputs (must exist in project root)
- prds/0-<product-slug>-mother.md
- prds/1-verify-tooling.md
- prds/2-<slug>.md ... prds/n-<slug>.md
- plans/1-verify-tooling.md
- plans/2-<slug>.md ... plans/n-<slug>.md
- docs/ASSUMPTIONS.md (create if missing)
- PROGRESS.md (create if missing)
- schemas/milestone_report.schema.json (create if missing)
- scripts/implement_prds.sh
- output/reports/*.json (runner output)

## Output stability and idempotency
- Use stable, sortable filenames with numeric prefixes and slugs.
- Create missing directories/files; update existing content without deleting user data.
- Never remove user content unless explicitly instructed.

## Workflow (strict order)

### 0) Repo probe and rule load
- Run repo probe (rg --files or ls).
- Load project profile if present (.codex/project.profile.md).
- Load relevant rules per AGENTS router.

### 1) Intake and minimal questions
- Ask only blocking questions that affect direction or feasibility.
- Anything else becomes an explicit assumption recorded in docs/ASSUMPTIONS.md.

Checklist (max 1 pass):
- [ ] User intent and target outcomes are clear enough to proceed.
- [ ] Blocking unknowns asked (max 1-2 questions).
- [ ] Non-blocking unknowns converted into assumptions.

### 2) Research (if web search tools are available and allowed)
- If web search is available and allowed by rules, produce:
  - At least 3 competitors or similar projects.
  - A comparison table (features, interaction patterns, UX, pricing/positioning if relevant).
  - Borrowed ideas and deliberate trade-offs.
- If web search is not available:
  - Mark competitive analysis as pending.
  - List 5 most important references the user should provide.

Checklist (max 1 pass):
- [ ] Competitive analysis present or marked pending with 5 reference asks.

### 3) Create mother PRD (prds/0-*-mother.md)
- Use references/mother_prd_template.md.
- Fill every section; use N/A if not applicable.
- Include default tech stack and constraints even if provisional.
- If iteration exceeds 3 passes, add a top banner with Open Questions and Assumptions.

Checklist (max 3 iterations):
- [ ] All required sections completed.
- [ ] Competitive analysis present or explicitly pending.
- [ ] Default tech stack and constraints filled.
- [ ] Risks and mitigations defined.

### 4) Create verify tooling PRD (prds/1-verify-tooling.md)
- Use references/verify_prd_template.md.
- Must define make verify and minimal lint/test/ci skeleton.
- Ensure acceptance criteria prove make verify passes on minimal scaffold.
 - If iteration exceeds 2 passes, add a top banner with Open Questions and Assumptions.

Checklist (max 2 iterations):
- [ ] make verify defined and testable.
- [ ] Lint/format/test/ci skeleton included.
- [ ] Acceptance criteria include local reproduction steps.

### 5) Create ordered sub-PRDs (prds/2..n)
- Use references/sub_prd_template.md for each.
- Must be strictly ordered and non-blocking (n+1 depends only on <= n).
- Each sub-PRD must include acceptance criteria and verification steps (must include make verify).
 - If iteration exceeds 2 passes, add a top banner with Open Questions and Assumptions.

Checklist (max 2 iterations):
- [ ] Each sub-PRD is independently implementable in order.
- [ ] Each has >=5 acceptance criteria with negative cases.
- [ ] Dependencies only point to earlier PRDs.

### 6) Create per-PRD plans (plans/1..n)
- Use references/plan_template.md for each.
- Plans must be executable, ordered, and include commands and key files.
 - If iteration exceeds 2 passes, add Open Questions and Assumptions at the top.

Checklist (max 2 iterations):
- [ ] Steps are ordered and concrete (files/dirs/commands).
- [ ] Self-test and review checklist present.
- [ ] Verification commands include make verify.

### 7) Create assumptions, progress, schema, and runner
- Create docs/ASSUMPTIONS.md from references/assumptions_template.md if missing.
- Create PROGRESS.md from references/progress_template.md if missing.
- Create schemas/milestone_report.schema.json from references/milestone_report_schema_template.json if missing.
- Create scripts/implement_prds.sh (see Runner Script Spec below).

Checklist (max 1 pass):
- [ ] All required files created or updated without deleting user content.
- [ ] Runner script uses sort -V and skips mother PRD.

## Runner Script Spec (scripts/implement_prds.sh)
- Bash script with: set -euo pipefail
- Create directories: output/reports, schemas, docs, prds, plans
- PRD list:
  - find prds -maxdepth 1 -type f -name '[1-9]*-*.md' | sort -V
- For each PRD, call:
  codex exec --full-auto --output-schema ./schemas/milestone_report.schema.json \\
    -o "output/reports/<prd_basename>.json" \\
    "<strict prompt>"
- Strict prompt must include:
  - Read <prd>
  - Implement exactly what it requires
  - If you make ANY assumption: update docs/ASSUMPTIONS.md
  - Update PROGRESS.md with PASS/FAIL and evidence + link to output/reports/<prd_basename>.json
  - Run: make verify
  - If make verify fails: fix until it passes
  - Do not move to next PRD until DONE
- After each PRD:
  - git add -A
  - git commit -m "Implement <prd_basename>" || true
- End with a summary message pointing to output/reports and PROGRESS.md

## Assumptions and open questions
- Only ask when blocked or directionally uncertain.
- All other unknowns go to docs/ASSUMPTIONS.md with required fields:
  - Assumption, Reason, Impact, To confirm, Date

## Mandatory skill mapping (call when needed, then merge output)
- Backend API or service architecture: use $backend-development
- Database schema/migrations/indexes: use $database-design
- Frontend IA/UX/layout/visuals: use $frontend-design
- Testing strategy or local/E2E testing: use $webapp-testing
- Plan generation: optionally use $create-plan, but merge into plan_template format
- Code review (runner phase): optionally use $code-review and merge into PRD/Plan
- If a required skill is unavailable, proceed and mark "Skill unavailable" in the affected section.

## References (load only as needed)
- references/mother_prd_template.md
- references/verify_prd_template.md
- references/sub_prd_template.md
- references/plan_template.md
- references/progress_template.md
- references/assumptions_template.md
- references/milestone_report_schema_template.json
