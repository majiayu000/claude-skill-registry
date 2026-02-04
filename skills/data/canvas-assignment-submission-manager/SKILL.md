---
name: canvas-assignment-submission-manager
description: Manages assignment submissions on Canvas LMS. Identifies missing submissions from grade records, prepares files with proper naming conventions, and submits assignments. Handles course identification, assignment listing, submission status checking, file preparation, and automated submission.
---
# Instructions

## Primary Objective
Help a forgetful student identify and submit missing Canvas assignments based on a published grade summary, while respecting excused absences.

## Core Workflow

### 1. Initialization & Context Gathering
- **Read User Memory**: Use `memory-read_graph` to retrieve the student's personal information (Student ID, Email, Name).
- **Identify Target Course**: Use `canvas-canvas_list_courses` to list all courses. The target course is typically identifiable by name (e.g., "Cinema Culture Appreciation") or code (e.g., "FILM101") mentioned in the user request or grade sheet.
- **Explore Workspace**: Use `filesystem-list_allowed_directories` and `filesystem-directory_tree` to understand the file structure, locating the grade summary file and potential assignment directories.

### 2. Analyze Submission Status
- **Locate Grade Summary**: Find the Excel file (e.g., `Cinema_Culture_Grade_Summary.xlsx`) in the workspace. Use `local-python-execute` with pandas to read it.
- **Parse Grade Data**: Identify the row for the current student (matching Student ID or Name). Extract the status for each assignment ("Not Submitted", a score, or "Excused").
- **Cross-reference with Canvas**: Use `canvas-canvas_list_assignments` for the target course with `include_submissions: true`. This returns the official list of assignments and the user's current submission status (`workflow_state`).
- **Determine Actionable Items**: Compare the grade sheet "Not Submitted" status with Canvas's `workflow_state`. Only submit assignments that are **both** marked as missing on the grade sheet **and** have `workflow_state: "unsubmitted"` in Canvas. Respect any user-stated excusals (e.g., "officially excused from Assignment 2").

### 3. Prepare and Submit Assignments
- **Find Assignment Files**: Search the workspace directory tree (e.g., `homeworks/mine/`) for files whose content matches the assignment descriptions. Use `filesystem-read_multiple_files` to inspect likely candidates.
- **Enforce Naming Conventions**: Check each assignment's `description` field for specific file naming requirements (e.g., `StudentID_FILM101_Assignment4.md`). If required, create a new file with the correct name using `filesystem-write_file`, copying the content from the found assignment file.
- **Submit Assignments**: For each missing assignment, use `canvas-canvas_submit_assignment_with_file` with the `course_id`, `assignment_id`, and the path to the correctly named file.

### 4. Handle Administrative Tasks
- **Locate Supporting Documents**: Find any referenced documents (e.g., "Leave Application.pdf") in the workspace using the directory tree.
- **Communicate with Instructors**: If instructed, send an email to the relevant TA or instructor (email often found in the grade summary) using `emails-send_email`. Attach the supporting document and clearly state the student's request (e.g., reminder about an excused absence).

## Critical Rules & Guardrails
- **No Content Creation**: Only submit assignment files that already exist in the workspace. Do not generate new answer content.
- **Selective Submission**: Only submit assignments identified as missing. Do not re-submit assignments that already have a score or submission.
- **Data-Driven Decisions**: Base all decisions on data from the official grade sheet and Canvas API, not assumptions.
- **Preserve User Info**: Use the Student ID, Name, and Email from memory for file naming and communication.

## Error Handling
- If the grade sheet cannot be parsed, inform the user and halt.
- If an assignment file cannot be found, do not submit anything for that assignment. Inform the user.
- If a Canvas API call fails (e.g., course not found), report the error and stop.

## Final Step
Provide the user with a clear summary of actions taken: which assignments were identified as missing, which were submitted, and any administrative communications sent.
