---
name: browser-debugging
description: Debug client-side issues using browser developer tools. Identify JavaScript errors, styling issues, and performance problems in the browser.
---

# Browser Debugging

## Overview

Browser debugging tools help identify and fix client-side issues including JavaScript errors, layout problems, and performance issues.

## When to Use

- JavaScript errors
- Layout/styling issues
- Performance problems
- User interaction issues
- Network request failures
- Animation glitches

## Instructions

### 1. **Browser DevTools Fundamentals**

```yaml
Chrome DevTools Tabs:

Elements/Inspector:
  - Inspect HTML structure
  - Edit HTML/CSS in real-time
  - View computed styles
  - Check accessibility tree
  - Modify DOM

Console:
  - View JavaScript errors
  - Execute JavaScript
  - View console logs
  - Monitor messages
  - Clear errors

Sources/Debugger:
  - Set breakpoints
  - Step through code
  - Watch variables
  - Call stack view
  - Conditional breakpoints

Network:
  - View all requests
  - Check response status
  - Inspect headers
  - View response body
  - Throttle network

Performance:
  - Record runtime
  - Identify bottlenecks
  - Flame charts
  - Memory usage
  - Frame rate

Memory:
  - Heap snapshots
  - Memory growth
  - Object allocation
  - Detect leaks

---

Essential Shortcuts:

F12 / Ctrl+Shift+I: Open DevTools
Ctrl+Shift+C: Element inspector
Ctrl+Shift+J: Console
Ctrl+Shift+K: Console (Firefox)
```

### 2. **Debugging Techniques**

```javascript
// Breakpoints

// Line breakpoint
// Click line number in Sources tab

// Conditional breakpoint
// Right-click line → Add conditional breakpoint
if (userId === 123) {
  // Pauses only when userId is 123
}

// DOM breakpoint
// Right-click element → Break on → subtree modifications
// Pauses when DOM changes

// Event listener breakpoint
// Sources tab → Event Listener Breakpoints
// Pauses on specific event

// Debugger statement
function problematicFunction() {
  debugger;  // Pauses here if DevTools open
  // ... rest of code
}

---

Watch Expressions

// Add variable to watch
// Updates as code executes
watch: {
  userId: 123,
  orders: [],
  total: 0
}

Call Stack
// Shows function call chain
main()
  -> processUser()
    -> validateUser()
      -> PAUSED HERE

Step Controls:
  Step over: Execute current line
  Step into: Enter function
  Step out: Exit function
  Continue: Run to next breakpoint
```

### 3. **Common Issues & Solutions**

```yaml
Issue: JavaScript Error in Console

Error Message: "Uncaught TypeError: Cannot read property 'map' of undefined"

Solution Steps:
  1. Note line number from error
  2. Click line to go to Sources tab
  3. Set breakpoint before error
  4. Check variable values
  5. Trace how undefined value occurred

Example:
  const data = await fetchData();
  const items = data.results.map(x => x.name);
  // Error if results is undefined
  // Add check: const items = data?.results?.map(...)

---

Issue: Element Not Showing (Hidden)

Debug:
  1. Right-click element → Inspect
  2. Check display: none in CSS
  3. Check visibility: hidden
  4. Check opacity: 0
  5. Check position off-screen
  6. Check z-index buried
  7. Check parent hidden

---

Issue: CSS Not Applying

Debug:
  1. Inspect element
  2. View Styles panel
  3. Find CSS rule
  4. Check if crossed out (overridden)
  5. Check specificity
  6. Check media queries
  7. Check !important usage

---

Issue: Memory Leak

Detect:
  1. Memory tab
  2. Take heap snapshot
  3. Perform action
  4. Take another snapshot
  5. Compare (delta)
  6. Objects retained? (leaked)
  7. Check detached DOM nodes

Fix:
  - Remove event listeners
  - Clear timers
  - Release object references
  - Cleanup subscriptions
```

### 4. **Performance Debugging**

```yaml
Network Performance:

1. Open Network tab
2. Reload page
3. Identify slow resources:
   - Large images (>500KB)
   - Large JavaScript (>300KB)
   - Slow requests (>2s)
   - Waterfall bottlenecks

Solutions:
  - Optimize images
  - Code split JavaScript
  - Lazy load resources
  - Compress assets
  - Use CDN

Runtime Performance:

1. Performance tab
2. Record interaction
3. Analyze flame chart:
   - Long red bars = slow
   - Identify functions
   - Check main thread blocking
   - Monitor frame rate

Solutions:
  - Move work to Web Workers
  - Defer non-critical work
  - Optimize algorithms
  - Use requestAnimationFrame

---

Checklist:

Console:
  [ ] No errors
  [ ] No warnings (expected ones)
  [ ] No unhandled promise rejections

Elements:
  [ ] HTML structure correct
  [ ] CSS applied correctly
  [ ] No accessibility issues
  [ ] Responsive at all breakpoints

Network:
  [ ] All resources load successfully
  [ ] No excessive requests
  [ ] File sizes reasonable
  [ ] No blocked resources

Performance:
  [ ] Frame rate >60 FPS
  [ ] No long tasks (>50ms)
  [ ] LCP <2.5s
  [ ] Memory stable
```

## Key Points

- Open DevTools with F12
- Console tab shows JavaScript errors first
- Sources tab for setting breakpoints
- Inspector for HTML/CSS inspection
- Network tab for request analysis
- Performance tab for profiling
- Memory tab for leak detection
- Use conditional breakpoints for debugging
- Monitor console for warnings/errors
- Test on real devices/networks
