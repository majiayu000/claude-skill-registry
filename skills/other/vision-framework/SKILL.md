---
name: vision-framework
description: "Implement computer vision features including text recognition (OCR), face detection, barcode scanning, image segmentation, object tracking, and document scanning in iOS apps. Covers both the modern Swift-native Vision API (iOS 16+) and legacy VNRequest patterns, VisionKit DataScannerViewController for live camera scanning, and VNCoreMLRequest for custom model inference. Use when adding OCR, barcode scanning, face detection, or custom Core ML model inference with Vision."
---

# Vision Framework

Detect text, faces, barcodes, objects, and body poses in images and video using
on-device computer vision. Patterns target iOS 26+ with Swift 6.2,
backward-compatible where noted.

See `references/vision-requests.md` for complete code patterns and
`references/visionkit-scanner.md` for DataScannerViewController integration.

## Contents

- [Two API Generations](#two-api-generations)
- [Request Pattern (Modern API)](#request-pattern-modern-api)
- [Text Recognition (OCR)](#text-recognition-ocr)
- [Face Detection](#face-detection)
- [Barcode Detection](#barcode-detection)
- [Document Scanning (iOS 26+)](#document-scanning-ios-26)
- [Image Segmentation](#image-segmentation)
- [Object Tracking](#object-tracking)
- [Other Request Types](#other-request-types)
- [Core ML Integration](#core-ml-integration)
- [VisionKit: DataScannerViewController](#visionkit-datascannerviewcontroller)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Two API Generations

Vision has two distinct API layers. Prefer the modern API for new code.

| Aspect | Modern (iOS 18+) | Legacy |
|---|---|---|
| Pattern | `let result = try await request.perform(on: image)` | `VNImageRequestHandler` + completion handler |
| Request types | Swift types — structs and classes (`RecognizeTextRequest`, `DetectFaceRectanglesRequest`) | ObjC classes (`VNRecognizeTextRequest`, `VNDetectFaceRectanglesRequest`) |
| Concurrency | Native async/await | Completion handlers or synchronous `perform` |
| Observations | Typed return values | Cast `results` from `[Any]` |
| Availability | iOS 18+ / macOS 15+ | iOS 11+ |

The modern API uses the `ImageProcessingRequest` protocol. Each request type
has a `perform(on:orientation:)` method that accepts `CGImage`, `CIImage`,
`CVPixelBuffer`, `CMSampleBuffer`, `Data`, or `URL`. Most requests are
structs; stateful requests for video tracking (e.g., `TrackObjectRequest`,
`TrackRectangleRequest`, `DetectTrajectoriesRequest`) are final classes.

## Request Pattern (Modern API)

All modern Vision requests follow the same pattern: create a request struct,
call `perform(on:)`, and handle the typed result.

```swift
import Vision

func recognizeText(in image: CGImage) async throws -> [String] {
    var request = RecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = [Locale.Language(identifier: "en-US")]

    let observations = try await request.perform(on: image)
    return observations.compactMap { observation in
        observation.topCandidates(1).first?.string
    }
}
```

### Legacy Pattern (Pre-iOS 18)

Use `VNImageRequestHandler` with completion-based requests when targeting
older deployment versions.

```swift
import Vision

func recognizeTextLegacy(in image: CGImage) throws -> [String] {
    var recognized: [String] = []
    let request = VNRecognizeTextRequest { request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        recognized = observations.compactMap { $0.topCandidates(1).first?.string }
    }
    request.recognitionLevel = .accurate

    let handler = VNImageRequestHandler(cgImage: image)
    try handler.perform([request])
    return recognized
}
```

## Text Recognition (OCR)

### Modern: RecognizeTextRequest (iOS 18+)

```swift
var request = RecognizeTextRequest()
request.recognitionLevel = .accurate       // .fast for real-time
request.recognitionLanguages = [
    Locale.Language(identifier: "en-US"),
    Locale.Language(identifier: "fr-FR"),
]
request.usesLanguageCorrection = true
request.customWords = ["SwiftUI", "Xcode"] // domain-specific terms

let observations = try await request.perform(on: cgImage)
for observation in observations {
    guard let candidate = observation.topCandidates(1).first else { continue }
    let text = candidate.string
    let confidence = candidate.confidence  // 0.0 ... 1.0
    let bounds = observation.boundingBox   // normalized coordinates
}
```

### Legacy: VNRecognizeTextRequest

```swift
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US", "fr-FR"]
request.usesLanguageCorrection = true
```

**Key differences:** Modern API uses `Locale.Language` for languages; legacy
uses string identifiers. Both support `.accurate` (best quality) and `.fast`
(real-time suitable) recognition levels.

## Face Detection

Detect face rectangles, landmarks (eyes, nose, mouth), and capture quality.

```swift
// Modern API
let faceRequest = DetectFaceRectanglesRequest()
let faces = try await faceRequest.perform(on: cgImage)

for face in faces {
    let boundingBox = face.boundingBox   // normalized CGRect
    let roll = face.roll                 // Measurement<UnitAngle>
    let yaw = face.yaw                  // Measurement<UnitAngle>
}

// Landmarks (eyes, nose, mouth contours)
var landmarkRequest = DetectFaceLandmarksRequest()
let landmarkFaces = try await landmarkRequest.perform(on: cgImage)
for face in landmarkFaces {
    let landmarks = face.landmarks
    let leftEye = landmarks?.leftEye?.normalizedPoints
    let nose = landmarks?.nose?.normalizedPoints
}
```

### Coordinate System

Vision uses a normalized coordinate system with origin at the bottom-left.
Convert to UIKit (top-left origin) before display:

```swift
func convertToUIKit(_ rect: CGRect, imageHeight: CGFloat) -> CGRect {
    CGRect(
        x: rect.origin.x,
        y: imageHeight - rect.origin.y - rect.height,
        width: rect.width,
        height: rect.height
    )
}
```

## Barcode Detection

Detect 1D and 2D barcodes including QR codes.

```swift
var request = DetectBarcodesRequest()
request.symbologies = [.qr, .ean13, .code128, .pdf417]

let barcodes = try await request.perform(on: cgImage)
for barcode in barcodes {
    let payload = barcode.payloadString          // decoded content
    let symbology = barcode.symbology            // .qr, .ean13, etc.
    let bounds = barcode.boundingBox             // normalized rect
}
```

Common symbologies: `.qr`, `.aztec`, `.pdf417`, `.dataMatrix`, `.ean8`,
`.ean13`, `.code39`, `.code128`, `.upce`, `.itf14`.

## Document Scanning (iOS 26+)

`RecognizeDocumentsRequest` provides structured document reading with layout
understanding beyond basic OCR. Returns `DocumentObservation` objects with a
nested `Container` structure for paragraphs, tables, lists, and barcodes.

```swift
var request = RecognizeDocumentsRequest()
let documents = try await request.perform(on: cgImage)

for observation in documents {
    let container = observation.document

    // Full text content
    let fullText = container.text

    // Structured access to paragraphs
    for paragraph in container.paragraphs {
        let paragraphText = paragraph.text
    }

    // Tables and lists
    for table in container.tables { /* structured table data */ }
    for list in container.lists { /* structured list data */ }

    // Embedded barcodes detected within the document
    for barcode in container.barcodes { /* barcode data */ }

    // Document title if detected
    if let title = container.title { print(title) }
}
```

For simpler document camera scanning, use VisionKit's
`VNDocumentCameraViewController` which provides a full-screen camera UI with
auto-capture, perspective correction, and multi-page scanning.

## Image Segmentation

### Modern: GeneratePersonSegmentationRequest (iOS 18+)

```swift
var request = GeneratePersonSegmentationRequest()
request.qualityLevel = .accurate  // .balanced, .fast

let mask = try await request.perform(on: cgImage)
// mask is a PersonSegmentationObservation with a pixelBuffer property
let maskBuffer = mask.pixelBuffer
// Apply mask using Core Image: CIFilter.blendWithMask()
```

### Legacy: VNGeneratePersonSegmentationRequest

```swift
let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate  // .balanced, .fast
request.outputPixelFormat = kCVPixelFormatType_OneComponent8

let handler = VNImageRequestHandler(cgImage: cgImage)
try handler.perform([request])

guard let mask = request.results?.first?.pixelBuffer else { return }
// Apply mask using Core Image: CIFilter.blendWithMask()
```

Quality levels:
- `.accurate` -- best quality, slowest (~1s), full resolution
- `.balanced` -- good quality, moderate speed (~100ms), 960x540
- `.fast` -- lowest quality, fastest (~10ms), 256x144, suitable for real-time

### Instance Segmentation (iOS 18+)

Separate masks per person for individual effects.

```swift
// Modern API (iOS 18+)
let request = GeneratePersonInstanceMaskRequest()
let observation = try await request.perform(on: cgImage)
let indices = observation.allInstances

for index in indices {
    let mask = try observation.generateMask(forInstances: IndexSet(integer: index))
    // mask is a CVPixelBuffer with only this person visible
}
```

```swift
// Legacy API (iOS 17+)
let request = VNGeneratePersonInstanceMaskRequest()
let handler = VNImageRequestHandler(cgImage: cgImage)
try handler.perform([request])

guard let result = request.results?.first else { return }
let indices = result.allInstances
for index in indices {
    let instanceMask = try result.generateMaskedImage(
        ofInstances: IndexSet(integer: index),
        from: handler,
        croppedToInstancesExtent: false
    )
}
```

See `references/vision-requests.md` for mask composition and Core Image filter
integration patterns.

## Object Tracking

### Modern: TrackObjectRequest (iOS 18+)

`TrackObjectRequest` is a stateful request that maintains tracking context
across frames. Conforms to both `ImageProcessingRequest` and `StatefulRequest`.

```swift
// Initialize with a detected object's bounding box
let initialObservation = DetectedObjectObservation(boundingBox: detectedRect)
var request = TrackObjectRequest(observation: initialObservation)
request.trackingLevel = .accurate

// For each video frame:
let results = try await request.perform(on: pixelBuffer)
if let tracked = results.first {
    let updatedBounds = tracked.boundingBox
    let confidence = tracked.confidence
}
```

### Legacy: VNTrackObjectRequest

```swift
let trackRequest = VNTrackObjectRequest(detectedObjectObservation: initialObservation)
trackRequest.trackingLevel = .accurate

let sequenceHandler = VNSequenceRequestHandler()
// For each frame:
try sequenceHandler.perform([trackRequest], on: pixelBuffer)
if let result = trackRequest.results?.first {
    let updatedBounds = result.boundingBox
    trackRequest.inputObservation = result
}
```

## Other Request Types

Vision provides additional requests covered in `references/vision-requests.md`:

| Request | Purpose |
|---|---|
| `ClassifyImageRequest` | Classify scene content (outdoor, food, animal, etc.) |
| `GenerateAttentionBasedSaliencyImageRequest` | Heat map of where viewers focus attention |
| `GenerateObjectnessBasedSaliencyImageRequest` | Heat map of object-like regions |
| `GenerateForegroundInstanceMaskRequest` | Foreground object segmentation (not person-specific) |
| `DetectRectanglesRequest` | Detect rectangular shapes (documents, cards, screens) |
| `DetectHorizonRequest` | Detect horizon angle for auto-leveling photos |
| `DetectHumanBodyPoseRequest` | Detect body joints (shoulders, elbows, knees) |
| `DetectHumanBodyPose3DRequest` | 3D human body pose estimation |
| `DetectHumanHandPoseRequest` | Detect hand joints and finger positions |
| `DetectAnimalBodyPoseRequest` | Detect animal body joint positions |
| `DetectFaceCaptureQualityRequest` | Face capture quality scoring (0–1) for photo selection |
| `TrackRectangleRequest` | Track rectangular objects across video frames |
| `TrackOpticalFlowRequest` | Optical flow between video frames |
| `DetectTrajectoriesRequest` | Detect object trajectories in video |

All modern request types above are iOS 18+ / macOS 15+.

## Core ML Integration

Run custom Core ML models through Vision for automatic image preprocessing
(resizing, normalization, color space conversion).

```swift
// Modern API (iOS 18+)
let model = try MLModel(contentsOf: modelURL)
let request = CoreMLRequest(model: .init(model))
let results = try await request.perform(on: cgImage)

// Classification model
if let classification = results.first as? ClassificationObservation {
    let label = classification.identifier
    let confidence = classification.confidence
}
```

```swift
// Legacy API
let vnModel = try VNCoreMLModel(for: model)
let request = VNCoreMLRequest(model: vnModel) { request, error in
    guard let results = request.results as? [VNClassificationObservation] else { return }
    let topResult = results.first
}
let handler = VNImageRequestHandler(cgImage: cgImage)
try handler.perform([request])
```

For model conversion and optimization, see the `coreml` skill.

## VisionKit: DataScannerViewController

`DataScannerViewController` provides a full-screen live camera scanner for text
and barcodes. See `references/visionkit-scanner.md` for complete patterns.

### Quick Start

```swift
import VisionKit

// Check availability (requires A12+ chip and camera)
guard DataScannerViewController.isSupported,
      DataScannerViewController.isAvailable else { return }

let scanner = DataScannerViewController(
    recognizedDataTypes: [
        .text(languages: ["en"]),
        .barcode(symbologies: [.qr, .ean13])
    ],
    qualityLevel: .balanced,
    recognizesMultipleItems: true,
    isHighFrameRateTrackingEnabled: true,
    isHighlightingEnabled: true
)
scanner.delegate = self
present(scanner, animated: true) {
    try? scanner.startScanning()
}
```

### SwiftUI Integration

Wrap `DataScannerViewController` in `UIViewControllerRepresentable`. See
`references/visionkit-scanner.md` for the full implementation.

## Common Mistakes

**DON'T:** Use the legacy `VNImageRequestHandler` API for new iOS 18+ projects.
**DO:** Use modern struct-based requests with `perform(on:)` and async/await.
**Why:** Modern API provides type safety, better Swift concurrency support, and cleaner error handling.

**DON'T:** Forget to convert normalized coordinates before drawing bounding boxes.
**DO:** Use `VNImageRectForNormalizedRect(_:_:_:)` or manual conversion from bottom-left origin to UIKit top-left origin.
**Why:** Vision uses normalized coordinates (0...1) with bottom-left origin; UIKit uses points with top-left origin.

**DON'T:** Run Vision requests on the main thread.
**DO:** Perform requests on a background thread or use async/await from a detached task.
**Why:** Image analysis is CPU/GPU-intensive and blocks the UI if run on the main actor.

**DON'T:** Use `.accurate` recognition level for real-time camera feeds.
**DO:** Use `.fast` for live video, `.accurate` for still images or offline processing.
**Why:** Accurate recognition is too slow for 30fps video; fast recognition trades quality for speed.

**DON'T:** Ignore the `confidence` score on observations.
**DO:** Filter results by confidence threshold (e.g., > 0.5) appropriate for your use case.
**Why:** Low-confidence results are often incorrect and degrade user experience.

**DON'T:** Create a new `VNImageRequestHandler` for each frame when tracking objects.
**DO:** Use `VNSequenceRequestHandler` for video frame sequences.
**Why:** Sequence handler maintains temporal context for tracking; per-frame handlers lose state.

**DON'T:** Request all barcode symbologies when you only need QR codes.
**DO:** Specify only the symbologies you need in the request.
**Why:** Fewer symbologies means faster detection and fewer false positives.

**DON'T:** Assume `DataScannerViewController` is available on all devices.
**DO:** Check both `isSupported` (hardware) and `isAvailable` (user permissions) before presenting.
**Why:** Requires A12+ chip; `isAvailable` also checks camera access authorization.

## Review Checklist

- [ ] Uses modern Vision API (iOS 18+) unless targeting older deployments
- [ ] Vision requests run off the main thread (async/await or background queue)
- [ ] Normalized coordinates converted before UI display
- [ ] Confidence threshold applied to filter low-quality observations
- [ ] Recognition level matches use case (`.fast` for video, `.accurate` for stills)
- [ ] Language hints set for text recognition when input language is known
- [ ] Barcode symbologies limited to only those needed
- [ ] `DataScannerViewController` availability checked before presentation
- [ ] Camera usage description (`NSCameraUsageDescription`) in Info.plist for VisionKit
- [ ] Person segmentation quality level appropriate for use case
- [ ] `VNSequenceRequestHandler` used for video frame tracking (not per-frame handler)
- [ ] Error handling covers request failures and empty results

## References

- Vision request patterns: `references/vision-requests.md`
- VisionKit scanner integration: `references/visionkit-scanner.md`
- Apple docs: [Vision](https://sosumi.ai/documentation/vision) |
  [VisionKit](https://sosumi.ai/documentation/visionkit) |
  [RecognizeTextRequest](https://sosumi.ai/documentation/vision/recognizetextrequest) |
  [DataScannerViewController](https://sosumi.ai/documentation/visionkit/datascannerviewcontroller)
