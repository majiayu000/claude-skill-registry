---
name: repository-todo-tracker
description: Scans a GitHub repository for TODO/FIXME comments in source code files and updates documentation (like README) with a comprehensive, organized list. Handles authentication, recursive file search, comment extraction, comparison with existing documentation, and markdown updates while preserving formatting.
---
# Instructions

## Core Objective
When the user requests to scan a repository for TODOs and update documentation, you must:
1.  Authenticate with GitHub.
2.  Find all relevant source files in the specified branch.
3.  Extract all TODO/FIXME comments.
4.  Compare with the existing TODO list in the documentation.
5.  Update the documentation by removing completed items and adding new ones, maintaining the specified format and order.

## Step-by-Step Process

### 1. Clarify & Parse User Request
-   **Identify Target Repository:** Extract the repo name and owner from the user's request. If the owner is "my" or "our", you will need to discover the authenticated user's repositories.
-   **Identify Target Branch:** Extract the branch name (e.g., `dev`, `main`). Default to `main` if unspecified.
-   **Identify Target Documentation File:** Usually `README.md`. Confirm with the user if ambiguous.
-   **Identify File Types:** The request typically specifies file extensions (e.g., `.py`). Use these. If unspecified, default to common source files (`.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`).
-   **Identify Section Title:** The request often specifies a section title to update (e.g., `### 📝 Complete TODO List`). You **MUST** keep this exact title unchanged.

### 2. Authenticate and Discover Repository
-   Check for a GitHub token, typically in a file like `.github_token` in the workspace.
-   Use the token to call the GitHub API (`github-get_me`, `github-search_repositories`, or direct API calls via `local-python-execute` with `requests`).
-   If the repository owner is ambiguous (e.g., "my repo"), list the authenticated user's repositories to find the correct one.

### 3. Fetch Repository Structure & Target Files
-   Get the recursive file tree for the target branch using the GitHub API.
-   Filter the tree to identify:
    -   All source files matching the specified extensions.
    -   The target documentation file (e.g., `README.md`).
-   Fetch and save the current content of the documentation file. Note its `sha` for later updates.

### 4. Extract TODO Comments from Source Code
-   For each identified source file, fetch its content via the GitHub API.
-   Use a regular expression (e.g., `r'#\\s*TODO[:\\s]*(.*)'`, case-insensitive) to scan each line for TODO comments.
-   For each match, record:
    -   `file`: The repository-relative file path.
    -   `line`: The line number.
    -   `text`: The TODO description (trimmed).
-   Save this list as a JSON file in the workspace for later comparison. **Sort the list lexicographically by file path, then by line number within the same file.**

### 5. Parse the Existing TODO List from Documentation
-   Locate the target section in the documentation using the specified title (e.g., `### 📝 Complete TODO List`).
-   Parse each TODO item. They are typically in the format:
    `- [ ] **<file_path>:<line_number>** - <description>`
-   Create a mapping keyed by `"<file_path>:<line_number>"` for easy comparison.

### 6. Generate the Updated TODO List
-   **Identify Completed TODOs:** Items present in the documentation mapping but **not** in the newly extracted code list. These should be removed.
-   **Identify New TODOs:** Items present in the new code list but **not** in the documentation mapping. These should be added.
-   Generate the new, complete TODO list section content:
    1.  Start with the exact, original section title.
    2.  For each item in the **sorted** extracted code list, add a line in the format: `- [ ] **<file>:<line>** - <text>`

### 7. Update the Documentation File
-   In the documentation content, replace the entire old TODO section (from the title to the beginning of the next major section or end of file) with the newly generated content.
-   Use the GitHub API to update the file. You **must** provide:
    -   The commit `message` describing the update.
    -   The new file `content` (base64 encoded).
    -   The original file `sha`.
    -   The target `branch`.
-   Verify the update was successful by fetching the file again and checking the TODO count.

### 8. Provide a Summary
-   Report back to the user with a clear summary:
    -   Number of TODOs removed (completed).
    -   Number of new TODOs added.
    -   Final total count.
    -   Confirmation that the section title was preserved.
    -   The commit SHA of the update.

## Key Rules & Constraints
-   **Order is Mandatory:** The final TODO list **must** be sorted lexicographically by file path, then by ascending line number within each file.
-   **Preserve the Title:** The specified section title string must remain **exactly** as provided by the user.
-   **Handle Authentication Errors:** If the initial GitHub tool calls fail due to repository access restrictions, fall back to using the token with direct API calls via `local-python-execute`.
-   **Rate Limiting:** Be mindful of GitHub API rate limits. Introduce small delays (`time.sleep`) when fetching many files in a loop.
-   **Error Handling:** Check HTTP status codes and provide informative error messages if file fetching or updates fail.
