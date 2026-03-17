---
name: create-agent
description: Creates a new LearningAgent with directory structure, core-knowledge.md, and Claude Code agent file. Guides the user through initial configuration.
---

# Create LearningAgent

Create a new LearningAgent and guide the user through initial configuration.

## Arguments

`$ARGUMENTS` is the agent name. Use dashes for multi-word names (e.g., `rails-activejob`). If not provided, ask the user what to name the agent.

## Procedure

### Step 1: Validate and Run Scaffold Script

If the name contains spaces or uppercase letters, normalize to lowercase dashes (e.g., "Rails ActiveJob" → `rails-activejob`).

Check `.claude/agents/` for an existing file matching `<agent-name>.md`. If found, inform the user of the conflict and ask how to proceed.

Run the scaffold script:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/create_agent.sh $ARGUMENTS
```

If the script reports that directories already exist, inform the user and ask whether to proceed with updating the configuration or stop.

### Step 2: Configure the Agent

Ask the user about the agent's domain:

- What domain or area of expertise does this agent cover?
- What kinds of tasks will it be delegated to handle?

Based on their answers, update:

1. **`.deepwork/learning-agents/<agent-name>/core-knowledge.md`**: Replace the TODO content with the agent's core expertise in second person ("You should...", "You are an expert on...").

   Example:
   ```
   You are an expert on Rails ActiveJob. You understand the full job lifecycle,
   supported adapters (Sidekiq, Resque, DelayedJob), retry configuration with
   exponential backoff, and callback patterns. You should always check the adapter
   documentation before recommending queue-specific features.
   ```

2. **`.claude/agents/<agent-name>.md`** frontmatter: Replace the TODO placeholders:
   - `name`: The agent's display name (human-readable, e.g., "Rails ActiveJob Expert")
   - `description`: A concise description for deciding when to invoke this agent (2-3 sentences max). Example: "Expert on Rails ActiveJob patterns including job creation, queue configuration, and retry logic. Invoke when delegating background job tasks or debugging queue issues."

### Step 3: Seed Initial Knowledge (Optional)

Ask the user if they want to seed any initial topics or learnings. If yes, create files using these formats:

**Topic file** (`.deepwork/learning-agents/<agent-name>/topics/<topic-name>.md`):
```yaml
---
name: "Topic Name"
keywords:
  - keyword1
  - keyword2
last_updated: "YYYY-MM-DD"
---

Detailed documentation about this topic area...
```

**Learning file** (`.deepwork/learning-agents/<agent-name>/learnings/<learning-name>.md`):
```yaml
---
name: "Learning Name"
last_updated: "YYYY-MM-DD"
summarized_result: |
  One sentence summary of the key takeaway.
---

## Context
...
## Key Takeaway
...
```

### Step 4: Summary

Output in this format:

```
## Agent Created: <agent-name>

**Files created/modified:**
- `.deepwork/learning-agents/<agent-name>/core-knowledge.md` — core expertise
- `.deepwork/learning-agents/<agent-name>/topics/` — topic documentation
- `.deepwork/learning-agents/<agent-name>/learnings/` — experience-based insights
- `.claude/agents/<agent-name>.md` — Claude Code agent file
```

Then output the following restart warning **exactly as written**, including the emphasis markers and blank lines. This is critical — the user WILL NOT be able to use the new agent without doing this:

```
---

## !! IMPORTANT — YOU MUST RESTART CLAUDE CODE !!

Claude Code does NOT hot-reload agent files. The agent you just created
is **invisible** to Claude until you restart.

**Do this now:**

1. Exit this Claude Code session (type `/exit` or Ctrl+C)
2. Restart with: `claude -c` (this continues your conversation)
3. The new agent will then be available via the Task tool

If you skip this step, Claude will not find the agent when you try to use it.

---
```

After the restart warning, output:

```
**Usage (after restart):**
  Use the Task tool with `name: "<agent-name>"` to invoke this agent.

**Learning cycle:**
  The post-Task hook will automatically track sessions. Run `/learning-agents learn`
  after sessions to identify and incorporate learnings.
```

## Guardrails

- Do NOT overwrite existing files without user confirmation
- Do NOT create agents with names that conflict with existing Claude Code agents
- Use dashes consistently in folder names and `.claude/agents/` filenames
- Keep the `.claude/agents/` `description` field concise (2-3 sentences max)
