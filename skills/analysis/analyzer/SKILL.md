---
name: analyzer
description: >
  Comprehensive codebase analysis methodology for existing projects.
  Use when onboarding to a new codebase, doing periodic health checks, or before refactoring.
---

# Kodo Analyzer Skill

Comprehensive codebase analysis methodology for existing projects.

## Purpose

The Kodo Analyzer system provides systematic codebase analysis to:
- Infer and document existing features
- Identify gaps, bugs, and security issues
- Calculate health scores per category
- Generate actionable recommendations
- Track health trends over time

## When to Use

- New project onboarding (existing codebase)
- Periodic health checks
- Pre-refactoring assessment
- Security audits
- Documentation generation
- Before major releases

## Architecture

```
+-------------------------------------+
|     /kodo analyze Command           |
+-----------------+-------------------+
                  |
+-----------------v-------------------+
|   kodo-codebase-analyzer (Main)     |
|   - Orchestrates sub-agents         |
|   - Aggregates results              |
|   - Calculates health scores        |
+-----------------+-------------------+
                  |
    +-------------+-------------+
    |             |             |
+---v---+   +----v----+   +---v---+
| Group |   |  Group  |   | Group |
|   1   |   |    2    |   |   3   |
+---+---+   +----+----+   +---+---+
    |            |            |
+---v-------+ +--v--------+ +v------------+
| database  | | deps      | | security    |
| api       | | analytics | | performance |
| frontend  | | docs      | |             |
+-----------+ +-----------+ +-------------+
```

## Analysis Categories

### 1. Database Analysis
- Schema quality and relationships
- RLS policy coverage
- Index optimization
- Unused table/column detection
- Migration health

### 2. API Analysis
- Endpoint inventory
- Authentication coverage
- Error handling patterns
- Edge function candidates
- Documentation gaps

### 3. Frontend Analysis
- Component inventory
- Accessibility compliance
- State management patterns
- Performance concerns
- UI consistency

### 4. Dependencies Analysis
- Outdated packages
- Security vulnerabilities
- Better alternatives
- Unused dependencies
- License compliance

### 5. Analytics Analysis
- Event coverage
- Naming consistency
- Feature flag usage
- Funnel completeness
- User identification

### 6. Documentation Analysis
- Coverage assessment
- Code-doc accuracy
- Staleness detection
- Quality metrics

### 7. Security Analysis
- Authentication flows
- Authorization patterns
- Input validation
- Secrets management
- CORS configuration

### 8. Performance Analysis
- Database query optimization
- Bundle size analysis
- Caching strategies
- Render performance
- Asset optimization

## Output Structure

```
./docs/analysis/
├── summary.md           # Executive summary
├── database/
│   └── report.md
├── api/
│   └── report.md
├── frontend/
│   └── report.md
├── dependencies/
│   └── report.md
├── analytics/
│   └── report.md
├── documentation/
│   └── report.md
├── security/
│   └── report.md
└── performance/
    └── report.md
```

## Health Scoring

See `references/health-scoring.md` for detailed methodology.

| Category | Weight | Score Factors |
|----------|--------|---------------|
| Database | 15% | RLS, indexes, unused detection |
| API | 15% | Auth, errors, documentation |
| Frontend | 15% | A11y, states, performance |
| Dependencies | 10% | Freshness, security |
| Analytics | 10% | Coverage, consistency |
| Documentation | 10% | Coverage, accuracy |
| Security | 15% | Auth, validation, secrets |
| Performance | 10% | Queries, bundles, caching |

## Issue Classification

See `references/issue-categories.md` for severity definitions.

- **Critical**: Security vulnerabilities, data loss risks
- **High**: Bugs, missing auth, accessibility failures
- **Medium**: Performance issues, code quality
- **Low**: Style inconsistencies, minor improvements

## Workflow

### Step 1: Initialize
```bash
kodo analyze              # Standard analysis
kodo analyze --deep       # Deep mode: extract full content + learnings from docs/
kodo analyze --deep --auto  # Auto-accept all findings
```

**Deep Mode** (`--deep`): In addition to standard analysis, extracts learnings from documentation:
- Scans `docs/` directory recursively
- Extracts rules, decisions, tech-stack choices, workflows, domain terms, conventions
- Creates context entries in `.kodo/context-tree/`
- Creates learnings in `.kodo/learnings/` (grouped by category)
- Assigns HIGH confidence to your design docs (`docs/plans/`), MEDIUM to inherited docs

### Step 2: Review Summary
Check overall health score and critical issues.

### Step 3: Drill Down
Review individual category reports in `./docs/analysis/`.

### Step 4: Prioritize
Use the prioritization matrix:
- High Impact + Low Effort = Do First
- Critical issues = Immediate attention

### Step 5: Track Progress
```bash
# Store in context for trend tracking
kodo curate --category analysis --title "Health Report $(date)"
```

### Step 6: Re-analyze
Run periodic analyses to track improvement:
```bash
kodo analyze --quick  # Weekly
kodo analyze          # Monthly
```

## Integration

### Kodo Context Storage
Analysis results are stored in `.kodo/context/analysis/`:
```bash
# Query previous analyses
kodo query "health score"
kodo query "security issues"
kodo query "performance bottlenecks"
```

### Feature Documentation
Analysis can infer features and populate `./docs/features/`:
```bash
kodo analyze  # Also generates feature docs
```

### Configuration
Set analysis preferences in `.kodo/config.json`:
```json
{
  "analyzer": {
    "analyzers": {
      "database": { "enabled": true },
      "api": { "enabled": true },
      "frontend": { "enabled": true },
      "dependencies": { "enabled": true },
      "analytics": { "enabled": true },
      "documentation": { "enabled": true },
      "security": { "enabled": true },
      "performance": { "enabled": true }
    },
    "output": {
      "directory": "./docs/analysis",
      "populateFeatureDocs": true
    },
    "thresholds": {
      "critical": 50,
      "warning": 70
    }
  }
}
```

## Best Practices

1. **Run full analysis on new projects** - Establish baseline
2. **Run quick analysis weekly** - Catch regressions
3. **Fix critical issues immediately** - Security first
4. **Review recommendations** - Not all apply
5. **Track health trends** - Compare over time
6. **Focus on high-impact fixes** - Use prioritization matrix

## Agent Model Assignments

| Agent | Model | Reason |
|-------|-------|--------|
| kodo-codebase-analyzer | sonnet | Orchestration, complex decisions |
| kodo-security-analyzer | sonnet | Critical security analysis |
| kodo-performance-analyzer | sonnet | Complex performance patterns |
| kodo-database-analyzer | haiku | Straightforward schema analysis |
| kodo-api-analyzer | haiku | Pattern-based endpoint analysis |
| kodo-frontend-analyzer | haiku | Component scanning |
| kodo-dependencies-analyzer | haiku | Package checking |
| kodo-posthog-analyzer | haiku | Event tracking analysis |
| kodo-documentation-analyzer | haiku | Doc coverage checking |

## Related Commands

- `/kodo analyze` - Run analysis
- `/kodo analyze --deep` - Run analysis with full content extraction + learnings
- `/kodo extract <file>` - Extract learnings from a single file
- `/kodo curate` - Store analysis in context
- `/kodo query` - Search previous analyses
- `/kodo reflect` - Capture learnings from analysis

## References

- `references/health-scoring.md` - Score calculation methodology
- `references/issue-categories.md` - Issue severity definitions
- `references/analysis-templates.md` - Output templates
