---
version: 1.0.1
name: bap-identity
description: Manage BAP (Bitcoin Attestation Protocol) identity files using bap-cli. This skill should be used when users need to create, decrypt, list, or extract BAP identity backups, work with .bep encrypted files, or generate test fixtures for Playwright tests involving BAP identities.
location: user
---

# BAP Identity Management

## Overview

This skill enables comprehensive management of BAP (Bitcoin Attestation Protocol) identity files using two complementary command-line tools:

- **bap-cli**: High-level BAP identity operations (create, list, extract member identities)
- **bbackup**: Low-level encryption/decryption of any JSON backup data

Use this skill when working with encrypted BAP identity backups (.bep files), creating new identities, extracting member identities, encrypting/decrypting JSON files, or generating test fixtures.

## Prerequisites

### Required Tools

Verify both tools are installed:

```bash
bap --version
bbackup --version
```

### Installing bap-cli

```bash
git clone https://github.com/b-open-io/bap-cli.git
cd bap-cli
bun install
bun run build
bun link
```

### Installing bbackup

```bash
git clone https://github.com/rohenaz/bitcoin-backup.git
cd bitcoin-backup
bun install
bun run build
bun link
```

## Tool Selection Guide

Choose the appropriate tool based on the task:

### Use bap-cli when:
- Creating new BAP identities
- Listing identities in a master backup
- Extracting member identities from master backup
- Working specifically with BAP identity structures
- Generating test fixtures for automated tests

### Use bbackup when:
- Encrypting arbitrary JSON data to .bep format
- Decrypting .bep files to inspect contents
- Upgrading encryption strength (100k → 600k iterations)
- Working with non-BAP backup formats (WifBackup, OneSatBackup, VaultBackup)
- Need lower-level control over encryption parameters

### Use both when:
- Inspecting BAP identities created by bap-cli
- Re-encrypting backups with different passwords
- Migrating between encryption strengths
- Debugging backup file issues

## Core Operations with bap-cli

### Creating New Identity Backups

When users request a new BAP identity, use the `bap new` command with appropriate backup type:

**Type42 backups** (recommended for simplicity):
- Use random root private key
- Simpler key management
- Suitable for most use cases

```bash
bap new --type type42 --password <password> --name "<name>" --output <file.bep>
```

**Legacy (BIP32) backups** (for hierarchical deterministic wallets):
- Use HD derivation from mnemonic
- Generates BIP32 mnemonic phrase
- Required when mnemonic recovery is needed

```bash
bap new --type legacy --password <password> --name "<name>" --output <file.bep>
```

**Important**: Always use strong passwords. The password encrypts the backup file and cannot be recovered if lost.

### Listing Identities

When users need to see what identities are in a backup file, use `bap list`:

```bash
bap list <backup.bep> --password <password>
```

This displays:
- All identity keys with their indices
- Backup type (Type42 or Legacy)
- Number of identities in the backup

Use this before extracting member identities to determine the correct index.

### Extracting Member Identities

When users need to extract a single identity from a master backup (common for distributing individual identities), use `bap member`:

```bash
bap member <master.bep> --password <password> --index <index> --output <member.bep>
```

The index is zero-based. To find the correct index:
1. First run `bap list` on the master backup
2. Note the index of the desired identity
3. Extract using that index

### Decrypting and Inspecting Backups

When users need to view the contents of an encrypted backup, use `bap export`:

```bash
bap export <backup.bep> --password <password>
```

This outputs the decrypted JSON structure. Use this to:
- Debug backup issues
- Verify backup contents
- Inspect identity structure

Optionally save re-encrypted version:

```bash
bap export <backup.bep> --password <password> --output <new.bep>
```

## Core Operations with bbackup

### Encrypting JSON Files

When users have JSON data that needs encryption:

```bash
bbackup enc <input.json> -p <password> [-o <output.bep>]
```

**Use cases:**
- Encrypting manually created backup JSON
- Encrypting exported identity data
- Creating custom encrypted payloads

**Example:**
```bash
# Create JSON file
echo '{"wif":"L5EZftvrYa...","label":"My Key"}' > wallet.json

# Encrypt it
bbackup enc wallet.json -p "strongpass" -o wallet.bep
```

### Decrypting to JSON

When users need to inspect encrypted .bep files:

```bash
bbackup dec <input.bep> -p <password> [-o <output.json>]
```

**Use cases:**
- Inspecting backup contents
- Debugging encrypted files
- Extracting data for processing

**Example:**
```bash
# Decrypt to JSON
bbackup dec identity.bep -p "password" -o identity.json

# View contents
cat identity.json
```

### Upgrading Encryption Strength

When users have older backups with weaker encryption (100k iterations):

```bash
bbackup upg <old.bep> -p <password> -o <upgraded.bep>
```

This upgrades to 600,000 PBKDF2 iterations (NIST recommended).

**Use cases:**
- Strengthening security of existing backups
- Migrating legacy backups
- Preparing backups for long-term storage

## Combined Workflows

### Inspect BAP Identity Using bbackup

When users need to examine a BAP identity created by bap-cli:

```bash
# Create identity with bap-cli
bap new --type type42 --password pass123 --name "Alice" --output alice.bep

# Decrypt with bbackup to inspect
bbackup dec alice.bep -p pass123 -o alice.json

# View the JSON structure
cat alice.json

# Shows: { "ids": "...", "rootPk": "...", "label": "Alice", "createdAt": "..." }
```

This is useful for:
- Understanding the internal structure
- Debugging identity issues
- Verifying backup contents
- Extracting specific fields programmatically

### Change Password on BAP Identity

When users need to re-encrypt a backup with a different password:

```bash
# Decrypt with old password
bbackup dec identity.bep -p "oldpass" -o identity.json

# Re-encrypt with new password
bbackup enc identity.json -p "newpass" -o identity-new.bep

# Clean up temporary file
rm identity.json
```

### Upgrade Security of BAP Backup

When users have older BAP identities that need stronger encryption:

```bash
# Upgrade directly (maintains same password)
bbackup upg old-identity.bep -p "password" -o identity-upgraded.bep

# Verify it works with bap-cli
bap list identity-upgraded.bep --password password
```

### Extract and Transform Member Identity

When users need to extract and modify a member identity:

```bash
# Extract member with bap-cli
bap member master.bep --password pass --index 0 --output member.bep

# Decrypt to JSON with bbackup
bbackup dec member.bep -p pass -o member.json

# Modify JSON as needed (e.g., change label)
# ... manual editing or script ...

# Re-encrypt modified version
bbackup enc member.json -p pass -o member-modified.bep
```

### Debug Backup Issues

When users encounter problems with backups:

1. Try with bap-cli first:
```bash
bap list problematic.bep --password password
```

2. If that fails, try bbackup for more details:
```bash
bbackup dec problematic.bep -p password -o debug.json
```

3. Inspect the JSON structure:
```bash
cat debug.json | jq .  # Pretty print if jq is available
```

## Test Fixture Generation (Programmatic)

When users need BAP identities for Playwright or automated testing, use the programmatic API:

```typescript
import { createType42Backup } from "bap-cli";

// Generate backup with multiple test identities
const backup = await createType42Backup("testpassword123", [
  { name: "Test User 1" },
  { name: "Test User 2" },
]);

// Save to file
await backup.saveTo("/tmp/test-backup.bep");

// Get identity keys for assertions
const keys = await backup.getIdentityKeys();

// Extract member backup for specific identity
const memberBackup = await backup.getMemberBackup(0);

// Clean up temp files when done
await backup.cleanup();
```

This approach is more efficient than CLI for test automation as it:
- Generates identities programmatically
- Provides direct access to keys for test assertions
- Handles cleanup automatically
- Works with multiple identities in a single operation

## File Format Details

All BAP identity files use the `.bep` extension (Bitcoin Encrypted Payload):

**Master backups** (from bap-cli):
- Contain root key/xprv and can generate multiple identities
- Structure: `{ ids, rootPk/xprv, label?, createdAt? }`

**Member backups** (from bap-cli):
- Contain single identity (WIF and identity key)
- Structure: `{ wif, id, label?, createdAt? }`

**Encryption** (used by both tools):
- Algorithm: AES-256-GCM
- Key derivation: PBKDF2-SHA256
- Iterations: 600,000 (recommended) or 100,000 (legacy)
- Format: Base64 encoded string

## Error Handling

### bap-cli Errors

**"Error: type must be 'legacy' or 'type42'"**
- Use correct --type flag with valid value

**"Error: Invalid index"**
- Run `bap list` first to see available indices
- Indices are zero-based (first identity is index 0)

**Decryption failures**
- Verify correct password
- Ensure file is not corrupted
- Check file is actually a .bep backup

**"bap: command not found"**
- Install bap-cli globally using installation steps above

### bbackup Errors

**"Decryption failed"**
- Wrong password
- Corrupted file
- Try bap-cli commands if file is BAP-specific

**"Invalid backup format"**
- Input file for `enc` must be valid JSON
- Check JSON syntax: `cat file.json | jq .`

**"Password too short"**
- Minimum 8 characters required
- Use 12+ characters for high-value secrets

### General Troubleshooting

1. **Verify tools are installed**:
```bash
which bap bbackup
```

2. **Test basic encryption cycle**:
```bash
echo '{"test":"data"}' > test.json
bbackup enc test.json -p "testpass" -o test.bep
bbackup dec test.bep -p "testpass" -o out.json
diff test.json out.json  # Should match
rm test.json test.bep out.json
```

3. **Check file format**:
```bash
file backup.bep  # Should show ASCII text (base64)
head -c 50 backup.bep  # Should show base64 characters
```

## Reference Documentation

Complete command reference and advanced usage:

- **bap-cli**: See `references/bap-cli-reference.md` for:
  - Detailed command syntax
  - All available options
  - Programmatic API documentation
  - Complete examples

- **bbackup**: See `references/bbackup-reference.md` for:
  - Encryption specifications
  - Security features
  - Integration patterns
  - Troubleshooting guide

## Common Use Case Patterns

### Pattern 1: Create → Inspect → Distribute

```bash
# 1. Create master identity
bap new --type type42 --password masterpass --name "Org Master" --output master.bep

# 2. Verify contents
bbackup dec master.bep -p masterpass -o master.json
cat master.json

# 3. Extract member for distribution
bap member master.bep --password masterpass --index 0 --output member-alice.bep

# 4. Distribute member.bep to Alice
```

### Pattern 2: Import → Upgrade → Export

```bash
# 1. Receive old backup
# old.bep (using 100k iterations)

# 2. Upgrade encryption
bbackup upg old.bep -p "password" -o new.bep

# 3. Verify with BAP tools
bap list new.bep --password password
```

### Pattern 3: Generate → Test → Cleanup

```typescript
// In test file
const backup = await createType42Backup("testpass", [
  { name: "Test Identity" }
]);

await backup.saveTo("/tmp/test.bep");

// Run tests using /tmp/test.bep

await backup.cleanup();  // Removes temp files
```
