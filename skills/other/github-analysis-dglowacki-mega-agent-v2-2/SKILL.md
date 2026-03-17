---
name: github-analysis
description: Analyze GitHub commits, generate PR reviews, calculate contributor leaderboards, and assess code quality. Use when analyzing git commits, reviewing code, generating GitHub activity reports, or tracking developer contributions.
---

# GitHub Analysis

Analyze GitHub activity, review code, and track contributions.

## Quick Start

Analyze commits from JSON file:
```bash
python scripts/analyze_commits.py commits.json
```

Generate leaderboard:
```bash
python scripts/calculate_leaderboard.py commits.json --period week
```

## Commit Analysis

### What to Extract

From each commit, analyze:
- **Author & timestamp**
- **Commit message quality**
  - Clear (explains what and why)
  - Vague (just what, no why)
  - Cryptic (no context)
- **Files changed** (count and types)
- **Lines added/removed**
- **Code quality indicators**
  - TODOs added
  - FIXMEs added
  - Console.log/debugging code
  - Commented code
  - Large file changes (>500 lines)

### Quality Scoring

**Commit Message Quality:**
- Excellent (8-10): Clear what + why, follows conventions
- Good (5-7): Clear what, some context
- Poor (1-4): Vague or no context
- Bad (0): Single word, "wip", "test"

**Code Quality Indicators:**
```bash
# Check for debugging code
grep -r "console.log\|debugger\|print(" changed_files/

# Check for TODOs
grep -r "TODO\|FIXME" changed_files/ | wc -l

# Check for commented code
grep -r "^[[:space:]]*//.*=\|^[[:space:]]*/\*" changed_files/
```

## PR Review Template

Use this structure for code reviews:

```markdown
# Pull Request Review

## Summary
[1-2 sentence overview of changes]

## Code Quality Assessment

### Structure & Organization
- ✅ **Good**: Well-organized, clear separation of concerns
- ⚠️  **Needs Work**: Mixed responsibilities, unclear structure
- 🔴 **Issues**: Significant structural problems

### Naming & Readability
- **Variables**: [clear/unclear/inconsistent]
- **Functions**: [descriptive/vague/confusing]
- **Comments**: [helpful/missing/outdated]

### Testing
- [ ] Unit tests included
- [ ] Integration tests updated
- [ ] Edge cases covered
- [ ] Test coverage: [%]

## Issues Found

### 🔴 Critical
- [Issue with security/correctness impact]

### 🟡 Warnings
- [Issue that should be addressed]

### 🔵 Suggestions
- [Nice-to-have improvements]

## Security Check

- [ ] No hardcoded credentials
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization correct

## Performance

- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Appropriate caching

## Recommendations

1. [Priority recommendation]
2. [Additional improvement]
3. [Nice-to-have enhancement]

## Verdict

- [ ] ✅ **Approve** - Ready to merge
- [ ] 🟡 **Approve with Comments** - Minor issues, can merge
- [ ] 🔴 **Request Changes** - Must address issues before merge
```

## Contributor Leaderboard

### Metrics

Track these metrics per contributor:

1. **Commit Count** (weight: 1x)
2. **Lines Changed** (weight: 0.5x)
   - Added lines + modified lines
3. **Commit Quality** (weight: 2x)
   - Average message quality score
4. **PR Reviews** (weight: 1.5x)
   - Number of PR reviews contributed
5. **Response Time** (weight: 1x)
   - Average time to respond to PR comments

### Scoring Formula

```
Total Score = (commits × 1) +
              (lines_changed / 100 × 0.5) +
              (avg_quality × 2) +
              (pr_reviews × 1.5) +
              (10 - avg_response_hours × 1)
```

### Leaderboard Format

```markdown
# GitHub Contributor Leaderboard
## Period: [Week/Month]

| Rank | Contributor | Score | Commits | Lines | Quality | Reviews |
|------|-------------|-------|---------|-------|---------|---------|
| 1    | John Doe    | 45.2  | 12      | 1,234 | 8.5     | 5       |
| 2    | Jane Smith  | 38.7  | 10      | 987   | 7.8     | 4       |
```

## Code Quality Metrics

### Complexity Analysis

```bash
# Count function complexity (rough estimate)
# Functions with >4 nested levels or >50 lines
grep -n "function\|def " file.js | while read line; do
    # Analyze complexity
done
```

### Code Churn

Files with high churn (changed frequently):
```bash
git log --format=format: --name-only | \
    sort | uniq -c | sort -rn | head -20
```

High churn may indicate:
- Unstable code
- Unclear requirements
- Technical debt
- Active development area

### Test Coverage

```bash
# Run test coverage (example)
npm test -- --coverage
python -m pytest --cov=src tests/
```

Good coverage targets:
- Critical paths: 90%+
- Business logic: 80%+
- Overall: 70%+

## Data Processing

### Input Format (commits.json)

```json
[
  {
    "sha": "abc123",
    "author": "John Doe",
    "email": "john@example.com",
    "date": "2026-01-04T10:30:00Z",
    "message": "Add user authentication feature",
    "files_changed": ["src/auth.js", "src/users.js"],
    "additions": 125,
    "deletions": 45,
    "files_count": 2
  }
]
```

### Output Format (analysis.json)

```json
{
  "summary": {
    "total_commits": 25,
    "total_contributors": 5,
    "total_files_changed": 67,
    "total_lines": 2345
  },
  "contributors": [
    {
      "name": "John Doe",
      "commits": 12,
      "lines_changed": 1234,
      "avg_quality": 8.5,
      "score": 45.2
    }
  ],
  "hot_files": [
    {"file": "src/auth.js", "changes": 8}
  ],
  "quality_issues": [
    {"type": "TODO", "count": 5},
    {"type": "console.log", "count": 3}
  ]
}
```

## Scripts

### analyze_commits.py

Analyzes commit data and generates metrics.

**Usage:**
```bash
python scripts/analyze_commits.py input.json --output analysis.json
```

### calculate_leaderboard.py

Calculates contributor rankings.

**Usage:**
```bash
python scripts/calculate_leaderboard.py commits.json \
    --period week \
    --output leaderboard.json
```

### generate_report.py

Generates HTML report from analysis.

**Usage:**
```bash
python scripts/generate_report.py analysis.json \
    --template github-summary \
    --output report.html
```

## Integration with Agents

### Code Agent

```python
# Get commits from GitHub
commits = github.get_commits(repo='owner/repo', days=7)

# Analyze with skill
python scripts/analyze_commits.py commits.json
```

### Reporting Agent

```python
# Generate leaderboard
python scripts/calculate_leaderboard.py commits.json

# Create HTML report
python scripts/generate_report.py analysis.json --template github-summary
```

## Reference Files

- [metrics.md](reference/metrics.md) - Detailed scoring algorithms
- [patterns.md](reference/patterns.md) - Code quality patterns to detect
- [templates.md](reference/templates.md) - Additional report templates
