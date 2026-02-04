---
name: render-template
description: Render templates with variable substitution using {{variable}} or ${variable} syntax. Use for generating formatted output, reports, commit messages, or any text requiring variable interpolation.
---

# Render Template

Render templates with variable substitution, supporting various syntax formats and helper functions.

## When to Use

- Format commit messages with dynamic data
- Generate report sections with variables
- Create formatted outputs from templates
- Replace placeholders in text templates
- Consolidate formatting logic across Skills

## Instructions

### Step 1: Receive Template and Data

Accept template string and variable data.

**Expected Input**:

- `template`: String (template with placeholders)
- `variables`: Object (key-value pairs for substitution)
- `syntax`: String (optional: mustache|shell|mixed, default: mustache)

**Supported Syntax**:

- **Mustache**: `{{variable}}`, `{{object.property}}`
- **Shell**: `${variable}`, `${VARIABLE}`
- **Mixed**: Supports both

### Step 2: Parse Template

Identify all placeholders in template.

**Placeholder Patterns**:

- `{{variable}}`: Simple variable
- `{{object.property}}`: Nested property
- `{{#if condition}}...{{/if}}`: Conditional (optional)
- `{{#each array}}...{{/each}}`: Loop (optional)

### Step 3: Resolve Variables

Replace placeholders with values from variables object.

**Resolution Rules**:

- Direct match: `{{name}}` → `variables.name`
- Nested property: `{{user.name}}` → `variables.user.name`
- Missing variable: Replace with empty string or keep placeholder (configurable)
- Undefined: Replace with empty string

### Step 4: Apply Filters (Optional)

Support simple filters if specified.

**Common Filters**:

- `{{variable | uppercase}}`: Convert to uppercase
- `{{variable | lowercase}}`: Convert to lowercase
- `{{variable | capitalize}}`: Capitalize first letter
- `{{date | format:YYYY-MM-DD}}`: Format date

### Step 5: Return Rendered Output

Return final rendered string.

**Expected Output**: String (template with variables replaced)

## Error Handling

- **Missing Variables**: Replace with empty string or warn (configurable)
- **Invalid Template Syntax**: Return error describing syntax issue
- **Circular References**: Detect and return error
- **Type Mismatch**: Convert to string automatically

## Examples

### Example 1: Simple Variable Substitution

**Input**:

```json
{
  "template": "Hello {{name}}, your score is {{score}}!",
  "variables": {
    "name": "Alice",
    "score": 95
  },
  "syntax": "mustache"
}
```

**Output**:

```
Hello Alice, your score is 95!
```

### Example 2: Nested Properties

**Input**:

```json
{
  "template": "User: {{user.name}} ({{user.email}})\nRole: {{user.role}}",
  "variables": {
    "user": {
      "name": "Bob",
      "email": "bob@example.com",
      "role": "admin"
    }
  }
}
```

**Output**:

```
User: Bob (bob@example.com)
Role: admin
```

### Example 3: Shell Syntax

**Input**:

```json
{
  "template": "Version: ${VERSION}\nDate: ${RELEASE_DATE}",
  "variables": {
    "VERSION": "0.8.0",
    "RELEASE_DATE": "2025-10-17"
  },
  "syntax": "shell"
}
```

**Output**:

```
Version: 0.8.0
Date: 2025-10-17
```

### Example 4: Commit Message Template

**Input**:

```json
{
  "template": "{{type}}({{scope}}): {{description}}\n\n{{body}}\n\n🤖 Generated with Claude Code\nCo-Authored-By: Claude <noreply@anthropic.com>",
  "variables": {
    "type": "feat",
    "scope": "auth",
    "description": "add OAuth2 support",
    "body": "Implemented OAuth2 flow with token refresh.\nSupports Google and GitHub providers."
  }
}
```

**Output**:

```
feat(auth): add OAuth2 support

Implemented OAuth2 flow with token refresh.
Supports Google and GitHub providers.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 5: Missing Variables

**Input**:

```json
{
  "template": "Name: {{name}}\nAge: {{age}}\nCity: {{city}}",
  "variables": {
    "name": "Alice"
  }
}
```

**Output (with empty string replacement)**:

```
Name: Alice
Age:
City:
```

**Output (with keep placeholder)**:

```
Name: Alice
Age: {{age}}
City: {{city}}
```

### Example 6: Report Header Template

**Input**:

```json
{
  "template": "# {{reportType}} Report: {{version}}\n\n**Generated**: {{timestamp}}\n**Status**: {{statusEmoji}} {{status}}\n**Version**: {{version}}",
  "variables": {
    "reportType": "Bug Hunting",
    "version": "2025-10-17",
    "timestamp": "2025-10-17 14:30:00 UTC",
    "statusEmoji": "✅",
    "status": "success"
  }
}
```

**Output**:

```markdown
# Bug Hunting Report: 2025-10-17

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ✅ success
**Version**: 2025-10-17
```

## Validation

- [ ] Replaces simple variables correctly
- [ ] Handles nested properties
- [ ] Supports multiple syntax formats
- [ ] Handles missing variables gracefully
- [ ] Converts types to strings
- [ ] Preserves formatting (line breaks, indentation)
- [ ] Detects circular references
- [ ] Returns clear error messages

## Supporting Files

None required - pure template rendering logic.

## Integration with Other Skills

This Skill consolidates formatting logic used by:

- **format-commit-message**: Use render-template for message formatting
- **generate-report-header**: Use render-template for header generation
- **format-todo-list**: Use render-template for activeForm generation
- **generate-changelog**: Use render-template for section formatting

**Example Integration**:

```
Instead of: Hard-coded string formatting in each Skill
Use: render-template Skill with predefined templates
Result: Consistent formatting, easier to maintain
```
