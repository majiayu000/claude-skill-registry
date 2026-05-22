---
name: module-scaffolding
description: Module scaffolding using Yeoman generator including validation and sync-meta
---

# Module Scaffolding Patterns

## Author Email Configuration

**IMPORTANT**: The `--author` parameter should be read from the user's global CLAUDE.md configuration file:
- **Location**: `~/.claude/CLAUDE.md`
- **Format**: Look for the line `my work email is <email>`
- **Usage**: Extract the email and pass it to the Yeoman generator
- **Never hardcode**: Use the placeholder `<email-from-global-CLAUDE.md>` in documentation

Example from global CLAUDE.md:
```markdown
- my work email is user@company.com. use this as author in my new projects
```

The module-scaffolder agent should parse this file and extract the email automatically.

## Critical Scaffolding Sequence

**This sequence MUST be followed exactly:**

1. **Yeoman generator** - Creates module structure
2. **`npm run sync-meta`** - Syncs package.json → api.yml (CRITICAL!)
3. **`npm install`** - Installs dependencies
4. **Build/validation** - Comes later in Phase 7

**NEVER skip sync-meta** - api.yml title/version must match package.json.

## Yeoman Generator Execution

### Basic Pattern

```bash
# Navigate to repository root
cd /Users/ctamas/code/zborg/module

# Run @auditmation/hub-module generator with parameters
yo @auditmation/hub-module \
  --productPackage '@zerobias-org/product-{vendor}-{product}' \
  --modulePackage '@zerobias-org/module-{vendor}-{product}' \
  --packageVersion '0.0.0' \
  --description '{ServiceName}' \
  --repository 'https://github.com/zerobias-org/module' \
  --author '<email-from-global-CLAUDE.md>'
```

### Example: Bitbucket Module

```bash
yo @auditmation/hub-module \
  --productPackage '@zerobias-org/product-bitbucket-bitbucket' \
  --modulePackage '@zerobias-org/module-bitbucket-bitbucket' \
  --packageVersion '0.0.0' \
  --description 'Bitbucket' \
  --repository 'https://github.com/zerobias-org/module' \
  --author '<email-from-global-CLAUDE.md>'
```

### Parameter Rules

- `--productPackage`: Product package from @product-specialist (must be installed via npm first)
- `--modulePackage`: Module package name (replace 'product-' with 'module-')
- `--packageVersion`: Start at `0.0.0` for new modules
- `--description`: Service display name (capitalized, e.g., 'Bitbucket', 'Jira', 'S3')
- `--repository`: Fixed URL: `https://github.com/zerobias-org/module`
- `--author`: User's email from global CLAUDE.md (`~/.claude/CLAUDE.md`)

## Metadata Sync Pattern

### CRITICAL: Always Run sync-meta After Yeoman

```bash
cd package/<vendor>/<product>

# Sync package.json metadata to api.yml
npm run sync-meta
```

**What sync-meta does:**
- Reads `title` and `version` from package.json
- Writes them to api.yml automatically
- Ensures api.yml always matches package.json

**Why this matters:**
- api.yml title/version MUST match package.json
- Manual edits get overwritten by sync-meta
- Sync-meta runs automatically on version bumps
- Validation checks WILL fail if not synced

**NEVER manually edit** api.yml title/version - always use sync-meta.

## Scaffold Output Verification

### Check Created Structure

```bash
ls -la package/<vendor>/<product>/

# Required files:
- package.json ✓
- tsconfig.json ✓
- .eslintrc ✓
- .gitignore ✓
- .mocharc.json ✓
- connectionProfile.yml ✓
- .npmrc (symlink) ✓
- .nvmrc (symlink) ✓

# Required directories:
- src/ ✓
- test/unit/ ✓
- test/integration/ ✓
```

## Dependency Installation

### Install After sync-meta

```bash
# Already in module directory after scaffold
npm install
```

**Sequence matters:**
1. Yeoman creates structure
2. sync-meta updates api.yml
3. npm install (only after sync-meta)

## Comprehensive Validation Checklist

**Agent must run ALL validations and report results:**

```bash
# Navigate to module directory first
cd package/${VENDOR}/${SUITE}/${SERVICE}  # or package/${VENDOR}/${SERVICE}

# ===== VALIDATION 1: Directory Structure =====
echo "Validation 1: Directory structure"
ls -la | grep -E "package.json|api.yml|connectionProfile.yml|connectionState.yml|src|test"
# Expected: All files/directories present

# ===== VALIDATION 2: package.json Metadata =====
echo "Validation 2: package.json metadata"
jq -r '.name, .moduleId, .author' package.json
# Expected:
# - name: @zerobias-org/module-{vendor}-{suite?}-{service}
# - moduleId: {vendor}-{suite?}-{service}
# - author: {correct_email}

# ===== VALIDATION 3: api.yml Product Reference =====
echo "Validation 3: api.yml product reference"
grep -q "x-product-infos" api.yml && echo "✓ Product reference present" || echo "✗ FAILED: Missing x-product-infos"
# Expected: ✓ Product reference present

# ===== VALIDATION 4: api.yml Title and Version =====
echo "Validation 4: api.yml title and version"
TITLE_VERSION_COUNT=$(grep -E "^(title|version):" api.yml | wc -l | tr -d ' ')
if [ "$TITLE_VERSION_COUNT" -eq 2 ]; then
  echo "✓ Title and version present"
  grep -E "^(title|version):" api.yml
else
  echo "✗ FAILED: Expected 2 (title + version), found $TITLE_VERSION_COUNT"
fi
# Expected: 2 lines (title: and version:)

# ===== VALIDATION 5: connectionProfile.yml Stub Exists =====
echo "Validation 5: connectionProfile.yml stub"
if [ -f "connectionProfile.yml" ]; then
  echo "✓ connectionProfile.yml stub exists (will be designed in Phase 3)"
  head -n 5 connectionProfile.yml
else
  echo "✗ FAILED: connectionProfile.yml stub missing (Yeoman should create this)"
fi

# ===== VALIDATION 6: connectionState.yml Stub Exists =====
echo "Validation 6: connectionState.yml stub"
if [ -f "connectionState.yml" ]; then
  echo "✓ connectionState.yml stub exists (will be designed in Phase 3)"
  head -n 5 connectionState.yml
else
  echo "✗ FAILED: connectionState.yml stub missing (Yeoman should create this)"
fi

# ===== VALIDATION 7: Source Files Exist =====
echo "Validation 7: Source files"
SRC_INDEX=$([ -f "src/index.ts" ] && echo "✓" || echo "✗ FAILED")
SRC_IMPL=$(ls src/*Impl.ts 2>/dev/null | head -n 1)
if [ -n "$SRC_IMPL" ]; then
  echo "✓ Implementation file: $SRC_IMPL"
else
  echo "✗ FAILED: No *Impl.ts found in src/"
fi
# Expected: src/index.ts and src/{Service}Impl.ts exist

# ===== VALIDATION 8: Test Files Exist =====
echo "Validation 8: Test files"
UNIT_TEST=$(ls test/unit/*Test.ts 2>/dev/null | head -n 1 || ls test/unit/*Impl.ts 2>/dev/null | head -n 1)
INTEGRATION_TEST=$(ls test/integration/*Test.ts 2>/dev/null | head -n 1 || ls test/integration/Common.ts 2>/dev/null)

if [ -n "$UNIT_TEST" ]; then
  echo "✓ Unit test: $UNIT_TEST"
else
  echo "✗ FAILED: No unit test found"
fi

if [ -n "$INTEGRATION_TEST" ]; then
  echo "✓ Integration test: $INTEGRATION_TEST"
else
  echo "⚠ WARNING: No integration test found (may be added later)"
fi

# ===== VALIDATION 9: Dependencies Installed =====
echo "Validation 9: Dependencies installed"
if [ -d "node_modules" ] && [ -f "package-lock.json" ]; then
  PACKAGE_COUNT=$(ls node_modules | wc -l | tr -d ' ')
  echo "✓ node_modules exists ($PACKAGE_COUNT packages)"
else
  echo "✗ FAILED: Dependencies not installed"
fi

# ===== VALIDATION 10: Symlinks Created =====
echo "Validation 10: Symlinks"
if [ -L ".npmrc" ]; then
  NPMRC_TARGET=$(readlink .npmrc)
  echo "✓ .npmrc → $NPMRC_TARGET"
else
  echo "⚠ WARNING: .npmrc symlink not created (may not be needed)"
fi

if [ -L ".nvmrc" ]; then
  NVMRC_TARGET=$(readlink .nvmrc)
  echo "✓ .nvmrc → $NVMRC_TARGET"
else
  echo "⚠ WARNING: .nvmrc symlink not created (may not be needed)"
fi

# ===== VALIDATION 11: TypeScript Configuration Valid =====
echo "Validation 11: TypeScript configuration"
if npx tsc --showConfig > /dev/null 2>&1; then
  echo "✓ tsconfig.json valid"
else
  echo "✗ FAILED: tsconfig.json invalid"
fi

# ===== VALIDATION SUMMARY =====
echo ""
echo "========================================="
echo "SCAFFOLDING VALIDATION COMPLETE"
echo "========================================="
echo "All critical validations passed ✓"
echo "Module ready for Phase 3 (API Specification)"
echo ""
echo "NOTE: Build validation deferred to Phase 7"
echo "      (stubs are not yet fully implemented)"
```

## Output File Pattern

### Write Results to Memory

```bash
# Write results to output file
OUTPUT_PATH="${MEMORY_PATH}/${OUTPUT_FILE}"
cat > "${OUTPUT_PATH}" <<EOF
{
  "phase": 2,
  "name": "Module Scaffolding",
  "status": "completed",
  ...
}
EOF
```

## Standard Output Format

**File:** `${PROJECT_ROOT}/.claude/.localmemory/{workflow}-{module-id}/{outputFile}`

**Example:** `.claude/.localmemory/create-module-github-github/phase-02-scaffolding.json`

**Required Structure:**

```json
{
  "phase": 2,
  "name": "Module Scaffolding",
  "status": "completed",
  "timestamp": "2025-10-08T10:30:00Z",
  "modulePath": "package/github/github",
  "moduleIdentifier": "github-github",
  "components": {
    "vendor": "github",
    "suite": null,
    "service": "github"
  },
  "yeomanCommand": "yo @auditmation/hub-module --productPackage '@auditlogic/product-github-github' --modulePackage '@zerobias-org/module-github-github' --packageVersion '0.0.0' --description 'GitHub' --repository 'https://github.com/zerobias-org/module' --author '<email-from-global-CLAUDE.md>'",
  "generatedFiles": {
    "packageJson": "package/github/github/package.json",
    "apiYml": "package/github/github/api.yml",
    "connectionProfile": "package/github/github/connectionProfile.yml",
    "connectionState": "package/github/github/connectionState.yml",
    "tsconfig": "package/github/github/tsconfig.json",
    "sourceIndex": "package/github/github/src/index.ts",
    "sourceImpl": "package/github/github/src/GithubImpl.ts",
    "unitTest": "package/github/github/test/unit/GithubTest.ts",
    "integrationTest": "package/github/github/test/integration/ConnectionTest.ts"
  },
  "validations": {
    "1_directoryStructure": {
      "name": "Directory structure",
      "status": "passed"
    },
    "2_packageJsonMetadata": {
      "name": "package.json metadata",
      "status": "passed",
      "details": {
        "name": "@zerobias-org/module-github-github",
        "moduleId": "github-github",
        "author": "<email-from-global-CLAUDE.md>"
      }
    },
    "3_apiYmlProductReference": {
      "name": "api.yml product reference",
      "status": "passed"
    },
    "4_apiYmlTitleVersion": {
      "name": "api.yml title and version",
      "status": "passed",
      "details": {
        "title": "GitHub API",
        "version": "0.0.0"
      }
    },
    "5_connectionProfileStubExists": {
      "name": "connectionProfile.yml stub exists",
      "status": "passed",
      "note": "Stub only - will be designed by @credential-manager + @api-architect in Phase 3"
    },
    "6_connectionStateStubExists": {
      "name": "connectionState.yml stub exists",
      "status": "passed",
      "note": "Stub only - will be designed by @credential-manager + @api-architect in Phase 3"
    },
    "7_sourceFilesExist": {
      "name": "Source files exist",
      "status": "passed",
      "details": {
        "index": "src/index.ts",
        "implementation": "src/GithubImpl.ts"
      }
    },
    "8_testFilesExist": {
      "name": "Test files exist",
      "status": "passed",
      "details": {
        "unit": "test/unit/GithubTest.ts",
        "integration": "test/integration/ConnectionTest.ts"
      }
    },
    "9_dependenciesInstalled": {
      "name": "Dependencies installed",
      "status": "passed",
      "details": {
        "packageCount": 247
      }
    },
    "10_symlinksCreated": {
      "name": "Symlinks created",
      "status": "passed",
      "details": {
        "npmrc": "../../../.npmrc",
        "nvmrc": "../../../.nvmrc"
      }
    },
    "11_typescriptConfigValid": {
      "name": "TypeScript configuration valid",
      "status": "passed"
    }
  },
  "validationSummary": {
    "total": 11,
    "passed": 11,
    "failed": 0,
    "warnings": 0
  },
  "note": "Build validation deferred to Phase 7 (stubs are not yet fully implemented)",
  "gitCommit": {
    "status": "committed",
    "hash": "abc123def456",
    "message": "chore: scaffold github-github module"
  }
}
```

## Tools and Commands

### Check for Generator

```bash
# List available generators
yo --help

# Check if module generator exists
npm run | grep create-module
```

### Execute Generator

```bash
# Yeoman @auditmation/hub-module generator
yo @auditmation/hub-module \
  --productPackage '@zerobias-org/product-bitbucket-bitbucket' \
  --modulePackage '@zerobias-org/module-bitbucket-bitbucket' \
  --packageVersion '0.0.0' \
  --description 'Bitbucket' \
  --repository 'https://github.com/zerobias-org/module' \
  --author '<email-from-global-CLAUDE.md>'

# All parameters are required
# Product package must be installed first (npm install @zerobias-org/product-{vendor}-{product})
# Author email is read from ~/.claude/CLAUDE.md
```

### Verify Symlinks

```bash
cd package/<vendor>/<product>
ls -la | grep "^l"  # List symlinks
readlink .npmrc     # Verify target
readlink .nvmrc
```

### Post-Scaffold Validation

```bash
# Check package.json validity
cat package.json | jq .

# Verify TypeScript config
npx tsc --showConfig

# Test npm scripts exist
npm run | grep -E "(build|test|generate)"
```

## Success Criteria

Scaffolding MUST meet all criteria:

- ✅ Generator executes without errors
- ✅ All required files and directories created
- ✅ **npm run sync-meta executed** (CRITICAL - validates api.yml synced)
- ✅ api.yml title and version **synced from package.json** (not manually edited)
- ✅ Symlinks point to correct locations
- ✅ npm install completes successfully
- ✅ package.json has valid JSON and correct fields
- ✅ Module structure matches template standards
- ✅ TypeScript configuration is valid
- ✅ Ready for next phase (API specification design)
- ⏭️  Build validation deferred to Phase 7 (after implementation)

## Common Issues and Solutions

### Issue: Generator Not Found

```bash
# Install @auditmation/hub-module generator globally
npm install -g @auditmation/hub-module

# Or install Yeoman if not present
npm install -g yo

# Verify installation
yo --version
yo --generators  # Should show @auditmation/hub-module
```

### Issue: Symlinks Broken

```bash
# Recreate symlinks
cd package/<vendor>/<product>
rm .npmrc .nvmrc
ln -s ../../../.npmrc .npmrc
ln -s ../../../.nvmrc .nvmrc
```

### Issue: Missing Directories

```bash
# Create missing directories
mkdir -p src test/unit test/integration
```

### Issue: npm install Fails

```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: api.yml Missing Title/Version

**Cause:** Forgot to run `npm run sync-meta`

**Fix:** ALWAYS run sync-meta after Yeoman, BEFORE npm install

```bash
cd package/{vendor}/{service}
npm run sync-meta

# Validate
grep -E "^(title|version):" api.yml
```

### Issue: Title/Version Don't Match package.json

**Cause:** Manually edited api.yml

**Fix:** NEVER manually edit - always use sync-meta

```bash
# Correct workflow:
1. Edit package.json version (if needed)
2. Run: npm run sync-meta
3. api.yml updates automatically

# Validation:
PACKAGE_VERSION=$(jq -r '.version' package.json)
API_VERSION=$(grep "^version:" api.yml | awk '{print $2}')
[ "$PACKAGE_VERSION" == "$API_VERSION" ] && echo "✓ Synced" || echo "✗ Out of sync"
```

### Issue: Build Fails After Scaffolding

**Cause:** Wrong sequence or missing sync-meta

**Fix:** Follow EXACT sequence:

```bash
1. yo @auditmation/hub-module ...  # Yeoman
2. npm run sync-meta               # Sync (CRITICAL!)
3. npm install                     # Dependencies
4. npm run build                   # Build

# Sequence matters - sync-meta MUST come before npm install
```
