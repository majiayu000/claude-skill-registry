---
name: chatroom
description: Start the agent chatroom for real-time coordination between parallel agents. Use when spawning multiple agents that need to communicate or when you want to monitor agent activity.
---

# Agent Chatroom

This skill starts a real-time chatroom for **coordination between parallel agents and the user**. The chatroom is for quick communication, asking questions, and getting help - not for posting work output or results.

## Starting the Chatroom

When this skill is invoked, you MUST:

1. **Find the plugin root** - look for the agent-chatroom plugin in the enabled plugins list or use this path:
   - macOS/Linux: `~/.claude/plugins/*/agent-chatroom` or the cloned repo location
   - The plugin root contains `spawn-terminal.js` and `ui.js`

2. **Start the chatroom server/UI** by running:
   ```bash
   node <plugin-root>/spawn-terminal.js <plugin-root>/ui.js
   ```

3. **Wait for the server** to be ready (check port 3030):
   ```bash
   nc -z localhost 3030 && echo "Ready" || echo "Starting..."
   ```

4. **Confirm to the user** that the chatroom is open.

## Agent Instructions

After starting the chatroom, whenever you spawn agents (using the Task tool):
- **ALWAYS use `run_in_background: true`** so agents run independently
- **MUST append the chatroom instructions below** to each agent's prompt

```
## ⛔ CRITICAL: NEVER RETURN TEXT - IT DISCONNECTS YOU ⛔

**THIS IS THE MOST IMPORTANT RULE:**
- You must NEVER return/output a text response directly
- Returning text = completing your task = disconnecting from the team
- If you want to report ANYTHING, use `chatroom_broadcast` tool instead
- Your ONLY allowed outputs are TOOL CALLS
- Every response you give MUST end with a tool call (chatroom_check, chatroom_broadcast, or work tools)

**WHY:** When you return text without a tool call, you EXIT and disconnect. The team loses you.

**CORRECT behavior:**
- Starting work? → `chatroom_status(name: "yourname", status: "busy", task: "Reading auth.ts")`
- Finished work? → `chatroom_status(name: "yourname", status: "idle")`
- Want to report something? → `chatroom_broadcast(message: "Found the bug!", name: "yourname")`
- Nothing to do? → `chatroom_check(name: "yourname")` (and keep checking every 20 seconds)

**WRONG behavior (NEVER DO THIS):**
- Returning "Here's my status report..."
- Returning "I've completed the task..."
- Returning any text without a tool call

## Chatroom Instructions

You have access to a real-time chatroom for **coordination only**.

**At start:**
- Call `chatroom_join` with your agent name

**During work:**
- **Before starting work:** Call `chatroom_status(name: "yourname", status: "busy", task: "what you're doing")`
- **After finishing work:** Call `chatroom_status(name: "yourname", status: "idle")`
- Call `chatroom_broadcast(message: "...", name: "yourname")` for questions and important updates
- Call `chatroom_check(name: "yourname")` every 15-30 seconds to see messages
- Use other tools (Read, Edit, Bash, etc.) for your actual work
- **IMPORTANT:** Always include your `name` parameter on ALL chatroom calls

**Chatroom etiquette:**
- Brief messages only (like Slack)
- No code dumps or verbose logs
- Ask questions, coordinate, report blockers

## Your Work Loop (MANDATORY)

You MUST follow this pattern FOREVER:

```
INFINITE LOOP:
  1. chatroom_check(name: "yourname") - look for new messages/instructions
  2. If you have work to do:
     a. chatroom_status(name: "yourname", status: "busy", task: "description")
     b. Do the work (Read, Edit, Bash, etc.)
     c. chatroom_status(name: "yourname", status: "idle")
  3. If user says "@yourname stop" or "shutdown":
     - chatroom_broadcast(message: "leaving", category: "leaving", name: "yourname")
     - chatroom_leave(name: "yourname")
     - ONLY THEN you may exit
  4. If no shutdown command: go back to step 1
  5. NEVER EXIT THIS LOOP WITHOUT SHUTDOWN COMMAND
```

## The ONLY Way to Exit

- User explicitly says "@yourname stop", "shutdown", or "all agents stop"
- You see this in chatroom_check results
- Then and ONLY then: broadcast "leaving", call `chatroom_leave(name: "yourname")`, and exit

**If you are unsure whether to exit: DON'T. Keep looping.**
```

## User Interaction

The chatroom UI terminal allows the user to:
- See all agent messages in real-time
- Send messages/instructions to agents
- Close the terminal to shut down the chatroom (agents will detect this and exit)

## Example Workflow

User: `/chatroom` then "spawn backend and frontend agents to build a feature"

You should:
1. Start the chatroom (run the spawn-terminal command)
2. Spawn agents with chatroom instructions appended to their prompts
3. Agents join and work independently, using the chatroom to:
   - Ask each other questions ("What endpoint should I call?")
   - Request user decisions ("REST or GraphQL?")
   - Get help when blocked ("Can't find the auth middleware")
   - Post brief status ("Done with API, standing by")
4. User can direct agents via the chatroom terminal
5. Agents return their actual work output to the orchestrator (not the chatroom)
6. When user closes the terminal, agents exit gracefully

## Example Chatroom Messages

**Good:**
- "frontend: Hey backend, what's the response format for /users?"
- "backend: @frontend - JSON with {id, name, email}"
- "backend: User, should I add rate limiting?"
- "frontend: Blocked - need the API key location"
- "backend: Done with auth module, standing by"

**Bad (don't do this):**
- "Here are my 5 research findings: 1. Dragon fruit exports increased..."
- "Implementing the following code: function handleAuth() { ... }"
- "Full analysis complete: The market trends show..."
