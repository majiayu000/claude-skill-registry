---
name: logseq-to-obsidian
description: Migrate Logseq graphs to Obsidian vaults. Use when the user wants to convert their Logseq notes to Obsidian format, migrate from Logseq, or mentions both Logseq and Obsidian in a migration context. Handles property conversion, admonition blocks, block references, journal renaming, collapsed states, numbered lists, and image syntax. Designed for Claude Code usage from within the user's Logseq graph folder.
---

# Logseq to Obsidian Migration

Migrate Logseq graphs to clean Obsidian vaults while preserving content and structure.

## Workflow

### Step 1: Locate and Analyze the Graph

First, find the Logseq graph. Check current directory for `pages/` and `journals/` folders:

```bash
ls -la
```

If not in a Logseq graph, ask the user for the path.

Run the analysis script to detect patterns:

```bash
python3 scripts/analyze_graph.py /path/to/logseq/graph --json
```

This outputs a JSON report of detected features (admonitions, block refs, properties, namespaces, etc.).

### Step 2: Check for Existing Config

Check if a config file already exists:

```bash
cat /path/to/logseq/graph/.logseq-to-obsidian/config.json 2>/dev/null || echo "No config found"
```

If config exists, ask: "Found existing migration config. Use these settings, or reconfigure?"

If using existing config, skip to Step 4.

### Step 3: Gather Preferences and Write Config

Based on analysis, ask ONLY the questions that matter. Skip questions for features not detected.

**IMPORTANT: The AskUserQuestion tool has a maximum of 4 questions per call.** If you have more than 4 questions, ask in multiple rounds. Never skip questions.

#### Round 1 — Core questions (always ask)
1. Output folder location (default: `../obsidian-vault`)
2. "Keep all bullets or flatten top-level to paragraphs?" (recommend flatten for document-like notes)
3. "Place pages in vault root or in a `pages/` subfolder?" (recommend root — cleaner structure)
4. "Organize pages by parent?" (recommend yes — pages linked from only one parent get nested, reducing sidebar clutter)

#### Round 2 — Conditional questions (ask if detected, in a second AskUserQuestion call)
- **Namespaces found** → "Convert `Parent/Child` pages to folder hierarchy?"
- **Block references found** → "Flag block refs for manual fix, or remove?"

If no conditional questions are needed, skip Round 2.

#### Automatic defaults (never ask)
- Journals → `Daily/` folder, `YYYY-MM-DD.md` format
- Properties → YAML frontmatter
- Admonitions → Obsidian callouts
- `collapsed:: true` → Remove
- `logseq.order-list-type:: number` → Standard numbered lists
- Image sizing `{:height X, :width Y}` → Remove

After gathering preferences, create the config directory and write the config file:

```bash
mkdir -p /path/to/logseq/graph/.logseq-to-obsidian
```

Then use the Write tool to create `/path/to/logseq/graph/.logseq-to-obsidian/config.json`:

```json
{
  "version": 1,
  "source": "/absolute/path/to/logseq/graph",
  "output": "/absolute/path/to/obsidian/vault",
  "preferences": {
    "flattenTopLevel": false,
    "namespacesToFolders": false,
    "organizeByParent": false,
    "pagesInRoot": false,
    "blockRefs": "flag",
    "journalsFolder": "Daily"
  }
}
```

**Important:** Use absolute paths in the config file.

### Step 4: Run Dry-Run Migration

Always run dry-run first using the config:

```bash
python3 scripts/migrate.py --config /path/to/logseq/graph/.logseq-to-obsidian/config.json --dry-run
```

Show the user:
- Number of files to process
- Sample of 2-3 converted files (before/after)
- Any warnings or issues detected

### Step 5: Execute Migration

After user confirms:

```bash
python3 scripts/migrate.py --config /path/to/logseq/graph/.logseq-to-obsidian/config.json
```

The script:
1. Creates output directory structure
2. Processes all `.md` files in `pages/` and `journals/`
3. Copies `assets/` folder
4. Reports progress and any issues

### Step 6: Post-Migration Guidance

After migration, provide:

1. **Recommended Obsidian plugins** for Logseq refugees:
   - Calendar (visual calendar sidebar)
   - Periodic Notes (daily/weekly notes)
   - Outliner (folding, move items up/down)
   - Dataview (query notes, replaces Logseq queries)

2. **Manual fixes needed** (if any):
   - Block references flagged with `<!-- TODO: -->`
   - Logseq queries that need Dataview conversion

3. **Quick start**: "Open Obsidian → Open folder as vault → Select the output folder"

## Config File Reference

The config file is stored at `.logseq-to-obsidian/config.json` in the Logseq graph directory.

### Schema

```json
{
  "version": 1,
  "source": "/absolute/path/to/logseq/graph",
  "output": "/absolute/path/to/obsidian/vault",
  "preferences": {
    "flattenTopLevel": false,
    "namespacesToFolders": false,
    "organizeByParent": false,
    "pagesInRoot": false,
    "blockRefs": "flag",
    "journalsFolder": "Daily"
  }
}
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `version` | number | No | `1` | Config schema version |
| `source` | string | Yes | - | Absolute path to Logseq graph |
| `output` | string | Yes | - | Absolute path to output Obsidian vault |
| `preferences.flattenTopLevel` | boolean | No | `false` | Convert top-level bullets to paragraphs |
| `preferences.namespacesToFolders` | boolean | No | `false` | Convert `A/B` pages to folder hierarchy |
| `preferences.organizeByParent` | boolean | No | `false` | Nest pages under their parent's folder (pages with exactly 1 incoming link) |
| `preferences.pagesInRoot` | boolean | No | `false` | Place pages in vault root instead of `pages/` folder |
| `preferences.blockRefs` | string | No | `"flag"` | `"flag"` or `"remove"` |
| `preferences.journalsFolder` | string | No | `"Daily"` | Folder name for journal files |

### Re-running Migrations

Users can edit the config file directly and re-run without going through questions again:

```bash
python3 scripts/migrate.py --config .logseq-to-obsidian/config.json
```

Or via the Node wrapper:

```bash
logseq-to-obsidian --config .logseq-to-obsidian/config.json
```

## Conversion Reference

See `references/patterns.md` for complete Logseq→Obsidian syntax mappings.

## Script Options

### analyze_graph.py

```bash
python3 scripts/analyze_graph.py <logseq-path> [--sample-size N] [--json]
```

- `--sample-size`: Number of files to analyze (default: 50)
- `--json`: Output raw JSON only (for parsing)

### migrate.py

```bash
python3 scripts/migrate.py --config <config-file> [--dry-run] [--verbose]
python3 scripts/migrate.py <logseq-path> --output <obsidian-path> [options]
```

Config mode (recommended):
- `--config`: Path to config JSON file

CLI mode options:
- `--dry-run`: Preview without writing files
- `--journals-folder NAME`: Journal folder name (default: "Daily")
- `--flatten-top-level`: Convert top-level bullets to paragraphs
- `--namespaces-to-folders`: Convert `A/B` pages to `A/B.md` in folders
- `--organize-by-parent`: Nest pages under their parent's folder (pages linked from exactly one parent)
- `--pages-in-root`: Place pages in vault root instead of `pages/` folder
- `--block-refs [flag|remove]`: How to handle block references (default: flag)
- `--verbose`: Show detailed progress
