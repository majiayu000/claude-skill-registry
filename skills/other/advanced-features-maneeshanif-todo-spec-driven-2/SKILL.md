---
name: advanced-features
description: Implement advanced task features - Priorities, Tags, Due Dates, Reminders, Recurring Tasks, Search, Filter, and Sort. Use when adding Phase 5 advanced functionality. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# Advanced Features Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Read Phase 5 Spec** - `spec-prompt-phase-5.md` for user stories
3. **Update database models** - Add new fields and tables
4. **Create migrations** - Alembic migrations
5. **Implement API endpoints** - FastAPI routers
6. **Build UI components** - React components
7. **Add event publishing** - Dapr pub/sub integration

## Feature Overview

| Feature | Description | Priority |
|---------|-------------|----------|
| **Priorities** | Low/Medium/High task priority | P0 |
| **Tags** | Categorize tasks with labels | P0 |
| **Due Dates** | Task deadlines with time | P0 |
| **Reminders** | Notification before due date | P1 |
| **Recurring Tasks** | Daily/Weekly/Monthly repeat | P1 |
| **Search** | Full-text task search | P1 |
| **Filter** | Filter by status/priority/tag | P0 |
| **Sort** | Sort by date/priority/name | P0 |

## Database Models

### Updated Task Model

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecurrenceType(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None)
    status: str = Field(default="pending")
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: datetime | None = Field(default=None)
    recurrence_type: RecurrenceType = Field(default=RecurrenceType.NONE)
    recurrence_interval: int | None = Field(default=None)
    next_occurrence: datetime | None = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tags: list["TaskTag"] = Relationship(back_populates="task")
    reminders: list["Reminder"] = Relationship(back_populates="task")
```

### Tag Model

```python
# backend/src/models/tag.py
from sqlmodel import SQLModel, Field, Relationship
import uuid

class Tag(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=50, index=True)
    color: str = Field(default="#6B7280")  # Hex color
    user_id: uuid.UUID = Field(foreign_key="user.id")

    # Relationships
    tasks: list["TaskTag"] = Relationship(back_populates="tag")

class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tag"

    task_id: uuid.UUID = Field(foreign_key="task.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id", primary_key=True)

    # Relationships
    task: "Task" = Relationship(back_populates="tags")
    tag: "Tag" = Relationship(back_populates="tasks")
```

### Reminder Model

```python
# backend/src/models/reminder.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

class Reminder(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="task.id")
    remind_at: datetime
    message: str | None = Field(default=None)
    is_sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: "Task" = Relationship(back_populates="reminders")
```

## API Endpoints

### Tags Router

```python
# backend/src/routers/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID

router = APIRouter(prefix="/api/tags", tags=["tags"])

@router.get("/")
async def list_tags(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """List all tags for current user."""
    statement = select(Tag).where(Tag.user_id == user.id)
    tags = session.exec(statement).all()
    return tags

@router.post("/")
async def create_tag(
    tag_data: TagCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Create a new tag."""
    tag = Tag(**tag_data.model_dump(), user_id=user.id)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

@router.post("/{task_id}/tags/{tag_id}")
async def add_tag_to_task(
    task_id: UUID,
    tag_id: UUID,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Add a tag to a task."""
    task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
    session.add(task_tag)
    session.commit()
    return {"status": "added"}

@router.delete("/{task_id}/tags/{tag_id}")
async def remove_tag_from_task(
    task_id: UUID,
    tag_id: UUID,
    session: Session = Depends(get_session)
):
    """Remove a tag from a task."""
    statement = select(TaskTag).where(
        TaskTag.task_id == task_id,
        TaskTag.tag_id == tag_id
    )
    task_tag = session.exec(statement).first()
    if task_tag:
        session.delete(task_tag)
        session.commit()
    return {"status": "removed"}
```

### Filter & Search Endpoint

```python
# backend/src/routers/tasks.py (updated)
from fastapi import Query
from typing import Optional
from datetime import datetime

@router.get("/")
async def list_tasks(
    # Filter parameters
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[Priority] = Query(None, description="Filter by priority"),
    tag_ids: Optional[list[UUID]] = Query(None, description="Filter by tag IDs"),
    due_before: Optional[datetime] = Query(None, description="Due before date"),
    due_after: Optional[datetime] = Query(None, description="Due after date"),

    # Search
    search: Optional[str] = Query(None, description="Search in title/description"),

    # Sort
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)"),

    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),

    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """List tasks with filtering, search, and sorting."""
    statement = select(Task).where(Task.user_id == user.id)

    # Apply filters
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)
    if due_before:
        statement = statement.where(Task.due_date <= due_before)
    if due_after:
        statement = statement.where(Task.due_date >= due_after)

    # Tag filter (requires join)
    if tag_ids:
        statement = statement.join(TaskTag).where(TaskTag.tag_id.in_(tag_ids))

    # Full-text search
    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            (Task.title.ilike(search_term)) |
            (Task.description.ilike(search_term))
        )

    # Sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    # Pagination
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)

    tasks = session.exec(statement).all()
    return tasks
```

### Reminders Router

```python
# backend/src/routers/reminders.py
from fastapi import APIRouter, Depends
from dapr.clients import DaprClient

router = APIRouter(prefix="/api/reminders", tags=["reminders"])

@router.post("/")
async def create_reminder(
    reminder_data: ReminderCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Create a reminder for a task."""
    # Create reminder in database
    reminder = Reminder(**reminder_data.model_dump())
    session.add(reminder)
    session.commit()
    session.refresh(reminder)

    # Publish event for scheduling
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="taskpubsub",
            topic_name="reminder-events",
            data={
                "event_type": "reminder.created",
                "reminder_id": str(reminder.id),
                "task_id": str(reminder.task_id),
                "user_id": str(user.id),
                "remind_at": reminder.remind_at.isoformat()
            }
        )

    return reminder
```

## Frontend Components

### Priority Badge Component

```tsx
// frontend/components/tasks/priority-badge.tsx
import { Badge } from "@/components/ui/badge";

interface PriorityBadgeProps {
  priority: "low" | "medium" | "high";
}

const priorityConfig = {
  low: { label: "Low", className: "bg-gray-100 text-gray-800" },
  medium: { label: "Medium", className: "bg-yellow-100 text-yellow-800" },
  high: { label: "High", className: "bg-red-100 text-red-800" },
};

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  const config = priorityConfig[priority];
  return <Badge className={config.className}>{config.label}</Badge>;
}
```

### Tag Component

```tsx
// frontend/components/tasks/tag-badge.tsx
import { Badge } from "@/components/ui/badge";
import { X } from "lucide-react";

interface TagBadgeProps {
  name: string;
  color: string;
  onRemove?: () => void;
}

export function TagBadge({ name, color, onRemove }: TagBadgeProps) {
  return (
    <Badge
      style={{ backgroundColor: color }}
      className="text-white flex items-center gap-1"
    >
      {name}
      {onRemove && (
        <X className="h-3 w-3 cursor-pointer" onClick={onRemove} />
      )}
    </Badge>
  );
}
```

### Filter Bar Component

```tsx
// frontend/components/tasks/filter-bar.tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { DatePicker } from "@/components/ui/date-picker";

interface FilterBarProps {
  onFilterChange: (filters: TaskFilters) => void;
}

export function FilterBar({ onFilterChange }: FilterBarProps) {
  const [filters, setFilters] = useState<TaskFilters>({});

  return (
    <div className="flex gap-4 flex-wrap">
      <Input
        placeholder="Search tasks..."
        onChange={(e) => handleSearchChange(e.target.value)}
        className="w-64"
      />

      <Select onValueChange={(value) => handleFilterChange("status", value)}>
        <SelectTrigger className="w-32">
          <SelectValue placeholder="Status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="pending">Pending</SelectItem>
          <SelectItem value="in_progress">In Progress</SelectItem>
          <SelectItem value="completed">Completed</SelectItem>
        </SelectContent>
      </Select>

      <Select onValueChange={(value) => handleFilterChange("priority", value)}>
        <SelectTrigger className="w-32">
          <SelectValue placeholder="Priority" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="low">Low</SelectItem>
          <SelectItem value="medium">Medium</SelectItem>
          <SelectItem value="high">High</SelectItem>
        </SelectContent>
      </Select>

      <DatePicker
        placeholder="Due before"
        onChange={(date) => handleFilterChange("due_before", date)}
      />
    </div>
  );
}
```

## Event Publishing

```python
# backend/src/services/task_events.py
from dapr.clients import DaprClient
import json

class TaskEventPublisher:
    """Publish task events to Kafka via Dapr."""

    async def publish_task_created(self, task: Task):
        await self._publish("task.created", task)

    async def publish_task_updated(self, task: Task):
        await self._publish("task.updated", task)

    async def publish_task_deleted(self, task_id: str, user_id: str):
        with DaprClient() as client:
            client.publish_event(
                pubsub_name="taskpubsub",
                topic_name="task-events",
                data=json.dumps({
                    "event_type": "task.deleted",
                    "task_id": task_id,
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                })
            )

    async def _publish(self, event_type: str, task: Task):
        with DaprClient() as client:
            client.publish_event(
                pubsub_name="taskpubsub",
                topic_name="task-events",
                data=json.dumps({
                    "event_type": event_type,
                    "task_id": str(task.id),
                    "user_id": str(task.user_id),
                    "task": task.model_dump(mode="json"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            )
```

## Alembic Migration

```python
# backend/alembic/versions/xxx_add_advanced_features.py
"""Add advanced task features

Revision ID: xxx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Add new columns to task table
    op.add_column('task', sa.Column('priority', sa.String(10), default='medium'))
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('recurrence_type', sa.String(10), default='none'))
    op.add_column('task', sa.Column('recurrence_interval', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('next_occurrence', sa.DateTime(), nullable=True))

    # Create tag table
    op.create_table(
        'tag',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('color', sa.String(7), default='#6B7280'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id'))
    )

    # Create task_tag junction table
    op.create_table(
        'task_tag',
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('task.id'), primary_key=True),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tag.id'), primary_key=True)
    )

    # Create reminder table
    op.create_table(
        'reminder',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('task.id')),
        sa.Column('remind_at', sa.DateTime(), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('is_sent', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now())
    )

    # Create indexes
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])
    op.create_index('ix_tag_name', 'tag', ['name'])
    op.create_index('ix_reminder_remind_at', 'reminder', ['remind_at'])

def downgrade():
    op.drop_index('ix_reminder_remind_at')
    op.drop_index('ix_tag_name')
    op.drop_index('ix_task_due_date')
    op.drop_index('ix_task_priority')
    op.drop_table('reminder')
    op.drop_table('task_tag')
    op.drop_table('tag')
    op.drop_column('task', 'next_occurrence')
    op.drop_column('task', 'recurrence_interval')
    op.drop_column('task', 'recurrence_type')
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'priority')
```

## Verification Checklist

- [ ] Database models updated (Task, Tag, TaskTag, Reminder)
- [ ] Alembic migration created and applied
- [ ] Tags API endpoints working
- [ ] Reminders API endpoints working
- [ ] Filter/Search/Sort working on tasks list
- [ ] Priority badges displayed in UI
- [ ] Tag management UI working
- [ ] Due date picker working
- [ ] Events published to Kafka
- [ ] All tests passing

## References

- [Phase 5 Spec](../../../spec-prompt-phase-5.md) - User stories
- [SQLModel Relationships](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
