---
name: test-parser-jdk
description: Test the Java parser by parsing JDK source files and fixing parse errors. Use when asked to find/fix parse errors, test the parser, or improve JDK compatibility.
---

# Test Parser with JDK Sources

## Overview

This skill helps identify and fix parse errors in the Java parser by running it against JDK source files in `testcases/jdk/`.

## Commands

### Run the JDK parse test

```bash
go test -v -run TestParseJDKSourceFiles ./java/parser/ 2>&1 | grep -c "parse error"
```

This shows the total count of files with parse errors.

### List files with parse errors

```bash
go test -v -run TestParseJDKSourceFiles ./java/parser/ 2>&1 | grep "parse error" | head -20
```

### Parse a specific file and show errors

```bash
go run ./cmd/javalyzer parse <file> 2>&1 | grep -i "error"
```

Example:
```bash
go run ./cmd/javalyzer parse testcases/jdk/java.base/java/io/ObjectStreamClass.java 2>&1 | grep -i "error"
```

## Workflow for Fixing Parse Errors

1. **Identify a failing file**: Run the test and pick the first file with errors
2. **Find the error location**: Parse the file and grep for "ERROR:" to see line numbers
3. **Read the problematic code**: Use Read tool to examine the Java syntax at that location
4. **Understand the syntax**: Identify which Java language feature isn't being parsed
5. **Fix the parser**: Edit `java/parser/parser.go` to handle the syntax
6. **Verify the fix**: Re-parse the file to confirm errors are gone
7. **Run full test**: Check the total error count decreased
8. **Commit**: Use `git commit --no-verify -m "parser: <description of fix>"`

## Common Parse Error Patterns

- **Switch expressions**: `case null, default ->` (Java 21)
- **Array type method references**: `String[]::new`, `Class<?>[]::new`
- **Pattern matching**: `case String s ->`
- **Record patterns**: `case Point(int x, int y) ->`
- **Sealed classes**: `sealed class`, `permits`

## Key Parser Files

- `java/parser/parser.go` - Main parser implementation
- `java/parser/grammar.ebnf` - Grammar reference
- `java/parser/lexer.go` - Token definitions

## Example Error Output

```
Error [314:24-314:31] ERROR: expected expression
```

This means at line 314, columns 24-31, the parser expected an expression but found something unexpected.
