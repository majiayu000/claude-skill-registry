---
name: gitlab-commits
description: "Manages GitLab commits. Use for listing, creating, reverting, or querying commit details/diffs/comments. Triggers: commit history, changes, reversions."
---

### Overview
This skill covers commit operations via MCP. Use for code changes, diffs, or discussions.

### Available Tools
- `get_commits`: Get commits in a GitLab project, optionally filtered.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (Optional[str]): Optional. - Commit SHA
    - `ref_name` (Optional[str]): Optional. - Branch, tag, or commit SHA to filter commits
    - `since` (Optional[str]): Optional. - Only commits after this date (ISO 8601 format)
    - `until` (Optional[str]): Optional. - Only commits before this date (ISO 8601 format)
    - `path` (Optional[str]): Optional. - Only commits that include this file path
    - `all` (Optional[bool]): Optional. - Include all commits across all branches
- `create_commit`: Create a new commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (str): Optional. - Branch name for the commit
    - `commit_message` (str): Optional. - Commit message
    - `actions` (List[Dict[str, str]]): Optional. - List of actions (create/update/delete files)
    - `author_email` (Optional[str]): Optional. - Author email for the commit
    - `author_name` (Optional[str]): Optional. - Author name for the commit
- `get_commit_diff`: Get the diff of a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `revert_commit`: Revert a commit in a target branch in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA to revert
    - `branch` (str): Optional. - Target branch to apply the revert
    - `dry_run` (Optional[bool]): Optional. - Simulate the revert without applying
- `get_commit_comments`: Retrieve comments on a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `create_commit_comment`: Create a new comment on a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `note` (str): Optional. - Content of the comment
    - `path` (Optional[str]): Optional. - File path to associate with the comment
    - `line` (Optional[int]): Optional. - Line number in the file for the comment
    - `line_type` (Optional[str]): Optional. - Type of line ('new' or 'old')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_commit_discussions`: Retrieve discussions (threaded comments) on a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_commit_statuses`: Retrieve build/CI statuses for a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ref` (Optional[str]): Optional. - Filter statuses by reference (branch or tag)
    - `stage` (Optional[str]): Optional. - Filter statuses by CI stage
    - `name` (Optional[str]): Optional. - Filter statuses by job name
    - `coverage` (Optional[bool]): Optional. - Include coverage information
    - `all` (Optional[bool]): Optional. - Include all statuses
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `post_build_status_to_commit`: Post a build/CI status to a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `state` (str): Optional. - State of the build (e.g., 'pending', 'running', 'success', 'failed')
    - `target_url` (Optional[str]): Optional. - URL to link to the build
    - `context` (Optional[str]): Optional. - Context of the status (e.g., 'ci/build')
    - `description` (Optional[str]): Optional. - Description of the status
    - `coverage` (Optional[float]): Optional. - Coverage percentage
    - `pipeline_id` (Optional[int]): Optional. - ID of the associated pipeline
    - `ref` (Optional[str]): Optional. - Reference (branch or tag) for the status
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_commit_merge_requests`: Retrieve merge requests associated with a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_commit_gpg_signature`: Retrieve the GPG signature for a specific commit in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `commit_hash` (str): Optional. - Commit SHA
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use project_id and commit_hash for specifics.
2. For creation, build actions list (e.g., [{"action": "create", "file_path": "file.txt", "content": "..."}]).
3. Async tools (e.g., delete) support progress via ctx.

### Examples
- List commits: `get_commits` with project_id="123", ref_name="main", since="2023-01-01".
- Create: `create_commit` with project_id="123", branch="feature", commit_message="Add file", actions=[...].
- Revert: `revert_commit` with project_id="123", commit_hash="abc123", branch="main".

### Error Handling
- Invalid ref: Check branch/SHA existence first.
- Conflicts: Use diff tools to resolve.

Reference `tools-reference.md` for schemas.
