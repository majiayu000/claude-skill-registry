---
name: dialogue-daily-check
description: Log a daily check assessment for developer experience. Captures good/bad day indicators from C-6/C-7 research. Triggers on "daily check", "end of day check", "session check", "how was today".
allowed-tools: Bash, AskUserQuestion
---

# Dialogue: Daily Check Assessment

Log a daily check assessment to capture developer experience indicators at the end of a session.

## Framework Grounding

This skill operationalises:
- **C-6 (Hicks et al. 2024)**: Developer Thriving—agency, motivation, learning culture, support
- **C-7 (Obi et al. 2024)**: "Bad Days"—blockers, interruptions, context switching, unclear requirements

## When to Use

Use this skill at the end of substantive work sessions to:
- Capture developer experience signals
- Build longitudinal data for pattern detection
- Surface systematic issues early

The Stop hook will remind you when a daily check hasn't been done and substantive work occurred.

## How to Log a Daily Check

### Option 1: Interactive Collection (Recommended)

Ask the user the following questions using AskUserQuestion. Frame these as a quick 5-7 question check-in about the session.

**Good day indicators:**
1. Did you make meaningful progress on tasks today? (yes/no)
2. Did you learn something new or deepen understanding? (yes/no)
3. Did you have support when needed? (yes/no)
4. Did you have control over how to approach your work? (yes/no)

**Bad day indicators:**
5. Did you encounter blockers that impeded progress? (yes/no)
6. Did excessive context switching disrupt your flow? (yes/no)
7. Did you work with unclear or ambiguous requirements? (yes/no)

**Overall:**
8. Rate the overall session quality (1-5)
9. Any notes or reflections? (optional free text)

### Option 2: Direct Script Invocation

If you already have the responses, invoke the logging script directly:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-daily-check/scripts/log-daily-check.sh \
  <assessor> \
  <made_progress> <learned_something> <felt_supported> <had_agency> \
  <experienced_blockers> <context_switching> <unclear_requirements> \
  <session_quality> \
  [task_ref] [notes]
```

### Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `assessor` | `ai:claude` or `human:<id>` | Who is being assessed |
| `made_progress` | `true` or `false` | Made meaningful progress |
| `learned_something` | `true` or `false` | Learned something new |
| `felt_supported` | `true` or `false` | Had support when needed |
| `had_agency` | `true` or `false` | Had control over approach |
| `experienced_blockers` | `true` or `false` | Encountered blockers |
| `context_switching` | `true` or `false` | Excessive context switching |
| `unclear_requirements` | `true` or `false` | Unclear requirements |
| `session_quality` | `1-5` | Overall session quality |
| `task_ref` | string (optional) | Task reference (e.g., "FW-023") |
| `notes` | string (optional) | Free-text reflection |

## Example Interactive Flow

```
AI: Let me do a quick end-of-session check. This helps track developer experience patterns.

[Uses AskUserQuestion with the 7-8 questions]

AI: Thanks! Let me log that assessment.

[Invokes log-daily-check.sh with collected responses]

AI: Daily check logged as ASSESS-20260122-170000.
    Session quality: 4/5
    Good: Made progress, learned something, felt supported
    Challenges: Some unclear requirements
```

## Example Direct Invocation

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-daily-check/scripts/log-daily-check.sh \
  "human:pidster" \
  true true true true \
  false false true \
  4 \
  "FW-023" \
  "Productive session implementing assessments"
```

## Output

The script returns the generated assessment ID (e.g., `ASSESS-20260122-170000`).

The assessment is stored in `.dialogue/logs/assessments/` and creates:
- Assessment YAML file
- Context graph node (ARTIFACT with artifact_type: ASSESSMENT)
- CREATED edge from assessor to assessment
- ASSESSES edge to task (if task_ref provided)

## Interpreting Results

**Healthy session indicators:**
- 3+ good day indicators true
- 0-1 bad day indicators true
- Session quality 4-5

**Warning signals:**
- Fewer than 2 good day indicators
- 2+ bad day indicators
- Session quality below 3

**Pattern detection** (future capability):
- Track trends over time
- Identify systematic issues (e.g., chronic unclear requirements)
- Correlate with task types, phases, or collaboration patterns

## Schema Reference

See [Assessment Schema](./schema.md) for the complete DAILY_CHECK response schema and validation rules.
