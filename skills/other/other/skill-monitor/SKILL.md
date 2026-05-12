---
name: skill-monitor
description: Analyze skill effectiveness across sessions. Computes per-skill metrics (action rate, friction, outcomes), identifies degrading skills, and generates improvement recommendations. Requires session-scan data in metrics.jsonl.
argument-hint: "[--skill NAME] [--improve] [--window 7d|30d|all]"
disable-model-invocation: true
---

# Skill Monitor

Closed-loop skill effectiveness monitoring. Reads session metrics,
computes per-skill signals, identifies what's working and what needs
improvement.

Inspired by the deploy-monitor-evaluate-improve feedback loop:
skills get better over time instead of staying static.

## Requirements

Requires `.claude/session-metrics/metrics.jsonl` from `/session-scan`.
If no data: suggest running `/session-scan` first.

## Usage

```
/skill-monitor                     # Dashboard: all skills
/skill-monitor --skill review      # Deep-dive on one skill
/skill-monitor --improve           # Generate improvement recommendations
/skill-monitor --window 30d        # Change comparison window (default: 7d)
```

## What Main Context Does

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:

- **`--skill NAME`**: Focus on one skill (e.g., `review`, `plan`, `investigate`)
- **`--improve`**: Spawn analysis agent for improvement recommendations
- **`--window PERIOD`**: Comparison window (`7d`, `30d`, `all`; default: `7d`)

### Step 2: Load Metrics

Read `.claude/session-metrics/metrics.jsonl`. For each entry, extract
the `skill_effectiveness` field (added by compute-metrics.py v2).

Filter by window period. Count sessions with and without skill usage.

If no `skill_effectiveness` data exists in metrics: "Metrics were
computed before skill tracking was added. Run `/session-scan --rescan`
to recompute."

**OTel `invocation_trigger` (CC v2.1.126+)**: when `compute-metrics.py`
ingests `claude_code.skill_activated` events, each invocation carries
an `invocation_trigger` of `"user-slash"`, `"claude-proactive"`, or
`"nested-skill"`. If absent (older sessions), default to
`"unknown"` — do NOT assume `"user-slash"`.

### Step 3: Compute Per-Skill Aggregates

For each skill found across all sessions, aggregate:

```
| Metric                  | Computation                                    |
|-------------------------|------------------------------------------------|
| Total invocations       | Sum of invocation_count across sessions        |
| Sessions used in        | Count of sessions containing this skill        |
| Action rate             | Weighted avg of per-session action_rate         |
| Avg post-errors         | Weighted avg of avg_post_errors                |
| Avg post-corrections    | Weighted avg of avg_post_corrections           |
| Outcome distribution    | Count of effective/friction/no_action/mixed    |
| Effectiveness score     | action_rate - (0.3 * avg_post_corrections)     |
| Adjusted score          | For analysis/check skills, use lower thresholds |
| Trigger distribution    | Counts of user-slash / claude-proactive / nested-skill / unknown |
| Proactive trigger rate  | claude-proactive / (user-slash + claude-proactive + nested-skill) |
| Auto-load gap           | Skills with 0 claude-proactive invocations across window |
```

**Auto-load gap detection (CC v2.1.126+)**: Skills with `auto-loaded`
behavior in their description (i.e., not `disable-model-invocation: true`)
are EXPECTED to fire as `claude-proactive`. A skill that is ONLY ever
invoked via `user-slash` is failing its description's routing intent.
Flag any auto-loadable skill where `proactive_trigger_rate == 0` over
the window. This is the structural answer to the "zero skill
auto-loading" gap from the 137-session analysis (see MEMORY.md).
**Confidence floor**: only flag if total invocations >= 5 in window.

**Skill type weighting**: Analysis and check skills (verify, triage,
perf, boundaries, pr-review, audit) have low action rates BY DESIGN —
their success is "found issues" or "confirmed things pass". Apply
adjusted thresholds:

| Skill Type | Flag Threshold | Expected Action Rate |
|------------|---------------|---------------------|
| Execution (work, quick, full) | < 0.5 | > 0.7 |
| Analysis (perf, boundaries, audit, pr-review) | < 0.3 | 0.3-0.5 |
| Check (verify, triage) | < 0.1 | 0.0-0.3 |
| Knowledge (compound, learn, brief) | < 0.5 | > 0.5 |

Also compute **baseline friction** (avg friction of sessions WITHOUT
any skill usage) vs **skill friction** (avg friction of sessions
WITH skill usage). Delta = skill_friction - baseline_friction.
Negative delta = skills reduce friction (good).

### Step 4: Display Dashboard

**Dashboard mode** (no `--skill`):

```
## Skill Effectiveness Dashboard (last {window})

Baseline friction (no skills): 0.32 | With skills: 0.18 | Delta: -0.14

| Skill           | Uses | Sessions | Slash/Proactive/Nested | Action% | Errors | Corr | Outcome   | Score |
|-----------------|------|----------|------------------------|---------|--------|------|-----------|-------|
| /phx:review     | 12   | 8        |    8 /  3 /  1         | 92%     | 0.5    | 0.1  | effective | 0.89  |
| /phx:plan       | 9    | 7        |    9 /  0 /  0         | 100%    | 0.2    | 0.0  | effective | 1.00  |
| /phx:investigate| 5    | 5        |    5 /  0 /  0         | 80%     | 1.2    | 0.4  | mixed     | 0.68  |

Skills needing attention:
- /phx:investigate (high post-errors)
- /phx:plan (auto-load gap — 0/9 proactive; description not routing)
```

Flag skills using type-adjusted thresholds (see weighting table above).
Also flag if avg_post_corrections > 1 or outcome is predominantly "friction".
**Also flag auto-load gap**: auto-loadable skills (without
`disable-model-invocation: true`) with proactive_trigger_rate == 0 and
total invocations >= 5. This is a description/routing problem — the skill
exists but Claude isn't loading it on its own.

When displaying flagged skills, note if the flag is "expected" for the
skill type (e.g., verify at 0.24 is normal for a check skill).

**Skill deep-dive** (`--skill NAME`):

Show per-session breakdown for that skill, including session IDs,
dates, individual outcome signals, AND `invocation_trigger` per
invocation. If a skill is dominated by `user-slash` triggers, surface
which 1-3 description keywords might unlock proactive routing —
cross-reference against the skill's current description in
`plugins/elixir-phoenix/skills/{name}/SKILL.md`. If session reports
exist in `.claude/session-analysis/`, reference them.

### Step 5: Improvement Mode (--improve)

Spawn `skill-effectiveness-analyzer` agent:

```
Agent(subagent_type="skill-effectiveness-analyzer", model="sonnet", prompt="""
Analyze skill effectiveness data and recommend improvements.

Metrics data: {aggregated_metrics_json}

Sessions with friction outcomes: {session_ids}

For each underperforming skill:
1. Identify failure patterns from outcome signals
2. Propose specific skill/agent changes
3. Suggest new Iron Laws if patterns are systematic

Write recommendations to: .claude/skill-metrics/recommendations-{date}.md
""")
```

### Step 6: Write Output

Write aggregated metrics to `.claude/skill-metrics/dashboard-{date}.json`:

```json
{
  "computed_at": "2026-03-03T14:00:00Z",
  "window": "7d",
  "baseline_friction": 0.32,
  "skill_friction": 0.18,
  "friction_delta": -0.14,
  "skills": {
    "/phx:plan": {
      "invocations": 9,
      "trigger_distribution": {
        "user-slash": 9,
        "claude-proactive": 0,
        "nested-skill": 0,
        "unknown": 0
      },
      "proactive_trigger_rate": 0.0,
      "auto_load_gap": true
    }
  },
  "flagged_skills": ["investigate", "plan:auto-load-gap"]
}
```

Append-only: never modify previous dashboard files.

## Iron Laws

1. **NEVER modify metrics.jsonl** — read-only from this skill
2. **Baseline comparison is mandatory** — raw numbers without baseline are meaningless
3. **Flag, don't judge** — surface data, let the human decide what to fix
4. **Evidence tags on recommendations** — every suggestion needs session citations
5. **Trigger source must not be inferred** — only treat invocations as
   `user-slash` / `claude-proactive` / `nested-skill` when the OTel
   `invocation_trigger` attribute is present (CC v2.1.126+). Older
   sessions use `"unknown"`; never silently bucket them as user-slash —
   it would hide the auto-load gap.

## Integration

```
/session-scan → metrics.jsonl (with skill_effectiveness)
       ↓
/skill-monitor → dashboard + flagged skills
       ↓
/skill-monitor --improve → recommendations
       ↓
Developer updates skills/agents → deploy → repeat
```

## References

- `references/effectiveness-metrics.md` — Full metrics schema and evaluation criteria
- `references/improvement-template.md` — Template for improvement recommendations
