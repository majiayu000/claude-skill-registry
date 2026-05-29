---
name: propose-project-learning
description: Propose additions to project CLAUDE.md based on session learnings
argument-hint: "[--save]"
---

# Propose Project Learning

Retrospect on the current session and propose learnings for the project's CLAUDE.md.

## Purpose

After working on a project, identify patterns, conventions, preferences, and rules that should be documented in the project's CLAUDE.md to improve future sessions.

## Usage

```bash
/propose-project-learning        # Analyze and propose learnings
/propose-project-learning --save # Save proposal to ~/.claude/learnings/
```

## What This Captures

| Category | Examples |
|----------|----------|
| **Code conventions** | Naming patterns, file organization, import ordering |
| **Architecture decisions** | Preferred patterns, avoided anti-patterns |
| **Tool preferences** | Test frameworks, linters, formatters |
| **Project-specific rules** | Business logic constraints, domain terminology |
| **Workflow preferences** | Commit style, PR conventions, review process |

## Execution Instructions

When the user runs this command:

### 1. Analyze Current Session

Review the conversation history for:

- **Corrections made** - When the user corrected Claude's approach
- **Explicit preferences** - "Always use X", "Never do Y", "Prefer Z"
- **Repeated patterns** - Consistent choices across multiple files
- **Project conventions** - Naming, structure, organization patterns
- **Tool/framework specifics** - Project-specific configurations or usage

### 2. Check Existing CLAUDE.md

Read the project's CLAUDE.md (if exists) to avoid duplicates:

```bash
cat CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found"
```

Also check for CLAUDE.local.md:

```bash
cat CLAUDE.local.md 2>/dev/null
```

### 3. Generate Proposal

Format the proposal as:

```markdown
# Proposed Learnings for CLAUDE.md

Based on this session, consider adding these to your project's CLAUDE.md:

## Code Conventions

- Use `snake_case` for all Python function names
- Prefer dataclasses over plain dicts for structured data

## Architecture

- All API endpoints go through the service layer, never direct DB access
- Use repository pattern for database operations

## Testing

- Use pytest fixtures, not setUp/tearDown methods
- Mock external services at the client level, not individual methods

## Project-Specific

- The `core` module should have no dependencies on other app modules
- All dates are stored as UTC, converted to local time only in templates

---

To add these to your CLAUDE.md:
1. Review each suggestion
2. Copy relevant items to CLAUDE.md
3. Adjust wording to match your style
```

### 4. Handle --save Flag

If `--save` is provided:

1. **Ensure directory exists**:
   ```bash
   mkdir -p ~/.claude/learnings/projects/{project-slug}/proposals/
   ```

2. **Save proposal** with timestamp:
   ```bash
   # File: ~/.claude/learnings/projects/{project-slug}/proposals/learning-{timestamp}.md
   ```

3. **Confirm**:
   ```
   Proposal saved to ~/.claude/learnings/projects/{project-slug}/proposals/learning-2026-01-09.md

   Review later with: cat ~/.claude/learnings/projects/{project-slug}/proposals/
   ```

### 5. Offer Next Steps

```
Next steps:
  [1] Add to CLAUDE.md now (I'll help edit)
  [2] Save for later (/propose-project-learning --save)
  [3] Dismiss

Select option:
```

## Quality Criteria

Only propose learnings that are:

| Criterion | Description |
|-----------|-------------|
| **Specific** | Concrete rules, not vague guidelines |
| **Actionable** | Claude can follow them in future sessions |
| **Project-relevant** | Not general best practices already known |
| **Validated** | Based on actual session behavior, not assumptions |

## Examples

### Good Learnings

```markdown
- API responses use `{"data": ..., "error": null}` wrapper format
- All Django models inherit from `BaseModel` in `core.models`
- Use `ruff` for linting, not `flake8`
```

### Poor Learnings (Too Generic)

```markdown
- Write clean code
- Follow PEP 8
- Use meaningful variable names
```

## Notes

- This command analyzes the current session context
- Works best after substantial implementation work
- Complements `/propose-forge-improvement` which targets Product Forge itself
- Learnings are project-specific, not global
