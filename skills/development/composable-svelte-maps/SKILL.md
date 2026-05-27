---
name: composable-svelte-maps
description: Interactive maps and geospatial visualizations for Composable Svelte. Use when implementing maps, geolocation, markers, overlays, or geospatial data visualization. Covers Map component, markers, popups, GeoJSON layers, heatmaps, tile providers, viewport controls from @composable-svelte/maps package built with Maplibre GL.
---

# Composable Svelte Maps

Interactive maps and geospatial data visualization with Maplibre GL and Mapbox GL.

---

## PACKAGE OVERVIEW

**Package**: `@composable-svelte/maps`

**Purpose**: State-driven interactive maps with markers, layers, and geospatial features.

**Technology Stack**:
- **Maplibre GL**: Open-source WebGL-based maps (primary)
- **Mapbox GL**: Optional premium provider (requires API key)

**Core Features**:
- Interactive maps with zoom/pan
- Markers with popups
- GeoJSON layers (polygons, lines, points)
- Heatmap visualization
- Multiple tile providers (OSM, CartoDB, Stamen, etc.)
- Viewport animations (flyTo, fitBounds)
- Feature interactions (hover, click)

**State Management**:
All map state managed via pure reducers following Composable Architecture patterns.

---

## QUICK START

```typescript
import { createStore } from '@composable-svelte/core';
import { Map, mapReducer, createInitialMapState } from '@composable-svelte/maps';

// Create map store
const mapStore = createStore({
  initialState: createInitialMapState({
    center: [-74.006, 40.7128],  // NYC
    zoom: 12,
    tileProvider: 'osm'
  }),
  reducer: mapReducer,
  dependencies: {}
});

// Render map
<Map
  store={mapStore}
  width="100%"
  height="600px"
/>
```

---

## MAP COMPONENT

**Purpose**: Root container for interactive maps.

### Props

- `store: Store<MapState, MapAction>` - Map store (required)
- `width: string | number` - Width (default: '100%')
- `height: string | number` - Height (default: '600px')
- `onMapClick: (lngLat: [number, number]) => void` - Click handler (optional)
- `children: Snippet` - Child components (optional)

### Usage

```typescript
<Map
  store={mapStore}
  width="100%"
  height="600px"
  onMapClick={(lngLat) => console.log('Clicked:', lngLat)}
/>
```

### Lifecycle

1. Creates container element
2. Initializes Maplibre/Mapbox
3. Sets up manual subscription for state sync
4. Dispatches `mapLoaded` when ready
5. Syncs viewport, markers, layers, popups
6. Cleans up on unmount

---

## STATE MANAGEMENT

### MapState Interface

```typescript
interface MapState {
  // Provider
  provider: 'maplibre' | 'mapbox';
  accessToken?: string;  // Mapbox only

  // Tile provider
  tileProvider: TileProvider;
  customTileURL?: string;
  customAttribution?: string;

  // Viewport
  viewport: {
    center: [number, number];  // [lng, lat]
    zoom: number;              // 0-22
    bearing: number;           // 0-360 (rotation)
    pitch: number;             // 0-60 (tilt)
    bounds?: [[number, number], [number, number]];
  };

  // Interaction
  isInteractive: boolean;
  isDragging: boolean;
  isZooming: boolean;
  flyToTarget?: FlyToOptions;

  // Markers
  markers: Marker[];

  // Layers
  layers: Layer[];

  // Popups
  popups: Popup[];

  // Feature interactions
  hoveredFeature: FeatureReference | null;
  selectedFeatures: FeatureReference[];

  // Map style
  style: string;  // Style URL

  // Loading
  isLoaded: boolean;
  isLoading: boolean;
  error: string | null;
}
```

### MapAction Types

```typescript
type MapAction =
  // Viewport
  | { type: 'setCenter'; center: [number, number] }
  | { type: 'setZoom'; zoom: number }
  | { type: 'setBearing'; bearing: number }
  | { type: 'setPitch'; pitch: number }
  | { type: 'fitBounds'; bounds: [[number, number], [number, number]]; padding?: number }
  | { type: 'flyTo'; center: [number, number]; zoom?: number; duration?: number }
  | { type: 'resetNorth' }

  // Interaction
  | { type: 'zoomIn' }
  | { type: 'zoomOut' }
  | { type: 'panStart'; position: [number, number] }
  | { type: 'panMove'; delta: [number, number] }
  | { type: 'panEnd' }

  // Markers
  | { type: 'addMarker'; marker: Marker }
  | { type: 'removeMarker'; id: string }
  | { type: 'updateMarker'; id: string; updates: Partial<Marker> }
  | { type: 'moveMarker'; id: string; position: [number, number] }
  | { type: 'clearMarkers' }

  // Layers
  | { type: 'addLayer'; layer: Layer }
  | { type: 'removeLayer'; id: string }
  | { type: 'toggleLayerVisibility'; id: string }
  | { type: 'updateLayerStyle'; id: string; style: Partial<LayerStyle> }
  | { type: 'clearLayers' }

  // Popups
  | { type: 'openPopup'; popup: Popup }
  | { type: 'closePopup'; id: string }
  | { type: 'closeAllPopups' }

  // Features
  | { type: 'featureHovered'; feature: FeatureReference }
  | { type: 'featureUnhovered' }
  | { type: 'featureClicked'; feature: FeatureReference }
  | { type: 'clearSelection' }

  // Map lifecycle
  | { type: 'viewportChanged'; viewport: MapViewport }
  | { type: 'mapLoaded' }
  | { type: 'mapError'; error: string }
  | { type: 'changeStyle'; style: string }
  | { type: 'changeTileProvider'; provider: TileProvider; customURL?: string };
```

### Creating Initial State

```typescript
import { createInitialMapState } from '@composable-svelte/maps';

const initialState = createInitialMapState({
  center: [-74.006, 40.7128],  // NYC
  zoom: 12,
  tileProvider: 'osm',
  provider: 'maplibre'  // Default (free)
});
```

---

## VIEWPORT CONTROLS

### Center & Zoom

```typescript
// Set center
mapStore.dispatch({
  type: 'setCenter',
  center: [-122.4194, 37.7749]  // San Francisco
});

// Set zoom
mapStore.dispatch({
  type: 'setZoom',
  zoom: 15
});

// Zoom in/out
mapStore.dispatch({ type: 'zoomIn' });
mapStore.dispatch({ type: 'zoomOut' });
```

### Bearing & Pitch

```typescript
// Rotate map (bearing)
mapStore.dispatch({
  type: 'setBearing',
  bearing: 45  // 0-360 degrees
});

// Tilt map (pitch)
mapStore.dispatch({
  type: 'setPitch',
  pitch: 30  // 0-60 degrees
});

// Reset to north
mapStore.dispatch({ type: 'resetNorth' });
```

### Animated Navigation

```typescript
// Fly to location
mapStore.dispatch({
  type: 'flyTo',
  center: [-0.1276, 51.5074],  // London
  zoom: 12,
  duration: 2000  // milliseconds
});

// Fit bounds
mapStore.dispatch({
  type: 'fitBounds',
  bounds: [
    [-74.1, 40.7],  // Southwest corner
    [-73.9, 40.8]   // Northeast corner
  ],
  padding: 50
});
```

---

## MARKERS

**Purpose**: Point-of-interest indicators on the map.

### Marker Interface

```typescript
interface Marker<TData = unknown> {
  id: string;
  position: [number, number];  // [lng, lat]
  icon?: string;               // URL or data URI
  draggable?: boolean;
  data?: TData;                // Custom data
  popup?: {
    content: string;
    isOpen: boolean;
  };
}
```

### Adding Markers

```typescript
mapStore.dispatch({
  type: 'addMarker',
  marker: {
    id: 'marker-1',
    position: [-74.006, 40.7128],
    icon: '/icons/pin-red.png',
    draggable: false,
    data: { name: 'NYC', population: 8000000 },
    popup: {
      content: '<h3>New York City</h3><p>Population: 8M</p>',
      isOpen: false
    }
  }
});
```

### Updating Markers

```typescript
// Update marker properties
mapStore.dispatch({
  type: 'updateMarker',
  id: 'marker-1',
  updates: {
    icon: '/icons/pin-blue.png',
    popup: { content: 'Updated!', isOpen: true }
  }
});

// Move marker
mapStore.dispatch({
  type: 'moveMarker',
  id: 'marker-1',
  position: [-73.935, 40.730]
});
```

### Removing Markers

```typescript
// Remove single marker
mapStore.dispatch({
  type: 'removeMarker',
  id: 'marker-1'
});

// Clear all markers
mapStore.dispatch({ type: 'clearMarkers' });
```

---

## LAYERS

**Purpose**: Visualize geospatial data (polygons, lines, heatmaps).

### Layer Types

- **GeoJSON**: Polygon, LineString, Point, MultiPolygon, etc.
- **Heatmap**: Density visualization from point data

### Layer Interface

```typescript
interface Layer {
  id: string;
  type: 'geojson' | 'heatmap';
  data: GeoJSON | string;  // Object or URL
  style: LayerStyle;
  visible: boolean;
  interactive: boolean;
}

interface LayerStyle {
  fillColor?: string;
  fillOpacity?: number;
  strokeColor?: string;
  strokeWidth?: number;
  strokeOpacity?: number;
  radius?: number;              // For points
  intensity?: number;           // For heatmaps
  colorGradient?: [number, string][];  // For heatmaps
}
```

### GeoJSON Layer

```typescript
// Add GeoJSON layer
mapStore.dispatch({
  type: 'addLayer',
  layer: {
    id: 'neighborhoods',
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [[
              [-74.0, 40.7],
              [-74.0, 40.8],
              [-73.9, 40.8],
              [-73.9, 40.7],
              [-74.0, 40.7]
            ]]
          },
          properties: { name: 'Chelsea', population: 50000 }
        }
      ]
    },
    style: {
      fillColor: '#3388ff',
      fillOpacity: 0.5,
      strokeColor: '#0066cc',
      strokeWidth: 2
    },
    visible: true,
    interactive: true
  }
});

// Or load from URL
mapStore.dispatch({
  type: 'addLayer',
  layer: {
    id: 'countries',
    type: 'geojson',
    data: '/data/countries.geojson',
    style: { fillColor: '#88cc88', fillOpacity: 0.3 },
    visible: true,
    interactive: true
  }
});
```

### Heatmap Layer

```typescript
mapStore.dispatch({
  type: 'addLayer',
  layer: {
    id: 'crime-heatmap',
    type: 'heatmap',
    data: {
      type: 'FeatureCollection',
      features: crimeData.map(crime => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [crime.lng, crime.lat]
        },
        properties: { intensity: crime.severity }
      }))
    },
    style: {
      intensity: 1.0,
      radius: 30,
      colorGradient: [
        [0, 'rgba(0, 0, 255, 0)'],
        [0.5, 'rgba(0, 255, 255, 0.5)'],
        [1, 'rgba(255, 0, 0, 1)']
      ]
    },
    visible: true,
    interactive: false
  }
});
```

### Managing Layers

```typescript
// Update layer style
mapStore.dispatch({
  type: 'updateLayerStyle',
  id: 'neighborhoods',
  style: {
    fillColor: '#ff8800',
    fillOpacity: 0.7
  }
});

// Toggle visibility
mapStore.dispatch({
  type: 'toggleLayerVisibility',
  id: 'neighborhoods'
});

// Remove layer
mapStore.dispatch({
  type: 'removeLayer',
  id: 'neighborhoods'
});

// Clear all layers
mapStore.dispatch({ type: 'clearLayers' });
```

---

## POPUPS

**Purpose**: Display information overlays at specific locations.

### Popup Interface

```typescript
interface Popup {
  id: string;
  position: [number, number];  // [lng, lat]
  content: string;             // HTML content
  isOpen: boolean;
  closeButton?: boolean;
  closeOnClick?: boolean;
}
```

### Managing Popups

```typescript
// Open popup
mapStore.dispatch({
  type: 'openPopup',
  popup: {
    id: 'info-popup',
    position: [-74.006, 40.7128],
    content: '<h3>NYC</h3><p>The Big Apple</p>',
    isOpen: true,
    closeButton: true,
    closeOnClick: true
  }
});

// Close popup
mapStore.dispatch({
  type: 'closePopup',
  id: 'info-popup'
});

// Close all popups
mapStore.dispatch({ type: 'closeAllPopups' });
```

---

## TILE PROVIDERS

**Purpose**: Different map styles and base layers.

### Available Providers

- `'osm'` - OpenStreetMap (default, free)
- `'carto-light'` - CartoDB Light (free)
- `'carto-dark'` - CartoDB Dark (free)
- `'stamen-terrain'` - Stamen Terrain (free)
- `'stamen-toner'` - Stamen Toner (free)
- `'satellite'` - Satellite imagery (requires Mapbox)
- `'custom'` - Custom tile URL

### Changing Tile Provider

```typescript
// Use built-in provider
mapStore.dispatch({
  type: 'changeTileProvider',
  provider: 'carto-dark'
});

// Use custom tiles
mapStore.dispatch({
  type: 'changeTileProvider',
  provider: 'custom',
  customURL: 'https://tiles.example.com/{z}/{x}/{y}.png',
  customAttribution: '© Example Maps'
});
```

### Style Presets

```typescript
// Change map style (Mapbox only)
mapStore.dispatch({
  type: 'changeStyle',
  style: 'mapbox://styles/mapbox/streets-v11'
});
```

---

## FEATURE INTERACTIONS

**Purpose**: Respond to user interactions with map features (layers).

### Hover

```typescript
// Listen for hover
$effect(() => {
  if ($mapStore.hoveredFeature) {
    console.log('Hovered:', $mapStore.hoveredFeature);
    // Update UI, show tooltip, etc.
  }
});

// Reducer handles hover automatically from map component
```

### Click

```typescript
// Listen for click
$effect(() => {
  const selected = $mapStore.selectedFeatures;
  if (selected.length > 0) {
    console.log('Selected features:', selected);
    // Display info panel, highlight, etc.
  }
});

// Clear selection
mapStore.dispatch({ type: 'clearSelection' });
```

### FeatureReference Interface

```typescript
interface FeatureReference<TData = unknown> {
  layer: string;              // Layer ID
  featureId: string | number; // Feature ID
  data?: TData;               // Feature properties
}
```

---

## COMPLETE EXAMPLES

### Basic Map with Markers

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Map, mapReducer, createInitialMapState } from '@composable-svelte/maps';

// Create map store
const mapStore = createStore({
  initialState: createInitialMapState({
    center: [-74.006, 40.7128],
    zoom: 12,
    tileProvider: 'osm'
  }),
  reducer: mapReducer,
  dependencies: {}
});

// Add markers
const cities = [
  { id: 'nyc', name: 'New York', position: [-74.006, 40.7128] },
  { id: 'sf', name: 'San Francisco', position: [-122.4194, 37.7749] },
  { id: 'la', name: 'Los Angeles', position: [-118.2437, 34.0522] }
];

cities.forEach(city => {
  mapStore.dispatch({
    type: 'addMarker',
    marker: {
      id: city.id,
      position: city.position,
      popup: {
        content: `<h3>${city.name}</h3>`,
        isOpen: false
      }
    }
  });
});
</script>

<Map store={mapStore} width="100%" height="600px" />
```

### GeoJSON Visualization

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Map, mapReducer, createInitialMapState } from '@composable-svelte/maps';

const mapStore = createStore({
  initialState: createInitialMapState({
    center: [-98.5795, 39.8283],  // Center of US
    zoom: 4,
    tileProvider: 'carto-light'
  }),
  reducer: mapReducer,
  dependencies: {}
});

// Load US states GeoJSON
fetch('/data/us-states.geojson')
  .then(res => res.json())
  .then(geojson => {
    mapStore.dispatch({
      type: 'addLayer',
      layer: {
        id: 'us-states',
        type: 'geojson',
        data: geojson,
        style: {
          fillColor: '#3388ff',
          fillOpacity: 0.4,
          strokeColor: '#0066cc',
          strokeWidth: 2
        },
        visible: true,
        interactive: true
      }
    });
  });

// Handle feature clicks
$effect(() => {
  const selected = $mapStore.selectedFeatures;
  if (selected.length > 0) {
    const state = selected[0].data;
    console.log('Selected state:', state.name);

    // Open popup
    mapStore.dispatch({
      type: 'openPopup',
      popup: {
        id: 'state-popup',
        position: state.centroid,
        content: `<h3>${state.name}</h3><p>Population: ${state.population}</p>`,
        isOpen: true
      }
    });
  }
});
</script>

<Map store={mapStore} width="100%" height="600px" />
```

### Heatmap with Controls

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Map, mapReducer, createInitialMapState } from '@composable-svelte/maps';

const mapStore = createStore({
  initialState: createInitialMapState({
    center: [-118.2437, 34.0522],  // LA
    zoom: 11,
    tileProvider: 'carto-dark'
  }),
  reducer: mapReducer,
  dependencies: {}
});

// Crime data (example)
const crimeData = [
  { lat: 34.05, lng: -118.25, severity: 5 },
  { lat: 34.06, lng: -118.24, severity: 8 },
  // ... more points
];

// Add heatmap layer
mapStore.dispatch({
  type: 'addLayer',
  layer: {
    id: 'crime-heatmap',
    type: 'heatmap',
    data: {
      type: 'FeatureCollection',
      features: crimeData.map(crime => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [crime.lng, crime.lat]
        },
        properties: { weight: crime.severity }
      }))
    },
    style: {
      intensity: 1.0,
      radius: 30,
      colorGradient: [
        [0, 'rgba(0, 0, 255, 0)'],
        [0.5, 'rgba(0, 255, 255, 0.5)'],
        [1, 'rgba(255, 0, 0, 1)']
      ]
    },
    visible: true,
    interactive: false
  }
});

// Intensity control
let intensity = $state(1.0);

$effect(() => {
  mapStore.dispatch({
    type: 'updateLayerStyle',
    id: 'crime-heatmap',
    style: { intensity }
  });
});
</script>

<div>
  <Map store={mapStore} width="100%" height="600px" />

  <div class="controls">
    <label>
      Intensity: {intensity.toFixed(1)}
      <input
        type="range"
        bind:value={intensity}
        min="0"
        max="2"
        step="0.1"
      />
    </label>
  </div>
</div>
```

---

## COMMON PATTERNS

### User Location

```typescript
navigator.geolocation.getCurrentPosition(
  (position) => {
    const userLocation = [position.coords.longitude, position.coords.latitude];

    // Center on user
    mapStore.dispatch({
      type: 'flyTo',
      center: userLocation,
      zoom: 15,
      duration: 1500
    });

    // Add marker
    mapStore.dispatch({
      type: 'addMarker',
      marker: {
        id: 'user-location',
        position: userLocation,
        icon: '/icons/user-pin.png'
      }
    });
  },
  (error) => console.error('Geolocation error:', error)
);
```

### Draggable Markers

```typescript
mapStore.dispatch({
  type: 'addMarker',
  marker: {
    id: 'draggable-pin',
    position: [-74.006, 40.7128],
    draggable: true
  }
});

// Listen for updates
$effect(() => {
  const marker = $mapStore.markers.find(m => m.id === 'draggable-pin');
  if (marker) {
    console.log('Marker position:', marker.position);
  }
});
```

### Layer Toggle

```typescript
let showLayer = $state(true);

$effect(() => {
  if (showLayer) {
    mapStore.dispatch({
      type: 'addLayer',
      layer: myLayer
    });
  } else {
    mapStore.dispatch({
      type: 'removeLayer',
      id: myLayer.id
    });
  }
});

<button onclick={() => showLayer = !showLayer}>
  {showLayer ? 'Hide' : 'Show'} Layer
</button>
```

### Viewport Sync

```typescript
// Sync viewport between two maps
const map1Store = createStore({...});
const map2Store = createStore({...});

$effect(() => {
  const viewport = $map1Store.viewport;
  map2Store.dispatch({ type: 'viewportChanged', viewport });
});
```

---

## PERFORMANCE CONSIDERATIONS

### Large GeoJSON Files

**Problem**: Loading large GeoJSON (10MB+) can freeze UI.

**Solutions**:
1. **Simplify geometry**: Use tools like `mapshaper` to reduce vertices
2. **Tile vector data**: Use vector tiles (`.pbf`) instead of GeoJSON
3. **Load progressively**: Stream features in chunks

```typescript
// Example: Load in chunks
async function loadLargeGeoJSON(url: string) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';
  let features = [];

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Parse complete features
    // (simplified - actual implementation more complex)
    const parsed = parsePartialGeoJSON(buffer);
    features.push(...parsed.features);
    buffer = parsed.remaining;

    // Update map periodically
    if (features.length >= 100) {
      mapStore.dispatch({
        type: 'addLayer',
        layer: {
          id: 'large-layer',
          type: 'geojson',
          data: { type: 'FeatureCollection', features },
          style: myStyle,
          visible: true,
          interactive: true
        }
      });
      features = [];
    }
  }
}
```

### Many Markers

**Problem**: 1000+ markers slow down rendering.

**Solutions**:
1. **Clustering**: Group nearby markers
2. **Viewport culling**: Only show markers in view
3. **Use GeoJSON layer**: More efficient than individual markers

### Heatmap Performance

**Problem**: Heatmaps with 10,000+ points lag.

**Solutions**:
1. **Reduce radius**: Smaller radius = less overlap = faster
2. **Lower intensity**: Less blending computation
3. **Downsample**: Show fewer points when zoomed out

---

## TESTING

### Basic Map Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { mapReducer, createInitialMapState } from '@composable-svelte/maps';

const store = new TestStore({
  initialState: createInitialMapState({
    center: [0, 0],
    zoom: 10
  }),
  reducer: mapReducer,
  dependencies: {}
});

// Test viewport change
await store.send({
  type: 'setCenter',
  center: [-74.006, 40.7128]
}, (state) => {
  expect(state.viewport.center).toEqual([-74.006, 40.7128]);
});

await store.send({
  type: 'setZoom',
  zoom: 15
}, (state) => {
  expect(state.viewport.zoom).toBe(15);
});
```

### Marker Testing

```typescript
await store.send({
  type: 'addMarker',
  marker: {
    id: 'test-marker',
    position: [0, 0]
  }
}, (state) => {
  expect(state.markers.length).toBe(1);
  expect(state.markers[0].id).toBe('test-marker');
});

await store.send({
  type: 'moveMarker',
  id: 'test-marker',
  position: [1, 1]
}, (state) => {
  expect(state.markers[0].position).toEqual([1, 1]);
});

await store.send({
  type: 'removeMarker',
  id: 'test-marker'
}, (state) => {
  expect(state.markers.length).toBe(0);
});
```

---

## TROUBLESHOOTING

**Map not rendering**:
- Check Maplibre GL CSS imported: `import 'maplibre-gl/dist/maplibre-gl.css'`
- Verify container has explicit height set
- Check browser console for initialization errors

**Markers not appearing**:
- Verify position format: `[longitude, latitude]` (not `[lat, lng]`)
- Check marker is within viewport bounds
- Ensure icon URL is valid (if using custom icon)

**GeoJSON not showing**:
- Validate GeoJSON format (use online validator)
- Check coordinates are `[lng, lat]` order
- Verify layer `visible: true`

**Poor performance**:
- Simplify geometry (reduce vertices)
- Use vector tiles for large datasets
- Cluster markers when zoomed out
- Reduce heatmap radius/intensity

**Tile provider not working**:
- Check network requests in DevTools
- Verify custom tile URL format includes `{z}/{x}/{y}`
- Some providers require attribution in UI

---

## CROSS-REFERENCES

**Related Skills**:
- **composable-svelte-core**: Store, reducer, Effect system
- **composable-svelte-components**: UI components (Button, Slider, etc.)
- **composable-svelte-testing**: TestStore for testing map reducers

**When to Use Each Package**:
- **maps**: Geospatial data, interactive maps, markers, GeoJSON
- **charts**: 2D data visualization (see composable-svelte-charts)
- **graphics**: 3D scenes, WebGPU/WebGL (see composable-svelte-graphics)
- **code**: Code editors, media players (see composable-svelte-code)
