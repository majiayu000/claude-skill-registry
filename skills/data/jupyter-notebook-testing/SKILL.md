---
name: jupyter-notebook-testing
description: Create and manage Jupyter notebooks for testing Adobe Edge Delivery Services (EDS) blocks interactively in the browser using the ipynb-viewer block. Interactive JavaScript execution, overlay previews with backdrop, direct ES6 imports. Use when creating notebooks, testing blocks with ipynb files in browser, generating overlay previews, or creating executable documentation.
---

# Jupyter Notebook Testing for EDS Blocks

Interactive testing environment for EDS blocks using Jupyter notebooks **in the browser** via the ipynb-viewer block.

## When to Use This Skill

Use this skill when:
- Creating new Jupyter notebooks (`.ipynb` files) for EDS block testing
- Using direct imports for helper functions (`testBlock`, `showPreview`)
- Testing blocks in browser environment with ipynb-viewer block
- Generating overlay previews with `showPreview()`
- Debugging blocks with different content structures
- Creating executable documentation for blocks
- Working with minimal DOM structure requirements
- Troubleshooting preview styling or decoration issues

## Overview

Test EDS blocks rapidly with Jupyter notebooks using **browser execution**:

- **Browser execution only**: Notebooks run via ipynb-viewer block on your EDS site
- **Direct imports**: Each cell imports what it needs independently
- **Helper functions**: `testBlock` and `showPreview` via ES6 imports
- **Overlay previews**: Full-screen overlays with backdrop (no popup blockers)
- **Minimal DOM**: Critical EDS-compatible structure (block decoration)

### Key Benefits

- **Browser-native**: Uses native browser APIs directly
- **No build steps**: Test blocks immediately without compilation
- **Visual previews**: Overlay with full styling (no popup blockers)
- **No initialization**: Each cell imports what it needs
- **EDS-compatible**: Follows EDS block decoration patterns
- **Executable docs**: Share interactive notebooks with end users

### Technology Stack

- **ipynb-viewer**: EDS block for executing notebooks in browser
- **Browser native APIs**: Direct DOM manipulation
- **scripts/ipynb-helpers.js**: External helper module with browser functions

## Quick Start

### 1. Create or Open Notebook

**Option A: Copy existing template**
```bash
cp test.ipynb my-block-tests.ipynb
# View on EDS site using ipynb-viewer block
```

**Option B: Create from scratch**
- Create new `.ipynb` file
- Copy the first code cell from `test.ipynb`
- Add to EDS page via ipynb-viewer block

### 2. View Notebook on EDS Site

Add ipynb-viewer block to your page:

```
| IPynb Viewer |
|--------------|
| /test.ipynb |
```

### 3. Test Your Block

**Simple pattern - import what you need:**

```javascript
// Any cell: Test a block
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', `
  <div>
    <div>Question 1</div>
    <div>Answer 1</div>
  </div>
`);
console.log('✓ Block created');
return block.outerHTML;
```

**Note:** Just write your code naturally with `await` and `return` - it runs in async context.

### 4. Generate Visual Preview

**Opens overlay:**

```javascript
// Any cell: Visual preview in overlay
const { showPreview } = await import('/scripts/ipynb-helpers.js');
const content = `
  <div>
    <div>Question 1</div>
    <div>Answer 1</div>
  </div>
`;

// Opens overlay with backdrop
await showPreview('accordion', content);

return '✓ Preview overlay opened';
```

## Browser Execution

### Purpose

End-user interaction and presentations with executable notebooks.

### Features

- Native browser APIs
- Direct JavaScript execution
- Console output display
- Overlay previews (no popup blockers)
- Interactive block decoration
- No file system access

### When to Use

- Sharing executable demos
- Interactive tutorials
- Client presentations
- Live coding examples
- Block testing and experimentation

## Helper Functions

All helper functions are in **scripts/ipynb-helpers.js**, imported in each cell as needed.

### Available Helper Functions

Import what you need in each cell:

| Function | Purpose | Behavior |
|----------|---------|----------|
| `testBlock()` | Test block decoration | Uses native browser DOM |
| `showPreview()` | Visual preview | Opens overlay with backdrop |

**Usage Pattern:**

```javascript
// Import what you need in each cell
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

// Use the functions
const block = await testBlock('accordion', '<div>content</div>');
await showPreview('accordion', '<div>content</div>');

// Use document directly
const div = document.createElement('div');

return block.outerHTML; // Return value to display in output
```

## Overlay Preview System

Live previews use full-screen overlays - no popup blockers!

### How It Works

1. **Creates overlay**: Full-screen overlay with semi-transparent backdrop
2. **Responsive preview buttons**: Switch between Mobile (375×667), Tablet (768×1024), and Desktop (95%×95vh) views
3. **Minimal DOM** (EDS-compatible): Block decorated properly with CSS/JS
4. **Auto-decoration**: Dynamically imports and executes block JavaScript

### Key Benefits

✅ No popup blockers | ✅ Responsive testing | ✅ Better UX (stays on page) | ✅ Clean DOM | ✅ EDS-compatible | ✅ Full styling

### Responsive Preview Controls

Test blocks across different device sizes with one click:

- **📱 Mobile** (375px × 667px) - iPhone SE/8 size
- **📱 Tablet** (768px × 1024px) - iPad size
- **🖥️ Desktop** (95% × 95vh) - Full desktop view (default)

Switch between views interactively with smooth transitions to test block responsiveness!

## DOM Structure Requirements

### Minimal Structure

Block is decorated properly within overlay content area:

```html
<div class="ipynb-preview-content">
  <div class="blockname block"><!-- content rows --></div>
</div>
```

### Why This Matters

EDS blocks iterate over `block.children` directly. The overlay system ensures proper structure for decoration.

**Benefits:** No wrapper interference | Proper block decoration | Full CSS/JS support

## Troubleshooting

### Preview Shows Unstyled Content

**Cause:** CSS not loading or block decoration failed. **Check DevTools Console + Network tab** for 404s and errors. **Fix:** Verify block CSS exists.

### Overlay Not Appearing

**Symptom:** `showPreview()` runs but no overlay appears. **Cause:** JavaScript error during execution. **Fix:** Check browser console for errors.

### Import Errors

**Symptom:** Cells fail with import errors. **Cause:** Incorrect import path. **Fix:** Use absolute path `/scripts/ipynb-helpers.js`

## When to Use Notebooks

**✅ Use For:** Quick validation, content experimentation, debugging, prototyping, executable documentation, `showPreview()` testing, interactive demos

**❌ Don't Use For:** Complex interactions requiring Node.js, file system operations, automated testing, CI/CD pipelines

## Best Practices

1. **Import what you need**: Each cell imports helper functions independently
2. **Write async code naturally**: Use `await` directly - cells run in async context
3. **Return values**: Use `return` to display results in output cell
4. **Use direct imports**: `const { testBlock, showPreview } = await import(...)`
5. **Test visual output**: Always use `showPreview()` for verification
6. **No initialization required**: Run any cell at any time
7. **Structure notebooks**: Clear, focused cells with markdown documentation

## Integration with ipynb-viewer Block

The **ipynb-viewer** EDS block executes notebooks in browser:

```
| IPynb Viewer |
|--------------|
| /path/to/notebook.ipynb |
```

**Features:** Interactive execution (async/await support), console capture, markdown rendering (tables, code blocks, lists), error handling

**Key Points:** No initialization required | Each cell imports independently | Browser uses native APIs | Helper functions via ES6 imports

## Reference Files

For detailed information, see:

- **[EXAMPLES.md](EXAMPLES.md)** - Content structure patterns and complete examples
- **[ADVANCED_TECHNIQUES.md](ADVANCED_TECHNIQUES.md)** - Performance testing, batch testing, validation
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions for popup issues, styling issues

## Related Documentation

- **[docs/for-ai/explaining-jupyter.md](../../docs/for-ai/explaining-jupyter.md)** - Comprehensive Jupyter notebook documentation
- **[blocks/ipynb-viewer/README.md](../../blocks/ipynb-viewer/README.md)** - ipynb-viewer block documentation
- **[scripts/ipynb-helpers.js](../../scripts/ipynb-helpers.js)** - Helper functions implementation
- **[test.ipynb](../../test.ipynb)** - Reference notebook with examples

## Summary

Jupyter notebooks with browser execution provide an interactive testing environment for EDS blocks that:

- **Browser-native execution**: Direct browser APIs, no Node.js complexity
- **No initialization required**: Each cell imports what it needs
- **Helper functions**: `testBlock`, `showPreview` via direct imports
- **Overlay previews**: Visual feedback (no popup blockers)
- **Minimal DOM structure**: EDS-compatible block decoration
- **ipynb-viewer integration**: End-user executable notebooks
- **Instant feedback**: No server or build overhead
- **Shareable**: Create interactive demos and documentation

Use this skill whenever you need to rapidly test, debug, or document EDS blocks in the browser without the ceremony of traditional development environments.

---

**Skill Status**: ✅ Complete - Browser-only execution
**Line Count**: < 500 lines
**Progressive Disclosure**: Detailed content in reference files
