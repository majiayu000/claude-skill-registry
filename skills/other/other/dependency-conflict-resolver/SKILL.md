---
name: dependency-conflict-resolver
description: Detect and resolve package dependency conflicts before installation across npm/yarn/pnpm, pip/poetry, cargo, and composer. Auto-trigger when installing/upgrading packages. Validates peer dependencies, version compatibility, security vulnerabilities. Auto-resolves safe conflicts (patches, dev deps), suggests manual review for breaking changes. Prevents conflicting versions, security vulnerabilities, broken builds.
---

<objective>
Proactively detect and resolve dependency conflicts before package installation to prevent broken builds, security vulnerabilities, and version incompatibilities across JavaScript, Python, Rust, and PHP ecosystems.
</objective>

<quick_start>
<workflow>
**Pre-installation check workflow:**

1. **Detect package manager**: Identify ecosystem from lockfiles (package-lock.json, requirements.txt, Cargo.lock, composer.lock)
2. **Scan for conflicts**: Check peer dependencies, version ranges, transitive dependencies
3. **Security audit**: Run ecosystem-specific audit tools (npm audit, pip-audit, cargo-audit, composer audit)
4. **Analyze severity**: Classify conflicts by risk level (safe auto-fix, manual review, blocking)
5. **Present resolution**: Auto-apply safe fixes, suggest alternatives for breaking changes, block critical vulnerabilities with alternatives
</workflow>

<trigger_detection>
**Auto-invoke when detecting these commands:**
- `npm install`, `npm i`, `yarn add`, `pnpm add`
- `pip install`, `poetry add`
- `cargo add`, `cargo install`
- `composer require`, `composer install`
</trigger_detection>

<quick_example>
```bash
# User attempts: npm install react@18.0.0
# Skill detects: Peer dependency conflict with react-dom@17.0.0

[CONFLICT DETECTED]
Package: react@18.0.0
Conflict: react-dom@17.0.0 requires react ^17.0.0
Risk: MEDIUM (breaking change)

[RECOMMENDED ACTION]
Option 1: Upgrade react-dom to ^18.0.0 (recommended)
  npm install react@18.0.0 react-dom@18.0.0

Option 2: Downgrade react to ^17.0.0
  npm install react@17.0.0

[SECURITY CHECK]
✓ No known vulnerabilities in react@18.0.0
✓ No known vulnerabilities in react-dom@18.0.0
```
</quick_example>
</quick_start>

<workflow>
<detection_phase>
**1. Identify Package Manager and Context**

Scan current directory for lockfiles and package manifests:
- **JavaScript**: package.json + (package-lock.json | yarn.lock | pnpm-lock.yaml)
- **Python**: requirements.txt | Pipfile | pyproject.toml + (Pipfile.lock | poetry.lock)
- **Rust**: Cargo.toml + Cargo.lock
- **PHP**: composer.json + composer.lock

Extract:
- Current dependency versions (from lockfile)
- Requested package and version (from user command)
- Version constraints (from manifest)
</detection_phase>

<conflict_analysis>
**2. Analyze Dependency Conflicts**

Check for conflicts in order of severity:

**A. Peer Dependency Conflicts**
- Compare requested version against peer dependency requirements
- Identify which packages will be incompatible
- Calculate semver compatibility ranges

**B. Transitive Dependency Conflicts**
- Build dependency graph of all transitive dependencies
- Detect duplicate packages with incompatible versions
- Identify shared dependencies requiring specific versions

**C. Version Constraint Violations**
- Validate against existing version constraints in manifest
- Check for semver range compatibility (^, ~, >=, etc.)
- Detect locked versions that prevent resolution

**D. Platform/Runtime Conflicts**
- Check Node.js, Python, PHP version requirements
- Validate feature flags (Rust features)
- Check platform-specific dependencies
</conflict_analysis>

<security_audit>
**3. Security Vulnerability Scan**

Run ecosystem-specific security audits:

**JavaScript (npm/yarn/pnpm):**
```bash
npm audit --json
# Parse output for HIGH/CRITICAL vulnerabilities
# Check: GHSA IDs, CVE numbers, severity scores
```

**Python (pip/poetry):**
```bash
pip-audit --format json
# Or: poetry audit --json
# Parse PyPA Advisory Database results
```

**Rust (cargo):**
```bash
cargo audit --json
# Check RustSec Advisory Database
# Identify RUSTSEC-YYYY-NNNN advisories
```

**PHP (composer):**
```bash
composer audit --format json
# Parse security advisories
# Check for blocked insecure packages
```

For each vulnerability found:
- Extract severity (LOW, MODERATE, HIGH, CRITICAL)
- Identify patched versions
- Find alternative packages if no patch available
- Assess exploitability and context
</security_audit>

<resolution_strategy>
**4. Classify Conflicts and Generate Resolutions**

**Auto-resolve (apply without asking):**
- Patch version updates (1.2.3 → 1.2.4)
- Dev dependency conflicts with no production impact
- Security patches within same minor version
- Compatible semver range adjustments (^1.2.0 allows 1.2.4)

**Suggest manual review (present options):**
- Minor version updates (1.2.x → 1.3.x)
- Production dependency conflicts
- Peer dependency mismatches requiring upgrades
- Multiple resolution paths with tradeoffs

**Block with alternatives (prevent installation):**
- Major version conflicts requiring breaking changes
- Critical/High security vulnerabilities without patches
- Incompatible platform/runtime requirements
- Circular dependency deadlocks

**Resolution output format:**
```
[CONFLICT TYPE] Brief description
Package: package-name@requested-version
Current: package-name@current-version
Conflict: dependency-name requires version-constraint

[IMPACT ASSESSMENT]
Risk: LOW | MEDIUM | HIGH | CRITICAL
Scope: dev-only | production | peer-dependency | transitive

[RECOMMENDED ACTIONS]
1. [Primary recommendation with command]
2. [Alternative approach with tradeoffs]
3. [Fallback option if applicable]

[SECURITY STATUS]
✓ No vulnerabilities | ⚠ Vulnerabilities found (details below)
```
</resolution_strategy>

<execution_phase>
**5. Execute Resolution**

**For auto-resolvable conflicts:**
1. Generate updated install command with resolved versions
2. Execute installation with resolved dependencies
3. Verify lockfile updates
4. Log changes for review

**For manual review conflicts:**
1. Present options with AskUserQuestion tool
2. Explain tradeoffs for each option
3. Execute user-selected resolution
4. Confirm successful installation

**For blocking conflicts:**
1. Prevent installation
2. Display detailed error explanation
3. Suggest alternative packages or version ranges
4. Provide documentation links for further investigation
</execution_phase>
</workflow>

<ecosystem_specific_patterns>
**JavaScript (npm/yarn/pnpm)**

Common conflict patterns:
- React version mismatches between react and react-dom
- Peer dependency warnings for plugin ecosystems (Babel, ESLint, Webpack)
- Duplicate packages at different major versions in monorepos

Resolution tools:
- `npm ls <package>` - Show dependency tree for package
- `npm why <package>` - Explain why package is installed
- `npm audit fix` - Auto-fix vulnerabilities
- `npm overrides` (package.json) - Force specific versions globally

See [references/javascript-patterns.md](references/javascript-patterns.md) for detailed examples.

**Python (pip/poetry)**

Common conflict patterns:
- Platform-specific wheels causing resolution failures
- Conflicting constraints from multiple requirements files
- Python version incompatibilities (3.8 vs 3.9+ features)

Resolution tools:
- `pip check` - Verify installed packages have compatible dependencies
- `pip install --dry-run` - Simulate installation without applying
- `poetry show --tree` - Display dependency tree
- `poetry update --dry-run` - Preview updates without applying

See [references/python-patterns.md](references/python-patterns.md) for detailed examples.

**Rust (cargo)**

Common conflict patterns:
- Feature flag conflicts across workspace members
- Git dependencies with conflicting version constraints
- Platform-specific dependencies (Windows vs Linux)

Resolution tools:
- `cargo tree -d` - Show duplicate dependencies
- `cargo tree -i <package>` - Show inverse dependencies
- `cargo update --dry-run` - Preview updates
- `cargo outdated` - Check for newer versions

See [references/rust-patterns.md](references/rust-patterns.md) for detailed examples.

**PHP (composer)**

Common conflict patterns:
- Platform requirements (PHP version, extensions)
- Symfony component version mismatches
- Security advisories blocking updates

Resolution tools:
- `composer why <package>` - Show why package is installed
- `composer why-not <package> <version>` - Explain why version can't be installed
- `composer outdated` - List available updates
- `composer audit` - Security vulnerability scan

See [references/php-patterns.md](references/php-patterns.md) for detailed examples.
</ecosystem_specific_patterns>

<advanced_features>
**Semver Compatibility Analysis**

Understand version constraint symbols:
- `^1.2.3` → >=1.2.3 <2.0.0 (compatible changes)
- `~1.2.3` → >=1.2.3 <1.3.0 (patch updates only)
- `>=1.2.3 <2.0.0` → Explicit range
- `1.2.x` → Any patch version in 1.2.x
- `*` → Any version (avoid in production)

**Lockfile Strategy:**
- Always commit lockfiles (package-lock.json, poetry.lock, etc.)
- Use `npm ci` / `poetry install` in CI/CD (installs exact versions)
- Regularly update dependencies to avoid security debt
- Use automated tools (Dependabot, Renovate) for monitoring

**Monorepo Considerations:**
- Check workspace/sub-package dependencies
- Ensure consistent versions across workspace
- Use workspace protocols (pnpm workspace:, yarn workspace:)
- Validate peer dependencies across workspace packages

**Security Best Practices:**
- Prioritize CRITICAL and HIGH vulnerabilities
- Assess vulnerability context (dev vs production runtime)
- Check if vulnerability is exploitable in your usage
- Subscribe to security advisories for your ecosystem
- Integrate audit checks into CI/CD pipelines

See [references/advanced-resolution.md](references/advanced-resolution.md) for complex scenarios.
</advanced_features>

<anti_patterns>
**Avoid these common mistakes:**

**1. Blindly using --force or --legacy-peer-deps**
- Problem: Bypasses conflict detection, hides real issues
- Alternative: Investigate root cause, resolve properly

**2. Ignoring security warnings**
- Problem: Leaves known vulnerabilities in production
- Alternative: Assess severity, update or find alternatives

**3. Using wildcard versions (*) in production**
- Problem: Unpredictable builds, potential breaking changes
- Alternative: Use specific version ranges (^, ~)

**4. Deleting lockfiles to "fix" conflicts**
- Problem: Loses reproducible builds, may install incompatible versions
- Alternative: Resolve conflicts properly, regenerate lockfile

**5. Installing packages without checking compatibility**
- Problem: Breaks existing functionality, wastes debugging time
- Alternative: Use this skill to check before installing

**6. Mixing package managers (npm + yarn)**
- Problem: Conflicting lockfiles, inconsistent dependency resolution
- Alternative: Standardize on one package manager per project

**7. Upgrading all dependencies at once**
- Problem: Hard to identify which upgrade caused breakage
- Alternative: Update incrementally, test between updates

**8. Using outdated audit tools**
- Problem: Misses recent vulnerabilities and advisories
- Alternative: Keep audit tools updated, use latest patterns
</anti_patterns>

<success_criteria>
**Conflict successfully resolved when:**

- ✓ All peer dependencies are satisfied
- ✓ No version constraint violations
- ✓ Security audit passes (or vulnerabilities acknowledged)
- ✓ Lockfile updated consistently
- ✓ Installation completes without errors
- ✓ Dependency tree has no duplicate incompatible versions
- ✓ Platform/runtime requirements met
- ✓ Tests pass after installation (if applicable)

**Blocked installation when:**
- ✗ Critical security vulnerabilities without patches
- ✗ Circular dependency deadlock
- ✗ Incompatible platform requirements (Node 14 vs Node 18)
- ✗ Breaking changes without user approval
</success_criteria>

<reference_guides>
For ecosystem-specific details and advanced scenarios:

- **[references/javascript-patterns.md](references/javascript-patterns.md)** - npm/yarn/pnpm conflict examples and solutions
- **[references/python-patterns.md](references/python-patterns.md)** - pip/poetry conflict examples and solutions
- **[references/rust-patterns.md](references/rust-patterns.md)** - cargo conflict examples and solutions
- **[references/php-patterns.md](references/php-patterns.md)** - composer conflict examples and solutions
- **[references/advanced-resolution.md](references/advanced-resolution.md)** - Complex scenarios (monorepos, workspaces, feature flags)
- **[references/security-audit-guide.md](references/security-audit-guide.md)** - Security vulnerability assessment and remediation
</reference_guides>
