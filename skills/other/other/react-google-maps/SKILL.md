---
name: react-google-maps
description: Expert implementation of @vis.gl/react-google-maps library for Google Maps in React. Use when building maps, markers, pins, infowindows, places autocomplete, geocoding, draggable markers, polygons, circles, polylines, drawing tools, or any Google Maps JavaScript API integration in React/Next.js applications.
---

# @vis.gl/react-google-maps

Official React library for Google Maps JavaScript API, maintained by vis.gl with Google sponsorship.

## Quick Start

```tsx
import { APIProvider, Map, AdvancedMarker, Pin } from '@vis.gl/react-google-maps';

function App() {
  return (
    <APIProvider apiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!}>
      <Map
        style={{ width: '100%', height: '400px' }}
        defaultCenter={{ lat: 18.4655, lng: -66.1057 }}
        defaultZoom={12}
        mapId="YOUR_MAP_ID" // Required for AdvancedMarker
      >
        <AdvancedMarker position={{ lat: 18.4655, lng: -66.1057 }}>
          <Pin background="#0f9d58" borderColor="#006425" glyphColor="#60d98f" />
        </AdvancedMarker>
      </Map>
    </APIProvider>
  );
}
```

## Installation

```bash
npm install @vis.gl/react-google-maps
```

## Key Exports

```tsx
// Components
import {
  APIProvider,      // Wraps app, loads Maps JS API
  Map,              // Map container
  AdvancedMarker,   // Modern marker (requires mapId)
  Pin,              // Customizable pin for AdvancedMarker
  InfoWindow,       // Popup windows
  MapControl,       // Custom controls on map
  Marker,           // Legacy marker (deprecated)
} from '@vis.gl/react-google-maps';

// Hooks
import {
  useMap,                  // Access google.maps.Map instance
  useMapsLibrary,          // Load additional libraries (places, geocoding, drawing)
  useAdvancedMarkerRef,    // Connect marker to InfoWindow
  useApiIsLoaded,          // Check if API is loaded
} from '@vis.gl/react-google-maps';

// Enums
import {
  ControlPosition,     // For MapControl positioning
  CollisionBehavior,   // For marker collision handling
} from '@vis.gl/react-google-maps';
```

## Critical Requirements

1. **mapId is required for AdvancedMarker** - Create one at Google Cloud Console > Maps > Map Styles
2. **APIProvider must wrap all map components** - Place at app root or layout level
3. **Circle, Polygon, Polyline are NOT exported** - See `references/geometry-components.md` for implementations
4. **places.Autocomplete is deprecated** (March 2025) - Use AutocompleteService with custom UI instead

## Reference Files

Read these files based on the task:

| Task | Reference File |
|------|---------------|
| Map, Marker, InfoWindow, Pin details | `references/components-api.md` |
| useMap, useMapsLibrary, hooks | `references/hooks-api.md` |
| Circle, Polygon, Polyline | `references/geometry-components.md` |
| Places Autocomplete, Geocoding | `references/places-autocomplete.md` |
| Draggable markers + real-time sync, controlled maps | `references/patterns.md` |

## Common Patterns

### Marker with InfoWindow

```tsx
const MarkerWithInfo = ({ position }: { position: google.maps.LatLngLiteral }) => {
  const [markerRef, marker] = useAdvancedMarkerRef();
  const [open, setOpen] = useState(false);

  return (
    <>
      <AdvancedMarker ref={markerRef} position={position} onClick={() => setOpen(true)} />
      {open && (
        <InfoWindow anchor={marker} onClose={() => setOpen(false)}>
          <p>Hello!</p>
        </InfoWindow>
      )}
    </>
  );
};
```

### Draggable Marker with Real-Time Circle Sync

```tsx
const DraggableWithCircle = () => {
  const [position, setPosition] = useState({ lat: 18.4655, lng: -66.1057 });

  return (
    <>
      <AdvancedMarker
        position={position}
        draggable
        onDrag={(e) => {
          // Updates DURING drag for real-time sync
          if (e.latLng) setPosition({ lat: e.latLng.lat(), lng: e.latLng.lng() });
        }}
      />
      <Circle center={position} radius={1000} /> {/* Follows marker in real-time */}
    </>
  );
};
```

### Custom Map Control

```tsx
<Map {...props}>
  <MapControl position={ControlPosition.TOP_LEFT}>
    <button onClick={handleClick}>Custom Button</button>
  </MapControl>
</Map>
```

## TypeScript Types

```tsx
// Position types
type LatLngLiteral = { lat: number; lng: number };
type LatLngAltitudeLiteral = { lat: number; lng: number; altitude: number };

// Event types
type MapMouseEvent = google.maps.MapMouseEvent;
type AdvancedMarkerClickEvent = google.maps.marker.AdvancedMarkerClickEvent;

// Library types (from useMapsLibrary)
type PlacesLibrary = google.maps.PlacesLibrary;
type GeocodingLibrary = google.maps.GeocodingLibrary;
type DrawingLibrary = google.maps.DrawingLibrary;
```
