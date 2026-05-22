---
name: typescript-quality-checker
description: Validate TypeScript/JavaScript code quality with ESLint, Prettier, type
  checking, and security analysis. Use for TypeScript/JS codebases to ensure code
  quality and standards.
allowed-tools: Read, Bash, Grep, Glob
---

# TypeScript Quality Checker Skill

## Purpose

This skill provides comprehensive TypeScript/JavaScript code quality validation including formatting (Prettier), linting (ESLint), type checking (tsc), security analysis (npm audit), and code complexity analysis. Ensures code meets TypeScript best practices and project standards.

## When to Use

- Validating TypeScript/JavaScript code quality before commit
- Running pre-commit quality checks
- CI/CD quality gate validation
- Code review preparation
- Ensuring code style compliance
- Type safety validation
- Security vulnerability detection in dependencies

## Quality Check Workflow

### 1. Environment Setup

**Verify Tools Installed:**
```bash
# Check Node.js and npm versions
node --version
npm --version

# Check TypeScript compiler
npx tsc --version

# Check quality tools
npx eslint --version
npx prettier --version
```

**Install Development Dependencies:**
```bash
# Install all dev dependencies
npm install --save-dev

# Or install quality tools specifically
npm install --save-dev \
  typescript \
  eslint \
  prettier \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  eslint-config-prettier \
  eslint-plugin-prettier
```

**Deliverable:** Quality tools ready

---

### 2. Code Formatting Check (Prettier)

**Check Formatting:**
```bash
# Check if code is formatted
npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Check specific files
npx prettier --check src/index.ts

# Check with detailed output
npx prettier --check --log-level debug "src/**/*.ts"
```

**Auto-Format Code:**
```bash
# Format all code
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Format specific directory
npx prettier --write "src/components/**/*.tsx"

# Check what would change (dry run)
npx prettier --check --list-different "src/**/*.ts"
```

**Configuration (.prettierrc.json):**
```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**.prettierignore:**
```
node_modules/
dist/
build/
coverage/
*.min.js
package-lock.json
```

**Deliverable:** Formatting validation report

---

### 3. Type Checking (TypeScript Compiler)

**Run Type Checks:**
```bash
# Check types
npx tsc --noEmit

# Check with specific config
npx tsc --noEmit --project tsconfig.json

# Check and show all errors
npx tsc --noEmit --pretty

# Incremental type checking
npx tsc --noEmit --incremental
```

**Watch Mode for Development:**
```bash
# Watch and type check continuously
npx tsc --noEmit --watch

# With specific project
npx tsc --noEmit --watch --project tsconfig.json
```

**Configuration (tsconfig.json):**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "build"]
}
```

**Deliverable:** Type checking report

---

### 4. Linting (ESLint)

**Run ESLint:**
```bash
# Lint entire codebase
npx eslint "src/**/*.{ts,tsx,js,jsx}"

# Lint with auto-fix
npx eslint "src/**/*.{ts,tsx,js,jsx}" --fix

# Lint with detailed output
npx eslint "src/**/*.{ts,tsx,js,jsx}" --format=stylish

# Generate HTML report
npx eslint "src/**/*.{ts,tsx,js,jsx}" --format=html --output-file=eslint-report.html
```

**Check Specific Rules:**
```bash
# Check for unused variables
npx eslint "src/**/*.ts" --rule '@typescript-eslint/no-unused-vars: error'

# Check complexity
npx eslint "src/**/*.ts" --rule 'complexity: ["error", 10]'

# Check max lines
npx eslint "src/**/*.ts" --rule 'max-lines: ["error", 500]'
```

**Configuration (.eslintrc.json):**
```json
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint", "prettier"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "rules": {
    "prettier/prettier": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": ["error", {
      "argsIgnorePattern": "^_"
    }],
    "complexity": ["error", 10],
    "max-lines": ["error", 500],
    "max-lines-per-function": ["error", 50],
    "no-console": ["warn", {
      "allow": ["warn", "error"]
    }]
  },
  "ignorePatterns": ["dist/", "build/", "node_modules/", "*.config.js"]
}
```

**Deliverable:** Linting report

---

### 5. Security Analysis

**npm Audit:**
```bash
# Check for vulnerabilities
npm audit

# Detailed audit
npm audit --json

# Production dependencies only
npm audit --production

# Fix vulnerabilities
npm audit fix

# Fix including breaking changes
npm audit fix --force
```

**Check for Outdated Packages:**
```bash
# List outdated packages
npm outdated

# Check specific package
npm outdated typescript

# Update packages
npm update
```

**Dependency License Check:**
```bash
# Install license checker
npm install --save-dev license-checker

# Check licenses
npx license-checker --summary

# Exclude specific licenses
npx license-checker --exclude "MIT,Apache-2.0"
```

**Deliverable:** Security analysis report

---

### 6. Code Complexity Analysis

**ESLint Complexity Rules:**
```bash
# Check cyclomatic complexity
npx eslint "src/**/*.ts" --rule 'complexity: ["error", 10]'

# Check max depth
npx eslint "src/**/*.ts" --rule 'max-depth: ["error", 4]'

# Check max nested callbacks
npx eslint "src/**/*.ts" --rule 'max-nested-callbacks: ["error", 3]'
```

**TypeScript-Specific Complexity:**
```bash
# Install complexity tool
npm install --save-dev ts-complex

# Analyze complexity
npx ts-complexity src/
```

**Deliverable:** Complexity analysis report

---

### 7. Import/Export Validation

**Check Unused Exports:**
```bash
# Install ts-prune
npm install --save-dev ts-prune

# Find unused exports
npx ts-prune

# Exclude specific files
npx ts-prune --ignore "index.ts"
```

**Check Import Order:**
```bash
# Install eslint-plugin-import
npm install --save-dev eslint-plugin-import

# Add to .eslintrc.json
{
  "plugins": ["import"],
  "rules": {
    "import/order": ["error", {
      "groups": [
        "builtin",
        "external",
        "internal",
        "parent",
        "sibling",
        "index"
      ],
      "newlines-between": "always"
    }]
  }
}
```

**Deliverable:** Import validation report

---

### 8. Comprehensive Quality Check

**Run All Checks:**
```bash
#!/bin/bash
# scripts/quality-check.sh

set -e  # Exit on first error

echo "=== TypeScript Quality Checks ==="

echo "1. Code Formatting (Prettier)..."
npx prettier --check "src/**/*.{ts,tsx,js,jsx}"

echo "2. Type Checking (tsc)..."
npx tsc --noEmit

echo "3. Linting (ESLint)..."
npx eslint "src/**/*.{ts,tsx}" --max-warnings=0

echo "4. Security Audit..."
npm audit --production

echo "5. Unused Exports..."
npx ts-prune || true  # Don't fail on unused exports

echo "=== All Quality Checks Passed ✅ ==="
```

**package.json Scripts:**
```json
{
  "scripts": {
    "lint": "eslint 'src/**/*.{ts,tsx}' --max-warnings=0",
    "lint:fix": "eslint 'src/**/*.{ts,tsx}' --fix",
    "format": "prettier --write 'src/**/*.{ts,tsx,json,css,md}'",
    "format:check": "prettier --check 'src/**/*.{ts,tsx,json,css,md}'",
    "type-check": "tsc --noEmit",
    "quality": "npm run format:check && npm run type-check && npm run lint",
    "test": "jest",
    "test:coverage": "jest --coverage"
  }
}
```

**Deliverable:** Comprehensive quality report

---

## Quality Standards

### Code Formatting
- [ ] All code formatted with Prettier
- [ ] Consistent use of semicolons
- [ ] Consistent quote style (single/double)
- [ ] Trailing commas in multiline
- [ ] Line length ≤ 100 characters

### Type Checking
- [ ] All functions have return types
- [ ] No implicit `any` types
- [ ] Strict null checks enabled
- [ ] No unused parameters
- [ ] No unused variables

### Linting
- [ ] No ESLint errors
- [ ] Max warnings: 0
- [ ] Complexity ≤ 10 per function
- [ ] Max lines ≤ 500 per file
- [ ] Imports properly ordered

### Security
- [ ] No critical vulnerabilities
- [ ] No high-severity vulnerabilities
- [ ] Dependencies up to date
- [ ] Licenses compliant
- [ ] No hardcoded secrets

### Code Quality
- [ ] Functions < 50 lines
- [ ] Files < 500 lines
- [ ] Max nesting depth: 4
- [ ] Cyclomatic complexity < 10
- [ ] No unused exports

---

## Quality Check Matrix

| Check | Tool | Threshold | Auto-Fix |
|-------|------|-----------|----------|
| Formatting | Prettier | Must pass | Yes |
| Type checking | tsc | 0 errors | No |
| Linting | ESLint | 0 errors | Partial |
| Security | npm audit | 0 critical | Partial |
| Complexity | ESLint | ≤ 10 | No |
| Unused exports | ts-prune | Warning only | No |

---

## Pre-commit Integration

**Setup Husky and lint-staged:**
```bash
# Install tools
npm install --save-dev husky lint-staged

# Initialize husky
npx husky-init && npm install

# Add pre-commit hook
npx husky add .husky/pre-commit "npx lint-staged"
```

**Configuration (package.json):**
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "prettier --write",
      "eslint --fix",
      "tsc-files --noEmit"
    ],
    "*.{json,css,md}": [
      "prettier --write"
    ]
  }
}
```

**Deliverable:** Pre-commit hooks configured

---

## CI/CD Integration

**GitHub Actions Example:**
```yaml
# .github/workflows/quality.yml
name: TypeScript Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Check formatting
        run: npm run format:check

      - name: Type checking
        run: npm run type-check

      - name: Linting
        run: npm run lint

      - name: Security audit
        run: npm audit --production --audit-level=high

      - name: Run tests
        run: npm test

      - name: Check coverage
        run: npm run test:coverage
```

**Deliverable:** CI/CD quality pipeline

---

## Quality Check Troubleshooting

### Prettier Formatting Failures

```bash
# Check what would change
npx prettier --check --list-different "src/**/*.ts"

# Apply fixes
npx prettier --write "src/**/*.ts"

# Check specific file
npx prettier --check src/index.ts
```

### TypeScript Type Errors

```bash
# Show detailed errors
npx tsc --noEmit --pretty

# Check specific file
npx tsc --noEmit src/component.tsx

# Skip lib check (faster)
npx tsc --noEmit --skipLibCheck
```

### ESLint Violations

```bash
# Show detailed violations
npx eslint "src/**/*.ts" --format=stylish

# Auto-fix safe violations
npx eslint "src/**/*.ts" --fix

# Ignore specific line (last resort)
// eslint-disable-next-line rule-name
```

### npm Audit Issues

```bash
# Show detailed audit
npm audit --json

# Fix non-breaking changes
npm audit fix

# Override (use with caution)
npm audit fix --force
```

---

## Quality Report Template

```markdown
# TypeScript Quality Check Report

## Summary
- **Status**: ✅ All checks passed
- **Date**: 2024-01-15
- **Code Base**: src/

## Checks Performed

### Formatting (Prettier)
- **Status**: ✅ PASS
- **Files Checked**: 87
- **Issues**: 0

### Type Checking (tsc)
- **Status**: ✅ PASS
- **Files Checked**: 87
- **Errors**: 0
- **Warnings**: 0

### Linting (ESLint)
- **Status**: ✅ PASS
- **Files Checked**: 87
- **Errors**: 0
- **Warnings**: 0

### Security (npm audit)
- **Status**: ✅ PASS
- **Dependencies**: 342
- **Vulnerabilities**: 0 critical, 0 high, 2 moderate

### Complexity
- **Status**: ✅ PASS
- **Average Complexity**: 3.8
- **Max Complexity**: 9
- **Files > 10**: 0

## Details

All TypeScript quality checks passed successfully. Code is well-formatted, type-safe, lint-free, secure, and maintainable.

## Recommendations

- Continue using strict TypeScript settings
- Keep complexity below 10
- Run pre-commit hooks before commits
- Update moderate-severity vulnerabilities when possible
```

---

## Integration with Code Quality Specialist

**Input:** TypeScript/JavaScript codebase quality check request
**Process:** Run all TypeScript quality tools and analyze results
**Output:** Comprehensive quality report with pass/fail status
**Next Step:** Report to code-quality-specialist for consolidation

---

## Best Practices

### Development
- Enable Prettier on save (IDE integration)
- Enable ESLint in IDE for real-time feedback
- Use strict TypeScript settings
- Fix type errors immediately
- Use pre-commit hooks

### Pre-Commit
- Run full quality check script
- Ensure all checks pass
- Fix issues before pushing
- Review security warnings

### CI/CD
- Run quality checks on every PR
- Fail build on quality violations
- Generate quality reports
- Track quality metrics over time

### Code Review
- Verify quality checks passed
- Review type definitions
- Check security scan results
- Validate complexity metrics

---

## Supporting Resources

- **TypeScript**: https://www.typescriptlang.org/docs
- **ESLint**: https://eslint.org/docs
- **Prettier**: https://prettier.io/docs
- **typescript-eslint**: https://typescript-eslint.io
- **npm audit**: https://docs.npmjs.com/cli/v8/commands/npm-audit

---

## Success Metrics

- [ ] All code formatted with Prettier
- [ ] All type checks passing
- [ ] Zero linting violations
- [ ] No critical security issues
- [ ] Complexity under threshold
- [ ] All quality checks automated