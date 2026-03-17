---
name: gemini-cli-docs
description: Single source of truth and librarian for ALL Gemini CLI documentation. Manages local documentation storage, scraping, discovery, and resolution. Use when finding, locating, searching, or resolving Gemini CLI documentation; discovering docs by keywords, category, tags, or natural language queries; scraping from llms.txt; managing index metadata (keywords, tags, aliases); or rebuilding index from filesystem. Run scripts to scrape, find, and resolve documentation. Handles doc_id resolution, keyword search, natural language queries, category/tag filtering, alias resolution, llms.txt parsing, markdown subsection extraction for internal use, hash-based drift detection, and comprehensive index maintenance.
allowed-tools: Read, Glob, Grep, Bash
---

# Gemini CLI Documentation Skill

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

This skill provides three slash commands for common workflows:

- **`/google-ecosystem:scrape-docs`** - Scrape Gemini CLI documentation from geminicli.com, then refresh index and validate
- **`/google-ecosystem:refresh-docs`** - Refresh the local index and metadata without scraping from remote sources
- **`/google-ecosystem:validate-docs`** - Validate the index and references for consistency and drift without scraping

## Overview

This skill provides automation tooling for Gemini CLI documentation management. It manages:

- **Canonical storage** (encapsulated in skill) - Single source of truth for official docs
- **Subsection extraction** - Token-optimized extracts (60-90% savings)
- **Drift detection** - Hash-based validation against upstream sources
- **Sync workflows** - Maintenance automation
- **Documentation discovery** - Keyword-based search and doc_id resolution
- **Index management** - Metadata, keywords, tags, aliases for resilient references

**Core value:** Prevents link rot, enables offline access, optimizes token costs, automates maintenance, and provides resilient doc_id-based references.

## When to Use This Skill

This skill should be used when:

- **Scraping documentation** - Fetching docs from geminicli.com llms.txt
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

- **Run directly**: `python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/scrape_docs.py --llms-txt https://geminicli.com/llms.txt`
- **Streaming logs**: Scripts emit progress naturally via stdout
- **Wait for completion**: Scripts exit when done with exit code
- **NEVER use `run_in_background=true`**: Scripts are designed for foreground execution
- **NEVER poll output**: Streaming logs appear automatically, no BashOutput polling needed
- **NEVER use background jobs**: No `&`, no `nohup`, no background process management

### Anti-Pattern Detection

**Red flags indicating incorrect execution:**

- Using `run_in_background=true` in Bash tool
- Repeated BashOutput calls in a loop
- Checking process status with `ps` or `pgrep`
- Manual polling of script output
- Background job management (`&`, `nohup`, `jobs`)
- **Using BashOutput AFTER Task agent completes**

**If you recognize these patterns, STOP and correct immediately.**

### Error and Warning Reporting

**CRITICAL: Report ALL errors, warnings, and issues - never suppress or ignore them.**

When executing scripts via Task agents:

- **Report script errors**: Exit codes, exceptions, error messages
- **Report warnings**: Deprecation warnings, import issues, configuration problems
- **Report unexpected output**: 404s, timeouts, validation failures
- **Include context**: What was being executed when the error occurred

**Red flags that indicate issues:**

- Non-zero exit code
- Lines containing "ERROR", "FAILED", "Exception", "Traceback"
- "WARNING" or "WARN" messages
- "404 Not Found", "500 Internal Server Error"

## Quick Start

### Refresh Index End-to-End (No Scraping)

Use this when you want to rebuild and validate the local index/metadata **without scraping**:

**Use Python 3.13 for validation** - spaCy/Pydantic have compatibility issues with Python 3.14+

```bash
# Use Python 3.13 for full compatibility with spaCy
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/management/manage_index.py refresh
```

### Scrape All Documentation

Use this when the user explicitly wants to **hit the network and scrape docs**:

```bash
# Scrape from llms.txt
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/scrape_docs.py \
  --llms-txt https://geminicli.com/llms.txt

# Refresh index after scraping (use Python 3.13)
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/management/manage_index.py refresh
```

**With options:**

```bash
# Skip existing files (incremental update)
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/scrape_docs.py \
  --llms-txt https://geminicli.com/llms.txt \
  --skip-existing

# Filter to specific section
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/scrape_docs.py \
  --llms-txt https://geminicli.com/llms.txt \
  --filter "/docs/"
```

### Find Documentation

```bash
# Resolve doc_id to file path
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py resolve <doc_id>

# Search by keywords (default: 25 results)
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py search checkpointing session

# Search with custom limit
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py --limit 10 search tools

# Natural language search
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py query "how to use checkpointing"

# List by category
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py category docs

# List by tag
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/find_docs.py tag cli
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

The gemini-cli-docs skill uses a unified configuration system with a single source of truth.

**Configuration Files:**

- **`config/defaults.yaml`** - Central configuration file with all default values
- **`config/config_registry.py`** - Canonical configuration system with environment variable support
- **`config/filtering.yaml`** - Content filtering rules
- **`config/tag_detection.yaml`** - Tag detection patterns
- **`references/sources.json`** - Documentation sources configuration

**Environment Variable Overrides:**

All configuration values can be overridden using environment variables: `GEMINI_DOCS_<SECTION>_<KEY>`

**Full details:** [references/configuration.md](references/configuration.md)

## Dependencies

**Required:** `pyyaml`, `requests`, `beautifulsoup4`, `markdownify`, `filelock`
**Optional (recommended):** `spacy` with `en_core_web_sm` model (for keyword extraction)

**Check dependencies:**

```bash
python plugins/google-ecosystem/skills/gemini-cli-docs/scripts/setup/check_dependencies.py
```

**Python Version:** Python 3.13 recommended (required for spaCy operations)

**Full details:** [references/dependencies.md](references/dependencies.md)

## Core Capabilities

### 1. Scraping Documentation

Fetch documentation from geminicli.com using llms.txt format. Features: llms.txt parsing, HTML to Markdown conversion, automatic metadata tracking, URL-based folder organization.

**Guide:** [references/capabilities/scraping-guide.md](references/capabilities/scraping-guide.md)

### 2. Extracting Subsections

Extract specific markdown sections for token-optimized responses. Features: ATX-style heading structure parsing, section boundaries detection, provenance frontmatter, token economics (60-90% savings typical).

**Guide:** [references/capabilities/extraction-guide.md](references/capabilities/extraction-guide.md)

### 3. Change Detection

Detect documentation drift via 404 checking and hash comparison. Features: 404 URL detection, missing file detection, content hash comparison, orphaned file detection, cleanup automation.

**Guide:** [references/capabilities/change-detection-guide.md](references/capabilities/change-detection-guide.md)

### 4. Finding and Resolving Documentation

Discover and resolve documentation references using doc_id, keywords, or natural language queries. Features: doc_id resolution, keyword-based search, natural language query processing, category and tag filtering.

**Guide:** [references/capabilities/discovery-guide.md](references/capabilities/discovery-guide.md)

### 5. Index Management and Maintenance

Maintain index metadata, keywords, tags, and rebuild index from filesystem.

**Guide:** [references/capabilities/index-management-guide.md](references/capabilities/index-management-guide.md)

## Workflows

Common maintenance and operational workflows:

- **Scraping Gemini CLI Documentation** - Fetching docs from geminicli.com
- **Refreshing the Index** - Rebuilding metadata after changes
- **Detecting and Cleaning Drift** - Finding and removing stale docs
- **Adding Documentation Categories** - Onboarding new doc sections

**Detailed Workflows:** [references/workflows.md](references/workflows.md)

## Metadata & Keyword Audit Workflows

**Quick validation:**

```bash
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/validation/quick_validate.py
```

**Search audit:**

```bash
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/validation/run_search_audit.py
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/validation/analyze_search_audit.py
```

**Tag configuration audit:**

```bash
py -3.13 plugins/google-ecosystem/skills/gemini-cli-docs/scripts/validation/audit_tag_config.py
```

## Platform-Specific Requirements

### Windows Users

**MUST use PowerShell (recommended) or prefix Git Bash commands with `MSYS_NO_PATHCONV=1`**

Git Bash on Windows converts Unix paths to Windows paths, breaking filter patterns.

**Example:**

```bash
MSYS_NO_PATHCONV=1 python scripts/core/scrape_docs.py \
    --llms-txt https://geminicli.com/llms.txt \
    --filter "/docs/"
```

**See:** [references/troubleshooting.md#git-bash-path-conversion](references/troubleshooting.md)

## Troubleshooting

### spaCy Installation Issues

**Problem:** spaCy installation fails with Python 3.14+.

**Solution:** Use Python 3.13:

```bash
py -3.13 -m pip install spacy
py -3.13 -m spacy download en_core_web_sm
```

### Unicode Encoding Errors

**Status:** FIXED - Scripts auto-detect Windows and configure UTF-8 encoding.

### 404 Errors During Scraping

**Status:** EXPECTED - Some llms.txt entries may reference docs that don't exist yet. Scripts handle gracefully and continue.

**Full troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)

## Public API

The gemini-cli-docs skill provides a clean public API for external tools:

```python
from gemini_docs_api import (
    find_document,
    resolve_doc_id,
    get_docs_by_tag,
    get_docs_by_category,
    search_by_keywords,
    get_document_section,
    detect_drift,
    cleanup_drift,
    refresh_index
)

# Natural language search
docs = find_document("model routing configuration")

# Resolve doc_id to metadata
doc = resolve_doc_id("geminicli-com-docs-checkpointing")

# Get docs by tag
cli_docs = get_docs_by_tag("cli")

# Extract specific section
section = get_document_section("geminicli-com-docs-commands", "Built-in Commands")

# Detect drift
drift = detect_drift(check_404s=True, check_hashes=True)

# Cleanup drift (dry run first)
result = cleanup_drift(clean_404s=True, dry_run=True)

# Refresh index with drift detection
result = refresh_index(check_drift=True, cleanup_drift=False)
```

## Plugin Maintenance

For plugin-specific maintenance workflows:

**See:** [references/plugin-maintenance.md](references/plugin-maintenance.md)

Quick reference:

- **Update workflow**: Scrape -> Validate -> Review -> Commit -> Version bump -> Push
- **Version bumps**: Patch for doc refresh, Minor for new features, Major for breaking changes
- **Testing**: Run `manage_index.py verify` and test search before pushing

## Development Mode

When developing this plugin locally, you may want changes to go to your dev repo instead of the installed plugin location.

### Enabling Dev Mode

**PowerShell:**

```powershell
$env:GEMINI_DOCS_DEV_ROOT = "D:\repos\gh\melodic\claude-code-plugins"
```

**Bash/Zsh:**

```bash
export GEMINI_DOCS_DEV_ROOT="/path/to/claude-code-plugins"
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
Remove-Item Env:GEMINI_DOCS_DEV_ROOT
```

**Bash/Zsh:**

```bash
unset GEMINI_DOCS_DEV_ROOT
```

## Documentation Categories

| Category | Topics |
| --- | --- |
| Get Started | installation, authentication, configuration, quickstart |
| CLI | commands, settings, themes, checkpointing, telemetry, trusted folders |
| Core | architecture, tools API, policy engine, memport |
| Tools | file system, shell, web fetch, web search, memory tool, MCP servers |
| Extensions | creating, managing, releasing extensions |
| IDE | VS Code, JetBrains, IDE companion |

## Gemini CLI Features

Key features documented:

- **Checkpointing**: File state snapshots, session management, rewind
- **Model Routing**: Flash vs Pro selection, automatic routing
- **Token Caching**: Prompt compression, cost optimization
- **Policy Engine**: Security controls, trusted folders
- **Memport**: Memory import/export
- **MCP Servers**: Model Context Protocol integration
- **Extensions**: Plugin system for CLI
- **Sandbox**: Isolated execution environment

## Directory Structure

```
gemini-cli-docs/
  SKILL.md                    # This file (public)
  gemini_docs_api.py          # Public API
  canonical/                  # Documentation storage (private)
    geminicli-com/            # Scraped from geminicli.com
    index.yaml                # Metadata index
    index.json                # JSON mirror
  scripts/                    # Implementation (private)
    core/                     # Scraping, discovery
    management/               # Index management
    maintenance/              # Cleanup, drift detection
    validation/               # Validation scripts
    utils/                    # Shared utilities
    setup/                    # Setup scripts
  config/                     # Configuration
    defaults.yaml             # Default settings
    filtering.yaml            # Content filtering
    tag_detection.yaml        # Tag patterns
  references/                 # Technical documentation (public)
    technical-details.md
    workflows.md
    troubleshooting.md
    plugin-maintenance.md
    configuration.md
    dependencies.md
    capabilities/
      scraping-guide.md
      extraction-guide.md
      change-detection-guide.md
      discovery-guide.md
      index-management-guide.md
  .cache/                     # Cache storage (inverted index)
  logs/                       # Log files
```

## Related Documentation

- **[references/technical-details.md](references/technical-details.md)** - Architecture and internals
- **[references/workflows.md](references/workflows.md)** - Common operational workflows
- **[references/troubleshooting.md](references/troubleshooting.md)** - Problem resolution
- **[references/plugin-maintenance.md](references/plugin-maintenance.md)** - Plugin update workflows
- **[references/configuration.md](references/configuration.md)** - Configuration reference
- **[references/dependencies.md](references/dependencies.md)** - Dependency management

## Source

Documentation is scraped from: https://geminicli.com/llms.txt

## Test Scenarios

### Scenario 1: Keyword Search

**Query**: "Search for checkpointing documentation"
**Expected Behavior**:

- Skill activates on keyword "documentation"
- Returns relevant docs from index
**Success Criteria**: User receives matching documentation entries

### Scenario 2: Natural Language Query

**Query**: "How do I configure model routing in Gemini CLI?"
**Expected Behavior**:

- Skill activates on "Gemini CLI"
- Uses find_docs.py query command
**Success Criteria**: Returns relevant documentation with configuration steps

### Scenario 3: Doc ID Resolution

**Query**: "Resolve geminicli-com-docs-checkpointing"
**Expected Behavior**:

- Resolves doc_id to file path
- Returns document metadata
**Success Criteria**: User receives full path and document content

### Scenario 4: Drift Detection

**Query**: "Check for stale documentation"
**Expected Behavior**:

- Runs drift detection script
- Reports 404 URLs, missing files, hash mismatches
**Success Criteria**: User receives drift report with actionable items

### Scenario 5: Section Extraction

**Query**: "Get the 'Built-in Commands' section from the commands doc"
**Expected Behavior**:

- Extracts specific section from document
- Returns only the requested content
**Success Criteria**: User receives targeted section, not full document

## Version History

- v2.0.0 (2025-12-05): Full feature parity with docs-management - added maintenance scripts, validation scripts, enhanced API, comprehensive documentation
- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101

**Status:** Production-ready with full feature parity to docs-management skill.
