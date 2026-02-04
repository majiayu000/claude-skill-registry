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
├── your-block.js       # Decoration logic (REQUIRED)
├── your-block.css      # Block-specific styles (REQUIRED)
├── README.md           # Usage documentation (REQUIRED)
├── EXAMPLE.md          # Google Docs example (REQUIRED)
└── test.html           # Development test file (RECOMMENDED)
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
