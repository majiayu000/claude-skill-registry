---
name: priority-classification
description: Automatically classifies tasks into four priority levels (VERY IMPORTANT, HIGH, MEDIUM, LOW) based on due dates, urgency keywords, and explicit priority settings. Triggers special behaviors for VERY IMPORTANT tasks including notifications and visual emphasis.
---

# Priority Classification Skill

## Overview

The priority classification skill automatically evaluates and assigns priority levels to tasks based on temporal urgency, keyword detection, and explicit priority markers. This skill is fundamental to the todo application's intelligent task management system.

## When to Apply

Apply this skill:
- Immediately when a new task is created
- When a task's due date is updated
- When a task's title or description is modified (to detect urgency keywords)
- When explicit priority is set or changed by user
- During bulk imports or data migrations
- Every 60 seconds for temporal re-evaluation of all tasks

## Priority Levels

This skill defines exactly **four priority levels**:

1. **VERY IMPORTANT** - Highest priority, triggers notifications
2. **HIGH** - Second priority, requires attention soon
3. **MEDIUM** - Standard priority for routine tasks
4. **LOW** - Lowest priority, distant or flexible deadlines

## Classification Logic

### VERY IMPORTANT Classification

A task is classified as VERY IMPORTANT if **ANY** of the following conditions are met:

1. **Temporal urgency**: Task due date is within the next 6 hours
2. **Keyword detection**: Task title or description contains urgency keywords (case-insensitive):
   - "urgent"
   - "critical"
   - "asap"
3. **Explicit marking**: User explicitly sets priority to VERY IMPORTANT

**Example classifications**:
```javascript
// Task due in 4 hours
{ title: "Submit report", dueDate: "2025-12-16T17:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: VERY IMPORTANT (due within 6 hours)

// Task with urgency keyword
{ title: "URGENT: Review contract", dueDate: "2025-12-18T10:00:00" }
// Classification: VERY IMPORTANT (contains "urgent")

// Task with critical keyword
{ title: "Fix critical bug in production", dueDate: "2025-12-20T15:00:00" }
// Classification: VERY IMPORTANT (contains "critical")

// Task with asap keyword
{ title: "Need this asap", dueDate: null }
// Classification: VERY IMPORTANT (contains "asap")
```

### HIGH Classification

A task is classified as HIGH if:

1. Task due date is within the next 24 hours (but not within 6 hours)
2. User explicitly sets priority to HIGH

**Example classifications**:
```javascript
// Task due in 18 hours
{ title: "Prepare presentation", dueDate: "2025-12-17T07:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: HIGH (due within 24 hours)

// Task due in 23 hours
{ title: "Email client", dueDate: "2025-12-17T12:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: HIGH (due within 24 hours)
```

### MEDIUM Classification

A task is classified as MEDIUM if:

1. Task has a reasonable deadline (2-7 days from now)
2. Task has no specific urgency markers
3. User explicitly sets priority to MEDIUM
4. Default priority when no other classification applies

**Example classifications**:
```javascript
// Task due in 3 days
{ title: "Review documentation", dueDate: "2025-12-19T13:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: MEDIUM (reasonable deadline)

// Task due in 5 days
{ title: "Plan team meeting", dueDate: "2025-12-21T10:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: MEDIUM (standard deadline)
```

### LOW Classification

A task is classified as LOW if:

1. Task has a distant deadline (more than 7 days from now)
2. Task has no due date and no urgency keywords
3. User explicitly sets priority to LOW

**Example classifications**:
```javascript
// Task due in 10 days
{ title: "Research new tools", dueDate: "2025-12-26T13:00:00" }
// Current time: 2025-12-16T13:00:00
// Classification: LOW (distant deadline)

// Task with no due date
{ title: "Someday review old notes", dueDate: null }
// Current time: 2025-12-16T13:00:00
// Classification: LOW (no deadline, no urgency keywords)
```

## Visual Styling Rules

Each priority level has specific visual styling to ensure immediate recognition:

### VERY IMPORTANT Styling

```css
.priority-very-important {
  background-color: #8B5CF6; /* Purple background */
  color: #FFFFFF; /* White text */
  font-weight: 600; /* Bold text */
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
  animation: pulse 2s infinite; /* Animated pulse effect */
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(139, 92, 246, 0);
  }
}
```

**Visual characteristics**:
- Background: #8B5CF6 (purple)
- Text: White (#FFFFFF)
- Font weight: 600
- Border radius: 4px
- Padding: 2px 8px
- Font size: 12px
- Animation: 2-second pulse effect with purple glow

### HIGH Styling

```css
.priority-high {
  background-color: transparent;
  color: #EF4444; /* Red accent */
  font-weight: 600;
  border: 1px solid #EF4444;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
}
```

**Visual characteristics**:
- Background: Transparent
- Text: #EF4444 (red)
- Border: 1px solid #EF4444
- Font weight: 600
- Border radius: 4px
- Padding: 2px 8px
- Font size: 12px

### MEDIUM Styling

```css
.priority-medium {
  background-color: transparent;
  color: #F59E0B; /* Yellow accent */
  font-weight: 600;
  border: 1px solid #F59E0B;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
}
```

**Visual characteristics**:
- Background: Transparent
- Text: #F59E0B (yellow/amber)
- Border: 1px solid #F59E0B
- Font weight: 600
- Border radius: 4px
- Padding: 2px 8px
- Font size: 12px

### LOW Styling

```css
.priority-low {
  background-color: transparent;
  color: #6B7280; /* Gray accent */
  font-weight: 600;
  border: 1px solid #6B7280;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
}
```

**Visual characteristics**:
- Background: Transparent
- Text: #6B7280 (gray)
- Border: 1px solid #6B7280
- Font weight: 600
- Border radius: 4px
- Padding: 2px 8px
- Font size: 12px

## Implementation Guidelines

### Classification Function

```javascript
function classifyTaskPriority(task) {
  const now = new Date();
  const dueDate = task.dueDate ? new Date(task.dueDate) : null;

  // Check for explicit priority setting
  if (task.explicitPriority) {
    return task.explicitPriority;
  }

  // Check for urgency keywords
  const urgencyKeywords = ['urgent', 'critical', 'asap'];
  const taskText = `${task.title} ${task.description}`.toLowerCase();
  const hasUrgencyKeyword = urgencyKeywords.some(keyword =>
    taskText.includes(keyword)
  );

  if (hasUrgencyKeyword) {
    return 'VERY_IMPORTANT';
  }

  // Temporal classification
  if (dueDate) {
    const hoursUntilDue = (dueDate - now) / (1000 * 60 * 60);

    if (hoursUntilDue <= 6) {
      return 'VERY_IMPORTANT';
    } else if (hoursUntilDue <= 24) {
      return 'HIGH';
    } else if (hoursUntilDue <= 168) { // 7 days
      return 'MEDIUM';
    } else {
      return 'LOW';
    }
  }

  // Default for tasks with no due date and no urgency
  return 'LOW';
}
```

### UI Component Example

```jsx
function PriorityChip({ priority }) {
  const styles = {
    VERY_IMPORTANT: 'priority-very-important',
    HIGH: 'priority-high',
    MEDIUM: 'priority-medium',
    LOW: 'priority-low'
  };

  const labels = {
    VERY_IMPORTANT: 'VERY IMPORTANT',
    HIGH: 'HIGH',
    MEDIUM: 'MEDIUM',
    LOW: 'LOW'
  };

  return (
    <span className={styles[priority]}>
      {labels[priority]}
    </span>
  );
}
```

## Special Behaviors

### VERY IMPORTANT Triggers

When a task is classified as VERY IMPORTANT:

1. **Visual emphasis**: Apply purple background with pulse animation
2. **Notification triggering**: Task becomes eligible for notification system
3. **Sort priority**: Task appears at top of lists (when sorted by priority)
4. **Alert indicators**: Show special alert icons or badges
5. **Focus requirements**: May require user acknowledgment

### Re-evaluation Schedule

Priority should be re-evaluated:
- **Immediately**: On task creation or update
- **Every 60 seconds**: For temporal drift (tasks approaching deadlines)
- **On page load**: To catch any missed evaluations

## Edge Cases

### Tasks Without Due Dates

Tasks without due dates default to LOW priority unless:
- They contain urgency keywords (→ VERY IMPORTANT)
- User explicitly sets higher priority

### Completed Tasks

Completed tasks retain their priority classification for historical record but:
- Do not trigger notifications
- May be filtered out of active views
- Are excluded from temporal re-evaluation

### Past Due Dates

Tasks with past due dates (overdue):
- Maintain their original classification
- Should display "OVERDUE" status separately from priority
- May be highlighted with additional visual indicators

### Keyword Variations

The keyword detection is case-insensitive and matches partial words:
- "URGENT" → matches
- "urgent" → matches
- "urgently" → matches (contains "urgent")
- "criticality" → matches (contains "critical")

## Integration Points

This skill integrates with:
- **Temporal Evaluation Skill**: Provides time-based classification logic
- **Notification Trigger Skill**: Identifies tasks eligible for notifications
- **Task Sorting Skill**: Provides priority-based sorting
- **Task Filter Skill**: Enables filtering by priority level
- **Notification UI Skill**: Determines visual theme for notifications

## Testing Examples

### Test Case 1: Temporal VERY IMPORTANT
```javascript
const task = {
  id: '1',
  title: 'Submit report',
  dueDate: new Date(Date.now() + 5 * 60 * 60 * 1000), // 5 hours from now
};
const priority = classifyTaskPriority(task);
// Expected: 'VERY_IMPORTANT'
```

### Test Case 2: Keyword VERY IMPORTANT
```javascript
const task = {
  id: '2',
  title: 'URGENT: Review contract',
  dueDate: new Date(Date.now() + 48 * 60 * 60 * 1000), // 2 days from now
};
const priority = classifyTaskPriority(task);
// Expected: 'VERY_IMPORTANT'
```

### Test Case 3: HIGH Priority
```javascript
const task = {
  id: '3',
  title: 'Prepare presentation',
  dueDate: new Date(Date.now() + 20 * 60 * 60 * 1000), // 20 hours from now
};
const priority = classifyTaskPriority(task);
// Expected: 'HIGH'
```

### Test Case 4: MEDIUM Priority
```javascript
const task = {
  id: '4',
  title: 'Review documentation',
  dueDate: new Date(Date.now() + 72 * 60 * 60 * 1000), // 3 days from now
};
const priority = classifyTaskPriority(task);
// Expected: 'MEDIUM'
```

### Test Case 5: LOW Priority
```javascript
const task = {
  id: '5',
  title: 'Research new tools',
  dueDate: new Date(Date.now() + 240 * 60 * 60 * 1000), // 10 days from now
};
const priority = classifyTaskPriority(task);
// Expected: 'LOW'
```

## Performance Considerations

- Classification should complete in < 1ms per task
- Keyword matching uses simple string inclusion (not regex) for performance
- Re-evaluation runs on a 60-second interval (not per-second)
- Bulk classification should be batched for large task lists

## Consistency Rules

- Same task always receives same priority given same inputs
- Priority classification is deterministic (no randomness)
- Temporal classifications update predictably as time passes
- Keyword detection is case-insensitive but language-specific (English)
