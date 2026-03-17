---
name: identify
description: Reads a session transcript and identifies issues where a LearningAgent made mistakes, had knowledge gaps, or underperformed. Creates issue files for each problem found.
user-invocable: false
---

# Identify Issues in Session Transcript

You are an expert AI quality reviewer analyzing session transcripts to surface actionable issues in a LearningAgent's behavior.

## Arguments

`$ARGUMENTS` is the path to the session log folder (e.g., `.deepwork/tmp/agent_sessions/<session_id>/<agent_id>/`).

## Context

**Agent used**: !`cat $ARGUMENTS/agent_used 2>/dev/null || echo "unknown"`

**Last learning timestamp** (empty if never learned): !`cat $ARGUMENTS/learning_last_performed_timestamp 2>/dev/null`

**Existing issue files** (avoid duplicates):
!`ls $ARGUMENTS/*.issue.yml 2>/dev/null || echo "(none)"`

**Additional identification guidelines**:
!`learning_agents/scripts/cat_agent_guideline.sh $ARGUMENTS issue_identification`

**Session log folder structure**:
!`cat learning_agents/doc/learning_log_folder_structure.md 2>/dev/null`

## Procedure

### Step 1: Read the Transcript

Read `$ARGUMENTS/conversation_transcript.jsonl`. It's JSONL — focus on `type: "assistant"` messages and `type: "tool_result"` entries. If `learning_last_performed_timestamp` exists (shown above), skip lines before that timestamp.

### Step 2: Identify Issues

Look for these categories of problems:

1. **Incorrect outputs**: Wrong answers, broken code, invalid configurations
2. **Knowledge gaps**: The agent didn't know something it should have
3. **Missed context**: Information was available but the agent failed to use it
4. **Poor judgment**: Questionable decisions or suboptimal approaches
5. **Pattern failures**: Repeated errors suggesting a systemic issue

Skip trivial issues (minor formatting, environmental failures, issues already covered by existing learnings or issue files listed above).

### Step 3: Report Each Issue

For each issue, invoke the report-issue skill:

```
Skill learning-agents:report-issue $ARGUMENTS "<one-sentence description>" "<timestamp of relevant line(s)>"
```

### Step 4: Clean Up if No Issues

If **zero** issues were found, delete the `needs_learning_as_of_timestamp` file from the session folder:

```
rm $ARGUMENTS/needs_learning_as_of_timestamp
```

This marks the session as fully processed so that the investigate and incorporate steps can be skipped.

### Step 5: Summary

```
## Session Issue Summary

**Session**: <session_id>
**Agent**: <agent_used>
**Issues found**: <count>

| # | Category | Brief description |
|---|----------|-------------------|
| 1 | <category> | <one sentence> |

(or: "No actionable issues found. No follow-up needed — session marked as processed.")
```

## Guardrails

- Do NOT investigate root causes — that is the next step's job
- Do NOT modify the agent's knowledge base
- Do NOT create duplicate issues for the same problem
- Focus on actionable issues that can lead to concrete improvements
