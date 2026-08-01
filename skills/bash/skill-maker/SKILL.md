---
name: skill-maker
description: Scaffold a new Claude Code skill following this repo's conventions — copy a canonical template, apply the PATTERNS.md checklist, verify with lint. Use when the user runs /skill-maker, asks to create or package a new skill, or wants to turn a procedure into a slash command.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /skill-maker — Scaffold a New Skill

You turn a described procedure into a working skill: a directory with a `SKILL.md` and a `README.md` that follows this repo's conventions. Input is the user's request; output is a card Claude can follow.

## Usage

```
/skill-maker a skill that turns raw site photos into a numbered photo log
/skill-maker package our submittal-review checklist as a slash command
/skill-maker <any procedure worth repeating>
```

## Hard rule: no interview

Derive everything — name, description, tools, steps — from the request. Do not ask setup questions. Ask exactly one question only if the skill's purpose is genuinely indecipherable from what the user wrote; otherwise make the reasonable call and note it when presenting the result.

## Anatomy of what you're producing

A skill is a procedure card. Four load-bearing parts:

| Part | Job |
|---|---|
| `name` | Kebab-case, matches the directory, becomes the slash command |
| `description` | The **trigger**, not a label — how Claude knows to reach for the card unasked |
| `allowed-tools` | The blast radius — the minimum set the steps need |
| Steps | The procedure itself: numbered, concrete, in execution order |

## Step 1 — Scaffold from the template

Copy `templates/example-skill/` (bundled next to this SKILL.md) and adapt every line. **This skill's output is files on disk, not a proposal**: create the target directory and write both `SKILL.md` and `README.md` immediately — the write permission prompt is the user's approval moment, so never present a draft and wait for a go-ahead first. If the bundled template can't be located, scaffold from the Anatomy table above.

- **Name**: kebab-case, derived from the request. Directory name and frontmatter `name` must match.
- **Description**: trigger-phrased — what the skill does AND when to invoke it, with phrases the user would actually say. A description that only labels never fires.
- **allowed-tools**: only what the steps actually need. Read-only skill? No Write. No shell work? No Bash.
- **Steps**: concrete and numbered, in the order the work happens. Include an output-format block when the skill produces a document or record. Nothing from the template survives verbatim except the shape.
- **README.md**: adapt alongside — what it does, usage, nothing more.

**Where it goes** — detect the target:

| Condition | Target |
|---|---|
| cwd is the skills-for-architects repo — root `.claude-plugin/plugin.json` exists with name `architecture-studio` | `skills/{name}/` |
| any other project | `.claude/skills/{name}/` in the project |
| user explicitly asks for a global skill | `$HOME/.claude/skills/{name}/` |

## Step 2 — Apply the conventions checklist

Read `PATTERNS.md` at runtime — repo installs have it at the plugin root — and apply its rules to the scaffolded skill. Do not work from a remembered copy; the file is the authority.

Enforce these portable essentials regardless of target:

1. Description states **what** and **when**.
2. `README.md` exists alongside `SKILL.md`.
3. No `~/` paths in the SKILL.md body — they break on every machine but the author's. Use project-relative paths, or `$HOME` in the rare case a home path is the point.
4. `allowed-tools` is the minimum blast radius for the steps as written.
5. If the skill produces code, zoning, or life-safety analysis, its steps must instruct ending every report with the canonical disclaimer block followed by the marker `<!-- architecture-studio:requires-disclaimer -->` — see how `skills/occupancy-calculator/SKILL.md` does it.

## Step 3 — Verify

**Inside the repo:** run `scripts/lint.sh` with Bash and fix findings until green. Then remind the author: a new skill moves the catalog counts — the root README (catalog table, Skill Groups, "N skills" claims), the `/skills` menu headline, and the manifest descriptions all state counts the lint checks against the tree.

**Outside the repo:** run the Step 2 checklist explicitly, item by item, and say so. The house lint applies only to catalog contributions — a private skill owes it nothing.

## Finish

The job is done only when both files exist on disk — confirm their paths, then show the finished SKILL.md to the user. Tell them:

- **How to invoke it**: `/{name}` plus whatever the skill takes after the slash.
- **How to iterate**: edit the SKILL.md like any file — change a step, tighten the description, run it again.

Never commit anything; that's the author's call.
