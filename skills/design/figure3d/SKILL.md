---
name: figure3d
description: Create 3D geometric solid visualizations (cubes, prisms, pyramids, cylinders, cones, spheres) with SVG projections. Use when rendering 3D figures in mini-lessons or geometry questions.
---

# Figure3D Skill

This skill guides you through creating 3D solid visualizations using the `Figure3D` component. The component renders 3D geometric solids as 2D SVG projections.

## When to Use This Skill

Invoke this skill when:
- Creating geometry mini-lessons involving 3D solids
- Rendering cubes, prisms, pyramids, cylinders, cones, or spheres in practice questions
- Visualizing volume and surface area concepts
- Building interactive 3D explorations with rotation
- Demonstrating spatial geometry for PAES curriculum

## Supported Solids (Spanish)

| Type | Spanish Name | Description |
|------|--------------|-------------|
| `cubo` | Cubo | Cube with equal sides |
| `prisma_rectangular` | Prisma Rectangular | Rectangular prism/cuboid |
| `prisma_triangular` | Prisma Triangular | Prism with triangular base |
| `piramide_cuadrada` | Piramide Cuadrada | Square pyramid |
| `piramide_triangular` | Piramide Triangular | Triangular pyramid/tetrahedron |
| `cilindro` | Cilindro | Cylinder |
| `cono` | Cono | Cone |
| `esfera` | Esfera | Sphere |

## Quick Start

### Cubo simple

```tsx
import { Figure3D } from '@/components/figures/Figure3D';

// Cubo de lado 100
<Figure3D
  fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
/>
```

### Prisma rectangular

```tsx
// Prisma rectangular (largo x ancho x altura)
<Figure3D
  fromType={{
    type: 'prisma_rectangular',
    dimensions: { largo: 120, ancho: 80, altura: 100 },
  }}
  showGrid
/>
```

### Piramide con altura visible

```tsx
// Piramide cuadrada con linea de altura
<Figure3D
  fromType={{
    type: 'piramide_cuadrada',
    dimensions: { base: 100, altura: 120 },
  }}
  heightLine={{ show: true, showRightAngleMarker: true }}
  dimensionLabels={{ showHeight: true, showBase: true }}
/>
```

### Cilindro

```tsx
// Cilindro con radio y altura
<Figure3D
  fromType={{
    type: 'cilindro',
    dimensions: { radio: 50, altura: 100 },
  }}
  dimensionLabels={{ showRadius: true, showHeight: true }}
/>
```

### Cono

```tsx
// Cono con altura y base resaltada
<Figure3D
  fromType={{
    type: 'cono',
    dimensions: { radio: 60, altura: 100 },
  }}
  faceConfig={{ highlightBase: true }}
  heightLine={{ show: true }}
/>
```

### Esfera

```tsx
// Esfera (renderizada con gradiente radial)
<Figure3D
  fromType={{
    type: 'esfera',
    dimensions: { radio: 80 },
  }}
/>
```

### Con proyeccion y rotacion interactiva

```tsx
// Cubo interactivo con rotacion por mouse/touch
<Figure3D
  fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
  projection="isometric"
  interactive
  onRotationChange={(azimuth, elevation) => {
    console.log('Rotacion:', azimuth, elevation);
  }}
/>
```

### Aristas ocultas visibles (punteadas)

```tsx
// Muestra aristas traseras con lineas punteadas
<Figure3D
  fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
  edges={{ hiddenEdgeStyle: 'dashed' }}
/>
```

### Aristas ocultas invisibles

```tsx
// Solo muestra aristas frontales
<Figure3D
  fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
  edges={{ hiddenEdgeStyle: 'none' }}
/>
```

---

## Props Reference

### Construction (use ONE of these)

| Prop | Type | Description |
|------|------|-------------|
| `fromType` | `SolidDimensions` | **Recommended.** Build from solid type with dimensions |
| `vertices` | `Point3D[]` | Custom vertices for advanced use |
| `faces` | `number[][]` | Custom faces (array of vertex indices per face) |
| `customEdges` | `[number, number][]` | Custom edges (pairs of vertex indices) |

### SolidDimensions

```typescript
// Union type - use the appropriate dimensions for the solid type
type SolidDimensions =
  | { type: 'cubo'; dimensions: { lado: number } }
  | { type: 'prisma_rectangular'; dimensions: { largo: number; ancho: number; altura: number } }
  | { type: 'prisma_triangular'; dimensions: { baseWidth: number; baseHeight: number; profundidad: number } }
  | { type: 'piramide_cuadrada'; dimensions: { base: number; altura: number } }
  | { type: 'piramide_triangular'; dimensions: { base: number; altura: number } }
  | { type: 'cilindro'; dimensions: { radio: number; altura: number } }
  | { type: 'cono'; dimensions: { radio: number; altura: number } }
  | { type: 'esfera'; dimensions: { radio: number } };
```

### Projection Settings

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `projection` | `ProjectionType \| ProjectionConfig` | `'isometric'` | Projection type or full config |
| `azimuth` | `number` | `45` | Horizontal rotation (0-360 degrees) |
| `elevation` | `number` | `35` | Vertical angle (-90 to 90 degrees) |

### ProjectionType

```typescript
type ProjectionType = 'isometric' | 'cavalier' | 'cabinet' | 'dimetric';
```

| Type | Description | Depth Scale |
|------|-------------|-------------|
| `isometric` | Equal foreshortening on all axes (30 degrees) | 1.0 |
| `cavalier` | Oblique with full-scale depth | 1.0 |
| `cabinet` | Oblique with half-scale depth | 0.5 |
| `dimetric` | Two axes equally foreshortened | 0.5 |

### Interactive Rotation

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `interactive` | `boolean` | `false` | Enable mouse/touch drag rotation |
| `onRotationChange` | `(azimuth, elevation) => void` | - | Callback when rotation changes |

### Edge Configuration

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `edges.hiddenEdgeStyle` | `'dashed' \| 'dotted' \| 'none'` | `'dashed'` | How to render back-facing edges |
| `edges.edgeColor` | `string` | `'rgb(59, 130, 246)'` | Color for visible edges |
| `edges.edgeWidth` | `number` | `2` | Stroke width for edges |
| `edges.hiddenEdgeColor` | `string` | `'rgb(156, 163, 175)'` | Color for hidden edges |

### Face Configuration

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `faceConfig.fill` | `string` | `'rgba(59, 130, 246, 0.15)'` | Face fill color |
| `faceConfig.fillOpacity` | `number` | - | Face fill opacity |
| `faceConfig.highlightBase` | `boolean` | `false` | Highlight base face(s) |
| `faceConfig.highlightLateral` | `boolean` | `false` | Highlight lateral faces |
| `faceConfig.baseColor` | `string` | `'rgba(168, 85, 247, 0.3)'` | Base highlight color |
| `faceConfig.lateralColor` | `string` | - | Lateral highlight color |

### Height Line Configuration

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `heightLine.show` | `boolean` | `false` | Show height (altura) line |
| `heightLine.style` | `'solid' \| 'dashed' \| 'dotted'` | `'dashed'` | Line style |
| `heightLine.color` | `string` | `'rgb(239, 68, 68)'` | Line color (red) |
| `heightLine.showRightAngleMarker` | `boolean` | `false` | Show right angle marker at base |

### Dimension Labels

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `dimensionLabels.showHeight` | `boolean` | `false` | Show altura label |
| `dimensionLabels.showBase` | `boolean` | `false` | Show base dimension |
| `dimensionLabels.showRadius` | `boolean` | `false` | For cylinders, cones, spheres |
| `dimensionLabels.showEdge` | `boolean` | `false` | Show edge length (for cubes) |
| `dimensionLabels.heightLabel` | `string` | `'h'` | Custom height label |
| `dimensionLabels.baseLabel` | `string` | - | Custom base label |
| `dimensionLabels.radiusLabel` | `string` | `'r'` | Custom radius label |

### Vertex Labels

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `vertexLabels.show` | `boolean` | `false` | Show vertex labels |
| `vertexLabels.labels` | `string[]` | - | Custom labels for vertices |
| `vertexLabels.fontSize` | `number` | `12` | Label font size |

### Visual Styling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fill` | `string` | `'rgba(59, 130, 246, 0.15)'` | Default face fill color |
| `fillOpacity` | `number` | - | Fill opacity |
| `stroke` | `string` | `'rgb(59, 130, 246)'` | Default edge stroke color |
| `strokeWidth` | `number` | `2` | Edge stroke width |

### Grid and Background

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showGrid` | `boolean` | `false` | Show background grid |
| `gridSize` | `number` | `20` | Grid cell size in pixels |
| `gridColor` | `string` | `'rgb(229, 231, 235)'` | Grid line color |

### SVG Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `number` | auto | SVG width |
| `height` | `number` | auto | SVG height |
| `viewBox` | `string` | auto | Custom viewBox |
| `padding` | `number` | `40` | Padding around the figure |
| `className` | `string` | - | CSS class name |
| `ariaLabel` | `string` | - | Aria label for accessibility |
| `standalone` | `boolean` | `true` | `true`: renders `<svg>`, `false`: renders `<g>` |

---

## Common Patterns

### Volumen del Cubo

```tsx
<Figure3D
  fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
  dimensionLabels={{ showEdge: true, edgeLabel: 'a' }}
  showGrid
/>
// Volumen = a^3
```

### Volumen del Prisma Rectangular

```tsx
<Figure3D
  fromType={{
    type: 'prisma_rectangular',
    dimensions: { largo: 120, ancho: 80, altura: 100 },
  }}
  dimensionLabels={{
    showHeight: true,
    showBase: true,
  }}
/>
// Volumen = largo x ancho x altura
```

### Volumen y Area de la Piramide

```tsx
<Figure3D
  fromType={{
    type: 'piramide_cuadrada',
    dimensions: { base: 100, altura: 120 },
  }}
  faceConfig={{ highlightBase: true }}
  heightLine={{ show: true, showRightAngleMarker: true }}
  dimensionLabels={{ showHeight: true, showBase: true }}
/>
// Volumen = (1/3) x base^2 x altura
```

### Volumen del Cilindro

```tsx
<Figure3D
  fromType={{
    type: 'cilindro',
    dimensions: { radio: 50, altura: 100 },
  }}
  faceConfig={{ highlightBase: true }}
  dimensionLabels={{ showRadius: true, showHeight: true }}
/>
// Volumen = pi x r^2 x h
// Area = 2 x pi x r x (r + h)
```

### Volumen del Cono

```tsx
<Figure3D
  fromType={{
    type: 'cono',
    dimensions: { radio: 60, altura: 100 },
  }}
  heightLine={{ show: true, showRightAngleMarker: true }}
  dimensionLabels={{ showRadius: true, showHeight: true }}
/>
// Volumen = (1/3) x pi x r^2 x h
```

### Volumen de la Esfera

```tsx
<Figure3D
  fromType={{
    type: 'esfera',
    dimensions: { radio: 80 },
  }}
  dimensionLabels={{ showRadius: true }}
/>
// Volumen = (4/3) x pi x r^3
// Area = 4 x pi x r^2
```

### Comparacion de Solidos

```tsx
// Cubo y piramide lado a lado
<div className="flex gap-4">
  <Figure3D
    fromType={{ type: 'cubo', dimensions: { lado: 80 } }}
    width={200}
    height={200}
  />
  <Figure3D
    fromType={{
      type: 'piramide_cuadrada',
      dimensions: { base: 80, altura: 80 },
    }}
    width={200}
    height={200}
  />
</div>
```

---

## Color Palette

| Elemento | Color | CSS Value |
|----------|-------|-----------|
| Face fill | Blue 500 (15%) | `rgba(59, 130, 246, 0.15)` |
| Edge stroke | Blue 500 | `rgb(59, 130, 246)` |
| Hidden edge | Gray 400 | `rgb(156, 163, 175)` |
| Base highlight | Purple 500 (30%) | `rgba(168, 85, 247, 0.3)` |
| Height line | Red 500 | `rgb(239, 68, 68)` |
| Grid | Gray 200 | `rgb(229, 231, 235)` |
| Labels | Gray 700 | `rgb(55, 65, 81)` |

---

## Debug Page

Para experimentar interactivamente con todas las opciones:

**URL:** `/admin/figure-debug`

Selecciona "Figura 3D" en el selector de tipo de figura.

La pagina de debug permite:
- Seleccionar tipo de solido (cubo, prisma, piramide, cilindro, cono, esfera)
- Ajustar dimensiones con sliders dinamicos por tipo
- Cambiar proyeccion (isometrica, cavalier, cabinet, dimetrica)
- Ajustar angulos de rotacion (azimut y elevacion)
- Activar/desactivar rotacion interactiva
- Opciones visuales:
  - Mostrar/ocultar aristas ocultas
  - Resaltar base
  - Mostrar linea de altura
  - Mostrar etiquetas de dimensiones
  - Mostrar grid
- Ver propiedades calculadas (volumen, area superficial)
- Copiar el codigo generado

---

## Integration with Mini-Lessons

### In Step Components

```tsx
// En Step2Explore.tsx
import { Figure3D } from '@/components/figures/Figure3D';

export default function Step2Explore({ isActive }: LessonStepProps) {
  const [showHeight, setShowHeight] = useState(false);
  const [altura, setAltura] = useState(100);

  return (
    <div className="flex flex-col items-center">
      <Figure3D
        fromType={{
          type: 'piramide_cuadrada',
          dimensions: { base: 100, altura },
        }}
        heightLine={{ show: showHeight, showRightAngleMarker: true }}
      />

      <div className="mt-4 space-y-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={showHeight}
            onChange={(e) => setShowHeight(e.target.checked)}
          />
          Mostrar altura
        </label>

        <input
          type="range"
          min="50"
          max="150"
          value={altura}
          onChange={(e) => setAltura(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
```

### Interactive Rotation

```tsx
export default function Step3Explore({ isActive }: LessonStepProps) {
  const [azimuth, setAzimuth] = useState(45);
  const [elevation, setElevation] = useState(35);

  return (
    <div className="flex flex-col items-center">
      <Figure3D
        fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
        interactive
        azimuth={azimuth}
        elevation={elevation}
        onRotationChange={(newAzimuth, newElevation) => {
          setAzimuth(newAzimuth);
          setElevation(newElevation);
        }}
      />
      <Text size="sm" className="mt-2">
        Arrastra para rotar la figura
      </Text>
    </div>
  );
}
```

### With Animation

```tsx
import { motion } from 'framer-motion';

// Wrap Figure3D in motion.div for animations
<motion.div
  initial={{ opacity: 0, scale: 0.8 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.5 }}
>
  <Figure3D
    fromType={{ type: 'cubo', dimensions: { lado: 100 } }}
  />
</motion.div>
```

---

## Utility Functions

Las funciones matematicas estan disponibles en `@/lib/geometry/figure3d`:

```typescript
import {
  // Volume calculations
  volumeCubo,
  volumePrismaRectangular,
  volumePrismaTriangular,
  volumePiramideCuadrada,
  volumePiramideTriangular,
  volumeCilindro,
  volumeCono,
  volumeEsfera,

  // Surface area calculations
  areaSuperficieCubo,
  areaSuperficiePrismaRectangular,
  areaSuperficieCilindro,
  areaSuperficieCono,
  areaSuperficieEsfera,

  // Solid generators
  generateCube,
  generatePrismaRectangular,
  generatePrismaTriangular,
  generatePiramideCuadrada,
  generatePiramideTriangular,
  generateCilindro,
  generateCono,
  generateEsfera,
  generateSolid,  // Unified generator

  // Vector math
  vec3Add,
  vec3Subtract,
  vec3Scale,
  vec3Dot,
  vec3Cross,
  vec3Normalize,
  vec3Length,
  vec3Centroid,

  // Rotation
  rotateX,
  rotateY,
  rotateZ,
  rotatePoint,

  // Projection
  project3Dto2D,
  projectVertices,
  normalizeProjectionConfig,

  // Visibility
  calculateFaceNormal,
  isFaceFrontFacing,
  sortFacesByDepth,
  getEdgeVisibility,
  getAllEdgeVisibilities,

  // Validation
  validateCubeDimensions,
  validatePrismaRectangularDimensions,
  validateCilindroDimensions,
  validateConoDimensions,
  validateEsferaDimensions,

  // Names
  getSolidTypeName,  // Returns Spanish name for solid type
} from '@/lib/geometry/figure3d';
```

### Example Usage

```typescript
import {
  volumeCubo,
  volumeCilindro,
  areaSuperficieCubo,
  areaSuperficieCilindro,
} from '@/lib/geometry/figure3d';

// Cube with side 5
const cubeVol = volumeCubo(5);                // 125
const cubeArea = areaSuperficieCubo(5);       // 150

// Cylinder with radius 3 and height 10
const cylVol = volumeCilindro(3, 10);         // 282.74...
const cylArea = areaSuperficieCilindro(3, 10); // 245.04...
```

---

## Rendering Details

### Face Sorting (Painter's Algorithm)

Faces are rendered back-to-front using the painter's algorithm:
1. Calculate depth (z-coordinate) of each face centroid after projection
2. Sort faces by depth (farthest first)
3. Render faces in order so front faces paint over back faces

### Edge Visibility

Edge visibility is determined by the faces they belong to:
- **Visible edges**: Connected to at least one front-facing face
- **Hidden edges**: Only connected to back-facing faces
- **Silhouette edges**: Connected to one front-facing and one back-facing face

### Sphere Rendering

Spheres are a special case - they're not polyhedra and are rendered as:
1. A circle with the projected radius
2. A radial gradient for 3D shading effect
3. Optional radius line and label

---

## Angle Convention

Rotation angles follow standard 3D conventions:
- **Azimuth (0-360)**: Horizontal rotation around the vertical (Y) axis
- **Elevation (-90 to 90)**: Vertical angle from the horizontal plane

```
           +Y (up)
            |
            |
            +--- +X (right)
           /
          /
        +Z (toward viewer)
```

Default isometric view: `azimuth: 45`, `elevation: 35.264` (arctan(1/sqrt(2)))
