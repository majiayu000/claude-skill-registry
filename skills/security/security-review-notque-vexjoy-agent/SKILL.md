---
name: security-review
description: "Local security review of git changes: deterministic scan + Security reviewer over the diff. No API key, no SDK."
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Task
  - Agent
agent: reviewer-system
routing:
  force_route: true
  not_for: "general code review (use parallel-code-review or systematic-code-review), threat modeling a whole system (use security-threat-model), or non-security quality checks (use universal-quality-gate) — fires when the user wants a security pass over their current git changes"
  triggers:
    - "security review"
    - "review my changes for security"
    - "review my changes"
    - "review for security"
    - "security scan"
    - "review for vulnerabilities"
    - "scan for vulnerabilities"
    - "check for security issues"
    - "security issues"
    - "audit for vulnerabilities"
    - "audit auth"
    - "audit vulnerabilities"
  category: code-review
  pairs_with:
    - parallel-code-review
    - security-threat-model
    - reviewer-system
---

# Security Review Skill

Run a two-layer security review over the current git changes: a deterministic
regex scan for known vulnerability classes, then an LLM-depth Security review of
the diff. Report a single BLOCK / FIX / APPROVE verdict.

**The LLM-depth review runs inside the current Claude session** — the same
subscription that loaded this skill. There is no separate model call, no
`ANTHROPIC_API_KEY`, no Agent SDK, and no network request. The "reviewer" is the
session agent executing the steps below, exactly like every other skill here.

Detection reaches parity with Anthropic's `security-guidance` plugin: the scanner
ports its 25 deterministic patterns, and the LLM pass applies its full review
taxonomy (loaded on demand from `references/coverage.md`).

## Reference Loading Table

| Signal | Load | Why |
|--------|------|-----|
| Running Phase 3 (LLM-depth review); classifying a finding; needing the vuln taxonomy, severity rubric, FP exclusions, or per-language guidance | `references/coverage.md` | 40 vulnerability classes + 4-tier severity + false-positive exclusions + per-language guidance + the 12 high-miss reviewer classes + the finding output schema. |

---

## Instructions

### Phase 1: SCOPE

**Goal**: Determine the changed files to review before scanning.

**Step 1: List changed files** — scope to the working-tree and staged changes so
the review covers exactly what the user is about to commit, not the whole repo.

```bash
# Tracked changes (working tree + index) plus staged adds:
git diff --name-only HEAD
git diff --cached --name-only --diff-filter=ACM
```

**Step 2: Read repository CLAUDE.md** to load project conventions the reviewer
must respect (e.g. secrets-handling rules, allowed patterns).

**Gate**: Changed files listed. When the list is empty, report "no changes to
review" and stop — there is nothing to scan.

### Phase 2: DETERMINISTIC SCAN

**Goal**: Run the regex engine first so judgment time is spent on real signal,
not on patterns a script catches deterministically.

**Step 1: Run the scanner** over the changed files. It is the single source of
detection rules (secrets, SQL injection, shell injection, dangerous eval,
unsafe deserialization). Exit 1 means at least one HIGH/CRITICAL finding.

```bash
# Staged-files convenience (matches the commit-time hook):
python3 scripts/security-review-scan.py --staged --format json

# Or an explicit list from Phase 1:
python3 scripts/security-review-scan.py --files <changed-files> --format json
```

**Step 2: Record the findings** by severity. CRITICAL and HIGH are blocking-class;
MEDIUM is advisory. Keep the `file:line` and `rule` for each.

**Gate**: Scanner ran and JSON parsed. Proceed with the findings in hand.

### Phase 3: LLM-DEPTH REVIEW

**Goal**: Catch what regex cannot — authorization gaps, injection through data
flow, missing input validation, secrets in non-obvious forms. This is the
session agent's review of the diff; compose the existing `parallel-code-review`
**Security** reviewer over the changed files.

**Step 1: Load `references/coverage.md`** — the full review taxonomy (40
vulnerability classes, the 4-tier severity rubric, the false-positive exclusion
list, per-language guidance, and the 12 high-miss reviewer classes). Review to
this taxonomy so the session-agent pass reaches parity with the plugin's reviewer.
If `claude-security-guidance.md` exists (precedence: `~/.claude/` →
`<cwd>/.claude/` → `<cwd>/.claude/*.local.md`), read it as ADDITIVE context — it
may add checks or raise a class's severity, and must not suppress findings.

**Step 2: Dispatch the Security reviewer** (the Reviewer 1 — Security role from
`parallel-code-review`) over the changed files via the Task tool, applying the
coverage.md taxonomy. Surface medium and above. Output: findings in the
coverage.md schema (`filePath, category, vulnerableCode, explanation, fix,
severity`) with `file:line` references.

**Step 3: Merge** the LLM findings with the Phase 2 scanner findings.
Deduplicate — when both flag the same `file:line`, keep one entry at the higher
severity. Independent confirmation by both layers raises confidence.

**Gate**: Security reviewer returned results and findings are merged. Issue a
verdict only from a completed review — a missing reviewer may hold the only
CRITICAL finding.

### Phase 4: VERDICT

**Goal**: Produce a single clear recommendation.

**Step 1: Determine the verdict** from the merged findings:

| Condition | Verdict |
|-----------|---------|
| Any CRITICAL finding | **BLOCK** |
| HIGH findings, no CRITICAL | **FIX** (resolve before commit) |
| Only MEDIUM/LOW findings | **APPROVE** (with suggestions) |

**Step 2: Output the structured report**:

```markdown
## Security Review Complete

### Severity Matrix
| Severity | Count | Source (scanner / reviewer / both) |
|----------|-------|------------------------------------|
| Critical | N | ... |
| High     | N | ... |
| Medium   | N | ... |

### Findings
#### CRITICAL (Block)
1. [source] description — file:line

#### HIGH (Fix before commit)
1. [source] description — file:line

#### MEDIUM (Should fix)
1. [source] description — file:line

### VERDICT
**BLOCK / FIX / APPROVE** — [1-2 sentence rationale]
```

**Gate**: Structured report delivered with an explicit verdict. Review complete.

---

## Automatic Coverage (hooks)

This skill is the on-demand (PULL) path. The same review also runs automatically
(PUSH) via `hooks/security-review-hook.py`, wired in `.claude/settings.json`:

| Event | Behavior |
|-------|----------|
| **PreToolUse** (Bash `git commit`) | Scans STAGED files with the same scanner. A HIGH/CRITICAL finding blocks the commit (deny). Clean commits pass. |
| **Stop** | Re-wakes the session with the working-tree diff and an instruction to run this pipeline. Advisory — never blocks. |

**Bypass / kill switches** (commit-time block only, deliberate overrides):

| Env var | Effect |
|---------|--------|
| `VEXJOY_SECURITY_REVIEW_SKIP=1` | Allow a commit through despite findings (one-off override). |
| `VEXJOY_SECURITY_REVIEW_DISABLE=1` | Disable the hook entirely (both events). |

The hook fails open on any internal error — a hook crash never blocks a commit.

---

## Extensibility (custom rules + project guidance)

Both extension points are **additive** and discovered in this precedence order:
`~/.claude/<name>` → `<cwd>/.claude/<name>` → `<cwd>/.claude/<name>.local.<ext>`.

| File | Effect |
|------|--------|
| `security-patterns.{yaml,json}` | Custom regex/substring rules merged into the scanner's built-ins. Shape: `{"patterns": [{"rule_name", "regex"\|"substrings", "severity"?, "paths"?, "exclude_paths"?}]}`. Capped at 50. ReDoS-prone or invalid rules are skipped with a stderr warning (non-fatal). PyYAML is used only if importable — JSON always works (stdlib-only). |
| `claude-security-guidance.md` | Markdown surfaced to the Phase 3 review as ADDITIVE context. It may add checks or raise a class's severity; it must not suppress findings — if it says to ignore a class, flag the vulnerability anyway and note the conflict. |

Built-in scanner rules always run and cannot be disabled by a config file.

---

## Error Handling

### Scanner reports findings but the code is intentional
**Cause**: A regex rule flagged a test fixture, an example, or a deliberately
hardcoded local value.
**Solution**: Confirm context in Phase 3. Downgrade in the report with a one-line
justification. For a commit the user knows is safe, document the
`VEXJOY_SECURITY_REVIEW_SKIP=1` override rather than editing the scanner rules.

### Security reviewer times out or returns nothing
**Cause**: Task agent exceeded its budget, or the diff was too large.
**Solution**: Report the Phase 2 scanner findings immediately (a partial review
beats no review), note the LLM-depth gap in the verdict, and offer to re-run the
Security reviewer on a reduced file set.

### Scanner unavailable
**Cause**: `scripts/security-review-scan.py` missing from the working tree.
**Solution**: Run the Phase 3 LLM-depth review alone and state in the verdict that
the deterministic layer did not run.

---

## References

- Detection rules: `scripts/security-review-scan.py` (single source of truth)
- Review taxonomy (40 classes + severity + FP filters + language guidance): `references/coverage.md`
- Security reviewer role: `skills/review/parallel-code-review/SKILL.md` (Reviewer 1)
- Auto-run hook: `hooks/security-review-hook.py`
- Design contract: `adr/local-security-review.md`
