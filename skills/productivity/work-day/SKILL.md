---
name: work-day
description: Manages the SNMG18 Working Docs directory structure in Google Drive by verifying and creating month folders (YYYY-MM Work format) and day folders (YYYY-MM-DD format) for a specified date. Use when preparing folders for a specific work day, organizing documents by date, or ensuring the date-based folder structure is ready. Accepts dates in various formats or defaults to today.
---

# Work Day

## Overview

Ensure the SNMG18 Working Docs directory structure in Google Drive is properly organized with folders for a specified month and day, automatically creating any missing folders using the reverse-date naming convention with "Work" suffix for months (YYYY-MM Work for months, YYYY-MM-DD for days).

## Target Directory Structure
```
Google Drive Root
└── SNMG00 Management/
    └── SNMG18 Working Docs/
        └── YYYY-MM Work/     (e.g., 2025-10 Work for October 2025)
            └── YYYY-MM-DD/   (e.g., 2025-10-25 for October 25, 2025)
```

## Usage

When invoked, determine the target date:
- If user provides a date (e.g., "tomorrow", "October 30", "2025-11-15"), use that date
- If no date specified, use today's date

## Workflow

Execute these steps in order:

### Step 1: Determine Target Date

Convert the user's input (or today's date if not specified) to:
- Month format: YYYY-MM Work (e.g., 2025-10 Work)
- Day format: YYYY-MM-DD (e.g., 2025-10-25)

Use the reverse-date or reverse-month skills if needed for date conversion, then append " Work" to the month folder name.

### Step 2: Verify Parent Folders

Use **Claude's Google Drive search** (`google_drive_search`) to search for "SNMG00 Management" folder in Google Drive root:
- If not found, report error to user and stop
- If found, note the folder ID and proceed to next step

Use **Claude's Google Drive search** (`google_drive_search`) to search for "SNMG18 Working Docs" folder inside "SNMG00 Management":
- If not found, report error to user and stop
- If found, note the folder ID and proceed to next step

### Step 3: Check/Create Month Folder

Use **Claude's Google Drive search** (`google_drive_search`) to search for the month folder (YYYY-MM Work) inside "SNMG18 Working Docs":
- If found, report "Month folder exists", note the folder ID, and proceed
- If not found:
  - Use **Zapier Google Drive integration** (`Zapier:google_drive_create_folder`) to create the folder with name in YYYY-MM Work format
  - Report "Month folder created"
  - Note the new folder ID and proceed

### Step 4: Check/Create Day Folder

Use **Claude's Google Drive search** (`google_drive_search`) to search for the day folder (YYYY-MM-DD) inside the month folder:
- If found, report "Day folder exists"
- If not found:
  - Use **Zapier Google Drive integration** (`Zapier:google_drive_create_folder`) to create the folder with name in YYYY-MM-DD format inside the month folder
  - Report "Day folder created"

### Step 5: Report Status

Provide a summary:
- The target date being prepared
- Status of each folder (existed or created)
- Google Drive link to the target date's folder
- Confirmation that the structure is ready

## Tool Usage Notes

**For searching folders**: Use Claude's native Google Drive integration
- `google_drive_search` - to find existing folders
- Query format: Search by folder name within parent folders

**For creating folders**: Use Zapier's Google Drive integration
- `Zapier:google_drive_create_folder` - to create new folders
- Provide: folder name and parent folder ID

## Example Usage

**User request**: "Prepare folders for work day"
→ Use today's date (e.g., creates "2025-10 Work/2025-10-25")

**User request**: "Set up folders for tomorrow"
→ Use tomorrow's date (e.g., creates "2025-10 Work/2025-10-26")

**User request**: "Prepare work day for October 30"
→ Use October 30 of current year (creates "2025-10 Work/2025-10-30")

**User request**: "Set up 2025-11-15"
→ Use November 15, 2025 (creates "2025-11 Work/2025-11-15")

## Date Format Reference

- **Month folder**: YYYY-MM Work (e.g., 2025-10 Work, 2025-11 Work, 2026-01 Work)
- **Day folder**: YYYY-MM-DD (e.g., 2025-10-25, 2025-11-03, 2026-01-15)

The month format includes " Work" suffix to clearly identify these as work-related directories. Day folders use standard ISO 8601 format to ensure proper chronological sorting.

## Error Handling

If "SNMG00 Management" or "SNMG18 Working Docs" folders don't exist, stop execution and inform the user that the parent folders must be created first before using this skill.