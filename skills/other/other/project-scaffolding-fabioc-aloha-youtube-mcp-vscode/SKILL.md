---
name: "Project Scaffolding Skill"
description: "First impressions matter. Set projects up for success."
applyTo: "**/*scaffold*,**/*init*,**/*new*,**/*create*,**/README*"
---

# Project Scaffolding Skill

> First impressions matter. Set projects up for success.

## Essential Files

| File | Purpose |
| ---- | ------- |
| `README.md` | Hero banner + overview + quick start |
| `CONTRIBUTING.md` | How to contribute |
| `LICENSE.md` | Legal terms |
| `CHANGELOG.md` | Version history |
| `.gitignore` | Ignored files |
| `.editorconfig` | Consistent formatting |

## README Structure

```markdown
<!-- Hero SVG banner -->
# Project Name

> One-line description

## Features
- Feature 1
- Feature 2

## Quick Start
[3 commands max]

## Documentation
[Links]

## License
[Badge + link]
```

## Hero Banner Pattern

- Width: 800-1200px
- Height: 200-400px
- Include: Logo, tagline, 3-5 key features
- Format: SVG (scalable), PNG fallback
- Dark/light mode variants

## Documentation Folder

```text
docs/
├── README.md           # Index
├── QUICK-START.md      # 5-min guide
├── ARCHITECTURE.md     # System design
├── API.md              # Reference
└── CONTRIBUTING.md     # Dev guide
```

## Planning Files

| File | When |
| ---- | ---- |
| `ROADMAP.md` | Multi-phase projects |
| `TODO.md` | Simple task tracking |
| `DECISIONS.md` | Architecture decisions |
| `RISKS.md` | Known risks |

## Config Files by Stack

| Stack | Essential Configs |
| ----- | ----------------- |
| Node.js | `package.json`, `tsconfig.json`, `.nvmrc` |
| Python | `pyproject.toml`, `requirements.txt` |
| VS Code | `.vscode/settings.json`, `launch.json` |
| GitHub | `.github/workflows/`, `CODEOWNERS` |

## Quality Gates

- [ ] README has hero banner
- [ ] Quick start works in < 5 min
- [ ] License specified
- [ ] Contributing guide exists
- [ ] .gitignore appropriate for stack

## Synapses

See [synapses.json](synapses.json) for connections.
