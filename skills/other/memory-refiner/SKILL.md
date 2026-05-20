---
name: memory-refiner
description: Use this skill when the user asks to refine Codex memory, improve Codex instructions or config, analyze session or history patterns, optimize context efficiency, or update global or project-local Codex guidance based on repeated interaction patterns.
metadata:
  short-description: Refine Codex memory and config from history and active instruction layers
---

# Memory Refiner

## Overview

Use this skill to audit how Codex is configured and instructed, then suggest targeted improvements. This skill is Codex-specific: analyze Codex files and usage patterns, not Claude files.

## When To Use

Use this skill when the user asks to:
- refine or optimize Codex memory, instructions, rules, or config
- analyze repeated session patterns or recurring corrections
- reduce context bloat or reorganize guidance for lazy loading
- separate global guidance from project-local overrides

## Workflow

### 1. Collect Evidence

- Use the current conversation as the highest-signal short-term evidence.
- Treat interruption or abort notices in the current conversation (for example `Conversation interrupted` or `turn_aborted`) as workflow signals, even if they do not appear in `history.jsonl`.
- Run `python3 scripts/scan_history.py --format markdown` to summarize `~/.codex/history.jsonl`.
- Look for repeated preferences, repeated corrections, interruption or abort signals, approval friction, context bloat, stale guidance, and recurring task patterns.

### 2. Audit Active Memory Surfaces

- Run `python3 scripts/list_memory_surfaces.py --cwd "$PWD" --format markdown`.
- Read only the files that are relevant to the request.
- Include the current project's local `.codex/` when present.
- Include repo-local instruction files such as `AGENTS.md` when present.

### 3. Apply Scope Precedence

Use this precedence when evaluating what should win for the current repo:

1. Current project `.codex/`
2. Repo-local `AGENTS.md` or similar repo-local instruction files
3. Global `~/.codex`

Flag shadowing, duplication, and conflicts across these scopes.

### 4. Synthesize Recommendations

- Separate findings by scope: global, project-local, and repo-local.
- Keep universal guidance project, language, framework, and technology agnostic unless repeated evidence strongly justifies specificity.
- Treat explicit user statements as higher priority than inferred preferences.
- Do not turn one-off incidents into permanent memory.

### 5. Suggest Before Applying

For each recommendation, provide:
- target file
- scope
- priority
- change type: `add`, `modify`, `move`, `delete`, or `split`
- exact proposed change or diff-ready text
- a short rationale tied to evidence

Do not apply changes until the user approves the specific items.

### 6. Apply Approved Changes

- Apply only the approved subset.
- Re-check for conflicts after editing.
- Re-run surface discovery if the scope layout changed.

## In Scope

- `~/.codex/AGENTS.md`
- `~/.codex/instructions/**/*.md`
- `~/.codex/rules/*.rules`
- `~/.codex/config.toml`
- `~/.codex/skills/*/SKILL.md`
- `~/.codex/skills/*/agents/openai.yaml`
- current project `.codex/**/*.{md,toml,rules,yaml,yml}`
- current project `AGENTS.md`

## Out Of Scope By Default

- Claude config or Claude skills
- unrelated repositories' `.codex/` directories
- auth, sqlite, logs, tmp, sessions, caches, and shell history
- raw history dumps when a compact summary is enough

## Output Style

- Be compact and evidence-based.
- Separate facts, assumptions, and recommendations.
- Prefer moving specialized guidance out of global or root files into lazy-loaded files when appropriate.
