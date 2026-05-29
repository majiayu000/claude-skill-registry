---
name: Puzzle Fetcher
description: Download and parse Advent of Code puzzles using aoc-cli. Extracts examples, expected outputs, and problem requirements from puzzle descriptions. Use when needing to fetch AoC puzzles, parse puzzle examples, or when user mentions downloading or reading AoC puzzle data.
---

# Puzzle Fetcher

## Purpose

This skill handles downloading puzzle descriptions and input files from adventofcode.com using the `aoc-cli` tool, then parsing them to extract examples, expected outputs, and problem requirements.

## Primary Responsibilities

1. Download puzzle description (Markdown format)
2. Download puzzle input
3. Parse puzzle description to extract:
   - Problem statement and requirements
   - Example inputs
   - Expected outputs for examples
   - Part 1 vs Part 2 differentiations
4. Structure data for consumption by TDD solver

## Using aoc-cli

### Download Puzzle and Input

```bash
# Download for specific day
aoc download --day {day} --year 2025 \
  --puzzle-file puzzles/day{day:02}/puzzle.md \
  --input-file puzzles/day{day:02}/input.txt

# Example for Day 1:
aoc download --day 1 --year 2025 \
  --puzzle-file puzzles/day01/puzzle.md \
  --input-file puzzles/day01/input.txt
```

### Handle Different Scenarios

```bash
# If puzzle not yet unlocked
# aoc-cli will return error: "Puzzle X of 2025 is still locked"

# If already downloaded and --overwrite not specified
# aoc-cli will skip download and inform file exists

# Force re-download
aoc download --day 1 --year 2025 --overwrite
```

## Parsing Puzzle Description

The puzzle.md file is in Markdown format. Parse it to extract:

### 1. Problem Title
```markdown
## --- Day 1: Calorie Counting ---
```
Extract: "Calorie Counting"

### 2. Example Inputs/Outputs

Look for patterns like:
```markdown
For example:

```
1000
2000
3000

4000
```

This list represents...
```

Example extraction logic:
- Find code blocks (triple backticks) that appear before explanatory text
- These are usually example inputs
- Look for phrases like "the answer is", "the total is", "should be" to find expected outputs
- Common patterns:
  - "the result is **42**" → Extract 42
  - "a total of **24000** calories" → Extract 24000
  - "How many...? Your puzzle answer was `123`" → Extract 123

### 3. Part 1 vs Part 2

Part 2 typically appears after:
```markdown
## --- Part Two ---
```

Important:
- Part 2 often modifies Part 1 requirements
- May introduce new examples
- May reuse Part 1 examples with different expected outputs

## Output Format

Structure the parsed data as JSON for downstream consumption:

```json
{
  "day": 1,
  "year": 2025,
  "title": "Calorie Counting",
  "part1": {
    "description": "Find the elf carrying the most calories...",
    "examples": [
      {
        "input": "1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000",
        "expected_output": "24000",
        "explanation": "The fourth elf has the most calories"
      }
    ]
  },
  "part2": {
    "description": "Find the top three elves carrying the most calories...",
    "examples": [
      {
        "input": "1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000",
        "expected_output": "45000",
        "explanation": "Top three totals: 24000 + 11000 + 10000"
      }
    ]
  },
  "input_file_path": "puzzles/day01/input.txt",
  "puzzle_file_path": "puzzles/day01/puzzle.md"
}
```

Save this to: `puzzles/day{day:02}/parsed.json`

## Example Extraction Strategies

### Strategy 1: Code Block Detection
```markdown
For example:

```
<example input here>
```

The answer is **123**
```

→ Input: content of code block
→ Output: 123

### Strategy 2: Inline Examples
```markdown
If the input is `abc`, the output would be `42`.
```

→ Input: "abc"
→ Output: 42

### Strategy 3: Multi-Step Examples
```markdown
Given this input:

```
line1
line2
```

First, do X which gives Y.
Then, do Z which results in **final answer 42**.
```

→ Input: "line1\nline2"
→ Output: 42

## Edge Cases to Handle

### Multiple Examples
Some puzzles provide multiple examples:
```markdown
For example:

Example 1:
Input: `abc`
Output: `1`

Example 2:
Input: `def`
Output: `2`
```

Create separate example objects for each.

### Examples Without Explicit Output
Some examples show the process but don't state the answer:
```markdown
For example, given this input...
[process description]
```

In this case:
- Flag that expected output needs manual extraction
- Include process description in explanation field
- May need to compute expected output from process

### Part 2 Reusing Part 1 Examples
Part 2 often says "using the same example from Part 1":
- Reference Part 1's example input
- Extract Part 2's expected output
- Link them together

## Validation

Before returning parsed data, validate:

✅ Puzzle file exists and is readable
✅ Input file exists and is readable
✅ At least one example extracted for Part 1
✅ Title extracted successfully
✅ Part 1 description exists
✅ If Part 2 section exists, Part 2 data extracted

## Error Handling

### Puzzle Not Available Yet
```
Error: Puzzle 5 of 2025 is still locked
Action: Return error status, orchestrator will handle retry
```

### Network Failure
```
Error: Failed to connect to adventofcode.com
Action: Retry up to 3 times with exponential backoff
```

### Parsing Failure
```
Error: Could not extract examples from puzzle description
Action: Save raw puzzle.md, flag for manual review
Log: Warning about parsing failure
Still proceed with solution attempt using manual test creation
```

## File Organization

After fetching:
```
puzzles/
  day01/
    puzzle.md        # Raw puzzle description from aoc-cli
    input.txt        # Real puzzle input
    parsed.json      # Structured parsed data
  day02/
    ...
```

## Testing This Skill

Create test cases with:
1. Mock puzzle.md files with various formats
2. Verify correct extraction of examples
3. Test edge cases (no examples, multiple examples, etc.)
4. Validate JSON output structure

## Integration Points

### Called By
- aoc-orchestrator skill (main workflow)

### Calls
- `aoc-cli` command-line tool via Bash

### Outputs Used By
- tdd-solver skill (consumes parsed.json)

## Performance Considerations

- Cache puzzle descriptions once downloaded
- Don't re-download if file exists (unless forced)
- Parsing should complete in < 1 second
- Network download typically < 5 seconds

## Command Interface

When invoked directly:

```bash
# Fetch today's puzzle
./scripts/fetch-puzzle.sh

# Fetch specific day
./scripts/fetch-puzzle.sh 5

# Force re-download
./scripts/fetch-puzzle.sh 1 --force

# Dry run (download but don't parse)
./scripts/fetch-puzzle.sh 1 --dry-run
```
