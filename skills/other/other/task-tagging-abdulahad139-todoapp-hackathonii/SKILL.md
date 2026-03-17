---
name: task-tagging
description: Provides categorical organization for tasks using a predefined set of seven standard tags (Work, Personal, Shopping, Health, Finance, Learning, Urgent). Enforces tag validation rules including duplicate prevention and 5-tag maximum per task.
---

# Task Tagging Skill

## Overview

The task tagging skill enables contextual categorization of tasks using a standardized set of tags. This skill provides consistent visual styling, validation rules, and user interface behaviors for tag management.

## When to Apply

Apply this skill:
- When creating a new task and user adds tags
- When editing an existing task's tags
- During tag input and autocomplete interactions
- When displaying task lists with tag filters
- During bulk import or migration (to validate and apply tags)
- When rendering tag chips in UI components

## Standard Tag Categories

This skill defines exactly **seven standard tag categories**:

1. **Work** - Professional tasks, meetings, projects
2. **Personal** - Personal errands, appointments, life admin
3. **Shopping** - Purchase items, grocery lists, shopping errands
4. **Health** - Medical appointments, exercise, wellness activities
5. **Finance** - Bills, budgeting, financial planning
6. **Learning** - Study, courses, skill development
7. **Urgent** - Time-sensitive tasks requiring immediate attention

## Tag Rules and Constraints

### Primary and Secondary Tags

- **One primary tag**: The main category for the task
- **Up to 4 secondary tags**: Additional contextual tags
- **Maximum 5 tags total** per task

**Example valid combinations**:
```javascript
// Valid: 1 primary + 2 secondary tags
{ tags: ['Work', 'Urgent', 'Finance'] }

// Valid: 1 primary tag only
{ tags: ['Personal'] }

// Valid: 1 primary + 4 secondary tags (max)
{ tags: ['Work', 'Learning', 'Finance', 'Urgent', 'Health'] }

// Invalid: 6 tags (exceeds maximum)
{ tags: ['Work', 'Personal', 'Shopping', 'Health', 'Finance', 'Learning'] }
```

### Duplicate Prevention

No duplicate tags are allowed on the same task:

```javascript
// Valid: All unique tags
{ tags: ['Work', 'Urgent'] }

// Invalid: 'Work' appears twice
{ tags: ['Work', 'Work', 'Personal'] }
```

### Tag Validation Rules

1. **Maximum count**: 5 tags per task
2. **No duplicates**: Each tag must be unique
3. **Standard categories only**: Tags must be from the predefined set
4. **Case handling**: Tag names are case-sensitive and should match exactly

## Tag Color Scheme

Each tag has a specific color for visual consistency:

### Work Tag
```css
.tag-work {
  background-color: #DBEAFE; /* Light blue background */
  color: #1E40AF; /* Dark blue text */
  border: 1px solid #93C5FD;
}
```
- Background: #DBEAFE (light blue)
- Text: #1E40AF (dark blue)
- Border: #93C5FD (medium blue)

### Personal Tag
```css
.tag-personal {
  background-color: #FCE7F3; /* Light pink background */
  color: #BE185D; /* Dark pink text */
  border: 1px solid #F9A8D4;
}
```
- Background: #FCE7F3 (light pink)
- Text: #BE185D (dark pink)
- Border: #F9A8D4 (medium pink)

### Shopping Tag
```css
.tag-shopping {
  background-color: #FEF3C7; /* Light yellow background */
  color: #92400E; /* Dark amber text */
  border: 1px solid #FCD34D;
}
```
- Background: #FEF3C7 (light yellow)
- Text: #92400E (dark amber)
- Border: #FCD34D (medium yellow)

### Health Tag
```css
.tag-health {
  background-color: #D1FAE5; /* Light green background */
  color: #065F46; /* Dark green text */
  border: 1px solid #6EE7B7;
}
```
- Background: #D1FAE5 (light green)
- Text: #065F46 (dark green)
- Border: #6EE7B7 (medium green)

### Finance Tag
```css
.tag-finance {
  background-color: #E0E7FF; /* Light indigo background */
  color: #3730A3; /* Dark indigo text */
  border: 1px solid #A5B4FC;
}
```
- Background: #E0E7FF (light indigo)
- Text: #3730A3 (dark indigo)
- Border: #A5B4FC (medium indigo)

### Learning Tag
```css
.tag-learning {
  background-color: #FECACA; /* Light red background */
  color: #991B1B; /* Dark red text */
  border: 1px solid #FCA5A5;
}
```
- Background: #FECACA (light red)
- Text: #991B1B (dark red)
- Border: #FCA5A5 (medium red)

### Urgent Tag
```css
.tag-urgent {
  background-color: #FEE2E2; /* Light rose background */
  color: #7F1D1D; /* Dark rose text */
  border: 1px solid #FECACA;
  font-weight: 600; /* Bold for emphasis */
}
```
- Background: #FEE2E2 (light rose)
- Text: #7F1D1D (dark rose)
- Border: #FECACA (medium rose)
- Font weight: 600 (bold)

## UI Chip/Badge Styling

All tag chips follow a consistent design pattern:

```css
.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 16px; /* Rounded corners */
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

/* Hover state */
.tag-chip:hover {
  opacity: 0.8;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Active state */
.tag-chip:active {
  transform: translateY(0);
  box-shadow: none;
}

/* Remove button (X) - hidden by default */
.tag-chip .remove-btn {
  opacity: 0;
  margin-left: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

/* Show remove button on hover */
.tag-chip:hover .remove-btn {
  opacity: 1;
}

.tag-chip .remove-btn:hover {
  color: #DC2626; /* Red on hover */
}
```

**Visual characteristics**:
- Border radius: 16px (fully rounded)
- Padding: 4px 12px
- Font size: 12px
- Font weight: 500
- Gap between text and X button: 4px
- Subtle background colors with contrasting text
- X button appears on hover
- Hover lift effect (translateY -1px)
- Smooth transitions (0.2s)

## Tag Autocomplete Behavior

### Input Field Interaction

When user types in tag input field:

1. **Debounce**: Wait 150ms after last keystroke
2. **Filter**: Show matching tags from standard categories
3. **Case-insensitive matching**: "wor" matches "Work"
4. **Prefix matching**: Match from start of tag name
5. **Limit results**: Show maximum 5 suggestions

### Autocomplete Dropdown

```jsx
function TagAutocomplete({ inputValue, onSelect }) {
  const [suggestions, setSuggestions] = useState([]);

  const standardTags = [
    'Work', 'Personal', 'Shopping',
    'Health', 'Finance', 'Learning', 'Urgent'
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (inputValue.length > 0) {
        const filtered = standardTags.filter(tag =>
          tag.toLowerCase().startsWith(inputValue.toLowerCase())
        );
        setSuggestions(filtered.slice(0, 5));
      } else {
        setSuggestions([]);
      }
    }, 150);

    return () => clearTimeout(timer);
  }, [inputValue]);

  return (
    <div className="autocomplete-dropdown">
      {suggestions.map(tag => (
        <div
          key={tag}
          className="autocomplete-item"
          onClick={() => onSelect(tag)}
        >
          {tag}
        </div>
      ))}
    </div>
  );
}
```

### Autocomplete Styling

```css
.autocomplete-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.autocomplete-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.autocomplete-item:hover {
  background-color: #F3F4F6;
}

.autocomplete-item:active {
  background-color: #E5E7EB;
}
```

## Tag Removal Interaction

### Remove Button Behavior

1. **Hidden by default**: X button has opacity: 0
2. **Show on hover**: Opacity transitions to 1 on chip hover
3. **Click to remove**: Clicking X removes the tag
4. **Confirmation**: Optional confirmation for primary tag removal
5. **Immediate update**: UI updates instantly on removal

### Remove Button Implementation

```jsx
function TagChip({ tag, onRemove, isPrimary }) {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleRemove = () => {
    if (isPrimary && !showConfirm) {
      setShowConfirm(true);
      setTimeout(() => setShowConfirm(false), 3000);
    } else {
      onRemove(tag);
      setShowConfirm(false);
    }
  };

  return (
    <div className={`tag-chip tag-${tag.toLowerCase()}`}>
      <span>{tag}</span>
      <button
        className="remove-btn"
        onClick={handleRemove}
        aria-label={`Remove ${tag} tag`}
      >
        ×
      </button>
      {showConfirm && (
        <span className="confirm-text">Click again to remove</span>
      )}
    </div>
  );
}
```

## Validation Implementation

### Tag Validation Function

```javascript
function validateTags(tags) {
  const errors = [];
  const standardTags = [
    'Work', 'Personal', 'Shopping',
    'Health', 'Finance', 'Learning', 'Urgent'
  ];

  // Check maximum count
  if (tags.length > 5) {
    errors.push('Maximum 5 tags allowed per task');
  }

  // Check for duplicates
  const uniqueTags = new Set(tags);
  if (uniqueTags.size !== tags.length) {
    errors.push('Duplicate tags are not allowed');
  }

  // Check for invalid tags
  const invalidTags = tags.filter(tag => !standardTags.includes(tag));
  if (invalidTags.length > 0) {
    errors.push(`Invalid tags: ${invalidTags.join(', ')}`);
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
```

### Validation Error Display

```jsx
function TagInput({ tags, setTags }) {
  const [validationErrors, setValidationErrors] = useState([]);

  const handleAddTag = (newTag) => {
    const updatedTags = [...tags, newTag];
    const validation = validateTags(updatedTags);

    if (validation.isValid) {
      setTags(updatedTags);
      setValidationErrors([]);
    } else {
      setValidationErrors(validation.errors);
      // Show error for 3 seconds
      setTimeout(() => setValidationErrors([]), 3000);
    }
  };

  return (
    <div className="tag-input-container">
      {/* Tag input field and chips */}
      {validationErrors.length > 0 && (
        <div className="validation-errors">
          {validationErrors.map((error, idx) => (
            <div key={idx} className="error-message">
              {error}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Complete UI Component Example

```jsx
function TaskTagManager({ task, onUpdateTags }) {
  const [tags, setTags] = useState(task.tags || []);
  const [inputValue, setInputValue] = useState('');
  const [showAutocomplete, setShowAutocomplete] = useState(false);

  const standardTags = [
    'Work', 'Personal', 'Shopping',
    'Health', 'Finance', 'Learning', 'Urgent'
  ];

  const getTagClassName = (tag) => {
    return `tag-chip tag-${tag.toLowerCase()}`;
  };

  const handleAddTag = (tag) => {
    const validation = validateTags([...tags, tag]);
    if (validation.isValid) {
      const updatedTags = [...tags, tag];
      setTags(updatedTags);
      onUpdateTags(updatedTags);
      setInputValue('');
      setShowAutocomplete(false);
    } else {
      alert(validation.errors.join('\n'));
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    const updatedTags = tags.filter(tag => tag !== tagToRemove);
    setTags(updatedTags);
    onUpdateTags(updatedTags);
  };

  return (
    <div className="task-tag-manager">
      {/* Display existing tags */}
      <div className="tag-list">
        {tags.map((tag, index) => (
          <div key={tag} className={getTagClassName(tag)}>
            <span>{tag}</span>
            <button
              className="remove-btn"
              onClick={() => handleRemoveTag(tag)}
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {/* Tag input */}
      {tags.length < 5 && (
        <div className="tag-input-wrapper">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onFocus={() => setShowAutocomplete(true)}
            placeholder="Add tag..."
            className="tag-input"
          />
          {showAutocomplete && (
            <TagAutocomplete
              inputValue={inputValue}
              onSelect={handleAddTag}
            />
          )}
        </div>
      )}
    </div>
  );
}
```

## Testing Examples

### Test Case 1: Valid Tag Addition
```javascript
const tags = ['Work', 'Urgent'];
const validation = validateTags([...tags, 'Finance']);
// Expected: { isValid: true, errors: [] }
```

### Test Case 2: Maximum Tags Exceeded
```javascript
const tags = ['Work', 'Personal', 'Shopping', 'Health', 'Finance'];
const validation = validateTags([...tags, 'Learning']);
// Expected: { isValid: false, errors: ['Maximum 5 tags allowed per task'] }
```

### Test Case 3: Duplicate Tag
```javascript
const tags = ['Work', 'Urgent'];
const validation = validateTags([...tags, 'Work']);
// Expected: { isValid: false, errors: ['Duplicate tags are not allowed'] }
```

### Test Case 4: Invalid Tag
```javascript
const tags = ['Work'];
const validation = validateTags([...tags, 'Custom']);
// Expected: { isValid: false, errors: ['Invalid tags: Custom'] }
```

## Integration Points

This skill integrates with:
- **Priority Classification Skill**: Tags can influence priority (e.g., "Urgent" tag)
- **Task Filter Skill**: Enables filtering by specific tags
- **Task Search Skill**: Tags are searchable fields
- **Task Organization Agent**: Uses tagging for contextual organization

## Performance Considerations

- Tag validation should complete in < 1ms
- Autocomplete debounce prevents excessive filtering (150ms)
- Tag chip rendering optimized with CSS transitions
- Maximum 5 tags prevents UI clutter and performance issues

## Accessibility Considerations

- Remove buttons have aria-label for screen readers
- Tag chips are keyboard navigable
- Color contrast ratios meet WCAG AA standards
- Focus states are clearly visible
