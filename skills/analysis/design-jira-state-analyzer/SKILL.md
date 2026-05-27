---
name: design-jira-state-analyzer
description: |
  Designs and implements state transition analysis systems for tracking time spent in different states. Use when analyzing workflows with state changes (Jira, GitHub PRs, deployments, support tickets, etc.). Covers state machine fundamentals, temporal calculations, bottleneck detection, and business metrics. Trigger keywords: "state analysis", "duration tracking", "workflow metrics", "bottleneck", "cycle time", "state transitions", "time in status", "how long", "state duration", "workflow performance", "state machine", "changelog analysis", "SLA tracking", "process metrics".

---

# Design Jira State Analyzer

## When to Use This Skill

**Explicit Triggers:**
- "Analyze state transitions in Jira"
- "Calculate time spent in each status"
- "Find workflow bottlenecks"
- "Track cycle time for tickets"
- "Measure how long tickets stay in review"
- "Analyze workflow performance"
- "Design a state analyzer"
- "Calculate business hours in status"

**Implicit Triggers:**
- Questions about "how long does it take" for workflow stages
- Requests for SLA tracking or compliance analysis
- Need to optimize process flow or reduce delays
- Questions about which states slow down delivery
- Requests to measure team velocity or throughput
- Need to analyze deployment pipeline duration

**Use This Skill When:**
- Building systems to track state changes over time
- Analyzing workflows with discrete states (Jira, GitHub PRs, deployments, support tickets)
- Calculating temporal metrics (cycle time, lead time, flow efficiency)
- Detecting bottlenecks in multi-stage processes
- Implementing SLA monitoring and compliance tracking
- Extracting insights from audit logs or changelogs

**Do NOT Use This Skill When:**
- You need real-time event processing (use stream processing instead)
- Data lacks complete state history (partial data leads to invalid metrics)
- States are not well-defined or change frequently (fix data model first)
- You need predictive analytics (this skill covers historical analysis only)

## What This Skill Does

Provides comprehensive guidance on designing and implementing state transition analysis systems. Covers state machine fundamentals, extracting transitions from audit logs, calculating temporal durations (calendar days and business hours), detecting bottlenecks, analyzing workflow metrics (cycle time, lead time, flow efficiency), and exporting results for stakeholders. Includes practical examples for Jira, GitHub PRs, and custom systems.

## Quick Start

Analyze how long a ticket spends in each state:

```python
from jira_tool.analysis.state_analyzer import StateDurationAnalyzer
from jira_tool.client import JiraClient

# Fetch issue with changelog
client = JiraClient()
issue = client.get_issue("PROJ-123", expand=["changelog"])

# Analyze state durations
analyzer = StateDurationAnalyzer()
durations = analyzer.analyze_issue(issue)

# Get results
for duration in durations:
    print(f"{duration.state}: {duration.calendar_days} days, {duration.business_hours} business hours")
```

Or use the CLI for batch analysis:
```bash
# Export issues with changelog
uv run jira-tool search "project = PROJ" --expand changelog --format json -o issues.json

# Analyze state durations
uv run jira-tool analyze state-durations issues.json -o durations.csv --business-hours
```

## Instructions

### Step 1: Understand State Machines and Transitions

Every system with state changes follows this pattern:

1. **States**: Discrete conditions (To Do, In Progress, Done, Blocked, etc.)
2. **Transitions**: Changes from one state to another (To Do → In Progress)
3. **Timeline**: When each transition occurred (from audit log/changelog)
4. **Duration**: Time between transitions

**Key Principle**: A complete state history lets you calculate exactly how long items spend in each state.

**Real-World Examples**:
- **Jira Ticket**: `Created → To Do → In Progress → Review → Done` (track days in each)
- **GitHub PR**: `Created → In Review → Approved → Merged` (track review duration)
- **Deployment**: `Queued → Building → Testing → Staging → Production` (track stage duration)
- **Support Ticket**: `New → Assigned → Investigating → Resolved → Closed` (track response time)

### Step 2: Extract State Transitions from Audit Logs

The foundation of state analysis is reliable transition data. Most systems provide this through:
- **Changelog** (Jira issues, GitHub API)
- **Audit logs** (enterprise systems)
- **Event streams** (modern event-driven architectures)
- **Status history** (deployment platforms)

**Pattern**: Extract raw transition data into structured records:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StateTransition:
    timestamp: datetime        # When it changed
    from_state: str | None    # Previous state (None if created)
    to_state: str             # New state
    author: str | None        # Who made the change
```

**Example from Jira changelog**:
```json
{
  "created": "2024-01-15T10:30:00Z",
  "changelog": {
    "histories": [
      {
        "created": "2024-01-15T10:30:00Z",
        "items": [
          {
            "field": "status",
            "fromString": null,
            "toString": "To Do"
          }
        ]
      },
      {
        "created": "2024-01-16T09:00:00Z",
        "items": [
          {
            "field": "status",
            "fromString": "To Do",
            "toString": "In Progress"
          }
        ]
      }
    ]
  }
}
```

**Extraction Logic**: For each status change in changelog, create a StateTransition

### Step 3: Calculate Duration Between Transitions

Once you have transitions, calculate time spent in each state:

**Duration Metrics**:
1. **Calendar Days**: Total elapsed days (includes nights, weekends)
2. **Business Hours**: Time within working hours (e.g., 9 AM - 5 PM, weekdays only)
3. **Active Hours**: Excludes explicitly defined off-hours

**Implementation Pattern**:

```python
from datetime import datetime, timedelta, UTC

@dataclass
class StateDuration:
    state: str
    start_time: datetime
    end_time: datetime | None      # None if still in state
    calendar_days: float
    business_hours: float

def calculate_calendar_days(start: datetime, end: datetime) -> float:
    """Calculate elapsed calendar days."""
    delta = end - start
    return delta.total_seconds() / (24 * 3600)

def calculate_business_hours(
    start: datetime,
    end: datetime,
    business_start: int = 9,       # 9 AM
    business_end: int = 17,        # 5 PM
) -> float:
    """Calculate time within business hours (Mon-Fri, 9-5)."""
    current = start
    hours = 0.0

    while current < end:
        # Only count weekdays
        if current.weekday() < 5:  # Mon=0, Fri=4
            day_start = current.replace(hour=business_start, minute=0, second=0)
            day_end = current.replace(hour=business_end, minute=0, second=0)

            # Clamp to actual interval
            interval_start = max(current, day_start)
            interval_end = min(end, day_end)

            if interval_start < interval_end:
                hours += (interval_end - interval_start).total_seconds() / 3600

        # Move to next day
        current = (current + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    return hours
```

**Considerations**:
- **Timezone Awareness**: Always use UTC internally, convert for display
- **Partial Days**: Handle transitions at any time (not just business hour boundaries)
- **Open Issues**: Current state has `end_time = None` (still ongoing)
- **Business Hours**: Configurable per organization (not all use 9-5)

### Step 4: Detect Bottlenecks

Once you have durations, find which states take the longest:

**Pattern**: Aggregate by state and sort by duration

```python
def find_bottlenecks(durations: list[StateDuration]) -> dict[str, dict]:
    """Identify states where items spend most time."""
    by_state = {}

    for duration in durations:
        if duration.state not in by_state:
            by_state[duration.state] = {
                'total_days': 0,
                'count': 0,
                'max_days': 0,
                'avg_business_hours': 0
            }

        stats = by_state[duration.state]
        if duration.end_time:  # Only closed items
            stats['total_days'] += duration.calendar_days
            stats['count'] += 1
            stats['max_days'] = max(stats['max_days'], duration.calendar_days)

    # Calculate averages
    for state, stats in by_state.items():
        if stats['count'] > 0:
            stats['avg_days'] = stats['total_days'] / stats['count']

    # Sort by average duration
    return dict(sorted(
        by_state.items(),
        key=lambda x: x[1].get('avg_days', 0),
        reverse=True
    ))
```

**Interpretation**:
- States with high average = bottlenecks
- States with high variance = inconsistent process
- States in critical path = focus areas for improvement

### Step 5: Analyze Patterns and Metrics

Extract actionable insights from duration data:

**Common Metrics**:

1. **Cycle Time**: Total time from creation to completion
```
Cycle Time = sum of all state durations
(Useful for: capacity planning, delivery promises)
```

2. **Lead Time**: Time from request to delivery (may exclude certain states)
```
Lead Time = cycle time minus waiting states
(Useful for: customer SLA tracking)
```

3. **Flow Efficiency**: Percentage of time in value-added states
```
Flow Efficiency = (active work time) / (total time)
(Useful for: process optimization)
```

4. **State-Specific Metrics**:
```
Review Wait Time = average time in "In Review" state
Development Time = average time in "In Progress" state
```

**Analysis Patterns**:
- **Trend**: Is cycle time getting longer or shorter? (Performance degradation)
- **Distribution**: Are most items fast with occasional slow ones? (Outlier analysis)
- **Correlation**: Do certain states predict long cycle times? (Predictive metrics)
- **Seasonality**: Do Mondays take longer? (Resource constraints)

### Step 6: Export and Communicate Results

Format analysis results for different audiences:

**Format 1: CSV (Spreadsheet-Friendly)**
```csv
issue_key,state,start_time,end_time,calendar_days,business_hours
PROJ-123,To Do,2024-01-15T10:30:00Z,2024-01-16T09:00:00Z,0.94,8.5
PROJ-123,In Progress,2024-01-16T09:00:00Z,2024-01-18T14:30:00Z,2.23,16.5
```

Use for: Excel analysis, stakeholder reports, historical records

**Format 2: JSON (Programmatic Processing)**
```json
{
  "issues": [
    {
      "key": "PROJ-123",
      "states": [
        {
          "state": "To Do",
          "calendar_days": 0.94,
          "business_hours": 8.5
        }
      ],
      "cycle_time_days": 4.17
    }
  ],
  "summary": {
    "by_state": {
      "In Progress": {
        "avg_days": 2.8,
        "max_days": 8.5
      }
    }
  }
}
```

Use for: Further analysis, automation, dashboards

**Format 3: Visualization Data**
```
State Analysis Summary:
========================
Total Items Analyzed: 47
Average Cycle Time: 5.2 days (35.4 business hours)

By State:
  In Progress: avg 2.8 days (18% of time)
  Code Review: avg 1.9 days (23% of time) ⚠️ BOTTLENECK
  Testing: avg 0.8 days (10% of time)
  Done: avg 0.7 days (8% of time)
```

Use for: Dashboards, reports, team communication

### Step 7: Extend for Your Use Case

**Template for Custom State Analyzer**:

```python
from datetime import datetime, UTC
from dataclasses import dataclass

@dataclass
class YourStateTransition:
    timestamp: datetime
    from_state: str | None
    to_state: str
    # Add domain-specific fields:
    # user_id: str
    # reason: str
    # severity: int

class YourStateAnalyzer:
    def extract_transitions(self, audit_log: dict) -> list[YourStateTransition]:
        """Extract transitions from your system's format."""
        # Implement for your audit log structure
        pass

    def calculate_durations(self, transitions: list) -> list[StateDuration]:
        """Calculate time in each state."""
        # Implement calculation logic
        pass

    def find_bottlenecks(self, durations: list) -> dict:
        """Identify slow states."""
        # Implement bottleneck detection
        pass

    def format_report(self, durations: list) -> str:
        """Export results."""
        # Implement report generation
        pass
```

**Common Adaptations**:
- **GitHub PRs**: Extract from `pull_requests.timeline` API (comments with state changes)
- **Deployments**: Parse CI/CD logs for stage transitions (timestamp from log entries)
- **Support Tickets**: Extract from ticket history (created, assigned, resolved timestamps)
- **Manufacturing**: Use MES (Manufacturing Execution System) event logs

## Examples

### Example 1: Analyze Single Jira Issue

```bash
# Get issue with changelog
uv run jira-tool get PROJ-123

# Or analyze via CLI (shorter version)
uv run jira-tool search "key = PROJ-123" --expand changelog --format json -o issue.json
uv run jira-tool analyze state-durations issue.json -o durations.csv
```

### Example 2: Find Bottlenecks Across Project

```bash
# Export all issues from last sprint with changelog
uv run jira-tool search "sprint in openSprints()" \
  --expand changelog \
  --format json \
  -o sprint_issues.json

# Analyze state durations
uv run jira-tool analyze state-durations sprint_issues.json \
  -o sprint_analysis.csv \
  --business-hours

# Load CSV and find bottlenecks
python3 << 'EOF'
import pandas as pd

df = pd.read_csv('sprint_analysis.csv')

# Group by state and calculate averages
bottlenecks = df.groupby('state').agg({
    'calendar_days': 'mean',
    'business_hours': 'mean'
}).sort_values('calendar_days', ascending=False)

print("Bottleneck States (by average duration):")
print(bottlenecks)
EOF
```

### Example 3: Track SLA Compliance

```bash
# Analyze customer-facing issues
uv run jira-tool search "type = Bug AND labels = urgent" \
  --expand changelog \
  --format json \
  -o urgent_bugs.json

uv run jira-tool analyze state-durations urgent_bugs.json \
  -o bug_analysis.csv \
  --date-from 2024-01-01 --date-to 2024-12-31

# Check if average resolution time meets SLA (< 24 business hours)
python3 << 'EOF'
import pandas as pd

df = pd.read_csv('bug_analysis.csv')
total_hours = df[df['state'] == 'Resolved']['business_hours'].sum()
avg_hours = df[df['state'] == 'Resolved']['business_hours'].mean()

sla_threshold = 24
compliance = (avg_hours <= sla_threshold) * 100 if avg_hours > 0 else 0

print(f"Average Resolution Time: {avg_hours:.1f} business hours")
print(f"SLA Threshold: {sla_threshold} hours")
print(f"Compliance: {compliance:.0f}%")
EOF
```

### Example 4: Custom State Analyzer (GitHub PR Review Time)

```python
# analyze_github_prs.py
import json
from datetime import datetime, UTC
from dataclasses import dataclass

@dataclass
class PRStateTransition:
    timestamp: datetime
    from_state: str | None
    to_state: str

class GitHubPRAnalyzer:
    """Analyze GitHub PR time in review."""

    def extract_transitions(self, pr_data: dict):
        """Extract state transitions from GitHub PR timeline."""
        transitions = []

        # PR created = initial state
        created_at = datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00'))
        transitions.append(PRStateTransition(
            timestamp=created_at,
            from_state=None,
            to_state='Draft' if pr_data['draft'] else 'Open'
        ))

        # Parse review states from timeline
        for event in pr_data.get('timeline', []):
            if event['event'] == 'review_requested':
                transitions.append(PRStateTransition(
                    timestamp=datetime.fromisoformat(event['created_at'].replace('Z', '+00:00')),
                    from_state='Open',
                    to_state='In Review'
                ))
            elif event['event'] == 'pull_request_review':
                transitions.append(PRStateTransition(
                    timestamp=datetime.fromisoformat(event['submitted_at'].replace('Z', '+00:00')),
                    from_state='In Review',
                    to_state=f"Review-{event['state']}"  # APPROVED, CHANGES_REQUESTED, COMMENTED
                ))
            elif event['event'] == 'merged':
                transitions.append(PRStateTransition(
                    timestamp=datetime.fromisoformat(event['created_at'].replace('Z', '+00:00')),
                    from_state=transitions[-1].to_state,
                    to_state='Merged'
                ))

        return transitions

# Usage
analyzer = GitHubPRAnalyzer()
pr_data = json.load(open('pr.json'))
transitions = analyzer.extract_transitions(pr_data)

for t in transitions:
    print(f"{t.from_state} → {t.to_state} at {t.timestamp}")
```

## Requirements

### For Jira Analysis (Project-Based)
- **Jira Cloud instance** with REST API v3 access
- **Environment variables**: `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`
- **Python 3.10+** with jira-tool installed (`uv sync`)
- **Changelog data**: Issues must be exported with `--expand changelog`

### For Custom Analysis
- **Audit log access**: Your system must provide state change history
- **Python 3.8+** (dataclasses support)
- **datetime library** for temporal calculations
- **Optional**: pandas for advanced statistical analysis

## Related Skills

- **jira-api** - Fetch issue data with changelog using Jira REST API v3
- **export-and-analyze-jira-data** - Data export patterns and bulk analysis workflows
- **build-jira-document-format** - Create analysis reports in Atlassian Document Format
- **kafka-consumer-implementation** - For real-time state tracking with event streams
- **observability-analyze-logs** - Extract state transitions from application logs

## Notes

**Key Implementation Points:**
- Always use UTC internally for timestamp calculations
- Handle open issues where end_time is None (still in current state)
- Business hours are configurable per organization (default: Mon-Fri, 9 AM - 5 PM)
- Complete state history is required for accurate analysis
- Partial days must be handled correctly (transitions happen at any time)

**Common Pitfalls:**
- Missing changelog expansion in API queries (`--expand changelog` flag required)
- Ignoring timezone conversions (leads to incorrect duration calculations)
- Not filtering out non-status changes from changelog (focus on status field only)
- Treating weekends as business days (skews business hours metric)
- Calculating averages including incomplete items (exclude items still in progress)

**Business Hours Calculation:**
- See Step 3 for complete implementation
- Handles partial days, weekends, and configurable work hours
- Returns floating-point hours for precise metrics
