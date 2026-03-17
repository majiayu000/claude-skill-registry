---
name: task-filter
description: Provides comprehensive task filtering across three dimensions (Status, Priority, Due Date) with cumulative AND logic, localStorage persistence, and removable filter chips UI. Supports nine total filter options across the three categories.
---

# Task Filter Skill

## Overview

The task filter skill enables users to narrow down task lists using multiple filter criteria applied simultaneously. Filters are cumulative (AND logic), persist across sessions, and display as removable chips for easy management.

## When to Apply

Apply this skill:
- When user selects a filter option from filter controls
- When displaying the current active filters as chips
- When user removes a filter chip
- When loading the app (to restore saved filter state)
- When combining filters with search results
- When filter state needs to persist to localStorage

## Filter Types and Options

This skill defines **three filter types** with specific options:

### 1. Status Filter

Four options to filter by task completion status:

- **Not Started** - Tasks that haven't been begun
- **In Progress** - Tasks currently being worked on
- **Complete** - Finished tasks
- **All** - No status filtering (shows all statuses)

```javascript
const STATUS_OPTIONS = {
  NOT_STARTED: 'Not Started',
  IN_PROGRESS: 'In Progress',
  COMPLETE: 'Complete',
  ALL: 'All'
};
```

### 2. Priority Filter

Five options to filter by priority level:

- **VERY IMPORTANT** - Highest priority tasks only
- **HIGH** - High priority tasks only
- **MEDIUM** - Medium priority tasks only
- **LOW** - Low priority tasks only
- **All** - No priority filtering (shows all priorities)

```javascript
const PRIORITY_OPTIONS = {
  VERY_IMPORTANT: 'VERY IMPORTANT',
  HIGH: 'HIGH',
  MEDIUM: 'MEDIUM',
  LOW: 'LOW',
  ALL: 'All'
};
```

### 3. Due Date Filter

Five options to filter by temporal urgency:

- **Overdue** - Tasks with past due dates
- **Today** - Tasks due today (current date)
- **This Week** - Tasks due within current calendar week
- **This Month** - Tasks due within current calendar month
- **All** - No due date filtering (shows all due dates)

```javascript
const DUE_DATE_OPTIONS = {
  OVERDUE: 'Overdue',
  TODAY: 'Today',
  THIS_WEEK: 'This Week',
  THIS_MONTH: 'This Month',
  ALL: 'All'
};
```

## Filter Combination Logic

### Cumulative AND Logic

Multiple filters combine using **AND logic** - a task must match ALL active filters:

```javascript
function applyFilters(tasks, filters) {
  return tasks.filter(task => {
    // Check status filter
    if (filters.status !== 'All' && task.status !== filters.status) {
      return false;
    }

    // Check priority filter
    if (filters.priority !== 'All' && task.priority !== filters.priority) {
      return false;
    }

    // Check due date filter
    if (filters.dueDate !== 'All' && !matchesDueDateFilter(task, filters.dueDate)) {
      return false;
    }

    return true; // Task matches all filters
  });
}
```

### AND Logic Examples

```javascript
// Example 1: Status + Priority filters
// Filters: { status: 'In Progress', priority: 'HIGH', dueDate: 'All' }
// Result: Only tasks that are BOTH "In Progress" AND "HIGH" priority

// Example 2: All three filters
// Filters: { status: 'Not Started', priority: 'VERY IMPORTANT', dueDate: 'Today' }
// Result: Only tasks that are "Not Started" AND "VERY IMPORTANT" AND due "Today"

// Example 3: Single filter
// Filters: { status: 'Complete', priority: 'All', dueDate: 'All' }
// Result: Only completed tasks (no priority or due date restrictions)
```

### "All" Option Behavior

Setting a filter to **"All"** clears that specific filter dimension:

```javascript
// Before: { status: 'In Progress', priority: 'HIGH', dueDate: 'Today' }
// User sets priority to "All"
// After: { status: 'In Progress', priority: 'All', dueDate: 'Today' }
// Effect: Shows In Progress tasks due Today, regardless of priority
```

## Due Date Filter Logic

### Date Comparison Implementation

```javascript
function matchesDueDateFilter(task, dueDateFilter) {
  if (!task.dueDate) return false; // Tasks without due dates excluded

  const taskDue = new Date(task.dueDate);
  const now = new Date();
  now.setHours(0, 0, 0, 0); // Normalize to start of day

  switch (dueDateFilter) {
    case 'Overdue':
      return taskDue < now;

    case 'Today':
      const today = new Date(now);
      const tomorrow = new Date(now);
      tomorrow.setDate(tomorrow.getDate() + 1);
      return taskDue >= today && taskDue < tomorrow;

    case 'This Week':
      const weekStart = getStartOfWeek(now);
      const weekEnd = new Date(weekStart);
      weekEnd.setDate(weekEnd.getDate() + 7);
      return taskDue >= weekStart && taskDue < weekEnd;

    case 'This Month':
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
      const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      return taskDue >= monthStart && taskDue < monthEnd;

    case 'All':
      return true;

    default:
      return true;
  }
}

function getStartOfWeek(date) {
  const day = date.getDay();
  const diff = date.getDate() - day; // Sunday as start of week
  const startOfWeek = new Date(date);
  startOfWeek.setDate(diff);
  startOfWeek.setHours(0, 0, 0, 0);
  return startOfWeek;
}
```

### Due Date Examples

```javascript
// Assume today is 2025-12-16

// Task due 2025-12-15 (yesterday)
matchesDueDateFilter(task, 'Overdue'); // true
matchesDueDateFilter(task, 'Today'); // false

// Task due 2025-12-16 (today)
matchesDueDateFilter(task, 'Overdue'); // false
matchesDueDateFilter(task, 'Today'); // true
matchesDueDateFilter(task, 'This Week'); // true

// Task due 2025-12-18 (this week)
matchesDueDateFilter(task, 'This Week'); // true
matchesDueDateFilter(task, 'This Month'); // true

// Task due 2025-12-28 (this month, but not this week)
matchesDueDateFilter(task, 'This Week'); // false
matchesDueDateFilter(task, 'This Month'); // true

// Task with no due date
matchesDueDateFilter(task, 'Overdue'); // false (excluded)
matchesDueDateFilter(task, 'All'); // true
```

## Filter Persistence

### localStorage Storage

Filter state persists across browser sessions using localStorage:

```javascript
const FILTER_STORAGE_KEY = 'todo-app-filters';

function saveFilters(filters) {
  try {
    localStorage.setItem(FILTER_STORAGE_KEY, JSON.stringify(filters));
  } catch (error) {
    console.error('Failed to save filters:', error);
  }
}

function loadFilters() {
  try {
    const saved = localStorage.getItem(FILTER_STORAGE_KEY);
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (error) {
    console.error('Failed to load filters:', error);
  }

  // Return default filters if none saved
  return {
    status: 'All',
    priority: 'All',
    dueDate: 'All'
  };
}

function clearFilters() {
  try {
    localStorage.removeItem(FILTER_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear filters:', error);
  }
}
```

### Persistence Behavior

- **On filter change**: Save immediately to localStorage
- **On app load**: Restore filters from localStorage
- **On clear all**: Remove from localStorage and reset to defaults
- **On logout**: Optionally clear filters (user preference)

## Filter Chips UI

### Active Filter Display

Active filters display as removable chips above the task list:

```jsx
function FilterChips({ filters, onRemoveFilter }) {
  const activeFilters = [];

  if (filters.status !== 'All') {
    activeFilters.push({ type: 'status', value: filters.status });
  }
  if (filters.priority !== 'All') {
    activeFilters.push({ type: 'priority', value: filters.priority });
  }
  if (filters.dueDate !== 'All') {
    activeFilters.push({ type: 'dueDate', value: filters.dueDate });
  }

  if (activeFilters.length === 0) {
    return null; // No active filters
  }

  return (
    <div className="filter-chips">
      <span className="filter-label">Active filters:</span>
      {activeFilters.map(filter => (
        <div key={filter.type} className="filter-chip">
          <span className="filter-value">{filter.value}</span>
          <button
            className="remove-btn"
            onClick={() => onRemoveFilter(filter.type)}
            aria-label={`Remove ${filter.value} filter`}
          >
            ×
          </button>
        </div>
      ))}
      {activeFilters.length > 1 && (
        <button
          className="clear-all-btn"
          onClick={() => onRemoveFilter('all')}
        >
          Clear all
        </button>
      )}
    </div>
  );
}
```

### Filter Chip Styling

```css
.filter-chips {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background-color: #EDE9FE; /* Light purple */
  color: #6B21A8; /* Dark purple */
  border: 1px solid #C4B5FD;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.filter-chip:hover {
  background-color: #DDD6FE;
  border-color: #A78BFA;
}

.filter-value {
  user-select: none;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background: transparent;
  border: none;
  font-size: 18px;
  line-height: 1;
  color: #6B21A8;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s ease;
}

.remove-btn:hover {
  color: #DC2626; /* Red on hover */
}

.clear-all-btn {
  padding: 6px 12px;
  background-color: transparent;
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-all-btn:hover {
  background-color: #FEE2E2;
  border-color: #DC2626;
}
```

### Chip Removal Behavior

Clicking a chip's remove button clears that specific filter:

```javascript
function handleRemoveFilter(filterType) {
  if (filterType === 'all') {
    // Clear all filters
    setFilters({
      status: 'All',
      priority: 'All',
      dueDate: 'All'
    });
  } else {
    // Clear specific filter
    setFilters(prev => ({
      ...prev,
      [filterType]: 'All'
    }));
  }
}
```

## Complete Filter Implementation

```jsx
function TaskFilterSystem({ tasks, onFilteredTasks }) {
  const [filters, setFilters] = useState(() => loadFilters());

  // Save filters to localStorage whenever they change
  useEffect(() => {
    saveFilters(filters);
  }, [filters]);

  // Apply filters to tasks
  const filteredTasks = useMemo(() => {
    return applyFilters(tasks, filters);
  }, [tasks, filters]);

  // Notify parent of filtered results
  useEffect(() => {
    onFilteredTasks(filteredTasks);
  }, [filteredTasks, onFilteredTasks]);

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const handleRemoveFilter = (filterType) => {
    if (filterType === 'all') {
      setFilters({
        status: 'All',
        priority: 'All',
        dueDate: 'All'
      });
    } else {
      setFilters(prev => ({
        ...prev,
        [filterType]: 'All'
      }));
    }
  };

  return (
    <div className="task-filter-system">
      <FilterControls filters={filters} onChange={handleFilterChange} />
      <FilterChips filters={filters} onRemoveFilter={handleRemoveFilter} />
      <TaskList tasks={filteredTasks} />
    </div>
  );
}
```

## Filter Controls UI

```jsx
function FilterControls({ filters, onChange }) {
  return (
    <div className="filter-controls">
      {/* Status Filter */}
      <div className="filter-group">
        <label>Status</label>
        <select
          value={filters.status}
          onChange={(e) => onChange('status', e.target.value)}
          className="filter-select"
        >
          <option value="All">All</option>
          <option value="Not Started">Not Started</option>
          <option value="In Progress">In Progress</option>
          <option value="Complete">Complete</option>
        </select>
      </div>

      {/* Priority Filter */}
      <div className="filter-group">
        <label>Priority</label>
        <select
          value={filters.priority}
          onChange={(e) => onChange('priority', e.target.value)}
          className="filter-select"
        >
          <option value="All">All</option>
          <option value="VERY IMPORTANT">VERY IMPORTANT</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="LOW">LOW</option>
        </select>
      </div>

      {/* Due Date Filter */}
      <div className="filter-group">
        <label>Due Date</label>
        <select
          value={filters.dueDate}
          onChange={(e) => onChange('dueDate', e.target.value)}
          className="filter-select"
        >
          <option value="All">All</option>
          <option value="Overdue">Overdue</option>
          <option value="Today">Today</option>
          <option value="This Week">This Week</option>
          <option value="This Month">This Month</option>
        </select>
      </div>
    </div>
  );
}
```

### Filter Controls Styling

```css
.filter-controls {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 160px;
}

.filter-group label {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 14px;
  color: #374151;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: #9CA3AF;
}

.filter-select:focus {
  outline: none;
  border-color: #8B5CF6; /* Purple theme */
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}
```

## Testing Examples

### Test Case 1: Single Status Filter
```javascript
const tasks = [
  { id: 1, status: 'Not Started', priority: 'HIGH', dueDate: null },
  { id: 2, status: 'In Progress', priority: 'MEDIUM', dueDate: null },
  { id: 3, status: 'Complete', priority: 'LOW', dueDate: null }
];

const filters = { status: 'In Progress', priority: 'All', dueDate: 'All' };
const result = applyFilters(tasks, filters);
// Expected: [{ id: 2, status: 'In Progress', ... }]
```

### Test Case 2: Multiple Filters (AND Logic)
```javascript
const tasks = [
  { id: 1, status: 'In Progress', priority: 'HIGH', dueDate: '2025-12-16' },
  { id: 2, status: 'In Progress', priority: 'MEDIUM', dueDate: '2025-12-16' },
  { id: 3, status: 'Not Started', priority: 'HIGH', dueDate: '2025-12-16' }
];

const filters = { status: 'In Progress', priority: 'HIGH', dueDate: 'Today' };
const result = applyFilters(tasks, filters);
// Expected: [{ id: 1, ... }] (only task matching all three filters)
```

### Test Case 3: Overdue Filter
```javascript
const now = new Date('2025-12-16');
const tasks = [
  { id: 1, status: 'Not Started', priority: 'HIGH', dueDate: '2025-12-15' },
  { id: 2, status: 'In Progress', priority: 'MEDIUM', dueDate: '2025-12-17' }
];

const filters = { status: 'All', priority: 'All', dueDate: 'Overdue' };
const result = applyFilters(tasks, filters);
// Expected: [{ id: 1, dueDate: '2025-12-15', ... }]
```

### Test Case 4: All Filters Set to "All"
```javascript
const tasks = [
  { id: 1, status: 'Not Started', priority: 'HIGH', dueDate: null },
  { id: 2, status: 'In Progress', priority: 'MEDIUM', dueDate: null },
  { id: 3, status: 'Complete', priority: 'LOW', dueDate: null }
];

const filters = { status: 'All', priority: 'All', dueDate: 'All' };
const result = applyFilters(tasks, filters);
// Expected: All 3 tasks (no filtering applied)
```

## Integration Points

This skill integrates with:
- **Task Search Skill**: Filters applied after search (search + filter)
- **Task Sorting Skill**: Filtered results can be sorted
- **Priority Classification Skill**: Filters by priority levels
- **Temporal Evaluation Skill**: Provides due date filtering logic
- **Task Organization Agent**: Uses filtering for task management

## Performance Considerations

- Filter application should complete in < 100ms for 1000 tasks
- localStorage operations are wrapped in try-catch for error handling
- useMemo prevents unnecessary re-filtering
- Filter state changes are batched with React state updates

## Edge Cases

### Tasks Without Due Dates
Tasks with no due date are excluded from all due date filters except "All":

```javascript
// Task: { dueDate: null }
matchesDueDateFilter(task, 'Overdue'); // false
matchesDueDateFilter(task, 'Today'); // false
matchesDueDateFilter(task, 'This Week'); // false
matchesDueDateFilter(task, 'All'); // true
```

### Week Boundaries
Week calculation uses Sunday as the start of the week (configurable):

```javascript
// Configurable week start day
function getStartOfWeek(date, weekStartDay = 0) { // 0 = Sunday, 1 = Monday
  const day = date.getDay();
  const diff = (day < weekStartDay ? 7 : 0) + day - weekStartDay;
  const startOfWeek = new Date(date);
  startOfWeek.setDate(date.getDate() - diff);
  startOfWeek.setHours(0, 0, 0, 0);
  return startOfWeek;
}
```

## Accessibility

- Filter dropdowns have descriptive labels
- Remove buttons have aria-labels
- Filter chips are keyboard navigable
- Clear all button has clear visual affordance
- Active filters announced to screen readers
