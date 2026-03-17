---
name: code-implement
description: Language-specific coding guidelines. Use when implementing code in Python or other supported languages.
---

# Code Implement Skill

Language-specific patterns, anti-patterns, and best practices for writing code.

---

## When to Use

- Writing code in supported languages
- Deciding on code structure, patterns, or style
- Designing domain models or data structures
- Organizing code into modules

**IMPORTANT - Workflow Integration:**
- **Multiple independent tasks from a plan?** → Use `task-dispatch` skill instead (it will invoke this skill per task with quality gates)
- **Single implementation task or asking about patterns?** → Use this skill directly

---

## Git Workflow

When implementing from a spec:

1. **Create a branch for the spec** (if not already on one):
   - Branch from main/master
   - Name: `feat/<spec-name>`
   - Example: `feat/user-auth` for `./specs/active/user-auth/`

2. **Verify before starting:**
   - Confirm you're on the correct spec branch
   - Pull latest if branch already exists

---

## Supported Languages

Language-specific guidelines are in `~/.claude/skills/code-implement/resources/loqui/languages/{language}/`.

**Use Read tool** (not Glob) to access resources - paths outside cwd require direct reads.

Each language directory follows this structure:

```
~/.claude/skills/code-implement/resources/loqui/languages/{language}/
├── README.md              # Overview, core principles, anti-patterns checklist
├── quality.md             # Naming, comments, documentation conventions
├── composition.md         # Structuring behavior (classes/functions/modules)
├── modules.md             # Package structure, organization, public APIs
├── errors.md              # Error handling patterns and practices
└── ...                    # Additional language-specific resources as needed
```

**Start with the language README** for quick reference and core principles, then dive into specific topic files as needed.

---

## Related Skills

- **task-dispatch**: Use for multiple independent implementation tasks (invokes this skill per task)
- **code-test**: Use for TDD workflow (write test first, then implement)
- **code-review**: Review methodology (delegates here for language specifics)
- **pr-review**: GitHub PR workflow (delegates to code-review)

---

## Reference

- [defense-in-depth.md](reference/defense-in-depth.md) - Multi-layer validation patterns
- [root-cause-tracing.md](reference/root-cause-tracing.md) - Tracing bugs to their source
