---
name: refresh-claude
description: Review recent changes and update CLAUDE.md to keep it relevant for future sessions. Use after significant changes or periodically to maintain context.
tools: Read, Grep, Glob, Edit, Write, Bash
user-invocable: true
---

# Refresh CLAUDE.md

You are refreshing the project's CLAUDE.md file to ensure it stays relevant and useful for future Claude Code sessions.

## Purpose

CLAUDE.md serves as persistent context between sessions. When a project evolves, CLAUDE.md should evolve too. This skill:

1. Reviews recent changes to the codebase
2. Identifies new patterns, conventions, or important context
3. Updates CLAUDE.md to reflect current state
4. Removes outdated information

## Process

### Step 1: Analyze Recent Changes

```bash
# Recent commits
git log --oneline -20

# Changed files
git diff --stat HEAD~10..HEAD

# New files
git diff --name-status HEAD~10..HEAD | grep "^A"
```

Look for:
- New features or modules
- New dependencies or tools
- Changed conventions or patterns
- New commands or scripts
- Architecture changes

### Step 2: Review Current CLAUDE.md

Read the existing CLAUDE.md and identify:
- [ ] Outdated information
- [ ] Missing new features/tools
- [ ] Incorrect commands or paths
- [ ] Stale conventions

### Step 3: Scan the Codebase

Check for patterns not reflected in CLAUDE.md:

```bash
# Check for new test patterns
ls -la **/test* **/*test* **/*spec* 2>/dev/null | head -20

# Check for new config files
ls -la *.config.* .* 2>/dev/null | head -20

# Check package.json/pyproject.toml/etc for new scripts
cat package.json 2>/dev/null | jq '.scripts' || true
```

### Step 4: Update CLAUDE.md

Make targeted updates:

**DO update:**
- New commands (dev, test, build, lint)
- New project structure (directories, key files)
- New conventions discovered in code
- Important architectural decisions
- New dependencies that affect how to work with the code

**DON'T add:**
- Implementation details that change frequently
- Obvious things (e.g., "this is a JavaScript project" for a .js repo)
- Temporary workarounds
- Personal preferences not enforced by tooling

### Step 5: Verify Changes

After updating, verify:
- [ ] Commands still work
- [ ] Paths are correct
- [ ] No duplicate sections
- [ ] Concise and scannable

## Output Format

```markdown
## CLAUDE.md Refresh Summary

### Changes Made
- Added: [what was added]
- Updated: [what was updated]
- Removed: [what was removed]

### Context Discovered
- [New pattern or convention found]
- [New tool or command found]

### Recommendations
- [Suggestions for project improvements]
```

## Guidelines

### Keep It Concise
CLAUDE.md should be scannable. Every line should earn its place.

```
❌ "This project uses React, which is a JavaScript library for building user interfaces..."
✓ "React 18 with TypeScript. See src/components/ for patterns."
```

### Focus on What's Actionable
Include information Claude needs to work effectively:

```
✓ Commands to run
✓ Key file locations
✓ Conventions to follow
✓ Things to avoid
```

### Avoid Duplication
Don't repeat what's in:
- README.md (user-facing docs)
- Code comments (implementation details)
- Config files (tooling handles it)

### Keep It Fresh
Remove information that's:
- No longer accurate
- Covered by tooling (linters, formatters)
- Too detailed for context

## Example Updates

### Adding a New Command
```markdown
## Commands
+ npm run e2e        # Run end-to-end tests
```

### Adding a Convention
```markdown
## Conventions
+ API routes follow REST conventions in `src/api/`
+ Use `zod` for runtime validation at API boundaries
```

### Removing Outdated Info
```markdown
- ## Legacy
- The old auth system in `src/auth-old/` is deprecated.
```

## When to Run

- After adding major features
- After significant refactoring
- After adding new tools or dependencies
- Periodically (weekly/monthly) on active projects
- Before onboarding new team members
