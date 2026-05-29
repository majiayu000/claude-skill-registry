---
name: explaining-rules
description: Explains which coding rules apply to files and why they matter. Uses the rule index to discover all available rules dynamically. Use when the user asks about rules, coding standards, or best practices.
---

<identity>
Explaining Rules - Explains applicable coding rules by querying the rule index dynamically. Discovers all 1,081+ rules without hard-coding.
</identity>

<capabilities>
- User asks "What rules apply to this file?"
- Explaining coding standards to team members
- Onboarding new developers
- Understanding rule coverage for a project
- Reviewing which rules are active
</capabilities>

<instructions>
<execution_process>

### Step 1: Load Rule Index

Load the complete rule index to discover all available rules:

- @.claude/context/rule-index.json

The index contains metadata for all rules in `.claude/rules-master/` and `.claude/archive/`.

**Note**: If the index is empty or missing, it needs to be generated first:

- Run `pnpm index-rules` or `node scripts/generate-rule-index.mjs`
- This scans all rules and creates the index file

### Step 2: Analyze Target File or Query

Determine what needs explanation:

- **File path**: Analyze file extension, imports, and directory structure
- **Technology stack**: User mentions specific technologies
- **General query**: User asks about rules in general

### Step 3: Detect Technologies

For file-based queries, detect technologies using:

- File extension (`.tsx` → TypeScript, React)
- Import statements (`next` → Next.js, `react` → React)
- Directory structure (`app/` → Next.js App Router)
- Framework-specific patterns

See [reference/technology-detection.md](reference/technology-detection.md) for detailed detection patterns.

### Step 4: Query Rule Index

Use the index's `technology_map` to find relevant rules:

```javascript
// Pseudocode
const detectedTech = ['nextjs', 'react', 'typescript'];
const relevantRules = [];

detectedTech.forEach(tech => {
  const rules = index.technology_map[tech] || [];
  relevantRules.push(...rules);
});

// Remove duplicates
const uniqueRules = [...new Set(relevantRules)];
```

### Step 5: Load Relevant Rules

Load only the relevant rule files (progressive disclosure):

- Master rules take priority (from `.claude/rules-master/`)
- Archive rules supplement (from `.claude/archive/`)
- Load 5-10 most relevant rules, not all 1,081

### Step 6: Explain Rules

For each relevant rule, explain:

- **What it covers**: Main purpose and scope
- **Why it applies**: Connection to the file/query
- **Key requirements**: Most important standards
- **Examples**: Code examples showing compliance

Use the template in [reference/rule-explanation-template.md](reference/rule-explanation-template.md) for consistent output.
</execution_process>

<best_practices>

1. **Be Specific**: Explain why each rule applies, not just what it says
2. **Prioritize**: Master rules first, then archive rules
3. **Use Examples**: Show code examples from the rule files
4. **Progressive Disclosure**: Load only relevant rules, not all 1,081
5. **Context-Aware**: Adapt explanation to user's experience level
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Output Format**

Structure explanations clearly:

```markdown
## Rules Applicable to [file/query]

**Technologies Detected**: [list]

### Master Rules (Always Active)

- **[Rule Name]**: [brief description]
  - **Applies because**: [reason]
  - **Key requirements**: [list]
  - **Example**: [code snippet]

### Archive Rules (On-Demand)

- **[Rule Name]**: [brief description]
  - **When to use**: [context]
  - **Key points**: [list]
```

</formatting_example>
</examples>
