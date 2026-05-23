---
name: learn
description: Runs the learning cycle on all LearningAgent sessions with pending transcripts. Identifies issues, investigates root causes, and incorporates learnings into agent definitions.
---

# Learning Cycle

Process unreviewed LearningAgent session transcripts to identify issues, investigate root causes, and incorporate learnings into agent definitions.

## Arguments

This skill takes no arguments. It automatically discovers all pending sessions.

## Session Log Folders needing Processing

!`learning_agents/scripts/list_pending_sessions.sh`

## Procedure

If the list above is empty (or the `.deepwork/tmp/agent_sessions` directory does not exist), inform the user that there are no pending sessions to learn from and stop.

### Step 1: Process Each Session

For each session log folder, run the learning cycle in sequence.

#### 1a: Identify Issues

Spawn a Task to run the identify skill:

```
Task tool call:
  name: "identify-issues"
  subagent_type: learning-agents:learning-agent-expert
  model: sonnet
  prompt: "Run: Skill learning-agents:identify <session_log_folder>"
```

**Run those in parallel**

#### 1b: Investigate and Incorporate

After identification completes, **skip** any session where the identify step reported zero issues. Only proceed with sessions that had issues identified.

For remaining sessions, start a new Task to run investigation and incorporation in sequence for each session_log_folder:

```
Task tool call:
  name: "investigate-and-incorporate"
  subagent_type: learning-agents:learning-agent-expert
  model: sonnet
  prompt: "Run these two skills in sequence:
           1. Skill learning-agents:investigate-issues <session_log_folder>
           2. Skill learning-agents:incorporate-learnings <session_log_folder>"
```

**Run session log folders from the same agent serially, but different agents in parallel.** I.e. if Agent A has 7 sessions and Agent B has 3 sessions, you should have 3 "batches" of Tasks where you do one session for Agent A and one for Agent B, then you would have 4 more Tasks run serially for the remaining Agent A sessions.

#### Handling failures

If a sub-skill Task fails for a session, log the failure, skip that session, and continue processing remaining sessions. Do not mark `needs_learning_as_of_timestamp` as resolved for failed sessions.

### Step 2: Summary

Output in this format:

```
## Learning Cycle Summary

- **Sessions processed**: <count>
- **Total issues identified**: <count>
- **Agents updated**: <comma-separated list of agent names>
- **Key learnings**:
  - <agent-name>: <brief learning description>
- **Skipped sessions** (if any): <session path> — <reason>
```

## Guardrails

- Do NOT modify agent files directly — always delegate to the learning cycle skills in Tasks
- Use Sonnet model for Task spawns to balance cost and quality
- Use the `learning-agents:learning-agent-expert` agent for Task spawns
