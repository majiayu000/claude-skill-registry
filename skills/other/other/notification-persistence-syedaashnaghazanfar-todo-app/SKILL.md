---
name: notification-persistence
description: Stores notifications in localStorage with schema (id, taskId, message, timestamp, read, priority). Provides retrieval methods (getUnread, getAll, markAsRead) and maintains last 50 notifications with automatic cleanup for deleted tasks.
---

# Notification Persistence Skill

## Overview

The notification persistence skill manages the lifecycle of notification data in browser localStorage. It provides CRUD operations, read/unread state management, and automatic cleanup.

## When to Apply

Apply this skill:
- When a notification is triggered (persist immediately)
- When displaying notification history
- When user marks notification as read
- When user deletes a task (cleanup notifications)
- When retrieving unread count for badge display
- When app initializes (load existing notifications)

## Storage Schema

### Notification Object Structure

```typescript
interface Notification {
  id: string; // UUID
  taskId: string; // Associated task ID
  message: string; // Notification message text
  timestamp: number; // Unix timestamp (milliseconds)
  read: boolean; // Read/unread state
  priority: string; // "VERY IMPORTANT"
}
```

### Example Notification

```javascript
{
  id: "550e8400-e29b-41d4-a716-446655440000",
  taskId: "task_123",
  message: "Task \"Submit quarterly report\" is due in 3 hours and 45 minutes",
  timestamp: 1702739700000, // Unix timestamp
  read: false,
  priority: "VERY IMPORTANT"
}
```

## Storage Key

```javascript
const STORAGE_KEY = 'todo-app-notifications';
```

## Core Operations

### 1. Save Notification

```javascript
function saveNotification(notification) {
  try {
    // Generate UUID if not provided
    if (!notification.id) {
      notification.id = generateUUID();
    }

    // Get existing notifications
    const notifications = getAllNotifications();

    // Add new notification
    notifications.unshift(notification); // Add to beginning

    // Keep only last 50
    const limited = notifications.slice(0, 50);

    // Save to localStorage
    localStorage.setItem(STORAGE_KEY, JSON.stringify(limited));

    return notification;
  } catch (error) {
    console.error('Failed to save notification:', error);
    return null;
  }
}
```

### 2. Get All Notifications

```javascript
function getAllNotifications() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];

    const notifications = JSON.parse(stored);

    // Ensure valid structure
    return notifications.filter(n =>
      n.id && n.taskId && n.message && n.timestamp
    );
  } catch (error) {
    console.error('Failed to load notifications:', error);
    return [];
  }
}
```

### 3. Get Unread Notifications

```javascript
function getUnreadNotifications() {
  return getAllNotifications().filter(n => !n.read);
}
```

### 4. Mark as Read

```javascript
function markAsRead(notificationId) {
  try {
    const notifications = getAllNotifications();

    const updated = notifications.map(n =>
      n.id === notificationId ? { ...n, read: true } : n
    );

    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));

    return true;
  } catch (error) {
    console.error('Failed to mark as read:', error);
    return false;
  }
}
```

### 5. Mark All as Read

```javascript
function markAllAsRead() {
  try {
    const notifications = getAllNotifications();

    const updated = notifications.map(n => ({ ...n, read: true }));

    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));

    return true;
  } catch (error) {
    console.error('Failed to mark all as read:', error);
    return false;
  }
}
```

### 6. Delete Notification

```javascript
function deleteNotification(notificationId) {
  try {
    const notifications = getAllNotifications();

    const filtered = notifications.filter(n => n.id !== notificationId);

    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));

    return true;
  } catch (error) {
    console.error('Failed to delete notification:', error);
    return false;
  }
}
```

## Notification History Retention

### 50-Notification Limit

Only the most recent 50 notifications are kept:

```javascript
function enforceLimit() {
  const notifications = getAllNotifications();

  if (notifications.length > 50) {
    const limited = notifications.slice(0, 50);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(limited));
  }
}
```

### Automatic Cleanup on Save

```javascript
// Limit is enforced automatically in saveNotification()
// Oldest notifications are automatically removed
```

## Task Deletion Cleanup

### Remove Associated Notifications

When a task is deleted, remove all its notifications:

```javascript
function cleanupTaskNotifications(taskId) {
  try {
    const notifications = getAllNotifications();

    const filtered = notifications.filter(n => n.taskId !== taskId);

    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));

    return {
      success: true,
      removed: notifications.length - filtered.length
    };
  } catch (error) {
    console.error('Failed to cleanup notifications:', error);
    return { success: false, removed: 0 };
  }
}
```

### Bulk Cleanup

Cleanup notifications for multiple deleted tasks:

```javascript
function bulkCleanup(taskIds) {
  try {
    const notifications = getAllNotifications();

    const taskIdSet = new Set(taskIds);
    const filtered = notifications.filter(n => !taskIdSet.has(n.taskId));

    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));

    return {
      success: true,
      removed: notifications.length - filtered.length
    };
  } catch (error) {
    console.error('Failed to bulk cleanup:', error);
    return { success: false, removed: 0 };
  }
}
```

## UUID Generation

```javascript
function generateUUID() {
  // Use crypto.randomUUID if available
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }

  // Fallback implementation
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
```

## Complete Service Implementation

```javascript
class NotificationPersistenceService {
  constructor() {
    this.storageKey = 'todo-app-notifications';
    this.maxNotifications = 50;
  }

  // Save new notification
  save(notification) {
    if (!notification.id) {
      notification.id = generateUUID();
    }

    if (!notification.timestamp) {
      notification.timestamp = Date.now();
    }

    if (notification.read === undefined) {
      notification.read = false;
    }

    const notifications = this.getAll();
    notifications.unshift(notification);

    const limited = notifications.slice(0, this.maxNotifications);
    this._write(limited);

    return notification;
  }

  // Get all notifications
  getAll() {
    return this._read();
  }

  // Get unread notifications
  getUnread() {
    return this._read().filter(n => !n.read);
  }

  // Get unread count
  getUnreadCount() {
    return this.getUnread().length;
  }

  // Mark notification as read
  markAsRead(id) {
    const notifications = this._read();
    const updated = notifications.map(n =>
      n.id === id ? { ...n, read: true } : n
    );
    this._write(updated);
  }

  // Mark all as read
  markAllAsRead() {
    const notifications = this._read();
    const updated = notifications.map(n => ({ ...n, read: true }));
    this._write(updated);
  }

  // Delete notification
  delete(id) {
    const notifications = this._read();
    const filtered = notifications.filter(n => n.id !== id);
    this._write(filtered);
  }

  // Cleanup notifications for deleted task
  cleanupTask(taskId) {
    const notifications = this._read();
    const filtered = notifications.filter(n => n.taskId !== taskId);
    const removed = notifications.length - filtered.length;
    this._write(filtered);
    return removed;
  }

  // Clear all notifications
  clear() {
    this._write([]);
  }

  // Internal read method
  _read() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (!stored) return [];
      return JSON.parse(stored);
    } catch (error) {
      console.error('Failed to read notifications:', error);
      return [];
    }
  }

  // Internal write method
  _write(notifications) {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(notifications));
    } catch (error) {
      console.error('Failed to write notifications:', error);

      // Handle quota exceeded
      if (error.name === 'QuotaExceededError') {
        console.warn('localStorage quota exceeded, clearing old notifications');
        const limited = notifications.slice(0, 25); // Keep only 25
        localStorage.setItem(this.storageKey, JSON.stringify(limited));
      }
    }
  }
}

// Singleton instance
export const notificationPersistence = new NotificationPersistenceService();
```

## React Hook Usage

```jsx
function useNotificationPersistence() {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  // Load notifications on mount
  useEffect(() => {
    const loaded = notificationPersistence.getAll();
    setNotifications(loaded);
    setUnreadCount(notificationPersistence.getUnreadCount());
  }, []);

  const save = useCallback((notification) => {
    const saved = notificationPersistence.save(notification);
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(notificationPersistence.getUnreadCount());
    return saved;
  }, []);

  const markAsRead = useCallback((id) => {
    notificationPersistence.markAsRead(id);
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(notificationPersistence.getUnreadCount());
  }, []);

  const markAllAsRead = useCallback(() => {
    notificationPersistence.markAllAsRead();
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(0);
  }, []);

  return {
    notifications,
    unreadCount,
    save,
    markAsRead,
    markAllAsRead
  };
}
```

## Error Handling

### localStorage Unavailable

```javascript
function isLocalStorageAvailable() {
  try {
    const test = '__test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
}

// Fallback to in-memory storage
let memoryStorage = {};

function safeGetItem(key) {
  if (isLocalStorageAvailable()) {
    return localStorage.getItem(key);
  }
  return memoryStorage[key] || null;
}

function safeSetItem(key, value) {
  if (isLocalStorageAvailable()) {
    localStorage.setItem(key, value);
  } else {
    memoryStorage[key] = value;
  }
}
```

### Quota Exceeded

```javascript
function handleQuotaExceeded() {
  // Reduce to 25 notifications
  const notifications = getAllNotifications();
  const reduced = notifications.slice(0, 25);

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(reduced));
  } catch (error) {
    // If still failing, clear completely
    localStorage.removeItem(STORAGE_KEY);
  }
}
```

## Testing Examples

```javascript
// Test 1: Save notification
const notification = {
  taskId: 'task_1',
  message: 'Test notification',
  priority: 'VERY IMPORTANT'
};
const saved = notificationPersistence.save(notification);
console.log(saved.id); // UUID generated

// Test 2: Get all
const all = notificationPersistence.getAll();
console.log(all.length); // 1

// Test 3: Mark as read
notificationPersistence.markAsRead(saved.id);
const unread = notificationPersistence.getUnread();
console.log(unread.length); // 0

// Test 4: Cleanup task
notificationPersistence.cleanupTask('task_1');
const remaining = notificationPersistence.getAll();
console.log(remaining.length); // 0

// Test 5: 50-notification limit
for (let i = 0; i < 60; i++) {
  notificationPersistence.save({
    taskId: `task_${i}`,
    message: `Notification ${i}`,
    priority: 'VERY IMPORTANT'
  });
}
const limited = notificationPersistence.getAll();
console.log(limited.length); // 50 (not 60)
```

## Integration Points

This skill integrates with:
- **Notification Trigger Skill**: Persists triggered notifications
- **Notification UI Skill**: Provides data for display
- **Task Management**: Cleans up on task deletion
- **Notification Experience Agent**: Coordinates persistence operations

## Performance Considerations

- Read/write operations < 50ms for 50 notifications
- JSON serialization optimized
- Cleanup operations batched
- Memory-efficient (50-notification limit)
