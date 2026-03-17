---
name: diff-review
description: Deep multi-perspective review of current branch changes vs main — code quality, security, testing gaps, and language-specific gotchas. Use before requesting review to catch issues proactively.
---

# Diff Review

**Do NOT use `gh` or any GitHub CLI commands. All information must come from local git.**

Multi-perspective analysis of current branch changes vs main to catch issues before reviewers do.

## Step 1 — Identify Changes

```bash
# Get diff and commit list for current branch vs main
git diff main...HEAD
git log main..HEAD --oneline
```

FAIL FAST if current branch IS main or has no commits ahead of main.

Extract: branch name, commit list.

## Step 2 — Gather Full Context

```bash
# Full diff
git diff main...HEAD

# Changed files list
git diff main...HEAD --name-only
```

**Read every changed file in full** — not just the diff hunks. Understanding surrounding context is critical for catching issues that span beyond the changed lines.

## Step 3 — Detect Review Scope

### Language detection

Inspect file extensions of changed files. Load matching language skills for perspective 4.5:

| Extension | Skill |
|-----------|-------|
| `.py` | `languages:python-patterns` |
| `.js`, `.ts`, `.tsx` | `languages:js-ts-patterns` |
| `.go` | `languages:go-concurrency-patterns` |
| `.sh` | `languages:bash-defensive-patterns` |
| `.swift` | `languages:swift-patterns` |
| `.rs` | `languages:rust-project-patterns` |

### Flag missing tests

If the diff modifies source files but includes no test changes, flag this for the testing review perspective.

## Step 4 — Multi-Perspective Analysis

This is the core of the review. Analyze the diff from each perspective independently, then merge findings.

### 4.1 Code Review Excellence

Cross-reference `workflow:code-review-excellence` Phase 3 checklist:

- **Edge cases**: empty inputs, nulls, boundary values, concurrency, large inputs
- **Error handling**: missing catches, swallowed errors, unhelpful messages
- **Logic errors**: off-by-one, incorrect conditions, race conditions, resource leaks
- **Missing validation**: unchecked assumptions, missing type guards

### 4.2 Code Quality

Cross-reference `workflow:code-quality`:

- Code smells and anti-patterns
- Naming clarity and consistency
- DRY violations (duplicated logic)
- Unnecessary complexity
- Coupling and cohesion issues

### 4.3 Security Analysis

Cross-reference `security:security-analysis`, `security:auth-implementation-patterns`, `security:secrets-management`:

- STRIDE threat model against changed components
- Vulnerability patterns: injection, XSS, SSRF, path traversal
- Input validation gaps
- Authentication and authorization gaps
- Secrets or credentials in code
- Insecure defaults

### 4.4 Testing Review

Cross-reference `testing:language-testing-patterns`, `testing:test-driven-development`:

- Coverage gaps — untested branches, edge cases, error paths
- Test quality — behavior tests vs implementation tests
- Missing integration or boundary tests
- Flaky test indicators

### 4.5 Language-Specific Gotchas

Apply auto-detected `languages:*-patterns` skills. Common examples:

- **Python**: mutable default args, late binding closures, iterator exhaustion
- **TypeScript/JS**: `any` type leaks, missing `await`, prototype pollution, `==` vs `===`
- **Go**: goroutine leaks, unchecked errors, nil pointer dereference, defer in loops
- **Bash**: unquoted variables, missing `set -euo pipefail`, word splitting
- **Swift**: retain cycles, force unwrapping, main thread violations
- **Rust**: unnecessary `clone()`, unsafe blocks, lifetime issues

## Step 5 — Structured Findings Report

Merge all findings and deduplicate. Present organized by severity:

```markdown
## Diff Review — {BRANCH_NAME}

### Critical
- {finding} — {file:line} — {perspective that caught it}

### High
- {finding} — {file:line} — {perspective}

### Medium
- {finding} — {file:line} — {perspective}

### Test Gaps
- {description of missing coverage}

### What Looks Good
- {positive observation — acknowledge strong patterns}
```

If no findings at a severity level, omit that section. Always include "What Looks Good" to be balanced.

## Step 6 — Decision Gate

**Default behavior: report only.** Do NOT automatically implement fixes.

After presenting findings, ask:

```
What would you like to do?
1. Implement fixes for the findings above
2. Nothing — review complete
```

If the user chooses to implement fixes, follow the same execution rules as `workflow:pr-comment-resolution` Step 4 (scope guard, atomic commits, verify before push).

---

## Agent Team Mode

When invoked via `/team-review` or when the diff is large (>500 lines changed), consider using agent teams for parallel multi-perspective review.

### Team Configuration

```yaml
team:
  recommended_size: 4
  agent_roles:
    - name: security-reviewer
      type: Explore
      focus: "STRIDE analysis, vulnerability patterns, secrets detection"
      skills_loaded: ["security:security-analysis", "security:auth-implementation-patterns"]
      steps: ["Step 4.3"]
    - name: quality-reviewer
      type: Explore
      focus: "Code smells, edge cases, error handling, naming, DRY"
      skills_loaded: ["workflow:code-quality", "workflow:code-review-excellence"]
      steps: ["Step 4.1", "Step 4.2"]
    - name: test-reviewer
      type: Explore
      focus: "Coverage gaps, test quality, missing integration tests"
      skills_loaded: ["testing:language-testing-patterns", "testing:test-driven-development"]
      steps: ["Step 4.4"]
    - name: language-reviewer
      type: Explore
      focus: "Language-specific gotchas, idiom violations"
      skills_loaded: ["Auto-detected languages:*-patterns"]
      steps: ["Step 4.5"]
  file_ownership: "shared-read-only"
  lead_mode: "hands-on"
```

### Team Workflow

1. **Lead** executes Steps 1-3 (identify changes, gather context, detect scope)
2. **Lead** distributes the full diff + changed files to all reviewers
3. **Reviewers** work in parallel, each covering their assigned steps
4. **Lead** collects findings, deduplicates, resolves contradictions
5. **Lead** produces Step 5 structured report + Step 6 decision gate

### Single-Agent Fallback

Without team mode, execute all perspectives sequentially (default behavior). Team mode is an optional enhancement for large diffs or when explicitly requested.

---

## Cross-References

- `workflow:code-review-excellence` — Edge case checklist, severity framework
- `workflow:code-quality` — Code smell detection, anti-pattern identification
- `security:security-analysis` — STRIDE model, vulnerability pattern matching
- `security:auth-implementation-patterns` — Auth review checklist
- `security:secrets-management` — Secrets detection patterns
- `testing:language-testing-patterns` — Coverage analysis, test quality assessment
- `testing:test-driven-development` — Test design principles
- `workflow:verification-before-completion` — Verification gate if implementing fixes
- `languages:*-patterns` — Auto-detected language-specific review lenses
