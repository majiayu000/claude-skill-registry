---
name: investigate-issues
description: Investigates identified issues in a LearningAgent session by reading the transcript, determining root causes, and updating issue files with investigation reports.
user-invocable: false
---

# Investigate Issues

Research identified issues from a LearningAgent session to determine their root causes.

## Arguments

`$ARGUMENTS` is the path to the session log folder (e.g., `.deepwork/tmp/agent_sessions/<session_id>/<agent_id>/`).

## Context

**Session log folder structure**:
!`cat learning_agents/doc/learning_log_folder_structure.md 2>/dev/null`

**Agent used**: !`cat $ARGUMENTS/agent_used 2>/dev/null || echo "unknown"`

**Identified issues to investigate**:
!`grep -l 'status: identified' $ARGUMENTS/*.issue.yml 2>/dev/null || echo "(none)"`

**Additional investigation guidelines**:
!`learning_agents/scripts/cat_agent_guideline.sh $ARGUMENTS issue_investigation`

## Current Agent State
-------- CURRENT KNOWLEDGE OF AGENT --------
!`learning_agents/scripts/generate_agent_instructions_for_session.sh $ARGUMENTS`
------ END CURRENT KNOWLEDGE OF AGENT-------

## Procedure

If no identified issues are listed above, report that and stop.

Refer back to the `conversation_transcript.jsonl` file as needed in this process.

### Step 1: Investigate Each Issue

For each issue file with status `identified`:

1. **Read the issue file** to understand what went wrong
2. **Search the transcript** for relevant sections — grep for keywords from `issue_description` or locate lines near `seen_at_timestamps`
3. **Determine root cause** using this taxonomy:
   - **Knowledge gap**: Missing or incomplete content in `core-knowledge.md`
   - **Missing documentation**: A topic file does not exist or lacks needed detail
   - **Incorrect instruction**: An existing instruction leads the agent to wrong behavior
   - **Missing runtime context**: Information that should have been injected at runtime was absent

### Step 2: Update Issue Files

For each investigated issue, use Edit to update the issue file:

1. Change `status: identified` to `status: investigated`
2. Add the `investigation_report` field:

```yaml
status: investigated
investigation_report: |
  <Root cause analysis with specific transcript line numbers as evidence.
  Explain what knowledge gap or instruction deficiency caused the issue.>
```

### Step 3: Summary

Simply say "Session log folder <session log folder> done."

## Guardrails

- Do NOT modify the agent's knowledge base — that is the incorporate step's job
- Do NOT change the `issue_description` — only add the `investigation_report`
- Do NOT skip issues — investigate every `identified` issue
- Be specific about evidence — reference transcript line numbers
