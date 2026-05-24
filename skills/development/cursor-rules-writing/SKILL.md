---
name: cursor-rules-writing
description: Create Cursor IDE rules in .mdc format with proper frontmatter, glob patterns, and cross-references. Covers rule structure, file organization, triggering mechanisms, and quality standards. Use when creating or modifying Cursor rules for context injection.
version: 1.0.0
---

# Cursor Rules Writing

## Purpose
Guide the creation of Cursor IDE rules in .mdc format following best practices for optimal AI context injection and maintainability.

## When NOT to Use This Skill
- Writing general documentation (use regular .md files)
- Creating Claude Code skills (use skill-writing skill instead)
- Configuring Cursor IDE settings (not rules)
- Writing code comments or inline documentation

## Quick Start Workflow

### Step 1: Identify the Context Need
**Ask:** What specific knowledge does Cursor need for this project?

```bash
# Evaluate the gap:
# - What domain knowledge is unique to this project?
# - Which files/patterns need special context?
# - What are developers repeatedly explaining to Cursor?
```

**Only create a rule if:**
- ✅ Context is project-specific and non-obvious
- ✅ Applies to multiple files or scenarios
- ✅ Reduces repetitive prompting
- ❌ General programming knowledge (Cursor already knows)
- ❌ One-time context (use chat instead)

### Step 2: Choose Rule Type and Trigger
**Determine how rule should be applied:**

```yaml
# Always Apply (use sparingly)
alwaysApply: true          # Loaded in every chat session

# File-based triggering (most common)
globs: ["**/*.yaml"]       # Applies when matching files are referenced
alwaysApply: false

# Manual application
# No globs, no alwaysApply  # User invokes with @rule-name.mdc
```

### Step 3: Create MDC File with Frontmatter
```bash
# Create rule file in .cursor/rules/ directory
touch .cursor/rules/my-rule.mdc
```

**Start with frontmatter template:**

```yaml
---
description: Brief description of what this rule provides. Include what context it covers and when it applies. Keep under 200 characters for clarity.
globs: ["**/*.ts", "**/*.tsx"]  # Optional: file patterns
alwaysApply: false              # Optional: default false
---
```

### Step 4: Write Focused Content
**Keep under 500 lines for optimal performance**

```markdown
# Rule Title

## Overview
One paragraph explaining what context this rule provides.

**Related rules:** See @other-rule.mdc for related context.

---

## Key Concepts
Core information Cursor needs to know.

---

## Examples
Concrete examples with ✅/❌ patterns.

---

## Resources
Links to relevant documentation.
```

### Step 5: Test and Refine
```bash
# Test rule application:
# 1. Open file matching glob pattern
# 2. Start Cursor chat
# 3. Verify rule context is loaded
# 4. Check @-mentions work correctly
```

## MDC File Format

### Frontmatter Structure
**YAML frontmatter with 3 possible fields:**

```yaml
---
description: Clear, concise description of rule context and when to apply it.
globs: ["pattern1", "pattern2"]  # Optional: array of glob patterns
alwaysApply: false               # Optional: boolean (default: false)
---
```

**Field Descriptions:**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `description` | Yes | String | Used by Agent to determine relevance. Be specific about what context is provided and when to use the rule. |
| `globs` | No | Array | File patterns for automatic rule application. Omit for manual-only rules. |
| `alwaysApply` | No | Boolean | If true, rule loads in every chat. Use sparingly - causes context bloat. |

**Frontmatter Rules:**
- ✅ Description must be clear and specific
- ✅ Use globs for file-based triggering
- ✅ Avoid alwaysApply unless truly universal
- ❌ Don't include title/name field (file name is the identifier)
- ❌ Don't use first or second person in description

### Good vs Bad Frontmatter

```yaml
# ❌ Bad - Vague description, no trigger info
---
description: Helper for working with files.
alwaysApply: true
---

# ❌ Bad - Too broad, will cause context pollution
---
description: Contains all project documentation and guidelines.
alwaysApply: true
---

# ✅ Good - Specific, clear when to apply
---
description: Core guidance for writing production-ready Helm charts including Chart.yaml structure, values.yaml patterns, and template helpers. Apply when creating or modifying Helm chart files.
globs: ["**/Chart.yaml", "**/values*.yaml", "**/templates/**/*.yaml"]
alwaysApply: false
---

# ✅ Good - Manual-only rule, no triggers
---
description: Advanced debugging techniques for React rendering performance issues. Use when diagnosing slow re-renders or unnecessary updates.
---
```

## Glob Patterns

### Pattern Syntax
**Cursor uses standard glob patterns:**

```yaml
globs:
  - "*.ts"                    # All .ts files in any directory
  - "**/*.tsx"                # All .tsx files recursively
  - "**/tests/**/*"           # All files in tests directories
  - "src/components/*.tsx"    # .tsx files in specific directory
  - "**/{Chart,values}.yaml"  # Multiple specific filenames
```

**Pattern Matching:**
- `*` - Matches any characters except `/`
- `**` - Matches any characters including `/` (recursive)
- `?` - Matches single character
- `[abc]` - Matches a, b, or c
- `{a,b}` - Matches pattern a or pattern b

### Effective Glob Patterns

```yaml
# ✅ Good - Specific to chart files
globs: ["**/Chart.yaml", "**/values*.yaml", "**/templates/**/*.yaml"]

# ✅ Good - TypeScript components
globs: ["**/components/**/*.tsx", "**/hooks/**/*.ts"]

# ✅ Good - Configuration files
globs: ["**/*.config.{js,ts}", "**/.*rc", "**/.*rc.json"]

# ❌ Too broad - matches everything
globs: ["**/*"]

# ❌ Too narrow - misses common cases
globs: ["Chart.yaml"]  # Only root, misses nested charts
```

### Testing Glob Patterns

```bash
# Use shell glob expansion to test patterns
echo .cursor/rules/*.mdc

# Find files matching pattern
find . -path "**/Chart.yaml"

# Test specific pattern
ls **/values*.yaml
```

## Cross-References

### Referencing Other Rules
**Use `@filename.mdc` syntax to reference related rules:**

```markdown
**Related rules:** See @helm-chart-writing.mdc for chart creation, @helm-chart-review.mdc for quality checks, @helm-argocd-gitops.mdc for GitOps integration.
```

**Cross-reference benefits:**
- ✅ Keeps rules focused and modular
- ✅ Allows rule composition
- ✅ Reduces duplication
- ✅ User can manually load related context

**Best practices:**
- Reference related rules at the top (Overview section)
- Use descriptive text: "See @X for Y" not just "@X"
- Don't create circular references
- Test that referenced rules exist

## Content Organization

### Structure Pattern
```markdown
---
# Frontmatter
---

# Rule Title

## Overview
Brief introduction paragraph.

**Related rules:** Cross-references here.

---

## Section 1: Core Concepts
Main content with examples.

---

## Section 2: Patterns
Common patterns and anti-patterns.

---

## Resources
External links and documentation.

---

**Maintenance note at bottom**
```

### Section Guidelines

**Overview (Required):**
- 1-2 sentences explaining rule purpose
- Cross-references to related rules
- Sets expectations for what follows

**Core Content (Required):**
- Organized into logical sections
- Use `---` to separate major sections
- Include concrete examples
- Show good vs bad patterns (✅/❌)

**Examples (Highly Recommended):**
- Real-world, project-specific examples
- Before/after comparisons
- Common mistakes to avoid

**Resources (Optional):**
- Links to official documentation
- Internal wiki pages
- Related project files

### Content Best Practices

```markdown
# ✅ Good - Concrete examples
## API Error Handling

All API routes must handle errors consistently:

\`\`\`typescript
// ✅ Good - Proper error handling
app.get('/api/users', async (req, res) => {
  try {
    const users = await db.users.findAll();
    res.json({ data: users });
  } catch (error) {
    logger.error('Failed to fetch users', { error });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ❌ Bad - No error handling
app.get('/api/users', async (req, res) => {
  const users = await db.users.findAll();
  res.json(users);
});
\`\`\`

# ❌ Bad - Vague instructions
## Error Handling
Make sure to handle errors properly in your code. Always catch exceptions and return appropriate status codes.
```

## File Length Management

### 500-Line Target
**Keep rules under 500 lines for optimal performance:**

```
Rule Size Guide:
├─ Under 300 lines: Ideal (fast loading)
├─ 300-500 lines: Good (acceptable)
├─ 500-700 lines: Consider splitting
└─ Over 700 lines: Must split into multiple rules
```

### Splitting Strategies

**Option 1: By topic**
```
helm-expert-skill.mdc (overview, always loaded)
├─ @helm-chart-writing.mdc (creation patterns)
├─ @helm-chart-review.mdc (quality checks)
├─ @helm-argocd-gitops.mdc (GitOps patterns)
└─ @helm-production-patterns.mdc (deployment strategies)
```

**Option 2: By file type**
```
typescript-patterns.mdc
├─ globs: ["**/*.ts"]
├─ Content: General TypeScript patterns

react-components.mdc
├─ globs: ["**/*.tsx"]
├─ Content: React-specific patterns
```

**Option 3: By scenario**
```
database-migrations.mdc
├─ globs: ["**/migrations/**/*"]
├─ Content: Migration patterns

api-testing.mdc
├─ globs: ["**/tests/api/**/*"]
├─ Content: API test patterns
```

## Triggering Mechanisms

### Always Apply Rules
```yaml
---
description: Project architecture and core patterns used across all code.
alwaysApply: true
---
```

**Use when:**
- Universal context needed in every chat
- Core architecture principles
- Project-wide conventions

**Avoid when:**
- Context is file-specific
- Only needed occasionally
- Rule is large (causes bloat)

### File-Based Triggering
```yaml
---
description: Helm chart best practices for Chart.yaml and values.yaml.
globs: ["**/Chart.yaml", "**/values*.yaml"]
alwaysApply: false
---
```

**Use when (most common):**
- Context applies to specific file types
- Patterns for certain directories
- Language/framework-specific guidance

### Manual Application
```yaml
---
description: Advanced performance optimization techniques. Use when debugging performance issues.
---
```

**Use when:**
- Context only needed on-demand
- Specialized troubleshooting
- Reference documentation
- Rarely needed context

## Common Pitfalls

### Pitfall 1: Overly Broad Rules
```yaml
# ❌ Bad - Too much context loaded always
---
description: Everything about the project including architecture, patterns, deployment, testing, and documentation.
alwaysApply: true
---
```

**Solution:** Split into focused rules with specific globs.

### Pitfall 2: Missing Glob Patterns
```yaml
# ❌ Bad - Only matches root Chart.yaml
---
globs: ["Chart.yaml"]
---
```

**Solution:** Use recursive patterns: `["**/Chart.yaml"]`

### Pitfall 3: Duplicate Context
```yaml
# ❌ Bad - Same content in multiple rules
# both-rules.mdc and api-patterns.mdc contain identical API guidelines
```

**Solution:** Single source of truth, cross-reference with @.

### Pitfall 4: Vague Descriptions
```yaml
# ❌ Bad
description: Helper for working with files.

# ✅ Good
description: File upload validation patterns including size limits, type checking, and virus scanning. Apply when implementing file upload endpoints.
```

### Pitfall 5: Too Long
```markdown
# ❌ Bad - 1200 line rule file
# Single file with all project context
```

**Solution:** Split into multiple composable rules under 500 lines each.

## Quality Checklist

### Frontmatter Quality
- [ ] Description is clear and specific
- [ ] Description explains WHAT context is provided
- [ ] Description explains WHEN to apply the rule
- [ ] Globs use recursive patterns (**/) where appropriate
- [ ] alwaysApply is false unless truly universal
- [ ] No unnecessary frontmatter fields

### Content Quality
- [ ] Under 500 lines (or justified if longer)
- [ ] Organized into logical sections with `---` separators
- [ ] Includes concrete, project-specific examples
- [ ] Shows good vs bad patterns (✅/❌)
- [ ] Cross-references related rules with @filename.mdc
- [ ] No duplicate content from other rules
- [ ] Examples use real project code patterns

### File Organization
- [ ] File stored in .cursor/rules/ directory
- [ ] Filename is descriptive and kebab-case
- [ ] Filename ends with .mdc extension
- [ ] Overview section at top
- [ ] Related rules referenced early
- [ ] Resources section at bottom

### Testing
- [ ] Rule loads when expected (check glob patterns)
- [ ] @-mention works in chat
- [ ] No conflicts with other rules
- [ ] Context is relevant and helpful
- [ ] File size is reasonable (<500 lines ideal)

## Resources

- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Glob Pattern Documentation](https://en.wikipedia.org/wiki/Glob_(programming))
- skill-writing skill (for Claude Code skills, not Cursor rules)

## Quick Reference

```bash
# Create new rule
mkdir -p .cursor/rules
touch .cursor/rules/my-rule.mdc

# Rule template
cat > .cursor/rules/my-rule.mdc << 'EOF'
---
description: Brief description of what this rule provides and when to use it.
globs: ["**/*.ext"]
alwaysApply: false
---

# Rule Title

## Overview
Brief introduction.

**Related rules:** See @other-rule.mdc for related context.

---

## Key Content

Concrete examples and patterns.

---

## Resources

- [Link to docs](https://example.com)
EOF

# Test glob pattern
find . -path "**/Chart.yaml"

# List all rules
ls -la .cursor/rules/*.mdc
```

---

**This skill follows the skill-writing meta skill best practices and should be reviewed quarterly for updates.**
