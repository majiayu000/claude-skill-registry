---
name: cobol-modernization
description: This skill provides guidance for translating COBOL programs to modern languages (Python, Java, etc.) while preserving exact behavior. It should be used when tasks involve COBOL-to-modern-language migration, legacy code translation, fixed-width file format handling, or ensuring byte-level compatibility between source and target implementations.
---

# COBOL Modernization

## Overview

This skill guides the translation of COBOL programs to modern languages while ensuring functional equivalence. COBOL modernization requires meticulous attention to data formats, file handling semantics, and numeric precision to achieve byte-for-byte output compatibility.

## Core Principles

### Complete Source Understanding First

Before writing any translation code:

1. **Read the entire COBOL source** - Never work from truncated views. If output is truncated, request the complete file in chunks or use multiple reads with offsets.
2. **Map all data structures** - Identify every WORKING-STORAGE, FILE SECTION, and LINKAGE SECTION variable with exact PICTURE clauses.
3. **Document file formats** - Create explicit specifications for every file's record layout including field positions, lengths, and data types.
4. **Identify all I/O operations** - Note READ, WRITE, REWRITE, DELETE operations and their conditions.

### Fixed-Width Record Handling

COBOL programs typically use fixed-width record formats. Critical considerations:

- **Record length calculation** - Sum all field lengths from the FD (File Description) or record definitions
- **Padding behavior** - COBOL pads strings with spaces and numbers with zeros
- **Numeric formatting** - PICTURE clauses like `9(10)` mean 10-digit zero-padded numbers
- **Sign handling** - Signed numbers may use trailing sign conventions

### Verification Strategy

Implement a systematic comparison approach:

1. **Create baseline outputs** - Run the original COBOL program to establish expected outputs
2. **Test incrementally** - Verify each logical section before moving to the next
3. **Byte-level comparison** - Use `diff` or `cmp` to verify exact output match, not just logical equivalence
4. **Preserve test artifacts** - Keep backup copies of all data files until verification is complete

## Translation Workflow

### Phase 1: Analysis

1. Read and document all COBOL source files completely
2. Map every data structure with exact field specifications:
   ```
   Field Name | PICTURE | Length | Position | Type
   ACCOUNT-ID | X(5)    | 5      | 1-5      | Alphanumeric
   BALANCE    | 9(10)   | 10     | 6-15     | Numeric
   ```
3. Document all file record layouts with byte positions
4. Identify validation logic and business rules
5. Note any COBOL-specific behaviors (REWRITE semantics, file status codes)

### Phase 2: Implementation

1. Implement data parsing functions that match exact COBOL field positions
2. Use string slicing based on documented positions, not assumptions
3. Implement numeric formatting to match PICTURE clauses exactly
4. Handle file operations with equivalent semantics (especially REWRITE vs WRITE)

### Phase 3: Verification

1. Back up all original data files before any testing
2. Run COBOL program and capture outputs
3. Restore data files to original state
4. Run translated program and capture outputs
5. Compare outputs byte-by-byte
6. Test multiple scenarios including:
   - Happy path (valid transactions)
   - Invalid inputs (missing records, bad references)
   - Edge cases (zero values, maximum lengths)
   - Boundary conditions (empty files, single records)

## Common Pitfalls

### Incomplete Source Reading

**Problem**: Working from truncated code views leads to missing logic.
**Prevention**: Always verify the complete source is available. If truncated, use offset reading or request full file.

### Record Length Mismatch

**Problem**: Input files don't match expected record lengths.
**Prevention**: Calculate expected length from COBOL definitions. If files differ, investigate whether COBOL handles short records with padding.

### Numeric Field Formatting

**Problem**: Python's default number-to-string conversion doesn't match COBOL's zero-padded format.
**Prevention**: Use explicit formatting: `f"{value:010d}"` for `PIC 9(10)`.

### REWRITE vs WRITE Semantics

**Problem**: COBOL's REWRITE updates a record in place; Python file operations differ.
**Prevention**: For indexed files, read entire file, modify in memory, write complete file. Track record positions explicitly.

### Premature Cleanup

**Problem**: Removing backup files before confirming task completion.
**Prevention**: Keep all backups until explicit final verification succeeds.

### Assuming Input Validity

**Problem**: Not testing with malformed or edge-case inputs.
**Prevention**: Create explicit test cases for invalid inputs, boundary values, and empty files.

## Verification Checklist

Before declaring translation complete:

- [ ] Complete COBOL source has been read (no truncation)
- [ ] All data structures documented with exact field positions
- [ ] All file formats documented with record layouts
- [ ] Translated code has been read back and verified complete
- [ ] COBOL baseline outputs captured for comparison
- [ ] Translated outputs match byte-for-byte
- [ ] Multiple test scenarios executed (valid, invalid, edge cases)
- [ ] Backup files preserved until final verification

## Testing Script Pattern

Create a reusable comparison workflow:

```bash
# Backup original data
for f in *.DAT; do cp "$f" "${f}.orig"; done

# Run COBOL version
./run_cobol.sh
for f in *.DAT; do cp "$f" "${f%.DAT}_COBOL.DAT"; done

# Restore and run Python version
for f in *.DAT.orig; do cp "$f" "${f%.orig}"; done
python program.py
for f in *.DAT; do [[ ! "$f" =~ (COBOL|orig) ]] && cp "$f" "${f%.DAT}_PYTHON.DAT"; done

# Compare outputs
for f in *_COBOL.DAT; do
    base="${f%_COBOL.DAT}"
    diff -q "${base}_COBOL.DAT" "${base}_PYTHON.DAT" || echo "MISMATCH: $base"
done
```

## Edge Cases to Test

1. **Insufficient balance** - Buyer lacks funds for transaction
2. **Empty data files** - How do both programs handle empty inputs?
3. **Malformed input** - Non-numeric values, wrong field lengths
4. **Self-referential transactions** - Buyer equals seller
5. **Multiple transactions** - Batch processing if supported
6. **Maximum values** - Largest values that fit in PICTURE clauses
7. **Missing references** - Referenced records that don't exist
