---
name: skill-creator
description: Creates new Claude Code skills following repository conventions with proper structure, frontmatter, workflows, code examples, and reference files. Use when users request "create a skill", "new skill", "generate skill", or "add skill to collection".
---

# Skill Creator

Generate production-ready Claude Code skills following established conventions.

## Core Workflow

1. **Define skill purpose**: Clear name, description, and use cases
2. **Determine category**: Place in correct folder (foundation, frontend, backend, etc.)
3. **Create SKILL.md**: Main skill file with frontmatter and content
4. **Add references**: Optional templates.md, conventions.md, or patterns.md
5. **Include examples**: Production-ready code samples
6. **Write checklist**: Output verification checklist

## Skill Categories

| Category       | Path                   | Purpose                                   |
| -------------- | ---------------------- | ----------------------------------------- |
| Foundation     | `foundation/`          | Project setup, dev environment, git, docs |
| Frontend       | `frontend/`            | React, Vue, UI components, styling, UX    |
| Backend        | `backend/`             | APIs, auth, server logic, services        |
| AI Engineering | `ai-engineering/`      | LLMs, RAG, agents, prompts                |
| Architecture   | `architecture/`        | System design, ADRs, tech decisions       |
| CI/CD          | `ci-cd/`               | Automation, deployments, pipelines        |
| Database       | `database-management/` | Migrations, queries, data engineering     |
| Testing        | `testing/`             | Unit tests, integration, e2e, mocks       |
| Security       | `security/`            | Vulnerabilities, auth, hardening          |
| Performance    | `performance/`         | Observability, monitoring, optimization   |

## SKILL.md Template

```markdown
---
name: skill-name-in-kebab-case
description: One-line description of what the skill does and when to use it. Include trigger phrases like "use when users request X, Y, or Z".
---

# Skill Title

Brief tagline explaining the skill's value proposition.

## Core Workflow

1. **Step one**: Description
2. **Step two**: Description
3. **Step three**: Description
   ...

## [Main Content Sections]

### Section with Code Examples

\`\`\`typescript
// Production-ready code example
\`\`\`

### Patterns / Templates

Document reusable patterns with examples.

## Best Practices

- Practice one
- Practice two
- Practice three

## Output Checklist

Every output should include:

- [ ] Item one
- [ ] Item two
- [ ] Item three
```

## Reference Files Structure

When skills need supplementary documentation:

```
skill-name/
├── SKILL.md              # Main skill file (required)
└── references/            # Optional reference materials
    ├── templates.md       # Code/file templates
    ├── conventions.md     # Standards and conventions
    └── patterns.md        # Reusable patterns
```

## Frontmatter Requirements

```yaml
---
name: kebab-case-skill-name # Must match folder name
description: >
  Clear description including:
  - What the skill does
  - When to use it
  - Trigger phrases ("use when X", "create Y", "generate Z")
---
```

## Content Guidelines

### Code Examples

- Must be production-ready, not pseudocode
- Include TypeScript types where applicable
- Show complete, working examples
- Use modern syntax and best practices

### Sections to Include

1. **Core Workflow**: Numbered steps for using the skill
2. **Main Content**: Patterns, templates, examples
3. **Best Practices**: Industry-proven recommendations
4. **Output Checklist**: Verification items

### Writing Style

- Active voice, imperative mood
- Concise, scannable formatting
- Tables for structured comparisons
- Code blocks for all technical content

## Skill Quality Criteria

### Completeness

- [ ] Solves a specific, well-defined problem
- [ ] Includes working code examples
- [ ] Has clear trigger phrases in description
- [ ] Provides output verification checklist

### Consistency

- [ ] Follows naming conventions (kebab-case)
- [ ] Uses standard section headings
- [ ] Matches existing skill format
- [ ] Placed in correct category folder

### Usefulness

- [ ] Examples are copy-paste ready
- [ ] Covers common use cases
- [ ] Anticipates edge cases
- [ ] References external docs where helpful

## Example: Creating a New Skill

### Step 1: Define the Skill

```
Name: api-rate-limiter
Category: backend
Purpose: Implement rate limiting for APIs
Triggers: "add rate limiting", "protect API", "throttle requests"
```

### Step 2: Create Folder Structure

```bash
mkdir -p backend/api-rate-limiter
touch "backend/api-rate-limiter/SKILL.md"
```

### Step 3: Write SKILL.md

```markdown
---
name: api-rate-limiter
description: Implements rate limiting for APIs using token bucket, sliding window, or fixed window algorithms. Use when users request "add rate limiting", "protect API from abuse", or "throttle requests".
---

# API Rate Limiter

Protect your APIs from abuse with production-ready rate limiting.

## Core Workflow

...
```

### Step 4: Add References (if needed)

```bash
mkdir -p backend/api-rate-limiter/references
touch backend/api-rate-limiter/references/algorithms.md
```

## Output Checklist

When creating a new skill:

- [ ] Skill name is kebab-case
- [ ] Description includes trigger phrases
- [ ] Placed in correct category folder
- [ ] SKILL.md follows template structure
- [ ] Code examples are production-ready
- [ ] Includes Core Workflow section
- [ ] Has Output Checklist section
- [ ] Reference files added if needed
