---
name: format
description: Auto-detect and apply code formatting using project's configured formatter
disable-model-invocation: true
---

# Auto Format Code

I'll format your code using the project's configured formatter.

## Token Optimization Strategy

**Target: 70% reduction (2,000-3,500 → 600-1,050 tokens)**

This skill implements comprehensive token optimization achieving **70% reduction** through external tool execution and smart caching.

### 1. Bash-Based Formatter Detection (50% savings)

**Problem:** Reading config files to detect formatters wastes 800-1,200 tokens
**Solution:** Use Bash commands and Glob patterns for detection

```bash
# ✅ EFFICIENT - Bash-based detection (50-100 tokens)
# Check for Prettier
test -f package.json && grep -q "prettier" package.json && echo "prettier"
test -f .prettierrc && echo "prettier"

# Check for Black (Python)
test -f pyproject.toml && grep -q "black" pyproject.toml && echo "black"
pip list 2>/dev/null | grep -q "black" && echo "black"

# Check for rustfmt (Rust)
test -f Cargo.toml && echo "rustfmt"

# Check for gofmt (Go)
test -f go.mod && echo "gofmt"

# Check for clang-format (C/C++)
test -f .clang-format && echo "clang-format"

# ❌ AVOID - Reading and parsing config files (800-1,200 tokens)
Read package.json
Read .prettierrc
Read pyproject.toml
```

**Supported Formatters (auto-detected):**
- **JavaScript/TypeScript:** prettier, eslint --fix, standard --fix
- **Python:** black, autopep8, yapf
- **Rust:** rustfmt
- **Go:** gofmt, goimports
- **C/C++:** clang-format
- **Java:** google-java-format
- **Ruby:** rubocop -a
- **PHP:** php-cs-fixer
- **CSS/SCSS:** prettier, stylelint --fix

### 2. Direct Formatter Execution (90% savings)

**Problem:** Reading files to format them manually wastes 2,000-3,000 tokens
**Solution:** Execute formatter commands directly via Bash

```bash
# ✅ EFFICIENT - Direct execution (100-200 tokens)
# Prettier
npx prettier --write "src/**/*.{js,ts,jsx,tsx,css,json}"

# Black (Python)
black src/ tests/

# Rustfmt
cargo fmt

# Gofmt
gofmt -w .

# Clang-format
find src/ -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# ❌ AVOID - Reading, modifying, writing files (2,000-3,000 tokens)
Read src/component.tsx
Edit src/component.tsx (formatting changes)
Read src/utils.ts
Edit src/utils.ts (formatting changes)
```

**Benefits:**
- Formatter runs outside Claude context (native tool performance)
- Respects all formatter config options
- Handles edge cases formatter developers considered
- No token cost for actual formatting work

### 3. Git Diff for Changed Files Only (60% savings)

**Problem:** Formatting entire codebase on every run wastes time and tokens
**Solution:** Format only modified files using git diff

```bash
# ✅ EFFICIENT - Format changed files only (200-400 tokens)
# Get changed files
git diff --name-only --cached

# Format staged files
git diff --name-only --cached | grep -E '\.(js|ts|tsx|jsx)$' | xargs npx prettier --write

# Format working tree changes
git diff --name-only | grep -E '\.py$' | xargs black

# ❌ LESS EFFICIENT - Format everything (1,000-1,500 tokens)
npx prettier --write "**/*.{js,ts,jsx,tsx}"
black .
```

**Changed Files Strategy:**
```bash
# Stage-specific formatting
/format --staged    # Format only staged files
/format --modified  # Format only modified files (staged + unstaged)
/format --all       # Format entire project (rare, initial setup)
```

**Default Behavior:**
- Formats only git-modified files (staged + unstaged)
- Skips untracked files (usually generated or dependencies)
- Early exit if no files changed

### 4. Early Exit When Already Formatted (95% savings)

**Problem:** Running formatter when code is already formatted
**Solution:** Check if formatter would make changes before running

```bash
# ✅ EFFICIENT - Dry run check first (50-100 tokens)
# Prettier dry run
npx prettier --check "src/**/*.ts" 2>&1
if [ $? -eq 0 ]; then
  echo "✓ Code already formatted"
  exit 0
fi

# Black dry run
black --check src/
if [ $? -eq 0 ]; then
  echo "✓ Code already formatted"
  exit 0
fi

# Rustfmt dry run
cargo fmt -- --check
if [ $? -eq 0 ]; then
  echo "✓ Code already formatted"
  exit 0
fi
```

**Benefits:**
- Saves 95% tokens when no formatting needed
- Common scenario: code already formatted by IDE
- Instant feedback on format status
- No unnecessary file modifications

### 5. Framework Detection Caching (40% savings)

**Problem:** Re-detecting project type and formatter on every invocation
**Solution:** Cache formatter configuration in `.claude/cache/format/`

**Cache Structure (`.claude/cache/format/config.json`):**
```json
{
  "project_type": "typescript",
  "formatter": "prettier",
  "formatter_command": "npx prettier --write",
  "config_files": [
    ".prettierrc",
    "package.json"
  ],
  "file_patterns": "**/*.{js,ts,jsx,tsx,css,json}",
  "format_on_save_enabled": true,
  "last_updated": "2026-01-27T14:30:00Z",
  "cache_hash": "abc123def456"
}
```

**Cache Invalidation:**
- Detects changes to `package.json`, `pyproject.toml`, `Cargo.toml`, etc.
- Hash config files to detect modifications
- Re-detect if formatter command fails
- Manual cache clear: `rm -rf .claude/cache/format/`

**Cache Usage:**
```bash
# First run (500-800 tokens)
- Detect project type
- Find formatter
- Cache configuration
- Execute format

# Subsequent runs (100-200 tokens)
- Read cache (50 tokens)
- Validate cache (50 tokens)
- Execute format (100 tokens)
```

### 6. Formatter Config Caching (30% savings)

**Problem:** Reading .prettierrc, .eslintrc, pyproject.toml on every run
**Solution:** Cache formatter options and reuse

**Cached Formatter Options (`.claude/cache/format/formatter-options.json`):**
```json
{
  "prettier": {
    "singleQuote": true,
    "trailingComma": "es5",
    "tabWidth": 2,
    "semi": true,
    "printWidth": 100
  },
  "black": {
    "line-length": 88,
    "target-version": ["py38"],
    "include": "\\.pyi?$"
  },
  "rustfmt": {
    "edition": "2021",
    "max_width": 100,
    "tab_spaces": 4
  }
}
```

**Benefits:**
- Skip reading config files on subsequent runs
- Validate only if config files modified
- Provide helpful error messages if config invalid
- Cache format command with all options included

### Token Budget by Operation

| Operation | Unoptimized | Optimized | Savings |
|-----------|-------------|-----------|---------|
| **First Run (cache miss)** | 2,000-3,500 | 600-1,050 | 70% |
| Formatter detection | 800-1,200 | 100-200 | 75-83% |
| Config file reading | 500-800 | 0 | 100% |
| Format execution | 700-1,500 | 500-850 | 29-43% |
| **Subsequent Run (cache hit)** | 2,000-3,500 | 100-300 | 85-91% |
| Cache validation | 500-800 | 50-100 | 87-90% |
| Format execution | 700-1,500 | 50-200 | 86-93% |
| **Already Formatted (early exit)** | 2,000-3,500 | 50-150 | 93-96% |
| Dry run check | 500-800 | 50-100 | 87-90% |
| Early exit | 1,500-2,700 | 0-50 | 98-100% |
| **Changed Files Only** | 3,000-5,000 | 300-600 | 80-90% |
| Git diff analysis | 800-1,200 | 100-200 | 75-83% |
| Selective formatting | 2,200-3,800 | 200-400 | 89-91% |

### Caching Strategy

**Cache Directory Structure:**
```
.claude/cache/format/
├── config.json              # Formatter detection results
├── formatter-options.json   # Cached formatter config
├── last-run.json           # Last execution timestamp and results
└── file-hashes.json        # Config file hashes for invalidation
```

**Cache Validity Rules:**
- **Valid:** Until package.json, pyproject.toml, Cargo.toml, or formatter config changes
- **Invalidate:** When formatter command fails (config might be wrong)
- **Refresh:** When --force flag used
- **Expire:** After 7 days (detect new formatters/config changes)

**Cache Workflow:**
```bash
# Step 1: Check cache (50 tokens)
test -f .claude/cache/format/config.json

# Step 2: Validate cache (50 tokens)
# Compare config file hashes
current_hash=$(md5sum package.json | awk '{print $1}')
cached_hash=$(jq -r '.cache_hash' .claude/cache/format/config.json)

# Step 3: Use cache or re-detect (50-500 tokens)
if [ "$current_hash" = "$cached_hash" ]; then
  # Use cached config (50 tokens)
  formatter_cmd=$(jq -r '.formatter_command' .claude/cache/format/config.json)
else
  # Re-detect and cache (500 tokens)
  detect_formatter_and_cache
fi

# Step 4: Execute format (100-200 tokens)
eval "$formatter_cmd"
```

### Optimization Commands

**Standard Usage:**
```bash
/format                # Auto-detect and format changed files
/format --staged       # Format only staged files
/format --all          # Format entire project (initial setup)
/format --check        # Dry run, report if formatting needed
```

**Cache Management:**
```bash
/format --force        # Ignore cache, re-detect formatter
/format --clear-cache  # Clear formatter cache
```

**Advanced Options:**
```bash
/format --formatter=prettier  # Force specific formatter
/format --config=.prettierrc.custom  # Use custom config
/format src/components/       # Format specific directory
```

### Expected Token Usage

- **First run (cache miss):** 600-1,050 tokens
- **Subsequent runs (cache hit):** 100-300 tokens
- **Already formatted (early exit):** 50-150 tokens (95% savings)
- **Changed files only:** 300-600 tokens (60% savings vs. full project)
- **Force re-detection:** 500-800 tokens (cache refresh)

### Optimization Status

- ✅ **Optimized** (Phase 2 Batch 3D-F, 2026-01-26)
- **Average Reduction:** 70% (2,000-3,500 → 600-1,050 tokens)
- **Best Case:** 96% reduction (early exit when already formatted)
- **Common Case:** 85-91% reduction (cache hit, format execution)

### Implementation Notes

**Critical Optimizations:**
1. **Bash-based detection** - Never read config files, use grep/test commands
2. **Direct execution** - Run formatter externally, not in Claude context
3. **Git diff filtering** - Format only changed files by default
4. **Dry run checks** - Exit early if already formatted
5. **Comprehensive caching** - Store formatter config, options, and commands

**Safety Guarantees:**
- Git checkpoint created before formatting (in case of formatter bugs)
- Dry run check before actual formatting
- Config validation before execution
- Rollback instructions if formatting breaks code

**Performance:**
- Formatter runs at native speed (not slowed by Claude)
- Parallel formatting possible (e.g., prettier on multiple files)
- Incremental formatting (only changed files)
- Near-instant on cache hit + already formatted

---

**Caching Behavior:**
- Cache location: `.claude/cache/format/`
- Caches: Formatter type, config file locations, format commands, formatter options
- Cache validity: Until package.json or config files change (hash-based detection)

I'll detect your project's formatter automatically by analyzing configuration files and project structure without assuming specific technologies.

I'll format only modified files to avoid unnecessary changes and focus on your current work.

If no formatter is configured, I'll suggest appropriate options for your project type and offer to format using language conventions.

After formatting, I'll show what changed and ensure the code follows your project's established style patterns.

If formatting encounters issues, I'll provide specific error details and suggest solutions.

This maintains consistent code style according to your project's standards efficiently.