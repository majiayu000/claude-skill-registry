---
name: data-visualization
description: Build data visualizations, charts, graphs, and maps in Flutter/Dart using the data_visualization package suite. Use when the user asks to create charts (line, bar, pie, scatter, heatmap), maps (geographic projections, GeoJSON), hierarchical visualizations (treemap, tree, pack), network graphs, or any data visualization in Flutter.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Data Visualization for Flutter

Use this skill when building data visualizations in Flutter applications. The `data_visualization` package suite provides D3.js-like functionality for Flutter.

## Installation

Add to `pubspec.yaml`:

```yaml
dependencies:
  data_visualization: ^1.0.0
```

Or add individual packages as needed (see Package Reference below).

## Core Concepts

### Scales (dv_scale)

Transform data values to visual coordinates:

```dart
import 'package:dv_scale/dv_scale.dart';

// Linear scale for continuous data
final xScale = scaleLinear(domain: [0, 100], range: [0, 400]);

// Band scale for categorical data (bar charts)
final bandScale = scaleBand(domain: ['A', 'B', 'C'], range: [0, 300]);

// Time scale for dates
final timeScale = scaleTime(
  domain: [DateTime(2024, 1, 1), DateTime(2024, 12, 31)],
  range: [0, 800],
);

// Ordinal scale for color mapping
final colorScale = scaleOrdinal(
  domain: ['cat1', 'cat2'],
  range: [Colors.red, Colors.blue],
);
```

### Curves (dv_curve)

Smooth line interpolation:

```dart
import 'package:dv_curve/dv_curve.dart';

final points = [Point(0, 10), Point(50, 80), Point(100, 30)];
final curve = curveCatmullRom();
final smoothPoints = curve.generate(points);

// Available: curveLinear(), curveBasis(), curveCardinal(),
// curveMonotoneX(), curveStep(), curveNatural()
```

### Shapes (dv_shape)

Generate paths for chart elements:

```dart
import 'package:dv_shape/dv_shape.dart';

// Line generator
final lineGen = LineGenerator<Point>(
  x: (d, i) => xScale(d.x),
  y: (d, i) => yScale(d.y),
  curve: curveCatmullRom(),
);

// Area generator
final areaGen = AreaGenerator<Point>(
  x: (d, i) => xScale(d.x),
  y0: (d, i) => yScale(0),
  y1: (d, i) => yScale(d.y),
);

// Pie layout
final pieGen = PieGenerator<Map>(value: (d, i) => d['value']);
final arcs = pieGen.generate(data);

// Arc generator
final arcGen = ArcGenerator(
  innerRadius: 50, outerRadius: 100,
  startAngle: 0, endAngle: math.pi / 2,
);
```

### Geographic (dv_geo_core, dv_geo)

Map projections and GeoJSON:

```dart
import 'package:dv_geo_core/dv_geo_core.dart';

// Projections
final mercator = geoMercator(center: (0, 0), scale: 100, translate: Point(200, 200));
final orthographic = geoOrthographic(center: (0, 0), scale: 150, translate: center, rotate: (-30, 0, 0));
final equirect = geoEquirectangular(center: (0, 0), scale: 100, translate: center);

// Project (lon, lat) -> (x, y)
final projected = mercator.project(-74.0, 40.7);

// GeoJSON
final geojson = GeoJsonFeatureCollection.fromJson(jsonData);
final geoPath = GeoPath(mercator);
final paths = geoPath.generate(geojson);
```

### Hierarchy (dv_hierarchy)

Hierarchical data layouts:

```dart
import 'package:dv_hierarchy/dv_hierarchy.dart';

final root = HierarchyNode<Map>(
  data: {'name': 'root'},
  children: [
    HierarchyNode(data: {'name': 'A', 'value': 100}),
    HierarchyNode(data: {'name': 'B', 'value': 200}),
  ],
);

root.sum((d) => (d['value'] as num?)?.toDouble() ?? 0);

// Layouts - each sets x0, y0, x1, y1 or x, y, r on nodes
treemapLayout(root, width: 400, height: 300);
treeLayout(root, width: 400, height: 300);
packLayout(root, width: 400, height: 400);
clusterLayout(root, width: 400, height: 300);
partitionLayout(root, width: 400, height: 300);
```

## Common Chart Patterns

### Line Chart

```dart
class LineChartPainter extends CustomPainter {
  final List<Point> data;
  LineChartPainter(this.data);

  @override
  void paint(Canvas canvas, Size size) {
    final xScale = scaleLinear(domain: [0, data.length - 1], range: [50, size.width - 20]);
    final yScale = scaleLinear(domain: [0, 100], range: [size.height - 40, 20]);

    final curve = curveCatmullRom();
    final points = data.map((p) => Point(xScale(p.x), yScale(p.y))).toList();
    final curvePoints = curve.generate(points);

    final path = Path()..moveTo(curvePoints.first.x, curvePoints.first.y);
    for (final p in curvePoints.skip(1)) {
      path.lineTo(p.x, p.y);
    }

    canvas.drawPath(path, Paint()
      ..color = Colors.blue
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

### Bar Chart

```dart
class BarChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  BarChartPainter(this.data);

  @override
  void paint(Canvas canvas, Size size) {
    final labels = data.map((d) => d['label'] as String).toList();
    final values = data.map((d) => d['value'] as double).toList();

    final xScale = scaleBand(domain: labels, range: [50, size.width - 20], padding: 0.2);
    final yScale = scaleLinear(domain: [0, values.reduce(math.max)], range: [size.height - 40, 20]);

    for (int i = 0; i < data.length; i++) {
      final x = xScale(labels[i])!;
      final y = yScale(values[i]);
      canvas.drawRect(
        Rect.fromLTWH(x, y, xScale.bandwidth, yScale(0) - y),
        Paint()..color = Colors.indigo,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

### Pie Chart

```dart
class PieChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  PieChartPainter(this.data);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) / 2 - 20;

    final pie = PieGenerator<Map>(value: (d, i) => d['value'] as double);
    final arcs = pie.generate(data);
    final colors = [Colors.blue, Colors.red, Colors.green, Colors.orange];

    for (int i = 0; i < arcs.length; i++) {
      final arc = arcs[i];
      final arcGen = ArcGenerator(
        innerRadius: radius * 0.5,
        outerRadius: radius,
        startAngle: arc.startAngle,
        endAngle: arc.endAngle,
      );

      canvas.save();
      canvas.translate(center.dx, center.dy);
      canvas.drawPath(arcGen.generate(), Paint()..color = colors[i % colors.length]);
      canvas.restore();
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

### Geographic Map

```dart
class GeoMapPainter extends CustomPainter {
  final GeoJsonFeatureCollection worldData;
  GeoMapPainter(this.worldData);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Point(size.width / 2, size.height / 2);
    final proj = geoMercator(center: (0, 0), scale: size.width / 6, translate: center);

    final geoPath = GeoPath(proj);
    final paths = geoPath.generate(worldData);

    for (final pathPoints in paths) {
      if (pathPoints.length < 3) continue;
      final path = Path()..moveTo(pathPoints.first.x, pathPoints.first.y);
      for (int i = 1; i < pathPoints.length; i++) {
        path.lineTo(pathPoints[i].x, pathPoints[i].y);
      }
      path.close();
      canvas.drawPath(path, Paint()..color = Colors.green.shade300);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

## Package Reference

| Package | Description |
|---------|-------------|
| `data_visualization` | Umbrella package (includes all) |
| `dv_scale` | Scale functions (linear, log, band, ordinal, time) |
| `dv_curve` | Curve interpolation |
| `dv_shape` | Shape generators (line, area, arc, pie, stack) |
| `dv_geo_core` | Map projections, GeoJSON parsing |
| `dv_geo` | Geographic widgets |
| `dv_hierarchy` | Hierarchical layouts (treemap, tree, pack) |
| `dv_stats` | Statistical functions (mean, regression) |
| `dv_axis` | Chart axes |
| `dv_grid` | Grid lines |
| `dv_legend` | Legend widgets |
| `dv_annotation` | Chart annotations |
| `dv_tooltip` | Tooltips |
| `dv_brush` | Brush selection |
| `dv_zoom` | Zoom/pan |
| `dv_xychart` | XY chart series (line, bar, area, scatter) |
| `dv_heatmap` | Heatmap visualization |
| `dv_network` | Force-directed network graphs |
| `dv_mock_data` | Mock data generators |
| `dv_glyph` | Symbol glyphs (circle, square, triangle) |
| `dv_gradient` | Gradient definitions |
| `dv_pattern` | Pattern fills |
| `dv_marker` | Markers |
| `dv_text` | Text rendering |
| `dv_group` | SVG-like group transforms |
| `dv_clip_path` | Clipping paths |
| `dv_point` | 2D Point class |
| `dv_vendor` | Array operations, interpolation |
| `dv_delaunay` | Delaunay triangulation |
| `dv_voronoi` | Voronoi diagrams |
| `dv_bounds` | Chart bounds/margins |
| `dv_responsive` | Responsive containers |
| `dv_event` | Pointer event handling |
| `dv_drag` | Drag interaction |
| `dv_threshold` | Reference lines/areas |

## Resources

- **Live Demo**: https://gsmlg-app.github.io/data_visualization/
- **GitHub**: https://github.com/gsmlg-dev/data_visualization
- **pub.dev**: https://pub.dev/packages/data_visualization
