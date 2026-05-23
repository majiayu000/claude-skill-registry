---
name: rule-auditor
description: Validates code against coding standards and best practices. Reports compliance violations and suggests fixes.
version: 2.0
model: haiku
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Run audits early in development cycle
  - Focus on high-severity violations first
  - Provide specific, actionable fixes
  - Group violations by category
error_handling: graceful
streaming: supported
---

# Rule Auditor Skill

<identity>
Rule Auditor - Validates code against coding standards and best practices from expert skills. Reports compliance violations and suggests fixes.
</identity>

<capabilities>
- Auditing code against best practices
- Identifying violations and anti-patterns
- Suggesting fixes for violations
- Generating compliance reports
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Applicable Skills

Find relevant expert skills based on the code being audited:

| File Type     | Expert Skills                   |
| ------------- | ------------------------------- |
| `.ts`, `.tsx` | typescript-expert, react-expert |
| `.py`         | python-backend-expert           |
| `.go`         | go-expert                       |
| `.java`       | java-expert                     |
| `*.test.*`    | testing-expert                  |

### Step 2: Load Best Practices

Read the relevant skill files to understand best practices:

```bash
cat .claude/skills/[skill-name]/SKILL.md
```

Extract key rules and patterns to check for.

### Step 3: Scan Target Files

Analyze the target files for violations:

1. **Read target files**: Use Read tool to examine code
2. **Check patterns**: Look for anti-patterns from skill guidelines
3. **Identify issues**: Note file, line, and violation type

Common checks:

- Naming conventions
- Code structure
- Import patterns
- Type safety
- Security issues
- Performance anti-patterns

### Step 4: Generate Report

Create a structured compliance report:

```markdown
## Audit Report

**Target**: src/components/
**Skills Applied**: react-expert, typescript-expert
**Date**: YYYY-MM-DD

### Summary

- **Pass**: 12 rules
- **Warn**: 3 rules
- **Fail**: 2 rules

### Violations

#### FAIL: Avoid using `any` type

- **File**: src/components/UserAuth.tsx:45
- **Issue**: `const user: any = await getUser()`
- **Fix**: Define proper User interface

#### WARN: Use Server Components by default

- **File**: src/components/UserAuth.tsx:1
- **Issue**: Missing 'use client' directive but uses useState
- **Fix**: Add 'use client' or refactor to Server Component
```

</execution_process>

<best_practices>

1. **Run Early**: Audit during development, not just before commit
2. **Prioritize**: Focus on high-severity violations first
3. **Be Specific**: Include file paths and line numbers
4. **Suggest Fixes**: Provide actionable remediation steps
5. **Group Issues**: Organize by severity and category

</best_practices>
</instructions>

<examples>
<usage_example>
**Audit Request**:

```
Audit src/components/ for TypeScript and React best practices
```

**Response**:

```markdown
## Audit Report: src/components/

### Violations Found

1. **[ERROR]** src/components/User.tsx:23
   - Rule: Avoid `any` type
   - Code: `const data: any = response.json()`
   - Fix: `const data: UserResponse = response.json()`

2. **[WARN]** src/components/Form.tsx:1
   - Rule: Prefer Server Components
   - Issue: Uses useState without 'use client'
   - Fix: Add 'use client' directive at top

### Passed Checks

- Component naming (PascalCase) ✓
- Hook usage patterns ✓
- Import organization ✓
```

</usage_example>
</examples>

## Rules

- Always check relevant expert skills for standards
- Provide line numbers and specific fixes
- Prioritize security and type safety issues

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
