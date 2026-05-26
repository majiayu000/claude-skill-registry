---
name: AOC Orchestrator
description: Main coordinator for the automated Advent of Code workflow. Orchestrates puzzle fetching, TDD solving, and submission for daily AoC challenges. Use when running the full automated solving pipeline or when user requests to solve an AoC day.
---

# AOC Orchestrator

## Purpose

This skill is the main coordinator for the automated Advent of Code workflow. It orchestrates the entire process from puzzle fetching to submission, managing the execution of other specialized skills and handling the overall workflow state.

## When to Use This Skill

- Automatically triggered by cron/launchd on puzzle unlock days (December 1-12, 2025)
- Can be manually invoked for testing or re-running specific days
- Used when the user wants to execute the full end-to-end workflow

## Workflow Steps

### 0. Pre-flight Check: Is This Day Already Solved?

**CRITICAL**: This MUST be the first step. Do not proceed if the puzzle is already complete.

1. Run `aoc calendar --year 2025` to see progress (completed days show decorations/artwork)
2. Check if report exists: `puzzles/day<DD>/report.md` - if it shows both parts completed, EXIT
3. Check state file if it exists: `state/day<DD>.json`

**If both parts are already solved**: DO NOT proceed. Report "Day X is already complete! Nothing to do." and EXIT.

### 1. Initialization (only if not already complete)
```bash
# Check current date and determine which day to solve
# Verify session cookie is configured
```

### 2. Invoke Puzzle Fetcher Skill
- Download puzzle description and input
- Parse examples and expected outputs
- Extract part 1 and part 2 requirements

### 3. Invoke TDD Solver Skill - Part 1
- Generate test cases from examples
- Implement solution using TDD
- Verify all tests pass
- Generate answer from real input

### 4. Invoke Submission Handler Skill - Part 1
- Submit part 1 answer
- Parse response
- Handle success/failure

### 5. If Part 1 Succeeds, Invoke TDD Solver Skill - Part 2
- Parse part 2 requirements
- Generate new test cases
- Extend or rewrite solution for part 2
- Verify all tests pass

### 6. Invoke Submission Handler Skill - Part 2
- Submit part 2 answer
- Handle final results

## Error Handling

### Puzzle Not Yet Available
```
If puzzle unlock time not reached:
  - Log: "Puzzle for day X not yet available"
  - Exit gracefully
  - Next cron execution will retry
```

### Already Solved
```
If day already has both stars:
  - Log: "Day X already completed"
  - Exit gracefully
  - No further action needed
```

### Network Errors
```
If network request fails:
  - Log error details
  - Retry up to 3 times with exponential backoff
  - If still failing, exit and alert
```

### Compilation Errors
```
If Rust code fails to compile:
  - Log compiler errors
  - Attempt to fix based on error messages
  - Retry compilation
  - Max 5 fix attempts per part
```

## State Management

Track workflow state in `state/day{day}.json`:

```json
{
  "day": 1,
  "year": 2025,
  "status": "in_progress",
  "part1": {
    "status": "completed",
    "answer": 24000,
    "submitted_at": "2025-12-01T05:01:23Z",
    "attempts": 1
  },
  "part2": {
    "status": "in_progress",
    "answer": null,
    "submitted_at": null,
    "attempts": 0
  },
  "started_at": "2025-12-01T05:00:15Z",
  "completed_at": null
}
```

## Success Criteria

- ✅ Both part 1 and part 2 answers accepted
- ✅ All tests passing
- ✅ Code compiles without warnings
- ✅ Solution completes in < 15 seconds
- ✅ State file updated correctly

## Logging

Log all actions to `logs/day{day}.log`:

```
[2025-12-01 05:00:15] INFO: Starting orchestration for Day 1
[2025-12-01 05:00:16] INFO: Invoking puzzle-fetcher skill
[2025-12-01 05:00:18] INFO: Puzzle downloaded successfully
[2025-12-01 05:00:18] INFO: Invoking tdd-solver skill for Part 1
[2025-12-01 05:02:45] INFO: Part 1 solution implemented, all tests pass
[2025-12-01 05:02:46] INFO: Invoking submission-handler for Part 1
[2025-12-01 05:02:47] SUCCESS: Part 1 answer accepted!
[2025-12-01 05:02:48] INFO: Invoking tdd-solver skill for Part 2
...
```

## Command Interface

When invoked manually:

```bash
# Run for today's puzzle
cargo run --bin aoc-orchestrator

# Run for specific day
cargo run --bin aoc-orchestrator -- --day 5

# Dry run (no submission)
cargo run --bin aoc-orchestrator -- --day 1 --dry-run

# Force re-run even if already solved
cargo run --bin aoc-orchestrator -- --day 1 --force

# Verbose debugging
cargo run --bin aoc-orchestrator -- --day 1 --debug
```

## Integration with Other Skills

### Calling Puzzle Fetcher
```rust
// Pseudo-code showing skill invocation
let puzzle_data = invoke_skill("puzzle-fetcher", {
    "day": day_number,
    "year": 2025
})?;
```

### Calling TDD Solver
```rust
let solution = invoke_skill("tdd-solver", {
    "day": day_number,
    "part": 1,
    "examples": puzzle_data.examples,
    "input": puzzle_data.input
})?;
```

### Calling Submission Handler
```rust
let result = invoke_skill("submission-handler", {
    "day": day_number,
    "part": 1,
    "answer": solution.answer
})?;
```

## Performance Metrics

Track and report:
- Total time from start to completion
- Time per phase (fetch, solve part1, submit part1, solve part2, submit part2)
- Number of test iterations required
- Number of submission attempts
- Compilation time

## Post-Completion Actions

After both parts completed successfully:
- Generate solution summary
- Run `cargo fmt` to format code
- Run `cargo clippy` to check for issues
- Optionally commit to git with message: `"Solve Day {day} - {puzzle_title}"`
- Update calendar status file

## Failure Recovery

If workflow fails mid-execution:
- Save current state to state file
- Next invocation should resume from last successful step
- Don't re-fetch puzzle if already downloaded
- Don't re-solve part 1 if already accepted
