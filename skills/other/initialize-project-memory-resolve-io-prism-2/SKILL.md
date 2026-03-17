---
name: initialize-project-memory
description: Use to set up Obsidian vault and populate it with existing codebase knowledge. Enables context memory for AI development.
version: 1.0.0
---
# Task: Initialize Project Memory

Set up Obsidian vault and populate it with existing codebase knowledge.

## When to Use

- When setting up context memory for a new project
- When enabling AI-assisted development with persistent knowledge
- When migrating project knowledge to Obsidian format
- When starting a project that needs pattern tracking

## Quick Start

1. Install dependencies (`pip install python-frontmatter`)
2. Run `python skills/context-memory/utils/init_vault.py`
3. Verify vault created at `docs/memory/`
4. Optionally configure `PRISM_OBSIDIAN_VAULT` for custom location

## Prerequisites

- [ ] Python 3.10+ installed
- [ ] Obsidian installed (optional, for browsing)

## Steps

### 1. Install Dependencies

```bash
cd .prism
pip install python-frontmatter
```

### 2. Initialize Vault

```bash
python skills/context-memory/utils/init_vault.py
```

This creates:
- `docs/memory/` vault folder (at project root)
- Folder structure (Files, Patterns, Decisions, Commits, etc.)
- Index files (README, File Index, Pattern Index, Decision Log)
- `.gitignore` configuration

**Default location:** `docs/memory/` (one level up from `.prism/`)

**Custom location:** Set `PRISM_OBSIDIAN_VAULT` in `.env` file

### 3. Verify Setup

```bash
# Check vault exists (from project root)
ls -lh docs/memory/

# Check structure
ls docs/memory/PRISM-Memory/

# View stats
python -c "from skills.context-memory.utils.storage_obsidian import get_memory_stats; print(get_memory_stats())"
```

### 4. Enable Hooks

Create/update `.claude/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/capture-file-context-obsidian.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/capture-commit-context-obsidian.py"
          }
        ]
      }
    ]
  }
}
```

### 5. Interactive Analysis (Populate Initial Context)

Ask Claude Code to analyze key files:

```
"Please analyze the main entry points and core modules in this project"
```

Claude will:
- Read and analyze files using native tools
- Create markdown notes in the vault
- Organize by file path structure
- Capture patterns and architecture decisions

### 6. Enable REST API (Optional but Recommended)

For instant synchronization with Obsidian:

1. Install **Local REST API** plugin in Obsidian
2. Get API key from plugin settings
3. Configure `.prism/.env`:
   ```bash
   cd .prism
   cp .env.example .env
   # Edit .env and replace 'your-api-key-here' with your actual key
   ```
4. Test: `python skills/context-memory/utils/obsidian_rest_client.py`

**Security:** Never commit `.env` - it contains your personal API key!

**Benefits:** Instant updates in Obsidian, 10x faster search

See: `skills/context-memory/reference/obsidian-rest-api.md` for details

### 7. Open in Obsidian (Optional)

1. Launch Obsidian
2. File > Open vault
3. Select `docs/memory/` (from project root)
4. Explore the knowledge graph

### 8. Verify Results

```bash
# Check stats
python -c "from skills.context-memory.utils.storage_obsidian import get_memory_stats; import json; print(json.dumps(get_memory_stats(), indent=2))"

# Test search
python -c "from skills.context-memory.utils.storage_obsidian import recall_query; results = recall_query('authentication'); print(f'Found {len(results)} results')"

# Browse notes (from project root)
ls docs/memory/PRISM-Memory/Files/
ls docs/memory/PRISM-Memory/Patterns/
```

### 9. Automatic Capture is Now Active

With hooks enabled, all future edits are captured automatically:
- File changes â†’ Notes in `Files/`
- Git commits â†’ Notes in `Commits/`
- Context builds as you code
- No manual intervention needed

## Expected Results

After completion:
- Vault contains markdown notes for analyzed files
- Notes organized by file path structure
- Full-text search available
- Visual knowledge graph in Obsidian
- Hooks capture future changes automatically

## Vault Structure

```
docs/memory/PRISM-Memory/
â”œâ”€â”€ Files/              # File analyses (mirrors source structure)
â”‚   â””â”€â”€ src/
â”‚       â””â”€â”€ auth/
â”‚           â””â”€â”€ jwt.ts.md
â”œâ”€â”€ Patterns/           # Code patterns by category
â”‚   â””â”€â”€ Architecture/
â”‚       â””â”€â”€ Repository Pattern.md
â”œâ”€â”€ Decisions/          # Architectural decisions
â”‚   â””â”€â”€ 2025-01-15 Use JWT for Auth.md
â”œâ”€â”€ Commits/            # Git commits by month
â”‚   â””â”€â”€ 2025-01/
â”‚       â””â”€â”€ abc1234-add-authentication.md
â””â”€â”€ Index/              # Overview and navigation
    â”œâ”€â”€ README.md
    â”œâ”€â”€ File Index.md
    â””â”€â”€ Pattern Index.md
```

## Troubleshooting

### Vault Not Found
```
âŒ Vault does not exist: docs/memory
```
**Solution:** Run `python skills/context-memory/utils/init_vault.py` from `.prism/` directory

### Import Error
```
ModuleNotFoundError: No module named 'frontmatter'
```
**Solution:** Run `pip install python-frontmatter`

### Hook Not Capturing Files
**Check:**
- Verify hook paths in `.claude/hooks.json`
- Ensure vault exists at `docs/memory/` (from project root)
- Confirm file is source code (hooks skip .md, .json, etc.)
- Review `.prism-memory-log.txt` for errors
- Check REST API status in `.prism-memory-api-log.txt` (if using API)

### Notes Not Appearing in Obsidian
**Solution:**
- Close and reopen vault in Obsidian
- Check vault path matches in `.env`
- Verify files exist in filesystem

## Success Criteria

- [ ] Vault initialized with folder structure
- [ ] Can view markdown notes in filesystem
- [ ] Search returns relevant results
- [ ] Hooks enabled for automatic capture
- [ ] Obsidian opens vault successfully (optional)

## Next Steps

1. Browse vault in Obsidian to see knowledge graph
2. Use graph view (Ctrl+G) to visualize connections
3. Query context: `recall_query("authentication patterns")`
4. Continue development - context captures automatically
5. Link notes manually for better knowledge organization

## Benefits

- **Human-readable:** Browse notes in any text editor or Obsidian
- **Visual:** Graph view shows code relationships
- **Searchable:** Full-text search across all notes
- **Linkable:** Connect concepts with wikilinks
- **Git-friendly:** Markdown files work with version control

