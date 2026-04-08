---
name: skill-evolution
description: "Self-evolving skill system. Skills are scored after execution (0-100) on 5 dimensions. Score 90+ over 5 runs = crystallized (locked). Score below 30 = auto-repair attempted. Skills improve themselves through usage feedback."
---

# Skill Evolution

Darwinian selection for skills. Skills that produce good outcomes are crystallized and protected. Skills that produce poor outcomes are repaired or archived. Every execution generates a score that drives the next generation of the skill.

## The 5 Scoring Dimensions

Each skill execution is scored 0-100 on five dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Accuracy | 25% | Did the skill produce the correct result for the task? |
| Relevance | 20% | Was the skill content applicable to the actual use case? |
| Token Efficiency | 20% | Did the skill guide the agent without bloat or repetition? |
| User Satisfaction | 20% | Did the outcome meet or exceed user expectations? |
| Reusability | 15% | Could another agent use this skill in a similar situation? |

**Composite score** = weighted average of all five dimensions (0-100).

### Scoring Rubric

```
90-100: Excellent -- candidate for crystallization
70-89:  Good -- active skill, no action needed
50-69:  Adequate -- flag for review after 3 more runs
30-49:  Poor -- schedule auto-repair attempt
0-29:   Critical -- immediate auto-repair or archive
```

## Skill Lifecycle

```
DRAFT          ACTIVE         CRYSTALLIZED      ARCHIVED
  |               |                |                |
New skill   In regular use   Proven stable    Deprecated/replaced
  |               |                |                |
  +-- first run ->+-- score >90   ++-- score <30    |
                  |   for 5+ runs  |   (3 attempts)  |
                  +-- score <30 -->+ auto-repair      |
                  |   auto-repair  |   fails 3x -->--+
                  +-- score >90 -->+
```

### Draft
New skills enter as Draft. They receive no special protection and are evaluated critically on first use. A Draft skill that scores below 30 on its very first run is discarded rather than repaired.

### Active
Skills in regular use. Scores are tracked in `~/.claude/skill-scores.jsonl`. No action unless scores trend below 30 or above 90 over a rolling window of 5 runs.

### Crystallized
A skill that maintains an average composite score above 90 over 5 or more consecutive runs is crystallized:
- Git tag applied: `skill/<name>/crystallized-v<N>`
- Read-only flag added to frontmatter: `locked: true`
- Skill is excluded from auto-repair
- Changes require explicit human unlock + PR

### Archived
A skill that fails auto-repair 3 times is archived:
- Moved to `skills/_archived/<name>/`
- Git tag applied: `skill/<name>/archived`
- Replacement skill drafted by `catalyst` agent if the capability is still needed

## Score Storage Format

Append one record per execution to `~/.claude/skill-scores.jsonl`:

```jsonl
{"skill":"experiment-loop","ts":"2026-04-07T10:00:00Z","session":"abc123","scores":{"accuracy":88,"relevance":92,"token_efficiency":75,"user_satisfaction":90,"reusability":85},"composite":86.5,"feedback":"Loop ran 4 iterations successfully, target nearly met"}
{"skill":"experiment-loop","ts":"2026-04-07T14:30:00Z","session":"def456","scores":{"accuracy":95,"relevance":90,"token_efficiency":82,"user_satisfaction":95,"reusability":88},"composite":90.4,"feedback":"Bundle size reduced 28%, target exceeded"}
```

### Score CLI (quick check)

```bash
# Average scores for a skill (last 10 runs)
cat ~/.claude/skill-scores.jsonl | python3 -c "
import sys, json, statistics
skill = '$1'
runs = [json.loads(l) for l in sys.stdin if json.loads(l).get('skill') == skill][-10:]
if runs:
    avg = statistics.mean(r['composite'] for r in runs)
    print(f'{skill}: {avg:.1f} avg over {len(runs)} runs')
"
```

## Crystallization Protocol

When a skill reaches 90+ composite score over 5+ consecutive runs:

1. Verify scores in `~/.claude/skill-scores.jsonl` -- confirm no outliers inflating the average
2. Add `locked: true` to the skill's frontmatter
3. Apply git tag:
   ```bash
   git tag skill/<name>/crystallized-v1 -m "Crystallized: avg score 92.3 over 7 runs"
   git push origin skill/<name>/crystallized-v1
   ```
4. Log the crystallization in `thoughts/SKILL-EVOLUTION.md`
5. Notify via canavar cross-training so all agents know this skill is stable

## Auto-Repair Protocol

When a skill's composite score drops below 30:

### Diagnosis
1. Identify the lowest-scoring dimension (the primary failure mode)
2. Read the last 3 session feedback notes from `~/.claude/skill-scores.jsonl`
3. Summarize what went wrong (specific, not vague)

### Repair
The `catalyst` agent rewrites the failing section(s) of the skill:
- Only the sections relevant to the low-scoring dimension
- Preserve all high-scoring sections unchanged
- Add a concrete example for the repaired section

### Validation
After repair, the skill is re-scored on a synthetic test case by the `verifier` agent:
- Synthetic score must be 50+ to proceed to Active state
- If synthetic score < 50, attempt 2 of 3 repairs begins

### Escalation
After 3 failed auto-repairs:
- Archive the skill
- Alert via `thoughts/SKILL-EVOLUTION.md`
- Spawn `catalyst` to draft a replacement from scratch

## Evolution Log Format

Append events to `thoughts/SKILL-EVOLUTION.md`:

```markdown
## 2026-04-07

### skill: experiment-loop
- Status change: Active -> Crystallized
- Trigger: avg composite 91.2 over 6 consecutive runs
- Git tag: skill/experiment-loop/crystallized-v1
- Notable strength: Token Efficiency dimension consistently 85+

### skill: legacy-deploy-helper
- Status change: Active -> Auto-Repair (attempt 1/3)
- Trigger: composite 24 on last run
- Lowest dimension: Relevance (12) -- skill referenced outdated Heroku patterns
- Repair: catalyst rewrote "Deployment Targets" section with Vercel/Railway focus
- Post-repair synthetic score: 71 -- promoted back to Active
```

## Integration with Canavar Cross-Training

Skill evolution data feeds into canavar's cross-training pipeline:

- A crystallized skill is injected into canavar's `skill-matrix.json` with `trust: locked`
- An archived skill is marked `trust: deprecated` -- agents stop referencing it
- Auto-repair failures are logged to `error-ledger.jsonl` with `source: skill-evolution`
- The canavar leaderboard tracks which agents most frequently produce high-scoring skill executions

```bash
# View crystallized skills
node ~/.claude/hooks/dist/canavar-cli.mjs leaderboard --filter crystallized

# View skills needing repair
cat ~/.claude/skill-scores.jsonl | python3 -c "
import sys, json, collections
runs = [json.loads(l) for l in sys.stdin]
low = {r['skill'] for r in runs if r['composite'] < 30}
print('Skills needing repair:', low)
"
```

## Activation

This skill activates automatically when:
- A skill completes an execution (PostToolUse hook)
- A skill is referenced in a session that ends with user dissatisfaction
- The `verifier` agent reports a skill-guided task as failed

Agents involved: `catalyst` (repair), `verifier` (validation), `self-learner` (feedback extraction), `canavar` (cross-training propagation).
