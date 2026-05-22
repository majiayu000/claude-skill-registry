---
name: eds-block-development
description: Guide for developing EDS blocks using vanilla JavaScript, Content Driven Development, and block decoration patterns. Covers block structure, decorate function, content extraction, DOM manipulation, and EDS best practices for Adobe Edge Delivery Services.
---

# EDS Block Development Guide

## ⚠️ CRITICAL WARNING: EDS Reserved Class Names

**BEFORE WRITING ANY CODE, READ THIS:**

EDS automatically adds these class names to your blocks:
- `.{blockname}-container` - Added to parent `<section>` element
- `.{blockname}-wrapper` - Added to block's parent `<div>` wrapper

**❌ NEVER use these suffixes in your CSS or JavaScript:**
```css
/* ❌ PRODUCTION BUG - Will break entire page */
.overlay-container { position: fixed; opacity: 0; }

/* ✅ SAFE - Use different suffix */
.overlay-backdrop { position: fixed; opacity: 0; }
```

**Safe suffixes:** `-backdrop`, `-panel`, `-inner`, `-grid`, `-list`, `-content`, `-dialog`, `-popup`

See [CSS Best Practices](#critical-avoid-eds-reserved-class-names) section below for full details.

---

## Purpose

Guide developers through creating and modifying Adobe Edge Delivery Services (EDS) blocks following vanilla JavaScript patterns, Content Driven Development principles, and EDS best practices.

## When to Use This Skill

Automatically activates when:
- Creating new blocks in `/blocks/`
- Modifying existing block JavaScript (`.js` files)
- Implementing block decoration patterns
- Working with EDS content structures
- Using keywords: "block", "decorate", "EDS block"

---

## Quick Start: Block Structure

### File Organization

Every EDS block follows this structure:

```
blocks/your-block/
├── your-block.js             # Decoration logic (REQUIRED)
├── your-block.css            # Block-specific styles (REQUIRED)
├── README.md                 # Usage documentation (REQUIRED)
├── EXAMPLE.md                # Google Docs example (REQUIRED)
├── test.html                 # Development test file (RECOMMENDED)
└── block-architecture.md     # Technical architecture (OPTIONAL - for complex blocks)
```

**Critical naming convention:** File names must match the block name exactly (kebab-case).

---

## Google Docs Table Structure (CRITICAL)

### How EDS Recognizes Blocks

**The first row of a table in Google Docs is the block name that drives everything:**

1. **First row (header row)** = Block name (e.g., "overlay", "cards", "hero")
   - EDS uses this name to load `/blocks/{name}/{name}.js`
   - EDS uses this name to load `/blocks/{name}/{name}.css`
   - This triggers the `decorate()` function
   - **WITHOUT THIS, YOUR BLOCK WILL NOT LOAD**

2. **Subsequent rows** = Block content (data rows)
   - Row 2, Row 3, etc. become `block.children[0]`, `block.children[1]`, etc.
   - Your `decorate()` function processes these rows

### Example: Google Docs Table

```
| overlay        | ← HEADER ROW (block name) - CRITICAL!
|----------------|
| Learn More     | ← Row 2 becomes block.children[0]
| Welcome! ...   | ← Row 3 becomes block.children[1]
```

**What EDS does:**
1. Sees header row "overlay"
2. Loads `/blocks/overlay/overlay.js`
3. Loads `/blocks/overlay/overlay.css`
4. Calls `decorate(blockElement)`
5. Your code processes rows 2 and 3

### Common Mistake

❌ **WRONG** - No header row:
```
| Learn More     |
| Welcome! ...   |
```
Result: Block not recognized, CSS/JS not loaded, no decoration happens

✅ **CORRECT** - Header row with block name:
```
| overlay        | ← Must match /blocks/overlay/
|----------------|
| Learn More     |
| Welcome! ...   |
```

---

## The Decorate Function Pattern

All EDS blocks export a default `decorate` function that receives the block element:

```javascript
export default function decorate(block) {
  // 1. Configuration (at the top)
  const config = {
    animationDuration: 300,
    maxItems: 10,
    errorMessage: 'Failed to load content'
  };

  // 2. Extract content from EDS structure
  const rows = Array.from(block.children);
  const content = rows.map(row => {
    const cells = Array.from(row.children);
    return cells.map(cell => cell.textContent.trim());
  });

  // 3. Create new DOM structure
  const container = document.createElement('div');
  container.className = 'your-block-wrapper';

  // 4. Build your component
  content.forEach(([title, description]) => {
    const item = document.createElement('div');
    item.className = 'your-block-item';
    item.innerHTML = `
      <h3>${title}</h3>
      <p>${description}</p>
    `;
    container.appendChild(item);
  });

  // 5. Setup event handlers
  container.querySelectorAll('.your-block-item').forEach(item => {
    item.addEventListener('click', () => {
      console.log('Item clicked');
    });
  });

  // 6. Replace block content
  block.textContent = '';
  block.appendChild(container);
}
```

---

## Configuration Object Architecture

### ⚠️ CRITICAL: Separation of Concerns

**Every block must distinguish between:**

1. **Global Constants** - Developer-facing messages and module-level state
2. **Runtime Configuration** - User-facing settings, durations, URLs, icons, text
3. **Metadata Overrides** - Notebook-specific configuration from `.ipynb` metadata

### Global Constants Pattern

**Place at the top of your JavaScript file (before all other code):**

```javascript
// ============================================================================
// GLOBAL CONSTANTS - Developer-facing error messages (easily searchable)
// ============================================================================
const BLOCKNAME_ERRORS = {
  CONFIG_MISSING: 'Incomplete code: Configuration object missing. Block cannot initialize.',
  INVALID_DATA: 'Invalid data format. Expected array of objects.',
  FETCH_FAILED: 'Failed to fetch remote data.',
};

// ============================================================================
// MODULE-LEVEL CONSTANTS
// ============================================================================
// Module-level cache (persists across block instances)
const BLOCKNAME_CACHE = new Map();
```

**Why this matters:**

- Error messages are **developer-facing** - they help developers debug issues
- Placing them at the top makes them **easily searchable** with Ctrl+F
- Separates concerns: developers modify global constants, users/metadata configure runtime behavior
- **Never put error messages in the config object** - they're not runtime configuration

### Runtime Configuration Object

**Define inside `decorate()` function:**

```javascript
export default function decorate(block) {
  // Configuration object - runtime settings
  const config = {
    // Messages (user-facing)
    errorMessage: 'Failed to load content',
    loadingMessage: 'Loading...',

    // Timing
    animationDuration: 300,
    defaultTimeout: 5000,

    // Limits
    maxItems: 10,
    maxRetries: 3,

    // URLs and Paths
    apiEndpoint: '/api/data.json',
    fallbackUrl: 'https://example.com/fallback',

    // UI Icons (HTML entities)
    icons: {
      close: '&times;',
      arrow: '&#9654;',
      warning: '&#9888;',
    },

    // UI Text
    text: {
      submitButton: 'Submit',
      cancelButton: 'Cancel',
      confirmMessage: 'Are you sure?',
    },
  };

  // Extract metadata overrides
  const metadata = block.dataset;
  const timeout = metadata.timeout ? parseInt(metadata.timeout) : config.defaultTimeout;

  // Use config and metadata throughout
  // ...
}
```

**What belongs in config object:**

- ✅ Durations and timing values
- ✅ API endpoints and URLs
- ✅ UI text and icons
- ✅ Limits and thresholds
- ✅ User-facing messages
- ❌ Error messages (use global constants)
- ❌ Module-level caches (use module constants)

### Metadata Override Pattern

**For `.ipynb` notebooks:**

```javascript
export default function decorate(block) {
  const config = { /* ... */ };

  // Extract notebook metadata (if applicable)
  const notebookData = JSON.parse(block.textContent || '{}');
  const metadata = notebookData.metadata || {};

  // Override config with metadata (convert units if needed)
  const splashDuration = metadata['splash-duration']
    ? metadata['splash-duration'] * 1000  // Convert seconds to milliseconds
    : config.defaultSplashDuration;

  const autorun = metadata.autorun === true;  // Boolean from metadata

  // Use overridden values
  showSplashScreen(splashDuration);
}
```

**For EDS blocks with data attributes:**

```javascript
export default function decorate(block) {
  const config = { /* ... */ };

  // Override config with data attributes
  const layout = block.dataset.layout || 'grid';
  const columns = parseInt(block.dataset.columns) || config.defaultColumns;

  // Apply configuration
  block.classList.add(`layout-${layout}`);
  block.style.setProperty('--columns', columns);
}
```

### Dependency Injection for Config

**When config is needed in helper functions, use dependency injection:**

```javascript
// ❌ BAD - Global access (causes ReferenceError)
function createOverlay(data) {
  const icon = config.icons.close;  // ReferenceError: config is not defined
  // ...
}

// ✅ GOOD - Dependency injection
function createOverlay(data, config) {
  const icon = config.icons.close;  // Explicit parameter
  // ...
}

export default function decorate(block) {
  const config = { /* ... */ };

  // Pass config explicitly
  const overlay = createOverlay(data, config);
}
```

**For nested function calls:**

```javascript
function createOverlay(data, config) {
  // Config validation guard clause
  if (!config) {
    console.error('[BLOCK] CRITICAL: Config object missing in createOverlay');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'block-error';
    errorDiv.textContent = BLOCKNAME_ERRORS.CONFIG_MISSING;
    return errorDiv;
  }

  // Pass config down the chain
  const content = renderContent(data, config);
  const footer = renderFooter(config);

  // ...
}

function renderContent(data, config) {
  // Config flows through entire call chain
  const icon = config.icons.arrow;
  // ...
}

export default function decorate(block) {
  const config = { /* ... */ };

  // Top-level call passes config
  const overlay = createOverlay(data, config);
}
```

### Config Validation Pattern

**CRITICAL: Never use hardcoded fallbacks with `||` operator:**

```javascript
// ❌ BAD - Hardcoded fallback bypasses config
function createOverlay(data, config = null) {
  const icon = config?.icons?.close || '&times;';  // Fallback defeats config purpose
  const timeout = config?.timeout || 5000;         // Hardcoded value
}

// ✅ GOOD - Guard clause with explicit error
function createOverlay(data, config = null) {
  // Fail explicitly if config missing
  if (!config) {
    console.error('[BLOCK] CRITICAL: Config object missing');
    const errorDiv = document.createElement('div');
    errorDiv.textContent = BLOCKNAME_ERRORS.CONFIG_MISSING;
    return errorDiv;
  }

  // Direct property access (no fallbacks)
  const icon = config.icons.close;
  const timeout = config.timeout;

  // Config is guaranteed to exist here
}
```

**Why this matters:**

- Fallbacks hide configuration issues
- Block should **fail explicitly** if config missing
- Makes bugs obvious during development
- Forces proper dependency injection

**Only acceptable use of fallback:**

```javascript
// ✅ Acceptable - Ternary for intentional default behavior
const layout = config ? config.layout : 'grid';

// ✅ Acceptable - Metadata override with config fallback
const duration = metadata['duration'] || config.defaultDuration;
```

### Refactoring Existing Blocks

**When reviewing or modifying existing blocks, check for:**

1. **Hardcoded values scattered throughout code**
   - Extract to config object at top of `decorate()`
   - Group by category (messages, timing, limits, etc.)

2. **Error messages in function bodies**
   - Move to `BLOCKNAME_ERRORS` global constant at file top
   - Update all usages to reference global constant

3. **Functions accessing config globally**
   - Add `config` parameter to function signature
   - Pass config explicitly from call sites
   - Add guard clause for config validation

4. **Hardcoded fallbacks using `||` operator**
   - Replace with guard clauses that fail explicitly
   - Use ternary only for intentional defaults

**Refactoring checklist:**

```javascript
// Before refactoring:
function helper() {
  const icon = '&times;';  // ❌ Hardcoded
  const timeout = 5000;    // ❌ Hardcoded
  if (error) {
    showError('Failed');   // ❌ Hardcoded message
  }
}

// After refactoring:
const BLOCK_ERRORS = {
  FETCH_FAILED: 'Failed to load data',  // ✅ Global constant
};

export default function decorate(block) {
  const config = {
    icons: { close: '&times;' },  // ✅ Config object
    timeout: 5000,                 // ✅ Config object
  };

  helper(config);  // ✅ Dependency injection
}

function helper(config) {
  if (!config) {  // ✅ Guard clause
    console.error(BLOCK_ERRORS.CONFIG_MISSING);
    return;
  }

  const icon = config.icons.close;  // ✅ Direct access
  const timeout = config.timeout;   // ✅ Direct access

  if (error) {
    showError(BLOCK_ERRORS.FETCH_FAILED);  // ✅ Global constant
  }
}
```

### Real-World Example: ipynb-viewer

**See `blocks/ipynb-viewer/ipynb-viewer.js` for comprehensive implementation:**

- **Global constants** (lines 14-24): Error messages and module cache
- **Config object** (lines 4073-4105): Runtime settings organized by category
- **Metadata overrides** (lines 4120-4125): Splash duration from notebook metadata
- **Dependency injection** (lines 2236, 3349): Config passed through function chain
- **Guard clauses** (lines 2238-2245, 3351-3362): Fail explicitly if config missing

**Key architectural decisions:**

1. Error messages promoted to global constants (easily searchable)
2. All hardcoded values moved to config object
3. Config passed explicitly through all function calls
4. No `||` fallbacks - functions fail with clear errors
5. Metadata overrides use ternary for intentional defaults

---

## Content Extraction Patterns

### Basic Two-Column Pattern

```javascript
export default function decorate(block) {
  const rows = Array.from(block.children);

  const items = rows.map(row => {
    const [titleCell, descriptionCell] = row.children;
    return {
      title: titleCell?.textContent?.trim() || '',
      description: descriptionCell?.textContent?.trim() || ''
    };
  });

  // Use the items...
}
```

### Picture Extraction Pattern

```javascript
function extractPicture(cell) {
  const picture = cell.querySelector('picture');
  if (!picture) return null;

  return {
    img: picture.querySelector('img'),
    sources: Array.from(picture.querySelectorAll('source'))
  };
}

export default function decorate(block) {
  const rows = Array.from(block.children);

  rows.forEach(row => {
    const [imageCell, contentCell] = row.children;
    const picture = extractPicture(imageCell);

    if (picture) {
      // Use the picture element
    }
  });
}
```

### Link Extraction Pattern

```javascript
function extractLink(cell) {
  const link = cell.querySelector('a');
  return link ? {
    href: link.href,
    text: link.textContent.trim(),
    target: link.target
  } : null;
}
```

---

## DOM Manipulation Best Practices

### 1. Clear the Block First

```javascript
export default function decorate(block) {
  // Extract data first
  const data = extractContent(block);

  // Clear the block
  block.textContent = '';

  // Add new content
  const container = createNewStructure(data);
  block.appendChild(container);
}
```

### 2. Use Document Fragments for Multiple Elements

```javascript
function createItems(data) {
  const fragment = document.createDocumentFragment();

  data.forEach(item => {
    const element = document.createElement('div');
    element.textContent = item;
    fragment.appendChild(element);
  });

  return fragment;
}

export default function decorate(block) {
  const data = extractContent(block);
  block.textContent = '';
  block.appendChild(createItems(data));
}
```

### 3. Minimize DOM Manipulation

```javascript
// ❌ BAD - Multiple reflows
data.forEach(item => {
  const element = document.createElement('div');
  element.textContent = item;
  block.appendChild(element); // Triggers reflow each time
});

// ✅ GOOD - Single reflow
const fragment = document.createDocumentFragment();
data.forEach(item => {
  const element = document.createElement('div');
  element.textContent = item;
  fragment.appendChild(element);
});
block.appendChild(fragment); // Single reflow
```

---

## Error Handling

### Basic Error Handling

```javascript
export default function decorate(block) {
  try {
    const config = { /* ... */ };
    const content = extractContent(block);

    if (!content || content.length === 0) {
      throw new Error('No content found');
    }

    const container = createStructure(content);
    block.textContent = '';
    block.appendChild(container);

  } catch (error) {
    console.error('Block decoration failed:', error);
    block.innerHTML = '<p class="error-message">Unable to load content</p>';
  }
}
```

### Async Operations

```javascript
export default async function decorate(block) {
  try {
    // Show loading state
    block.innerHTML = '<p class="loading">Loading...</p>';

    // Fetch data
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();

    // Clear and render
    block.textContent = '';
    block.appendChild(createStructure(data));

  } catch (error) {
    console.error('Failed to load data:', error);
    block.innerHTML = '<p class="error-message">Failed to load content</p>';
  }
}
```

---

## CSS Best Practices

### Block-Specific Naming

```css
/* Namespace all classes with block name */
.your-block-wrapper {
  /* Container styles */
}

.your-block-item {
  /* Item styles */
}

.your-block-title {
  /* Title styles */
}

/* Use BEM naming for variants */
.your-block-item--featured {
  /* Featured variant */
}

.your-block-item__icon {
  /* Item element */
}
```

### ⚠️ CRITICAL: Avoid EDS Reserved Class Names

**EDS automatically adds these classes:**
- `.{blockname}-wrapper` - Added to the block's parent `<div>` wrapper
- `.{blockname}-container` - Added to the parent `<section>` element
- `.block` - Added to all block elements
- `.section` - Added to all section elements
- `.button-container` - Added to parent elements of buttons
- `.default-content-wrapper` - Added to default content wrappers

**DO NOT use these class names in your CSS or JavaScript:**

```css
/* ❌ BAD - Conflicts with EDS automatic naming */
.overlay-container {
  position: fixed;  /* Will be applied to the section, breaking layout */
}

.cards-wrapper {
  display: grid;  /* Will conflict with EDS's .cards-wrapper on block element */
}

/* ✅ GOOD - Use different suffixes */
.overlay-backdrop {
  position: fixed;  /* Safe - won't conflict */
}

.cards-grid {
  display: grid;  /* Safe - different name */
}

.overlay-modal-container {
  /* Safe - more specific name */
}
```

**Why this matters:**
- EDS's `decorateBlock()` adds `.{blockname}-wrapper` to block parent divs (line 682)
- EDS's `decorateBlock()` adds `.{blockname}-container` to parent sections (line 684)
- EDS's `decorateBlock()` adds `.block` to all block elements (line 677)
- EDS's `decorateSections()` adds `.section` to all sections (line 503)
- EDS's `decorateButtons()` adds `.button-container` to button parents (lines 430, 439, 448)
- If your CSS uses these same class names, styles will be applied to the wrong elements
- This can cause invisible pages, broken layouts, or unexpected behavior

**Additional conflicts to avoid:**
```css
/* ❌ Never style these EDS-generated classes with layout-breaking properties */
.block {
  position: fixed;  /* Will break ALL blocks on the page */
}

.section {
  display: none;  /* Will hide ALL sections */
}

.button-container {
  position: absolute;  /* Will break ALL button layouts */
}
```

**Safe naming patterns:**
- `.{blockname}-backdrop`
- `.{blockname}-modal`
- `.{blockname}-content`
- `.{blockname}-inner`
- `.{blockname}-grid`
- `.{blockname}-list`
- `.{blockname}-panel`
- `.{blockname}-overlay`

**Reference:** See `scripts/aem.js`:
- Lines 674-686: `decorateBlock()` - adds wrapper/container classes
- Lines 489-530: `decorateSections()` - adds section classes
- Lines 421-453: `decorateButtons()` - adds button-container classes

### Mobile-First Responsive Design

```css
/* Base styles (mobile) */
.your-block-item {
  padding: 1rem;
  margin-bottom: 1rem;
}

/* Tablet */
@media (min-width: 600px) {
  .your-block-item {
    padding: 1.5rem;
  }
}

/* Desktop */
@media (min-width: 900px) {
  .your-block-item {
    padding: 2rem;
  }
}
```

### Use CSS Variables

```css
.your-block {
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: var(--body-font-family);
  padding: var(--spacing-m);
}
```

### ⚠️ CRITICAL: Verify HTML Structure Before Writing CSS

**NEVER assume what HTML elements exist** - always inspect the actual DOM structure first.

**Why this matters:**

- Different parsers generate different HTML structures
- CSS targeting non-existent elements wastes debugging time
- Assumptions about `<p>` tags, `<div>` wrappers, or structure can be wrong

**Real-world example (ipynb-viewer parseMarkdown):**

The `parseMarkdown()` function converts double newlines to `<br><br>` tags, NOT `<p>` tags:

```javascript
// parseMarkdown() implementation (line 397)
html = html.replace(/\n\n+/g, '<br><br>'); // Paragraph breaks use <br><br>
html = html.replace(/\n/g, ' '); // Single newlines become spaces
```

**Problem pattern:**

```css
/* ❌ WRONG - Assumes <p> tags exist */
.your-block p {
  margin: 0.15rem 0;  /* No effect if parseMarkdown uses <br><br> */
}

/* ✅ CORRECT - Targets actual structure */
.your-block br {
  margin: 0.15rem 0;
  line-height: 0.15rem;
}

/* Hide consecutive br tags for better spacing */
.your-block br + br {
  display: none;
}
```

**Best practices when writing CSS:**

1. **Always verify HTML structure** - Use DevTools to inspect actual DOM
2. **Don't assume** - Just because you expect `<p>` tags doesn't mean they exist
3. **Check the renderer** - Look at how content is generated (parseMarkdown, renderCell, etc.)
4. **Test in isolation** - Add a bright background color to verify selector matches
5. **Read the source** - 5 minutes reading code beats 1 hour of trial-and-error

**How to verify:**

1. Open browser DevTools (F12)
2. Inspect the content area element
3. Look at the actual HTML generated by your parser/renderer
4. Check what elements exist (br vs p vs div vs section)
5. Write CSS rules for the **actual** structure, not the **assumed** structure

**Impact:**

- **Before verification**: Wasted hours debugging "why isn't my CSS working?"
- **After verification**: Immediate fix by targeting correct elements
- **Root cause**: Assumptions about HTML structure without inspection

**Documentation:** See `LEARNINGS.md` section "ipynb-viewer: parseMarkdown() Uses <br> Tags, Not <p> Tags"

---

## Accessibility

### Semantic HTML

```javascript
export default function decorate(block) {
  const container = document.createElement('nav'); // Use semantic elements
  container.setAttribute('aria-label', 'Block navigation');

  const list = document.createElement('ul');

  items.forEach(item => {
    const li = document.createElement('li');
    const button = document.createElement('button');
    button.textContent = item.text;
    button.setAttribute('aria-label', `Open ${item.text}`);

    li.appendChild(button);
    list.appendChild(li);
  });

  container.appendChild(list);
  block.textContent = '';
  block.appendChild(container);
}
```

### Keyboard Navigation

```javascript
export default function decorate(block) {
  const items = block.querySelectorAll('.your-block-item');

  items.forEach((item, index) => {
    // Make items focusable
    item.setAttribute('tabindex', '0');

    // Handle keyboard events
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        item.click();
      }

      if (e.key === 'ArrowDown' && items[index + 1]) {
        items[index + 1].focus();
      }

      if (e.key === 'ArrowUp' && items[index - 1]) {
        items[index - 1].focus();
      }
    });
  });
}
```

---

## Performance Optimization

### 1. Lazy Loading Images

```javascript
export default function decorate(block) {
  const images = block.querySelectorAll('img');

  images.forEach(img => {
    img.setAttribute('loading', 'lazy');
  });
}
```

### 2. Debouncing Event Handlers

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

export default function decorate(block) {
  const handleResize = debounce(() => {
    // Resize logic
  }, 250);

  window.addEventListener('resize', handleResize);
}
```

### 3. Use requestIdleCallback for Non-Critical Work

```javascript
export default function decorate(block) {
  // Critical rendering
  const container = createStructure(data);
  block.appendChild(container);

  // Non-critical work
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      // Analytics, non-critical enhancements, etc.
      trackBlockView(block);
    });
  } else {
    setTimeout(() => {
      trackBlockView(block);
    }, 1);
  }
}
```

---

## Testing Your Block

### Create test.html

**⚠️ CRITICAL: Correct EDS HTML Structure**

The HTML structure in test.html must EXACTLY match how EDS transforms Google Docs tables:

```
Block Element (has block name class)
└── Row(s) (direct children, one <div> per row)
    └── Cell(s) (children of row, one <div> per cell)
```

**Example - Two-column block with one row:**
```html
<div class="your-block">          <!-- Block element -->
    <div>                          <!-- Row 1 -->
        <div>Cell 1 content</div>  <!-- Cell 1 -->
        <div>Cell 2 content</div>  <!-- Cell 2 -->
    </div>
</div>
```

**Example - Two-column block with multiple rows:**
```html
<div class="your-block">           <!-- Block element -->
    <div>                           <!-- Row 1 -->
        <div>Row 1, Cell 1</div>    <!-- Cell 1 -->
        <div>Row 1, Cell 2</div>    <!-- Cell 2 -->
    </div>
    <div>                           <!-- Row 2 -->
        <div>Row 2, Cell 1</div>    <!-- Cell 1 -->
        <div>Row 2, Cell 2</div>    <!-- Cell 2 -->
    </div>
</div>
```

**❌ COMMON MISTAKE - Extra wrapper div:**
```html
<!-- ❌ WRONG - Do NOT add extra wrapper divs -->
<div class="your-block">
    <div>                    <!-- ❌ Extra wrapper -->
        <div>                <!-- Row -->
            <div>Cell 1</div>
            <div>Cell 2</div>
        </div>
    </div>
</div>
```

### Complete test.html Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Block Test</title>

    <!-- EDS Core Styles -->
    <link rel="stylesheet" href="/styles/styles.css">
    <!-- Block CSS is loaded automatically by loadBlock() -->

    <style>
        /* EDS pattern - ensure body appears */
        body.appear {
            display: block;
        }

        /* Optional: Test page styling */
        body {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .test-section {
            margin: 2rem 0;
            padding: 1.5rem;
            border: 2px solid #ccc;
            border-radius: 8px;
            background: #f9f9f9;
        }

        .test-section h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h1>Your Block Test Page</h1>

    <!-- Test Case 1: Basic Usage -->
    <div class="test-section">
        <h2>Test Case 1: Basic Two-Column Block</h2>

        <div class="your-block">
            <div>
                <div>Title 1</div>
                <div>Description 1</div>
            </div>
            <div>
                <div>Title 2</div>
                <div>Description 2</div>
            </div>
        </div>
    </div>

    <!-- Test Case 2: With Images -->
    <div class="test-section">
        <h2>Test Case 2: With Images</h2>

        <div class="your-block">
            <div>
                <div>
                    <picture>
                        <img src="https://via.placeholder.com/300x200" alt="Test Image">
                    </picture>
                </div>
                <div>Content with image</div>
            </div>
        </div>
    </div>

    <!-- Test Case 3: Block Variant -->
    <div class="test-section">
        <h2>Test Case 3: Block Variant</h2>

        <div class="your-block variant-name">
            <div>
                <div>Variant content</div>
                <div>Testing variant styling</div>
            </div>
        </div>
    </div>

    <script type="module">
        import { loadBlock } from '/scripts/aem.js';

        // CRITICAL: Add body.appear class FIRST (before loadBlock)
        // This makes the page visible (EDS hides body by default)
        document.body.classList.add('appear');

        // Get all blocks to test
        const blocks = document.querySelectorAll('.your-block');

        console.log(`Testing ${blocks.length} block(s)...`);

        // Load each block
        for (const block of blocks) {
            try {
                // Add .block class to mimic EDS production behavior
                block.classList.add('block');

                // CRITICAL: Set blockName dataset (required by loadBlock)
                // In production, decorateBlock() gets this from classList[0]
                block.dataset.blockName = 'your-block';

                // Load the block (loads JS and CSS automatically)
                await loadBlock(block);

                console.log('✅ Block loaded:', block.className);
            } catch (error) {
                console.error('❌ Block failed:', block.className, error);
            }
        }

        console.log('All blocks loaded!');
    </script>
</body>
</html>
```

**Important Notes:**

1. **Block Structure**: Each block must have rows as direct children, and cells as children of rows
2. **`.block` class**: Added by script to mimic EDS production (where `decorateBlock()` adds it automatically)
3. **`block.dataset.blockName`**: **CRITICAL** - Must be set before calling `loadBlock()`, otherwise you'll get "undefined" errors
4. **`body.appear`**: REQUIRED - EDS hides body by default, this class makes it visible
5. **Block loading order**: Add `body.appear` class BEFORE calling `loadBlock()`
6. **Multiple blocks**: Use `querySelectorAll()` and loop to test multiple instances
7. **Console logging**: Add logs to track loading progress and catch errors
8. **Block wrappers**: If your block uses `document.querySelector('.{blockname}-wrapper')` (e.g., for expressions plugin), wrap each block in `<div class="{blockname}-wrapper">` in test.html

**Common Errors:**
- If you see `/blocks/undefined/undefined.js 404`, you forgot to set `block.dataset.blockName`!
- If you see `Cannot read properties of null (reading 'firstChild')` in expressions.js, you need to wrap blocks in `.{blockname}-wrapper` divs

### Common HTML Structure Mistakes

❌ **WRONG** - Extra nesting:
```html
<div class="your-block">
    <div><div><div>Content</div></div></div>  <!-- Too many divs! -->
</div>
```

❌ **WRONG** - Missing row wrapper:
```html
<div class="your-block">
    <div>Cell 1</div>  <!-- No row wrapper! -->
    <div>Cell 2</div>
</div>
```

✅ **CORRECT** - Proper structure:
```html
<div class="your-block">
    <div>               <!-- Row -->
        <div>Cell 1</div>  <!-- Cell -->
        <div>Cell 2</div>  <!-- Cell -->
    </div>
</div>
```

✅ **CORRECT** - With wrapper (when block uses `.{blockname}-wrapper` selector):
```html
<div class="your-block-wrapper">  <!-- Wrapper for global selectors -->
    <div class="your-block">
        <div>                      <!-- Row -->
            <div>Cell 1</div>      <!-- Cell -->
            <div>Cell 2</div>      <!-- Cell -->
        </div>
    </div>
</div>
```

**When to use wrappers in test.html:**
- Your block uses `document.querySelector('.{blockname}-wrapper')` in its JavaScript
- Your block depends on external plugins (like expressions) that expect wrappers
- In production, EDS automatically wraps blocks in `.{blockname}-wrapper` divs
- Without the wrapper, code that queries for it will get `null` and may error

### Debugging Tips for test.html

If your test.html doesn't work, check:

1. **Structure**: Use browser DevTools to inspect the DOM structure
   - Right-click block → Inspect Element
   - Verify: Block → Row(s) → Cell(s)

2. **Classes**: Check that `.block` class was added
   - Should see: `<div class="your-block block">`

3. **Console errors**: Open DevTools Console (F12)
   - Look for JavaScript errors
   - Check if `loadBlock()` succeeded

4. **Network tab**: Check if CSS/JS files loaded
   - Should see: `/blocks/your-block/your-block.css`
   - Should see: `/blocks/your-block/your-block.js`

5. **Block scoping**: Ensure your JS uses `block` parameter, not global selectors
   ```javascript
   // ✅ CORRECT
   const cells = block.querySelectorAll('div > div');

   // ❌ WRONG
   const cells = document.querySelectorAll('.your-block div > div');
   ```

### Test with Development Server

```bash
npm run debug
```

Access your test at: `http://localhost:3000/blocks/your-block/test.html`

---

## Block Variations

### ⚠️ CRITICAL: Single JavaScript File for All Variations

**MANDATORY RULE: Each block must have exactly ONE JavaScript file, regardless of how many variations it supports.**

EDS blocks should NEVER have multiple JavaScript files like:
- ❌ `blockname.js`, `blockname-variation1.js`, `blockname-variation2.js`
- ❌ `view-myblog.js`, `view-myblog-ai.js`

Instead, all variation logic must be handled within the single JavaScript file using class detection:

```javascript
export default async function decorate(block) {
  // Detect variation by checking for class
  const isVariationA = block.classList.contains('variation-a');
  const isVariationB = block.classList.contains('variation-b');

  // Apply variation-specific logic
  if (isVariationA) {
    // Handle variation A logic
    const data = await fetchAndFilterData();
    renderVariationA(block, data);
  } else if (isVariationB) {
    // Handle variation B logic
    renderVariationB(block);
  } else {
    // Handle default/standard variation
    renderStandard(block);
  }
}
```

### Why Single File Architecture

- **Maintainability**: All logic for a block is in one place
- **EDS Convention**: The system expects one JS file per block
- **Performance**: Avoids loading multiple files for the same block
- **Consistency**: Follows the same pattern as CSS variations
- **Simplicity**: Easier to understand and debug

### Real-World Example

A blog block with an AI filter variation:

✅ **CORRECT:**
```
blocks/view-myblog/
├── view-myblog.js    # Single file with both standard and AI filtering
├── view-myblog.css
└── README.md
```

❌ **INCORRECT:**
```
blocks/view-myblog/
├── view-myblog.js
├── view-myblog-ai.js  # DON'T DO THIS
├── view-myblog.css
└── README.md
```

**Implementation pattern:**
```javascript
export default async function decorate(block) {
  // Detect AI variation
  const isAIVariation = block.classList.contains('ai');

  // Fetch data
  const rawData = await fetchData();

  // Filter or transform data based on variation
  const processedData = isAIVariation ? filterAIContent(rawData) : rawData;

  // Render with variation-aware logic
  const title = isAIVariation ? 'Latest AI Posts' : 'Latest Posts';
  render(block, processedData, title);
}

// Helper function for AI filtering
function filterAIContent(data) {
  // Filter logic specific to AI variation
  return data.filter(post =>
    post.url.includes('/ai/') ||
    post.title.toLowerCase().includes('ai')
  );
}
```

### How Authors Use Variations

In Google Docs:
```
| view-myblog (ai) |
|------------------|
```

This creates:
```html
<div class="view-myblog ai block">
  <!-- Content -->
</div>
```

Your single JavaScript file detects the `ai` class and applies appropriate logic.

---

## Common Patterns

### Configuration Object

```javascript
export default function decorate(block) {
  // Configuration at the top
  const config = {
    autoplay: block.dataset.autoplay === 'true',
    delay: parseInt(block.dataset.delay) || 3000,
    animation: block.dataset.animation || 'fade'
  };

  // Use config throughout
}
```

### Data Attributes for Options

```javascript
export default function decorate(block) {
  // Read options from data attributes
  const layout = block.dataset.layout || 'grid';
  const columns = parseInt(block.dataset.columns) || 3;

  // Apply classes based on options
  block.classList.add(`layout-${layout}`);
  block.style.setProperty('--columns', columns);
}
```

### Helper Functions

```javascript
// Helper functions outside decorate
function createCard(data) {
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <h3>${data.title}</h3>
    <p>${data.description}</p>
  `;
  return card;
}

export default function decorate(block) {
  const data = extractContent(block);

  const container = document.createElement('div');
  data.forEach(item => {
    container.appendChild(createCard(item));
  });

  block.textContent = '';
  block.appendChild(container);
}
```

---

## Common Mistakes to Avoid

### ❌ CRITICAL: Don't Use EDS Reserved Class Names

```javascript
// ❌ BAD - Class name conflicts with EDS automatic naming
function createOverlay(content) {
  const backdrop = document.createElement('div');
  backdrop.className = 'overlay-container'; // EDS adds this to parent section!
  return backdrop;
}

// ✅ GOOD - Use different class name
function createOverlay(content) {
  const backdrop = document.createElement('div');
  backdrop.className = 'overlay-backdrop'; // Safe - won't conflict
  return backdrop;
}
```

**Never use these patterns in your code:**
- `.{blockname}-container` - Reserved by EDS for parent sections
- `.{blockname}-wrapper` - Reserved by EDS for block elements

**This mistake caused a production bug:** Using `.overlay-container` in CSS with `position: fixed; z-index: 999; opacity: 0;` made entire pages invisible because EDS added `overlay-container` class to the parent section, applying those styles to the wrong element.

### ⚠️ CRITICAL: When to Use and When to Avoid Global Selectors

**Understanding the distinction between block-scoped and document-level operations is essential for EDS block development.**

#### ❌ NEVER Use Global Selectors for Block-Scoped Operations

**This is the most common bug in EDS blocks!**

When decorating a block, NEVER query for the block itself or its children using global selectors. ALWAYS use the `block` parameter.

```javascript
// ❌ BAD - Uses global selectors instead of block parameter
export default function decorate(block) {
  const bioElement = document.querySelector('.bio');  // ❌ Gets FIRST block on page!

  if (!bioElement.classList.contains('hide-author')) {
    const imgElement = document.querySelector('.bio.block img');  // ❌ Global!
    const bioBlock = document.querySelector('.bio.block');        // ❌ Global!

    bioBlock.appendChild(authorElement);  // ❌ Always modifies first block!
  }
}
```

**Why this is wrong:**
- `document.querySelector('.bio')` always returns the FIRST matching element on the page
- If you have multiple bio blocks, they ALL use the first block's configuration
- The second, third, etc. blocks won't work correctly
- Image link conversion fails because it checks the wrong block

```javascript
// ✅ GOOD - Uses block parameter for proper scoping
export default function decorate(block) {
  // Check the CURRENT block, not a global selector
  if (!block.classList.contains('hide-author')) {
    // Find img within CURRENT block
    const imgElement = block.querySelector('img');

    // Append to CURRENT block
    block.appendChild(authorElement);
  }
}
```

**Why this is correct:**
- The `block` parameter is the specific block being decorated
- Each block operates independently
- Multiple blocks on the same page work correctly
- Each block can have different configurations

**Real-world bug example:**
```javascript
// ❌ This code broke in production:
const bioElement = document.querySelector('.bio');  // Always gets first block
if (!bioElement.classList.contains('hide-author')) {
  // Processes ALL blocks, but checks only the FIRST block's classes!
}
```

**The fix:**
```javascript
// ✅ Check the CURRENT block being decorated:
if (!block.classList.contains('hide-author')) {
  // Now each block checks its OWN classes
}
```

#### ✅ WHEN Global Selectors Are Appropriate

**Global selectors are INTENTIONAL and necessary for document-level operations.**

Some blocks legitimately need to operate at the document level, not just within their own scope. These are typically structural blocks that affect page-wide behavior.

**Document-level blocks include:**
- **Header/Navigation** - Controls body scroll, global keyboard events, responsive layout
- **Index/Table of Contents** - Scans all page headings to build navigation
- **Showcaser/Code Display** - Collects all code snippets from the entire page

**Example: Index Block (Document-Level)**
```javascript
export default function decorate(block) {
  // Global Selector is INTENTIONAL - used for Document access
  // This block scans ALL page headings to build table of contents
  const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');

  // Build navigation from all page headings
  headers.forEach((header, index) => {
    header.id = `header-${index}`;
    // Create nav links...
  });

  // ✅ Use block parameter for the block's own content
  const nav = block.querySelector('.index-content');
  // Add navigation items to block...
}
```

**Example: Header Block (Document-Level)**
```javascript
export default function decorate(block) {
  // Global Selector is INTENTIONAL - used for Document access
  // Document-level media query for responsive behavior
  const mobileMedia = window.matchMedia('(min-width: 900px)');

  function toggleMenu(open) {
    // Global Selector is INTENTIONAL - used for Document access
    // Document body scroll control when mobile menu is open
    document.body.style.overflowY = open ? 'hidden' : '';
  }

  // Global Selector is INTENTIONAL - used for Document access
  // Document-level keyboard listener for Escape key
  window.addEventListener('keydown', (e) => {
    if (e.code === 'Escape') {
      toggleMenu(false);
    }
  });
}
```

**When to use document-level selectors:**
- ✅ Querying page metadata: `document.querySelector('meta[name="author"]')`
- ✅ Controlling document body: `document.body.style.overflowY`
- ✅ Global event listeners: `window.addEventListener('keydown', ...)`
- ✅ Responsive queries: `window.matchMedia('(min-width: 900px)')`
- ✅ Page-wide element collection: `document.querySelectorAll('h1, h2, h3, h4, h5, h6')`
- ✅ Document structure access: `document.querySelector('header')`

**Defensive documentation pattern:**
Always add a comment explaining intentional global selector usage:
```javascript
// Global Selector is INTENTIONAL - used for Document access
// [Brief explanation of why this needs document-level access]
const elements = document.querySelector[All](...);
```

**For meta tags specifically:**
```javascript
// Meta tag selector is INTENTIONAL - document-level metadata
const author = document.querySelector('meta[name="author"]');
```

#### Rule of Thumb

**Inside `decorate(block)` function:**
- ✅ `block.querySelector()` - ALWAYS correct for block-scoped queries
- ✅ `block.classList` - ALWAYS correct for block-scoped classes
- ✅ `block.appendChild()` - ALWAYS correct for block-scoped DOM manipulation
- ❌ `document.querySelector('.your-block')` - NEVER correct (use `block` parameter)
- ✅ `document.querySelector('meta[name="author"]')` - OK for document-level metadata
- ✅ `document.querySelectorAll('h1, h2, h3, h4, h5, h6')` - OK for document-level queries
- ✅ `window.matchMedia()` - OK for responsive behavior
- ✅ `document.body` - OK for document-level control

**Key distinction:** Are you querying/modifying the block itself (use `block` parameter) or the document/page (global selectors are intentional)?

### ❌ Don't Forget to Clear the Block

```javascript
// ❌ BAD - Original content remains
export default function decorate(block) {
  const container = document.createElement('div');
  block.appendChild(container); // Adds to existing content
}

// ✅ GOOD - Clear first
export default function decorate(block) {
  const data = extractContent(block);
  block.textContent = ''; // Clear first
  block.appendChild(container);
}
```

### ❌ Don't Use innerHTML for User Content

```javascript
// ❌ BAD - XSS vulnerability
export default function decorate(block) {
  const userInput = block.textContent;
  block.innerHTML = `<div>${userInput}</div>`; // Dangerous!
}

// ✅ GOOD - Use textContent or createElement
export default function decorate(block) {
  const userInput = block.textContent;
  const div = document.createElement('div');
  div.textContent = userInput; // Safe
  block.textContent = '';
  block.appendChild(div);
}
```

### ❌ Don't Forget Error Handling

```javascript
// ❌ BAD - No error handling
export default async function decorate(block) {
  const response = await fetch('/api/data');
  const data = await response.json();
  renderData(block, data);
}

// ✅ GOOD - Proper error handling
export default async function decorate(block) {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    renderData(block, data);
  } catch (error) {
    console.error('Failed to load:', error);
    block.innerHTML = '<p>Failed to load content</p>';
  }
}
```

### ❌ CRITICAL: Don't Forget to Update ALL Block Documentation

**This is a common mistake that causes incomplete documentation after architectural changes.**

When making architectural changes to a block (refactoring, adding major features, changing patterns), you must update **ALL** documentation files, not just some of them.

**Required documentation files for EVERY block:**

1. **blocks/{blockname}/README.md** - Primary user-facing documentation
   - Overview and features
   - Usage examples
   - Configuration options
   - Architecture sections (if applicable)

2. **blocks/{blockname}/block-architecture.md** - Technical documentation
   - Architecture patterns
   - Module descriptions
   - Code organization
   - Version history

3. **CHANGELOG.md** - Project-wide changelog
   - Document all changes with details
   - Include architectural benefits
   - List affected files

4. **CLAUDE.md** - Project guide for AI assistants
   - Critical patterns section
   - Reference to block features
   - Links to documentation

5. **README.md** (project root) - Project overview
   - Update block descriptions
   - Add new features to lists

6. **docs/for-ai/index.md** - AI documentation index
   - Add entries for new documentation
   - Update existing references

**Real-world mistake:**

After implementing a unified overlay architecture refactor for ipynb-viewer:
- ✅ Updated: CHANGELOG.md, CLAUDE.md, project README.md, docs/for-ai/index.md
- ✅ Created: overlay/README.md, summary document, progress tracking
- ✅ Updated: block-architecture.md
- ❌ **FORGOT**: blocks/ipynb-viewer/README.md (the main block README!)

**Impact:**
- Users see outdated documentation
- New architecture not discoverable
- Inconsistent documentation across files
- Confusion about which version is current

**Checklist for architectural changes:**

```bash
# After making architectural changes, verify ALL these files are updated:
blocks/{blockname}/README.md           # Main block documentation
blocks/{blockname}/block-architecture.md  # Technical documentation
CHANGELOG.md                           # Project changelog
CLAUDE.md                              # Project guide
README.md                              # Project root
docs/for-ai/index.md                   # AI docs index
```

**Before committing, ask yourself:**
1. Did I update the main block README.md?
2. Did I update block-architecture.md?
3. Did I add a CHANGELOG.md entry?
4. Did I update CLAUDE.md with critical patterns?
5. Did I update the project README.md?
6. Did I update docs/for-ai/index.md?

**Why this matters:**
- Documentation is the first thing developers read
- Incomplete docs waste time (users don't know about new features)
- Inconsistent docs cause confusion (which version is correct?)
- Main README.md is often viewed first - must be current

**Pattern to follow:**

```javascript
// After completing architectural work:
// 1. List all documentation files
// 2. Check each file systematically
// 3. Update with consistent information
// 4. Commit all updates together
```

**Related production bug:** After implementing unified overlay refactor (8 modules, complete architecture change), the main blocks/ipynb-viewer/README.md was not updated, leaving users with no knowledge of the new architecture until a code review caught the omission.

---

## When Struggling to Find Answers

**If you're having trouble understanding a block's implementation or finding specific technical details:**

1. **Check for block-specific architecture documentation:**
   - Look for `blocks/{blockname}/block-architecture.md` in the block folder
   - This file contains detailed technical architecture specific to that block
   - Example: `blocks/ipynb-viewer/block-architecture.md` documents the ipynb-viewer's rendering pipeline, processing order, and critical implementation details

2. **Why this matters:**
   - Block-specific architecture docs contain implementation details not found in general EDS guides
   - They document processing order, critical timing issues, and block-specific patterns
   - They often include solutions to previously encountered bugs and edge cases

3. **When to read block-architecture.md:**
   - When implementing similar functionality in a new block
   - When debugging issues in an existing block
   - When making modifications to complex blocks
   - When you need to understand the "why" behind implementation decisions

**Example:** The ipynb-viewer block has extensive architecture documentation covering:
- Markdown parsing pipeline and processing order
- Code block restoration timing (critical for preventing rendering bugs)
- Smart link resolution patterns
- Overlay system architecture

---

## JavaScript Code Quality & ESLint Standards

### Critical ESLint Rules to Follow

**The project uses Airbnb JavaScript style guide with custom rules. Follow these patterns to avoid lint errors:**

### 1. No Unused Variables

```javascript
// ❌ BAD - Variable defined but never used
function processData(data, context) {
  const result = data.map(item => item.value);
  return result;
  // 'context' is never used - ESLint error!
}

// ✅ GOOD - Prefix unused parameters with underscore
function processData(data, _context) {
  const result = data.map(item => item.value);
  return result;
  // '_context' prefix signals intentionally unused
}

// ✅ GOOD - Remove unused parameter entirely
function processData(data) {
  const result = data.map(item => item.value);
  return result;
}
```

**Why this matters:** Unused variables clutter code and may indicate bugs or incomplete implementations.

### 2. No Variable Shadowing

```javascript
// ❌ BAD - 'block' parameter shadows outer 'block'
export default function decorate(block) {
  const rows = Array.from(block.children);

  rows.forEach((row) => {
    function processBlock(block) { // Shadows outer 'block'!
      return block.textContent;
    }
  });
}

// ✅ GOOD - Use specific names to avoid shadowing
export default function decorate(block) {
  const rows = Array.from(block.children);

  rows.forEach((row) => {
    function processBlock(element) { // Clear, no shadowing
      return element.textContent;
    }
  });
}
```

**Why this matters:** Variable shadowing makes code confusing and error-prone. It's unclear which variable you're referencing.

### 3. No Unary Operators (++ and --)

```javascript
// ❌ BAD - Unary operators not allowed
for (let i = 0; i < items.length; i++) {
  processItem(items[i]);
}

let count = 0;
count++;

// ✅ GOOD - Use += 1 or -= 1
for (let i = 0; i < items.length; i += 1) {
  processItem(items[i]);
}

let count = 0;
count += 1;

// ✅ BETTER - Use forEach or map
items.forEach((item) => processItem(item));
```

**Why this matters:** Unary operators can be confusing and lead to subtle bugs with pre/post increment behavior.

### 4. No Lonely If (else with single if)

```javascript
// ❌ BAD - Lone if as only statement in else block
if (condition1) {
  doSomething();
} else {
  if (condition2) { // Lonely if in else
    doSomethingElse();
  }
}

// ✅ GOOD - Use else if
if (condition1) {
  doSomething();
} else if (condition2) {
  doSomethingElse();
}
```

**Why this matters:** Reduces unnecessary nesting and improves readability.

### 5. Avoid Await in Loop (When Possible)

```javascript
// ⚠️ PROBLEMATIC - Sequential awaits in loop
for (const file of files) {
  await processFile(file); // Processes one at a time
}

// ✅ BETTER - Process in parallel
await Promise.all(files.map(file => processFile(file)));

// ✅ ACCEPTABLE - When sequential processing is required
// Add eslint-disable comment with explanation
/* eslint-disable no-await-in-loop */
// Sequential processing required to avoid race conditions
for (const file of files) {
  await updateFile(file);
}
/* eslint-enable no-await-in-loop */
```

**Why this matters:** Await in loops is often unintentional and causes unnecessary slowness. However, it's acceptable when you need sequential processing (e.g., file writes to avoid race conditions).

### 6. ParseInt Always Needs Radix

```javascript
// ❌ BAD - Missing radix parameter
const number = parseInt(str);

// ✅ GOOD - Always specify radix (usually 10)
const number = parseInt(str, 10);
```

**Why this matters:** Without radix, `parseInt('08')` may parse as octal (base 8) instead of decimal.

### 7. Use Number.isNaN Instead of isNaN

```javascript
// ❌ BAD - Global isNaN has type coercion issues
if (isNaN(value)) {
  // ...
}

// ✅ GOOD - Number.isNaN is strict
if (Number.isNaN(value)) {
  // ...
}
```

**Why this matters:** Global `isNaN('hello')` returns `true` because it coerces to number first. `Number.isNaN()` is strict.

### 8. Escape Special Characters in Regex

```javascript
// ❌ BAD - Unescaped special characters
const pattern = /file.txt/;

// ✅ GOOD - Escape dots and other special chars
const pattern = /file\.txt/;
```

**Why this matters:** Unescaped dots match any character, not literal dots.

### 9. Object Formatting (object-curly-newline)

```javascript
// ❌ BAD - Inconsistent formatting for long objects
const cell = { cell_type: 'code', source: ['console.log("test");'], metadata: {}, outputs: [] };

// ✅ GOOD - Use line breaks for objects with multiple properties
const cell = {
  cell_type: 'code',
  source: ['console.log("test");'],
  metadata: {},
  outputs: [],
};

// ✅ ALSO GOOD - Single line for simple objects
const point = { x: 10, y: 20 };
```

**Why this matters:** Consistent formatting improves readability for complex objects.

### 10. Import/Require Patterns

```javascript
// ❌ BAD - Unable to resolve path (incorrect relative path)
import { helper } from '../../../../../../../scripts/scripts.js';

// ✅ GOOD - Fix relative path
import { helper } from '../../scripts/scripts.js';

// ✅ GOOD - Or add eslint-disable for intentional external references
// eslint-disable-next-line import/no-unresolved
import { helper } from '../external/scripts.js';
```

**Why this matters:** Incorrect import paths cause runtime errors.

### Quick Checklist Before Committing

✅ **Run linter:** `npm run lint:js`
✅ **No unused variables** - Remove or prefix with `_`
✅ **No shadowing** - Use specific variable names
✅ **Use `+= 1` instead of `++`**
✅ **Use `else if` instead of `else { if }`**
✅ **Always specify radix in parseInt()**
✅ **Use `Number.isNaN()` not `isNaN()`**
✅ **Escape special regex characters**
✅ **Format long objects with line breaks**

### When to Disable Rules

**Only disable rules with clear justification:**

```javascript
// ✅ GOOD - Justified disable with explanation
/* eslint-disable no-await-in-loop */
// Sequential file processing required to avoid race conditions
for (const file of files) {
  await writeFile(file);
}
/* eslint-enable no-await-in-loop */

// ❌ BAD - Blanket disable without reason
/* eslint-disable */
// Don't do this!
```

### Common Patterns That Pass Linting

```javascript
// Pattern: Processing array items
items.forEach((item, index) => {
  processItem(item);
  // If index is unused, either remove it or prefix: (_item, _index)
});

// Pattern: Event handlers with unused event object
button.addEventListener('click', (_e) => {
  // Use _e to signal event param is intentionally unused
  handleClick();
});

// Pattern: Function parameters you might not use yet
function createOverlay(content, _options) {
  // _options prefix shows it's for future use
  return buildOverlay(content);
}
```

### Auto-Fix with ESLint

Some errors can be auto-fixed:

```bash
# Fix auto-fixable issues
npm run lint:js -- --fix

# Or for specific file
npx eslint blocks/your-block/your-block.js --fix
```

**Auto-fixable rules include:**
- Trailing commas
- Quote style
- Indentation
- Some spacing issues

**Not auto-fixable (require manual fixes):**
- Unused variables
- Variable shadowing
- Unary operators
- Most logic issues

---

## Related Documentation

- **[Block Architecture Standards](../../../docs/for-ai/implementation/block-architecture-standards.md)** - Comprehensive architecture guide
- **[Frontend Guidelines](../../../docs/for-ai/guidelines/frontend-guidelines.md)** - JavaScript and CSS standards
- **[EDS Native Testing](../../../docs/for-ai/testing/eds-native-testing-standards.md)** - Testing patterns
- **[Content Driven Development](../content-driven-development/SKILL.md)** - CDD workflow

---

## Next Steps

1. Read the Content Driven Development skill for workflow guidance
2. Create your block structure with proper file organization
3. Implement the decorate function following these patterns
4. Create a test.html file to test locally
5. Run tests and verify functionality
6. Document your block in README.md and EXAMPLE.md

**Remember:** EDS blocks are simple, performant, and follow vanilla JavaScript patterns. Avoid frameworks, keep dependencies minimal, and focus on clean, maintainable code.
