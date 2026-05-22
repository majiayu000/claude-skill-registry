---
name: readme-writer
description: |
  Write effective README files following SOTA 2026 conventions.
  Use when: (1) creating new README.md, (2) improving existing README,
  (3) reviewing README quality. Covers badges, ToC, quick start,
  GIF demos, CLI documentation patterns.
category: documentation
user-invocable: true
---

# README Writer

Write effective README files following SOTA 2026 best practices.

## Quick Reference

| Section | Priority | Purpose |
|---------|----------|---------|
| Title + Tagline | Required | One sentence explaining what it does |
| Badges | High | Build status, version, license at a glance |
| Hero Example | Required | Copy-paste code that works immediately |
| What It Does | Required | 3-5 bullets explaining value |
| Quick Start | Required | Get running in under 10 minutes |
| Why/Motivation | Medium | Problem-solution framing |
| Features | Medium | Categorized feature list |
| Installation | High | Step-by-step for different platforms |
| Usage/Examples | High | Code examples with expected output |
| API Reference | Medium | For libraries/CLIs with many commands |
| Configuration | Medium | Config file locations and options |
| Contributing | Medium | Link to CONTRIBUTING.md |
| License | Required | Clear license statement |
| ToC | High | For READMEs over 200 lines |

## When to Use

- Creating a new open source project
- Improving an existing README that feels incomplete
- Reviewing README quality before release
- Converting internal docs to public README

## Hero Pattern

The first thing users see should be:

1. **Title**: Project name
2. **Tagline**: One sentence (under 120 chars)
3. **Badges**: npm version, build status, license
4. **Hero code**: Runnable example in under 5 lines

```markdown
# project-name

Brief tagline explaining what this does.

[![npm](https://img.shields.io/npm/v/project-name)](https://npmjs.com/package/project-name)
[![build](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)

\`\`\`bash
npx project-name init
\`\`\`
```

## Decision Tree

**How long is the README?**
- Under 100 lines: No ToC needed
- 100-200 lines: Optional ToC
- Over 200 lines: ToC required

**Is it a CLI tool?**
- Yes: Document `--help`, `--json`, show GIF demos
- No: Focus on code examples

**Is it a library?**
- Yes: API reference with types
- No: Usage examples sufficient

**Is it a monorepo?**
- Yes: Use `monorepo-readme` skill instead
- No: Standard structure applies

## Quality Checklist

Before publishing, verify:

- [ ] New user can get running in under 10 minutes
- [ ] Hero example works with copy-paste
- [ ] All code examples are tested
- [ ] No broken links
- [ ] License is specified
- [ ] Contact/contributing info exists

## Reference Files

| Topic | File |
|-------|------|
| Section ordering | [references/structure.md](references/structure.md) |
| Badge patterns | [references/badges.md](references/badges.md) |
| CLI documentation | [references/cli-docs.md](references/cli-docs.md) |
| Full checklist | [references/checklist.md](references/checklist.md) |

## Skill Chaining

This skill works with:
- **markdown-writer**: For consistent prose style
- **doc-maintenance**: For keeping README updated
- **monorepo-readme**: For multi-package projects

## Sources

- [Make a README](https://www.makeareadme.com/)
- [awesome-readme](https://github.com/matiassingers/awesome-readme)
- [readme-best-practices](https://github.com/jehna/readme-best-practices)
