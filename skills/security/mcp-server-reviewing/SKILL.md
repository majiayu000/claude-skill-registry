---
name: mcp-server-reviewing
description: Audits MCP servers for security vulnerabilities, missing validation, error handling issues, and production readiness. Use when reviewing MCP PRs or auditing server quality.
version: 1.0.0
---

# MCP Server Reviewing

## Purpose

Audit MCP (Model Context Protocol) servers for security issues, architectural violations, missing validation, and production readiness. Ensure servers follow SDK best practices.

## When to Use This Skill

- Reviewing MCP server code in PRs
- Auditing existing MCP servers for quality
- Pre-release security and quality checks
- Verifying MCP servers follow best practices

## When NOT to Use This Skill

- Writing new MCP servers (use **mcp-server-writing**)
- General TypeScript/Python code review (use language-specific reviewers)
- Reviewing non-MCP server code

---

## Severity Classification

| Severity     | Description                                                  | Action                    |
| ------------ | ------------------------------------------------------------ | ------------------------- |
| **CRITICAL** | Security vulnerabilities, secrets exposure, data leaks       | Block PR, fix immediately |
| **HIGH**     | Missing validation, error swallowing, transport violations   | Block PR, require fix     |
| **MEDIUM**   | Missing descriptions, poor error messages, logging issues    | Request fix before merge  |
| **LOW**      | Style issues, optimization opportunities, minor improvements | Suggest improvements      |

---

## Automated Detection Commands

Run these commands to detect common violations. Each command includes the violation code for reference.

### Security Violations (S1-S5)

**S1: Hardcoded Secrets**

```bash
grep -rn "api[_-]\?key\s*[:=]" --include="*.ts" --include="*.py" src/ | grep -v "process\.env\|os\.environ"
```

**S2: Console.log to stdout (breaks stdio transport)**

```bash
grep -rn "console\.log\|print(" --include="*.ts" --include="*.py" src/ | grep -v "console\.error\|sys\.stderr\|\.test\.\|\.spec\."
```

**S3: Missing ReDoS Protection**

```bash
grep -rn "new RegExp\|\.match\|\.replace\|\.split" --include="*.ts" --include="*.py" src/ | grep -v "safeInput\|MAX_INPUT"
```

**S4: Unsafe eval/exec**

```bash
grep -rn "eval(\|exec(\|Function(" --include="*.ts" --include="*.py" src/
```

**S5: SQL Injection Risk**

```bash
grep -rn "query.*\`\|execute.*f\"\|cursor\.execute.*%" --include="*.ts" --include="*.py" src/
```

### Architecture Violations (A1-A5)

**A1: Missing Tool Descriptions**

```bash
grep -rn "name:\s*['\"]" --include="*.ts" src/ -A 3 | grep -B 3 "inputSchema" | grep -v "description"
```

**A2: Missing inputSchema Property Descriptions**

```bash
grep -rn "properties:" --include="*.ts" src/ -A 10 | grep -E "type.*string|type.*number" | grep -v "description"
```

**A3: Tools Without Validation**

```bash
grep -rn "request\.params\|args\." --include="*.ts" src/ | grep -v "validate\|ajv\|zod\|schema"
```

**A4: Missing isError Flag**

```bash
grep -rn "content.*error\|success.*false" --include="*.ts" src/ | grep -v "isError"
```

**A5: Direct Response Without JSON**

```bash
grep -rn "text:.*\`" --include="*.ts" src/ | grep -v "JSON\.stringify"
```

### Error Handling Violations (E1-E5)

**E1: Empty Catch Blocks**

```bash
grep -rn "catch.*{" --include="*.ts" --include="*.py" src/ -A 2 | grep -E "^\s*}\s*$"
```

**E2: Swallowed Errors (catch without rethrow or return)**

```bash
grep -rn "catch" --include="*.ts" src/ -A 5 | grep -v "throw\|return\|logger\|console\.error"
```

**E3: Missing Error Context**

```bash
grep -rn "throw new Error\|raise.*Error" --include="*.ts" --include="*.py" src/ | grep -v ":\|context\|failed"
```

**E4: Generic Error Messages**

```bash
grep -rn "\"error\"\|\"Error\"\|\"failed\"" --include="*.ts" src/ | grep -v "suggestion\|field\|message"
```

**E5: Unhandled Promise Rejections**

```bash
grep -rn "\.then(" --include="*.ts" src/ | grep -v "\.catch\|await"
```

### Maintainability Violations (M1-M5)

**M1: Magic Numbers/Strings**

```bash
grep -rn "[0-9]\{4,\}\|timeout.*[0-9]" --include="*.ts" --include="*.py" src/ | grep -v "const\|MAX_\|MIN_\|DEFAULT_"
```

**M2: Missing Type Annotations (Python)**

```bash
grep -rn "def.*(" --include="*.py" src/ | grep -v "->.*:"
```

**M3: TODO/FIXME in Production Code**

```bash
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.ts" --include="*.py" src/
```

**M4: Duplicate Tool Definitions**

```bash
grep -rn "name:\s*['\"]" --include="*.ts" src/ | cut -d: -f3 | sort | uniq -d
```

**M5: Inconsistent Error Response Format**

```bash
grep -rn "isError.*true" --include="*.ts" src/ -B 5 | grep "text:" | grep -v "success\|errors"
```

---

## Manual Review Checklist

### Security Review

- [ ] **S1**: No hardcoded API keys, passwords, or secrets
- [ ] **S2**: All logging goes to stderr (not stdout)
- [ ] **S3**: Input length limited before regex processing
- [ ] **S4**: No eval(), exec(), or dynamic code execution
- [ ] **S5**: Parameterized queries for any database access
- [ ] **S6**: Environment variables used for configuration
- [ ] **S7**: Sensitive data not logged (passwords, tokens, PII)

### Architecture Review

- [ ] **A1**: All tools have clear `description` fields
- [ ] **A2**: All inputSchema properties have `description`
- [ ] **A3**: Input validation before any processing
- [ ] **A4**: Error responses include `isError: true`
- [ ] **A5**: All responses are JSON-serialized
- [ ] **A6**: Resources use appropriate URI schemes
- [ ] **A7**: Prompts have clear argument descriptions

### Error Handling Review

- [ ] **E1**: No empty catch blocks
- [ ] **E2**: Errors logged or re-thrown, never swallowed
- [ ] **E3**: Error messages include context (what failed, why)
- [ ] **E4**: Error responses include `suggestion` field
- [ ] **E5**: Async operations properly awaited/handled
- [ ] **E6**: Graceful degradation for external dependencies

### Production Readiness Review

- [ ] **P1**: Structured logging with JSON format
- [ ] **P2**: Health check endpoint or mechanism
- [ ] **P3**: Configurable timeouts for external calls
- [ ] **P4**: Graceful shutdown handling
- [ ] **P5**: No debug/development code in production
- [ ] **P6**: Dependencies pinned to specific versions
- [ ] **P7**: Dockerfile or deployment configuration present

---

## Common Violations with Fixes

### S2: Logging to stdout (CRITICAL)

**Problem:** stdout is reserved for JSON-RPC messages. Logging there corrupts the transport.

```typescript
// ❌ BAD: Breaks MCP stdio transport
console.log("Processing request:", args);
```

```typescript
// ✅ GOOD: Log to stderr
console.error(
  JSON.stringify({
    timestamp: new Date().toISOString(),
    level: "INFO",
    message: "Processing request",
    context: { args_keys: Object.keys(args) },
  }),
);
```

### S3: Missing ReDoS Protection (HIGH)

**Problem:** Unbounded input to regex can cause catastrophic backtracking.

```typescript
// ❌ BAD: No input length limit
const matches = userInput.match(/complex.*pattern/);
```

```typescript
// ✅ GOOD: Limit input before regex
const MAX_INPUT_LENGTH = 50_000;
const safeInput = (text: string) =>
  text.length > MAX_INPUT_LENGTH ? text.slice(0, MAX_INPUT_LENGTH) : text;

const matches = safeInput(userInput).match(/complex.*pattern/);
```

### A1: Missing Tool Description (MEDIUM)

**Problem:** LLM can't understand when to use the tool.

```typescript
// ❌ BAD: No description
{
  name: "process_data",
  inputSchema: { type: "object", properties: { data: { type: "string" } } }
}
```

```typescript
// ✅ GOOD: Clear description explaining purpose and return value
{
  name: "process_data",
  description: "Validates and transforms input data according to specified format. Returns structured result with validation errors if any.",
  inputSchema: {
    type: "object",
    properties: {
      data: {
        type: "string",
        description: "Raw data string to process"
      },
      format: {
        type: "string",
        enum: ["json", "csv", "xml"],
        description: "Expected input format for validation"
      }
    },
    required: ["data", "format"]
  }
}
```

### A4: Missing isError Flag (HIGH)

**Problem:** Client can't distinguish errors from successful responses.

```typescript
// ❌ BAD: Error without isError flag
return {
  content: [{ type: "text", text: JSON.stringify({ error: "Not found" }) }],
};
```

```typescript
// ✅ GOOD: Proper error response
return {
  content: [
    {
      type: "text",
      text: JSON.stringify({
        success: false,
        errors: [
          {
            field: "id",
            message: "Resource not found",
            suggestion: "Verify the ID exists and try again",
          },
        ],
      }),
    },
  ],
  isError: true,
};
```

### E1: Empty Catch Block (HIGH)

**Problem:** Errors are silently swallowed, making debugging impossible.

```typescript
// ❌ BAD: Silent failure
try {
  await riskyOperation();
} catch (error) {
  // do nothing
}
```

```typescript
// ✅ GOOD: Log and handle appropriately
try {
  await riskyOperation();
} catch (error) {
  logger.error("Risky operation failed", { error: error.message });
  return createErrorResponse([
    {
      field: "operation",
      message: "Operation failed",
      suggestion: "Check input parameters and retry",
    },
  ]);
}
```

### E4: Generic Error Messages (MEDIUM)

**Problem:** Users can't understand what went wrong or how to fix it.

```typescript
// ❌ BAD: Unhelpful error
return { error: "Something went wrong" };
```

```typescript
// ✅ GOOD: Specific, actionable error
return {
  success: false,
  errors: [
    {
      field: "partner_id",
      message: "Invalid UUID format: 'abc123'",
      suggestion: "Use format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    },
  ],
};
```

---

## Review Report Template

Use this template when reporting review findings:

```markdown
# MCP Server Review: [Server Name]

**Reviewer:** [Name]
**Date:** [Date]
**Files Reviewed:** [List of files]

## Summary

| Severity | Count |
| -------- | ----- |
| CRITICAL | X     |
| HIGH     | X     |
| MEDIUM   | X     |
| LOW      | X     |

**Recommendation:** [APPROVE / APPROVE WITH CHANGES / REQUEST CHANGES / BLOCK]

## Critical Issues

### [S1] Hardcoded API Key

- **File:** src/config.ts:42
- **Code:** `const API_KEY = "sk_live_..."`
- **Fix:** Move to environment variable

## High Issues

### [A4] Missing isError Flag

- **File:** src/tools/processor.ts:128
- **Code:** Error response without isError
- **Fix:** Add `isError: true` to error responses

## Medium Issues

### [A1] Missing Tool Description

- **File:** src/index.ts:56
- **Tool:** `validate_input`
- **Fix:** Add description explaining tool purpose

## Low Issues

### [M3] TODO Comment

- **File:** src/utils/parser.ts:89
- **Comment:** `// TODO: optimize this`
- **Suggestion:** Create ticket or remove

## Checklist Results

- [x] Security: 6/7 passed
- [x] Architecture: 5/7 passed
- [ ] Error Handling: 4/6 passed
- [x] Production: 7/7 passed
```

---

## Workflow

### Step 1: Run Automated Detection

```bash
# Run all security checks
grep -rn "console\.log\|api[_-]\?key\s*[:=]" --include="*.ts" src/

# Run all architecture checks
grep -rn "name:\s*['\"]" --include="*.ts" src/ -A 5 | grep -v description
```

### Step 2: Manual Checklist Review

Walk through each section of the manual review checklist, marking items as pass/fail.

### Step 3: Code Walkthrough

1. Read each tool definition
2. Trace request handling flow
3. Verify error paths
4. Check resource and prompt definitions

### Step 4: Generate Report

Use the review report template to document findings with specific file locations and code snippets.

### Step 5: Classify and Prioritize

1. Group findings by severity
2. Identify blocking issues (CRITICAL/HIGH)
3. Suggest fixes for each issue

---

## Related Skills

- **mcp-server-writing** - Create new MCP servers
- **security-scan** - General security scanning
- **quality-check** - Code quality checks

## Resources

- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
- [MCP FAQs](https://modelcontextprotocol.info/docs/faqs/)
- See **REFERENCE.md** for complete violation catalog
- See **CHECKLISTS/** for printable audit checklists
