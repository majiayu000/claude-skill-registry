---
name: dex-improve
description: Workshop an improvement idea into implementation plan
---

## What This Command Does

**In plain English:** Your design partner for making Dex better. Three ways to use it:

1. **Workshop an idea** — Bring a fuzzy improvement idea, we'll shape it into a concrete plan
2. **Review what's new** — See recent Claude Code changes and how they could improve your system
3. **Full capability audit** — Find features you're not using that could help with your jobs-to-be-done

**When to use it:**
- "I have an idea but don't know how to implement it"
- "What new Claude Code features should I be using?"
- "Am I getting the most out of this system?"

**How to run it:**
```
/dex-improve                           # Shows menu of options
/dex-improve "your idea here"          # Jumps straight to workshopping
```

---

## Entry Point

When invoked, offer these options:

```
How would you like to explore improvements?

1. **I have an idea** — Workshop a specific improvement
2. **What's new?** — Review Claude Code changes since [last check: DATE]
3. **Full audit** — Review all capabilities vs. your current usage

Or just describe your idea and I'll start workshopping.
```

If user provides $IDEA argument, skip to Mode 1 directly.

---

## Mode 1: Workshop an Idea

**Arguments:** $IDEA — High-level description of what you want to improve

### Phase 1: Understand

Parse the idea and frame it back:

1. Identify which Dex areas are involved:
   - Workflows (daily, weekly routines)
   - Automation (scripts, hooks, scheduled tasks)
   - Relationships (people tracking, meetings)
   - Task management (capture, flow, priorities)
   - Projects (planning, tracking, health)
   - Information retrieval (search, lookups)

2. State your understanding in 2-3 sentences
3. Note any ambiguity that needs clarification

### Phase 2: Research + Capability Scan

Build context from multiple sources:

**Internal (always check):**
```
06-Resources/Learnings/                 # What you've learned so far
System/Skills/                       # Existing reusable behaviors
.claude/commands/                    # Existing commands that might overlap
System/pillars.yaml                  # Strategic priorities
```

**External (when needed):**
- Search web for latest Claude Code capabilities
- Check official docs at docs.anthropic.com

Check:
- Does similar functionality already exist?
- What existing patterns could we leverage?

### Phase 3: Capability Match

Map requirements to optimal Claude Code features:

| Requirement Pattern | Suggested Feature | Why |
|---------------------|-------------------|-----|
| "Every time I edit X, do Y" | PostToolUse hook | Automatic trigger after tool completion |
| "Before doing X, check Y" | PreToolUse hook | Validation/confirmation gate |
| "At start of session, load Z" | SessionStart hook | Context injection |
| "Fast search while I work" | Explore sub-agent | Haiku model, runs in parallel |
| "Different perspective on X" | Custom sub-agent | Isolated context, specific focus |
| "Multi-step structured workflow" | Skill | Reusable behavior, always available |
| "Explicit invocation with steps" | Command | User-triggered workflow |
| "Connect to external service" | MCP integration | Tool access to external systems |

Present the capability analysis to the user.

### Phase 4: Expand

Suggest 2-3 adjacent improvements:

- Based on capability analysis, what else could we solve?
- Flag compound opportunities (build A, get B nearly free)
- Connect to existing gaps in the system
- Consider synergies with strategic pillars

Frame as: "While we're here, you might also consider..."

### Phase 5: Refine

Drive toward concrete requirements through focused questions:

- Ask max 2-3 questions at a time
- Validate capability assumptions
- Confirm implementation approach preference
- Identify acceptance criteria

Loop between Research → Expand → Refine until requirements are solid.

### Phase 6: Plan + Update

When requirements are firm:

1. Generate the plan document (see template below)
2. Save to `plans/dex-improvement-[slug].md`
3. Add any new patterns to `06-Resources/Learnings/`
4. Add viable future ideas to backlog

---

## Mode 2: What's New?

Review recent Claude Code changes and suggest improvements.

### Process

1. **Read state file:** `System/claude-code-state.json`
   - If missing, this is first run — do a full scan instead

2. **Fetch current changelog:** Use WebSearch to find latest Claude Code changelog/releases

3. **Compare:** What's new since `last_check` date?

4. **For each new feature, evaluate:**
   - Is this relevant to Dex use cases?
   - What existing workflow could it improve?
   - Does it unlock something previously impossible?

5. **Present findings:**

```
📢 Claude Code Updates (since [last check date])

=== NEW CAPABILITIES ===

1. [Feature Name]
   - What it does: [description]
   - How it could help: [specific Dex improvement]
   - Effort to implement: Low/Medium/High

2. [Feature Name]
   ...

=== SUGGESTED IMPROVEMENTS ===

Based on these new capabilities, here's what you could build:

1. [Improvement name]
   - What: [description]
   - Why: [connects to which pillar/job-to-be-done]
   - Uses: [which new capability]

Want to workshop any of these? (Enter number or describe your own idea)
```

6. **Update state file** with current date and capabilities seen

### State File Format

Location: `System/claude-code-state.json`

```json
{
  "last_check": "2026-01-22",
  "last_version_seen": "1.0.30",
  "features_seen": [
    "hooks",
    "sub-agents",
    "skills",
    "commands",
    "mcp"
  ],
  "features_noted": [
    {
      "version": "1.0.30",
      "feature": "Async hooks",
      "date_seen": "2026-01-22"
    }
  ]
}
```

---

## Mode 3: Full Capability Audit

Review all known Claude Code capabilities against your current system.

### Process

1. **Inventory current usage:**
   - Scan `.claude/` folder for hooks, commands, settings
   - Check `System/Skills/` for skills
   - Check `core/mcp/` for MCP integrations
   - Read `06-Resources/Learnings/` for known patterns

2. **Load capability reference:**
   - Use the capability match table (from Mode 1, Phase 3)
   - Search web for comprehensive Claude Code feature list if needed

3. **Gap analysis:**

```
=== CAPABILITY AUDIT ===

✅ Using Well:
- Commands (12 defined)
- Skills (person-lookup)

⚠️ Underutilized:
- Hooks — No hooks configured. Could automate:
  - Session start: Load context automatically
  - Post-edit: Update related files

❌ Not Using:
- Sub-agents — Could parallelize research tasks
- MCP beyond tasks — Calendar, email integrations possible

=== RECOMMENDATIONS ===

Ranked by impact vs. effort:

1. [High impact, low effort]
   - Add SessionStart hook to load daily context
   - Why: Saves 30 seconds every session
   - Connects to: [pillar]

2. [High impact, medium effort]
   ...
```

4. **Offer to workshop** any recommendation the user wants to pursue

---

## Plan Output Template

Create at: `plans/dex-improvement-[slug].md`

```markdown
# Dex Improvement: [Title]

**Created:** [Date]
**Status:** Planning → In Progress → Complete
**Pillar:** [pillar name if configured]

## Overview

[2-3 sentence summary of what we're improving and why]

## Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Capability Analysis

| Requirement | Implementation | Feature Type | Rationale |
|-------------|----------------|--------------|-----------|
| [req] | [how] | Hook/Sub-agent/Skill/Command | [why this approach] |

## Recommended Approach

[Which Claude Code features to use and why. Include trade-offs considered.]

## Implementation Steps

### Phase 1: [Foundation]
1. [Step]
2. [Step]

### Phase 2: [Core]
1. [Step]
2. [Step]

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `path/to/file` | Create/Modify | [what] |

## Compound Opportunities

[What else we could solve while building this]

- [ ] [Adjacent improvement 1]
- [ ] [Adjacent improvement 2]

## Acceptance Criteria

- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]

## Questions Resolved

- Q: [Question that came up]
- A: [How we decided]
```

---

## Example Interactions

### Mode 1: Workshop
```
/dex-improve "Better meeting action item capture"

> **Understanding:** You want to improve how action items flow from meetings 
> into your task system. This touches workflows (meeting processing) and 
> task management (capture and routing).
>
> **Current state** (from Learnings):
> - Meeting notes go to `00-Inbox/Meetings/`
> - Action items manually extracted during review
>
> **Capability scan:**
> - PostToolUse hook could auto-trigger processing after meeting note creation
> - Sub-agent could parallel process: action items, follow-ups, person updates
>
> **Questions:**
> 1. Where are items getting lost—during capture, or in follow-through?
> 2. Would auto-drafted follow-up emails be valuable?
```

### Mode 2: What's New
```
/dex-improve
> [selects "What's new?"]

> 📢 Claude Code Updates (since 2026-01-15)
>
> === NEW CAPABILITIES ===
> 1. Async Hooks — Hooks can now run without blocking
>    - How it could help: Faster session startup
>    - Effort: Low
>
> === SUGGESTED IMPROVEMENTS ===
> 1. Non-blocking context loading
>    - What: Load learnings/preferences in background
>    - Why: Snappier session starts
>
> Want to workshop any of these?
```

### Mode 3: Full Audit
```
/dex-improve
> [selects "Full audit"]

> === CAPABILITY AUDIT ===
>
> ✅ Using Well: Commands (12), Skills (1)
> ⚠️ Underutilized: Hooks (0 configured)
> ❌ Not Using: Sub-agents, Advanced MCP
>
> === TOP RECOMMENDATION ===
> Add SessionStart hook — saves context loading time every session
>
> Want me to workshop this improvement?
```

---

## Behaviors

### Always Do
- Check internal patterns before suggesting new implementations
- Tie suggestions to user's pillars/jobs-to-be-done when configured
- Update state file after Mode 2 runs
- Offer concrete capability recommendations, not just ideas

### Never Do
- Skip the research phase
- Suggest capabilities without explaining why they fit
- Output a plan before requirements are confirmed
- Make changes without explicit approval

---

## Philosophy

This isn't just requirements gathering—it's capability-aware design. The goal is to help you leverage Claude Code's full potential while building exactly what you need, nothing more.
