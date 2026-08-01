---
name: web-maps-mapbox
description: Mapbox GL JS interactive maps - map initialization, markers, popups, sources, layers, expressions, clustering, 3D terrain, geocoding, directions
---

# Mapbox GL JS Patterns

> **Quick Guide:** Use Mapbox GL JS v3 for interactive vector maps. Initialize with `new mapboxgl.Map()`, add data via sources (GeoJSON, vector), visualize with layers (fill, line, circle, symbol, fill-extrusion, heatmap), style dynamically with expressions. Use the Standard style as the default base with slots (`bottom`, `middle`, `top`) for layer placement. Enable clustering on GeoJSON sources for large point datasets. Use `setTerrain` + `setFog` for 3D terrain. Types are included in the `mapbox-gl` package (no `@types/mapbox-gl` needed).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST add sources before layers that reference them -- adding a layer without its source throws a runtime error)**

**(You MUST listen for `load` or `style.load` before calling `addSource`/`addLayer` -- the style is not ready on construction)**

**(You MUST clean up map instances with `map.remove()` on unmount -- leaks GPU memory and event listeners)**

**(You MUST use named constants for coordinates, zoom levels, and style values -- NO magic numbers)**

**(You MUST use expressions for data-driven styling instead of iterating features and setting styles individually)**

</critical_requirements>

---

**Auto-detection:** Mapbox, mapbox-gl, mapboxgl, Map, Marker, Popup, NavigationControl, GeolocateControl, addSource, addLayer, GeoJSON source, vector source, expressions, flyTo, easeTo, fitBounds, setTerrain, setFog, fill-extrusion, clustering, slot, Standard style, mapbox-gl-geocoder, mapbox-gl-directions, mapbox-gl-draw

**When to use:**

- Rendering interactive vector tile maps with custom styling
- Displaying point/line/polygon data on a map with data-driven styling
- Building map-based UIs with markers, popups, and custom controls
- Visualizing large datasets with clustering, heatmaps, or 3D extrusions
- Adding geocoding search, routing directions, or drawing tools
- Creating 3D terrain visualizations with elevation data

**When NOT to use:**

- Static map images without interactivity (use Mapbox Static Images API)
- Simple embedded maps without custom data (a basic iframe embed suffices)
- Applications requiring offline-only maps without a Mapbox access token

**Key patterns covered:**

- Map initialization with Standard style and access token
- Markers, popups, and built-in controls
- Source/layer model (GeoJSON, vector, raster-dem)
- Expression-based data-driven styling
- Clustering with automatic expansion on click
- 3D terrain, fog, and fill-extrusion buildings
- Camera animation (flyTo, easeTo, fitBounds)
- Event handling (click, mouseenter, mouseleave on layers)
- v3 slot system and Standard style configuration

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Map setup, markers, popups, controls, events, camera animation
- [examples/layers.md](examples/layers.md) - Sources, layers, expressions, clustering, data-driven styling
- [examples/interaction.md](examples/interaction.md) - 3D terrain, fog, fill-extrusion, drawing, geocoding, directions
- [reference.md](reference.md) - Decision frameworks, layer types, expression operators, anti-patterns

---

<philosophy>

## Philosophy

Mapbox GL JS renders vector tiles on the GPU using WebGL 2, enabling smooth 60fps map interactions with large datasets. The core mental model is **sources + layers + expressions**:

1. **Sources** hold the data (GeoJSON, vector tiles, raster tiles, images)
2. **Layers** define how to visualize sources (fill, line, circle, symbol, fill-extrusion, heatmap, raster)
3. **Expressions** make layers data-driven (color by property, size by zoom, filter by attribute)

This separation means one source can power multiple layers (e.g., same GeoJSON rendered as both a fill layer and a line layer for borders), and layers can be styled entirely through expressions without touching the data.

**v3 Standard style:** The default style is `mapbox://styles/mapbox/standard`, which includes 3D buildings, terrain-aware rendering, and a slot system (`bottom`, `middle`, `top`) for inserting custom layers at predetermined positions in the visual stack. Use `setConfigProperty` to customize the Standard style's appearance without replacing it.

**TypeScript:** Types are bundled with `mapbox-gl` since v3 -- do not install `@types/mapbox-gl`.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Map Initialization

Initialize with container, style, center, zoom. Always wait for `load` event before adding sources/layers.

```typescript
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

const DEFAULT_CENTER: [number, number] = [-74.006, 40.7128]; // [lng, lat]
const DEFAULT_ZOOM = 12;

mapboxgl.accessToken = process.env.MAPBOX_ACCESS_TOKEN!;

const map = new mapboxgl.Map({
  container: "map", // HTML element ID or element reference
  style: "mapbox://styles/mapbox/standard",
  center: DEFAULT_CENTER,
  zoom: DEFAULT_ZOOM,
});

map.on("load", () => {
  // Safe to add sources and layers here
});
```

**Why good:** Named constants for coordinates/zoom, waits for `load` before data operations, uses Standard style

See [examples/core.md](examples/core.md) Pattern 1 for cleanup patterns and bad examples.

---

### Pattern 2: Markers, Popups, and Controls

Markers are DOM elements placed at coordinates. Popups display content on click. Controls add navigation UI.

```typescript
const MARKER_COLOR = "#e74c3c";

const popup = new mapboxgl.Popup({ offset: 25, maxWidth: "300px" }).setHTML(
  "<h3>Location</h3><p>Description</p>",
);

new mapboxgl.Marker({ color: MARKER_COLOR })
  .setLngLat([-74.006, 40.7128])
  .setPopup(popup)
  .addTo(map);

map.addControl(new mapboxgl.NavigationControl(), "top-right");
map.addControl(
  new mapboxgl.GeolocateControl({ trackUserLocation: true }),
  "top-right",
);
map.addControl(new mapboxgl.ScaleControl({ unit: "metric" }), "bottom-left");
```

**Why good:** Popup bound to marker (opens on click automatically), controls positioned explicitly, named color constant

See [examples/core.md](examples/core.md) Pattern 2 for custom marker elements and programmatic popup examples.

---

### Pattern 3: Source and Layer Model

Add a GeoJSON source, then one or more layers that reference it. Sources and layers are independent -- one source can feed multiple layers.

```typescript
map.on("load", () => {
  map.addSource("parks", {
    type: "geojson",
    data: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: [
              /* ... */
            ],
          },
          properties: { name: "Central Park", area: 3.41 },
        },
      ],
    },
  });

  map.addLayer({
    id: "parks-fill",
    type: "fill",
    source: "parks",
    slot: "middle", // v3 Standard style slot
    paint: {
      "fill-color": "#2ecc71",
      "fill-opacity": 0.5,
    },
  });

  map.addLayer({
    id: "parks-outline",
    type: "line",
    source: "parks",
    slot: "middle",
    paint: {
      "line-color": "#27ae60",
      "line-width": 2,
    },
  });
});
```

**Why good:** Source defined once, two layers visualize it differently, `slot: "middle"` places layers correctly in Standard style

See [examples/layers.md](examples/layers.md) Pattern 1-2 for all source types and layer configuration.

---

### Pattern 4: Data-Driven Styling with Expressions

Expressions are JSON arrays that style features based on their properties or zoom level.

```typescript
map.addLayer({
  id: "population-circles",
  type: "circle",
  source: "cities",
  paint: {
    // Size by population
    "circle-radius": [
      "interpolate",
      ["linear"],
      ["get", "population"],
      10000,
      5,
      100000,
      15,
      1000000,
      30,
    ],
    // Color by category
    "circle-color": [
      "match",
      ["get", "type"],
      "capital",
      "#e74c3c",
      "major",
      "#3498db",
      "#95a5a6", // fallback
    ],
  },
});
```

**Why good:** Expressions handle all styling on the GPU -- no JavaScript loops over features, scales with any dataset size

See [examples/layers.md](examples/layers.md) Pattern 3-4 for expression operators and filter expressions.

---

### Pattern 5: Clustering

Enable clustering on a GeoJSON source for large point datasets. Use three layers: cluster circles, count labels, unclustered points.

```typescript
const CLUSTER_RADIUS = 50;
const CLUSTER_MAX_ZOOM = 14;

map.addSource("earthquakes", {
  type: "geojson",
  data: "/data/earthquakes.geojson",
  cluster: true,
  clusterMaxZoom: CLUSTER_MAX_ZOOM,
  clusterRadius: CLUSTER_RADIUS,
});
```

**Why good:** Clustering is handled entirely by the source -- no external library needed, automatic `point_count` property on clusters

See [examples/layers.md](examples/layers.md) Pattern 5 for complete cluster layers and click-to-expand interaction.

---

### Pattern 6: Camera Animation

`flyTo` for dramatic transitions, `easeTo` for smooth pans, `fitBounds` for fitting data in view.

```typescript
const FLY_ZOOM = 15;
const FLY_SPEED = 1.2;
const BOUNDS_PADDING_PX = 50;

map.flyTo({
  center: [-122.4194, 37.7749],
  zoom: FLY_ZOOM,
  speed: FLY_SPEED,
  essential: true, // not affected by prefers-reduced-motion
});

map.fitBounds(
  [
    [-122.5, 37.7],
    [-122.3, 37.8],
  ], // [sw, ne]
  { padding: BOUNDS_PADDING_PX },
);
```

**Why good:** `essential: true` ensures critical navigation animations still play even with reduced-motion preferences, padding keeps data away from edges

See [examples/core.md](examples/core.md) Pattern 4 for easeTo, moveend listener, and bearing/pitch animation.

---

### Pattern 7: Layer Event Handling

Listen for events on specific layers for interactive features (click popups, hover effects).

```typescript
map.on("click", "parks-fill", (e) => {
  const feature = e.features?.[0];
  if (!feature) return;

  const coordinates = e.lngLat;
  const name = feature.properties?.name ?? "Unknown";

  new mapboxgl.Popup()
    .setLngLat(coordinates)
    .setHTML(`<strong>${name}</strong>`)
    .addTo(map);
});

// Cursor feedback on hover
map.on("mouseenter", "parks-fill", () => {
  map.getCanvas().style.cursor = "pointer";
});
map.on("mouseleave", "parks-fill", () => {
  map.getCanvas().style.cursor = "";
});
```

**Why good:** Events scoped to a specific layer (not the whole map), cursor change signals interactivity

See [examples/core.md](examples/core.md) Pattern 5 for feature-state hover highlighting.

---

### Pattern 8: 3D Terrain and Fog

Add elevation with a raster-dem source and atmospheric effects with fog.

```typescript
const TERRAIN_EXAGGERATION = 1.5;
const TERRAIN_MAX_ZOOM = 14;
const TERRAIN_TILE_SIZE = 512;

map.on("style.load", () => {
  map.addSource("mapbox-dem", {
    type: "raster-dem",
    url: "mapbox://mapbox.mapbox-terrain-dem-v1",
    tileSize: TERRAIN_TILE_SIZE,
    maxzoom: TERRAIN_MAX_ZOOM,
  });

  map.setTerrain({ source: "mapbox-dem", exaggeration: TERRAIN_EXAGGERATION });

  map.setFog({
    range: [-1, 2],
    "horizon-blend": 0.3,
    color: "white",
    "high-color": "#add8e6",
    "space-color": "#d8f2ff",
    "star-intensity": 0.0,
  });
});
```

**Why good:** Named exaggeration constant, terrain source separate from visual layers, fog adds atmospheric depth

See [examples/interaction.md](examples/interaction.md) Pattern 1-2 for fog presets and fill-extrusion 3D buildings.

---

### Pattern 9: v3 Standard Style Configuration

Customize the Standard style's built-in appearance without replacing it.

```typescript
// At initialization
const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/standard",
  config: {
    basemap: {
      lightPreset: "dusk",
      showPointOfInterestLabels: false,
    },
  },
});

// At runtime
map.setConfigProperty("basemap", "lightPreset", "night");
map.setConfigProperty("basemap", "showPlaceLabels", true);
```

**Why good:** Configuration API modifies the Standard style's built-in features without needing to understand its internal layer structure

</patterns>

---

<decision_framework>

## Decision Framework

### Choosing a Layer Type

```
What geometry are you displaying?
|
+-> Points?
|   +-> Few (<100) with custom HTML? -> Markers (DOM-based)
|   +-> Many or data-driven styling? -> circle layer or symbol layer
|   +-> Heatmap visualization? -> heatmap layer
|
+-> Lines/routes?
|   +-> line layer (width, color, dash patterns)
|
+-> Polygons?
|   +-> Flat colored areas? -> fill layer
|   +-> 3D extruded shapes? -> fill-extrusion layer
|
+-> Raster imagery?
    +-> raster layer (satellite, custom tiles)
```

### Choosing a Source Type

```
Where is your data?
|
+-> Local/API GeoJSON? -> type: "geojson"
|   +-> Dynamic updates? -> Use map.getSource(id).setData(newData)
|   +-> Large point dataset? -> Enable cluster: true
|
+-> Mapbox tileset or third-party vector tiles? -> type: "vector"
|
+-> Elevation data? -> type: "raster-dem"
|
+-> Image overlay? -> type: "image" (with coordinates bounds)
```

### Markers vs Circle Layers

```
How many points?
|
+-> < 100 with custom HTML/interaction? -> Markers (DOM elements)
+-> 100-10,000? -> circle layer (GPU-rendered)
+-> 10,000+? -> circle layer with clustering enabled on source
```

### Styling Approach

```
Is the style static (same for all features)?
|
+-> YES -> Use literal paint values: "circle-color": "#e74c3c"
+-> NO -> Does it depend on a data property?
    +-> Discrete categories? -> "match" expression
    +-> Continuous range? -> "interpolate" expression
    +-> Conditional logic? -> "case" expression
    +-> Zoom-dependent? -> "interpolate" with ["zoom"]
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Calling `addSource`/`addLayer` before the `load` event -- style is not ready, throws error
- Adding a layer that references a source that doesn't exist -- must add source first
- Not calling `map.remove()` on component unmount -- leaks GPU memory, WebGL contexts, and event listeners
- Using `Popup.setHTML()` with unsanitized user input -- XSS vulnerability. Use `setText()` or `setDOMContent()` for user data
- Iterating features to set individual styles instead of using expressions -- defeats GPU rendering, O(n) JavaScript vs O(1) GPU expressions

**Medium Priority Issues:**

- Using Markers for large datasets (100+ points) -- DOM elements are expensive, use circle/symbol layers instead
- Not scoping layer events to a specific layer -- `map.on("click", handler)` fires for any click, `map.on("click", "layer-id", handler)` targets one layer
- Missing cursor feedback on interactive layers -- users don't know features are clickable without `mouseenter`/`mouseleave` cursor changes
- Hardcoding coordinates, zoom levels, or style values -- use named constants
- Using `@types/mapbox-gl` package -- types are included in `mapbox-gl` since v3

**Gotchas & Edge Cases:**

- Coordinates are `[longitude, latitude]` -- reversed from the common `[lat, lng]` order used by some libraries
- `queryRenderedFeatures` only returns features currently visible in the viewport -- for all features use `querySourceFeatures`
- GeoJSON source `setData()` replaces the entire dataset -- for partial updates use `featureState` via `map.setFeatureState()`
- `style.load` fires every time the style changes (including `setStyle`), `load` fires only once -- use `style.load` for operations that must survive style switches
- Expression property access returns `null` for missing properties -- always provide fallback values in `match`/`case`/`coalesce`
- Popup `setHTML` does not sanitize HTML -- any user-provided content must be sanitized before passing
- `flyTo` with `essential: true` overrides `prefers-reduced-motion` -- use only for critical navigation, not decorative animations
- Clustered sources automatically add `point_count` and `cluster_id` properties -- do not create these manually
- `getClusterExpansionZoom` is async (callback-based) -- handle errors and check if map still exists before calling `easeTo`
- `map.getSource()` returns `undefined` if the source doesn't exist -- always guard the return value
- Layer `slot` property only works with the Standard style -- classic styles use `beforeId` parameter in `addLayer`
- `fill-extrusion` layers require `fill-extrusion-height` property -- without it extrusions are flat (0 height)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST add sources before layers that reference them -- adding a layer without its source throws a runtime error)**

**(You MUST listen for `load` or `style.load` before calling `addSource`/`addLayer` -- the style is not ready on construction)**

**(You MUST clean up map instances with `map.remove()` on unmount -- leaks GPU memory and event listeners)**

**(You MUST use named constants for coordinates, zoom levels, and style values -- NO magic numbers)**

**(You MUST use expressions for data-driven styling instead of iterating features and setting styles individually)**

**Failure to follow these rules will cause runtime errors, memory leaks, and XSS vulnerabilities.**

</critical_reminders>
