---
name: codex-cli-docs
description: Single source of truth and librarian for ALL OpenAI Codex CLI documentation. Manages local documentation storage, scraping, discovery, and resolution. Use when finding, locating, searching, or resolving Codex CLI documentation; discovering docs by keywords, category, tags, or natural language queries; scraping from llms.txt; managing index metadata (keywords, tags, aliases); or rebuilding index from filesystem. Run scripts to scrape, find, and resolve documentation. Handles doc_id resolution, keyword search, natural language queries, category/tag filtering, alias resolution, llms.txt parsing, markdown subsection extraction for internal use, hash-based drift detection, and comprehensive index maintenance.
allowed-tools: Read, Glob, Grep, Bash
---

# OpenAI Codex CLI Documentation Skill

## CRITICAL: Path Doubling Prevention - MANDATORY

**ABSOLUTE PROHIBITION: NEVER use `cd` with `&&` in PowerShell when running scripts from this skill.**

**The Problem:** If your current working directory is already inside the skill directory, using relative paths causes PowerShell to resolve paths relative to the current directory instead of the repository root, resulting in path doubling.

**REQUIRED Solutions (choose one):**

1. **ALWAYS use absolute paths** (recommended)
2. **Use separate commands** (never `cd` with `&&`)
3. **Run from repository root** with relative paths

**NEVER DO THIS:**

- Chain `cd` with `&&`: `cd <relative-path> && python <script>` causes path doubling
- Assume current directory
- Use relative paths when current dir is inside skill directory

## CRITICAL: Large File Handling - MANDATORY SCRIPT USAGE

### ABSOLUTE PROHIBITION: NEVER use read_file tool on the index.yaml file

The file exceeds context limits and will cause issues. You MUST use scripts.

**REQUIRED: ALWAYS use manage_index.py scripts for ANY index.yaml access:**

```bash
python scripts/management/manage_index.py count
python scripts/management/manage_index.py list
python scripts/management/manage_index.py get <doc_id>
python scripts/management/manage_index.py verify
```

All scripts automatically handle large files via `index_manager.py`.

## Available Slash Commands

This skill provides slash commands for common workflows (once plugin commands are created):

- **`/openai-ecosystem:scrape-docs`** - Scrape Codex CLI documentation from llms.txt sources
- **`/openai-ecosystem:refresh-docs`** - Refresh the local index and metadata without scraping
- **`/openai-ecosystem:validate-docs`** - Validate the index and references for consistency

## Overview

This skill provides automation tooling for OpenAI Codex CLI documentation management. It manages:

- **Canonical storage** (encapsulated in skill) - Single source of truth for official docs
- **Subsection extraction** - Token-optimized extracts (60-90% savings)
- **Drift detection** - Hash-based validation against upstream sources
- **Sync workflows** - Maintenance automation
- **Documentation discovery** - Keyword-based search and doc_id resolution
- **Index management** - Metadata, keywords, tags, aliases for resilient references

**Core value:** Prevents link rot, enables offline access, optimizes token costs, automates maintenance, and provides resilient doc_id-based references.

## When to Use This Skill

This skill should be used when:

- **Scraping documentation** - Fetching docs from OpenAI Codex CLI sources
- **Finding documentation** - Searching for docs by keywords, category, or natural language
- **Resolving doc references** - Converting doc_id to file paths
- **Managing index metadata** - Adding keywords, tags, aliases, updating metadata
- **Rebuilding index** - Regenerating index from filesystem (handles renames/moves)

## Workflow Execution Pattern

**CRITICAL: This section defines HOW to execute operations in this skill.**

### Delegation Strategy

#### Default approach: Delegate to Task agent

For ALL scraping, validation, and index operations, delegate execution to a general-purpose Task agent.

**How to invoke:**

Use the Task tool with:

- `subagent_type`: "general-purpose"
- `description`: Short 3-5 word description
- `prompt`: Full task description with execution instructions

### Execution Pattern

**Scripts run in FOREGROUND by default. Do NOT background them.**

When Task agents execute scripts:

- **Run directly**: `python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/scrape_docs.py`
- **Streaming logs**: Scripts emit progress naturally via stdout
- **Wait for completion**: Scripts exit when done with exit code
- **NEVER use `run_in_background=true`**: Scripts are designed for foreground execution
- **NEVER poll output**: Streaming logs appear automatically, no BashOutput polling needed
- **NEVER use background jobs**: No `&`, no `nohup`, no background process management

### Error and Warning Reporting

**CRITICAL: Report ALL errors, warnings, and issues - never suppress or ignore them.**

When executing scripts via Task agents:

- **Report script errors**: Exit codes, exceptions, error messages
- **Report warnings**: Deprecation warnings, import issues, configuration problems
- **Report unexpected output**: 404s, timeouts, validation failures
- **Include context**: What was being executed when the error occurred

## Quick Start

### Refresh Index End-to-End (No Scraping)

Use this when you want to rebuild and validate the local index/metadata **without scraping**:

```bash
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/management/refresh_index.py
```

### Scrape All Documentation

Use this when the user explicitly wants to **hit the network and scrape docs**:

```bash
# Scrape from configured llms.txt sources
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/scrape_docs.py

# Refresh index after scraping
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/management/refresh_index.py
```

### Find Documentation

```bash
# Resolve doc_id to file path
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/find_docs.py resolve <doc_id>

# Search by keywords (default: 25 results)
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/find_docs.py search sandbox tools

# Natural language search
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/find_docs.py query "how to configure sandbox"

# List by category
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/find_docs.py category guides

# List by tag
python plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/find_docs.py tag cli
```

**Search Options:**

| Option | Default | Description |
| --- | --- | --- |
| `--limit N` | 25 | Maximum number of results to return |
| `--no-limit` | - | Return all matching results (no limit) |
| `--min-score N` | - | Only return results with relevance score >= N |
| `--fast` | - | Index-only search (skip content grep) |
| `--json` | - | Output results as JSON |
| `--verbose` | - | Show relevance scores |

## Configuration System

The codex-cli-docs skill uses a unified configuration system.

**Configuration Files:**

- **`config/defaults.yaml`** - Central configuration file with all default values
- **`config/filtering.yaml`** - Content filtering rules
- **`config/tag_detection.yaml`** - Tag detection patterns
- **`references/sources.json`** - Documentation sources configuration

**Environment Variable Overrides:**

All configuration values can be overridden using environment variables: `CODEX_DOCS_<SECTION>_<KEY>`

## Dependencies

**Required:** `pyyaml`, `requests`, `beautifulsoup4`, `markdownify`, `filelock`
**Optional (recommended):** `yake` (for keyword extraction)

**Python Version:** Python 3.11+ recommended

## Core Capabilities

### 1. Scraping Documentation

Fetch documentation from configured sources using llms.txt format.

### 2. Extracting Subsections

Extract specific markdown sections for token-optimized responses.

### 3. Change Detection

Detect documentation drift via 404 checking and hash comparison.

### 4. Finding and Resolving Documentation

Discover and resolve documentation references using doc_id, keywords, or natural language queries.

### 5. Index Management and Maintenance

Maintain index metadata, keywords, tags, and rebuild index from filesystem.

## Platform-Specific Requirements

### Windows Users

**MUST use PowerShell (recommended) or prefix Git Bash commands with `MSYS_NO_PATHCONV=1`**

Git Bash on Windows converts Unix paths to Windows paths, breaking filter patterns.

**Example:**

```bash
MSYS_NO_PATHCONV=1 python scripts/core/scrape_docs.py --filter "/docs/"
```

## Troubleshooting

### Unicode Encoding Errors

**Status:** FIXED - Scripts auto-detect Windows and configure UTF-8 encoding.

### 404 Errors During Scraping

**Status:** EXPECTED - Some llms.txt entries may reference docs that don't exist yet. Scripts handle gracefully and continue.

## Public API

The codex-cli-docs skill provides a clean public API for external tools:

```python
from codex_docs_api import (
    find_document,
    resolve_doc_id,
    get_docs_by_tag,
    get_docs_by_category,
    search_by_keywords,
    get_document_section,
    detect_drift,
    refresh_index
)

# Natural language search
docs = find_document("sandbox configuration")

# Resolve doc_id to metadata
doc = resolve_doc_id("codex-cli-docs-getting-started")

# Get docs by tag
cli_docs = get_docs_by_tag("cli")

# Extract specific section
section = get_document_section("codex-cli-overview", "Installation")
```

## Development Mode

When developing this plugin locally, you may want changes to go to your dev repo instead of the installed plugin location.

### Enabling Dev Mode

**PowerShell:**

```powershell
$env:CODEX_DOCS_DEV_ROOT = "D:\repos\gh\melodic\claude-code-plugins"
```

**Bash/Zsh:**

```bash
export CODEX_DOCS_DEV_ROOT="/path/to/claude-code-plugins"
```

### Verifying Mode

When you run any major script (scrape, refresh, rebuild), a mode banner will display:

**Dev mode:**

```text
[DEV MODE] Using local plugin: D:\repos\gh\melodic\claude-code-plugins
```

**Prod mode:**

```text
[PROD MODE] Using installed skill directory
```

### Disabling Dev Mode

**PowerShell:**

```powershell
Remove-Item Env:CODEX_DOCS_DEV_ROOT
```

**Bash/Zsh:**

```bash
unset CODEX_DOCS_DEV_ROOT
```

## Directory Structure

```text
codex-cli-docs/
  SKILL.md                    # This file (public)
  codex_docs_api.py           # Public API
  canonical/                  # Documentation storage (private)
    index.yaml                # Metadata index
  scripts/                    # Implementation (private)
    core/                     # Scraping, discovery
    management/               # Index management
    maintenance/              # Cleanup, drift detection
    utils/                    # Shared utilities
  config/                     # Configuration
    defaults.yaml             # Default settings
    filtering.yaml            # Content filtering
    tag_detection.yaml        # Tag patterns
  references/                 # Technical documentation (public)
    sources.json              # Documentation sources
  .cache/                     # Cache storage (inverted index)
  logs/                       # Log files
```

## Source

Documentation is scraped from OpenAI Codex CLI llms.txt sources (configured in sources.json).

## Test Scenarios

### Scenario 1: Keyword Search

**Query**: "Search for sandbox documentation"
**Expected Behavior**:

- Skill activates on keyword "documentation"
- Returns relevant docs from index
**Success Criteria**: User receives matching documentation entries

### Scenario 2: Natural Language Query

**Query**: "How do I configure the Codex CLI sandbox?"
**Expected Behavior**:

- Skill activates on "Codex CLI"
- Uses find_docs.py query command
**Success Criteria**: Returns relevant documentation with configuration steps

### Scenario 3: Doc ID Resolution

**Query**: "Resolve codex-cli-getting-started"
**Expected Behavior**:

- Resolves doc_id to file path
- Returns document metadata
**Success Criteria**: User receives full path and document content

## Version History

- v1.0.0 (2025-12-15): Initial release - full skill structure adapted from gemini-cli-docs

## Last Updated

**Date:** 2025-12-15
**Model:** claude-opus-4-5-20251101

**Status:** Initial release - awaiting llms.txt source configuration for scraping.
