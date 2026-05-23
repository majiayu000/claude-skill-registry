---
name: javascript-eslint-linter
description: Ensure JavaScript/TypeScript code follows industry standards using ESLint linter with linting-workflow framework
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: code-quality
---

## What I do

I implement JavaScript/TypeScript-specific ESLint linting by extending the `linting-workflow` framework:

1. **Detect JavaScript/TypeScript Environment**: Identify JavaScript or TypeScript project (npm, yarn, pnpm)
2. **Detect ESLint Linter**: Check if ESLint is installed and configured
3. **Delegate to Linting Workflow**: Use `linting-workflow` for core linting functionality
4. **Provide JavaScript-Specific Guidance**: Help interpret ESLint error codes (no-unused-vars, semi, eqeqeq, etc.)
5. **Ensure JavaScript Best Practices**: Guide on JavaScript/TypeScript style standards and conventions

## When to use me

Use this workflow when:
- Writing or modifying JavaScript/TypeScript code that needs to follow industry standards
- Before committing JavaScript/TypeScript changes to ensure code quality
- When you see ESLint linting errors and need help fixing them
- Setting up a new JavaScript/TypeScript project with proper linting configuration
- You want to ensure code quality in automated workflows

**Framework**: This skill extends `linting-workflow` for generic linting, adding JavaScript/TypeScript-specific ESLint guidance.

## Steps

### Step 1: Detect JavaScript/TypeScript Environment

Verify this is a JavaScript/TypeScript project:
```bash
# Check for JavaScript/TypeScript files
ls *.js *.jsx *.ts *.tsx 2>/dev/null

# Check for JavaScript/TypeScript project files
[ -f package.json ] && [ -f package-lock.json ]
```

### Step 2: Detect ESLint Configuration

Check for ESLint in project:
```bash
# Check package.json for ESLint
grep -q "eslint" package.json

# Check for ESLint config files
[ -f .eslintrc.json ] || [ -f .eslintrc.js ] || [ -f .eslintrc.yaml ] || [ -f eslint.config.js ] || [ -f eslint.config.ts ] || [ -f eslint.config.mjs ]
```

### Step 3: Detect TypeScript

Check if this is a TypeScript project:
```bash
# Check for TypeScript files
if [ -f tsconfig.json ]; then
  PROJECT_TYPE="typescript"
else
  PROJECT_TYPE="javascript"
fi

echo "Project type: $PROJECT_TYPE"
```

### Step 4: Detect Package Manager

Check for package manager:
```bash
# Check for package manager
if [ -f package-lock.json ]; then
  PKG_MANAGER="npm"
  LINT_CMD="npm run lint"
  LINT_FIX_CMD="npm run lint -- --fix"
elif [ -f yarn.lock ]; then
  PKG_MANAGER="yarn"
  LINT_CMD="yarn lint"
  LINT_FIX_CMD="yarn lint --fix"
elif [ -f pnpm-lock.yaml ]; then
  PKG_MANAGER="pnpm"
  LINT_CMD="pnpm run lint"
  LINT_FIX_CMD="pnpm run lint --fix"
fi

echo "Package manager: $PKG_MANAGER"
```

### Step 5: Delegate to Linting Workflow

Use `linting-workflow` framework for:
- Language detection (JavaScript/TypeScript)
- Linter detection (ESLint)
- Package manager detection (npm/yarn/pnpm)
- Running linting with appropriate commands
- Auto-fix application
- Error resolution guidance
- Verification and re-running

### Step 6: JavaScript-Specific ESLint Error Guidance

**Common ESLint Error Codes:**

| Error Code | Description | Common Fix |
|------------|-------------|-------------|
| no-unused-vars | Variables/imports defined but not used | Remove or use variable/import |
| semi | Missing semicolons | Add semicolons to statements |
| eqeqeq | Use == instead of === | Change == to === |
| no-console | Console statements found | Remove console.log/console.error |
| prefer-const | Variable could be const | Change let to const |
| no-undef | Undefined variable used | Define variable or import |
| quotes | Inconsistent quote style | Use consistent quotes (' or ") |
| indent | Incorrect indentation | Fix indentation level |
| no-trailing-spaces | Trailing whitespace | Remove trailing spaces |
| comma-dangle | Trailing comma in object/array | Remove trailing comma |
| no-extra-semi | Extra semicolon | Remove extra semicolon |

**Error Resolution Template:**
```
For each ESLint error found:

1. **File**: <file>
   Line: <line>
   Column: <column>
   Error: <error message>
   Code: <no-unused-vars | semi | eqeqeq | etc.>

2. **ESLint Rule Explanation**:
   <Description of what ESLint is checking>

3. **Recommended Fix**:
   <Step-by-step fix instructions>

4. **Example**:
   ```javascript
   // Before (incorrect)
   <code>

   // After (corrected)
   <code>
   ```

5. **Apply Fix**:
   <Action to take>
```

## Best Practices

**Refer to `linting-workflow` for general linting best practices.**

JavaScript/TypeScript-specific best practices:
- **ESLint Configuration**: Use ESLint with appropriate plugins for your project
- **TypeScript**: Use `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` for TypeScript projects
- **Prettier Integration**: Use eslint-config-prettier for formatting
- **Airbnb Style Guide**: Follow Airbnb JavaScript/TypeScript Style Guide (common industry standard)
- **React Rules**: Use eslint-plugin-react and eslint-plugin-react-hooks for React projects
- **Import Order**: Use eslint-plugin-import for consistent import ordering
- **Accessibility**: Use eslint-plugin-jsx-a11y for React accessibility
- **No Var**: Prefer const/let over var
- **Arrow Functions**: Use arrow functions where appropriate
- **Template Literals**: Use template literals instead of string concatenation
- **Destructuring**: Use destructuring for object/array access
- **ESLint Config**: Configure ESLint in package.json or separate config file

## Common ESLint Issues

### ESLint Not Detected

**Issue**: ESLint is not installed or not found in package.json

**Solution**: Install ESLint:
```bash
# With npm
npm install --save-dev eslint

# With yarn
yarn add --dev eslint

# With pnpm
pnpm add -D eslint
```

### TypeScript ESLint Configuration

**Issue**: ESLint not configured for TypeScript

**Solution**: Install TypeScript ESLint packages:
```bash
# Install TypeScript ESLint packages
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Configure in .eslintrc.json
cat > .eslintrc.json <<EOF
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "plugins": ["@typescript-eslint"],
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"]
}
EOF
```

### React ESLint Configuration

**Issue**: ESLint not configured for React

**Solution**: Install React ESLint packages:
```bash
# Install React ESLint packages
npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y

# Configure in .eslintrc.json
cat > .eslintrc.json <<EOF
{
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "plugins": ["react", "react-hooks", "jsx-a11y"],
  "rules": {
    "react/prop-types": "off",
    "react/react-in-jsx-scope": "off"
  }
}
EOF
```

### Prettier Integration

**Issue**: Formatting conflicts between ESLint and Prettier

**Solution**: Install eslint-config-prettier:
```bash
# Install Prettier integration packages
npm install --save-dev eslint-config-prettier eslint-plugin-prettier

# Configure in .eslintrc.json
cat > .eslintrc.json <<EOF
{
  "extends": ["prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error",
    "prettier/prettier": "off"
  }
}
EOF
```

## Troubleshooting Checklist

Before linting:
- [ ] JavaScript/TypeScript project is identified
- [ ] ESLint is installed
- [ ] ESLint configuration file exists
- [ ] Package manager is detected (npm/yarn/pnpm)
- [ ] TypeScript is detected (if applicable)

After linting:
- [ ] Linting completed successfully
- [ ] Auto-fix applied (if errors found)
- [ ] Errors are categorized and displayed
- [ ] User receives JavaScript/TypeScript-specific guidance
- [ ] Linting is re-run after fixes

## Related Commands

```bash
# npm + ESLint
npm run lint
npm run lint -- --fix
npm install --save-dev eslint

# yarn + ESLint
yarn lint
yarn lint --fix
yarn add --dev eslint

# pnpm + ESLint
pnpm run lint
pnpm run lint --fix
pnpm add -D eslint

# Direct ESLint
npx eslint .
npx eslint . --fix

# ESLint checks
npx eslint --select E,F,W .
npx eslint --fix --select E,F,W .

# TypeScript ESLint
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin

# React ESLint
npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y

# Prettier integration
npm install --save-dev eslint-config-prettier eslint-plugin-prettier
```

## Related Skills

- `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper component architecture
- `linting-workflow`: Core linting framework
- `nextjs-unit-test-creator`: JavaScript/TypeScript test generation
- `nextjs-pr-workflow`: Next.js PR workflow with linting
- `typescript-dry-principle`: TypeScript code refactoring
