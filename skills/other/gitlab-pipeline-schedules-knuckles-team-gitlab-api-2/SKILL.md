---
name: gitlab-pipeline-schedules
description: "Manages GitLab pipeline schedules. Use for creating, editing, running scheduled pipelines. Triggers: cron jobs, automation."
---

### Overview
Covers scheduled CI.

### Available Tools
- `get_pipeline_schedules`: Retrieve a list of pipeline schedules for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `get_pipeline_schedule`: Retrieve details of a specific pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
- `get_pipelines_triggered_from_schedule`: Retrieve pipelines triggered by a specific pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
- `create_pipeline_schedule`: Create a pipeline schedule for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `description` (Optional[str]): Optional. - Description of the pipeline schedule
    - `ref` (str): Optional. - Reference (e.g., branch or tag) for the pipeline
    - `cron` (str): Optional. - Cron expression defining the schedule (e.g., '0 0 * * *')
    - `cron_timezone` (Optional[str]): Optional. - Timezone for the cron schedule (e.g., 'UTC')
    - `active` (Optional[bool]): Optional. - Whether the schedule is active
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `edit_pipeline_schedule`: Edit a pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `description` (Optional[str]): Optional. - New description of the pipeline schedule
    - `ref` (Optional[str]): Optional. - New reference (e.g., branch or tag) for the pipeline
    - `cron` (Optional[str]): Optional. - New cron expression for the schedule (e.g., '0 0 * * *')
    - `cron_timezone` (Optional[str]): Optional. - New timezone for the cron schedule (e.g., 'UTC')
    - `active` (Optional[bool]): Optional. - Whether the schedule is active
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `take_pipeline_schedule_ownership`: Take ownership of a pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_pipeline_schedule`: Delete a pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `run_pipeline_schedule`: Run a pipeline schedule immediately in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `create_pipeline_schedule_variable`: Create a variable for a pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `key` (str): Optional. - Key of the variable
    - `value` (str): Optional. - Value of the variable
    - `variable_type` (Optional[str]): Optional. - Type of variable (e.g., 'env_var')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_pipeline_schedule_variable`: Delete a variable from a pipeline schedule in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `pipeline_schedule_id` (int): Optional. - Pipeline schedule ID
    - `key` (str): Optional. - Key of the variable to delete
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Cron format for schedules.

### Examples
- Create: `create_pipeline_schedule` with project_id="123", ref="main", cron="0 0 * * *".
- Run: `run_pipeline_schedule` with pipeline_schedule_id=1.

### Error Handling
- Invalid cron: Validate format.
