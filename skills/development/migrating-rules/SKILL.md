---
name: migrating-rules
description: Helps migrate code when updating to new rule versions. Compares rule versions from the index and generates migration plans. Use when rules are updated or when migrating between framework versions.
---

<identity>
Migrating Rules - Helps migrate code when rules are updated or when switching between framework versions by comparing rule differences.
</identity>

<capabilities>
- Rules are updated to new versions
- Migrating from one framework to another (e.g., Next.js 14 → 15)
- Updating coding standards
- User asks "How do I update my code for the new rules?"
- Rule changes require code modifications
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Migration Context

Determine what needs migration:

- **Rule version update**: Same framework, updated rules
- **Framework migration**: Different framework (e.g., Pages Router → App Router)
- **Standard update**: Coding standards changed
- **Technology change**: New technology added to stack

### Step 2: Load Rule Index

Load the rule index to find relevant rules:

- @.claude/context/rule-index.json

### Step 3: Identify Source and Target Rules

Find the rules involved in migration:

- **Source rule**: Current rule being used
- **Target rule**: New rule to migrate to
- **Both rules**: If migrating between frameworks

### Step 4: Load Rule Files

Load both source and target rule files:

- Read source rule file
- Read target rule file
- Compare differences

### Step 5: Analyze Differences

Compare rules to identify:

- **Removed patterns**: What's no longer allowed
- **New patterns**: What's now required
- **Changed patterns**: What's been modified
- **Breaking changes**: Incompatible changes

See [reference/migration-patterns.md](reference/migration-patterns.md) for common migration patterns.

### Step 6: Generate Migration Plan

Create step-by-step migration plan:

- **Inventory**: List all files affected
- **Priority**: Order of migration (critical first)
- **Steps**: Specific code changes needed
- **Verification**: How to verify migration success
  </execution_process>

<best_practices>

1. **Be Comprehensive**: Identify all affected code
2. **Prioritize**: Critical changes first
3. **Show Examples**: Before/after code for each change
4. **Step-by-Step**: Break complex migrations into clear steps
5. **Verify**: Include verification steps
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Migration Plan Format**

Structure migration plan clearly:

```markdown
## Migration Plan: [Source] → [Target]

**Migration Type**: [Rule update / Framework migration / Standard update]
**Affected Files**: [count]
**Estimated Effort**: [low/medium/high]

### Overview

**Source Rule**: [rule name and path]
**Target Rule**: [rule name and path]
**Key Changes**: [summary of main differences]

### Breaking Changes

#### [Change 1]

**Impact**: [high/medium/low]
**Description**: [what changed]

**Before**:
\`\`\`[language]
[old code pattern]
\`\`\`

**After**:
\`\`\`[language]
[new code pattern]
\`\`\`

**Migration Steps**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

---

### New Requirements

#### [Requirement 1]

**Description**: [new requirement]

**Action Required**:
[What needs to be done]

**Example**:
\`\`\`[language]
[code example]
\`\`\`

---

### Deprecated Patterns

#### [Pattern 1]

**Status**: Deprecated
**Replacement**: [new pattern]

**Migration**:
\`\`\`[language]
// Old (deprecated)
[old code]

// New (recommended)
[new code]
\`\`\`

---

### Migration Checklist

- [ ] Step 1: [action]
- [ ] Step 2: [action]
- [ ] Step 3: [action]
- [ ] Verification: [how to verify]

### Verification

[How to verify migration is complete and correct]
```

</formatting_example>
</examples>

<examples>
<code_example>
**Common Migration Scenarios**:

**Next.js 14 → 15**:

- App Router changes
- React 19 features
- Server Component patterns

**Pages Router → App Router**:

- Route structure changes
- Data fetching patterns
- Layout changes

**TypeScript Strict Mode**:

- Type safety improvements
- `any` → proper types
- Null checking

**Python 3.10 → 3.12**:

- Type hint improvements
- Pattern matching
- Performance optimizations

For each scenario, see migration-patterns.md for detailed patterns.
</code_example>
</examples>
