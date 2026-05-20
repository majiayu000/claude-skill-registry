---
name: data-viz-2025
description: State-of-the-art data visualization for React/Next.js/TypeScript with Tailwind CSS. Creates compelling, tested, and accessible visualizations following Tufte principles and NYT Graphics standards. Activate on "data viz", "chart", "graph", "visualization", "dashboard", "plot", "Recharts", "Nivo", "D3". NOT for static images, print graphics, or basic HTML tables.
allowed-tools: Read,Write,Edit,Bash
---

# Data Visualization 2025: The Art & Science of Visual Communication

Create visualizations that Seaborn users, Tufte readers, and everyone else will love. Marry NYT Graphics rigor with MoMA aesthetics, Nike energy, and On Kawara precision.

## When to Use This Skill

✅ **Use for:**
- Building interactive charts, dashboards, and data stories
- Complex visualizations (chord diagrams, Sankey flows, network graphs)
- Real-time data displays with animations
- Mobile-responsive data components
- Accessible, tested visualizations for production

❌ **NOT for:**
- Static PNG/SVG exports without interaction (use design tools)
- Basic HTML tables (use semantic markup)
- Print-only graphics (different constraints)
- Simple icon displays (use icon libraries)

## Core Philosophy: The Three Pillars

### 1. **Clarity** (Tufte's Data-Ink Ratio)
Every visual element must earn its place. Remove chart junk, maximize signal-to-noise.

### 2. **Beauty** (Aesthetic Standards)
Visualizations are art. Use spring physics, thoughtful color, and premium design systems.

### 3. **Truth** (Graphical Integrity)
Data representation must be honest. Test rigorously, document assumptions, preserve context.

## Quick Decision Tree

```
What are you building?
├─ Exploratory analysis / many iterations
│  └─ → Observable Plot (grammar-of-graphics)
│
├─ Standard business charts (bars, lines, pies)
│  ├─ Simple React integration needed
│  │  └─ → Recharts (easiest, most popular)
│  └─ Premium aesthetics + theming
│     └─ → Nivo (beautiful out of the box)
│
├─ Custom, one-of-a-kind visualizations
│  ├─ Need low-level control
│  │  └─ → Visx (React + D3 primitives)
│  └─ Full D3 power
│     └─ → D3.js directly (steeper learning curve)
│
└─ Dashboard with Tailwind design system
   ├─ → Tremor (purpose-built for dashboards)
   └─ → shadcn-ui Charts (Recharts + shadcn styling)
```

## The Data Viz Stack (2025)

### Recommended Packages

```json
{
  "dependencies": {
    "@observablehq/plot": "^0.6.0",        // Exploratory, grammar-of-graphics
    "recharts": "^2.12.0",                  // React charts, simple & popular
    "@nivo/core": "^0.87.0",                // Beautiful, themeable charts
    "@visx/visx": "^3.10.0",                // Low-level D3 + React primitives
    "d3": "^7.9.0",                         // Direct D3 for custom work
    "@tremor/react": "^3.15.0",             // Tailwind dashboard components
    "framer-motion": "^11.0.0"              // Smooth animations
  },
  "devDependencies": {
    "@percy/cli": "^1.29.0",                // Visual regression testing
    "@testing-library/react": "^14.2.0",    // Component testing
    "@storybook/react": "^7.6.0"            // Component playground
  }
}
```

### When to Use Each Library

**Observable Plot** - You want ggplot2/Vega-Lite in JavaScript
- Grammar-of-graphics approach (marks, scales, transforms)
- Perfect for rapid prototyping
- Great for notebooks and exploratory analysis

**Recharts** - You want it to "just work" in React
- Component-based (everything is a `<Component />`)
- Excellent documentation and community
- TypeScript support built-in
- Smallest learning curve

**Nivo** - You want visually stunning results
- 20+ chart types with beautiful defaults
- Canvas, SVG, and HTML rendering
- Server-side rendering support (unique feature)
- Extensive customization via props

**Visx** - You want maximum control with React patterns
- Low-level primitives (scales, axes, shapes)
- Compose your own chart types
- Airbnb's D3 + React toolkit
- Best for novel visualizations

**D3.js** - You want unlimited power (and responsibility)
- Full control over every pixel
- Steepest learning curve
- Best for advanced, custom work
- Use with `useEffect` and `useRef` in React

## The Tufte Checklist

Before shipping any visualization, verify:

- [ ] **Data-ink ratio maximized** - Remove gridlines, decorations, 3D effects, shadows
- [ ] **Graphical integrity** - Visual representation proportional to data values
- [ ] **Clear labeling** - Direct labels on data (not legends requiring color matching)
- [ ] **No chart junk** - No unnecessary ornamentation or Moiré vibration
- [ ] **Layered information** - Use small multiples instead of overloaded single charts
- [ ] **Show data variation, not design variation** - Consistent visual encoding

Read `references/tufte-principles.md` for deep dive.

## The NYT Graphics Workflow

The New York Times graphics team process:

1. **Make 500 charts** → Pick the one that displays information best
2. **Simplify within reason** → Remove noise and clutter
3. **Annotate with insight** → Words should highlight patterns, not just describe data
4. **Test with real users** → Watch people interact, identify confusion
5. **Responsive by default** → Mobile-first, progressive enhancement

Read `references/nyt-workflow.md` for case studies.

## Animation & Micro-interactions

Data viz isn't static. Movement communicates:

### When to Animate
- **State transitions** - Data updates, filter changes
- **Draw attention** - Highlight insights, guide the eye
- **Show relationships** - Morphing between views reveals structure
- **Delight** - Thoughtful motion = premium feel

### Animation Principles
```typescript
// Use spring physics, not linear easing
const springConfig = {
  type: "spring",
  stiffness: 300,
  damping: 30
};

// Stagger for multiple elements
const staggerChildren = {
  delayChildren: 0.1,
  staggerChildren: 0.05
};

// Respect prefers-reduced-motion
const shouldAnimate = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

Read `references/animation-patterns.md` for complete patterns library.

## Color: Beyond the Rainbow

### Semantic Color Systems
```typescript
// Qualitative (categorical data)
const categorical = [
  "#d97706", "#7c3aed", "#059669", "#dc2626", "#2563eb"
];

// Sequential (ordered data, low to high)
const sequential = [
  "#fef3c7", "#fcd34d", "#f59e0b", "#d97706", "#92400e"
];

// Diverging (data with meaningful center)
const diverging = [
  "#dc2626", "#f87171", "#fef2f2", "#c7d2fe", "#6366f1"
];
```

### Accessibility Requirements
- **Contrast ratio ≥4.5:1** for text on backgrounds
- **Don't rely on color alone** - Use shapes, patterns, labels
- **Colorblind-safe palettes** - Test with simulators
- **Consider dark mode** - Colors must work in both themes

## Testing Data Visualizations

### Visual Regression Testing
```bash
# Percy - Automated visual testing
npx percy snapshot ./storybook-static

# Chromatic - For Storybook
npx chromatic --project-token=<token>
```

### Data Accuracy Testing
```typescript
// Verify rendered elements match data
test('bar chart renders correct number of bars', () => {
  const data = [{ x: 'A', y: 10 }, { x: 'B', y: 20 }];
  render(<BarChart data={data} />);

  const bars = screen.getAllByTestId('bar');
  expect(bars).toHaveLength(2);
});

// Verify scale accuracy
test('bar heights proportional to values', () => {
  const data = [{ x: 'A', y: 10 }, { x: 'B', y: 20 }];
  render(<BarChart data={data} />);

  const bars = screen.getAllByTestId('bar');
  const heights = bars.map(b => parseInt(b.style.height));
  expect(heights[1]).toBe(heights[0] * 2); // B is 2x A
});
```

Read `references/testing-strategies.md` for comprehensive test suites.

## Responsive Design Patterns

### Mobile-First Approach
```typescript
// Desktop: Show everything
// Tablet: Simplify axes, reduce labels
// Mobile: Minimal chart, key insights only

const ChartResponsive = ({ data }: Props) => {
  const isMobile = useMediaQuery('(max-width: 640px)');

  return (
    <ResponsiveContainer width="100%" height={isMobile ? 200 : 400}>
      <LineChart data={data}>
        {!isMobile && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis
          dataKey="date"
          tick={isMobile ? { fontSize: 10 } : undefined}
          interval={isMobile ? 'preserveStartEnd' : 'auto'}
        />
        <YAxis tick={isMobile ? false : undefined} />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#d97706" />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### Touch-Friendly Interactions
- **Minimum touch target: 44×44px** - Tooltips, buttons, interactive elements
- **Swipe gestures** - Navigate time series, change views
- **Pinch-to-zoom** - For dense charts (use carefully)
- **Long-press context menus** - Advanced actions

## Data Storytelling

Every visualization tells a story. Follow the narrative arc:

1. **Hook** - What's the surprising insight?
2. **Context** - Why should we care?
3. **Evidence** - Show the data clearly
4. **Conclusion** - What should we do?

### Narrative Techniques
- **Scrollytelling** - Charts animate as user scrolls
- **Progressive disclosure** - Start simple, reveal complexity
- **Annotations** - Point out the insight, don't make users hunt
- **Comparison** - Show before/after, us vs. them, expected vs. actual

Read `references/data-storytelling.md` for narrative frameworks.

## Common Anti-Patterns

### ❌ The "Rainbow Vomit" Pie Chart
**Problem:** 12 colors, tiny slices, legend on the side
**Solution:** Max 5 categories, direct labels, consider bar chart instead

### ❌ The "Misleading Axis" Bar Chart
**Problem:** Y-axis doesn't start at zero, exaggerates differences
**Solution:** Always start at zero for bar charts (lines can vary)

### ❌ The "Dual-Axis Confusion" Line Chart
**Problem:** Two Y-axes with different scales mislead viewers
**Solution:** Use separate charts or normalize to same scale

### ❌ The "3D Perspective" Lie
**Problem:** 3D effects distort data perception
**Solution:** Stick to 2D, use color/size for third dimension

### ❌ The "Spinner of Death" Loading State
**Problem:** Empty screen with spinner for 2+ seconds
**Solution:** Skeleton loading that shows chart structure immediately

Read `references/antipatterns.md` for exhaustive catalog.

## Implementation Workflow

### 1. Explore Your Data
```bash
# Use Observable Plot for rapid iteration
npm install @observablehq/plot

# Create throwaway prototypes, iterate fast
# When you find the right chart, implement in production library
```

### 2. Build Production Component
```typescript
// Use Recharts for standard charts
// Use Nivo for beautiful, themeable charts
// Use Visx/D3 for custom visualizations

// Always wrap in error boundaries
// Always show skeleton loading state
// Always handle empty/loading/error states
```

### 3. Test Thoroughly
```bash
# Visual regression testing
npx percy snapshot

# Component testing
npm test -- --coverage

# Accessibility testing
npx axe-core src/components/charts
```

### 4. Document & Deploy
```typescript
// Storybook for component playground
// Props documentation with TypeScript
// Usage examples for each chart type
```

## AI-Enhanced Visualizations

### When to Use Claude/Haiku
- **Dynamic annotations** - Generate insights from data
- **Color palette suggestions** - AI-powered color harmony
- **Chart type recommendations** - "What's the best way to show this?"
- **Accessibility descriptions** - Auto-generate alt text

### Example: AI Annotation
```typescript
const generateInsight = async (data: DataPoint[]) => {
  const response = await fetch('/api/claude', {
    method: 'POST',
    body: JSON.stringify({
      model: 'claude-haiku',
      prompt: `Analyze this data and provide ONE key insight (max 15 words): ${JSON.stringify(data)}`
    })
  });

  return response.text(); // "Sales peaked in Q3, driven by mobile conversions"
};
```

## Inspiration Galleries

**Study these regularly:**
- [ObservableHQ Featured Notebooks](https://observablehq.com/@observablehq/explore-featured-collections)
- [Information is Beautiful Awards](https://www.informationisbeautifulawards.com/)
- [NYT Graphics on Twitter](https://twitter.com/nytgraphics)
- [FlowingData](https://flowingdata.com/)
- [Datawrapper River](https://river.datawrapper.de/)
- [The Pudding](https://pudding.cool/)

## Performance Optimization

### Bundle Size Management
```typescript
// ❌ DON'T import entire library
import { LineChart } from 'recharts';

// ✅ DO tree-shake where possible
import LineChart from 'recharts/lib/chart/LineChart';

// Use dynamic imports for heavy charts
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false // Disable SSR for client-only charts
});
```

### Canvas vs SVG
- **SVG** - Better for &lt; 1000 data points, accessibility, crisp at any scale
- **Canvas** - Better for > 1000 data points, animations, performance
- **WebGL** - Best for > 10,000 data points, 3D, gaming-level performance

### Virtualization
For large datasets, render only visible portion:
```typescript
// Use react-window or react-virtualized for long lists
// Aggregate/sample data for chart display
// Store full dataset separately for export
```

## Accessibility Standards (WCAG AA)

### Requirements
- **Keyboard navigation** - All interactive elements accessible via Tab
- **Screen reader support** - Provide data tables as alternative
- **Focus indicators** - Visible focus states for interactive elements
- **Color contrast** - ≥4.5:1 for small text, ≥3:1 for large text
- **Reduced motion** - Respect `prefers-reduced-motion: reduce`

### Implementation
```typescript
<figure role="img" aria-labelledby="chart-title chart-desc">
  <h2 id="chart-title">Sales Over Time</h2>
  <p id="chart-desc">
    Line chart showing sales increased 45% from Q1 to Q4,
    peaking in November at $2.3M.
  </p>

  <LineChart data={data} />

  {/* Provide data table alternative */}
  <details>
    <summary>View data table</summary>
    <table>...</table>
  </details>
</figure>
```

## Reference Materials

This skill includes comprehensive reference documentation:

- **`references/tufte-principles.md`** - Edward Tufte's data visualization principles with examples
- **`references/library-comparison.md`** - Deep dive on Observable Plot, Recharts, Nivo, Visx, D3
- **`references/testing-strategies.md`** - Visual regression, component testing, accessibility testing
- **`references/animation-patterns.md`** - Motion design patterns for charts
- **`references/data-storytelling.md`** - Narrative techniques and scrollytelling patterns
- **`references/antipatterns.md`** - Common mistakes and how to avoid them
- **`references/nyt-workflow.md`** - New York Times graphics team best practices

## Utility Scripts

- **`scripts/data-transform.ts`** - Common data transformations (rollup, pivot, normalize)
- **`scripts/chart-test-helpers.ts`** - Testing utilities for verifying chart accuracy
- **`scripts/color-palette-generator.ts`** - Generate accessible color palettes
- **`scripts/performance-benchmark.ts`** - Benchmark chart rendering performance

## Quick Start: Building Your First Chart

```typescript
// 1. Install dependencies
// npm install recharts framer-motion

// 2. Create a simple line chart
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

const data = [
  { month: 'Jan', value: 400 },
  { month: 'Feb', value: 300 },
  { month: 'Mar', value: 600 },
];

export const SalesChart = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#d97706"
          strokeWidth={2}
          dot={{ fill: '#d97706', r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  </motion.div>
);

// 3. Test it
// 4. Ship it with confidence
```

---

**Remember:** The best visualization is the one that makes the insight obvious. When in doubt, simplify. When confused, prototype 10 options. When shipping, test ruthlessly.

This skill guides: Chart selection | Library integration | Testing strategies | Animation patterns | Accessibility compliance | Performance optimization
