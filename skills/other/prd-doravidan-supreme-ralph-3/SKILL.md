---
name: prd
description: Generate intelligent PRD (Product Requirements Document) from feature description
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# PRD - Product Requirements Document Generator

Generate intelligent, context-aware PRDs for RALPH autonomous development.

## Commands

| Command | Description |
|---------|-------------|
| `/prd [feature]` | Generate PRD for a feature |
| `/prd --interactive` | Interactive PRD creation with questions |
| `/prd --from-spec` | Generate PRD from existing PROJECT_SPEC.md |
| `/prd --simple` | Quick spec for simple features (1-2 stories) |
| `/prd --complex` | Deep analysis for complex features (7+ stories) |

## Triggers

- `/prd Add user authentication`
- "create a PRD for [feature]"
- "generate user stories for [feature]"

## Process

### Step 1: Gather Context

First, read project context if available:

```bash
# Check for PROJECT_SPEC.md
if [ -f PROJECT_SPEC.md ]; then
  echo "✓ Found PROJECT_SPEC.md - using project context"
  cat PROJECT_SPEC.md
fi

# Check for .ralph/config.yaml
if [ -f .ralph/config.yaml ]; then
  echo "✓ Found .ralph/config.yaml"
  cat .ralph/config.yaml
fi

# Detect tech stack from files
ls package.json requirements.txt go.mod Cargo.toml 2>/dev/null
```

### Step 2: Clarify Feature Requirements

Use AskUserQuestion to understand the feature:

```
? What is the scope of this feature?
  ○ Small (1-3 user stories)
  ○ Medium (4-6 user stories) (Recommended)
  ○ Large (7-10 user stories)
  ○ Let me specify

? Should this feature include tests?
  ○ Yes, comprehensive tests (Recommended)
  ○ Yes, basic tests only
  ○ No tests
  ○ Follow existing project pattern

? Any specific libraries or patterns to use?
  ○ Use recommended for tech stack
  ○ Let me specify
```

### Step 3: Generate Intelligent Stories

Based on the tech stack, generate appropriate user stories:

#### TypeScript/JavaScript Patterns

**Frontend (React/Next.js):**
1. Types → Hooks → Components → Integration → Polish

**Backend (Express/Node):**
1. Types → Services → Routes → Middleware → Tests

**Full-stack (Next.js):**
1. Types → API Routes → Server Actions → Components → Integration

#### Python Patterns

**FastAPI/Django:**
1. Models → Schemas → Services → Routes → Tests

#### Go Patterns

**Standard:**
1. Types → Core Logic → Handlers → Middleware → Tests

### Step 4: Generate prd.json

Create a comprehensive PRD:

```json
{
  "project": "[Feature Name]",
  "branchName": "ralph/[feature-slug]",
  "description": "[Detailed description of the feature]",
  "projectContext": {
    "language": "[detected language]",
    "framework": "[detected framework]",
    "testFramework": "[detected test framework]"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "[What this story implements]",
      "acceptanceCriteria": [
        "[Specific, testable criterion 1]",
        "[Specific, testable criterion 2]",
        "[Quality gate: npm test passes]"
      ],
      "priority": 1,
      "passes": false
    }
    // ... more stories
  ]
}
```

### Acceptance Criteria Guidelines

**Good acceptance criteria are:**
- Specific and testable
- Include actual file paths
- Include quality commands
- Cover edge cases
- Mention error handling

**Example - Good:**
```json
"acceptanceCriteria": [
  "User interface defined in src/types/user.ts with id, email, passwordHash, createdAt fields",
  "Session interface defined with userId, token, expiresAt fields",
  "Types exported and importable: import { User, Session } from '@/types/user'",
  "npx tsc --noEmit passes with no errors"
]
```

**Example - Bad:**
```json
"acceptanceCriteria": [
  "Create user type",
  "Add session type",
  "Make sure it works"
]
```

### Step 5: Create Feature Branch Name

Generate a descriptive branch name:

```javascript
function generateBranchName(feature) {
  const slug = feature
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 50);
  return `ralph/${slug}`;
}
```

Examples:
- "User authentication" → `ralph/user-authentication`
- "Add dark mode toggle" → `ralph/add-dark-mode-toggle`
- "Fix login button" → `ralph/fix-login-button`

### Step 6: Save PRD Files

Create two files:

1. **prd.json** - Machine-readable format for RALPH

```bash
# Write prd.json
cat > prd.json << 'EOF'
{
  "project": "...",
  "branchName": "...",
  ...
}
EOF
```

2. **tasks/prd-[feature-slug].md** - Human-readable version

```markdown
# PRD: [Feature Name]

Generated: [date]
Branch: ralph/[feature-slug]

## Overview

[Description]

## User Stories

### US-001: [Title]
**Priority:** 1
**Status:** Incomplete

[Description]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Quality gate]

---

### US-002: [Title]
...
```

### Step 7: Display Summary

```
╔════════════════════════════════════════════════════════════════╗
║                    PRD Generated!                               ║
╚════════════════════════════════════════════════════════════════╝

Feature: User Authentication
Branch: ralph/user-authentication
Stories: 6 user stories

Created:
  ✓ prd.json (machine-readable)
  ✓ tasks/prd-user-authentication.md (human-readable)

User Stories:
  US-001: Create User model and auth types (P1)
  US-002: Implement password hashing service (P2)
  US-003: Create JWT token utilities (P3)
  US-004: Add login and register routes (P4)
  US-005: Implement auth middleware (P5)
  US-006: Add logout and session management (P6)

Next Steps:
  1. Review prd.json and adjust acceptance criteria if needed
  2. Create the feature branch:
     git checkout -b ralph/user-authentication
  3. Run /ralph-run to start autonomous development
```

## Example PRDs by Feature Type

### Authentication Feature

```json
{
  "project": "User Authentication",
  "branchName": "ralph/user-authentication",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create User model and auth types",
      "priority": 1,
      "acceptanceCriteria": [
        "User interface with id, email, passwordHash, createdAt",
        "Session interface with userId, token, expiresAt",
        "Types exported from src/types/auth.ts",
        "Type checking passes"
      ]
    },
    {
      "id": "US-002",
      "title": "Implement password hashing service",
      "priority": 2,
      "acceptanceCriteria": [
        "hashPassword(plain) returns hashed string",
        "verifyPassword(plain, hash) returns boolean",
        "Uses bcrypt with cost factor 10",
        "Unit tests in tests/services/auth.test.ts pass"
      ]
    }
    // ... more stories
  ]
}
```

### CRUD Feature

```json
{
  "project": "Product Management CRUD",
  "branchName": "ralph/product-crud",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create Product model and types",
      "priority": 1,
      "acceptanceCriteria": [
        "Product interface with id, name, price, description, createdAt",
        "CreateProductInput type for creation",
        "UpdateProductInput type with partial fields",
        "Types exported from src/types/product.ts"
      ]
    },
    {
      "id": "US-002",
      "title": "Implement Product repository",
      "priority": 2,
      "acceptanceCriteria": [
        "create(input) creates and returns product",
        "findById(id) returns product or null",
        "findAll() returns all products",
        "update(id, input) updates and returns product",
        "delete(id) removes product"
      ]
    }
    // ... more stories
  ]
}
```

### UI Component Feature

```json
{
  "project": "Dark Mode Toggle",
  "branchName": "ralph/dark-mode-toggle",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create theme context and types",
      "priority": 1,
      "acceptanceCriteria": [
        "Theme type with 'light' | 'dark' values",
        "ThemeContext with theme and toggleTheme",
        "ThemeProvider component wraps app",
        "useTheme hook returns context"
      ]
    },
    {
      "id": "US-002",
      "title": "Implement theme persistence",
      "priority": 2,
      "acceptanceCriteria": [
        "Theme saved to localStorage",
        "Theme loaded on app start",
        "System preference detected if no saved theme",
        "Theme persists across page refreshes"
      ]
    }
    // ... more stories
  ]
}
```

## Complexity-Based Spec Creation Pipeline

The PRD process adapts based on detected or specified complexity:

### SIMPLE Mode (`/prd --simple`)

For quick, small features:

```
Pipeline: Discovery → Quick Spec → Validate

1. Discovery (1-2 questions)
   - What does this feature do?
   - Any specific constraints?

2. Quick Spec
   - 1-2 user stories
   - Essential criteria only
   - Skip deep analysis

3. Validate
   - Check schema validity
   - Verify against PROJECT_SPEC.md
```

### STANDARD Mode (Default)

For typical features:

```
Pipeline: Discovery → Requirements → Context → Spec → Plan → Validate

1. Discovery (3-5 questions)
   - Feature scope
   - User impact
   - Technical considerations

2. Requirements
   - Break into user stories
   - Define acceptance criteria
   - Identify dependencies

3. Context
   - Read PROJECT_SPEC.md
   - Check existing patterns
   - Query memory for similar features

4. Spec Generation
   - Create prd.json
   - Generate human-readable version

5. Plan Preview
   - Estimate complexity
   - Suggest pipeline configuration

6. Validate
   - Schema validation
   - Pattern compliance
   - Quality gate coverage
```

### COMPLEX Mode (`/prd --complex`)

For large, architectural features:

```
Pipeline: Research → Discovery → Requirements → Context → Spec → Self-Critique → Plan → Validate

1. Research Phase (NEW)
   - Analyze codebase architecture
   - Identify integration points
   - Check for breaking changes
   - Review similar implementations in memory

2. Extended Discovery (6-8 questions)
   - Detailed scope definition
   - Risk identification
   - Performance considerations
   - Security implications

3. Deep Requirements
   - 7+ user stories
   - Detailed acceptance criteria
   - Edge case coverage
   - Error handling requirements

4. Context Analysis
   - Full codebase scan
   - Dependency graph analysis
   - Memory query for patterns

5. Comprehensive Spec
   - Detailed prd.json
   - Architecture diagrams
   - Risk assessment

6. Self-Critique (NEW)
   - Review generated spec
   - Check for gaps
   - Validate feasibility
   - Suggest improvements

7. Plan Generation
   - Detailed subtask breakdown
   - Parallel execution opportunities
   - Human checkpoint recommendations

8. Validate
   - Schema validation
   - Architecture compliance
   - Security review
   - Test coverage analysis
```

### Auto-Detection

Without flags, complexity is auto-detected:

```
Analyzing feature: "Add user authentication"

Detected complexity: STANDARD
  - Mentions multiple components (types, routes, middleware)
  - Requires security considerations
  - Involves database/storage

Using STANDARD pipeline...
```

## Tips

- **Be specific** in acceptance criteria - vague criteria lead to vague implementations
- **Include quality gates** - Every story should have "tests pass" or "lint passes"
- **Order by dependency** - Lower priority stories can depend on higher priority ones
- **Keep stories small** - If a story is too big, split it
- **Match tech stack** - Use patterns appropriate for the project's framework
- **Use appropriate mode** - Simple for quick fixes, complex for major features
