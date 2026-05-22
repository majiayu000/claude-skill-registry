---
name: gitlab-pipelines
description: "Manages GitLab pipelines. Use for listing, running pipelines. Triggers: CI triggers."
---

### Overview
Handles pipeline execution.

### Available Tools
- `get_pipelines`: Retrieve a list of pipelines for a specific GitLab project, optionally filtered by scope, status, or ref or details of a specific pipeline in a GitLab project..
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_id` (Optional[int]): Optional. - Pipeline ID
    - `scope` (Optional[str]): Optional. - Filter pipelines by scope (e.g., 'running', 'branches')
    - `status` (Optional[str]): Optional. - Filter pipelines by status (e.g., 'success', 'failed')
    - `ref` (Optional[str]): Optional. - Filter pipelines by reference (e.g., branch or tag name)
    - `source` (Optional[str]): Optional. - Filter pipelines by source (e.g., 'push', 'schedule')
    - `updated_after` (Optional[str]): Optional. - Filter pipelines updated after this date (ISO 8601 format)
    - `updated_before` (Optional[str]): Optional. - Filter pipelines updated before this date (ISO 8601 format)
- `run_pipeline`: Run a pipeline for a specific GitLab project with a given reference (e.g., branch or tag).
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ref` (str): Optional. - Reference (e.g., branch or tag) to run the pipeline on
    - `variables` (Optional[Dict[str, str]]): Optional. - Dictionary of pipeline variables
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use ref for branch/tag.

### Examples
- Run: `run_pipeline` with project_id="123", ref="main".
- List: `get_pipelines` with project_id="123", status="running".

### Error Handling
- Failed triggers: Check config.
