---
name: codex-retrospective
description: Use when you want Codex to review its own recent history (last N days or specific period) and improve its behavior. Produces minimal, high-signal updates to AGENTS.md and tiny reusable skills. The goal is long-term fluency — Codex gradually becomes better at your specific style, constraints, and workflows.
---

# Codex Retrospective

A structured self-improvement loop for Codex.

This skill turns Codex from a one-off collaborator into a system that **gets meaningfully better at working with you** over time by systematically eating its own usage history.

## Why This Exists

Most people improve their agent usage by manually maintaining `AGENTS.md` or skills when they notice problems. This skill makes that process deliberate, regular, and high-leverage.

It is directly inspired by strong practices from heavy users (especially Greg Brockman's emphasis on updating the "constitution" from real failures and friction), but executed as a repeatable arsenal-style workflow.

## Core Principle

**Minimal effective change, grounded in evidence from actual history.**

Every output must be:
- The smallest possible useful addition or edit
- Backed by specific patterns observed in recent sessions
- Designed to prevent repetition of the same friction

## When to Trigger

- After a painful or repetitive session ("Codex should have known better by now")
- Periodically (weekly or monthly): "Do a retrospective on the last 7/30 days of my Codex usage"
- When `codex-fluent` reports that Codex is constantly re-asking for the same context or preferences
- After you have manually corrected the same class of mistake multiple times

## The Retrospective Process

### 1. Scope Definition

You specify the time window or focus area:
- "Last 14 days"
- "The three big auth + payments threads from last month"
- "All sessions involving the new Go service"

### 2. History Analysis (The Skill Guides Codex)

Codex is instructed to look for:
- Recurring mistakes or inefficient patterns
- Things the user had to explain or correct repeatedly
- High-friction moments (lots of back-and-forth, context loss, wrong assumptions)
- Successful patterns worth encoding so they happen by default
- Opportunities to extract tiny, reusable skills

### 3. Output — Strict Format

The skill forces Codex to produce output in this order:

1. **Retrospective Summary** (short, evidence-based)
2. **Proposed AGENTS.md Updates** (exact diff or append text only)
3. **New or Refined Minimal Skills** (at most 1-2 tiny ones, full SKILL.md with frontmatter)
4. **Rationale + Evidence** (which sessions/patterns drove each proposal)
5. **Application Plan** (how to safely apply the changes)

### 4. Human Gate + Application

You review. The skill then helps you apply the minimal changes cleanly (never blindly overwriting large sections of AGENTS.md).

## Relationship with codex-fluent

These two skills are designed to be used together:

- `codex-retrospective` finds **behavioral and knowledge** improvements (better defaults, new rules, extracted skills).
- `codex-fluent` finds **state and context** hygiene improvements (session bloat, missing handoffs, archive opportunities).

A good monthly ritual for serious users:
1. Run `codex-retrospective` on the last 30 days.
2. Run `codex-fluent` diagnosis.
3. Apply the best changes from both.

## Hard Constraints on Output

- Never propose large rewrites of AGENTS.md.
- Never create big new skills. Tiny, focused, high-ROI only.
- Every proposal must reference concrete history ("In the payment retry thread on May 3rd and the similar incident on May 18th...").
- If nothing high-confidence was found, say so clearly instead of manufacturing improvements.

## References

- `references/retrospective-prompt.md` — The core prompt template used to drive Codex's self-analysis
- `references/agents-md-update-rules.md` — Strict rules for what kind of changes are acceptable
- `references/minimal-skill-criteria.md` — What qualifies as a "tiny useful skill" worth extracting
- `references/examples/` — Real (sanitized) retrospective outputs and the resulting AGENTS.md diffs

## Success Looks Like

After 4–8 weeks of regular use:
- Codex makes fewer basic assumption errors in your domain
- You spend less time re-explaining preferences and constraints
- Your AGENTS.md and skills folder feel like they were written by someone who has worked with you for a long time (because they were)
- New projects ramp up faster because the constitution already encodes hard-won lessons

Start with a focused 7- or 14-day retrospective on a project where you've felt the most friction recently. The pattern will become natural quickly.