---
name: pencilkit-drawing
description: "Add Apple Pencil drawing, canvas views, tool pickers, and ink serialization using PencilKit. Use when building drawing apps, annotation features, handwriting capture, signature fields, or any Apple Pencil-powered experience on iOS/iPadOS/visionOS."
---

# PencilKit Drawing

Capture Apple Pencil and finger input using `PKCanvasView`, manage drawing
tools with `PKToolPicker`, serialize drawings with `PKDrawing`, and wrap
PencilKit in SwiftUI. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [PKCanvasView Basics](#pkcanvasview-basics)
- [PKToolPicker](#pktoolpicker)
- [PKDrawing Serialization](#pkdrawing-serialization)
- [Exporting to Image](#exporting-to-image)
- [Stroke Inspection](#stroke-inspection)
- [SwiftUI Integration](#swiftui-integration)
- [PaperKit Relationship](#paperkit-relationship)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

PencilKit requires no entitlements or Info.plist entries. Import `PencilKit`
and create a `PKCanvasView`.

```swift
import PencilKit
```

**Platform availability:** iOS 13+, iPadOS 13+, Mac Catalyst 13.1+, visionOS 1.0+.

## PKCanvasView Basics

`PKCanvasView` is a `UIScrollView` subclass that captures Apple Pencil and
finger input and renders strokes.

```swift
import PencilKit
import UIKit

class DrawingViewController: UIViewController, PKCanvasViewDelegate {
    let canvasView = PKCanvasView()

    override func viewDidLoad() {
        super.viewDidLoad()
        canvasView.delegate = self
        canvasView.drawingPolicy = .anyInput
        canvasView.tool = PKInkingTool(.pen, color: .black, width: 5)
        canvasView.frame = view.bounds
        canvasView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(canvasView)
    }

    func canvasViewDrawingDidChange(_ canvasView: PKCanvasView) {
        // Drawing changed -- save or process
    }
}
```

### Drawing Policies

| Policy | Behavior |
|---|---|
| `.default` | Apple Pencil draws; finger scrolls |
| `.anyInput` | Both pencil and finger draw |
| `.pencilOnly` | Only Apple Pencil draws; finger always scrolls |

```swift
canvasView.drawingPolicy = .pencilOnly
```

### Configuring the Canvas

```swift
// Set a large drawing area (scrollable)
canvasView.contentSize = CGSize(width: 2000, height: 3000)

// Enable/disable the ruler
canvasView.isRulerActive = true

// Set the current tool programmatically
canvasView.tool = PKInkingTool(.pencil, color: .blue, width: 3)
canvasView.tool = PKEraserTool(.vector)
```

## PKToolPicker

`PKToolPicker` displays a floating palette of drawing tools. The canvas
automatically adopts the selected tool.

```swift
class DrawingViewController: UIViewController {
    let canvasView = PKCanvasView()
    let toolPicker = PKToolPicker()

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        toolPicker.setVisible(true, forFirstResponder: canvasView)
        toolPicker.addObserver(canvasView)
        canvasView.becomeFirstResponder()
    }
}
```

### Custom Tool Picker Items

Create a tool picker with specific tools.

```swift
let toolPicker = PKToolPicker(toolItems: [
    PKToolPickerInkingItem(type: .pen, color: .black),
    PKToolPickerInkingItem(type: .pencil, color: .gray),
    PKToolPickerInkingItem(type: .marker, color: .yellow),
    PKToolPickerEraserItem(type: .vector),
    PKToolPickerLassoItem(),
    PKToolPickerRulerItem()
])
```

### Ink Types

| Type | Description |
|---|---|
| `.pen` | Smooth, pressure-sensitive pen |
| `.pencil` | Textured pencil with tilt shading |
| `.marker` | Semi-transparent highlighter |
| `.monoline` | Uniform-width pen |
| `.fountainPen` | Variable-width calligraphy pen |
| `.watercolor` | Blendable watercolor brush |
| `.crayon` | Textured crayon |

## PKDrawing Serialization

`PKDrawing` is a value type (struct) that holds all stroke data. Serialize
it to `Data` for persistence.

```swift
// Save
func saveDrawing(_ drawing: PKDrawing) throws {
    let data = drawing.dataRepresentation()
    try data.write(to: fileURL)
}

// Load
func loadDrawing() throws -> PKDrawing {
    let data = try Data(contentsOf: fileURL)
    return try PKDrawing(data: data)
}
```

### Combining Drawings

```swift
var drawing1 = PKDrawing()
let drawing2 = PKDrawing()
drawing1.append(drawing2)

// Non-mutating
let combined = drawing1.appending(drawing2)
```

### Transforming Drawings

```swift
let scaled = drawing.transformed(using: CGAffineTransform(scaleX: 2, y: 2))
let translated = drawing.transformed(using: CGAffineTransform(translationX: 100, y: 0))
```

## Exporting to Image

Generate a `UIImage` from a drawing.

```swift
func exportImage(from drawing: PKDrawing, scale: CGFloat = 2.0) -> UIImage {
    drawing.image(from: drawing.bounds, scale: scale)
}

// Export a specific region
let region = CGRect(x: 0, y: 0, width: 500, height: 500)
let scale = UITraitCollection.current.displayScale
let croppedImage = drawing.image(from: region, scale: scale)
```

## Stroke Inspection

Access individual strokes, their ink, and control points.

```swift
for stroke in drawing.strokes {
    let ink = stroke.ink
    print("Ink type: \(ink.inkType), color: \(ink.color)")
    print("Bounds: \(stroke.renderBounds)")

    // Access path points
    let path = stroke.path
    print("Points: \(path.count), created: \(path.creationDate)")

    // Interpolate along the path
    for point in path.interpolatedPoints(by: .distance(10)) {
        print("Location: \(point.location), force: \(point.force)")
    }
}
```

### Constructing Strokes Programmatically

```swift
let points = [
    PKStrokePoint(location: CGPoint(x: 0, y: 0), timeOffset: 0,
                  size: CGSize(width: 5, height: 5), opacity: 1,
                  force: 0.5, azimuth: 0, altitude: .pi / 2),
    PKStrokePoint(location: CGPoint(x: 100, y: 100), timeOffset: 0.1,
                  size: CGSize(width: 5, height: 5), opacity: 1,
                  force: 0.5, azimuth: 0, altitude: .pi / 2)
]
let path = PKStrokePath(controlPoints: points, creationDate: Date())
let stroke = PKStroke(ink: PKInk(.pen, color: .black), path: path,
                      transform: .identity, mask: nil)
let drawing = PKDrawing(strokes: [stroke])
```

## SwiftUI Integration

Wrap `PKCanvasView` in a `UIViewRepresentable` for SwiftUI.

```swift
import SwiftUI
import PencilKit

struct CanvasView: UIViewRepresentable {
    @Binding var drawing: PKDrawing
    @Binding var toolPickerVisible: Bool

    func makeUIView(context: Context) -> PKCanvasView {
        let canvas = PKCanvasView()
        canvas.delegate = context.coordinator
        canvas.drawingPolicy = .anyInput
        canvas.drawing = drawing
        return canvas
    }

    func updateUIView(_ canvas: PKCanvasView, context: Context) {
        if canvas.drawing != drawing {
            canvas.drawing = drawing
        }
        let toolPicker = context.coordinator.toolPicker
        toolPicker.setVisible(toolPickerVisible, forFirstResponder: canvas)
        if toolPickerVisible { canvas.becomeFirstResponder() }
    }

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    class Coordinator: NSObject, PKCanvasViewDelegate {
        let parent: CanvasView
        let toolPicker = PKToolPicker()

        init(_ parent: CanvasView) {
            self.parent = parent
            super.init()
        }

        func canvasViewDrawingDidChange(_ canvasView: PKCanvasView) {
            parent.drawing = canvasView.drawing
        }
    }
}
```

### Usage in SwiftUI

```swift
struct DrawingScreen: View {
    @State private var drawing = PKDrawing()
    @State private var showToolPicker = true

    var body: some View {
        CanvasView(drawing: $drawing, toolPickerVisible: $showToolPicker)
            .ignoresSafeArea()
    }
}
```

## PaperKit Relationship

PaperKit (iOS 26+) extends PencilKit with a complete markup experience
including shapes, text boxes, images, stickers, and loupes. Use PaperKit
when you need more than freeform drawing.

| Capability | PencilKit | PaperKit |
|---|---|---|
| Freeform drawing | Yes | Yes |
| Shapes & lines | No | Yes |
| Text boxes | No | Yes |
| Images & stickers | No | Yes |
| Markup toolbar | No | Yes |
| Data model | `PKDrawing` | `PaperMarkup` |

PaperKit uses PencilKit under the hood -- `PaperMarkupViewController` accepts
`PKTool` for its `drawingTool` property and `PaperMarkup` can append a
`PKDrawing`. See `references/paperkit-integration.md` for PaperKit patterns.

## Common Mistakes

### DON'T: Forget to call becomeFirstResponder for the tool picker

The tool picker only appears when its associated responder is first responder.

```swift
// WRONG: Tool picker never shows
toolPicker.setVisible(true, forFirstResponder: canvasView)

// CORRECT: Also become first responder
toolPicker.setVisible(true, forFirstResponder: canvasView)
canvasView.becomeFirstResponder()
```

### DON'T: Create multiple tool pickers for the same canvas

One `PKToolPicker` per canvas. Creating extras causes visual conflicts.

```swift
// WRONG
func viewDidAppear(_ animated: Bool) {
    let picker = PKToolPicker()  // New picker every appearance
    picker.setVisible(true, forFirstResponder: canvasView)
}

// CORRECT: Store picker as a property
let toolPicker = PKToolPicker()
```

### DON'T: Ignore content version for backward compatibility

Newer ink types crash on older OS versions. Set `maximumSupportedContentVersion`
if you need backward-compatible drawings.

```swift
// WRONG: Saves a drawing with .watercolor, crashes on iOS 16
canvasView.tool = PKInkingTool(.watercolor, color: .blue)

// CORRECT: Limit content version for compatibility
canvasView.maximumSupportedContentVersion = .version2
```

### DON'T: Compare drawings by data representation

`PKDrawing` data is not deterministic; the same visual drawing can produce
different bytes. Use equality operators instead.

```swift
// WRONG
if drawing1.dataRepresentation() == drawing2.dataRepresentation() { }

// CORRECT
if drawing1 == drawing2 { }
```

## Review Checklist

- [ ] `PKCanvasView.drawingPolicy` set appropriately (`.default` for Pencil-primary apps)
- [ ] `PKToolPicker` stored as a property, not recreated each appearance
- [ ] `canvasView.becomeFirstResponder()` called to show the tool picker
- [ ] Drawing serialized via `dataRepresentation()` and loaded via `PKDrawing(data:)`
- [ ] `canvasViewDrawingDidChange` delegate method used to track changes
- [ ] `maximumSupportedContentVersion` set if backward compatibility needed
- [ ] Exported images use appropriate scale factor for the device
- [ ] SwiftUI wrapper avoids infinite update loops by checking `drawing != binding`
- [ ] Tool picker observer added before becoming first responder
- [ ] Drawing bounds checked before image export (empty drawings have `.zero` bounds)

## References

- Extended PencilKit patterns (advanced strokes, Scribble, delegate): `references/pencilkit-patterns.md`
- PaperKit integration patterns: `references/paperkit-integration.md`
- [PencilKit framework](https://sosumi.ai/documentation/pencilkit)
- [PKCanvasView](https://sosumi.ai/documentation/pencilkit/pkcanvasview)
- [PKDrawing](https://sosumi.ai/documentation/pencilkit/pkdrawing-swift.struct)
- [PKToolPicker](https://sosumi.ai/documentation/pencilkit/pktoolpicker)
- [PKInkingTool](https://sosumi.ai/documentation/pencilkit/pkinkingtool-swift.struct)
- [PKStroke](https://sosumi.ai/documentation/pencilkit/pkstroke-swift.struct)
- [Drawing with PencilKit](https://sosumi.ai/documentation/pencilkit/drawing-with-pencilkit)
- [Configuring the PencilKit tool picker](https://sosumi.ai/documentation/pencilkit/configuring-the-pencilkit-tool-picker)
