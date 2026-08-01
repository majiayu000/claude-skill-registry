---
name: web-maps-leaflet
description: Leaflet interactive maps - map setup, tile layers, markers, popups, GeoJSON, custom controls, plugins, clustering, events
---

# Leaflet Interactive Map Patterns

> **Quick Guide:** Use Leaflet (v1.9.4) for lightweight interactive maps. `L.map` for initialization, `L.tileLayer` for base maps, `L.marker`/`L.popup` for points of interest, `L.geoJSON` for vector data with `onEachFeature`/`pointToLayer`/`style`/`filter` callbacks. Always include tile layer attribution. Always clean up maps with `map.remove()` on teardown. Use `L.markerClusterGroup` for 100+ markers. Use `@types/leaflet` for TypeScript support.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `map.remove()` when tearing down a map instance -- prevents memory leaks and orphaned event listeners)**

**(You MUST include attribution on tile layers -- most tile providers require it legally)**

**(You MUST use `L.markerClusterGroup` or canvas rendering for 100+ markers -- DOM markers do not scale)**

**(You MUST use named constants for coordinates, zoom levels, and style values -- NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** Leaflet, L.map, L.tileLayer, L.marker, L.popup, L.geoJSON, L.control, L.layerGroup, L.featureGroup, L.icon, L.divIcon, L.circleMarker, L.polyline, L.polygon, L.circle, markerClusterGroup, leaflet.markercluster, @types/leaflet, leaflet.css, addTo(map), bindPopup, onEachFeature, pointToLayer, flyTo, fitBounds

**When to use:**

- Rendering interactive maps with markers, popups, and overlays
- Displaying GeoJSON data (points, lines, polygons) on a map
- Building maps with layer switching (base layers, overlays)
- Creating custom map controls and interactions
- Handling large marker datasets with clustering

**When NOT to use:**

- 3D globe or terrain visualization (consider a WebGL-based mapping library)
- Real-time collaborative map editing (consider a specialized collaborative mapping tool)
- Vector tiles or client-side styling of map tiles (Leaflet renders raster tiles natively; vector tile support requires plugins)

**Key patterns covered:**

- Map initialization with tile layers and attribution
- Markers, popups, tooltips, and custom icons
- GeoJSON layers with `onEachFeature`, `pointToLayer`, `style`, `filter`
- Layer groups, feature groups, and layer control
- Custom controls via `L.Control.extend`
- Marker clustering with `L.markerClusterGroup`
- Events and interactive behavior
- TypeScript setup with `@types/leaflet`
- Performance strategies for large datasets

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Map setup, tile layers, markers, popups, GeoJSON, layer control, events
- [examples/advanced.md](examples/advanced.md) - Custom controls, clustering, performance, canvas rendering, TypeScript
- [reference.md](reference.md) - Decision frameworks, API quick reference, anti-patterns

---

<philosophy>

## Philosophy

Leaflet is a lightweight (~42KB gzipped) open-source library for mobile-friendly interactive maps. It provides a small, well-designed API covering the essentials, with a rich plugin ecosystem for everything else.

**Core principles:**

1. **Simplicity first** -- The core API covers 95% of map use cases. Plugins extend the rest.
2. **Layer-based architecture** -- Everything on the map is a layer (tiles, markers, GeoJSON, controls). Layers are added/removed independently.
3. **Method chaining** -- Most methods return `this`, enabling fluent builder-style setup.
4. **Event-driven interaction** -- Maps, markers, and layers emit events (`click`, `moveend`, `zoomend`). Subscribe with `.on()`.
5. **Mobile-first** -- Touch interactions, pinch zoom, and retina tile support are built in.

**When to use Leaflet:**

- Standard 2D web maps with markers, popups, and overlays
- GeoJSON visualization and interaction
- Projects needing a small bundle size
- Maps with up to ~10K markers (with clustering)

**When NOT to use Leaflet:**

- Maps requiring WebGL rendering for 100K+ features (consider a GL-based library)
- 3D visualization or globe projection
- Client-side vector tile styling (requires plugins or a different library)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Map Initialization and Tile Layers

Create a map targeting a DOM element, set the view, and add a tile layer with attribution.

```typescript
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const INITIAL_CENTER: L.LatLngExpression = [51.505, -0.09];
const INITIAL_ZOOM = 13;
const MAX_ZOOM = 19;

const map = L.map("map").setView(INITIAL_CENTER, INITIAL_ZOOM);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: MAX_ZOOM,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
```

**Why good:** Named constants for coordinates and zoom, attribution included (legally required by most providers), CSS import ensures controls render correctly

```typescript
// Bad -- magic numbers, missing attribution, missing CSS import
const map = L.map("map").setView([51.505, -0.09], 13);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
```

**Why bad:** Magic numbers for coordinates and zoom, missing attribution violates tile provider terms, missing CSS import causes broken control rendering

See [examples/core.md](examples/core.md) Pattern 1 for tile provider options and `invalidateSize` usage.

---

### Pattern 2: Markers, Popups, and Tooltips

Markers pin locations on the map. Bind popups (click-to-open) or tooltips (hover) for additional information.

```typescript
const MARKER_POSITION: L.LatLngExpression = [51.5, -0.09];

const marker = L.marker(MARKER_POSITION).addTo(map);
marker.bindPopup("<b>Hello</b><br>I am a popup.");
marker.bindTooltip("Hover text", { permanent: false, direction: "top" });
```

Standalone popups (not attached to a marker):

```typescript
L.popup().setLatLng([51.513, -0.09]).setContent("Standalone popup").openOn(map);
```

**Gotcha:** `openOn(map)` closes any previously open popup. Use `addTo(map)` if multiple popups should be open simultaneously.

See [examples/core.md](examples/core.md) Pattern 2 for custom icons, `L.divIcon`, and icon class extension.

---

### Pattern 3: GeoJSON Layers

`L.geoJSON` renders GeoJSON data with powerful callbacks for styling, filtering, and interaction.

```typescript
const CIRCLE_MARKER_RADIUS = 8;
const CIRCLE_MARKER_FILL_COLOR = "#ff7800";
const CIRCLE_MARKER_WEIGHT = 1;

const geoLayer = L.geoJSON(geojsonData, {
  pointToLayer: (feature, latlng) =>
    L.circleMarker(latlng, {
      radius: CIRCLE_MARKER_RADIUS,
      fillColor: CIRCLE_MARKER_FILL_COLOR,
      weight: CIRCLE_MARKER_WEIGHT,
      fillOpacity: 0.8,
    }),
  onEachFeature: (feature, layer) => {
    if (feature.properties?.name) {
      layer.bindPopup(feature.properties.name);
    }
  },
  style: (feature) => ({
    color: feature?.properties?.color ?? "#3388ff",
    weight: 2,
  }),
  filter: (feature) => feature?.properties?.visible !== false,
}).addTo(map);
```

**Why good:** `pointToLayer` customizes point rendering, `onEachFeature` binds interactivity, `style` enables data-driven visualization, `filter` excludes features declaratively

See [examples/core.md](examples/core.md) Pattern 3 for dynamic style updates, `addData`, and `resetStyle`.

---

### Pattern 4: Layer Groups and Layer Control

Group layers logically and provide a UI for toggling visibility.

```typescript
const cities = L.layerGroup([markerA, markerB]);
const parks = L.layerGroup([polygonA, polygonB]);

const baseLayers = {
  OpenStreetMap: osmTileLayer,
  Satellite: satelliteTileLayer,
};

const overlays = {
  Cities: cities,
  Parks: parks,
};

L.control.layers(baseLayers, overlays).addTo(map);
```

**Key distinction:** Base layers are radio buttons (one active at a time). Overlays are checkboxes (multiple can be active). Use `L.featureGroup` instead of `L.layerGroup` when you need `getBounds()` or `bindPopup` on the group.

See [examples/core.md](examples/core.md) Pattern 4 for programmatic layer toggling and feature group bounds.

---

### Pattern 5: Events and Interaction

Leaflet uses `.on()` for event binding. Maps, markers, and layers all support events.

```typescript
map.on("click", (e: L.LeafletMouseEvent) => {
  const { lat, lng } = e.latlng;
  L.popup()
    .setLatLng(e.latlng)
    .setContent(`Clicked at ${lat.toFixed(5)}, ${lng.toFixed(5)}`)
    .openOn(map);
});

map.on("zoomend", () => {
  console.log("Zoom level:", map.getZoom());
});

marker.on("dragend", (e: L.DragEndEvent) => {
  const pos = (e.target as L.Marker).getLatLng();
  console.log("Marker moved to:", pos);
});
```

Remove listeners with `.off()`:

```typescript
const handler = () => {
  /* ... */
};
map.on("moveend", handler);
map.off("moveend", handler); // cleanup
```

See [examples/core.md](examples/core.md) Pattern 5 for common event types reference.

---

### Pattern 6: Custom Controls

Extend `L.Control` to build custom map controls.

```typescript
const InfoControl = L.Control.extend({
  options: { position: "bottomleft" as L.ControlPosition },

  onAdd(_map: L.Map): HTMLElement {
    const container = L.DomUtil.create("div", "info-control");
    container.innerHTML = "<h4>Map Info</h4>";
    L.DomEvent.disableClickPropagation(container);
    return container;
  },

  onRemove(_map: L.Map): void {
    // cleanup event listeners if needed
  },
});

new InfoControl().addTo(map);
```

**Key rule:** Call `L.DomEvent.disableClickPropagation(container)` on interactive controls to prevent map clicks from firing through the control.

See [examples/advanced.md](examples/advanced.md) Pattern 1 for interactive controls with buttons and update methods.

---

### Pattern 7: Marker Clustering

Use `leaflet.markercluster` plugin for large marker datasets. Without clustering, 1000+ DOM markers will degrade performance severely.

```typescript
import "leaflet.markercluster";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

const MAX_CLUSTER_RADIUS = 50;
const DISABLE_CLUSTERING_ZOOM = 18;

const clusterGroup = L.markerClusterGroup({
  maxClusterRadius: MAX_CLUSTER_RADIUS,
  disableClusteringAtZoom: DISABLE_CLUSTERING_ZOOM,
  chunkedLoading: true,
  showCoverageOnHover: false,
});

markers.forEach((m) => clusterGroup.addLayer(m));
map.addLayer(clusterGroup);
```

**Why good:** `chunkedLoading` prevents UI freeze for bulk additions, `disableClusteringAtZoom` shows individual markers at close zoom, `maxClusterRadius` controls granularity

See [examples/advanced.md](examples/advanced.md) Pattern 2 for custom cluster icons and `refreshClusters`.

---

### Pattern 8: TypeScript Setup

Install `leaflet` and `@types/leaflet` for full type safety. Leaflet types cover all classes, options, and events.

```typescript
import L, {
  type LatLngExpression,
  type MapOptions,
  type TileLayerOptions,
} from "leaflet";

const options: MapOptions = {
  center: [51.505, -0.09],
  zoom: 13,
  zoomControl: true,
};

const map = L.map("map", options);
```

**Install:** `npm install leaflet` + `npm install -D @types/leaflet`

For markercluster types: `npm install -D @types/leaflet.markercluster`

See [examples/advanced.md](examples/advanced.md) Pattern 3 for typed GeoJSON features and event handlers.

---

### Pattern 9: Map Cleanup

Always remove map instances on component teardown to prevent memory leaks and orphaned event listeners.

```typescript
// Vanilla JS / framework-agnostic cleanup
function destroyMap(map: L.Map): void {
  map.off(); // remove all event listeners
  map.remove(); // destroy the map instance, clean up DOM
}
```

**Why this matters:** Leaflet attaches resize observers, animation frames, and event listeners to the DOM. Calling `map.remove()` is the single most important cleanup action -- it handles all internal teardown.

**Gotcha:** If you re-initialize a map on the same DOM element without calling `remove()` first, Leaflet throws "Map container is already initialized."

</patterns>

---

<performance>

## Performance Optimization

### Marker Count Thresholds

| Marker Count | Strategy                                      | Notes                              |
| ------------ | --------------------------------------------- | ---------------------------------- |
| < 100        | Standard `L.marker`                           | DOM markers are fine               |
| 100 - 10K    | `L.markerClusterGroup`                        | Clusters reduce DOM nodes          |
| 10K - 50K    | `L.markerClusterGroup` + `chunkedLoading`     | Batch additions to avoid UI freeze |
| 50K+         | Canvas-based rendering plugin or vector tiles | DOM/SVG cannot handle this volume  |

### GeoJSON Performance Tips

- Use `filter` option to exclude features before rendering (cheaper than rendering then hiding)
- Simplify geometry server-side for overview zoom levels (reduce coordinate precision)
- Add GeoJSON data in chunks using `addData()` for progressive rendering
- Call `clearLayers()` and re-add instead of updating individual feature styles when dataset changes completely

### General Tips

- Use `map.invalidateSize()` after container resize (CSS transitions, accordion expand)
- Set `preferCanvas: true` in map options for vector layers (circles, polylines) to render on canvas instead of SVG
- Use `L.circleMarker` instead of `L.marker` for data points -- renders on the vector renderer and is lighter than DOM markers
- Avoid attaching large HTML to popups -- use `setContent()` lazily on popup open event

</performance>

---

<decision_framework>

## Decision Framework

### Choosing a Marker Strategy

```
How many markers?
|
+-> < 100 -> Standard L.marker with L.icon or L.divIcon
|
+-> 100 - 10K -> L.markerClusterGroup (leaflet.markercluster plugin)
|
+-> 10K - 50K -> L.markerClusterGroup with chunkedLoading + consider L.circleMarker
|
+-> 50K+ -> Canvas rendering plugin or switch to vector tiles
```

### Choosing a Layer Type

```
What data are you displaying?
|
+-> Single coordinate point -> L.marker (with icon) or L.circleMarker (data viz)
|
+-> Line path -> L.polyline
|
+-> Area boundary -> L.polygon or L.circle
|
+-> GeoJSON dataset -> L.geoJSON (handles all geometry types)
|
+-> Grouped items needing toggle -> L.layerGroup (no shared popup) or L.featureGroup (shared popup/bounds)
```

### Choosing an Icon

```
What does the marker represent?
|
+-> Location pin (default) -> L.marker() with no icon option (uses default blue pin)
|
+-> Custom image -> L.icon({ iconUrl, iconSize, iconAnchor })
|
+-> HTML/CSS content -> L.divIcon({ html, className, iconSize })
|
+-> Data point (many) -> L.circleMarker (renders on vector layer, not DOM)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `map.remove()` on teardown -- causes memory leaks, orphaned DOM listeners, and "container already initialized" errors on re-mount
- Missing tile layer attribution -- violates terms of service for OpenStreetMap and most tile providers
- Using standard `L.marker` for 100+ points -- DOM markers cause severe performance degradation; use clustering or canvas
- Magic numbers for coordinates, zoom levels, or style values -- use named constants

**Medium Priority Issues:**

- Not calling `map.invalidateSize()` after container resize -- map renders incorrectly (grey tiles, offset clicks)
- Not importing `leaflet.css` -- controls, popups, and markers render without proper styling
- Using `openOn(map)` when multiple popups should be visible simultaneously -- it auto-closes the previous popup; use `addTo(map)` instead
- Not disabling click propagation on custom controls -- clicks on control elements trigger map click events

**Gotchas & Edge Cases:**

- **Default icon path issue:** Leaflet's default marker icon references images relative to the CSS file. With bundlers, the path breaks. Fix by importing and setting `L.Icon.Default.prototype.options` or using `L.divIcon`/`L.icon` explicitly.
- `L.geoJSON` expects coordinates in `[longitude, latitude]` order (GeoJSON spec), but `L.latLng` uses `[latitude, longitude]` -- mixing them up is the most common coordinate bug
- `flyTo` and `panTo` cancel each other if called in rapid succession -- debounce or guard against concurrent calls
- `map.fitBounds` on an empty `FeatureGroup` throws an error -- check `getBounds().isValid()` first
- `L.Control.extend` uses Leaflet's class system, not ES6 classes -- `new L.Control.extend({...})` returns a constructor, not an instance
- Tile layer `maxZoom` vs map `maxZoom`: tile layer's `maxZoom` limits tile availability; map's `maxZoom` limits user zoom. If map allows zoom 20 but tiles only go to 18, you see grey tiles.
- `L.markerClusterGroup.refreshClusters()` must be called after changing marker icons or data -- clusters do not auto-update

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `map.remove()` when tearing down a map instance -- prevents memory leaks and orphaned event listeners)**

**(You MUST include attribution on tile layers -- most tile providers require it legally)**

**(You MUST use `L.markerClusterGroup` or canvas rendering for 100+ markers -- DOM markers do not scale)**

**(You MUST use named constants for coordinates, zoom levels, and style values -- NO magic numbers)**

**Failure to follow these rules will cause memory leaks, legal violations, and performance degradation.**

</critical_reminders>
