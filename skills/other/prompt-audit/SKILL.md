---
name: prompt-audit
description: Audit a prompt the user is about to send to Claude (or another coding AI) for completeness and effectiveness. Use this skill whenever the user shares a prompt and asks for feedback — phrases like "is this prompt good", "audit my prompt", "review this prompt", "will Claude understand this", "improve this prompt", "is this enough context". Also trigger proactively when you notice the user is about to dispatch a vague, under-specified, or over-constrained prompt for non-trivial work. Checks the 6 essential elements (goal, scope, existing patterns, constraints, verification, done definition), flags what's missing, explains why each gap matters, and produces an improved rewrite. Treat this skill as the litmus test for "Be Claude's PM" — if the prompt fails the audit, the work that follows will probably fail too.
---

# prompt-audit

Most AI-coding failures trace back to thin prompts. A prompt that takes 30 seconds to write and 2 minutes for Claude to "execute" produces code that takes 2 hours to fix. This skill catches that before it happens.

## When to use

Use whenever the user is evaluating, drafting, or about to send a prompt for non-trivial coding work. Triggers include:

- "Is this prompt good?"
- "Audit / review / check my prompt"
- "Will Claude understand this?"
- "How do I improve this prompt?"
- The user pastes a prompt and asks anything about it
- You notice the user is about to send a vague prompt for a complex task — proactively offer to audit it

Don't audit:

- Single-line throwaway prompts the user is happy with
- Pure conversation / clarification messages (not actual task prompts)

## The six essential elements

A good coding prompt for non-trivial work has all six. Missing any one drops the success rate noticeably.

| # | Element | What it answers | Why it matters |
|---|---|---|---|
| 1 | **Goal** | What problem are we solving? Who uses the result? | Without a goal, Claude optimizes the wrong thing |
| 2 | **Scope** | Which files / modules can change? Which can't? | Without scope, Claude touches things it shouldn't |
| 3 | **Existing patterns** | What in the codebase should we mimic? | Without patterns, Claude reinvents conventions inconsistently |
| 4 | **Constraints** | Performance, dependencies, compatibility | Without constraints, Claude makes choices the user won't accept |
| 5 | **Verification** | What tests prove this is correct? | Without verification, "done" is undefined |
| 6 | **Done definition** | When can we mark this complete? | Without done, Claude over-builds or under-builds |

## Workflow

### Step 1 — Parse the prompt

Read the prompt the user shared. Identify which of the 6 elements are present, partially present, or missing. Be honest — "we should follow good patterns" is not a real existing-pattern reference; an actual file path is.

### Step 2 — Score each element

For each element, classify as:

- ✅ **Clear** — concrete, actionable, unambiguous
- ⚠️ **Vague** — present but too abstract to be useful
- ❌ **Missing** — not addressed at all

### Step 3 — Diagnose with reasons

For each gap, explain to the user *why* this matters in the specific task at hand — not just generic best-practice scolding. Example:

> "Your scope is missing — and because this prompt mentions `auth/`, Claude will likely modify shared auth middleware that 30+ other endpoints depend on. That's a core-code change that needs explicit human ownership."

### Step 4 — Watch for over-constraint too

The opposite failure mode: a prompt that dictates every variable name, every line of pseudocode, every internal step. This makes the model worse, not better. If you see this, flag it:

> "Your prompt over-constrains the implementation. The model performs best when given goals + constraints + patterns, then trusted to write the code. Treat the prompt like onboarding a junior — explain what matters, not what to type."

### Step 5 — Produce a rewrite

Always produce an improved version, even if the original was decent. Use this structure:

```
[Goal]
<Who uses this, what done means>

[Scope]
- Can modify: <list>
- Must not modify: <list>

[Existing patterns]
- Mirror <specific file or module>
- Convention: <e.g., service.ts + route.ts + *.test.ts>

[Constraints]
- <Performance, dependencies, compat>

[Verification]
- 3 e2e tests: <happy + 2 errors, described at user level>
- Manual: <if applicable>

[Done]
- <Concrete checklist>
```

If the user's task isn't big enough to need all six, drop the unused ones rather than padding with placeholders.

### Step 6 — Show before/after side by side

End the audit with a direct comparison so the user sees the gain. Example:

```
Before (6 words): "Add a user activity report endpoint."
After (~250 words): <full structured prompt>
Why the rewrite is better: scope is now explicit, existing pattern named, verification defined, done measurable.
```

## Red flags worth calling out

When you spot any of these in the original prompt, surface them explicitly:

- **Touches core code without acknowledging it.** "Just add this to the auth middleware..."
- **No verification at all.** "It should work."
- **Vague pronouns.** "Make it better." "Fix this." (Better what? This what?)
- **No file paths anywhere.** Hard to ground without paths.
- **Implies multiple PRs in one prompt.** "Build the auth flow and the user dashboard and the reporting." Suggest splitting.
- **Domain the user clearly doesn't know.** Hard to PM a domain you don't understand. Ask: "How will you tell if this is right?"
- **Asks the AI to write the spec.** "Figure out what we should build." Not Claude's job — that's product work.

## Output format

Use this structure for the audit:

```markdown
## Audit summary
<1-2 sentences: overall verdict>

## Element check
| Element | Status | Notes |
|---|---|---|
| Goal | ✅ / ⚠️ / ❌ | <observation> |
| Scope | ✅ / ⚠️ / ❌ | <observation> |
| Existing patterns | ✅ / ⚠️ / ❌ | <observation> |
| Constraints | ✅ / ⚠️ / ❌ | <observation> |
| Verification | ✅ / ⚠️ / ❌ | <observation> |
| Done | ✅ / ⚠️ / ❌ | <observation> |

## Red flags
<bullet list, or "None">

## Improved version
<full rewrite>

## Why the rewrite is better
<2-3 specific gains>
```

## Stopping condition

End the skill when:

- The user has the rewritten prompt
- Or the user pushes back: "It's fine as is." (Don't keep relitigating.)
