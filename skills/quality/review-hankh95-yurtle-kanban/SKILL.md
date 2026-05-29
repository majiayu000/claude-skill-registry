---
name: review
description: Pre-merge review - verify tests, docs, and merge readiness for an expedition
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Bash(pytest *), Bash(python3 *), Bash(gh *), Read, Glob, Grep
argument-hint: "EXP-XXX"
---

# Review Expedition

Perform pre-merge review of an expedition: verify tests exist and pass, docs are updated, and merge if ready.

## Required Argument

`$ARGUMENTS` must be an expedition ID (e.g., `EXP-711` or `711`).

## Steps

### 1. Load Expedition

```bash
# Find expedition file
ls kanban-work/expeditions/EXP-$ARGUMENTS*.md 2>/dev/null || ls kanban-work/expeditions/EXP-$ARGUMENTS*.md
```

Read the expedition file and extract:
- **tags**: Determine required test types (`standard-tests`, `live-being-tests`)
- **status**: Current kanban status
- **branch**: Associated branch name

### 2. Check Test Coverage

Based on expedition tags, verify tests exist:

#### If `standard-tests` tag (or no tags = default):
```bash
# Find unit/integration tests for this expedition
find . -name "test_*$ARGUMENTS*.py" -o -name "test_exp$ARGUMENTS*.py" | grep -v __pycache__

# Run standard tests
pytest brain/tests/ -v --tb=short 2>&1 | tail -50
```

#### If `live-being-tests` tag:
```bash
# Find CLI-first live tests
ls live-being-tests/test_*$ARGUMENTS*.py 2>/dev/null
ls live-being-tests/test_exp$ARGUMENTS*.py 2>/dev/null

# Run live being tests (may need specific being)
pytest live-being-tests/test_*$ARGUMENTS*.py -v --tb=short 2>&1 | tail -50
```

### 3. Check Documentation

Verify related docs were updated:

```bash
# What files changed in this branch vs main?
git diff --name-only main...HEAD | grep -E '\.(md|rst)$'

# Check if expedition doc was updated
git diff --name-only main...HEAD | grep -i "exp.*$ARGUMENTS"
```

**Documentation checklist:**
- [ ] Expedition doc updated with completion notes
- [ ] README updated if user-facing changes
- [ ] API docs updated if new endpoints

### 4. Generate Review Report

Output a structured report:

```
## Review: EXP-$ARGUMENTS

### Test Coverage
| Type | Required | Found | Status |
|------|----------|-------|--------|
| Standard (unit/integration) | Yes/No | X files | PASS/FAIL/MISSING |
| Live Being Tests | Yes/No | X files | PASS/FAIL/MISSING |

### Documentation
| Doc | Updated | Notes |
|-----|---------|-------|
| Expedition doc | Yes/No | ... |
| README | Yes/No | ... |
| Other | Yes/No | ... |

### Merge Readiness
- [ ] All required tests pass
- [ ] Documentation updated
- [ ] Branch up to date with main
- [ ] No merge conflicts

### Recommendation
READY TO MERGE / NEEDS WORK: [specific issues]
```

### 5. If Ready: Offer to Merge

If all checks pass, offer to:

```bash
# Update branch with main
git fetch origin main
git rebase origin/main

# Merge to main
git checkout main
git merge --no-ff exp-$ARGUMENTS-branch -m "Merge EXP-$ARGUMENTS: Title"

# Push
git push origin main

# Update kanban
yurtle-kanban move EXP-$ARGUMENTS done

# Delete feature branch (optional, not expedition branches)
git branch -d exp-$ARGUMENTS-branch
```

### 6. If Not Ready: List Action Items

Create a checklist of what needs to be done:

```
## Action Items for EXP-$ARGUMENTS

- [ ] Add unit tests for [specific module]
- [ ] Add live-being-tests for [specific feature]
- [ ] Update expedition doc with [missing section]
- [ ] Fix failing test: [test name]
```
