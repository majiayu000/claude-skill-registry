---
name: setup-node
description: Sets up Node.js/TypeScript development environment with npm/yarn, dependencies, ESLint, Prettier, testing (Jest/Vitest), and TypeScript type checking. Ensures consistent tooling configuration. Use when starting work on Node.js/TypeScript projects, after cloning repositories, setting up CI/CD, or troubleshooting environment issues.
version: 1.0.0
---

# Node.js Development Setup Skill

## Purpose

Quickly set up and verify a Node.js/TypeScript development environment with all necessary tooling.

## Workflow

### Quick Setup Checklist

1. ✅ Verify Node.js 18+ and npm 9+
2. ✅ Detect package manager (npm/yarn/pnpm)
3. ✅ Install dependencies
4. ✅ Verify package.json scripts
5. ✅ Setup ESLint
6. ✅ Setup Prettier
7. ✅ Setup TypeScript (if applicable)
8. ✅ Setup Testing (Jest/Vitest)
9. ✅ Setup Git hooks (Husky + lint-staged)
10. ✅ Verify build
11. ✅ Run quality checks
12. ✅ Test execution

**For detailed step-by-step instructions with commands and troubleshooting, see `references/DETAILED-WORKFLOW.md`.**

## Common Node.js Commands Reference

### Package Management

```bash
npm install <package>         # Install package
npm install -D <package>      # Install as dev dependency
npm install -g <package>      # Install globally
npm uninstall <package>       # Remove package
npm update                    # Update all packages
npm outdated                  # Check for outdated packages
npm audit                     # Security audit
npm audit fix                 # Auto-fix vulnerabilities
```

### Project Commands

```bash
npm run dev                   # Development server
npm run build                 # Production build
npm test                      # Run tests
npm run lint                  # Lint code
npm run format                # Format code
```

### Yarn Equivalents

```bash
yarn add <package>            # Install package
yarn add -D <package>         # Install as dev dependency
yarn remove <package>         # Remove package
yarn upgrade                  # Update all packages
yarn audit                    # Security audit
```

---

## Troubleshooting

### Issue: "npm: command not found"

**Solution**: Node.js not installed

```bash
# macOS
brew install node

# Or use nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

### Issue: "Cannot find module 'X'"

**Solution**: Dependencies not installed

```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: "EACCES: permission denied"

**Solution**: Global npm permissions issue

```bash
# Fix npm permissions (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

### Issue: "TypeScript errors in node_modules"

**Solution**: Skip library checking

```json
// tsconfig.json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

### Issue: "ESLint and Prettier conflicts"

**Solution**: Install eslint-config-prettier

```bash
npm install --save-dev eslint-config-prettier
```

Add to .eslintrc.js:

```javascript
extends: [
  // ... other configs
  'prettier', // Must be last
],
```

---

## Best Practices

1. **Use Node version manager (nvm)** - Easily switch Node versions
2. **Lock dependency versions** - Commit package-lock.json
3. **Separate dev dependencies** - Use --save-dev for tooling
4. **Enable TypeScript strict mode** - Catch more errors
5. **Configure ESLint + Prettier** - Consistent code style
6. **Use git hooks** - Automate checks with Husky
7. **Target 90%+ coverage** - Comprehensive testing
8. **Regular security audits** - Run `npm audit` frequently

---

## Integration with Other Skills

This skill may be invoked by:

- **`quality-check`** - When checking Node.js code quality
- **`run-tests`** - When running Node.js tests
