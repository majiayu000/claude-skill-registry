---
name: Daily Reporter
description: Generate comprehensive daily status reports after solving AoC puzzles. Documents success/failure, challenges faced, retry attempts, execution time, and insights for workflow tuning. Use after completing each day's puzzle to provide developer feedback on automation effectiveness.
---

# Daily Reporter

## Purpose

This skill generates comprehensive, neutral status reports after each day's puzzle completion. The reports help the developer understand:

- Whether the automated workflow is functioning correctly
- What challenges were encountered
- If any workflow tuning is needed for subsequent days
- Overall automation effectiveness and patterns

## When to Use This Skill

- **Automatically**: After successfully completing both parts of a day
- **On failure**: After exhausting all retry attempts
- **On partial completion**: After completing only part 1

## Report Structure

Each daily report follows a consistent format for easy parsing and analysis.

### File Location

Reports are saved to: `puzzles/day{day:02}/report.md`

Example: `puzzles/day01/report.md`, `puzzles/day12/report.md`

### Report Template

```markdown
# Day {N} - {Puzzle Title} - Status Report

**Date**: {YYYY-MM-DD HH:MM:SS EST}
**Overall Status**: ✅ Success | ⚠️ Partial | ❌ Failed
**Total Execution Time**: {MM}m {SS}s

---

## Summary

{Brief 1-2 sentence summary of the day}

## Part 1

**Status**: ✅ Correct | ❌ Failed
**Submission Attempts**: {N}
**Time to First Submission**: {MM}m {SS}s
**Time to Correct Answer**: {MM}m {SS}s

### Test Results
- Total Tests Written: {N}
- Tests Passing: {N}
- Test Iterations: {N}

### Implementation Approach
{Brief description of the algorithm/approach used}

### Challenges Encountered
{List any challenges, or "None - straightforward implementation"}

- Challenge 1: Description
- Challenge 2: Description

### Retry Analysis (if applicable)
{If first submission failed}

**First Attempt**: Answer {X} - Response: "{error message}"
**Root Cause**: {What was wrong}
**Fix Applied**: {How it was resolved}
**Second Attempt**: Answer {Y} - Response: "Correct"

## Part 2

**Status**: ✅ Correct | ❌ Failed | ⏸️ Not Started
**Submission Attempts**: {N}
**Time to First Submission**: {MM}m {SS}s
**Time to Correct Answer**: {MM}m {SS}s

### Test Results
- Total Tests Written: {N}
- Tests Passing: {N}
- Test Iterations: {N}

### Implementation Approach
{Brief description - was Part 1 reused or rewritten?}

### Challenges Encountered
{List any challenges}

### Retry Analysis (if applicable)
{Same format as Part 1}

## Metrics

| Metric | Value |
|--------|-------|
| Total Submission Attempts | {N} |
| Total Test Iterations | {N} |
| Total Tests Written | {N} |
| First Attempt Success Rate | {N}/2 parts |
| Code Compilation Time | {N}s |
| Average Test Execution Time | {N}ms |

## Code Quality

**Lines of Code**: {N}
**Functions Created**: {N}
**Clippy Warnings**: {N}
**Formatting Issues**: {N}

## Insights & Patterns

### What Worked Well
- {Observation 1}
- {Observation 2}

### What Could Be Improved
- {Suggestion 1}
- {Suggestion 2}

### Edge Cases Discovered
- {Edge case 1}
- {Edge case 2}

## Workflow Performance

**Fetch Phase**: {N}s - ✅ Success | ❌ Failed
**Parse Phase**: {N}s - ✅ Success | ❌ Failed
**TDD Phase Part 1**: {N}s - ✅ Success | ❌ Failed
**TDD Phase Part 2**: {N}s - ✅ Success | ❌ Failed
**Submission Phase**: {N}s - ✅ Success | ❌ Failed

## Recommendations for Developer

{Neutral assessment of whether workflow tuning is needed}

Example responses:
- "Workflow performed optimally. No tuning required."
- "Consider increasing test iteration limit (currently hit max on Part 2)."
- "Puzzle fetcher may need better parsing for multi-example formats."
- "Retry logic worked well - correctly identified integer overflow issue."

## Detailed Logs

Full execution logs available at:
- `logs/solver_{timestamp}.log`
- `logs/day{day}_detailed.log`

## State File

Final state saved to: `state/day{day}.json`

---

## Slack Message (Norwegian)

**Ready to share with your team:**

```
🎄 AoC 2025 - Dag {N}: {Puzzle Title}

Status: {✅ Begge deler løst | ⚠️ Delvis | ❌ Feilet}
Tid: {M}m {S}s
Forsøk: {N} submission(s)

{Part 1 emoji} Del 1: {Første forsøk ✓ | {N} forsøk}
{Part 2 emoji} Del 2: {Første forsøk ✓ | {N} forsøk}

{One-liner about challenges or success}

{Optional: Link to report or interesting insight}
```

### Slack Message Examples

**Perfect Day:**
```
🎄 AoC 2025 - Dag 1: Calorie Counting

Status: ✅ Begge deler løst
Tid: 6m 23s
Forsøk: 2 submissions

✅ Del 1: Første forsøk ✓
✅ Del 2: Første forsøk ✓

Helt grei oppgave - parsing og summering. Ingen utfordringer! 🚀
```

**With Retries:**
```
🎄 AoC 2025 - Dag 5: Supply Stacks

Status: ✅ Begge deler løst
Tid: 10m 45s
Forsøk: 4 submissions

⚠️ Del 1: 3 forsøk (stack order + off-by-one)
✅ Del 2: Første forsøk ✓

Interessant: Trengte å reversere stack parsing-logikken. Retry-logikken fungerte perfekt! 💪
```

**Partial Completion:**
```
🎄 AoC 2025 - Dag 8: Treetop Tree House

Status: ⚠️ Del 1 løst
Tid: 15m 30s (fortsatt pågår)
Forsøk: 1 submission

✅ Del 1: Første forsøk ✓
⏸️ Del 2: Jobber med det...

Del 2 krever optimalisering - brute force er for treg. Tester binary search approach nå.
```

**Challenging Day:**
```
🎄 AoC 2025 - Dag 11: Monkey in the Middle

Status: ✅ Begge deler løst
Tid: 25m 15s
Forsøk: 6 submissions

⚠️ Del 1: 2 forsøk (integer overflow)
⚠️ Del 2: 4 forsøk (modulo arithmetic)

Krevende! Måtte bytte fra i32 til i64, deretter implementere Chinese Remainder Theorem for Del 2. Lærerikt! 🧠
```

**Failed Day:**
```
🎄 AoC 2025 - Dag 12: Hill Climbing

Status: ❌ Max forsøk nådd
Tid: 45m (timeout)
Forsøk: 5 submissions (alle feil)

❌ Del 1: 5 forsøk - fortsatt feil
❌ Del 2: Ikke startet

Problem: Pathfinding-algoritmen finner ikke korteste vei. Må debugge BFS-logikken. Trenger manuell gjennomgang. 🔍
```

---

**Report Generated**: {YYYY-MM-DD HH:MM:SS EST}
**Automation Version**: 1.0.0
```

## Data Collection Requirements

To generate accurate reports, collect data throughout the workflow:

### During Execution

Track in state file (`state/dayXX.json`):

```json
{
  "day": 1,
  "year": 2025,
  "title": "Calorie Counting",
  "started_at": "2025-12-01T05:02:00Z",
  "completed_at": "2025-12-01T05:08:23Z",
  "overall_status": "completed",

  "part1": {
    "status": "correct",
    "attempts": [
      {
        "number": 1,
        "answer": 24000,
        "submitted_at": "2025-12-01T05:05:00Z",
        "response": "correct",
        "time_to_submit": 180
      }
    ],
    "tests": {
      "total": 8,
      "passing": 8,
      "iterations": 5
    },
    "implementation": {
      "approach": "Parse into groups, sum each, find maximum",
      "lines_of_code": 45,
      "functions": 3
    },
    "challenges": [],
    "time_breakdown": {
      "parsing": 2.5,
      "implementation": 120.0,
      "testing": 45.0,
      "submission": 2.0
    }
  },

  "part2": {
    "status": "correct",
    "attempts": [
      {
        "number": 1,
        "answer": 45000,
        "submitted_at": "2025-12-01T05:08:15Z",
        "response": "correct",
        "time_to_submit": 195
      }
    ],
    "tests": {
      "total": 12,
      "passing": 12,
      "iterations": 3
    },
    "implementation": {
      "approach": "Reused Part 1 parsing, sorted and took top 3",
      "lines_of_code": 15,
      "functions": 0
    },
    "challenges": [],
    "time_breakdown": {
      "implementation": 150.0,
      "testing": 30.0,
      "submission": 2.0
    }
  },

  "workflow_phases": {
    "fetch": {"duration": 3.2, "status": "success"},
    "parse": {"duration": 1.8, "status": "success"},
    "tdd_part1": {"duration": 167.5, "status": "success"},
    "submit_part1": {"duration": 2.0, "status": "success"},
    "tdd_part2": {"duration": 182.0, "status": "success"},
    "submit_part2": {"duration": 2.0, "status": "success"}
  },

  "code_quality": {
    "clippy_warnings": 0,
    "formatting_issues": 0,
    "compilation_time": 8.5
  }
}
```

## Report Generation Process

### Step 1: Load State Data

```rust
// Read state file
let state = fs::read_to_string("state/day{day}.json")?;
let data: DayState = serde_json::from_str(&state)?;
```

### Step 2: Analyze Patterns

```rust
// Identify patterns
let had_retries = data.part1.attempts.len() > 1 || data.part2.attempts.len() > 1;
let first_attempt_success = data.part1.attempts[0].response == "correct"
                           && data.part2.attempts[0].response == "correct";
let total_time = data.completed_at - data.started_at;
```

### Step 3: Generate Insights

Based on the data, generate neutral, factual insights:

**Example: Smooth Execution**
```markdown
## Insights & Patterns

### What Worked Well
- Both parts solved on first submission attempt
- Test coverage was comprehensive (covered all edge cases)
- TDD iterations were minimal (5 for Part 1, 3 for Part 2)
- Clear parsing strategy from examples

### What Could Be Improved
- None identified - workflow performed optimally

### Edge Cases Discovered
- None beyond examples provided in puzzle
```

**Example: Retry Scenario**
```markdown
## Insights & Patterns

### What Worked Well
- Test suite correctly validated example cases
- Retry logic successfully identified integer overflow issue
- Root cause analysis was accurate

### What Could Be Improved
- Consider adding automatic integer size checking (i32 vs i64)
- Could benefit from larger number test cases by default

### Edge Cases Discovered
- Real input contained numbers exceeding i32::MAX
- This wasn't apparent from examples which used small numbers
```

### Step 4: Generate Recommendations

```markdown
## Recommendations for Developer

{Analysis based on metrics}

Examples:

**Optimal Performance:**
"Workflow performed optimally. Both parts solved on first attempt with
comprehensive test coverage. No tuning required."

**Minor Issues:**
"Part 2 required 2 submission attempts due to off-by-one error not covered
by examples. Consider enhancing edge case test generation to include
boundary conditions automatically."

**Significant Issues:**
"Part 1 required 4 submission attempts. Test suite passed but real input
had edge case (negative numbers) not in examples. Recommend improving
puzzle parser to extract ALL constraints from problem description, not just
examples."

**Workflow Failure:**
"Failed to complete Part 2 after 5 attempts. Root cause: Misunderstood
problem requirements regarding 'consecutive' vs 'any order'. Recommend
enhancing natural language understanding of problem constraints."
```

### Step 5: Write Report File

```rust
// Generate markdown
let report = generate_report(&data)?;

// Write to file
fs::write(format!("puzzles/day{:02}/report.md", day), report)?;

// Log completion
println!("✅ Daily report generated: puzzles/day{:02}/report.md", day);
```

## Integration with Orchestrator

The daily reporter should be called as the **final step** of the orchestrator:

```
Orchestrator Flow:
1. Fetch puzzle
2. Parse examples
3. Solve Part 1 (TDD)
4. Submit Part 1
5. Solve Part 2 (TDD)
6. Submit Part 2
7. Generate Daily Report  ← NEW STEP
8. Cleanup & finish
```

## Report Tone Guidelines

Reports should be:

- **Neutral**: Factual, not judgmental
- **Informative**: Provide actionable data
- **Comprehensive**: Cover all aspects
- **Concise**: Avoid unnecessary detail
- **Analytical**: Identify patterns and trends

**Good Examples:**
- "Part 1 required 3 attempts. Root cause: Integer overflow. Fix: Changed i32 to i64."
- "TDD approach worked well with 5 test iterations for comprehensive coverage."
- "Puzzle parser successfully extracted 2 examples with expected outputs."

**Bad Examples:**
- "Failed miserably on Part 1" (judgmental)
- "Something went wrong" (not informative)
- "It worked" (not comprehensive)

## Multi-Day Analysis

After multiple days, reports enable trend analysis:

```bash
# Generate summary across all days
./scripts/analyze-reports.sh

# Example output:
# Total Days Completed: 12/12
# First Attempt Success Rate: 75% (18/24 parts)
# Average Retries Per Part: 1.3
# Most Common Failure: Integer overflow (5 occurrences)
# Average Solve Time: 4m 23s
```

## Example Reports

### Example 1: Perfect Execution

```markdown
# Day 1 - Calorie Counting - Status Report

**Date**: 2025-12-01 00:08:23 EST
**Overall Status**: ✅ Success
**Total Execution Time**: 6m 23s

---

## Summary

Both parts solved successfully on first submission attempt. Straightforward parsing and algorithm implementation.

## Part 1

**Status**: ✅ Correct
**Submission Attempts**: 1
**Time to Correct Answer**: 3m 0s

### Challenges Encountered
None - straightforward implementation

## Recommendations for Developer

Workflow performed optimally. No tuning required.
```

### Example 2: Retry Scenario

```markdown
# Day 5 - Supply Stacks - Status Report

**Date**: 2025-12-05 00:12:45 EST
**Overall Status**: ✅ Success
**Total Execution Time**: 10m 45s

---

## Part 1

**Status**: ✅ Correct
**Submission Attempts**: 3

### Retry Analysis

**Attempt 1**: Answer "CMZ" - Response: "That's not the right answer"
**Root Cause**: Reversed stack order (read top-to-bottom instead of bottom-to-top)
**Fix Applied**: Inverted parsing logic for stack initialization

**Attempt 2**: Answer "MCD" - Response: "That's not the right answer"
**Root Cause**: Off-by-one error in move logic (moved N+1 instead of N)
**Fix Applied**: Fixed loop bounds

**Attempt 3**: Answer "MZC" - Response: "Correct"

## Recommendations for Developer

Retry logic worked well, correctly identifying and fixing issues. Consider
adding more comprehensive parsing validation tests to catch stack order
issues earlier.
```

## Output Locations

Reports accessible at:
- `puzzles/day01/report.md` through `puzzles/day12/report.md`
- Summary: `reports/summary.md` (generated after all days)
- Analysis: `reports/analysis.json` (machine-readable metrics)

## Success Criteria

A good daily report should:
- ✅ Be generated automatically without errors
- ✅ Contain accurate metrics from state file
- ✅ Provide actionable insights
- ✅ Help developer assess workflow health
- ✅ Enable multi-day trend analysis
