---
name: dev:interrogate
description: Interrogate code changes to surface decisions, alternatives, and confidence levels. Use when user asks to "interrogate", "what decisions", "hardest part", "alternatives", or wants to understand the reasoning behind code changes.
allowed-tools: Bash(git diff:*), Bash(git show:*), Bash(gh pr diff:*)
argument-hint: <unstaged|staged|changes|commit|pr> [--quick|--skeptical]
---

# Interrogate Code Changes

Ask "why" instead of just reading code. Surfaces assumptions, decisions, and confidence levels.

## Workflow

@context/workflows/interrogate.md

## Input: $ARGUMENTS

Parse arguments to determine:
- **Target:** `unstaged` (default), `staged`, `changes` (staged+unstaged), `commit <hash>`, `pr <number>`, or `range <ref1>..<ref2>`
- **Mode:** `--quick` (minimal output) or `--skeptical` (extra validation)

## Gather Context

Based on target, gather the code diff:

### Target: unstaged (default)
```bash
git diff
```

### Target: staged
```bash
git diff --cached
```

### Target: changes
```bash
git diff HEAD
```

### Target: commit <hash>
```bash
git show <hash>
```

### Target: pr <number>
```bash
gh pr diff <number>
```

### Target: range <ref1>..<ref2>
```bash
git diff <ref1>..<ref2>
```

## Execute Interrogation

Apply the three core questions from the workflow to the gathered diff:

1. **What was the hardest decision?**
2. **What alternatives did you reject?**
3. **What are you least confident about?**

## Mode Behavior

- **Default:** Full explanations with confidence levels and structured tables
- **--quick:** Compact table with brief answers only
- **--skeptical:** Full output plus follow-up probes:
  - "Walk me through the logic step by step"
  - "What edge cases could break this?"
  - "If this code has a bug, where is it most likely?"

## Output

Format output per @context/workflows/interrogate.md#Output-Format based on selected mode.
