---
name: Check Code Block Highlights
description: Verify that hl_lines attributes in markdown code blocks correctly highlight the intended lines. Use when reviewing documentation with code examples, especially Before/After comparisons, or when highlights seem incorrect.
---

# Check Code Block Highlights

Verify that `hl_lines` attributes in markdown code blocks are correctly set to highlight the intended lines.

## Critical Understanding

**`hl_lines` is snippet-relative, NOT related to `linenums`**:

- `linenums="21"` sets the _displayed_ starting line number
- `hl_lines="3"` highlights the _3rd line of the snippet_ (which displays as line 23)
- These are completely independent attributes

Example:

```markdown
`groovy linenums="21" hl_lines="3"
process FOO {      <- displayed as line 21 (snippet line 1)
    input:         <- displayed as line 22 (snippet line 2)
    val x          <- displayed as line 23 (snippet line 3) - HIGHLIGHTED
}
`
```

## When to Use

- After writing or editing code blocks with highlights
- When reviewing Before/After comparison blocks
- When a user reports highlights look wrong
- As part of lesson review/validation

## How to Check

For each code block with `hl_lines`:

1. **Identify the code block** - Find blocks with `hl_lines="..."` attribute

2. **Count snippet lines** - Number each line of the code block starting from 1:

   ```
   1: #!/usr/bin/env nextflow
   2: (blank line)
   3: process FOO {
   4:     publishDir 'results'  <- if this should be highlighted, hl_lines should include "4"
   ...
   ```

3. **Verify intent** - For Before/After blocks:

   - "After" should highlight the NEW or CHANGED lines
   - "Before" should highlight the lines that WILL change (same content positions)
   - Both blocks should highlight corresponding lines showing the difference

4. **Check for common errors**:
   - Off-by-one errors (highlighting blank lines instead of code)
   - Confusing `linenums` with `hl_lines` (thinking hl_lines="21" highlights displayed line 21)
   - Highlighting section headers (`input:`, `output:`) instead of the actual values

## Fixing Issues

When you find incorrect highlights:

1. Count the actual line positions in the snippet (1-indexed)
2. Identify which lines contain the meaningful changes
3. Update `hl_lines` to reference those snippet line numbers
4. Verify Before/After blocks highlight corresponding positions

## Output Format

For each file checked, report:

```
## [filename]

### Block at line [N]: [description]
- Current: hl_lines="X Y Z"
- Lines X, Y, Z contain: [what's on those lines]
- Issue: [description of problem, if any]
- Suggested fix: hl_lines="A B C" (highlighting [what those lines contain])

### Summary
- Blocks checked: N
- Issues found: M
- [List of fixes needed]
```

## Example Analysis

Given this code block:

```markdown
`groovy title="example.nf" linenums="1" hl_lines="8 11 14"
#!/usr/bin/env nextflow       <- snippet line 1
                              <- snippet line 2 (blank)
process SAY_HELLO {           <- snippet line 3
                              <- snippet line 4 (blank)
    publishDir 'results'      <- snippet line 5
                              <- snippet line 6 (blank)
    input:                    <- snippet line 7
        val greeting          <- snippet line 8 - HIGHLIGHTED
                              <- snippet line 9 (blank)
    output:                   <- snippet line 10
        path "*.txt"          <- snippet line 11 - HIGHLIGHTED
                              <- snippet line 12 (blank)
    script:                   <- snippet line 13
        """echo hi"""         <- snippet line 14 - HIGHLIGHTED
}
`
```

Analysis: `hl_lines="8 11 14"` correctly highlights the input value (line 8), output value (line 11), and script content (line 14).

## Notes

- Blank lines count! They're common sources of off-by-one errors
- In Before/After comparisons, both blocks should highlight the same conceptual elements
- When in doubt, count every line including blanks and comments
