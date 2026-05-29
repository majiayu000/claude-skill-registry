---
name: task-search
description: Provides fast, case-insensitive text search across task titles, descriptions, and tags with debounced input, relevance ranking, and highlighted matching text. Uses AND logic for multi-token queries and limits results to top 50 for performance.
---

# Task Search Skill

## Overview

The task search skill enables users to quickly find specific tasks using text-based queries. It implements intelligent search algorithms with debouncing, relevance ranking, and visual highlighting of matched terms.

## When to Apply

Apply this skill:
- When user types in the search input field
- After 300ms debounce delay from last keystroke
- When displaying search results in task lists
- When highlighting matched text in search results
- When filtering large task datasets
- When implementing search-as-you-type functionality

## Search Algorithm

### Case-Insensitive Partial Matching

The search algorithm uses case-insensitive partial string matching:

```javascript
function matchesSearchTerm(text, searchTerm) {
  return text.toLowerCase().includes(searchTerm.toLowerCase());
}

// Examples
matchesSearchTerm('Submit Report', 'submit'); // true
matchesSearchTerm('Submit Report', 'SUBMIT'); // true
matchesSearchTerm('Submit Report', 'port'); // true (partial match)
matchesSearchTerm('Submit Report', 'xyz'); // false
```

### Searchable Fields

The search operates across three task fields:

1. **Title** (highest priority)
2. **Description** (medium priority)
3. **Tags** (lower priority)

```javascript
function getSearchableText(task) {
  return {
    title: task.title || '',
    description: task.description || '',
    tags: (task.tags || []).join(' ')
  };
}
```

### Multi-Token Search Logic

The search uses **AND logic** for multiple tokens:

```javascript
function tokenizeQuery(query) {
  return query.trim().split(/\s+/).filter(token => token.length > 0);
}

// Example: "urgent report" splits into ["urgent", "report"]
// Task must match BOTH tokens to be included in results
```

**AND Logic Examples**:
```javascript
// Query: "urgent report"
// Tokens: ["urgent", "report"]

// Match: Task with title "Urgent: Submit Report"
// (contains both "urgent" AND "report")

// No match: Task with title "Submit Report"
// (contains "report" but not "urgent")

// No match: Task with title "Urgent meeting"
// (contains "urgent" but not "report")
```

### Relevance Ranking

Results are ranked by match location (highest to lowest priority):

1. **Exact title match** - Highest relevance
2. **Partial title match** - High relevance
3. **Description match** - Medium relevance
4. **Tag match** - Lower relevance

```javascript
function calculateRelevanceScore(task, tokens) {
  const text = getSearchableText(task);
  let score = 0;

  tokens.forEach(token => {
    const lowerToken = token.toLowerCase();

    // Exact title match: +100 points
    if (text.title.toLowerCase() === lowerToken) {
      score += 100;
    }
    // Partial title match: +50 points
    else if (text.title.toLowerCase().includes(lowerToken)) {
      score += 50;
    }

    // Description match: +10 points
    if (text.description.toLowerCase().includes(lowerToken)) {
      score += 10;
    }

    // Tag match: +5 points
    if (text.tags.toLowerCase().includes(lowerToken)) {
      score += 5;
    }
  });

  return score;
}
```

### Result Limit

Search results are limited to **top 50 matches** for performance:

```javascript
const MAX_SEARCH_RESULTS = 50;

function searchTasks(tasks, query) {
  const tokens = tokenizeQuery(query);

  if (tokens.length === 0) {
    return tasks; // No search query, return all
  }

  // Filter tasks that match all tokens
  const matches = tasks.filter(task => {
    const text = getSearchableText(task);
    const searchableString = `${text.title} ${text.description} ${text.tags}`.toLowerCase();

    return tokens.every(token =>
      searchableString.includes(token.toLowerCase())
    );
  });

  // Calculate relevance scores
  const rankedMatches = matches.map(task => ({
    task,
    score: calculateRelevanceScore(task, tokens)
  }));

  // Sort by relevance (highest first)
  rankedMatches.sort((a, b) => b.score - a.score);

  // Return top 50 results
  return rankedMatches.slice(0, MAX_SEARCH_RESULTS).map(item => item.task);
}
```

## Debounce Timing

### 300ms Delay

Search executes **300ms after the last keystroke** to prevent excessive processing:

```javascript
function useSearchDebounce(query, delay = 300) {
  const [debouncedQuery, setDebouncedQuery] = useState(query);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, delay);

    return () => clearTimeout(timer);
  }, [query, delay]);

  return debouncedQuery;
}

// Usage in component
function TaskSearch({ tasks }) {
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedQuery = useSearchDebounce(searchQuery, 300);

  const searchResults = useMemo(() => {
    return searchTasks(tasks, debouncedQuery);
  }, [tasks, debouncedQuery]);

  return (
    <div>
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search tasks..."
      />
      <TaskList tasks={searchResults} searchQuery={debouncedQuery} />
    </div>
  );
}
```

### Debounce Benefits

- **Reduced CPU usage**: Prevents search on every keystroke
- **Better UX**: Smoother typing experience
- **Network efficiency**: Fewer API calls if searching backend
- **Performance**: Limits processing for large task lists

## Text Highlighting

### Highlight Matched Terms

Matched text is visually highlighted in search results:

```jsx
function highlightText(text, query) {
  if (!query) return text;

  const tokens = tokenizeQuery(query);
  let highlightedText = text;

  tokens.forEach(token => {
    const regex = new RegExp(`(${escapeRegex(token)})`, 'gi');
    highlightedText = highlightedText.replace(
      regex,
      '<mark>$1</mark>'
    );
  });

  return highlightedText;
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Component implementation
function HighlightedText({ text, query }) {
  const highlighted = highlightText(text, query);

  return (
    <span dangerouslySetInnerHTML={{ __html: highlighted }} />
  );
}
```

### Highlight Styling

```css
mark {
  background-color: #FEF3C7; /* Light yellow background */
  color: #92400E; /* Dark amber text */
  padding: 2px 4px;
  border-radius: 2px;
  font-weight: 600;
}

/* Alternative purple theme to match VERY IMPORTANT */
mark.purple-theme {
  background-color: #EDE9FE; /* Light purple background */
  color: #6B21A8; /* Dark purple text */
}
```

### Highlighting Examples

```jsx
// Query: "urgent"
// Text: "Urgent: Submit Report"
// Result: <mark>Urgent</mark>: Submit Report

// Query: "report submit"
// Text: "Submit urgent report"
// Result: <mark>Submit</mark> urgent <mark>report</mark>

// Query: "WORK"
// Text: "Working on project"
// Result: <mark>Work</mark>ing on project (case-insensitive)
```

## Empty State Handling

### No Results Found

When search returns zero results:

```jsx
function SearchResults({ results, query }) {
  if (query && results.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">🔍</div>
        <h3>No tasks found</h3>
        <p>No tasks match your search for "{query}"</p>
        <p className="suggestion">Try different keywords or check your spelling</p>
      </div>
    );
  }

  return (
    <div className="search-results">
      {results.map(task => (
        <TaskCard key={task.id} task={task} searchQuery={query} />
      ))}
    </div>
  );
}
```

### Empty State Styling

```css
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #6B7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #6B7280;
  margin-bottom: 4px;
}

.empty-state .suggestion {
  font-size: 12px;
  color: #9CA3AF;
  font-style: italic;
}
```

## Complete Search Implementation

```jsx
function TaskSearchComponent({ tasks, onSearchResults }) {
  const [searchQuery, setSearchQuery] = useState('');
  const debouncedQuery = useSearchDebounce(searchQuery, 300);

  const searchResults = useMemo(() => {
    return searchTasks(tasks, debouncedQuery);
  }, [tasks, debouncedQuery]);

  useEffect(() => {
    onSearchResults(searchResults);
  }, [searchResults, onSearchResults]);

  const handleClearSearch = () => {
    setSearchQuery('');
  };

  return (
    <div className="task-search">
      <div className="search-input-wrapper">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search tasks by title, description, or tags..."
          className="search-input"
        />
        {searchQuery && (
          <button
            onClick={handleClearSearch}
            className="clear-button"
            aria-label="Clear search"
          >
            ×
          </button>
        )}
      </div>

      {debouncedQuery && (
        <div className="search-info">
          Found {searchResults.length} task{searchResults.length !== 1 ? 's' : ''}
          {searchResults.length >= 50 && ' (showing top 50)'}
        </div>
      )}

      <SearchResults results={searchResults} query={debouncedQuery} />
    </div>
  );
}
```

## Search Input Styling

```css
.task-search {
  width: 100%;
  margin-bottom: 24px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  font-size: 18px;
  color: #9CA3AF;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 40px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #8B5CF6; /* Purple theme */
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.search-input::placeholder {
  color: #9CA3AF;
}

.clear-button {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 20px;
  color: #6B7280;
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s ease;
}

.clear-button:hover {
  color: #DC2626; /* Red on hover */
}

.search-info {
  margin-top: 8px;
  font-size: 12px;
  color: #6B7280;
  font-weight: 500;
}
```

## Testing Examples

### Test Case 1: Single Token Search
```javascript
const tasks = [
  { id: 1, title: 'Submit Report', description: '', tags: [] },
  { id: 2, title: 'Review Code', description: '', tags: [] },
  { id: 3, title: 'Team Meeting', description: '', tags: [] }
];

const results = searchTasks(tasks, 'report');
// Expected: [{ id: 1, title: 'Submit Report', ... }]
```

### Test Case 2: Multi-Token AND Logic
```javascript
const tasks = [
  { id: 1, title: 'Urgent Report', description: '', tags: [] },
  { id: 2, title: 'Submit Report', description: '', tags: ['Urgent'] },
  { id: 3, title: 'Urgent Meeting', description: '', tags: [] }
];

const results = searchTasks(tasks, 'urgent report');
// Expected: [
//   { id: 1, title: 'Urgent Report', ... },
//   { id: 2, title: 'Submit Report', tags: ['Urgent'], ... }
// ]
// Note: Task 3 excluded (has "urgent" but not "report")
```

### Test Case 3: Relevance Ranking
```javascript
const tasks = [
  { id: 1, title: 'Report', description: 'Submit the report', tags: [] },
  { id: 2, title: 'Meeting', description: 'Discuss report', tags: [] },
  { id: 3, title: 'Annual Report', description: '', tags: [] }
];

const results = searchTasks(tasks, 'report');
// Expected order:
// 1. id: 1 (exact title match + description match)
// 2. id: 3 (partial title match)
// 3. id: 2 (description match only)
```

### Test Case 4: Case-Insensitive Search
```javascript
const tasks = [
  { id: 1, title: 'URGENT TASK', description: '', tags: [] }
];

const results = searchTasks(tasks, 'urgent');
// Expected: [{ id: 1, title: 'URGENT TASK', ... }]
```

### Test Case 5: Tag Search
```javascript
const tasks = [
  { id: 1, title: 'Submit Report', description: '', tags: ['Work', 'Urgent'] },
  { id: 2, title: 'Buy Groceries', description: '', tags: ['Personal'] }
];

const results = searchTasks(tasks, 'work');
// Expected: [{ id: 1, title: 'Submit Report', tags: ['Work', 'Urgent'], ... }]
```

### Test Case 6: Empty Query
```javascript
const tasks = [
  { id: 1, title: 'Task 1', description: '', tags: [] },
  { id: 2, title: 'Task 2', description: '', tags: [] }
];

const results = searchTasks(tasks, '');
// Expected: All tasks returned (no filtering)
```

### Test Case 7: Top 50 Limit
```javascript
const tasks = Array.from({ length: 100 }, (_, i) => ({
  id: i + 1,
  title: `Task ${i + 1}`,
  description: 'Common description',
  tags: []
}));

const results = searchTasks(tasks, 'task');
// Expected: Exactly 50 tasks returned
```

## Performance Optimization

### Memoization

```javascript
import { useMemo } from 'react';

function TaskList({ tasks, searchQuery }) {
  const filteredTasks = useMemo(() => {
    return searchTasks(tasks, searchQuery);
  }, [tasks, searchQuery]);

  return (
    <div>
      {filteredTasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}
```

### Virtual Scrolling

For large result sets, implement virtual scrolling:

```jsx
import { FixedSizeList } from 'react-window';

function VirtualTaskList({ tasks, searchQuery }) {
  const filteredTasks = useMemo(() => {
    return searchTasks(tasks, searchQuery);
  }, [tasks, searchQuery]);

  const Row = ({ index, style }) => (
    <div style={style}>
      <TaskCard task={filteredTasks[index]} searchQuery={searchQuery} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={filteredTasks.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

## Integration Points

This skill integrates with:
- **Task Filter Skill**: Combines with filters (search + filters applied together)
- **Task Sorting Skill**: Search results can be sorted
- **Priority Classification Skill**: Search matches can include priority
- **Task Tagging Skill**: Tags are searchable fields
- **Task Organization Agent**: Uses search for task discovery

## Edge Cases

### Special Characters

Escape special regex characters in search queries:

```javascript
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Query: "report (urgent)"
// Escaped: "report \\(urgent\\)"
```

### Whitespace Handling

Trim and collapse whitespace:

```javascript
function tokenizeQuery(query) {
  return query.trim().split(/\s+/).filter(token => token.length > 0);
}

// Query: "  urgent   report  "
// Tokens: ["urgent", "report"]
```

### Empty Descriptions/Tags

Handle null or undefined fields gracefully:

```javascript
function getSearchableText(task) {
  return {
    title: task.title || '',
    description: task.description || '',
    tags: (task.tags || []).join(' ')
  };
}
```

## Accessibility

- Search input has clear focus states
- Clear button has aria-label
- Results count announced to screen readers
- Keyboard navigation supported
- Empty state is descriptive
