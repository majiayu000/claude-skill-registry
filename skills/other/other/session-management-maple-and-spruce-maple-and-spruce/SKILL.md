---
name: session-management
description: Managing session docs, updating documentation throughout SDLC, archiving sessions. Use when starting/ending sessions or updating docs.
---

# Session & Documentation Management

## When to Use

Use this skill at the start and end of every session, and whenever documentation needs updating during development work.

## Self-Updating Documentation Workflow

Documentation in this project is designed to stay current. Follow this READ -> FIND -> UPDATE -> CREATE -> ARCHIVE lifecycle.

### READ Phase (start of session / before coding)

Always read these at session start:
1. `AGENTS.md` - Project context and directives
2. `docs/sessions/SESSION.md` - Current work status and next steps
3. Run `gh issue list` to check open issues

Read these based on the task:
- Feature work: `docs/reference/implementation-status.md`, `docs/reference/REQUIREMENTS.md`
- Pattern questions: `docs/architecture/PATTERNS-AND-PRACTICES.md`
- Architecture decisions: `docs/architecture/DECISIONS.md`
- Environment/deployment: `docs/guides/environment-setup.md`, `docs/architecture/ci-cd.md`

### FIND Phase (locating relevant docs)

| What you need | Where to look |
|---------------|---------------|
| Procedural workflows | `.claude/skills/{name}/SKILL.md` |
| Path-specific rules | `.claude/rules/` (auto-loaded by glob match) |
| System design, ADRs | `docs/architecture/` |
| How-to guides | `docs/guides/` |
| Status tracking, specs | `docs/reference/` |
| Session context | `docs/sessions/` |

### UPDATE Phase (during and after coding)

Update these as you work:

| When this happens | Update this file |
|-------------------|-----------------|
| Feature started or completed | `docs/reference/implementation-status.md` |
| New Cloud Function deployed | `docs/reference/deployed-functions.md` |
| Task completed in session | `docs/sessions/SESSION.md` |
| Architecture decision made | `docs/architecture/DECISIONS.md` (new ADR) |
| New code pattern established | `docs/architecture/PATTERNS-AND-PRACTICES.md` |
| New feature planned | `docs/reference/REQUIREMENTS.md` |
| Future idea captured | `docs/reference/BACKLOG.md` |

### CREATE Phase (when new docs are needed)

| Doc type | Location | Format |
|----------|----------|--------|
| Procedural workflow | `.claude/skills/{name}/SKILL.md` | Frontmatter + instructions |
| Path-specific rule | `.claude/rules/{context}.md` | Globs frontmatter + rules |
| Architecture doc | `docs/architecture/` | Markdown |
| How-to guide | `docs/guides/` | Markdown |
| Reference/tracking | `docs/reference/` | Markdown |

#### Skill format

```markdown
---
name: skill-name
description: Brief description including trigger keywords. Max 200 chars.
---

# Skill Title

## When to Use
## Instructions
## Examples
## Common Issues
```

#### Rule format

```markdown
---
globs: ["path/pattern/**"]
---

# Rule Title
Context-specific rules here.
```

### ARCHIVE Phase (end of session)

1. Update `docs/sessions/SESSION.md` with:
   - What was completed
   - Current status
   - Next steps
   - Any blockers
2. When starting a new phase or milestone, archive the current session:
   - Copy content to `docs/sessions/history/YYYY-MM-DD.md`
   - Reset `docs/sessions/SESSION.md` for the new context
