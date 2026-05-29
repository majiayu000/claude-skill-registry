---
name: workspace-file-discovery-manager
description: When the user needs to search for specific files in a workspace based on content patterns, assignment names, or file types, especially when filenames are unknown. This skill triggers when users mention 'files saved somewhere in workspace' or 'can't remember filenames'. It performs directory exploration, content-based file matching, and organizes found files by relevance to specific assignments or document types.
---
# Instructions

## Primary Objective
Help users locate and manage files in their workspace when they cannot remember exact filenames, particularly for academic assignments, documents, or specific content types.

## Core Workflow

### 1. Initial Setup & Context Gathering
- **Access User Memory**: Retrieve the user's personal information (name, ID, email, courses) using `memory-read_graph`.
- **Identify Workspace**: Use `filesystem-list_allowed_directories` to locate the accessible workspace root.
- **Explore Directory Structure**: Use `filesystem-directory_tree` to map the entire workspace contents.

### 2. File Discovery & Matching
- **Content-Based Search**: When users describe file content (e.g., "assignment about cinematography"), search through file contents using `filesystem-read_multiple_files` on likely candidates.
- **Pattern Matching**: Look for files with names containing keywords from assignment descriptions, course codes, or user identifiers.
- **Grade/Submission Analysis**: If a grade summary or submission record exists (e.g., Excel files), analyze it with `local-python-execute` (pandas) to identify missing submissions.

### 3. File Preparation & Submission
- **Rename Files to Requirements**: Check assignment descriptions for specific naming conventions (e.g., `StudentID_Course_AssignmentX.md`). Create correctly named copies using `filesystem-write_file`.
- **Submit to LMS**: Use Canvas tools (`canvas-canvas_submit_assignment_with_file`) to submit files for identified missing assignments.
- **Handle Excused Assignments**: Do not submit assignments that are officially excused (user will provide context). Instead, assist with notifying instructors/TAs.

### 4. Notification & Documentation
- **Locate Supporting Documents**: Find relevant documents (leave applications, certificates, etc.) in the workspace.
- **Communicate with Instructors**: Use `emails-send_email` to notify TAs/instructors about excused assignments or provide documentation, attaching relevant files.

## Key Decision Points
- **Only Submit Missing Work**: Cross-reference grade sheets with submission statuses. Only submit assignments marked as "Not Submitted" that are not excused.
- **Preserve Original Files**: Do not modify or delete original workspace files. Create renamed copies in the workspace root for submission.
- **No Content Creation**: Never generate assignment content. Only submit files that already exist in the workspace.
- **Verify File Types**: Ensure submitted files match allowed extensions specified in assignment details.

## Error Handling
- If no matching files are found for a described assignment, inform the user and do not submit anything.
- If grade sheets cannot be parsed, attempt to infer submission status from Canvas API directly.
- If email sending fails, save the composed message and attachment paths for the user to send manually.

## Bundled Resources
- Use `scripts/analyze_grade_sheet.py` for robust Excel/CSV grade sheet parsing.
- Refer to `references/file_matching_patterns.md` for common academic file naming conventions.
