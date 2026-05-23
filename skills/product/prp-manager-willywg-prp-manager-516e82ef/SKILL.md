---
name: prp-manager
description: Create and execute PRPs (Product Requirements Prompts) for feature implementation using Context Engineering principles. Use when planning new features, initializing PRP setup, executing existing PRPs, or when the user mentions "PRP", "feature planning", "implementation blueprint", or "context engineering". Helps achieve one-pass implementation success.
license: MIT
compatibility: Works with any agent supporting the Agent Skills specification. Requires file system access.
metadata:
  author: willywg
  version: "1.0"
---
# PRP Manager Skill

## Purpose
Create comprehensive PRPs (Product Requirements Prompts) that enable AI agents to implement features with sufficient context and validation loops for one-pass implementation success.

## When to Use
- **Initialize**: Setting up PRPs for a new project (creates custom template)
- **Generate**: Planning a new feature or enhancement
- **Execute**: Implementing an existing PRP file

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **One-Pass Success**: Goal is working code through comprehensive context

## References
- **Default Template**: See [assets/templates/prp_base.md](assets/templates/prp_base.md)
- **Usage Examples**: See [references/examples.md](references/examples.md)
- **Customization Guide**: See [references/customization.md](references/customization.md)
- **Project Template**: `PRPs/templates/prp_base.md` (generated per project)

---

## Workflow 1: Initialize PRPs (RECOMMENDED FIRST)

> Run this first in any new project to create a customized PRP template.

### When to Suggest
- User asks to create a PRP but `PRPs/templates/prp_base.md` doesn't exist
- User explicitly asks to initialize or setup PRPs
- First time using PRPs in a project

### Step 1: Analyze Project

**Read these files (in order of priority):**
```yaml
AI Agent Configuration:
  - AGENTS.md                              # Universal AI agent guidance (agents.md standard)
  - CLAUDE.md or .claude/settings.json    # Claude-specific rules
  - GEMINI.md                              # Gemini-specific rules

Project Documentation:
  - README.md                              # Project overview
  - CONTRIBUTING.md                        # Contribution guidelines

Package/Dependencies:
  - package.json                           # Node.js projects
  - pyproject.toml or requirements.txt     # Python projects
  - Cargo.toml                             # Rust projects
  - go.mod                                 # Go projects

Code Quality:
  - .eslintrc* / biome.json               # JS/TS linting
  - ruff.toml / pyproject.toml [ruff]     # Python linting
  - mypy.ini / pyproject.toml [mypy]      # Python type checking
  - tsconfig.json                          # TypeScript config

Testing:
  - jest.config.* / vitest.config.*       # JS/TS testing
  - pytest.ini / pyproject.toml [pytest]  # Python testing
  - tests/ or __tests__/ structure        # Test patterns
```

### Step 2: Detect Stack & Conventions

**Extract from analysis:**
- Language/Framework (Python/FastAPI, Node/Express, etc.)
- Package manager (uv, npm, pnpm, yarn, cargo)
- Linting tools and commands
- Type checking tools and commands
- Testing framework and commands
- Project structure conventions
- Any special rules from AGENTS.md/CLAUDE.md/GEMINI.md

### Step 3: Generate Custom Template

**Create directory and template:**
```bash
mkdir -p PRPs/templates
```

**Generate `PRPs/templates/prp_base.md` with:**
- Project-specific validation commands
- Correct package manager syntax
- Actual linting/testing tools used
- Codebase tree format matching project structure
- Any gotchas from AGENTS.md/CLAUDE.md/GEMINI.md
- Test patterns from existing tests

### Step 4: Confirm Setup

**Output created:**
- `PRPs/templates/prp_base.md` - Customized for this project

**Summary to user:**
- Stack detected
- Validation commands configured
- Any special rules applied
- Ready to generate PRPs

---

## Workflow 2: Generate PRP

### Pre-check
If `PRPs/templates/prp_base.md` doesn't exist:
> "I notice this project doesn't have a PRP template yet. Would you like me to initialize PRPs first? This will create a customized template based on your project's stack and conventions."

### Step 1: Understand the Request
- What is the feature/enhancement?
- What is the expected end state?
- Any specific patterns to follow?

### Step 2: Research Phase

**Codebase Analysis:**
- Search for similar features/patterns
- Identify files to reference
- Note existing conventions
- Check test patterns

**External Research (if needed):**
- Library documentation (include URLs)
- Implementation examples
- Best practices and pitfalls

### Step 3: Generate the PRP

**Check existing PRPs:**
```bash
ls -1 PRPs/*.md 2>/dev/null | grep -E '^PRPs/[0-9]{3}--' | sort -r | head -5
```

**Naming:** `PRPs/{NNN}--{feature-name}.md`
- 3-digit padding (001, 002, ...)
- kebab-case for feature name

**Use template from:** `PRPs/templates/prp_base.md`

### Step 4: Quality Check

- [ ] All context included for one-pass implementation
- [ ] Validation gates are executable
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Gotchas documented

**Score** (1-10): Confidence for one-pass success

---

## Workflow 3: Execute PRP

### Step 1: Load and Understand
- Read PRP completely
- Understand all context
- Extend research if gaps found

### Step 2: Plan
- Think before executing
- Break into manageable steps
- Use task tracking if available
- Identify patterns from existing code

### Step 3: Execute
- Follow implementation blueprint
- Implement in task order
- Mark tasks as completed

### Step 4: Validate
- Run each validation command
- Fix failures
- Re-run until all pass

### Step 5: Complete
- All checklist items done
- Final validation suite passed
- Re-read PRP to verify
- Report completion status

---

## Best Practices

**DO:**
- Initialize PRPs first for new projects
- Include comprehensive context for AI agents
- Reference real files and patterns
- Provide executable validation commands
- Document known gotchas
- List tasks in execution order

**DON'T:**
- Skip initialization (generic template is less effective)
- Create new patterns when existing ones work
- Skip validation
- Ignore failing tests
- Hardcode values that should be config

---

## Output Summary

### For Initialize
```
✅ PRPs Initialized for [Project Name]

Stack Detected:
- Language: Python 3.11
- Framework: FastAPI
- Package Manager: uv
- Linting: ruff
- Type Checking: mypy
- Testing: pytest

Created:
- PRPs/templates/prp_base.md

Ready to generate PRPs!
```

### For Generate
```
📄 PRPs/005--feature-name.md

Confidence: 8/10
Key Notes: [implementation highlights]
```

### For Execute
```
✅ PRP Execution Complete

Tasks: 5/5 completed
Validation: All passing
Status: SUCCESS
```
