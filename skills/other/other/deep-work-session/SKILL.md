---
name: deep-work-session
description: Enter and manage Deep Work sessions in Agent Hive. Use this skill when starting a focused work session on a project, generating session context, following the handoff protocol, or managing your responsibilities as an agent during a work session.
---

# Deep Work Session

A Deep Work session is a focused period where an AI agent works on a specific Agent Hive project. This skill guides you through the complete session lifecycle.

## Session Lifecycle

```
1. ENTER -> 2. CLAIM -> 3. WORK -> 4. UPDATE -> 5. HANDOFF
```

## Starting a Deep Work Session

### Via Dashboard

1. Run the dashboard:
   ```bash
   make dashboard
   # Or: uv run streamlit run src/dashboard.py
   ```

2. Open http://localhost:8501
3. Select a project from the sidebar
4. Click "Generate Context"
5. Copy the context and paste to your AI agent

### Via Script

```bash
make session PROJECT=projects/your-project
# Or: ./scripts/start_session.sh projects/your-project
```

### Manual Entry

Read the AGENCY.md file directly and follow the protocol below.

## Your Responsibilities

When entering a Deep Work session, you MUST:

1. **Read AGENCY.md first** - Understand the project context fully
2. **Claim the project** - Set `owner` to your agent name
3. **Work on priority tasks** - Focus on highest priority incomplete items
4. **Update progress** - Mark tasks complete, add notes
5. **Handle blocking** - Set `blocked: true` if you need help
6. **Follow handoff protocol** - Clean up state before ending

## Claiming a Project

Before starting work, verify and update the frontmatter:

```yaml
# Check these are true:
status: active        # Must be active
blocked: false        # Must not be blocked
owner: null           # Must be unclaimed

# Then set owner:
owner: "claude-sonnet-4"
last_updated: "2025-01-15T14:30:00Z"
```

## Working on Tasks

### Task Prioritization

Work on tasks in this order:
1. Tasks marked `critical` priority
2. Tasks marked `high` priority
3. Tasks that unblock other projects
4. Remaining tasks by document order

### Marking Progress

Update the markdown content as you complete tasks:

```markdown
## Tasks
- [x] Research existing solutions    # Completed
- [x] Design architecture            # Completed
- [ ] Implement core feature         # In progress
- [ ] Write tests                    # Not started
```

### Adding Agent Notes

Document your work with timestamped notes:

```markdown
## Agent Notes
- **2025-01-15 15:45 - claude-sonnet-4**: Completed architecture design.
  Chose event-driven pattern for scalability. Implementation ready to begin.
- **2025-01-15 14:30 - claude-sonnet-4**: Starting research phase.
  Will evaluate 3 existing solutions.
```

## Handling Blockers

If you encounter something you cannot resolve:

```yaml
blocked: true
blocking_reason: "Need database credentials from DevOps team"
status: blocked  # Optional: change status too
```

Add a note explaining:
```markdown
- **2025-01-15 16:00 - claude-sonnet-4**: BLOCKED - Cannot proceed with
  database integration. Need credentials from DevOps. Created ticket #123.
```

## Handoff Protocol

Before ending your session, you MUST complete these steps:

### 1. Update All Completed Tasks
Mark everything you finished with `[x]`

### 2. Update Timestamp
```yaml
last_updated: "2025-01-15T16:30:00Z"
```

### 3. Add Final Notes
Document what was accomplished and any context for the next agent:

```markdown
- **2025-01-15 16:30 - claude-sonnet-4**: Session complete. Finished
  research and design phases. Implementation is ready to begin - start
  with `src/feature.py`. Note: the authentication module has a known
  issue (see issue #45).
```

### 4. Release or Retain Ownership

**If completely done with the project:**
```yaml
owner: null
status: completed  # If all tasks done
```

**If handing off to another agent:**
```yaml
owner: null
status: active  # Keep active for next agent
```

**If you'll continue later:**
```yaml
owner: "claude-sonnet-4"  # Keep ownership
# Add note about when you'll return
```

### 5. Set Blocking if Needed
```yaml
blocked: true  # Only if external help needed
blocking_reason: "Waiting for API access approval"
```

## Generated Context Format

The Dashboard generates this context package:

```markdown
# DEEP WORK SESSION CONTEXT
# Project: project-id
# Generated: 2025-01-15T14:30:00

---

## YOUR ROLE
[Responsibilities and instructions]

---

## AGENCY.MD CONTENT
[Full AGENCY.md file with frontmatter and content]

---

## PROJECT FILE STRUCTURE
[Directory tree of project files]

---

## AVAILABLE COMMANDS
[What actions you can take]

---

## HANDOFF PROTOCOL
[Required steps before ending]

---

## BOOTSTRAP COMPLETE
[Signal to begin work]
```

## Best Practices

1. **Claim immediately** - Prevent conflicts with other agents
2. **Update frequently** - Keep state current throughout session
3. **Be thorough in notes** - Future agents need context
4. **Don't overcommit** - Better to complete fewer tasks well
5. **Clean handoff** - Always follow the handoff protocol
6. **Use coordinator** - If available, use real-time coordination server

## Session Checklist

### Starting
- [ ] Read AGENCY.md completely
- [ ] Verify project is claimable
- [ ] Set `owner` to your agent name
- [ ] Update `last_updated`
- [ ] Identify highest priority task

### During
- [ ] Mark tasks as you complete them
- [ ] Add notes for significant progress
- [ ] Set `blocked` if you hit a wall
- [ ] Update `last_updated` periodically

### Ending
- [ ] All completed tasks marked with [x]
- [ ] Final `last_updated` timestamp
- [ ] Comprehensive closing notes added
- [ ] `owner` released or retained intentionally
- [ ] `status` updated if appropriate
- [ ] `blocked`/`blocking_reason` set if needed
