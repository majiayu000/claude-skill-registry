---
name: claude-md-author
description: This skill should be used when the user asks to "create a CLAUDE.md", "write a CLAUDE.md", "set up CLAUDE.md", "configure Claude for this project", "add project instructions for Claude", "initialize Claude context", or mentions needing project-specific Claude instructions.
---

# CLAUDE.md Authoring Guide

This skill guides the creation of effective CLAUDE.md files that provide Claude with essential project context.

## Core Principle

LLMs are stateless—they have no memory between sessions. The only thing Claude knows about a codebase is the tokens provided to it. CLAUDE.md enters every conversation, making it the primary tool for context management.

## The WHAT-WHY-HOW Framework

Structure CLAUDE.md content around three categories:

| Category | Purpose | Examples |
|----------|---------|----------|
| **WHAT** | Technology stack, project structure, codebase organization | "This is a Next.js app using TypeScript and Prisma" |
| **WHY** | Project purpose, component functions | "The auth module handles OAuth2 flow for enterprise SSO" |
| **HOW** | Commands, testing procedures, verification methods | "Run `npm test` before commits; lint with `npm run lint`" |

## Critical Constraints

### Instruction Budget

Frontier LLMs reliably follow approximately 150-200 instructions. Claude Code's system prompt already contains ~50 instructions, leaving limited budget for CLAUDE.md. Smaller models degrade exponentially as instructions increase.

### Size Guidelines

- Target under 300 lines
- Aim for under 60 lines if possible (HumanLayer's CLAUDE.md achieves this)
- Every line should provide universal value across all sessions

## What to Include

**Essential elements:**
- Build and test commands (the HOW)
- Project structure overview (the WHAT)
- Key architectural decisions (the WHY)
- Patterns and conventions specific to this codebase
- File references using `file:line` format (not code snippets)

**Example build/test section:**
```markdown
## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Type check: `npx tsc --noEmit`
```

## What to Avoid

### Never Use as a Linter

"Never send an LLM to do a linter's job." Code style guidelines waste tokens and degrade performance. Use deterministic tools (ESLint, Prettier, Biome) instead. Configure hooks to run formatters automatically.

### Avoid Auto-Generation

CLAUDE.md is one of the highest leverage points for Claude's effectiveness. Manually craft it rather than using `/init` commands. Auto-generated content tends to be verbose and generic.

### Skip Universally Irrelevant Content

Claude may ignore CLAUDE.md entirely if content seems task-irrelevant. The system explicitly reminds Claude that "this context may or may not be relevant to your tasks."

### No Duplicate Information

Avoid copying code snippets—they become outdated quickly. Use `file:line` pointers instead.

## Progressive Disclosure Strategy

Store task-specific guidance in separate files rather than bloating CLAUDE.md:

```
.claude/
├── CLAUDE.md              # Core context (universal)
├── docs/
│   ├── testing.md         # Testing procedures
│   ├── deployment.md      # Deployment guide
│   └── architecture.md    # Architecture decisions
└── plans/                 # Implementation plans
```

Reference these in CLAUDE.md:
```markdown
## Documentation
- Testing procedures: `.claude/docs/testing.md`
- Deployment guide: `.claude/docs/deployment.md`
```

## Alternative Mechanisms

Consider using Claude Code's other features instead of cramming everything into CLAUDE.md:

| Need | Better Approach |
|------|-----------------|
| Code formatting | Hooks that run formatters |
| Task-specific instructions | Slash commands linking to guides |
| Recent changes context | Commands referencing version control |
| One-time procedures | Separate markdown files |

## Creation Workflow

To create an effective CLAUDE.md:

1. **Audit the codebase**: Identify build commands, test procedures, key patterns
2. **Draft minimal content**: Start with WHAT-WHY-HOW essentials only
3. **Remove task-specific content**: Move specialized instructions to `.claude/docs/`
4. **Use pointers**: Replace code snippets with `file:line` references
5. **Test for universality**: Ask "Will this help in every Claude session?"

## Template

```markdown
# Project Name

Brief one-line description of what this project does.

## Stack
- [Primary language/framework]
- [Database/storage]
- [Key dependencies]

## Commands
- Build: `command`
- Test: `command`
- Lint: `command`

## Structure
- `src/` - Application code
- `tests/` - Test files
- [Other key directories]

## Key Patterns
- [Pattern 1 with file:line reference]
- [Pattern 2 with file:line reference]

## Notes
- [Important architectural decision]
- [Gotcha or non-obvious behavior]
```

## Additional Resources

For detailed examples and anti-patterns, consult:
- **`references/examples.md`** - Real CLAUDE.md examples
- **`references/anti-patterns.md`** - Common mistakes to avoid
