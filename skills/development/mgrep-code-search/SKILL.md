---
name: searching-with-mgrep
description: Performs semantic code search using mgrep for natural language queries across codebases. Use when exploring codebases with 30+ files, searching for concepts rather than exact strings, or understanding unfamiliar code. Triggers include "semantic search", "mgrep", "find feature", or "where is X implemented".
allowed-tools: Bash, Read
user-invocable: false
---

# mgrep Code Search

## Overview

mgrep is a semantic search tool that enables natural language queries across code, text, PDFs, and images. It is particularly effective for exploring larger or complex codebases where traditional pattern matching falls short.

## When to Use This Skill

Use mgrep when:

- The codebase contains more than 30 non-gitignored files
- There are nested directory structures
- Searching for concepts, features, or intent rather than exact strings
- Exploring an unfamiliar codebase
- Need to understand "where" or "how" something is implemented

Use traditional grep/ripgrep when:

- Searching for exact patterns or symbols
- Regex-based refactoring
- Tracing specific function or variable names

## Quick Start

### Indexing

Before searching, start the watcher to index the repository:

```bash
bunx @mixedbread/mgrep watch
```

The `watch` command indexes the repository and maintains synchronisation with file changes. It respects `.gitignore` and `.mgrepignore` patterns.

### Searching

```bash
bunx @mixedbread/mgrep "your natural language query" [path]
```

## Search Commands

### Basic Search

```bash
bunx @mixedbread/mgrep "where is authentication configured?"
bunx @mixedbread/mgrep "how do we handle errors in API calls?" src/
bunx @mixedbread/mgrep "database connection setup" src/lib
```

### Search Options

| Option          | Description                              |
| --------------- | ---------------------------------------- |
| `-m <count>`    | Maximum results (default: 10)            |
| `-c, --content` | Display full result content              |
| `-a, --answer`  | Generate AI-powered synthesis of results |
| `-s, --sync`    | Update index before searching            |
| `--no-rerank`   | Disable relevance optimisation           |

### Examples with Options

```bash
# Get more results
bunx @mixedbread/mgrep -m 25 "user authentication flow"

# Show full content of matches
bunx @mixedbread/mgrep -c "error handling patterns"

# Get an AI-synthesised answer
bunx @mixedbread/mgrep -a "how does the caching layer work?"

# Sync index before searching
bunx @mixedbread/mgrep -s "payment processing" src/services
```

## Workflow

1. **Start watcher** (once per session or when files change significantly):

   ```bash
   bunx @mixedbread/mgrep watch
   ```

1. **Search semantically**:

   ```bash
   bunx @mixedbread/mgrep "what you're looking for" [optional/path]
   ```

1. **Refine as needed** using path constraints or options:

   ```bash
   bunx @mixedbread/mgrep -m 20 -c "refined query" src/specific/directory
   ```

## Environment Variables

Configure defaults via environment variables:

| Variable          | Purpose                         |
| ----------------- | ------------------------------- |
| `MGREP_MAX_COUNT` | Default result limit            |
| `MGREP_CONTENT`   | Enable content display (1/true) |
| `MGREP_ANSWER`    | Enable AI synthesis (1/true)    |
| `MGREP_SYNC`      | Pre-search sync (1/true)        |

## Important Notes

- Always use `bunx @mixedbread/mgrep` to run commands (not npm/bunx or direct installation)
- Run `bunx @mixedbread/mgrep watch` before searching to ensure the index is current
- mgrep respects `.gitignore` patterns automatically
- Create `.mgrepignore` for additional exclusions
