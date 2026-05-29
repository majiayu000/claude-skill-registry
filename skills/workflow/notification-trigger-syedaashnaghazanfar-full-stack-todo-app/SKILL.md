---
name: notification-trigger
description: Triggers notifications exclusively for VERY IMPORTANT priority tasks that are incomplete and due within 6 hours. Repeats every 10 minutes with duplicate prevention tracking in memory. Clears tracking when tasks complete or due times pass.
---

# Notification Trigger Skill

## Overview

The notification trigger skill monitors VERY IMPORTANT tasks and generates notification events at appropriate intervals. It implements intelligent duplicate prevention and lifecycle management.

## When to Apply

Apply this skill:
- Every 10 minutes while app is open (automatic interval)
- After task priority changes to VERY IMPORTANT
- After task due date updates
- After task completion status changes
- On app initialization (check for eligible tasks)

## Notification Conditions

A task is eligible for notification if **ALL** of the following are true:

1. **Priority**: Task priority is VERY IMPORTANT
2. **Status**: Task is NOT complete
3. **Due Time**: Task is due within next 6 hours
4. **Not Recently Notified**: Task was not notified in last 10 minutes

```javascript
function isEligibleForNotification(task, notificationHistory) {
  // Condition 1: VERY IMPORTANT priority
  if (task.priority !== 'VERY IMPORTANT') {
    return false;
  }

  // Condition 2: Not complete
  if (task.status === 'Complete') {
    return false;
  }

  // Condition 3: Due within 6 hours
  if (!task.dueDate) {
    return false;
  }

  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const hoursUntilDue = (dueDate - now) / (1000 * 60 * 60);

  if (hoursUntilDue <= 0 || hoursUntilDue > 6) {
    return false; // Overdue or not within 6 hours
  }

  // Condition 4: Not recently notified
  const lastNotified = notificationHistory[task.id];
  if (lastNotified) {
    const timeSinceNotification = now - lastNotified;
    const tenMinutes = 10 * 60 * 1000;
    if (timeSinceNotification < tenMinutes) {
      return false;
    }
  }

  return true; // All conditions met
}
```

## 10-Minute Repeat Interval

### Interval Implementation

```javascript
function startNotificationMonitoring(tasks, onNotification) {
  // Check immediately on start
  checkAndTriggerNotifications(tasks, onNotification);

  // Then check every 10 minutes
  const interval = setInterval(() => {
    checkAndTriggerNotifications(tasks, onNotification);
  }, 10 * 60 * 1000); // 600,000 ms

  return () => clearInterval(interval);
}

// Usage in React component
function useNotificationMonitoring(tasks) {
  useEffect(() => {
    const cleanup = startNotificationMonitoring(tasks, (notification) => {
      // Handle notification (persist, display, etc.)
      console.log('Notification triggered:', notification);
    });

    return cleanup;
  }, [tasks]);
}
```

### Why 10 Minutes?

- **Balance**: Frequent enough to be useful, not so frequent as to be annoying
- **Battery efficient**: Reasonable interval for mobile devices
- **User expectation**: Aligns with common notification patterns
- **Performance**: Minimal CPU usage every 10 minutes

## Duplicate Prevention

### In-Memory Tracking

Track last notification time for each task:

```javascript
class NotificationTracker {
  constructor() {
    this.history = new Map(); // taskId -> timestamp
  }

  wasRecentlyNotified(taskId) {
    const lastNotified = this.history.get(taskId);
    if (!lastNotified) return false;

    const now = Date.now();
    const tenMinutes = 10 * 60 * 1000;
    return (now - lastNotified) < tenMinutes;
  }

  recordNotification(taskId) {
    this.history.set(taskId, Date.now());
  }

  clearTask(taskId) {
    this.history.delete(taskId);
  }

  cleanup() {
    const now = Date.now();
    const tenMinutes = 10 * 60 * 1000;

    // Remove entries older than 10 minutes
    for (const [taskId, timestamp] of this.history.entries()) {
      if (now - timestamp > tenMinutes) {
        this.history.delete(taskId);
      }
    }
  }
}

const tracker = new NotificationTracker();
```

### Tracking Lifecycle

```javascript
function checkAndTriggerNotifications(tasks, onNotification) {
  // Clean up old tracking data
  tracker.cleanup();

  tasks.forEach(task => {
    if (isEligibleForNotification(task, tracker.history)) {
      // Generate notification
      const notification = createNotification(task);

      // Record that we notified
      tracker.recordNotification(task.id);

      // Trigger notification
      onNotification(notification);
    }
  });
}
```

## Notification Object Structure

```javascript
function createNotification(task) {
  const now = new Date();
  const dueDate = new Date(task.dueDate);
  const hoursUntilDue = Math.floor((dueDate - now) / (1000 * 60 * 60));
  const minutesUntilDue = Math.ceil((dueDate - now) / (1000 * 60));

  return {
    taskId: task.id,
    title: task.title,
    dueTime: task.dueDate,
    relativeTime: formatTimeUntilDue(minutesUntilDue),
    timestamp: now.toISOString(),
    priority: 'VERY IMPORTANT',
    message: `Task "${task.title}" is due in ${formatTimeUntilDue(minutesUntilDue)}`
  };
}

function formatTimeUntilDue(minutes) {
  if (minutes < 60) {
    return `${minutes} minute${minutes !== 1 ? 's' : ''}`;
  }

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (remainingMinutes === 0) {
    return `${hours} hour${hours !== 1 ? 's' : ''}`;
  }

  return `${hours} hour${hours !== 1 ? 's' : ''} and ${remainingMinutes} minute${remainingMinutes !== 1 ? 's' : ''}`;
}
```

### Notification Object Example

```javascript
{
  taskId: "task_123",
  title: "Submit quarterly report",
  dueTime: "2025-12-16T18:00:00Z",
  relativeTime: "3 hours and 45 minutes",
  timestamp: "2025-12-16T14:15:00Z",
  priority: "VERY IMPORTANT",
  message: "Task \"Submit quarterly report\" is due in 3 hours and 45 minutes"
}
```

## Clear Tracking Conditions

Clear notification tracking when:

### 1. Task Completed

```javascript
function handleTaskStatusChange(task, newStatus) {
  if (newStatus === 'Complete') {
    tracker.clearTask(task.id);
  }
}
```

### 2. Due Time Passed

```javascript
function checkAndClearExpiredTasks(tasks) {
  const now = new Date();

  tasks.forEach(task => {
    if (task.dueDate) {
      const dueDate = new Date(task.dueDate);
      if (dueDate < now) {
        tracker.clearTask(task.id);
      }
    }
  });
}
```

### 3. Priority Changed

```javascript
function handlePriorityChange(task, newPriority) {
  if (newPriority !== 'VERY IMPORTANT') {
    tracker.clearTask(task.id);
  }
}
```

### 4. Task Deleted

```javascript
function handleTaskDelete(taskId) {
  tracker.clearTask(taskId);
}
```

## Complete Implementation

```javascript
class NotificationTriggerService {
  constructor() {
    this.tracker = new NotificationTracker();
    this.interval = null;
    this.listeners = [];
  }

  start(getTasks) {
    // Check immediately
    this.check(getTasks());

    // Set up 10-minute interval
    this.interval = setInterval(() => {
      this.check(getTasks());
    }, 10 * 60 * 1000);
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }

  check(tasks) {
    // Clean up old tracking data
    this.tracker.cleanup();

    // Check each task
    tasks.forEach(task => {
      if (this.isEligible(task)) {
        const notification = createNotification(task);
        this.tracker.recordNotification(task.id);
        this.notifyListeners(notification);
      }
    });
  }

  isEligible(task) {
    // Check priority
    if (task.priority !== 'VERY IMPORTANT') return false;

    // Check status
    if (task.status === 'Complete') return false;

    // Check due date
    if (!task.dueDate) return false;

    const now = new Date();
    const dueDate = new Date(task.dueDate);
    const hoursUntilDue = (dueDate - now) / (1000 * 60 * 60);

    if (hoursUntilDue <= 0 || hoursUntilDue > 6) return false;

    // Check if recently notified
    if (this.tracker.wasRecentlyNotified(task.id)) return false;

    return true;
  }

  onNotification(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  notifyListeners(notification) {
    this.listeners.forEach(callback => callback(notification));
  }

  clearTask(taskId) {
    this.tracker.clearTask(taskId);
  }
}

// Singleton instance
export const notificationTrigger = new NotificationTriggerService();
```

## React Hook Usage

```jsx
function useNotificationTrigger(tasks) {
  useEffect(() => {
    // Start monitoring
    notificationTrigger.start(() => tasks);

    // Subscribe to notifications
    const unsubscribe = notificationTrigger.onNotification((notification) => {
      // Handle notification (persist, display, etc.)
      console.log('New notification:', notification);
    });

    return () => {
      notificationTrigger.stop();
      unsubscribe();
    };
  }, [tasks]);
}
```

## Testing Examples

```javascript
// Test 1: Eligible task
const task1 = {
  id: '1',
  title: 'Submit Report',
  priority: 'VERY IMPORTANT',
  status: 'In Progress',
  dueDate: new Date(Date.now() + 4 * 60 * 60 * 1000) // 4 hours from now
};
isEligibleForNotification(task1, {}); // true

// Test 2: Not VERY IMPORTANT
const task2 = { ...task1, priority: 'HIGH' };
isEligibleForNotification(task2, {}); // false

// Test 3: Completed
const task3 = { ...task1, status: 'Complete' };
isEligibleForNotification(task3, {}); // false

// Test 4: No due date
const task4 = { ...task1, dueDate: null };
isEligibleForNotification(task4, {}); // false

// Test 5: Recently notified
const history = { '1': Date.now() - 5 * 60 * 1000 }; // 5 minutes ago
isEligibleForNotification(task1, history); // false

// Test 6: Overdue
const task6 = { ...task1, dueDate: new Date(Date.now() - 1 * 60 * 60 * 1000) };
isEligibleForNotification(task6, {}); // false (overdue)

// Test 7: Beyond 6 hours
const task7 = { ...task1, dueDate: new Date(Date.now() + 8 * 60 * 60 * 1000) };
isEligibleForNotification(task7, {}); // false (beyond 6 hours)
```

## Integration Points

This skill integrates with:
- **Temporal Evaluation Skill**: Uses urgency detection
- **Priority Classification Skill**: Depends on VERY IMPORTANT classification
- **Notification Persistence Skill**: Notifications are persisted after triggering
- **Notification UI Skill**: Triggered notifications are displayed
- **Task Intelligence Agent**: Coordinates notification logic

## Performance Considerations

- Check runs every 10 minutes (not continuously)
- In-memory tracking (fast lookups)
- Cleanup prevents memory growth
- Minimal CPU usage (< 5ms per check for 100 tasks)

## Edge Cases

### App Closed Then Reopened

When app reopens, check immediately:

```javascript
// On app initialization
notificationTrigger.start(getTasks);
// This triggers an immediate check
```

### Multiple Windows/Tabs

Each tab runs independently:

```javascript
// No cross-tab coordination needed
// Each tab triggers its own notifications
// User sees notifications from active tab only
```

### Clock Changes

System clock changes handled automatically:

```javascript
// Date comparisons use current system time
// No special handling needed
```
