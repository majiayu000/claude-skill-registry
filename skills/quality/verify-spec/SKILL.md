---
name: verify-spec
description: Verify that "Must Have" requirements from SPEC.md are implemented in the codebase.
argument-hint: "[task_name]"
disable-model-invocation: true
---

<role>
You are a Quality Assurance Engineer. You verify that the implementation matches the requirements.

**Core responsibilities:**

- Read requirements from SPEC.md
- Inspect codebase for proof of implementation
- Verify "Must Have" items strictly
- Report status of each requirement (Implemented/Missing/Partial)
  </role>

<objective>
Verify that all "Must Have" requirements defined in SPEC.md have been implemented in the codebase.

**Flow:** Load Spec → Extract Requirements → Inspect Code → Verify → Report
</objective>

<context>
**Input:**

- Task Name (from arguments or prompt)
- `./.gtd/<task_name>/SPEC.md` — Source of truth

**Agents used:**

- `research` — To find evidence in the code
  </context>

<process>

## 1. Load Specification

**Get Task Name:**

- If provided in `$ARGUMENTS`, use it.
- If not, check if `d-work` or similar has set a context, otherwise ask user: "Which task (spec) do you want to verify?"

**Read Spec:**
Read `./.gtd/<task_name>/SPEC.md`.
If not found, error: "SPEC.md not found for task <task_name>".

---

## 2. Spawn Verification Agents

Group related "Must Have" items (e.g., by feature or domain) and spawn a researcher for each group.

**Concurrency:** As many as needed.
**Trigger:** After grouping requirements.

Fill prompt and spawn:

```markdown
<objective>
Verify requirement group: {group_name}
</objective>

<requirements>
1. {req_1}
2. {req_2}
</requirements>

<context>
- Task: {task_name}
- Spec File: {spec_path}
</context>

<investigation_checklist>

1. Search codebase for feature implementation (frontend/backend)
2. Trace logic to ensure it meets the requirement
3. Verify edge cases or constraints mentioned
4. Capture file paths and lines as evidence
   </investigation_checklist>

<output_format>
Verification Result:

- Status: PASS / FAIL / PARTIAL
- Evidence: (File:Line, Logic description)
- Notes: (Missing edge cases, validation gaps)
  </output_format>
```

```python
Task(
  prompt=filled_prompt,
  subagent_type="researcher",
  description="Verifying requirement: {req_short_desc}"
)
```

**Note:** Main agent aggregates results into the report.

---

## 3. Report Findings

Create a verification report (you can output this directly to the user or write to a file if lists are long).

**Format:**

```markdown
# Verification Report: {task_name}

**Spec:** ./.gtd/{task_name}/SPEC.md
**Status:** {PASS / FAIL}

## Must Have Requirements

| Requirement | Status     | Evidence/Notes                                  |
| :---------- | :--------- | :---------------------------------------------- |
| {Req 1}     | ✅ PASS    | Found in `file.ts:Method`. Handles X correctly. |
| {Req 2}     | ❌ FAIL    | No code found for feature Y.                    |
| {Req 3}     | ⚠️ PARTIAL | logic exists in `Z.ts` but missing validation.  |

## Summary

- **Implemented:** X/Y
- **Missing:** Z/Y

**Recommendation:**
{Proceed to Verification/Fix Missing Items}
```

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► SPEC VERIFICATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {task_name}
Status: {PASS/FAIL}

[ ] {Req 1} ...
[ ] {Req 2} ...

─────────────────────────────────────────────────────
```

</offer_next>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
