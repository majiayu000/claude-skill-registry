---
name: optimizing-claude-md
description: Use when CLAUDE.md is bloated or ineffective. Use when Claude ignores instructions, file exceeds 150 lines, response formatting rules aren't working, or user asks to optimize/restructure their Claude Code configuration.
---

# Optimizing CLAUDE.md

## Overview

Claude Code has a **priority hierarchy** for instructions. Most optimization failures come from putting rules in the wrong tier.

## When to Use

- CLAUDE.md exceeds 150 lines
- Claude ignores rules you've written
- Response formatting directives ("be concise") aren't working
- Multiple sections marked CRITICAL/MANDATORY
- User asks to optimize, restructure, or create CLAUDE.md

## Priority Hierarchy

| Tier | Mechanism | Priority | Purpose |
|---|---|---|---|
| **1. Output styles** | `~/.claude/output-styles/` | System prompt (highest) | Response format, tone, word limits |
| **2. CLAUDE.md** | Project root | User message (medium) | Project rules, safety guardrails |
| **3. .claude/rules/** | `.claude/rules/*.md` | Same as CLAUDE.md, auto-loaded | Topic-specific reference material |
| **4. Auto memory** | `~/.claude/projects/*/memory/` | First 200 lines | Claude's own scratchpad — not for your instructions |

**The #1 mistake:** Putting response formatting rules in CLAUDE.md. They belong in an output style (system prompt level). CLAUDE.md formatting rules get ignored under pressure.

**Auto memory note:** Don't put instructions in MEMORY.md — it's Claude's scratchpad. During optimization, ignore it unless your instructions leaked into it.

**Global vs project:** Project CLAUDE.md rules take precedence over `~/.claude/CLAUDE.md`. Put personal preferences in global, project rules in project. Don't duplicate between them.

## Decision Framework: Keep, Move, or Cut

For each section, ask in order:

1. **Response format rule?** (word limits, tone) → Output style
2. **Would removing it cause mistakes THIS session?** → No: move to `.claude/rules/` or cut. Yes: keep.
3. **Needed every session?** → Yes: keep. No: move to `.claude/rules/`
4. **Discoverable from codebase?** (package.json, READMEs) → Cut it.

## Target: Under 150 lines (best teams run 60-80)

LLMs follow ~150-200 instructions reliably. System prompt uses ~50. Every CLAUDE.md line competes for the rest. If everything is CRITICAL, nothing is.

## Restructuring Workflow

1. **Audit** — Count lines. Classify each section: safety guardrail, project context, reference material, or response formatting.
2. **Extract formatting → output style** — Create `~/.claude/output-styles/<name>.md`. Activate with `/output-style <name>`.
   ```markdown
   ---
   name: Concise
   description: Minimal responses with hard word limits
   keep-coding-instructions: true
   ---
   Max 150 words per response. Bullet points over paragraphs. No preamble before actions.
   ```
3. **Move reference material → `.claude/rules/`** — Auto-loads at same priority. Scope to paths with `paths:` frontmatter when topic-specific. **Never use custom dirs** (`_docs/`, `references/`) — Claude won't auto-load them. **Caveat:** Path-scoped rules only load for matching files — never put safety rules in path-scoped files.
4. **Apply U-shaped attention** — Top: safety guardrails. Middle: project context. Bottom: reference pointers.
5. **Deduplicate across tiers** — Check global CLAUDE.md, project CLAUDE.md, output style, and rules files. Same rule twice = wasted budget.
6. **Add anti-bloat line** at top: `**When adding to this file:** Be terse. Show commands, not prose.`

## Content Classification

| Content type | Destination |
|---|---|
| Word limits, banned phrases, tone | Output style |
| Data-loss prevention rules | CLAUDE.md (top) |
| Path handling gotchas | CLAUDE.md (top) |
| Tech stack, project structure | CLAUDE.md (middle) |
| Architecture patterns | CLAUDE.md (middle) |
| Dev commands, build scripts | `.claude/rules/dev-commands.md` |
| Testing examples, philosophy | `.claude/rules/testing.md` |
| Agent workflows, slash commands | `.claude/rules/agent-os.md` |
| Framework-specific setup | `.claude/rules/` with `paths:` frontmatter |
| Code style enforcement | Linter config, not CLAUDE.md |

## Common Mistakes

| Mistake | Fix |
|---|---|
| "Be concise" in CLAUDE.md | Quantified limits in output style: "max 150 words" |
| Everything marked CRITICAL | Reserve for data-loss prevention only |
| Inline test examples (60+ lines) | Move to `.claude/rules/testing.md` |
| Content moved to custom dirs | Use `.claude/rules/` (official, auto-loaded) |
| Deleting anti-bloat instruction | Keep it — file will grow back without it |
| Over-compressing copyable commands | Keep exact commands; compress prose around them |
| Skipping output styles | Create output style first, then restructure CLAUDE.md |
| Dumping everything into one rules file | Split by topic: `dev-commands.md`, `testing.md`, etc. Same decision framework applies to rules files. |

## When NOT to Use

- File under 100 lines and working well
- Just adding one rule
- Problem is coding behavior, not instruction following
