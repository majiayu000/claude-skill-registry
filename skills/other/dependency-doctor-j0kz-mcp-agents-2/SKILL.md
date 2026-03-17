---
name: dependency-doctor
description: Diagnose and heal dependency issues in ANY package manager, ANY language. Use when facing version conflicts, security vulnerabilities, or dependency bloat.
---

# Dependency Doctor - Heal Your Package Problems

## 🎯 When to Use This Skill

Use when experiencing:

- Security vulnerabilities in dependencies
- Version conflicts ("dependency hell")
- Broken builds after updates
- Slow install times
- Large node_modules/vendor folders
- "Works on my machine" issues
- License compliance concerns

## ⚡ Quick Health Check (30 seconds)

### Universal Diagnosis Commands:

```bash
# JavaScript/Node.js
npm audit
npm outdated
npm ls --depth=0

# Python
pip check
pip list --outdated
safety check

# Java
mvn dependency:tree
mvn versions:display-dependency-updates

# Go
go mod tidy
go list -m -u all

# Ruby
bundle audit
bundle outdated

# .NET
dotnet list package --vulnerable
dotnet list package --outdated

# Rust
cargo audit
cargo outdated
```

## 🔍 Common Dependency Diseases & Cures

### 1. Security Vulnerabilities 🚨

#### WITH MCP (Security Scanner):

```
"Scan my dependencies for security vulnerabilities"
"Fix all high-severity security issues"
```

#### WITHOUT MCP:

**Diagnosis:**

```bash
# JavaScript
npm audit --json | jq '.metadata.vulnerabilities'

# Python
pip install safety
safety check --json

# Ruby
gem install bundler-audit
bundle audit check
```

**Treatment:**

```bash
# Auto-fix (JavaScript)
npm audit fix

# Force fixes (use carefully!)
npm audit fix --force

# Manual fix for specific package
npm install package-name@latest

# Python manual update
pip install --upgrade package-name
```

**Prevention:**

```json
// package.json - Add security check to CI
{
  "scripts": {
    "security": "npm audit --audit-level=moderate",
    "preinstall": "npm audit"
  }
}
```

### 2. Version Conflicts (Dependency Hell) 🔥

**Symptoms:**

- "Cannot resolve dependency tree"
- "Peer dependency not satisfied"
- Different versions required by different packages

**Diagnosis:**

```bash
# Find conflicts
npm ls package-name

# See why a package is installed
npm explain package-name

# Python conflicts
pip check
pipdeptree -p package-name
```

**Treatment:**

```bash
# JavaScript - Resolution strategies

# 1. Clean install
rm -rf node_modules package-lock.json
npm install

# 2. Force resolutions (package.json)
{
  "overrides": {
    "package-name": "1.2.3"
  }
}

# 3. Use npm-force-resolutions
npm install --save-dev npm-force-resolutions

# Python - Use virtual environments
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 3. Bloated Dependencies 🎈

**Diagnosis - Find the Culprits:**

```bash
# JavaScript - Analyze bundle size
npm install -g npm-check
npm-check

# Or use disk usage
du -sh node_modules/* | sort -hr | head -20

# Analyze what's using space
npx webpack-bundle-analyzer stats.json
```

**Treatment - Diet Plan:**

```javascript
// 1. Find lighter alternatives
const HEAVY_TO_LIGHT = {
  moment: 'dayjs', // 67kb → 2kb
  lodash: 'lodash-es', // Tree-shakeable
  request: 'node-fetch', // 300kb → 25kb
  bluebird: 'native', // Use native promises
  jquery: 'vanilla', // No dependency
};

// 2. Import only what you need
// BAD
import _ from 'lodash';

// GOOD
import debounce from 'lodash/debounce';

// 3. Lazy load heavy dependencies
const heavyLib = () => import('heavy-library');
```

**Bundle Size Budget:**

```json
// package.json
{
  "bundlesize": [
    {
      "path": "./dist/app.js",
      "maxSize": "100 kB"
    }
  ]
}
```

### 4. Outdated Dependencies 📅

**Safe Update Strategy:**

```bash
# 1. Check what needs updating
npm outdated

# 2. Update in order of safety
# Patch versions (1.0.x) - Usually safe
npm update

# Minor versions (1.x.0) - Check changelog
npm install package@^1

# Major versions (x.0.0) - Read migration guide
npm install package@latest

# 3. Test after each update
npm test
```

**Automated Updates with Checks:**

```yaml
# GitHub Dependabot config
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: 'npm'
    directory: '/'
    schedule:
      interval: 'weekly'
    open-pull-requests-limit: 10
    groups:
      minor-and-patch:
        patterns:
          - '*'
        update-types:
          - 'minor'
          - 'patch'
```

### 5. Ghost Dependencies 👻

**Find Unused Dependencies:**

```bash
# JavaScript
npx depcheck

# Python
pip install pip-autoremove
pip-autoremove -l

# Result shows unused packages
```

**Clean Up:**

```bash
# Remove unused
npm uninstall package-name

# Or use depcheck to auto-remove
npx depcheck --json | jq '.dependencies[]' | xargs npm uninstall
```

## 📊 Dependency Management Best Practices

### 1. Lock Files Are Sacred

```bash
# ALWAYS commit lock files
git add package-lock.json  # npm
git add yarn.lock          # yarn
git add pnpm-lock.yaml     # pnpm
git add Pipfile.lock       # Python pipenv
git add go.sum             # Go

# Reproduce exact environment
npm ci  # Instead of npm install
```

### 2. Dependency Hygiene Routine

```javascript
// Weekly routine
const weeklyMaintenance = async () => {
  // 1. Security check
  await exec('npm audit');

  // 2. Remove unused
  await exec('npx depcheck');

  // 3. Update patch versions
  await exec('npm update');

  // 4. Check for major updates
  await exec('npm outdated');

  // 5. Clean cache
  await exec('npm cache clean --force');

  // 6. Deduplicate
  await exec('npm dedupe');
};
```

### 3. Version Range Strategies

```json
{
  "dependencies": {
    // Exact version (safest, least flexible)
    "critical-lib": "1.2.3",

    // Patch updates only (recommended for prod)
    "stable-lib": "~1.2.3", // 1.2.x

    // Minor updates (good for dev)
    "modern-lib": "^1.2.3", // 1.x.x

    // Latest (danger zone!)
    "experimental": "*"
  }
}
```

## 🚨 Emergency Procedures

### Broken After Update:

```bash
# 1. Rollback immediately
git checkout package-lock.json
npm ci

# 2. Find breaking change
npm ls package-name
git diff package-lock.json

# 3. Pin to working version
npm install package-name@1.2.3 --save-exact

# 4. File issue and wait for fix
```

### Cannot Install Dependencies:

```bash
# Nuclear option - clean everything
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install

# Still broken? Check Node version
node --version
nvm use 18  # Use LTS version

# Registry issues?
npm config set registry https://registry.npmjs.org/
```

### Production Emergency:

```dockerfile
# Reproducible builds in Docker
FROM node:18-alpine
WORKDIR /app

# Copy lock file FIRST
COPY package*.json ./

# Use ci for exact versions
RUN npm ci --only=production

# Then copy code
COPY . .

CMD ["node", "app.js"]
```

## 📈 Dependency Metrics

### Track Your Health:

```javascript
// dependency-health.js
const getMetrics = async () => {
  const metrics = {
    total: Object.keys(require('./package.json').dependencies).length,
    outdated: await getOutdatedCount(),
    vulnerable: await getVulnerabilityCount(),
    unused: await getUnusedCount(),
    duplicates: await getDuplicateCount(),
    size: await getTotalSize(),
  };

  // Calculate health score
  metrics.health = calculateHealth(metrics);

  return metrics;
};

function calculateHealth(metrics) {
  let score = 100;

  score -= metrics.vulnerable * 10; // -10 per vulnerability
  score -= metrics.outdated * 2; // -2 per outdated
  score -= metrics.unused * 3; // -3 per unused
  score -= metrics.duplicates; // -1 per duplicate

  if (metrics.total > 100) score -= 10; // Too many deps
  if (metrics.size > 100_000_000) score -= 10; // Too large

  return Math.max(0, score);
}
```

## 🛡️ Dependency Security Policy

```markdown
# Security Policy

## Automated Checks

- CI runs `npm audit` on every PR
- Dependabot creates PRs for security updates
- Weekly security report via GitHub Actions

## Severity Levels

- **Critical**: Fix immediately, hotfix to production
- **High**: Fix within 24 hours
- **Moderate**: Fix within 1 week
- **Low**: Fix in next release

## Approved Sources

✅ npm official registry
✅ GitHub packages (our org)
❌ Random GitHub repos
❌ Unverified registries

## License Requirements

✅ MIT, Apache 2.0, BSD
⚠️ GPL (check with legal)
❌ Proprietary, AGPL
```

## 💊 Preventive Medicine

### Dependency Budget:

```javascript
// dependency-budget.js
const BUDGET = {
  maxDependencies: 50,
  maxSize: 50_000_000, // 50MB
  maxDepth: 3,
  allowedLicenses: ['MIT', 'Apache-2.0', 'BSD'],
  bannedPackages: ['left-pad', 'is-odd'],
};

// Pre-install check
function checkBudget(packageName) {
  const metrics = getCurrentMetrics();

  if (metrics.count >= BUDGET.maxDependencies) {
    throw new Error('Dependency budget exceeded');
  }

  if (isBanned(packageName)) {
    throw new Error(`Package ${packageName} is banned`);
  }

  // Check before adding
  return true;
}
```

### Dependency Documentation:

```markdown
## Why This Dependency?

### Package: stripe

**Purpose**: Payment processing
**Alternatives considered**: PayPal SDK, Square
**Why chosen**: Best API, good docs
**Can we remove?**: No, core feature
**Owner**: Payment team

### Package: lodash

**Purpose**: Utility functions
**Alternatives considered**: Ramda, native
**Why chosen**: Team familiarity
**Can we remove?**: Yes, migrate to lodash-es
**Owner**: Frontend team
```

## 🎯 Quick Reference Card

```bash
# Daily health check
alias dephealth='npm audit && npm outdated && npx depcheck'

# Emergency fix
alias depfix='rm -rf node_modules package-lock.json && npm cache clean --force && npm install'

# Update safely
alias depsafe='npm update && npm test && npm audit'

# Full maintenance
alias depmaint='npm audit fix && npm dedupe && npm prune && npx depcheck'
```

Remember: Dependencies are like medicine - necessary but can have side effects. Use wisely! 💊
