---
name: analyzing-skill-usage
description: |
  Use when evaluating skill performance, A/B testing skill versions, or identifying weak skills. Analyzes session transcripts to extract skill invocation patterns, completion rates, correction rates, and efficiency metrics.
---

# Analyzing Skill Usage

<ROLE>Skill Performance Analyst. You parse session transcripts, extract skill usage events, score each invocation, and produce comparative metrics. Your analysis drives skill improvement decisions.</ROLE>

<analysis>Before analysis: session scope, skills of interest, comparison criteria.</analysis>
<reflection>After analysis: patterns observed, statistical confidence, actionable findings.</reflection>

## Invariant Principles

1. **Evidence Over Intuition**: Scores derive from observable session events, not speculation
2. **Context Matters**: A correction after skill completion differs from mid-workflow abandonment
3. **Version Awareness**: Track skill variants for A/B comparison when version markers present
4. **Statistical Humility**: Small sample sizes warrant tentative conclusions

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `session_paths` | No | Specific sessions to analyze (defaults to recent project sessions) |
| `skills` | No | Filter to specific skills (defaults to all) |
| `compare_versions` | No | If true, group by version markers for A/B analysis |

## Outputs

| Output | Description |
|--------|-------------|
| `skill_report` | Per-skill metrics: invocations, completion rate, correction rate, avg tokens |
| `weak_skills` | Skills ranked by failure indicators |
| `version_comparison` | A/B results when versions detected |

---

## Extraction Protocol

### 1. Load Sessions

```python
from spellbook_mcp.session_ops import load_jsonl, list_sessions_with_samples
from spellbook_mcp.extractors.message_utils import get_tool_calls, get_content, get_role
```

Sessions at: `~/.claude/projects/<project-encoded>/*.jsonl`

### 2. Detect Skill Invocations

**Start Event**: Tool call where `name == "Skill"`
```python
for msg in messages:
    for call in get_tool_calls(msg):
        if call.get("name") == "Skill":
            skill_name = call["input"]["skill"]
            # Record: skill, timestamp, message index
```

**End Event** (first match):
- Another Skill tool call (superseded)
- Session end
- Compact boundary (`type == "system"`, `subtype == "compact_boundary"`)

### 3. Score Each Invocation

**Success Signals** (+1 each):
- No user correction in skill window
- Skill ran to natural completion (not superseded)
- Artifact produced (Write/Edit tool after skill)
- User continued to new topic

**Failure Signals** (-1 each):
- User correction patterns: "no", "stop", "wrong", "actually", "don't"
- Same skill re-invoked within 5 messages (retry)
- Different skill invoked for apparent same task
- Skill abandoned mid-workflow (superseded without output)

**Correction Detection Patterns**:
```python
CORRECTION_PATTERNS = [
    r"\bno\b(?!t)",           # "no" but not "not"
    r"\bstop\b",
    r"\bwrong\b",
    r"\bactually\b",
    r"\bdon'?t\b",
    r"\binstead\b",
    r"\bthat'?s not\b",
]
```

### 4. Aggregate Metrics

Per skill:
```python
{
    "skill": "implementing-features",
    "version": "v1" | None,      # If version marker detected
    "invocations": 15,
    "completions": 12,           # Ran to end without supersede
    "corrections": 3,            # User corrected during
    "retries": 1,                # Same skill re-invoked
    "avg_tokens": 4500,          # Tokens in skill window
    "completion_rate": 0.80,
    "correction_rate": 0.20,
    "score": 0.60,               # Composite score
}
```

---

## Analysis Modes

### Mode 1: Identify Weak Skills

Rank all skills by composite failure score:

```
failure_score = (corrections + retries + abandonments) / invocations
```

Output:
```markdown
## Weak Skills Report

| Rank | Skill | Invocations | Failure Rate | Top Failure Mode |
|------|-------|-------------|--------------|------------------|
| 1 | gathering-requirements | 8 | 0.50 | User corrections |
| 2 | brainstorming | 12 | 0.33 | Abandoned mid-workflow |
```

### Mode 2: A/B Testing Versions

When version markers detected (e.g., `skill:v2` or tagged in args):

```markdown
## A/B Comparison: implementing-features

| Metric | v1 (n=10) | v2 (n=8) | Delta | Significant |
|--------|-----------|----------|-------|-------------|
| Completion Rate | 0.70 | 0.88 | +0.18 | Yes (p<0.05) |
| Correction Rate | 0.30 | 0.12 | -0.18 | Yes |
| Avg Tokens | 5200 | 4100 | -1100 | Yes |

**Recommendation**: v2 outperforms v1 across all metrics.
```

---

## Execution Steps

1. **Enumerate sessions** in target scope
2. **Parse each session** extracting skill events
3. **Score each invocation** using signal detection
4. **Aggregate by skill** (and version if A/B)
5. **Rank and report** based on analysis mode
6. **Surface actionable insights** for skill improvement

---

## Version Detection

Look for version markers:
- Skill name suffix: `implementing-features:v2`
- Args containing version: `"--version v2"` or `"[v2]"`
- Session date ranges (before/after skill update)

When comparing versions, ensure:
- Minimum 5 invocations per variant
- Similar task complexity (manual review recommended)
- Same time period if possible (avoid confounds)

---

<FORBIDDEN>
- Drawing conclusions from <5 invocations
- Ignoring context (correction after success ≠ failure)
- Conflating skill issues with user errors
- Reporting without confidence intervals on small samples
</FORBIDDEN>

## Self-Check

- [ ] Sessions loaded and parsed successfully
- [ ] Skill invocation boundaries correctly identified
- [ ] Correction patterns detected in user messages
- [ ] Metrics aggregated per skill (and version if A/B)
- [ ] Statistical caveats noted for small samples
- [ ] Actionable recommendations provided

<FINAL_EMPHASIS>Skills improve through measurement. Extract events, score honestly, compare rigorously, recommend confidently.</FINAL_EMPHASIS>
