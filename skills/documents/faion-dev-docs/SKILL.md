---
user-invocable: false
name: faion-dev-docs
description: Creates or updates CLAUDE.md documentation for any module/folder. Use when user asks to create docs, document module, add CLAUDE.md. Triggers on "CLAUDE.md", "documentation", "document this", "create docs".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*), Bash(ls:*), Bash(wc:*)
---

# Creating CLAUDE.md Documentation

**Communication: User's language. Docs: English.**

## Purpose

Create standardized AI-readable CLAUDE.md documentation for any module, package, or folder. One file per context — CLAUDE.md only.

## Philosophy

- **One file**: CLAUDE.md contains all context for its directory
- **Progressive detail**: Brief at top, details in sections
- **Self-contained**: No external AGENTS.md, GEMINI.md, etc.
- **Subfolder docs**: Each significant subfolder can have its own CLAUDE.md

## Structure

```
{folder}/
├── CLAUDE.md           # Context for this folder (100-200 lines)
└── subfolder/
    └── CLAUDE.md       # Context for subfolder (if needed)
```

## Workflow

1. **Analyze Folder** — Read key files, understand purpose
2. **Identify Type** — Backend, frontend, infra, library, etc.
3. **Write CLAUDE.md** — Follow template for that type
4. **Verify** — Check line count, completeness

## Universal CLAUDE.md Template

```markdown
# {Folder Name}

{One-sentence description of purpose}

## Overview

{2-3 sentences explaining what this folder contains and why}

## Structure

| Path | Purpose |
|------|---------|
| `file.py` | Description |
| `subfolder/` | Description |

## Key Concepts

- **Concept1**: Explanation
- **Concept2**: Explanation

## Entry Points

- `main_file.py` — Primary entry point
- `config.py` — Configuration

## Common Operations

### Operation 1
```bash
command example
```

### Operation 2
Brief explanation of how to do X.

## Dependencies

- dep1: purpose
- dep2: purpose

## Notes

- Important consideration 1
- Important consideration 2
```

## Type-Specific Sections

### Backend (Django/FastAPI/etc.)
```markdown
## Models
| Model | Purpose |
|-------|---------|
| **User** | User accounts |

## Services
| Service | Purpose |
|---------|---------|
| `create_user()` | Creates new user |

## API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/users/` | Create user |
```

### Frontend (React/Angular/Vue)
```markdown
## Components
| Component | Purpose |
|-----------|---------|
| `Button` | Reusable button |

## State Management
- Store location: `src/store/`
- Pattern: Redux/Context/etc.

## Routing
| Route | Component | Purpose |
|-------|-----------|---------|
| `/home` | HomePage | Landing |
```

### Infrastructure (K8s/Terraform/etc.)
```markdown
## Resources
| Resource | Purpose |
|----------|---------|
| `deployment.yaml` | App deployment |

## Environments
| Env | Description |
|-----|-------------|
| dev | Development |
| prod | Production |

## Commands
```bash
kubectl apply -f deployment.yaml
```
```

### Library/Package
```markdown
## Public API
| Function/Class | Purpose |
|----------------|---------|
| `parse()` | Parse input |

## Usage
```python
from package import parse
result = parse(data)
```
```

## Size Guidelines

- Target: 100-150 lines
- Maximum: 200 lines
- If larger needed → split to subfolders with own CLAUDE.md

## What to Include

- Purpose and context
- Key files and their roles
- Important concepts
- Common operations
- Dependencies

## What NOT to Include

- Full code listings (reference files instead)
- Duplicated parent context
- Temporary/generated files
- Obvious information

## Checklist

- [ ] Purpose clear in first 3 lines
- [ ] Structure table present
- [ ] Key concepts explained
- [ ] Entry points identified
- [ ] Line count within limits
