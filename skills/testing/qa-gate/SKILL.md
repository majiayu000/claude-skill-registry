---
name: qa-gate
description: Create or update a quality gate decision for a story or code changes. Runs quality checks, specialist reviews, and produces a persistent YAML gate file with actionable findings. Supports PASS, CONCERNS, FAIL, or WAIVED decisions.
---

# /qa-gate - Quality Gate Decision

## Description

Generate a quality gate decision with persistent YAML output. Runs automated checks and optional specialist reviews, then produces a gate file that can be tracked and referenced.

**Key Features:**
- Persistent YAML gate files for traceability
- Standardized severity scale (low, medium, high)
- Issue ID prefixes for categorization (SEC-, PERF-, TEST-, etc.)
- WAIVED status with approval tracking
- Updates story file with gate reference
- NFR validation (security, performance, reliability, accessibility)

## Usage

```bash
# Quick gate for a story (tests, types, lint only)
/qa-gate 3.1.5

# Full gate with specialist reviews
/qa-gate 3.1.5 --deep

# Gate for current branch (no story reference)
/qa-gate --branch

# Gate with specific specialists
/qa-gate 3.1.5 --security --performance

# Waive known issues
/qa-gate 3.1.5 --waive --reason "Accepted for MVP" --approved-by "Product Owner"

# Quick check without persisting file
/qa-gate 3.1.5 --dry-run
```

## Parameters

- **story** - Story number (e.g., `3.1.5`) or omit for branch-based review
- **--deep** - Run all specialist reviews (security, performance, accessibility)
- **--security** - Run security specialist review
- **--performance** - Run performance specialist review
- **--accessibility** - Run accessibility specialist review
- **--branch** - Review current branch without story reference
- **--waive** - Mark gate as WAIVED (requires --reason and --approved-by)
- **--reason** - Reason for waiver
- **--approved-by** - Who approved the waiver
- **--dry-run** - Run checks but don't persist gate file

---

## EXECUTION INSTRUCTIONS

### Phase 1: Parse Arguments & Locate Files

```
1. Parse story number or --branch flag
2. If story provided:
   - Find story file: docs/stories/{STORY_NUM}.*.md
   - Extract story title and slug
3. Determine gate file path: docs/qa/gates/{STORY_NUM}-{slug}.yml
4. Check if gate file already exists (for history tracking)
```

### Phase 2: Run Required Checks

**Always run these checks first:**

```bash
# Run in parallel for speed
pnpm test --filter='...[origin/main]'
pnpm check-types --filter='...[origin/main]'
pnpm lint --filter='...[origin/main]'
```

**Collect results:**
```yaml
checks:
  tests: { status: PASS|FAIL, details: "X tests passed" }
  types: { status: PASS|FAIL, details: "No type errors" }
  lint: { status: PASS|FAIL, details: "No lint errors" }
```

### Phase 3: Specialist Reviews (if --deep or specific flags)

**Use haiku model for fast, focused reviews:**

```
# Security Review (if --deep or --security)
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Security review",
  prompt: "You are a security specialist. Review the code changes.

           Check for:
           - Authentication/authorization issues
           - Injection vulnerabilities (SQL, XSS, command)
           - Sensitive data exposure
           - OWASP Top 10 issues
           - Hardcoded secrets or credentials

           For each finding, provide:
           - id: SEC-{NNN}
           - severity: low|medium|high
           - finding: Brief description
           - suggested_action: How to fix
           - file: File path
           - line: Line number (if applicable)

           Return findings as YAML array."
)

# Performance Review (if --deep or --performance)
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Performance review",
  prompt: "You are a performance specialist. Review the code changes.

           Check for:
           - N+1 query patterns
           - Missing database indexes
           - Unnecessary re-renders in React
           - Large bundle imports
           - Missing memoization
           - Inefficient algorithms

           For each finding, provide:
           - id: PERF-{NNN}
           - severity: low|medium|high
           - finding: Brief description
           - suggested_action: How to fix
           - file: File path

           Return findings as YAML array."
)

# Accessibility Review (if --deep or --accessibility)
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Accessibility review",
  prompt: "You are an accessibility specialist. Review the code changes.

           Check for:
           - WCAG 2.1 AA compliance
           - Keyboard navigation support
           - Screen reader compatibility
           - Missing ARIA labels/roles
           - Color contrast issues
           - Focus management

           For each finding, provide:
           - id: A11Y-{NNN}
           - severity: low|medium|high
           - finding: Brief description with WCAG criterion
           - suggested_action: How to fix
           - file: File path

           Return findings as YAML array."
)
```

### Phase 4: Determine Gate Decision

**Decision logic:**

```
IF --waive flag provided:
  gate = WAIVED
ELSE IF any check FAILED OR any high severity issue:
  gate = FAIL
ELSE IF any medium severity issue:
  gate = CONCERNS
ELSE:
  gate = PASS
```

**Status reason (1-2 sentences):**
- PASS: "All checks passed with no significant issues."
- CONCERNS: "Non-blocking issues found that should be addressed."
- FAIL: "{reason for failure - e.g., 'Tests failing' or 'High severity security issue'}"
- WAIVED: "{user-provided reason}"

### Phase 5: Generate Gate File

**Write YAML to `docs/qa/gates/{STORY_NUM}-{slug}.yml`:**

```yaml
schema: 1
story: "{STORY_NUM}"
story_title: "{STORY_TITLE}"
gate: PASS|CONCERNS|FAIL|WAIVED
status_reason: "{1-2 sentence explanation}"
reviewer: "Claude Code"
updated: "{ISO-8601 timestamp}"

# Waiver (only active if WAIVED)
waiver:
  active: false  # or true if WAIVED
  reason: ""     # populated if WAIVED
  approved_by: "" # populated if WAIVED

# All issues found
top_issues: []
# Example:
#   - id: "SEC-001"
#     severity: high
#     finding: "No rate limiting on login endpoint"
#     suggested_action: "Add rate limiting middleware"
#     file: "src/api/auth/login.ts"

# NFR validation summary
nfr_validation:
  security: { status: PASS|CONCERNS|FAIL|SKIPPED, issue_count: 0 }
  performance: { status: PASS|CONCERNS|FAIL|SKIPPED, issue_count: 0 }
  accessibility: { status: PASS|CONCERNS|FAIL|SKIPPED, issue_count: 0 }
  tests: { status: PASS|FAIL, details: "" }
  types: { status: PASS|FAIL, details: "" }
  lint: { status: PASS|FAIL, details: "" }

# Risk summary
risk_summary:
  totals: { high: 0, medium: 0, low: 0 }
  recommendations:
    must_fix: []   # high severity items
    should_fix: [] # medium severity items
```

### Optional Phase 5b: Generate UX Gate File

When UX review is requested or required (e.g., UI-heavy stories), `/qa-gate` SHOULD coordinate with the UX Expert agent to produce a separate **UX gate** file.

- UX gate path: `docs/qa/gates/{STORY_NUM}-{slug}-ux.yml`
- UX gate content: follows the UX gate schema defined in `work/agents/ux-expert.md` and should include:
  - `ux_score` (0–100)
  - `gate` (PASS | CONCERNS | FAIL | WAIVED) from a UX/a11y/design-system perspective
  - Summaries of AXE/Lighthouse checks, design-system conformance, and console status
- UX agent SHOULD use Playwright and Chrome DevTools MCP integrations to:
  - Run a11y/AXE checks and, where feasible, Lighthouse-style audits
  - Verify use of the shared design system components
  - Confirm there are no unresolved console errors/warnings related to the flow

`/qa-gate` does not compute UX scores itself but MAY:
- Check for the existence of `docs/qa/gates/{STORY_NUM}-{slug}-ux.yml`
- Surface the UX gate status alongside the main QA gate in its summary output

### Phase 6: Update Story File (if story provided)

**Append to story's QA Results section:**

```markdown
## QA Results

### Gate Status

Gate: {STATUS} → docs/qa/gates/{STORY_NUM}-{slug}.yml
Updated: {ISO-8601 timestamp}
Reviewer: Claude Code

{If issues found:}
Top Issues:
- [{ID}] {severity}: {finding}
```

### Phase 7: Report Summary

```
═══════════════════════════════════════════════════════
  Quality Gate: {STORY_NUM} - {STORY_TITLE}
═══════════════════════════════════════════════════════

Gate: {PASS|CONCERNS|FAIL|WAIVED}
Reason: {status_reason}

Checks:
  Tests:    {PASS|FAIL}
  Types:    {PASS|FAIL}
  Lint:     {PASS|FAIL}

{If specialist reviews run:}
NFR Validation:
  Security:      {STATUS} ({N} issues)
  Performance:   {STATUS} ({N} issues)
  Accessibility: {STATUS} ({N} issues)

{If issues found:}
Top Issues ({N} total):
  [{ID}] {severity}: {finding}
  ...

Gate File: docs/qa/gates/{STORY_NUM}-{slug}.yml

{If FAIL:}
Recommendation: Address high-severity issues before proceeding.

{If CONCERNS:}
Recommendation: Review issues and proceed with awareness.

{If WAIVED:}
Waiver: {reason}
Approved By: {approved_by}
═══════════════════════════════════════════════════════
```

---

## Issue ID Prefixes

| Prefix | Category |
|--------|----------|
| SEC- | Security issues |
| PERF- | Performance issues |
| A11Y- | Accessibility issues |
| TEST- | Testing gaps |
| REL- | Reliability issues |
| MNT- | Maintainability concerns |
| ARCH- | Architecture issues |
| DOC- | Documentation gaps |
| REQ- | Requirements issues |

## Severity Scale

**Fixed values - no variations:**

| Severity | Description | Action |
|----------|-------------|--------|
| `high` | Critical issues, should block | Must fix before release |
| `medium` | Should fix soon, not blocking | Schedule for soon |
| `low` | Minor issues, cosmetic | Fix when convenient |

## Gate Statuses

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `PASS` | All good | No issues or only low severity |
| `CONCERNS` | Proceed with awareness | Medium severity issues present |
| `FAIL` | Should not proceed | High severity issues or check failures |
| `WAIVED` | Accepted despite issues | Explicitly approved to proceed |

---

## Sub-Agent Architecture

```
Main Orchestrator (/qa-gate)
    │
    ├─▶ Required Checks (inline)
    │   ├── pnpm test
    │   ├── pnpm check-types
    │   └── pnpm lint
    │
    └─▶ Specialist Reviews (parallel, haiku)
        ├── Security specialist
        ├── Performance specialist
        └── Accessibility specialist
```

---

## Integration with /implement

The `/implement` skill calls `/qa-gate` for its QA phase:

```
/implement 3.1.5
    │
    ├─▶ ... implementation phases ...
    │
    └─▶ /qa-gate 3.1.5 --deep
            └── Produces gate file and updates story
```

---

## Examples

### Quick Gate (tests only)
```bash
/qa-gate 3.1.5
# Runs: tests, types, lint
# Output: docs/qa/gates/3.1.5-my-story.yml
```

### Deep Gate (all specialists)
```bash
/qa-gate 3.1.5 --deep
# Runs: tests, types, lint + security, performance, accessibility
# Output: docs/qa/gates/3.1.5-my-story.yml
```

### Waive Known Issues
```bash
/qa-gate 3.1.5 --waive --reason "MVP release, will fix in v2" --approved-by "Tech Lead"
# Sets gate to WAIVED with approval tracking
```

### Branch Review (no story)
```bash
/qa-gate --branch --deep
# Reviews current branch without story reference
# Output: docs/qa/gates/branch-{branch-name}.yml
```
