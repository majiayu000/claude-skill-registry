---
name: sqlite-db-truncate
description: This skill should be used when recovering data from corrupted or truncated SQLite databases. Apply this skill when a .db file cannot be opened with standard SQLite tools, when binary truncation has occurred, or when manual parsing of the SQLite binary format is needed to extract recoverable data.
---

# SQLite Database Truncation Recovery

## Overview

Recover data from SQLite databases that have been corrupted through binary truncation. This skill provides a systematic approach to binary format analysis and data extraction when standard SQLite libraries fail.

## Recommended Approach

### Phase 1: Initial Assessment (Do This First)

Before writing any recovery code, perform thorough analysis:

1. **Check file size and basic properties**
   ```python
   import os
   file_size = os.path.getsize('database.db')
   print(f"File size: {file_size} bytes")
   print(f"Expected pages: {file_size // 4096} (assuming 4KB pages)")
   ```

2. **Attempt standard recovery methods first**
   ```bash
   # Try sqlite3 recovery (may work for partial corruption)
   sqlite3 database.db ".recover" > recovered.sql 2>&1
   sqlite3 database.db "PRAGMA integrity_check;"
   ```

3. **Create comprehensive hex dump before coding**
   ```python
   with open('database.db', 'rb') as f:
       data = f.read()

   # Examine first 256 bytes thoroughly
   for i in range(0, min(256, len(data)), 16):
       hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
       ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
       print(f"{i:04x}: {hex_str:<48} {ascii_str}")
   ```

**Critical observations to document**:
- Is the SQLite header present? (Bytes 0-15 should be "SQLite format 3\0")
- What is the page size? (Bytes 16-17, big-endian)
- Is page 0 corrupted/zeroed?
- Where does data appear to start?
- What page type byte is present? (Look for 0x0d = leaf table)

### Phase 2: Recovery Method Selection

Choose the appropriate method based on Phase 1 findings:

**If standard SQLite tools work**: Use `sqlite3` library directly, no manual parsing needed.

**If header is intact but data is truncated**: Standard recovery may partially work; supplement with manual parsing for truncated pages.

**If header is corrupted/missing**: Manual binary parsing is required. Common scenario for truncated databases where first page is damaged.

### Phase 3: Structured Binary Parsing

Follow this order strictly to avoid iteration waste:

#### Step 1: Identify Page Structure

```python
# For truncated DBs, data often starts at a page boundary
# Common page types:
# 0x0d (13) = Leaf table page (contains actual row data)
# 0x05 (5) = Interior table page (contains child page pointers)
# 0x0a (10) = Leaf index page
# 0x02 (2) = Interior index page

page_type = data[0]  # Or data[100] if header is intact
if page_type == 0x0d:
    print("Found leaf table page - contains recoverable data")
```

#### Step 2: Extract Cell Count and Pointers

```python
import struct

# For leaf table page (0x0d), header is 8 bytes
# Bytes 3-4: number of cells (big-endian uint16)
num_cells = struct.unpack('>H', data[3:5])[0]
print(f"Cell count: {num_cells}")

# Cell pointer array starts at byte 8
cell_pointers = []
for i in range(num_cells):
    ptr_offset = 8 + (i * 2)
    if ptr_offset + 2 <= len(data):
        ptr = struct.unpack('>H', data[ptr_offset:ptr_offset+2])[0]
        # Validate pointer is within file bounds
        if ptr < len(data):
            cell_pointers.append(ptr)
        else:
            print(f"Warning: Cell pointer {ptr} exceeds file size {len(data)}")
```

#### Step 3: Parse ONE Cell First (Critical)

Before processing all cells, validate the parsing logic on a single cell:

```python
def parse_cell_verbose(data, offset):
    """Parse a single cell with detailed debug output."""
    print(f"\n=== Cell at offset {offset} (0x{offset:04x}) ===")
    print(f"Raw bytes: {' '.join(f'{b:02x}' for b in data[offset:offset+32])}")

    # Read payload size (varint)
    payload_size, pos = read_varint(data, offset)
    print(f"Payload size: {payload_size} (next pos: {pos})")

    # Read row ID (varint)
    row_id, pos = read_varint(data, pos)
    print(f"Row ID: {row_id} (next pos: {pos})")

    # Read header size (varint)
    header_size, header_start = read_varint(data, pos)
    print(f"Header size: {header_size} (header starts at: {header_start})")

    # Calculate header end
    header_end = pos + header_size
    print(f"Header end: {header_end}")

    # Read serial types
    serial_types = []
    current = header_start
    while current < header_end:
        serial_type, current = read_varint(data, current)
        serial_types.append(serial_type)
        print(f"  Serial type: {serial_type} (meaning: {describe_serial_type(serial_type)})")

    # Parse column values
    body_offset = header_end
    columns = []
    for i, st in enumerate(serial_types):
        value, body_offset = decode_serial_type(st, data, body_offset)
        print(f"  Column {i}: {value}")
        columns.append(value)

    return {'row_id': row_id, 'columns': columns}

# Test on first cell
result = parse_cell_verbose(data, cell_pointers[0])
print(f"\nParsed result: {result}")
```

**Validation checks**:
- Does the row ID look reasonable?
- Do column values make sense for the expected schema?
- Does string data decode properly as UTF-8?
- Are numeric values within expected ranges?

#### Step 4: Generalize to All Cells

Only after single-cell validation succeeds:

```python
recovered_rows = []
failed_cells = []

for ptr in cell_pointers:
    try:
        if ptr >= len(data):
            failed_cells.append({'offset': ptr, 'reason': 'beyond file boundary'})
            continue

        result = parse_cell(data, ptr)

        # Validate completeness
        if all(v is not None for v in result['columns']):
            recovered_rows.append(result)
        else:
            failed_cells.append({'offset': ptr, 'reason': 'incomplete data', 'partial': result})
    except Exception as e:
        failed_cells.append({'offset': ptr, 'reason': str(e)})

print(f"Recovered: {len(recovered_rows)} rows")
print(f"Failed: {len(failed_cells)} cells")
```

### Phase 4: Output Generation

```python
import json

# Format output according to task requirements
output = [
    {'word': row['columns'][0], 'value': row['columns'][1]}
    for row in recovered_rows
    if row['columns'][0] is not None and row['columns'][1] is not None
]

with open('recover.json', 'w') as f:
    json.dump(output, f, indent=2)

# Also save recovery log for debugging
with open('recovery.log', 'w') as f:
    f.write(f"Total cells found: {len(cell_pointers)}\n")
    f.write(f"Successfully recovered: {len(output)}\n")
    f.write(f"Failed/partial: {len(failed_cells)}\n")
    for fail in failed_cells:
        f.write(f"  {fail}\n")
```

## Common Pitfalls to Avoid

### Pitfall 1: Writing Multiple Trial Scripts

**Problem**: Creating `attempt1.py`, `attempt2.py`, etc. wastes time and creates confusion.

**Solution**: Build ONE modular script with helper functions. Use verbose debug output to understand issues rather than rewriting from scratch. Keep all utility functions (varint parsing, serial type decoding) in reusable form.

### Pitfall 2: Skipping Initial Analysis

**Problem**: Jumping straight to code without understanding the data structure leads to many wasted iterations.

**Solution**: Always complete Phase 1 (Initial Assessment) fully. Document observations about:
- Header presence/absence
- Page size and type
- Visible patterns in hex dump
- Estimated truncation point

### Pitfall 3: Not Validating Single Cell First

**Problem**: Processing all cells with buggy parsing logic produces incorrect output that's hard to debug.

**Solution**: Parse ONE cell with verbose output first (Phase 3, Step 3). Verify each field matches expectations before generalizing.

### Pitfall 4: Including Incomplete Records

**Problem**: Adding records with `null` values pollutes the output.

**Solution**: Only include records where ALL required fields are successfully recovered. Log partial recoveries separately for debugging.

### Pitfall 5: Cleaning Up Before Verification

**Problem**: Deleting scripts/debug output before fully verifying results makes later debugging impossible.

**Solution**: Keep all artifacts until final output is verified correct. Only clean up as a final step after confirmation.

### Pitfall 6: Syntax Errors from Rushed Coding

**Problem**: Basic syntax errors like `if48 <=` (missing space) or `12and` (missing space).

**Solution**: Write code carefully. Review before executing. Common mistakes:
- Missing spaces around operators
- Incomplete string concatenation
- Incorrect indentation

### Pitfall 7: Confusing Serial Type Encoding

**Problem**: Misinterpreting serial type codes leads to wrong data extraction.

**Key formulas**:
- TEXT length: `(serial_type - 13) // 2` (for odd values >= 13)
- BLOB length: `(serial_type - 12) // 2` (for even values >= 12)
- Type 1 = 8-bit int, Type 7 = 64-bit float

## Verification Strategies

### 1. Sanity Check Record Count

```python
# Cell count should match expected number of records
print(f"Expected records: (check task description)")
print(f"Cell pointers found: {len(cell_pointers)}")
print(f"Successfully recovered: {len(recovered_rows)}")
```

### 2. Check Value Patterns

```python
# Look for expected patterns in recovered data
words = [r['columns'][0] for r in recovered_rows]
values = [r['columns'][1] for r in recovered_rows]

print(f"Word pattern: {words[:3]} ... {words[-1]}")
print(f"Value range: {min(values)} to {max(values)}")
```

### 3. Validate JSON Output

```python
# Re-read and validate output file
with open('recover.json') as f:
    output = json.load(f)

print(f"Output records: {len(output)}")
for record in output[:3]:
    print(f"  {record}")

# Check for null values
null_count = sum(1 for r in output if None in r.values())
print(f"Records with null values: {null_count}")
```

## Bundled Resources

### scripts/sqlite_recovery.py

Utility functions for SQLite binary parsing:
- `read_varint(data, offset)` - Decode variable-length integers
- `decode_serial_type(serial_type, data, offset)` - Extract column values based on serial type
- `describe_serial_type(serial_type)` - Human-readable serial type description
- `hex_dump(data, offset, length)` - Format binary data for debugging

Execute the script directly to analyze a database file:
```bash
python scripts/sqlite_recovery.py database.db
```

### references/sqlite_format.md

Comprehensive reference for SQLite binary format including:
- Database header structure (100 bytes)
- Page types and their headers
- Varint encoding algorithm
- Serial type codes (0-11 and formula-based for text/blob)
- Cell structure for leaf table pages
- Common truncation patterns

**Grep patterns for quick lookup**:
- `"Serial Type"` - Find type code reference
- `"Varint"` - Variable-length integer encoding
- `"Page Header"` - Page structure details
- `"Truncation"` - Handling truncated data

## Decision Flowchart

```
Database recovery task
        │
        ▼
┌─────────────────────────┐
│ Phase 1: Initial        │
│ Assessment              │
│ - Check file size       │
│ - Try standard sqlite3  │
│ - Create hex dump       │
│ - Document observations │
└───────────┬─────────────┘
            │
            ▼
    Standard tools work?
       │         │
      YES        NO
       │         │
       ▼         ▼
  Use sqlite3   Manual parsing required
  directly             │
                       ▼
        ┌─────────────────────────┐
        │ Phase 3: Binary Parsing │
        │ Step 1: Identify pages  │
        │ Step 2: Extract cells   │
        │ Step 3: Parse ONE cell  │◄── CRITICAL
        │ Step 4: Validate        │
        │ Step 5: Generalize      │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │ Phase 4: Output         │
        │ - Only complete records │
        │ - Log partial/failed    │
        │ - Verify before cleanup │
        └─────────────────────────┘
```
