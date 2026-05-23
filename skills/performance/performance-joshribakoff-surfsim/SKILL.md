---
name: performance
description: Apply performance optimization patterns for game loop, rendering, and state updates. Use when discussing frame rate, optimization, profiling, or when editing core game loop code. Auto-apply when user mentions "slow", "fps", "lag", or "performance".
---

# Performance Optimization Skill

This is a real-time game requiring 60fps. Apply these patterns for performance-critical code.

## Performance Budget

| Operation | Budget | Notes |
|-----------|--------|-------|
| Full frame | 16ms | 60fps target |
| Physics update | 2-4ms | Wave simulation |
| Rendering | 8-10ms | Canvas draw calls |
| UI updates | 2-3ms | React reconciliation |
| Overhead | 2ms | GC, browser, etc. |

## Game Loop Patterns

### RequestAnimationFrame
```javascript
function gameLoop(timestamp) {
  const deltaTime = timestamp - lastTimestamp;
  lastTimestamp = timestamp;

  update(deltaTime);
  render();

  requestAnimationFrame(gameLoop);
}
```

### Fixed Time Step (for physics)
```javascript
const PHYSICS_STEP = 1000 / 60; // 16.67ms
let accumulator = 0;

function update(deltaTime) {
  accumulator += deltaTime;
  while (accumulator >= PHYSICS_STEP) {
    physicsUpdate(PHYSICS_STEP);
    accumulator -= PHYSICS_STEP;
  }
}
```

## Memory Optimization

### Object Pooling
```javascript
// Pre-allocate reusable objects
const foamRowPool = [];
function getFoamRow() {
  return foamRowPool.pop() || createFoamRow();
}
function releaseFoamRow(row) {
  foamRowPool.push(row);
}
```

### Typed Arrays
```javascript
// Use for numeric data
const grid = new Float32Array(width * height);
const indices = new Uint16Array(count);
```

### Avoid Allocation in Hot Paths
```javascript
// Bad - creates new object every frame
function update() {
  const vec = { x: 0, y: 0 };
}

// Good - reuse scratch objects
const scratchVec = { x: 0, y: 0 };
function update() {
  scratchVec.x = 0;
  scratchVec.y = 0;
}
```

## Canvas Rendering Optimization

### Batch Draw Calls
```javascript
// Bad - many small paths
for (const segment of segments) {
  ctx.beginPath();
  ctx.moveTo(segment.x1, segment.y1);
  ctx.lineTo(segment.x2, segment.y2);
  ctx.stroke();
}

// Good - single path
ctx.beginPath();
for (const segment of segments) {
  ctx.moveTo(segment.x1, segment.y1);
  ctx.lineTo(segment.x2, segment.y2);
}
ctx.stroke();
```

### Layer Canvases
```javascript
// Static background on separate canvas
const bgCanvas = document.createElement('canvas');
// Only redraw when needed, composite over game canvas
```

### Avoid State Changes
```javascript
// Bad - changes style every iteration
for (const item of items) {
  ctx.fillStyle = item.color;
  ctx.fillRect(item.x, item.y, item.w, item.h);
}

// Good - group by style
const byColor = groupBy(items, 'color');
for (const [color, items] of byColor) {
  ctx.fillStyle = color;
  for (const item of items) {
    ctx.fillRect(item.x, item.y, item.w, item.h);
  }
}
```

## Profiling

### Browser DevTools
- Performance tab: flame chart, frame timing
- Memory tab: heap snapshots, allocation timeline

### In-Code Timing
```javascript
const start = performance.now();
expensiveOperation();
console.log(`Operation: ${performance.now() - start}ms`);
```

### Performance Tests
```javascript
// src/render/foamRendering.perf.test.js
it('renders under 16ms budget', () => {
  const start = performance.now();
  renderFoam(testData);
  expect(performance.now() - start).toBeLessThan(16);
});
```

## Common Pitfalls

1. **GC Pressure**: Creating objects in game loop
2. **Layout Thrashing**: Reading/writing DOM in alternation
3. **Unthrottled Events**: Mouse/touch events firing faster than frames
4. **Unnecessary Work**: Recalculating unchanged values

## Reference Plans

- `plans/tooling/128-react-performance-optimization.md`
- `plans/bugfixes/130-bathymetry-heatmap-performance.md`
- `plans/perf-test-separation.md`
