---
name: skill-plan
description: "[Tooling & Meta] Guide for creating effective skills, adding skill references, skill scripts or optimizing existing skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, frameworks, libraries or plugins usage, or API and tool integrations."
license: Complete terms in LICENSE.txt
---

# Skill Creator

Create and optimize Claude Code skills -- modular packages providing specialized workflows, tool integrations, and domain expertise.

## Skill Structure

```
.claude/skills/skill-name/
  SKILL.md        # Required. <100 lines. Quick reference.
  references/     # Docs loaded on-demand (also <100 lines each)
  scripts/        # Executable code (Node.js/Python preferred)
  assets/         # Output files (templates, images, fonts)
```

For detailed format spec, frontmatter fields, and file organization:
**⚠️ MUST READ:** `.claude/skills/skill-plan/references/skill-structure-guide.md`

## Creation Workflow

1. **Understand** -- Gather concrete usage examples; ask clarifying questions
2. **Plan** -- Identify reusable resources (scripts, references, assets) from examples
3. **Initialize** -- Run `scripts/init_skill.py <name> --path <dir>` for scaffold
4. **Implement** -- Write SKILL.md (<100 lines), create references/scripts/assets
5. **Package** -- Run `scripts/package_skill.py <path>` to validate and zip

## Constraints

- `SKILL.md` must be **<100 lines** (frontmatter + body)
- References/ files also **<100 lines** each; split further if needed
- **Progressive disclosure**: heavy content in references/, not SKILL.md
- Combine related topics into one skill (e.g., cloudflare-* -> devops)
- Imperative writing style ("Create X" not "You should create X")
- No "Task Planning Notes" boilerplate
- Scripts: prefer Node.js/Python, include tests, respect `.env` loading order

## Writing SKILL.md

1. Purpose statement (1-2 lines)
2. Decision tree or workflow steps (concise, <5 lines per step)
3. `Read:` directives to references/ for detailed guidance
4. No inline code examples >5 lines -- move to references/

## Quality Gate

Before finalizing, validate against checklist:
**⚠️ MUST READ:** `.claude/skills/skill-plan/references/skill-quality-checklist.md`

## Iteration

After using a skill on real tasks, watch for: Claude re-discovering known info, ignoring bundled scripts, false triggers, or missed triggers. Update SKILL.md, description keywords, or references accordingly.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
