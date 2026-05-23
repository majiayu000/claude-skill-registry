---
name: fixing-rule-violations
description: Provides detailed fix instructions for coding rule violations. Uses the rule index to locate violated rules and extract fix patterns. Use when code violates rules or when the user asks how to fix compliance issues.
---

<identity>
Fixing Rule Violations - Provides actionable fix instructions for rule violations by locating violated rules in the index and extracting fix patterns.
</identity>

<capabilities>
- Code violates a specific rule
- User reports a compliance issue
- Rule auditor identifies violations
- User asks "How do I fix this rule violation?"
- Code review finds standards violations
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify the Violation

Determine what rule was violated:

- **From rule-auditor**: Violation report with rule name/path
- **From user**: Description of the issue
- **From code**: Analyze code to identify which rule applies

### Step 2: Load Rule Index

Load the rule index to locate the violated rule:

- @.claude/context/rule-index.json

### Step 3: Find Violated Rule

Search the index for the violated rule:

- **By name**: Search `rules` array for matching name
- **By path**: If path is known, find rule with matching path
- **By technology**: Query `technology_map` if rule type is known

### Step 4: Load Rule File

Load the full rule file to get fix instructions:

- Read the rule file from the path in the index
- Extract sections related to the violation
- Find fix patterns and examples

### Step 5: Extract Fix Instructions

From the rule file, extract:

- **What's wrong**: The violation pattern
- **Why it's wrong**: Explanation from the rule
- **How to fix**: Specific fix instructions
- **Example**: Before/after code examples

See [reference/fix-patterns.md](reference/fix-patterns.md) for common fix patterns.

### Step 6: Generate Fix Instructions

Provide actionable fix with:

- **Exact code changes**: Show before/after
- **Step-by-step**: Break down complex fixes
- **Context**: Explain why the fix works
- **Verification**: How to verify the fix
  </execution_process>

<best_practices>

1. **Be Specific**: Provide exact code changes, not vague suggestions
2. **Show Examples**: Always include before/after code
3. **Explain Why**: Help user understand the fix
4. **Step-by-Step**: Break complex fixes into clear steps
5. **Verify**: Include verification steps
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Output Format**

Structure fix instructions clearly:

```markdown
## Fix for [Rule Name] Violation

**Violated Rule**: [rule name]
**Rule Path**: [path from index]
**Violation Location**: [file:line]

### The Problem

[Description of what's wrong]

### Why This Violates the Rule

[Explanation from rule file]

### How to Fix

**Step 1**: [Action]
\`\`\`[language]
[Code showing fix]
\`\`\`

**Step 2**: [Action]
\`\`\`[language]
[Code showing fix]
\`\`\`

### Before and After

**Before** (violates rule):
\`\`\`[language]
[violating code]
\`\`\`

**After** (compliant):
\`\`\`[language]
[fixed code]
\`\`\`

### Verification

[How to verify the fix works]
```

</formatting_example>
</examples>

<examples>
<code_example>
**Common Violation Types**:

**TypeScript Violations**:

- Using `any` instead of proper types
- Missing type annotations
- Incorrect interface definitions

**React/Next.js Violations**:

- Missing 'use client' directive
- Using useEffect for data fetching
- Not using Server Components when possible

**Python Violations**:

- Missing type hints
- Not using async/await properly
- Incorrect error handling

**Code Quality Violations**:

- Magic numbers
- Unclear variable names
- Missing error handling

For each type, see fix-patterns.md for standard fixes.
</code_example>
</examples>
