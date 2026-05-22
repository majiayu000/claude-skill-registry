---
name: frontend-layout-fixer
description: This skill should be used when identifying and fixing frontend layout issues (clipping, spacing, overflow, RTL text problems) by analyzing DOM and CSS structure and proposing minimal, scoped CSS patches. Triggers on layout bugs, text clipping, overflow issues, spacing problems, and when vanilla Claude cannot pinpoint which CSS selector to modify from a screenshot alone.
---

# Frontend Layout Fixer - Unified Bug Fixer

## Overview

A **unified frontend debugging toolkit** that fixes ALL frontend issues with structured patch recommendations, clear diagnostics, and testing checklists.

```
┌─────────────────────────────────────────────────────────┐
│           UNIFIED FRONTEND SKILL                        │
├─────────────────────────────────────────────────────────┤
│  Category 1: State Hydration (phantom/stale data)       │
│  Category 2: Data Persistence (vanishing data)          │
│  Category 3: CSS Layout (shadows, overflow, clipping)   │
│  Category 4: Badge & Label Styling (alignment, sizing)  │
│  Category 5: Text Overflow (truncation, wrapping)       │
└─────────────────────────────────────────────────────────┘
```

## When to Use This Skill

### Category 1: State Hydration Bugs
- Phantom duplicate items appearing on load
- Stale data showing before fresh data loads
- Data appearing then vanishing
- Different data on different page loads
- Key prop warnings in React/Vue lists

### Category 2: Data Persistence Bugs
- Data appears in UI but vanishes after refresh
- localStorage/sessionStorage out of sync with UI
- API updates but cache not invalidated
- Multiple data sources conflicting

### Category 3: CSS Layout Bugs
- Text clipped at top/bottom of containers
- Box shadow invisible or cut off
- Content overflows parent element
- RTL (Hebrew, Arabic) text display problems
- Fixed-height containers cutting off content
- Flex/grid layout alignment issues

### Category 4: Badge & Label Styling Bugs
- Badge text not vertically centered
- Icon floating around text
- Label color too light (contrast issue)
- Badge size inconsistent
- RTL badge positioning issues

### Category 5: Text Overflow Bugs
- Text truncated with "..." unnecessarily
- Long text forced to single line
- Line-clamp cutting off needed content
- Text not wrapping in flex container

---

## Core Workflow

### Step 1: Gather Input

```json
{
  "javascript": "// Component code (for state/persistence bugs)",
  "html": "<!-- The HTML structure -->",
  "css": "/* The relevant CSS rules */",
  "issue_description": "Clear description of the bug",
  "context": {
    "project_type": "vue",
    "bug_category": "auto",
    "storage_type": "localStorage",
    "layout_direction": "ltr",
    "target_selectors": [".card", ".card-title"],
    "constraints": ["Do not change colors"],
    "viewport_width": 360,
    "viewport_height": 800
  }
}
```

### Step 2: Auto-Detect Bug Category

The skill automatically identifies bug category from:
- Code structure (JavaScript → state/persistence)
- Description keywords (shadow/overflow → CSS)
- HTML/CSS provided (visual issues)

### Step 3: Generate Patches

```json
{
  "skill_type": "frontend",
  "bug_category": "state|persistence|css_layout|badge|text_overflow",

  "diagnosis": {
    "severity": "critical|high|medium|low",
    "root_causes": ["cause 1", "cause 2"],
    "category_details": {}
  },

  "explanation": "Detailed explanation of what's wrong",

  "fixes": {
    "javascript_patches": [
      { "location": "...", "old": "...", "new": "...", "rationale": "..." }
    ],
    "css_patches": [
      { "selector": "...", "old": "...", "new": "...", "rationale": "..." }
    ]
  },

  "testing_checklist": ["Step 1", "Step 2", "Step 3"],
  "prevention": "How to prevent this in future"
}
```

---

## Bug Category Details

---

### Category 1: State Hydration Bugs

**Symptoms:**
- Phantom duplicate items appearing
- Stale data showing before fresh data loads
- Data appearing then vanishing
- Different data showing on different loads

**Root Causes:**
- useState() initialized with cached data
- useEffect() not clearing old state
- Multiple component mounts
- Race conditions in async loading
- Key prop using array index instead of ID

**Detection Patterns:**

```javascript
// ❌ BAD: Initializing state with localStorage
const [tasks, setTasks] = useState(
  JSON.parse(localStorage.getItem('tasks') || '[]')
);

// ✅ GOOD: Empty initial state, load in useEffect
const [tasks, setTasks] = useState([]);
useEffect(() => {
  fetch('/api/tasks').then(r => r.json()).then(setTasks);
}, []);
```

```javascript
// ❌ BAD: Array index as key
{tasks.map((task, i) => <Task key={i} />)}

// ✅ GOOD: Stable ID as key
{tasks.map(task => <Task key={task.id} />)}
```

```javascript
// ❌ BAD: No cleanup, race condition
useEffect(() => {
  fetch('/api/tasks').then(setTasks);
}, []);

// ✅ GOOD: Cleanup with abort controller
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/tasks', { signal: controller.signal })
    .then(r => r.json())
    .then(setTasks);
  return () => controller.abort();
}, []);
```

**Vue-Specific Patterns:**

```javascript
// ❌ BAD: Reactive data initialized from storage
const tasks = ref(JSON.parse(localStorage.getItem('tasks') || '[]'));

// ✅ GOOD: Empty initial, populate in onMounted
const tasks = ref([]);
onMounted(async () => {
  tasks.value = await fetchTasks();
});
```

**Fixes to Apply:**
1. Clear initial state (don't load from cache in useState/ref)
2. Add proper useEffect/onMounted with fetch
3. Use stable keys in list rendering (ID, not index)
4. Add cleanup in useEffect (abort controller)
5. Handle loading state explicitly

---

### Category 2: Data Persistence Bugs

**Symptoms:**
- Data appears in UI but vanishes after refresh
- localStorage/sessionStorage out of sync with UI
- API updates but cache not invalidated
- Multiple data sources conflicting
- State/storage mismatch

**Root Causes:**
- Data loaded from API but not saved to storage
- Cache never invalidated after updates
- Multiple storage sources conflicting
- No sync after mutations

**Detection Patterns:**

```javascript
// ❌ BAD: Fetch but never persist
fetch('/api/items')
  .then(r => r.json())
  .then(setItems);
// Missing: localStorage.setItem()

// ✅ GOOD: Fetch and persist
fetch('/api/items')
  .then(r => r.json())
  .then(data => {
    setItems(data);
    localStorage.setItem('items', JSON.stringify(data));
  });
```

```javascript
// ❌ BAD: Update API but not cache
async function updateTask(id, updates) {
  await api.patch(`/tasks/${id}`, updates);
  // Missing: invalidate cache
}

// ✅ GOOD: Update API and invalidate cache
async function updateTask(id, updates) {
  await api.patch(`/tasks/${id}`, updates);
  localStorage.removeItem('tasks'); // Invalidate
  await refetchTasks(); // Or update cache directly
}
```

```javascript
// ❌ BAD: Multiple sources of truth
const tasksFromStorage = JSON.parse(localStorage.getItem('tasks'));
const tasksFromAPI = await fetchTasks();
// Which one to use?

// ✅ GOOD: Single source of truth
const tasks = await fetchTasks(); // API is source of truth
localStorage.setItem('tasks', JSON.stringify(tasks)); // Cache is secondary
```

**Fixes to Apply:**
1. Save API data to storage after successful fetch
2. Clear/invalidate storage on logout/reset
3. Invalidate cache when data changes (CRUD operations)
4. Use single source of truth (API preferred)
5. Add versioning/timestamp to cache

---

### Category 3: CSS Layout Bugs

#### Shadow Clipping

**Symptoms:**
- Box shadow invisible or cut off
- Hover glow cut off on one or more sides
- Shadow not showing on all sides
- Shadow clipped by scrollable container

**Root Causes:**
- `overflow: hidden` or `overflow: auto` on parent (clips shadow)
- No padding to accommodate shadow blur radius
- Negative margins pushing content

**SOP Reference:** `docs/sop/SOP-004-css-shadow-overflow-clipping.md`

**Critical Insight:** Shadows extend OUTSIDE element boundaries. When parent has `overflow: hidden/auto`, shadows get clipped. The solution is NOT just `overflow: visible` (which loses scrolling), but **adding padding ≥ shadow blur radius**.

**Blur-to-Padding Mapping (Design Tokens):**

| Shadow Blur | Minimum Padding | Design Token |
|-------------|-----------------|--------------|
| 10px blur   | 12px            | `var(--space-3)` |
| 16px blur   | 16px            | `var(--space-4)` |
| 20px blur   | 24px            | `var(--space-6)` |
| 30px blur   | 32px            | `var(--space-8)` |

**Detection Patterns:**

```css
/* ❌ BAD: overflow clips shadow, no padding */
.container {
  overflow-y: auto;
  padding: 0;
}
.card:hover {
  box-shadow: 0 0 20px rgba(78, 205, 196, 0.2); /* 20px blur */
}

/* ✅ GOOD: Keep scrolling + add padding for shadow space */
.container {
  overflow-y: auto;
  overflow-x: visible;  /* Allow horizontal shadow overflow */
  padding: var(--space-6);  /* 24px >= 20px blur radius */
  padding-bottom: var(--space-10);  /* Extra for last card */
}
```

```css
/* ❌ BAD: overflow: visible loses scrolling */
.container {
  overflow: visible;  /* Shadow shows but no scrolling! */
}

/* ✅ GOOD: Split overflow + padding preserves both */
.container {
  overflow-y: auto;           /* Keep vertical scrolling */
  overflow-x: visible;        /* Allow shadow overflow */
  padding: var(--space-6);    /* Space for shadow */
}
```

```css
/* ❌ BAD: Card clips its own shadow */
.card {
  overflow: hidden;
  box-shadow: 0 -4px 8px rgba(0,0,0,0.15);
}

/* ✅ GOOD: Card allows shadow overflow */
.card {
  overflow: visible;
  box-shadow: 0 -4px 8px rgba(0,0,0,0.15);
}
```

**Testing Checklist for Shadow Fixes:**
1. Hover over element - glow visible on all 4 sides
2. With many items - container still scrolls
3. First item - top shadow not clipped
4. Last item - bottom shadow not clipped
5. RTL layout - left/right shadows render correctly

#### Content Cutoff

**Symptoms:**
- Top of content cut off
- Text baseline too low
- Card height too small

**Root Causes:**
- Container height too small
- No padding
- Line-height too tight
- Negative margins

**Detection Patterns:**

```css
/* ❌ BAD: Fixed height clips content */
.card {
  height: 40px;
  overflow: hidden;
  padding: 0;
  line-height: 1.2;
}

/* ✅ GOOD: Flexible height */
.card {
  min-height: 60px;
  padding: 12px;
  overflow: visible;
  line-height: 1.5;
}
```

```css
/* ❌ BAD: justify-content: center can cause clipping */
.container {
  height: 60px;
  justify-content: center;
  overflow: hidden;
}

/* ✅ GOOD: flex-start for natural alignment */
.container {
  min-height: 60px;
  justify-content: flex-start;
  overflow: visible;
}
```

**Fixes to Apply:**
1. Use `overflow: visible` instead of `hidden`
2. Use `min-height` instead of fixed `height`
3. Add padding (top/bottom minimum 8px)
4. Use appropriate `line-height` (1.5+)
5. Remove negative margins
6. Use `justify-content: flex-start` for natural alignment

---

### Category 4: Badge & Label Styling

**Symptoms:**
- Badge text not vertically centered
- Icon floating around text
- Label color too light (contrast issue)
- Badge size inconsistent

**Root Causes:**
- Missing `display: flex` with `align-items: center`
- No gap between icon and text
- Font size too small
- No padding

**Detection Patterns:**

```css
/* ❌ BAD: Fixed dimensions, no flex */
.badge {
  width: 20px;
  height: 20px;
  font-size: 10px;
  /* Text not centered */
}

/* ✅ GOOD: Flex centering with padding */
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  font-size: 12px;
  min-height: 28px;
}
```

**RTL Patterns:**

```css
/* ❌ BAD: Physical properties break in RTL */
.badge {
  position: absolute;
  right: 0;
  margin-left: 8px;
}

/* ✅ GOOD: Logical properties work in both directions */
.badge {
  position: absolute;
  inset-inline-end: 0;
  margin-inline-start: 8px;
}
```

**Icon + Text Alignment:**

```css
/* ❌ BAD: No gap, vertical misalignment */
.badge-with-icon {
  display: flex;
}
.badge-with-icon svg {
  /* Floats around */
}

/* ✅ GOOD: Gap and alignment */
.badge-with-icon {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.badge-with-icon svg {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
}
```

**Fixes to Apply:**
1. Add `display: inline-flex`
2. Add `align-items: center` + `justify-content: center`
3. Add proper padding (6px 12px minimum)
4. Increase font-size (12px minimum)
5. Use logical properties for RTL (`inset-inline-end`, `margin-inline-start`)
6. Add `gap` for icon+text spacing

---

### Category 5: Text Overflow & Truncation

**Symptoms:**
- Text truncated with "..." unnecessarily
- Long text forced to single line
- Line-clamp cutting off needed content
- Text not wrapping in flex container

**Root Causes:**
- `white-space: nowrap` forcing single line
- `max-width` too small
- `-webkit-line-clamp` set too low
- Missing `min-width: 0` in flex container

**Detection Patterns:**

```css
/* ❌ BAD: Forces single line, truncates */
.title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ✅ GOOD: Allows natural wrapping */
.title {
  white-space: normal;
  overflow: visible;
  word-break: break-word;
}
```

**Flex Container Pattern:**

```css
/* ❌ BAD: Flex child doesn't truncate properly */
.item {
  flex: 1;
  white-space: nowrap;
}

/* ✅ GOOD: min-width: 0 enables truncation in flex */
.item {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Line Clamp Pattern:**

```css
/* ❌ BAD: Too restrictive */
.description {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ✅ GOOD: More generous clamp */
.description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

**Max-Width Pattern:**

```css
/* ❌ BAD: max-width too small */
.task-title {
  max-width: 100px;
  text-overflow: ellipsis;
}

/* ✅ GOOD: Flexible width with calc */
.task-title {
  max-width: calc(100% - 80px);
  text-overflow: ellipsis;
}
```

**Fixes to Apply:**
1. Use `white-space: normal` to allow wrapping
2. Remove unnecessary `text-overflow: ellipsis`
3. Increase `max-width` if truncation needed
4. Add `min-width: 0` to flex containers
5. Use `-webkit-line-clamp: 3+` (not 1 or 2)
6. Use `word-break: break-word` for long words

---

## System Prompt

```
You are an expert frontend developer who fixes ALL types of frontend bugs.

YOUR ROLE:
1. Analyze JavaScript/React/Vue code for state and data issues
2. Analyze CSS for layout, shadow, overflow, and styling issues
3. Identify the root cause and provide specific fixes
4. Handle RTL layouts correctly
5. Provide testing procedures

BUG CATEGORIES YOU FIX:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 1: STATE HYDRATION BUGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Phantom duplicates, stale data, data appearing/vanishing

Root Causes:
- useState() initialized with cached data
- useEffect() not clearing old state
- Key prop using array index instead of ID

Detection:
❌ const [tasks, setTasks] = useState(JSON.parse(localStorage.getItem('tasks') || '[]'))
✅ const [tasks, setTasks] = useState([])

❌ {tasks.map((task, i) => <Task key={i} />)}
✅ {tasks.map(task => <Task key={task.id} />)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 2: DATA PERSISTENCE BUGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Data vanishes after refresh, cache/API mismatch

Root Causes:
- API data not saved to storage
- Cache never invalidated after updates
- Multiple data sources conflicting

Detection:
❌ fetch('/api/items').then(setItems) // No localStorage.setItem()
✅ fetch('/api/items').then(data => { setItems(data); localStorage.setItem(...) })

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 3: CSS LAYOUT BUGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shadow Clipping (scrollable container - PREFERRED):
❌ .container { overflow-y: auto; padding: 0; }
✅ .container { overflow-y: auto; overflow-x: visible; padding: var(--space-6); }
   Blur-to-padding: 10px→space-3, 16px→space-4, 20px→space-6, 30px→space-8

Shadow Clipping (non-scrollable):
❌ .card { overflow: hidden; box-shadow: 0 -4px 8px; }
✅ .card { overflow: visible; box-shadow: 0 -4px 8px; }

Content Cutoff:
❌ .card { height: 40px; overflow: hidden; padding: 0; }
✅ .card { min-height: 60px; padding: 12px; overflow: visible; }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 4: BADGE & LABEL STYLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Badge text not centered, icons floating

Detection:
❌ .badge { width: 20px; height: 20px; font-size: 10px; }
✅ .badge { display: inline-flex; align-items: center; justify-content: center; padding: 6px 12px; }

RTL:
❌ .badge { position: absolute; right: 0; }
✅ .badge { position: absolute; inset-inline-end: 0; }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 5: TEXT OVERFLOW & TRUNCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptoms: Text truncated unnecessarily, no wrapping

Detection:
❌ .title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
✅ .title { white-space: normal; overflow: visible; word-break: break-word; }

Flex:
❌ .item { flex: 1; white-space: nowrap; }
✅ .item { flex: 1; min-width: 0; white-space: nowrap; }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANALYSIS APPROACH:
1. Determine bug category from description
2. Analyze provided code/CSS
3. Identify root causes
4. Find specific problematic code
5. Provide exact fixes
6. Include testing steps

OUTPUT JSON:
{
  "skill_type": "frontend",
  "bug_category": "state|persistence|css_layout|badge|text_overflow",
  "diagnosis": {
    "severity": "critical|high|medium|low",
    "root_causes": ["..."],
    "category_details": {}
  },
  "explanation": "...",
  "fixes": {
    "javascript_patches": [...],
    "css_patches": [...]
  },
  "testing_checklist": [...],
  "prevention": "..."
}
```

---

## User Prompt Template

```
Analyze this frontend bug. Determine which category it falls into and provide specific fixes.

Issue Description: {issue_description}

Framework/Context: {project_type}
Storage Type: {storage_type}
Layout Direction: {layout_direction}
Target Selectors: {target_selectors}

{javascript_code_block}

{html_code_block}

{css_code_block}

ANALYSIS QUESTIONS:
1. Is this a state/hydration issue? (data appearing/vanishing)
2. Is this a data persistence issue? (cache/storage problem)
3. Is this a CSS layout issue? (shadows, overflow, clipping)
4. Is this a badge/label styling issue? (alignment, sizing)
5. Is this a text overflow issue? (truncation, wrapping)

Provide:
1. Bug category identification
2. Root cause analysis
3. Specific problematic code snippets
4. Exact fixes needed
5. Testing procedure
6. Prevention tips
```

---

## Usage Examples

### Example 1: State Hydration Bug (Phantom Tasks)

**Input:**
```javascript
const input = {
  javascript: `
    function TaskList() {
      const [tasks, setTasks] = useState(
        JSON.parse(localStorage.getItem('tasks') || '[]')
      );

      useEffect(() => {
        fetch('/api/tasks')
          .then(r => r.json())
          .then(data => {
            setTasks(data);
            localStorage.setItem('tasks', JSON.stringify(data));
          });
      }, []);

      return (
        <div>
          {tasks.map((task, i) => (
            <div key={i}>{task.title}</div>
          ))}
        </div>
      );
    }
  `,
  issue_description: "Phantom duplicate tasks appearing, stale tasks show first",
  context: { project_type: "react" }
};
```

**Expected Output:**
```json
{
  "bug_category": "state",
  "diagnosis": {
    "severity": "high",
    "root_causes": [
      "useState initialized with localStorage data",
      "Array index used as key instead of stable ID"
    ]
  },
  "fixes": {
    "javascript_patches": [
      {
        "location": "useState initialization",
        "old": "useState(JSON.parse(localStorage.getItem('tasks') || '[]'))",
        "new": "useState([])",
        "rationale": "Start with empty state, populate in useEffect"
      },
      {
        "location": "map key prop",
        "old": "tasks.map((task, i) => <div key={i}>",
        "new": "tasks.map(task => <div key={task.id}>",
        "rationale": "Use stable ID as key to prevent duplicate renders"
      }
    ]
  },
  "testing_checklist": [
    "Clear localStorage and refresh page",
    "Verify no phantom tasks on initial load",
    "Check DevTools for duplicate key warnings"
  ]
}
```

---

### Example 2: Data Persistence Bug (Vanishing Tasks)

**Input:**
```javascript
const input = {
  javascript: `
    useEffect(() => {
      fetch('/api/tasks')
        .then(r => r.json())
        .then(data => setTasks(data));
    }, []);
  `,
  issue_description: "Tasks load fine but vanish after page refresh",
  context: { storage_type: "localStorage" }
};
```

**Expected Output:**
```json
{
  "bug_category": "persistence",
  "diagnosis": {
    "severity": "high",
    "root_causes": [
      "API data fetched but not persisted to localStorage",
      "No fallback to cached data when API unavailable"
    ]
  },
  "fixes": {
    "javascript_patches": [
      {
        "location": "fetch callback",
        "old": ".then(data => setTasks(data))",
        "new": ".then(data => { setTasks(data); localStorage.setItem('tasks', JSON.stringify(data)); })",
        "rationale": "Persist API response to localStorage for offline support"
      }
    ]
  },
  "prevention": "Always sync API data to local storage after successful fetch"
}
```

---

### Example 3: CSS Layout Bug (Shadow Clipping in Scrollable Container)

**Input:**
```javascript
const input = {
  html: `
    <div class="tasks-container">
      <div class="task-card">Task 1</div>
      <div class="task-card">Task 2</div>
    </div>
  `,
  css: `
    .tasks-container {
      overflow-y: auto;
      padding: 0;
    }
    .task-card:hover {
      box-shadow: 0 0 20px rgba(78, 205, 196, 0.2);
    }
  `,
  issue_description: "Hover glow cut off on sides, container needs to scroll",
  context: { target_selectors: [".tasks-container", ".task-card"] }
};
```

**Expected Output:**
```json
{
  "bug_category": "css_layout",
  "diagnosis": {
    "severity": "medium",
    "root_causes": [
      "overflow-y: auto clips shadows that extend beyond boundary",
      "No padding to accommodate 20px shadow blur radius"
    ]
  },
  "fixes": {
    "css_patches": [
      {
        "selector": ".tasks-container",
        "old": "overflow-y: auto; padding: 0;",
        "new": "overflow-y: auto; overflow-x: visible; padding: var(--space-6);",
        "rationale": "Keep scrolling, allow horizontal shadow overflow, add 24px padding >= 20px blur"
      }
    ]
  },
  "testing_checklist": [
    "Hover over task card - glow visible on all 4 sides",
    "With many tasks - column still scrolls",
    "First card - top shadow not clipped",
    "Last card - bottom shadow not clipped"
  ],
  "prevention": "Before adding overflow: hidden/auto, check if children have shadows and add padding >= blur radius"
}
```

### Example 3b: CSS Layout Bug (Shadow Clipping on Card)

**Input:**
```javascript
const input = {
  html: `
    <div class="card">
      <h3>Task Title</h3>
      <p>Task description</p>
    </div>
  `,
  css: `
    .card {
      overflow: hidden;
      box-shadow: 0 -4px 8px rgba(0,0,0,0.15);
      padding: 16px;
    }
  `,
  issue_description: "Box shadow not visible at top, being clipped",
  context: { target_selectors: [".card"] }
};
```

**Expected Output:**
```json
{
  "bug_category": "css_layout",
  "diagnosis": {
    "severity": "medium",
    "root_causes": [
      "overflow: hidden on card clips the negative-offset box-shadow"
    ]
  },
  "fixes": {
    "css_patches": [
      {
        "selector": ".card",
        "old": "overflow: hidden;",
        "new": "overflow: visible;",
        "rationale": "Allow shadow to extend beyond card boundaries"
      }
    ]
  },
  "testing_checklist": [
    "Verify shadow visible on all sides",
    "Check no content overflow issues introduced"
  ]
}
```

---

### Example 4: Badge Styling Bug (Misalignment)

**Input:**
```javascript
const input = {
  html: `
    <div class="task-header">
      <span class="priority-badge">H</span>
      <span class="date-label">Jan 13</span>
    </div>
  `,
  css: `
    .priority-badge {
      background: #E53935;
      color: white;
      width: 20px;
      height: 20px;
      font-size: 10px;
    }
  `,
  issue_description: "Priority badge text not centered vertically",
  context: {
    target_selectors: [".priority-badge"],
    layout_direction: "rtl"
  }
};
```

**Expected Output:**
```json
{
  "bug_category": "badge",
  "diagnosis": {
    "severity": "medium",
    "root_causes": [
      "Missing display: flex for centering",
      "Fixed dimensions without flexbox alignment"
    ]
  },
  "fixes": {
    "css_patches": [
      {
        "selector": ".priority-badge",
        "old": ".priority-badge { background: #E53935; color: white; width: 20px; height: 20px; font-size: 10px; }",
        "new": ".priority-badge { background: #E53935; color: white; display: inline-flex; align-items: center; justify-content: center; min-width: 20px; min-height: 20px; padding: 2px 6px; font-size: 11px; font-weight: 600; }",
        "rationale": "Use flexbox for perfect centering, padding for flexibility"
      }
    ]
  },
  "testing_checklist": [
    "Verify badge text is vertically centered",
    "Test with single char (H, M, L) and longer text",
    "Verify RTL layout displays correctly"
  ]
}
```

---

### Example 5: Text Overflow Bug (Truncation)

**Input:**
```javascript
const input = {
  html: `
    <div class="task-item">
      <span class="task-title">
        Important task with a very long title that should wrap
      </span>
      <span class="task-date">Jan 13</span>
    </div>
  `,
  css: `
    .task-item {
      display: flex;
      gap: 8px;
    }

    .task-title {
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  `,
  issue_description: "Task title text being cut off with ellipsis when there's room",
  context: { target_selectors: [".task-title"] }
};
```

**Expected Output:**
```json
{
  "bug_category": "text_overflow",
  "diagnosis": {
    "severity": "medium",
    "root_causes": [
      "white-space: nowrap prevents natural wrapping",
      "Missing min-width: 0 for proper flex truncation"
    ]
  },
  "fixes": {
    "css_patches": [
      {
        "selector": ".task-title",
        "old": ".task-title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }",
        "new": ".task-title { flex: 1; min-width: 0; white-space: normal; word-break: break-word; }",
        "rationale": "Allow natural wrapping, min-width: 0 enables proper flex behavior"
      }
    ]
  },
  "testing_checklist": [
    "Verify long titles wrap naturally",
    "Check short titles display on single line",
    "Test with different viewport widths"
  ]
}
```

---

## Best Practices

### 1. Provide Context

Always include relevant context:
- `project_type`: "react", "vue", "angular", "vanilla"
- `storage_type`: "localStorage", "sessionStorage", "indexedDB"
- `layout_direction`: "ltr", "rtl"

### 2. Selector Hints Are Critical

Provide 3-5 likely CSS selectors:

```json
"target_selectors": [".task-card", ".card-title", ".card-meta", ".card-content"]
```

### 3. Constraints Prevent Regressions

Include what NOT to change:

```json
"constraints": [
  "Do not change colors",
  "Do not modify responsive breakpoints",
  "Keep existing animations",
  "Preserve RTL text support"
]
```

### 4. Testing Checklist Verification

Always follow the testing checklist to verify fixes work.

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Could not find old_block" | CSS changed or whitespace mismatch | Provide unminified CSS with exact formatting |
| "Invalid JSON response" | Claude returned explanation text | Check system prompt enforces JSON-only output |
| "Constraint violation" | Patch changes protected properties | Re-run with clearer selector hints |
| "Category not detected" | Ambiguous description | Be more specific about the symptom |

---

## Resources

### assets/

- `README.md` - Quick start guide
- `examples/` - Example inputs and outputs

### Related Skills

| Skill | Purpose |
|-------|---------|
| `dev-debugging` | General debugging for Vue.js/Pinia |
| `dev-implement-ui-ux` | UI/UX design and implementation |
| `vue-flow-debug` | Vue Flow canvas debugging |

---

## Quick Reference

### State Hydration Fixes
```javascript
// Clear initial state
useState([])  // Not useState(localStorage.getItem(...))

// Use stable keys
key={item.id}  // Not key={index}

// Cleanup useEffect
return () => controller.abort();
```

### Data Persistence Fixes
```javascript
// Save after fetch
localStorage.setItem('key', JSON.stringify(data));

// Invalidate on update
localStorage.removeItem('key');

// Single source of truth
const data = await api.fetch(); // API is authoritative
```

### CSS Layout Fixes
```css
/* Shadow clipping (scrollable container) */
overflow-y: auto;           /* Keep scrolling */
overflow-x: visible;        /* Allow shadow overflow */
padding: var(--space-6);    /* >= shadow blur radius */

/* Shadow clipping (non-scrollable) */
overflow: visible;          /* Allow shadow */

/* Blur-to-padding: 10px→space-3, 16px→space-4, 20px→space-6, 30px→space-8 */

/* Content cutoff */
min-height: 60px;   /* Not height */
padding: 12px;      /* Not 0 */
line-height: 1.5;   /* Not 1.2 */
```

### Badge Styling Fixes
```css
/* Centering */
display: inline-flex;
align-items: center;
justify-content: center;

/* RTL */
inset-inline-end: 0;  /* Not right */
margin-inline-start: 8px;  /* Not margin-left */
```

### Text Overflow Fixes
```css
/* Allow wrapping */
white-space: normal;  /* Not nowrap */
word-break: break-word;

/* Flex truncation */
min-width: 0;  /* Required for flex items */
```
