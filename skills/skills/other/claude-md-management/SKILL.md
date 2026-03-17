---
name: claude-md-management
description: Provides comprehensive CLAUDE.md file management capabilities including auditing, quality assessment, and targeted improvements. Use when user asks to check, audit, update, improve, fix, maintain, or validate CLAUDE.md files. Also triggers for "project memory optimization", "CLAUDE.md quality check", "documentation review", or when CLAUDE.md needs to be created from scratch. This skill scans all CLAUDE.md files, evaluates quality against standardized criteria, outputs detailed quality reports with scores and recommendations, then makes targeted updates with user approval.
allowed-tools: Read, Glob, Grep, Bash, Edit
---

# CLAUDE.md Management

Provides comprehensive CLAUDE.md file management capabilities including auditing, quality assessment, and targeted improvements. This skill ensures Claude Code has optimal project context by maintaining high-quality documentation files.

## Overview

CLAUDE.md files are the primary mechanism for providing project-specific context to Claude Code sessions. This skill manages the complete lifecycle of CLAUDE.md files: discovery, quality assessment, reporting, and improvement. It follows a 5-phase workflow that ensures documentation is current, actionable, and concise.

The skill evaluates CLAUDE.md files against standardized quality criteria across 6 dimensions: Commands/Workflows, Architecture Clarity, Non-Obvious Patterns, Conciseness, Currency, and Actionability. Each file receives a score (0-100) and letter grade (A-F) with specific improvement recommendations.

## When to Use

Use this skill when:

- User explicitly asks to "check", "audit", "update", "improve", "fix", or "maintain" CLAUDE.md
- User mentions "CLAUDE.md quality", "documentation review", or "project memory optimization"
- CLAUDE.md needs to be created from scratch for a new project
- User asks about improving Claude's understanding of the codebase
- Documentation has become stale or outdated
- Starting work on a new codebase and need to understand existing documentation
- User presses `#` during a session to incorporate learnings into CLAUDE.md

**Trigger phrases:** "audit CLAUDE.md", "check documentation quality", "improve project context", "review CLAUDE.md", "validate documentation"

## Instructions

### Phase 1: Discovery

Find all CLAUDE.md files in the repository:

```bash
find . -name "CLAUDE.md" -o -name ".claude.md" -o -name ".claude.local.md" 2>/dev/null | head -50
```

**File Types & Locations:**

| Type | Location | Purpose |
|------|----------|---------|
| Project root | `./CLAUDE.md` | Primary project context (checked into git, shared with team) |
| Local overrides | `./.claude.local.md` | Personal/local settings (gitignored, not shared) |
| Global defaults | `~/.claude/CLAUDE.md` | User-wide defaults across all projects |
| Package-specific | `./packages/*/CLAUDE.md` | Module-level context in monorepos |
| Subdirectory | Any nested location | Feature/domain-specific context |

### Phase 2: Quality Assessment

For each CLAUDE.md file, read [references/quality-criteria.md](references/quality-criteria.md) and evaluate against these criteria:

| Criterion | Weight | What to Check |
|-----------|--------|---------------|
| Commands/workflows | 20 pts | Are build/test/deploy commands present and working? |
| Architecture clarity | 20 pts | Can Claude understand the codebase structure? |
| Non-obvious patterns | 15 pts | Are gotchas and quirks documented? |
| Conciseness | 15 pts | Is content dense without filler? |
| Currency | 15 pts | Does it reflect current codebase state? |
| Actionability | 15 pts | Are instructions executable and copy-paste ready? |

**Quality Scores:** A (90-100), B (70-89), C (50-69), D (30-49), F (0-29)

### Phase 3: Quality Report Output

**CRITICAL: Always output the quality report BEFORE making any updates.**

Format:
```markdown
## CLAUDE.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Files needing update: X

### File-by-File Assessment
#### 1. ./CLAUDE.md (Project Root)
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | X/20 | ... |
| Architecture clarity | X/20 | ... |
| Non-obvious patterns | X/15 | ... |
| Conciseness | X/15 | ... |
| Currency | X/15 | ... |
| Actionability | X/15 | ... |

**Issues:**
- [List specific problems]

**Recommended additions:**
- [List what should be added]
```

### Phase 4: Targeted Updates

After report output, ask user for confirmation before updating.

**Read [references/update-guidelines.md](references/update-guidelines.md) for detailed update principles.**

Key principles:
1. **Propose targeted additions only** - commands, gotchas, patterns, configs
2. **Keep it minimal** - avoid obvious info, generic advice, one-off fixes
3. **Show diffs** - file, change (diff format), explanation

Diff format:
```markdown
### Update: ./CLAUDE.md
**Why:** [Brief explanation of why this helps]

```diff
+ ## Quick Start
+
+ ```bash
+ npm install
+ npm run dev
+ ```
```
```

### Phase 5: Apply Updates

After user approval, use Edit tool to apply changes. Preserve existing content structure.

## Examples

### Example 1: Quality Assessment

**User request:** "Check if my CLAUDE.md is good"

**Response:**
```markdown
## CLAUDE.md Quality Report

### Summary
- Files found: 1
- Average score: 65/100
- Files needing update: 1

### File-by-File Assessment

#### 1. ./CLAUDE.md
**Score: 65/100 (Grade: C)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | 10/20 | Only npm install documented |
| Architecture clarity | 15/20 | Basic tree, missing module relationships |
| Non-obvious patterns | 5/15 | No gotchas documented |
| Conciseness | 15/15 | Concise and dense |
| Currency | 10/15 | Some outdated paths |
| Actionability | 10/15 | Some vague instructions |

**Issues:**
- Missing test command
- Missing build command
- No documentation of auth flow complexity
- References to old src/structure

**Recommended additions:**
- Add Commands section with test/build
- Document auth module gotcha
- Update architecture paths
```

### Example 2: Creating from Scratch

**User request:** "Create a CLAUDE.md for this React project"

**Response:**
```markdown
I'll create a CLAUDE.md for your React project. Let me first analyze the codebase structure.

[Scans package.json, src/, and key config files]

## CLAUDE.md Quality Report

### Summary
- Files found: 0
- Creating new CLAUDE.md at project root

### Proposed CLAUDE.md Content:

# Project Name

## Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server (Vite on port 5173) |
| `npm run build` | Production build |
| `npm run test` | Run Vitest tests |
| `npm run lint` | ESLint check |

## Architecture

```
src/
├── components/    # Reusable UI components
├── pages/         # Route pages
├── hooks/         # Custom React hooks
├── lib/           # Utilities and API clients
└── main.tsx       # Entry point
```

## Gotchas

- Vite requires files in `public/` for static assets
- State updates in `useEffect` need proper dependency arrays
```

Shall I create this file?
```

### Example 3: Update Proposal

**User request:** "Update my CLAUDE.md with what you learned"

**Response:**
```markdown
### Update: ./CLAUDE.md

**Why:** Discovered that tests require database setup which wasn't documented.

```diff
## Testing

+ **Prerequisites:** Start test database first with `docker-compose up -d test-db`
+ `npm run test` - Run all tests
+ `npm run test:unit` - Unit tests only (no DB required)
```

Also found issue with API_BASE_URL:

```diff
## Environment

- `API_BASE_URL` - API endpoint (default: localhost:3000)
+ `API_BASE_URL` - API endpoint (required for production, defaults to http://localhost:3000 in dev)
```

Apply these changes?
```

## Best Practices

1. **Always read references before acting**: Quality criteria, templates, and update guidelines contain essential details
2. **Report before editing**: Never modify CLAUDE.md without first presenting a quality report
3. **Preserve existing structure**: When updating, maintain the existing organization and style
4. **Be project-specific**: Only add information specific to this codebase, not generic advice
5. **Verify commands work**: Before suggesting commands, mentally or actually verify they execute correctly
6. **Use progressive disclosure**: Keep SKILL.md lean, reference detailed rubrics in separate files
7. **Score consistently**: Apply the same scoring standards across all files for fair comparison

## Constraints and Warnings

1. **Never modify without approval**: Always get user confirmation before editing CLAUDE.md files
2. **Don't remove content without asking**: If suggesting deletions, explicitly mark them and get approval
3. **Respect `.claude.local.md`**: These are personal settings; never suggest modifying them in shared docs
4. **Avoid generic advice**: Do not add "write good code" type content - focus on project-specific patterns
5. **Keep diffs concise**: Show only the actual changes, not entire file contents
6. **Verify file paths**: Ensure all referenced files exist before documenting them
7. **Score objectively**: Use the rubric consistently; don't inflate scores for incomplete documentation
