---
name: kodex-init
description: Bootstrap a Kodex knowledge base by analyzing codebase structure and creating topic stubs
user-invocable: true
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__kodex_create_topic
  - mcp__plugin_mermaid-collab_mermaid__kodex_list_topics
  - mcp__plugin_mermaid-collab_mermaid__kodex_flag_topic
---

# Kodex Init

Bootstrap a Kodex knowledge base by analyzing codebase structure and creating topic stubs.

## Overview

This skill analyzes a codebase to identify logical topic boundaries and creates stub topics in the Kodex knowledge base. Topics are created as drafts requiring human approval before going live.

**Use when:**
- Setting up Kodex for a new project
- Onboarding to an unfamiliar codebase
- Refreshing topic coverage after major refactoring

---

## Step 1: Explore Codebase Structure

Walk the directory tree to understand the project structure.

### 1.1 List Top-Level Directories

```bash
ls -d */ 2>/dev/null | grep -v -E '^(node_modules|vendor|\.git|dist|build|out|coverage|__pycache__|\.)'
```

### 1.2 Check Framework Indicators

Look for these files to identify the tech stack:
- `package.json` → Node.js/React/Vue
- `pubspec.yaml` → Flutter/Dart
- `Cargo.toml` → Rust
- `go.mod` → Go
- `*.csproj` → .NET
- `requirements.txt` / `pyproject.toml` → Python

### 1.3 Check Infrastructure Files

- `Dockerfile`, `docker-compose.yml` → deployment topic
- `.github/workflows/`, `.gitlab-ci.yml` → ci-cd topic
- `jest.config.*`, `vitest.config.*`, `pytest.ini` → testing topic
- `.env`, `config/` → configuration topic

### Exclusion Patterns

**Always exclude:**
- `node_modules/`, `vendor/`, `.git/`
- `dist/`, `build/`, `out/`, `coverage/`
- `__pycache__/`, `.cache/`
- Hidden directories (starting with `.`)
- Binary and generated files

---

## Step 2: Build Topic List

### 2.1 Directory-Based Topics

For each significant directory (3+ files or contains entry point):

```
topic_name = kebab-case(directory_name)
title = Title Case(directory_name)
source_files = [list of files in directory]
```

### 2.2 Standard Topics

Check for and add these standard topics when indicators exist:

| Topic | Indicators |
|-------|------------|
| `deployment` | Dockerfile, docker-compose.yml, k8s/, helm/ |
| `ci-cd` | .github/workflows/, .gitlab-ci.yml, .circleci/ |
| `testing` | test/, __tests__/, *.test.*, jest.config.*, pytest.ini |
| `configuration` | .env*, config/, settings.* |
| `database` | migrations/, schema/, prisma/, drizzle/ |
| `authentication` | auth/, login/, session/, jwt/ |
| `api` | routes/, controllers/, api/, endpoints/ |

### 2.3 Granularity Guidelines

- **Target:** 10-30 topics depending on codebase size
- **Merge:** Similar small folders into one topic
- **Split:** Large complex areas (20+ files) into multiple topics
- **Don't:** Create a topic for every single file

---

## Step 3: Present for Approval

Display the proposed topic list to the user:

```
Proposed topics for this codebase:

1. [name]: Title (N files)
   - path/to/file1
   - path/to/file2

2. [name]: Title (N files)
   ...
```

Ask user:
```
What would you like to do?

1. Approve all - Create these topics
2. Add a topic - I want to add another
3. Remove a topic - Remove one from the list
4. Edit a topic - Modify name or files
```

Handle modifications and re-display until user approves.

---

## Step 4: Create Topics

For each approved topic, call the MCP tool:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_create_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "<topic-name>",
  "title": "<Topic Title>",
  "content": {
    "conceptual": "# <Topic Title>\n\nTopic pending documentation.\n\n## Source Files\n- path/to/file1\n- path/to/file2",
    "technical": "",
    "files": "",
    "related": ""
  }
}
```

---

## Step 5: Flag Topics as Incomplete

After creating all topics, flag each one as incomplete so they appear in the fix queue:

```
Tool: mcp__plugin_mermaid-collab_mermaid__kodex_flag_topic
Args: {
  "project": "<absolute-path-to-cwd>",
  "name": "<topic-name>",
  "type": "incomplete",
  "description": "Stub topic needs detailed content based on actual codebase analysis"
}
```

Call this for each topic created in Step 4.

### Summary

After creating and flagging all topics, display:

```
Created N topics as drafts:
- topic-1: Title 1
- topic-2: Title 2
...

All topics flagged as incomplete for review.
Use /kodex-fix to fill in detailed content, or review drafts in the Kodex UI.
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Cannot read directory | Log warning, skip, continue |
| No significant directories | Warn user, ask for guidance |
| MCP tool fails | Log error, continue with remaining |
| User cancels | Exit with no changes |

---

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `kodex_create_topic` | Create a new topic as draft |
| `kodex_list_topics` | Check existing topics before creating |
| `kodex_flag_topic` | Flag topic as incomplete for review |

---

## Integration

**Standalone skill** - Does not require an active collab session.

**Related skills:**
- `kodex-fix` - Fix flagged incomplete topics
- `using-kodex` - Query and flag existing topics
