---
name: using-cesiumjs-skills
description: Use when starting any conversation involving CesiumJS development - provides orientation on available domain skills and how they activate
---

# CesiumJS Skills Orientation

This plugin provides 14 domain skills covering CesiumJS v1.139 (~535 public symbols). Skills activate passively via description matching — no explicit invocation is required.

## Available Skills

| Skill | Use when... |
|---|---|
| `cesiumjs-viewer-setup` | Initializing a CesiumJS app, configuring widgets, setting Ion tokens, bootstrapping a globe |
| `cesiumjs-camera` | Positioning the camera, flyTo animations, constraining navigation, entity tracking |
| `cesiumjs-entities` | Adding points/labels/models/polygons, loading GeoJSON/KML/CZML/GPX data |
| `cesiumjs-3d-tiles` | Loading tilesets, styling features, querying metadata, voxels, point clouds, clipping |
| `cesiumjs-imagery` | Adding/swapping base map layers, configuring imagery providers, split-screen comparisons |
| `cesiumjs-terrain-environment` | Configuring terrain, querying heights, atmosphere/sky/fog/lighting/shadows, panoramas |
| `cesiumjs-primitives` | Performance-critical static geometry, custom shapes, batching, billboard/label/point collections |
| `cesiumjs-materials-shaders` | Fabric materials, ImageBasedLighting, post-processing effects, bloom, tonemapping |
| `cesiumjs-custom-shader` | Writing GLSL shader bodies for Model/Cesium3DTileset/VoxelPrimitive; reading feature IDs or structural metadata inside a shader |
| `cesiumjs-time-properties` | Time-dynamic entity attributes, simulation clock, interpolation, sampled/callback properties |
| `cesiumjs-spatial-math` | Coordinate conversions, ellipsoid geometry, model matrices, intersection tests, projections |
| `cesiumjs-interaction` | User clicks on the globe, entity/feature selection, hover effects, drag interactions |
| `cesiumjs-models-particles` | glTF/GLB model loading, animations, particle effects (fire, smoke) |
| `cesiumjs-core-utilities` | HTTP requests via Resource, Color, Event, error handling, helper functions |

## Cross-Domain Questions

When a question spans multiple domains, consult `docs/DOMAINS.md` — the definitive ownership map assigning every public CesiumJS class, function, and enum to exactly one skill.

## Runtime Verification

Chrome DevTools MCP is available for browser-based iteration: console error checking, network inspection, screenshots, and Lighthouse audits.
