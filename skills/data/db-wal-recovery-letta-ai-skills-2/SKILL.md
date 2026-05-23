---
name: db-wal-recovery
description: Guide for recovering data from SQLite Write-Ahead Log (WAL) files that may be corrupted, encrypted, or inaccessible through standard methods. This skill should be used when tasks involve SQLite database recovery, WAL file analysis, encrypted database files, or discrepancies between tool outputs and filesystem access.
---

# SQLite WAL File Recovery

## Overview

This skill provides systematic approaches for recovering data from SQLite Write-Ahead Log (WAL) files. WAL recovery tasks often involve files that are corrupted, encrypted, or exhibit unusual access patterns. The skill emphasizes thorough investigation over pattern-guessing and provides verification strategies to ensure actual data recovery rather than fabrication.

## Critical Principle: Never Guess Data

When recovering database records, the goal is to **recover actual data**, not to generate plausible data based on patterns. If data cannot be recovered through technical means, acknowledge failure rather than fabricate records.

## Investigation Workflow

### Phase 1: Environment Discovery

Before attempting recovery, conduct thorough environment discovery:

1. **Inventory all files** using multiple methods:
   - Use built-in tool commands (e.g., `LS`, `Read`) to list directory contents
   - Use bash commands (`ls -la`, `find`, `locate`) independently
   - Compare outputs—discrepancies are significant clues

2. **Check for discrepancies between tools and bash**:
   - If a built-in tool shows a file exists but bash cannot access it, this indicates special access requirements
   - Document the exact discrepancy: tool name, output shown, bash command tried, bash result
   - This discrepancy often indicates encrypted filesystems, virtual files, or special permissions

3. **Examine the environment for clues**:
   - Check environment variables for encryption keys or paths
   - Look for configuration files (.env, config.json, .sqlite*, etc.)
   - Search for related files (key files, password files, encrypted containers)

### Phase 2: File Analysis

When a WAL file is located:

1. **Examine file headers**:
   - Valid SQLite WAL files start with magic bytes: `377f0682` (hex) or specific WAL header signature
   - Check byte offsets 0-32 for WAL header structure
   - Compare against documented SQLite WAL format (see references/wal_format.md)

2. **Analyze binary structure**:
   - Use `xxd` or `hexdump` for initial inspection
   - Look for recognizable patterns (ASCII strings, repeated structures)
   - Identify frame boundaries in WAL files

3. **Detect encryption or corruption**:
   - High entropy throughout = likely encrypted
   - Valid header but corrupted frames = partial corruption
   - No recognizable structure = unknown encoding or encryption

### Phase 3: Recovery Approaches

Attempt recovery methods in order of likelihood:

#### For Encrypted Files

1. **Search for decryption keys**:
   - Environment variables
   - Adjacent files (*.key, *.pem, config files)
   - Database pragmas (PRAGMA key for SQLCipher)

2. **Try common encryption schemes**:
   - SQLCipher (most common SQLite encryption)
   - SEE (SQLite Encryption Extension)
   - Custom XOR with multi-byte keys (not just single-byte)
   - AES-256-CBC with standard key derivation

3. **Test multiple key formats**:
   - Raw bytes
   - Hex-encoded strings
   - Base64-encoded keys
   - Passphrase-based derivation (PBKDF2)

#### For Corrupted Files

1. **Attempt SQLite recovery tools**:
   - `sqlite3 .recover` command
   - `.dump` to extract what's possible
   - Third-party tools like `undark` or `sqlite-recover`

2. **Manual page reconstruction**:
   - Identify valid WAL frames
   - Extract page data from intact frames
   - Apply changes to database manually

3. **Partial recovery**:
   - Extract readable text strings with `strings` command
   - Parse individual records from binary data
   - Reconstruct table structure from fragments

#### For Virtual/Inaccessible Files

When tools show a file that bash cannot access:

1. **Investigate the access method**:
   - The tool showing the file has special access—understand how
   - Try reading through the same tool that listed the file
   - Look for mount points, FUSE filesystems, or encrypted containers

2. **Check for special filesystems**:
   - EncFS, gocryptfs, or similar encrypted filesystems
   - FUSE-mounted virtual filesystems
   - Container-based isolation

3. **Examine tool capabilities**:
   - Some tools may have built-in decryption
   - Check tool documentation for special file handling
   - Try tool-specific read commands

## Verification Strategies

### Before Declaring Success

1. **Verify recovered data makes sense**:
   - Check data types match expected schema
   - Validate relationships between records
   - Compare against known valid records

2. **Cross-reference with database**:
   - Query the main database for gaps or references to missing data
   - Check foreign key relationships
   - Examine indexes for expected entries

3. **Test data integrity**:
   - Run `PRAGMA integrity_check`
   - Verify transaction consistency
   - Check checkpoint status

### Red Flags Indicating Incorrect Approach

- Finding yourself "guessing" what data should be
- Relying on pattern recognition rather than actual data extraction
- Multiple arbitrary choices for the same record
- High uncertainty about recovered values
- No binary data supporting the recovered values

## Common Pitfalls

### Pitfall 1: Abandoning Investigation Too Early

**Wrong**: Conclude file doesn't exist after a few bash commands fail
**Right**: Investigate why built-in tools showed different results; the discrepancy is a clue

### Pitfall 2: Single-Method Encryption Testing

**Wrong**: Try only single-byte XOR and conclude file isn't encrypted
**Right**: Test multiple encryption schemes, key lengths, and formats systematically

### Pitfall 3: Pattern-Based Data Generation

**Wrong**: Notice alphabetical pattern and generate next items in sequence
**Right**: Recovery means extracting actual data; if data cannot be extracted, acknowledge failure

### Pitfall 4: Ignoring WAL File Structure

**Wrong**: Treat WAL as opaque binary blob
**Right**: Parse according to documented SQLite WAL format to identify frames and pages

### Pitfall 5: Missing Environmental Clues

**Wrong**: Focus only on the database files
**Right**: Search entire environment for keys, configuration, related files

## Escalation Checklist

If standard recovery fails, verify completion of:

- [ ] Compared tool output vs bash output for all file operations
- [ ] Searched for encryption keys in environment and adjacent files
- [ ] Tested at least 5 different encryption/encoding schemes
- [ ] Examined WAL file structure against documented format
- [ ] Attempted SQLite built-in recovery commands
- [ ] Tried reading through same tool that originally showed the file
- [ ] Checked for special filesystems or mount points
- [ ] Extracted and analyzed any readable string content
- [ ] Documented specific technical blockers preventing recovery

Only after completing this checklist should recovery be considered impossible.

## Resources

Reference documentation for detailed technical specifications:

- `references/wal_format.md` - SQLite WAL file format specification and structure
