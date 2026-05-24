---
name: explain-this
description: "Explain whatever the user is pointing at right now in plain language: a pending question, a piece of code, an error, a command output, or an artifact like a plan or findings report. Use when the user asks to \"explain this\", \"what am I being asked\", \"what's happening right now\", \"help me understand this\", \"what does this mean\", \"what does this error mean\", \"what is this code doing\", or \"what do these options mean\"."
---

# Explain This

Take whatever the user is pointing at and translate it into plain language. "This" is usually the most recent assistant output or something pasted as an argument: a multi-option prompt, a free-form question, a code block, an error, a command output, or an artifact like a plan, findings report, or diff.

## Step 1: Identify the Subject

Pick the subject in priority order:

1. Text passed as an argument — use that
2. A quoted or selected region from the user's most recent message — use that
3. The most recent non-trivial assistant output — use that
4. If the guess is not obvious, lead the explanation by naming what was picked so the user can redirect

## Step 2: Ground in State

Read whatever makes the explanation concrete, no more:

- Files the subject references
- The active skill's `SKILL.md` when a skill-specific question is being asked
- `git status` and `git diff --stat` when the subject involves staged or unstaged changes
- Any artifact cited (plan, spec, findings, test plan, audit, PR, commit)

## Step 3: Produce the Explanation

The reader is an experienced developer who may not be fluent in every tech stack or acronym but doesn't need concepts from first principles. Skip ELI5. Use plain language; strip skill-internal jargon, or define it inline when the jargon is what the user needs explained (for example, "P1 peer" becomes "priority 1 finding from the peer reviewer").

Go beyond "what this does" and surface the trade-offs: pros and cons per choice, benefits and costs, whether the thing reads as clean and elegant or redundant and overcomplicated. Be honest about red flags; be honest about solid work.

Shape the output to match the subject. Use the branch that applies; drop the rest.

**Question with discrete options** — restate the question plainly, then enumerate options using this template:

```
**What you're being asked:** <plain-language restatement>

### Your Options
**1. <label as shown>** — <concrete effect: files changed, next step, what is lost>
  - **Pros:** <what you gain>
  - **Cons:** <what it costs>
**2. <label>** — <concrete effect>
  - **Pros:** <...>
  - **Cons:** <...>

### When Each Fits
- Pick **<option>** if your goal is <goal>.
- Pick **<option>** if your goal is <other goal>.
```

Apply these option-specific rules:

- Describe each option's real-world effect. Example:
  - Concrete: "Renames the module to `auth-v2` and updates the 3 import sites in `src/`."
  - Too abstract: "Cleans up the auth code."
- If an option was labelled "(Recommended)" in the original, repeat that label verbatim. Do not add a fresh recommendation.
- If an option would skip a safety step (tests, review, a gate), call that out.
- If the pending question was posed via `AskUserQuestion`, re-invoke `AskUserQuestion` after the explanation with the same question, header, and options so the user can answer inline without losing the dialog. Preserve any "(Recommended)" label verbatim. Otherwise (plain-text prompt from the assistant), end by noting the question is still pending and the user should reply to the original prompt directly.

**Free-form question** — restate the question plainly, say what the answer will be used for (which file gets written, which step consumes it), and call out what makes a good answer versus a problematic one. End by noting the question is still pending.

**Code, error, or command output** — say what it does or means, likely cause or purpose, and what action is typically expected. Judge the design: is it clean and idiomatic, or are there smells like redundant guards, tangled control flow, or unnecessary abstraction?

**Artifact (plan, findings, diff, PR)** — summarize its contents, the decisions it represents, and what step comes next. Flag strengths and weaknesses: over-engineering, missing cases, clear wins.

## Rules

- Read-only. Do not modify files, stage changes, or answer a pending question on the user's behalf.
- If an active skill's SKILL.md contradicts what the conversation shows, trust the conversation and note the discrepancy briefly.
- If the subject cannot be identified at all, say so and stop.
