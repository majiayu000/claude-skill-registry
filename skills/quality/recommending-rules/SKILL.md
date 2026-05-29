---
name: recommending-rules
description: Analyzes codebase to find gaps in rule coverage and suggests rule improvements. Compares codebase against all indexed rules to identify missing standards. Use when setting up new projects or reviewing rule coverage.
---

<identity>
Recommending Rules - Analyzes codebase to identify gaps in rule coverage by comparing against all indexed rules.
</identity>

<capabilities>
- Setting up a new project
- Reviewing rule coverage for existing project
- User asks "What rules should I use?"
- Identifying missing standards
- Project uses technologies without corresponding rules
</capabilities>

<instructions>
<execution_process>

### Step 1: Load Rule Index

Load the complete rule index:

- @.claude/context/rule-index.json

This contains all 1,081+ available rules.

### Step 2: Analyze Codebase

Scan the codebase to identify technologies used:

- **File extensions**: `.tsx`, `.py`, `.sol`, etc.
- **Package files**: `package.json`, `requirements.txt`, `Cargo.toml`
- **Framework files**: `next.config.js`, `fastapi` imports, etc.
- **Directory structure**: `app/`, `components/`, `routers/`, etc.

See [reference/coverage-analysis.md](reference/coverage-analysis.md) for detailed analysis patterns.

### Step 3: Identify Technologies

Extract technologies from codebase:

- Primary languages (TypeScript, Python, etc.)
- Frameworks (Next.js, FastAPI, etc.)
- Testing tools (Cypress, Playwright, Jest, etc.)
- Build tools (Docker, Kubernetes, etc.)

### Step 4: Query Rule Index

For each detected technology, query the index:

- Use `technology_map` to find all rules for each technology
- Collect all potentially relevant rules
- Remove duplicates

### Step 5: Compare with Active Rules

Check which rules are currently active:

- Check `.claude/rules/manifest.yaml` for loaded rules
- Check `.claude/config.yaml` for agent-specific rules
- Identify which indexed rules are NOT currently loaded

### Step 6: Generate Recommendations

For each missing rule, provide:

- **Rule name and description**: From index metadata
- **Why it's relevant**: Connection to codebase technologies
- **Priority**: High/Medium/Low based on codebase usage
- **How to activate**: Instructions for loading the rule
  </execution_process>

<best_practices>

1. **Be Specific**: Explain why each rule is relevant
2. **Prioritize**: High priority for core technologies, low for edge cases
3. **Provide Context**: Show how rule connects to codebase
4. **Actionable**: Include clear activation instructions
5. **Comprehensive**: Check all technologies, not just obvious ones
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Output Format**

Structure recommendations clearly:

```markdown
## Rule Coverage Analysis

**Codebase Technologies**: [list]
**Currently Active Rules**: [count]
**Recommended Rules**: [count]

### High Priority Recommendations

#### [Rule Name]

**Path**: [path from index]
**Type**: [master/archive]
**Relevance**: [why it applies]
**Priority**: High

**Description**: [from index metadata]

**Why You Need This**:
[Explanation of why this rule is important for your codebase]

**How to Activate**:
[Instructions for loading the rule]

---

### Medium Priority Recommendations

[Similar structure]

---

### Low Priority Recommendations

[Similar structure]

### Summary

- **Total rules available**: [count]
- **Rules currently active**: [count]
- **Rules recommended**: [count]
- **Coverage gap**: [percentage]
```

</formatting_example>
</examples>

<examples>
<code_example>
**Recommendation Criteria**:

**High Priority**:

- Core framework rules (Next.js, React, TypeScript for TS projects)
- Universal standards (PROTOCOL_ENGINEERING)
- Testing rules matching test framework used
- Security rules for production code

**Medium Priority**:

- Framework-specific optimizations
- Code style rules for secondary languages
- Tool-specific rules (Docker, CI/CD)

**Low Priority**:

- Niche technology rules
- Deprecated framework rules
- Rules for unused features
  </code_example>
  </examples>
