---
name: claude-project-docs
description: Generate concise CLAUDE.md files and agent documentation following best practices. Use when setting up a new project for Claude Code, auditing existing CLAUDE.md, or creating progressive disclosure documentation structure.
---

# Claude Project Docs

Create well-crafted, minimal CLAUDE.md files (~60 lines) with progressive disclosure through agent_docs/.

## When to Use

Invoke when user:
- Asks to "set up Claude for this project" or "create a CLAUDE.md"
- Wants to "audit" or "improve" their existing CLAUDE.md
- Needs to create agent documentation or progressive disclosure structure
- Says "help Claude understand this codebase"

## Core Methodology

### The 60-Line Rule

CLAUDE.md goes into EVERY session. Keep it:
- **< 60 lines** ideal (HumanLayer recommendation)
- **< 300 lines** absolute maximum
- **Universally applicable** - no task-specific content

### WHAT/WHY/HOW Structure

```markdown
# Project Name

[One sentence: what this is]

## Tech Stack
- [Framework/Language]
- [Key dependencies]

## Project Structure
[3-5 line overview of directories that matter]

## Development
[Essential commands only - build, test, run]

## Critical Rules
[2-3 non-negotiable constraints]

## Reference Documentation
When working on specific tasks, read:
- `agent_docs/[topic].md`
```

### Progressive Disclosure

Create `agent_docs/` for task-specific documentation:

| File | Content |
|------|---------|
| `building.md` | Build commands, compilation, bundling |
| `testing.md` | Test commands, coverage, fixtures |
| `architecture.md` | System design, key decisions |
| `database.md` | Schema, migrations, connections |
| `deployment.md` | Deploy process, environments |

Claude reads these ON DEMAND, not every session.

## Anti-Patterns to Prevent

**NEVER include in CLAUDE.md:**
- Code style rules (use ESLint/Prettier/linters)
- Full command documentation (use agent_docs/)
- Implementation examples (point to actual code)
- > 300 lines of content
- Generic boilerplate from /init

**Why:** LLMs follow ~150-200 instructions reliably. Every unnecessary line degrades compliance.

## Workflow

### 1. Generate New CLAUDE.md

```
User: Set up Claude for this project
→ Analyze: package.json, pyproject.toml, go.mod, Makefile
→ Generate: Minimal CLAUDE.md (~60 lines)
→ Create: agent_docs/ structure
```

### 2. Audit Existing CLAUDE.md

```
User: Audit my CLAUDE.md
→ Check: Line count, anti-patterns, task-specific content
→ Report: Issues found with severity
→ Suggest: Specific removals and agent_docs/ migrations
```

### 3. Create Agent Docs

```
User: Create agent docs for testing
→ Generate: agent_docs/testing.md with project-specific content
→ Update: CLAUDE.md reference section
```

## Output Format

When generating CLAUDE.md:
1. Show the complete file content
2. Explain what was included and why
3. List what was intentionally excluded
4. Suggest agent_docs/ files to create next

## References

For templates and examples:
- `references/claude-md-template.md` - Minimal starter template
- `references/agent-docs-catalog.md` - Complete agent_docs file list
- `references/anti-patterns.md` - Detailed anti-pattern guide
- `references/examples/` - Project-type examples

---

**Principle:** High leverage documentation. Every line in CLAUDE.md costs context across all sessions.
