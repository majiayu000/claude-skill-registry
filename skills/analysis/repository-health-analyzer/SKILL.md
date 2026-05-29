---
name: repository-health-analyzer
version: "1.0.0"
category: coordination
description: "Repository Health Analyzer"
---

# Repository Health Analyzer

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Category:** workspace-hub
> **Related Skills:** repo-sync, compliance-check, knowledge-base-system

## Overview

Analyzes health metrics across all 26+ repositories. Provides unified health scores, identifies issues, and generates actionable reports.

## Health Dimensions

### 1. Git Health (30 points)
- Clean working directory
- Up to date with remote
- No merge conflicts
- Branch strategy followed

### 2. Code Quality (25 points)
- Test coverage ≥80%
- No lint errors
- Documentation present
- Type annotations (if applicable)

### 3. Compliance (25 points)
- CLAUDE.md present
- Agent OS structure
- Git hooks installed
- Standards followed

### 4. Activity (10 points)
- Recent commits (< 30 days)
- Active development
- Regular updates

### 5. Dependencies (10 points)
- No security vulnerabilities
- Up-to-date dependencies
- No deprecated packages

**Total:** 100 points

## Quick Health Check

```bash
# Check single repository
./scripts/monitoring/check_repo_health.sh digitalmodel

# Check all repositories
./scripts/monitoring/check_all_repos.sh

# Generate health report
./scripts/monitoring/generate_health_report.sh
```

## Health Analysis Script

```python
#!/usr/bin/env python3
# scripts/monitoring/analyze_repo_health.py

import subprocess
from pathlib import Path
import json
from datetime import datetime, timedelta

def analyze_repository(repo_path):
    """Analyze repository health."""
    health = {
        "repository": repo_path.name,
        "timestamp": datetime.now().isoformat(),
        "scores": {},
        "total_score": 0,
        "grade": "F",
        "issues": [],
        "recommendations": []
    }

    # Git Health (30 points)
    health["scores"]["git"] = check_git_health(repo_path)

    # Code Quality (25 points)
    health["scores"]["quality"] = check_code_quality(repo_path)

    # Compliance (25 points)
    health["scores"]["compliance"] = check_compliance(repo_path)

    # Activity (10 points)
    health["scores"]["activity"] = check_activity(repo_path)

    # Dependencies (10 points)
    health["scores"]["dependencies"] = check_dependencies(repo_path)

    # Calculate total
    health["total_score"] = sum(health["scores"].values())

    # Assign grade
    health["grade"] = calculate_grade(health["total_score"])

    return health

def check_git_health(repo_path):
    """Check git health (max 30 points)."""
    score = 30

    # Check for uncommitted changes
    result = subprocess.run(
        ["git", "-C", str(repo_path), "status", "--porcelain"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        score -= 10

    # Check if up to date with remote
    result = subprocess.run(
        ["git", "-C", str(repo_path), "status"],
        capture_output=True, text=True
    )
    if "behind" in result.stdout:
        score -= 10

    # Check for merge conflicts
    if "unmerged" in result.stdout:
        score -= 10

    return max(0, score)

def check_code_quality(repo_path):
    """Check code quality (max 25 points)."""
    score = 25

    # Check test coverage
    coverage_file = repo_path / ".coverage"
    if not coverage_file.exists():
        score -= 15
    else:
        # Parse coverage (simplified)
        # In reality, run pytest --cov and parse results
        pass

    # Check for lint errors
    # Run linter and check results
    # score -= errors * 2

    # Check documentation
    docs_dir = repo_path / "docs"
    if not docs_dir.exists() or not list(docs_dir.glob("*.md")):
        score -= 5

    return max(0, score)

def check_compliance(repo_path):
    """Check compliance (max 25 points)."""
    score = 25

    # CLAUDE.md
    if not (repo_path / "CLAUDE.md").exists():
        score -= 10

    # Agent OS structure
    if not (repo_path / ".agent-os/product").exists():
        score -= 10

    # Git hooks
    if not (repo_path / ".git/hooks/pre-commit").exists():
        score -= 5

    return max(0, score)

def check_activity(repo_path):
    """Check activity (max 10 points)."""
    result = subprocess.run(
        ["git", "-C", str(repo_path), "log", "-1", "--format=%ci"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        last_commit = datetime.fromisoformat(result.stdout.strip().split()[0])
        days_ago = (datetime.now() - last_commit).days

        if days_ago <= 7:
            return 10
        elif days_ago <= 30:
            return 7
        elif days_ago <= 90:
            return 4
        else:
            return 0

    return 0

def check_dependencies(repo_path):
    """Check dependencies (max 10 points)."""
    score = 10

    # Check for uv.lock or package-lock.json
    if (repo_path / "uv.lock").exists():
        # Check for outdated dependencies
        # In reality, run `uv lock --check` or similar
        pass
    elif (repo_path / "package-lock.json").exists():
        # Check npm dependencies
        pass
    else:
        score -= 5

    return max(0, score)

def calculate_grade(score):
    """Calculate letter grade from score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

if __name__ == "__main__":
    repos_file = Path("config/repos.conf")
    repos = [line.split('=')[0] for line in repos_file.read_text().split('\n')
             if line and not line.startswith('#')]

    all_health = []

    for repo_name in repos:
        repo_path = Path(repo_name)
        if repo_path.exists():
            health = analyze_repository(repo_path)
            all_health.append(health)

            print(f"{repo_name}: {health['total_score']}/100 ({health['grade']})")

    # Generate report
    report_path = Path("reports/health/repository_health.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(all_health, indent=2))

    print(f"\n✓ Health report saved to {report_path}")
```

## Health Dashboard

### Console Dashboard

```
Repository Health Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Health: 82/100 (B)

Top Performers:
1. digitalmodel          95/100 (A) ✓
2. worldenergydata       92/100 (A) ✓
3. aceengineer-admin     89/100 (B) ✓

Needs Attention:
1. repo-alpha            65/100 (D) ⚠
2. repo-beta             58/100 (F) ✗
3. repo-gamma            61/100 (D) ⚠

Critical Issues:
- 3 repos with uncommitted changes
- 2 repos missing CLAUDE.md
- 1 repo behind remote by 15 commits
- 4 repos with test coverage < 80%

Recommendations:
1. Update CLAUDE.md in 2 repositories
2. Commit and push pending changes in 3 repositories
3. Improve test coverage in 4 repositories
4. Install git hooks in 5 repositories
```

### HTML Dashboard

```python
def generate_html_dashboard(health_data):
    """Generate interactive HTML dashboard."""
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Overall scores
    df = pd.DataFrame(health_data)

    # Score distribution
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Score Distribution', 'Health by Dimension',
                       'Timeline', 'Top Issues'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'scatter'}, {'type': 'table'}]]
    )

    # Score distribution
    fig.add_trace(
        go.Bar(x=df['repository'], y=df['total_score'],
               name='Health Score'),
        row=1, col=1
    )

    # Health by dimension
    dimensions = ['git', 'quality', 'compliance', 'activity', 'dependencies']
    for dim in dimensions:
        fig.add_trace(
            go.Bar(x=df['repository'],
                   y=[s['scores'][dim] for s in health_data],
                   name=dim),
            row=1, col=2
        )

    # Save dashboard
    fig.write_html('reports/health/dashboard.html',
                   include_plotlyjs='cdn')
```

## Issue Detection

```python
def detect_issues(health_data):
    """Detect and categorize issues."""
    issues = {
        "critical": [],
        "warning": [],
        "info": []
    }

    for repo in health_data:
        # Critical issues (score < 60)
        if repo["total_score"] < 60:
            issues["critical"].append({
                "repo": repo["repository"],
                "issue": f"Overall health score {repo['total_score']}/100",
                "recommendation": "Review all health dimensions"
            })

        # Missing compliance
        if repo["scores"]["compliance"] < 15:
            issues["critical"].append({
                "repo": repo["repository"],
                "issue": "Missing critical compliance files",
                "recommendation": "Run compliance setup script"
            })

        # Low test coverage
        if repo["scores"]["quality"] < 15:
            issues["warning"].append({
                "repo": repo["repository"],
                "issue": "Low test coverage",
                "recommendation": "Increase test coverage to 80%+"
            })

        # Inactive repository
        if repo["scores"]["activity"] == 0:
            issues["info"].append({
                "repo": repo["repository"],
                "issue": "No commits in 90+ days",
                "recommendation": "Archive if no longer active"
            })

    return issues
```

## Automated Monitoring

### Scheduled Health Checks

```yaml
# .github/workflows/health-check.yml
name: Repository Health Check

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Health Analysis
        run: python scripts/monitoring/analyze_repo_health.py

      - name: Generate Dashboard
        run: python scripts/monitoring/generate_dashboard.py

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: health-report
          path: reports/health/
```

### Alerting

```python
def send_alerts(issues):
    """Send alerts for critical issues."""
    if issues["critical"]:
        # Send email/Slack notification
        message = f"CRITICAL: {len(issues['critical'])} health issues detected"

        for issue in issues["critical"]:
            message += f"\n- {issue['repo']}: {issue['issue']}"

        send_notification(message)
```

## Integration

```bash
# Check health before major operations
./scripts/repository_sync commit all

# If health check fails
if ! ./scripts/monitoring/check_all_repos.sh; then
    echo "Health check failed. Fix issues before proceeding."
    exit 1
fi
```

---

**Monitor health across all repositories with unified metrics!** 📊
