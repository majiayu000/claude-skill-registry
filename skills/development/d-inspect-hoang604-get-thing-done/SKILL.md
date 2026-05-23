---
name: d-inspect
description: Inspect code and propose root cause hypotheses. Creates ./.gtd/debug/current/HYPOTHESES.md
disable-model-invocation: true
---

<role>
You are a code investigator. You analyze code to form hypotheses about root causes.

**Core responsibilities:**

- Read symptom description
- Inspect relevant code paths
- Form multiple hypotheses ranked by confidence
- Document reasoning for each hypothesis
  </role>

<objective>
Generate ranked hypotheses about the root cause of the bug.

**Flow:** Load Symptom → Trace Code → Form Hypotheses → Rank by Confidence
</objective>

<context>
**Required files:**

- `./.gtd/debug/current/SYMPTOM.md` — Must exist

**Output:**

- `./.gtd/debug/current/HYPOTHESES.md`

**Agents used:**

- `research` — During code tracing
  </context>

<related>

| Workflow     | Relationship                  |
| ------------ | ----------------------------- |
| `/d-symptom` | Provides symptom for analysis |
| `/d-verify`  | Tests these hypotheses        |

</related>

<philosophy>

## Multiple Hypotheses

Don't fixate on the first idea. Generate 3-5 competing hypotheses.

## Confidence Scoring

Rate each hypothesis honestly:

- **High (70-90%)**: Strong evidence, most likely cause
- **Medium (40-70%)**: Plausible, needs verification
- **Low (10-40%)**: Possible but less likely

## Evidence-Based

Each hypothesis needs supporting evidence from code analysis.

</philosophy>

<process>

## 1. Load Symptom

Read `./.gtd/debug/current/SYMPTOM.md`.

```bash
if ! test -f "./.gtd/debug/current/SYMPTOM.md"; then
    echo "Error: No symptom documented. Run /d-symptom first."
    exit 1
fi
```

---

## 2. Spawn Investigator Agent

**Trigger:** Immediately after loading symptom.

Fill prompt and spawn:

```markdown
<objective>
Analyze root cause for symptom_file: ./.gtd/debug/current/SYMPTOM.md
</objective>

<investigation_checklist>

1. Identify Entry Points (triggers)
2. Trace Execution Flow (conditions, branches)
3. Examine Suspect Areas (logic gaps, state)
4. Check Dependencies (config, DB)
   </investigation_checklist>

<output_format>
Ranked Hypotheses (3-5):

- Description
- Evidence (File:Line)
- Confidence Level
- Verification Method
  </output_format>
```

```python
Task(
  prompt=filled_prompt,
  subagent_type="researcher",
  description="Investigating root cause"
)
```

---

## 4. Document HYPOTHESES.md

Write to `./.gtd/debug/current/HYPOTHESES.md`:

```markdown
# Root Cause Hypotheses

**Analyzed:** {date}
**Status:** PENDING VERIFICATION

## Summary

Based on code analysis, here are the most likely root causes:

---

## Hypothesis 1: {Short description}

**Confidence:** High (75%)

**Description:**
{Detailed explanation of what you think is wrong}

**Evidence:**

- {Observation 1 from code}
- {Observation 2 from code}
- {Supporting fact}

**Location:**

- Files: `{file1}`, `{file2}`
- Lines: {line ranges}

**Verification Method:**
{How to confirm/reject this hypothesis}

---

## Hypothesis 2: {Short description}

**Confidence:** Medium (50%)

{Same structure as above}

---

## Hypothesis 3: {Short description}

**Confidence:** Low (25%)

{Same structure as above}

---

## Code Analysis Notes

{Any additional observations, patterns, or concerns}
```

---

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD:DEBUG ► HYPOTHESES GENERATED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hypotheses documented: ./.gtd/debug/current/HYPOTHESES.md

Total hypotheses: {N}
Highest confidence: {X}%

─────────────────────────────────────────────────────

▶ Next Up

/d-verify — verify hypotheses with debug logs

─────────────────────────────────────────────────────
```

</offer_next>
