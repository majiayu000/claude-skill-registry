---
name: quality-gates
description: Run comprehensive quality checks including linting, type checking, tests, and security audits before commits or deployments
version: 1.0.0
author: AI-Vibe-Prompts
tags: [quality, testing, linting, security, ci-cd]
auto_invoke: true
---

# Quality Gates Skill

## Objective

Enforce code quality standards by running automated checks that must pass before code can be committed, merged, or deployed. Acts as a guardian ensuring consistent quality across the codebase.

## When to Use This Skill

Auto-invoke when:
- User completes feature implementation
- Before creating commits or pull requests
- User asks to "test", "validate", "check quality", or "verify"
- Before deployment or release
- After significant refactoring

## Quality Gate Levels

### Level 1: Pre-Commit Gates (Fast, < 30 seconds)
Essential checks that run before every commit.

### Level 2: Pre-Push Gates (Moderate, < 2 minutes)
Comprehensive checks before pushing to remote.

### Level 3: Pre-Deploy Gates (Thorough, < 5 minutes)
Complete validation before production deployment.

## Gate Execution Workflow

### Gate 1: Linting (JavaScript/TypeScript)

**Purpose**: Enforce code style and catch common errors

**Tools**: Bash, Read

**Process**:
1. **Detect linter** by checking for:
   - ESLint: `.eslintrc*`, `eslint.config.*`
   - Biome: `biome.json`
   - None: Skip this gate

2. **Read package.json** to find lint script:
   ```json
   "scripts": {
     "lint": "eslint .",
     "lint:fix": "eslint . --fix"
   }
   ```

3. **Execute linter**:
   ```bash
   # Try to run lint script
   npm run lint
   
   # If fails, try direct commands
   npx eslint . || npx biome check .
   ```

4. **Parse results**:
   - Exit code 0: ✅ PASS
   - Exit code non-zero: ❌ FAIL
   - Extract error count and file locations

5. **Auto-fix attempt** (if failures found):
   ```bash
   npm run lint:fix || npx eslint . --fix
   ```

**Success Criteria**: Zero linting errors (warnings acceptable)

### Gate 2: Type Checking (TypeScript)

**Purpose**: Verify type safety and catch type errors

**Tools**: Bash, Read, Grep

**Process**:
1. **Detect TypeScript** by checking for:
   - `tsconfig.json`
   - TypeScript in dependencies

2. **Read tsconfig.json** to check strictness:
   - `strict: true`
   - `noImplicitAny`, `strictNullChecks`, etc.

3. **Execute type checker**:
   ```bash
   # Try to run typecheck script
   npm run typecheck || npm run type-check
   
   # If no script, run directly
   npx tsc --noEmit
   ```

4. **Parse results**:
   - Exit code 0: ✅ PASS
   - Exit code non-zero: ❌ FAIL
   - Extract error count and locations

**Success Criteria**: Zero type errors

### Gate 3: Unit & Integration Tests

**Purpose**: Verify code functionality and prevent regressions

**Tools**: Bash, Read, Grep

**Process**:
1. **Detect test framework**:
   - Vitest: `vitest.config.*`, `vitest` in dependencies
   - Jest: `jest.config.*`, `jest` in dependencies
   - Native test: `--test` flag with Node.js 20+

2. **Count test files**:
   ```bash
   # Use Grep to find test files
   find . -name "*.test.*" -o -name "*.spec.*" | wc -l
   ```

3. **Execute tests**:
   ```bash
   # Run unit tests (fast)
   npm run test || npm run test:unit
   
   # Or direct command
   npx vitest run || npx jest --ci
   ```

4. **Parse results**:
   - Total tests run
   - Passed / Failed / Skipped
   - Coverage percentage (if available)

5. **Coverage check** (if configured):
   ```bash
   npm run test:coverage
   
   # Check if meets threshold (e.g., 80%)
   ```

**Success Criteria**: 
- All tests pass (100%)
- Coverage ≥ configured threshold (if set)

### Gate 4: Build Verification

**Purpose**: Ensure code compiles and builds without errors

**Tools**: Bash

**Process**:
1. **Detect build system**:
   - Next.js: `next build`
   - Vite: `vite build`
   - Webpack: `webpack --mode production`
   - TypeScript: `tsc`

2. **Execute build**:
   ```bash
   npm run build
   ```

3. **Check build artifacts**:
   - Verify output directory exists: `dist/`, `build/`, `.next/`
   - Check for build errors in logs

4. **Clean up** (optional):
   ```bash
   # Remove build artifacts to save space
   rm -rf dist/ build/ .next/
   ```

**Success Criteria**: Build completes with exit code 0

### Gate 5: Security Audit

**Purpose**: Identify known vulnerabilities in dependencies

**Tools**: Bash, Read

**Process**:
1. **Run npm/pnpm audit**:
   ```bash
   npm audit --json || pnpm audit --json
   ```

2. **Parse audit results**:
   - Critical vulnerabilities: 0
   - High vulnerabilities: 0
   - Moderate vulnerabilities: < threshold
   - Low vulnerabilities: informational

3. **Check for specific vulnerabilities**:
   - Prototype pollution
   - Remote code execution (RCE)
   - SQL injection
   - Cross-site scripting (XSS)

4. **Suggest fixes**:
   ```bash
   npm audit fix
   # or
   npm audit fix --force  # (if safe)
   ```

**Success Criteria**: 
- Zero critical/high vulnerabilities
- Moderate vulnerabilities acknowledged or fixed

### Gate 6: Code Complexity Analysis (Optional)

**Purpose**: Flag overly complex code that may need refactoring

**Tools**: Grep, Bash

**Process**:
1. **Detect code complexity tools**:
   - eslint-plugin-complexity
   - SonarQube
   - CodeClimate

2. **Basic complexity checks**:
   ```bash
   # Find files with excessive lines
   find src -name "*.{ts,tsx,js,jsx}" -exec wc -l {} \; | awk '$1 > 500'
   
   # Find deeply nested code (>5 levels)
   grep -rn "^[[:space:]]\{20,\}" src/
   
   # Count TODO/FIXME
   grep -rn "TODO\|FIXME\|HACK" src/ | wc -l
   ```

**Success Criteria**: 
- No files > 500 lines (warning only)
- No nesting > 5 levels (warning only)

### Gate 7: Git Pre-Commit Checks

**Purpose**: Ensure commit quality and prevent sensitive data leaks

**Tools**: Bash, Grep

**Process**:
1. **Check for sensitive data**:
   ```bash
   # Search for API keys, secrets, tokens
   git diff --cached | grep -i "api[_-]key\|secret\|password\|token"
   
   # Check for .env files being committed
   git diff --cached --name-only | grep "\.env$"
   ```

2. **Validate commit message** (if Conventional Commits):
   - Format: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, test, chore

3. **Check file sizes**:
   ```bash
   # Flag files > 1MB
   git diff --cached --name-only | xargs ls -lh | awk '$5 > 1000000'
   ```

**Success Criteria**: 
- No secrets in diff
- No .env files
- No large files (> 1MB)

## Execution Strategy

### Sequential Execution (Default)
Run gates in order, stop on first failure:
```
Lint → TypeCheck → Test → Build → Audit
```

### Parallel Execution (Fast Mode)
Run independent gates simultaneously:
```
[Lint + TypeCheck + Test] → Build → Audit
```

### Selective Execution
Run only relevant gates based on changes:
- `.ts/.tsx` files changed → TypeCheck
- Dependencies updated → Audit
- Test files changed → Tests only

## Output Format

```markdown
# Quality Gate Results

## Summary
✅ 5/7 Gates Passed | ❌ 2/7 Gates Failed

## Gate Details

### ✅ Gate 1: Linting
- **Status**: PASS
- **Duration**: 3.2s
- **Details**: 0 errors, 2 warnings

### ❌ Gate 2: Type Checking
- **Status**: FAIL
- **Duration**: 5.1s
- **Errors**: 3 type errors found
  - `src/components/Button.tsx:15` - Property 'onClick' is missing
  - `src/utils/api.ts:42` - Type 'string' is not assignable to type 'number'
  - `src/hooks/useAuth.ts:8` - Cannot find name 'User'

### ✅ Gate 3: Tests
- **Status**: PASS
- **Duration**: 12.4s
- **Tests**: 124 passed, 0 failed, 2 skipped
- **Coverage**: 87% (target: 80%)

### ⏭️ Gate 4: Build
- **Status**: SKIPPED (previous gate failed)

### ⏭️ Gate 5: Security Audit
- **Status**: SKIPPED (previous gate failed)

## Action Required
Fix the 3 type errors in Gate 2 before proceeding.

## Recommendations
1. Run `npm run typecheck` locally to see full error details
2. Consider adding pre-commit hooks to catch these earlier
3. Current code coverage (87%) exceeds target - excellent work!
```

## Integration with Git Hooks

### Setup Husky + lint-staged (Recommended)

**Check if installed**:
```bash
test -d .husky && echo "Husky installed" || echo "Husky not found"
```

**Suggest installation** if missing:
```bash
npm install --save-dev husky lint-staged
npx husky init
```

**Configure .husky/pre-commit**:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run quality gates
npm run lint
npm run typecheck
npm run test
```

### Alternative: git commit -m with manual checks

If no hooks, prompt user:
```
⚠️  No pre-commit hooks detected.
Would you like me to run quality gates before committing? (Recommended)
```

## Progressive Quality Gates

### Level 1: Essential (Always Run)
- Linting
- Type checking

### Level 2: Standard (Pre-Push)
- Essential +
- Unit tests
- Security audit

### Level 3: Comprehensive (Pre-Deploy)
- Standard +
- Integration tests
- E2E tests
- Build verification
- Performance tests

## Error Recovery

### Auto-Fix Capability
- **Lint errors**: Run `eslint --fix` or `biome check --apply`
- **Format errors**: Run `prettier --write` 
- **Security vulnerabilities**: Run `npm audit fix`

### Manual Fix Required
- Type errors
- Test failures
- Build errors

### Bypass (Use with Caution)
```bash
# Skip hooks for emergency fixes only
git commit --no-verify -m "emergency: fix critical bug"
```

## Best Practices

1. **Fail Fast**: Stop at first critical failure to save time
2. **Clear Feedback**: Always show which gate failed and why
3. **Actionable**: Provide exact commands to fix issues
4. **Configurable**: Respect project's quality thresholds
5. **Performance**: Cache results when possible
6. **Incremental**: Only check changed files when appropriate

## Configuration

### Read from package.json
```json
{
  "qualityGates": {
    "coverage": {
      "minimum": 80,
      "enabled": true
    },
    "audit": {
      "level": "moderate",
      "enabled": true
    },
    "complexity": {
      "maxLines": 500,
      "maxDepth": 5
    }
  }
}
```

### Default Settings
If no config found, use sensible defaults:
- Coverage minimum: 70%
- Audit level: high/critical only
- Max file lines: 500
- Max nesting: 5 levels

## Integration with Other Skills

- `codebase-analysis` - Use to detect available quality tools
- `git-workflow` - Integrate with commit/push process
- `ci-cd-setup` - Configure gates for CI pipeline

## Version History

- **1.0.0** (2025-01-03): Initial skill with 7 quality gates and progressive execution
