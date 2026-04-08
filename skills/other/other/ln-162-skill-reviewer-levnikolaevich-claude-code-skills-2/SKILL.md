---
name: ln-162-skill-reviewer
description: "Reviews skills (D1-D11 + M1-M6 criteria) or .claude/commands for quality. Use when validating skill correctness before release."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-162-skill-reviewer

**Type:** L3 Worker (standalone-capable)
**Category:** 1XX Documentation Pipeline

Universal reviewer with two modes:
- `SKILL` for `ln-*/SKILL.md`
- `COMMAND` for `.claude/commands/*.md`

> **Plan Mode behavior:** Phases 1-4 and 6-7 are research. Run them fully in Plan Mode, write the report plus fix list into the plan, and apply edits only after approval.

---

## Mode Detection

| Condition | Mode | Review Profile |
|-----------|------|----------------|
| `ln-*/SKILL.md` files exist in CWD | SKILL | Full D1-D11 + M1-M6 |
| `.claude/commands/*.md` files exist | COMMAND | Structural + actionability |
| Both exist | SKILL | Override with `$ARGUMENTS=commands` |

## Input

`$ARGUMENTS` options:
- empty -> auto-detect mode and scope
- `ln-400 ln-500` -> SKILL mode, specific skills
- `commands` -> COMMAND mode, all `.claude/commands/*.md`
- `deploy.md run-tests.md` -> COMMAND mode, specific files

When invoked by another skill, file paths may be passed directly.

---

## SKILL Mode

### Phase 1: Scope Detection

If `$ARGUMENTS` is provided:
- treat each token as a skill directory prefix
- glob `{prefix}*/SKILL.md`

If `$ARGUMENTS` is empty:
- inspect git diff, staged files, and untracked files
- collect primary skill dirs
- collect affected skills referencing changed shared files
- collect dependency skills from worker tables and `Skill()` invocations

Report:
`Scope: {N} primary, {M} affected, {K} dependency skills.`

### Phase 2: Automated Verification

Run:

```bash
bash references/run_checks.sh {scoped SKILL.md files}
```

Automated failures are pre-verified. Record every one.

### Phase 3: Structural Review

**MANDATORY READ:** Load `references/structural_review.md`, `shared/references/skill_contract.md`, `shared/references/mcp_applicability_matrix.md`, and `shared/references/mcp_tool_preferences.md`

Review every skill in scope across D1-D11.

Treat these as structural issues, not style nits:
- missing `**Type:**` when role-sensitive checks depend on it
- worker independence violations in L3 workers
- broken shared paths
- stale root-doc assumptions after `AGENTS.md canonical / CLAUDE.md thin shim`
- markdown-analysis skills missing `markdown_read_protocol.md`
- extraction or audit skills contradicting the shared docs-quality contract
- skills contradicting the shared skill contract
- skills that should make `hex-line` primary but only describe built-in file tools
- skills that should make `hex-graph` primary but still describe grep/manual analysis as the default path
- skills that add `hex-graph` or `hex-line` with no real applicability per the shared matrix
- wrong MCP namespaces such as `mcp__hex_graph__...`

### Phase 4: Intent Review

**MANDATORY READ:** Load `references/intent_review.md`

Apply M1-M6 to primary skills only. Read the git diff for each primary skill.

### Phase 5: Fix

Auto-fix deterministic issues:
- wrong paths
- stale references
- duplicated wording
- worker-independence violations with exact removals
- copied docs shell sections in command files

Do not guess on ambiguous behavior.

After fixes, re-read each primary skill end-to-end and compress redundant wording without changing behavior.

### Phase 6: Report

Verdict rules:
- any structural violation not auto-fixed -> `FAIL`
- only advisory intent concerns remain -> `PASS with CONCERNS`
- zero findings -> `PASS`

Report format:

```text
## Skill Coherence Review -- {PASS|PASS with CONCERNS|FAIL}

**Scope:** {reviewed skills}
**Verdict:** {verdict}
```

### Phase 7: Volatile Numbers Cleanup

Remove stale aggregate counts from SKILL.md files. Keep only local counts intrinsic to the reviewed file.

---

## COMMAND Mode

**MANDATORY READ:** Load `references/command_review_criteria.md`

### Phase 1: Scope Detection

- explicit file paths -> review those files
- `commands` -> glob `.claude/commands/*.md`
- coordinator-supplied file list -> review those files

### Phase 2: Review

For each command file:
- apply all command review criteria
- verify source provenance
- verify no copied docs shell sections remain

### Phase 3: Fix

Auto-fix where safe:
- missing frontmatter
- missing `allowed-tools`
- description too long
- missing `Last Updated`
- exact copied docs shell sections

### Phase 4: Report

```text
## Command Review -- {N} files

| File | Verdict | Issues |
|------|---------|--------|

Verdicts: PASS / FIXED / WARN / FAIL
Pass rate: {X}%
```

---

## Rules

- Automated checks are non-negotiable.
- Read all scoped files before reporting.
- Fix deterministic issues immediately.
- Do not update versions or dates unless the user explicitly requests it.
- `shared/` changes affect all referencing skills.
- Worker independence is mandatory for L3 workers:
  - no `**Coordinator:**`
  - no `**Parent:**`
  - no required caller declaration
- Docs-model drift is a structural defect, not a preference.
- `Agent Teams` / `TeamCreate` are deprecated outside clearly marked historical references.

## Reference Files

- `references/structural_review.md`
- `references/intent_review.md`
- `references/automated_checks.md`
- `references/run_checks.sh`
- `references/deprecated_apis.md`
- `references/command_review_criteria.md`
- `references/check_marketplace.mjs`

## Definition of Done

- [ ] Scope detected
- [ ] Automated checks executed
- [ ] D1-D11 reviewed across all scoped skills
- [ ] M1-M6 evaluated for primary skills
- [ ] Fixable findings auto-fixed
- [ ] Post-fix holistic compaction completed
- [ ] Final verdict report generated

---

**Version:** 1.0.0
**Last Updated:** 2026-03-26
