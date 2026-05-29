---
name: file-organization
description: Enforces project file organization standards from CLAUDE.md/PROJECT.md - auto-fix mode
version: 1.0.0
category: enforcement
auto_invoke: true
triggers:
  - before_file_create
  - before_file_move
  - before_directory_create
---

# File Organization Skill

**Purpose**: Enforce project-specific file organization rules from CLAUDE.md and PROJECT.md.

**Mode**: Auto-fix (automatically moves files to correct locations)

---

## Auto-Invoke Triggers

This skill is automatically invoked:

- **Before file creation**: Validates proposed file location
- **Before file move**: Validates destination path
- **Before directory creation**: Validates directory structure

---

## What This Skill Enforces

### 1. Root Directory Policy

**Rule**: Maximum 8 essential .md files in root

**Allowed in root**:

- README.md
- CHANGELOG.md
- LICENSE
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md
- CLAUDE.md
- PROJECT.md

**All other .md files**: Must be in `docs/` subdirectories

### 2. Shell Scripts Organization

**Rule**: All `.sh` files in `scripts/` subdirectories

**Categories**:

- `scripts/debug/` - Debugging and troubleshooting tools
- `scripts/test/` - Testing utilities
- `scripts/build/` - Build and deployment scripts
- `scripts/` - General utility scripts

**Example**:

- ❌ `./test-auth.sh`
- ✅ `./scripts/test/test-auth.sh`

### 3. Documentation Organization

**Rule**: Documentation in `docs/` subdirectories by category

**Categories**:

- `docs/guides/` - User-facing guides
- `docs/debugging/` - Troubleshooting and debug info
- `docs/development/` - Developer documentation
- `docs/architecture/` - Architecture decisions (ADRs)
- `docs/reference/` - API reference, technical specs

**Example**:

- ❌ `./USER-GUIDE.md`
- ✅ `./docs/guides/user-guide.md`

### 4. Source Code Organization

**Rule**: All source code in `src/`, all tests in `tests/`

**Example**:

- ❌ `./my-module.ts`
- ✅ `./src/my-module.ts`
- ✅ `./tests/unit/my-module.test.ts`

---

## Workflow

### Phase 1: Parse Organization Rules

#### Step 1.1: Read CLAUDE.md File Organization Section

```bash
# Extract file organization section
awk '/## File Organization/,/^## [A-Z]/' CLAUDE.md

# Or from PROJECT.md
awk '/## File Organization Standards/,/^## [A-Z]/' PROJECT.md
```

**Parse rules**:

```json
{
  "root_policy": {
    "max_md_files": 8,
    "essential_files": ["README.md", "CHANGELOG.md", ...]
  },
  "scripts": {
    "allowed_locations": ["scripts/debug/", "scripts/test/", "scripts/build/"]
  },
  "documentation": {
    "allowed_locations": ["docs/guides/", "docs/debugging/", "docs/development/", "docs/architecture/", "docs/reference/"],
    "root_allowed": false
  },
  "source_code": {
    "allowed_locations": ["src/"]
  }
}
```

#### Step 1.2: Load Exceptions (if configured)

Check `.claude/config.yml` for exceptions:

```yaml
file_organization:
  exceptions:
    - "build*.sh" # Allow build scripts in root
    - "Dockerfile*" # Allow Dockerfiles anywhere
```

---

### Phase 2: Validate File Location

When Claude attempts to create a file:

#### Step 2.1: Determine File Type

```bash
FILE_PATH="$1"
FILE_EXT="${FILE_PATH##*.}"
FILE_NAME=$(basename "$FILE_PATH")
FILE_DIR=$(dirname "$FILE_PATH")
```

**Categorize**:

- `.sh` → Shell script
- `.md` → Documentation
- `.ts`, `.js`, `.py`, `.go`, `.rs` → Source code
- `.json`, `.yaml`, `.toml` → Configuration (allowed in root)

#### Step 2.2: Check if Location Matches Rules

**For shell scripts (`.sh`)**:

```bash
if [[ "$FILE_EXT" == "sh" ]]; then
  if [[ ! "$FILE_PATH" =~ ^scripts/ ]]; then
    echo "❌ Shell scripts must be in scripts/ subdirectories"
    # Determine correct location
    if [[ "$FILE_NAME" =~ ^test- ]]; then
      CORRECT_PATH="scripts/test/$FILE_NAME"
    elif [[ "$FILE_NAME" =~ ^debug- ]]; then
      CORRECT_PATH="scripts/debug/$FILE_NAME"
    else
      CORRECT_PATH="scripts/$FILE_NAME"
    fi
  fi
fi
```

**For markdown files (`.md`)**:

```bash
if [[ "$FILE_EXT" == "md" ]]; then
  # Check if essential file
  ESSENTIAL="README|CHANGELOG|LICENSE|CONTRIBUTING|CODE_OF_CONDUCT|SECURITY|CLAUDE|PROJECT"

  if [[ ! "$FILE_NAME" =~ ^($ESSENTIAL)\.md$ ]]; then
    # Not essential - must be in docs/
    if [[ ! "$FILE_PATH" =~ ^docs/ ]]; then
      echo "❌ Non-essential .md files must be in docs/ subdirectories"

      # Infer category from name
      if [[ "$FILE_NAME" =~ -guide|tutorial|getting-started ]]; then
        CORRECT_PATH="docs/guides/$FILE_NAME"
      elif [[ "$FILE_NAME" =~ debug|troubleshoot|error ]]; then
        CORRECT_PATH="docs/debugging/$FILE_NAME"
      elif [[ "$FILE_NAME" =~ arch|design|adr ]]; then
        CORRECT_PATH="docs/architecture/$FILE_NAME"
      elif [[ "$FILE_NAME" =~ api|reference ]]; then
        CORRECT_PATH="docs/reference/$FILE_NAME"
      else
        CORRECT_PATH="docs/$FILE_NAME"
      fi
    fi
  fi
fi
```

**For source code**:

```bash
if [[ "$FILE_EXT" =~ ^(ts|js|py|go|rs)$ ]]; then
  # Exclude test files
  if [[ ! "$FILE_NAME" =~ \.test\.|_test\.|\.spec\. ]]; then
    # Should be in src/
    if [[ ! "$FILE_PATH" =~ ^src/ ]]; then
      echo "❌ Source code must be in src/"
      CORRECT_PATH="src/$FILE_NAME"
    fi
  else
    # Test file - should be in tests/
    if [[ ! "$FILE_PATH" =~ ^tests/ ]]; then
      echo "❌ Test files must be in tests/"
      # Determine test type
      if [[ "$FILE_NAME" =~ \.unit\. ]]; then
        CORRECT_PATH="tests/unit/$FILE_NAME"
      elif [[ "$FILE_NAME" =~ \.integration\. ]]; then
        CORRECT_PATH="tests/integration/$FILE_NAME"
      else
        CORRECT_PATH="tests/unit/$FILE_NAME"
      fi
    fi
  fi
fi
```

---

### Phase 3: Enforcement Action

**Enforcement level** (from `.claude/config.yml`):

```yaml
file_organization:
  enforcement: "auto-fix" # or "block" or "warn"
```

#### Mode 1: Auto-Fix (Default)

**Action**: Automatically move to correct location and notify

```
🤖 file-organization skill activated

Proposed: ./test-auth.sh
Rule Check: Shell scripts → scripts/debug/ or scripts/test/
File Purpose: Testing script (detected from name prefix "test-")
Correct Location: scripts/test/

✅ Auto-corrected to: scripts/test/test-auth.sh
   Reason: Testing scripts belong in scripts/test/ (CLAUDE.md:45)

File created at correct location.
```

**Implementation**:

```bash
# Instead of creating at wrong location
# Claude creates at correct location directly
PROPOSED="./test-auth.sh"
CORRECT="./scripts/test/test-auth.sh"

# Create parent directory if needed
mkdir -p $(dirname "$CORRECT")

# Create file at correct location
# (Claude's Write/Edit tool uses $CORRECT instead of $PROPOSED)
```

#### Mode 2: Block

**Action**: Prevent creation, require Claude to use correct path

```
❌ CLAUDE.md Rule Violation:
   Shell scripts must be in scripts/debug/ or scripts/test/

   Proposed: ./test-auth.sh
   Suggested: scripts/test/test-auth.sh
   Reason: Keeps root directory clean (CLAUDE.md policy)

Please create file at correct location:
  Write: scripts/test/test-auth.sh
```

#### Mode 3: Warn

**Action**: Allow but log warning

```
⚠️ File organization warning:
   Created: ./test-auth.sh
   Recommended: scripts/test/test-auth.sh
   Reason: Shell scripts should be in scripts/ subdirectories

File created at requested location.
Note: Run /align-project to organize files.
```

---

### Phase 4: Update Documentation References

When auto-fixing, update any documentation that references the old path:

```bash
OLD_PATH="./test-auth.sh"
NEW_PATH="./scripts/test/test-auth.sh"

# Search for references in docs
REFS=$(grep -r "$OLD_PATH" --include="*.md" .)

if [ -n "$REFS" ]; then
  echo "📝 Updating documentation references..."

  # Auto-update (since file hasn't been created yet, unlikely to have refs)
  # But check for template references
fi
```

---

### Phase 5: Track File Organization

Create `.claude/file-org-log.json` to track auto-fixes:

```json
{
  "auto_fixes": [
    {
      "timestamp": "2024-10-26T15:30:00Z",
      "proposed": "./test-auth.sh",
      "corrected": "./scripts/test/test-auth.sh",
      "reason": "Shell scripts must be in scripts/ subdirectories",
      "rule": "CLAUDE.md:45"
    }
  ]
}
```

**Purpose**: Audit trail for auto-corrections

---

## Special Cases

### Case 1: New Directory Category

```
🤖 file-organization skill activated

Proposed: ./scripts/deploy/deploy.sh
Rule Check: scripts/deploy/ not in documented categories

New category detected: scripts/deploy/
This isn't documented in CLAUDE.md.

Options:
1. Allow (one-off script) → use scripts/deploy.sh
2. Create new category → Add to CLAUDE.md:

   ## File Organization
   - scripts/deploy/ - Deployment scripts

Create new category? [y/N]
```

If yes:

- Create directory
- Update CLAUDE.md with new category
- Proceed with file creation

If no:

- Move to `scripts/` root instead

### Case 2: Configuration Files

```
Proposed: ./tsconfig.json
Rule Check: Configuration file
Enforcement: SKIP (config files allowed in root)

✅ Config file - root location is standard
```

**Allowed in root without restriction**:

- `package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`
- `.env`, `.env.example`, `.gitignore`
- `Dockerfile`, `docker-compose.yml`

### Case 3: Hidden Files/Directories

```
Proposed: ./.github/workflows/ci.yml
Rule Check: Hidden directory
Enforcement: SKIP (hidden dirs have different conventions)

✅ GitHub workflows - standard location
```

**Allowed without restrictions**:

- `.github/` - GitHub-specific files
- `.vscode/` - VS Code settings
- `.idea/` - JetBrains IDE settings

---

## Integration with Pre-Commit Hook

**Pre-commit validation** (enhanced hook):

```bash
#!/bin/bash
# .claude/hooks/pre-commit.sh

# Check for files in wrong locations
echo "🔍 Validating file organization..."

# Check for non-essential .md in root
ROOT_MD_COUNT=$(git diff --cached --name-only --diff-filter=A | \
  grep '^[^/]*\.md$' | \
  grep -v -E '(README|CHANGELOG|LICENSE|CONTRIBUTING|CODE_OF_CONDUCT|SECURITY|CLAUDE|PROJECT)\.md' | \
  wc -l)

if [ "$ROOT_MD_COUNT" -gt 0 ]; then
  echo "❌ Attempting to commit non-essential .md files in root:"
  git diff --cached --name-only --diff-filter=A | \
    grep '^[^/]*\.md$' | \
    grep -v -E '(README|CHANGELOG|LICENSE|CONTRIBUTING|CODE_OF_CONDUCT|SECURITY|CLAUDE|PROJECT)\.md'
  echo ""
  echo "Move to docs/ subdirectories per CLAUDE.md"
  exit 1
fi

# Check for shell scripts in root
ROOT_SH=$(git diff --cached --name-only --diff-filter=A | grep '^[^/]*\.sh$' | wc -l)

if [ "$ROOT_SH" -gt 0 ]; then
  echo "❌ Attempting to commit shell scripts in root:"
  git diff --cached --name-only --diff-filter=A | grep '^[^/]*\.sh$'
  echo ""
  echo "Move to scripts/ subdirectories per CLAUDE.md"
  exit 1
fi

echo "✅ File organization validated"
```

---

## Configuration

Add to `.claude/config.yml`:

```yaml
file_organization:
  # Enforcement level
  enforcement: "auto-fix" # Options: "auto-fix", "block", "warn"

  # Root directory policy
  root_directory:
    max_md_files: 8
    essential_files:
      - "README.md"
      - "CHANGELOG.md"
      - "LICENSE"
      - "CONTRIBUTING.md"
      - "CODE_OF_CONDUCT.md"
      - "SECURITY.md"
      - "CLAUDE.md"
      - "PROJECT.md"

  # Directory structure rules
  rules:
    shell_scripts:
      allowed_locations:
        - "scripts/debug/"
        - "scripts/test/"
        - "scripts/build/"
      exceptions: []

    markdown_docs:
      allowed_locations:
        - "docs/guides/"
        - "docs/debugging/"
        - "docs/development/"
        - "docs/architecture/"
        - "docs/reference/"
      root_allowed: false # Only essential files

    source_code:
      allowed_locations:
        - "src/"
      exceptions:
        - "tests/"

  # Exceptions (files/patterns exempt from rules)
  exceptions:
    - "build*.sh" # Allow build.sh in root
    - "Dockerfile*" # Dockerfiles anywhere

  # Auto-create directories
  auto_create_dirs: true # Create target directory if missing
```

---

## Success Criteria

After implementation:

- ✅ Claude cannot create files in wrong locations (blocked or auto-fixed)
- ✅ Pre-commit catches any files that slip through
- ✅ Auto-fix moves files to correct locations with explanation
- ✅ Documentation references auto-updated after file moves
- ✅ Root directory stays clean (max 8 .md files)
- ✅ Audit trail of all auto-corrections

---

## Performance

**Fast validation**:

- Rule parsing: < 10ms (cached)
- Path validation: < 5ms per file
- Auto-fix: < 50ms (includes directory creation)

**Total overhead**: < 100ms per file operation

---

**This skill prevents file organization debt by enforcing standards at creation time, eliminating manual cleanup.**
