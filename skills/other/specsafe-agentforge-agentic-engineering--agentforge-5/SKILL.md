---
name: specsafe-agentforge
description: Repository-specific SpecSafe workflow for AgentForge. Use when creating, refining, testing, implementing, or reviewing AgentForge specs so work follows the documented SpecSafe stages, prompt files, and source-of-truth rules consistently.
---

# SpecSafe for AgentForge

Use this skill for any meaningful feature work in AgentForge. It is the single entry point for the full SpecSafe lifecycle.

---

## Step 1 — Retrieve Project Context

Read these files in order before taking any action:

| # | File | Why |
|---|------|-----|
| 1 | `AGENTS.md` | agent config, runtime constraints |
| 2 | `PROJECT_STATE.md` | canonical active spec and stage |
| 3 | `docs/SPECSAFE_WORKFLOW.md` | full stage definitions and stage commands |
| 4 | `docs/PRE_SPEC_CHECKLIST.md` | required checks before opening a new spec |
| 5 | `docs/SOURCE_OF_TRUTH.md` | authoritative external doc URLs (Mastra, Convex, LibSQL, Drizzle) |
| 6 | `docs/SKILLS.md` | available skills and when to use them |
| 7 | `docs/AI_OPERATIONS.md` | agent operating rules and tool restrictions |
| 8 | active spec in `specs/active/` | requirements, scope, and `## 6.5 Current Focus` |

Then run:

```
pnpm spec:status
```

From this, determine:
- the active spec ID
- the current stage (`SPEC`, `TEST`, `CODE`, `QA`, `COMPLETE`, `ARCHIVED`)
- the exact next step from `## 6.5 Current Focus` in the active spec, if present
- whether `PROJECT_STATE.md` and the spec header agree — fix or flag any mismatch

---

## Step 2 — Choose the Right Stage

Use this index to find the prompt file and sub-skill for the current work:

| Stage | When to Use | Prompt Files | Sub-Skill |
|-------|-------------|--------------|-----------|
| session start | start of any session | — | `agentforge-session-start` |
| SPEC | creating or refining a spec | `prompts/planner.md`, `prompts/spec-writer.md` | `specsafe-spec-start` |
| TEST | writing tests from the spec | `prompts/test-designer.md` | `specsafe-test-create` |
| CODE | implementing the slice | `prompts/implementer.md` | `specsafe-implement` |
| QA / REVIEW | reviewing and verifying | `prompts/reviewer.md`, `prompts/security-reviewer.md` | `specsafe-review` |
| COMPLETE | completing and archiving | `prompts/reviewer.md`, `prompts/docs-curator.md` | `specsafe-complete` |

Load the prompt file for the active stage before doing work. The sub-skill provides detailed step-by-step instructions for that stage.

---

## Step 3 — Move Through Stages in Order

```
SPEC → TEST → CODE → QA → COMPLETE → ARCHIVED
```

Stage advancement commands:

```
pnpm spec:stage <SPEC-ID> <STAGE>   # advance a spec to the next stage
pnpm spec:sync                      # sync PROJECT_STATE.md from spec files
pnpm spec:status                    # verify current state after any stage change
```

Do not skip stages. Update the spec file header and `PROJECT_STATE.md` before ending the session after any stage change.

---

## Rules

- One active implementation spec at a time. Do not open overlapping implementation specs without explicit ownership.
- Do not write production code without a spec.
- Keep the current slice narrow. Be explicit about out-of-scope items.
- Verify Mastra and Convex behavior against official docs (see `docs/SOURCE_OF_TRUTH.md`) before implementation.
- Do not use upstream `specsafe status`, `specsafe list`, `specsafe qa`, or `specsafe done` as authoritative lifecycle operations in this repo. Use `pnpm spec:*` commands instead.
- If the active spec has no `## 6.5 Current Focus`, call that out before starting implementation.
- If documentation or status files were not read, stop and read them before continuing.
