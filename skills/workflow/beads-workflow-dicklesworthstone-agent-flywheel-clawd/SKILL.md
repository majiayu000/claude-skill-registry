---
name: beads-workflow
description: "Converting markdown plans into beads (tasks with dependencies) and polishing them until they're implementation-ready. The bridge between planning and agent swarm execution. Includes exact prompts used."
---

# Beads Workflow — From Plan to Actionable Tasks

> **Core Principle:** "Check your beads N times, implement once" — where N is as many as you can stomach.
>
> Beads are so detailed and polished that you can mechanically unleash a big swarm of agents to implement them, and it will come out just about perfectly.

---

## What Are Beads?

Beads are **epics/tasks/subtasks with dependency structure**, optimized for AI coding agents. Think of them as Jira or Linear, but designed for machines.

Key properties:
- **Self-contained** — Never need to refer back to the original markdown plan
- **Self-documenting** — Include background, reasoning, justifications, considerations
- **Dependency-aware** — Explicit structure of what blocks what
- **Rich descriptions** — Long markdown comments, not short bullet points

---

## Why Beads Work

```
┌─────────────────────────────────────────────────────────────┐
│ MARKDOWN PLAN (~3,500 lines)                                │
│   └─► Fits in context window                                │
│   └─► Models reason about entire system at once             │
├─────────────────────────────────────────────────────────────┤
│                    ↓ CONVERT TO BEADS ↓                     │
├─────────────────────────────────────────────────────────────┤
│ BEADS (distributed tasks)                                   │
│   └─► Each bead is self-contained                           │
│   └─► Any agent can pick up any bead                        │
│   └─► BV (Beads Viewer) handles prioritization              │
│   └─► Agent Mail handles coordination                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Converting Plans to Beads

### THE EXACT PROMPT — Plan to Beads Conversion (Claude Code + Opus 4.5)

```
OK so now read ALL of PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md; please take ALL of that and elaborate on it and use it to create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.). The beads should be so detailed that we never need to consult back to the original markdown plan document. Remember to ONLY use the `bd` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

**Note:** Replace `PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md` with your actual plan filename.

### Alternative Shorter Version

```
OK so please take ALL of that and elaborate on it more and then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.)  Use only the `bd` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

### What This Creates

- Tasks and subtasks with clear scope
- Dependency links (what must complete before what)
- Detailed descriptions with:
  - Background context
  - Reasoning and justification
  - Technical considerations
  - How it serves project goals

---

## Polishing Beads

### Why Polish?

Even after initial conversion, beads continue to improve with review. You get incremental improvements even at round 6+.

### THE EXACT PROMPT — Polish Beads (Full Version)

```
Reread AGENTS dot md so it's still fresh in your mind. Then read ALL of PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md . Use ultrathink. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things! DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY! Also make sure that as part of the beads we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. It's critical that EVERYTHING from the markdown plan be embedded into the beads so that we never need to refer back to the markdown plan and we don't lose any important context or ideas or insights into the new features planned and why we are making them.
```

### THE EXACT PROMPT — Polish Beads (Standard Version)

```
Reread AGENTS dot md so it's still fresh in your mind. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things!

DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY!

Also, make sure that as part of these beads, we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. Remember to ONLY use the `bd` tool to create and modify the beads and to add the dependencies to beads. Use ultrathink.
```

### Polishing Protocol

1. Run the polishing prompt
2. Review changes
3. Repeat until steady-state (typically 6-9 rounds)
4. If it flatlines, start a fresh CC session
5. Optionally have Codex with GPT 5.2 do a final round

---

## Fresh Session Technique

If polishing starts to flatline, start a brand new Claude Code session:

### THE EXACT PROMPT — Re-establish Context

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project.  Use ultrathink.
```

### THE EXACT PROMPT — Then Review Beads

```
We recently transformed a markdown plan file into a bunch of new beads. I want you to very carefully review and analyze these using `bd` and `bv`.
```

Then follow up with the standard polish prompt.

---

## Cross-Model Review

For extra polish, have different models review the beads:

| Model | Strength |
|-------|----------|
| **Claude Code + Opus 4.5** | Primary creation and refinement |
| **Codex + GPT 5.2** | Final review pass |
| **Gemini CLI** | Alternative perspective |

---

## Bead Quality Checklist

Before implementation, verify each bead:

- [ ] **Self-contained** — Can be understood without external context
- [ ] **Clear scope** — One coherent piece of work
- [ ] **Dependencies explicit** — Links to blocking/blocked beads
- [ ] **Testable** — Clear success criteria
- [ ] **Includes tests** — Unit tests and e2e tests in scope
- [ ] **Preserves features** — Nothing from the plan was lost
- [ ] **Not oversimplified** — Complexity preserved where needed

---

## Using bd (Beads CLI)

### Basic Commands

```bash
# Initialize beads in project
bd init

# Create a new bead
bd create "Implement user authentication" -t feature -p 1

# Add dependencies
bd depend BD-123 BD-100  # BD-123 depends on BD-100

# Update status
bd update BD-123 --status in_progress

# Close a bead
bd close BD-123 --reason "Completed and tested"

# List ready beads (no blockers)
bd ready --json
```

### Robot Mode for Agents

```bash
# Get triage recommendations
bv --robot-triage

# Get the single top pick
bv --robot-next

# Get parallel execution tracks
bv --robot-plan

# Get graph insights (PageRank, bottlenecks, cycles)
bv --robot-insights
```

**CRITICAL:** Never run bare `bv` — it launches interactive TUI. Always use `--robot-*` flags.

---

## Integration with Agent Mail

### Conventions

- Use Beads issue ID as Mail `thread_id`: `send_message(..., thread_id="bd-123")`
- Prefix subjects: `[bd-123] Starting auth refactor`
- Include issue ID in file reservation `reason`: `file_reservation_paths(..., reason="bd-123")`

### Typical Flow

```bash
# 1. Pick ready work
bd ready --json

# 2. Reserve files
file_reservation_paths(project_key, agent_name, ["src/**"], reason="bd-123")

# 3. Announce start
send_message(..., thread_id="bd-123", subject="[bd-123] Starting work")

# 4. Work on the bead
# ...

# 5. Complete
bd close bd-123 --reason "Completed"
release_file_reservations(project_key, agent_name)
```

---

## Test Coverage Beads

### THE EXACT PROMPT — Add Test Coverage

```
Do we have full unit test coverage without using mocks/fake stuff? What about complete e2e integration test scripts with great, detailed logging? If not, then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid with detailed comments.
```

---

## When Beads Are Ready

Your beads are ready for implementation when:

1. **Steady-state reached** — Multiple polishing rounds yield minimal changes
2. **Cross-model reviewed** — At least one alternative model has reviewed
3. **No cycles** — `bv --robot-insights | jq '.Cycles'` returns empty
4. **Tests included** — Each feature bead has associated test beads
5. **Dependencies clean** — Graph makes logical sense

---

## Example Bead Structure

A well-formed bead looks like:

```
ID: BD-123
Title: Implement OAuth2 login flow
Type: feature
Priority: P1
Status: open

Dependencies: [BD-100 (User model), BD-101 (Session management)]
Blocks: [BD-200 (Protected routes), BD-201 (User dashboard)]

Description:
Implement OAuth2 login flow supporting Google and GitHub providers.

## Background
This is the primary authentication mechanism for the application.
Users should be able to sign in with existing Google/GitHub accounts
to reduce friction.

## Technical Approach
- Use NextAuth.js for OAuth2 implementation
- Store provider tokens encrypted in Supabase
- Create unified user record on first login
- Handle account linking for multiple providers

## Success Criteria
- User can click "Sign in with Google/GitHub"
- OAuth flow completes and redirects to dashboard
- User record created/updated in database
- Session cookie set correctly
- Logout clears session properly

## Test Plan
- Unit: Token encryption/decryption
- Unit: User record creation
- E2E: Full OAuth flow (mock provider)
- E2E: Account linking scenario

## Considerations
- Handle provider API rate limits
- Graceful degradation if provider is down
- GDPR compliance for EU users
```

---

## Complete Prompt Reference

### Plan to Beads (Full)
```
OK so now read ALL of PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md; please take ALL of that and elaborate on it and use it to create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.). The beads should be so detailed that we never need to consult back to the original markdown plan document. Remember to ONLY use the `bd` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

### Plan to Beads (Short)
```
OK so please take ALL of that and elaborate on it more and then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting (including relevant background, reasoning/justification, considerations, etc.-- anything we'd want our "future self" to know about the goals and intentions and thought process and how it serves the over-arching goals of the project.)  Use only the `bd` tool to create and modify the beads and add the dependencies. Use ultrathink.
```

### Polish Beads (Full)
```
Reread AGENTS dot md so it's still fresh in your mind. Then read ALL of PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md . Use ultrathink. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things! DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY! Also make sure that as part of the beads we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. It's critical that EVERYTHING from the markdown plan be embedded into the beads so that we never need to refer back to the markdown plan and we don't lose any important context or ideas or insights into the new features planned and why we are making them.
```

### Polish Beads (Standard)
```
Reread AGENTS dot md so it's still fresh in your mind. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. It's a lot easier and faster to operate in "plan space" before we start implementing these things!

DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY!

Also, make sure that as part of these beads, we include comprehensive unit tests and e2e test scripts with great, detailed logging so we can be sure that everything is working perfectly after implementation. Remember to ONLY use the `bd` tool to create and modify the beads and to add the dependencies to beads. Use ultrathink.
```

### Fresh Session — Context
```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project.  Use ultrathink.
```

### Fresh Session — Review
```
We recently transformed a markdown plan file into a bunch of new beads. I want you to very carefully review and analyze these using `bd` and `bv`.
```

### Add Test Coverage
```
Do we have full unit test coverage without using mocks/fake stuff? What about complete e2e integration test scripts with great, detailed logging? If not, then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid with detailed comments.
```

---

## Common Mistakes

1. **Oversimplifying** — Preserve complexity where it's needed
2. **Losing features** — Every plan feature should become beads
3. **Skipping tests** — Include unit and e2e test beads
4. **Single review** — Keep polishing until truly steady-state
5. **Missing dependencies** — Make all blocking relationships explicit
6. **Short descriptions** — Beads should be verbose and self-documenting
