---
name: viewer-api
description: CRITICAL for Case Study viewer development. ALWAYS query Context7 FIRST before implementing any APS Viewer or Edit2D features. Provides Edit2D patterns, coordinate systems, and proven approaches. The viewer is 85% of user interaction - quality is non-negotiable.
---

# Autodesk APS Viewer & Edit2D Development

**CRITICAL**: The Case Study viewer is the primary user experience (85% of interaction time). Quality is non-negotiable. This skill documents proven patterns for the Autodesk Viewer JavaScript API.

---

## MANDATORY: Query Context7 FIRST

**BEFORE writing any Viewer or Edit2D code, ALWAYS query Context7:**

```
Library ID: /websites/aps_autodesk_en_viewer_v7
```

### How to Query

```typescript
// Step 1: Resolve library (if needed)
mcp__context7__resolve-library-id({
  libraryName: "Autodesk Viewer",
  query: "your specific question"
})

// Step 2: Query docs
mcp__context7__query-docs({
  libraryId: "/websites/aps_autodesk_en_viewer_v7",
  query: "Edit2D PolygonPath setEllipseArc circle shape"  // Be specific!
})
```

### Why This is Mandatory

Autodesk's documentation is scattered across:
- Official docs (incomplete for Edit2D)
- Stack Overflow answers
- GitHub issues
- Kean Walmsley's blog posts
- Autodesk forums

**Context7 has aggregated this knowledge.** We wasted hours trying `Shape.fromSVG()` with arc commands when `PolygonPath.setEllipseArc()` was documented in Context7 all along.

---

## Case Study Viewer Architecture

| File | Purpose |
|------|---------|
| `src/components/case-study-viewer/case-study-viewer.tsx` | Main viewer component |
| `src/components/case-study-viewer/edit2d-markers.ts` | Edit2D-based product markers |
| `src/components/case-study-viewer/hooks/` | Viewer initialization, events, coordinates |
| `src/components/case-study-viewer/placement-tool.ts` | Click-to-place tool |

---

## Edit2D Shape Classes

### Native Classes (USE THESE)

Edit2D provides native classes for programmatic shape creation. **Always prefer these over string-based methods.**

| Class | Use Case |
|-------|----------|
| `Autodesk.Edit2D.Polygon` | Closed shapes (rectangles, irregular polygons) |
| `Autodesk.Edit2D.Polyline` | Open lines |
| `Autodesk.Edit2D.PolygonPath` | Complex shapes with arc segments |
| `Autodesk.Edit2D.EllipseArcParams` | Arc definition for PolygonPath |

### Creating True Circles

**IMPORTANT**: Edit2D has NO Circle class. Circles are PolygonPath with arc segments:

```typescript
const Edit2D = window.Autodesk?.Edit2D

// 1. Create path with 2 diametrically opposite points
const polygonPath = new Edit2D.PolygonPath([
  { x: cx - radius, y: cy },  // Left point
  { x: cx + radius, y: cy }   // Right point
])

// 2. Define arc parameters
const params = new Edit2D.EllipseArcParams()
params.rx = radius
params.ry = radius
params.rotation = 0
params.largeArcFlag = false  // Semicircle is not "large"
params.sweepFlag = true      // Clockwise

// 3. Apply to both segments (top + bottom semicircles)
polygonPath.setEllipseArc(0, params)  // Top arc
polygonPath.setEllipseArc(1, params)  // Bottom arc

// 4. Style and add
polygonPath.style.lineColor = '#000000'
ctx.addShape(polygonPath)
```

### Creating Rectangles

```typescript
const polygon = new Edit2D.Polygon([
  { x: x, y: y },           // Top-left
  { x: x + w, y: y },       // Top-right
  { x: x + w, y: y + h },   // Bottom-right
  { x: x, y: y + h }        // Bottom-left
])
```

### Creating Lines

```typescript
const polyline = new Edit2D.Polyline([
  { x: x1, y: y1 },
  { x: x2, y: y2 }
])
```

---

## KNOWN PITFALLS

### Shape.fromSVG() Does NOT Support Arcs

```typescript
// ❌ WRONG - produces "Inf or NaN" errors
const shape = Edit2D.Shape.fromSVG(`<path d="M 0 50 A 50 50 0 1 0 100 50..." />`)

// ✅ CORRECT - use native PolygonPath.setEllipseArc()
const shape = new Edit2D.PolygonPath([...])
shape.setEllipseArc(0, params)
```

### Polygon Circle Approximation is Ugly

```typescript
// ❌ WRONG - 16-sided polygon looks jagged
const sides = 16
const points = []
for (let i = 0; i < sides; i++) {
  const angle = (i / sides) * Math.PI * 2
  points.push({ x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r })
}
const polygon = new Edit2D.Polygon(points)

// ✅ CORRECT - use PolygonPath.setEllipseArc() for smooth circles
```

### Coordinate System

Edit2D uses "page coordinates" which are the same as MarkupsCore:
- Origin (0,0) is typically at drawing center
- Conversion to/from DWG model coords requires `getPageToModelTransform()`

```typescript
// Page coords → DWG model coords
const transform = viewer.model.getPageToModelTransform(0)
const modelPoint = new THREE.Vector3(pageX, pageY, 0).applyMatrix4(transform)

// DWG model coords → Page coords
const inverse = transform.clone().invert()
const pagePoint = new THREE.Vector3(dwgX, dwgY, 0).applyMatrix4(inverse)
```

### Unit Scaling for Symbols

Product symbols are defined in mm. Convert to page units:

```typescript
const MM_TO_METERS = 0.001
const mmToPageUnits = MM_TO_METERS / (modelUnitScale * pageToModelScale)
const radiusInPageUnits = radiusMm * mmToPageUnits
```

---

## Viewer Extensions

### Edit2D Extension

```typescript
// Load extension
await viewer.loadExtension('Autodesk.Edit2D')
const edit2d = viewer.getExtension('Autodesk.Edit2D')

// Initialize context
edit2d.registerDefaultTools()
const ctx = edit2d.defaultContext

// Add shapes to layer
ctx.addShape(shape)
ctx.removeShape(shape)
ctx.clearLayer()
```

### Selection Events

```typescript
const selectionEvents = window.Autodesk?.Edit2D?.Selection?.Events
ctx.selection.addEventListener(
  selectionEvents.SELECTION_CHANGED,
  () => {
    const selected = ctx.selection.getSelectedShapes()
    // Handle selection...
  }
)
```

---

## Quick Reference: Context7 Queries

| Task | Query |
|------|-------|
| Circle/ellipse shapes | "Edit2D PolygonPath setEllipseArc EllipseArcParams" |
| Selection handling | "Edit2D selection getSelectedShapes" |
| Shape styles | "Edit2D shape style lineColor fillColor" |
| Coordinate transforms | "viewer getPageToModelTransform" |
| Tool activation | "Edit2D polygonEditTool activateTool" |
| SVG conversion | "Edit2D Shape fromSVG toSVG" |

---

## Implementation Checklist

Before implementing any Viewer/Edit2D feature:

- [ ] Query Context7 with specific terms
- [ ] Check if native Edit2D class exists (Polygon, Polyline, PolygonPath)
- [ ] Avoid string-based parsing (fromSVG) for complex shapes
- [ ] Handle coordinate system transformations
- [ ] Test with actual marker placement
- [ ] Verify no console errors (especially "Inf or NaN")

---

## See Also

- Case Study feature: [docs/features/case-study.md](../../docs/features/case-study.md)
- Edit2D Context7 docs: `/websites/aps_autodesk_en_viewer_v7`
- Component: `src/components/case-study-viewer/`
