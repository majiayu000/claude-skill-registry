---
name: creating-bookmarklets
description: Creates browser-executable JavaScript bookmarklets with strict formatting requirements. Use when users mention bookmarklets, browser utilities, dragging code to bookmarks bar, or need JavaScript that runs when clicked in the browser toolbar.
metadata:
  version: 1.0.3
---

# Bookmarklet Creation

## Critical Requirements

### Comment Style - ABSOLUTE
**Use ONLY `/* */` comments. NEVER use `//` comments.**

Bookmark execution contexts fail with `//` style. Every comment must use block format.

```javascript
/* ✓ Correct */
const x = 5; /* inline */

/* ✗ Wrong - breaks bookmarklets */
// const x = 5;
const y = 10; // inline
```

### IIFE Wrapper
All bookmarklets must wrap in IIFE:

```javascript
(function() {
  /* bookmarklet code */
})();
```

### Protocol Prefix
All delivered bookmarklets must begin with `javascript:` protocol:

```javascript
javascript:(function() {
  /* bookmarklet code */
})();
```

This makes the code immediately usable without requiring manual modification during installation.

## Workflow

### 1. Generate Pretty-Printed Code

Create readable source with:
- 2-space indentation
- Descriptive variable names
- Block comments for key sections
- Logical organization
- **Prepend `javascript:` protocol to the code**

**This version with `javascript:` prefix gets stored in GitHub and shown to users, making it ready for installation without manual modification.**

### 2. Provide Installation

**Default approach - reference installer:**
```
Install: https://austegard.com/web-utilities/bookmarklet-installer.html
```

Installer handles:
- Minification with Terser
- URL encoding
- Draggable link generation
- GitHub repo integration

**Alternative - generate link programmatically:**
Use Terser.js to create installable link if requested:

```javascript
async function createBookmarkletLink(code, title) {
  const minified = await Terser.minify(code);
  const encoded = encodeURIComponent(minified.code).replace(/'/g, "%27");
  return `<a href="javascript:${encoded}">${title}</a>`;
}
```

Requires: `<script src="https://cdn.jsdelivr.net/npm/terser/dist/bundle.min.js"></script>`

### 3. Deliverables

Always provide:
1. Pretty-printed source code **with `javascript:` protocol prepended**
2. Installation method (installer link or generated link)
3. Brief description of functionality
4. Usage instructions

The code should be delivered in a format ready for direct use - users should be able to copy the entire code block (including `javascript:`) without modification.

## Code Standards

### Error Handling
```javascript
(function() {
  try {
    /* main logic */
  } catch (error) {
    console.error('Bookmarklet error:', error);
    alert('Operation failed: ' + error.message);
  }
})();
```

### Console Logging
Include debug traces by default:

```javascript
console.log('Bookmarklet: Starting');
/* operations */
console.log('Bookmarklet: Complete');
```

### User Feedback
```javascript
/* Success */
alert('✓ Content copied to clipboard');

/* Error */
alert('✗ Failed to access clipboard');
```

## Common Patterns

### DOM Manipulation
```javascript
(function() {
  const element = document.querySelector('.target');
  if (!element) {
    alert('Element not found');
    return;
  }
  /* manipulate element */
})();
```

### Data Extraction
```javascript
(function() {
  const data = Array.from(document.querySelectorAll('.item'))
    .map(item => ({
      title: item.querySelector('.title')?.textContent.trim(),
      value: item.querySelector('.value')?.textContent.trim()
    }));
  
  console.log('Extracted:', data);
})();
```

### Clipboard Operations
```javascript
(function() {
  const text = 'content to copy';
  navigator.clipboard.writeText(text)
    .then(() => alert('✓ Copied'))
    .catch(err => {
      console.error('Clipboard error:', err);
      alert('✗ Copy failed');
    });
})();
```

### Dynamic Library Loading
```javascript
(function() {
  if (typeof someLibrary === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.example.com/library.js';
    script.onload = function() {
      /* proceed with logic */
    };
    document.head.appendChild(script);
  }
})();
```

## Browser Compatibility

Provide fallbacks for unsupported features:

```javascript
if (!navigator.clipboard) {
  alert('Clipboard API not supported');
  return;
}
```

## Constraints

**Cannot use:**
- External files (CSS, images) without embedding
- Build tools or preprocessing
- `//` style comments

**Can use:**
- Fetch API
- localStorage/sessionStorage
- Modern browser APIs
- CDN libraries (loaded dynamically)

## Testing

Before delivering:
1. Verify no `//` comments exist
2. Test in browser console wrapped in IIFE
3. Check error handling with missing DOM elements
4. Verify user feedback for all paths

## Example Output

```
javascript:(function() {
  /* Pretty-printed bookmarklet code */
})();

Install: https://austegard.com/web-utilities/bookmarklet-installer.html

Extracts all links from current page and copies to clipboard as markdown list. Works on any webpage.
```

## GitHub Storage

User repository: https://github.com/oaustegard/bookmarklets

Pretty-printed format matches storage requirements. Installer loads directly from this repo.
