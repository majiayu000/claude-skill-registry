---
name: parallel-task-execution
description: >
  Patterns for running independent tasks in parallel using multiple tool calls
  and Agent invocations. Use when the user has multiple independent operations,
  asks about fan-out/fan-in, or wants to speed up multi-step workflows.
---

# Parallel Task Execution

Claude Code can execute multiple independent tool calls in a single response. This dramatically reduces wall-clock time for tasks that do not depend on each other.

## When to Use
- Multiple files need to be read, searched, or analyzed independently
- User wants to speed up a multi-step workflow
- Several subagents can investigate different aspects simultaneously
- Independent operations (read + grep + glob) can run concurrently
- User asks about fan-out/fan-in or parallel execution

## Core Patterns

### Identifying Independent Operations

Two operations are independent when neither needs the other's result. Test by asking: "Can I start operation B without knowing the result of operation A?"

```
# INDEPENDENT (run in parallel):
- Read file A and Read file B
- Grep for pattern X and Grep for pattern Y
- Analyze auth module and Analyze database module

# DEPENDENT (run sequentially):
- Find the config file, THEN read it
- Read the test file, THEN modify it based on contents
- Get the function signature, THEN find all call sites
```

### Parallel Tool Calls

Make multiple tool calls in a single response block:

```
# Single response with 3 parallel calls:

Call 1 - Read:
  file_path: "src/auth/middleware.ts"

Call 2 - Read:
  file_path: "src/auth/tokens.ts"

Call 3 - Read:
  file_path: "src/auth/permissions.ts"
```

All three files are read concurrently. Results arrive together for synthesis.

### Fan-Out with Subagents

Launch multiple Agent tool calls for independent investigations:

```
# Fan-out: 3 parallel subagents

Agent 1:
  prompt: "Analyze all React components in src/components/
           for accessibility issues (missing aria labels,
           no keyboard handlers). Report findings as a list."

Agent 2:
  prompt: "Check all API routes in src/api/ for proper
           error handling. Report which routes lack try/catch
           or return generic error messages."

Agent 3:
  prompt: "Review all database queries in src/db/
           for N+1 query problems. Report file paths and
           the specific query patterns."
```

### Fan-In: Synthesizing Results

After parallel calls complete, synthesize in the next response:

```
# Step 1: Parallel fan-out (3 Agent calls)
# Step 2: All results arrive
# Step 3: Synthesize

"Based on the three analyses:
 - Accessibility: 4 components need aria labels (Agent 1)
 - Error handling: 2 routes missing try/catch (Agent 2)
 - Database: 1 N+1 query in user-posts loader (Agent 3)

 Priority order: Database N+1 > Error handling > Accessibility"
```

### Mixed Parallel Operations

Combine different tool types in a single parallel batch:

```
# All independent, all in parallel:

Call 1 - Glob:
  pattern: "src/**/*.test.ts"

Call 2 - Grep:
  pattern: "TODO|FIXME|HACK"
  path: "src/"

Call 3 - Read:
  file_path: "package.json"

Call 4 - Bash:
  command: "git log --oneline -10"
```

### Sequential Dependencies with Parallel Branches

When some steps depend on others but have parallel sub-branches:

```
# Step 1 (sequential): Read the config to understand the project
Read: "tsconfig.json"

# Step 2 (parallel, depends on Step 1):
# After reading tsconfig, these are independent:
Grep: pattern "import.*from" in src/    # Find all imports
Glob: "src/**/*.d.ts"                   # Find type declarations
Bash: "npx tsc --noEmit 2>&1 | wc -l"  # Count type errors
```

### Background Execution for Long Tasks

Use `run_in_background` for commands that take a while:

```
Bash:
  command: "npm run test:coverage"
  run_in_background: true

# Continue working on other things while tests run.
# You will be notified when the background task completes.
```

### Parallel File Creation

When creating multiple independent files:

```
# All independent, all in parallel:

Write: "src/utils/format.ts"
  content: "..."

Write: "src/utils/validate.ts"
  content: "..."

Write: "src/utils/transform.ts"
  content: "..."
```

## Anti-Patterns

- **Parallelizing dependent operations**: Reading a file and then editing it based on contents must be sequential. Making these parallel causes the edit to use stale or missing data.
- **Too many parallel calls**: Launching 20 subagents simultaneously can overwhelm the system. Keep parallel batches to 3-5 concurrent operations for stability.
- **Ignoring partial failures**: When one of several parallel operations fails, do not ignore it. Address the failure before proceeding with synthesis.
- **Serializing independent work**: Running 5 independent file reads one after another wastes time. If they do not depend on each other, run them in parallel.
- **Using parallel agents for tiny tasks**: Do not launch a subagent to read a single file. Use the Read tool directly. Subagents have overhead and are only worth it for multi-step investigations.

## Quick Reference

| Pattern | When | How |
|---------|------|-----|
| Parallel reads | Multiple files to inspect | Multiple Read calls in one response |
| Parallel searches | Multiple patterns or directories | Multiple Grep/Glob calls in one response |
| Fan-out agents | Independent investigations | Multiple Agent calls in one response |
| Fan-in synthesis | After parallel results arrive | Single response analyzing all results |
| Background tasks | Long-running commands | `run_in_background: true` on Bash |
| Mixed parallel | Different tool types, independent | Mix Read + Grep + Glob + Bash in one response |

**Independence test**: "Can B start without A's result?" If yes, parallelize.
**Batch size**: 3-5 concurrent operations is the sweet spot.
**Synthesis**: Always dedicate a response to combining parallel results.
