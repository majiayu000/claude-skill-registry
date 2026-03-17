---
name: weekly-report
description: Generate comprehensive weekly progress reports for AINative platform. Use when (1) Creating end-of-week status reports, (2) Summarizing commits and features, (3) Documenting bug fixes and improvements, (4) Tracking sprint progress, (5) Preparing stakeholder updates. Analyzes git commits, GitHub issues, and PRs to produce structured markdown reports.
---

# Weekly Report Generation

Generate comprehensive weekly progress reports that summarize development activity across all AINative repositories.

## Report Structure

### Required Sections

1. **Executive Summary** - High-level overview of the week
2. **Developer Velocity** - Week-over-week metrics, trends, productivity analysis
3. **Major Features Implemented** - New functionality with commit refs
4. **Critical Bug Fixes** - Issues resolved with root cause analysis
5. **Security Improvements** - Vulnerability fixes, hardening
6. **Infrastructure & DevOps** - Deployment, configuration changes
7. **Frontend Improvements** - UI/UX changes across web apps
8. **Work In Progress** - Ongoing work, backlog updates
9. **Commit Statistics** - Quantitative analysis
10. **Success Metrics** - KPIs and feature completion tracking
11. **Next Week Priorities** - Upcoming focus areas

## Data Collection Process

### Step 1: Load User Identities

```bash
# Load all your git identities from config
if [ -f .claude/user-identities.json ]; then
    # Extract all git emails
    GIT_EMAILS=$(cat .claude/user-identities.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('|'.join(data['git_emails']))
")
    PRIMARY_NAME=$(cat .claude/user-identities.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data['primary_name'])
")
    GH_USERNAMES=$(cat .claude/user-identities.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(', '.join(['@' + u for u in data['github_usernames']]))
")
    echo "Generating weekly report for: $PRIMARY_NAME"
    echo "Tracking emails: $GIT_EMAILS"
    echo "GitHub accounts: $GH_USERNAMES"
else
    # Fallback to current git user
    GIT_EMAILS=$(git config user.email)
    PRIMARY_NAME=$(git config user.name)
    GH_USERNAMES="@$(gh api user --jq .login)"
    echo "Generating weekly report for: $PRIMARY_NAME <$GIT_EMAILS>"
    echo "GitHub: $GH_USERNAMES"
fi
```

### Step 2: Gather YOUR Git Commits (From ALL Identities)

```bash
# Build author filter for ALL your emails
# Format: --author="email1" --author="email2" --author="email3"
AUTHOR_FILTER=$(echo "$GIT_EMAILS" | tr '|' '\n' | sed 's/^/--author="/; s/$/"/' | tr '\n' ' ')

# Get YOUR commits from the past week (ALL identities)
git log $AUTHOR_FILTER --since="7 days ago" --pretty=format:"%h %s (%ae)" --no-merges | head -100

# Count YOUR commits by date (ALL identities)
git log $AUTHOR_FILTER --since="7 days ago" --format="%ad" --date=short | sort | uniq -c

# Total YOUR commit count (ALL identities)
git log $AUTHOR_FILTER --since="7 days ago" --no-merges --oneline | wc -l

# Files YOU modified (ALL identities)
git log $AUTHOR_FILTER --since="7 days ago" --name-only --pretty=format: | sort -u | wc -l

# Breakdown by email identity
echo "$GIT_EMAILS" | tr '|' '\n' | while read email; do
    count=$(git log --author="$email" --since="7 days ago" --no-merges --oneline | wc -l)
    echo "$email: $count commits"
done
```

### Step 3: Gather Issues Assigned to YOU

```bash
# Issues assigned to YOU that were closed this week
gh issue list --assignee="@me" --state closed --limit 100 --json number,title,closedAt,labels

# All issues assigned to YOU
gh issue list --assignee="@me" --state all --limit 100 --json number,title,state,createdAt,updatedAt

# Get issue details for YOUR assigned issues
gh issue view <issue-number>
```

### Step 4: Analyze YOUR PRs

```bash
# PRs created by YOU that were merged this week
gh pr list --author="@me" --state merged --limit 50 --json number,title,mergedAt

# All PRs created by YOU
gh pr list --author="@me" --state all --limit 50 --json number,title,state,createdAt

# Get PR details
gh pr view <pr-number>
```

### Step 5: Calculate Weekly Developer Velocity (YOUR velocity only)

```bash
# This week's commit count (all your identities)
THIS_WEEK_COMMITS=$(git log $AUTHOR_FILTER --since="7 days ago" --no-merges --oneline | wc -l | tr -d ' ')

# Last week's commit count (all your identities)
LAST_WEEK_COMMITS=$(git log $AUTHOR_FILTER --since="14 days ago" --until="7 days ago" --no-merges --oneline | wc -l | tr -d ' ')

# Daily average this week
DAILY_AVG=$(echo "scale=1; $THIS_WEEK_COMMITS / 7" | bc)

# Last 4 weeks commit counts (all your identities)
for week in {0..3}; do
  start_days=$((week * 7))
  end_days=$(((week + 1) * 7))
  WEEK_COUNT=$(git log $AUTHOR_FILTER --since="$end_days days ago" --until="$start_days days ago" --no-merges --oneline | wc -l | tr -d ' ')
  echo "Week -$week: $WEEK_COUNT commits"
done

# 4-week moving average (all your identities)
FOUR_WEEK_COMMITS=$(git log $AUTHOR_FILTER --since="28 days ago" --no-merges --oneline | wc -l | tr -d ' ')
FOUR_WEEK_AVG=$(echo "scale=1; $FOUR_WEEK_COMMITS / 4" | bc)

# Issues closed this week (assigned to you)
ISSUES_CLOSED_WEEK=$(gh issue list --assignee="@me" --state closed --search "closed:>=$(date -d '7 days ago' +%Y-%m-%d)" --json number --jq 'length')

# PRs merged this week (created by you)
PRS_MERGED_WEEK=$(gh pr list --author="@me" --state merged --search "merged:>=$(date -d '7 days ago' +%Y-%m-%d)" --json number --jq 'length')

# Calculate week-over-week change
if [ "$LAST_WEEK_COMMITS" -gt 0 ]; then
  WOW_CHANGE=$(echo "scale=1; (($THIS_WEEK_COMMITS - $LAST_WEEK_COMMITS) / $LAST_WEEK_COMMITS) * 100" | bc)
else
  WOW_CHANGE="N/A"
fi

# Velocity trend vs 4-week average
if [ "$THIS_WEEK_COMMITS" -gt "$FOUR_WEEK_AVG" ]; then
  VELOCITY_TREND="📈 Trending Up"
elif [ "$THIS_WEEK_COMMITS" -lt "$FOUR_WEEK_AVG" ]; then
  VELOCITY_TREND="📉 Trending Down"
else
  VELOCITY_TREND="➡️ Stable"
fi

# Weekly velocity score (weighted: commits * 1 + issues * 5 + PRs * 8)
WEEKLY_VELOCITY_SCORE=$(echo "$THIS_WEEK_COMMITS * 1 + $ISSUES_CLOSED_WEEK * 5 + $PRS_MERGED_WEEK * 8" | bc)

# Productivity rating based on real historical benchmarks (urbantech profile, last year)
# Benchmarks derived from percentile analysis:
# - Exceptional: 90th percentile (46+ commits/week, 100+ velocity points)
# - Strong: 75th percentile (23+ commits/week, 60+ velocity points)
# - Good: 50th percentile (11+ commits/week, 30+ velocity points)
# - Light: Below median (<11 commits/week, <30 velocity points)
if [ "$WEEKLY_VELOCITY_SCORE" -ge 100 ] && [ "$THIS_WEEK_COMMITS" -ge 46 ]; then
  PRODUCTIVITY_RATING="🔥 Exceptional (top 10%)"
elif [ "$WEEKLY_VELOCITY_SCORE" -ge 60 ] && [ "$THIS_WEEK_COMMITS" -ge 23 ]; then
  PRODUCTIVITY_RATING="⭐ Strong (top 25%)"
elif [ "$WEEKLY_VELOCITY_SCORE" -ge 30 ] && [ "$THIS_WEEK_COMMITS" -ge 11 ]; then
  PRODUCTIVITY_RATING="✅ Good (above median)"
else
  PRODUCTIVITY_RATING="⚠️ Light Week (below median)"
fi
```

**Note**: This report tracks only YOUR contributions (commits, issues assigned to you, PRs you created).

## Report Template

```markdown
# AINative Platform - Weekly Progress Report
## [Start Date] - [End Date]

**Developer**: [Git User Name] <[git.email]>
**GitHub**: @[username]
**Period**: 7 days

**Note**: This report contains only YOUR commits, issues assigned to YOU, and PRs created by YOU.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Developer Velocity](#developer-velocity)
3. [Major Features Implemented](#major-features-implemented)
4. [Critical Bug Fixes](#critical-bug-fixes)
5. [Security Improvements](#security-improvements)
6. [Infrastructure & DevOps](#infrastructure--devops)
7. [Frontend Improvements](#frontend-improvements)
8. [Work In Progress](#work-in-progress)
9. [Commit Statistics](#commit-statistics)
10. [Success Metrics](#success-metrics)
11. [Next Week Priorities](#next-week-priorities)

---

## Executive Summary

This reporting period you made **[X] commits** across [N] repositories. Your major accomplishments include:

- **[Feature 1]**: Brief description
- **[Feature 2]**: Brief description
- **[Bug Fix]**: Brief description
- **[Security]**: Brief description

**Your Status**: [Overall assessment of your work]

**Note**: This summary reflects only YOUR contributions. For team-wide reports, see the project manager's consolidated report.

---

## Developer Velocity

**Weekly Productivity Overview**:
- Total Commits: 47
- Issues Closed: 8
- PRs Merged: 5
- Velocity Score: 87 points (commits×1 + issues×5 + PRs×8)
- Productivity Rating: ⭐ Strong (top 25%)

**Week-over-Week Comparison**:
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Commits | 47 | 38 | +23.7% 📈 |
| Issues Closed | 8 | 5 | +60% 📈 |
| PRs Merged | 5 | 3 | +66.7% 📈 |
| Daily Avg | 6.7 commits/day | 5.4 commits/day | +24% |

**4-Week Velocity Trend**:
```
Week -3  Week -2  Week -1  This Week
  32       38       42        47      📈 Trending Up
```

**Monthly Analysis**:
- 4-Week Average: 39.8 commits/week
- This Week vs 4-Week Avg: +18% above average
- Velocity Trend: 📈 Trending Up
- Consistency Score: Strong (steady growth pattern)

**Daily Activity Pattern** (This Week):
| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|-----|-----|-----|-----|-----|-----|-----|
| 8   | 9   | 7   | 10  | 6   | 4   | 3   |

**Velocity Benchmarks** (based on last year's data):
- 🔥 Exceptional: 46+ commits/week, 100+ velocity points (top 10%)
- ⭐ Strong: 23+ commits/week, 60+ velocity points (top 25%)
- ✅ Good: 11+ commits/week, 30+ velocity points (above median)
- ⚠️ Light: <11 commits/week, <30 velocity points (below median)

**Velocity Insights**:
- You're operating 18% above your 4-week moving average
- Sustained productivity increase over the past 4 weeks (+47% since week -3)
- Strong output on weekdays with consistent weekend contributions
- Issues and PRs completion rate significantly improved (+60%+ on both metrics)
- This week's 47 commits puts you in Strong territory, approaching Exceptional levels

---

## Major Features Implemented

### 1. [Feature Name]
**Commits**: [commit_hash1, commit_hash2]
**Status**: Complete/In Progress
**Story Points**: [X]

#### Problem Solved:
[Description of what problem this feature addresses]

#### Implementation Details:

**Backend** (`src/backend/app/services/`):
- `service_file.py` - Description of service

**API Endpoints** (`src/backend/app/api/v1/endpoints/`):
- `endpoint.py` - Description of endpoint

**Impact**: HIGH/MEDIUM/LOW - [Why this matters]

---

## Critical Bug Fixes

### 1. [Bug Title] (CRITICAL/HIGH/MEDIUM/LOW)
**Commit**: [commit_hash]
**Issue #[number]**: [Brief description]

**Root Causes**:
1. [Cause 1]
2. [Cause 2]

**Fixes**:
- [What was fixed]
- [How it was fixed]

**Impact**: [Effect of the fix]

---

## Security Improvements

### 1. [Security Issue Title]
**Commits**: [commit_hashes]
**Issues**: #[numbers]

#### Vulnerabilities Fixed:
- **[Package]**: [Vulnerability type] (SEVERITY)

**Impact**: [Security improvement]

---

## Infrastructure & DevOps

### 1. [Infrastructure Change]
**Commits**: [commit_hashes]

**Changes**:
- [Change 1]
- [Change 2]

---

## Frontend Improvements

### [App Name] ([X] commits)

#### 1. [Improvement Title]
**Commits**: [commit_hashes]

**Changes**:
- [Change 1]
- [Change 2]

---

## Work In Progress

### [Feature/Project Name]
**Issues**: #[range]
**Status**: [Current status]

[Description of ongoing work]

---

## Commit Statistics

**Your Total Commits**: [X]
**Period**: [Start Date] - [End Date] ([N] days)
**Your Daily Average**: [X] commits/day
**Files You Modified**: [Y]

**Your Commits by Repository**:
| Repository | Your Commits | Focus Area |
|------------|--------------|------------|
| AINative-Studio/core | [X] | [Focus] |
| relycapital/AINative-website | [X] | [Focus] |

**Your Commit Categories**:
| Type | Count | Percentage |
|------|-------|------------|
| Features | [X] | [X]% |
| Bug Fixes | [X] | [X]% |
| Security | [X] | [X]% |
| Tests | [X] | [X]% |
| DevOps | [X] | [X]% |
| Docs | [X] | [X]% |

**Note**: Statistics show only commits authored by you (`git log --author="your@email.com"`).

**Commits by Date**:
| Date | Commits | Key Changes |
|------|---------|-------------|
| [Date] | [X] | [Summary] |

---

## Success Metrics

### Technical Metrics

| Metric | Target | Status |
|--------|--------|--------|
| [Metric 1] | [Target] | Achieved/Pending |

### Feature Completion

| Feature | Status | Impact |
|---------|--------|--------|
| [Feature] | Complete/In Progress | CRITICAL/HIGH/MEDIUM/LOW |

---

## Next Week Priorities

1. **[Priority 1]**: [Description]
2. **[Priority 2]**: [Description]
3. **[Priority 3]**: [Description]

---

## Document Version

**Version**: 1.0
**Date**: [Date]
**Author**: [Username]
**Status**: Ready for Review

---

*End of Weekly Progress Report*
```

## File Naming Convention

```
docs/reports/WEEKLY_REPORT_YYYY-MM-DD_username.md
```

Example: `WEEKLY_REPORT_2026-01-04_ranveerd11.md`

## Quality Checklist

Before finalizing the report:

- [ ] All commits from the week are analyzed
- [ ] GitHub issues are linked with # notation
- [ ] Commit hashes are included for traceability
- [ ] Impact levels (CRITICAL/HIGH/MEDIUM/LOW) assigned
- [ ] Statistics are accurate
- [ ] Next week priorities are actionable
- [ ] No sensitive data (credentials, PII) included
- [ ] File placed in `docs/reports/` directory

## Repositories to Include

1. **AINative-Studio/core** - Main backend and API
2. **relycapital/AINative-website** - Marketing website
3. **urbantech/live.ainative.studio** - Live streaming platform
4. **AINative-Studio/chatwoot-zerodb** - Customer support integration

## Categorizing Commits

| Prefix/Keywords | Category |
|-----------------|----------|
| feat, add, implement | Features |
| fix, resolve, correct | Bug Fixes |
| security, CVE, vulnerability | Security |
| test, spec, coverage | Tests |
| deploy, CI, CD, config | DevOps |
| doc, readme, comment | Docs |
| refactor, clean, optimize | Refactor |

## Impact Assessment

- **CRITICAL**: Core functionality, data integrity, security vulnerabilities
- **HIGH**: Major features, significant bug fixes, performance improvements
- **MEDIUM**: Enhancements, moderate fixes, integrations
- **LOW**: Minor fixes, UI polish, documentation

## Example Usage

```bash
# Invoke the weekly report skill
/weekly-report

# Generate report for specific date range
/weekly-report --start 2026-01-01 --end 2026-01-07

# Generate report for specific author
/weekly-report --author ranveerd11
```
