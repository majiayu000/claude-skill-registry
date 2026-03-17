---
name: temporal-evaluation
description: Calculates time-based task status including overdue detection, urgency levels (urgent/upcoming/soon), and relative time displays. Updates temporal status every 60 seconds with timezone-aware comparisons and edge case handling for tasks without due dates.
---

# Temporal Evaluation Skill

## Overview

The temporal evaluation skill continuously assesses task urgency based on time windows and provides human-readable relative time displays. It forms the foundation for time-sensitive features like priority classification and notifications.

## When to Apply

Apply this skill:
- Every 60 seconds while app is open (continuous monitoring)
- Immediately when a task's due date is created or updated
- When loading tasks (initial evaluation)
- When displaying relative time strings ("in 2 hours", "3 days ago")
- Before triggering notifications (to check eligibility)
- When calculating overdue/urgent/upcoming/soon status

## Time Windows

This skill defines specific time windows for classification:

- **10 minutes**: Notification check interval
- **6 hours**: Urgent threshold (VERY IMPORTANT priority)
- **24 hours**: Upcoming threshold (HIGH priority)
- **1 week (7 days)**: Soon threshold (MEDIUM priority)

```javascript
const TIME_WINDOWS = {
  TEN_MINUTES: 10 * 60 * 1000, // 600,000 ms
  SIX_HOURS: 6 * 60 * 60 * 1000, // 21,600,000 ms
  TWENTY_FOUR_HOURS: 24 * 60 * 60 * 1000, // 86,400,000 ms
  ONE_WEEK: 7 * 24 * 60 * 60 * 1000 // 604,800,000 ms
};
```

## Temporal Status Classification

### Overdue Detection

A task is overdue if its due date is in the past:

```javascript
function isOverdue(task) {
  if (!task.dueDate) return false;

  const now = new Date();
  const dueDate = new Date(task.dueDate);

  return dueDate < now;
}

// Examples
// Current time: 2025-12-16 14:00:00
isOverdue({ dueDate: '2025-12-16 13:00:00' }); // true (1 hour ago)
isOverdue({ dueDate: '2025-12-16 15:00:00' }); // false (1 hour from now)
isOverdue({ dueDate: null }); // false (no due date)
```

### Urgent Detection

A task is urgent if it's due within the next 6 hours:

```javascript
function isUrgent(task) {
  if (!task.dueDate) return false;

  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const timeUntilDue = dueDate - now;

  return timeUntilDue > 0 && timeUntilDue <= TIME_WINDOWS.SIX_HOURS;
}

// Examples
// Current time: 2025-12-16 14:00:00
isUrgent({ dueDate: '2025-12-16 18:00:00' }); // true (4 hours from now)
isUrgent({ dueDate: '2025-12-16 21:00:00' }); // false (7 hours from now)
isUrgent({ dueDate: '2025-12-16 13:00:00' }); // false (overdue, not urgent)
```

### Upcoming Detection

A task is upcoming if it's due within the next 24 hours (but not within 6 hours):

```javascript
function isUpcoming(task) {
  if (!task.dueDate) return false;

  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const timeUntilDue = dueDate - now;

  return timeUntilDue > TIME_WINDOWS.SIX_HOURS &&
         timeUntilDue <= TIME_WINDOWS.TWENTY_FOUR_HOURS;
}

// Examples
// Current time: 2025-12-16 14:00:00
isUpcoming({ dueDate: '2025-12-17 10:00:00' }); // true (20 hours from now)
isUpcoming({ dueDate: '2025-12-16 18:00:00' }); // false (4 hours - urgent, not upcoming)
isUpcoming({ dueDate: '2025-12-18 10:00:00' }); // false (beyond 24 hours)
```

### Soon Detection

A task is soon if it's due within the next 7 days (but not within 24 hours):

```javascript
function isSoon(task) {
  if (!task.dueDate) return false;

  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const timeUntilDue = dueDate - now;

  return timeUntilDue > TIME_WINDOWS.TWENTY_FOUR_HOURS &&
         timeUntilDue <= TIME_WINDOWS.ONE_WEEK;
}

// Examples
// Current time: 2025-12-16 14:00:00
isSoon({ dueDate: '2025-12-20 14:00:00' }); // true (4 days from now)
isSoon({ dueDate: '2025-12-17 10:00:00' }); // false (20 hours - upcoming, not soon)
isSoon({ dueDate: '2025-12-25 14:00:00' }); // false (beyond 7 days)
```

## Complete Temporal Status

```javascript
function getTemporalStatus(task) {
  if (!task.dueDate) {
    return {
      hasStatus: false,
      overdue: false,
      urgent: false,
      upcoming: false,
      soon: false
    };
  }

  return {
    hasStatus: true,
    overdue: isOverdue(task),
    urgent: isUrgent(task),
    upcoming: isUpcoming(task),
    soon: isSoon(task)
  };
}
```

## Timezone-Aware Comparisons

All time comparisons use the user's local timezone:

```javascript
function compareWithTimezone(taskDueDate) {
  // Both dates are created in local timezone
  const now = new Date(); // Local timezone
  const dueDate = new Date(taskDueDate); // Parsed in local timezone

  // Comparison is timezone-aware
  return dueDate - now;
}

// ISO 8601 format with timezone
// "2025-12-16T14:00:00-05:00" (EST)
// "2025-12-16T14:00:00+00:00" (UTC)

// Store due dates in ISO 8601 format for portability
function storeDueDate(date) {
  return date.toISOString(); // Always stores in UTC
}

function parseDueDate(isoString) {
  return new Date(isoString); // Converts to local timezone
}
```

## Relative Time Display

### Format Function

Convert milliseconds to human-readable relative time:

```javascript
function getRelativeTime(task) {
  if (!task.dueDate) return null;

  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const diff = dueDate - now; // milliseconds

  if (diff < 0) {
    // Past (overdue)
    return formatPastTime(Math.abs(diff));
  } else {
    // Future
    return formatFutureTime(diff);
  }
}

function formatPastTime(ms) {
  const minutes = Math.floor(ms / (1000 * 60));
  const hours = Math.floor(ms / (1000 * 60 * 60));
  const days = Math.floor(ms / (1000 * 60 * 60 * 24));

  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`;

  const weeks = Math.floor(days / 7);
  return `${weeks} week${weeks !== 1 ? 's' : ''} ago`;
}

function formatFutureTime(ms) {
  const minutes = Math.floor(ms / (1000 * 60));
  const hours = Math.floor(ms / (1000 * 60 * 60));
  const days = Math.floor(ms / (1000 * 60 * 60 * 24));

  if (minutes < 1) return 'in less than a minute';
  if (minutes < 60) return `in ${minutes} minute${minutes !== 1 ? 's' : ''}`;
  if (hours < 24) return `in ${hours} hour${hours !== 1 ? 's' : ''}`;
  if (days < 7) return `in ${days} day${days !== 1 ? 's' : ''}`;

  const weeks = Math.floor(days / 7);
  return `in ${weeks} week${weeks !== 1 ? 's' : ''}`;
}
```

### Relative Time Examples

```javascript
// Current time: 2025-12-16 14:00:00

getRelativeTime({ dueDate: '2025-12-16 14:30:00' }); // "in 30 minutes"
getRelativeTime({ dueDate: '2025-12-16 16:00:00' }); // "in 2 hours"
getRelativeTime({ dueDate: '2025-12-17 14:00:00' }); // "in 1 day"
getRelativeTime({ dueDate: '2025-12-20 14:00:00' }); // "in 4 days"
getRelativeTime({ dueDate: '2025-12-23 14:00:00' }); // "in 1 week"

getRelativeTime({ dueDate: '2025-12-16 13:30:00' }); // "30 minutes ago"
getRelativeTime({ dueDate: '2025-12-16 12:00:00' }); // "2 hours ago"
getRelativeTime({ dueDate: '2025-12-15 14:00:00' }); // "1 day ago"
getRelativeTime({ dueDate: '2025-12-12 14:00:00' }); // "4 days ago"
getRelativeTime({ dueDate: '2025-12-09 14:00:00' }); // "1 week ago"
```

## Continuous Evaluation

### 60-Second Update Interval

Update temporal status every 60 seconds:

```javascript
function useTemporalEvaluation(tasks) {
  const [evaluatedTasks, setEvaluatedTasks] = useState([]);

  useEffect(() => {
    // Initial evaluation
    const evaluate = () => {
      const updated = tasks.map(task => ({
        ...task,
        temporalStatus: getTemporalStatus(task),
        relativeTime: getRelativeTime(task)
      }));
      setEvaluatedTasks(updated);
    };

    evaluate();

    // Re-evaluate every 60 seconds
    const interval = setInterval(evaluate, 60 * 1000);

    return () => clearInterval(interval);
  }, [tasks]);

  return evaluatedTasks;
}
```

### Performance Optimization

```javascript
function evaluateTemporalStatus(tasks) {
  const now = Date.now(); // Cache current time

  return tasks.map(task => {
    if (!task.dueDate) {
      return { ...task, temporalStatus: null, relativeTime: null };
    }

    const dueDate = new Date(task.dueDate).getTime();
    const diff = dueDate - now;

    return {
      ...task,
      temporalStatus: calculateStatus(diff),
      relativeTime: formatRelativeTime(diff)
    };
  });
}

// Should complete in < 5ms for 1000 tasks
```

## Edge Cases

### Tasks Without Due Dates

Tasks without due dates have no temporal status:

```javascript
function handleNoDueDate(task) {
  if (!task.dueDate) {
    return {
      temporalStatus: null,
      relativeTime: null,
      isOverdue: false,
      isUrgent: false
    };
  }
}
```

### Past Due Dates (Overdue)

Overdue tasks have special handling:

```javascript
function handleOverdue(task) {
  const status = getTemporalStatus(task);

  if (status.overdue) {
    return {
      ...status,
      displayPriority: 'OVERDUE', // Special display
      relativeTime: getRelativeTime(task), // "2 hours ago"
      urgent: false, // No longer urgent (already past)
      upcoming: false,
      soon: false
    };
  }

  return status;
}
```

### Invalid Dates

Handle malformed date strings:

```javascript
function safeParseDate(dateString) {
  if (!dateString) return null;

  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      console.warn('Invalid date:', dateString);
      return null;
    }
    return date;
  } catch (error) {
    console.error('Date parsing error:', error);
    return null;
  }
}
```

### Daylight Saving Time

Handle DST transitions correctly:

```javascript
// Date objects automatically handle DST
// No special handling needed for standard operations

// However, be aware of edge cases:
function isDSTTransition(date1, date2) {
  return date1.getTimezoneOffset() !== date2.getTimezoneOffset();
}
```

## Display Component

```jsx
function TemporalStatusDisplay({ task }) {
  const status = getTemporalStatus(task);
  const relativeTime = getRelativeTime(task);

  if (!status.hasStatus) {
    return <span className="no-due-date">No due date</span>;
  }

  return (
    <div className="temporal-status">
      {status.overdue && (
        <span className="status-overdue">⚠️ Overdue</span>
      )}
      {status.urgent && !status.overdue && (
        <span className="status-urgent">🔥 Urgent</span>
      )}
      {status.upcoming && (
        <span className="status-upcoming">⏰ Upcoming</span>
      )}
      {status.soon && (
        <span className="status-soon">📅 Soon</span>
      )}
      <span className="relative-time">{relativeTime}</span>
    </div>
  );
}
```

## Styling

```css
.temporal-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.status-overdue {
  color: #DC2626;
  font-weight: 600;
}

.status-urgent {
  color: #EA580C;
  font-weight: 600;
}

.status-upcoming {
  color: #F59E0B;
  font-weight: 500;
}

.status-soon {
  color: #059669;
  font-weight: 500;
}

.relative-time {
  color: #6B7280;
  font-weight: 400;
}

.no-due-date {
  color: #9CA3AF;
  font-style: italic;
}
```

## Integration Points

This skill integrates with:
- **Priority Classification Skill**: Provides temporal urgency for classification
- **Notification Trigger Skill**: Determines notification eligibility
- **Task Filter Skill**: Powers due date filtering
- **Task Sorting Skill**: Provides temporal data for sorting

## Testing Examples

```javascript
// Current time: 2025-12-16 14:00:00

// Test 1: Overdue
const task1 = { dueDate: '2025-12-16 12:00:00' };
getTemporalStatus(task1); // { overdue: true, urgent: false, ... }
getRelativeTime(task1); // "2 hours ago"

// Test 2: Urgent
const task2 = { dueDate: '2025-12-16 18:00:00' };
getTemporalStatus(task2); // { overdue: false, urgent: true, ... }
getRelativeTime(task2); // "in 4 hours"

// Test 3: Upcoming
const task3 = { dueDate: '2025-12-17 10:00:00' };
getTemporalStatus(task3); // { overdue: false, upcoming: true, ... }
getRelativeTime(task3); // "in 20 hours"

// Test 4: Soon
const task4 = { dueDate: '2025-12-20 14:00:00' };
getTemporalStatus(task4); // { overdue: false, soon: true, ... }
getRelativeTime(task4); // "in 4 days"

// Test 5: No due date
const task5 = { dueDate: null };
getTemporalStatus(task5); // { hasStatus: false, ... }
getRelativeTime(task5); // null
```
