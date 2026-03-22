---
name: skill-optimize
version: 1.0.0
description: '[Skill Management] Optimize an existing agent skill'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Optimize an existing skill for token efficiency, clarity, and effectiveness.

**Workflow:**

1. **Analyze** — Review skill structure, line count, progressive disclosure
2. **Optimize** — Reduce SKILL.md size, move details to references, improve clarity
3. **Validate** — Verify skill still works correctly after optimization

**Key Rules:**

- Delegates to `skill-creator` for optimization patterns
- SKILL.md target: under 100 lines with progressive disclosure
- Reference files also under 100 lines each

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

Think harder.
Use `skill-creator` and `claude-code` skills.
Use `docs-seeker` skills to search for documentation if needed.

## Arguments

SKILL: $1 (default: `*`)
PROMPT: $2 (default: empty)

## Your mission

Optimize an existing skill in `.claude/skills/${SKILL}` directory.

**Mode detection:**

- If arguments contain "auto" or "trust me": Skip plan approval, implement directly.
- Otherwise: Propose plan first, ask user to review before implementing.

## Additional instructions

<additional-instructions>$PROMPT</additional-instructions>

## Output Requirements

An output implementation plan must also follow the progressive disclosure structure:

- Always keep in mind that `SKILL.md` and reference files should be token consumption efficient, so that **progressive disclosure** can be leveraged at best.
- `SKILL.md` is always short and concise, straight to the point, treat it as a quick reference guide.
- Create a directory using naming pattern from `## Naming` section.
- Save the overview access point at `plan.md`, keep it generic, under 80 lines, and list each phase with status/progress and links.
- For each phase, add `phase-XX-phase-name.md` files containing sections (Context links, Overview with date/priority/statuses, Key Insights, Requirements, Architecture, Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps).

**IMPORTANT:**

- Skills are not documentation, they are practical instructions for Claude Code to use the tools, packages, plugins or APIs to achieve the tasks.
- Each skill teaches Claude how to perform a specific development task, not what a tool does.
- Claude Code can activate multiple skills automatically to achieve the user's request.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
