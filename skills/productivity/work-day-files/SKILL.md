---
name: work-day-files
description: Lists files contained in a work-day folder while delegating formatting to the list-files skill. Uses the work-day skill to locate the appropriate folder structure (YYYY-MM Work/YYYY-MM-DD) in Google Drive, then passes the target folder to list-files for table generation. Accepts dates in various formats and automatically detects the correct folder level.
---

# Work Day Files

## Overview

Retrieve and summarize all files stored in a specific work-day folder within the SNMG18 Working Docs directory structure. This skill leverages the work-day skill to navigate the proper folder hierarchy and delegates presentation entirely to the list-files skill, ensuring consistent catalog formatting.

## Target Directory Structure

```
Google Drive Root
└── SNMG00 Management/
    └── SNMG18 Working Docs/
        └── YYYY-MM Work/     (e.g., 2025-10 Work for October 2025)
            └── YYYY-MM-DD/   (e.g., 2025-10-25 for October 25, 2025)
                └── [FILES]   ← Files are listed and summarized from here
```

## Usage

- Accept a date parameter if provided; otherwise default to today.
- Parse relative terms ("today", "next Monday"), natural language dates ("October 30"), ISO strings ("2025-11-15"), or other common formats, then normalize to **YYYY-MM-DD**.
- Translate the normalized date into the folder names `YYYY-MM Work` (month) and `YYYY-MM-DD` (day).

## Workflow

1. **Determine the target date.** Convert the user's input—or today's date if omitted—to ISO format. Reject only unparseable strings.
2. **Walk the folder hierarchy with `google_drive_search`.**
   - Locate `SNMG00 Management` at the Drive root, then `SNMG18 Working Docs` beneath it.
   - Inside `SNMG18 Working Docs`, find the month folder (`YYYY-MM Work`).
   - Within the month folder, find the day folder (`YYYY-MM-DD`).
   - Report an error and stop at the first missing level.
3. **List files from the day folder.** If the folder is empty, respond "No files found in this work-day folder". Otherwise, pass the folder ID to `list-files` with its default formatting (non-recursive scope, detailed summaries, modifiedTime desc) unless the user requests overrides.

Embed the Markdown table returned by `list-files` directly in the response—no extra prose or reformatting.

## Tool Usage Notes

- Use `google_drive_search` for every folder lookup and to confirm the day folder's contents.
- Call `list-files` for the final table; adjust its parameters only when the requester specifies different limits, sorting, or filters.
- Fetch file contents with `google_drive_fetch` or `web_fetch` only if the user asks for document details.

## Example Usage

Requests such as "today," "October 30," or "2025-11-15" all follow the same pattern: parse the date, navigate to `SNMG18 Working Docs/YYYY-MM Work/YYYY-MM-DD/`, and return the `list-files` table for that folder.

## Error Handling

**Missing parent folders**: If "SNMG00 Management" or "SNMG18 Working Docs" folders don't exist, report error and stop.

**Missing work month folder**: If the YYYY-MM Work folder doesn't exist for the requested date, report that no work folders exist for that month.

**Missing work day folder**: If the YYYY-MM-DD folder doesn't exist for the requested date, report that no folder exists for that specific day.

**Empty folder**: If the day folder exists but contains no files, report that no files are present.

**File access issues**: If a file cannot be accessed or summarized, note the filename and indicate that the summary could not be generated due to access restrictions or file type limitations.

## Alignment with `list-files`

- Allow `list-files` to handle all summarization and metadata enrichment.
- Do not manually rewrite or extend the table output after `list-files` responds.
- If the caller needs adjustments (different limit, sort, or filters), reinvoke `list-files` with updated parameters instead of editing the table manually.

## Dependencies

This skill depends on:
- **work-day skill**: For understanding folder structure (reference only, not called directly)
- **Google Drive integration**: For searching and accessing files
- **Date parsing**: For converting user input to ISO format
