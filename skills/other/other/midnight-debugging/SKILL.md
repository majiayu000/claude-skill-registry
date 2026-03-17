---
name: midnight-tooling:midnight-debugging
description: Use when encountering Midnight errors like "compact: command not found", "ERR_UNSUPPORTED_DIR_IMPORT", version mismatches, proof server failures, "@midnight-ntwrk" package errors, or compilation failures.
---

# Midnight Environment Debugging

Expert knowledge for identifying and resolving common Midnight development toolchain issues.

## Diagnostic Approach

When encountering Midnight-related errors, follow this systematic approach:

1. **Identify the error category** (see Error Categories below)
2. **Check cache freshness** - Run `/midnight:sync-releases` if version info needed
3. **Run diagnostics** - Use `/midnight:doctor` for comprehensive checks
4. **Apply targeted fixes** - Use the solutions from this skill
5. **Verify the fix** - Run `/midnight:check` to confirm

For comprehensive diagnostics:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py
```

## Error Categories

### 1. PATH and Installation Errors

**Symptom**: `compact: command not found`

**Diagnosis**:
```bash
# Check if compact exists somewhere
ls -la ~/.compact/bin/compact 2>/dev/null || echo "Not in default location"

# Check PATH
echo $PATH | tr ':' '\n' | grep -i compact
```

**Solutions**:

| Cause | Fix |
|-------|-----|
| Not installed | Run Compact installer (see midnight-setup skill) |
| Not in PATH | Add `export PATH="$HOME/.compact/bin:$PATH"` to shell profile |
| Wrong shell profile | Edit `~/.zshrc` (macOS) or `~/.bashrc` (Linux) |
| Profile not sourced | Open a **new** terminal window |

### 2. Version Mismatch Errors

**Symptoms**:
- Runtime errors mentioning version incompatibility
- Build failures after updating one component
- `pragma language_version` mismatches

**Diagnosis**:
```bash
# Check current versions
compact compile --version
npm list @midnight-ntwrk/compact-runtime
npm list @midnight-ntwrk/ledger
```

**Key Rule**: All Midnight components must use compatible versions per the support matrix.

**Solutions**:

1. **Check the compatibility matrix** in cached release notes or run `/midnight:versions`

2. **Use exact versions in package.json** (no `^` or `~`):
   ```json
   {
     "dependencies": {
       "@midnight-ntwrk/compact-runtime": "0.9.0",
       "@midnight-ntwrk/ledger": "4.0.0"
     }
   }
   ```

3. **Clean install after version changes**:
   ```bash
   rm -rf node_modules package-lock.json
   npm ci
   ```

4. **Recompile contracts after compiler update**:
   ```bash
   rm -rf contract/*.cjs contract/*.prover contract/*.verifier
   compact compile src/contract.compact contract/
   ```

See `references/version-mismatch-guide.md` for detailed version troubleshooting.

### 3. Node.js Import Errors

**Symptom**: `ERR_UNSUPPORTED_DIR_IMPORT`

**Causes**:
- Stale terminal environment after Node version switch
- Cached module references
- Wrong Node.js version active

**Solutions**:

1. **Open a new terminal window** (not just source profile)

2. **Clear module cache**:
   ```bash
   rm -rf node_modules/.cache
   ```

3. **Verify correct Node version**:
   ```bash
   node --version  # Should be 18+
   nvm use 18      # If using nvm
   ```

4. **Reinstall node_modules**:
   ```bash
   rm -rf node_modules
   npm install
   ```

### 4. Proof Server Issues

**Symptoms**:
- Connection refused on port 6300
- Wallet cannot generate proofs
- "Proof server not responding"

**Diagnosis**:
```bash
# Check if running
docker ps | grep proof-server

# Check if port is available
lsof -i :6300

# Check Docker is running
docker info
```

**Solutions**:

| Issue | Fix |
|-------|-----|
| Not running | `docker run -p 6300:6300 midnightnetwork/proof-server -- midnight-proof-server --network testnet` |
| Port in use | Stop other process: `kill $(lsof -t -i:6300)` or use different port |
| Docker not running | Start Docker Desktop |
| Image not pulled | `docker pull midnightnetwork/proof-server:latest` |
| Wrong network | Ensure `--network testnet` matches your target |

### 5. Compilation Errors

**Symptoms**:
- Contract compilation fails
- Type errors in Compact code
- Circuit generation errors

**Diagnosis**:
```bash
# Check compiler version matches pragma
compact compile --version

# In contract file, check pragma:
# pragma language_version 0.18;
```

**Common Issues**:

| Error | Cause | Fix |
|-------|-------|-----|
| Pragma mismatch | Contract declares different version | Update pragma or switch compiler version |
| Type errors | Language feature changed | Check release notes for breaking changes |
| Circuit too large | Complex computation | Simplify logic or split into multiple transactions |

### 6. Package Installation Errors

**Symptoms**:
- `npm install` fails for @midnight-ntwrk packages
- Peer dependency conflicts
- Registry errors

**Solutions**:

1. **Check npm registry access**:
   ```bash
   npm view @midnight-ntwrk/compact-runtime
   ```

2. **Clear npm cache**:
   ```bash
   npm cache clean --force
   ```

3. **Use exact versions** to avoid peer conflicts

4. **Don't mix lockfiles** - use only `package-lock.json` (npm) OR `bun.lock` (Bun)

## Quick Diagnostic Commands

| Check | Command |
|-------|---------|
| All tool versions | `/midnight:check` |
| Comprehensive diagnostic | `/midnight:doctor` |
| Current vs latest versions | `/midnight:versions` |
| Component changelog | `/midnight:changelog compact` |

## Error Message Reference

See `references/common-errors.md` for a complete catalog of error messages and their solutions.

## When to Seek Additional Help

If standard troubleshooting doesn't resolve the issue:

1. Check the [Midnight FAQ](https://docs.midnight.network/develop/faq)
2. Review the [Getting Help](https://docs.midnight.network/getting-started/getting-help) section
3. Join the Midnight developer community channels
