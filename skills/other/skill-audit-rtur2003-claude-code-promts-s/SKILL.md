---
name: skill-audit
description: Use when a skill isn't triggering as expected, before adding a new skill (to check for a name collision), during periodic cleanup of an accumulated skills directory, or when asked to review skill quality — checks frontmatter validity, description quality against Skill Discovery Optimization conventions, body size, and cross-scope name collisions.
---

# Skill Audit

## Overview

Skills accumulate. Nobody deletes them, most developers hit 8-12 installed skills before the per-session token cost of loading every description starts to outweigh the benefit, and a skill installed at both the personal and project scope with the same name fails silently — the higher-precedence one wins and the other never fires, with no error anywhere. This script checks the mechanical properties that predict a skill working or silently failing: valid frontmatter, a description that leads with the trigger (not a workflow summary), a body under the token-efficiency guideline, and no name collision across scopes.

**Core principle:** A skill that never triggers and a skill that doesn't exist have the same effect on the user, but only one of them is visible in a directory listing. This script finds the invisible kind.

## Usage

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py [skills_dir ...]
```

With no arguments, checks `.claude/skills/` (project) and `~/.claude/skills/` (personal) if they exist. Pass explicit paths to also check a plugin's `skills/` directory (plugin skill dirs aren't auto-discovered, since a plugin's install location varies). Exit code 0 = clean, 1 = findings, 2 = usage error.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py .claude/skills ~/.claude/skills ./my-plugin/skills
```

## What it checks

| Check | Why it matters |
|---|---|
| Frontmatter parses | A `SKILL.md` without valid `---`-delimited YAML at the top is invisible to Claude Code — not degraded, just never loaded |
| `name` field matches directory name | The command comes from the directory name for personal/project skills; a mismatched `name` field is almost always a copy-paste leftover from another skill |
| Description opens with a trigger phrase | Per Skill Discovery Optimization: "Route the task and adopt it as your instructions" (what it does) trains the model to act on the summary instead of reading the body; "Use when the user names a task" (when to fire) doesn't |
| Description doesn't summarize the workflow | A description that describes the *process* ("dispatches a subagent per task, reviews between each") gives the model a shortcut that has been observed to cause it to skip steps the actual skill body specifies |
| Description length | Over 1024 characters fails the Agent Skills spec limit |
| Body word count | Past ~2000 words (~500 lines), token cost per invocation is high enough that a reference file loaded on demand almost always beats keeping everything inline |
| Cross-scope name collisions | Two `SKILL.md` files with the same `name` (or same directory name) at different scopes — one always wins, the other never triggers, and nothing tells you which |

## What it does not check

Whether the skill's *instructions* are correct, whether it actually gets invoked on the prompts it should (that requires running real scenarios — see the with-skill/without-skill baseline in [`agent-skills-prompt.md`](../../../prompts/english/agents/agent-skills-prompt.md)), or whether supporting files referenced from the body actually exist and are useful. This script catches the mechanical failure modes; it is not a substitute for testing trigger accuracy.

## Remember

> A clean audit means the skill is *structurally* capable of working. It says nothing about whether it triggers on the right prompts or produces the right output — that's a separate, behavioral test, not a static one.
