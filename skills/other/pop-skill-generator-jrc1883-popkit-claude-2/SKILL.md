---
name: skill-generator
description: "Use when you want to capture project-specific patterns as reusable skills - generates custom skills based on codebase patterns, common workflows, and team conventions discovered during analysis. Creates skills for patterns, testing, deployment, debugging, and setup. Do NOT use for generic skills that would work across any project - those belong in popkit core, not project-specific generation."
---

# Skill Generator

## Overview

Create custom skills tailored to the specific project's patterns, workflows, and conventions. Skills become part of the project's .claude/skills/ directory.

**Core principle:** Capture project wisdom as reusable, teachable skills.

**Trigger:** `/popkit:project skills` command after project analysis

## Arguments

| Flag                 | Description                                                      |
| -------------------- | ---------------------------------------------------------------- |
| `--from-analysis`    | Use `.claude/analysis.json` for pattern-based generation         |
| `--patterns-only`    | Only generate skills for detected patterns (skip generic skills) |
| `--min-confidence N` | Minimum pattern confidence threshold (default: 0.6)              |
| `--no-embed`         | Skip auto-embedding of generated skills                          |

## Analysis-Driven Generation

When `.claude/analysis.json` exists (from `/popkit:project analyze --json`), the generator uses structured pattern data:

### Step 0: Check for Analysis

```python
import json
from pathlib import Path

analysis_path = Path.cwd() / ".claude" / "analysis.json"
if analysis_path.exists():
    analysis = json.loads(analysis_path.read_text())
    patterns = analysis.get("patterns", [])
    recommended_skills = analysis.get("recommended_skills", [])
    frameworks = analysis.get("frameworks", [])
else:
    # Fall back to manual discovery
    patterns = []
    recommended_skills = []
```

### Pattern-to-Skill Mapping

When analysis is available, generate skills based on detected patterns:

| Pattern                                  | Confidence | Generated Skill                                    |
| ---------------------------------------- | ---------- | -------------------------------------------------- |
| `nextjs` + `vercel-config`               | >= 0.6     | `project:deploy` - Vercel deployment               |
| `prisma` OR `drizzle`                    | >= 0.6     | `project:db-migrate` - Database migrations         |
| `supabase`                               | >= 0.6     | `project:supabase-sync` - Supabase operations      |
| `feature-flags`                          | >= 0.6     | `project:feature-toggle` - Feature flag management |
| `docker-compose`                         | >= 0.6     | `project:docker-dev` - Docker development          |
| `redux` OR `zustand`                     | >= 0.6     | `project:state-patterns` - State management        |
| `react-query`                            | >= 0.6     | `project:data-fetching` - Server state             |
| `colocated-tests`                        | >= 0.6     | `project:testing` - Test conventions               |
| `atomic-design`                          | >= 0.6     | `project:components` - Component patterns          |
| `express-routes` OR `controller-pattern` | >= 0.6     | `project:api-patterns` - API conventions           |

### Generated Skill Format

Skills generated from analysis include detection context:

```markdown
---
name: project:deploy
description: "Deploy to Vercel with preview and production environments. Detected from Next.js + Vercel configuration (confidence: 0.92)."
---

# Deploy to Vercel

Automates deployment workflow for this project.

## Detected From

- Pattern: `nextjs` (confidence: 0.95)
- Pattern: `vercel-config` (confidence: 0.90)
- Files: `vercel.json`, `next.config.js`

## Process

1. Run type check and lint
2. Run tests
3. Deploy to preview (PR) or production (main)
   ...
```

### Auto-Embedding After Generation

After writing each SKILL.md, automatically embed for semantic discovery:

```python
import sys
# No longer needed - install popkit-shared instead
from embedding_project import auto_embed_item

# After writing skill file
skill_path = ".claude/skills/project-deploy/SKILL.md"
success = auto_embed_item(skill_path, "project-skill")

if success:
    print(f"✓ Embedded: {skill_path}")
else:
    print(f"⚠ Embedding skipped (no API key or error)")
```

## What Gets Generated

```
.claude/skills/
├── [project]-patterns.md     # Project coding patterns
├── [project]-testing.md      # Testing conventions
├── [project]-deployment.md   # Deployment workflow
├── [project]-debugging.md    # Common debug scenarios
└── [project]-setup.md        # Dev environment setup
```

## Generation Process

### Step 1: Analyze Codebase

Discover patterns and conventions:

```bash
# Find common patterns
grep -r "// Pattern:" --include="*.ts" .
grep -r "# Pattern:" --include="*.py" .

# Find test patterns
ls tests/ __tests__/ spec/ 2>/dev/null

# Find CI/CD
ls .github/workflows/ .gitlab-ci.yml Jenkinsfile 2>/dev/null

# Find documentation
ls docs/ README.md CONTRIBUTING.md 2>/dev/null
```

### Step 2: Identify Skill Opportunities

Analyze for:

| Area       | Look For                    | Skill Generated     |
| ---------- | --------------------------- | ------------------- |
| Components | Repeated component patterns | component-patterns  |
| API        | REST/GraphQL patterns       | api-patterns        |
| State      | Redux/Context/Zustand usage | state-management    |
| Testing    | Test file patterns          | testing-conventions |
| Auth       | Auth patterns               | authentication-flow |
| Database   | ORM patterns                | database-patterns   |

### Step 3: Generate Pattern Skill

```markdown
---
name: [project]-patterns
description: Coding patterns and conventions for [project]
---

# [Project] Coding Patterns

## Component Pattern

[Based on analysis of existing components]

### Standard Component Structure

\`\`\`typescript
// [Pattern discovered from codebase]
\`\`\`

### When to Use

- [Discovered use cases]

### Examples in Codebase

- `src/components/[Example1].tsx`
- `src/components/[Example2].tsx`

## API Pattern

[Based on analysis of API routes]

### Standard Route Structure

\`\`\`typescript
// [Pattern discovered from API routes]
\`\`\`

## Naming Conventions

- Components: [Discovered convention]
- Files: [Discovered convention]
- Functions: [Discovered convention]
```

### Step 4: Generate Testing Skill

```markdown
---
name: [project]-testing
description: Testing conventions and patterns for [project]
---

# [Project] Testing Conventions

## Test Framework

[Detected: Jest/Vitest/Pytest/etc.]

## Test Structure

### Unit Tests

Location: `[discovered test path]`
Pattern:
\`\`\`typescript
// [Pattern from existing tests]
\`\`\`

### Integration Tests

Location: `[discovered test path]`
Pattern:
\`\`\`typescript
// [Pattern from existing tests]
\`\`\`

## Running Tests

\`\`\`bash

# All tests

[discovered command]

# Single file

[discovered command]

# Watch mode

[discovered command]
\`\`\`

## Mocking Conventions

[Based on analysis of test files]
```

### Step 5: Generate Deployment Skill

```markdown
---
name: [project]-deployment
description: Deployment workflow for [project]
---

# [Project] Deployment

## Environments

| Environment                          | URL | Branch |
| ------------------------------------ | --- | ------ |
| [Discovered environments from CI/CD] |

## Deployment Process

### Pre-Deployment Checklist

- [ ] Tests passing
- [ ] Lint clean
- [ ] Build successful
- [ ] [Project-specific checks]

### Deploy Commands

\`\`\`bash

# [Commands discovered from CI/CD or package.json]

\`\`\`

## Rollback Process

[Based on CI/CD analysis or documented process]
```

### Step 6: Generate Setup Skill

```markdown
---
name: [project]-setup
description: Development environment setup for [project]
---

# [Project] Dev Setup

## Prerequisites

- [Node.js/Python/Rust version]
- [Database requirements]
- [Other dependencies]

## Quick Start

\`\`\`bash

# Clone

git clone [repo]

# Install dependencies

[detected install command]

# Setup environment

[detected setup steps]

# Start development

[detected dev command]
\`\`\`

## Environment Variables

| Variable                     | Description | Default |
| ---------------------------- | ----------- | ------- |
| [From .env.example analysis] |

## Common Issues

[Based on README or docs analysis]
```

## Post-Generation

After generating:

```
Skills generated at .claude/skills/

Skills created:
✓ [project]-patterns.md - Coding patterns (47 patterns found)
  └─ Embedded for semantic discovery
  └─ Available immediately (hot-reload in Claude Code 2.1.0+)
✓ [project]-testing.md - Test conventions
  └─ Embedded for semantic discovery
  └─ Available immediately (hot-reload in Claude Code 2.1.0+)
✓ [project]-deployment.md - Deployment workflow
  └─ Embedded for semantic discovery
  └─ Available immediately (hot-reload in Claude Code 2.1.0+)
✓ [project]-setup.md - Dev environment setup
  └─ Embedded for semantic discovery
  └─ Available immediately (hot-reload in Claude Code 2.1.0+)

Embedding Summary:
- Total skills: 4
- Successfully embedded: 4
- Skipped: 0

These skills are now available for this project and discoverable via semantic search.

Note: With Claude Code 2.1.0+, generated skills are immediately available
without restarting your session. Test with `/skill invoke <skill-name>`.

Would you like me to review and refine any of them?
```

### When Analysis Available

```
Analysis-driven skill generation from .claude/analysis.json

Patterns used (confidence >= 0.6):
- nextjs (0.95) → project:deploy
- prisma (0.85) → project:db-migrate
- react-query (0.90) → project:data-fetching
- colocated-tests (0.75) → project:testing

Skills created:
✓ project-deploy/SKILL.md - Vercel deployment
  └─ Detected from: nextjs, vercel-config
  └─ Embedded for semantic discovery
✓ project-db-migrate/SKILL.md - Database migrations
  └─ Detected from: prisma
  └─ Embedded for semantic discovery
...
```

## Customization

Generated skills can be:

1. Edited to add more patterns
2. Extended with team-specific conventions
3. Linked from CLAUDE.md for automatic loading
4. Re-embedded after changes with `/popkit:project embed`

## Integration

**Requires:**

- Project analysis (via analyze-project skill) for pattern-driven generation
- Voyage AI API key for auto-embedding (optional, but recommended)

**Enables:**

- Project-specific guidance
- Consistent coding patterns
- Faster onboarding
- Team convention enforcement
- Semantic discovery of project skills
