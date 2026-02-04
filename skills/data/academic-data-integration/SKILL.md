---
name: academic-data-integration
description: When the user needs to integrate multiple data sources (Canvas API, user memory, file systems) to create comprehensive academic reports. This skill combines course information, assignment details, submission status, and user context to generate actionable insights. Triggers include requests that involve cross-referencing multiple data sources or creating consolidated academic reports from disparate systems.
---
# Instructions

## Objective
Integrate data from Canvas LMS, user memory, and local workspace files to identify and report on unsubmitted academic work. The primary output is formatted CSV files containing sorted lists of pending quizzes and assignments.

## Core Workflow

### 1. Initial Data Gathering
- **Read User Memory**: Use `memory-read_graph` to retrieve the user's personal information. Pay special attention to academic exemptions (e.g., English entrance exam score).
- **Fetch Course List**: Use `canvas-canvas_list_courses` to get all enrolled courses. Note the `course_code` and `name` for each.

### 2. Understand Output Format
- **Inspect Workspace**: Use `local-python-execute` to list files in `/workspace/dumps/workspace/` and examine any existing CSV files (e.g., `quiz_info.csv`, `assignment_info.csv`).
- **Analyze Headers**: Note the required CSV columns and data format from the example rows.

### 3. Collect Pending Work Details
- **Fetch Assignments & Quizzes**: For each course ID obtained in step 1, call:
    - `canvas-canvas_list_assignments` with `include_submissions: true`.
    - `canvas-canvas_list_quizzes`.
- **Identify Unsubmitted Items**:
    - **Assignments**: An item is "unsubmitted" if `submission.workflow_state` is `"unsubmitted"` AND `is_quiz_assignment` is `false`.
    - **Quizzes**: A quiz is "required" if its `quiz_type` is `"assignment"` (graded). Ignore `"practice_quiz"` types.
    - **Apply Exemptions**: Cross-reference user memory with course announcements. For example, if a user's English entrance score is ≥90 and a course announcement grants an exemption, exclude that quiz.

### 4. Enrich Data & Sort
- **Fetch Course Details**: Optionally use `canvas-canvas_get_course` for each course if additional metadata (like credits) is needed but not in the initial list.
- **Determine Credits**: If credit information is unavailable via API, infer it logically (e.g., 101/201/301-level = 3 credits, 401-level = 4 credits) based on the `course_code`.
- **Clean Data**: Remove the `-x` suffix (e.g., `-1`) from `course_code` and `course_name`.
- **Sort Final Lists**:
    1. **Primary Key**: Deadline (`due_at`) in chronological order.
    2. **Secondary Key**: Course code in dictionary (alphabetical) order for items with identical deadlines.

### 5. Generate Output Files
- **Write CSVs**: Use `local-python-execute` to run a Python script that:
    1. Creates the sorted lists of quizzes and assignments.
    2. Writes to the existing CSV file paths in the workspace **without changing the filenames**.
    3. Formats data exactly as the example headers specify.
- **Verify**: Read and print the final CSV contents to confirm correct formatting and sorting.

## Key Decision Points
- **Inclusion/Exclusion Logic**: Document why specific items were included or excluded (e.g., "exempt due to high English score", "practice quiz not graded").
- **Data Fallbacks**: When API data is missing (e.g., credits), use reasoned defaults and note the assumption.
- **Sorting Validation**: Double-check that sorting by deadline then course code is correctly implemented.

## Final Output
The skill is complete when:
1. The `quiz_info.csv` and `assignment_info.csv` files in the workspace are updated with the current, sorted list of unsubmitted work.
2. A clear summary is provided explaining what was found and any logical decisions made.
