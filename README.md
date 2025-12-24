# Claude Skills Registry

<p align="center">
  <img src="https://img.shields.io/badge/Skills-100+-purple?style=flat-square" alt="Skills">
  <img src="https://img.shields.io/badge/Updated-Daily-green?style=flat-square" alt="Updated">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
</p>

> The official skills registry for [sk](https://github.com/majiayu000/caude-skill-manager) - Claude Skills Manager

## What is this?

This repository maintains a curated index of Claude Code skills, enabling fast and reliable skill discovery through the `sk` CLI.

## Using the Registry

```bash
# Install sk first
go install github.com/majiayu000/caude-skill-manager@latest

# Search skills (uses this registry)
sk search testing
sk search pdf
sk search --popular

# Install a skill
sk install anthropics/skills/docx
```

## Registry Structure

```
skill-registry/
├── registry.json       # Main index (all skills)
├── sources/            # Individual source configs
│   ├── anthropic.json  # Official Anthropic skills
│   ├── community.json  # Community skills
│   └── awesome.json    # Curated awesome skills
├── categories/         # Category-based indexes
│   ├── documents.json
│   ├── development.json
│   └── ...
└── scripts/            # Update scripts
    └── update.py
```

## Adding Your Skill

### Option 1: Submit via Issue

1. Open an [issue](https://github.com/majiayu000/skill-registry/issues/new)
2. Use the "Add Skill" template
3. Provide: repo URL, name, description, category

### Option 2: Submit via PR

1. Fork this repo
2. Add your skill to `sources/community.json`:

```json
{
  "name": "your-skill-name",
  "repo": "your-username/your-repo",
  "path": "optional/path/to/skill",
  "description": "What your skill does",
  "category": "development",
  "tags": ["testing", "automation"]
}
```

3. Submit a PR

## Categories

| Category | Description |
|----------|-------------|
| `documents` | Document creation/editing (docx, pdf, pptx) |
| `development` | Development tools and workflows |
| `design` | UI/UX design and frontend |
| `testing` | Testing and QA |
| `ai` | AI/ML tools and integrations |
| `productivity` | Productivity and automation |
| `data` | Data processing and analysis |
| `devops` | DevOps and infrastructure |

## API

The registry can be accessed directly via raw GitHub URLs:

```bash
# Full registry
curl https://raw.githubusercontent.com/majiayu000/skill-registry/main/registry.json

# Specific category
curl https://raw.githubusercontent.com/majiayu000/skill-registry/main/categories/documents.json
```

## Auto-Updates

This registry is automatically updated daily via GitHub Actions:
- Fetches latest skill metadata from GitHub
- Validates SKILL.md files exist
- Updates star counts and descriptions
- Removes dead/invalid skills

## License

MIT License - see [LICENSE](LICENSE) for details.
