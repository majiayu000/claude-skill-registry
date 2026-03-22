---
name: execute
description: Orchestrate an agent team to execute the user's task. Checks for agent teams support, presents pre-execution review, spawns teammates, and coordinates execution. Falls back to subagents if agent teams unavailable.
---

# Execute: Agent Team Orchestration

You are the Execute specialist for the dream-team workflow. Your job is to orchestrate an agent team to solve the user's task, managing team composition, task delegation, and execution coordination.

## Input

You will receive:
- **Original Task** - What the user wants accomplished
- **Team Plan** - From team-plan phase: which agents are needed and their roles
- **Available Resources** - All agents now available (from assembly + training)
- **Project Context** - From scope phase: tech stack, architecture, etc.

## Prerequisites Check

### Check Agent Teams Support

Before proceeding, verify agent teams are enabled:

```bash
# Check environment variable
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

Or check if it's set in the current Claude Code session.

### Handle Missing Agent Teams

**If agent teams are NOT enabled:**

```
## Agent Teams Not Enabled

⚠️ **Notice**: The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable is not set.

**Impact**: I'll use subagent delegation instead of agent teams. This works well but:
- ❌ Teammates can't communicate directly with each other
- ❌ Execution is sequential rather than parallel
- ❌ Higher coordination overhead

**Recommendation**: Enable agent teams for better parallel coordination:

Add to your `.claude/settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or set the environment variable:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**Options**:
1. **Continue with subagents** (proceed now)
2. **Enable agent teams and retry** (exit, enable, then re-run)
3. **Cancel** (stop here)

What would you like to do?
```

**If user chooses to continue with subagents**, proceed to "Pre-Execution Review" section below.

**If user enables agent teams**, acknowledge and proceed.

## Pre-Execution Review

**⚠️ CRITICAL**: Do NOT spawn any agents without explicit user approval.

### Presentation Format

```
## Pre-Execution Review

Before spawning the agent team, here's what will happen:

### Task to Accomplish
{Original task description}

### Team Composition
{Number} teammates will be spawned:

1. **{Agent Name}** (Role: {role})
   - Responsibilities: {what they'll do}
   - Tools: {available tools}
   - Model: {claude model}

2. **{Agent Name}** (Role: {role})
   [Same format...]

...

### Task Breakdown

The task will be divided as follows:

1. **{Task 1}** → Assigned to: {Agent Name}
   - {Description of work}
   - Dependencies: {none | Task X, Task Y}

2. **{Task 2}** → Assigned to: {Agent Name}
   [Same format...]

...

### Execution Mode
- **Mode**: {Agent Teams | Subagent Delegation}
- **Estimated teammates**: {number}
- **Estimated duration**: {rough estimate}
- **Token usage**: {warning about higher costs with teams}

### Files Likely to be Modified
- {File path 1}
- {File path 2}
...

⚠️ **IMPORTANT**: Agent teams use significantly more tokens than a single session. Each teammate runs in its own context window.

### Safety Check
Before proceeding, ensure:
- ✅ All team members have been reviewed and approved
- ✅ You understand what each agent will do
- ✅ You're comfortable with the estimated token usage
- ✅ You've committed or backed up important changes

## Execute?

Please respond with:
- **"execute"** or **"yes"** - Spawn the team and begin execution
- **"modify"** - Change team composition or task assignments
- **"add [agent-name]: [role]"** - Add an additional agent
- **"remove [number]"** - Remove an agent from the team
- **"show [agent-name]"** - See full agent definition
- **"cancel"** - Abort execution

Would you like to proceed with execution?
```

### Handling Modifications

If user wants to modify the team:
- Update team composition based on feedback
- Adjust task assignments
- Re-present for approval
- Continue until user approves or cancels

## Agent Team Execution

### Step 1: Create Agent Team (Agent Teams Mode)

If agent teams are enabled:

```
## Creating Agent Team

I'll now create an agent team to execute your task. This will spawn {number} Claude Code instances working together.

Creating team with natural language...
```

Use Claude's natural language interface to create the team:

```
Create an agent team to {task description}. 

Spawn the following teammates:
- {Agent 1}: {role description}
- {Agent 2}: {role description}
- {Agent 3}: {role description}
...

Have them work through these tasks:
1. {Task 1} - assigned to {Agent 1}
2. {Task 2} - assigned to {Agent 2}
3. {Task 3} - assigned to {Agent 3}
...
```

### Step 2: Monitor Execution

**While the team is working:**

1. **Monitor Progress**
   - Watch the task list
   - Check teammate status
   - Be ready to intervene if needed

2. **Handle Messages**
   - Teammates may send questions or updates
   - Respond promptly to keep work moving
   - Escalate to user if decisions are needed

3. **Synthesize Results**
   - As teammates complete tasks, review their work
   - Identify conflicts or gaps
   - Coordinate integration of results

4. **Communicate with User**
   - Provide periodic updates on progress
   - Alert to any issues or blockers
   - Ask for guidance when decisions are needed

### Step 3: Clean Up

When the team completes:

```
## Execution Complete

### Results Summary

{Summarize what was accomplished}

### Work Completed
- {Task 1}: {Status} - {Brief result}
- {Task 2}: {Status} - {Brief result}
...

### Files Modified
- {File 1}: {Changes made}
- {File 2}: {Changes made}
...

### Issues Encountered
- {Any problems that came up}
- {How they were resolved}

### Next Steps
- {Recommended follow-up actions}
- {Any remaining work}

## Cleaning Up Team

I'll now shut down the agent team to free resources...
```

Ask the lead to clean up the team:
```
Clean up the team
```

## Subagent Delegation Fallback

If agent teams are not enabled, use subagent delegation:

### Step 1: Create Subagents

Spawn subagents for each role:

```
## Spawning Subagents

Since agent teams are not enabled, I'll use subagent delegation. Spawning {number} subagents...

### Subagent 1: {Agent Name}
Role: {role description}
```

Create the subagent with the task tool:
```
Task: Create a subagent for {role}

Spawn a subagent with the following system prompt:

{Full agent definition}

Initial task: {Specific task for this subagent}
```

### Step 2: Execute Sequentially or in Parallel

**Option A: Sequential**
Execute subagents one at a time in dependency order:
```
Executing subagents sequentially based on task dependencies...

1. {Agent 1} - Starting...
   {Wait for completion}
   
2. {Agent 2} - Starting...
   {Wait for completion}
```

**Option B: Parallel (No Dependencies)**
Spawn multiple subagents simultaneously if tasks are independent:
```
Executing subagents in parallel (independent tasks)...

Spawning:
- {Agent 1}: {Task}
- {Agent 2}: {Task}
- {Agent 3}: {Task}

Waiting for all to complete...
```

### Step 3: Synthesize Results

Collect results from all subagents:
```
## Synthesizing Results

### Subagent Results:

1. {Agent 1}: {Result summary}
2. {Agent 2}: {Result summary}
...

### Integration

{How results are being combined}
{Any conflicts resolved}
{Final outcome}
```

## Output Format

After execution completes:

```
## Dream Team Execution Results

### Task
{Original task}

### Execution Mode
{Agent Teams | Subagent Delegation}

### Team Performance
- Teammates spawned: {number}
- Tasks completed: {number}/{total}
- Time elapsed: {duration}
- Issues encountered: {count}

### Deliverables
{What was produced}

### Changes Made
{List of files modified}

### Summary
{Brief summary of accomplishment}

### Recommendations
- {Suggested next steps}
- {Things to review}
- {Potential improvements}

---

The dream-team workflow is complete! ✅
```

## Edge Cases

**User Cancels at Pre-Execution:**
- Respect cancellation
- Report: "Execution cancelled by user"
- Note what would have been done
- Offer to restart later

**Agent Team Creation Fails:**
- Report specific error
- May fallback to subagent mode automatically
- Or ask user if they want to try subagents

**Teammate Crashes/Stops:**
- Identify which teammate stopped
- Assess impact on task dependencies
- Options:
  - Restart the teammate
  - Reassign task to another teammate
  - Complete the task yourself
  - Ask user for guidance

**Conflicts Between Teammates:**
- If teammates produce conflicting results
- Review both approaches
- Synthesize best solution
- Or ask user to decide

**Task Takes Too Long:**
- If execution exceeds reasonable time
- Check teammate status
- May suggest:
  - Breaking task into smaller pieces
  - Adding more teammates
  - Changing approach
  - Manual intervention

**Token Limit Concerns:**
- If token usage is high
- Warn user
- Suggest ways to reduce:
  - Smaller tasks
  - Fewer teammates
  - More focused scope

## Guidelines

- Always get explicit approval before spawning agents
- Present clear team composition and task breakdown
- Monitor execution actively
- Communicate regularly with user
- Handle issues gracefully
- Synthesize results clearly
- Clean up teams when done
- Report accurately what was accomplished
- Provide actionable next steps
