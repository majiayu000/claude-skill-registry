---
name: code-review
description: Review current git changes or latest commit using code-reviewer and architect-reviewer agents. Use after completing code changes to get comprehensive quality feedback.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Task
disable-model-invocation: true
---

# Code Review Command

## Purpose

Perform comprehensive code review of current changes or latest commit. Automatically invokes:

- **code-reviewer agent**: Always (code quality, security, maintainability)
- **architect-reviewer agent**: Conditionally (architectural impact assessment)

---

## Workflow

### 1. Determine Review Target

**Check for uncommitted changes:**

```bash
git status --porcelain
```

**Decision:**

- If changes exist: Review uncommitted changes via `git diff`
- If no changes: Review latest commit via `git log -1` and `git show HEAD`

### 2. Analyze Change Scope

**Extract metrics from git output:**

Count:

- Files changed
- Lines added/removed
- Directories affected
- New files vs modifications

Detect:

- Database migration files (`migrations/`, `schema.prisma`, `*.sql`)
- API contract files (`*.graphql`, `openapi.yaml`, API route files)
- Configuration files (`package.json`, `go.mod`, `docker-compose.yml`)
- New directories or modules

### 3. Invoke code-reviewer Agent

**Always execute using Task tool with subagent_type: "code-reviewer":**

```
Perform comprehensive code review of the current changes.

Focus areas:
- Code quality: readability, naming, structure
- Security: exposed secrets, input validation, vulnerability patterns
- Error handling: edge cases, error messages, recovery
- Performance: obvious bottlenecks, inefficient patterns
- Testing: coverage for critical paths
- Coding standards compliance

Changes to review:
{paste git diff or git show output}

Provide feedback organized by:
- Critical issues (must fix before merge)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific code examples and fix recommendations.
```

The code-reviewer agent has access to Read, Write, Edit, Bash, and Grep tools and will analyze the code thoroughly.

### 4. Conditional architect-reviewer Invocation

**Scope Classification Criteria** (score each criterion met):

| Criterion             | Threshold                                        | Score |
| --------------------- | ------------------------------------------------ | ----- |
| Files Modified        | ≥ 8 files                                        | +1    |
| Total Lines Changed   | ≥ 300 lines                                      | +1    |
| Directories Affected  | ≥ 3 directories                                  | +1    |
| New Module/Package    | New directory with ≥3 files                      | +1    |
| API Contract Changes  | Modified: schema/, .graphql, api/, route files   | +1    |
| Database Schema       | Modified: migrations, schema files, ORM models   | +1    |
| Config/Infrastructure | Modified: docker-compose, Dockerfile, K8s, CI/CD | +1    |
| Dependency Changes    | Modified: package.json, go.mod, requirements.txt | +1    |

**Decision**:

- **Score < 3** → Invoke `code-reviewer` only
- **Score ≥ 3** → Invoke both `code-reviewer` and `architect-reviewer`

**Request architect-reviewer using Task tool with subagent_type: "architect-reviewer":**

```
Perform architectural review of these changes.

Change scope:
- Files changed: {count}
- Lines: +{added} -{removed}
- Directories affected: {list}
- Scope score: {X}/8
- Triggered by: {list of criteria met}

Evaluate:
- System design impact
- Scalability implications
- Technology choice justification
- Integration pattern soundness
- Security architecture
- Technical debt introduced/resolved
- Evolution path clarity

Provide strategic recommendations prioritized by:
- Critical architectural risks
- Design improvement opportunities
- Long-term maintainability concerns

Changes to review:
{paste git diff or git show output}
```

The architect-reviewer agent has access to Read, Write, Edit, Bash, Glob, and Grep tools for comprehensive analysis.

---

## Output Format

**Generate consolidated review summary:**

```markdown
# Code Review Report

**Generated**: {timestamp}
**Scope**: {uncommitted changes / latest commit: {hash}}
**Files Changed**: {count}
**Reviewers Invoked**: code-reviewer{, architect-reviewer if applicable}

---

## 📊 Change Summary

- **Lines**: +{added} -{removed}
- **Files**: {count} ({new_count} new, {modified_count} modified)
- **Directories**: {affected directories}

---

## 🔍 Code Reviewer Feedback

{consolidated output from code-reviewer agent}

---

## 🏗️ Architecture Reviewer Feedback

{if invoked, consolidated output from architect-reviewer agent}
{if not invoked, state: "Architectural review not required for this change scope"}

---

## ✅ Review Checklist

Based on agent feedback, generate action items:

### Critical (Must Fix)

- [ ] {issue 1}
- [ ] {issue 2}

### High Priority (Should Fix)

- [ ] {issue 3}

### Suggestions (Consider)

- [ ] {improvement 1}

---

## 📝 Next Steps

{recommended actions based on review results}
```

---

## Important Notes

- **Never modify code directly** - this command only performs review
- **Agent autonomy**: code-reviewer and architect-reviewer may read files, run tests, or analyze dependencies as needed
- **Coding guidelines**: code-reviewer checks for coding standard violations
- **Incremental reviews**: For large changes (>20 files), agents may focus on high-impact areas first
- **Git safety**: All git commands are read-only (status, diff, log, show)

---

## Example Usage

```bash
# Review uncommitted changes
/code-review

# Review specific commit (pass commit hash in conversation)
# User: "Review commit abc123"
# Then: /code-review
```

---

## Execution Instructions for Claude

1. Run `git status --porcelain` to detect changes
2. If changes exist:
   - Run `git diff` to get uncommitted changes
   - Run `git diff --stat` for metrics
3. If no changes:
   - Run `git log -1 --oneline` to get latest commit
   - Run `git show HEAD` to get commit changes
   - Run `git show HEAD --stat` for metrics
4. Calculate scope score against 8 criteria
5. **Always** invoke code-reviewer using Task tool with subagent_type: "code-reviewer"
6. **If score ≥ 3** invoke architect-reviewer using Task tool with subagent_type: "architect-reviewer"
7. Wait for agent(s) to complete analysis
8. Consolidate feedback into structured report
9. Generate actionable checklist

**Token optimization:**

- Use `git diff --stat` and `git show --stat` for metrics (avoid full diff parsing)
- Only pass full diff content to agents, not to your own analysis
- Let agents handle file reading - don't pre-read all changed files
