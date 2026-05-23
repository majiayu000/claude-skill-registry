---
name: planning-setup
description: Sets up planning-with-files infrastructure for complex projects. Creates task_plan.md, findings.md, progress.md, updates CLAUDE.md with methodology guidance, and adds .claude/rules enforcement. Use when starting a project that will require >5 tool calls or complex multi-step work.
---

# Planning Setup Skill

I scaffold planning-with-files infrastructure for your project:
- Three planning files (task_plan.md, findings.md, progress.md)
- CLAUDE.md methodology guidance
- .claude/rules enforcement for planning discipline

## When to Use This vs EnterPlanMode

- **Use this skill** when starting a new project that needs persistent planning infrastructure across sessions
- **Use EnterPlanMode** for single-session implementation tasks where built-in task tracking suffices

This skill creates files that persist; EnterPlanMode is for in-session planning that doesn't need to survive restarts.

## Interactive Setup Workflow

I use the `AskUserQuestion` tool to gather your preferences interactively, presenting options with descriptions so you can make informed choices. I'll ask you 6-8 questions to customize the planning infrastructure:

1. **Project name**: What should I call this project?
2. **Goal**: What's the one-sentence goal of this project?
3. **Phases**: What are the major phases? (Or should I suggest phases based on the goal?)
4. **Key questions**: What are the 3-5 key questions this project needs to answer?
5. **Constraints**: What constraints or requirements should I know about?
6. **File location**: Should planning files go in the project root or a subdirectory (like `planning/` or `docs/`)?
7. **CLAUDE.md**: Does CLAUDE.md already exist? Should I create it or append to it?
8. **Hybrid tracking**: Want to use TaskCreate/TaskUpdate for individual tasks within phases?

## What Gets Created

### Planning Files (Customized from Templates)

**task_plan.md** - Phase tracking, decisions, errors
- Goal and current phase
- Phase checklist with status
- Key questions to answer
- Decisions made table
- Errors encountered table

**findings.md** - Research discoveries, visual findings
- Requirements section
- Research findings
- Technical decisions table
- Issues encountered
- Visual/browser findings (with 2-Action Rule reminder)

**progress.md** - Session log, test results
- Session-by-session log format
- Test results table
- Error log
- 5-Question Reboot Check

### CLAUDE.md Updates

Adds planning methodology section:
- High-level overview
- When to use planning-with-files
- Reference to this skill

### .claude/rules/planning-with-files.md

Enforcement rules:
- **Create plan first** - For complex tasks requiring >5 tool calls
- **2-Action Rule** - Save findings after browser/search ops
- **Read before decide** - Refresh goals before major decisions
- **Log all errors** - Track and mutate approach

## Workflow

After gathering your answers, I:

1. Create the planning directory (if requested)
2. Generate customized task_plan.md with your goal, phases, and questions
3. Generate findings.md with initial structure
4. Generate progress.md with session log template
5. Update or create CLAUDE.md with planning guidance
6. Create .claude/rules/planning-with-files.md with enforcement rules
7. Provide a summary of what was created and how to use it

## Integration with TaskCreate/TaskUpdate

The planning-with-files approach works alongside Claude's built-in task tools:
- **task_plan.md** tracks project phases (high-level)
- **TaskCreate/TaskUpdate** manage individual tasks within each phase (granular)

This hybrid approach gives you:
- Big-picture phase tracking in files
- Detailed task management in the task system
- Full context preserved across sessions

## After Setup

Once setup is complete, see [references/usage-guide.md](references/usage-guide.md) for:
- Daily workflow
- When to update each file
- The 5-Question Reboot Test
- Working with the 4 core rules

For the principles behind this system, see [references/manus-principles.md](references/manus-principles.md).

## Templates

All templates are in [templates/](templates/) and are customized during setup.
