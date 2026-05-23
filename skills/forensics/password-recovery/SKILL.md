---
name: password-recovery
description: This skill provides guidance for recovering passwords or sensitive data from disk images, corrupted files, or forensic scenarios. Use this skill when tasked with extracting passwords from disk images, recovering deleted files containing credentials, or performing data forensics to find lost authentication information.
---

# Password Recovery

## Overview

This skill guides agents through password and credential recovery from disk images, file systems, and forensic scenarios. It emphasizes proper forensic tool usage, systematic fragment analysis, and validation of recovered data.

## Core Workflow

### Phase 1: Image Analysis and Format Identification

Before searching for password data, understand the container format:

1. **Identify the image type**
   - Check for filesystem signatures (ext2/3/4, NTFS, FAT)
   - Look for archive signatures (PK for ZIP, 7z, etc.)
   - Use `file` command, but verify with hex inspection if results are ambiguous

2. **Examine the structure**
   ```bash
   # Check file type
   file image.img

   # Examine hex header for signatures
   xxd image.img | head -50

   # Look for common signatures
   # - "PK" at offset 0 indicates ZIP
   # - ext4 superblock at offset 1024
   # - NTFS "NTFS" at offset 3
   ```

3. **Determine recovery approach based on format**
   - Filesystem image → use forensic tools (extundelete, debugfs, testdisk)
   - Archive → extract properly before searching
   - Raw data → byte-level search as last resort

### Phase 2: Use Proper Forensic Tools First

**Critical**: Always attempt structured recovery before raw byte searching.

For ext2/3/4 filesystems:
```bash
# List deleted files
extundelete --list image.img

# Recover specific file
extundelete --restore-file path/to/file image.img

# Interactive filesystem exploration
debugfs image.img
# Within debugfs: ls -d, stat, cat, dump
```

For NTFS:
```bash
# Use ntfsundelete or autopsy
ntfsundelete image.img --scan
```

For FAT:
```bash
# Use testdisk or photorec
testdisk image.img
```

### Phase 3: Fragment Search (Only After Tool-Based Recovery Fails)

If forensic tools cannot recover complete files, proceed with fragment search:

1. **Extract candidate strings systematically**
   ```bash
   # Extract all printable strings
   strings -n 8 image.img > all_strings.txt

   # Search with context
   strings image.img | grep -i "password" -A2 -B2
   ```

2. **Document fragment locations and context**
   ```bash
   # Find offset of specific pattern
   grep -boa "PATTERN" image.img

   # Examine surrounding bytes
   xxd -s OFFSET -l 256 image.img
   ```

3. **Analyze fragments before combining**
   - Record exact offset of each fragment
   - Examine bytes immediately before and after each fragment
   - Check if fragments are within the same filesystem block
   - Look for structural indicators (file headers, delimiters)

## Validation Strategies

### Fragment Combination Validation

Before concatenating fragments, verify:

1. **Proximity check**: Are fragments within reasonable distance?
   - Same filesystem block (typically 4KB) → likely same file
   - Separated by megabytes → likely different files

2. **Context check**: What surrounds each fragment?
   - Look for consistent file format markers
   - Check for terminating characters (null bytes, newlines)

3. **Order verification**: Test multiple orderings if ambiguous
   - Fragment A + Fragment B
   - Fragment B + Fragment A
   - Consider overlapping characters

### Password Format Validation

When password format constraints are known:

1. **Length validation**: Does the result match expected length?
2. **Character set validation**: Does it use allowed characters only?
3. **Pattern validation**: Does it match expected patterns (e.g., specific prefix)?

**Warning**: Meeting format constraints does NOT confirm correctness. Multiple strings can satisfy the same constraints.

## Common Pitfalls

### 1. Skipping Forensic Tools

**Mistake**: Jumping directly to `strings` and `grep` without trying proper recovery tools.

**Why it matters**: Forensic tools understand file system structure and can recover complete files, including proper fragment ordering.

**Solution**: Always run `extundelete --list` or equivalent first to see what can be recovered structurally.

### 2. Confirmation Bias in Fragment Assembly

**Mistake**: Finding fragments that mathematically combine to expected length and assuming they belong together.

**Why it matters**: Disk images may contain multiple unrelated strings. Finding two fragments that add up to 23 characters doesn't mean they're from the same source.

**Solution**:
- Examine the context around each fragment
- Check if fragments are from the same filesystem region
- Consider alternative combinations
- Look for evidence they belong together beyond length matching

### 3. Ignoring Container Format

**Mistake**: Treating all disk images as raw byte sequences.

**Why it matters**: A disk image containing a ZIP file should be extracted first. "PK" signatures indicate ZIP structure that can be properly parsed.

**Solution**: Always check hex headers for format signatures before raw searching:
- `504B` (PK) = ZIP archive
- `377ABCAF` = 7z archive
- `1F8B` = gzip

### 4. Incomplete String Extraction

**Mistake**: Assuming `PASSWORD=VALUE` contains the complete password.

**Why it matters**: The password might extend beyond what's visible in one extraction, or the extraction might be truncated.

**Solution**:
- Extract more context around matches
- Check for null terminators or line endings
- Verify against expected format/length requirements

### 5. Premature Conclusion

**Mistake**: Stopping after finding the first plausible answer.

**Why it matters**: The first match might be incorrect, especially with fragmented data.

**Solution**:
- Generate multiple candidate passwords
- Validate each against known constraints
- If possible, test candidates against the target system

## Verification Checklist

Before finalizing a recovered password:

- [ ] Attempted recovery with proper forensic tools (extundelete, debugfs, etc.)
- [ ] Identified and analyzed the disk image format
- [ ] If fragments were combined, verified they're from the same logical region
- [ ] Examined context around all fragments
- [ ] Tested alternative fragment orderings if applicable
- [ ] Validated against all known format constraints
- [ ] Considered whether other valid combinations exist

## References

For detailed information on forensic tools and techniques, see `references/forensic_tools.md`.
