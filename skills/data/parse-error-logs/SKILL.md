---
name: parse-error-logs
description: Parse build errors, test failures, type-check output, and validation logs into structured data. Use when processing npm/pnpm output, TypeScript errors, Jest failures, or any validation command results for quality gates.
allowed-tools: Read
---

# Parse Error Logs

Parse error and validation output from various tools into structured, actionable data.

## When to Use

- Quality gate validation (type-check, build, tests)
- Parse TypeScript compiler errors
- Extract test failure information
- Process npm/pnpm command output
- Summarize validation results
- Feed error data to bug-fixer or other workers

## Instructions

### Step 1: Receive Raw Output

Accept raw command output as input.

**Expected Input**:

- `output`: String (raw stdout/stderr from command)
- `type`: String (typescript|jest|npm|build|generic)

### Step 2: Identify Error Patterns

Detect error patterns based on type.

**TypeScript Patterns**:

```
error TS2322: Type 'string' is not assignable to type 'number'.
src/file.ts(10,5): error TS2322
```

**Jest Patterns**:

```
FAIL src/test.spec.ts
● Test Suite › test name
  Expected: 5
  Received: 3
```

**npm/pnpm Patterns**:

```
ERR! code ENOENT
ERR! syscall open
ERR! path /path/to/file
```

**Build Patterns**:

```
ERROR in ./src/file.ts
Module not found: Error: Can't resolve 'module'
```

### Step 3: Extract Error Details

Parse each error into structured format.

**For Each Error Extract**:

- `file`: File path (if available)
- `line`: Line number (if available)
- `column`: Column number (if available)
- `code`: Error code (e.g., "TS2322", "ENOENT")
- `message`: Error message
- `severity`: error|warning|info
- `type`: Classification (type-error, test-failure, dependency, etc.)

### Step 4: Categorize and Count

Group errors by type and count occurrences.

**Categories**:

- Type errors
- Test failures
- Dependency issues
- Build errors
- Linting errors
- Runtime errors

### Step 5: Return Structured Data

Return complete error analysis.

**Expected Output**:

```json
{
  "success": false,
  "totalErrors": 15,
  "totalWarnings": 3,
  "summary": {
    "typeErrors": 8,
    "testFailures": 5,
    "buildErrors": 2
  },
  "errors": [
    {
      "file": "src/utils.ts",
      "line": 42,
      "column": 10,
      "code": "TS2322",
      "message": "Type 'string' is not assignable to type 'number'",
      "severity": "error",
      "type": "type-error"
    }
  ],
  "warnings": [
    {
      "file": "src/deprecated.ts",
      "line": 15,
      "code": "TS6133",
      "message": "'oldFunction' is declared but never used",
      "severity": "warning",
      "type": "unused-variable"
    }
  ]
}
```

## Error Handling

- **Empty Output**: Return success with zero errors
- **Unrecognized Format**: Return generic parse with raw message
- **Partial Parse**: Include what was parsed, note unparsable lines
- **Invalid Type**: Warn and default to "generic" parsing

## Examples

### Example 1: TypeScript Errors

**Input**:

```json
{
  "output": "src/app.ts(10,5): error TS2322: Type 'string' is not assignable to type 'number'.\nsrc/utils.ts(25,12): error TS2304: Cannot find name 'undefined'.",
  "type": "typescript"
}
```

**Output**:

```json
{
  "success": false,
  "totalErrors": 2,
  "totalWarnings": 0,
  "summary": {
    "typeErrors": 2
  },
  "errors": [
    {
      "file": "src/app.ts",
      "line": 10,
      "column": 5,
      "code": "TS2322",
      "message": "Type 'string' is not assignable to type 'number'",
      "severity": "error",
      "type": "type-error"
    },
    {
      "file": "src/utils.ts",
      "line": 25,
      "column": 12,
      "code": "TS2304",
      "message": "Cannot find name 'undefined'",
      "severity": "error",
      "type": "type-error"
    }
  ],
  "warnings": []
}
```

### Example 2: Jest Test Failures

**Input**:

```json
{
  "output": "FAIL src/utils.test.ts\n  ● Math › addition\n    expect(received).toBe(expected)\n    Expected: 5\n    Received: 3\n      at Object.<anonymous> (src/utils.test.ts:10:15)",
  "type": "jest"
}
```

**Output**:

```json
{
  "success": false,
  "totalErrors": 1,
  "totalWarnings": 0,
  "summary": {
    "testFailures": 1
  },
  "errors": [
    {
      "file": "src/utils.test.ts",
      "line": 10,
      "column": 15,
      "code": null,
      "message": "expect(received).toBe(expected) - Expected: 5, Received: 3",
      "severity": "error",
      "type": "test-failure",
      "testName": "Math › addition"
    }
  ],
  "warnings": []
}
```

### Example 3: Successful Build

**Input**:

```json
{
  "output": "✓ Built successfully\nCompleted in 2.3s",
  "type": "build"
}
```

**Output**:

```json
{
  "success": true,
  "totalErrors": 0,
  "totalWarnings": 0,
  "summary": {},
  "errors": [],
  "warnings": []
}
```

### Example 4: Mixed Errors and Warnings

**Input**:

```json
{
  "output": "Warning: React Hook useEffect has a missing dependency\nerror TS2339: Property 'foo' does not exist on type 'Bar'",
  "type": "typescript"
}
```

**Output**:

```json
{
  "success": false,
  "totalErrors": 1,
  "totalWarnings": 1,
  "summary": {
    "typeErrors": 1,
    "lintWarnings": 1
  },
  "errors": [
    {
      "code": "TS2339",
      "message": "Property 'foo' does not exist on type 'Bar'",
      "severity": "error",
      "type": "type-error"
    }
  ],
  "warnings": [
    {
      "message": "React Hook useEffect has a missing dependency",
      "severity": "warning",
      "type": "lint-warning"
    }
  ]
}
```

## Validation

- [ ] Parses TypeScript errors correctly
- [ ] Parses Jest test failures
- [ ] Parses npm/pnpm errors
- [ ] Parses build errors
- [ ] Extracts file, line, column when available
- [ ] Categorizes errors by type
- [ ] Returns summary counts
- [ ] Handles successful output (zero errors)
- [ ] Handles mixed errors and warnings

## Supporting Files

- `patterns.json`: Regex patterns for common error formats
