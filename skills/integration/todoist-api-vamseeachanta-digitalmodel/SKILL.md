---
name: todoist-api
version: 1.0.0
description: Task management API integration for Todoist with projects, tasks, labels, filters, webhooks, and Python SDK usage
author: workspace-hub
category: productivity
type: skill
capabilities:
  - task_management
  - project_organization
  - label_filtering
  - natural_language_dates
  - recurring_tasks
  - webhook_integration
  - sync_api
  - batch_operations
tools:
  - todoist-api
  - todoist-python
  - curl
  - jq
tags: [todoist, tasks, api, productivity, gtd, webhooks, automation, project-management]
platforms: [rest-api, python, web, mobile]
related_skills:
  - api-integration
  - webhook-automation
  - obsidian
  - notion-api
---

# Todoist API Integration Skill

Master the Todoist API for task management automation, including projects, tasks, labels, filters, webhooks, and Python SDK patterns. This skill covers REST API v2, Sync API v9, and integration patterns.

## When to Use This Skill

### USE Todoist API when:
- Automating task creation from external systems
- Building integrations with other productivity tools
- Creating custom task dashboards or reports
- Implementing GTD workflows programmatically
- Syncing tasks with calendar applications
- Building CLI tools for task management
- Automating recurring task patterns
- Integrating with CI/CD for project tracking

### DON'T USE Todoist API when:
- Need complex project management (use Jira, Asana)
- Require database-style queries (use Notion API)
- Need real-time collaboration on tasks (use Linear)
- Building for enterprise with SSO requirements
- Need Gantt charts or resource management

## Prerequisites

### API Authentication

```bash
# Get your API token from:
# https://todoist.com/app/settings/integrations/developer

# Set environment variable
export TODOIST_API_KEY="your-api-token-here"

# Verify authentication
curl -s -X GET "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq '.[0]'
```

### Python SDK Installation

```bash
# Install official Python SDK
pip install todoist-api-python

# Or with uv
uv pip install todoist-api-python

# For sync API features
pip install todoist-api-python requests
```

### Verify Setup

```python
from todoist_api_python import TodoistAPI

api = TodoistAPI("your-api-token")

# Test connection
try:
    projects = api.get_projects()
    print(f"Connected! Found {len(projects)} projects")
except Exception as e:
    print(f"Connection failed: {e}")
```

## Core Capabilities

### 1. Projects Management

**REST API - Projects:**
```bash
# List all projects
curl -s -X GET "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Get specific project
curl -s -X GET "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Create project
curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Work Tasks",
        "color": "blue",
        "is_favorite": true,
        "view_style": "list"
    }' | jq

# Create sub-project
curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Q1 Goals",
        "parent_id": "PARENT_PROJECT_ID",
        "color": "green"
    }' | jq

# Update project
curl -s -X POST "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Work Tasks - Updated",
        "color": "red"
    }' | jq

# Delete project
curl -s -X DELETE "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY"

# Get project collaborators
curl -s -X GET "https://api.todoist.com/rest/v2/projects/PROJECT_ID/collaborators" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq
```

**Python SDK - Projects:**
```python
from todoist_api_python import TodoistAPI
import os

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

# List all projects
projects = api.get_projects()
for project in projects:
    print(f"{project.name} (ID: {project.id})")

# Get specific project
project = api.get_project(project_id="2345678901")
print(f"Project: {project.name}, Color: {project.color}")

# Create project
new_project = api.add_project(
    name="New Project",
    color="blue",
    is_favorite=True,
    view_style="board"  # "list" or "board"
)
print(f"Created: {new_project.name} (ID: {new_project.id})")

# Create sub-project
sub_project = api.add_project(
    name="Sub Project",
    parent_id="2345678901",
    color="green"
)

# Update project
updated = api.update_project(
    project_id="2345678901",
    name="Updated Name",
    color="red"
)

# Delete project
api.delete_project(project_id="2345678901")

# Get project sections
sections = api.get_sections(project_id="2345678901")
for section in sections:
    print(f"  Section: {section.name}")
```

### 2. Tasks Management

**REST API - Tasks:**
```bash
# List all tasks
curl -s -X GET "https://api.todoist.com/rest/v2/tasks" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Get tasks with filter
curl -s -X GET "https://api.todoist.com/rest/v2/tasks?filter=today" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Get tasks for specific project
curl -s -X GET "https://api.todoist.com/rest/v2/tasks?project_id=PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Get single task
curl -s -X GET "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Create task with all options
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "content": "Complete project report",
        "description": "Include Q4 metrics and projections",
        "project_id": "PROJECT_ID",
        "section_id": "SECTION_ID",
        "parent_id": null,
        "order": 1,
        "labels": ["work", "urgent"],
        "priority": 4,
        "due_string": "tomorrow at 5pm",
        "due_lang": "en",
        "assignee_id": null
    }' | jq

# Create task with natural language due date
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "content": "Weekly review",
        "due_string": "every friday at 4pm"
    }' | jq

# Update task
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "content": "Updated task content",
        "priority": 3,
        "due_string": "next monday"
    }' | jq

# Complete task
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID/close" \
    -H "Authorization: Bearer $TODOIST_API_KEY"

# Reopen task
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID/reopen" \
    -H "Authorization: Bearer $TODOIST_API_KEY"

# Delete task
curl -s -X DELETE "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY"
```

**Python SDK - Tasks:**
```python
from todoist_api_python import TodoistAPI
from datetime import datetime, timedelta
import os

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

# Get all tasks
tasks = api.get_tasks()
for task in tasks:
    due = task.due.string if task.due else "No due date"
    print(f"- [{task.priority}] {task.content} (Due: {due})")

# Get tasks with filter
today_tasks = api.get_tasks(filter="today")
overdue_tasks = api.get_tasks(filter="overdue")
high_priority = api.get_tasks(filter="p1 | p2")

# Get tasks for project
project_tasks = api.get_tasks(project_id="2345678901")

# Create task
new_task = api.add_task(
    content="Review pull requests",
    description="Check all open PRs in main repo",
    project_id="2345678901",
    section_id="3456789012",
    labels=["work", "development"],
    priority=4,  # 1=normal, 2=medium, 3=high, 4=urgent
    due_string="tomorrow at 10am",
    due_lang="en"
)
print(f"Created task: {new_task.id}")

# Create sub-task
sub_task = api.add_task(
    content="Review frontend PR #123",
    parent_id=new_task.id,
    priority=3
)

# Create recurring task
recurring_task = api.add_task(
    content="Weekly team standup",
    due_string="every monday at 9am"
)

# Update task
updated_task = api.update_task(
    task_id=new_task.id,
    content="Review all pull requests",
    priority=4,
    due_string="today at 5pm"
)

# Complete task
api.close_task(task_id=new_task.id)

# Reopen task
api.reopen_task(task_id=new_task.id)

# Delete task
api.delete_task(task_id=new_task.id)

# Move task to different project
api.update_task(
    task_id="1234567890",
    project_id="NEW_PROJECT_ID"
)
```

### 3. Labels Management

**REST API - Labels:**
```bash
# List all labels
curl -s -X GET "https://api.todoist.com/rest/v2/labels" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Create label
curl -s -X POST "https://api.todoist.com/rest/v2/labels" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "urgent",
        "color": "red",
        "order": 1,
        "is_favorite": true
    }' | jq

# Update label
curl -s -X POST "https://api.todoist.com/rest/v2/labels/LABEL_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "high-priority",
        "color": "orange"
    }' | jq

# Delete label
curl -s -X DELETE "https://api.todoist.com/rest/v2/labels/LABEL_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY"
```

**Python SDK - Labels:**
```python
from todoist_api_python import TodoistAPI

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

# List all labels
labels = api.get_labels()
for label in labels:
    print(f"@{label.name} (color: {label.color})")

# Create label
new_label = api.add_label(
    name="review",
    color="blue",
    order=1,
    is_favorite=True
)

# Update label
api.update_label(
    label_id=new_label.id,
    name="code-review",
    color="green"
)

# Delete label
api.delete_label(label_id=new_label.id)

# Get tasks with specific label
review_tasks = api.get_tasks(filter="@code-review")
```

### 4. Sections Management

**REST API - Sections:**
```bash
# List sections for project
curl -s -X GET "https://api.todoist.com/rest/v2/sections?project_id=PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Create section
curl -s -X POST "https://api.todoist.com/rest/v2/sections" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "In Progress",
        "project_id": "PROJECT_ID",
        "order": 2
    }' | jq

# Update section
curl -s -X POST "https://api.todoist.com/rest/v2/sections/SECTION_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Currently Working"
    }' | jq

# Delete section
curl -s -X DELETE "https://api.todoist.com/rest/v2/sections/SECTION_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY"
```

**Python SDK - Sections:**
```python
# Create Kanban-style sections
sections = ["Backlog", "To Do", "In Progress", "Review", "Done"]

for i, section_name in enumerate(sections):
    api.add_section(
        name=section_name,
        project_id="2345678901",
        order=i
    )

# Get sections
sections = api.get_sections(project_id="2345678901")
for section in sections:
    print(f"Section: {section.name} (ID: {section.id})")

# Move task to section
api.update_task(
    task_id="1234567890",
    section_id="IN_PROGRESS_SECTION_ID"
)
```

### 5. Comments Management

**REST API - Comments:**
```bash
# Get comments for task
curl -s -X GET "https://api.todoist.com/rest/v2/comments?task_id=TASK_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Get comments for project
curl -s -X GET "https://api.todoist.com/rest/v2/comments?project_id=PROJECT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" | jq

# Add comment to task
curl -s -X POST "https://api.todoist.com/rest/v2/comments" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "task_id": "TASK_ID",
        "content": "This is a comment on the task"
    }' | jq

# Add comment with attachment
curl -s -X POST "https://api.todoist.com/rest/v2/comments" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "task_id": "TASK_ID",
        "content": "See attached file",
        "attachment": {
            "file_name": "report.pdf",
            "file_type": "application/pdf",
            "file_url": "https://example.com/report.pdf"
        }
    }' | jq

# Update comment
curl -s -X POST "https://api.todoist.com/rest/v2/comments/COMMENT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "content": "Updated comment content"
    }' | jq

# Delete comment
curl -s -X DELETE "https://api.todoist.com/rest/v2/comments/COMMENT_ID" \
    -H "Authorization: Bearer $TODOIST_API_KEY"
```

**Python SDK - Comments:**
```python
# Get comments for task
comments = api.get_comments(task_id="1234567890")
for comment in comments:
    print(f"  {comment.posted_at}: {comment.content}")

# Add comment
new_comment = api.add_comment(
    task_id="1234567890",
    content="Added some notes about this task"
)

# Update comment
api.update_comment(
    comment_id=new_comment.id,
    content="Updated notes"
)

# Delete comment
api.delete_comment(comment_id=new_comment.id)
```

### 6. Filters and Queries

**Filter Syntax:**
```bash
# Date filters
"today"                    # Due today
"tomorrow"                 # Due tomorrow
"overdue"                  # Past due date
"next 7 days"              # Due in next week
"no date"                  # No due date set
"Jan 15"                   # Specific date
"before: Jan 20"           # Before date
"after: Jan 10"            # After date

# Priority filters
"p1"                       # Priority 1 (urgent)
"p2"                       # Priority 2 (high)
"p3"                       # Priority 3 (medium)
"p4"                       # Priority 4 (normal)
"(p1 | p2)"               # Priority 1 OR 2

# Label filters
"@work"                    # Has label "work"
"@work & @urgent"          # Has both labels
"@work | @personal"        # Has either label
"!@work"                   # Does NOT have label

# Project filters
"#Work"                    # In project "Work"
"##Work"                   # In project "Work" and sub-projects
"#Work & #Q1"              # In both projects (intersection)

# Search filters
"search: meeting"          # Content contains "meeting"

# Assignee filters
"assigned to: me"          # Assigned to current user
"assigned to: John"        # Assigned to John
"assigned by: me"          # Assigned by current user

# Combined filters
"today & @work"            # Due today with work label
"(today | overdue) & p1"   # Today or overdue AND priority 1
"#Work & !@done"           # In Work project without done label
```

**Python Filter Examples:**
```python
# Get tasks with various filters
today_work = api.get_tasks(filter="today & @work")
urgent = api.get_tasks(filter="(p1 | p2) & (today | overdue)")
project_pending = api.get_tasks(filter="#ProjectAlpha & !@completed")
this_week = api.get_tasks(filter="next 7 days")
no_date = api.get_tasks(filter="no date & @inbox")

# Complex filter
complex_filter = api.get_tasks(
    filter="(today | tomorrow) & (p1 | p2) & (#Work | #Personal) & !@waiting"
)
```

### 7. Sync API

**Sync API Basics:**
```bash
# Initial sync (full read)
curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "sync_token=*&resource_types=[\"all\"]" | jq

# Incremental sync (with sync token)
SYNC_TOKEN="your-sync-token-from-previous-response"
curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "sync_token=$SYNC_TOKEN&resource_types=[\"items\",\"projects\"]" | jq

# Batch operations with commands
curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
    -H "Authorization: Bearer $TODOIST_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "commands": [
            {
                "type": "item_add",
                "temp_id": "temp1",
                "uuid": "unique-uuid-1",
                "args": {
                    "content": "Task 1",
                    "project_id": "PROJECT_ID"
                }
            },
            {
                "type": "item_add",
                "temp_id": "temp2",
                "uuid": "unique-uuid-2",
                "args": {
                    "content": "Task 2",
                    "project_id": "PROJECT_ID"
                }
            }
        ]
    }' | jq
```

**Python Sync Operations:**
```python
import requests
import json
import uuid

TODOIST_API_KEY = os.environ["TODOIST_API_KEY"]
SYNC_URL = "https://api.todoist.com/sync/v9/sync"

def sync_read(sync_token="*", resource_types=None):
    """Read data using Sync API"""
    if resource_types is None:
        resource_types = ["all"]

    response = requests.post(
        SYNC_URL,
        headers={"Authorization": f"Bearer {TODOIST_API_KEY}"},
        data={
            "sync_token": sync_token,
            "resource_types": json.dumps(resource_types)
        }
    )
    return response.json()

def batch_add_tasks(tasks):
    """Add multiple tasks in one request"""
    commands = []
    for task in tasks:
        commands.append({
            "type": "item_add",
            "temp_id": f"temp_{uuid.uuid4().hex[:8]}",
            "uuid": str(uuid.uuid4()),
            "args": task
        })

    response = requests.post(
        SYNC_URL,
        headers={
            "Authorization": f"Bearer {TODOIST_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"commands": commands}
    )
    return response.json()

# Example: Add multiple tasks at once
tasks_to_add = [
    {"content": "Task 1", "project_id": "2345678901", "priority": 4},
    {"content": "Task 2", "project_id": "2345678901", "priority": 3},
    {"content": "Task 3", "project_id": "2345678901", "priority": 2},
]

result = batch_add_tasks(tasks_to_add)
print(f"Added {len(tasks_to_add)} tasks")
```

### 8. Webhooks

**Webhook Setup:**
```python
from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)
TODOIST_CLIENT_SECRET = os.environ["TODOIST_CLIENT_SECRET"]

def verify_webhook(payload, signature):
    """Verify webhook signature"""
    computed = hmac.new(
        TODOIST_CLIENT_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

@app.route("/webhook/todoist", methods=["POST"])
def todoist_webhook():
    # Verify signature
    signature = request.headers.get("X-Todoist-Hmac-SHA256", "")
    if not verify_webhook(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    # Parse event
    event = request.json
    event_name = event.get("event_name")
    event_data = event.get("event_data", {})

    print(f"Received event: {event_name}")

    # Handle different event types
    if event_name == "item:added":
        handle_task_added(event_data)
    elif event_name == "item:completed":
        handle_task_completed(event_data)
    elif event_name == "item:updated":
        handle_task_updated(event_data)
    elif event_name == "item:deleted":
        handle_task_deleted(event_data)
    elif event_name == "project:added":
        handle_project_added(event_data)

    return jsonify({"status": "ok"})

def handle_task_added(data):
    print(f"New task: {data.get('content')}")
    # Add your logic here

def handle_task_completed(data):
    print(f"Task completed: {data.get('content')}")
    # Add your logic here

def handle_task_updated(data):
    print(f"Task updated: {data.get('content')}")
    # Add your logic here

def handle_task_deleted(data):
    print(f"Task deleted: {data.get('id')}")
    # Add your logic here

def handle_project_added(data):
    print(f"New project: {data.get('name')}")
    # Add your logic here

if __name__ == "__main__":
    app.run(port=5000)
```

**Webhook Events:**
```python
# Available webhook events
WEBHOOK_EVENTS = {
    # Task events
    "item:added": "Task created",
    "item:updated": "Task updated",
    "item:deleted": "Task deleted",
    "item:completed": "Task completed",
    "item:uncompleted": "Task reopened",

    # Project events
    "project:added": "Project created",
    "project:updated": "Project updated",
    "project:deleted": "Project deleted",
    "project:archived": "Project archived",
    "project:unarchived": "Project unarchived",

    # Note/Comment events
    "note:added": "Comment added",
    "note:updated": "Comment updated",
    "note:deleted": "Comment deleted",

    # Label events
    "label:added": "Label created",
    "label:updated": "Label updated",
    "label:deleted": "Label deleted",

    # Section events
    "section:added": "Section created",
    "section:updated": "Section updated",
    "section:deleted": "Section deleted",

    # Reminder events
    "reminder:fired": "Reminder triggered",
}
```

## Complete Examples

### Example 1: GTD Weekly Review Automation

```python
#!/usr/bin/env python3
"""gtd_weekly_review.py - Automate GTD weekly review"""

from todoist_api_python import TodoistAPI
from datetime import datetime, timedelta
import os

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

def weekly_review():
    """Perform GTD weekly review"""
    report = {
        "completed_this_week": [],
        "overdue": [],
        "upcoming": [],
        "no_due_date": [],
        "waiting_for": []
    }

    # Get all tasks
    all_tasks = api.get_tasks()

    # Get completed tasks (last 7 days)
    # Note: REST API doesn't provide completed tasks easily
    # Would need Sync API for completed items

    # Categorize active tasks
    today = datetime.now().date()
    week_ahead = today + timedelta(days=7)

    for task in all_tasks:
        # Check for waiting label
        if "waiting" in [l.lower() for l in task.labels]:
            report["waiting_for"].append(task)
            continue

        if task.due:
            due_date = datetime.strptime(task.due.date, "%Y-%m-%d").date()

            if due_date < today:
                report["overdue"].append(task)
            elif due_date <= week_ahead:
                report["upcoming"].append(task)
        else:
            report["no_due_date"].append(task)

    return report

def generate_review_report(report):
    """Generate markdown review report"""
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# Weekly Review - {today}

## Overdue Tasks ({len(report['overdue'])})
"""
    for task in report["overdue"]:
        content += f"- [ ] {task.content} (Due: {task.due.string})\n"

    content += f"""
## Upcoming This Week ({len(report['upcoming'])})
"""
    for task in sorted(report["upcoming"], key=lambda t: t.due.date):
        content += f"- [ ] {task.content} (Due: {task.due.string})\n"

    content += f"""
## Waiting For ({len(report['waiting_for'])})
"""
    for task in report["waiting_for"]:
        content += f"- {task.content}\n"

    content += f"""
## Tasks Without Due Date ({len(report['no_due_date'])})
"""
    for task in report["no_due_date"][:10]:  # Limit to 10
        content += f"- {task.content}\n"

    if len(report["no_due_date"]) > 10:
        content += f"- ... and {len(report['no_due_date']) - 10} more\n"

    return content

def create_review_task():
    """Create next week's review task"""
    api.add_task(
        content="Weekly Review",
        due_string="next sunday at 6pm",
        labels=["review"],
        priority=4
    )

if __name__ == "__main__":
    report = weekly_review()
    markdown_report = generate_review_report(report)

    # Save report
    filename = f"weekly_review_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w") as f:
        f.write(markdown_report)

    print(f"Report saved: {filename}")
    print(f"\nSummary:")
    print(f"  Overdue: {len(report['overdue'])}")
    print(f"  Upcoming: {len(report['upcoming'])}")
    print(f"  Waiting: {len(report['waiting_for'])}")
    print(f"  No date: {len(report['no_due_date'])}")

    # Create next review task
    create_review_task()
```

### Example 2: Project Template Creator

```python
#!/usr/bin/env python3
"""project_template.py - Create projects from templates"""

from todoist_api_python import TodoistAPI
import os
import json

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

# Define project templates
TEMPLATES = {
    "sprint": {
        "color": "blue",
        "sections": ["Backlog", "To Do", "In Progress", "Review", "Done"],
        "tasks": [
            {"content": "Sprint Planning", "section": "To Do", "priority": 4},
            {"content": "Daily Standups", "section": "To Do", "due_string": "every weekday at 9am"},
            {"content": "Sprint Review", "section": "Backlog", "priority": 3},
            {"content": "Sprint Retrospective", "section": "Backlog", "priority": 3},
        ]
    },
    "content_piece": {
        "color": "green",
        "sections": ["Research", "Writing", "Editing", "Publishing"],
        "tasks": [
            {"content": "Research topic", "section": "Research", "priority": 3},
            {"content": "Create outline", "section": "Research", "priority": 3},
            {"content": "Write first draft", "section": "Writing", "priority": 4},
            {"content": "Self-review and edit", "section": "Editing", "priority": 3},
            {"content": "Final review", "section": "Editing", "priority": 3},
            {"content": "Publish", "section": "Publishing", "priority": 4},
        ]
    },
    "event": {
        "color": "yellow",
        "sections": ["Planning", "Preparation", "Execution", "Follow-up"],
        "tasks": [
            {"content": "Define event goals", "section": "Planning", "priority": 4},
            {"content": "Create guest list", "section": "Planning", "priority": 3},
            {"content": "Book venue", "section": "Preparation", "priority": 4},
            {"content": "Send invitations", "section": "Preparation", "priority": 4},
            {"content": "Confirm RSVPs", "section": "Preparation", "priority": 3},
            {"content": "Event execution", "section": "Execution", "priority": 4},
            {"content": "Send thank you notes", "section": "Follow-up", "priority": 3},
            {"content": "Event retrospective", "section": "Follow-up", "priority": 2},
        ]
    }
}

def create_project_from_template(name: str, template_name: str, due_date: str = None):
    """Create a project from template"""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    template = TEMPLATES[template_name]

    # Create project
    project = api.add_project(
        name=name,
        color=template["color"],
        view_style="board"
    )
    print(f"Created project: {project.name} (ID: {project.id})")

    # Create sections
    section_ids = {}
    for i, section_name in enumerate(template["sections"]):
        section = api.add_section(
            name=section_name,
            project_id=project.id,
            order=i
        )
        section_ids[section_name] = section.id
        print(f"  Created section: {section_name}")

    # Create tasks
    for task_def in template["tasks"]:
        task_args = {
            "content": task_def["content"],
            "project_id": project.id,
            "section_id": section_ids[task_def["section"]],
            "priority": task_def.get("priority", 1)
        }

        if "due_string" in task_def:
            task_args["due_string"] = task_def["due_string"]
        elif due_date:
            task_args["due_string"] = due_date

        task = api.add_task(**task_args)
        print(f"  Created task: {task.content}")

    return project

def list_templates():
    """List available templates"""
    print("Available templates:")
    for name, template in TEMPLATES.items():
        print(f"\n  {name}:")
        print(f"    Sections: {', '.join(template['sections'])}")
        print(f"    Tasks: {len(template['tasks'])}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create Todoist project from template")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--template", help="Template name")
    parser.add_argument("--due", help="Due date for tasks (optional)")

    args = parser.parse_args()

    if args.list:
        list_templates()
    elif args.name and args.template:
        create_project_from_template(args.name, args.template, args.due)
    else:
        parser.print_help()
```

### Example 3: Daily Task Report

```python
#!/usr/bin/env python3
"""daily_report.py - Generate daily task report"""

from todoist_api_python import TodoistAPI
from datetime import datetime
import os

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

def generate_daily_report():
    """Generate a daily task report"""
    today = datetime.now().strftime("%Y-%m-%d")

    # Get tasks for different filters
    overdue = api.get_tasks(filter="overdue")
    due_today = api.get_tasks(filter="today")
    high_priority = api.get_tasks(filter="(p1 | p2) & !today & !overdue")

    # Group today's tasks by project
    projects = {}
    for task in due_today:
        project_id = task.project_id
        if project_id not in projects:
            try:
                project = api.get_project(project_id)
                projects[project_id] = {"name": project.name, "tasks": []}
            except:
                projects[project_id] = {"name": "Unknown", "tasks": []}
        projects[project_id]["tasks"].append(task)

    # Generate report
    report = f"""# Daily Task Report - {today}

## Summary
- Overdue: {len(overdue)}
- Due Today: {len(due_today)}
- High Priority (upcoming): {len(high_priority)}

## Overdue Tasks
"""
    for task in overdue:
        report += f"- [{priority_emoji(task.priority)}] {task.content} (Due: {task.due.string})\n"

    report += "\n## Today's Tasks by Project\n"
    for project_id, project_data in projects.items():
        report += f"\n### {project_data['name']}\n"
        for task in project_data["tasks"]:
            report += f"- [{priority_emoji(task.priority)}] {task.content}\n"

    report += "\n## High Priority (Upcoming)\n"
    for task in high_priority[:5]:
        due = task.due.string if task.due else "No date"
        report += f"- [{priority_emoji(task.priority)}] {task.content} (Due: {due})\n"

    return report

def priority_emoji(priority):
    """Convert priority number to visual indicator"""
    return {4: "!", 3: "*", 2: "-", 1: " "}.get(priority, " ")

if __name__ == "__main__":
    report = generate_daily_report()
    print(report)

    # Optionally save to file
    filename = f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {filename}")
```

## Integration Examples

### Integration with Slack

```python
#!/usr/bin/env python3
"""slack_todoist.py - Post Todoist tasks to Slack"""

import os
import requests
from todoist_api_python import TodoistAPI

TODOIST_API_KEY = os.environ["TODOIST_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

api = TodoistAPI(TODOIST_API_KEY)

def post_daily_tasks_to_slack():
    """Post today's tasks to Slack"""
    tasks = api.get_tasks(filter="today")

    if not tasks:
        message = "No tasks due today!"
    else:
        task_list = "\n".join([f"- {t.content}" for t in tasks])
        message = f"*Tasks for Today ({len(tasks)}):*\n{task_list}"

    payload = {
        "text": message,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    if post_daily_tasks_to_slack():
        print("Posted to Slack successfully")
    else:
        print("Failed to post to Slack")
```

### Integration with Calendar (Google Calendar)

```python
#!/usr/bin/env python3
"""calendar_sync.py - Sync Todoist tasks with Google Calendar"""

from todoist_api_python import TodoistAPI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

api = TodoistAPI(os.environ["TODOIST_API_KEY"])

def sync_tasks_to_calendar():
    """Sync tasks with due dates to Google Calendar"""
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("calendar", "v3", credentials=creds)

    # Get tasks with due dates in next 7 days
    tasks = api.get_tasks(filter="next 7 days")

    for task in tasks:
        if not task.due:
            continue

        # Check if event already exists
        existing = find_existing_event(service, task.id)
        if existing:
            continue

        # Create calendar event
        event = {
            "summary": task.content,
            "description": f"Todoist Task ID: {task.id}\nPriority: {task.priority}",
            "start": {
                "date": task.due.date,
            },
            "end": {
                "date": task.due.date,
            },
            "extendedProperties": {
                "private": {
                    "todoist_id": task.id
                }
            }
        }

        service.events().insert(calendarId="primary", body=event).execute()
        print(f"Created calendar event: {task.content}")

def find_existing_event(service, todoist_id):
    """Find existing calendar event for Todoist task"""
    events = service.events().list(
        calendarId="primary",
        privateExtendedProperty=f"todoist_id={todoist_id}"
    ).execute()
    return events.get("items", [])
```

## Best Practices

### 1. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=50):
    """Decorator to rate limit API calls"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=50)
def api_call(func, *args, **kwargs):
    return func(*args, **kwargs)
```

### 2. Error Handling

```python
from todoist_api_python import TodoistAPI
import requests

def safe_api_call(func, *args, max_retries=3, **kwargs):
    """Execute API call with retry logic"""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # Rate limited
                wait_time = int(e.response.headers.get("Retry-After", 60))
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            elif e.response.status_code >= 500:
                # Server error, retry
                time.sleep(2 ** attempt)
            else:
                raise
        except requests.exceptions.ConnectionError:
            time.sleep(2 ** attempt)

    raise Exception(f"Failed after {max_retries} retries")
```

### 3. Batch Operations

```python
def batch_create_tasks(tasks, batch_size=50):
    """Create tasks in batches to avoid rate limits"""
    results = []
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_results = sync_batch_add(batch)
        results.extend(batch_results)
        if i + batch_size < len(tasks):
            time.sleep(1)  # Brief pause between batches
    return results
```

### 4. Caching

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "todoist"
CACHE_TTL = timedelta(minutes=5)

def get_cached_or_fetch(key, fetch_func, ttl=CACHE_TTL):
    """Get from cache or fetch fresh data"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{key}.json"

    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at < ttl:
            return data["value"]

    value = fetch_func()
    cache_data = {
        "cached_at": datetime.now().isoformat(),
        "value": value
    }
    cache_file.write_text(json.dumps(cache_data, default=str))
    return value
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```python
# Verify your API token
curl -s -X GET "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_API_KEY"

# Check if token is set correctly
echo $TODOIST_API_KEY

# Regenerate token at:
# https://todoist.com/app/settings/integrations/developer
```

**Issue: 429 Too Many Requests**
```python
# Implement exponential backoff
import time

def retry_with_backoff(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e):
                wait = 2 ** i
                print(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
            else:
                raise
```

**Issue: Task not appearing**
```python
# Check if task was created in different project
all_tasks = api.get_tasks()
for task in all_tasks:
    if "keyword" in task.content.lower():
        print(f"Found: {task.content} in project {task.project_id}")
```

**Issue: Due dates not parsing**
```python
# Use explicit date format
api.add_task(
    content="Test task",
    due_date="2025-01-20"  # ISO format
)

# Or use due_datetime for specific time
api.add_task(
    content="Test task",
    due_datetime="2025-01-20T14:00:00Z"  # ISO with time
)
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-17 | Initial release with comprehensive Todoist API coverage |

## Resources

- [Todoist REST API Documentation](https://developer.todoist.com/rest/v2/)
- [Todoist Sync API Documentation](https://developer.todoist.com/sync/v9/)
- [Todoist Python SDK](https://github.com/Doist/todoist-api-python)
- [Filter Query Syntax](https://todoist.com/help/articles/introduction-to-filters)
- [Webhook Events Reference](https://developer.todoist.com/sync/v9/#webhooks)

---

*This skill enables powerful task management automation through Todoist's comprehensive API, supporting projects, tasks, labels, filters, webhooks, and batch operations.*
