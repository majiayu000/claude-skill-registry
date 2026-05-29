---
name: managing-imports
description: Organize incoming files and track import status through the file staging workflow
---

# Managing Imports

## Overview

Manage import file workflow from drop to archive: organize files, check duplicates, track status, and clear processed files.

**Use when:** Processing new import files, checking import status, or archiving successfully imported data.

**Announce at start:** "I'm using the managing-imports skill to [operation]."

## What This Skill Does

Wraps the file staging system (`scripts/utilities/file_staging/`) with user-friendly operations:
1. **Stage files** - Classify and organize files from inbox
2. **Check duplicates** - Query import_manifest for SHA256 matches
3. **Track status** - Show files in each workflow stage
4. **Clear processed** - Move imported files to archive

## Operations

### Stage Files

**When:** New files dropped in inbox, need to classify and organize for import.

**Process:**

1. **Verify inbox has files**
   ```bash
   cd /Users/anthonybyrnes/PycharmProjects/Python419
   find imports/inbox -type f | wc -l
   ```

   If 0 files, report: "Inbox is empty. No files to stage."

2. **Run file staging orchestrator**
   ```bash
   cd /Users/anthonybyrnes/PycharmProjects/Python419
   PYTHONPATH=. python3 -m scripts.utilities.file_staging \
     --drop-folder imports/inbox \
     --use-db \
     --generate-plan
   ```

   **What this does:**
   - Scans inbox for files
   - Classifies file type (LBHRA, PS_LB, LBSR08E, 419F, PROGRAM_LIST, COTA_PERSISTENCE)
   - Detects academic term from file content
   - Checks SHA256 against import_manifest for duplicates
   - Moves to `imports/staged/{type}/`
   - Generates staging manifest JSON
   - Creates import plan script (if --generate-plan)

3. **Parse orchestrator output**

   Look for:
   - Files processed count
   - Files staged count
   - Files skipped (duplicates)
   - Staging manifest path
   - Import plan path (if generated)

4. **Report results**

   Format:
   ```
   Staging Complete:
   - Processed: 15 files
   - Staged: 12 files (ready for import)
   - Skipped: 3 files (duplicates)

   Staged files by type:
   - LBHRA: 5 files → imports/staged/lbhra/
   - PS_LB: 4 files → imports/staged/ps-lb/
   - 419F: 3 files → imports/staged/419f/

   Manifest: imports/staged/staging-manifest-YYYY-MM-DD-HHMMSS.json
   Import plan: imports/staged/import-plan-YYYY-MM-DD-HHMMSS.sh
   ```

**Error Handling:**

- If orchestrator fails, show error and recommend manual classification
- If --use-db fails, warn that duplicates weren't checked
- If staging folder doesn't exist, create it first

---

### Check Duplicates

**When:** Want to verify if files have already been imported before staging.

**Process:**

1. **Get file path or directory**

   User provides:
   - Single file path
   - Directory path (checks all files in directory)

2. **Calculate SHA256 hashes**

   For each file:
   ```bash
   shasum -a 256 <file_path>
   ```

3. **Query import_manifest**

   ```python
   import psycopg2
   from dotenv import load_dotenv
   import os

   load_dotenv()
   conn = psycopg2.connect(
       host=os.getenv('DB_HOST'),
       dbname=os.getenv('DB_NAME'),
       user=os.getenv('DB_USER'),
       password=os.getenv('DB_PASSWORD')
   )

   cursor = conn.cursor()
   cursor.execute("""
       SELECT
           original_path,
           file_type,
           term_code,
           imported_at
       FROM import_manifest
       WHERE file_hash = %s
   """, (file_hash,))

   result = cursor.fetchone()
   ```

4. **Report duplicates**

   For each duplicate found:
   ```
   DUPLICATE: filename.txt
   - SHA256: abc123...
   - Previously imported: 2025-11-10 14:32:15
   - Original path: imports/archive/lbhra/2024-fall/filename.txt
   - File type: LBHRA
   - Term: 2024-fall
   - Action: SKIP (already in database)
   ```

   For non-duplicates:
   ```
   NEW: filename.txt
   - SHA256: def456...
   - Not found in import_manifest
   - Action: READY FOR IMPORT
   ```

**SQL Helper:**

```sql
-- Check multiple files at once
SELECT
    file_hash,
    original_path,
    file_type,
    term_code,
    imported_at
FROM import_manifest
WHERE file_hash IN ('hash1', 'hash2', 'hash3')
ORDER BY imported_at DESC;
```

---

### Track Status

**When:** Need overview of import workflow stages, checking what's queued for import.

**Process:**

1. **Count files in each stage**

   ```bash
   cd /Users/anthonybyrnes/PycharmProjects/Python419

   # Inbox
   INBOX=$(find imports/inbox -type f 2>/dev/null | wc -l | tr -d ' ')

   # Staged by type
   LBHRA=$(find imports/staged/lbhra -type f 2>/dev/null | wc -l | tr -d ' ')
   PS_LB=$(find imports/staged/ps-lb -type f 2>/dev/null | wc -l | tr -d ' ')
   LBSR08E=$(find imports/staged/lbsr08e -type f 2>/dev/null | wc -l | tr -d ' ')
   F419=$(find imports/staged/419f -type f 2>/dev/null | wc -l | tr -d ' ')
   PROGRAM=$(find imports/staged/program-list -type f 2>/dev/null | wc -l | tr -d ' ')
   COTA=$(find imports/staged/cota-persistence -type f 2>/dev/null | wc -l | tr -d ' ')

   # Processing
   PROCESSING=$(find imports/processing -type f 2>/dev/null | wc -l | tr -d ' ')

   # Archive (total)
   ARCHIVE=$(find imports/archive -type f 2>/dev/null | wc -l | tr -d ' ')
   ```

2. **Detect terms for staged files**

   For each type with staged files, group by term:
   ```bash
   # Example: LBHRA files by term
   for file in imports/staged/lbhra/*.txt; do
       # Run term detector
       TERM=$(PYTHONPATH=. python3 -c "
   from scripts.utilities.file_staging.term_detector import detect_term
   result = detect_term('$file')
   print(result.get('term_code', 'unknown'))
       ")
       echo "$file -> $TERM"
   done
   ```

   Count by term for display.

3. **Format output**

   ```
   Import Status:

   Inbox: 0 files

   Staged: 13 files ready for import
     - LBHRA (5 files):
       - 2024-fall: 2 files
       - 2025-spring: 3 files
     - PS_LB (4 files):
       - 2024-fall: 1 file
       - 2025-spring: 3 files
     - 419F (3 files):
       - 2025-spring: 3 files
     - LBSR08E (0 files)
     - Program List (0 files)
     - COTA Persistence (1 file):
       - 2024-fall: 1 file

   Processing: 0 files

   Archive: 1,247 files across 6 types
   ```

4. **Show recent imports from manifest**

   ```sql
   SELECT
       file_type,
       term_code,
       COUNT(*) as file_count,
       MAX(imported_at) as last_import
   FROM import_manifest
   GROUP BY file_type, term_code
   ORDER BY last_import DESC
   LIMIT 10;
   ```

   Display as:
   ```
   Recent Imports (from manifest):
   - LBHRA 2025-spring: 3 files (last: 2025-11-13 10:45:22)
   - PS_LB 2025-spring: 3 files (last: 2025-11-13 10:47:15)
   - 419F 2024-fall: 5 files (last: 2025-11-12 16:23:01)
   ```

**Error Handling:**

- If directories don't exist, show "0 files" (not errors)
- If database unavailable, show file counts only (skip manifest query)
- If term detection fails for a file, mark as "term: unknown"

---

### Clear Processed

**When:** Import succeeded, files verified in database, ready to move to archive.

**Process:**

1. **Verify files are in manifest**

   ```sql
   SELECT
       file_hash,
       original_path,
       file_type,
       term_code
   FROM import_manifest
   WHERE original_path LIKE '%staged%'
   ORDER BY imported_at DESC;
   ```

   These are successfully imported files still in staging.

2. **Determine archive destination**

   For each file:
   - File type: `LBHRA`, `PS_LB`, etc.
   - Term code: `2024-fall`, `2025-spring`, etc.
   - Archive path: `imports/archive/{type}/{term}/`

   Example:
   - File: `imports/staged/lbhra/LBHRA_Report_Fall2024.txt`
   - Type: `lbhra`
   - Term: `2024-fall`
   - Destination: `imports/archive/lbhra/2024-fall/`

3. **Create archive directories if needed**

   ```bash
   mkdir -p imports/archive/{type}/{term}
   ```

4. **Move files**

   ```bash
   mv imports/staged/{type}/{filename} imports/archive/{type}/{term}/
   ```

5. **Update manifest (optional)**

   If tracking archive paths:
   ```sql
   UPDATE import_manifest
   SET original_path = %s
   WHERE file_hash = %s;
   ```

6. **Report results**

   ```
   Cleared Processed Files:

   Moved to archive:
   - LBHRA (5 files):
     - 2024-fall: 2 files → imports/archive/lbhra/2024-fall/
     - 2025-spring: 3 files → imports/archive/lbhra/2025-spring/
   - PS_LB (4 files):
     - 2025-spring: 4 files → imports/archive/ps-lb/2025-spring/

   Total: 9 files archived

   Remaining staged: 4 files
   ```

**Safety Checks:**

- NEVER move files not in manifest (risk of losing unimported data)
- Verify SHA256 matches before moving
- Confirm database has imported records (check record counts)
- Keep staging files until import verified complete

**Error Handling:**

- If manifest query fails, ABORT (don't move files)
- If term unknown, archive to `imports/archive/{type}/unknown-term/`
- If move fails, log error but continue with other files
- Report any failed moves separately

---

## Integration

**Wraps:**
- File staging system: `scripts/utilities/file_staging/orchestrator.py`
- Term detector: `scripts/utilities/file_staging/term_detector.py`
- Duplicate checker: `scripts/utilities/file_staging/duplicate_checker.py`

**Database:**
- Table: `import_manifest` (SHA256 tracking)
- Connection: Uses `.env` credentials

**Used by:**
- `project-status` skill (shows import queue)
- Import workflows (pre-import organization)

**Depends on:**
- `/imports/` directory structure
- File staging system installed
- Database connection available (for duplicates)

## Implementation Details

**File Type Patterns:**

```python
FILE_TYPE_PATTERNS = {
    'LBHRA': r'LBHRA.*\.txt$',
    'PS_LB': r'PS_LB.*\.txt$',
    'LBSR08E': r'LBSR08E.*\.txt$',
    '419F': r'419F.*\.txt$',
    'PROGRAM_LIST': r'(?i)program.*list.*\.xlsx?$',
    'COTA_PERSISTENCE': r'(?i)(ta|ga|isa).*\.txt$',
}
```

**Term Code Mapping:**

```python
TERM_CODES = {
    'fall': 'YYYY-fall',
    'spring': 'YYYY-spring',
    'summer': 'YYYY-summer',
    'winter': 'YYYY-winter',
}
```

**Database Schema:**

```sql
CREATE TABLE import_manifest (
    id SERIAL PRIMARY KEY,
    file_hash VARCHAR(64) UNIQUE NOT NULL,
    original_path TEXT NOT NULL,
    file_type VARCHAR(50),
    term_code VARCHAR(20),
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size BIGINT,
    record_count INTEGER
);
```

## Usage Examples

### Example 1: Stage New Files

**User:** "I have new import files in the inbox. Can you stage them?"

**Assistant:** "I'm using the managing-imports skill to stage files from inbox."

[Runs staging operation]

**Output:**
```
Staging Complete:
- Processed: 8 files
- Staged: 8 files (ready for import)
- Skipped: 0 files (no duplicates)

Staged files by type:
- LBHRA: 3 files → imports/staged/lbhra/
- PS_LB: 3 files → imports/staged/ps-lb/
- 419F: 2 files → imports/staged/419f/

Manifest: imports/staged/staging-manifest-2025-11-14-143022.json
Import plan: imports/staged/import-plan-2025-11-14-143022.sh

Next step: Review import plan and execute imports.
```

### Example 2: Check Import Status

**User:** "What's in the import queue?"

**Assistant:** "I'm using the managing-imports skill to track import status."

[Runs track status operation]

**Output:**
```
Import Status:

Inbox: 0 files

Staged: 8 files ready for import
  - LBHRA (3 files):
    - 2025-spring: 3 files
  - PS_LB (3 files):
    - 2025-spring: 3 files
  - 419F (2 files):
    - 2025-spring: 2 files

Processing: 0 files

Archive: 1,255 files across 6 types

Recent Imports (from manifest):
- PS_LB 2025-spring: 3 files (last: 2025-11-14 10:15:33)
- LBHRA 2025-spring: 3 files (last: 2025-11-14 10:12:45)
- 419F 2024-fall: 5 files (last: 2025-11-13 15:22:11)
```

### Example 3: Check for Duplicates

**User:** "Check if these files are duplicates before I import them."

**Assistant:** "I'm using the managing-imports skill to check for duplicates."

[Runs duplicate check on inbox]

**Output:**
```
Duplicate Check Results:

DUPLICATE: LBHRA_Spring2025_v2.txt
- SHA256: abc123def456...
- Previously imported: 2025-11-10 14:32:15
- Original path: imports/archive/lbhra/2025-spring/LBHRA_Spring2025.txt
- File type: LBHRA
- Term: 2025-spring
- Action: SKIP (already in database)

NEW: PS_LB_Spring2025_Updated.txt
- SHA256: 789xyz012abc...
- Not found in import_manifest
- Action: READY FOR IMPORT

Summary:
- Duplicates: 1 file (skip)
- New files: 1 file (ready to import)
```

### Example 4: Archive Processed Files

**User:** "Import completed successfully. Archive the processed files."

**Assistant:** "I'm using the managing-imports skill to clear processed files."

[Runs clear processed operation]

**Output:**
```
Cleared Processed Files:

Moved to archive:
- LBHRA (3 files):
  - 2025-spring: 3 files → imports/archive/lbhra/2025-spring/
- PS_LB (3 files):
  - 2025-spring: 3 files → imports/archive/ps-lb/2025-spring/
- 419F (2 files):
  - 2025-spring: 2 files → imports/archive/419f/2025-spring/

Total: 8 files archived

Remaining staged: 0 files

All staged files have been archived.
```

## Common Mistakes

**Staging without database connection:**
- **Problem:** Can't check duplicates, might re-import files
- **Fix:** Always use `--use-db` flag when staging

**Moving files before import verified:**
- **Problem:** Lose track of files if import fails
- **Fix:** Only clear processed after verifying database records

**Not detecting terms correctly:**
- **Problem:** Files archived to wrong term directory
- **Fix:** Verify term detection output, use term detector directly if needed

**Archiving files not in manifest:**
- **Problem:** Risk losing unimported data
- **Fix:** Always check manifest first, never move untracked files

## Red Flags

**Never:**
- Stage files without checking duplicates (use --use-db)
- Move files from staging without manifest verification
- Delete files from inbox (move to staged instead)
- Archive files before import completes
- Skip error handling (always check command exit codes)

**Always:**
- Verify database connection before duplicate checks
- Create archive directories before moving files
- Log all file operations (staging manifest tracks this)
- Report counts after each operation (files processed, staged, skipped)
- Keep import plan scripts for audit trail

## Workflow Summary

```
1. New files arrive
   ↓
   Drop in: /imports/inbox/

2. Stage files (this skill)
   ↓
   Run: managing-imports → stage files
   ↓
   Result: /imports/staged/{type}/

3. Execute imports (external scripts)
   ↓
   Run: Import plan scripts
   ↓
   Update: import_manifest table

4. Clear processed (this skill)
   ↓
   Run: managing-imports → clear processed
   ↓
   Result: /imports/archive/{type}/{term}/
```

**Complete Lifecycle:**

```
inbox → staged → processing → archive
         ↑
         └─ duplicates skipped (from import_manifest check)
```
