---
name: verify-plan-coverage
description: >
  Use when validating that an implementation plan covers all requirements from a spec
  or architecture doc. Use after writing-plans completes, before plan execution.
  Use when concerned about silent requirement drops, value mutations, or missing edge cases.
allowed-tools: Read, Glob, Grep, AskUserQuestion
user-invocable: true
---

# Verify Plan Coverage

Cross-reference a spec and architecture doc against an implementation plan. Catch silent requirement drops, value mutations, and orphan tasks.

**Core principle:** Plans drop ~14% of requirements silently. This skill makes every gap visible and actionable.

## When to Use

- After `writing-plans` or `dotnet-writing-plans` or `react-writing-plans` completes
- Before executing a plan with `subagent-driven-development`
- When reviewing any plan against its source spec/architecture
- `/verify-plan-coverage` with optional path arguments

## Inputs

Resolve source documents. Check these locations in order:

1. **User-provided paths** in `$ARGUMENTS` (if any)
2. **Spec:** `_docs/specs/{DATE}-{feature}.md`
3. **Architecture:** `_docs/specs/{DATE}-{feature}-architecture.md`
4. **Plan(s):** `_docs/plans/{DATE}-*.md` or `MANIFEST.json` listing plan files

If ambiguous or multiple candidates → use AskUserQuestion to confirm which files.

If `MANIFEST.json` exists, read it and process ALL plan files listed. A requirement covered by ANY plan counts as covered. Track which plan file covers each requirement.

## Algorithm

Execute these phases IN ORDER. Do not skip phases. Do not summarize — check EVERY item.

### Phase 1: Extract Requirements from Spec

Read the spec. Extract and assign IDs to EVERY item:

- **S1..Sn:** Each numbered "In Scope" item. Copy FULL text including all numbers, thresholds, limits, error codes.
- **UF1..UFn:** Each User Flow step that implies a system behavior.

Spec entities (Upload, UploadError, etc.) are checked via their **architecture** counterparts (E1..En) in Phase 5. Do NOT create a separate ENT category — entities are architecture contracts.

**CRITICAL: Copy exact values.** "up to 10MB" means 10MB. "HTTP 413" means 413. "3 times with exponential backoff (1s, 2s, 4s)" means exactly those numbers. You will compare these character-by-character later.

### Phase 2: Extract Contracts from Architecture

Read the architecture doc. Extract and assign IDs:

- **EP1..EPn:** Each API endpoint — method + path + request/response types + status code.
- **E1..En:** Each entity with classification and ALL listed behaviors.
- **C1..Cn:** Each component from Component Tree.

### Phase 3: Extract Plan Coverage

For EACH `### Task N:` in the plan:

1. Parse `**Implements:**` field → note what it claims to implement
2. Parse `**Behaviors:**` → list EVERY behavior with specific values
3. Parse `**Files:**` → file paths

**Infrastructure tasks:** If `Implements:` contains "N/A" or "infrastructure", mark as exempt from orphan checking.

### Phase 4: Forward Check (Completeness) — Spec → Plan

For EACH spec requirement (S1..Sn), user flow (UF1..UFn):

**Search for implementing task(s).** Look at EVERY task's `Implements:` AND `Behaviors:` fields.

**Classify using ONLY these categories:**

- **COVERED:** A task explicitly implements this requirement AND its behaviors match the spec values exactly.
- **PARTIAL:** A task touches this area but doesn't fully cover it. Examples: validates size but not format; renders a component but no dedicated task for it.
- **MISSING:** No task addresses this requirement at all.
- **MUTATED:** A task implements this requirement BUT a specific value differs from the spec.

**CRITICAL — Anti-Hallucination Rules:**

These rules exist because baseline testing showed agents hallucinate coverage. Every rule below addresses a documented failure mode.

1. **A task implementing POST /uploads does NOT automatically cover GET /uploads/{id} or DELETE /uploads/{id}.** Each endpoint is a separate contract. Check method + path EXACTLY.
2. **A behavior mentioning a component name does NOT mean that component is fully covered.** "Renders UploadForm component" in Task 4 means UploadForm is PARTIAL (referenced, no dedicated task), not COVERED.
3. **An entity behavior on one aggregate does NOT cover a different entity.** "MarkFailed increments retry count" on Upload does NOT mean UploadError entity is covered.
4. **"Implied" coverage is NOT coverage.** If you catch yourself writing "implied by" or "covered via" or "included in", STOP. Check: is there an explicit task with explicit behaviors? If not, it's PARTIAL at best.
5. **When checking user flows, verify EACH step independently.** "Covered at high level" is not a valid assessment. Check: does a specific task behavior address this specific flow step?

### Phase 5: Forward Check (Completeness) — Architecture → Plan

For EACH architecture contract (EP1..EPn, E1..En, C1..Cn):

Apply the SAME classification rules. Check EVERY endpoint, entity, and component individually.

### Phase 6: Mutation Scan

For EACH item classified as COVERED or PARTIAL:

Compare specific values between source document and plan:
- Numbers (file sizes: MB, GB)
- HTTP status codes
- Thresholds, limits, counts
- Retry counts, timing values
- Error codes, error messages

If ANY value differs → reclassify as MUTATED. Quote BOTH values.

**Do not rationalize differences.** "5MB" ≠ "10MB" even if "they both validate file size." The number matters.

### Phase 7: Backward Check (Orphan Detection)

For EACH plan task:

1. Skip tasks where `Implements:` contains "N/A" or "infrastructure"
2. Check: does the `Implements:` reference match a REAL contract in the architecture doc?
3. If no match → flag as ORPHAN

**Check the actual endpoint.** Task 5 claims "PATCH /uploads/{id}/notify" — is PATCH /uploads/{id}/notify listed in the architecture's API Contract section? If not, it's an orphan.

### Phase 8: Generate Fix Instructions

For EACH gap, generate a SPECIFIC fix instruction:

| Gap Type | Fix Format |
|----------|------------|
| MISSING (no task) | "ADD TASK: [name] — [what it implements] with behaviors: [list]" |
| PARTIAL (incomplete) | "ADD BEHAVIOR to Task N: [missing behavior text]" |
| MUTATED (wrong value) | "MUTATED: Task N, behavior M: Change [wrong] to [correct]" |
| ORPHAN (no contract) | "ORPHAN WARNING: Task N implements [ref] which doesn't exist in architecture. Remove task or add endpoint to architecture." |

**Fix instructions must be specific enough to act on.** Not "add rate limiting" but "ADD TASK: Rate limiting — max 100 uploads/hour/user implementing S5".

### Phase 9: Report

Output this EXACT format:

```
PLAN COVERAGE REPORT

Spec: [path]
Architecture: [path]
Plan: [path(s)]

SPEC REQUIREMENTS:
S1: "[full text]" → [STATUS]
    [detail if not COVERED]
S2: "[full text]" → [STATUS]
    [detail]
...

USER FLOWS:
UF1: "[step text]" → [STATUS] ([which task])
    [detail if PARTIAL/MISSING]
...

ARCHITECTURE CONTRACTS:
EP1: [METHOD /path] → [STATUS] ([which task])
EP2: [METHOD /path] → [STATUS]
...
E1: [entity name] → [STATUS] ([which task])
...
C1: [component name] → [STATUS] ([which task])
...

Note: [list infrastructure-exempt tasks]

ORPHAN TASKS:
Task N: "[implements ref]" → NOT IN ARCHITECTURE
    [detail]

FIXES NEEDED:
1. [specific fix instruction]
2. [specific fix instruction]
...

SUMMARY:
Spec: N/M fully covered (X%) — N COVERED, N PARTIAL, N MISSING, N MUTATED
  (Note: MUTATED counts as "not fully covered")
User Flows: N/M fully covered (X%) — N COVERED, N PARTIAL
Architecture: N/M fully covered (X%) — N COVERED, N PARTIAL, N MISSING
Mutations: N
Orphan tasks: N
```

**Summary math rules:**
- Only COVERED counts as "fully covered"
- PARTIAL, MISSING, and MUTATED all count as "not fully covered"
- **Spec denominator** = count of S items only (S1..Sn)
- **User Flows denominator** = count of UF items (UF1..UFn)
- **Architecture denominator** = endpoints + entities + components (EP + E + C items)
- Count each status separately in the breakdown

**CRITICAL: Follow the report template EXACTLY.** Do not add extra sections (no separate ENTITIES section). Spec entities are checked as architecture contracts (E1..En). The only sections are: SPEC REQUIREMENTS, USER FLOWS, ARCHITECTURE CONTRACTS, ORPHAN TASKS, FIXES NEEDED, SUMMARY.

**Cross-check before writing SUMMARY:** Go back through your detailed report and COUNT each status. The summary numbers MUST match the detailed line items exactly. If you wrote 3 items as COVERED in the detail, the summary must say 3 COVERED.

## Rationalization Table

| Agent Excuse | Reality |
|-------------|---------|
| "Task 3 creates upload endpoints so GET and DELETE are covered" | Each endpoint is a separate contract. POST ≠ GET ≠ DELETE. Check method + path. |
| "UploadForm is rendered by UploadPage so it's covered" | Referenced ≠ dedicated task. PARTIAL at best. |
| "UploadError is implied by MarkFailed" | Different entity. Needs its own task or explicit behaviors. |
| "Covered at high level" | Not a valid status. Use COVERED, PARTIAL, MISSING, or MUTATED only. |
| "The values are close enough" | No. 5MB ≠ 10MB. HTTP 400 ≠ HTTP 413. Quote both values, classify as MUTATED. |
| "User flows are implicitly handled" | Check each step against specific task behaviors. Implicit ≠ covered. |
