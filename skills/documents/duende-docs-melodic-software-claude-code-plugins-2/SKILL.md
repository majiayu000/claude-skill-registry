---
name: duende-docs
description: Single source of truth and librarian for ALL Duende Software documentation. Manages local documentation storage, scraping, discovery, and resolution. Use when finding, locating, searching, or resolving Duende documentation; discovering docs by keywords, category, tags, or natural language queries; scraping from llms-full.txt; managing index metadata (keywords, tags, aliases); or rebuilding index from filesystem. Run scripts to scrape, find, and resolve documentation. Handles doc_id resolution, keyword search, natural language queries, category/tag filtering, alias resolution, llms-full.txt parsing, markdown subsection extraction for internal use, hash-based drift detection, and comprehensive index maintenance.
allowed-tools: Read, Glob, Grep, Bash
---

# Duende Documentation Skill

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

- **`/duende-ecosystem:scrape-docs`** - Scrape Duende documentation from llms-full.txt
- **`/duende-ecosystem:refresh-docs`** - Refresh the local index and metadata without scraping
- **`/duende-ecosystem:validate-docs`** - Validate the index and references for consistency

## Overview

This skill provides automation tooling for Duende Software documentation management. It manages:

- **Canonical storage** (encapsulated in skill) - Single source of truth for official docs
- **Subsection extraction** - Token-optimized extracts (60-90% savings)
- **Drift detection** - Hash-based validation against upstream sources
- **Sync workflows** - Maintenance automation
- **Documentation discovery** - Keyword-based search and doc_id resolution
- **Index management** - Metadata, keywords, tags, aliases for resilient references

**Core value:** Prevents link rot, enables offline access, optimizes token costs, automates maintenance, and provides resilient doc_id-based references.

## When to Use This Skill

This skill should be used when:

- **Scraping documentation** - Fetching docs from Duende llms-full.txt
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

- **Run directly**: `python plugins/duende-ecosystem/skills/duende-docs/scripts/core/scrape_docs.py`
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
python plugins/duende-ecosystem/skills/duende-docs/scripts/management/refresh_index.py
```

### Scrape All Documentation

Use this when the user explicitly wants to **hit the network and scrape docs**:

```bash
# Scrape from llms-full.txt (all products in one file)
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/scrape_docs.py

# Refresh index after scraping
python plugins/duende-ecosystem/skills/duende-docs/scripts/management/refresh_index.py
```

### Find Documentation

```bash
# Resolve doc_id to file path
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/find_docs.py resolve <doc_id>

# Search by keywords (default: 25 results)
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/find_docs.py search oauth dpop

# Natural language search
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/find_docs.py query "how to configure DPoP"

# List by category
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/find_docs.py category identityserver

# List by tag
python plugins/duende-ecosystem/skills/duende-docs/scripts/core/find_docs.py tag bff
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

The duende-docs skill uses a unified configuration system.

**Configuration Files:**

- **`config/defaults.yaml`** - Central configuration file with all default values
- **`config/filtering.yaml`** - Content filtering rules
- **`config/tag_detection.yaml`** - Tag detection patterns

**Environment Variable Overrides:**

All configuration values can be overridden using environment variables: `DUENDE_DOCS_<SECTION>_<KEY>`

## Dependencies

**Required:** `pyyaml`, `requests`, `filelock`
**Optional (recommended):** `yake` (for keyword extraction)

**Python Version:** Python 3.11+ recommended

## Core Capabilities

### 1. Scraping Documentation

Fetch documentation from Duende llms-full.txt (pre-rendered markdown for all products).

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
MSYS_NO_PATHCONV=1 python scripts/core/scrape_docs.py --filter "/identityserver/"
```

## Troubleshooting

### Unicode Encoding Errors

**Status:** FIXED - Scripts auto-detect Windows and configure UTF-8 encoding.

### 404 Errors During Scraping

**Status:** EXPECTED - Some entries may reference docs that don't exist yet. Scripts handle gracefully and continue.

## Public API

The duende-docs skill provides a clean public API for external tools:

```python
from duende_docs_api import (
    find_document,
    resolve_doc_id,
    get_docs_by_tag,
    get_docs_by_category,
    search_by_keywords,
    get_document_section,
    refresh_index
)

# Natural language search
docs = find_document("DPoP token binding")

# Resolve doc_id to metadata
doc = resolve_doc_id("duende-identityserver-dpop")

# Get docs by tag
bff_docs = get_docs_by_tag("bff")

# Extract specific section
section = get_document_section("duende-identityserver-overview", "Installation")
```

## Development Mode

When developing this plugin locally, you may want changes to go to your dev repo instead of the installed plugin location.

### Enabling Dev Mode

**PowerShell:**

```powershell
$env:DUENDE_DOCS_DEV_ROOT = "D:\repos\gh\melodic\claude-code-plugins"
```

**Bash/Zsh:**

```bash
export DUENDE_DOCS_DEV_ROOT="/path/to/claude-code-plugins"
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
Remove-Item Env:DUENDE_DOCS_DEV_ROOT
```

**Bash/Zsh:**

```bash
unset DUENDE_DOCS_DEV_ROOT
```

## Directory Structure

```text
duende-docs/
  SKILL.md                    # This file (public)
  duende_docs_api.py          # Public API
  canonical/                  # Documentation storage (private)
    index.yaml                # Metadata index
    duendesoftware-com/       # Domain-based storage
      identityserver/         # IdentityServer docs
      bff/                    # BFF docs
      accesstokenmanagement/  # Access Token Management docs
      identitymodel/          # IdentityModel docs
      identitymodel-oidcclient/ # OidcClient docs
      general/                # General information docs
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

Documentation is scraped from Duende's llms-full.txt at <https://docs.duendesoftware.com/llms-full.txt>.

## Documentation Categories

Duende documentation is organized into the following categories:

| Category | Description |
| --- | --- |
| identityserver | IdentityServer OAuth 2.0/OIDC framework documentation |
| bff | Backend-for-Frontend security framework |
| accesstokenmanagement | Access token lifecycle management library |
| identitymodel | Protocol operations library |
| identitymodel-oidcclient | Native OIDC client library |
| general | Licensing, support, glossary, shared concepts |

## Tags

Common tags used for Duende documentation:

- `oauth` - OAuth 2.0 protocol
- `oidc` - OpenID Connect protocol
- `openid-connect` - OpenID Connect (alias)
- `tokens` - Token handling
- `access-token` - Access token management
- `refresh-token` - Refresh token handling
- `bff` - Backend-for-Frontend pattern
- `spa` - Single-page application security
- `blazor` - Blazor integration
- `aspnetcore` - ASP.NET Core integration
- `dotnet` - .NET framework
- `authentication` - Authentication flows
- `authorization` - Authorization policies
- `dpop` - DPoP token binding
- `mtls` - Mutual TLS authentication
- `client-credentials` - Client credentials flow
- `quickstart` - Getting started guides
- `sample-code` - Code samples and examples

## Test Scenarios

### Scenario 1: Keyword Search

**Query**: "Search for DPoP documentation"
**Expected Behavior**:

- Skill activates on keyword "DPoP"
- Returns relevant docs from index
**Success Criteria**: User receives matching documentation entries

### Scenario 2: Natural Language Query

**Query**: "How do I configure IdentityServer for Blazor?"
**Expected Behavior**:

- Skill activates on "IdentityServer" and "Blazor"
- Uses find_docs.py query command
**Success Criteria**: Returns relevant documentation with configuration steps

### Scenario 3: Doc ID Resolution

**Query**: "Resolve duende-identityserver-quickstart"
**Expected Behavior**:

- Resolves doc_id to file path
- Returns document metadata
**Success Criteria**: User receives full path and document content

## Version History

- v1.0.0 (2025-12-16): Initial release - full skill structure

## Last Updated

**Date:** 2025-12-16
**Model:** claude-opus-4-5-20251101

**Status:** Initial release - ready for scraping from <https://docs.duendesoftware.com/llms-full.txt>.
