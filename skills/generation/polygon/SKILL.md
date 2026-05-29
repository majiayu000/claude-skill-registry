---
name: polygon
description: Create polygon geometry figures with vertices, angles, diagonals, apothem, and center. Use when rendering regular polygons (5-12 sides) in mini-lessons or geometry questions.
---

# Polygon Figure Skill

This skill guides you through creating polygon visualizations using the `PolygonFigure` component. Supports regular and irregular polygons with 5-12 sides.

## When to Use This Skill

Invoke this skill when:
- Creating geometry mini-lessons involving polygons (5+ sides)
- Rendering regular polygons (pentagon, hexagon, etc.) in practice questions
- Visualizing polygon properties (interior angles, diagonals, apothem)
- Building interactive polygon explorations
- Demonstrating suma de angulos interiores, diagonales, apotema, etc.

## Quick Start

### Regular polygon (simplest)

```tsx
import { PolygonFigure } from '@/components/figures/PolygonFigure';

// Hexagon with center point
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  showCenter
/>

// Pentagon with grid
<PolygonFigure
  fromRegular={{ sides: 5, radius: 80 }}
  showGrid
/>
```

### With apothem line

```tsx
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  showCenter
  showApothem={{ label: 'a' }}
/>
```

### With all diagonals

```tsx
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  diagonals="all"
/>
```

### With interior angle arcs

```tsx
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  angles={[
    { showArc: true, showDegrees: true },
    { showArc: true, showDegrees: true },
    { showArc: true, showDegrees: true },
    { showArc: true, showDegrees: true },
    { showArc: true, showDegrees: true },
    { showArc: true, showDegrees: true },
  ]}
/>
```

### With edge labels

```tsx
<PolygonFigure
  fromRegular={{ sides: 5, radius: 80 }}
  edges={[
    { label: 'a' },
    { label: 'b' },
    { label: 'c' },
    { label: 'd' },
    { label: 'e' },
  ]}
/>
```

### Specific diagonals

```tsx
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  diagonals={[
    { from: 0, to: 3, label: 'd1' },
    { from: 1, to: 4, label: 'd2' },
  ]}
/>
```

### Custom vertices (irregular polygon)

```tsx
<PolygonFigure
  vertices={[
    { x: 200, y: 50, label: 'A' },
    { x: 300, y: 100, label: 'B' },
    { x: 280, y: 200, label: 'C' },
    { x: 180, y: 220, label: 'D' },
    { x: 100, y: 150, label: 'E' },
  ]}
  showGrid
/>
```

---

## Props Reference

### Construction (use ONE of these)

| Prop | Type | Description |
|------|------|-------------|
| `fromRegular` | `FromRegularConfig` | **Recommended.** Build regular polygon from sides and radius |
| `vertices` | `LabeledPoint[]` | Custom vertices for irregular polygons (min 5) |

### FromRegularConfig

```typescript
interface FromRegularConfig {
  sides: number;      // Number of sides (5-12)
  radius: number;     // Circumradius (distance from center to vertices)
  rotation?: number;  // Rotation in degrees (default: -90, starts from top)
  centerX?: number;   // Center X coordinate (default: 200)
  centerY?: number;   // Center Y coordinate (default: 150)
}
```

### LabeledPoint

```typescript
interface LabeledPoint {
  x: number;          // X coordinate
  y: number;          // Y coordinate
  label?: string;     // Vertex label (e.g., 'A', 'B', 'C')
}
```

### Edge Configuration

```typescript
interface PolygonEdgeConfig {
  label?: string;           // Edge label (e.g., 'a', 'b', 'c')
  measurement?: string;     // Measurement with units (e.g., '5 cm')
  color?: string;           // Custom color
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  strokeWidth?: number;
  showMeasurement?: boolean;
}
```

### Angle Configuration

```typescript
interface PolygonAngleConfig {
  label?: string;        // Label (degrees or Greek letter)
  showArc?: boolean;     // Show angle arc
  arcRadius?: number;    // Arc radius (default: 25)
  color?: string;        // Custom color
  showDegrees?: boolean; // Show degree value (e.g., '108°')
}
```

### Diagonal Configuration

```typescript
interface DiagonalConfig {
  from: number;  // Starting vertex index (0-based)
  to: number;    // Ending vertex index (0-based)
  label?: string;
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
}
```

### Apothem Configuration

```typescript
interface ApothemConfig {
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  label?: string;           // Label (e.g., 'a', 'apotema')
  showMeasurement?: boolean;
  toEdge?: number;          // Which edge to draw to (0-based index)
}
```

### Display Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `edges` | `PolygonEdgeConfig[]` | - | Edge labels and measurements |
| `angles` | `PolygonAngleConfig[]` | - | Angle arcs and labels |
| `diagonals` | `DiagonalConfig[] \| 'all'` | - | Specific diagonals or all |
| `showApothem` | `boolean \| ApothemConfig` | `false` | Show apothem line |
| `showCenter` | `boolean` | `false` | Show center point |
| `centerLabel` | `string` | `'O'` | Label for center point |

### Visual Styling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fill` | `string` | `'rgba(59,130,246,0.15)'` | Fill color |
| `fillOpacity` | `number` | - | Fill opacity |
| `stroke` | `string` | `'rgb(59,130,246)'` | Stroke color |
| `strokeWidth` | `number` | `2` | Stroke width |
| `showVertices` | `boolean` | `true` | Show vertex points |
| `vertexRadius` | `number` | `4` | Vertex point radius |

### Grid and Background

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showGrid` | `boolean` | `false` | Show grid background |
| `gridSize` | `number` | `20` | Grid cell size |
| `gridColor` | `string` | `'rgb(229,231,235)'` | Grid color |

### SVG Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `number` | auto | SVG width |
| `height` | `number` | auto | SVG height |
| `viewBox` | `string` | auto | Custom viewBox |
| `padding` | `number` | `40` | Padding around polygon |
| `className` | `string` | - | Additional CSS classes |
| `ariaLabel` | `string` | - | Accessibility label |

---

## Common Patterns

### Interior Angles Sum

```tsx
// Regular hexagon showing all interior angles
// Sum = (n-2) * 180 = (6-2) * 180 = 720°
// Each angle = 720/6 = 120°
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  angles={Array.from({ length: 6 }, () => ({
    showArc: true,
    showDegrees: true,
  }))}
/>
```

### Diagonals Count

```tsx
// Hexagon with all diagonals
// Number of diagonals = n(n-3)/2 = 6(6-3)/2 = 9
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  diagonals="all"
  showCenter
/>
```

### Apothem and Area

```tsx
// Pentagon with apothem (for area calculation)
// Area = (perimeter * apothem) / 2
<PolygonFigure
  fromRegular={{ sides: 5, radius: 80 }}
  showCenter
  showApothem={{ label: 'a', strokeStyle: 'dashed' }}
  edges={[
    { label: 's' },  // One side labeled for perimeter
    {},
    {},
    {},
    {},
  ]}
/>
```

### Regular vs Irregular

```tsx
// Regular octagon
<PolygonFigure
  fromRegular={{ sides: 8, radius: 80 }}
  showCenter
/>

// Irregular pentagon (custom vertices)
<PolygonFigure
  vertices={[
    { x: 200, y: 30, label: 'A' },
    { x: 320, y: 100, label: 'B' },
    { x: 280, y: 220, label: 'C' },
    { x: 120, y: 220, label: 'D' },
    { x: 80, y: 100, label: 'E' },
  ]}
/>
```

### Complete Polygon Info

```tsx
// Hexagon with all features
<PolygonFigure
  fromRegular={{ sides: 6, radius: 80 }}
  showCenter
  centerLabel="O"
  showApothem={{ label: 'a' }}
  edges={[
    { label: 'l' },
    {},
    {},
    {},
    {},
    {},
  ]}
  angles={[
    { showArc: true, showDegrees: true },
    {},
    {},
    {},
    {},
    {},
  ]}
  showGrid
/>
```

---

## Spanish Polygon Names

| Sides | Spanish Name | English |
|-------|--------------|---------|
| 5 | pentagono | pentagon |
| 6 | hexagono | hexagon |
| 7 | heptagono | heptagon |
| 8 | octagono | octagon |
| 9 | eneagono | nonagon |
| 10 | decagono | decagon |
| 11 | endecagono | hendecagon |
| 12 | dodecagono | dodecagon |

---

## Color Palette

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Polygon fill | `rgba(59,130,246,0.15)` | - |
| Polygon stroke | `rgb(59,130,246)` | `stroke-blue-400` |
| Angle arc | `rgb(245,158,11)` | `stroke-amber-400` |
| Diagonal | `rgb(168,85,247)` | `stroke-purple-400` |
| Apothem | `rgb(16,185,129)` | `stroke-emerald-400` |
| Center point | `rgb(239,68,68)` | `fill-red-400` |
| Grid | `rgb(229,231,235)` | `stroke-gray-700` |
| Vertex | `rgb(17,24,39)` | `fill-white` |

---

## Debug Page

For interactive experimentation with all options:

**URL:** `/admin/figure-debug`

Select "Poligono" in the figure type selector.

The debug page allows:
- Adjust number of sides (5-12) with slider
- Adjust radius and rotation
- Toggle center point, apothem, diagonals
- Toggle edge labels and angle arcs
- Select presets (Pentagon, Hexagon, Octagon, Decagon, Dodecagon)
- View calculated properties (interior angle, diagonal count, apothem, side length)
- Copy generated code

---

## Integration with Mini-Lessons

### In Step Components

```tsx
// En Step2Explore.tsx
import { PolygonFigure } from '@/components/figures/PolygonFigure';

export default function Step2Explore({ isActive }: LessonStepProps) {
  const [sides, setSides] = useState(6);
  const [showDiagonals, setShowDiagonals] = useState(false);

  return (
    <div className="flex flex-col items-center">
      <PolygonFigure
        fromRegular={{ sides, radius: 80 }}
        showCenter
        diagonals={showDiagonals ? 'all' : undefined}
      />

      <div className="mt-4 space-y-2">
        <label className="flex items-center gap-2">
          <span>Lados:</span>
          <input
            type="range"
            min="5"
            max="12"
            value={sides}
            onChange={(e) => setSides(Number(e.target.value))}
          />
          <span>{sides}</span>
        </label>

        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={showDiagonals}
            onChange={(e) => setShowDiagonals(e.target.checked)}
          />
          Mostrar diagonales
        </label>
      </div>
    </div>
  );
}
```

### With Animation

```tsx
import { motion } from 'framer-motion';

// Wrap PolygonFigure in motion.div for animations
<motion.div
  initial={{ opacity: 0, rotate: -10 }}
  animate={{ opacity: 1, rotate: 0 }}
  transition={{ duration: 0.5 }}
>
  <PolygonFigure
    fromRegular={{ sides: 6, radius: 80 }}
    showCenter
  />
</motion.div>
```

---

## Utility Functions

Mathematical functions available in `@/lib/geometry/polygonUtils`:

```typescript
import {
  // Construction
  buildRegularPolygon,      // Build vertices for regular polygon
  polygonPath,              // SVG path string

  // Calculations
  polygonCentroid,          // Center point of polygon
  polygonArea,              // Area of polygon
  polygonSignedArea,        // Signed area (for orientation)
  angleAtVertex,            // Angle at a specific vertex
  regularInteriorAngle,     // Interior angle for regular polygon
  regularExteriorAngle,     // Exterior angle for regular polygon
  calculateApothem,         // Apothem of regular polygon
  calculateSideLength,      // Side length of regular polygon
  diagonalCount,            // Number of diagonals: n(n-3)/2
  calculateAllDiagonals,    // All diagonal pairs [from, to]

  // Geometry helpers
  distance,                 // Distance between points
  midpoint,                 // Midpoint of two points
  calculateApothemLine,     // Apothem line endpoints

  // Label positioning
  calculateVertexLabelPosition,
  calculateEdgeLabelPosition,
  calculateDiagonalLabelPosition,

  // Angle visualization
  describeAngleArc,         // SVG path for angle arc

  // Validation
  validatePolygon,          // Validate sides and radius
  validateVertices,         // Validate vertex array
  isRegular,                // Check if polygon is regular

  // Names
  getPolygonName,           // Get Spanish name (pentagono, hexagono, etc.)
} from '@/lib/geometry/polygonUtils';
```

### Example Usage

```typescript
import {
  regularInteriorAngle,
  diagonalCount,
  calculateApothem,
  getPolygonName,
} from '@/lib/geometry/polygonUtils';

const sides = 6;
const radius = 80;

console.log('Nombre:', getPolygonName(sides));           // 'hexagono'
console.log('Angulo interior:', regularInteriorAngle(sides));  // 120
console.log('Numero de diagonales:', diagonalCount(sides));    // 9
console.log('Apotema:', calculateApothem(sides, radius));      // 69.28...
```

---

## Mathematical Formulas

| Property | Formula | Example (Hexagon) |
|----------|---------|-------------------|
| Interior angle | `(n-2) * 180 / n` | `(6-2)*180/6 = 120°` |
| Sum of interior angles | `(n-2) * 180` | `(6-2)*180 = 720°` |
| Exterior angle | `360 / n` | `360/6 = 60°` |
| Number of diagonals | `n(n-3) / 2` | `6(6-3)/2 = 9` |
| Apothem | `r * cos(π/n)` | `80 * cos(π/6) = 69.28` |
| Side length | `2 * r * sin(π/n)` | `2*80*sin(π/6) = 80` |
| Perimeter | `n * side` | `6 * 80 = 480` |
| Area | `(perimeter * apothem) / 2` | `(480 * 69.28) / 2` |

Where `n` = number of sides, `r` = circumradius.
