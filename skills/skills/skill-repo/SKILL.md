---
name: skill-repo
description: "Agent Skill: Guide for structuring Netresearch skill repositories. Use when creating skills, standardizing repos, or setting up composer/release workflows. By Netresearch."
---

# Skill Repository Structure Guide

Standards for Netresearch skill repository layout and distribution.

## When to Use

- Creating a new skill repository
- Standardizing an existing skill repo
- Setting up release workflows

## Repository Structure

```
{skill-name}/
├── SKILL.md              # AI instructions (required)
├── README.md             # Human documentation (required)
├── LICENSE               # MIT (required)
├── composer.json         # PHP distribution
├── references/           # Extended docs
├── scripts/              # Automation
└── .github/workflows/release.yml
```

## SKILL.md Requirements

```yaml
---
name: skill-name          # lowercase, hyphens, max 64 chars
description: "Agent Skill: ... By Netresearch."
---
```

- Under 500 lines, use references/ for extended content

## Installation Methods

1. **Marketplace**: `/plugin marketplace add netresearch/claude-code-marketplace`
2. **Release**: Download and extract to `~/.claude/skills/{name}/`
3. **Composer**: `composer require netresearch/agent-{name}`

## Composer Package

```json
{
  "name": "netresearch/agent-{skill-name}",
  "type": "ai-agent-skill",
  "require": {"netresearch/composer-agent-skill-plugin": "*"},
  "extra": {"ai-agent-skill": "SKILL.md"}
}
```

## Validation

```bash
scripts/validate-skill.sh
```

## References

- `references/installation-methods.md`
- `references/composer-setup.md`
- `templates/README.md.template`

---

> **Contributing:** https://github.com/netresearch/skill-repo-skill
