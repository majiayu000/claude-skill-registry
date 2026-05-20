---
name: supply-chain-security
description: Typosquatting detection, install script analysis, dependency confusion prevention, and phantom dependency detection for npm/pip.
---

# Supply Chain Security

Patterns for auditing third-party dependencies before they own your production environment.

## Typosquatting Detection

Common substitution patterns attackers use against popular packages:

```python
# Levenshtein distance check against known-good package list
def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        return levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]

POPULAR_PACKAGES = ['express', 'lodash', 'react', 'axios', 'moment', 'chalk']

def is_typosquat(pkg: str, threshold: int = 2) -> list[str]:
    return [p for p in POPULAR_PACKAGES if 0 < levenshtein(pkg, p) <= threshold]

# Examples of known typosquats
typosquats = {
    'lodahs': 'lodash',       # character swap
    'expres': 'express',      # missing char
    'reakt': 'react',         # phonetic substitution
    'axois': 'axios',         # transposition
    'momnet': 'moment',       # transposition
}
```

Common substitution patterns to check manually:
- Character transposition: `lodash` → `lodahs`
- Missing character: `express` → `expres`
- Extra character: `chalk` → `cchalk`
- Hyphen/underscore swap: `my-lib` → `my_lib`
- Homoglyph: `rn` instead of `m` in package name

## Install Script Audit

```bash
# List all packages with install scripts (npm)
npm query ":root > *" | \
  node -e "const d=require('/dev/stdin');
    Object.entries(d.dependencies||{}).forEach(([k,v])=>{
      const pkg = require(\`./node_modules/\${k}/package.json\`);
      if(pkg.scripts?.preinstall||pkg.scripts?.postinstall||pkg.scripts?.install)
        console.log(k, Object.keys(pkg.scripts))
    })"

# Safer: use npm pack --dry-run to see what a package would install
npm pack lodash --dry-run

# Check a specific package's install scripts before installing
npm show <package> scripts
```

```typescript
// Automated install script audit
import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'

function auditInstallScripts(nodeModulesDir: string): void {
  const packages = fs.readdirSync(nodeModulesDir)

  for (const pkg of packages) {
    const pkgJsonPath = path.join(nodeModulesDir, pkg, 'package.json')
    if (!fs.existsSync(pkgJsonPath)) continue

    const pkgJson = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf-8'))
    const scripts = pkgJson.scripts ?? {}
    const suspicious = ['preinstall', 'postinstall', 'install']
      .filter(s => s in scripts)

    if (suspicious.length > 0) {
      console.warn(`[WARN] ${pkg} has install scripts: ${suspicious.join(', ')}`)
      console.warn(`       ${scripts[suspicious[0]]}`)
    }
  }
}

auditInstallScripts('./node_modules')
```

## Dependency Confusion Risk Assessment

```bash
# Check if your internal package names exist on the public registry
# If they do AND the public version is newer, npm may pull the public one

INTERNAL_PACKAGES=("@mycompany/auth" "@mycompany/utils" "internal-logger")

for pkg in "${INTERNAL_PACKAGES[@]}"; do
  result=$(npm show "$pkg" version 2>/dev/null)
  if [ -n "$result" ]; then
    echo "RISK: $pkg exists on public registry at version $result"
  else
    echo "OK:   $pkg not on public registry"
  fi
done
```

Prevention in `.npmrc`:

```ini
# Force scoped packages to your private registry
@mycompany:registry=https://npm.mycompany.com
@internal:registry=https://npm.mycompany.com

# Block public fallback for scoped packages
//npm.mycompany.com/:always-auth=true
```

## Phantom Dependency Detection

```bash
# Find imports/requires that aren't in package.json
# Node.js (using depcheck)
npx depcheck --ignores="@types/*" .

# Python (using pipreqs)
pip install pipreqs
pipreqs . --print | sort > required.txt
pip freeze | sort > installed.txt
diff required.txt installed.txt
```

```typescript
// Custom phantom dep detector for TypeScript
import { execSync } from 'child_process'
import fs from 'fs'

function detectPhantomDeps(srcDir: string): void {
  const pkgJson = JSON.parse(fs.readFileSync('package.json', 'utf-8'))
  const declared = new Set([
    ...Object.keys(pkgJson.dependencies ?? {}),
    ...Object.keys(pkgJson.devDependencies ?? {}),
  ])

  // Extract all import/require statements
  const imports = execSync(
    `rg --no-heading -oh "from ['\"]([^./][^'\"]+)['\"]" ${srcDir} | sed "s/from ['\"]//;s/['\"]//;s/\\/.*//"`
  ).toString().split('\n').filter(Boolean)

  const unique = new Set(imports)
  for (const imp of unique) {
    const root = imp.startsWith('@') ? imp.split('/').slice(0, 2).join('/') : imp.split('/')[0]
    if (!declared.has(root)) {
      console.warn(`[PHANTOM] "${root}" is imported but not in package.json`)
    }
  }
}
```

## Lock File Integrity Verification

```bash
# Verify package-lock.json integrity (npm)
npm ci --dry-run

# Detect if lock file is out of sync with package.json
npm install --package-lock-only
git diff --exit-code package-lock.json

# pip: verify requirements are pinned with hashes
pip install --require-hashes -r requirements.txt

# Generate hash-pinned requirements
pip-compile --generate-hashes requirements.in -o requirements.txt
```

## npm audit / pip-audit Integration

```bash
# npm - break build on high severity
npm audit --audit-level=high

# pip-audit
pip install pip-audit
pip-audit --requirement requirements.txt --fail-on CRITICAL,HIGH

# GitHub Actions integration
- name: Security audit
  run: |
    npm audit --audit-level=moderate
    npx better-npm-audit audit --level moderate
```

## SBOM Generation

```bash
# CycloneDX for Node.js
npm install -g @cyclonedx/cyclonedx-npm
cyclonedx-npm --output-format JSON --output-file sbom.json

# CycloneDX for Python
pip install cyclonedx-bom
cyclonedx-bom -r -o sbom.xml

# SPDX via syft
syft . -o spdx-json > sbom.spdx.json
```

## Known Malicious Package Indicators

Red flags when reviewing a new dependency:

```
- Install scripts that curl | bash external URLs
- Package published < 48 hours ago with thousands of weekly downloads
- Zero issues/stars on GitHub but high download count
- package.json "main" points to an obfuscated file
- Dependencies on packages with random hex names
- Author email is a free provider with a new account
- Version bump from 1.x to 99.x (dependency confusion attack)
```

## Dependency Pinning Strategy

```json
// package.json: exact pinning for production deps
{
  "dependencies": {
    "express": "4.18.2",      // exact - no caret/tilde
    "lodash": "4.17.21"
  },
  "devDependencies": {
    "typescript": "^5.3.0"   // range OK for dev tools
  }
}
```

```bash
# Convert all ranges to exact versions
npm shrinkwrap
# or use: npm-shrinkwrap.json over package-lock.json for published packages

# Renovate bot for automated safe updates with PR-per-dep
# renovate.json
{
  "extends": ["config:base"],
  "automerge": false,
  "reviewers": ["security-team"]
}
```

**Rule**: Never `npm install <unknown-package>` in production without running `npm audit`, checking install scripts, and verifying the package name against known typosquats.
