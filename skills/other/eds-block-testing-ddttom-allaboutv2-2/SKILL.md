---
name: eds-block-testing
description: Guide for testing EDS blocks using test.html files and the development server. Covers test file structure, EDS core integration, testing patterns, and debugging workflows for Adobe Edge Delivery Services blocks.
---

# EDS Block Testing Guide

## Purpose

Guide developers through testing Adobe Edge Delivery Services (EDS) blocks using test.html files, the development server, and proper EDS integration patterns.

## When to Use This Skill

Automatically activates when:
- Creating or editing `test.html` files in block directories
- Working with keywords: "test block", "test.html", "debug block"
- Implementing block testing patterns
- Using the development server

---

## Quick Start: Create a Test File

Every block should have a `test.html` file in its directory:

```
blocks/your-block/
├── your-block.js
├── your-block.css
├── README.md
├── EXAMPLE.md
└── test.html          ← Create this file
```

---

## Standard Test File Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Block Test - EDS Native Pattern</title>

    <!-- EDS Core Styles -->
    <link rel="stylesheet" href="/styles/styles.css">
    <link rel="stylesheet" href="/styles/fonts.css">
    <link rel="stylesheet" href="/styles/lazy-styles.css">

    <!-- Note: Block CSS is loaded automatically by EDS -->

    <style>
        /* Test-specific styling */
        body {
            padding: 2rem;
            background: var(--light-color);
        }

        .test-content {
            max-width: 1200px;
            margin: 0 auto;
            background: var(--background-color);
            padding: 2rem;
            border-radius: 8px;
        }

        .test-section {
            margin: 2rem 0;
            padding: 1rem;
            border: 1px solid var(--dark-color);
            border-radius: 4px;
        }

        /* EDS pattern - ensure body appears */
        body.appear {
            display: block;
        }
    </style>
</head>
<body>
    <div class="test-content">
        <h1>Your Block Test Page</h1>

        <div class="test-section">
            <h2>Test Case 1: Basic Usage</h2>

            <!-- Your block with test content (note: only block name class, .block is added by script) -->
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

        <div class="test-section">
            <h2>Test Case 2: With Images</h2>

            <div class="your-block">
                <div>
                    <div>
                        <picture>
                            <img src="/images/test-image.jpg" alt="Test">
                        </picture>
                    </div>
                    <div>Content with image</div>
                </div>
            </div>
        </div>
    </div>

    <!-- EDS Core Scripts -->
    <script type="module">
        import {
            sampleRUM,
            loadBlock,
            loadCSS
        } from '/scripts/aem.js';

        // Initialize RUM (optional for testing)
        sampleRUM('top');
        window.addEventListener('load', () => sampleRUM('load'));

        // CRITICAL: Add body.appear class FIRST (before loadBlock)
        // EDS global styles hide body by default to prevent FOUC
        // This makes the page visible before blocks load
        document.body.classList.add('appear');

        // Load all blocks on the page
        // Mimic EDS behavior: find by block name, add .block class automatically
        const blocks = document.querySelectorAll('.your-block');

        for (const block of blocks) {
            try {
                // Add .block class like EDS decorateBlock() does
                block.classList.add('block');
                await loadBlock(block);
                console.log(`✅ Block loaded: ${block.className}`);
            } catch (error) {
                console.error(`❌ Block failed: ${block.className}`, error);
            }
        }
    </script>
</body>
</html>
```

**Important Notes:**
- The `document.body.classList.add('appear')` line is **required** and must be called **before** `loadBlock()`. EDS hides the body by default (`body { display: none; }` in `styles/styles.css`) to prevent Flash of Unstyled Content (FOUC). Adding the `appear` class makes the page visible. In production, EDS adds this automatically, but test files must add it manually.
- **The `.block` class is automatically added by the script** (line `block.classList.add('block')`) to mimic EDS production behavior. In your HTML, only use the block name class (e.g., `class="your-block"`).
- This approach ensures test files behave identically to production where EDS's `decorateBlock()` adds the `.block` class automatically.

---

## Development Server Workflow

### Start the Server

```bash
npm run debug
```

The server starts on `http://localhost:3000` with:
- Automatic proxy fallback to production site
- CORS headers for cross-origin requests
- Enhanced logging for debugging
- Hot-reload support

### Access Your Test

```
http://localhost:3000/blocks/your-block/test.html
```

### Development Flow

1. Edit your block JavaScript or CSS
2. Refresh the test page in your browser
3. Check the browser console for errors
4. Iterate and test

---

## EDS Block Structure in Test Files

### Basic Two-Column Structure

```html
<div class="your-block">
    <!-- Row 1 -->
    <div>
        <div>Column 1 Content</div>
        <div>Column 2 Content</div>
    </div>
    <!-- Row 2 -->
    <div>
        <div>Column 1 Content</div>
        <div>Column 2 Content</div>
    </div>
</div>
```

**Important:**
- This structure matches how EDS creates blocks from Google Docs tables
- The `.block` class is **automatically added** by EDS's `decorateBlock()` function in production
- For test files, you can either:
  - Add `.block` manually: `<div class="your-block block">`
  - Let your test script add it automatically (recommended - mimics production behavior)

### With Images

```html
<div class="your-block">
    <div>
        <div>
            <picture>
                <source type="image/webp" srcset="/image.webp">
                <img src="/image.jpg" alt="Description" loading="lazy">
            </picture>
        </div>
        <div>Text content</div>
    </div>
</div>
```

### With Links

```html
<div class="your-block">
    <div>
        <div>
            <a href="https://example.com">Link Text</a>
        </div>
        <div>Description</div>
    </div>
</div>
```

### With Data Attributes

```html
<div class="your-block"
     data-layout="grid"
     data-columns="3"
     data-autoplay="true">
    <!-- Block content -->
</div>
```

**Note:** Examples show blocks without the `.block` class. Your test script should add it automatically to mimic EDS production behavior.

---

## Loading Blocks Programmatically

### Basic Block Loading

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');
    await loadBlock(block);
</script>
```

### Loading Multiple Blocks

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const blocks = document.querySelectorAll('.block');

    // Load blocks sequentially
    for (const block of blocks) {
        await loadBlock(block);
    }

    // Or load in parallel
    await Promise.all(
        Array.from(blocks).map(block => loadBlock(block))
    );
</script>
```

### With Error Handling

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const blocks = document.querySelectorAll('.block');

    for (const block of blocks) {
        try {
            await loadBlock(block);
            console.log(`✅ Loaded: ${block.className}`);
        } catch (error) {
            console.error(`❌ Failed to load: ${block.className}`, error);
            block.innerHTML = '<p class="error">Failed to load block</p>';
        }
    }
</script>
```

---

## Testing Different Scenarios

### Test Empty Content

```html
<div class="test-section">
    <h2>Test Case: Empty Content</h2>
    <div class="your-block block">
        <!-- No content - test error handling -->
    </div>
</div>
```

### Test Invalid Content

```html
<div class="test-section">
    <h2>Test Case: Invalid Structure</h2>
    <div class="your-block block">
        <div>
            <div>Only One Column</div>
            <!-- Missing second column -->
        </div>
    </div>
</div>
```

### Test Edge Cases

```html
<div class="test-section">
    <h2>Test Case: Very Long Content</h2>
    <div class="your-block block">
        <div>
            <div>Short title</div>
            <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit... (very long text)</div>
        </div>
    </div>
</div>
```

### Test Responsive Behavior

```html
<style>
    .test-mobile {
        max-width: 375px;
        margin: 0 auto;
    }

    .test-tablet {
        max-width: 768px;
        margin: 0 auto;
    }
</style>

<div class="test-section test-mobile">
    <h2>Test Case: Mobile View (375px)</h2>
    <div class="your-block block">
        <!-- Content -->
    </div>
</div>

<div class="test-section test-tablet">
    <h2>Test Case: Tablet View (768px)</h2>
    <div class="your-block block">
        <!-- Content -->
    </div>
</div>
```

---

## Debugging Tips

### Console Logging

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');

    console.group('Block Loading');
    console.log('Block element:', block);
    console.log('Block classes:', block.className);
    console.log('Block content before:', block.innerHTML);

    await loadBlock(block);

    console.log('Block content after:', block.innerHTML);
    console.groupEnd();
</script>
```

### Timing Performance

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');

    console.time('Block Load Time');
    await loadBlock(block);
    console.timeEnd('Block Load Time');
</script>
```

### Check Network Requests

Open Chrome DevTools → Network tab to see:
- Which CSS files are loaded
- Which JavaScript modules are loaded
- Any failed requests (404, 500, etc.)

### Common Issues and Solutions

#### Issue: Page is Blank or Invisible

**Symptoms:**
- Page loads but nothing displays
- Browser shows white/blank screen
- Console shows no JavaScript errors
- Elements exist in DOM but aren't visible

**Root Cause:** CSS class name conflicts with EDS reserved names

**Solution:** Never use these class patterns in your CSS or JavaScript:
- `.{blockname}-container` - EDS adds to parent `<section>` elements
- `.{blockname}-wrapper` - EDS adds to block parent `<div>` wrappers
- `.block` - EDS adds to all block elements (avoid styling globally)
- `.section` - EDS adds to all sections (avoid styling globally)
- `.button-container` - EDS adds to button parent elements
- `.default-content-wrapper` - EDS adds to default content wrappers

**Example of the bug:**
```css
/* ❌ BAD - Will be applied to parent section, not your modal */
.overlay-container {
  position: fixed;
  z-index: 999;
  opacity: 0;  /* Makes entire page invisible! */
}

/* ✅ GOOD - Use different suffix */
.overlay-backdrop {
  position: fixed;
  z-index: 999;
  opacity: 0;  /* Only affects your backdrop element */
}
```

**Why this happens:**
1. EDS's `decorateBlock()` adds `.{blockname}-container` to parent sections (aem.js:684)
2. Your CSS targets `.{blockname}-container` for your component
3. Browser applies your styles to the section instead of your element
4. Section gets `position: fixed; opacity: 0` making page invisible

**Other global classes that can cause issues:**
```css
/* ❌ DANGER - These affect ALL blocks/sections if styled incorrectly */
.block { position: fixed; }           /* Breaks ALL blocks */
.section { display: none; }           /* Hides ALL sections */
.button-container { overflow: hidden; } /* Breaks ALL buttons */
```

**How to debug:**
1. Open browser console
2. Run: `document.querySelector('section').className`
3. If you see `{blockname}-container` in the class list, rename your CSS classes
4. Check if styling global classes like `.block` or `.section` with layout properties

#### Issue: Block CSS Not Loading

**Solution:** Ensure your CSS file has the exact same name as your JS file:

```
blocks/your-block/
├── your-block.js   ✅ Matches
├── your-block.css  ✅ Matches
└── test.html
```

#### Issue: Block Not Rendering

**Check:**
1. Console for JavaScript errors
2. Block structure matches expected pattern
3. `decorate` function is exported as default
4. Block class name is correct

#### Issue: Images Not Loading

**Solution:** Use absolute paths from project root:

```html
<!-- ❌ BAD -->
<img src="image.jpg">

<!-- ✅ GOOD -->
<img src="/images/image.jpg">
```

---

## Interactive Testing Tools

### Add Test Controls

```html
<div class="test-controls">
    <button onclick="reloadBlock()">Reload Block</button>
    <button onclick="clearBlock()">Clear Block</button>
    <button onclick="logBlockState()">Log State</button>
</div>

<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');

    window.reloadBlock = async () => {
        console.log('Reloading block...');
        block.innerHTML = originalHTML; // Save original
        await loadBlock(block);
    };

    window.clearBlock = () => {
        block.innerHTML = '';
    };

    window.logBlockState = () => {
        console.log('Block state:', {
            className: block.className,
            children: block.children.length,
            innerHTML: block.innerHTML
        });
    };

    // Save original HTML
    const originalHTML = block.innerHTML;
    await loadBlock(block);
</script>
```

### Data Attribute Testing

```html
<div class="test-controls">
    <label>
        Layout:
        <select onchange="updateLayout(this.value)">
            <option value="grid">Grid</option>
            <option value="list">List</option>
            <option value="carousel">Carousel</option>
        </select>
    </label>
</div>

<div class="your-block block" data-layout="grid">
    <!-- Content -->
</div>

<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');
    const originalHTML = block.innerHTML;

    window.updateLayout = async (layout) => {
        block.innerHTML = originalHTML;
        block.dataset.layout = layout;
        await loadBlock(block);
    };

    await loadBlock(block);
</script>
```

---

## Accessibility Testing

### Test Keyboard Navigation

```html
<div class="test-section">
    <h2>Accessibility Test</h2>
    <p>Use Tab to navigate, Enter/Space to activate</p>

    <div class="your-block block">
        <!-- Interactive content -->
    </div>
</div>

<script type="module">
    // Log keyboard events for testing
    document.addEventListener('keydown', (e) => {
        console.log('Key pressed:', e.key, 'on:', e.target);
    });
</script>
```

### Test Screen Reader Compatibility

**Use Chrome DevTools:**
1. Open DevTools → Elements
2. Right-click element → Inspect Accessibility Properties
3. Check ARIA labels, roles, and descriptions

---

## Performance Testing

### Measure Rendering Time

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');

    // Mark start time
    performance.mark('block-load-start');

    await loadBlock(block);

    // Mark end time
    performance.mark('block-load-end');

    // Measure duration
    performance.measure(
        'block-load-time',
        'block-load-start',
        'block-load-end'
    );

    const measure = performance.getEntriesByName('block-load-time')[0];
    console.log(`Block loaded in ${measure.duration.toFixed(2)}ms`);
</script>
```

### Check for Memory Leaks

```html
<script type="module">
    import { loadBlock } from '/scripts/aem.js';

    const block = document.querySelector('.your-block');

    // Load and unload multiple times
    for (let i = 0; i < 100; i++) {
        const originalHTML = block.innerHTML;
        await loadBlock(block);

        // Reset for next iteration
        block.innerHTML = originalHTML;
    }

    console.log('Memory test complete - check DevTools Memory tab');
</script>
```

---

## Related Documentation

- **[EDS Block Development](../eds-block-development/SKILL.md)** - Block development patterns
- **[EDS Native Testing Standards](../../../docs/for-ai/testing/eds-native-testing-standards.md)** - Comprehensive testing guide
- **[Debug Guide](../../../docs/for-ai/testing/debug.md)** - Debugging workflows
- **[Development Server](../../../docs/Server-README.md)** - Server configuration

---

## Testing Checklist

Before considering your block complete, test:

- [ ] Basic functionality with standard content
- [ ] Empty/missing content handling
- [ ] Very long content (text overflow)
- [ ] Images load correctly
- [ ] Links work and have correct targets
- [ ] Responsive behavior (mobile, tablet, desktop)
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Performance (load time < 100ms for simple blocks)
- [ ] Browser console shows no errors
- [ ] Works with multiple instances on same page

---

## Next Steps

1. Create test.html for your block
2. Start the development server: `npm run debug`
3. Access your test file in the browser
4. Test all scenarios and edge cases
5. Fix any issues found during testing
6. Document test results in your README.md

**Remember:** Proper testing ensures your block works correctly in all scenarios and provides a great user experience on the production site!
