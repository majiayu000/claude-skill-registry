---
name: plugin-help
description: Show available commands and explain how to use the Gotrino inclusion plugin.
allowed-tools: Read, Glob
user-invocable: true
---

# Plugin Help

Show available commands and explain how to use the Gotrino inclusion plugin.

## Output

```markdown
# Gotrino - Inclusion Plugin

Tools to help you write more inclusive code.

## Quick Reference

### Fast Checks (run anytime)
| Command | What it does |
|---------|--------------|
| `/guardian [path]` | Quick inclusion gut-check (lightweight) |
| `/language-check [path]` | Scan for non-inclusive language |
| `/names-check [path]` | Check name diversity in examples |
| `/i18n-check [path]` | Find internationalization issues |

### Deeper Analysis
| Command | What it does |
|---------|--------------|
| `/examples-audit [path]` | Analyze mock data for cultural assumptions |
| `/inclusion-audit [path]` | Comprehensive inclusion review |
| `/test-assumption [path]` | Identify hidden assumptions about users |

### Utilities
| Command | What it does |
|---------|--------------|
| `/inclusive-names` | Generate diverse name suggestions |
| `/explain [path]` | Create decision record in `decisions/` |
| `/impact [path]` | Analyze change impact before making it |

### Setup
| Command | What it does |
|---------|--------------|
| `/teach-charter` | Configure plugin for your project |

## Typical Workflow

**Starting a new project:**
1. Run `/teach-charter` to set up your `.inclusion-config.md`
2. Define your scope (US-only? Global? etc.)
3. Set priorities for your team

**During development:**
- Run `/guardian` after generating forms, UI, or examples
- Chain it: "create the signup form, then /guardian it"
- Run focused checks (`/language-check`, `/names-check`) as needed

**Before shipping:**
- Run `/inclusion-audit` for comprehensive review
- Run `/test-assumption` on user-facing flows

## Configuration

Your settings are stored in `.inclusion-config.md`:

- **Scope decisions**: What's in/out of scope (e.g., i18n for US-only products)
- **Acknowledged findings**: Issues you've reviewed and accepted
- **Priorities**: What matters most for your project
- **Decisions location**: Where `/explain` saves decision records (default: `decisions/`)

Run `/teach-charter` to create or update this file.

## Philosophy

This plugin isn't a linter. It's a **second pair of eyes** that asks:

> "Who might this exclude? What assumptions are baked in?"

It won't catch everything, and not everything it catches needs fixing. Use judgment. The goal is code that welcomes more users, not compliance with rules.
```

## Process

1. Output the help text above
2. If `.inclusion-config.md` exists, note: "Config loaded. Run `/teach-charter` to view or update."
3. If no config exists, note: "No config found. Run `/teach-charter` to set up your project."
