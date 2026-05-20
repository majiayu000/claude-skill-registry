---
name: TypeScript Test Management
description: Manage TypeScript/JavaScript test files using ts-morph. List, add, remove, and modify describe/test blocks. Designed for LLM use with structured output.
allowed-tools:
  - Bash
  - Read
---

# TypeScript Test Management

This skill provides scripts to read and modify TypeScript/JavaScript test files using ts-morph. All modification scripts automatically format the output with Prettier.

## Requirements

Peer dependencies (must be installed in consuming project):
- `ts-morph` - AST manipulation
- `prettier` - Code formatting

## Available Scripts

### List Tests

View the hierarchy of describe/it blocks with line numbers:

```bash
.claude/skills/typescript-test-management/scripts/list-tests.cjs <file-path>
```

**Output format:**
```
describe "User Authentication" (10-50)
  it "should login successfully" (12-18)
  it "should reject invalid credentials" (20-26)
  describe "Password Reset" (28-48)
    it "should send reset email" (30-36)
```

### Add Describe Block

Add a new describe block to a test file:

```bash
# Add at the end of file
.claude/skills/typescript-test-management/scripts/add-describe.cjs <file-path> <describe-name>

# Add after specific line
.claude/skills/typescript-test-management/scripts/add-describe.cjs <file-path> <describe-name> --after-line=50

# Add after another describe (by name)
.claude/skills/typescript-test-management/scripts/add-describe.cjs <file-path> <describe-name> --after-describe="Existing Describe"
```

**Output:** Line numbers of created describe block (e.g., "Added describe at lines 52-58")

### Add Test Case

Add a test case inside a describe block:

```bash
# Add to first describe in file (placeholder body)
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> <test-name>

# Add to specific describe
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> <test-name> --describe="User Authentication"

# Simple inline body
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> "should return null" --body="expect(result).toBeNull()"

# Async test with body from file (file auto-deleted after use)
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> "should create entity" \
  --describe="Suite" --async --body-file=/tmp/test-body.js

# Add after specific test
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> <test-name> --after-test="existing test name"

# Add after specific line
.claude/skills/typescript-test-management/scripts/add-test.cjs <file-path> <test-name> --after-line=20
```

**Options:**
- `--describe="Name"` - Add to specific describe block
- `--body="code"` - Inline test body (simple cases)
- `--body-file=path` - Read test body from file (complex cases, auto-deleted)
- `--async` - Create async test function
- `--after-test="Name"` - Insert after specific test
- `--after-line=N` - Insert after line N

**Output:** Line numbers of created test (e.g., "Added test at lines 21-25")

### Add beforeEach

Add a beforeEach block to a describe for test setup:

```bash
# Simple inline body
.claude/skills/typescript-test-management/scripts/add-beforeEach.cjs <file-path> --body="jest.clearAllMocks()"

# Add to specific describe
.claude/skills/typescript-test-management/scripts/add-beforeEach.cjs <file-path> --describe="User Authentication" --body="mockReset()"

# Async beforeEach with body from file
.claude/skills/typescript-test-management/scripts/add-beforeEach.cjs <file-path> --describe="Suite" --async --body-file=/tmp/setup.js
```

**Options:**
- `--describe="Name"` - Add to specific describe block
- `--body="code"` - Inline body (required unless using --body-file)
- `--body-file=path` - Read body from file (auto-deleted)
- `--async` - Create async beforeEach

**Output:** Line numbers of created beforeEach (e.g., "Added beforeEach at lines 12-15")

### Add afterEach

Add an afterEach block to a describe for test cleanup:

```bash
# Simple inline body
.claude/skills/typescript-test-management/scripts/add-afterEach.cjs <file-path> --body="jest.restoreAllMocks()"

# Add to specific describe
.claude/skills/typescript-test-management/scripts/add-afterEach.cjs <file-path> --describe="Database Tests" --body="await db.cleanup()"

# Async afterEach with body from file
.claude/skills/typescript-test-management/scripts/add-afterEach.cjs <file-path> --describe="Suite" --async --body-file=/tmp/teardown.js
```

**Options:**
- `--describe="Name"` - Add to specific describe block
- `--body="code"` - Inline body (required unless using --body-file)
- `--body-file=path` - Read body from file (auto-deleted)
- `--async` - Create async afterEach

**Note:** afterEach is inserted after any existing beforeEach/beforeAll/afterAll blocks

**Output:** Line numbers of created afterEach (e.g., "Added afterEach at lines 16-19")

### Remove Test

Remove a test case by name (supports partial matching):

```bash
.claude/skills/typescript-test-management/scripts/remove-test.cjs <file-path> <test-name>
```

**Output:** Confirmation with line numbers removed

### Remove Describe

Remove a describe block and all its contents:

```bash
.claude/skills/typescript-test-management/scripts/remove-describe.cjs <file-path> <describe-name>
```

**Output:** Confirmation with line numbers removed

### Toggle Skip/Only

Toggle skip or only modifiers on tests or describe blocks:

```bash
# Toggle to skip
.claude/skills/typescript-test-management/scripts/toggle-skip.cjs <file-path> <test-or-describe-name> --skip

# Toggle to only
.claude/skills/typescript-test-management/scripts/toggle-skip.cjs <file-path> <test-or-describe-name> --only

# Remove modifier (back to normal)
.claude/skills/typescript-test-management/scripts/toggle-skip.cjs <file-path> <test-or-describe-name> --none
```

**Output:** Confirmation of change

### Replace Test/Describe Body

Replace the body of a test or describe block:

```bash
# Replace test body (inline)
.claude/skills/typescript-test-management/scripts/replace-test-body.cjs <file-path> <test-name> "expect(true).toBe(true)"

# Replace test body from file (auto-deleted after use)
.claude/skills/typescript-test-management/scripts/replace-test-body.cjs <file-path> <test-name> --body-file=/tmp/body.js

# Replace describe body (all its contents)
.claude/skills/typescript-test-management/scripts/replace-test-body.cjs <file-path> <describe-name> <new-body> --type=describe
```

**Options:**
- `--type=test` - Replace test body (default)
- `--type=describe` - Replace describe body
- `--body-file=path` - Read new body from file (auto-deleted)

**Note:** Supports partial matching of name

**Output:** Line numbers of modified block

## Design Notes

- **LLM-optimized**: Structured, concise output designed for programmatic consumption
- **Auto-formatting**: All modifications run Prettier for consistent formatting
- **Line numbers**: Modification operations return line numbers for LLM reference
- **Partial matching**: Remove/modify operations support partial name matching
- **Safe operations**: Scripts validate file structure before making changes

## Example Workflow

```bash
# 1. List current test structure
.claude/skills/typescript-test-management/scripts/list-tests.cjs src/auth.test.ts

# 2. Add a new describe block
.claude/skills/typescript-test-management/scripts/add-describe.cjs src/auth.test.ts "Session Management"
# Output: Added describe at lines 60-64

# 3. Add a simple test with inline body
.claude/skills/typescript-test-management/scripts/add-test.cjs src/auth.test.ts "should reject null" \
  --describe="Session Management" --body="expect(createSession(null)).rejects.toThrow()"
# Output: Added test at lines 61-63

# 4. Add a complex async test using body file
# First write the body to a temp file, then call add-test
.claude/skills/typescript-test-management/scripts/add-test.cjs src/auth.test.ts "should create session" \
  --describe="Session Management" --async --body-file=/tmp/test-body.js
# Output: Added test at lines 65-72

# 5. Toggle a test to skip
.claude/skills/typescript-test-management/scripts/toggle-skip.cjs src/auth.test.ts "should create session" --skip

# 6. Remove a test
.claude/skills/typescript-test-management/scripts/remove-test.cjs src/auth.test.ts "old test name"
```

## Body File Pattern

For complex test bodies with template literals, await expressions, or multi-line logic:

1. Write the test body to a temp file (e.g., `/tmp/test-body.js`)
2. Call the script with `--body-file=/tmp/test-body.js`
3. The file is automatically deleted after reading

This avoids shell escaping issues and works well with LLM parallel tool calls (Write + Bash in same message).

## Notes

- Works with Jest, Vitest, Mocha, and other test frameworks using describe/it syntax
- Supports both TypeScript (.ts, .tsx) and JavaScript (.js, .jsx) files
- Preserves existing code formatting through Prettier integration
- All scripts exit with non-zero status on errors
