---
name: midnight-tooling:midnight-compatibility
description: Use when checking Midnight version compatibility, understanding pragma language_version, verifying compiler and runtime version relationships, or troubleshooting version mismatch errors between Midnight components.
---

# Midnight Version Compatibility

Understanding version relationships between Midnight components.

## Component Overview

Midnight development involves multiple versioned components:

| Component | Purpose | Version Check |
|-----------|---------|---------------|
| Compact Developer Tools | CLI for managing compilers | `compact --version` |
| Compact Compiler | Compiles .compact to ZK circuits | `compact compile --version` |
| compact-runtime | JavaScript runtime library | `npm list @midnight-ntwrk/compact-runtime` |
| ledger | Core ledger types | `npm list @midnight-ntwrk/ledger` |
| midnight.js | JavaScript SDK | `npm list @midnight-ntwrk/midnight.js` |
| Proof Server | ZK proof generation | Docker image tag |

## Version Relationships

```
Language Version (in pragma)
         │
         ▼
┌─────────────────────────┐
│   Compact Compiler      │ ──── Produces ───▶ Contract Artifacts
│   (e.g., 0.26.0)        │
└─────────────────────────┘
         │
         │ Must match
         ▼
┌─────────────────────────┐
│   compact-runtime       │
│   (e.g., 0.9.0)         │
└─────────────────────────┘
         │
         │ Compatible with
         ▼
┌─────────────────────────┐
│   ledger, midnight.js   │
│   Proof Server          │
└─────────────────────────┘
```

## Checking Current Compatibility Matrix

The authoritative source is the support matrix in Midnight release notes.

To check current recommended versions:
```bash
/midnight:versions
```

Or parse directly:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-support-matrix.py
```

## Pragma Language Version

Every Compact contract must declare its language version:

```compact
pragma language_version 0.18;

ledger {
  // ...
}
```

### Pragma Rules

1. **Must match compiler capability**: The compiler must support the declared version
2. **Consistency**: All contracts in a project should use the same pragma
3. **Update on upgrade**: When upgrading compiler, update pragma if language version changed

### Finding Language Version for Compiler

The compiler version (e.g., 0.26.0) maps to a language version (e.g., 0.18.0):

```bash
# Check release notes for mapping
/midnight:changelog compact
```

Recent mappings (verify with release notes):
- Compiler 0.26.0 → Language 0.18.0 (Minokawa)
- Compiler 0.25.0 → Language 0.17.0

## Package Version Guidelines

### Use Exact Versions

In `package.json`, always use exact versions:

```json
{
  "dependencies": {
    "@midnight-ntwrk/compact-runtime": "0.9.0",
    "@midnight-ntwrk/ledger": "4.0.0",
    "@midnight-ntwrk/midnight.js": "2.1.0"
  }
}
```

**Never use**:
- `^0.9.0` (allows minor updates)
- `~0.9.0` (allows patch updates)
- `>=0.9.0` (allows any newer version)

### Why Exact Versions Matter

Midnight components have strict compatibility requirements. A minor version bump in one component may require updates to others. Using ranges can lead to:

- Silent incompatibilities
- Works-on-my-machine issues
- CI failures with different lockfiles

## Using npm ci

For reproducible builds, use `npm ci` instead of `npm install`:

```bash
# npm ci uses exact versions from package-lock.json
npm ci

# npm install may update within semver ranges
npm install  # Avoid for production
```

## Compiler Version Management

### List Available Versions

```bash
compact list
```

### List Installed Versions

```bash
compact list --installed
```

### Switch Default Version

```bash
# Update to latest
compact update

# Switch to specific version
compact update 0.25.0
```

### Use Specific Version for One Compilation

```bash
# Prefix with +version
compact compile +0.25.0 src/contract.compact contract/
```

This is useful for:
- Testing against multiple compiler versions
- Maintaining older contracts while developing new ones
- Gradual migration

## Proof Server Versions

The proof server must be compatible with your contracts:

```bash
# Check available tags
docker search midnightnetwork/proof-server

# Pull specific version
docker pull midnightnetwork/proof-server:4.0.0

# Run specific version
docker run -p 6300:6300 midnightnetwork/proof-server:4.0.0 -- midnight-proof-server --network testnet
```

## Breaking Changes Between Versions

When upgrading, check release notes for breaking changes:

```bash
/midnight:changelog compact
```

Common breaking changes include:
- New reserved keywords (e.g., `slice` in 0.18.0)
- Runtime function renames
- Type system changes
- New pragma requirements

## Version Upgrade Workflow

1. **Check current versions**: `/midnight:versions`
2. **Check target versions**: Review compatibility matrix
3. **Read release notes**: `/midnight:changelog <component>`
4. **Update package.json**: Use exact versions
5. **Update compiler**: `compact update <version>`
6. **Update pragma**: If language version changed
7. **Clean install**: `rm -rf node_modules && npm ci`
8. **Recompile**: `compact compile src/*.compact contract/`
9. **Test**: Run your test suite

## Additional Resources

- **`references/compatibility-matrix.md`** - Detailed version compatibility table
- **`references/pragma-guide.md`** - Pragma declaration guide

For troubleshooting version issues, see the `midnight-debugging` skill.
