---
name: kano-commit-convention-skill
description: Commit convention linting and changelog automation following the Kano commit format.
---

# kano-commit-convention-skill

**GitHub Copilot Skill Adapter** - This is a thin wrapper that points to the canonical skill documentation.

---

## 🎯 Quick Start

This skill provides **commit convention linting and changelog automation** following the Kano commit format.

**📚 Canonical Documentation**: [`skills/kano-commit-convention-skill/SKILL.md`](../../skills/kano-commit-convention-skill/SKILL.md)

> [!IMPORTANT]
> **You MUST read the canonical SKILL.md** before using this skill. The sections below provide quick navigation to key topics.

---

## Essential Reading (From Canonical SKILL.md)

### 1. **Overview and Commit Format**
   - Read: [Purpose](../../skills/kano-commit-convention-skill/SKILL.md#purpose)
   - Read: [Commit Format](../../skills/kano-commit-convention-skill/SKILL.md#commit-message-format)

### 2. **Usage**
   - Linting commits: See [kano-commit lint](../../skills/kano-commit-convention-skill/SKILL.md#cli-usage)
   - Generating changelog: See [changelog generation](../../skills/kano-commit-convention-skill/SKILL.md#changelog)

### 3. **Integration**
   - Git hooks: [pre-commit integration](../../skills/kano-commit-convention-skill/SKILL.md#pre-commit)
   - CI/CD: [GitHub Actions](../../skills/kano-commit-convention-skill/SKILL.md#ci-integration)

---

## Installation

```bash
cd skills/kano-commit-convention-skill
pip install -e .
```

---

## Common Tasks

### Lint Commit Messages
```bash
python skills/kano-commit-convention-skill/scripts/kano-commit lint
```

### Validate Last Commit
```bash
python skills/kano-commit-convention-skill/scripts/kano-commit lint --count 1
```

---

## Commit Format

```
[Subsystem][Type] Summary (TICKET-ID)
```

**Example:**
```
[Core][Feature] Add user authentication (KABSD-FTR-0001)
```

---

## References

| Topic | Link |
|-------|------|
| **Full Documentation** | [`SKILL.md`](../../skills/kano-commit-convention-skill/SKILL.md) |
| **Commit Format** | [`SKILL.md#commit-message-format`](../../skills/kano-commit-convention-skill/SKILL.md#commit-message-format) |
| **Examples** | [`references/`](../../skills/kano-commit-convention-skill/references/) |

---

## Before You Start

1. ✅ Read the canonical [`SKILL.md`](../../skills/kano-commit-convention-skill/SKILL.md)
2. ✅ Install dependencies: `pip install -e skills/kano-commit-convention-skill`
3. ✅ Set up pre-commit hooks (optional)
