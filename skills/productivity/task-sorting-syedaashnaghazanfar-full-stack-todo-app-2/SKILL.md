---
name: task-sorting
description: Provides stable task list sorting across four dimensions (Priority, Due Date, Created Date, Alphabetical) with ascending/descending toggles, tie-breaking rules, and visual sort indicators. Default sort prioritizes VERY IMPORTANT tasks first, then by soonest due date.
---

# Task Sorting Skill

## Overview

The task sorting skill enables users to organize task lists by various criteria with predictable, stable ordering. It implements intelligent tie-breaking rules and visual indicators for the current sort state.

## When to Apply

Apply this skill:
- When displaying task lists (apply default sort)
- When user selects a sort option from sort controls
- When user toggles sort direction (ascending/descending)
- After filtering tasks (sort filtered results)
- After searching tasks (sort search results)
- When tasks are added or updated (maintain sort order)

## Sort Options

This skill defines **four sort options**:

### 1. Priority Sort

Orders tasks by priority level with VERY IMPORTANT highest:

**Order**: VERY IMPORTANT > HIGH > MEDIUM > LOW

**Tie-breaker**: When priorities are equal, sub-sort by due date (soonest first)

```javascript
function sortByPriority(tasks, direction = 'asc') {
  const priorityOrder = {
    'VERY IMPORTANT': 1,
    'HIGH': 2,
    'MEDIUM': 3,
    'LOW': 4
  };

  return [...tasks].sort((a, b) => {
    const aPriority = priorityOrder[a.priority] || 999;
    const bPriority = priorityOrder[b.priority] || 999;

    // Primary sort: Priority
    if (aPriority !== bPriority) {
      return direction === 'asc'
        ? aPriority - bPriority
        : bPriority - aPriority;
    }

    // Tie-breaker: Due date (soonest first)
    return sortByDueDateTiebreaker(a, b);
  });
}
```

### 2. Due Date Sort

Orders tasks by due date with overdue and soon-due first:

**Order**: Overdue first > Soonest > Later > No due date last

**Tie-breaker**: When due dates are equal, use created date (newest first)

```javascript
function sortByDueDate(tasks, direction = 'asc') {
  return [...tasks].sort((a, b) => {
    const aDate = a.dueDate ? new Date(a.dueDate).getTime() : Infinity;
    const bDate = b.dueDate ? new Date(b.dueDate).getTime() : Infinity;

    // Primary sort: Due date
    if (aDate !== bDate) {
      return direction === 'asc'
        ? aDate - bDate // Soonest first
        : bDate - aDate; // Latest first
    }

    // Tie-breaker: Created date
    return sortByCreatedDateTiebreaker(a, b, 'desc'); // Newest first
  });
}
```

### 3. Created Date Sort

Orders tasks by creation timestamp:

**Default direction**: Newest first (descending)

**Tie-breaker**: Created date should be unique, but if equal, use task ID

```javascript
function sortByCreatedDate(tasks, direction = 'desc') {
  return [...tasks].sort((a, b) => {
    const aDate = new Date(a.createdAt).getTime();
    const bDate = new Date(b.createdAt).getTime();

    // Primary sort: Created date
    if (aDate !== bDate) {
      return direction === 'asc'
        ? aDate - bDate // Oldest first
        : bDate - aDate; // Newest first
    }

    // Tie-breaker: Task ID (should be rare)
    return a.id.localeCompare(b.id);
  });
}
```

### 4. Alphabetical Sort

Orders tasks by title alphabetically:

**Comparison**: Case-insensitive, A-Z

**Tie-breaker**: When titles are equal, use created date (newest first)

```javascript
function sortAlphabetically(tasks, direction = 'asc') {
  return [...tasks].sort((a, b) => {
    const aTitle = (a.title || '').toLowerCase();
    const bTitle = (b.title || '').toLowerCase();

    // Primary sort: Title
    if (aTitle !== bTitle) {
      return direction === 'asc'
        ? aTitle.localeCompare(bTitle) // A-Z
        : bTitle.localeCompare(aTitle); // Z-A
    }

    // Tie-breaker: Created date
    return sortByCreatedDateTiebreaker(a, b, 'desc'); // Newest first
  });
}
```

## Default Sort Order

When no sort is explicitly selected, use **priority-first** default:

1. **Primary**: VERY IMPORTANT tasks first
2. **Secondary**: Within same priority, sort by due date (soonest first)
3. **Tertiary**: For tasks with same priority and due date, use created date

```javascript
function defaultSort(tasks) {
  return sortByPriority(tasks, 'asc'); // This applies tie-breaking automatically
}
```

## Stable Sorting

### Preserve Relative Order

For items that compare equal, preserve their original relative order:

```javascript
// Array.sort() in modern JavaScript is stable by spec
// But for explicit control:
function stableSort(array, compareFn) {
  const indexed = array.map((item, index) => ({ item, index }));

  indexed.sort((a, b) => {
    const result = compareFn(a.item, b.item);
    return result !== 0 ? result : a.index - b.index;
  });

  return indexed.map(({ item }) => item);
}
```

### Stability Benefits

- Predictable results: Same input always produces same output
- Multi-level sorting: Secondary sorts don't disrupt primary order
- User trust: Consistent behavior builds confidence

## Tie-Breaking Rules

### Priority Sort Tie-Breaker

When priorities are equal, sort by due date (soonest first):

```javascript
function sortByDueDateTiebreaker(a, b) {
  const aDate = a.dueDate ? new Date(a.dueDate).getTime() : Infinity;
  const bDate = b.dueDate ? new Date(b.dueDate).getTime() : Infinity;
  return aDate - bDate; // Soonest first
}
```

### Due Date Sort Tie-Breaker

When due dates are equal, sort by created date (newest first):

```javascript
function sortByCreatedDateTiebreaker(a, b, direction = 'desc') {
  const aDate = new Date(a.createdAt).getTime();
  const bDate = new Date(b.createdAt).getTime();
  return direction === 'desc' ? bDate - aDate : aDate - bDate;
}
```

### Alphabetical Sort Tie-Breaker

When titles are equal, sort by created date (newest first):

```javascript
// Same as sortByCreatedDateTiebreaker
```

### Final Tie-Breaker

If all else is equal, use task ID for consistent ordering:

```javascript
function finalTiebreaker(a, b) {
  return a.id.localeCompare(b.id);
}
```

## Ascending/Descending Toggle

### Direction State

```javascript
function useSortState() {
  const [sortBy, setSortBy] = useState('priority'); // 'priority' | 'dueDate' | 'createdDate' | 'alphabetical'
  const [direction, setDirection] = useState('asc'); // 'asc' | 'desc'

  const toggleDirection = () => {
    setDirection(prev => prev === 'asc' ? 'desc' : 'asc');
  };

  const changeSortBy = (newSortBy) => {
    if (newSortBy === sortBy) {
      toggleDirection(); // Toggle if same field clicked
    } else {
      setSortBy(newSortBy);
      // Reset to default direction for new field
      setDirection(getDefaultDirection(newSortBy));
    }
  };

  return { sortBy, direction, changeSortBy, toggleDirection };
}

function getDefaultDirection(sortBy) {
  switch (sortBy) {
    case 'priority':
      return 'asc'; // VERY IMPORTANT first
    case 'dueDate':
      return 'asc'; // Soonest first
    case 'createdDate':
      return 'desc'; // Newest first
    case 'alphabetical':
      return 'asc'; // A-Z
    default:
      return 'asc';
  }
}
```

### Toggle Behavior

- **First click**: Apply sort in default direction
- **Second click**: Reverse direction
- **Different field**: Switch to new field with its default direction

## Visual Sort Indicators

### Arrow Icons

Display arrow icon next to active sort column:

```jsx
function SortIndicator({ isActive, direction }) {
  if (!isActive) return null;

  return (
    <span className="sort-arrow">
      {direction === 'asc' ? '↑' : '↓'}
    </span>
  );
}

// Usage in sort button
function SortButton({ label, field, currentSort, currentDirection, onSort }) {
  const isActive = currentSort === field;

  return (
    <button
      className={`sort-button ${isActive ? 'active' : ''}`}
      onClick={() => onSort(field)}
    >
      {label}
      <SortIndicator isActive={isActive} direction={currentDirection} />
    </button>
  );
}
```

### Sort Indicator Styling

```css
.sort-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background-color: transparent;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-button:hover {
  background-color: #F3F4F6;
  border-color: #9CA3AF;
}

.sort-button.active {
  background-color: #EDE9FE; /* Light purple */
  border-color: #8B5CF6; /* Purple */
  color: #6B21A8; /* Dark purple */
  font-weight: 600;
}

.sort-arrow {
  font-size: 16px;
  line-height: 1;
  color: #8B5CF6; /* Purple */
  font-weight: 700;
}
```

## Complete Sort Implementation

```jsx
function TaskSortSystem({ tasks, onSortedTasks }) {
  const [sortBy, setSortBy] = useState('priority');
  const [direction, setDirection] = useState('asc');

  const sortedTasks = useMemo(() => {
    switch (sortBy) {
      case 'priority':
        return sortByPriority(tasks, direction);
      case 'dueDate':
        return sortByDueDate(tasks, direction);
      case 'createdDate':
        return sortByCreatedDate(tasks, direction);
      case 'alphabetical':
        return sortAlphabetically(tasks, direction);
      default:
        return defaultSort(tasks);
    }
  }, [tasks, sortBy, direction]);

  useEffect(() => {
    onSortedTasks(sortedTasks);
  }, [sortedTasks, onSortedTasks]);

  const handleSort = (field) => {
    if (field === sortBy) {
      // Toggle direction
      setDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      // Change sort field
      setSortBy(field);
      setDirection(getDefaultDirection(field));
    }
  };

  return (
    <div className="task-sort-system">
      <div className="sort-controls">
        <span className="sort-label">Sort by:</span>
        <SortButton
          label="Priority"
          field="priority"
          currentSort={sortBy}
          currentDirection={direction}
          onSort={handleSort}
        />
        <SortButton
          label="Due Date"
          field="dueDate"
          currentSort={sortBy}
          currentDirection={direction}
          onSort={handleSort}
        />
        <SortButton
          label="Created"
          field="createdDate"
          currentSort={sortBy}
          currentDirection={direction}
          onSort={handleSort}
        />
        <SortButton
          label="A-Z"
          field="alphabetical"
          currentSort={sortBy}
          currentDirection={direction}
          onSort={handleSort}
        />
      </div>

      <TaskList tasks={sortedTasks} />
    </div>
  );
}
```

## Sort Controls Styling

```css
.task-sort-system {
  width: 100%;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  flex-wrap: wrap;
}

.sort-label {
  font-size: 12px;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-right: 4px;
}
```

## Testing Examples

### Test Case 1: Priority Sort (Ascending)
```javascript
const tasks = [
  { id: '1', title: 'Task 1', priority: 'MEDIUM', dueDate: null, createdAt: '2025-12-15' },
  { id: '2', title: 'Task 2', priority: 'VERY IMPORTANT', dueDate: null, createdAt: '2025-12-16' },
  { id: '3', title: 'Task 3', priority: 'LOW', dueDate: null, createdAt: '2025-12-14' }
];

const sorted = sortByPriority(tasks, 'asc');
// Expected order: Task 2 (VERY IMPORTANT), Task 1 (MEDIUM), Task 3 (LOW)
```

### Test Case 2: Priority Sort with Due Date Tie-Breaker
```javascript
const tasks = [
  { id: '1', priority: 'HIGH', dueDate: '2025-12-20', createdAt: '2025-12-15' },
  { id: '2', priority: 'HIGH', dueDate: '2025-12-18', createdAt: '2025-12-16' },
  { id: '3', priority: 'HIGH', dueDate: '2025-12-19', createdAt: '2025-12-14' }
];

const sorted = sortByPriority(tasks, 'asc');
// Expected order: Task 2 (due 12-18), Task 3 (due 12-19), Task 1 (due 12-20)
```

### Test Case 3: Due Date Sort (Ascending)
```javascript
const tasks = [
  { id: '1', dueDate: '2025-12-20', createdAt: '2025-12-15' },
  { id: '2', dueDate: '2025-12-18', createdAt: '2025-12-16' },
  { id: '3', dueDate: null, createdAt: '2025-12-14' }
];

const sorted = sortByDueDate(tasks, 'asc');
// Expected order: Task 2 (12-18), Task 1 (12-20), Task 3 (no due date)
```

### Test Case 4: Created Date Sort (Descending)
```javascript
const tasks = [
  { id: '1', title: 'Old', createdAt: '2025-12-10' },
  { id: '2', title: 'Recent', createdAt: '2025-12-16' },
  { id: '3', title: 'Middle', createdAt: '2025-12-14' }
];

const sorted = sortByCreatedDate(tasks, 'desc');
// Expected order: Task 2 (12-16), Task 3 (12-14), Task 1 (12-10)
```

### Test Case 5: Alphabetical Sort (Ascending)
```javascript
const tasks = [
  { id: '1', title: 'Zebra task', createdAt: '2025-12-15' },
  { id: '2', title: 'apple task', createdAt: '2025-12-16' },
  { id: '3', title: 'Banana task', createdAt: '2025-12-14' }
];

const sorted = sortAlphabetically(tasks, 'asc');
// Expected order: Task 2 (apple), Task 3 (Banana), Task 1 (Zebra)
// Note: Case-insensitive
```

### Test Case 6: Alphabetical with Equal Titles
```javascript
const tasks = [
  { id: '1', title: 'Same Title', createdAt: '2025-12-14' },
  { id: '2', title: 'Same Title', createdAt: '2025-12-16' },
  { id: '3', title: 'Same Title', createdAt: '2025-12-15' }
];

const sorted = sortAlphabetically(tasks, 'asc');
// Expected order: Task 2 (created 12-16), Task 3 (created 12-15), Task 1 (created 12-14)
// Tie-breaker: Newest first
```

### Test Case 7: Stable Sort
```javascript
const tasks = [
  { id: '1', priority: 'HIGH', dueDate: '2025-12-20', createdAt: '2025-12-15' },
  { id: '2', priority: 'HIGH', dueDate: '2025-12-20', createdAt: '2025-12-15' },
  { id: '3', priority: 'HIGH', dueDate: '2025-12-20', createdAt: '2025-12-15' }
];

const sorted = sortByPriority(tasks, 'asc');
// Expected order: 1, 2, 3 (preserves original order when all fields equal)
```

## Performance Considerations

- Sort operations should complete in < 200ms for 500 tasks
- Use memoization to prevent unnecessary re-sorting
- Array.sort() is O(n log n) complexity
- Stable sort is guaranteed in modern JavaScript
- Avoid sorting on every render (use useMemo)

## Integration Points

This skill integrates with:
- **Task Filter Skill**: Sort filtered results
- **Task Search Skill**: Sort search results
- **Priority Classification Skill**: Uses priority levels for sorting
- **Temporal Evaluation Skill**: Uses due dates for sorting
- **Task Organization Agent**: Applies sorting to organized task lists

## Edge Cases

### Tasks Without Due Dates

Tasks without due dates sort to the end in due date sorting:

```javascript
const aDate = a.dueDate ? new Date(a.dueDate).getTime() : Infinity;
```

### Empty Titles

Tasks with empty or null titles sort first or last depending on direction:

```javascript
const aTitle = (a.title || '').toLowerCase();
// Empty string comes before all others in ascending
```

### Equal Timestamps

Use final tie-breaker (task ID) for absolute consistency:

```javascript
if (aDate === bDate) {
  return a.id.localeCompare(b.id);
}
```

### Invalid Dates

Handle invalid date strings gracefully:

```javascript
function safeParseDate(dateString) {
  if (!dateString) return null;
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? null : date;
}
```

## Accessibility

- Sort buttons have clear labels
- Active sort visually indicated
- Sort direction communicated (arrow icon)
- Keyboard navigation supported
- Screen readers announce sort changes
