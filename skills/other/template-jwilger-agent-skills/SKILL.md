---
name: skill-name
description: >-
  What this skill teaches and when to activate it. Include keywords
  agents use to match tasks. Max 1024 characters.
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: build
  standalone: true
---

# Skill Name

**Value:** _Name the XP value(s) this skill serves -- feedback, communication,
simplicity, courage, or respect -- and state in one sentence why this skill
embodies that value._

## Purpose

What this skill teaches the agent to do and why it matters. Two to three
sentences maximum. State the problem it solves and the outcome it produces.

## Practices

_This is the main body. Concrete, actionable instructions the agent follows.
Write as imperative directives, not explanations. Principles first, then steps._

### Practice Name

State the practice as a clear rule. Explain why in one sentence. Then give
the steps.

1. Step one
2. Step two
3. Step three

**Example:**
```
Brief, concrete example showing the practice applied.
Keep examples minimal -- just enough to demonstrate the pattern.
```

### Another Practice

Repeat the pattern. Each practice should be independently understandable.

**Do:**
- Specific action the agent should take
- Another specific action

**Do not:**
- Specific anti-pattern and why it fails
- Another anti-pattern

## Enforcement Note

_State honestly what this skill can and cannot guarantee._

This skill provides advisory guidance. It instructs the agent on correct
behavior but cannot mechanically prevent violations. On harnesses with plugin
support (Claude Code hooks, OpenCode event hooks), enforcement plugins can add
mechanical guardrails. On harnesses without enforcement, the agent follows
these practices by convention. If you observe the agent violating a practice,
point it out. For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

_Self-check criteria the agent runs through after applying this skill._

After completing work guided by this skill, verify:

- [ ] Criterion one (specific, observable, binary)
- [ ] Criterion two
- [ ] Criterion three

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **other-skill-name:** How it complements this skill (one sentence)
- **another-skill:** How it complements this skill (one sentence)

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill other-skill-name
```
