---
name: regex-log
description: Guidance for extracting structured data from log files using regular expressions. This skill applies when parsing logs to extract dates, IP addresses, timestamps, or other structured patterns, especially when multiple conditions must be combined (e.g., "find the last date on lines containing an IP"). Use this skill for complex regex construction involving lookaheads, anchors, and pattern composition.
---

# Regex Log Extraction

## Overview

This skill provides guidance for constructing complex regular expressions to extract structured data from log files. It covers pattern composition strategies, verification approaches, and common pitfalls when dealing with multi-condition extractions (e.g., finding specific patterns only on lines matching other criteria).

## Approach Selection

When faced with a log extraction task, evaluate these approaches in order of complexity:

### Two-Stage Filtering (Recommended for Complex Conditions)

For tasks with multiple conditions (e.g., "find dates on lines with IP addresses"), consider a two-stage approach:

1. First filter: Identify lines matching one condition
2. Second filter: Extract target patterns from filtered lines

This approach is often cleaner and more maintainable than a single complex regex.

### Single Regex with Lookaheads

For single-pass extraction, use lookaheads to enforce multiple conditions:

- **Positive lookahead** `(?=...)`: Assert that a pattern exists somewhere
- **Negative lookahead** `(?!...)`: Assert that a pattern does NOT exist after current position

Structure: `^(?=.*CONDITION).*?(TARGET_PATTERN)(?!.*TARGET_PATTERN)`

The pattern above finds the last occurrence of TARGET_PATTERN on lines containing CONDITION.

## Pattern Construction Strategy

### Build Patterns Incrementally

1. **Define atomic patterns first**: Create and test each component separately
2. **Combine with clear structure**: Use Python string formatting to compose patterns
3. **Test each layer**: Verify behavior before adding complexity

Example approach for date + IP extraction:
```
Step 1: Define and test IPv4 pattern alone
Step 2: Define and test date pattern alone
Step 3: Combine with lookahead structure
Step 4: Test combined pattern thoroughly
```

### Common Pattern Components

**IPv4 addresses without leading zeros:**
- Octets: 0-9, 10-99, 100-199, 200-249, 250-255
- Requires explicit ranges to prevent matches like `01` or `001`

**Date validation (YYYY-MM-DD):**
- Different months have different day ranges
- 31-day months: 01, 03, 05, 07, 08, 10, 12
- 30-day months: 04, 06, 09, 11
- February: 01-28 or 01-29 (leap year handling may be needed)

**Word boundaries:**
- Use `\b` to prevent partial matches
- Test that `192.168.1.12024-01-15` does NOT match as valid IP + date

## Verification Strategy

### Required Test Categories

1. **Basic functionality**: Pattern matches expected targets
2. **Position variations**: Target appears before, after, and between other patterns
3. **Multiple occurrences**: Verify "first" or "last" logic works correctly
4. **Boundary conditions**: Patterns at line start, line end, adjacent to each other
5. **Rejection cases**: Invalid formats, partial matches, malformed data
6. **Edge cases**: Empty lines, lines with only spaces, very long lines

### Position Variation Tests

For "last date on lines with IP" type tasks, test ALL position combinations:
- IP before date: `192.168.1.1 ... 2024-01-15`
- IP after date: `2024-01-15 ... 192.168.1.1`
- Multiple dates with IP: `2024-01-14 192.168.1.1 2024-01-15` (should get 2024-01-15)
- Multiple IPs with date: `192.168.1.1 2024-01-15 10.0.0.1`
- IP at line end: `2024-01-15 192.168.1.1`

### Manual Trace-Through

For complex patterns, manually trace the regex engine's behavior on at least one example:

1. Write out the input string
2. Step through each regex component
3. Track backtracking and lookahead evaluations
4. Verify the captured groups contain expected values

## Common Pitfalls

### Greedy Quantifier Issues

- `.*` is greedy and consumes as much as possible
- Combined with lookaheads, this can cause unexpected behavior
- Consider using `.*?` (lazy) when appropriate
- Test with multiple potential matches on the same line

### Incomplete Date Validation

- `[0-9]{2}` for days allows invalid values like 00, 32-99
- Each month needs specific day validation
- February requires special handling (28 or 29 days)
- Single-digit dates like `2024-1-5` should be rejected if format requires zero-padding

### Leading Zero Handling in IPs

- IP octets should NOT match `01`, `001`, etc.
- Naive patterns like `[0-9]{1,3}` allow leading zeros
- Must explicitly enumerate valid ranges

### Word Boundary Placement

- `\b` behavior varies at start/end of strings
- Test patterns adjacent to punctuation and special characters
- Verify `192.168.1.12024-01-15` is NOT parsed as valid IP + date

### Anchor Behavior with MULTILINE

- `^` and `$` match line boundaries with `re.MULTILINE`
- Without this flag, they match only string start/end
- Confirm the correct flag is used for the task requirements

## Test Validation Checklist

Before finalizing a solution, confirm:

- [ ] All test output is visible and not truncated
- [ ] Tests cover all position variations
- [ ] At least one test verifies rejection of invalid formats
- [ ] Manual trace-through completed for one complex case
- [ ] Pattern components tested individually before combination
- [ ] Word boundaries prevent unintended partial matches

## Resources

### references/

Reference material for regex pattern construction is available in the `references/` directory:

- `regex_patterns.md`: Common regex patterns for log parsing with examples and explanations
