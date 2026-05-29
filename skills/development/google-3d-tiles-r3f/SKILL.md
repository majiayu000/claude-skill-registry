---
name: google-3d-tiles-r3f
description: Builds a 3D world using Google Maps Photorealistic 3D Tiles API with Three.js and React Three Fiber (R3F), including ECEF-to-ENU coordinate correction for a flat local coordinate system. Use when integrating Google 3D Tiles, Google Earth tiles, 3d-tiles-renderer, R3F map scenes, or when correcting 座標系 (coordinate systems) from ECEF to ENU for camera, physics, or audio positioning.
---

# Google 3D Tiles with R3F and ENU Coordinates

## When to Use This Skill

- Integrating **Google Maps Photorealistic 3D Tiles** or **Google Earth 3D Tiles API** into a web app
- Building a **Three.js** or **React Three Fiber (R3F)** scene that displays real-world 3D terrain/buildings
- Correcting **座標系 (coordinate systems)**: converting **ECEF** (Earth-Centered, Earth-Fixed) to **ENU** (East-North-Up) so the map is flat and Y-up for gameplay, camera, or audio
- Placing objects (camera, vehicles, audio sources) in the same coordinate system as the tiles

## Quick Overview

1. **Tiles**: Google 3D Tiles are served in **ECEF**. Use `3d-tiles-renderer` with `TilesRenderer` (R3F) and `GoogleCloudAuthPlugin` (API key).
2. **R3F**: Render tiles inside a `<Canvas>`; wrap `TilesRenderer` in a **transformer group** that applies an ECEF→ENU matrix so the scene is local and Y-up.
3. **Consistency**: Use a single **origin** (e.g. city center). Convert all lat/lng/alt to ENU with that origin so camera, physics, and tiles share the same 座標系.

## Stack and Packages

- **three** + **@react-three/fiber** (R3F)
- **3d-tiles-renderer** (provides `TilesRenderer`, `TilesPlugin`, `WGS84_ELLIPSOID`, `GoogleCloudAuthPlugin`, `GLTFExtensionsPlugin`)
- Optional: **three/examples/jsm/loaders/DRACOLoader** for compressed tiles

Google Tiles root URL: `https://tile.googleapis.com/v1/3dtiles/root.json`. API key required (Google Cloud Maps API / 3D Tiles).

## Coordinate Correction (ECEF → ENU)

- **ECEF**: Earth-centered, Cartesian. Tiles from Google are in ECEF.
- **ENU**: East-North-Up at a chosen origin. X=east, Y=north, Z=up (then remap to Three.js Y-up: X=east, Y=up, Z=-north so north is -Z).

**Steps:**

1. Get ENU→ECEF at origin (lat, lng) using WGS84 ellipsoid (e.g. `WGS84_ELLIPSOID.getEastNorthUpFrame` from `3d-tiles-renderer/three`), then invert to get **ECEF→ENU**.
2. Apply a **Y-up remap** so Three.js convention is X=east, Y=up, Z=-north (geographic north = -Z).
3. Set this matrix on the **parent group** of the tiles (e.g. the group that wraps `TilesRenderer`), and set `matrixAutoUpdate = false`.

All other scene objects (camera, entities) should use the **same origin** and the same ENU↔lat/lng conversion (e.g. `latLngAltToENU` / `enuToLatLngAlt`) so positions align with the transformed tiles.

## Checklist

- [ ] R3F `Canvas` with appropriate camera near/far and optional `logarithmicDepthBuffer` for large scenes
- [ ] Tiles: `TilesRenderer` wrapped in a group; apply ECEF→ENU+Y-up matrix to that group once on mount
- [ ] Auth: `TilesPlugin` with `GoogleCloudAuthPlugin` and `apiToken` (API key)
- [ ] Optional: `GLTFExtensionsPlugin` + DRACOLoader for Draco tiles
- [ ] Single origin (e.g. `ORIGIN_LAT`, `ORIGIN_LNG`); all lat/lng/alt converted to ENU relative to that origin
- [ ] Geo utils: `latLngAltToENU` and `enuToLatLngAlt` use the same Y-up remap (Z = -north) as the tiles transform

## Additional Resources

- **[reference.md](reference.md)** — Concepts and 座標系 summary; all code lives in **examples/** so the skill is project-agnostic.
- **[examples/](examples/)** — Copy-paste files: config, geo-utils, ECEF→ENU matrix + TilesTransformer, TilesScene, page snippet. See [examples/README.md](examples/README.md) for copy-to-path mapping.
