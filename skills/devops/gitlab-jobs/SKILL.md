---
name: gitlab-jobs
description: "Manages GitLab CI jobs. Use for listing, logs, canceling, retrying, or erasing jobs. Triggers: CI builds, job status."
---

### Overview
Covers job execution and logs.

### Available Tools
- `get_project_jobs`: Retrieve a list of jobs for a specific GitLab project, optionally filtered by scope or a single job by id.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (Optional[int]): Optional. - Job ID
    - `scope` (Optional[str]): Optional. - Filter jobs by scope (e.g., 'success', 'failed')
    - `include_retried` (Optional[bool]): Optional. - Include retried jobs
    - `include_invisible` (Optional[bool]): Optional. - Include invisible jobs (e.g., from hidden pipelines)
- `get_project_job_log`: Retrieve the log (trace) of a specific job in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (int): Optional. - Job ID
- `cancel_project_job`: Cancel a specific job in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (int): Optional. - Job ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `retry_project_job`: Retry a specific job in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (int): Optional. - Job ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `erase_project_job`: Erase (delete artifacts and logs of) a specific job in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (int): Optional. - Job ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `run_project_job`: Run (play) a specific manual job in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `job_id` (int): Optional. - Job ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_pipeline_jobs`: Retrieve a list of jobs for a specific pipeline in a GitLab project, optionally filtered by scope.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_id` (int): Optional. - Pipeline ID
    - `scope` (Optional[str]): Optional. - Filter jobs by scope (e.g., 'success', 'failed')

### Usage Instructions
1. Use job_id for actions.
2. Filters: scope, status.

### Examples
- Get log: `get_project_job_log` with project_id="123", job_id=456.
- Retry: `retry_project_job` with project_id="123", job_id=456.

### Error Handling
- Job not found: Verify IDs.
