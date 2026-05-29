---
name: ralph-loop-helper
description: Guide for using /ralph-loop command for long-running autonomous tasks. Use when starting iterative development loops, implementing Bedrock plugins, or running test-fix cycles. (project)
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: mineflayer-bedrock
  version: "1.0"
---

# Ralph Loop Helper

Guide users on effectively using `/ralph-loop` for long-running autonomous tasks in the mineflayer-bedrock project.

## Overview

The Ralph Wiggum plugin implements an iterative AI development loop. It uses a Stop hook that intercepts Claude's exit attempts, feeding the same prompt back to continue working until completion criteria are met.

**Core mechanism**: You run `/ralph-loop "task"` once. Claude works, tries to exit, the hook blocks it, re-feeds the prompt, and repeats until done.

## When to Use

- Implementing a new Bedrock plugin that needs to match Java API
- Running test suites and fixing all failures iteratively
- Large refactoring tasks with clear completion criteria
- Tasks with automatic verification (tests, linters, type checks)
- Greenfield implementations with well-defined requirements

## When NOT to Use

- Tasks requiring human judgment or design decisions
- One-shot operations (single file edits, quick fixes)
- Exploratory work with unclear success criteria
- Production debugging requiring careful analysis
- Tasks where you need to review intermediate results

## Known Limitations

### Multiline Prompts NOT Supported

CLI arguments cannot contain newlines due to Bash security restrictions. These GitHub issues track this:
- Issue #15640: Bash security blocks newlines
- Issue #15712: Command contains newlines error
- Issue #15824: Feature request for file-based prompts

**Workaround**: Keep prompts single-line or use phased execution (see below).

### Exact String Matching Only

`--completion-promise` uses exact string matching. You cannot use regex or multiple conditions like "SUCCESS OR BLOCKED". Use the `<promise>TAG</promise>` pattern for clarity.

### Token Consumption

Each iteration consumes full context window tokens. A 50-iteration loop on a large codebase can cost $50-100+ in API credits.

## Recommended Patterns

### 1. Always Use --max-iterations

This is your primary safety mechanism. Never rely solely on completion promises.

```bash
/ralph-loop "Your task..." --max-iterations 30
```

### 2. Use Promise Tags

Wrap completion signals in tags for clear detection:

```bash
/ralph-loop "Build feature X. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 25
```

### 3. Include Stuck Handling

Add escape instructions for when Claude gets stuck:

```bash
/ralph-loop "Implement feature. After 10 iterations without progress: document blockers, list attempts, suggest alternatives. Output <promise>BLOCKED</promise> if truly stuck, <promise>DONE</promise> if complete." --max-iterations 20
```

### 4. Phased Execution for Complex Tasks

Break large tasks into phases instead of one massive prompt:

```bash
# Phase 1
/ralph-loop "Phase 1: Create data models. Output <promise>P1_DONE</promise>" --max-iterations 15

# Phase 2
/ralph-loop "Phase 2: Implement API endpoints. Output <promise>P2_DONE</promise>" --max-iterations 20

# Phase 3
/ralph-loop "Phase 3: Add tests, ensure all pass. Output <promise>P3_DONE</promise>" --max-iterations 25
```

## Project-Specific Examples

### Implement a Bedrock Plugin

```bash
/ralph-loop "Implement inventory.mts Bedrock plugin in lib/bedrockPlugins/ matching the Java API in lib/plugins/inventory.js. Map Bedrock packets to same bot behavior. Run 'npm run mocha_test' after changes. Output <promise>PLUGIN_COMPLETE</promise> when tests pass." --max-iterations 30
```

### Fix Test Failures

```bash
/ralph-loop "Run 'npm run test:bedrock'. Fix any failing tests. Do not skip tests. Output <promise>TESTS_PASS</promise> when all tests green." --max-iterations 20
```

### API Compatibility Check

```bash
/ralph-loop "Compare lib/bedrockPlugins/health.mts with lib/plugins/health.js. Ensure Bedrock version exposes same API (functions, events, properties). Fix discrepancies. Run tests. Output <promise>API_MATCH</promise> when compatible." --max-iterations 15
```

### Type Error Resolution

```bash
/ralph-loop "Run 'npx tsc --noEmit'. Fix all TypeScript errors. Do not use 'any' type. Output <promise>TYPES_CLEAN</promise> when no errors." --max-iterations 25
```

## Cost Awareness

| Iterations | Estimated Cost |
|------------|----------------|
| 10-20      | $10-25         |
| 30-50      | $30-75         |
| 50+        | $50-150+       |

**Tips to reduce costs**:
- Start with lower `--max-iterations` and increase if needed
- Use phased execution to checkpoint progress
- Include clear completion criteria to exit early
- Monitor iteration count in output

## Commands Reference

### /ralph-loop

Start an iterative development loop.

```bash
/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"
```

**Options**:
- `--max-iterations <n>`: Stop after N iterations (required for safety)
- `--completion-promise <text>`: Exact string that signals completion

### /cancel-ralph

Cancel an active Ralph loop immediately.

```bash
/cancel-ralph
```

## Common Mistakes

| Mistake | Prevention |
|---------|------------|
| No iteration limit | Always use `--max-iterations` |
| Vague completion criteria | Use specific, testable conditions |
| Multiline prompts | Keep single-line or use phases |
| Relying only on promise | Set iteration limit as backup |
| Too many iterations at once | Start small, increase if needed |

## Related Skills

- `skill-builder`: For creating new Claude Code skills
- `create-analyzer`: For packet analysis tasks
