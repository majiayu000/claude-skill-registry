---
name: prettierignore
description: Generates .prettierignore to exclude build outputs, dependencies, and generated files from Prettier formatting. Prevents formatting of dist/, node_modules/, and coverage/ directories.
---

# Prettier Ignore Skill

## Purpose
Generate `.prettierignore` file to exclude build outputs, dependencies, and generated files from Prettier formatting.

## 🚨 MANDATORY FILE COUNT
**Expected Output**: **1 file**
- `.prettierignore` (standard format)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

Perform these checks in order before generating the file:

1. **Prettier Version**: Verify latest stable version and ignore file support
   - Run: `npm view prettier version`
   - **Check documentation**: Confirm `.prettierignore` format still supported
   - **If deprecated**: Use alternative format (e.g., config-based ignore)

2. **Build Output Detection**: Identify build directories from project config
   - **Check `vite.config.ts` or `vite.config.js`**:
     - Look for `build.outDir` property (default: `dist`)
     - If custom output dir found → Use that directory name
   - **Check `package.json` scripts**:
     - Look for build output paths in scripts
   - **Default**: Use `dist/` if no custom output detected

3. **Test Coverage Detection**: Check if test framework generates coverage reports
   - **Check for test framework** (from jest-config or vitest-config skills):
     - If `jest.config.js` exists → Check `coverageDirectory` (default: `coverage/`)
     - If `vitest.config.ts` exists → Check `test.coverage.reportsDirectory`
   - **Check `package.json` test scripts**:
     - Look for `--coverage` flag or coverage directory references
   - **Default**: Include `coverage/` in ignore patterns

4. **Package Manager Detection**: Identify which package manager is used
   - **Check for lock files**:
     - `package-lock.json` → npm
     - `yarn.lock` → yarn  
     - `pnpm-lock.yaml` → pnpm
   - **Note**: Lock files should NOT be in `.prettierignore` (formatting not applicable)
   - **Always exclude**: `node_modules/`

5. **Minified/Bundled Files**: Check for generated JavaScript patterns
   - **Standard patterns**: `*.min.js`, `*.bundle.js`
   - **Check build config**: Look for additional minified output patterns
   - **Always exclude**: Prevents formatting of production bundles

6. **Verify Glob Pattern Support**: Confirm pattern syntax compatibility
   - **Reference**: https://prettier.io/docs/en/ignore.html
   - **Test patterns**: Ensure glob syntax matches Prettier's expectations
   - **Common patterns**: `*/`, `**/*.ext`, negation with `!`

7. **Cross-Skill Coordination**: Verify consistency with other ignore files
   - **Check `.gitignore`**: Ensure `.prettierignore` doesn't format git-ignored generated files
   - **Check `.eslintignore`**: Similar exclusion patterns should align
   - **Principle**: Don't format files that are ignored by version control or linting

8. **Performance Optimization**: Validate ignore patterns reduce unnecessary processing
   - **Large directories**: `node_modules/`, `dist/`, `build/` significantly impact performance
   - **Generated files**: Coverage reports, minified bundles don't need formatting
   - **Benchmark**: Prettier should skip excluded files entirely (zero processing time)

## Execution Checklist

Execute in this order:

- [ ] 1. Verify `.prettierignore` format is still supported by latest Prettier
- [ ] 2. Detect build output directory from vite.config.ts (default: `dist/`)
- [ ] 3. Detect test coverage directory from test config (default: `coverage/`)
- [ ] 4. Identify package manager (npm/yarn/pnpm) for node_modules exclusion
- [ ] 5. Verify glob patterns are valid Prettier ignore syntax
- [ ] 6. Cross-check with `.gitignore` for consistency
- [ ] 7. Generate `.prettierignore` with minimal essential exclusions
- [ ] 8. Run validation script to confirm file exists and patterns are valid

## Output

### Primary Format: `.prettierignore`

```
# Build outputs
dist/
build/

# Dependencies
node_modules/

# Test coverage
coverage/

# Minified/bundled files
*.min.js
*.bundle.js
```

## Template
See: `examples.md` in this directory for complete template and detailed examples.

## 🛑 BLOCKING VALIDATION - MUST RUN AFTER FILE GENERATION

### Validation Script

Run this script after generating `.prettierignore` to verify correctness:

```bash
#!/bin/bash
# Prettier Ignore Validation Script

echo "🔍 Validating .prettierignore..."

# Check if file exists
if [ ! -f ".prettierignore" ]; then
  echo "❌ BLOCKING ERROR: .prettierignore file not found"
  exit 1
fi

# Check if file is not empty
if [ ! -s ".prettierignore" ]; then
  echo "❌ BLOCKING ERROR: .prettierignore is empty"
  exit 1
fi

# Check for required patterns
REQUIRED_PATTERNS=("dist/" "node_modules/" "coverage/")
for pattern in "${REQUIRED_PATTERNS[@]}"; do
  if ! grep -q "$pattern" .prettierignore; then
    echo "⚠️  WARNING: Missing recommended pattern: $pattern"
  fi
done

# Check glob pattern syntax (basic validation)
if grep -qE '^[^#].*\*\*.*\*\*' .prettierignore; then
  echo "⚠️  WARNING: Potential invalid glob pattern (multiple **)"
fi

echo "✅ .prettierignore validation passed"
exit 0
```

**Usage**: `bash validate-prettierignore.sh`

### Manual Verification

After generation, manually verify:

1. **File exists**: `ls -la .prettierignore`
2. **Content check**: `cat .prettierignore`
3. **Pattern test**: `prettier --check "**/*" --ignore-path .prettierignore` (should skip excluded paths)
4. **Performance test**: Verify Prettier runs faster with ignore file (compare with/without)

## Key Features
- **Minimal Exclusions**: Only essential patterns (build, deps, coverage, minified)
- **Performance Optimized**: Skips large directories that don't need formatting
- **Build-Aware**: Automatically detects custom build output directories
- **Coverage-Aware**: Excludes test coverage reports based on test framework config
- **Glob Patterns**: Uses standard ignore syntax compatible with Prettier
- **Cross-Tool Consistency**: Aligns with `.gitignore` and `.eslintignore`

### Pattern Philosophy
- **Build outputs**: Never format generated production code
- **Dependencies**: Skip third-party code in node_modules
- **Coverage reports**: Exclude auto-generated test reports
- **Minified files**: Don't format compressed/bundled JavaScript
- **Performance**: Only ignore what's necessary for speed improvement

### Configuration Strategy
- **Minimal approach**: Keep ignore list short and focused
- **No source code**: Never exclude `src/` or application code
- **No configs**: Format all config files (package.json, tsconfig.json, etc.)
- **No lock files**: These don't apply to Prettier (not formatted)
- **Glob efficiency**: Use directory patterns (`dir/`) over file globs when possible

### Integration Considerations
- **Git alignment**: Ensure git-ignored build outputs are also Prettier-ignored
- **CI/CD**: Verify ignore patterns work in automated formatting checks
- **Pre-commit hooks**: Lint-staged should respect `.prettierignore` patterns
- **Editor plugins**: VSCode Prettier extension respects this file

### Maintenance Considerations
- **Prettier updates**: Check release notes for ignore file format changes
- **Build config changes**: Update ignore patterns if output directory changes
- **New generated files**: Add patterns for new auto-generated content
- **Performance monitoring**: Verify ignore patterns still provide speed benefits
