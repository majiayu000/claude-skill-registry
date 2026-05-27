---
name: d-verify
description: Verify hypotheses with debug logging. Updates ./.gtd/debug/current/ROOT_CAUSE.md
disable-model-invocation: true
---

<role>
You are a hypothesis tester. You systematically verify hypotheses until the root cause is found.

**Core responsibilities:**

- Load hypotheses in confidence order
- Add strategic debug logs to test each hypothesis
- Run reproduction steps
- Analyze debug output
- Move to next hypothesis if rejected
- Document root cause when found
  </role>

<objective>
Find the actual root cause through systematic verification.

**Flow:** Load Hypotheses → Test Highest Confidence → Analyze → Found or Next
</objective>

<context>
**Required files:**

- `./.gtd/debug/current/SYMPTOM.md` — Reproduction steps
- `./.gtd/debug/current/HYPOTHESES.md` — Hypotheses to test

**Output:**

- `./.gtd/debug/current/ROOT_CAUSE.md` — When found
- Debug logs in code (temporary)
  </context>

<philosophy>

## One Hypothesis at a Time

Test systematically. Don't add logs for all hypotheses at once.

## Strategic Logging

Add logs that can definitively confirm or reject the hypothesis.

## Evidence-Based Conclusion

Root cause must be backed by debug output, not assumption.

## Know When to Stop

If all hypotheses are rejected, stop and ask user to inspect again.

</philosophy>

<process>

## 1. Load Context

Read both files:

- `./.gtd/debug/current/SYMPTOM.md` — For reproduction steps
- `./.gtd/debug/current/HYPOTHESES.md` — For hypotheses list

```bash
if ! test -f "./.gtd/debug/current/SYMPTOM.md" || ! test -f "./.gtd/debug/current/HYPOTHESES.md"; then
    echo "Error: Missing required files"
    exit 1
fi
```

---

## 2. Spawn Verification Agents

For each hypothesis, spawn a researcher to inspect code for confirmation/rejection (READ-ONLY).

**Concurrency:** As many as needed (Parallel).
**Trigger:** After loading hypotheses.

Fill prompt for each hypothesis:

```markdown
<objective>
Verify Hypothesis: {hypothesis_description}
</objective>

<context>
- Symptom: {symptom_description}
- Evidence: {existing_evidence}
</context>

<related>

| Workflow      | Relationship                    |
| ------------- | ------------------------------- |
| `/d-inspect`  | Provides hypotheses to test     |
| `/d-plan-fix` | Creates fix plan for root cause |

</related>

<investigation_checklist>

1. Locate relevant code
2. Check for logic errors matching hypothesis
3. Verify if preconditions/assumptions hold true
4. Identify where to add debug logs if needed
   </investigation_checklist>

<output_format>
Verification Report:

- Status: Confirmed / Rejected / Inconclusive
- Evidence Found: (Code snippets, logic analysis)
- Recommended Debug Log Location: (File:Line)
  </output_format>
```

```python
Task(
  prompt=filled_prompt,
  subagent_type="researcher",
  description="Verifying hypothesis: {short_desc}"
)
```

---

## 3. Review & Decide Actions

Review reports from all subagents.

### 3a. If Root Cause Confirmed by Inspection

If a subagent found definitive proof (e.g., obvious logic bug):

- **Skip logging.**
- Proceed to Document Root Cause.

### 3b. If Inconclusive / Needs Logs

Select the most promising hypothesis based on subagent findings.

**Action:**

1. Add debug logs to locations recommended by subagent.
2. Run reproduction steps.
3. Analyze output.

### 3c. If All Rejected

If all subagents report "Rejected" with strong evidence:

- **STOP**.
- Ask user to re-inspect or provide new ideas.

---

## 4. Document Root Cause

When confirmed (by inspection or logs), write to `./.gtd/debug/current/ROOT_CAUSE.md`:

```markdown
# Root Cause

**Found:** {date}
**Status:** CONFIRMED

## Root Cause

{Clear description of the actual root cause}

## Verified Hypothesis

**Original Hypothesis {N}:** {description}
**Confidence:** {original percentage} → **Confirmed**

## Evidence

{Debug output and observations that confirmed this}

**Debug logs showed:**

- {key finding 1}
- {key finding 2}

## Location

- **Files:** `{file1}`, `{file2}`
- **Lines:** {line ranges}
- **Function/Method:** {specific location}

## Why It Causes The Symptom

{Explain the causal chain from root cause to observed symptom}

## Rejected Hypotheses

{List other hypotheses tested and why they were rejected}
```

### 4a. Clean Up Debug Logs

Remove or comment out temporary debug logs added during verification.

---

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD:DEBUG ► ROOT CAUSE FOUND ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Root cause documented: ./.gtd/debug/current/ROOT_CAUSE.md

Verified hypothesis: {N}
Location: {files}

─────────────────────────────────────────────────────

▶ Next Up

/d-plan-fix — create fix plan

─────────────────────────────────────────────────────
```

</offer_next>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
