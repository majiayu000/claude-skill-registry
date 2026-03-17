---
name: create-team
description: Create an Agent Team with two explorer agents that independently explore a directory, then compare their findings. Use when asked to "create a team", "compare exploration", "dual explore", or "team explore".
argument-hint: <path-to-directory>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Task, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage, AskUserQuestion
---

# Create Team — Dual Explorer Comparison

Spawn an Agent Team with two independent explorer agents that explore the same directory, then compare their findings to surface coverage gaps, different interpretations, and combined insights.

This skill follows the hub-and-spoke pattern: you (the lead) coordinate the team while explorers work independently.

## Load References

Load the cc-teams and cc-tasks references for correct tool usage:

```
Read ${CLAUDE_PLUGIN_ROOT}/skills/cc-teams/SKILL.md
Read ${CLAUDE_PLUGIN_ROOT}/skills/cc-tasks/SKILL.md
```

---

## Phase 1: Setup & Spawning

**Goal:** Validate the target directory, create the team, spawn explorers, and assign tasks.

### Step 1: Validate Target Directory

1. If `$ARGUMENTS` is provided, use it as the target directory path
2. If no arguments, use `AskUserQuestion` to ask: "Which directory should the team explore?"
   - Options: suggest 2-3 top-level directories from `Glob` (`*/` pattern), plus "Other" for custom input
3. Verify the directory exists using `Glob` with a `*` pattern inside it
4. If the directory does not exist or is empty, inform the user and abort

Set `TARGET_DIR` to the validated directory path.

### Step 2: Quick Reconnaissance

Perform a brief scan of `TARGET_DIR` to provide context for the explorers:

1. List top-level contents with `Glob` (`{TARGET_DIR}/*`)
2. Count files by type with `Glob` (e.g., `{TARGET_DIR}/**/*.ts`, `{TARGET_DIR}/**/*.py`, `{TARGET_DIR}/**/*.md`)
3. Read any README.md or CLAUDE.md in the target directory if present

Set `RECON_SUMMARY` to a 3-5 line summary of what was found.

### Step 3: Create Team

```
TeamCreate:
  team_name: "explore-team-{unix-timestamp}"
  description: "Dual exploration of {TARGET_DIR}"
```

Set `TEAM_NAME` to the created team name.

### Step 4: Spawn Explorers

Spawn both explorers in the background using the Task tool:

**Explorer 1:**
```
Task:
  description: "You are explorer-1 in a dual exploration team. Wait for your task assignment. The codebase is at the current working directory."
  subagent_type: "agent-alchemy-core-tools:code-explorer"
  model: sonnet
  team_name: {TEAM_NAME}
  name: "explorer-1"
  run_in_background: true
```

**Explorer 2:**
```
Task:
  description: "You are explorer-2 in a dual exploration team. Wait for your task assignment. The codebase is at the current working directory."
  subagent_type: "agent-alchemy-core-tools:code-explorer"
  model: sonnet
  team_name: {TEAM_NAME}
  name: "explorer-2"
  run_in_background: true
```

### Step 5: Create and Assign Tasks

Create two exploration tasks with identical scope but no prescribed focus:

**Task 1 (for explorer-1):**
```
TaskCreate:
  subject: "Explore: {TARGET_DIR}"
  description: "Independently explore {TARGET_DIR} and produce a structured report. Context: {RECON_SUMMARY}. Explore freely — find key files, patterns, architecture, integration points, and potential issues. Use your standard output format."
  activeForm: "Explorer 1 exploring {TARGET_DIR}"
```

**Task 2 (for explorer-2):**
```
TaskCreate:
  subject: "Explore: {TARGET_DIR}"
  description: "Independently explore {TARGET_DIR} and produce a structured report. Context: {RECON_SUMMARY}. Explore freely — find key files, patterns, architecture, integration points, and potential issues. Use your standard output format."
  activeForm: "Explorer 2 exploring {TARGET_DIR}"
```

**Assign each task with status guard:**

For each task:
1. `TaskGet` to verify status is `pending` and owner is empty
2. `TaskUpdate` to set owner to the corresponding explorer
3. `SendMessage` to the explorer with task details:
   ```
   SendMessage:
     type: "message"
     recipient: "explorer-{N}"
     content: "Your exploration task {TASK_ID} is assigned. Explore {TARGET_DIR} independently and report your findings. Context: {RECON_SUMMARY}. Begin now."
     summary: "Exploration task assigned"
   ```

---

## Phase 2: Monitor & Compare

**Goal:** Wait for both explorers to finish, collect findings, and produce a comparison report.

### Step 1: Monitor Exploration

After assigning tasks, monitor progress:

1. When an explorer goes idle or sends a message, use `TaskGet` to check their task status
2. **If task is `completed`**: Record the explorer's findings from their messages
3. **If task is `in_progress`**: Explorer is still working — wait
4. **If task is `pending` with owner set**: Explorer hasn't started yet — wait
5. **If task is `pending` with no owner**: Re-assign using the status guard from Phase 1 Step 5

**Wait for BOTH exploration tasks to be marked complete before proceeding.**

### Step 2: Collect Findings

Gather the exploration reports from both explorers:

1. Read messages received from `explorer-1` — extract their structured findings
2. Read messages received from `explorer-2` — extract their structured findings
3. If either explorer produced empty or error output, note this as a gap

Set `FINDINGS_1` and `FINDINGS_2` to the respective reports.

### Step 3: Produce Comparison Report

Analyze both sets of findings and output a comparison report in this format:

```markdown
## Dual Exploration Comparison: {TARGET_DIR}

### Explorer 1 Summary
[2-3 sentence summary of explorer-1's findings]

### Explorer 2 Summary
[2-3 sentence summary of explorer-2's findings]

### Key Differences

| Aspect | Explorer 1 | Explorer 2 |
|--------|-----------|-----------|
| [area of divergence] | [explorer-1's interpretation] | [explorer-2's interpretation] |
| ... | ... | ... |

### Unique Discoveries
**Only found by Explorer 1:**
- [files, patterns, or insights explorer-2 missed]

**Only found by Explorer 2:**
- [files, patterns, or insights explorer-1 missed]

### Different Interpretations
[Cases where both explorers looked at the same code but reached different conclusions]

### Coverage Gaps
[Areas of {TARGET_DIR} that neither explorer investigated thoroughly]

### Combined Insights
[High-confidence findings where both explorers agree, plus a synthesis of their complementary discoveries]
```

Present this report to the user.

---

## Phase 3: Cleanup

**Goal:** Shut down the team gracefully.

1. **Shutdown explorers:**
   ```
   SendMessage type: "shutdown_request", recipient: "explorer-1", content: "Exploration complete"
   SendMessage type: "shutdown_request", recipient: "explorer-2", content: "Exploration complete"
   ```

2. **Wait for shutdown acknowledgments** from both explorers.

3. **Delete the team:**
   ```
   TeamDelete
   ```

---

## Error Handling

### Directory Validation Failure
- If the directory does not exist: inform the user and abort. Do not create a team.

### Explorer Failure
- If one explorer fails (empty output or error): proceed with the other explorer's findings. Note the failure in the comparison report under "Coverage Gaps."
- If both explorers fail: inform the user, clean up the team, and abort.

### Partial Results
- If one explorer produces significantly less output: note the imbalance in the report and highlight it as a coverage gap.

## Agent Coordination

- You (the lead) handle setup, monitoring, comparison, and cleanup
- Explorers work independently — no cross-explorer messaging (hub-and-spoke topology)
- Identical prompts ensure genuinely independent perspectives
- The value is in the comparison: different explorers naturally emphasize different aspects of the same codebase
