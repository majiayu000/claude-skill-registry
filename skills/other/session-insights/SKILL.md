---
name: session-insights
description: Analyze past Claude Code sessions to extract patterns, metrics, and recommendations.
---

# Session Insights

Analyze the current project's Claude Code usage patterns and generate actionable recommendations.

## Step 1: Gather session data

Collect data from available sources in the current project:

1. **Session metrics** — `~/.claude/metrics/{project-slug}/*.json` (structured JSON from session-report hook)
2. **CLAUDE_ERRORS.md** — error frequency by Area and Type
3. **Git log** — files most frequently modified in commits mentioning "fix", "bug", "error"
4. **.claude/agent-memory/** — learnings accumulated by agents
5. **Registry history** — audit score trend from `$DOTFORGE_DIR/registry/projects.yml`

If a source doesn't exist, skip it and note as "unavailable".

### Retroactive Analysis (no session metrics yet)

When `~/.claude/metrics/{project-slug}/` is empty or doesn't exist, reconstruct a pseudo-historical picture:

1. **CLAUDE_ERRORS.md** → parse dates and group errors by week/month to show trends
2. **Git log** → `git log --name-only --since="60 days ago"` to identify:
   - Hot files (most frequently changed)
   - Fix frequency (`git log --grep="fix" --oneline | wc -l`)
   - Commit cadence by week
3. **Registry history** → score progression over time
4. **Rule glob coverage** → cross-reference `git log --name-only` against `.claude/rules/*.md` globs to estimate historical rule coverage

Mark all retroactive data clearly as:
```
⚠ Inferred from git history — no session metrics available yet.
   Session metrics will accumulate automatically after /forge sync.
```

## Step 2: Compute metrics

From available data, calculate:

### Session Metrics (from ~/.claude/metrics/)
When JSON metrics files exist, aggregate across the last N sessions (default 20):
- **Total sessions**: count of metric files
- **Avg files touched**: mean files_touched per session
- **Avg hook blocks**: mean hook_blocks + lint_blocks (lower is better — team is learning)
- **Rule coverage trend**: plot rule_coverage over time (improving / stable / declining)
- **Error rate**: errors_added / sessions (target: < 0.5)

### Error Patterns
- **Top error areas**: group CLAUDE_ERRORS.md entries by Area, rank by count
- **Error types distribution**: count by Type (syntax, logic, integration, config, security)
- **Repeat offenders**: areas with 3+ errors (candidates for rule creation)

### File Activity
- **Hot files**: top 10 most-edited files (from git log)
- **Churn rate**: files edited > 5 times in last 30 days (may need refactoring)
- **Untested hot files**: hot files without corresponding test files

### Agent Usage (from agent-memory/)
- **Active agents**: which agents have accumulated learnings
- **Top learnings**: most recent entries per agent
- **Gaps**: agents with memory enabled but no learnings (underused)

### Score Trend (from registry)
- **Current score**: latest audit score
- **Trend**: improving, stable, or declining (compare last 3 audits)
- **Projected**: if declining, estimate when score drops below 7.0

## Step 3: Generate recommendations

Based on metrics, produce actionable recommendations:

1. **Repeat errors** → suggest creating a rule in `.claude/rules/` targeting that area
2. **Hot untested files** → suggest test creation
3. **Score declining** → suggest `/forge sync` to update configuration
4. **Underused agents** → suggest delegation patterns for common tasks
5. **High churn files** → suggest refactoring or better abstractions

## Step 4: Feed practices pipeline

For the top 3 most impactful recommendations:
1. Check if a practice already exists in `$DOTFORGE_DIR/practices/inbox/` or `active/`
2. If not, create a practice in `practices/inbox/`:
   - `source_type: session-insights`
   - `tags: [insights, <area>]`
3. Report which practices were created

## Step 5: Generate report

Output format:
```
═══ SESSION INSIGHTS: {{project}} ═══
Fecha: {{YYYY-MM-DD}}
Data sources: {{list of available sources}}

── SESSION METRICS ──
Sessions tracked: {{N}} (since {{first date}})
Avg files/session: {{N}} | Avg commits/session: {{N}}
Hook blocks: {{N}} destructive, {{N}} lint (total across sessions)
Rule coverage: {{trend}} ({{current}}% — last 5: {{values}})
Error rate: {{N}} errors/session
{{if retroactive: "⚠ Inferred from git history"}}

── ERROR PATTERNS ──
Top areas: {{area}} ({{count}} errors), ...
Type distribution: logic {{N}}, config {{N}}, ...
Repeat offenders: {{areas with 3+ errors}}

── FILE ACTIVITY ──
Hot files (last 30 days):
  1. {{file}} — {{N}} edits
  2. ...
Untested hot files: {{list or "none"}}
High churn (>5 edits): {{list or "none"}}

── AGENT USAGE ──
Active: {{agents with learnings}}
Underused: {{agents with empty memory}}

── SCORE TREND ──
Current: {{score}}/10
Trend: {{improving|stable|declining}} ({{last 3 scores}})

── RECOMMENDATIONS ──
1. {{recommendation}} — impact: {{high|medium|low}}
2. ...

── PRACTICES CREATED ──
{{list of new practices or "none"}}
```
