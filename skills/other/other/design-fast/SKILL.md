---
name: design-fast
version: 1.0.0
description: '[Design] Create a quick design'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

Think hard to plan & start working on these tasks follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules:
<tasks>$ARGUMENTS</tasks>

> **Skill Variant:** Variant of design skills — quick design implementation.

## Quick Summary

**Goal:** Create a quick UI design using design intelligence databases and subagents.

**Workflow:**
1. **Research** — Run `ui-ux-pro-max` searches for design intelligence
2. **Design** — Use `ui-ux-designer` subagent to create the design
3. **Review** — Present to user for approval

**Key Rules:**
- Always activate `ui-ux-pro-max` FIRST for design intelligence
- Default to pure HTML/CSS/JS if user doesn't specify framework
- Use `ai-multimodal` for generating real visual assets

## Required Skills (Priority Order)

1. **`ui-ux-pro-max`** - Design intelligence database (ALWAYS ACTIVATE FIRST)
2. **`frontend-design`** - Quick implementation

**Ensure token efficiency while maintaining high quality.**

## Workflow:

1. **FIRST**: Run `ui-ux-pro-max` searches to gather design intelligence:
    ```bash
    python3 $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<product-type>" --domain product
    python3 $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<style-keywords>" --domain style
    python3 $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<mood>" --domain typography
    python3 $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<industry>" --domain color
    ```
2. Use `ui-ux-designer` subagent to start the design process.
3. If user doesn't specify, create the design in pure HTML/CSS/JS.
4. Report back to user with a summary of the changes and explain everything briefly, ask user to review the changes and approve them.
5. If user approves the changes, update the `./docs/design-guidelines.md` docs if needed.

## Notes:

- Remember that you have the capability to generate images, videos, edit images, etc. with `ai-multimodal` skills. Use them to create the design and real assets.
- Always review, analyze and double check generated assets with `ai-multimodal` skills to verify quality.
- Maintain and update `./docs/design-guidelines.md` docs if needed.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
