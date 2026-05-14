# PPTX Slide Patterns

Slide pattern examples using the bundled TypeScript helper modules. All measurements in inches for 16:9 widescreen (10" x 5.625").

## Quick Import

```typescript
import pptxgen from 'pptxgenjs';
import * as h from '${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts';
```

## Common Dimensions

| Element | Position | Notes |
|---------|----------|-------|
| Safe margin | 0.5" from all edges | Minimum clearance |
| Content area | x:0.5, y:0.5, w:9, h:4.625 | Full usable space |
| Title area | x:0.5, y:0.3, w:9, h:0.8 | Standard heading position |
| Body area | x:0.5, y:1.3, w:9, h:3.8 | Below title |

## Title Slide

```typescript
const slide = pptx.addSlide();
slide.background = { color: '0a0a0a' };

// Main title
slide.addText(title, {
  x: 0.5, y: 1.2, w: 9, h: 1.8,
  fontSize: 44, fontFace: 'Clash Display',
  color: 'ffffff', bold: true, align: 'center',
  lineSpacing: 52
});

// Subtitle
slide.addText(subtitle, {
  x: 1.5, y: 3.2, w: 7, h: 0.8,
  fontSize: 22, fontFace: 'IBM Plex Sans',
  color: '999999', align: 'center'
});

// Speaker / event info
slide.addText(`${speaker} — ${event} — ${date}`, {
  x: 1, y: 4.5, w: 8, h: 0.5,
  fontSize: 14, fontFace: 'IBM Plex Sans',
  color: '666666', align: 'center'
});
```

## Content Slide with Bullets

```typescript
const slide = pptx.addSlide();

// Heading
slide.addText(heading, {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 32, fontFace: 'Clash Display',
  color: 'ffffff', bold: true
});

// Accent line under heading
slide.addShape(pptx.shapes.LINE, {
  x: 0.5, y: 1.05, w: 2, h: 0,
  line: { color: '4a9eff', width: 3 }
});

// Bullet list
const bulletItems = items.map(item => ({
  text: item,
  options: {
    fontSize: 20, fontFace: 'IBM Plex Sans',
    color: 'e0e0e0', bullet: { code: '2022' },
    breakLine: true, paraSpaceAfter: 8
  }
}));

slide.addText(bulletItems, {
  x: 0.7, y: 1.3, w: 8.5, h: 3.8,
  valign: 'top', lineSpacing: 28
});
```

## Two-Column: Image + Text

```typescript
const slide = pptx.addSlide();

// Heading (full width)
slide.addText('About Us', {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true
});

// Left column: text content
slide.addText('We build tools that empower developers to create amazing experiences effortlessly.', {
  x: 0.5, y: 1.3, w: 4.2, h: 3.8,
  fontSize: 18, fontFace: 'IBM Plex Sans',
  color: 'e0e0e0', valign: 'top', lineSpacing: 26
});

// Right column: image with helper sizing
const sizing = h.imageSizingContain('team.jpg', 5.2, 1.2, 4.3, 4.0);
slide.addImage({
  path: 'team.jpg',
  ...sizing,
  rounding: true
});
```

## Card Row

```typescript
const slide = pptx.addSlide();

// Heading
slide.addText('Team Members', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true, align: 'center'
});

// Use helper to create row of image-text cards
h.addCardRow(slide, [
  {
    image: { path: 'person1.jpg', boxHeight: 2.0 },
    text: 'Alice\nCo-founder'
  },
  {
    image: { path: 'person2.jpg', boxHeight: 2.0 },
    text: 'Bob\nCo-founder'
  },
  {
    image: { path: 'person3.jpg', boxHeight: 2.0 },
    text: 'Carol\nEngineer'
  }
], {
  x: 0.5, y: 1.2, w: 9, h: 3.8
});
```

## Quote Slide

```typescript
const slide = pptx.addSlide();
slide.background = { color: '4a9eff' };

// Quote mark
slide.addText('"', {
  x: 0.5, y: 0.5, w: 1, h: 1,
  fontSize: 80, fontFace: 'Georgia',
  color: 'ffffff', bold: true
});

// Quote text
slide.addText(quote, {
  x: 1.5, y: 1.2, w: 7, h: 2.5,
  fontSize: 24, fontFace: 'IBM Plex Sans',
  color: 'ffffff', italic: true,
  lineSpacing: 36, valign: 'middle'
});

// Attribution
slide.addText(`— ${author}, ${role}`, {
  x: 1.5, y: 4.0, w: 7, h: 0.5,
  fontSize: 16, fontFace: 'IBM Plex Sans',
  color: 'e0e0ff'
});
```

## Timeline

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add heading
slide.addText('Our Journey', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true
});

// Use helper to create timeline
h.addTimeline(slide, {
  x: 0.5, y: 1.5, w: 9, h: 2.5,
  theme,
  milestones: [
    { label: '2020', description: 'Founded' },
    { label: '2021', description: 'Series A' },
    { label: '2022', description: 'IPO' },
    { label: '2023', description: '1M users' },
    { label: '2024', description: 'Global expansion' }
  ]
});
```

## Feature Grid (3x2)

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add heading
slide.addText('Our Features', {
  x: 0.5, y: 0.2, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true, align: 'center'
});

// Use helper to create grid layout
h.addFeatureGrid(slide, {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  cols: 3, rows: 2,
  theme,
  features: [
    { title: 'Fast', description: 'Lightning quick performance' },
    { title: 'Reliable', description: 'Battle-tested in production' },
    { title: 'Simple', description: 'Easy to understand and use' },
    { title: 'Secure', description: 'Enterprise-grade security' },
    { title: 'Scalable', description: 'Grows with your needs' },
    { title: 'Open', description: 'Community-driven development' }
  ]
});
```

## Code Slide

```typescript
const slide = pptx.addSlide();

slide.addText('Implementation', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true
});

// Code block background
slide.addShape('roundRect', {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  fill: { color: '1e1e2e' },
  rectRadius: 0.1
});

// Use helper to syntax-highlight code
const codeRuns = h.codeToRuns('const x = value * 2;\nreturn x;', 'javascript');

// Code text with syntax highlighting
slide.addText(codeRuns, {
  x: 0.7, y: 1.4, w: 8.6, h: 3.4,
  valign: 'top', lineSpacing: 20, paraSpaceAfter: 0
});
```

## Section Divider

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Use helper to create full-slide section divider
h.addSectionDivider(slide, 'Part III: Implementation', theme);

// Optionally add a progress indicator
h.addProgressBar(slide, 3, 5, theme, { position: 'bottom', height: 0.04 });
```

## Comparison Table

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add heading
slide.addText('Comparison', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true, align: 'center'
});

// Use helper to create side-by-side comparison
h.addComparisonTable(slide, {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  theme,
  columns: [
    {
      title: 'Platform A',
      items: ['Fast', 'Reliable', 'Limited scaling']
    },
    {
      title: 'Platform B',
      items: ['Very fast', 'Redundant', 'Enterprise ready']
    },
    {
      title: 'Ours',
      items: ['Lightning', 'Bulletproof', 'Infinite scale']
    }
  ]
});
```

## Hierarchical Tree

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add heading
slide.addText('Organization Structure', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true
});

// Use helper to create three-level tree
h.addThreeLevelTree(slide, {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  theme,
  root: {
    title: 'Engineering',
    children: [
      { title: 'Backend', children: [{ title: 'API' }, { title: 'Data' }] },
      { title: 'Frontend', children: [{ title: 'Web' }, { title: 'Mobile' }] },
      { title: 'DevOps', children: [{ title: 'Infra' }, { title: 'Security' }] }
    ]
  }
});
```

## Metric Highlight

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add heading
slide.addText('Key Metrics', {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: 'Clash Display',
  color: 'ffffff', bold: true, align: 'center'
});

// Use helper to create metrics row
h.addMetricsRow(slide, {
  x: 0.5, y: 1.5, w: 9, h: 2.0,
  theme,
  metrics: [
    { value: '312%', label: 'Growth', unit: 'YoY' },
    { value: '50M+', label: 'Users', unit: 'Active' },
    { value: '99.9%', label: 'Uptime', unit: 'SLA' }
  ]
});
```

---

## Decorative Elements

### Staircase Accent

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add content
slide.addText('Beautiful Slides', {
  x: 0.5, y: 0.5, w: 9, h: 1.5,
  fontSize: 48, fontFace: 'Clash Display', color: 'ffffff', bold: true
});

// Add decorative staircase in corner
h.addStaircase(slide, {
  position: 'bottom-right',
  color: theme.accent,
  steps: 5,
  opacity: 0.2
});

// Add slide number with progress
h.addSlideNumber(slide, 5, 25, theme);
```

### Section Badge

```typescript
const slide = pptx.addSlide();
const theme = h.createTheme();

// Add badge at top
h.addSectionBadge(slide, 'NEW SECTION', { x: 0.5, y: 0.3 }, theme);

// Add slide content below
slide.addText('Introduction to Advanced Topics', {
  x: 0.5, y: 1.2, w: 9, h: 2,
  fontSize: 36, fontFace: 'Clash Display', color: 'ffffff'
});
```

---

## Layout Utilities

### Element Alignment

```typescript
const slide = pptx.addSlide();

// Add three elements at different positions
slide.addShape('rect', { x: 1, y: 1, w: 1, h: 1, fill: { color: '4a9eff' } });
slide.addShape('rect', { x: 3, y: 2.5, w: 1, h: 1, fill: { color: '4a9eff' } });
slide.addShape('rect', { x: 5, y: 1.5, w: 1, h: 1, fill: { color: '4a9eff' } });

// Align all to the same vertical center
h.alignSlideElements(slide, [0, 1, 2], 'verticallyCenter');

// Or align horizontally
h.alignSlideElements(slide, [0, 1, 2], 'horizontallyCenter');
```

### Element Distribution

```typescript
const slide = pptx.addSlide();

// Add elements at arbitrary positions
for (let i = 0; i < 4; i++) {
  slide.addShape('rect', {
    x: Math.random() * 8,
    y: Math.random() * 4,
    w: 1, h: 1,
    fill: { color: '4a9eff' }
  });
}

// Distribute elements evenly horizontally
h.distributeSlideElements(slide, [0, 1, 2, 3], 'horizontal');
```

### Validation & Diagnostics

```typescript
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();
// ... build slides ...

// Validate entire deck for issues
const report = h.validateDeck(pptx);

if (report.issues.length > 0) {
  console.error('Critical issues found:');
  report.issues.forEach(issue => {
    console.error(`  - ${issue.message}`);
  });
}

if (report.warnings.length > 0) {
  console.warn('Warnings:');
  report.warnings.forEach(warning => {
    console.warn(`  - ${warning.message}`);
  });
}

// Check individual slide for overlaps
const slide = pptx._slides[0];
h.warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true });
h.warnIfSlideElementsOutOfBounds(slide, pptx);

// Get slide dimensions for layout calculations
const { width, height } = h.getSlideDimensions(slide, pptx);
console.log(`Slide dimensions: ${width}" x ${height}"`);
```
