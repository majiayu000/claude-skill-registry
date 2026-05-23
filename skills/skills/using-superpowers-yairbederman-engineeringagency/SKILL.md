---
name: using-superpowers
description: Use at conversation start - establishes how to find and use skills, requiring skill loading before ANY response
---

# Using Skills

## The Rule

**Load and apply relevant skills BEFORE any response or action.** Even a 1% chance a skill might apply means you should check. If a skill turns out to be wrong for the situation, you don't need to use it.

## How to Access Skills

Skills are located in `global_workflows/skills/`. Each skill folder contains a `SKILL.md` file with:
- YAML frontmatter: `name` and `description`
- Detailed instructions for when and how to apply the skill

**To use a skill:**
1. Read the `SKILL.md` file
2. Announce: "Applying [skill-name] skill for [purpose]."
3. Follow the skill instructions exactly

## Mode-Based Auto-Loading

Skills are automatically applicable based on the current Engineering Agent mode:

| Agent Mode | Applicable Skills |
|------------|-------------------|
| ProductSpecReview | `brainstorming` |
| FeaturePlanning | `brainstorming`, `writing-plans` |
| TechSpec | `writing-plans` |
| TaskPlanning | `writing-plans` |
| Implementation | `test-driven-development`, `executing-plans` |
| BugFix | `test-driven-development` |
| CodeReview | `requesting-code-review` |

## Common Rationalizations (Don't Fall For These)

| Rationalization | Reality |
|-----------------|---------|
| "I already know TDD" | Skills have specific checklists. Read them. |
| "This is quick, no skill needed" | Simple things become complex. Use the skill. |
| "I'll check the skill later" | Check BEFORE doing anything. |
| "The skill is overkill" | Discipline prevents mistakes. |

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (brainstorming, writing-plans): Adapt principles to context.

The skill itself tells you which type it is.
