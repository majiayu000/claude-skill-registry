---
name: obsidian-file-manager
description: >
  This skill should be used when managing documentation files in an Obsidian vault,
  including creating session artifacts, moving planning documents from project directories
  to the vault, updating document lifecycle states (active → processed → archived),
  searching for documents by tags or content, and automating archival of old documents.
  Integrates with task-startup/task-wrapup workflows for any coding project.
---

# Obsidian File Manager Skill

Automated file management for Obsidian vault integration via the Local REST API.

## Triggers

This skill should be used when:

- Creating session artifacts or documentation in the vault
- Moving planning documents from project directories to vault
- Updating document lifecycle states (active → processed → archived)
- Searching for documents by tags, project, or content
- Automating archival of old documents based on retention policies
- Managing documentation during task-startup/task-wrapup workflows

## Quick Start

### Prerequisites

1. Obsidian with Local REST API plugin installed and enabled
2. Ruby 2.7+ installed
3. API key configured in `config/.env`

### Setup

```bash
# Configure API key (get from Obsidian → Settings → Local REST API)
echo "OBSIDIAN_API_KEY=your-key" > ~/.claude/skills/obsidian-file-manager/config/.env
chmod 600 ~/.claude/skills/obsidian-file-manager/config/.env
```

## Operations

### create - Create new document

```bash
~/.claude/skills/obsidian-file-manager/scripts/create_in_vault.rb \
  --type session \
  --project myproject \
  --subject "feature implementation" \
  --content "# Session Notes\n\n..." \
  --lifecycle active
```

### move - Move file to vault

```bash
~/.claude/skills/obsidian-file-manager/scripts/move_to_vault.rb \
  --source /path/to/project/docs/plan.md \
  --type plan \
  --project myproject
```

### update-lifecycle - Change document state

```bash
~/.claude/skills/obsidian-file-manager/scripts/update_lifecycle.rb \
  --path sessions/myproject/session_myproject_20251124.md \
  --lifecycle processed
```

### search - Find documents

```bash
~/.claude/skills/obsidian-file-manager/scripts/search_vault.rb \
  --query "project:myproject lifecycle:active type:session"
```

### archive - Auto-archive old documents

```bash
~/.claude/skills/obsidian-file-manager/scripts/auto_archive.rb --dry-run
```

## Project Partitioning

Files are organized by type first, then by project:

```
{type}/{project}/filename.md
```

This enables multi-project support within a single vault. For example:
- `planning/softtrak/plan_softtrak_auth_system.md`
- `planning/myotherproject/plan_myotherproject_api_design.md`

## Document Types

| Type | Directory Pattern | Purpose |
|------|-------------------|---------|
| session | sessions/{project}/ | Development session artifacts |
| plan | planning/{project}/ | Implementation plans |
| prd | projects/{project}/ | Product requirements |
| adr, decision | decisions/{project}/ | Architecture decisions |
| investigation | investigations/{project}/ | Research and analysis |
| resource | resources/{project}/ | Reference materials |

## Lifecycle States

| State | Description | Auto-Archive |
|-------|-------------|--------------|
| master | Reference docs | Never |
| active | Currently in use | Never |
| processed | Work complete | After 30 days |
| trash | Abandoned | After 7 days |
| archived | Long-term storage | N/A |

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Configuration error |
| 3 | API error |
| 4 | Validation error |
| 5 | File operation error |

## Resources

For detailed documentation, see `references/`:

- `references/operations.md` - Full parameter documentation
- `references/configuration.md` - Config file reference
- `references/integration.md` - Workflow integration patterns
- `references/troubleshooting.md` - Common issues and solutions

## Scripts

All scripts are in `scripts/`:

- `create_in_vault.rb` - Create new documents
- `move_to_vault.rb` - Move files to vault
- `update_lifecycle.rb` - Change lifecycle state
- `search_vault.rb` - Search vault
- `auto_archive.rb` - Automatic archival

Core libraries in `scripts/lib/`:

- `obsidian_client.rb` - REST API wrapper
- `file_namer.rb` - Naming conventions
- `tag_manager.rb` - Tag/frontmatter utilities
