---
name: eds-performance-debugging
description: Guide for debugging and performance optimization of EDS blocks including error handling, FOUC prevention, Core Web Vitals optimization, and debugging workflows for Adobe Edge Delivery Services.
---

# EDS Performance & Debugging Guide

## Purpose

Guide developers through debugging EDS blocks, optimizing performance, implementing proper error handling, and achieving excellent Core Web Vitals scores.

## When to Use This Skill

Automatically activates when:
- Debugging errors in blocks or scripts
- Working with keywords: "error", "debug", "performance", "slow", "FOUC"
- Optimizing Core Web Vitals
- Handling exceptions in block code

---

## Error Handling Patterns

### Basic Error Handling in Blocks

```javascript
export default function decorate(block) {
  try {
    // Extract content
    const content = extractContent(block);

    // Validate content
    if (!content || content.length === 0) {
      throw new Error('No content available');
    }

    // Create and render
    const container = createStructure(content);
    block.textContent = '';
    block.appendChild(container);

  } catch (error) {
    // Log error to console
    console.error('Block decoration failed:', error);

    // Show user-friendly error
    block.innerHTML = `
      <div class="error-message">
        <p>Unable to load content</p>
      </div>
    `;
  }
}
```

### Async Error Handling

```javascript
export default async function decorate(block) {
  try {
    // Show loading state
    showLoadingState(block);

    // Fetch data
    const response = await fetch('/api/data');

    // Check response
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Validate data
    if (!data || !Array.isArray(data)) {
      throw new Error('Invalid data format');
    }

    // Render content
    hideLoadingState(block);
    renderContent(block, data);

  } catch (error) {
    console.error('Failed to load block data:', error);

    // Show error state
    hideLoadingState(block);
    showErrorState(block, 'Failed to load content. Please try again later.');
  }
}

function showLoadingState(block) {
  block.innerHTML = '<div class="loading">Loading...</div>';
}

function hideLoadingState(block) {
  const loading = block.querySelector('.loading');
  if (loading) loading.remove();
}

function showErrorState(block, message) {
  block.innerHTML = `
    <div class="error-state">
      <p>${message}</p>
      <button onclick="location.reload()">Retry</button>
    </div>
  `;
}
```

### Graceful Degradation

```javascript
export default function decorate(block) {
  try {
    // Try to use modern feature
    if ('IntersectionObserver' in window) {
      setupLazyLoading(block);
    } else {
      // Fallback for older browsers
      loadAllImagesImmediately(block);
    }

  } catch (error) {
    console.error('Feature failed, using fallback:', error);
    // Fallback implementation
    basicImplementation(block);
  }
}
```

---

## Debugging Workflows

### Console Logging Best Practices

```javascript
export default function decorate(block) {
  // Use console groups for organization
  console.group('Block: your-block');

  // Log input state
  console.log('Input HTML:', block.innerHTML);
  console.log('Block classes:', block.className);

  try {
    const content = extractContent(block);
    console.log('Extracted content:', content);

    const container = createStructure(content);
    console.log('Created structure:', container);

    block.textContent = '';
    block.appendChild(container);

    console.log('Final HTML:', block.innerHTML);

  } catch (error) {
    console.error('Decoration failed:', error);
    console.trace(); // Show stack trace
  }

  console.groupEnd();
}
```

### Conditional Debugging

```javascript
const DEBUG = window.location.hostname === 'localhost';

function debug(...args) {
  if (DEBUG) {
    console.log('[DEBUG]', ...args);
  }
}

export default function decorate(block) {
  debug('Decorating block:', block.className);

  const content = extractContent(block);
  debug('Content extracted:', content);

  renderContent(block, content);
  debug('Rendering complete');
}
```

### Performance Timing

```javascript
export default async function decorate(block) {
  const startTime = performance.now();

  try {
    await loadAndRender(block);

    const endTime = performance.now();
    const duration = endTime - startTime;

    if (duration > 100) {
      console.warn(`Block took ${duration.toFixed(2)}ms (target: <100ms)`);
    } else {
      console.log(`Block loaded in ${duration.toFixed(2)}ms`);
    }

  } catch (error) {
    console.error('Block loading failed:', error);
  }
}
```

---

## FOUC Prevention

### CSS-First Approach

```css
/* your-block.css */

/* Hide block until decorated */
.your-block:not(.decorated) {
  visibility: hidden;
}

/* Show block after decoration */
.your-block.decorated {
  visibility: visible;
}
```

```javascript
// your-block.js
export default function decorate(block) {
  // Extract and process content
  const content = extractContent(block);
  const container = createStructure(content);

  // Replace content
  block.textContent = '';
  block.appendChild(container);

  // Mark as decorated (makes visible)
  block.classList.add('decorated');
}
```

### Placeholder Content

```css
.your-block::before {
  content: '';
  display: block;
  width: 100%;
  height: 300px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

.your-block.decorated::before {
  display: none;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Progressive Enhancement

```javascript
export default function decorate(block) {
  // Add loading class immediately
  block.classList.add('loading');

  try {
    // Build enhanced version
    const content = extractContent(block);
    const enhanced = createEnhancedStructure(content);

    // Replace with enhanced version
    block.textContent = '';
    block.appendChild(enhanced);

  } catch (error) {
    console.error('Enhancement failed:', error);
    // Keep original content if enhancement fails
  } finally {
    // Remove loading class
    block.classList.remove('loading');
    block.classList.add('decorated');
  }
}
```

---

## Core Web Vitals Optimization

### Largest Contentful Paint (LCP)

```javascript
export default function decorate(block) {
  // Prioritize above-the-fold images
  const images = block.querySelectorAll('img');

  images.forEach((img, index) => {
    if (index === 0) {
      // First image: high priority, no lazy loading
      img.loading = 'eager';
      img.fetchpriority = 'high';
    } else {
      // Other images: lazy load
      img.loading = 'lazy';
    }
  });
}
```

### Cumulative Layout Shift (CLS)

```css
/* Reserve space for images to prevent layout shift */
.your-block img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9; /* Reserve space */
}

/* Reserve space for dynamic content */
.your-block-container {
  min-height: 300px; /* Prevent shift during loading */
}
```

```javascript
export default async function decorate(block) {
  // Set explicit dimensions before loading content
  const height = block.offsetHeight;
  block.style.minHeight = `${height}px`;

  // Load content
  await loadContent(block);

  // Remove min-height after content loaded
  block.style.minHeight = '';
}
```

### First Input Delay (FID)

```javascript
export default function decorate(block) {
  // Defer non-critical work
  const criticalSetup = () => {
    // Critical rendering
    const content = extractContent(block);
    renderContent(block, content);
  };

  const nonCriticalSetup = () => {
    // Analytics, animations, etc.
    setupAnalytics(block);
    setupAnimations(block);
  };

  // Run critical work immediately
  criticalSetup();

  // Defer non-critical work
  if ('requestIdleCallback' in window) {
    requestIdleCallback(nonCriticalSetup);
  } else {
    setTimeout(nonCriticalSetup, 1);
  }
}
```

---

## Performance Optimization Patterns

### Minimize DOM Manipulation

```javascript
// ❌ BAD - Multiple reflows
export default function decorate(block) {
  items.forEach(item => {
    const div = document.createElement('div');
    div.textContent = item;
    block.appendChild(div); // Reflow on each append
  });
}

// ✅ GOOD - Single reflow
export default function decorate(block) {
  const fragment = document.createDocumentFragment();

  items.forEach(item => {
    const div = document.createElement('div');
    div.textContent = item;
    fragment.appendChild(div);
  });

  block.textContent = '';
  block.appendChild(fragment); // Single reflow
}
```

### Debounce Expensive Operations

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
    // Expensive resize logic
    recalculateLayout(block);
  }, 250);

  window.addEventListener('resize', handleResize);

  // Cleanup
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}
```

### Lazy Load Images

```javascript
export default function decorate(block) {
  const images = block.querySelectorAll('img');

  images.forEach(img => {
    // Native lazy loading
    img.loading = 'lazy';

    // Or use Intersection Observer
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const image = entry.target;
            image.src = image.dataset.src;
            observer.unobserve(image);
          }
        });
      });

      observer.observe(img);
    }
  });
}
```

### Optimize Event Listeners

```javascript
export default function decorate(block) {
  // ❌ BAD - Multiple listeners
  const items = block.querySelectorAll('.item');
  items.forEach(item => {
    item.addEventListener('click', handleClick);
  });

  // ✅ GOOD - Event delegation
  block.addEventListener('click', (e) => {
    const item = e.target.closest('.item');
    if (item) {
      handleClick(e, item);
    }
  });
}
```

---

## Common Issues and Solutions

### Issue: Blank Page / Block Not Visible

**Symptoms:**
- Console shows no errors
- JavaScript executes successfully
- Elements are in the DOM
- But page appears completely blank

**Root Cause:** EDS global styles hide `<body>` by default

**Solution:**

EDS uses a visibility pattern where the body is hidden until content is ready:

```css
/* In styles/styles.css */
body {
  display: none;  /* Hidden by default */
}

body.appear {
  display: block;  /* Only visible with this class */
}
```

**Fix for test files:**

```javascript
// Add to test.html or test-debug.html
<script type="module">
  import decorate from './your-block.js';

  // CRITICAL: Make body visible (required by EDS global styles)
  document.body.classList.add('appear');

  // Then proceed with decoration
  document.addEventListener('DOMContentLoaded', () => {
    const blocks = document.querySelectorAll('.your-block');
    blocks.forEach(decorate);
  });
</script>
```

**Debugging Steps:**

1. **Check if elements exist:**
   ```javascript
   console.log('Button in DOM:', document.querySelector('.your-button'));
   ```

2. **Check computed styles:**
   - Open DevTools → Elements tab
   - Inspect the element
   - Check Computed styles for `display: none` or `visibility: hidden`

3. **Check body visibility:**
   ```javascript
   console.log('Body classes:', document.body.className);
   console.log('Body computed display:', getComputedStyle(document.body).display);
   ```

4. **Force visibility (debugging):**
   ```javascript
   document.body.classList.add('appear');
   ```

**Production Notes:**
- In production, EDS automatically adds `appear` class when page loads
- Test files need to add it manually
- This pattern prevents FOUC (Flash of Unstyled Content)

### Issue: Block Not Rendering

**Check:**

```javascript
export default function decorate(block) {
  // 1. Check if block exists
  if (!block) {
    console.error('Block is null or undefined');
    return;
  }

  // 2. Check if block has content
  console.log('Block HTML:', block.innerHTML);
  if (!block.children.length) {
    console.warn('Block has no children');
  }

  // 3. Check for JavaScript errors
  try {
    const content = extractContent(block);
    console.log('Extracted content:', content);
  } catch (error) {
    console.error('Content extraction failed:', error);
  }
}
```

### Issue: Buttons Not Styled

**Symptoms:**
- Buttons exist in DOM but look unstyled
- No background color, borders, or padding

**Root Cause:** Global button styles not loading or not being applied

**Solution:**

1. **Verify global styles load:**
   ```html
   <!-- In test.html -->
   <link rel="stylesheet" href="/styles/styles.css">
   ```

2. **Check button inherits global styles:**
   ```css
   /* Global styles define button appearance */
   button {
     display: inline-block;
     padding: 5px 30px;
     background-color: var(--link-color);
     color: var(--background-color);
     border-radius: 30px;
     /* ... */
   }
   ```

3. **Add fallback styles if needed:**
   ```css
   /* In your-block.css - only if global styles fail */
   .your-block button {
     display: inline-block;
     padding: 10px 30px;
     background-color: #0066cc;
     color: white;
     border: none;
     border-radius: 30px;
     cursor: pointer;
   }
   ```

**Best Practice:** Rely on global styles, only add block-specific overrides

### Issue: CSS Not Loading

**Solution:**

1. Verify file names match exactly:
   ```
   blocks/your-block/
   ├── your-block.js   ← Must match
   ├── your-block.css  ← Must match
   ```

2. Check browser DevTools → Network tab for 404 errors

3. Ensure CSS is valid:
   ```bash
   npm run lint:css
   ```

### Issue: Memory Leaks

**Solution:** Clean up event listeners

```javascript
export default function decorate(block) {
  const handleClick = () => {
    console.log('Clicked');
  };

  // Add listener
  block.addEventListener('click', handleClick);

  // Return cleanup function
  return () => {
    block.removeEventListener('click', handleClick);
  };
}
```

### Issue: Race Conditions

**Solution:** Use proper async/await

```javascript
// ❌ BAD - Race condition
export default function decorate(block) {
  fetch('/api/data')
    .then(r => r.json())
    .then(data => renderData(block, data));

  // This runs before fetch completes
  setupEventListeners(block);
}

// ✅ GOOD - Proper sequencing
export default async function decorate(block) {
  const response = await fetch('/api/data');
  const data = await response.json();
  renderData(block, data);

  // This runs after data is rendered
  setupEventListeners(block);
}
```

---

## Browser DevTools Tips

### Network Tab

Monitor:
- CSS file loading (should be automatic)
- JavaScript module loading
- API requests and responses
- Failed requests (404, 500)

### Console Tab

Use:
- `console.log()` for debugging
- `console.error()` for errors
- `console.warn()` for warnings
- `console.table()` for structured data
- `console.time()` / `console.timeEnd()` for timing

### Performance Tab

Record and analyze:
1. Start recording
2. Interact with your block
3. Stop recording
4. Review:
   - Scripting time
   - Rendering time
   - Painting time
   - Long tasks (>50ms)

### Elements Tab

Use:
- Inspect DOM structure
- Check computed styles
- View event listeners
- Check accessibility tree

---

## Performance Monitoring

### Custom Timing

```javascript
export default async function decorate(block) {
  // Mark start
  performance.mark('block-start');

  // Do work
  await loadAndRender(block);

  // Mark end
  performance.mark('block-end');

  // Measure
  performance.measure('block-time', 'block-start', 'block-end');

  // Get results
  const measures = performance.getEntriesByName('block-time');
  console.log(`Block took ${measures[0].duration.toFixed(2)}ms`);

  // Clean up
  performance.clearMarks();
  performance.clearMeasures();
}
```

### Memory Usage

```javascript
if (performance.memory) {
  console.log('Memory usage:', {
    used: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
    total: (performance.memory.totalJSHeapSize / 1048576).toFixed(2) + ' MB',
    limit: (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2) + ' MB'
  });
}
```

---

## Testing for Performance

### Load Time Testing

```javascript
// Add to test.html
<script type="module">
  import { loadBlock } from '/scripts/aem.js';

  const block = document.querySelector('.your-block');

  const startTime = performance.now();
  await loadBlock(block);
  const endTime = performance.now();

  const duration = endTime - startTime;

  console.log(`Load time: ${duration.toFixed(2)}ms`);

  if (duration > 100) {
    console.warn('⚠️ Load time exceeds 100ms target');
  } else {
    console.log('✅ Load time within target');
  }
</script>
```

### Lighthouse Testing

```bash
# Test your block locally
npm run debug

# In Chrome:
# 1. Open DevTools
# 2. Go to Lighthouse tab
# 3. Select categories: Performance, Accessibility
# 4. Click "Generate report"
```

**Target scores:**
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+

---

## Error Boundaries

### Global Error Handler

```javascript
// In scripts/scripts.js or similar
window.addEventListener('error', (event) => {
  console.error('Global error:', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  });

  // Optionally send to analytics
  // trackError(event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);

  // Optionally send to analytics
  // trackError(event.reason);
});
```

### Block-Specific Error Boundary

```javascript
export default function decorate(block) {
  // Wrap entire block in try-catch
  const originalDecorate = () => {
    const content = extractContent(block);
    const container = createStructure(content);
    block.textContent = '';
    block.appendChild(container);
  };

  try {
    originalDecorate();
  } catch (error) {
    console.error(`Block ${block.className} failed:`, error);

    // Show error UI
    block.innerHTML = `
      <div class="block-error">
        <p>This content is temporarily unavailable.</p>
        ${DEBUG ? `<pre>${error.stack}</pre>` : ''}
      </div>
    `;
  }
}
```

---

## Related Documentation

- **[EDS Block Development](../eds-block-development/SKILL.md)** - Development patterns
- **[EDS Block Testing](../eds-block-testing/SKILL.md)** - Testing workflows
- **[Debug Guide](../../../docs/for-ai/testing/debug.md)** - Comprehensive debugging
- **[Instrumentation](../../../docs/for-ai/testing/instrumentation-how-it-works.md)** - Performance monitoring

---

## Performance Checklist

Before deploying your block:

- [ ] No JavaScript errors in console
- [ ] Load time < 100ms for simple blocks
- [ ] No layout shifts (CLS score < 0.1)
- [ ] Images lazy loaded (except hero images)
- [ ] Event delegation used for multiple items
- [ ] Proper error handling implemented
- [ ] Memory leaks checked and fixed
- [ ] Tested on slow network (3G)
- [ ] Tested on mobile devices
- [ ] Lighthouse performance score 90+

---

## Next Steps

1. Review your block for potential performance issues
2. Add proper error handling with try-catch
3. Implement FOUC prevention with CSS
4. Test performance with DevTools
5. Run Lighthouse audit
6. Fix any issues identified
7. Document performance characteristics

**Remember:** Fast, reliable blocks create better user experiences and improve your site's Core Web Vitals scores!
