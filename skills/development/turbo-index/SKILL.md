---
name: turbo-index
description: Index the current project for optimized search with QMD semantic search and fast file suggestions. Run this when entering a new codebase or after significant changes. Saves 60-80% tokens on exploration tasks.
---

# Turbo Index

You are running the turbo-index skill to set up optimized search for this project.

## Instructions

Follow these phases in order. Use the Bash tool to run commands. Report progress to the user after each phase.

### Phase 1: Check Dependencies

Run the dependency checker:

```bash
~/.claude/plugins/*/claude-turbo-search/scripts/install-deps.sh --check-only 2>/dev/null || \
  ~/claude-turbo-search/scripts/install-deps.sh --check-only 2>/dev/null || \
  echo "DEPS_SCRIPT_NOT_FOUND"
```

If dependencies are missing, ask the user if they want to install them. If yes, run without `--check-only`:

```bash
~/.claude/plugins/*/claude-turbo-search/scripts/install-deps.sh 2>/dev/null || \
  ~/claude-turbo-search/scripts/install-deps.sh 2>/dev/null
```

### Phase 2: Global Setup (if needed)

Check if file-suggestion.sh exists in ~/.claude/:

```bash
[ -f ~/.claude/file-suggestion.sh ] && echo "FILE_SUGGESTION_EXISTS" || echo "FILE_SUGGESTION_MISSING"
```

If missing, run the setup scripts:

```bash
# Setup file suggestion
~/.claude/plugins/*/claude-turbo-search/scripts/setup-file-suggestion.sh 2>/dev/null || \
  ~/claude-turbo-search/scripts/setup-file-suggestion.sh 2>/dev/null

# Setup QMD MCP server
~/.claude/plugins/*/claude-turbo-search/scripts/setup-mcp.sh 2>/dev/null || \
  ~/claude-turbo-search/scripts/setup-mcp.sh 2>/dev/null
```

### Phase 3: Run Cartographer (if needed)

Check if codebase map exists and its age:

```bash
if [ -f docs/CODEBASE_MAP.md ]; then
  # Check if older than 24 hours (86400 seconds)
  AGE=$(($(date +%s) - $(stat -f %m docs/CODEBASE_MAP.md 2>/dev/null || stat -c %Y docs/CODEBASE_MAP.md 2>/dev/null)))
  if [ $AGE -gt 86400 ]; then
    echo "CODEBASE_MAP_STALE"
  else
    echo "CODEBASE_MAP_FRESH"
  fi
else
  echo "CODEBASE_MAP_MISSING"
fi
```

If missing or stale, use the Skill tool to invoke cartographer:

```
Skill: cartographer
```

### Phase 4: Index with QMD

Get the project name and create/update the QMD collection:

```bash
PROJECT_NAME=$(basename "$PWD")
echo "Indexing project: $PROJECT_NAME"

# Add the project directory as a QMD collection
# Using correct QMD syntax: qmd collection add [path] --name <name> --mask <pattern>
qmd collection add . --name "$PROJECT_NAME" --mask "**/*.md"

# Add context for the collection
qmd context add . "Codebase documentation and structure for $PROJECT_NAME"

# Create vector embeddings for semantic search
echo "Creating vector embeddings (this may take a moment on first run)..."
qmd embed
```

Store metadata for staleness detection:

```bash
PROJECT_NAME=$(basename "$PWD")
mkdir -p .claude
cat > .claude/turbo-search.json << EOF
{
  "project": "$PROJECT_NAME",
  "lastIndexed": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "gitCommit": "$(git rev-parse HEAD 2>/dev/null || echo 'not-a-git-repo')",
  "qmdCollection": "$PROJECT_NAME"
}
EOF
echo "Metadata saved to .claude/turbo-search.json"
```

### Phase 5: Report Results

Get indexing stats and report to user:

```bash
PROJECT_NAME=$(basename "$PWD")

# Common exclusions for dependencies/build artifacts across languages
EXCLUDES=(
  # Node.js/JavaScript
  --glob '!node_modules/' --glob '!bower_components/' --glob '!.npm/'
  --glob '!.yarn/' --glob '!.pnpm-store/' --glob '!dist/' --glob '!build/' --glob '!coverage/'
  # Elixir
  --glob '!_build/' --glob '!deps/' --glob '!.elixir_ls/' --glob '!.fetch/'
  # Java
  --glob '!target/' --glob '!.gradle/' --glob '!.mvn/' --glob '!out/' --glob '!.settings/'
  # Ruby
  --glob '!vendor/' --glob '!.bundle/' --glob '!.gem/'
  # PHP
  --glob '!vendor/' --glob '!.composer/'
  # Python (bonus)
  --glob '!__pycache__/' --glob '!.venv/' --glob '!venv/' --glob '!.tox/'
  --glob '!.mypy_cache/' --glob '!.pytest_cache/' --glob '!*.egg-info/'
  # General
  --glob '!.git/'
)

# Count indexed files (excluding dependencies)
TOTAL_FILES=$(rg --files --follow --hidden "${EXCLUDES[@]}" . 2>/dev/null | wc -l | tr -d ' ')
MD_FILES=$(rg --files --glob "**/*.md" "${EXCLUDES[@]}" . 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Project \"$PROJECT_NAME\" indexed"
echo "   Total files: $TOTAL_FILES"
echo "   Markdown docs: $MD_FILES"
echo "   Estimated token savings: 60-80% on exploration"
echo ""
echo "QMD semantic search ready"
echo "Turbo file suggestion active"
echo ""
echo "Pro tip: Use 'qmd search \"query\"' to find files BEFORE reading them"
echo "   This saves tokens by only reading relevant content."
echo ""
echo "Try: qmd search \"authentication\" --files"
```

## Using QMD for Token Savings

After indexing, always prefer searching before reading:

```bash
# Find relevant files first (fast, low tokens)
qmd search "your topic" --files -n 5

# Then read only what you need
qmd get "path/to/relevant-file.md"
```

**The /qmd skill is also available** - use it when you need to search for content across your indexed projects.

## Notes

- This skill is idempotent - safe to run multiple times
- First run installs dependencies and configures Claude Code globally
- Subsequent runs just refresh the project index
- Restart Claude Code after first run to activate MCP tools
- Use `qmd search` before reading files to save tokens
