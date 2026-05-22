---
name: sai-fmt-testing
description: |
  Use this skill when the user asks you to test the sai fmt command
  in a given project.
---
# Skill: Testing and Improving `sai fmt`

## When to Use

Use this skill when asked to find formatting inconsistencies in `sai fmt` and fix them.

## Prerequisites

A **test repository** with Java source files. If not specified, ask the user.

## Key Files

- `format/java_pretty.go` - Main pretty printer implementation
- `format/java_pretty_test.go` - Test cases for the formatter

## Workflow

### Step 1: Select Test Repository

If no repository is specified, ask the user.

### Step 2: Pick a Java File

Select a `.java` file from the repository to test. Prefer files with varied constructs (classes, methods, generics, lambdas, etc.).

### Step 3: Diff Against Formatter Output

```bash
sai fmt <file> | diff -u - <file>
```

### Step 4: Inspect the Diff

Look for formatting issues that seem "off":

- Needless blank lines added or removed
- Incorrect indentation
- Broken method chains
- Mangled comments
- Wrong spacing around operators
- Issues with generics, annotations, or lambdas

### Step 5: Iterate or Create Test Case

**If no issues found:** Pick another file and repeat (up to 3 files total).

**If issues found:** Proceed to create a minimal test case.

### Step 6: Create Test Case

Add a minimal reproducer to `format/java_pretty_test.go`:

- Find the appropriate `Test*` function for the construct
- Add a new test case with `input` and `expected` fields
- Keep the test case as small as possible while reproducing the issue

### Step 7: Watch the Test Fail

```bash
go test ./format -run TestPrint<RelevantTest> -v
```

Confirm the test fails with the expected vs actual output.

### Step 8: Implement the Fix

**Important:** Do not rely on heuristics in the formatter. If the AST lacks necessary information to produce correct output, fix the parser first to include that information.

Common fix locations:

- `java/parser/parser.go` - Add missing AST nodes or structure
- `java/parser/node.go` - Add new node kinds if needed
- `format/java_pretty.go` / `format/java_pretty_stmt.go` - Update formatter to use the improved AST

### Step 9: Verify and Commit

```bash
githooks/pre-commit
git add format/java_pretty.go format/java_pretty_test.go
git commit -m "format: fix <description of the issue>"
```

## Tips

- Start with complex files (builders, streams, generics) as they're more likely to expose issues
- The formatter should be idempotent: running it twice should produce the same output
- When in doubt about expected output, follow Google Java Style Guide conventions
