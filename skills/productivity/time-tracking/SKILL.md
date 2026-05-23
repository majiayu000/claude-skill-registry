---
name: time-tracking
version: 1.0.0
description: Time tracking integration patterns with RescueTime and Toggl APIs for automated time entry, reporting, analytics, and project/task attribution
author: workspace-hub
category: productivity
type: skill
capabilities:
  - Time entry automation
  - Project and task attribution
  - Productivity analytics
  - Reporting and dashboards
  - RescueTime API integration
  - Toggl Track API integration
  - Automated time logging
  - Focus time analysis
  - Billable hours tracking
  - Team time management
tools:
  - toggl-api
  - rescuetime-api
  - curl
  - python-requests
tags: [time-tracking, toggl, rescuetime, productivity, automation, reporting, analytics, billing, project-management]
platforms: [rest-api, python]
related_skills:
  - todoist-api
  - trello-api
  - notion-api
  - api-integration
---

# Time Tracking Integration Skill

Master time tracking integrations with RescueTime and Toggl Track APIs for automated time entry, comprehensive reporting, productivity analytics, and project/task attribution. Build powerful time management automations and dashboards.

## When to Use This Skill

### USE Time Tracking APIs when:
- **Automating time entries** - Log time from scripts, CI/CD, or other tools
- **Building productivity dashboards** - Aggregate time data for analysis
- **Project billing** - Track billable hours automatically
- **Focus time analysis** - Understand productivity patterns
- **Team time management** - Aggregate team time data
- **Integration pipelines** - Connect time tracking with task managers
- **Automated reporting** - Generate time reports programmatically
- **Custom analytics** - Build specialized productivity insights

### DON'T USE Time Tracking APIs when:
- **Simple manual tracking** - Use native apps instead
- **Real-time monitoring** - APIs have rate limits
- **Invasive employee surveillance** - Ethical concerns
- **Complex invoicing** - Use dedicated billing software

## Prerequisites

### Toggl Track Setup

```bash
# Get API token from:
# https://track.toggl.com/profile (scroll to API Token)

# Set environment variable
export TOGGL_API_TOKEN="your-api-token"

# Toggl uses HTTP Basic Auth with token as username, "api_token" as password
# Or you can use the token directly

# Verify authentication
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/me" | jq '.fullname'
```

### RescueTime Setup

```bash
# Get API Key from:
# https://www.rescuetime.com/anapi/manage

# Set environment variable
export RESCUETIME_API_KEY="your-api-key"

# Verify authentication
curl -s "https://www.rescuetime.com/anapi/data?key=$RESCUETIME_API_KEY&format=json&restrict_kind=overview" | jq
```

### Python Setup

```bash
# Install dependencies
pip install requests python-dateutil pandas

# Using uv
uv pip install requests python-dateutil pandas

# Optional: For Toggl SDK
pip install toggl-python

# Verify
python -c "import requests; print('Ready for time tracking integration!')"
```

## Core Capabilities

### 1. Toggl Track - Time Entries

**REST API - Time Entries:**
```bash
# Get current running time entry
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/me/time_entries/current" | jq

# Get recent time entries (last 7 days by default)
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/me/time_entries" | jq

# Get time entries with date range
START_DATE=$(date -d "7 days ago" +%Y-%m-%dT00:00:00Z)
END_DATE=$(date +%Y-%m-%dT23:59:59Z)

curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/me/time_entries?start_date=$START_DATE&end_date=$END_DATE" | jq

# Start a time entry (timer)
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/time_entries" \
    -d '{
        "created_with": "api",
        "description": "Working on project documentation",
        "tags": ["documentation", "writing"],
        "billable": false,
        "workspace_id": WORKSPACE_ID,
        "project_id": PROJECT_ID,
        "start": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
        "duration": -1
    }' | jq

# Stop running time entry
curl -s -X PATCH -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/time_entries/TIME_ENTRY_ID/stop" | jq

# Create completed time entry
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/time_entries" \
    -d '{
        "created_with": "api",
        "description": "Code review session",
        "workspace_id": WORKSPACE_ID,
        "project_id": PROJECT_ID,
        "start": "2025-01-15T09:00:00.000Z",
        "duration": 3600,
        "tags": ["review", "development"]
    }' | jq

# Update time entry
curl -s -X PUT -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/time_entries/TIME_ENTRY_ID" \
    -d '{
        "description": "Updated description",
        "tags": ["updated-tag"]
    }' | jq

# Delete time entry
curl -s -X DELETE -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/time_entries/TIME_ENTRY_ID"
```

**Python - Toggl Time Entries:**
```python
import requests
from datetime import datetime, timedelta
from base64 import b64encode
import os

class TogglClient:
    """Toggl Track API client."""

    BASE_URL = "https://api.track.toggl.com/api/v9"

    def __init__(self, api_token=None):
        self.api_token = api_token or os.environ.get("TOGGL_API_TOKEN")
        self.auth = (self.api_token, "api_token")

    def _request(self, method, endpoint, data=None):
        """Make API request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(
            method,
            url,
            auth=self.auth,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json() if response.text else None

    def get_me(self):
        """Get current user info."""
        return self._request("GET", "/me")

    def get_workspaces(self):
        """Get user's workspaces."""
        return self._request("GET", "/workspaces")

    def get_current_entry(self):
        """Get currently running time entry."""
        return self._request("GET", "/me/time_entries/current")

    def get_time_entries(self, start_date=None, end_date=None):
        """Get time entries within date range."""
        params = []
        if start_date:
            params.append(f"start_date={start_date.isoformat()}Z")
        if end_date:
            params.append(f"end_date={end_date.isoformat()}Z")

        query = f"?{'&'.join(params)}" if params else ""
        return self._request("GET", f"/me/time_entries{query}")

    def start_timer(self, workspace_id, description, project_id=None, tags=None, billable=False):
        """Start a new timer."""
        data = {
            "created_with": "python_api",
            "description": description,
            "workspace_id": workspace_id,
            "billable": billable,
            "start": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "duration": -1  # -1 indicates running timer
        }

        if project_id:
            data["project_id"] = project_id
        if tags:
            data["tags"] = tags

        return self._request(
            "POST",
            f"/workspaces/{workspace_id}/time_entries",
            data
        )

    def stop_timer(self, workspace_id, entry_id):
        """Stop a running timer."""
        return self._request(
            "PATCH",
            f"/workspaces/{workspace_id}/time_entries/{entry_id}/stop"
        )

    def create_time_entry(
        self,
        workspace_id,
        description,
        start_time,
        duration_seconds,
        project_id=None,
        tags=None,
        billable=False
    ):
        """Create a completed time entry."""
        data = {
            "created_with": "python_api",
            "description": description,
            "workspace_id": workspace_id,
            "start": start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "duration": duration_seconds,
            "billable": billable
        }

        if project_id:
            data["project_id"] = project_id
        if tags:
            data["tags"] = tags

        return self._request(
            "POST",
            f"/workspaces/{workspace_id}/time_entries",
            data
        )

    def update_time_entry(self, workspace_id, entry_id, **kwargs):
        """Update an existing time entry."""
        return self._request(
            "PUT",
            f"/workspaces/{workspace_id}/time_entries/{entry_id}",
            kwargs
        )

    def delete_time_entry(self, workspace_id, entry_id):
        """Delete a time entry."""
        return self._request(
            "DELETE",
            f"/workspaces/{workspace_id}/time_entries/{entry_id}"
        )


# Example usage
if __name__ == "__main__":
    client = TogglClient()

    # Get user info
    user = client.get_me()
    print(f"User: {user['fullname']}")

    # Get workspaces
    workspaces = client.get_workspaces()
    workspace_id = workspaces[0]["id"]
    print(f"Workspace: {workspaces[0]['name']}")

    # Start timer
    entry = client.start_timer(
        workspace_id=workspace_id,
        description="Working on API integration",
        tags=["development", "api"]
    )
    print(f"Started timer: {entry['id']}")

    # Get current timer
    current = client.get_current_entry()
    if current:
        print(f"Running: {current['description']}")

    # Stop timer
    stopped = client.stop_timer(workspace_id, entry["id"])
    print(f"Stopped: Duration {stopped['duration']} seconds")
```

### 2. Toggl Track - Projects and Clients

**REST API - Projects:**
```bash
# Get workspace projects
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/projects" | jq

# Create project
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/projects" \
    -d '{
        "name": "Client Website Redesign",
        "color": "#0b83d9",
        "is_private": false,
        "active": true,
        "client_id": CLIENT_ID,
        "billable": true,
        "estimated_hours": 100
    }' | jq

# Get clients
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/clients" | jq

# Create client
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/clients" \
    -d '{
        "name": "Acme Corporation",
        "notes": "Primary contact: John Doe"
    }' | jq

# Get tags
curl -s -u "$TOGGL_API_TOKEN:api_token" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/tags" | jq

# Create tag
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/api/v9/workspaces/WORKSPACE_ID/tags" \
    -d '{"name": "urgent"}' | jq
```

**Python - Projects and Clients:**
```python
def get_projects(self, workspace_id):
    """Get all projects in workspace."""
    return self._request("GET", f"/workspaces/{workspace_id}/projects")

def create_project(
    self,
    workspace_id,
    name,
    client_id=None,
    color="#0b83d9",
    billable=False,
    estimated_hours=None
):
    """Create a new project."""
    data = {
        "name": name,
        "color": color,
        "billable": billable,
        "active": True
    }

    if client_id:
        data["client_id"] = client_id
    if estimated_hours:
        data["estimated_hours"] = estimated_hours

    return self._request(
        "POST",
        f"/workspaces/{workspace_id}/projects",
        data
    )

def get_clients(self, workspace_id):
    """Get all clients in workspace."""
    return self._request("GET", f"/workspaces/{workspace_id}/clients")

def create_client(self, workspace_id, name, notes=None):
    """Create a new client."""
    data = {"name": name}
    if notes:
        data["notes"] = notes

    return self._request(
        "POST",
        f"/workspaces/{workspace_id}/clients",
        data
    )
```

### 3. Toggl Track - Reports

**Reports API:**
```bash
# Summary report
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/reports/api/v3/workspace/WORKSPACE_ID/summary/time_entries" \
    -d '{
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "grouping": "projects",
        "sub_grouping": "users"
    }' | jq

# Detailed report
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/reports/api/v3/workspace/WORKSPACE_ID/search/time_entries" \
    -d '{
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "page_size": 50,
        "first_row_number": 0
    }' | jq

# Weekly report
curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
    -H "Content-Type: application/json" \
    "https://api.track.toggl.com/reports/api/v3/workspace/WORKSPACE_ID/weekly/time_entries" \
    -d '{
        "start_date": "2025-01-06",
        "end_date": "2025-01-12",
        "grouping": "projects"
    }' | jq
```

**Python - Reports:**
```python
class TogglReports:
    """Toggl Reports API client."""

    REPORTS_URL = "https://api.track.toggl.com/reports/api/v3"

    def __init__(self, api_token=None):
        self.api_token = api_token or os.environ.get("TOGGL_API_TOKEN")
        self.auth = (self.api_token, "api_token")

    def _request(self, method, endpoint, data=None):
        """Make API request."""
        url = f"{self.REPORTS_URL}{endpoint}"
        response = requests.request(
            method,
            url,
            auth=self.auth,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    def summary_report(
        self,
        workspace_id,
        start_date,
        end_date,
        grouping="projects",
        sub_grouping=None,
        project_ids=None,
        user_ids=None
    ):
        """Generate summary report."""
        data = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "grouping": grouping
        }

        if sub_grouping:
            data["sub_grouping"] = sub_grouping
        if project_ids:
            data["project_ids"] = project_ids
        if user_ids:
            data["user_ids"] = user_ids

        return self._request(
            "POST",
            f"/workspace/{workspace_id}/summary/time_entries",
            data
        )

    def detailed_report(
        self,
        workspace_id,
        start_date,
        end_date,
        page_size=50,
        first_row=0
    ):
        """Generate detailed report with pagination."""
        data = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "page_size": page_size,
            "first_row_number": first_row
        }

        return self._request(
            "POST",
            f"/workspace/{workspace_id}/search/time_entries",
            data
        )

    def weekly_report(
        self,
        workspace_id,
        start_date,
        end_date,
        grouping="projects"
    ):
        """Generate weekly report."""
        data = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "grouping": grouping
        }

        return self._request(
            "POST",
            f"/workspace/{workspace_id}/weekly/time_entries",
            data
        )


# Example usage
if __name__ == "__main__":
    reports = TogglReports()
    workspace_id = 12345678

    # Get summary report
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 31)

    summary = reports.summary_report(
        workspace_id=workspace_id,
        start_date=start,
        end_date=end,
        grouping="projects"
    )

    print("Summary Report:")
    for group in summary.get("groups", []):
        total_hours = group.get("seconds", 0) / 3600
        print(f"  {group.get('id')}: {total_hours:.1f} hours")
```

### 4. RescueTime - Data Retrieval

**REST API - Analytics:**
```bash
# Get summary data
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "perspective=rank" \
    -d "resolution_time=day" \
    -d "restrict_kind=overview" | jq

# Get data for specific date range
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "restrict_begin=2025-01-01" \
    -d "restrict_end=2025-01-31" \
    -d "restrict_kind=overview" | jq

# Get activity data by category
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "restrict_kind=category" \
    -d "resolution_time=week" | jq

# Get productivity data
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "restrict_kind=productivity" | jq

# Get activity details
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "restrict_kind=activity" \
    -d "resolution_time=day" | jq

# Get efficiency data (requires Premium)
curl -s "https://www.rescuetime.com/anapi/data" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "format=json" \
    -d "restrict_kind=efficiency" | jq
```

**Python - RescueTime Client:**
```python
import requests
from datetime import datetime, timedelta
import os

class RescueTimeClient:
    """RescueTime API client."""

    BASE_URL = "https://www.rescuetime.com/anapi"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("RESCUETIME_API_KEY")

    def _request(self, endpoint, params=None):
        """Make API request."""
        params = params or {}
        params["key"] = self.api_key
        params["format"] = "json"

        response = requests.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_daily_summary(self, date=None):
        """Get daily summary data."""
        params = {
            "perspective": "rank",
            "resolution_time": "day",
            "restrict_kind": "overview"
        }

        if date:
            params["restrict_begin"] = date.strftime("%Y-%m-%d")
            params["restrict_end"] = date.strftime("%Y-%m-%d")

        return self._request("data", params)

    def get_date_range_data(
        self,
        start_date,
        end_date,
        restrict_kind="overview",
        resolution="day"
    ):
        """Get data for date range."""
        params = {
            "restrict_begin": start_date.strftime("%Y-%m-%d"),
            "restrict_end": end_date.strftime("%Y-%m-%d"),
            "restrict_kind": restrict_kind,
            "resolution_time": resolution
        }

        return self._request("data", params)

    def get_productivity_data(self, start_date=None, end_date=None):
        """Get productivity scores."""
        params = {"restrict_kind": "productivity"}

        if start_date:
            params["restrict_begin"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["restrict_end"] = end_date.strftime("%Y-%m-%d")

        return self._request("data", params)

    def get_category_data(
        self,
        start_date=None,
        end_date=None,
        resolution="day"
    ):
        """Get data grouped by category."""
        params = {
            "restrict_kind": "category",
            "resolution_time": resolution
        }

        if start_date:
            params["restrict_begin"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["restrict_end"] = end_date.strftime("%Y-%m-%d")

        return self._request("data", params)

    def get_activity_data(
        self,
        start_date=None,
        end_date=None,
        resolution="day"
    ):
        """Get detailed activity data."""
        params = {
            "restrict_kind": "activity",
            "resolution_time": resolution
        }

        if start_date:
            params["restrict_begin"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["restrict_end"] = end_date.strftime("%Y-%m-%d")

        return self._request("data", params)

    def get_focus_time(self, start_date=None, end_date=None):
        """Calculate focus time from activities."""
        productivity = self.get_productivity_data(start_date, end_date)

        focus_time = 0
        total_time = 0

        for row in productivity.get("rows", []):
            # row format: [rank, time_seconds, productivity]
            time_seconds = row[1]
            productivity_score = row[2]  # -2 to 2

            total_time += time_seconds
            if productivity_score >= 1:  # Productive or very productive
                focus_time += time_seconds

        return {
            "focus_time_seconds": focus_time,
            "focus_time_hours": focus_time / 3600,
            "total_time_seconds": total_time,
            "total_time_hours": total_time / 3600,
            "focus_percentage": (focus_time / total_time * 100) if total_time > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    client = RescueTimeClient()

    # Get today's summary
    today = client.get_daily_summary()
    print("Today's Activity:")
    for row in today.get("rows", [])[:5]:
        print(f"  {row[3]}: {row[1] / 60:.0f} minutes")

    # Get focus time for last week
    start = datetime.now() - timedelta(days=7)
    end = datetime.now()

    focus = client.get_focus_time(start, end)
    print(f"\nFocus Time (Last 7 Days):")
    print(f"  Focus: {focus['focus_time_hours']:.1f} hours")
    print(f"  Total: {focus['total_time_hours']:.1f} hours")
    print(f"  Focus Rate: {focus['focus_percentage']:.1f}%")
```

### 5. RescueTime - FocusTime Triggers

**FocusTime API:**
```bash
# Start FocusTime session (requires Premium)
curl -s -X POST "https://www.rescuetime.com/anapi/focustime/start" \
    -d "key=$RESCUETIME_API_KEY" \
    -d "duration=60" | jq  # 60 minutes

# End FocusTime session
curl -s -X POST "https://www.rescuetime.com/anapi/focustime/end" \
    -d "key=$RESCUETIME_API_KEY" | jq

# Get current FocusTime status
curl -s "https://www.rescuetime.com/anapi/focustime/status" \
    -d "key=$RESCUETIME_API_KEY" | jq
```

**Python - FocusTime:**
```python
class RescueTimeFocusTime:
    """RescueTime FocusTime API client (Premium required)."""

    BASE_URL = "https://www.rescuetime.com/anapi/focustime"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("RESCUETIME_API_KEY")

    def start_focus(self, duration_minutes=60):
        """Start a FocusTime session."""
        response = requests.post(
            f"{self.BASE_URL}/start",
            data={
                "key": self.api_key,
                "duration": duration_minutes
            }
        )
        return response.json()

    def end_focus(self):
        """End current FocusTime session."""
        response = requests.post(
            f"{self.BASE_URL}/end",
            data={"key": self.api_key}
        )
        return response.json()

    def get_status(self):
        """Get current FocusTime status."""
        response = requests.get(
            f"{self.BASE_URL}/status",
            params={"key": self.api_key}
        )
        return response.json()
```

### 6. Automated Time Logging

**Log Time from Scripts:**
```python
#!/usr/bin/env python3
"""auto_time_logger.py - Automated time logging"""

import os
import subprocess
from datetime import datetime, timedelta
from toggl_client import TogglClient  # From earlier example

def log_git_commit_time(repo_path, workspace_id, project_id=None):
    """
    Log time entries based on git commits.
    Estimates time between commits.
    """
    client = TogglClient()

    # Get recent commits
    result = subprocess.run(
        ["git", "-C", repo_path, "log", "--format=%H|%s|%ai", "-n", "20"],
        capture_output=True,
        text=True
    )

    commits = []
    for line in result.stdout.strip().split("\n"):
        if "|" in line:
            hash_val, message, date_str = line.split("|", 2)
            commit_date = datetime.strptime(
                date_str.strip()[:19],
                "%Y-%m-%d %H:%M:%S"
            )
            commits.append({
                "hash": hash_val,
                "message": message,
                "date": commit_date
            })

    # Create time entries between commits
    for i in range(len(commits) - 1):
        current = commits[i]
        previous = commits[i + 1]

        duration = (current["date"] - previous["date"]).total_seconds()

        # Cap at 4 hours max
        duration = min(duration, 4 * 3600)

        # Skip very short intervals
        if duration < 300:  # Less than 5 minutes
            continue

        entry = client.create_time_entry(
            workspace_id=workspace_id,
            description=f"Git: {current['message'][:100]}",
            start_time=previous["date"],
            duration_seconds=int(duration),
            project_id=project_id,
            tags=["git", "auto-logged"]
        )

        print(f"Logged: {current['message'][:50]}... ({duration/3600:.1f}h)")


def log_pomodoro_session(
    workspace_id,
    description,
    project_id=None,
    duration_minutes=25
):
    """Log a completed Pomodoro session."""
    client = TogglClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    entry = client.create_time_entry(
        workspace_id=workspace_id,
        description=description,
        start_time=start_time,
        duration_seconds=duration_minutes * 60,
        project_id=project_id,
        tags=["pomodoro"]
    )

    print(f"Logged Pomodoro: {description} ({duration_minutes} min)")
    return entry


def log_meeting(
    workspace_id,
    title,
    start_time,
    end_time,
    project_id=None
):
    """Log a meeting time entry."""
    client = TogglClient()

    duration = (end_time - start_time).total_seconds()

    entry = client.create_time_entry(
        workspace_id=workspace_id,
        description=f"Meeting: {title}",
        start_time=start_time,
        duration_seconds=int(duration),
        project_id=project_id,
        tags=["meeting"]
    )

    print(f"Logged meeting: {title} ({duration/3600:.1f}h)")
    return entry
```

## Complete Examples

### Example 1: Weekly Time Report Generator

```python
#!/usr/bin/env python3
"""weekly_report.py - Generate weekly time reports"""

import os
from datetime import datetime, timedelta
from collections import defaultdict
import json

# Assuming TogglClient and TogglReports from earlier examples

class WeeklyReportGenerator:
    """Generate comprehensive weekly time reports."""

    def __init__(self, toggl_token=None, rescuetime_key=None):
        self.toggl = TogglClient(toggl_token)
        if rescuetime_key:
            self.rescuetime = RescueTimeClient(rescuetime_key)
        else:
            self.rescuetime = None

    def get_week_dates(self, weeks_ago=0):
        """Get start and end of a week."""
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday() + (7 * weeks_ago))
        end = start + timedelta(days=6)
        return datetime.combine(start, datetime.min.time()), \
               datetime.combine(end, datetime.max.time())

    def generate_toggl_report(self, start_date, end_date):
        """Generate Toggl time report."""
        entries = self.toggl.get_time_entries(start_date, end_date)

        # Aggregate by project and day
        by_project = defaultdict(float)
        by_day = defaultdict(float)
        by_tag = defaultdict(float)
        total_seconds = 0

        for entry in entries or []:
            duration = entry.get("duration", 0)
            if duration < 0:  # Running entry
                duration = (datetime.utcnow() - datetime.fromisoformat(
                    entry["start"].replace("Z", "")
                )).total_seconds()

            total_seconds += duration

            # By project
            project_id = entry.get("project_id", "No Project")
            by_project[project_id] += duration

            # By day
            day = entry["start"][:10]
            by_day[day] += duration

            # By tags
            for tag in entry.get("tags", []):
                by_tag[tag] += duration

        return {
            "total_hours": total_seconds / 3600,
            "by_project": {k: v / 3600 for k, v in by_project.items()},
            "by_day": {k: v / 3600 for k, v in sorted(by_day.items())},
            "by_tag": {k: v / 3600 for k, v in by_tag.items()},
            "entry_count": len(entries or [])
        }

    def generate_rescuetime_report(self, start_date, end_date):
        """Generate RescueTime productivity report."""
        if not self.rescuetime:
            return None

        # Get category data
        category_data = self.rescuetime.get_category_data(start_date, end_date)

        categories = defaultdict(float)
        for row in category_data.get("rows", []):
            category = row[3]  # Category name
            seconds = row[1]
            categories[category] += seconds / 3600

        # Get productivity data
        focus = self.rescuetime.get_focus_time(start_date, end_date)

        return {
            "focus_hours": focus["focus_time_hours"],
            "total_hours": focus["total_time_hours"],
            "focus_percentage": focus["focus_percentage"],
            "by_category": dict(sorted(
                categories.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10])
        }

    def generate_full_report(self, weeks_ago=0):
        """Generate complete weekly report."""
        start, end = self.get_week_dates(weeks_ago)

        report = {
            "period": {
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                "week_number": start.isocalendar()[1]
            },
            "generated_at": datetime.now().isoformat(),
            "toggl": self.generate_toggl_report(start, end),
            "rescuetime": self.generate_rescuetime_report(start, end)
        }

        return report

    def generate_markdown_report(self, report):
        """Generate markdown formatted report."""
        period = report["period"]

        md = f"""# Weekly Time Report

**Week {period['week_number']}:** {period['start']} to {period['end']}
**Generated:** {report['generated_at'][:10]}

## Tracked Time (Toggl)

| Metric | Value |
|--------|-------|
| Total Hours | {report['toggl']['total_hours']:.1f} |
| Time Entries | {report['toggl']['entry_count']} |

### Hours by Day

| Day | Hours |
|-----|-------|
"""

        for day, hours in report["toggl"]["by_day"].items():
            md += f"| {day} | {hours:.1f} |\n"

        md += "\n### Hours by Project\n\n"
        for project, hours in sorted(
            report["toggl"]["by_project"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            md += f"- **{project}**: {hours:.1f} hours\n"

        if report["rescuetime"]:
            rt = report["rescuetime"]
            md += f"""

## Productivity (RescueTime)

| Metric | Value |
|--------|-------|
| Focus Time | {rt['focus_hours']:.1f} hours |
| Total Tracked | {rt['total_hours']:.1f} hours |
| Focus Rate | {rt['focus_percentage']:.1f}% |

### Top Categories

"""
            for category, hours in list(rt["by_category"].items())[:5]:
                md += f"- **{category}**: {hours:.1f} hours\n"

        return md


# Example usage
if __name__ == "__main__":
    generator = WeeklyReportGenerator(
        toggl_token=os.environ.get("TOGGL_API_TOKEN"),
        rescuetime_key=os.environ.get("RESCUETIME_API_KEY")
    )

    # Generate report for current week
    report = generator.generate_full_report(weeks_ago=0)

    # Save JSON
    with open("weekly_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Generate markdown
    md_report = generator.generate_markdown_report(report)
    with open("weekly_report.md", "w") as f:
        f.write(md_report)

    print("Weekly report generated!")
    print(f"Total tracked: {report['toggl']['total_hours']:.1f} hours")
```

### Example 2: Project Time Attribution

```python
#!/usr/bin/env python3
"""project_attribution.py - Attribute time to projects automatically"""

import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

class ProjectTimeAttributor:
    """Automatically attribute time entries to projects."""

    def __init__(self, toggl_token):
        self.toggl = TogglClient(toggl_token)
        self.workspace_id = None
        self.projects = {}
        self.rules = []

    def load_workspace(self):
        """Load workspace and projects."""
        workspaces = self.toggl.get_workspaces()
        self.workspace_id = workspaces[0]["id"]

        projects = self.toggl.get_projects(self.workspace_id)
        self.projects = {p["name"]: p["id"] for p in projects}

        print(f"Loaded {len(self.projects)} projects")

    def add_rule(self, pattern, project_name, tags=None):
        """
        Add attribution rule.

        Args:
            pattern: Regex pattern to match description
            project_name: Project to assign
            tags: Optional tags to add
        """
        if project_name not in self.projects:
            print(f"Warning: Project '{project_name}' not found")
            return

        self.rules.append({
            "pattern": re.compile(pattern, re.IGNORECASE),
            "project_id": self.projects[project_name],
            "project_name": project_name,
            "tags": tags or []
        })

    def process_entries(self, days_back=7, dry_run=True):
        """
        Process time entries and apply attribution rules.

        Args:
            days_back: Number of days to process
            dry_run: If True, don't make changes

        Returns:
            Summary of changes
        """
        start = datetime.utcnow() - timedelta(days=days_back)
        end = datetime.utcnow()

        entries = self.toggl.get_time_entries(start, end)

        changes = {
            "processed": 0,
            "attributed": 0,
            "skipped": 0,
            "details": []
        }

        for entry in entries or []:
            changes["processed"] += 1

            # Skip if already has project
            if entry.get("project_id"):
                changes["skipped"] += 1
                continue

            description = entry.get("description", "")

            # Try each rule
            for rule in self.rules:
                if rule["pattern"].search(description):
                    change = {
                        "entry_id": entry["id"],
                        "description": description[:50],
                        "project": rule["project_name"],
                        "tags": rule["tags"]
                    }

                    if not dry_run:
                        update_data = {"project_id": rule["project_id"]}
                        if rule["tags"]:
                            existing_tags = entry.get("tags", [])
                            update_data["tags"] = list(set(existing_tags + rule["tags"]))

                        self.toggl.update_time_entry(
                            self.workspace_id,
                            entry["id"],
                            **update_data
                        )

                    changes["attributed"] += 1
                    changes["details"].append(change)
                    break

        return changes


# Example usage
if __name__ == "__main__":
    attributor = ProjectTimeAttributor(os.environ["TOGGL_API_TOKEN"])
    attributor.load_workspace()

    # Define attribution rules
    attributor.add_rule(
        r"(meeting|standup|sync)",
        "Internal - Meetings",
        tags=["meeting"]
    )

    attributor.add_rule(
        r"(code review|pr review|review)",
        "Development",
        tags=["review"]
    )

    attributor.add_rule(
        r"(bug|fix|hotfix)",
        "Development",
        tags=["bugfix"]
    )

    attributor.add_rule(
        r"(docs|documentation|readme)",
        "Documentation",
        tags=["docs"]
    )

    attributor.add_rule(
        r"(email|slack|communication)",
        "Internal - Communication",
        tags=["communication"]
    )

    # Process entries (dry run first)
    print("\n=== DRY RUN ===")
    changes = attributor.process_entries(days_back=7, dry_run=True)

    print(f"Processed: {changes['processed']}")
    print(f"Would attribute: {changes['attributed']}")
    print(f"Already assigned: {changes['skipped']}")

    if changes["details"]:
        print("\nChanges:")
        for change in changes["details"][:10]:
            print(f"  {change['description'][:30]}... -> {change['project']}")

    # Uncomment to apply changes
    # print("\n=== APPLYING CHANGES ===")
    # changes = attributor.process_entries(days_back=7, dry_run=False)
```

### Example 3: Productivity Dashboard Data

```python
#!/usr/bin/env python3
"""productivity_dashboard.py - Generate dashboard data"""

import os
from datetime import datetime, timedelta
import json

class ProductivityDashboard:
    """Generate data for productivity dashboard."""

    def __init__(self, toggl_token, rescuetime_key=None):
        self.toggl = TogglClient(toggl_token)
        self.rescuetime = RescueTimeClient(rescuetime_key) if rescuetime_key else None

    def get_daily_metrics(self, date=None):
        """Get metrics for a single day."""
        if date is None:
            date = datetime.now().date()

        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())

        metrics = {
            "date": date.isoformat(),
            "toggl": {},
            "rescuetime": {}
        }

        # Toggl metrics
        entries = self.toggl.get_time_entries(start, end) or []
        total_seconds = sum(
            e.get("duration", 0) for e in entries
            if e.get("duration", 0) > 0
        )

        metrics["toggl"] = {
            "total_hours": total_seconds / 3600,
            "entry_count": len(entries),
            "billable_hours": sum(
                e.get("duration", 0) / 3600
                for e in entries
                if e.get("billable") and e.get("duration", 0) > 0
            )
        }

        # RescueTime metrics
        if self.rescuetime:
            focus = self.rescuetime.get_focus_time(
                datetime.combine(date, datetime.min.time()),
                datetime.combine(date, datetime.max.time())
            )

            metrics["rescuetime"] = {
                "focus_hours": focus["focus_time_hours"],
                "total_hours": focus["total_time_hours"],
                "focus_rate": focus["focus_percentage"]
            }

        return metrics

    def get_weekly_trend(self, weeks=4):
        """Get weekly trend data."""
        trends = []
        today = datetime.now().date()

        for week_offset in range(weeks):
            week_start = today - timedelta(
                days=today.weekday() + (7 * week_offset)
            )
            week_end = week_start + timedelta(days=6)

            start_dt = datetime.combine(week_start, datetime.min.time())
            end_dt = datetime.combine(week_end, datetime.max.time())

            # Toggl data
            entries = self.toggl.get_time_entries(start_dt, end_dt) or []
            total_hours = sum(
                e.get("duration", 0) / 3600
                for e in entries
                if e.get("duration", 0) > 0
            )

            week_data = {
                "week_start": week_start.isoformat(),
                "week_number": week_start.isocalendar()[1],
                "toggl_hours": round(total_hours, 1)
            }

            # RescueTime data
            if self.rescuetime:
                focus = self.rescuetime.get_focus_time(start_dt, end_dt)
                week_data["focus_hours"] = round(focus["focus_time_hours"], 1)
                week_data["focus_rate"] = round(focus["focus_percentage"], 1)

            trends.append(week_data)

        return list(reversed(trends))

    def get_project_breakdown(self, days=30):
        """Get time breakdown by project."""
        start = datetime.utcnow() - timedelta(days=days)
        end = datetime.utcnow()

        entries = self.toggl.get_time_entries(start, end) or []

        by_project = defaultdict(float)
        for entry in entries:
            duration = entry.get("duration", 0)
            if duration > 0:
                project = entry.get("project_id", "No Project")
                by_project[project] += duration / 3600

        # Sort by hours
        sorted_projects = sorted(
            by_project.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"project_id": p, "hours": round(h, 1)}
            for p, h in sorted_projects
        ]

    def generate_dashboard_data(self):
        """Generate complete dashboard data."""
        today = datetime.now().date()

        return {
            "generated_at": datetime.now().isoformat(),
            "today": self.get_daily_metrics(today),
            "yesterday": self.get_daily_metrics(today - timedelta(days=1)),
            "weekly_trend": self.get_weekly_trend(weeks=4),
            "project_breakdown": self.get_project_breakdown(days=30)
        }


# Example usage
if __name__ == "__main__":
    dashboard = ProductivityDashboard(
        toggl_token=os.environ["TOGGL_API_TOKEN"],
        rescuetime_key=os.environ.get("RESCUETIME_API_KEY")
    )

    data = dashboard.generate_dashboard_data()

    # Save dashboard data
    with open("dashboard_data.json", "w") as f:
        json.dump(data, f, indent=2)

    # Print summary
    print("Dashboard Data Generated")
    print(f"\nToday: {data['today']['toggl']['total_hours']:.1f} hours tracked")

    if data['today'].get('rescuetime'):
        print(f"Focus rate: {data['today']['rescuetime']['focus_rate']:.1f}%")

    print(f"\nWeekly Trend:")
    for week in data['weekly_trend']:
        print(f"  Week {week['week_number']}: {week['toggl_hours']} hours")
```

## Integration Examples

### Time Tracking with GitHub Actions

```yaml
# .github/workflows/log-time.yml
name: Log Development Time

on:
  push:
    branches: [main, develop]

jobs:
  log-time:
    runs-on: ubuntu-latest
    steps:
      - name: Log commit time to Toggl
        env:
          TOGGL_API_TOKEN: ${{ secrets.TOGGL_API_TOKEN }}
          TOGGL_WORKSPACE_ID: ${{ secrets.TOGGL_WORKSPACE_ID }}
          TOGGL_PROJECT_ID: ${{ secrets.TOGGL_PROJECT_ID }}
        run: |
          # Log 30 minute entry for each commit
          DESCRIPTION="Commit: ${{ github.event.head_commit.message }}"
          START_TIME=$(date -u -d '30 minutes ago' +%Y-%m-%dT%H:%M:%S.000Z)

          curl -s -X POST -u "$TOGGL_API_TOKEN:api_token" \
            -H "Content-Type: application/json" \
            "https://api.track.toggl.com/api/v9/workspaces/$TOGGL_WORKSPACE_ID/time_entries" \
            -d '{
              "created_with": "github_actions",
              "description": "'"${DESCRIPTION:0:100}"'",
              "workspace_id": '"$TOGGL_WORKSPACE_ID"',
              "project_id": '"$TOGGL_PROJECT_ID"',
              "start": "'"$START_TIME"'",
              "duration": 1800,
              "tags": ["github", "automated"]
            }'
```

### Slack Daily Summary

```python
#!/usr/bin/env python3
"""slack_time_summary.py - Post daily time summary to Slack"""

import os
import requests
from datetime import datetime, timedelta

def post_daily_summary(toggl_token, slack_webhook):
    """Post daily time summary to Slack."""
    toggl = TogglClient(toggl_token)

    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    entries = toggl.get_time_entries(start, end) or []

    total_hours = sum(
        e.get("duration", 0) / 3600
        for e in entries
        if e.get("duration", 0) > 0
    )

    # Build message
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Daily Time Summary - {today}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Hours:*\n{total_hours:.1f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Entries:*\n{len(entries)}"
                    }
                ]
            }
        ]
    }

    # Add top activities
    if entries:
        activities = "\n".join([
            f"- {e.get('description', 'No description')[:40]}: "
            f"{e.get('duration', 0)/3600:.1f}h"
            for e in sorted(entries, key=lambda x: x.get("duration", 0), reverse=True)[:5]
        ])

        message["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Top Activities:*\n{activities}"
            }
        })

    # Post to Slack
    response = requests.post(slack_webhook, json=message)
    return response.status_code == 200


if __name__ == "__main__":
    success = post_daily_summary(
        toggl_token=os.environ["TOGGL_API_TOKEN"],
        slack_webhook=os.environ["SLACK_WEBHOOK_URL"]
    )
    print("Posted to Slack" if success else "Failed to post")
```

## Best Practices

### 1. Handle Rate Limits

```python
import time
from functools import wraps

def rate_limited(max_per_second=1):
    """Rate limiting decorator."""
    min_interval = 1.0 / max_per_second
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator
```

### 2. Cache API Responses

```python
from functools import lru_cache
from datetime import datetime

@lru_cache(maxsize=100)
def get_projects_cached(workspace_id, cache_key=None):
    """Get projects with caching."""
    return toggl.get_projects(workspace_id)

# Invalidate cache daily
cache_key = datetime.now().strftime("%Y-%m-%d")
projects = get_projects_cached(workspace_id, cache_key)
```

### 3. Validate Time Entries

```python
def validate_time_entry(entry):
    """Validate time entry before creating."""
    if not entry.get("description"):
        raise ValueError("Description is required")

    duration = entry.get("duration", 0)
    if duration > 12 * 3600:  # More than 12 hours
        raise ValueError("Duration exceeds 12 hours")

    if duration < 60:  # Less than 1 minute
        raise ValueError("Duration too short")

    return True
```

## Troubleshooting

### Common Issues

**Issue: 403 Forbidden (Toggl)**
```python
# Check API token
curl -u "YOUR_TOKEN:api_token" "https://api.track.toggl.com/api/v9/me"

# Ensure token has proper permissions
# Regenerate token at: https://track.toggl.com/profile
```

**Issue: Empty response (RescueTime)**
```python
# Check if data exists for date range
# RescueTime only has data when the client is running

# Verify API key
curl "https://www.rescuetime.com/anapi/data?key=YOUR_KEY&format=json"
```

**Issue: Time zone issues**
```python
# Always use UTC for Toggl API
from datetime import datetime, timezone

start = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
```

**Issue: Duration calculation**
```python
# Running entries have negative duration
entry = toggl.get_current_entry()
if entry and entry.get("duration", 0) < 0:
    # Calculate actual duration
    start = datetime.fromisoformat(entry["start"].replace("Z", "+00:00"))
    duration = (datetime.now(timezone.utc) - start).total_seconds()
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Toggl Track API integration
  - RescueTime API integration
  - Time entry automation
  - Reports and analytics
  - Project attribution
  - Weekly report generator
  - Productivity dashboard
  - GitHub Actions integration
  - Slack integration

## Resources

- **Toggl Track API**: https://engineering.toggl.com/docs/
- **Toggl Reports API**: https://engineering.toggl.com/docs/reports
- **RescueTime API**: https://www.rescuetime.com/anapi/setup/documentation
- **py-toggl**: https://github.com/toggl/toggl_api_docs

---

**Automate your time tracking workflows with Toggl and RescueTime APIs!**
