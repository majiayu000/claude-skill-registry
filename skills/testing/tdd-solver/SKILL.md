---
name: TDD Solver
description: Implement Advent of Code solutions using Test-Driven Development. Generates test cases from puzzle examples, writes failing tests first, implements solutions incrementally, and iterates until all tests pass. Use when solving AoC puzzles, implementing solutions with TDD, or when user mentions test-driven development or writing tests.
---

# TDD Solver

## Purpose

This skill implements puzzle solutions using strict Test-Driven Development (TDD) methodology. It generates test cases from examples, implements solutions incrementally, and iterates until all tests pass.

## Core Principles

1. **Tests First**: Always write tests before implementation
2. **Red-Green-Refactor**:
   - Red: Write failing test
   - Green: Make it pass with minimal code
   - Refactor: Clean up while keeping tests passing
3. **Incremental Development**: Build solution step by step
4. **Example-Driven**: All examples from puzzle must become tests

## Workflow

### Phase 1: Generate Test Cases

From parsed puzzle data, generate Rust test functions:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_INPUT: &str = "<extracted from puzzle>";

    #[test]
    fn test_part1_example1() {
        let result = part1(EXAMPLE_INPUT);
        assert_eq!(result, <expected_output>, "Example 1 should match");
    }

    // Additional examples...

    #[test]
    fn test_part1_edge_case_empty() {
        // Generate edge case tests
    }
}
```

### Phase 2: Initial Implementation Stub

Create minimal function signatures:

```rust
pub fn part1(input: &str) -> i64 {
    // TODO: Implement
    0
}

pub fn part2(input: &str) -> i64 {
    // TODO: Implement
    0
}
```

### Phase 3: Iterative Development

```
Loop:
  1. Run: cargo test
  2. If all tests pass → DONE
  3. If tests fail:
     a. Read failure output
     b. Understand what's needed
     c. Implement next piece
     d. Goto 1

  Max iterations: 50
  If exceeded → Flag for manual review
```

### Phase 4: Edge Case Detection

After examples pass, consider common edge cases:

```rust
#[test]
fn test_empty_input() {
    assert_eq!(part1(""), expected_for_empty);
}

#[test]
fn test_single_item() {
    assert_eq!(part1("single"), expected_for_single);
}

#[test]
fn test_large_numbers() {
    // Test integer overflow scenarios
}

#[test]
fn test_boundary_conditions() {
    // Min/max values, etc.
}
```

### Phase 5: Validation

Before declaring solution complete:

```bash
# All tests must pass
cargo test --package aoc-2025 --lib days::day{day}::tests

# No compiler warnings
cargo build 2>&1 | grep -i warning && exit 1

# Solution runs in reasonable time
timeout 15s cargo run -- {day}

# Code formatting
cargo fmt --check

# Clippy checks
cargo clippy -- -D warnings
```

## File Structure Per Day

```rust
// src/days/day{day}.rs

/// Day {day}: {Puzzle Title}
///
/// Problem description summary...

use std::fs;

// Helper functions for parsing
fn parse_input(input: &str) -> DataStructure {
    // Implement parsing logic
}

// Core solving logic
fn solve_part1_logic(data: &DataStructure) -> i64 {
    // Main algorithm
}

/// Part 1 solution
pub fn part1(input: &str) -> i64 {
    let data = parse_input(input);
    solve_part1_logic(&data)
}

/// Part 2 solution
pub fn part2(input: &str) -> i64 {
    let data = parse_input(input);
    solve_part2_logic(&data)
}

/// Entry point for running this day
pub fn run() {
    let input = fs::read_to_string("puzzles/day{day:02}/input.txt")
        .expect("Failed to read input file");

    println!("Day {day}: {Puzzle Title}");
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    // Example tests from puzzle
    // Edge case tests
    // Unit tests for helper functions
}
```

## Test Generation Templates

### Template 1: Basic Equality Test
```rust
#[test]
fn test_part1_example1() {
    let input = r#"<example input>"#;
    assert_eq!(part1(input), <expected>, "<description>");
}
```

### Template 2: Multi-Step Verification
```rust
#[test]
fn test_parsing_then_solving() {
    let input = r#"<example input>"#;
    let parsed = parse_input(input);
    assert_eq!(parsed.len(), <expected_length>);

    let result = solve_part1_logic(&parsed);
    assert_eq!(result, <expected>);
}
```

### Template 3: Error Handling
```rust
#[test]
#[should_panic(expected = "Invalid input")]
fn test_invalid_input() {
    part1("garbage input");
}
```

## Common Parsing Patterns

### Pattern 1: Line-by-Line Numbers
```rust
fn parse_input(input: &str) -> Vec<i64> {
    input
        .lines()
        .filter_map(|line| line.trim().parse().ok())
        .collect()
}
```

### Pattern 2: Groups Separated by Blank Lines
```rust
fn parse_input(input: &str) -> Vec<Vec<String>> {
    input
        .split("\n\n")
        .map(|group| group.lines().map(String::from).collect())
        .collect()
}
```

### Pattern 3: Grid/Matrix
```rust
fn parse_input(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}
```

### Pattern 4: Key-Value Pairs
```rust
fn parse_input(input: &str) -> HashMap<String, i64> {
    input
        .lines()
        .filter_map(|line| {
            let parts: Vec<_> = line.split(": ").collect();
            if parts.len() == 2 {
                Some((parts[0].to_string(), parts[1].parse().ok()?))
            } else {
                None
            }
        })
        .collect()
}
```

## Implementation Strategies

### Strategy 1: Brute Force First
Start with the simplest, most obvious solution:
```rust
pub fn part1(input: &str) -> i64 {
    // Even if O(n²) or worse, get it working first
    // Optimize later if needed
}
```

### Strategy 2: Incremental Optimization
Only optimize if:
- Tests are failing due to timeout
- Real input is too large for brute force
- Problem explicitly requires optimization

### Strategy 3: Reuse Common Utilities
```rust
use crate::utils::{
    read_input,
    parse_char_grid,
    parse_int_lines,
    split_by_blank_lines
};
```

## Debugging Failed Tests

When tests fail:

### 1. Read Error Message Carefully
```
assertion `left == right` failed
  left: 42
 right: 24
```

→ Solution returned 42, expected 24
→ Check logic, likely off by some factor

### 2. Add Debug Prints
```rust
#[test]
fn test_part1_example1() {
    let input = EXAMPLE_INPUT;
    let parsed = parse_input(input);
    eprintln!("Parsed: {:?}", parsed);  // Debug output

    let result = part1(input);
    eprintln!("Result: {}", result);    // Debug output

    assert_eq!(result, 24000);
}
```

### 3. Verify Parsing
Most errors come from incorrect parsing:
```rust
#[test]
fn test_parsing() {
    let input = EXAMPLE_INPUT;
    let parsed = parse_input(input);
    // Verify structure matches expectations
    assert_eq!(parsed.len(), 5, "Should have 5 groups");
}
```

### 4. Test Individual Components
```rust
#[test]
fn test_calculate_totals() {
    let data = vec![vec![1, 2, 3], vec![4, 5]];
    let totals = calculate_totals(&data);
    assert_eq!(totals, vec![6, 9]);
}
```

## Handling Part 2

Part 2 often:
- Extends Part 1 logic
- Changes the question asked
- Adds complexity or new requirements

### Option 1: Extend Part 1
```rust
pub fn part2(input: &str) -> i64 {
    // Reuse Part 1 parsing and logic
    let data = parse_input(input);

    // Modify the solving approach
    solve_part2_logic(&data)
}
```

### Option 2: Refactor Both Parts
If Part 2 reveals a better structure:
```rust
fn solve_generic(input: &str, mode: SolveMode) -> i64 {
    let data = parse_input(input);
    match mode {
        SolveMode::Part1 => solve_part1_logic(&data),
        SolveMode::Part2 => solve_part2_logic(&data),
    }
}

pub fn part1(input: &str) -> i64 {
    solve_generic(input, SolveMode::Part1)
}

pub fn part2(input: &str) -> i64 {
    solve_generic(input, SolveMode::Part2)
}
```

## Testing Before Submission

Before generating answer for submission:

```bash
# Run all tests
cargo test days::day{day}

# Run with real input (should complete quickly)
time cargo run -- {day}

# Verify output format (should be a single number)
cargo run -- {day} | grep "Part 1:" | awk '{print $3}' | grep -E '^[0-9]+$'
```

## Common Pitfalls

### Pitfall 1: Integer Overflow
```rust
// Use i64 instead of i32 for AoC problems
// Many puzzles have large numbers
pub fn part1(input: &str) -> i64 {  // Not i32!
    // ...
}
```

### Pitfall 2: Off-By-One Errors
```rust
// Careful with ranges
for i in 0..n {      // 0 to n-1
for i in 0..=n {     // 0 to n (inclusive)
```

### Pitfall 3: String Trimming
```rust
// Many puzzles have trailing newlines
let clean_input = input.trim();
```

### Pitfall 4: Example vs Real Input
```rust
// Example: Small, simple
// Real input: Large, complex edge cases

// Always test with both!
```

## Performance Requirements

- Solution must complete in < 15 seconds (AoC rule)
- Most efficient solutions run in < 1 second
- If taking too long, consider:
  - Better algorithm (reduce time complexity)
  - Memoization/caching
  - Different data structure

## Integration Points

### Input
- Parsed puzzle data from puzzle-fetcher skill
- Real input file from puzzles/day{day}/input.txt

### Output
- Implemented solution in src/days/day{day}.rs
- Answer for submission (single integer/string)
- All tests passing

### Called By
- aoc-orchestrator skill

### Reports To
- Test results to orchestrator
- Generated answer for submission-handler
