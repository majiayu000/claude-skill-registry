---
name: node-package-management
description: Reference guide for npm, pnpm, yarn, and bun package managers. Covers workspace configuration, security audits, troubleshooting, and migration between package managers. Use for complex monorepo setup, debugging package issues, or deep package manager reference.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash
metadata:
  author: Saturate
  version: "1.0"
---

# Node.js Package Management

Manage Node.js dependencies using the appropriate package manager CLI. This skill detects which package manager is in use and provides the correct commands.

## Golden Rule

**Always use the package manager CLI to manage dependencies. Never manually edit `package.json` or lock files.**

Why CLI commands are required:
- **Validation**: Checks package exists on registry before adding
- **Dependency resolution**: Correctly handles transitive dependencies
- **Lock file integrity**: Maintains proper checksums and dependency trees
- **Deduplication**: Automatically optimizes dependency structure
- **Security**: Updates lock files with security metadata

Manual editing bypasses these protections and causes broken installs, security gaps, and version conflicts.

## Detect Package Manager

**Check for lock files in this order:**

```bash
# Detection script
if [ -f "bun.lockb" ]; then
    echo "bun"
elif [ -f "pnpm-lock.yaml" ]; then
    echo "pnpm"
elif [ -f "yarn.lock" ]; then
    echo "yarn"
elif [ -f "package-lock.json" ]; then
    echo "npm"
else
    echo "none (default to npm)"
fi
```

**Also check for configuration files:**
- `.npmrc` → npm configuration
- `pnpm-workspace.yaml` → pnpm workspaces
- `yarn.lock` + `.yarnrc.yml` → Yarn 2+ (Berry)
- `bunfig.toml` → Bun configuration

**Version managers:**
- `.nvmrc` → Node version for nvm
- `.node-version` → Node version for fnm/asdf
- `engines` field in package.json → Required Node version

## Quick Command Reference

| Task | npm | pnpm | yarn | bun |
|------|-----|------|------|-----|
| Install all | `npm install` | `pnpm install` | `yarn install` | `bun install` |
| Add package | `npm install <pkg>` | `pnpm add <pkg>` | `yarn add <pkg>` | `bun add <pkg>` |
| Add dev | `npm install -D <pkg>` | `pnpm add -D <pkg>` | `yarn add -D <pkg>` | `bun add -d <pkg>` |
| Remove | `npm uninstall <pkg>` | `pnpm remove <pkg>` | `yarn remove <pkg>` | `bun remove <pkg>` |
| Update | `npm update <pkg>` | `pnpm update <pkg>` | `yarn upgrade <pkg>` | `bun update <pkg>` |
| Audit | `npm audit` | `pnpm audit` | `yarn audit` | `npm audit` |
| Clean install | `npm ci` | `pnpm install --frozen-lockfile` | `yarn install --frozen-lockfile` | `bun install --frozen-lockfile` |

**For detailed commands and options, see:**
- **npm**: [references/npm.md](references/npm.md)
- **pnpm**: [references/pnpm.md](references/pnpm.md)
- **yarn**: [references/yarn.md](references/yarn.md)
- **bun**: [references/bun.md](references/bun.md)

## Workspaces

For monorepo setups, each package manager has workspace support:

- **npm workspaces**: [references/workspaces.md#npm-workspaces](references/workspaces.md#npm-workspaces)
- **pnpm workspaces**: [references/workspaces.md#pnpm-workspaces](references/workspaces.md#pnpm-workspaces)
- **yarn workspaces**: [references/workspaces.md#yarn-workspaces](references/workspaces.md#yarn-workspaces)

Complete workspace guide: [references/workspaces.md](references/workspaces.md)

## Security

**Check for vulnerabilities:**
```bash
# Use the appropriate command for your package manager
npm audit
pnpm audit
yarn audit
```

**Fix vulnerabilities:**
```bash
npm audit fix
pnpm update <package> --latest
yarn upgrade-interactive
```

**CI/CD integration:**
```bash
# Fail CI if high/critical vulnerabilities found
npm audit --audit-level=high
pnpm audit --audit-level=high
```

For detailed security practices: [references/security.md](references/security.md)

## Version Management

**Semantic versioning in package.json:**
- `"1.2.3"` → Exact version (most strict)
- `"^1.2.3"` → Compatible (1.x.x, allows minor/patch)
- `"~1.2.3"` → Patch only (1.2.x)
- `"*"` → Latest (❌ dangerous, avoid)

**Check outdated packages:**
```bash
npm outdated
pnpm outdated
yarn outdated
```

**Lock exact versions:**
```bash
npm install --save-exact <package>
pnpm add --save-exact <package>
yarn add --exact <package>
```

For update strategies and version ranges: [references/security.md#version-management](references/security.md#version-management)

## Common Issues

**"Cannot find module" after install:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Peer dependency conflicts:**
```bash
# npm - use legacy resolver
npm install --legacy-peer-deps

# pnpm - see which package needs which peer
pnpm why <package>
```

**Lock file corruption:**
```bash
# Delete and regenerate
rm package-lock.json  # or pnpm-lock.yaml, yarn.lock, bun.lockb
npm install           # or pnpm/yarn/bun install
```

For complete troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

## Anti-Patterns to Avoid

### ❌ Manual Editing

**Never:**
- Edit `package.json` dependencies by hand
- Edit lock files directly
- Copy-paste lock files between projects

**Why it breaks:**
- Checksums become invalid
- Dependency resolution fails
- Transitive dependencies missing

### ❌ Mixing Package Managers

**Never mix in same project:**
- Pick one: npm, pnpm, yarn, or bun
- Add only one lock file to git
- Detect mixing: `ls -la *.lock* 2>/dev/null | wc -l` (should be 1)

### ❌ Using `sudo` with npm

```bash
# ❌ Bad - corrupts permissions
sudo npm install -g typescript

# ✓ Good - use nvm or fnm
nvm install 20
npm install -g typescript
```

### ❌ Committing node_modules

**Never commit to git:**
```bash
# Add to .gitignore
node_modules/
```

Lock files provide reproducibility without committing 100s of MB.

### ❌ Wildcard Versions

```json
// ❌ Bad - unpredictable builds
{ "dependencies": { "lodash": "*" } }

// ✓ Good - explicit version
{ "dependencies": { "lodash": "4.17.21" } }
```

For all anti-patterns: See package manager guides and [references/troubleshooting.md](references/troubleshooting.md)

## Migration Between Managers

**npm → pnpm:**
```bash
npm install -g pnpm
pnpm import  # imports from package-lock.json
```

**npm → yarn:**
```bash
npm install -g yarn
yarn install  # reads package.json
rm package-lock.json
```

**yarn → pnpm:**
```bash
npm install -g pnpm
rm yarn.lock
pnpm install
```

For detailed migration steps: [references/troubleshooting.md#migration](references/troubleshooting.md#migration)

## References

Package manager guides:
- [npm Commands](references/npm.md) - npm-specific commands, flags, and features
- [pnpm Commands](references/pnpm.md) - pnpm-specific commands, efficiency features
- [yarn Commands](references/yarn.md) - Yarn 1.x and Yarn 2+ (Berry) commands
- [bun Commands](references/bun.md) - Bun-specific commands and features

Advanced topics:
- [Workspaces](references/workspaces.md) - Monorepo management with workspaces
- [Security](references/security.md) - Vulnerability scanning, lock files, version management
- [Troubleshooting](references/troubleshooting.md) - Common issues, debugging, migrations

External documentation:
- [npm documentation](https://docs.npmjs.com/)
- [pnpm documentation](https://pnpm.io/)
- [Yarn documentation](https://yarnpkg.com/)
- [Bun documentation](https://bun.sh/docs)
