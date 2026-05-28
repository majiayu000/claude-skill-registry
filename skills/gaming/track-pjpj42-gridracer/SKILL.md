---
name: track
description: Design or generate a new track layout
argument-hint: "[track name or description]"
allowed-tools:
  - Read
  - Write
  - Edit
model: sonnet
---

# Track Designer

Create valid track layouts for GridRacer.

## Track Requirements (from design doc)

### Cell Types
```swift
enum CellType {
    case track    // Valid racing surface
    case wall     // Collision boundary
    case start    // Starting area
    case finish   // Finish line area
}
```

### Track Structure
```swift
struct Track {
    let width: Int
    let height: Int
    let cells: [[CellType]]
    let startPositions: [GridPoint]
    let finishLine: LineSegment
    let lapCount: Int
}
```

## Design Guidelines

1. **Closed loop**: Track must form a complete circuit
2. **Width**: Minimum 2 cells wide for passing
3. **Start positions**: Staggered, equal distance to first turn
4. **Finish line**: Perpendicular to track direction
5. **Corners**: Allow multiple racing lines
6. **Balance**: Fair for all starting positions

## Example: Simple Oval (10x8)

```
..........
.########.
.#......#.
.#......#.
.S......F.
.#......#.
.#......#.
.########.
..........
```

Legend: `.`=wall, `#`=track, `S`=start, `F`=finish

## Output Format

Generate Swift code for the track:
```swift
let simpleOval = Track(
    width: 10,
    height: 8,
    cells: [...],
    startPositions: [GridPoint(2, 4), GridPoint(2, 3)],
    finishLine: LineSegment(start: GridPoint(8, 3), end: GridPoint(8, 5)),
    lapCount: 3
)
```
