---
name: inheritance-debugging
description: Debug constructor inheritance issues where subclass properties are accessed
  before initialization.
---

# Skill: inheritance-debugging

## Scope
Debug constructor inheritance issues where subclass properties are accessed before initialization.

**Does:**
- Diagnose "undefined is not iterable" and NaN calculation errors
- Fix super() initialization order problems
- Add fallback defaults in render methods
- Verify fixes with incremental testing

**Does Not:**
- Cover general JavaScript debugging
- Handle non-inheritance related bugs

## Context

In jsgui3 controls, a common pattern is:
1. Base class constructor calls `compose()` or `render()`
2. Subclass constructor calls `super(spec)` then sets its own properties
3. **Problem**: Base class render runs BEFORE subclass properties exist

This manifests as:
- `undefined is not iterable` when destructuring `this._property`
- `NaN` calculations using undefined numeric properties
- Missing SVG attributes (x, width, height)
- Silent failures with empty renders

## Procedure

### 1. Identify the Pattern
Look for this constructor structure:

```javascript
class Child extends Parent {
    constructor(spec) {
        super(spec);  // ← Parent calls render() here

        this._my_property = spec.value || 'default';  // ← Too late!
    }
}
```

### 2. Run Isolated Tests
Create a debug script to test with `abstract: true`:

```javascript
const control = new MyControl({
    context,
    abstract: true,  // Skips compose/render
    ...options
});

console.log('Properties:', control._my_property);
```

If it works with `abstract: true` but fails without, this confirms the timing issue.

### 3. Add Fallback Defaults in Methods
In every method that uses subclass properties, add defaults:

```javascript
// Before (breaks during super())
render() {
    const [min, max] = this._range;  // undefined error
    const gap = this._gap;  // NaN
}

// After (safe)
render() {
    const range = this._range || [-10, 10];  // Fallback
    const [min, max] = range;
    const gap = this._gap !== undefined ? this._gap : 0.1;
}
```

### 4. Add Re-render After Properties Set
In the subclass constructor, re-render after setting properties:

```javascript
constructor(spec) {
    super(spec);  // Renders with defaults

    this._my_property = spec.value || 'default';

    // Re-render now that properties are set
    if (!spec.abstract && !spec.el && this._svg) {
        this.render_chart();
    }
}
```

### 5. Verify with Browser Subagent
Use browser testing to visually confirm the fix:

```
1. Start demo server
2. Navigate to demo page
3. Inspect rendered elements for correct attributes
4. Check console for errors
5. Screenshot for documentation
```

### 6. Run Unit Tests
Ensure all tests pass after the fix:

```bash
npx mocha test/controls/<control>.test.js --reporter min
```

## Real Example: Bar_Chart Fix

**Problem**: Bar rects had `y` and `height` but missing `x` and `width`.

**Root Cause**: `super(spec)` called `compose_chart()` → `render_chart()` → `render_bars()`, which used `this._bar_gap` before it was set.

**Fix**: Added fallback in `render_bars()`:
```javascript
const bar_gap = this._bar_gap !== undefined ? this._bar_gap : 0.1;
const group_gap = this._group_gap !== undefined ? this._group_gap : 0.2;
```

**Result**: 35 chart tests passing, bars render correctly.

## Validation Checklist
- [ ] Identified properties accessed before initialization
- [ ] Added fallback defaults to all affected methods
- [ ] Added re-render call after subclass properties set
- [ ] Debug script with `abstract: true` works
- [ ] Debug script without `abstract: true` works
- [ ] Unit tests pass
- [ ] Browser visual verification passed

## References
- [Chart_Base.js](file:///c:/Users/james/Documents/repos/jsgui3-html/controls/charts/Chart_Base.js) - Example of base class
- [Bar_Chart.js](file:///c:/Users/james/Documents/repos/jsgui3-html/controls/charts/Bar_Chart.js) - Fixed subclass example
- [Function_Graph.js](file:///c:/Users/james/Documents/repos/jsgui3-html/controls/charts/Function_Graph.js) - Another fixed example
