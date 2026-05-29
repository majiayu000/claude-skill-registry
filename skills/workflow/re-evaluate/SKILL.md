---
name: re-evaluate
description: Re-evaluate attempt repositories after issues are closed, update evaluation reports, and file new issues for any regressions or newly discovered problems.
type: anthropic-skill
version: "1.2"
---

# Re-Evaluate Attempt After Changes

## Overview
This SOP monitors attempt repositories for closed issues and code changes, re-runs
relevant evaluations, updates the main evaluation report, and files new issues for
any regressions or newly discovered problems.

## Parameters
- **attempt_repo** (required): Repository name (e.g., `2025-12-13-python-claude-hive`)
- **evaluation_path** (optional, default: `./results/{attempt_repo}.md`): Path to existing evaluation report
- **full_reeval** (optional, default: `false`): If true, run complete evaluation instead of targeted checks

## Steps

### 1. Check Repository for Changes
Determine if the repository has changed since the last evaluation.

**Constraints:**
- You MUST check for new commits since last evaluation
- You MUST identify closed issues that triggered changes
- You MUST NOT proceed if no changes detected (unless full_reeval=true)

```bash
# Navigate to existing clone or re-clone
cd ./reviews/{attempt_repo} || gh repo clone brazil-bench/{attempt_repo} ./reviews/{attempt_repo}

# Fetch latest changes
git fetch origin

# Check for new commits on main/master
git log HEAD..origin/main --oneline 2>/dev/null || git log HEAD..origin/master --oneline

# Pull latest changes
git pull origin main 2>/dev/null || git pull origin master

# Get the latest commit info
git log -1 --format="%H %ai %s"
```

### 2. Identify Closed Issues
List issues that have been closed since the last evaluation.

**Constraints:**
- You MUST fetch all closed issues from the repo
- You MUST categorize issues by type ([Missing], [Test Quality], [Docs], etc.)
- You SHOULD note which issues were addressed vs closed without fix

```bash
# List all closed issues
gh issue list -R brazil-bench/{attempt_repo} --state closed --json number,title,closedAt,labels

# Get details of recently closed issues
gh issue list -R brazil-bench/{attempt_repo} --state closed --limit 20 --json number,title,body,closedAt

# Check issue comments for resolution notes
gh issue view {issue_number} -R brazil-bench/{attempt_repo} --json comments
```

**Issue Categories to Track:**

| Issue Type | Re-evaluation Focus |
|------------|---------------------|
| `[Missing]` | Re-check spec compliance for that requirement |
| `[Test Quality]` | Re-run tests, recalculate skip ratio, **check integration tests are self-contained** |
| `[Docs]` | Re-check README for required elements |
| `[Quality]` | Re-review architecture/code quality |
| `[Compliance]` | Full spec compliance re-check |

**ALWAYS Check (regardless of issue type):**
- Integration tests must run without skipping due to missing dependencies
- Tests should use testcontainers or pytest-docker to manage data stores

### 3. Targeted Re-Evaluation
Based on closed issues, re-evaluate only the affected areas.

**Constraints:**
- You MUST re-evaluate areas corresponding to closed issues
- You MUST use the same methodology as the original evaluation
- You SHOULD skip unchanged areas unless full_reeval=true

#### 3a. Re-Evaluate Missing Requirements
For closed `[Missing]` issues:

```bash
# Read the original issue to understand what was missing
gh issue view {issue_number} -R brazil-bench/{attempt_repo}

# Check if the requirement is now implemented
# Search for relevant code changes
git diff {old_commit}..HEAD --stat

# Search for specific implementations
grep -r "{feature_keyword}" ./reviews/{attempt_repo}/src/
```

**Verification Checklist:**
- [ ] Code implementing the requirement exists
- [ ] Tests covering the requirement pass
- [ ] Integration with existing code is complete

#### 3b. Re-Evaluate Test Quality
For closed `[Test Quality]` issues:

```bash
cd ./reviews/{attempt_repo}

# Re-run tests to get current status
pytest --tb=no -v 2>&1 | grep -E "(PASSED|FAILED|SKIPPED|ERROR)" | head -100

# Get summary counts
pytest --tb=no -q 2>&1 | tail -5

# Recalculate skip ratio
pytest --collect-only -q 2>&1 | tail -3
```

**Metrics to Update:**
| Metric | Before | After |
|--------|--------|-------|
| Total Tests | | |
| Passed | | |
| Skipped | | |
| Skip Ratio | | |

#### 3c. Re-Evaluate Documentation
For closed `[Docs]` issues:

```bash
# Check README for required elements
head -150 ./reviews/{attempt_repo}/README.md

# Look for setup instructions
grep -E "Setup|Install|Prerequisites" ./reviews/{attempt_repo}/README.md

# Look for MCP server setup
grep -E "MCP|claude|server" ./reviews/{attempt_repo}/README.md

# Look for example Q&A
grep -E "Example|Question|Query|Usage" ./reviews/{attempt_repo}/README.md
```

**Documentation Checklist:**
- [ ] Setup Instructions present
- [ ] MCP Server Setup documented
- [ ] Example Q&A included

#### 3d. Re-Evaluate Spec Compliance
For closed `[Compliance]` issues or major changes:

```bash
# Read the spec requirements
cat ./tasks/beads/spec.md | grep -E "^##|^-"

# Check implementation against each requirement
# (Follow evaluate-attempt SOP Step 6)
```

#### 3e. Re-Evaluate Integration Test Quality (REQUIRED)
**ALWAYS check this** - integration tests must be self-contained and actually run.

```bash
cd ./reviews/{attempt_repo}

# Check if integration tests still skip due to missing dependencies
pytest --tb=no -v 2>&1 | grep -E "SKIPPED.*neo4j|SKIPPED.*database|SKIPPED.*not running"

# Check for testcontainers usage (good pattern)
grep -r "testcontainers\|Neo4jContainer\|DockerContainer" tests/ --include="*.py"

# Check for pytest-docker usage (good pattern)
grep -r "pytest-docker\|docker_compose_file" tests/ pyproject.toml

# Check for skip patterns that indicate external dependency issues
grep -r "pytest.skip.*neo4j\|pytest.skip.*database\|skipif.*connection" tests/ --include="*.py"

# Run tests and count integration test results
pytest -v tests/ 2>&1 | grep -E "integration|Integration" | head -20
```

**Self-Contained Test Verification:**

| Check | Command | Expected |
|-------|---------|----------|
| Uses testcontainers | `grep -r "testcontainers" tests/` | Has matches |
| No external skips | `grep "pytest.skip.*not running"` | No matches |
| Integration tests run | `pytest -v` output | 0 skipped for Neo4j |
| Docker fixture exists | `grep "Neo4jContainer" conftest.py` | Has matches |

**If Integration Tests Still Skip:**

File a new issue using the template from file-issues SOP section 3d-integration:
- Title: `[Test Quality] Integration tests must be self-contained - use testcontainers`
- Label: `bug`
- Include testcontainers code examples in issue body

**Scoring Impact:**

| Integration Test State | Score Modifier |
|----------------------|----------------|
| Self-contained (testcontainers/docker) | No penalty |
| In-memory mock (not persistent) | -10 points quality |
| Skips due to missing dependency | -10 points quality |
| No integration tests | -15 points quality |

**Skipped Test Policy:**
- ANY skipped test requires an issue to be filed
- Zero tolerance for skips - all tests must run and pass
- File separate issue for each category of skip

**Document in Report:**

```markdown
## Integration Test Quality

| Aspect | Status |
|--------|--------|
| Self-contained | Yes/No |
| Pattern used | testcontainers / pytest-docker / mock / external |
| Integration tests that run | X passed |
| Integration tests that skip | Y skipped |

{If skips exist}
⚠️ **Issue:** Integration tests skip when dependencies not running.
New issue filed: #{issue_number}
```

### 4. Update Evaluation Report
Update the existing evaluation report with new findings.

**Constraints:**
- You MUST preserve the original report structure
- You MUST add a "Re-Evaluation History" section
- You MUST update metrics that have changed
- You MUST timestamp each re-evaluation

**Report Update Template:**

```markdown
## Re-Evaluation History

### {DATE} - Re-evaluation after issue fixes

**Closed Issues Addressed:**
- #{issue_number}: {title} - {resolution}

**Updated Metrics:**
| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Spec Compliance | X/16 | Y/16 | +N |
| Skip Ratio | X% | Y% | -N% |
| Tests Passed | X | Y | +N |

**Changes Summary:**
{description of what changed}

**New Score:** {updated_score}
```

**Update Commands:**
```bash
# Read existing report
cat ./results/{attempt_repo}.md

# Create backup before modifying
cp ./results/{attempt_repo}.md ./results/{attempt_repo}.md.bak

# Update the report (use Edit tool)
# - Update Summary metrics
# - Update Requirements Checklist
# - Add Re-Evaluation History entry
```

### 5. Recalculate Benchmark Score
If metrics changed, recalculate the overall benchmark score.

**Constraints:**
- You MUST use the same scoring formula as compare-attempts SOP
- You MUST update the README leaderboard if rank changes
- You SHOULD note score changes in re-evaluation history

**Scoring Formula (from compare-attempts):**
```
Base Score = (Compliance/16 * 40) + (Effective_Tests * 0.5) + (1/Duration * 10)

Skip Penalty = -5 if Skip_Ratio > 10%

Final Score = Base Score + Skip Penalty
```

```bash
# Check current leaderboard
cat ./README.md | grep -A 20 "Leaderboard"

# Calculate new score
# (Apply formula with updated metrics)

# Update leaderboard if needed
# (Use Edit tool to update README.md)
```

### 6. File New Issues (If Needed)
If re-evaluation discovers new problems or regressions, file new issues.

**Constraints:**
- You MUST check for regressions (things that worked before but don't now)
- You MUST file issues for any new problems discovered
- You MUST NOT re-file issues that are still open
- You SHOULD reference the re-evaluation in issue body

**Regression Detection:**
```bash
# Compare test results
# If tests that passed before now fail, that's a regression

# Compare spec compliance
# If requirements that were met are now missing, that's a regression

# Compare code metrics
# Significant increases in complexity or decreases in coverage are concerns
```

**New Issue Template:**
```bash
gh issue create -R brazil-bench/{attempt_repo} \
  --title "[Regression] {description}" \
  --label "bug" \
  --body "$(cat <<'EOF'
## Issue

This regression was discovered during re-evaluation on {DATE}.

## Previous State
{what was working before}

## Current State
{what is broken now}

## Commits Involved
{commits between evaluations}

## Suggested Fix
{recommendation}

---
Discovered during re-evaluation: [results/{attempt_repo}.md](https://github.com/brazil-bench/pourpoise/blob/main/results/{attempt_repo}.md)
EOF
)"
```

### 7. Generate Summary
Output a summary of the re-evaluation results.

**Constraints:**
- You MUST list all closed issues that were verified
- You MUST note any metric changes
- You MUST note any new issues filed
- You MUST indicate if leaderboard position changed

**Output Format:**
```markdown
# Re-Evaluation Summary: {attempt_repo}

## Date
{YYYY-MM-DD}

## Closed Issues Verified
| Issue | Title | Status |
|-------|-------|--------|
| #1 | [Missing] MCP server | Verified Fixed |
| #2 | [Test Quality] Skip ratio | Verified Improved |
| #3 | [Docs] README | Partially Fixed |

## Metric Changes
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Spec Compliance | 13/16 | 15/16 | +2 |
| Skip Ratio | 25% | 8% | -17% |
| Benchmark Score | 45.2 | 52.8 | +7.6 |

## Leaderboard Impact
- Previous Rank: #4
- New Rank: #2

## New Issues Filed
| Issue | Title | Reason |
|-------|-------|--------|
| #5 | [Regression] Test X fails | Broken by commit abc123 |

## Report Updated
./results/{attempt_repo}.md

## Next Steps
{recommendations for remaining issues}
```

## Automation Tips

### Scheduled Re-Evaluation
To check all repos for changes:

```bash
# List all attempt repos
gh repo list brazil-bench --limit 50 --json name | jq -r '.[].name' | grep -E "^20[0-9]{2}-"

# For each repo, check for closed issues since last check
for repo in $(gh repo list brazil-bench --limit 50 --json name -q '.[].name' | grep -E "^20[0-9]{2}-"); do
  closed=$(gh issue list -R brazil-bench/$repo --state closed --json closedAt -q 'length')
  if [ "$closed" -gt 0 ]; then
    echo "$repo has $closed closed issues - needs re-evaluation"
  fi
done
```

### Webhook Trigger
Consider setting up a GitHub Action that triggers re-evaluation when:
- An issue is closed
- A PR is merged
- A commit is pushed to main

## Troubleshooting

**No changes detected but issues were closed**
- Issues may have been closed without fixes (won't fix, duplicate)
- Check issue comments for resolution type
- Use `--full_reeval` to force complete re-evaluation

**Tests fail during re-evaluation**
- Ensure dependencies are available (Neo4j, etc.)
- Check if new dependencies were added
- Review docker-compose or setup instructions for changes

**Score decreased after fixes**
- Possible regression introduced
- New skip patterns added
- Check diff between commits carefully

**Can't update leaderboard**
- Verify you have write access to pourpoise repo
- Check that README.md format hasn't changed
- Manually verify score calculations

## Examples

### Example 1: Re-evaluate after MCP server implementation

```bash
# User request
re-evaluate 2025-12-13-python-claude-hive

# Expected workflow:
# 1. Pull latest changes
# 2. Verify #1 [Missing] MCP server is now implemented
# 3. Update spec compliance from 13/16 to 14/16
# 4. Update evaluation report
# 5. Recalculate score
# 6. Update leaderboard if rank changed
```

### Example 2: Re-evaluate after test quality improvements

```bash
# User request
re-evaluate 2025-12-14-python-claude-beads-2

# Expected workflow:
# 1. Pull latest changes
# 2. Re-run tests to get new skip ratio
# 3. Verify skip ratio dropped from 20% to <10%
# 4. Remove skip penalty from score
# 5. Update evaluation report
# 6. Update leaderboard
```

### Example 3: Full re-evaluation

```bash
# User request
re-evaluate 2025-09-30-python-swarm --full-reeval

# Expected workflow:
# 1. Pull latest changes
# 2. Run complete evaluation (all steps from evaluate-attempt SOP)
# 3. Compare all metrics to previous evaluation
# 4. Update report with comprehensive re-evaluation
# 5. File issues for any new problems found
```
