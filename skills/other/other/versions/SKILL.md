---
name: versions
description: |
  Check package versions before installing. CRITICAL - AUTO-INVOKE when:
  - About to install any package (bun add, npm install)
  - User asks about "latest version", "update package"
  - Before implementing with any library

  MANDATORY: Never install packages without checking version first.
allowed-tools: [Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
---

# Package Version Checker

**CRITICAL**: Always check latest version before installing ANY package.

## Check Version

```bash
# Check latest version
bun info <package>

# Examples
bun info gsap
bun info lenis
bun info @react-three/fiber
bun info framer-motion
```

## Install with Version

```bash
# Install latest
bun add gsap@latest

# Install specific version
bun add gsap@3.12.5
```

## Check Darkroom Package Versions

```bash
# Lenis (smooth scroll)
bun info lenis

# Hamo (performance hooks)
bun info hamo

# Tempus (RAF management)
bun info tempus
```

## Check Outdated Packages

```bash
# List outdated packages in project
bun outdated
```

## Why This Matters

1. **Security** - Old versions may have vulnerabilities
2. **Features** - Latest versions have new APIs
3. **Compatibility** - Mismatched versions cause issues
4. **Training data** - Your knowledge may be outdated

## Workflow

1. **Check version** - `bun info <package>`
2. **Fetch docs** - Use context7 for current documentation
3. **Install** - `bun add <package>@latest`
4. **Verify** - Check `package.json` has correct version

## Output

Report:
- **Package**: Name
- **Latest version**: Current release
- **Your version**: What's in package.json (if applicable)
- **Action**: Install/update recommendation
