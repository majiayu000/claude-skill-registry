---
name: Submission Handler
description: Handle Advent of Code answer submissions with intelligent retry logic. Submits answers via aoc-cli, parses responses, handles failures, analyzes edge cases when tests pass but submission fails, and manages exponential backoff. Use when submitting AoC answers, handling submission failures, or implementing retry logic.
---

# Submission Handler

## Purpose

This skill manages the submission of Advent of Code answers using `aoc-cli`, parsing submission responses, and implementing intelligent retry logic when submissions fail despite all tests passing.

## Primary Responsibilities

1. Submit answers using aoc-cli
2. Parse and interpret submission responses
3. Handle success/failure scenarios
4. Analyze failures when tests pass but submission fails
5. Implement exponential backoff and retry logic
6. Respect AoC rate limiting

## Using aoc-cli for Submission

### Basic Submission

```bash
# Submit answer for part 1
aoc submit 1 <ANSWER> --day <DAY> --year 2025

# Submit answer for part 2
aoc submit 2 <ANSWER> --day <DAY> --year 2025

# Example for Day 1, Part 1
aoc submit 1 24000 --day 1 --year 2025
```

### Submission Responses

AoC provides different response types:

#### Success Response
```
That's the right answer! You are one gold star closer to saving your vacation. [[Continue to Part Two]]
```

#### Incorrect Answer
```
That's not the right answer. If you're stuck, make sure you're using the full input data.
```

#### Too Fast (Rate Limiting)
```
You gave an answer too recently; you have to wait after submitting an answer before trying again. You have 5m 23s left to wait.
```

#### Already Completed
```
You don't seem to be solving the right level. Did you already complete it?
```

## Response Parsing

### Extract Response Type

```rust
enum SubmissionResult {
    Correct,
    Incorrect,
    TooFast { wait_seconds: u32 },
    AlreadyCompleted,
    NetworkError,
}

fn parse_submission_response(output: &str) -> SubmissionResult {
    if output.contains("That's the right answer") {
        SubmissionResult::Correct
    } else if output.contains("not the right answer") {
        SubmissionResult::Incorrect
    } else if output.contains("wait after submitting") {
        let wait_time = extract_wait_time(output);
        SubmissionResult::TooFast { wait_seconds: wait_time }
    } else if output.contains("already complete") {
        SubmissionResult::AlreadyCompleted
    } else {
        SubmissionResult::NetworkError
    }
}
```

### Extract Wait Time

Parse wait time from rate limit messages:

```rust
fn extract_wait_time(message: &str) -> u32 {
    // Parse formats like "5m 23s" or "45s" or "2m"
    // Return total seconds to wait
}
```

## Retry Logic

### Scenario 1: Rate Limited (Too Fast)

```
Action:
1. Parse wait time from response
2. Log: "Rate limited. Waiting X seconds..."
3. Sleep for specified duration
4. Retry submission
```

### Scenario 2: Incorrect Answer - Tests Passed

This is the critical scenario requiring intelligent analysis.

```
Situation:
- All example tests pass
- Answer submission returns "incorrect"

Root Causes:
1. Edge cases not covered by examples
2. Input parsing issues
3. Integer overflow
4. Off-by-one errors
5. Incorrect assumptions about problem constraints
```

#### Analysis Strategy

```markdown
Step 1: Compare Example vs Real Input

- Are there patterns in real input not in examples?
- Are numbers much larger?
- Are there edge cases (empty groups, single items, etc.)?

Step 2: Review Common Edge Cases

- Empty input
- Single element
- All same values
- Very large numbers (>2^31)
- Negative numbers (if applicable)
- Boundary conditions

Step 3: Add New Test Cases

Generate tests for suspected issues:

```rust
#[test]
fn test_real_input_edge_case() {
    // Based on analysis of real input
}
```

Step 4: Re-implement with Fixes

Make changes, ensure all tests (including new ones) pass.

Step 5: Re-submit

Try again with backoff if still failing.
```

#### Backoff Strategy

```
Attempt 1: Submit immediately after fix
Attempt 2: Wait 1 minute
Attempt 3: Wait 5 minutes
Attempt 4: Wait 15 minutes
Attempt 5: Wait 1 hour
After 5 attempts: Flag for manual review
```

## Workflow Integration

### Called By
- aoc-orchestrator skill (after TDD solver completes)

### State Tracking

Track submission attempts in state file:

```json
{
  "day": 1,
  "part": 1,
  "attempts": [
    {
      "attempt_number": 1,
      "answer": 24000,
      "submitted_at": "2025-12-01T05:03:00Z",
      "result": "incorrect",
      "analysis": "Suspected edge case: empty groups not handled"
    },
    {
      "attempt_number": 2,
      "answer": 24500,
      "submitted_at": "2025-12-01T05:08:00Z",
      "result": "correct",
      "analysis": null
    }
  ]
}
```

## Common Failure Patterns

### Pattern 1: Integer Overflow

```rust
// Problem: Using i32 when values exceed 2^31
// Solution: Use i64

// Before:
pub fn part1(input: &str) -> i32 { ... }

// After:
pub fn part1(input: &str) -> i64 { ... }
```

### Pattern 2: Off-By-One

```rust
// Problem: Counting vs indexing confusion
// Solution: Carefully review loop bounds

// Check:
for i in 0..n {      // 0 to n-1
for i in 0..=n {     // 0 to n (inclusive)
```

### Pattern 3: Parsing Issues

```rust
// Problem: Trailing whitespace or newlines
// Solution: Trim input

let clean = input.trim();
```

### Pattern 4: Wrong Accumulator

```rust
// Problem: Summing when should find max
// Solution: Verify the problem asks for

// Sum example:
total += value;

// Max example:
max = max.max(value);

// Count example:
count += 1;
```

## Error Handling

### Network Failures

```bash
# If aoc-cli returns network error
Error: Failed to connect to adventofcode.com

Action:
1. Retry up to 3 times with exponential backoff
2. If still failing, log error and exit
3. Next orchestrator run will retry
```

### Session Cookie Issues

```bash
# If session cookie invalid/expired
Error: Please provide a valid session cookie

Action:
1. Log: "Session cookie invalid"
2. Alert user to update ~/.adventofcode.session
3. Exit gracefully
```

## Safety Guardrails

### Rate Limiting Respect

- Never submit more than once per minute
- Always respect wait times from AoC
- Maximum 5 attempts per part per day
- Log all submission attempts

### Validation Before Submission

```bash
# Validate answer format
- Must be a number or simple string
- No special characters
- Reasonable length (< 100 chars)
- Not obviously wrong (e.g., negative when asking for count)
```

## Logging

Log all submission attempts:

```
[2025-12-01 05:03:00] SUBMIT: Day 1, Part 1, Answer: 24000
[2025-12-01 05:03:01] RESULT: Incorrect - "not the right answer"
[2025-12-01 05:03:01] ANALYSIS: Comparing example vs real input...
[2025-12-01 05:05:30] ANALYSIS: Added test for empty group edge case
[2025-12-01 05:06:45] SUBMIT: Day 1, Part 1, Answer: 24500 (Attempt 2)
[2025-12-01 05:06:46] RESULT: Correct - "That's the right answer!"
```

## Command Interface

When invoked directly:

```bash
# Submit answer for specific day/part
./scripts/submit-answer.sh 1 1 24000

# Dry run (validate without submitting)
./scripts/submit-answer.sh 1 1 24000 --dry-run

# Force submission (skip validations)
./scripts/submit-answer.sh 1 1 24000 --force
```

## Success Metrics

Track for analysis:
- First attempt success rate
- Average attempts per part
- Most common failure patterns
- Time to correct answer after first failure

## Integration Example

```rust
// Pseudo-code showing full integration

// TDD solver produces answer
let answer = solve_part1(&input);

// Validation
assert!(all_tests_pass());

// Submit
let result = submit_answer(day, part, answer)?;

match result {
    SubmissionResult::Correct => {
        log_success();
        move_to_part2();
    },
    SubmissionResult::Incorrect => {
        analyze_failure();
        generate_new_tests();
        re_implement_fix();
        schedule_retry();
    },
    SubmissionResult::TooFast { wait_seconds } => {
        log_wait_time();
        sleep(wait_seconds);
        retry_submission();
    },
    // ... handle other cases
}
```

## Output Format

Return structured result to orchestrator:

```json
{
  "success": true,
  "day": 1,
  "part": 1,
  "answer": 24000,
  "attempts": 2,
  "total_time_seconds": 243,
  "first_attempt_correct": false
}
```
