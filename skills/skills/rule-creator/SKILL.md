---
name: rule-creator
description: Create and manage user rules that customize AI behavior. Use this skill when users want to create new rules, update existing rules, organize rules, or need guidance on writing effective rules for their projects or personal preferences.
---

# Rule Creator

Create effective user rules that customize AI behavior for projects and personal preferences.

## What Are User Rules?

User rules are custom instructions that modify how the AI assistant behaves. They can define:

- **Coding standards** - Style, patterns, and conventions
- **Language preferences** - Response language, terminology
- **Project configuration** - Framework choices, file structure
- **Workflow guidelines** - Git, testing, documentation practices

## Rule Creation Workflow

### Step 1: Identify Rule Purpose

Ask the user:
1. What behavior do you want to modify?
2. Is this a project rule (shared) or personal preference?
3. Are there exceptions to this rule?

### Step 2: Choose Rule Category

Common categories:
- `coding-style` - Code formatting, syntax preferences
- `language` - Response language, communication style
- `project` - Framework-specific, architecture decisions
- `git` - Commit messages, branching, PR guidelines
- `naming` - Variable, function, file naming conventions
- `security` - Authentication, secrets, input validation
- `testing` - Test coverage, naming, mocking practices
- `documentation` - Comments, README, JSDoc requirements

For templates and examples, see [references/rule-patterns.md](references/rule-patterns.md).

### Step 3: Write the Rule

Follow these principles:

1. **Be specific** - Use concrete examples
2. **Be actionable** - Clear instructions, not vague guidance
3. **Include examples** - Show correct usage
4. **Define exceptions** - When the rule doesn't apply

For detailed writing guidelines, see [references/best-practices.md](references/best-practices.md).

### Step 4: Format the Rule

Use this format:

```
## [Category]: [Short Title]

[Clear instruction in imperative form]

Example:
[Code or text example showing correct usage]

Exception: [When this rule doesn't apply, if any]
```

### Step 5: Validate the Rule

Check against this list:
- [ ] Clear and unambiguous?
- [ ] Specific context defined?
- [ ] Actionable instruction?
- [ ] Example included (if complex)?
- [ ] Exceptions documented?
- [ ] No conflicts with existing rules?

## Quick Templates

### Coding Style Rule

```
## Coding: [Title]

[What to do and how to do it]

✅ Correct:
[good example]

❌ Avoid:
[bad example]
```

### Project Configuration Rule

```
## Project: [Title]

Use [technology/pattern] for [purpose].

Configuration:
[relevant settings or file structure]
```

### Workflow Rule

```
## Workflow: [Title]

[Step-by-step process or checklist]

1. [First step]
2. [Second step]
3. [Third step]
```

## Managing Rules

### Adding Rules

Create or append to the user's rules file. Group related rules under clear headers.

### Updating Rules

When updating, preserve existing rules unless explicitly asked to replace them.

### Organizing Rules

Suggest organizing rules by:
1. Priority (security > performance > style)
2. Category (coding, git, testing, etc.)
3. Scope (project-wide vs file-specific)

## Output Location

Rules must be saved in the `.agent/rules/` directory with one file per rule category:

```
.agent/rules/
├── git-commit.md          # Git commit format rules
├── coding-style.md        # Coding style rules
├── naming-conventions.md  # Naming rules
├── security.md            # Security rules
└── testing.md             # Testing rules
```

### File Naming

- Use kebab-case: `{rule-name}.md`
- Name should reflect the rule category or purpose
- Examples: `git-commit.md`, `coding-style.md`, `api-design.md`

### File Structure

Each rule file should include YAML frontmatter with activation mode, followed by the rule content:

```markdown
---
activation: always_on  # or: manual, model_decision, glob
description: Brief description for model decision mode
globs: ["*.ts", "src/**/*.tsx"]  # only for glob activation
---

# [Rule Category Title]

Brief description of what this rule covers.

## Rule 1: [Title]

[Rule content with examples]

## Rule 2: [Title]

[Rule content with examples]
```

### Activation Modes

Rules can be activated in different ways:

| Mode | Frontmatter | Description |
|------|-------------|-------------|
| **Manual** | `activation: manual` | Activated via @mention in input (e.g., `@git-commit`) |
| **Always On** | `activation: always_on` | Always applied to all conversations |
| **Model Decision** | `activation: model_decision` | Model decides based on `description` field |
| **Glob** | `activation: glob` | Applied to files matching `globs` patterns |

#### Examples

**Always On** (recommended for general rules):
```yaml
---
activation: always_on
---
```

**Manual** (for specific workflows):
```yaml
---
activation: manual
---
```

**Model Decision** (context-dependent):
```yaml
---
activation: model_decision
description: Apply when working with git commits or version control
---
```

**Glob** (file-type specific):
```yaml
---
activation: glob
globs: ["*.ts", "*.tsx", "src/**/*.js"]
---
```

### @Mentions (File References)

Reference other files in rules using `@filename`:

| Path Type | Example | Resolution |
|-----------|---------|------------|
| Relative | `@../shared/common.md` | Relative to rule file location |
| Absolute | `@/docs/api.md` | First tries true absolute path, then workspace-relative |
| Workspace | `@app/types.ts` | Relative to workspace/repository root |

#### Use Cases

**Referencing shared documentation:**
```markdown
For API conventions, see @/docs/api-guidelines.md
```

**Including type definitions:**
```markdown
All API responses must follow the types in @app/types/api.types.ts
```

**Linking related rules:**
```markdown
See also: @coding-style.md for naming conventions
```

### Creating Rules

1. Check if `.agent/rules/` directory exists, create if not
2. Check if a file for this category already exists
3. If exists: append new rules to the file
4. If not: create new file with proper structure
