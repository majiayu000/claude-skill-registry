---
name: web-dataviz-d3
description: D3.js data visualization — selections, data joins, scales, axes, shapes, transitions, force layouts, geo projections, framework integration
---

# D3.js Data Visualization Patterns

> **Quick Guide:** D3 v7 is fully modular ES modules. Use `selection.join()` for the data join (replaces manual enter/update/exit). Prefer modular imports (`d3-selection`, `d3-scale`, etc.) to reduce bundle size. Scales map data domains to visual ranges; axes render tick marks from scales. Shape generators (`d3.line`, `d3.arc`, `d3.area`) produce SVG path strings from data arrays. Transitions animate attribute/style changes with automatic interpolation. For framework integration, let D3 handle data computation (scales, layouts, shapes) and let your framework own the DOM.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `selection.join()` for data joins — NOT manual enter/append/merge/exit chains)**

**(You MUST use modular imports (`d3-selection`, `d3-scale`, `d3-shape`) — NOT `import * as d3 from "d3"` in production bundles)**

**(You MUST use named constants for ALL visual dimensions, colors, and timing values — NO magic numbers)**

**(You MUST type D3 selections and scales with TypeScript generics — `Selection<SVGGElement, Datum, ...>`, `ScaleLinear<number, number>`)**

</critical_requirements>

---

**Auto-detection:** D3, d3, d3.js, d3-selection, d3-scale, d3-shape, d3-axis, d3-transition, d3-force, d3-geo, d3-zoom, d3-brush, d3-drag, d3-array, selection.join, data join, enter update exit, scaleLinear, scaleBand, scaleTime, axisBottom, axisLeft, forceSimulation, geoPath, geoMercator, line generator, arc generator, SVG visualization, data-driven documents

**When to use:**

- Building custom SVG/Canvas data visualizations from scratch
- Bindings between data arrays and DOM elements (the data join)
- Mapping data domains to pixel ranges (scales and axes)
- Generating SVG paths from data (lines, arcs, areas, pies)
- Animating data transitions with interpolated attributes
- Force-directed graph layouts and geographic map projections
- Adding zoom, brush, and drag interactions to visualizations

**When NOT to use:**

- Standard chart types (bar, line, pie) with minimal customization — use a charting library built on D3
- Dashboards with many chart widgets — use a higher-level charting library
- Simple data tables or non-graphical data display

**Key patterns covered:**

- Selections and the data join (`selection.data().join()`)
- Scales (linear, band, time, ordinal) and axes
- Shape generators (line, area, arc, pie, stack)
- Transitions and animated updates
- Force-directed graph layouts
- Geographic projections and choropleth maps
- Zoom, brush, and drag interactions
- Framework integration: D3 for math, framework for DOM
- Responsive SVG with viewBox
- TypeScript typing for D3

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Selections, data joins, scales, axes, shapes, responsive SVG
- [examples/interaction.md](examples/interaction.md) - Transitions, zoom, brush, drag, tooltips
- [examples/advanced.md](examples/advanced.md) - Force layouts, geo projections, framework integration patterns
- [reference.md](reference.md) - Module reference, decision frameworks, anti-patterns

---

<philosophy>

## Philosophy

D3 is a low-level visualization grammar, not a charting library. It provides primitives for binding data to DOM elements and applying data-driven transformations. This gives maximum control at the cost of more code than higher-level alternatives.

**Core mental model:**

1. **Select** elements (existing or placeholder)
2. **Bind** data to selections with `.data()`
3. **Join** to create/update/remove elements with `.join()`
4. **Encode** data as visual attributes with scales
5. **Annotate** with axes, labels, legends
6. **Animate** changes with transitions

**D3 v7 key decisions:**

- Pure ES modules — use modular imports for tree-shaking
- `selection.join()` replaces manual enter/update/exit boilerplate
- TypeScript types ship with each module (no `@types/d3` needed for core packages, but available for convenience)
- Works with any framework — D3 handles computation, your framework handles DOM rendering

**When NOT to use D3 directly:**

- Standard charts with minimal customization (use a charting library)
- Rapid prototyping where development speed matters more than customization
- Teams without SVG/visualization experience

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Selections and the Data Join

The data join is D3's core pattern: bind an array of data to DOM elements, then use `.join()` to create, update, and remove elements as data changes.

```typescript
import { select } from "d3-selection";

const BAR_HEIGHT = 30;
const BAR_GAP = 5;

// Select, bind data, join
select(svgElement)
  .selectAll<SVGRectElement, number>("rect")
  .data(values, (d) => String(d)) // key function for identity
  .join("rect") // enter + update merged
  .attr("y", (_, i) => i * (BAR_HEIGHT + BAR_GAP))
  .attr("width", (d) => xScale(d))
  .attr("height", BAR_HEIGHT);
```

**Why good:** `join("rect")` handles enter/update/exit in one call, key function ensures correct element-data binding across updates, typed selection generics

For advanced join with separate enter/update/exit callbacks, see [examples/core.md](examples/core.md) Pattern 1.

---

### Pattern 2: Scales — Mapping Data to Pixels

Scales are functions that map an input domain (data values) to an output range (pixel positions, colors).

```typescript
import { scaleLinear, scaleBand, scaleTime, scaleOrdinal } from "d3-scale";

const CHART_WIDTH = 600;
const CHART_HEIGHT = 400;

// Continuous: numbers -> pixels
const x = scaleLinear<number>()
  .domain([0, max(data, (d) => d.value)!])
  .range([0, CHART_WIDTH]);

// Categorical: strings -> pixel bands (bar charts)
const y = scaleBand<string>()
  .domain(data.map((d) => d.label))
  .range([0, CHART_HEIGHT])
  .padding(0.1);

// Time: Date -> pixels
const timeScale = scaleTime<number>()
  .domain([startDate, endDate])
  .range([0, CHART_WIDTH]);
```

**Why good:** TypeScript generics on scales, domain derived from data with `max()`, `.padding()` on band scale for gaps between bars

See [examples/core.md](examples/core.md) Pattern 2 for ordinal color scales and `scaleLog`/`scaleSqrt` patterns.

---

### Pattern 3: Axes — Rendering Scale Tick Marks

Axes are SVG groups generated from a scale. Render with `selection.call(axis)`.

```typescript
import { axisBottom, axisLeft } from "d3-axis";
import { format } from "d3-format";

const TICK_COUNT = 5;

// Create axes from scales
const xAxis = axisBottom(xScale).ticks(TICK_COUNT).tickFormat(format(",.0f"));
const yAxis = axisLeft(yScale);

// Render into <g> containers
svg
  .append("g")
  .attr("transform", `translate(0,${CHART_HEIGHT - MARGIN_BOTTOM})`)
  .call(xAxis);

svg.append("g").attr("transform", `translate(${MARGIN_LEFT},0)`).call(yAxis);
```

**Why good:** axes derived from scales (always in sync), `selection.call()` pattern for reusable rendering, `d3-format` for tick label formatting

See [examples/core.md](examples/core.md) Pattern 3 for time axes and grid line patterns.

---

### Pattern 4: Shape Generators — SVG Paths from Data

Shape generators are functions that take data arrays and produce SVG `d` attribute strings.

```typescript
import { line, area, arc, pie, curveMonotoneX } from "d3-shape";
import type { PieArcDatum } from "d3-shape";

// Line generator
const lineGen = line<DataPoint>()
  .x((d) => xScale(d.date))
  .y((d) => yScale(d.value))
  .curve(curveMonotoneX);

svg
  .append("path")
  .datum(data)
  .attr("d", lineGen)
  .attr("fill", "none")
  .attr("stroke", "steelblue");

// Pie + arc generators
const INNER_RADIUS = 0;
const OUTER_RADIUS = 150;

const pieGen = pie<SliceData>().value((d) => d.value);
const arcGen = arc<PieArcDatum<SliceData>>()
  .innerRadius(INNER_RADIUS)
  .outerRadius(OUTER_RADIUS);

svg
  .selectAll("path")
  .data(pieGen(sliceData))
  .join("path")
  .attr("d", arcGen)
  .attr("fill", (d) => colorScale(d.data.label));
```

**Why good:** generators configured once then reused, `.curve()` for smooth interpolation, typed `PieArcDatum` generic for pie data, named radius constants

See [examples/core.md](examples/core.md) Pattern 4 for area charts and stacked layouts.

---

### Pattern 5: Responsive SVG with viewBox

Use the `viewBox` attribute so SVG scales to its container without JS resize handlers.

```typescript
const VIEWBOX_WIDTH = 960;
const VIEWBOX_HEIGHT = 500;

const svg = select(container)
  .append("svg")
  .attr("viewBox", `0 0 ${VIEWBOX_WIDTH} ${VIEWBOX_HEIGHT}`)
  .attr("preserveAspectRatio", "xMidYMid meet")
  .style("width", "100%")
  .style("height", "auto");
```

**Why good:** SVG scales automatically, no resize listeners needed, chart dimensions stay consistent regardless of container size

For dynamic resizing with `ResizeObserver`, see [examples/core.md](examples/core.md) Pattern 5.

---

### Pattern 6: Transitions — Animated Data Updates

Transitions interpolate attributes and styles over time with easing.

```typescript
import { transition } from "d3-transition";
import { easeCubicOut } from "d3-ease";

const TRANSITION_DURATION_MS = 750;
const STAGGER_DELAY_MS = 50;

select(svgElement)
  .selectAll<SVGRectElement, DataPoint>("rect")
  .data(newData, (d) => d.id)
  .join(
    (enter) =>
      enter
        .append("rect")
        .attr("width", 0)
        .call((s) =>
          s
            .transition()
            .duration(TRANSITION_DURATION_MS)
            .attr("width", (d) => xScale(d.value)),
        ),
    (update) =>
      update.call((s) =>
        s
          .transition()
          .duration(TRANSITION_DURATION_MS)
          .attr("width", (d) => xScale(d.value)),
      ),
    (exit) =>
      exit.call((s) =>
        s
          .transition()
          .duration(TRANSITION_DURATION_MS)
          .attr("width", 0)
          .remove(),
      ),
  );
```

**Why good:** enter/update/exit each have distinct animated behavior, stagger creates cascading effect, named timing constants

See [examples/interaction.md](examples/interaction.md) Pattern 1 for easing functions and chained transitions.

---

### Pattern 7: Zoom and Pan

Apply zoom behavior with `d3.zoom()` and transform the visualization on zoom events.

```typescript
import { zoom, zoomIdentity } from "d3-zoom";
import type { D3ZoomEvent } from "d3-zoom";

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 32;

const zoomBehavior = zoom<SVGSVGElement, unknown>()
  .scaleExtent([MIN_ZOOM, MAX_ZOOM])
  .on("zoom", (event: D3ZoomEvent<SVGSVGElement, unknown>) => {
    chartGroup.attr("transform", event.transform.toString());
  });

svg.call(zoomBehavior);
```

**Why good:** typed zoom event and element generics, scale extent prevents over-zoom, transform applied to inner group (not the SVG itself)

See [examples/interaction.md](examples/interaction.md) Pattern 2 for semantic zoom and programmatic zoom controls.

---

### Pattern 8: Force-Directed Graph Layout

Force simulations position nodes using physics-based forces (repulsion, attraction, centering).

```typescript
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter,
  forceCollide,
} from "d3-force";

const CHARGE_STRENGTH = -300;
const COLLISION_RADIUS = 5;

const simulation = forceSimulation(nodes)
  .force(
    "link",
    forceLink(links)
      .id((d: NodeDatum) => d.id)
      .distance(100),
  )
  .force("charge", forceManyBody().strength(CHARGE_STRENGTH))
  .force("center", forceCenter(width / 2, height / 2))
  .force("collide", forceCollide(COLLISION_RADIUS))
  .on("tick", () => {
    // Update node and link positions from simulation
  });
```

**Why good:** named force constants, `.id()` accessor for node identity, `.distance()` for link length, collision prevents overlap

See [examples/advanced.md](examples/advanced.md) Pattern 1 for complete graph rendering with drag interaction.

---

### Pattern 9: Geographic Projections

Project geographic coordinates onto a 2D plane and render GeoJSON features as SVG paths.

```typescript
import { geoMercator, geoPath, geoNaturalEarth1 } from "d3-geo";
import type { GeoPermissibleObjects } from "d3-geo";

const projection = geoNaturalEarth1().fitSize(
  [CHART_WIDTH, CHART_HEIGHT],
  geoJsonData,
);

const pathGenerator = geoPath().projection(projection);

svg
  .selectAll("path")
  .data(geoJsonData.features)
  .join("path")
  .attr("d", pathGenerator)
  .attr("fill", (d) => colorScale(dataByRegion.get(d.properties.id) ?? 0));
```

**Why good:** `fitSize` auto-scales projection to container, path generator produces `d` strings from GeoJSON, color encodes data values per region

See [examples/advanced.md](examples/advanced.md) Pattern 2 for choropleth maps and interactive tooltips.

---

### Pattern 10: Framework Integration

When using D3 with a component framework, split responsibilities: D3 computes layouts, scales, and shapes; your framework renders the DOM.

```typescript
// Pattern: D3 for computation, framework for rendering
// In your component:

const xScale = scaleLinear().domain([0, maxValue]).range([0, width]);
const yScale = scaleBand().domain(labels).range([0, height]).padding(0.1);
const linePath = line<DataPoint>()
  .x((d) => xScale(d.x))
  .y((d) => yScale(d.y)!)(data);

// Your framework renders SVG with computed values
// <svg><path d={linePath} /><rect width={xScale(d.value)} /></svg>
```

**When D3 must own the DOM** (zoom, brush, drag, force tick): use a ref to an SVG element and call D3 in a lifecycle hook. Clean up the simulation/behavior on unmount.

See [examples/advanced.md](examples/advanced.md) Pattern 3 for the ref-based integration pattern and cleanup.

</patterns>

---

<decision_framework>

## Decision Framework

### D3 Module Selection

```
What are you building?
|
+-> Bar/line/area chart?
|   -> d3-selection, d3-scale, d3-axis, d3-shape, d3-array
|
+-> Pie/donut chart?
|   -> d3-shape (pie + arc generators), d3-scale (color)
|
+-> Force-directed graph?
|   -> d3-force, d3-selection, d3-drag
|
+-> Geographic map?
|   -> d3-geo, d3-selection, d3-scale (color)
|
+-> Animated transitions?
|   -> d3-transition, d3-ease, d3-interpolate
|
+-> Interactive (zoom/brush)?
    -> d3-zoom or d3-brush, d3-selection
```

### Framework Integration Strategy

```
Does the visualization need zoom, brush, drag, or force tick?
|
+-> NO -> D3 for computation only (scales, shapes, layouts)
|         Your framework renders SVG/HTML directly
|         Cleanest integration, fully declarative
|
+-> YES -> D3 owns the SVG via a ref element
           Call D3 in a lifecycle hook (mount/update)
           Clean up behaviors on unmount
```

### Scale Selection

| Data Type        | Scale        | Example                  |
| ---------------- | ------------ | ------------------------ |
| Continuous       | scaleLinear  | Revenue, temperature     |
| Categorical      | scaleBand    | Categories on bar chart  |
| Categorical dots | scalePoint   | Categories without width |
| Time series      | scaleTime    | Dates on x-axis          |
| Logarithmic      | scaleLog     | Exponential data ranges  |
| Square root      | scaleSqrt    | Bubble chart radius      |
| Color categories | scaleOrdinal | Category -> color        |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `import * as d3 from "d3"` in production — imports the entire 240KB+ bundle. Use modular imports: `import { select } from "d3-selection"`
- Manual enter/append/merge/exit chains — use `selection.join()` instead (simpler, fewer bugs)
- Animating non-interpolable attributes (class names, boolean attributes) — only animate numeric attributes and colors
- Missing key function in `.data(array, key)` when data identity matters — causes incorrect element-data binding on updates
- Mutating data arrays bound to selections — D3 stores references; mutations cause stale renders

**Medium Priority Issues:**

- Magic numbers for margins, radii, durations, colors — use named constants
- Creating a new SVG on every data update — select the existing SVG, update data bindings
- Appending axes on every update (duplicated tick marks) — select existing `<g>` and `.call(axis)` again, or use `.join()` pattern
- Forgetting `transition.remove()` on exit — exiting elements stay in the DOM invisible
- Not using `.nice()` on linear scales — domain ends at awkward values like `[0, 473]`

**Gotchas & Edge Cases:**

- `selection.join()` returns the merged enter+update selection — chained attributes apply to both new and existing elements
- `scaleBand().bandwidth()` returns the computed bar width — use it for rect width, not a hardcoded value
- `d3.max()` returns `undefined` for empty arrays — guard with `?? 0` or check array length first
- `transition.duration()` is per-element, not total — a 750ms transition on 100 elements still takes 750ms (not 75,000ms)
- `forceSimulation` runs asynchronously via `requestAnimationFrame` — stop it on unmount to prevent memory leaks
- `geoPath` without a projection renders pre-projected coordinates — only omit projection if GeoJSON is already projected
- Zoom transform applied to the SVG root clips panned content — apply transform to an inner `<g>` group instead
- `d3-transition` must be imported for `selection.transition()` to exist — it extends the selection prototype via side effect
- `.datum()` binds data to a single element without computing a join — use `.data()` for arrays, `.datum()` for single objects

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `selection.join()` for data joins — NOT manual enter/append/merge/exit chains)**

**(You MUST use modular imports (`d3-selection`, `d3-scale`, `d3-shape`) — NOT `import * as d3 from "d3"` in production bundles)**

**(You MUST use named constants for ALL visual dimensions, colors, and timing values — NO magic numbers)**

**(You MUST type D3 selections and scales with TypeScript generics — `Selection<SVGGElement, Datum, ...>`, `ScaleLinear<number, number>`)**

**Failure to follow these rules will cause bloated bundles, incorrect data binding, and untyped visualization code.**

</critical_reminders>
