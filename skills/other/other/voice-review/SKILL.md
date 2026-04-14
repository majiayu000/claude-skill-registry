---
name: voice-review
description: Dispatch parallel prose and craft review agents on generated
  text. Merges results into unified advisory tables. Auto-fixes hard
  failures and presents soft findings for user decision. Use after
  voice-generate or on any text that should match a voice profile.
version: 1.8.4
globs: "**/*.{md,txt}"
alwaysApply: false
category: writing-quality
tags:
- voice
- review
- prose
- craft
- quality
tools:
- Read
- Write
- Agent
- TodoWrite
complexity: medium
model_hint: standard
estimated_tokens: 1600
progressive_loading: false
dependencies:
- scribe:voice-extract
- scribe:voice-generate
- scribe:slop-detector
---

# Voice Review Skill

Dispatch dual review agents and present unified findings.

## Method: Parallel Dual-Gate Review

Two agents run in parallel on the generated text:
1. **Prose reviewer**: AI patterns, banned phrases, voice drift
2. **Craft reviewer**: Naming, destinations, dwelling, devices, anchoring

Hard failures (banned phrases, em dashes) are auto-fixed.
Everything else returns as advisory tables for user decision.

## Required TodoWrite Items

1. `voice-review:text-loaded` - Generated text read
2. `voice-review:register-loaded` - Voice register loaded
3. `voice-review:agents-dispatched` - Both reviewers launched
4. `voice-review:hard-fails-fixed` - Auto-corrections applied
5. `voice-review:advisories-presented` - Tables shown to user

## Step 1: Load Context

Read:
- The generated text (from file or clipboard)
- The active voice register
- The banned phrases list

## Step 2: Dispatch Review Agents

Launch both agents in parallel:

```
Agent(prose-reviewer):
  - text: {generated_text}
  - register: {register_content}
  - banned_phrases: {banned_list}

Agent(craft-reviewer):
  - text: {generated_text}
  - register: {register_content}
```

## Step 3: Process Results

### Hard Failures

Apply all auto-fixes from prose reviewer silently:
- Remove/replace banned phrases
- Replace em dashes with appropriate punctuation
- Rewrite negation-correction patterns

Report: "Fixed N hard failures (X banned phrases, Y em dashes, Z patterns)"

### Advisory Tables

Present both tables to the user:

**Prose Review Advisories:**

| # | Line | Pattern | Current | Proposed fix |
|---|------|---------|---------|--------------|

**Craft Review:**

| Dimension | Rating | Notes | Proposed improvement |
|-----------|--------|-------|---------------------|

## Step 4: User Decision

For each advisory row, user can:
- **Accept** (a): Apply the proposed fix
- **Reject** (r): Keep the current text
- **Rewrite** (w): Apply a custom fix

Present as:
```
[1] Prose: Frictionless transition at "Furthermore, the..."
    Proposed: Cut transition, start mid-thought
    [a]ccept / [r]eject / re[w]rite?
```

## Step 5: Apply Decisions

- Apply accepted fixes to the text
- Skip rejected items
- For rewrites, incorporate user's version
- Save final text

## Step 6: Snapshot (if learning active)

If the user has learning mode enabled:
- Save "post-review" snapshot (text after hard-fail fixes,
  before user decisions on advisories)
- Save "post-fixes" snapshot (text after user decisions)
- Both go to `~/.claude/voice-profiles/{name}/learning/snapshots/`

## Integration with voice-generate

When dispatched from voice-generate, the flow is:
1. voice-generate produces text
2. voice-generate calls voice-review
3. voice-review dispatches agents, processes results
4. User makes decisions on advisories
5. If learning mode: snapshots saved for later comparison

## Standalone Usage

Can also be run on any existing text:
```
/voice-review path/to/file.md --profile myvoice --register casual
```

## Exit Criteria

- Both review agents returned results
- Hard failures auto-fixed
- Advisory tables presented to user
- User decisions applied
- Final text saved
- Snapshots saved (if learning mode)
