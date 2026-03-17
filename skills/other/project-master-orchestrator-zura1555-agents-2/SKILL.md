---
name: project-master-orchestrator
description: "Central coordinator for multi-platform workflow management across GitHub, Plane.so, and ClickUp. Orchestrates monitoring, reporting, and issue management across platforms."
version: 1.0.0
author: "Thuong-Tuan Tran"
tags: [workflow, orchestration, project-management, clickup, github, plane]
---

# Project Master Orchestrator

## Overview

The **Project Master Orchestrator** is the central coordinator for a multi-agent workflow management system that integrates with GitHub, Plane.so, and ClickUp. It orchestrates specialized agents to monitor projects, generate reports, and manage issues across platforms.

## Core Responsibilities

1. **Workflow Orchestration**: Coordinate execution across multiple specialized agents
2. **State Management**: Maintain global state across all platforms and phases
3. **Platform Coordination**: Manage interactions with GitHub, Plane.so, and ClickUp
4. **Error Handling**: Implement retry logic, error recovery, and escalation
5. **Quality Assurance**: Validate outputs before proceeding between phases
6. **Reporting**: Generate comprehensive workflow reports and summaries

## Architecture

### Orchestration Pattern

The orchestrator follows a **6-phase hybrid execution model** combining sequential and parallel execution:

```
Phase 0: Initialization (Sequential) - 30s
Phase 1: Discovery & Data Collection (Parallel) - 1-2 min
Phase 2: Analysis & Processing (Sequential) - 2-3 min
Phase 3: Action Execution (Parallel with coordination) - 3-5 min
Phase 4: Synchronization & Validation (Sequential) - 1 min
Phase 5: Reporting & Completion (Sequential) - 1 min
```

### Agent Structure

**Phase 1 Agents (ClickUp-focused):**
- `clickup-integration-agent` - ClickUp API client
- `monitoring-collector-agent` - Event aggregation
- `project-report-generator` - Report generation
- `issue-manager-agent` - Task management

**Phase 2 Agents (Multi-platform):**
- `github-integration-agent` - GitHub API client
- `plane-integration-agent` - Plane.so API client

**Phase 3 Agents (Advanced):**
- `communication-facilitator-agent` - Communication analysis
- `project-manager-agent` - Project planning
- `data-synchronizer-agent` - Cross-platform sync
- `alert-system-agent` - Alert management

## Input Specification

### Command-Line Interface

```bash
python orchestrate_workflow.py \
  --action <monitor|report|manage|sync> \
  --platforms <clickup|github|plane> \
  --project <project-id> \
  [--report-type <daily|weekly|monthly|sprint>] \
  [--format <markdown|json|html|pdf>] \
  [--list-id <clickup-list-id>] \
  [--assignee <user-id>] \
  [--priority <low|medium|high|critical>]
```

### Input JSON Structure

```json
{
  "action": "monitor|report|manage",
  "platforms": ["clickup"], // Phase 1: ClickUp only
  "project": "project-identifier",
  "parameters": {
    "reportType": "daily|weekly|monthly",
    "format": "markdown|json|html|pdf",
    "listId": "clickup-list-id",
    "assignee": "user-id",
    "priority": "high",
    "sprint": "sprint-24"
  }
}
```

## Output Specification

### Global State File

**Location:** `project-workspace/active-projects/{workflow-id}/global-state.json`

```json
{
  "workflowId": "workflow-2025-12-02-143022",
  "action": "monitor|report|manage",
  "platforms": ["clickup"],
  "status": "phase_name",
  "createdAt": "2025-12-02T14:30:22.000Z",
  "author": "Thuong-Tuan Tran",
  "phases": {
    "initialization": {
      "status": "complete",
      "output": "global-state.json",
      "timestamp": "2025-12-02T14:30:22.000Z"
    },
    "discovery": {
      "status": "complete",
      "output": "data/clickup-collected.json",
      "agents": {
        "clickup": "complete",
        "monitoring": "complete"
      }
    },
    "analysis": {
      "status": "complete",
      "output": "analysis/clickup-analytics.json"
    },
    "actions": {
      "status": "complete",
      "subphases": {
        "monitoring": "complete",
        "report_generation": "complete",
        "issue_management": "complete"
      }
    },
    "synchronization": {
      "status": "complete",
      "output": "sync/status.json"
    },
    "reporting": {
      "status": "complete",
      "output": "reports/final-report.md"
    }
  },
  "metadata": {
    "executionTime": 485,
    "platformsData": {
      "clickup": {
        "spaces": [],
        "folders": [],
        "lists": [],
        "tasks": [],
        "timeTracked": 0
      }
    },
    "metrics": {
      "tasksCreated": 0,
      "tasksUpdated": 5,
      "tasksCompleted": 3,
      "reportsGenerated": 2,
      "monitoringEventsProcessed": 47
    },
    "errors": []
  }
}
```

### Generated Artifacts

**Monitoring:**
- `monitoring/clickup-events.json` - Real-time event stream
- `monitoring/dashboard.html` - Interactive monitoring dashboard

**Reports:**
- `reports/daily-{date}.md` - Daily standup report
- `reports/weekly-{week}.md` - Weekly progress report
- `reports/monthly-{month}.md` - Monthly project report
- `reports/velocity-report-{week}.md` - Sprint velocity report

**Analysis:**
- `analysis/clickup-analytics.json` - ClickUp analytics
- `analysis/patterns.json` - Pattern detection results
- `analysis/insights.json` - Generated insights

**Issues:**
- `issues/{task-id}.json` - Individual task data
- `issues/bulk-operations.json` - Bulk operation results

## Workflow Phases

### Phase 0: Initialization

**Duration:** ~30 seconds

**Activities:**
1. Parse user input and validate parameters
2. Generate unique workflow ID (format: `workflow-YYYY-MM-DD-HHMMSS`)
3. Create project workspace directory structure
4. Initialize global state file
5. Load platform configuration files
6. Test platform API connections
7. Setup webhook endpoints (if enabled)

**Validation Gates:**
- Platform credentials valid
- Required parameters present
- Workspace created successfully

**Output:**
- `global-state.json` - Initialized state
- Workspace directory structure

### Phase 1: Discovery & Data Collection

**Duration:** 1-2 minutes (parallel execution)

**Activities:**
1. **Parallel Execution** (ClickUp-focused):
   - Fetch spaces, folders, lists from ClickUp
   - Collect tasks with metadata
   - Retrieve time tracking data
   - Gather team activity metrics

2. **Monitoring Collection**:
   - Aggregate real-time events
   - Normalize event data
   - Detect patterns and correlations

**Validation Gates:**
- Platform API calls successful
- Data collected > 0
- No critical errors

**Output:**
- `data/clickup-collected.json` - ClickUp raw data
- `monitoring/clickup-events.json` - Event stream

### Phase 2: Analysis & Processing

**Duration:** 2-3 minutes

**Activities:**
1. Normalize data across platforms
2. Calculate velocity metrics
3. Identify bottlenecks and blockers
4. Generate insights and recommendations
5. Prepare action items

**Validation Gates:**
- Analysis complete
- Metrics calculated successfully
- Insights generated

**Output:**
- `analysis/clickup-analytics.json` - Analytics results
- `analysis/patterns.json` - Pattern detection
- `analysis/insights.json` - Generated insights

### Phase 3: Action Execution

**Duration:** 3-5 minutes (parallel with coordination)

**Activities:**
1. **Monitoring** (if action=monitor):
   - Process event stream
   - Detect anomalies
   - Generate alerts

2. **Report Generation** (if action=report):
   - Create daily/weekly/monthly reports
   - Format in requested output type
   - Generate visualizations

3. **Issue Management** (if action=manage):
   - Create/update tasks
   - Bulk operations
   - Status synchronization

**Coordination:**
- Shared state file updates
- Lock files for critical sections
- Event-driven triggers

**Output:**
- Action-specific artifacts
- Updated global state

### Phase 4: Synchronization & Validation

**Duration:** ~1 minute

**Activities:**
1. Validate all operations completed successfully
2. Check for conflicts or errors
3. Update global state
4. Prepare rollback data (if needed)
5. Log completion metrics

**Validation Gates:**
- All operations successful
- State consistent
- No unresolved errors

**Output:**
- `sync/status.json` - Synchronization status
- Updated global state

### Phase 5: Reporting & Completion

**Duration:** ~1 minute

**Activities:**
1. Generate final workflow report
2. Archive project artifacts
3. Send notifications (if configured)
4. Cleanup temporary files
5. Update state to "complete"

**Output:**
- `reports/final-report.md` - Workflow summary
- Archived project

## State Management

### MultiPlatformStateManager

The orchestrator uses an enhanced `MultiPlatformStateManager` class (in `scripts/multi_platform_state_manager.py`) that extends the existing `StateManager`:

**Key Features:**
- Platform-specific state tracking
- Multi-platform data aggregation
- Cross-platform synchronization status
- Error logging with retry logic
- Phase transition validation

**Usage:**
```python
state_manager = MultiPlatformStateManager(state_file)
state_manager.update_phase("discovery", "complete")
state_manager.add_platform_data("clickup", clickup_data)
state_manager.add_metric("tasks_created", 5)
state_manager.log_error("phase_name", error_details)
```

## Error Handling

### Retry Logic

**Pattern:** 3-attempt retry with exponential backoff

```python
retry_config = {
    "max_attempts": 3,
    "base_delay": 5,  # seconds
    "max_delay": 60,
    "backoff_factor": 2
}
```

**Error Handling Strategy:**
1. Log error to state.json
2. Retry operation (up to 3 attempts)
3. If max retries exceeded, mark phase as "error"
4. Continue with other parallel phases
5. Report final status in summary

### Error Types

**Recoverable Errors:**
- Network timeouts
- Rate limit exceeded
- Temporary API failures

**Non-Recoverable Errors:**
- Invalid authentication
- Missing required parameters
- Workspace creation failure

## Platform Integration

### ClickUp Integration (Phase 1)

**Configuration:**
- API token in `config/clickup-config.json`
- Rate limit: 100 requests/minute
- Webhook support for real-time events

**API Endpoints:**
- `/api/v2/list/{list_id}/task` - Task operations
- `/api/v2/space/{space_id}` - Space operations
- `/api/v2/folder/{folder_id}` - Folder operations
- `/api/v2/team` - Team operations

**Webhook Events:**
- Task created/updated/deleted
- List changed
- Time tracked
- Comment added

### GitHub Integration (Phase 2)

**Configuration:**
- Personal Access Token or GitHub App
- Rate limit: 5000 requests/hour
- Webhook support

**API Endpoints:**
- `/repos/{owner}/{repo}/issues` - Issues
- `/repos/{owner}/{repo}/pulls` - Pull Requests
- `/projects` - Projects v2
- `/repos/{owner}/{repo}/discussions` - Discussions

### Plane.so Integration (Phase 2)

**Configuration:**
- X-API-Key header
- Rate limit: 60 requests/minute
- Webhook support

**API Endpoints:**
- `/work-items/` - Work items
- `/projects/` - Projects
- `/cycles/` - Cycles
- `/modules/` - Modules

## Quality Gates

### Phase Transitions

**Requirements for moving to next phase:**
1. All previous phase outputs exist
2. No critical errors logged
3. Required data collected
4. Validation checks passed

### Output Validation

**Checks:**
- File exists
- File size > 0
- Valid JSON/Markdown format
- Required fields present
- Data consistency

## Performance Targets

**Execution Time:**
- Total workflow: < 12 minutes
- Phase 0 (Init): < 30 seconds
- Phase 1 (Discovery): < 2 minutes
- Phase 2 (Analysis): < 3 minutes
- Phase 3 (Actions): < 5 minutes
- Phase 4 (Sync): < 1 minute
- Phase 5 (Reporting): < 1 minute

**Reliability:**
- API success rate: > 99%
- Error rate: < 1%
- Data accuracy: > 99.5%

## Monitoring & Metrics

### Real-Time Metrics

**System Metrics:**
- Workflow execution time
- API call success rate
- Error rate by phase
- Agent response time

**Business Metrics:**
- Tasks monitored
- Reports generated
- Issues managed
- Sync success rate

### Alert Conditions

**Critical Alerts:**
- Execution time > 15 minutes
- API failure rate > 5%
- State corruption

**Warning Alerts:**
- Execution time > 10 minutes
- API failure rate > 2%
- Rate limit approaching (80%)

## Best Practices

### File Naming

**Conventions:**
- `data/{platform}-collected.json`
- `analysis/{type}-analysis.json`
- `reports/{report-type}-{identifier}.md`
- `monitoring/{platform}-events.json`
- `issues/{task-id}.json`

### State Updates

**Pattern:**
1. Update phase status before starting phase
2. Add output file path when complete
3. Add timestamp for tracking
4. Log errors with context
5. Update metrics incrementally

### Error Logging

**Include:**
- Phase name
- Error message
- Stack trace
- Timestamp
- Attempt number (for retries)
- Context data

## Examples

### Example 1: Daily Monitoring

```bash
python orchestrate_workflow.py \
  --action monitor \
  --platforms clickup \
  --project "ecommerce-platform" \
  --report-type daily
```

**Expected Output:**
- Real-time event monitoring
- Daily standup report
- Monitoring dashboard

### Example 2: Weekly Report Generation

```bash
python orchestrate_workflow.py \
  --action report \
  --platforms clickup \
  --report-type weekly \
  --format markdown html pdf \
  --sprint "sprint-24"
```

**Expected Output:**
- Weekly progress report (3 formats)
- Velocity metrics
- Sprint analytics

### Example 3: Task Management

```bash
python orchestrate_workflow.py \
  --action manage \
  --platforms clickup \
  --list-id "list-123" \
  --title "Implement new feature" \
  --description "Feature description" \
  --assignee "user-456" \
  --priority high
```

**Expected Output:**
- New task created
- Task data in `issues/` directory
- Success confirmation

## Resources

### Scripts

- `orchestrate_workflow.py` - Main orchestrator script
- `multi_platform_state_manager.py` - Enhanced state management
- `platform_clients/clickup_client.py` - ClickUp API client
- `platform_clients/github_client.py` - GitHub API client (Phase 2)
- `platform_clients/plane_client.py` - Plane.so API client (Phase 2)

### Configuration Files

- `config/clickup-config.json` - ClickUp credentials
- `config/github-config.json` - GitHub credentials (Phase 2)
- `config/plane-config.json` - Plane.so credentials (Phase 2)
- `config/monitoring-rules.json` - Monitoring thresholds
- `config/alert-rules.json` - Alert definitions

### Workspace Directories

- `project-workspace/active-projects/` - Active workflows
- `project-workspace/archive/` - Completed workflows
- `config/` - Configuration files
- `logs/` - Execution logs

## Validation Rules

### Input Validation

1. Action must be one of: monitor, report, manage, sync
2. At least one platform must be specified
3. Project ID is required
4. Report type required if action=report
5. Format must be one of: markdown, json, html, pdf

### State Validation

1. Workflow ID must be unique
2. Phase statuses must be valid (pending, in_progress, complete, error)
3. Metadata must include executionTime
4. Errors array must exist (can be empty)
5. Platforms array must match requested platforms

### Output Validation

1. All declared output files must exist
2. File sizes must be > 0
3. JSON files must be valid
4. Required fields present in outputs
5. Timestamps must be valid ISO 8601 format

## Troubleshooting

### Common Issues

**Issue:** "ClickUp API authentication failed"
- **Solution:** Verify API token in `config/clickup-config.json`
- Check token permissions and expiration

**Issue:** "Rate limit exceeded"
- **Solution:** Implement exponential backoff
- Reduce request frequency
- Upgrade API plan if needed

**Issue:** "Phase validation failed"
- **Solution:** Check previous phase outputs exist
- Verify file format and required fields
- Review state.json for error details

**Issue:** "Webhook delivery failed"
- **Solution:** Verify webhook URL is accessible
- Check webhook signature verification
- Review webhook event payload format

### Debug Mode

Enable verbose logging:
```bash
export LOG_LEVEL=DEBUG
python orchestrate_workflow.py --action monitor --platforms clickup
```

## Future Enhancements

**Phase 2-3 Roadmap:**
- GitHub Projects v2 integration
- Plane.so Cycles and Modules
- Cross-platform issue synchronization
- Advanced analytics and predictions
- Machine learning-based insights
- Slack/Discord notifications
- Custom dashboard creation

**Version History:**
- v1.0.0 - Initial ClickUp integration (Phase 1)
- v1.1.0 - GitHub and Plane.so support (Phase 2)
- v1.2.0 - Advanced features (Phase 3)

---

**Author:** Thuong-Tuan Tran
**Version:** 1.0.0
**Last Updated:** 2025-12-02
