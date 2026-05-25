---
name: rfc
description: >-
  Manage architecture RFCs: create, review, list, update, and transition status.
  Use when user mentions "RFC", "technical proposal", "architecture proposal",
  or wants to draft, review, list, update, or change status of RFCs.
argument-hint: "<action> [args]  (create <topic> | review <path> | status <number> <status> | list | update <path>)"
disable-model-invocation: true
---

# RFC Manager

Manage architecture RFCs with 5 operations: create, review, list, update, status.

## Argument Parsing

Parse `$ARGUMENTS` to determine the action:

| First word | Remaining args | Operation |
|------------|---------------|-----------|
| `create` | `<topic>` | Draft a new RFC |
| `review` | `<path-to-rfc>` | Review an existing RFC |
| `list` | (none) | List all RFCs |
| `update` | `<path-to-rfc>` | Update specific RFC sections |
| `status` | `<number> <status>` | Transition RFC status with validation and side effects |
| (empty) | | Ask the user which action to perform |

If the first word does not match any action, treat the entire `$ARGUMENTS` as a topic and default to `create`.

## RFC Directory Discovery

Used by all operations. Search for RFC files across all convention paths (exclude `*.spec.md` companion files):

1. `docs/rfcs/*.md`
2. `docs/20-architecture/rfcs/*.md` (jd-docs — detected via `.jd-config.json` or `docs/20-architecture/` directory)
3. `.arkhe/rfcs/*.md` (arkhe convention)
4. `arkhe/rfcs/*.md`

For **create** and **update**, resolve a write directory:
- If jd-docs detected → `docs/20-architecture/rfcs/`
- Else if `docs/rfcs/` exists → `docs/rfcs/`
- Else → create `docs/rfcs/` as default

## Operation: create

Draft a populated RFC — NOT a blank template. Gather context, write a spec, then write a real first draft with honest self-assessment.

1. **Determine topic** from args after `create` (or ask if empty)
2. **Gather context** — search conversation, research artifacts (`docs/30-research/`, `docs/50-research/`, `docs/research/`), memory files, relevant source code, and ADRs (`docs/20-architecture/22-adr/`, `docs/20-architecture/adr/`, `docs/adr/`). See [WORKFLOW.md](WORKFLOW.md) for detail.
3. **Confirm scope** with user before drafting — present what you found and proposed scope. Use `AskUserQuestion` for meaningful alternatives.
4. **Resolve number and slug** — discover write directory, glob all convention paths for highest existing number, assign next (zero-padded 4 digits). Confirm title with user, generate kebab-case slug. Both spec and RFC will use `NNNN-<slug>`.
5. **Write spec file** — read spec template at `${CLAUDE_SKILL_DIR}/templates/rfc-spec-template.md`. Fill Problem Statement, Key Constraints, Success Criteria, and Scope Boundaries with concrete content. Write to `<dir>/NNNN-<slug>.spec.md`. Present to user for confirmation via `AskUserQuestion`. See [WORKFLOW.md](WORKFLOW.md) for spec guidance.
6. **Read RFC template** at `${CLAUDE_SKILL_DIR}/templates/rfc-template.md` for section structure
7. **Draft populated RFC** filling every section with substantive content. See [WORKFLOW.md](WORKFLOW.md) for per-section guidance. Set Author to git user name, Status to `Draft`, Date to today.
8. **Append Author's Notes** — below Open Questions, record: shortcuts taken, unverified assumptions, areas of uncertainty, low-confidence sections. Aim for 3-8 items. Be specific — these feed the adversarial review. See [WORKFLOW.md](WORKFLOW.md) for confession guidelines.
9. **Write RFC** to `<dir>/NNNN-<slug>.md`
10. **Suggest next steps**: `/rfc review <path>` for adversarial design review (uses rfc-critic agent)

## Operation: review

Adversarial review of the RFC using the `rfc-critic` agent — a dedicated red-team reviewer that reads the Author's Notes as attack vectors and checks spec alignment.

1. **Read RFC** at the given path (if empty, ask — suggest globbing `docs/rfcs/*.md` and `docs/20-architecture/rfcs/*.md`)
2. **Load spec file** — check for a companion `NNNN-<slug>.spec.md` alongside the RFC. If found, read it.
3. **Discover architecture standards** (check in order, use first found):
   - `.arkhe/roadmap/architecture.md` (arkhe convention)
   - `docs/20-architecture/` directory (jd-docs convention)
   - `docs/architecture.md` or `docs/architecture/` (generic)
   - Fall back to general best practices
4. **Spawn rfc-critic agent** — use the Agent tool (subagent_type: `doc:rfc-critic`). Pass: the RFC content, spec content (if found), architecture standards (if found). See [WORKFLOW.md](WORKFLOW.md) for delegation details.
5. **Present review output** — the agent returns a structured review with confidence score, verdict, concerns by severity (each with evidence citations), and improvements. Display to user.
6. **Verdict criteria**:
   - **Approve**: No critical concerns, minor issues only
   - **Approve with changes**: No critical concerns, has major concerns with clear fixes
   - **Needs redesign**: Has critical concerns or fundamental architecture issues
7. Flag missing RFC template sections as Minor concerns
8. **Suggest next steps**: `/rfc update <path>` to address findings

## Operation: list

List all architecture RFCs with their current status.

1. Search all convention paths (see RFC Directory Discovery)
2. For each RFC, extract from headers: Number/Filename, Title (from `# RFC: [Title]` or first `#` heading), Status (`Draft`/`Review`/`Approved`/`Rejected`/`Superseded` — default "Unknown"), Author (default "—"), Date (default "—")
3. Output markdown table sorted by number descending (newest first):

```markdown
# Architecture RFCs

| # | Title | Status | Author | Date |
|---|-------|--------|--------|------|

**Summary**: X total — Y Draft, Z Review, W Approved
```

4. If no RFCs found, suggest `/rfc create <topic>`

## Operation: update

Re-draft specific sections of an existing RFC based on new context or feedback.

1. **Read RFC** at the given path (if empty, ask for path)
2. **Identify sections to update**:
   - If user specified sections in conversation, update those
   - If invoked after a `/rfc review`, use review findings to identify sections needing changes
   - Otherwise, ask the user which sections to revise
3. **Gather fresh context** from conversation, research, and codebase for the sections being updated
4. **Re-draft sections** — rewrite identified sections with improved content. Preserve all unchanged sections exactly as-is.
5. **Update Date** to today. Keep Status unchanged unless user requests a transition.
6. **Handle Author's Notes** — if status transitions to Approved, strip the Author's Notes section entirely. If major sections were re-drafted, refresh the confessions. See [WORKFLOW.md](WORKFLOW.md) for lifecycle rules.
7. **Check spec alignment** — if a companion `.spec.md` file exists and the update touches Goals, Non-Goals, or Architecture Overview, verify the RFC still aligns with the spec. Flag drift to the user.
8. **Show diff summary** — list which sections were changed and a brief description of each change
9. **Suggest next steps**: `/rfc review <path>` to verify the updates

## Operation: status

Transition RFC status with validation, warnings, and side effects.

1. **Find RFC** — resolve number to file path by globbing all convention paths for `NNNN-*.md`. Read current status from `**Status**:` field.
2. **Validate transition** — check against valid transitions. Warn (but allow) on unusual paths:
   - Valid: Draft → Review → Approved/Rejected, any → Superseded
   - Warn: Draft → Approved (skipping Review), Approved → Draft (going backwards)
   - On warning, use `AskUserQuestion` to confirm
3. **Apply status change** — update `**Status**:` field in the RFC
4. **Side effects**:
   - **→ Approved**: Strip `## Author's Notes` section entirely
5. **Confirm** — show old status → new status, side effects applied

**Valid statuses**: Draft | Review | Approved | Rejected | Superseded

Note: The `update` operation still handles inline status changes during content updates. Use `/rfc status` for dedicated status transitions with validation.

## Quality Standards

- Every section must contain real content, not placeholder text like `[describe here]`
- Reference specific files, packages, and patterns from the codebase
- If a section doesn't apply, state that explicitly with a one-line rationale
- Drafts should be good enough to review immediately, not skeletons to fill in later

## Progressive Disclosure

- [WORKFLOW.md](WORKFLOW.md) — detailed per-operation workflows
- [EXAMPLES.md](EXAMPLES.md) — usage examples for all operations
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — common issues and solutions
