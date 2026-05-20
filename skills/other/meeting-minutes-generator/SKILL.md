---
name: "meeting-minutes-generator"
description: "Generate structured construction meeting minutes. Track action items, decisions, and attendees."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📋", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Meeting Minutes Generator

## Business Case

### Problem Statement
Meeting documentation is inconsistent:
- Minutes not standardized
- Action items lost
- Decisions not tracked
- Poor distribution

### Solution
Standardized meeting minutes generation with action item tracking, decision logging, and automatic distribution.

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MeetingType(Enum):
    OAC = "oac"  # Owner-Architect-Contractor
    PROGRESS = "progress"
    COORDINATION = "coordination"
    SAFETY = "safety"
    PRECONSTRUCTION = "preconstruction"
    CLOSEOUT = "closeout"
    OTHER = "other"


class ActionStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    OVERDUE = "overdue"


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Attendee:
    name: str
    company: str
    role: str
    email: str
    present: bool = True


@dataclass
class ActionItem:
    action_id: str
    description: str
    assigned_to: str
    due_date: date
    priority: Priority
    status: ActionStatus
    created_meeting: str
    completed_date: Optional[date] = None
    notes: str = ""


@dataclass
class Decision:
    decision_id: str
    description: str
    made_by: str
    decision_date: date
    impact: str = ""


@dataclass
class DiscussionTopic:
    topic_id: str
    title: str
    presenter: str
    discussion: str
    decisions: List[Decision] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)  # Action IDs


@dataclass
class MeetingMinutes:
    meeting_id: str
    meeting_type: MeetingType
    title: str
    date: date
    time_start: str
    time_end: str
    location: str
    attendees: List[Attendee]
    topics: List[DiscussionTopic]
    action_items: List[ActionItem]
    next_meeting: Optional[date] = None
    prepared_by: str = ""
    approved_by: str = ""


class MeetingMinutesGenerator:
    """Generate and track meeting minutes."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.meetings: Dict[str, MeetingMinutes] = {}
        self.all_actions: Dict[str, ActionItem] = {}
        self._meeting_counter = 0
        self._action_counter = 0
        self._decision_counter = 0

    def create_meeting(self, meeting_type: MeetingType, title: str,
                      meeting_date: date, time_start: str, time_end: str,
                      location: str) -> MeetingMinutes:
        self._meeting_counter += 1
        meeting_id = f"MTG-{self._meeting_counter:04d}"

        meeting = MeetingMinutes(
            meeting_id=meeting_id,
            meeting_type=meeting_type,
            title=title,
            date=meeting_date,
            time_start=time_start,
            time_end=time_end,
            location=location,
            attendees=[],
            topics=[],
            action_items=[]
        )
        self.meetings[meeting_id] = meeting
        return meeting

    def add_attendee(self, meeting_id: str, name: str, company: str,
                    role: str, email: str, present: bool = True):
        if meeting_id not in self.meetings:
            return
        attendee = Attendee(name, company, role, email, present)
        self.meetings[meeting_id].attendees.append(attendee)

    def add_topic(self, meeting_id: str, title: str, presenter: str,
                 discussion: str) -> str:
        if meeting_id not in self.meetings:
            return ""
        topic_id = f"{meeting_id}-T{len(self.meetings[meeting_id].topics) + 1:02d}"
        topic = DiscussionTopic(topic_id, title, presenter, discussion)
        self.meetings[meeting_id].topics.append(topic)
        return topic_id

    def add_decision(self, meeting_id: str, topic_id: str, description: str,
                    made_by: str, impact: str = "") -> Decision:
        if meeting_id not in self.meetings:
            return None

        self._decision_counter += 1
        decision_id = f"DEC-{self._decision_counter:04d}"

        decision = Decision(
            decision_id=decision_id,
            description=description,
            made_by=made_by,
            decision_date=self.meetings[meeting_id].date,
            impact=impact
        )

        # Find topic and add decision
        for topic in self.meetings[meeting_id].topics:
            if topic.topic_id == topic_id:
                topic.decisions.append(decision)
                break

        return decision

    def create_action(self, meeting_id: str, description: str, assigned_to: str,
                     due_date: date, priority: Priority = Priority.MEDIUM) -> ActionItem:
        if meeting_id not in self.meetings:
            return None

        self._action_counter += 1
        action_id = f"ACT-{self._action_counter:04d}"

        action = ActionItem(
            action_id=action_id,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            priority=priority,
            status=ActionStatus.OPEN,
            created_meeting=meeting_id
        )

        self.meetings[meeting_id].action_items.append(action)
        self.all_actions[action_id] = action
        return action

    def update_action_status(self, action_id: str, status: ActionStatus):
        if action_id in self.all_actions:
            self.all_actions[action_id].status = status
            if status == ActionStatus.COMPLETE:
                self.all_actions[action_id].completed_date = date.today()

    def get_open_actions(self, assigned_to: str = None) -> List[ActionItem]:
        actions = [a for a in self.all_actions.values()
                  if a.status in [ActionStatus.OPEN, ActionStatus.IN_PROGRESS]]
        if assigned_to:
            actions = [a for a in actions if assigned_to.lower() in a.assigned_to.lower()]
        return sorted(actions, key=lambda x: x.due_date)

    def get_overdue_actions(self) -> List[ActionItem]:
        today = date.today()
        overdue = []
        for action in self.all_actions.values():
            if action.status in [ActionStatus.OPEN, ActionStatus.IN_PROGRESS]:
                if action.due_date < today:
                    action.status = ActionStatus.OVERDUE
                    overdue.append(action)
        return overdue

    def generate_minutes_document(self, meeting_id: str) -> str:
        """Generate formatted meeting minutes."""
        if meeting_id not in self.meetings:
            return ""

        mtg = self.meetings[meeting_id]

        lines = [
            f"# {mtg.title}",
            f"**Date:** {mtg.date.strftime('%B %d, %Y')}",
            f"**Time:** {mtg.time_start} - {mtg.time_end}",
            f"**Location:** {mtg.location}",
            f"**Project:** {self.project_name}",
            "",
            "## Attendees",
        ]

        for att in mtg.attendees:
            status = "Present" if att.present else "Absent"
            lines.append(f"- {att.name} ({att.company}) - {att.role} [{status}]")

        lines.extend(["", "## Discussion Topics"])

        for topic in mtg.topics:
            lines.extend([
                f"### {topic.title}",
                f"*Presented by: {topic.presenter}*",
                "",
                topic.discussion,
                ""
            ])

            if topic.decisions:
                lines.append("**Decisions:**")
                for dec in topic.decisions:
                    lines.append(f"- [{dec.decision_id}] {dec.description}")
                lines.append("")

        if mtg.action_items:
            lines.extend(["## Action Items", ""])
            lines.append("| ID | Action | Assigned | Due | Priority |")
            lines.append("|---|---|---|---|---|")
            for action in mtg.action_items:
                lines.append(f"| {action.action_id} | {action.description} | "
                           f"{action.assigned_to} | {action.due_date} | {action.priority.value} |")

        if mtg.next_meeting:
            lines.extend(["", f"## Next Meeting: {mtg.next_meeting.strftime('%B %d, %Y')}"])

        return "\n".join(lines)

    def export_all_actions(self, output_path: str):
        """Export action items to Excel."""
        data = [{
            'ID': a.action_id,
            'Description': a.description,
            'Assigned To': a.assigned_to,
            'Due Date': a.due_date,
            'Priority': a.priority.value,
            'Status': a.status.value,
            'Meeting': a.created_meeting
        } for a in self.all_actions.values()]

        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

generator = MeetingMinutesGenerator("Office Tower")

# Create meeting
meeting = generator.create_meeting(
    meeting_type=MeetingType.OAC,
    title="Weekly OAC Meeting #15",
    meeting_date=date.today(),
    time_start="10:00 AM",
    time_end="11:30 AM",
    location="Conference Room A"
)

# Add attendees
generator.add_attendee(meeting.meeting_id, "John Smith", "Owner LLC", "Owner Rep", "john@owner.com")

# Add topic
topic_id = generator.add_topic(meeting.meeting_id, "Schedule Update",
                               "Project Manager", "Discussed current schedule status...")

# Add decision
generator.add_decision(meeting.meeting_id, topic_id,
                      "Approved 2-week extension for concrete work", "Owner Rep")

# Create action
generator.create_action(meeting.meeting_id,
                       "Submit revised schedule", "Contractor",
                       date.today() + timedelta(days=7), Priority.HIGH)

# Generate document
minutes = generator.generate_minutes_document(meeting.meeting_id)
print(minutes)
```

## Resources
- **DDC Book**: Chapter 4 - Project Communication
