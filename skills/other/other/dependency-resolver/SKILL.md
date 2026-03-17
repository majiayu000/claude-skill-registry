---
name: dependency-resolver
description: Identify, analyze, and manage software dependencies before deployment. Use this skill when preparing applications for deployment, resolving dependency conflicts, updating dependencies, auditing security vulnerabilities, managing package versions, or troubleshooting dependency-related issues. Supports multiple package managers (npm, pip, maven, cargo, go mod, composer) and provides actionable recommendations for dependency management.
---

# Dependency Resolver

Analyze, manage, and resolve software dependencies to ensure safe and successful deployments. Identifies conflicts, security vulnerabilities, version mismatches, and missing dependencies.

## Core Capabilities

### 1. Dependency Analysis

Examine project dependencies:
- **Direct dependencies** - Packages explicitly required
- **Transitive dependencies** - Dependencies of dependencies
- **Dev dependencies** - Development-only packages
- **Peer dependencies** - Required by packages but not auto-installed
- **Optional dependencies** - Non-critical packages

### 2. Conflict Detection

Identify dependency issues:
- **Version conflicts** - Multiple versions of same package
- **Missing dependencies** - Required but not installed
- **Incompatible versions** - Version constraints that can't be satisfied
- **Circular dependencies** - Packages depending on each other
- **Platform incompatibility** - OS or architecture mismatches

### 3. Security Auditing

Check for vulnerabilities:
- **Known CVEs** - Common Vulnerabilities and Exposures
- **Outdated packages** - Old versions with security patches available
- **Malicious packages** - Typosquatting or compromised packages
- **License issues** - Incompatible or restrictive licenses

### 4. Dependency Resolution

Provide solutions:
- **Version pinning** - Lock compatible versions
- **Conflict resolution** - Strategies to resolve version conflicts
- **Dependency updates** - Safe upgrade paths
- **Alternative packages** - Replacement suggestions
- **Minimal installations** - Remove unnecessary dependencies

## Dependency Resolution Workflow

### Step 1: Identify Package Manager

Detect which dependency system is in use:

**Package manager files:**
```
npm/yarn:     package.json, package-lock.json, yarn.lock
pip:          requirements.txt, Pipfile, setup.py, pyproject.toml
maven:        pom.xml
gradle:       build.gradle, build.gradle.kts
cargo:        Cargo.toml, Cargo.lock
go:           go.mod, go.sum
composer:     composer.json, composer.lock
bundler:      Gemfile, Gemfile.lock
nuget:        *.csproj, packages.config
```

### Step 2: Parse Dependency Manifest

Read and understand dependency declarations:

**npm (package.json):**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "~4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "peerDependencies": {
    "react": ">=16.0.0"
  }
}
```

**Python (requirements.txt):**
```
django>=4.0,<5.0
requests==2.28.1
numpy>=1.20.0
pytest  # No version specified
```

**Maven (pom.xml):**
```xml
<dependencies>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>5.3.23</version>
  </dependency>
</dependencies>
```

### Step 3: Analyze Dependency Tree

Build complete dependency graph:

```
my-app
├── express@4.18.2
│   ├── body-parser@1.20.1
│   │   └── bytes@3.1.2
│   ├── cookie@0.5.0
│   └── debug@2.6.9
│       └── ms@2.0.0
└── lodash@4.17.21
```

**Check for:**
- Multiple versions of same package
- Deeply nested dependencies
- Large dependency trees
- Unmaintained packages

### Step 4: Detect Issues

Identify problems:

**Version conflicts:**
```
app requires:
  - package-a@1.0.0 (depends on shared@^1.0.0)
  - package-b@2.0.0 (depends on shared@^2.0.0)

Conflict: shared@1.x vs shared@2.x
```

**Missing dependencies:**
```
Error: Cannot find module 'missing-package'
Cause: Listed in package.json but not installed
```

**Security vulnerabilities:**
```
lodash@4.17.20 has known vulnerability CVE-2020-8203
Severity: High
Fix available: Upgrade to lodash@4.17.21
```

### Step 5: Propose Solutions

Recommend fixes:

**For version conflicts:**
- Use compatible versions
- Update conflicting packages
- Use resolutions/overrides
- Consider alternatives

**For missing dependencies:**
- Install missing packages
- Add to manifest file
- Check for typos

**For security issues:**
- Update vulnerable packages
- Apply security patches
- Replace with secure alternatives

## Dependency Management Patterns

### Pattern 1: Version Conflict Resolution

**Issue:**
```json
// package.json
{
  "dependencies": {
    "package-a": "^1.0.0",  // requires lodash@^3.0.0
    "package-b": "^2.0.0"   // requires lodash@^4.0.0
  }
}
```

**Analysis:**
```
Dependency tree:
├── package-a@1.0.0
│   └── lodash@3.10.1
└── package-b@2.0.0
    └── lodash@4.17.21

Conflict: Two versions of lodash (3.10.1 and 4.17.21)
```

**Solution 1: Update package-a**
```json
{
  "dependencies": {
    "package-a": "^2.0.0",  // Updated version uses lodash@^4.0.0
    "package-b": "^2.0.0"
  }
}
```

**Solution 2: Use resolutions (npm/yarn)**
```json
{
  "dependencies": {
    "package-a": "^1.0.0",
    "package-b": "^2.0.0"
  },
  "resolutions": {
    "lodash": "^4.17.21"
  }
}
```

**Solution 3: Find alternative**
```json
{
  "dependencies": {
    "alternative-package-a": "^1.0.0",  // Doesn't depend on lodash
    "package-b": "^2.0.0"
  }
}
```

### Pattern 2: Security Vulnerability Fix

**Audit result:**
```bash
$ npm audit

found 3 vulnerabilities (1 moderate, 2 high)

High: Prototype Pollution
Package: lodash
Dependency of: express
Path: express > lodash
More info: https://npmjs.com/advisories/1065
```

**Solution:**
```bash
# Check if update fixes it
npm audit fix

# Force update if needed
npm audit fix --force

# Or manually update
npm install lodash@latest
```

**Verify fix:**
```bash
npm audit
# 0 vulnerabilities
```

### Pattern 3: Missing Peer Dependency

**Error:**
```
npm WARN package-b@1.0.0 requires a peer of react@>=16.0.0 but none is installed.
```

**Analysis:**
```json
// package-b requires react but doesn't install it
{
  "peerDependencies": {
    "react": ">=16.0.0"
  }
}
```

**Solution:**
```bash
npm install react@^18.0.0
```

**Update package.json:**
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "package-b": "^1.0.0"
  }
}
```

### Pattern 4: Outdated Dependencies

**Check for updates:**
```bash
npm outdated

Package    Current  Wanted  Latest  Location
express    4.17.1   4.18.2  4.18.2  my-app
lodash     4.17.20  4.17.21 4.17.21 my-app
react      17.0.2   17.0.2  18.2.0  my-app
```

**Analysis:**
- **Current**: Installed version
- **Wanted**: Max version satisfying semver
- **Latest**: Newest version available

**Solution strategy:**
```bash
# Safe: Update to wanted versions
npm update

# Major updates (breaking changes)
npm install react@latest  # Review changelog first

# Pin specific version
npm install express@4.18.2 --save-exact
```

### Pattern 5: Circular Dependencies

**Detection:**
```
Circular dependency detected:
  package-a → package-b → package-c → package-a
```

**Analysis:**
```javascript
// package-a/index.js
const b = require('./package-b');

// package-b/index.js
const c = require('./package-c');

// package-c/index.js
const a = require('./package-a');  // Circular!
```

**Solution:**
```javascript
// Restructure to break cycle
// 1. Extract shared code to new package
// 2. Use dependency injection
// 3. Lazy loading

// Option 1: Extract shared functionality
// package-shared/index.js
module.exports = { sharedFunction };

// package-a/index.js
const shared = require('./package-shared');

// package-c/index.js
const shared = require('./package-shared');
```

### Pattern 6: Platform-Specific Dependencies

**Issue:**
```json
{
  "dependencies": {
    "fsevents": "^2.3.2"  // macOS only
  }
}
```

**Error on Linux:**
```
npm ERR! notsup Unsupported platform for fsevents@2.3.2
```

**Solution:**
```json
{
  "dependencies": {
    "chokidar": "^3.5.3"  // Cross-platform alternative
  },
  "optionalDependencies": {
    "fsevents": "^2.3.2"  // macOS optimization
  }
}
```

### Pattern 7: Dependency Bloat

**Analysis:**
```bash
# Check installed package sizes
npm ls --all --depth=0
du -sh node_modules/

# Result: 500MB for small app!
```

**Identify large packages:**
```bash
npx cost-of-modules

┌────────────────────────┬───────────┬────────────┐
│ name                   │ size      │ dependencies│
├────────────────────────┼───────────┼────────────┤
│ @babel/core            │ 45 MB     │ 234        │
│ webpack                │ 38 MB     │ 189        │
│ lodash                 │ 1.5 MB    │ 0          │
└────────────────────────┴───────────┴────────────┘
```

**Solutions:**
```json
// Use lighter alternatives
{
  "dependencies": {
    "lodash.debounce": "^4.0.8",  // Instead of full lodash
    "date-fns": "^2.29.3"         // Instead of moment.js
  }
}

// Remove unused dependencies
// Use: npm prune
// Or: yarn autoclean
```

## Version Constraint Syntax

### npm/JavaScript (Semver)

```
^1.2.3   - Compatible with 1.2.3 (>=1.2.3 <2.0.0)
~1.2.3   - Approximately 1.2.3 (>=1.2.3 <1.3.0)
1.2.x    - 1.2.0, 1.2.1, etc. (>=1.2.0 <1.3.0)
*        - Any version
latest   - Latest version
1.2.3    - Exact version
>=1.2.3  - Greater than or equal
<2.0.0   - Less than
1.2.3 - 2.3.4  - Range
```

### Python (PEP 440)

```
==1.2.3      - Exact version
>=1.2.3      - Minimum version
>=1.2,<2.0   - Range
~=1.2.3      - Compatible release (>=1.2.3, ==1.2.*)
!=1.2.3      - Exclude version
package      - Any version
```

### Maven/Java

```xml
<version>1.2.3</version>           <!-- Exact -->
<version>[1.2.3]</version>         <!-- Exact (hard) -->
<version>[1.0,2.0)</version>       <!-- Range: 1.0 <= x < 2.0 -->
<version>[1.0,)</version>          <!-- Minimum 1.0 -->
<version>(,2.0)</version>          <!-- Maximum < 2.0 -->
```

### Cargo/Rust

```toml
[dependencies]
package = "1.2.3"        # Exact: =1.2.3
package = "^1.2.3"       # Caret: >=1.2.3, <2.0.0
package = "~1.2.3"       # Tilde: >=1.2.3, <1.3.0
package = ">= 1.2.3"     # Inequality
package = "*"            # Any version
```

## Dependency Commands Reference

### npm/yarn

```bash
# Install dependencies
npm install
yarn install

# Add dependency
npm install package-name
yarn add package-name

# Add dev dependency
npm install --save-dev package-name
yarn add --dev package-name

# Update dependencies
npm update
yarn upgrade

# Check for outdated
npm outdated
yarn outdated

# Security audit
npm audit
yarn audit

# Fix vulnerabilities
npm audit fix
yarn audit fix

# List dependencies
npm ls
yarn list

# Remove unused
npm prune
yarn autoclean

# Lock file
npm ci  # Clean install from lock file
yarn install --frozen-lockfile
```

### Python (pip)

```bash
# Install dependencies
pip install -r requirements.txt

# Install package
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Upgrade package
pip install --upgrade package-name

# List installed
pip list

# Show outdated
pip list --outdated

# Security check
pip-audit  # Requires pip-audit package

# Freeze dependencies
pip freeze > requirements.txt

# Uninstall
pip uninstall package-name
```

### Maven

```bash
# Install dependencies
mvn install

# Update dependencies
mvn versions:update-properties

# Dependency tree
mvn dependency:tree

# Analyze dependencies
mvn dependency:analyze

# Check for updates
mvn versions:display-dependency-updates

# Security check (with OWASP plugin)
mvn dependency-check:check
```

### Go

```bash
# Install dependencies
go mod download

# Add dependency
go get package-name

# Update dependencies
go get -u ./...

# Tidy dependencies
go mod tidy

# Verify dependencies
go mod verify

# List dependencies
go list -m all

# Dependency graph
go mod graph

# Security check
go list -json -m all | nancy sleuth
```

## Pre-Deployment Checklist

### 1. Dependency Installation

```bash
# Verify all dependencies install successfully
npm ci  # or equivalent for your package manager

# Check for installation errors
echo $?  # Should be 0
```

### 2. Security Audit

```bash
# Run security audit
npm audit

# Check for high/critical vulnerabilities
# Fix if found
npm audit fix
```

### 3. License Compliance

```bash
# Check licenses
npx license-checker --summary

# Verify no GPL or incompatible licenses
npx license-checker --excludeLicenses "GPL,AGPL"
```

### 4. Dependency Tree Analysis

```bash
# Check for duplicate packages
npm dedupe

# Verify no circular dependencies
npm ls

# Check tree depth
npm ls --depth=5
```

### 5. Platform Compatibility

```bash
# Test on target platform
# Verify OS-specific dependencies work
# Check architecture compatibility (x64, arm64)
```

### 6. Lock File Consistency

```bash
# Ensure lock file is committed
git ls-files package-lock.json

# Verify lock file is up to date
npm ci
```

### 7. Size Check

```bash
# Check total size
du -sh node_modules/

# Identify large packages
npx cost-of-modules

# Remove dev dependencies for production
npm prune --production
```

## Common Issues and Solutions

### Issue 1: "Cannot find module"

**Error:**
```
Error: Cannot find module 'express'
```

**Causes:**
- Dependency not installed
- Not listed in package.json
- Wrong import path

**Solutions:**
```bash
# Install missing package
npm install express

# Add to package.json
npm install express --save

# Reinstall all dependencies
rm -rf node_modules
npm install
```

### Issue 2: Version Conflict

**Error:**
```
npm ERR! peer dep missing: react@>=16.0.0
```

**Solution:**
```bash
# Check peer dependencies
npm info package-name peerDependencies

# Install required peer dependency
npm install react@^16.0.0
```

### Issue 3: Lock File Out of Sync

**Error:**
```
npm ERR! package-lock.json lockfileVersion mismatch
```

**Solution:**
```bash
# Delete and regenerate
rm package-lock.json
npm install

# Or use correct npm version
nvm use 16
npm install
```

### Issue 4: Network/Registry Errors

**Error:**
```
npm ERR! network timeout
```

**Solution:**
```bash
# Increase timeout
npm config set timeout 60000

# Try different registry
npm config set registry https://registry.npmjs.org/

# Clear cache
npm cache clean --force
```

### Issue 5: Post-Install Script Failures

**Error:**
```
npm ERR! postinstall script failed
```

**Solution:**
```bash
# Check node/npm version
node --version
npm --version

# Update build tools
npm install -g node-gyp

# Install system dependencies (example for Ubuntu)
sudo apt-get install build-essential python3
```

## Best Practices

1. **Use lock files** - Commit package-lock.json, yarn.lock, Cargo.lock
2. **Pin major versions** - Avoid wildcards in production
3. **Regular updates** - Keep dependencies current, not cutting-edge
4. **Security audits** - Run before every deployment
5. **Minimal dependencies** - Only include what you need
6. **Review licenses** - Ensure compatibility with your project
7. **Test after updates** - Run full test suite
8. **Document decisions** - Note why specific versions are used
9. **Use semantic versioning** - Understand version implications
10. **Monitor size** - Keep bundle size reasonable

## Ecosystem-Specific Guides

For detailed ecosystem-specific information:

- **JavaScript/Node.js**: See [references/npm_yarn.md](references/npm_yarn.md)
- **Python**: See [references/python_deps.md](references/python_deps.md)
- **Java**: See [references/maven_gradle.md](references/maven_gradle.md)
- **Rust**: See [references/cargo.md](references/cargo.md)
- **Go**: See [references/go_modules.md](references/go_modules.md)
