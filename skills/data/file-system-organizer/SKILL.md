---
name: file-system-organizer
description: Organizes or restructures files and directories according to a specified hierarchy or categorization scheme. Analyzes existing structures, creates new directory trees, intelligently moves files based on content and naming patterns, and verifies the final organization.
---
# Instructions

## Objective
Reorganize the user's file system from a messy or unspecified state into a clean, logical directory structure as specified by the user.

## Core Workflow

### 1. Analyze the Current State
*   **Action:** Use `filesystem-list_directory` to explore the target workspace.
*   **Goal:** Understand the existing folder layout and identify all files that need to be categorized. Start from the root path the user indicates (e.g., `/workspace`). Recursively list subdirectories to build a complete mental map.

### 2. Parse the Target Structure
*   **Action:** Interpret the user's request, which may include a text-based tree diagram or a verbal description.
*   **Goal:** Build a clear, hierarchical model of the desired final directory structure (e.g., `School/Courses_Materials`, `Work/Projects`).

### 3. Create the Directory Hierarchy
*   **Action:** Use `filesystem-create_directory` to build the new structure.
*   **Critical Logic:** Create directories **sequentially from the root down**. Do not attempt to create a nested subdirectory (`A/B/C`) before its parent (`A/B`) exists. The trajectory shows that attempting this in parallel causes "Parent directory does not exist" errors.
*   **Best Practice:** Create all top-level directories first, then their immediate children, proceeding layer by layer.

### 4. Categorize and Move Files
*   **Action:** Use `filesystem-move_file` to relocate files from their original locations to their new, categorized homes.
*   **Intelligence Required:** Determine the correct destination for each file by analyzing:
    *   **File Name:** Keywords like `Course`, `Graduation`, `Exam`, `Project`, `Application`, `CV`, `Movie`, `Music`, `Picture`.
    *   **File Extension:** `.mp3`, `.mp4`, `.mkv` → Entertainment; `.pdf`, `.doc`, `.ppt`, `.xlsx` → likely School or Work.
    *   **Current Location:** A file inside an existing `Entertainment` folder is likely media.
    *   **Content Inference:** `cat.png` is a picture, likely of a pet.
*   **Procedure:** Move files in batches. Verify each move operation is successful before proceeding.

### 5. Cleanup and Verification
*   **Action:**
    1.  Use `filesystem-directory_tree` to generate a visual map of the newly organized workspace.
    2.  Present this tree to the user for confirmation.
    3.  If original source directories are now empty, remove them using `terminal-run_command` (e.g., `rm -rf /path/to/empty_folder`).
*   **Goal:** Leave the workspace tidy and provide clear evidence of the completed task.

## Key Principles
*   **Defensive Creation:** Always check for or assume parent directories need to be created first.
*   **Informed Moving:** Use multiple signals (name, extension, path) to make accurate categorization decisions.
*   **Verification:** Always show the end result. Do not assume success without checking.
