---
name: notification-ui
description: Renders notification bell icon with unread count badge, pulse animations for new notifications, and dropdown panel (320px × max 400px) displaying notification items with purple theme for VERY IMPORTANT tasks. Includes mark-as-read interaction and empty state handling.
---

# Notification UI Skill

## Overview

The notification UI skill provides the visual interface for displaying notifications, including a bell icon with badge, animated indicators, and an interactive notification panel.

## When to Apply

Apply this skill:
- When rendering the app header (bell icon)
- When displaying unread notification count
- When showing notification panel/dropdown
- When animating new notification arrivals
- When user interacts with notifications (click to mark as read)
- When displaying empty state (no notifications)

## Bell Icon Specifications

### Icon Size and Position

- **Size**: 24px × 24px
- **Position**: Top-right header
- **Color**: Default #374151 (gray), hover #1F2937 (dark gray)

```jsx
function BellIcon({ unreadCount, onClick }) {
  return (
    <button
      className="bell-icon-button"
      onClick={onClick}
      aria-label={`Notifications (${unreadCount} unread)`}
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="bell-icon"
      >
        <path
          d="M15 17H20L18.5951 15.5951C18.2141 15.2141 18 14.6973 18 14.1585V11C18 8.38757 16.3304 6.16509 14 5.34142V5C14 3.89543 13.1046 3 12 3C10.8954 3 10 3.89543 10 5V5.34142C7.66962 6.16509 6 8.38757 6 11V14.1585C6 14.6973 5.78595 15.2141 5.40493 15.5951L4 17H9M15 17V18C15 19.6569 13.6569 21 12 21C10.3431 21 9 19.6569 9 18V17M15 17H9"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {unreadCount > 0 && (
        <span className="badge">{unreadCount > 99 ? '99+' : unreadCount}</span>
      )}
    </button>
  );
}
```

### Bell Icon Styling

```css
.bell-icon-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.bell-icon-button:hover {
  background-color: #F3F4F6;
}

.bell-icon {
  color: #374151;
  transition: color 0.2s ease;
}

.bell-icon-button:hover .bell-icon {
  color: #1F2937;
}
```

## Unread Count Badge

### Badge Specifications

- **Shape**: Circular
- **Background**: #DC2626 (red)
- **Text**: White (#FFFFFF)
- **Display**: Count up to 99, then "99+"
- **Position**: Top-right corner of bell icon

```css
.badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #DC2626; /* Red */
  color: #FFFFFF; /* White */
  font-size: 10px;
  font-weight: 700;
  border-radius: 50%;
  padding: 0 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
```

### Badge Display Logic

```javascript
function getBadgeText(count) {
  if (count === 0) return null; // No badge
  if (count > 99) return '99+';
  return count.toString();
}
```

## Pulse Animation

### Animation Specifications

- **Duration**: 2 seconds
- **Effect**: Purple glow (#8B5CF6)
- **Trigger**: On new notification arrival
- **Iterations**: 3 times, then stop

```css
@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(139, 92, 246, 0);
  }
}

.bell-icon-button.pulsing {
  animation: pulse 2s ease-in-out 3;
}
```

### Animation Trigger

```jsx
function NotificationBell({ notifications }) {
  const [isPulsing, setIsPulsing] = useState(false);
  const prevCountRef = useRef(notifications.length);

  useEffect(() => {
    // Detect new notification
    if (notifications.length > prevCountRef.current) {
      setIsPulsing(true);

      // Stop animation after 6 seconds (3 iterations × 2s)
      setTimeout(() => setIsPulsing(false), 6000);
    }

    prevCountRef.current = notifications.length;
  }, [notifications.length]);

  return (
    <BellIcon
      className={isPulsing ? 'pulsing' : ''}
      unreadCount={notifications.filter(n => !n.read).length}
    />
  );
}
```

## Notification Dropdown Panel

### Panel Specifications

- **Width**: 320px
- **Max Height**: 400px
- **Scrollable**: Yes (overflow-y: auto)
- **Position**: Dropdown below bell icon
- **Elevation**: Shadow for depth

```css
.notification-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
  background-color: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
              0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

.notification-dropdown-header {
  padding: 16px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-dropdown-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.mark-all-read {
  font-size: 12px;
  color: #8B5CF6;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.mark-all-read:hover {
  color: #7C3AED;
  text-decoration: underline;
}
```

## Notification Item Styling

### Item Specifications

- **Padding**: 16px
- **Border**: Bottom separator (1px solid #F3F4F6)
- **Hover**: Background change to #F9FAFB
- **Purple Theme**: VERY IMPORTANT notifications use #8B5CF6 accent

```css
.notification-item {
  padding: 16px;
  border-bottom: 1px solid #F3F4F6;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.notification-item:hover {
  background-color: #F9FAFB;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: #FAF5FF; /* Very light purple */
}

.notification-item.unread:hover {
  background-color: #F3E8FF; /* Light purple */
}

.notification-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.notification-header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.notification-priority-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #8B5CF6; /* Purple for VERY IMPORTANT */
  margin-top: 6px;
  flex-shrink: 0;
}

.notification-message {
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
  flex: 1;
}

.notification-item.unread .notification-message {
  font-weight: 600;
  color: #111827;
}

.notification-time {
  font-size: 12px;
  color: #9CA3AF;
  display: flex;
  align-items: center;
  gap: 4px;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #8B5CF6; /* Purple */
}
```

## Complete Notification Item Component

```jsx
function NotificationItem({ notification, onMarkAsRead }) {
  const handleClick = () => {
    if (!notification.read) {
      onMarkAsRead(notification.id);
    }
  };

  const relativeTime = formatRelativeTime(notification.timestamp);

  return (
    <div
      className={`notification-item ${notification.read ? '' : 'unread'}`}
      onClick={handleClick}
    >
      <div className="notification-content">
        <div className="notification-header">
          <div className="notification-priority-indicator" />
          <p className="notification-message">{notification.message}</p>
        </div>
        <div className="notification-time">
          {!notification.read && <span className="unread-dot" />}
          <span>{relativeTime}</span>
        </div>
      </div>
    </div>
  );
}

function formatRelativeTime(timestamp) {
  const now = Date.now();
  const diff = now - timestamp;
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
}
```

## Mark-as-Read Interaction

### Click to Mark Read

Clicking an unread notification marks it as read:

```jsx
function handleNotificationClick(notification) {
  if (!notification.read) {
    // Mark as read
    notificationPersistence.markAsRead(notification.id);

    // Update UI state
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(notificationPersistence.getUnreadCount());

    // Optional: Navigate to task
    navigateToTask(notification.taskId);
  }
}
```

### Visual Feedback

```jsx
function NotificationItem({ notification, onMarkAsRead }) {
  const [isMarking, setIsMarking] = useState(false);

  const handleClick = async () => {
    if (!notification.read && !isMarking) {
      setIsMarking(true);
      await onMarkAsRead(notification.id);
      setIsMarking(false);
    }
  };

  return (
    <div
      className={`notification-item ${notification.read ? '' : 'unread'} ${isMarking ? 'marking' : ''}`}
      onClick={handleClick}
    >
      {/* ... */}
    </div>
  );
}
```

## Empty State

### Empty State Component

```jsx
function EmptyState() {
  return (
    <div className="notification-empty-state">
      <div className="empty-icon">🔔</div>
      <p className="empty-title">No notifications</p>
      <p className="empty-description">
        You're all caught up! Notifications for VERY IMPORTANT tasks will appear here.
      </p>
    </div>
  );
}
```

### Empty State Styling

```css
.notification-empty-state {
  padding: 48px 24px;
  text-align: center;
  color: #6B7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #9CA3AF;
  line-height: 1.5;
}
```

## Complete Notification System

```jsx
function NotificationSystem() {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const dropdownRef = useRef(null);

  // Load notifications
  useEffect(() => {
    const loaded = notificationPersistence.getAll();
    setNotifications(loaded);
    setUnreadCount(notificationPersistence.getUnreadCount());
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleMarkAsRead = (id) => {
    notificationPersistence.markAsRead(id);
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(notificationPersistence.getUnreadCount());
  };

  const handleMarkAllAsRead = () => {
    notificationPersistence.markAllAsRead();
    setNotifications(notificationPersistence.getAll());
    setUnreadCount(0);
  };

  return (
    <div className="notification-system" ref={dropdownRef}>
      <NotificationBell
        unreadCount={unreadCount}
        onClick={() => setIsOpen(!isOpen)}
        notifications={notifications}
      />

      {isOpen && (
        <div className="notification-dropdown">
          <div className="notification-dropdown-header">
            <h3 className="notification-dropdown-title">Notifications</h3>
            {unreadCount > 0 && (
              <button className="mark-all-read" onClick={handleMarkAllAsRead}>
                Mark all as read
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="notification-list">
              {notifications.map(notification => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={handleMarkAsRead}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Responsive Behavior

### Mobile Adjustments

```css
@media (max-width: 640px) {
  .notification-dropdown {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    max-height: 100%;
    border-radius: 0;
  }

  .notification-dropdown-header {
    position: sticky;
    top: 0;
    background-color: #FFFFFF;
    z-index: 1;
  }
}
```

## Integration Points

This skill integrates with:
- **Notification Persistence Skill**: Reads notification data
- **Notification Trigger Skill**: Displays triggered notifications
- **Priority Classification Skill**: Uses purple theme for VERY IMPORTANT
- **Notification Experience Agent**: Coordinates UI interactions

## Accessibility

- Bell icon button has aria-label with unread count
- Keyboard navigation supported (Enter/Space to open/close)
- Focus management in dropdown
- Screen reader announcements for new notifications
- Sufficient color contrast ratios (WCAG AA)

## Performance Considerations

- Dropdown renders only when open (conditional rendering)
- Virtual scrolling for large notification lists (>50)
- Debounced mark-as-read operations
- Memoized components to prevent unnecessary re-renders
