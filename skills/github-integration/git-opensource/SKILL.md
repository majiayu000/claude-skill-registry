---
name: git-opensource
description: Git workflows, GitHub management, and open source community building
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 02-community-builder
bond_type: SECONDARY_BOND
---

# Git & Open Source for DevRel

Manage **GitHub repositories** and build **open source communities**.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - task_type: enum[repo_setup, issue_triage, pr_review, release, community]
    - repository: string
  optional:
    - priority: enum[low, medium, high, critical]
    - labels: array[string]
```

### Output
```yaml
output:
  result:
    actions_taken: array[string]
    status: enum[completed, pending, escalated]
    next_steps: array[Action]
```

## GitHub for DevRel

### Repository Management
```
Repository
├── README.md           # First impression
├── CONTRIBUTING.md     # How to contribute
├── CODE_OF_CONDUCT.md  # Community standards
├── LICENSE             # Usage rights
├── .github/
│   ├── ISSUE_TEMPLATE/ # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/      # CI/CD
└── docs/               # Documentation
```

### Issue Management

| Label | Purpose | Color |
|-------|---------|-------|
| bug | Something broken | red |
| enhancement | New feature | blue |
| good first issue | Beginner friendly | green |
| help wanted | Need contributors | yellow |
| documentation | Docs related | purple |

### Issue Triage Workflow
```
New Issue → Label → Prioritize → Assign → Track
    ↓          ↓          ↓          ↓        ↓
 Template   Category   Severity   Owner    Milestone
```

## Open Source Community

### Contribution Funnel
```
Star → Issue → Discussion → PR → Maintainer
  ↓      ↓         ↓         ↓        ↓
Watch  Report   Engage   Contribute  Lead
```

### Growing Contributors
1. **Good first issues** - Curated beginner tasks
2. **Clear contributing guide** - Lower barriers
3. **Fast response times** - Keep momentum
4. **Recognition** - Thank contributors publicly
5. **Mentorship** - Help people level up

## GitHub Discussions

### Channel Structure
```
Discussions
├── Announcements    # Official news
├── Q&A              # Support questions
├── Ideas            # Feature requests
├── Show and Tell    # Community projects
└── General          # Everything else
```

## Release Management

### Semantic Versioning
```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  # Bug fix
1.0.1 → 1.1.0  # New feature
1.1.0 → 2.0.0  # Breaking change
```

### Changelog Format
```markdown
## [1.2.0] - 2024-01-15

### Added
- New authentication method

### Changed
- Improved error messages

### Fixed
- Rate limiting issue (#123)
```

## Metrics to Track

| Metric | Meaning |
|--------|---------|
| Stars | Interest |
| Forks | Intent to use/contribute |
| Issues open/closed | Health |
| PR velocity | Activity |
| Contributors | Community size |

## Retry Logic

```yaml
retry_patterns:
  stale_issues:
    strategy: "Ping author, close if no response"
    timeout: 14d

  failed_ci:
    strategy: "Identify flaky tests, rerun"
    max_retries: 2

  merge_conflicts:
    strategy: "Rebase on main, resolve"
    fallback: "Request author update"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| PR backlog | Growing queue | Triage sprint |
| Inactive contributors | No recent activity | Re-engage or remove |
| CI failures | Red builds | Fix or skip flaky |

## Debug Checklist

```
□ README clear and current?
□ Contributing guide complete?
□ Issue templates working?
□ CI/CD pipeline healthy?
□ Labels organized?
□ Milestones up to date?
```

## Test Template

```yaml
test_git_opensource:
  unit_tests:
    - test_repo_structure:
        assert: "All required files present"
    - test_ci_pipeline:
        assert: "Builds pass on main"

  integration_tests:
    - test_contribution_flow:
        assert: "Fork-clone-PR works"
```

## Observability

```yaml
metrics:
  - issues_closed: integer
  - prs_merged: integer
  - contributor_count: integer
  - response_time_avg: duration
```

See `assets/` for GitHub templates.
