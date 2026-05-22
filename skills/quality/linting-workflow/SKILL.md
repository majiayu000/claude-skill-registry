---
name: linting-workflow
description: Generic linting workflow for multiple languages with auto-fix and error resolution guidance
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: code-quality
---

## What I do

I provide a generic linting workflow that can be adapted for multiple languages:

1. **Detect Language**: Automatically detect project language (JavaScript/TypeScript, Python, etc.)
2. **Detect Linter**: Identify and configure appropriate linter (ESLint, Ruff, etc.)
3. **Detect Package Manager**: Determine package manager for running linter commands
4. **Run Linting**: Execute linter with appropriate command
5. **Apply Auto-Fix**: Use linter's auto-fix capability when available
6. **Guide Error Resolution**: Provide step-by-step guidance for fixing linting errors
7. **Verify Fixes**: Re-run linting to ensure all errors are resolved
8. **Commit Fixes**: Optionally commit linting fixes as separate commit

## When to use me

Use this framework when:
- You need to lint code before committing or creating PRs
- You want to ensure code follows industry standards and style guidelines
- You're building a workflow skill that includes code quality checks
- You need linting for multiple languages in a consistent way
- You want to integrate linting into automated workflows (PR creation, etc.)

This is a **framework skill** - it provides linting logic that other skills extend.

## Core Workflow Steps

### Step 1: Detect Project Language

**Purpose**: Determine which language and linter to use

**Detection Logic**:
```bash
# Check for language indicators
if [ -f "package.json" ]; then
  LANGUAGE="javascript"
  # Further check TypeScript
  if [ -f "tsconfig.json" ] || grep -q "typescript" package.json; then
    LANGUAGE="typescript"
  fi
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  LANGUAGE="python"
elif [ -f "go.mod" ]; then
  LANGUAGE="go"
elif [ -f "Gemfile" ]; then
  LANGUAGE="ruby"
else
  echo "Unable to detect language. Please specify manually."
  exit 1
fi

echo "Detected language: $LANGUAGE"
```

**Language Detection Summary**:

| Indicator | Language | Linter |
|-----------|----------|---------|
| `package.json` + `tsconfig.json` | TypeScript | ESLint |
| `package.json` | JavaScript | ESLint |
| `pyproject.toml` or `requirements.txt` | Python | Ruff |
| `go.mod` | Go | golint, golangci-lint |
| `Gemfile` | Ruby | RuboCop |

### Step 2: Detect Linter and Configuration

**Purpose**: Identify which linter is available and configured

#### JavaScript/TypeScript Linter Detection:

```bash
# Check package.json for ESLint
if grep -q "\"eslint\"" package.json; then
  LINTER="eslint"
  # Check for ESLint config
  ESLINT_CONFIG=""
  [ -f ".eslintrc.json" ] && ESLINT_CONFIG=".eslintrc.json"
  [ -f ".eslintrc.js" ] && ESLINT_CONFIG=".eslintrc.js"
  [ -f "eslint.config.js" ] && ESLINT_CONFIG="eslint.config.js"
  [ -f "eslint.config.mjs" ] && ESLINT_CONFIG="eslint.config.mjs"
  [ -f "eslint.config.ts" ] && ESLINT_CONFIG="eslint.config.ts"

  echo "Detected linter: ESLint"
  echo "Config file: $ESLINT_CONFIG"

# Check for other linters
elif grep -q "\"prettier\"" package.json; then
  LINTER="prettier"
  echo "Detected linter: Prettier"
elif grep -q "\"stylelint\"" package.json; then
  LINTER="stylelint"
  echo "Detected linter: Stylelint"
fi
```

#### Python Linter Detection:

```bash
# Check for Ruff
if grep -q "ruff" pyproject.toml 2>/dev/null || grep -q "ruff" requirements.txt 2>/dev/null; then
  LINTER="ruff"
  echo "Detected linter: Ruff"

# Check for other linters
elif grep -q "flake8" requirements.txt 2>/dev/null; then
  LINTER="flake8"
  echo "Detected linter: Flake8"
elif grep -q "pylint" requirements.txt 2>/dev/null; then
  LINTER="pylint"
  echo "Detected linter: Pylint"
elif grep -q "black" requirements.txt 2>/dev/null; then
  LINTER="black"
  echo "Detected linter: Black"
fi
```

### Step 3: Detect Package Manager

**Purpose**: Determine how to run linter commands

**Package Manager Detection**:

| Language | Manager | Detection | Run Command |
|----------|-----------|------------|-------------|
| JavaScript/TypeScript | npm | `package-lock.json` exists | `npm run <script>` |
| JavaScript/TypeScript | yarn | `yarn.lock` exists | `yarn <script>` |
| JavaScript/TypeScript | pnpm | `pnpm-lock.yaml` exists | `pnpm run <script>` |
| Python | Poetry | `pyproject.toml` exists | `poetry run <script>` |
| Python | pip | `requirements.txt` exists | `python -m <script>` or `<script>` |

**Implementation**:
```bash
# Detect package manager
if [ -f "package-lock.json" ]; then
  PKG_MANAGER="npm"
  RUN_CMD="npm run"
elif [ -f "yarn.lock" ]; then
  PKG_MANAGER="yarn"
  RUN_CMD="yarn"
elif [ -f "pnpm-lock.yaml" ]; then
  PKG_MANAGER="pnpm"
  RUN_CMD="pnpm run"
elif command -v poetry &>/dev/null && [ -f pyproject.toml ]; then
  PKG_MANAGER="poetry"
  RUN_CMD="poetry run"
else
  PKG_MANAGER="pip"
  RUN_CMD=""  # Direct command
fi

echo "Package manager: $PKG_MANAGER"
```

### Step 4: Determine Lint Command

**Purpose**: Build the appropriate command to run the linter

**JavaScript/TypeScript (ESLint)**:
```bash
# Run ESLint with package manager
if [ "$PKG_MANAGER" = "npm" ]; then
  LINT_CMD="npm run lint"
  LINT_FIX_CMD="npm run lint -- --fix"
elif [ "$PKG_MANAGER" = "yarn" ]; then
  LINT_CMD="yarn lint"
  LINT_FIX_CMD="yarn lint --fix"
elif [ "$PKG_MANAGER" = "pnpm" ]; then
  LINT_CMD="pnpm run lint"
  LINT_FIX_CMD="pnpm run lint --fix"
else
  # Direct ESLint command
  LINT_CMD="npx eslint ."
  LINT_FIX_CMD="npx eslint . --fix"
fi

echo "Lint command: $LINT_CMD"
echo "Auto-fix command: $LINT_FIX_CMD"
```

**Python (Ruff)**:
```bash
# Run Ruff with package manager
if [ "$PKG_MANAGER" = "poetry" ]; then
  LINT_CMD="poetry run ruff check ."
  LINT_FIX_CMD="poetry run ruff check . --fix"
else
  # Direct Ruff command
  LINT_CMD="ruff check ."
  LINT_FIX_CMD="ruff check . --fix"
fi

echo "Lint command: $LINT_CMD"
echo "Auto-fix command: $LINT_FIX_CMD"
```

### Step 5: Run Linting

**Purpose**: Execute linter to check code quality

**Implementation**:
```bash
# Run linter
echo ""
echo "🔍 Running linter..."
echo ""

$LINT_CMD

# Capture exit code
LINT_EXIT_CODE=$?

if [ $LINT_EXIT_CODE -eq 0 ]; then
  echo ""
  echo "✅ No linting errors found!"
else
  echo ""
  echo "❌ Linting errors found (exit code: $LINT_EXIT_CODE)"
fi
```

**Linting Output Categories**:

| Category | Description |
|----------|-------------|
| Syntax Errors | Invalid syntax that prevents code from running |
| Style Violations | Code doesn't follow style guidelines |
| Potential Bugs | Code patterns that may cause bugs |
| Deprecation Warnings | Use of deprecated features |
| Type Errors (TypeScript) | Type mismatches or missing type definitions |
| Missing Docstrings | Functions/classes without documentation (industry best practice) |

### Step 6: Apply Auto-Fix

**Purpose**: Use linter's auto-fix capability to resolve fixable errors

**Implementation**:
```bash
if [ $LINT_EXIT_CODE -ne 0 ]; then
  read -p "Apply auto-fix for linting errors? (y/n): " APPLY_FIX

  if [ "$APPLY_FIX" = "y" ]; then
    echo ""
    echo "🔧 Applying auto-fix..."
    echo ""

    # Run auto-fix command
    $LINT_FIX_CMD

    # Capture exit code
    FIX_EXIT_CODE=$?

    if [ $FIX_EXIT_CODE -eq 0 ]; then
      echo ""
      echo "✅ Auto-fix applied successfully!"
    else
      echo ""
      echo "⚠️  Auto-fix completed with errors (exit code: $FIX_EXIT_CODE)"
      echo "Some errors may require manual fixing."
    fi

    # Re-run linting to check remaining errors
    echo ""
    echo "🔍 Re-running linter to check remaining errors..."
    echo ""
    $LINT_CMD
  fi
fi
```

**Auto-Fix Capabilities**:

| Linter | Auto-Fix | What It Fixes |
|--------|-----------|---------------|
| ESLint | `--fix` | Style violations, unused variables, simple syntax issues |
| Prettier | `--write` | Formatting, indentation, quotes |
| Ruff | `--fix` | Style violations, unused imports, simple refactorings |
| Black | Direct | Formatting, indentation, line length |

### Step 7: Display Error Summary

**Purpose**: Show user which files and lines have linting errors

**Implementation**:
```bash
# Get linting errors (language-specific)
if [ "$LINTER" = "eslint" ]; then
  # ESLint JSON output
  $LINT_CMD --format json > /tmp/lint-results.json
  cat /tmp/lint-results.json | jq -r '.[] | "\(.filePath):\(.message) at line \(.line)"'

elif [ "$LINTER" = "ruff" ]; then
  # Ruff output
  $LINT_CMD --output-format concise
fi

# Summary
echo ""
echo "📊 Linting Error Summary:"
echo ""
echo "Total errors: <count>"
echo "Files affected: <count>"
echo "Most common error: <error type>"
```

### Step 8: Guide Error Resolution

**Purpose**: Provide step-by-step guidance for fixing common linting errors

**Common Error Categories**:

#### JavaScript/TypeScript Errors:

| Error Type | Description | Fix |
|-----------|-------------|-----|
| Unused variables | Variables defined but never used | Remove or use variable |
| Missing semicolons | Missing semicolons in JavaScript | Add semicolons |
| Unused imports | Imports not used in file | Remove import |
| React hooks violations | Incorrect React hook usage | Fix hook dependencies/rules |
| No-unused-vars | Variables declared but not used | Remove or use variable |
| prefer-const | Variables could be const | Change `let` to `const` |

#### Python Errors:

| Error Type | Description | Fix |
|-----------|-------------|-----|
| F401 | Unused imports | Remove unused import |
| F841 | Unused variables | Remove or use variable |
| E501 | Line too long | Break long lines |
| W291 | Trailing whitespace | Remove trailing spaces |
| E722 | Missing docstring | Add function docstring |
| F821 | Redefinition of variable | Rename variable |

**Resolution Guidance Template**:
```
For each error found:

1. **File: <file>**
   Line: <line number>
   Error: <error message>

2. **Recommended Fix:**
   <step-by-step fix instructions>

3. **Example:**
   ```<language>
   # Before (incorrect)
   <code>

   # After (corrected)
   <code>
   ```

4. **Apply Fix:**
   <action to take>
```

### Step 9: Re-Verify After Manual Fixes

**Purpose**: Re-run linting after user manually fixes errors

**Implementation**:
```bash
echo ""
read -p "Have you manually fixed the errors? Re-run linting? (y/n): " RE_RUN

if [ "$RE_RUN" = "y" ]; then
  echo ""
  echo "🔍 Re-running linter..."
  echo ""
  $LINT_CMD

  if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All linting errors resolved!"
  else
    echo ""
    echo "⚠️  Some errors remain. Please review and fix."
  fi
fi
```

### Step 10: Commit Linting Fixes

**Purpose**: Commit linting fixes as separate commit (optional)

**Implementation**:
```bash
# Check if there are changes to commit
GIT_STATUS=$(git status --porcelain)

if [ -n "$GIT_STATUS" ]; then
  echo ""
  read -p "Commit linting fixes? (y/n): " COMMIT_FIXES

  if [ "$COMMIT_FIXES" = "y" ]; then
    git add .
    git commit -m "Fix linting errors"

    echo ""
    echo "✅ Linting fixes committed"
  fi
else
  echo ""
  echo "No changes to commit."
fi
```

**Commit Message Options**:

| Context | Commit Message |
|---------|---------------|
| General fixes | `Fix linting errors` |
| ESLint fixes | `Fix ESLint errors` |
| Ruff fixes | `Fix Ruff linting errors` |
| Specific fixes | `Fix <error type> errors` |
 
### Step 11: Check Docstrings (Industry Best Practice)

**Purpose**: Verify all public functions, classes, and methods have proper docstrings

**Implementation**:
```bash
echo ""
echo "📝 Checking docstrings..."
echo ""

# Check for undocumented functions/classes
UNDOC_COUNT=0
MISSING_DOCSTRINGS=()

for file in $(git diff --name-only HEAD~1..HEAD); do
  case "$file" in
    *.py)
      UNDOC=$(grep -c 'def ' "$file" - $(grep -c '"""' "$file"))
      FUNCTIONS=$(grep -c 'def ' "$file")
      ;;
    *.java)
      UNDOC=$(grep -c 'public.*(' "$file" - $(grep -c '/\*\*' "$file"))
      METHODS=$(grep -c 'public.*(' "$file")
      ;;
    *.ts|tsx)
      UNDOC=$(grep -c 'function' "$file" - $(grep -c '/\*\*' "$file"))
      FUNCTIONS=$(grep -c 'function ' "$file")
      ;;
    *.cs|csx)
      UNDOC=$(grep -c 'public.*(' "$file" - $(grep -c '///' "$file"))
      METHODS=$(grep -c 'public.*(' "$file")
      ;;
  esac

  if [[ $UNDOC -gt 0 ]]; then
    UNDOC_COUNT=$((UNDOC_COUNT + UNDOC))
    MISSING_DOCSTRINGS+=("$file")
  fi
done

if [[ $UNDOC_COUNT -gt 0 ]]; then
  echo ""
  echo "❌ Found $UNDOC_COUNT undocumented items:"
  for item in "${MISSING_DOCSTRINGS[@]}"; do
    echo "   - $item"
  done
  echo ""
  echo "💡 Consider using 'docstring-generator' skill to add missing documentation"
else
  echo ""
  echo "✅ All functions/classes have docstrings!"
fi
```

**Docstring Check Results**:
- Count undocumented items
- List files with missing docstrings
- Suggest using docstring-generator skill
- Check docstring format compliance (PEP 257, Javadoc, JSDoc, XML docs)

**Language-Specific Docstring Standards**:

| Language | Docstring Format | Key Tags/Sections |
|-----------|------------------|-------------------|
| Python | PEP 257 (Google, NumPy, Sphinx) | Args, Returns, Raises |
| Java | Javadoc | @param, @return, @throws, @see |
| TypeScript | JSDoc/TSDoc | @param, @returns, @throws, @type |
| C# | XML Documentation Comments | <summary>, <param>, <returns>, <exception> |

## Language-Specific Linter Configuration

### JavaScript/TypeScript

**ESLint Configuration Files** (in priority order):
1. `eslint.config.ts` / `eslint.config.mjs` / `eslint.config.js` (ESLint 9+)
2. `.eslintrc.json`
3. `.eslintrc.js`
4. `.eslintrc.yaml`
5. `package.json` (in `eslintConfig` field)

**Common ESLint Rules**:
- `no-unused-vars`: Detect unused variables
- `no-console`: Detect console statements
- `prefer-const`: Suggest using `const` over `let`
- `eqeqeq`: Enforce `===` instead of `==`
- `no-var`: Require `let`/`const` instead of `var`
- React hooks rules: Enforce correct React hook usage

### Python

**Ruff Configuration Files**:
1. `pyproject.toml` (in `[tool.ruff]` section)
2. `.ruff.toml`
3. `ruff.toml`

**Common Ruff Rules**:
- `F401`: Unused imports
- `F841`: Unused variables
- `E501`: Line too long (> 88 characters)
- `W291`: Trailing whitespace
- `E722`: Missing docstrings
- `I001`: Import ordering

## Best Practices

- **Linting Before Commit**: Always run linting before committing code
- **Auto-Fix First**: Apply auto-fix before manual fixes
- **Incremental Fixes**: Fix errors in batches, re-run linting between batches
- **Clear Commit Messages**: Describe what was fixed in commit message
- **Fix Linting Errors**: Don't disable rules as a workaround
- **Consistent Style**: Follow language and project style guidelines
- **Editor Configuration**: Configure editor to run linting on save
- **CI/CD Integration**: Include linting in automated pipelines
- **Pre-Commit Hooks**: Use Husky or pre-commit to enforce linting

## Common Issues

### Linter Not Found

**Issue**: Linter is not installed or not found in PATH

**Solution**:
```bash
# JavaScript/TypeScript: Install ESLint
npm install --save-dev eslint

# Python: Install Ruff
pip install ruff
# Or with Poetry
poetry add --group dev ruff
```

### Configuration File Not Found

**Issue**: Linter cannot find configuration file

**Solution**:
```bash
# Verify config file exists
ls -la | grep -E "(eslint|ruff|pylint)"

# Create default config if missing
# ESLint
cat > .eslintrc.json <<EOF
{
  "extends": "eslint:recommended",
  "rules": {}
}
EOF

# Ruff
cat > pyproject.toml <<EOF
[tool.ruff]
line-length = 88
target-version = "py311"
EOF
```

### Too Many Errors

**Issue**: Large number of linting errors at once

**Solution**:
- Focus on one category at a time (syntax, style, etc.)
- Fix errors incrementally
- Re-run linting after each fix batch
- Use editor integration to fix errors as you go

### Auto-Fix Doesn't Work

**Issue**: `--fix` flag doesn't resolve errors

**Solution**:
- Some errors require manual intervention (semantic issues)
- Review error messages for guidance
- Check if linter supports auto-fix for that rule
- Manually fix and re-run linting

### Git Changes Conflict

**Issue**: Linting fixes conflict with other uncommitted changes

**Solution**:
```bash
# Stage only linting fixes
git add <files-with-linting-fixes>

# Commit linting fixes separately
git commit -m "Fix linting errors"
```

## Troubleshooting Checklist

Before linting:
- [ ] Language is detected correctly
- [ ] Linter is installed
- [ ] Configuration file exists
- [ ] Package manager is detected
- [ ] Working directory is clean (or changes are staged)

After linting:
- [ ] Linting command executed successfully
- [ ] Errors are categorized and displayed
- [ ] Auto-fix is attempted (if errors found)
- [ ] User receives guidance for manual fixes
- [ ] Linting is re-run after fixes

After committing fixes:
- [ ] Linting fixes are committed
- [ ] Commit message is clear
- [ ] No unintended changes are included
- [ ] Working tree is clean (or ready for next step)

## Related Commands

```bash
# JavaScript/TypeScript
npm run lint                    # Run linter
npm run lint -- --fix           # Run linter with auto-fix
npm install --save-dev eslint  # Install ESLint
npx eslint .                  # Run ESLint directly

# Python
poetry run ruff check .         # Run Ruff with Poetry
poetry run ruff check . --fix    # Run Ruff with auto-fix
ruff check .                   # Run Ruff directly
pip install ruff               # Install Ruff

# Git
git add .                      # Stage changes
git commit -m "Fix linting"     # Commit changes
git status                      # Check git status
```

## Relevant Skills

Language-specific linting skills that use this framework:
- `python-ruff-linter`: Python-specific Ruff linting guidance
- (Future) `javascript-eslint-linter`: JavaScript/TypeScript-specific ESLint guidance

Supporting framework skills:
- `pr-creation-workflow`: For running linting before PR creation
- `test-generator-framework`: For ensuring code quality before testing
