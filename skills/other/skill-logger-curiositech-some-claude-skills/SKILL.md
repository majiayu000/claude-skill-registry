---
name: skill-logger
description: Logs and scores skill usage quality, tracking output effectiveness, user satisfaction signals, and improvement opportunities. Expert in skill analytics, quality metrics, feedback loops, and continuous improvement. Activate on "skill logging", "skill quality", "skill analytics", "skill scoring", "skill performance", "skill metrics", "track skill usage", "skill improvement". NOT for creating skills (use agent-creator), skill documentation (use skill-coach), or runtime debugging (use debugger skills).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
category: Productivity & Meta
tags:
  - logging
  - analytics
  - metrics
  - quality
  - improvement
pairs-with:
  - skill: automatic-stateful-prompt-improver
    reason: Data for prompt optimization
  - skill: skill-coach
    reason: Quality tracking feeds coaching
---

# Skill Logger

Track, measure, and improve skill quality through systematic logging and scoring.

## When to Use This Skill

**Use for:**
- Setting up skill usage logging
- Defining quality metrics for skill outputs
- Analyzing skill performance over time
- Identifying skills that need improvement
- Building feedback loops for skill enhancement
- A/B testing skill variations

**NOT for:**
- Creating new skills → use agent-creator
- Skill documentation → use skill-coach
- Runtime debugging → use appropriate debugger skills
- General logging/monitoring → use devops-automator

## Core Logging Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    SKILL LOGGING PIPELINE                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CAPTURE          2. ANALYZE           3. SCORE              │
│  ├─ Invocation       ├─ Output parse      ├─ Quality metrics    │
│  ├─ Input context    ├─ Token usage       ├─ User satisfaction  │
│  ├─ Output           ├─ Tool calls        ├─ Goal completion    │
│  └─ Timing           └─ Error patterns    └─ Efficiency         │
│                                                                 │
│  4. AGGREGATE        5. ALERT             6. IMPROVE            │
│  ├─ Per-skill stats  ├─ Quality drops     ├─ Identify patterns  │
│  ├─ Trend analysis   ├─ Error spikes      ├─ Suggest changes    │
│  └─ Comparisons      └─ Underuse          └─ Track experiments  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## What to Log

### Invocation Data

```json
{
  "invocation_id": "uuid",
  "timestamp": "ISO8601",
  "skill_name": "wedding-immortalist",
  "skill_version": "1.2.0",

  "input": {
    "user_query": "Create a 3D model from my wedding photos",
    "context_tokens": 1500,
    "files_referenced": ["photos/", "config.json"]
  },

  "execution": {
    "duration_ms": 45000,
    "tool_calls": [
      {"tool": "Bash", "count": 5},
      {"tool": "Write", "count": 3}
    ],
    "tokens_used": {
      "input": 8500,
      "output": 3200
    },
    "errors": []
  },

  "output": {
    "type": "code_generation",
    "artifacts_created": ["pipeline.py", "config.yaml"],
    "response_length": 3200
  }
}
```

### Quality Signals

```python
QUALITY_SIGNALS = {
    # Implicit signals (automated)
    'completion': 'Did the skill complete without errors?',
    'token_efficiency': 'Output quality per token used',
    'tool_success_rate': 'Tool calls that succeeded',
    'retry_count': 'How many retries needed?',

    # Explicit signals (user feedback)
    'user_edit_ratio': 'How much did user modify output?',
    'user_accepted': 'Did user accept/use the output?',
    'follow_up_needed': 'Did user need to ask for fixes?',
    'explicit_rating': 'Thumbs up/down if available',

    # Outcome signals (delayed)
    'code_ran_successfully': 'Did generated code work?',
    'tests_passed': 'Did it pass tests?',
    'reverted': 'Was the output later reverted?',
}
```

## Scoring Framework

### Multi-Dimensional Quality Score

```python
def calculate_skill_score(invocation_log):
    """Score a skill invocation 0-100."""

    scores = {
        # Completion (25%)
        'completion': (
            25 if invocation_log['errors'] == [] else
            15 if invocation_log['recovered'] else
            0
        ),

        # Efficiency (20%)
        'efficiency': min(20, 20 * (
            BASELINE_TOKENS / invocation_log['tokens_used']
        )),

        # Output Quality (30%)
        'quality': (
            30 if invocation_log['user_accepted'] else
            20 if invocation_log['user_edit_ratio'] < 0.2 else
            10 if invocation_log['user_edit_ratio'] < 0.5 else
            0
        ),

        # User Satisfaction (25%)
        'satisfaction': (
            25 if invocation_log['explicit_rating'] == 'positive' else
            15 if invocation_log['no_follow_up'] else
            5 if invocation_log['follow_up_resolved'] else
            0
        ),
    }

    return sum(scores.values())
```

### Score Interpretation

| Score Range | Quality Level | Action |
|-------------|---------------|--------|
| 90-100 | Excellent | Document as exemplar |
| 75-89 | Good | Monitor for consistency |
| 50-74 | Acceptable | Review for improvements |
| 25-49 | Poor | Prioritize fixes |
| 0-24 | Failing | Immediate intervention |

## Log Storage Schema

### SQLite Schema (Local)

```sql
CREATE TABLE skill_invocations (
    id TEXT PRIMARY KEY,
    skill_name TEXT NOT NULL,
    skill_version TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Input
    user_query TEXT,
    context_tokens INTEGER,

    -- Execution
    duration_ms INTEGER,
    tokens_input INTEGER,
    tokens_output INTEGER,
    tool_calls_json TEXT,
    errors_json TEXT,

    -- Output
    output_type TEXT,
    artifacts_json TEXT,
    response_length INTEGER,

    -- Quality signals
    user_accepted BOOLEAN,
    user_edit_ratio REAL,
    follow_up_needed BOOLEAN,
    explicit_rating TEXT,

    -- Computed
    quality_score REAL,

    INDEX idx_skill_name (skill_name),
    INDEX idx_timestamp (timestamp),
    INDEX idx_quality (quality_score)
);

CREATE TABLE skill_aggregates (
    skill_name TEXT,
    period TEXT,  -- 'daily', 'weekly', 'monthly'
    period_start DATE,

    invocation_count INTEGER,
    avg_quality_score REAL,
    error_rate REAL,
    avg_tokens_used INTEGER,
    avg_duration_ms INTEGER,

    PRIMARY KEY (skill_name, period, period_start)
);
```

### JSON Log Format (Portable)

```json
{
  "logs_version": "1.0",
  "skill_name": "wedding-immortalist",
  "entries": [
    {
      "id": "uuid",
      "timestamp": "2025-01-15T14:30:00Z",
      "input": {...},
      "execution": {...},
      "output": {...},
      "quality": {
        "signals": {...},
        "score": 85,
        "computed_at": "2025-01-15T14:35:00Z"
      }
    }
  ]
}
```

## Analytics Queries

### Skill Performance Dashboard

```sql
-- Overall skill rankings
SELECT
    skill_name,
    COUNT(*) as uses,
    AVG(quality_score) as avg_quality,
    AVG(tokens_output) as avg_tokens,
    SUM(CASE WHEN errors_json != '[]' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as error_rate
FROM skill_invocations
WHERE timestamp > datetime('now', '-30 days')
GROUP BY skill_name
ORDER BY avg_quality DESC;

-- Quality trend (weekly)
SELECT
    skill_name,
    strftime('%Y-%W', timestamp) as week,
    AVG(quality_score) as avg_quality,
    COUNT(*) as uses
FROM skill_invocations
GROUP BY skill_name, week
ORDER BY skill_name, week;

-- Problem detection
SELECT skill_name, COUNT(*) as failures
FROM skill_invocations
WHERE quality_score < 50
  AND timestamp > datetime('now', '-7 days')
GROUP BY skill_name
HAVING failures >= 3
ORDER BY failures DESC;
```

### Improvement Opportunities

```python
def identify_improvement_opportunities(skill_name, logs):
    """Analyze logs to suggest skill improvements."""

    opportunities = []

    # Pattern 1: Common follow-up questions
    follow_ups = extract_follow_up_patterns(logs)
    if follow_ups:
        opportunities.append({
            'type': 'missing_capability',
            'description': f'Users frequently ask: {follow_ups[0]}',
            'suggestion': 'Add guidance for this common need'
        })

    # Pattern 2: High edit ratio in specific output types
    edit_patterns = analyze_edit_patterns(logs)
    if edit_patterns['code'] > 0.4:
        opportunities.append({
            'type': 'code_quality',
            'description': 'Users frequently edit generated code',
            'suggestion': 'Review code examples and templates'
        })

    # Pattern 3: Repeated errors
    error_patterns = cluster_errors(logs)
    for error_type, count in error_patterns:
        if count >= 3:
            opportunities.append({
                'type': 'recurring_error',
                'description': f'{error_type} occurred {count} times',
                'suggestion': 'Add error handling or documentation'
            })

    return opportunities
```

## Implementation Guide

### Basic Logger Hook

```python
# hooks/skill_logger.py
import json
import sqlite3
from datetime import datetime
from pathlib import Path

LOG_DB = Path.home() / '.claude' / 'skill_logs.db'

def log_skill_invocation(
    skill_name: str,
    user_query: str,
    output: str,
    tool_calls: list,
    duration_ms: int,
    tokens: dict,
    errors: list = None
):
    """Log a skill invocation to the database."""

    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO skill_invocations
        (id, skill_name, timestamp, user_query, duration_ms,
         tokens_input, tokens_output, tool_calls_json, errors_json,
         response_length)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(uuid.uuid4()),
        skill_name,
        datetime.utcnow().isoformat(),
        user_query,
        duration_ms,
        tokens.get('input', 0),
        tokens.get('output', 0),
        json.dumps(tool_calls),
        json.dumps(errors or []),
        len(output)
    ))

    conn.commit()
    conn.close()
```

### Quality Signal Collection

```python
def collect_quality_signals(invocation_id: str, signals: dict):
    """Update an invocation with quality signals."""

    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()

    # Update with user feedback
    cursor.execute('''
        UPDATE skill_invocations
        SET user_accepted = ?,
            user_edit_ratio = ?,
            follow_up_needed = ?,
            explicit_rating = ?,
            quality_score = ?
        WHERE id = ?
    ''', (
        signals.get('accepted'),
        signals.get('edit_ratio'),
        signals.get('follow_up'),
        signals.get('rating'),
        calculate_score(signals),
        invocation_id
    ))

    conn.commit()
    conn.close()
```

## Alerting & Notifications

### Alert Conditions

```python
ALERT_CONDITIONS = {
    'quality_drop': {
        'condition': 'avg_quality_7d < avg_quality_30d * 0.8',
        'message': 'Skill {skill} quality dropped 20%+ in past week',
        'severity': 'warning'
    },
    'error_spike': {
        'condition': 'error_rate_24h > error_rate_7d * 2',
        'message': 'Skill {skill} error rate doubled in past 24h',
        'severity': 'critical'
    },
    'underused': {
        'condition': 'uses_7d < uses_30d_avg * 0.5',
        'message': 'Skill {skill} usage down 50%+ this week',
        'severity': 'info'
    },
    'high_performer': {
        'condition': 'avg_quality_7d > 90 AND uses_7d > 10',
        'message': 'Skill {skill} performing excellently',
        'severity': 'positive'
    }
}
```

## Anti-Patterns

### "Log Everything"
**Wrong**: Logging complete input/output for every invocation.
**Why**: Privacy concerns, storage explosion, noise.
**Right**: Log metadata, summaries, and opt-in detailed logging.

### "Score Once, Forget"
**Wrong**: Calculating quality score immediately after completion.
**Why**: Misses delayed signals (did code work? was it reverted?).
**Right**: Collect signals over time, recalculate periodically.

### "Averages Only"
**Wrong**: Only tracking average quality scores.
**Why**: Hides distribution, misses failure modes.
**Right**: Track percentiles, failure rates, and patterns.

### "No Baseline"
**Wrong**: Measuring quality without establishing baselines.
**Why**: Can't detect improvement or regression.
**Right**: Establish baselines per skill, compare trends.

## Output Reports

### Weekly Skill Health Report

```markdown
# Skill Health Report - Week of 2025-01-13

## Overview
- Total invocations: 247
- Average quality: 78.3 (up 2.1 from last week)
- Error rate: 4.2% (down 1.8%)

## Top Performers
1. **wedding-immortalist** - 92.1 avg quality, 18 uses
2. **skill-coach** - 89.4 avg quality, 34 uses
3. **api-architect** - 87.2 avg quality, 22 uses

## Needs Attention
1. **legacy-code-converter** - 52.3 avg quality (down 15%)
   - Common issue: Missing dependency detection
   - Suggested fix: Add dependency scanning step

## Improvement Opportunities
- `partner-text-coach`: Users frequently ask for tone adjustment
- `yard-landscaper`: High edit ratio on plant recommendations
```

## Integration Points

- **skill-coach**: Feed quality data for skill improvements
- **agent-creator**: Use metrics when designing new skills
- **automatic-stateful-prompt-improver**: Quality signals for prompt optimization

---

**Core Philosophy**: What gets measured gets improved. Skill logging transforms intuition about skill quality into actionable data, enabling continuous improvement of the entire skill ecosystem.
