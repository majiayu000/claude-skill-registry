---
name: widget-tester
description: Expert assistant for testing the embeddable Bible widget functionality in the KR92 Bible Voice project. Use when creating widget tests, validating embed API responses, testing reference formats, checking audio integration, or creating regression test cases.
---

# Widget Tester

## Context Files (Read First)

For widget and embed details, read from `Docs/context/`:
- `Docs/context/supabase-map.md` - Embed Edge Function
- `Docs/context/packages-map.md` - Shared packages

## Capabilities

- Generate test HTML pages for widget validation
- Validate embed API responses
- Test different reference formats
- Check audio integration

## Widget Overview

The widget (`public/widget.js`) is an embeddable JavaScript component that displays Bible verses on external websites.

### Basic Usage
```html
<script src="https://your-app-url.com/widget.js" defer></script>
<div class="rn-bible" data-ref="Joh.3:16"></div>
```

## Usage Examples

### Example 1: Create Comprehensive Test Page
**User:** "Create a test page for all widget features"

**Assistant:**
```html
<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raamattu Widget Test - Comprehensive</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
      background: #f5f5f5;
    }
    section {
      background: white;
      padding: 2rem;
      margin: 2rem 0;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2 {
      color: #333;
    }
    .test-case {
      margin: 1.5rem 0;
      padding: 1rem;
      border-left: 3px solid #4CAF50;
      background: #f9f9f9;
    }
    .test-label {
      font-weight: bold;
      color: #666;
      margin-bottom: 0.5rem;
    }
  </style>
</head>
<body>
  <h1>🧪 Raamattu Widget - Comprehensive Test Suite</h1>

  <!-- Single Verse Tests -->
  <section>
    <h2>1. Single Verse Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 1.1: Basic Finnish reference</div>
      <div class="rn-bible" data-ref="Joh.3:16"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 1.2: English reference</div>
      <div class="rn-bible" data-ref="John 3:16"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 1.3: Period separator</div>
      <div class="rn-bible" data-ref="Joh.3.16"></div>
    </div>
  </section>

  <!-- Verse Range Tests -->
  <section>
    <h2>2. Verse Range Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 2.1: Small range (2 verses)</div>
      <div class="rn-bible" data-ref="Joh.3:16-17"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 2.2: Larger range (Beatitudes)</div>
      <div class="rn-bible" data-ref="Matt.5:3-10"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 2.3: Psalm passage</div>
      <div class="rn-bible" data-ref="Ps.23:1-4"></div>
    </div>
  </section>

  <!-- Numbered Books Tests -->
  <section>
    <h2>3. Numbered Books Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 3.1: With period and space</div>
      <div class="rn-bible" data-ref="1. Joh.4:8"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 3.2: With space only</div>
      <div class="rn-bible" data-ref="1 Joh.4:8"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 3.3: No space</div>
      <div class="rn-bible" data-ref="1Joh.4:8"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 3.4: Moses books</div>
      <div class="rn-bible" data-ref="1. Moos.1:1-3"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 3.5: Corinthians</div>
      <div class="rn-bible" data-ref="1 Kor.13:4-7"></div>
    </div>
  </section>

  <!-- Different Versions Tests -->
  <section>
    <h2>4. Different Version Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 4.1: Default (STLK 2017)</div>
      <div class="rn-bible" data-ref="Joh.3:16"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 4.2: 1933/38 version</div>
      <div class="rn-bible" data-ref="Joh.3:16" data-version="finpr_finn"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 4.3: KJV (English)</div>
      <div class="rn-bible" data-ref="John 3:16" data-version="KJV"></div>
    </div>
  </section>

  <!-- Audio Tests -->
  <section>
    <h2>5. Audio Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 5.1: Single verse with audio</div>
      <div class="rn-bible" data-ref="Joh.1:1"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 5.2: Verse range with audio</div>
      <div class="rn-bible" data-ref="Joh.1:1-5"></div>
    </div>
  </section>

  <!-- Edge Cases -->
  <section>
    <h2>6. Edge Case Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 6.1: Long chapter (Psalm 119:1-8)</div>
      <div class="rn-bible" data-ref="Ps.119:1-8"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 6.2: Last verse of Bible</div>
      <div class="rn-bible" data-ref="Ilm.22:21"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 6.3: First verse of Bible</div>
      <div class="rn-bible" data-ref="1. Moos.1:1"></div>
    </div>
  </section>

  <!-- Error Cases -->
  <section>
    <h2>7. Error Handling Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 7.1: Missing data-ref</div>
      <div class="rn-bible"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 7.2: Invalid reference</div>
      <div class="rn-bible" data-ref="InvalidBook.99:999"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 7.3: Invalid version</div>
      <div class="rn-bible" data-ref="Joh.3:16" data-version="INVALID"></div>
    </div>
  </section>

  <!-- Dynamic Loading Test -->
  <section>
    <h2>8. Dynamic Loading Test</h2>
    <button id="addDynamic" style="padding: 0.5rem 1rem; font-size: 1rem; cursor: pointer;">
      Add Dynamic Widget
    </button>
    <div id="dynamicContainer" style="margin-top: 1rem;"></div>
  </section>

  <script>
    // Test dynamic widget loading
    document.getElementById('addDynamic').addEventListener('click', function() {
      const container = document.getElementById('dynamicContainer');
      const widget = document.createElement('div');
      widget.className = 'rn-bible';
      widget.setAttribute('data-ref', 'Rom.8:28');
      container.innerHTML = '';
      container.appendChild(widget);

      // Widget should auto-initialize via MutationObserver
      console.log('Dynamic widget added');
    });
  </script>

  <!-- Widget Script -->
  <script src="https://iryqgmjauybluwnqhxbg.supabase.co/widget.js" defer></script>
</body>
</html>
```

### Example 2: Test API Response Format
**User:** "Create test to validate embed API response"

**Assistant:**
See full example in skill content...

### Example 3: Audio Integration Test
**User:** "Create test for widget audio functionality"

**Assistant:**
See full example in skill content...

## Test Checklist

### Widget Loading
- [ ] Script loads without errors
- [ ] Widgets initialize on page load
- [ ] Dynamic widgets auto-initialize
- [ ] Multiple widgets work independently

### Reference Format Support
- [ ] Finnish abbreviations (Joh, Matt, Ps)
- [ ] English abbreviations (John, Matt, Ps)
- [ ] Full names (Johannes, Matthew, Psalms)
- [ ] Numbered books (1. Joh, 1 Joh, 1Joh)
- [ ] Moses books (1. Moos, 2 Moos)
- [ ] Colon separator (Joh.3:16)
- [ ] Period separator (Joh.3.16)
- [ ] Verse ranges (Joh.3:16-17)

### Version Support
- [ ] Default version (finstlk201)
- [ ] Alternative Finnish (finpr_finn)
- [ ] English KJV

### Audio Features
- [ ] Play button visible when audio available
- [ ] Play button disabled when audio unavailable
- [ ] Audio plays correct time range
- [ ] Pause/resume works
- [ ] Auto-stop at end
- [ ] Reset to start after playback
- [ ] Only one audio plays at a time

### Error Handling
- [ ] Missing data-ref shows error
- [ ] Invalid reference shows error message
- [ ] Network errors handled gracefully
- [ ] Invalid version handled

### Styling
- [ ] Shadow DOM isolates styles
- [ ] Responsive on mobile
- [ ] Readable typography
- [ ] Proper spacing

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| Write automated tests | `test-writer` |
| Edge Function changes | `edge-function-generator` |
| Bible lookup issues | `bible-lookup-helper` |
