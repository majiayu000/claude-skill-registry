---
name: upgrade-packages-js
description: Safely upgrade JavaScript packages with breaking change detection, migration guidance, and automated code migrations (npm/pnpm/yarn). Cross-platform with git safety branch enforcement.
version: 2.5.0
author: Palakorn V. <palakorn@me.com>
tags: [npm, pnpm, yarn, upgrade, dependencies, semver, migration, codemod, monorepo]
triggers: [upgrade packages, update dependencies, check outdated, dependency upgrade]
---

# Skill: Package Upgrade (Cross-Platform)

Safely upgrade JavaScript packages while minimizing breaking change risk, with migration guidance and automated code upgrades.

---

## Non-Negotiables

1. **Verify JavaScript project first** - Stop immediately if not a JS/Node.js project
2. **Never force upgrade all at once** - Upgrade incrementally
3. **Detect package manager first** - npm/pnpm/yarn (including version)
4. **Never mix package managers** - Refuse if lockfiles conflict
5. **Git safety gate first** - Clean repo + new branch before upgrades
6. **Breaking-change evidence check** - For majors, check Releases/CHANGELOG/Migration/Codemods
7. **For breaking upgrades: migrate code + tests** - Apply codemods, implement fixes, add tests
8. **Check peer dependencies** - Ensure compatibility before upgrading
9. **Check Node.js engine compatibility** - Verify target versions support project's Node
10. **Check ESM/CJS compatibility** - Verify module system compatibility
11. **Test after each major upgrade** - Run build and tests
12. **Keep lockfile updated** - Commit lockfile changes
13. **Document skipped packages** - Record why packages were not upgraded
14. **Time-box upgrades** - Max time per major; if stuck, defer and document

---

## Project Language Detection (MANDATORY - RUN FIRST)

**This skill is for JavaScript/TypeScript (Node.js) projects only.** Run this check before anything else.

```bash
node -e "
const fs=require('fs'),p=require('path'),cwd=process.cwd();
const checks=[
  ['package.json','javascript/typescript','This skill supports this project type'],
  ['go.mod','go','Use: go get -u ./... or go-mod-upgrade'],
  ['Cargo.toml','rust','Use: cargo update or cargo-upgrades'],
  ['requirements.txt','python','Use: pip-review --auto or pip-upgrader'],
  ['pyproject.toml','python','Use: poetry update or pdm update'],
  ['Pipfile','python','Use: pipenv update'],
  ['composer.json','php','Use: composer update'],
  ['Gemfile','ruby','Use: bundle update'],
  ['pubspec.yaml','dart','Use: dart pub upgrade'],
  ['pom.xml','java','Use: mvn versions:use-latest-releases'],
  ['build.gradle','java','Use: gradle dependencyUpdates'],
  ['*.csproj','dotnet','Use: dotnet outdated or nukeeper'],
  ['Package.swift','swift','Use: swift package update'],
  ['mix.exs','elixir','Use: mix deps.update --all'],
];
const found=checks.filter(([f])=>f.includes('*')?require('fs').readdirSync(cwd).some(x=>x.endsWith(f.slice(1))):fs.existsSync(p.join(cwd,f)));
if(found.length===0){console.error('ERROR: No recognized project files found');process.exit(1)}
const js=found.find(([_,l])=>l==='javascript/typescript');
if(js){console.log('OK: JavaScript/TypeScript project detected (package.json found)');process.exit(0)}
const other=found[0];
console.error('ERROR: This skill is for JavaScript/TypeScript (Node.js) projects only.');
console.error('Detected: '+other[0]+' ('+other[1]+' project)');
console.error('Suggestion: '+other[2]);
process.exit(2);
"
```

### Supported vs Unsupported Projects

| File | Language | Supported | Alternative Command |
|------|----------|:---------:|---------------------|
| `package.json` | JavaScript/TypeScript | ✅ Yes | This skill |
| `go.mod` | Go | ❌ No | `go get -u ./...` |
| `Cargo.toml` | Rust | ❌ No | `cargo update` |
| `requirements.txt` | Python | ❌ No | `pip-review --auto` |
| `pyproject.toml` | Python (Poetry/PDM) | ❌ No | `poetry update` / `pdm update` |
| `composer.json` | PHP | ❌ No | `composer update` |
| `Gemfile` | Ruby | ❌ No | `bundle update` |
| `pom.xml` | Java (Maven) | ❌ No | `mvn versions:use-latest-releases` |
| `build.gradle` | Java (Gradle) | ❌ No | `gradle dependencyUpdates` |
| `pubspec.yaml` | Dart/Flutter | ❌ No | `dart pub upgrade` |
| `*.csproj` | .NET | ❌ No | `dotnet outdated` |
| `Package.swift` | Swift | ❌ No | `swift package update` |
| `mix.exs` | Elixir | ❌ No | `mix deps.update --all` |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | JavaScript/TypeScript project - proceed with skill |
| 1 | No recognized project files found |
| 2 | Non-JavaScript/TypeScript project detected - use alternative |

**IMPORTANT:** If exit code is not 0, STOP and inform the user. Do not proceed with the rest of this skill.

---

## PM Command Reference

Use `{PM}` = detected package manager. Use `{PMX}` = `npx` | `pnpm dlx` | `yarn dlx`.

| Purpose | npm | pnpm | yarn v1 | yarn Berry |
|---------|-----|------|---------|------------|
| Install | `npm install` | `pnpm install` | `yarn` | `yarn` |
| Add pkg | `npm install {pkg}` | `pnpm add {pkg}` | `yarn add {pkg}` | `yarn add {pkg}` |
| Add dev | `npm install -D {pkg}` | `pnpm add -D {pkg}` | `yarn add -D {pkg}` | `yarn add -D {pkg}` |
| Outdated | `npm outdated` | `pnpm outdated` | `yarn outdated` | `yarn upgrade-interactive` |
| Why installed | `npm explain {pkg}` | `pnpm why {pkg}` | `yarn why {pkg}` | `yarn why {pkg}` |
| Audit | `npm audit` | `pnpm audit` | `yarn audit` | `yarn npm audit` |
| Run ncu | `npx npm-check-updates` | `pnpm dlx npm-check-updates` | `yarn dlx npm-check-updates` | `yarn dlx npm-check-updates` |
| Frozen install | `npm ci` | `pnpm install --frozen-lockfile` | `yarn --frozen-lockfile` | `yarn --immutable` |
| Workspaces | `npm -ws` | `pnpm -r` | `yarn workspaces` | `yarn workspaces foreach` |

---

## Git Safety Gate (MANDATORY)

```bash
# One-command gate: checks + creates branch
node -e "const {execSync}=require('child_process');const run=(c)=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString().trim();try{run('git --version')}catch(e){console.error('ERROR: git not installed');process.exit(10)}try{if(run('git rev-parse --is-inside-work-tree')!=='true')throw 0}catch(e){console.error('ERROR: not a git repo');process.exit(11)}try{if(run('git status --porcelain')){console.error('ERROR: working tree not clean');process.exit(12)}}catch(e){process.exit(13)}const d=new Date();const pad=n=>String(n).padStart(2,'0');const name='chore/upgrade-packages-'+d.getFullYear()+pad(d.getMonth()+1)+pad(d.getDate())+'-'+pad(d.getHours())+pad(d.getMinutes());try{run('git checkout -b '+name);console.log('OK: created branch '+name)}catch(e){process.exit(14)}"
```

**Rules:**
- Never run install/upgrade unless branch created
- Commit `package.json` + lockfile on this branch

---

## Package Manager Detection (MANDATORY)

```bash
node -e "const fs=require('fs'),p=require('path');const cwd=process.cwd();let pm='';try{pm=JSON.parse(fs.readFileSync(p.join(cwd,'package.json'),'utf8')).packageManager||''}catch{}const locks=[['pnpm','pnpm-lock.yaml'],['yarn','yarn.lock'],['npm','package-lock.json']].filter(([_,f])=>fs.existsSync(p.join(cwd,f)));if(pm){console.log(pm);process.exit(0);}if(locks.length===1){console.log(locks[0][0]);process.exit(0);}if(locks.length>1){console.error('ERROR: multiple lockfiles');process.exit(2);}console.error('ERROR: unable to detect PM');process.exit(1);"
```

**Priority:** `package.json.packageManager` > single lockfile > STOP

**Yarn v1 vs Berry:** Check `yarn --version` (1.x = Classic, 2+ = Berry)

---

## Pre-Upgrade Checks

### Monorepo Detection
```bash
node -e "const pkg=require('./package.json');console.log(pkg.workspaces?'MONOREPO: '+JSON.stringify(pkg.workspaces):'SINGLE_PACKAGE')"
```

### Lock File Integrity
```bash
# npm: npm ci --dry-run | pnpm: pnpm install --frozen-lockfile --dry-run | yarn: yarn --frozen-lockfile --check-files
```

### Node.js Compatibility
```bash
node -e "const pkg=require('./package.json');console.log('Engines:',pkg.engines?.node||'any','Current:',process.version)"
npm view {package}@latest engines
```

### ESM/CJS Compatibility
```bash
node -e "const pkg=require('./package.json');console.log('Type:',pkg.type||'commonjs')"
npm view {package} type exports
```

| Project | Package | Compatible | Notes |
|---------|---------|------------|-------|
| commonjs | module | Maybe | Need dynamic import() or bundler |
| module | commonjs | Yes | Node handles interop |

### Stale Package Detection
```bash
npm view {package} time.modified
```
Flag packages >2 years since last publish.

### License Check
```bash
npm view {package} license
npx license-checker --summary
```

---

## Dependency Analysis

```bash
# View tree
{PM} ls --depth=0

# Why installed
{PM} explain {pkg}  # npm
{PM} why {pkg}      # pnpm/yarn

# Peer deps
npm view {pkg} peerDependencies
```

---

## Dependency Overrides

| PM | Location | Example |
|----|----------|---------|
| npm | `overrides` | `"overrides": {"glob": "^10.0.0"}` |
| pnpm | `pnpm.overrides` | `"pnpm": {"overrides": {"glob": "^10.0.0"}}` |
| yarn | `resolutions` | `"resolutions": {"glob": "^10.0.0"}` |

---

## Breaking Change Evidence Check (MANDATORY FOR MAJOR)

### Step 1: Get metadata
```bash
npm view {pkg} repository homepage --json
```

### Step 2: Check sources
- GitHub Releases: `{repo}/releases`
- CHANGELOG: `{repo}/blob/main/CHANGELOG.md`
- Migration: `{repo}/blob/main/UPGRADING.md` or `MIGRATION.md`

### Step 3: Keywords to scan
`BREAKING`, `Removed`, `Renamed`, `Deprecated`, `Migration`, `Codemod`, `engines`, `peerDependencies`

### Step 4: Required output
```
Package: {name} | From: {current} To: {target}
Evidence: Releases: {link} | Changelog: {link} | Migration: {link} | Codemod: {cmd}
Breaking changes: {...}
Required actions: {...}
Peer constraints: {...}
Node.js requirement: {...}
```

**If no evidence found:** Proceed to Automatic Web Search (next section).

---

## Automatic Web Search for Migration Guides (MANDATORY IF NO DOCS FOUND)

When GitHub Releases, CHANGELOG, or MIGRATION docs are not found or insufficient, **automatically search the web** for migration guides before asking the user.

### Search Queries (Execute in Order)

For a package `{pkg}` upgrading from `{from}` to `{to}`:

1. **Official migration guide:**
   ```
   "{pkg}" migration guide {from} to {to}
   "{pkg}" upgrade guide v{majorFrom} to v{majorTo}
   ```

2. **Breaking changes:**
   ```
   "{pkg}" {to} breaking changes
   "{pkg}" v{majorTo} changelog breaking
   ```

3. **Codemods:**
   ```
   "{pkg}" codemod {majorTo}
   "{pkg}" migration codemod
   ```

4. **Community guides:**
   ```
   "{pkg}" upgrade tutorial {majorTo}
   "{pkg}" migration blog post
   ```

### Trusted Sources Priority

Prioritize results from these domains:
| Priority | Source | Examples |
|----------|--------|----------|
| 1 | Official docs | `{pkg}.dev`, `{pkg}.io`, `{pkg}js.org` |
| 2 | GitHub | `github.com/{org}/{pkg}` (releases, discussions, wiki) |
| 3 | Dev blogs | `dev.to`, `medium.com`, `hashnode.dev` |
| 4 | Stack Overflow | `stackoverflow.com` (tagged answers) |
| 5 | Package news | `npmjs.com`, `socket.dev` |

### Search Result Evaluation

Extract and verify:
- [ ] **Breaking changes list** - API removals, renames, behavior changes
- [ ] **Migration steps** - Ordered steps from the guide
- [ ] **Codemod availability** - Auto-fix tools (`npx {pkg}-codemod`, etc.)
- [ ] **Minimum requirements** - Node.js version, peer dependencies
- [ ] **Known issues** - Common problems and workarounds

### Decision After Web Search

| Search Result | Action |
|---------------|--------|
| Official migration guide found | Follow the guide, proceed with upgrade |
| Community guide found (verified) | Use as reference, proceed cautiously |
| Breaking changes documented | Apply changes, test thoroughly |
| Only partial info found | Combine sources, ask user to verify approach |
| No useful results | **Stop** - Ask user before proceeding |

### Example Web Search Flow

```
Package: recharts 2.x → 3.x
Step 1: Check GitHub releases → Found but sparse
Step 2: Search "recharts migration guide 2 to 3" → Found official guide
Step 3: Search "recharts 3 breaking changes" → Found API changes list
Step 4: Search "recharts codemod 3" → No codemod available
Result: Proceed with manual migration using official guide
```

### Web Search Output Template

```
Package: {pkg} | From: {from} To: {to}
Search performed: Yes
Sources found:
  - Official: {url} (migration guide)
  - GitHub: {url} (release notes)
  - Community: {url} (tutorial)
Breaking changes identified:
  - {change 1}
  - {change 2}
Migration steps:
  1. {step 1}
  2. {step 2}
Codemod: {available/not available}
Confidence: {high/medium/low}
Recommendation: {proceed/ask user/skip}
```

### If Web Search Fails

If no useful migration information is found after web search:

1. **Log the search attempt** - Document what was searched
2. **Present options to user:**
   - Proceed anyway (high risk, manual testing required)
   - Skip this package (add to Skipped Packages)
   - User provides migration link
3. **Never silently upgrade** - Always get explicit confirmation for undocumented majors

---

## Upgrade Workflow

### Order
1. Dev dependencies (lower risk)
2. Patch upgrades
3. Minor upgrades
4. Major upgrades (one at a time, with migrations)
5. Framework upgrades (Next/React) last

### For each major upgrade:
1. Locate migration docs
2. Check Node/ESM/license compatibility
3. Run codemods if available
4. Implement manual changes
5. Cleanup dead code (`npx ts-prune`, `eslint --fix`)
6. Add/update tests
7. Verify: `{PM} install && npx tsc --noEmit && npm run lint && npm test && npm run build`
8. Commit: `git commit -m "chore(deps): upgrade {pkg} {from}→{to}"`

### Time limits
| Type | Max | If exceeded |
|------|-----|-------------|
| Patch | 5min | Investigate |
| Minor | 15min | Check for hidden breaks |
| Major | 30min-1hr | Document, defer |

---

## Common Dependency Groups

| Group | Packages | Why |
|-------|----------|-----|
| React | `react`, `react-dom`, `@types/react*` | Must align |
| Next.js | `next`, `eslint-config-next` | Paired releases |
| Prisma | `prisma`, `@prisma/client` | Must match exactly |
| TypeScript | `typescript`, `@types/node` | Compatibility |
| Tailwind | `tailwindcss`, `postcss`, `autoprefixer` | Paired releases |

---

## Framework Upgrades

### Next.js
```bash
{PM_ADD} next@latest react@latest react-dom@latest
npx @next/codemod@latest {codemod-name}
```

### Prisma
```bash
{PM_ADD} prisma@latest @prisma/client@latest
npx prisma generate && npx prisma validate
```

### TypeScript
```bash
{PM_ADD} -D typescript@latest
npx tsc --noEmit
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Peer conflicts | `npm view {pkg} peerDependencies`, check tree |
| ESM errors | Use dynamic `import()` or add `"type": "module"` |
| Type errors | Update `@types/{pkg}@latest` |
| Cache issues | `rm -rf .next node_modules/.cache` |
| Deprecated pkg | `npm view {pkg} deprecated`, find alternative |

### Rollback
```bash
git checkout package.json {lockfile}
{PM} install
```

---

## Pre-commit Hook Bypass (upgrade commits only)

```bash
HUSKY=0 git commit -m "chore(deps): upgrade packages"
# or: git commit --no-verify -m "..."
```

---

## Private Registry

Check `.npmrc` before upgrading. Verify auth:
```bash
npm whoami --registry={registry-url}
```

---

## Skipped Packages Template

```markdown
| Package | Current | Latest | Reason | Revisit |
|---------|---------|--------|--------|---------|
| old-lib | 2.0.0 | 3.0.0 | Needs React 19 | After React upgrade |
```

---

## Upgrade Report Template

```markdown
# Package Upgrade Report
**Date:** {date} | **PM:** {npm|pnpm|yarn} | **Branch:** {branch}

## Summary
- Upgraded: {count} | Major: {count} | Minor: {count} | Patch: {count} | Skipped: {count}

## Upgrades
| Package | From | To | Breaking | Migration |
|---------|------|----|---------:|-----------|

## Breaking Changes
### {pkg} {from}→{to}
- Docs: {link}
- Codemods: {cmd}
- Manual changes: {...}
- Tests added: {...}

## Verification
- [ ] Type check | [ ] Lint | [ ] Tests | [ ] Build

## Skipped
| Package | Reason |

## Rollback
`git checkout main -- package.json {lockfile} && {PM} install`
```

---

## Automated PR Creation

```bash
git push -u origin $(git branch --show-current)
gh pr create --title "chore(deps): upgrade packages $(date +%Y-%m-%d)" --body "## Package Upgrade\nSee upgrade report for details."
```

---

## Semver Notes

- **Pre-1.0.0:** Treat minors as potential breaking changes
- **@types/*:** Often break in patches; pin exact or test carefully
- **Prereleases (alpha/beta/rc/canary):** Never in production deps, only devDependencies with explicit justification

---

## Decision Matrix

| Situation | Action |
|-----------|--------|
| No errors | Continue |
| Minor type errors | Fix and continue |
| Major API changes | Follow migration + codemods + tests |
| No docs found | **Web search first**, then ask user if nothing found |
| Tests fail | Fix or revert |
| Time exceeded | Document, defer, create issue |
| ESM/CJS incompatible | Check bundler or find alternative |
| Node incompatible | Defer or find alternative |

---

## Detecting Major Version Blockers

Before upgrading any major version, run these checks to detect potential blockers.

### Step 1: Check Your Project Module Type

```bash
node -e "const pkg=require('./package.json'); console.log('Project type:', pkg.type || 'commonjs')"
```

| Result | Meaning |
|--------|---------|
| `commonjs` | Default Node.js, may have issues with ESM-only packages |
| `module` | ESM project, compatible with all modern packages |

### Step 2: Check if Target Package is ESM-Only

```bash
# Check the target version's module type
npm view {package}@{version} type

# Returns "module" = ESM-only
# Returns nothing/undefined = CommonJS compatible
```

### Step 3: ESM/CJS Compatibility Decision

| Your Project | Package Type | Compatible? | Action |
|--------------|--------------|-------------|--------|
| `commonjs` | `module` (ESM-only) | ❌ No | Skip, find alternative, or migrate project to ESM |
| `commonjs` | (empty/commonjs) | ✅ Yes | Safe to upgrade |
| `module` | `module` (ESM-only) | ✅ Yes | Safe to upgrade |
| `module` | (empty/commonjs) | ✅ Yes | Safe to upgrade |

### Step 4: Check Node.js Engine Compatibility

```bash
# Check required Node.js version
npm view {package}@{version} engines

# Compare with your project's Node version
node --version
```

If package requires newer Node.js than your project supports, skip or upgrade Node.js first.

### Step 5: Check for Deprecation

```bash
# Check if package is deprecated
npm view {package} deprecated

# If deprecated, find alternative
npm search {alternative-keywords}
```

### Step 6: Check Peer Dependencies

```bash
# View peer dependency requirements
npm view {package}@{version} peerDependencies

# Ensure your installed versions satisfy requirements
```

### Quick Pre-Upgrade Script

Run this before any major upgrade:

```bash
# Replace {pkg} and {ver} with actual values
node -e "
const pkg='{pkg}', ver='{ver}';
const {execSync}=require('child_process');
const run=c=>{try{return execSync(c,{encoding:'utf8'}).trim()}catch{return''}};
const projType=require('./package.json').type||'commonjs';
const pkgType=run('npm view '+pkg+'@'+ver+' type');
const engines=run('npm view '+pkg+'@'+ver+' engines');
const deprecated=run('npm view '+pkg+' deprecated');
console.log('Package:', pkg+'@'+ver);
console.log('Project type:', projType);
console.log('Package type:', pkgType||'commonjs');
console.log('Engines:', engines||'any');
console.log('Deprecated:', deprecated||'no');
console.log('---');
if(projType==='commonjs'&&pkgType==='module'){
  console.log('⚠️  BLOCKER: ESM-only package in CommonJS project');
  console.log('Options: 1) Skip upgrade  2) Find alternative  3) Migrate project to ESM');
}else if(deprecated){
  console.log('⚠️  BLOCKER: Package is deprecated');
}else{
  console.log('✅ No blockers detected - verify build after upgrade');
}
"
```

### CommonJS Project with ESM-Only Package: Options

If you encounter an ESM-only package in a CommonJS project:

1. **Skip upgrade** - Stay on last CommonJS-compatible version
2. **Find alternative** - Search for CJS-compatible package with similar functionality
3. **Use dynamic import** - `const pkg = await import('{package}')` (async only)
4. **Use bundler** - Webpack/Vite can sometimes handle ESM in CJS projects
5. **Migrate to ESM** - Add `"type": "module"` to package.json (major change)
