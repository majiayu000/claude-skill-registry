---
name: alignment-verification
description: >
  Zero-tolerance alignment verification protocol. Alignment is binary -
  elements are either in line or they're not. Report exact measurements,
  no tolerances, no "close enough."
---

# Alignment Verification Skill

RULE: Alignment is BINARY. In line or not. Zero tolerances.

## Core Principle

Alignment verification has exactly two outcomes:

- **Delta = 0px** --> ALIGNED: YES
- **Delta > 0px** --> ALIGNED: NO (report exact deviation)

There are NO tolerances. A 2px deviation in a row of chips is visible. A 1px misalignment between form labels is noticeable. "Close enough" does not exist.

When you claim something is aligned, you MUST prove it with pixel measurements.

## Mental Model

Alignment is a RELATIONSHIP between elements, not a property of a single element.

Every alignment check requires:

1. **Target Element(s)** - What you are checking
2. **Reference Element** - What you are aligning TO (parent, sibling, baseline)
3. **Alignment Type** - How they should relate (center, edge, spacing)
4. **Container Space** - For alignment to work, there must be space to align within

Example mental model:
```
"Button should be horizontally centered in its parent"
- Target: the button
- Reference: the parent container
- Type: horizontal center
- Container: parent must be wider than button for centering to be meaningful
```

## Verification Protocol

### Step 1: Identify What Should Align

Before measuring, explicitly state:
- Which elements are being checked
- What type of alignment is expected
- What the reference point is

### Step 2: Extract Exact Pixel Values

Use Puppeteer's evaluate to get precise measurements:

```javascript
// Get element bounding box via puppeteer_evaluate
puppeteer_evaluate({
  script: `
    const el = document.querySelector('[selector]');
    const box = el.getBoundingClientRect();
    JSON.stringify({ x: box.x, y: box.y, width: box.width, height: box.height });
  `
})
// Returns: { x, y, width, height }
```

Extract ALL values needed for your alignment type.

### Step 3: Calculate Exact Deviations

Calculate with full precision. DO NOT round. DO NOT apply tolerances.

```javascript
// For horizontal centering in parent
const parentBox = await page.locator('[parent]').boundingBox();
const childBox = await page.locator('[child]').boundingBox();

const parentCenter = parentBox.x + (parentBox.width / 2);
const childCenter = childBox.x + (childBox.width / 2);
const deviation = Math.abs(parentCenter - childCenter);
// Report: deviation === 0 ? "ALIGNED: YES" : `ALIGNED: NO (${deviation}px off)`
```

### Step 4: Output ALIGNMENT_CHECK Block

Every alignment verification MUST produce this output:

```
ALIGNMENT_CHECK:
- Task: [alignment goal in plain language]
- Type: [horizontal_center|vertical_center|left_edge|right_edge|top_edge|bottom_edge|spacing]
- Elements measured:
  - [selector]: [value]px
  - [selector]: [value]px
- ALIGNED: YES/NO
- Max deviation: Xpx
- Deviations: [list if multiple elements]
```

## Alignment Types with Code

### Center Horizontally in Parent

```javascript
// Measure
const parent = await page.locator('.parent').boundingBox();
const child = await page.locator('.child').boundingBox();

// Calculate
const parentCenterX = parent.x + (parent.width / 2);
const childCenterX = child.x + (child.width / 2);
const deviation = Math.abs(parentCenterX - childCenterX);

// Report
console.log(`Parent center: ${parentCenterX}px`);
console.log(`Child center: ${childCenterX}px`);
console.log(`Deviation: ${deviation}px`);
console.log(`ALIGNED: ${deviation === 0 ? 'YES' : 'NO'}`);
```

### Center Vertically in Parent

```javascript
// Measure
const parent = await page.locator('.parent').boundingBox();
const child = await page.locator('.child').boundingBox();

// Calculate
const parentCenterY = parent.y + (parent.height / 2);
const childCenterY = child.y + (child.height / 2);
const deviation = Math.abs(parentCenterY - childCenterY);

// Report
console.log(`Parent center Y: ${parentCenterY}px`);
console.log(`Child center Y: ${childCenterY}px`);
console.log(`Deviation: ${deviation}px`);
console.log(`ALIGNED: ${deviation === 0 ? 'YES' : 'NO'}`);
```

### Left Edge Alignment (Multiple Elements)

```javascript
// Measure all elements
const elements = await page.locator('.item').all();
const leftEdges = [];

for (const el of elements) {
  const box = await el.boundingBox();
  leftEdges.push(box.x);
}

// Calculate deviations from first element
const reference = leftEdges[0];
const deviations = leftEdges.map((x, i) => ({
  index: i,
  value: x,
  deviation: Math.abs(x - reference)
}));

// Report
const maxDeviation = Math.max(...deviations.map(d => d.deviation));
console.log(`Reference left edge: ${reference}px`);
deviations.forEach(d => {
  console.log(`Element ${d.index}: ${d.value}px (deviation: ${d.deviation}px)`);
});
console.log(`Max deviation: ${maxDeviation}px`);
console.log(`ALIGNED: ${maxDeviation === 0 ? 'YES' : 'NO'}`);
```

### Right Edge Alignment

```javascript
// Measure
const elements = await page.locator('.item').all();
const rightEdges = [];

for (const el of elements) {
  const box = await el.boundingBox();
  rightEdges.push(box.x + box.width);
}

// Calculate deviations from first element
const reference = rightEdges[0];
const deviations = rightEdges.map((r, i) => ({
  index: i,
  value: r,
  deviation: Math.abs(r - reference)
}));

// Report
const maxDeviation = Math.max(...deviations.map(d => d.deviation));
console.log(`ALIGNED: ${maxDeviation === 0 ? 'YES' : 'NO'}`);
```

### Top Edge Alignment

```javascript
// Measure
const elements = await page.locator('.item').all();
const topEdges = [];

for (const el of elements) {
  const box = await el.boundingBox();
  topEdges.push(box.y);
}

// Calculate deviations from first element
const reference = topEdges[0];
const maxDeviation = Math.max(...topEdges.map(y => Math.abs(y - reference)));

// Report
console.log(`ALIGNED: ${maxDeviation === 0 ? 'YES' : 'NO'}`);
console.log(`Max deviation: ${maxDeviation}px`);
```

### Equal Spacing Between Elements

```javascript
// Measure
const elements = await page.locator('.item').all();
const boxes = [];

for (const el of elements) {
  boxes.push(await el.boundingBox());
}

// Calculate gaps between consecutive elements
const gaps = [];
for (let i = 1; i < boxes.length; i++) {
  const gap = boxes[i].x - (boxes[i-1].x + boxes[i-1].width);
  gaps.push(gap);
}

// Calculate deviations from first gap
const referenceGap = gaps[0];
const deviations = gaps.map((g, i) => ({
  index: i,
  value: g,
  deviation: Math.abs(g - referenceGap)
}));

// Report
const maxDeviation = Math.max(...deviations.map(d => d.deviation));
console.log(`Reference gap: ${referenceGap}px`);
deviations.forEach(d => {
  console.log(`Gap ${d.index}: ${d.value}px (deviation: ${d.deviation}px)`);
});
console.log(`ALIGNED: ${maxDeviation === 0 ? 'YES' : 'NO'}`);
```

## Common Pitfalls

### CSS: margin: auto needs flex/grid parent

```css
/* WRONG - margin auto alone does nothing in block layout */
.child {
  margin: 0 auto;
}

/* RIGHT - parent must be flex or block with defined width */
.parent {
  display: flex;
  justify-content: center;
}
/* OR */
.child {
  width: 200px;  /* must have explicit width */
  margin: 0 auto;
}
```

### SwiftUI: .center needs frame larger than content

```swift
// WRONG - no frame means content hugs, nothing to center within
Text("Hello")
  .frame(alignment: .center)

// RIGHT - explicit frame provides space to center within
Text("Hello")
  .frame(maxWidth: .infinity, alignment: .center)
```

### Transforms affect visual but not bounding box

getBoundingClientRect() returns the ORIGINAL position before CSS transforms. If you use `transform: translateX()` or similar, the visual position differs from the measured position.

```javascript
// Element visually at 100px but boundingBox shows 0px due to transform
// Solution: account for transforms or use offsetLeft/getBoundingClientRect
```

### Asymmetric content (icon in button)

A button with an icon on one side may APPEAR off-center even when the button IS centered, because the visual weight is asymmetric.

```
[ Icon  Text  ] <-- Button is centered but looks left-heavy

Solution: Either accept true center or adjust with padding to achieve
optical center (but document this explicitly).
```

## Anti-Patterns (FORBIDDEN Language)

The following phrases are REJECTED in alignment verification:

| Phrase | Why Rejected |
|--------|--------------|
| "within tolerance" | There is no tolerance. 0px or report deviation. |
| "close enough" | Not a measurement. What is the actual deviation? |
| "approximately aligned" | Approximate is not aligned. Give the number. |
| "looks aligned" | Visual assertion without ALIGNMENT_CHECK block. |
| "alignment seems fine" | "Seems" is not measurement. Prove it. |
| "roughly centered" | "Roughly" is not a pixel value. |

### How to Fix

WRONG:
```
"The chips look aligned to me."
```

RIGHT:
```
ALIGNMENT_CHECK:
- Task: Verify horizontal alignment of chip row
- Type: top_edge
- Elements measured:
  - chip[0]: y=142px
  - chip[1]: y=142px
  - chip[2]: y=142px
  - chip[3]: y=144px
- ALIGNED: NO
- Max deviation: 2px
- Deviations: chip[3] is 2px below reference
```

## Complete Verification Example

Task: "Center the modal horizontally in the viewport"

```javascript
// Step 1: Identify
// - Target: .modal
// - Reference: viewport
// - Type: horizontal_center

// Step 2: Measure
const viewport = await page.viewportSize();
const modal = await page.locator('.modal').boundingBox();

// Step 3: Calculate
const viewportCenterX = viewport.width / 2;
const modalCenterX = modal.x + (modal.width / 2);
const deviation = Math.abs(viewportCenterX - modalCenterX);

// Step 4: Output
console.log(`
ALIGNMENT_CHECK:
- Task: Center modal horizontally in viewport
- Type: horizontal_center
- Elements measured:
  - viewport center: ${viewportCenterX}px
  - modal center: ${modalCenterX}px
- ALIGNED: ${deviation === 0 ? 'YES' : 'NO'}
- Max deviation: ${deviation}px
`);
```

## Integration with Other Skills

- **debugging-first**: Use alignment verification AFTER confirming elements render
- **design-qa-skill**: Alignment checks are one component of full design QA
- **lovable-pitfalls**: Avoid premature "looks good" claims by measuring

## When to Apply This Skill

ALWAYS apply when:
- User says "center this"
- User says "align these"
- User says "make them line up"
- Reviewing spacing consistency
- Verifying layout implementation

SKIP when:
- No alignment requirements mentioned
- Working on non-visual code (APIs, logic)
- User explicitly says "don't worry about exact alignment"
