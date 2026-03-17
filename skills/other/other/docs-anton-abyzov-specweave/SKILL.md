---
description: Documentation hub - browse, search, serve living docs. Use for "show docs", "browse docs", "find docs", "load docs", "read ADR", "serve docs", "preview docs", "docs status".
argument-hint: "[topic] [--serve] [--status] [--public] [--internal] [--adr] [--list]"
---

# Documentation Hub

## Project Overrides

!`s="docs"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

Browse, search, load, and serve SpecWeave living documentation.

## Config-Driven Directories

Read configured doc directories before any operation:

```bash
# Read configured doc directories (default: .specweave/docs)
DOC_DIRS=$(jq -r '(.documentation.directories // [".specweave/docs"])[]' .specweave/config.json 2>/dev/null)
[ -z "$DOC_DIRS" ] && DOC_DIRS=".specweave/docs"
```

All search/list commands below MUST iterate over `$DOC_DIRS` instead of hardcoding `.specweave/docs`.

## Behavior

### 1. No arguments: Show documentation dashboard

Run these diagnostic commands:

```bash
# Read configured doc directories
DOC_DIRS=$(jq -r '(.documentation.directories // [".specweave/docs"])[]' .specweave/config.json 2>/dev/null)
[ -z "$DOC_DIRS" ] && DOC_DIRS=".specweave/docs"

# Count documents across all directories
DOC_COUNT=0
for dir in $DOC_DIRS; do
  if [ -d "$dir" ]; then
    C=$(find "$dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    DOC_COUNT=$((DOC_COUNT + C))
  fi
done
echo "DOC_COUNT:$DOC_COUNT"

# Detect umbrella mode and list child repo docs
UMB_REPOS=$(jq -r '.umbrella | select(.enabled==true) | .childRepos[]? | "\(.id):\(.path)"' .specweave/config.json 2>/dev/null)
if [ -n "$UMB_REPOS" ]; then
  echo "UMBRELLA:true"
  for entry in $UMB_REPOS; do
    REPO_ID="${entry%%:*}"
    REPO_PATH="${entry#*:}"
    REPO_DOC_COUNT=0
    for scope_dir in internal public; do
      CHILD_DOCS="$REPO_PATH/.specweave/docs/$scope_dir"
      if [ -d "$CHILD_DOCS" ]; then
        C=$(find "$CHILD_DOCS" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        REPO_DOC_COUNT=$((REPO_DOC_COUNT + C))
      fi
    done
    echo "CHILD_REPO:$REPO_ID:$REPO_DOC_COUNT docs"
  done
fi

# Check Docusaurus install status
[ -d ".specweave/docs-site-internal/node_modules" ] && echo "DOCUSAURUS:installed" || echo "DOCUSAURUS:not_installed"

# Check if docs server is running
SERVER_INFO=$(lsof -i :3000-3010 -sTCP:LISTEN 2>/dev/null | grep -i node | head -1 | awk '{print $9}' | cut -d: -f2)
[ -n "$SERVER_INFO" ] && echo "SERVER:running:$SERVER_INFO" || echo "SERVER:stopped"

# List topics per directory
for dir in $DOC_DIRS; do
  echo "=== $dir ==="
  if [ -d "$dir/public" ]; then
    echo "  Public:"
    ls "$dir/public/" 2>/dev/null || echo "  (none)"
  fi
  if [ -d "$dir/internal" ]; then
    echo "  Internal:"
    ls "$dir/internal/" 2>/dev/null || echo "  (none)"
  fi
  if [ -d "$dir/internal/architecture/adr" ]; then
    echo "  ADRs:"
    ls "$dir/internal/architecture/adr/" 2>/dev/null || echo "  (none)"
  fi
  # For non-standard directories (e.g., docs/), list top-level folders
  if [ "$dir" != ".specweave/docs" ] && [ -d "$dir" ]; then
    echo "  Folders:"
    ls -d "$dir"/*/ 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
  fi
done

# In umbrella mode, also list child repo doc topics
if [ -n "$UMB_REPOS" ]; then
  for entry in $UMB_REPOS; do
    REPO_ID="${entry%%:*}"
    REPO_PATH="${entry#*:}"
    CHILD_DOC_DIR="$REPO_PATH/.specweave/docs"
    if [ -d "$CHILD_DOC_DIR" ]; then
      echo "=== $REPO_ID ==="
      [ -d "$CHILD_DOC_DIR/internal" ] && echo "  Internal:" && ls "$CHILD_DOC_DIR/internal/" 2>/dev/null || true
      [ -d "$CHILD_DOC_DIR/public" ] && echo "  Public:" && ls "$CHILD_DOC_DIR/public/" 2>/dev/null || true
    fi
  done
fi
```

Present as a clean dashboard.

**Then ALWAYS include serve guidance** (same as `--serve` behavior):
- If server is already running: "Docs server running at http://localhost:<port>"
- If server is NOT running: Show the `specweave docs preview` instructions (see section 4 below)

This ensures every `/sw:docs` invocation gives the user a clear path to browse docs in their browser.

### 2. `--list`: List topics only

Same as dashboard but skip server/Docusaurus diagnostics. Just list folder names with descriptions.

### 3. Topic argument: Search and load docs

When user provides a topic (e.g., `/sw:docs sync`, `/sw:docs troubleshooting`):

1. **Search** across all configured directories and child repos:
   ```bash
   DOC_DIRS=$(jq -r '(.documentation.directories // [".specweave/docs"])[]' .specweave/config.json 2>/dev/null)
   [ -z "$DOC_DIRS" ] && DOC_DIRS=".specweave/docs"

   # Add child repo doc dirs in umbrella mode
   UMB_REPOS=$(jq -r '.umbrella | select(.enabled==true) | .childRepos[]? | .path' .specweave/config.json 2>/dev/null)
   for repo_path in $UMB_REPOS; do
     [ -d "$repo_path/.specweave/docs" ] && DOC_DIRS="$DOC_DIRS $repo_path/.specweave/docs"
   done

   for dir in $DOC_DIRS; do
     find "$dir" -type d -iname "*<topic>*" -maxdepth 4 2>/dev/null
     find "$dir" -type f -iname "*<topic>*.md" -maxdepth 5 2>/dev/null
   done
   ```

2. **If found**: Read the most relevant files (up to 3-5) and present a summary
3. **If not found**: Search file contents with Grep for the topic keyword, then present matches

### 4. `--serve` or serve intent: Browser preview guide

Detect serve intent from: `--serve`, `--preview`, or phrases like "serve", "preview", "browser", "open docs", "start server".

1. Check if server is already running:
   ```bash
   lsof -i :3000-3010 -sTCP:LISTEN 2>/dev/null | grep -i node
   ```

2. **If running**: "Docs server already running at http://localhost:<port>"
3. **If not running**: Display:
   ```
   To view docs in browser with hot reload, run in your terminal:

     specweave docs preview

   First run auto-installs Docusaurus (~30-60 seconds).
   Subsequent runs start instantly.

   Options:
     specweave docs preview --port 3005            Use specific port
     specweave docs preview --no-browser           Don't auto-open browser
     specweave docs preview --project <id>         Target child repo (umbrella)
     specweave docs preview --project vskill       Example: preview vskill docs

   To stop: Ctrl+C in terminal, or: specweave docs kill
   ```

   **In umbrella projects**, also mention `--project <id>` usage to target child repo docs.

### 5. `--status`: Full status report

Run and display output of:
```bash
specweave docs status
```

### 6. Flags

| Flag | Behavior |
|------|----------|
| `--public` | Only search public docs |
| `--internal` | Only search internal docs |
| `--adr` | List and load ADRs specifically |
| `--list` | List topics without diagnostics |
| `--serve` | Browser preview guide |
| `--status` | Run `specweave docs status` |

### 7. ADR Mode (`--adr` or "ADR" in topic)

List all ADRs with their titles across all directories:
```bash
DOC_DIRS=$(jq -r '(.documentation.directories // [".specweave/docs"])[]' .specweave/config.json 2>/dev/null)
[ -z "$DOC_DIRS" ] && DOC_DIRS=".specweave/docs"
for dir in $DOC_DIRS; do
  for f in "$dir"/internal/architecture/adr/*.md; do
    [ -f "$f" ] && echo "$(basename "$f"): $(head -1 "$f" | sed 's/^# //')"
  done
done
```

If a specific ADR number is given, read and present it.

## Output Footer

Always append to any output:

```
Tip: Run `specweave docs preview` in your terminal to view all docs in browser with hot reload.
```
