---
name: datetime-timezone
description: Handle datetime and timezone conversions correctly across frontend, API, and database. Use this skill when working with datetime-local inputs, scheduling features, due dates, reminders, or any time-sensitive functionality. Covers the critical pitfall of browser datetime-local inputs lacking timezone info.
---

# DateTime and Timezone Handling

Correctly handle datetime values across the full stack: browser → API → database → back to browser.

## When to Use

- Implementing due dates, reminders, or scheduling features
- Working with `datetime-local` HTML inputs
- Storing timestamps in PostgreSQL/databases
- Displaying times in user's local timezone
- Debugging "wrong time" issues

## The Golden Rule

**Store UTC, Display Local**

```
Browser (local) → Convert to UTC → API → Store UTC → Database
Database → Return UTC → API → Browser → Display in local
```

## Critical Pitfall: datetime-local Input

The HTML `<input type="datetime-local">` returns a string **WITHOUT timezone info**:

```html
<input type="datetime-local" value="2025-12-15T23:13">
```

This gives you `"2025-12-15T23:13"` - but is this UTC? Local time? **The browser doesn't tell you.**

### The Bug

```typescript
// WRONG - Backend interprets as UTC, but user entered local time!
const dueDate = "2025-12-15T23:13"  // User in PKT (UTC+5)
await api.createTask({ due_date: dueDate })
// Backend stores as 23:13 UTC
// But user meant 23:13 PKT = 18:13 UTC
// Task is now 5 hours late!
```

### The Fix

```typescript
// CORRECT - Convert local datetime to UTC ISO string
function handleSubmit() {
  let dueDateUTC: string | undefined = undefined

  if (dueDate) {
    // datetime-local gives "2025-12-15T23:13" (local time, no TZ)
    // new Date() interprets it in browser's local timezone
    // toISOString() converts to UTC: "2025-12-15T18:13:00.000Z"
    const localDate = new Date(dueDate)
    dueDateUTC = localDate.toISOString()
  }

  await api.createTask({ due_date: dueDateUTC })
}
```

## Frontend Patterns (TypeScript/React)

### Converting datetime-local to UTC

```typescript
// Input: "2025-12-15T23:13" (from datetime-local)
// Output: "2025-12-15T18:13:00.000Z" (UTC ISO string)

function localToUTC(localDatetime: string): string {
  const date = new Date(localDatetime)
  return date.toISOString()
}
```

### Converting UTC to datetime-local (for editing)

```typescript
// Input: "2025-12-15T18:13:00Z" (UTC from API)
// Output: "2025-12-15T23:13" (local, for datetime-local input)

function utcToLocal(utcDatetime: string): string {
  const date = new Date(utcDatetime)
  // Format: YYYY-MM-DDTHH:MM (no seconds, no Z)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}
```

### Full Form Example (React)

```tsx
"use client"

import { useState } from "react"

export function TaskForm() {
  const [dueDate, setDueDate] = useState("")  // Local datetime string

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Convert local to UTC for API
    let dueDateUTC: string | undefined
    if (dueDate) {
      dueDateUTC = new Date(dueDate).toISOString()
    }

    await api.createTask({
      title: "My Task",
      due_date: dueDateUTC,  // UTC ISO string
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="datetime-local"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
      />
      <button type="submit">Create</button>
    </form>
  )
}
```

### Editing Existing Task

```tsx
"use client"

import { useState, useEffect } from "react"

export function EditTaskForm({ task }: { task: Task }) {
  const [dueDate, setDueDate] = useState("")

  useEffect(() => {
    // Convert UTC from API to local for input
    if (task.due_date) {
      setDueDate(utcToLocal(task.due_date))
    }
  }, [task])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Convert back to UTC for API
    const dueDateUTC = dueDate ? new Date(dueDate).toISOString() : undefined

    await api.updateTask(task.id, { due_date: dueDateUTC })
  }

  return (
    <input
      type="datetime-local"
      value={dueDate}
      onChange={(e) => setDueDate(e.target.value)}
    />
  )
}
```

## Backend Patterns (Python/FastAPI)

### Pydantic Model with Timezone Normalization

```python
from datetime import UTC, datetime
from pydantic import field_validator
from sqlmodel import SQLModel

class TaskCreate(SQLModel):
    title: str
    due_date: datetime | None = None

    @field_validator("due_date", mode="after")
    @classmethod
    def normalize_datetime(cls, v: datetime | None) -> datetime | None:
        """Convert timezone-aware to naive UTC for storage."""
        if v is None:
            return None
        # If timezone-aware, convert to UTC and strip timezone
        if v.tzinfo is not None:
            v = v.astimezone(UTC).replace(tzinfo=None)
        return v
```

### API Endpoint

```python
@router.post("/tasks", response_model=TaskRead)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    # due_date is already normalized to naive UTC by validator
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Response Serialization

```python
from datetime import datetime

class TaskRead(SQLModel):
    id: int
    title: str
    due_date: datetime | None = None  # Returned as ISO string with Z suffix
```

FastAPI automatically serializes `datetime` as ISO 8601 with `Z` suffix (UTC).

## Database Storage

**Always store as naive UTC** (no timezone info):

```sql
-- PostgreSQL
due_date TIMESTAMP  -- NOT TIMESTAMP WITH TIME ZONE
```

```python
# SQLModel
from datetime import datetime
from sqlmodel import Field

class Task(SQLModel, table=True):
    due_date: datetime | None = Field(default=None)
```

## Displaying Times to Users

### Relative Time (e.g., "in 2 hours")

```typescript
import { formatDistanceToNow } from 'date-fns'

function formatRelative(utcDatetime: string): string {
  const date = new Date(utcDatetime)
  return formatDistanceToNow(date, { addSuffix: true })
  // "in 2 hours", "3 days ago"
}
```

### Absolute Local Time

```typescript
function formatLocal(utcDatetime: string): string {
  const date = new Date(utcDatetime)
  return date.toLocaleString()
  // "12/15/2025, 11:13:00 PM" (in user's locale)
}
```

### With Specific Format

```typescript
import { format } from 'date-fns'

function formatDateTime(utcDatetime: string): string {
  const date = new Date(utcDatetime)
  return format(date, 'MMM d, yyyy h:mm a')
  // "Dec 15, 2025 11:13 PM"
}
```

## Debugging Timezone Issues

### 1. Log at Every Step

```typescript
// Frontend
console.log("datetime-local value:", dueDate)  // "2025-12-15T23:13"
console.log("Converted to UTC:", new Date(dueDate).toISOString())  // "2025-12-15T18:13:00.000Z"
```

```python
# Backend
logger.info("Received due_date: %s", task_in.due_date)  # 2025-12-15T18:13:00+00:00
logger.info("Stored due_date: %s", task.due_date)  # 2025-12-15 18:13:00
```

### 2. Check Browser Timezone

```javascript
console.log(Intl.DateTimeFormat().resolvedOptions().timeZone)
// "Asia/Karachi" (PKT = UTC+5)
```

### 3. Verify UTC Offset

```typescript
const date = new Date("2025-12-15T23:13")
console.log("UTC offset (minutes):", date.getTimezoneOffset())
// -300 for UTC+5 (PKT)
```

## Common Pitfalls

### 1. Sending datetime-local Directly

```typescript
// WRONG
const dueDate = e.target.value  // "2025-12-15T23:13"
await api.post({ due_date: dueDate })  // No timezone!

// CORRECT
const dueDate = new Date(e.target.value).toISOString()
await api.post({ due_date: dueDate })  // "2025-12-15T18:13:00.000Z"
```

### 2. Using Date.now() Without toISOString()

```typescript
// WRONG - sends milliseconds timestamp
await api.post({ timestamp: Date.now() })  // 1734285180000

// CORRECT
await api.post({ timestamp: new Date().toISOString() })  // "2025-12-15T18:13:00.000Z"
```

### 3. Comparing Dates Without Normalization

```python
# WRONG - comparing aware and naive
if task.due_date < datetime.now(UTC):  # Error or wrong result

# CORRECT - both naive UTC
if task.due_date < datetime.utcnow():
```

### 4. Displaying UTC Directly

```typescript
// WRONG - shows UTC time to user
<span>{task.due_date}</span>  // "2025-12-15T18:13:00Z" (confusing!)

// CORRECT - convert to local
<span>{new Date(task.due_date).toLocaleString()}</span>  // "Dec 15, 2025, 11:13 PM"
```

## Testing

### Test Timezone Conversion

```typescript
describe('datetime conversion', () => {
  it('converts local to UTC correctly', () => {
    // Mock timezone to PKT (UTC+5)
    const localDatetime = "2025-12-15T23:13"
    const utc = new Date(localDatetime).toISOString()

    // In PKT, 23:13 local = 18:13 UTC
    expect(utc).toBe("2025-12-15T18:13:00.000Z")
  })
})
```

### Test Backend Normalization

```python
def test_datetime_normalization():
    # With timezone
    task = TaskCreate(
        title="Test",
        due_date=datetime(2025, 12, 15, 18, 13, tzinfo=UTC)
    )
    assert task.due_date.tzinfo is None  # Normalized to naive
    assert task.due_date == datetime(2025, 12, 15, 18, 13)
```

## Summary

| Location | Format | Example |
|----------|--------|---------|
| `datetime-local` input | Local, no TZ | `2025-12-15T23:13` |
| API request/response | UTC ISO 8601 | `2025-12-15T18:13:00.000Z` |
| Database | Naive UTC | `2025-12-15 18:13:00` |
| Display to user | Local formatted | `Dec 15, 2025 11:13 PM` |
