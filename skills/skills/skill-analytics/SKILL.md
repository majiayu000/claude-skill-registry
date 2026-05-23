---
name: skill-analytics
description: Track skill usage patterns, most-used skills, token savings, and skill health metrics.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"📊","requires":{"bins":[]}}}
---

# /skill-analytics - Track Usage Patterns

**Know what works.** Track which skills you use most, token savings, and skill health.

---

## When To Use

User says:
- `/skill-analytics` or `/analytics`
- "show skill stats"
- "most used skills"
- "skill usage report"
- "token savings"
- "unused skills"

---

## How It Works

**Track usage in beads:**
1. Log each skill invocation to `.beads/skill_usage.json`
2. Track metadata: skill name, timestamp, session, project
3. Analyze patterns across sessions
4. Report insights

---

## Commands

```bash
# Show top skills
bd analytics --top-skills

# Show unused skills
bd analytics --unused

# Show token savings
bd analytics --tokens

# Full analytics report
bd analytics --report

# Skill health score
bd analytics --health
```

---

## Usage Tracking Format

```json
{
  "skill_usage": [
    {
      "skill": "front-door",
      "invoked_at": "2025-01-31T10:30:00Z",
      "session": "afd19be4",
      "project": "oneshot",
      "trigger": "build me",
      "success": true
    }
  ],
  "token_savings": {
    "freesearch": 45000,
    "dispatch": 12000,
    "total": 57000
  }
}
```

---

## Report Formats

### Top Skills
```bash
$ bd analytics --top-skills

📊 Most Used Skills (Last 30 Days)

1. front-door        45 uses  (40%)  ████████████████████
2. beads             28 uses  (25%)  ████████████
3. debugger          15 uses  (13%)  ██████
4. implement-plan    12 uses  (11%)  █████
5. freesearch        8 uses   (7%)   ███

Total invocations: 108
Avg per session: 12.3
```

### Unused Skills
```bash
$ bd analytics --unused

📋 Unused Skills (Last 30 Days)

High Priority (Core):
  - create-plan       (Core skill, never used)
  - resume-handoff    (Context skill, never used)

Medium Priority (Advanced):
  - ci-cd-setup       (Last used: 90 days ago)
  - oci-resources     (Last used: 60 days ago)

Low Priority (Specialized):
  - the-audit         (Specialized, rarely expected)
  - visual-iteration  (UI-specific, rarely expected)

Recommendation: Consider removing or aliasing unused Core skills
```

### Token Savings
```bash
$ bd analytics --tokens

💰 Token Savings (Last 30 Days)

Source          | Tokens Saved | % of Total
----------------|--------------|-----------
/freesearch     |     45,000   |   79%
/dispatch       |     12,000   |   21%
----------------|--------------|-----------
Total Saved     |     57,000   |

Equivalent to: ~114 standard Claude messages (500 tokens each)
Cost avoided:   ~$1.14 (at $0.02/1k tokens)
```

### Skill Health
```bash
$ bd analytics --health

🏥 ONE_SHOT Skill Health: 87/100

Test Coverage:    78% (25/32 tested)  [████████████░░] 26 pts
Syntax Valid:    100% (43/43 valid)   [██████████████] 30 pts
Tools Available:  95% (41/43 ok)      [██████████████░] 25 pts
Recent Updates:   60% (26/43 <30d)    [██████████░░░░░]  6 pts

Action Items:
  - Add tests for: git-workflow, secrets-sync
  - Check tools for: oci-resources, api-designer
  - Update docs for: hooks-manager (last updated 90d ago)
```

---

## Integration with Session Tracking

### Auto-Log Skill Usage
When a skill is invoked:
```python
# In skill implementation, after loading:
import json
from datetime import datetime, timezone

usage = {
    "skill": "skill-name",
    "invoked_at": datetime.now(timezone.utc).isoformat(),
    "session": os.getenv("CLAUDE_SESSION_ID", "unknown"),
    "project": os.path.basename(os.getcwd()),
    "success": True
}

# Append to usage log
usage_file = ".beads/skill_usage.json"
with open(usage_file, "a") as f:
    f.write(json.dumps(usage) + "\n")
```

### Token Savings Tracking
```python
# For freesearch skill:
tokens_saved_before = 0  # Would have used WebSearch
tokens_saved_after = 500  # Used Exa API instead

# Log savings
savings = {
    "source": "freesearch",
    "tokens_saved": 500,
    "date": datetime.now(timezone.utc).isoformat()
}
```

---

## Analytics Queries

### Skills by Category
```bash
$ bd analytics --by-category

Category       | Skills | Uses (30d) | Avg Use
---------------|--------|------------|----------
Core           |   5    |    72      |  14.4
Research       |   4    |    18      |   4.5
Development    |   7    |    10      |   1.4
Operations     |   6    |     5      |   0.8
```

### Skill Correlations
```bash
$ bd analytics --correlations

🔗 Skill Usage Patterns

front-door → create-plan (85% of front-door uses)
create-plan → implement-plan (92% of plans)
debugger → test-runner (67% after debugging)
beads → resume-handoff (45% of sessions)

Insights:
- Consider auto-chaining: front-door → create-plan
- Add test-runner suggestion after debugger
```

### Project-Specific Usage
```bash
$ bd analytics --by-project

Project        | Sessions | Top Skills
---------------|----------|----------------------------
oneshot        |    45    | beads, front-door, freesearch
homelab        |    12    | docker-composer, secrets-sync
client-xyz     |     8    | push-to-cloud, observability
```

---

## Quick Win from Research

**Competitor Analysis**: No existing skill system has built-in analytics
**Opportunity**: Be the first to track skill usage and insights
**Value**: Data-driven decisions about which skills to improve/remove

---

## Implementation Notes

**Storage**: `.beads/skill_usage.json` (git-ignored, aggregated for reports)
**Privacy**: Local-only, no telemetry sent externally
**Performance**: Append-only writes, minimal overhead

---

## Anti-Patterns

- Obsessive micro-tracking (log at session level, not per API call)
- Tracking private data (only skill names and timestamps)
- Comparing across users (analytics is personal, not social)
- Over-optimizing for usage (some skills are rarely needed but critical)

---

## Keywords

analytics, stats, usage, metrics, most used, unused skills, token savings, skill health
