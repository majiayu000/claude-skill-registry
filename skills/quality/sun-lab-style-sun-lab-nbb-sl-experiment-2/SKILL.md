---
name: applying-sun-lab-style
description: >-
  Applies Sun Lab Python coding conventions when writing, reviewing, or refactoring code. Covers
  .py files, docstrings, type annotations, naming conventions, README.md files, git commit messages,
  and Claude skill files. Use when writing new code, modifying existing code, reviewing pull requests,
  creating documentation, writing commit messages, or when the user asks about coding standards.
---

# Sun Lab Style Guide

Applies Sun Lab coding and documentation conventions.

**You MUST read the appropriate style guide and apply its conventions when writing or modifying any code,
documentation, commits, or skills. You MUST verify your changes against the style guide's checklist before submitting.**

---

## Workflow Selection

**CRITICAL:** You MUST read the appropriate guide before performing any task. The quick reference section below is
insufficient for compliance. Each guide contains detailed rules and verification checklists that you MUST follow.

| Task                        | Action                                        |
|-----------------------------|-----------------------------------------------|
| **Writing Python code?**    | Read [PYTHON_STYLE.md](PYTHON_STYLE.md)       |
| **Writing README?**         | Read [README_STYLE.md](README_STYLE.md)       |
| **Writing commit message?** | Read [COMMIT_STYLE.md](COMMIT_STYLE.md)       |
| **Writing skill file?**     | Read [SKILL_STYLE.md](SKILL_STYLE.md)         |

After reading the appropriate guide:
1. Apply all conventions from that guide
2. Verify against the guide's checklist before submitting

**Do not skip reading the guide.** The quick reference is only a reminder for frequently used rules, not a substitute
for the full guide.

---

## Style Guides

| Guide                                | Use When                                                                     |
|--------------------------------------|------------------------------------------------------------------------------|
| [PYTHON_STYLE.md](PYTHON_STYLE.md)   | Writing Python code (docstrings, type annotations, naming, error handling)   |
| [README_STYLE.md](README_STYLE.md)   | Creating or updating README files                                            |
| [COMMIT_STYLE.md](COMMIT_STYLE.md)   | Writing git commit messages                                                  |
| [SKILL_STYLE.md](SKILL_STYLE.md)     | Creating Claude skills or YAML configuration files                           |

---

## Quick Reference (Not a Substitute for Full Guides)

These are reminders only. You MUST read the full guide for your task before proceeding.

### Python Code (includes docstrings and inline comments)

- **Docstrings**: Google-style with Args, Returns, Raises, Notes, Attributes sections
- **Prose Over Lists**: Use prose in all documentation; bullet lists are forbidden in docstrings
- **Inline Comments**: Third person imperative, above the code, explain non-obvious logic
- **Naming**: Full words (`position` not `pos`), private members `_underscore`
- **Type Annotations**: All parameters and returns; always specify dtype for arrays
- **Error Handling**: Use `console.error()` from `ataraxis_base_utilities`
- **Line Length**: Maximum 120 characters

### Commit Messages

- Start with past tense verb: Added, Fixed, Updated, Refactored, Removed
- Header line ≤ 72 characters
- End with a period
- Multi-line commits: blank line after header, then `-- ` prefixed bullets

### README Files

- Third-person voice throughout
- Present tense as default

### Skills & Templates

- SKILL.md frontmatter: `name` (gerund form), `description` (third person)
- Line length ≤ 120 characters
