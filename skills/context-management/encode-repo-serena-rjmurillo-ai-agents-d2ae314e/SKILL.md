---
name: encode-repo-serena
version: 1.0.0
description: Systematically populate the Forgetful knowledge base using Serena's LSP-powered
  symbol analysis for accurate, comprehensive codebase understanding.
license: MIT
model: claude-sonnet-4-5
metadata:
  argument-hint: 'Project path or name to encode (default: current directory)'
---
# Encode Repository (Serena-Enhanced)

Transform an undocumented codebase into a rich, searchable knowledge repository using Serena's LSP-powered symbol analysis.

## Quick Start

```text
/encode-repo-serena
/encode-repo-serena ./my-project
"encode this repository"
"populate forgetful with this codebase"
```

| Input | Output | Duration |
|-------|--------|----------|
| Codebase path | Forgetful memories + entities + docs | 30-60 min |

## Prerequisites

1. **Serena plugin**: `claude plugins list | grep serena`
2. **Forgetful MCP**: Test with `execute_forgetful_tool("list_projects", {})`
3. If missing, run `/context-hub-setup` first

## Phase Overview

| Phase | Focus | Output |
|-------|-------|--------|
| **0** | Discovery | Project assessment, structure map |
| **1** | Foundation | 5-10 project overview memories |
| **1B** | Dependencies | 1-3 dependency memories |
| **2** | Symbols | 10-15 architecture memories |
| **2B** | Entities | Component entities + relationships |
| **3** | Patterns | 8-12 pattern memories |
| **4** | Features | 1-2 per critical feature |
| **5** | Decisions | Design decision memories |
| **6** | Artifacts | Code artifact storage |
| **6B** | Symbol Index | Document + entry memory |
| **7** | Documents | Long-form documentation |
| **7B** | Architecture | Architecture reference doc |

See [references/phases.md](references/phases.md) for full phase details.

## Memory Targets

| Profile | Total Memories | Documents | Entities |
|---------|----------------|-----------|----------|
| Small Simple | 17-31 | 2 | 3-5 |
| Small Complex | 28-46 | 2 | 5-10 |
| Medium | 38-66 | 2-3 | 10-20 |
| Large | 66-112 | 3-6 | 20-40 |

## Execution Order

```text
0 → 1 → 1B → 2 → 2B → 3 → 4 → 5 → 6 → 6B → 7 → 7B
```

**Guidelines**:

- Execute phases in order
- Use Serena's `find_symbol` and `find_referencing_symbols`
- Deduplicate entities before creating
- Link entities to memories bidirectionally
- Create entry memories for documents

## Quality Principles

| Principle | Description |
|-----------|-------------|
| Symbol-accurate | Use LSP data, not guesses |
| Atomic | One concept per memory |
| Size | 200-400 words ideal |
| Importance | Most should be 7-8 |
| Linking | Connect related memories |

## Validation Checklist

After completion:

- [ ] Test memory search: "How do I add a new API endpoint?"
- [ ] Test dependency query: "What dependencies does this project use?"
- [ ] List entities by project
- [ ] Verify entity relationships
- [ ] Check Symbol Index document exists
- [ ] Check Architecture Reference document exists
- [ ] Verify project.notes populated

See [references/validation.md](references/validation.md) for test commands.

## References

| Document | Content |
|----------|---------|
| [phases.md](references/phases.md) | Detailed phase workflows |
| [templates.md](references/templates.md) | Entity schemas, memory templates |
| [validation.md](references/validation.md) | Validation test commands |

## Related Skills

- `/context-hub-setup` - Setup Forgetful MCP
- `/using-forgetful-memory` - Memory best practices
- `/using-serena-symbols` - Serena symbol analysis
