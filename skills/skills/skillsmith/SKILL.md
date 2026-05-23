---
name: "Skillsmith"
description: "Discover, install, compare, and manage Claude Code skills. Use when searching for skills, evaluating quality, understanding trust tiers, checking quotas, or creating custom skills. Triggers: 'find skill', 'search skills', 'install skill', 'trust tier', 'create skill', 'skill quality', 'skill quota'."
---

# Skillsmith

Skillsmith is your skill discovery and management system for Claude Code. It provides access to 500+ community skills with trust verification, quality scoring, and security scanning.

## Quick Reference: MCP Tools

| Tool | Use When | Example |
|------|----------|---------|
| `search` | Finding skills by keyword, category, or trust tier | "Find testing skills" |
| `get_skill` | Getting full details about a specific skill | "Show details for community/jest-helper" |
| `install_skill` | Installing a skill to ~/.claude/skills/ | "Install the commit skill" |
| `uninstall_skill` | Removing an installed skill | "Uninstall jest-helper" |
| `skill_recommend` | Getting contextual recommendations | "Recommend skills for my React project" |
| `skill_validate` | Checking skill structure before manual install | "Validate this skill" |
| `skill_compare` | Comparing 2-5 skills side-by-side | "Compare jest-helper and vitest-helper" |
| `skill_suggest` | Getting suggestions based on current work | Automatic based on context |

## Trust Tiers

Skills are categorized by verification level:

| Tier | Badge | Meaning | When to Trust |
|------|-------|---------|---------------|
| **Official** | Green checkmark | Published by Anthropic, fully reviewed | Always safe |
| **Verified** | Blue checkmark | Verified publisher, 10+ stars, 30+ days old | Generally safe |
| **Community** | Yellow | Passed security scan, has required metadata | Review before install |
| **Unverified** | Red warning | No verification | Only if you trust the author |

For detailed criteria, see [TRUST_TIERS.md](docs/TRUST_TIERS.md).

## Quota System

API calls are limited by tier:

| Tier | API Calls/Month | Price |
|------|-----------------|-------|
| **Community** | 1,000 | Free |
| **Individual** | 10,000 | $9.99/mo |
| **Team** | 100,000 | $25/user/mo |
| **Enterprise** | Unlimited | $55/user/mo |

Warnings are shown at 80% and 90% usage. Upgrade at https://skillsmith.app/upgrade

For details, see [QUOTAS.md](docs/QUOTAS.md).

## Security Model

Skillsmith operates as a security boundary between untrusted skill sources and your Claude Code environment.

### What Skillsmith Validates

Before any skill is installed, Skillsmith performs:

1. **SKILL.md validation** - Must have valid YAML frontmatter with name and description
2. **Security scan** - Checks for jailbreak patterns, suspicious URLs, sensitive file access
3. **Typosquatting detection** - Warns if skill name is similar to known skills
4. **Blocklist check** - Rejects known-malicious skills

### What Skillsmith Cannot Prevent

- Novel attack patterns not in our detection database
- Social engineering in legitimate-looking instructions
- Runtime behavior (skills execute with your permissions)

**Recommendation**: Always review skill content before installation, especially for unverified skills.

For the complete security model, see [SECURITY.md](docs/SECURITY.md).

## Creating Skills

The **skill-builder** skill (auto-installed) helps you create custom skills:

```
"Create a skill for generating API documentation"
"Build a skill to automate code reviews"
```

The skill-builder guides you through:
- YAML frontmatter (name ≤64 chars, description ≤1024 chars)
- Progressive disclosure structure (4 levels)
- Directory organization
- Validation checklist

## Search Examples

```
# Find all testing skills
"Search for testing skills"

# Find verified skills only
"Find verified skills for git workflows"

# Filter by quality score
"Search for devops skills with score above 80"

# Compare options
"Compare jest-helper, vitest-helper, and mocha-helper"
```

## Common Tasks

### Install a Skill
```
"Install the commit skill"
```
Skillsmith downloads the skill, runs security scan, and installs to ~/.claude/skills/.

### Check What's Installed
```
"What skills do I have installed?"
```

### Remove a Skill
```
"Uninstall the old-skill"
```

### Get Recommendations
```
"Recommend skills for my TypeScript project"
```
Skillsmith analyzes your project context and suggests relevant skills.

## License

Skillsmith uses **Elastic License 2.0**:
- You can self-host for internal use
- You can modify for your own use
- You cannot offer Skillsmith as a managed service to others
- You cannot circumvent license key functionality

## Related Documentation

- [Security Deep-Dive](docs/SECURITY.md)
- [Trust Tiers](docs/TRUST_TIERS.md)
- [Quota System](docs/QUOTAS.md)

## Getting Help

- Docs: `npx @skillsmith/mcp-server --docs`
- Issues: https://github.com/smith-horn/skillsmith/issues
- Email: support@skillsmith.app
