---
name: coreml
description: "Integrate and optimize Core ML models in iOS apps for on-device machine learning inference. Covers model loading (.mlmodelc, .mlpackage), predictions with auto-generated classes and MLFeatureProvider, compute unit configuration (CPU, GPU, Neural Engine), MLTensor, VNCoreMLRequest, MLComputePlan, multi-model pipelines, and deployment strategies. Use when loading Core ML models, making predictions, configuring compute units, or profiling model performance."
---

# Core ML Swift Integration

Load, configure, and run Core ML models in iOS apps. This skill covers the
Swift side: model loading, prediction, MLTensor, profiling, and deployment.
Target iOS 26+ with Swift 6.2, backward-compatible to iOS 14 unless noted.

> **Scope boundary:** Python-side model conversion, optimization (quantization,
> palettization, pruning), and framework selection live in the `apple-on-device-ai`
> skill. This skill owns Swift integration only.

See `references/coreml-swift-integration.md` for complete code patterns including
actor-based caching, batch inference, image preprocessing, and testing.

## Contents

- [Loading Models](#loading-models)
- [Model Configuration](#model-configuration)
- [Making Predictions](#making-predictions)
- [MLTensor (iOS 18+)](#mltensor-ios-18)
- [Working with MLMultiArray](#working-with-mlmultiarray)
- [Image Preprocessing](#image-preprocessing)
- [Multi-Model Pipelines](#multi-model-pipelines)
- [Vision Integration](#vision-integration)
- [Performance Profiling](#performance-profiling)
- [Model Deployment](#model-deployment)
- [Memory Management](#memory-management)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Loading Models

### Auto-Generated Classes

When you drag a `.mlpackage` or `.mlmodelc` into Xcode, it generates a Swift
class with typed input/output. Use this whenever possible.

```swift
import CoreML

let config = MLModelConfiguration()
config.computeUnits = .all

let model = try MyImageClassifier(configuration: config)
```

### Manual Loading

Load from a URL when the model is downloaded at runtime or stored outside the
bundle.

```swift
let modelURL = Bundle.main.url(
    forResource: "MyModel", withExtension: "mlmodelc"
)!
let model = try MLModel(contentsOf: modelURL, configuration: config)
```

### Async Loading (iOS 16+)

Load models without blocking the main thread. Prefer this for large models.

```swift
let model = try await MLModel.load(
    contentsOf: modelURL,
    configuration: config
)
```

### Compile at Runtime

Compile a `.mlpackage` or `.mlmodel` to `.mlmodelc` on device. Useful for
models downloaded from a server.

```swift
let compiledURL = try await MLModel.compileModel(at: packageURL)
let model = try MLModel(contentsOf: compiledURL, configuration: config)
```

Cache the compiled URL -- recompiling on every launch wastes time. Copy
`compiledURL` to a persistent location (e.g., Application Support).

## Model Configuration

`MLModelConfiguration` controls compute units, GPU access, and model parameters.

### Compute Units Decision Table

| Value | Uses | When to Choose |
|---|---|---|
| `.all` | CPU + GPU + Neural Engine | Default. Let the system decide. |
| `.cpuOnly` | CPU | Background tasks, audio sessions, or when GPU is busy. |
| `.cpuAndGPU` | CPU + GPU | Need GPU but model has ops unsupported by ANE. |
| `.cpuAndNeuralEngine` | CPU + Neural Engine | Best energy efficiency for compatible models. |

```swift
let config = MLModelConfiguration()
config.computeUnits = .cpuAndNeuralEngine

// Allow low-priority background inference
config.computeUnits = .cpuOnly
```

### Configuration Properties

```swift
let config = MLModelConfiguration()
config.computeUnits = .all
config.allowLowPrecisionAccumulationOnGPU = true // faster, slight precision loss
```

## Making Predictions

### With Auto-Generated Classes

The generated class provides typed input/output structs.

```swift
let model = try MyImageClassifier(configuration: config)
let input = MyImageClassifierInput(image: pixelBuffer)
let output = try model.prediction(input: input)
print(output.classLabel)        // "golden_retriever"
print(output.classLabelProbs)   // ["golden_retriever": 0.95, ...]
```

### With MLDictionaryFeatureProvider

Use when inputs are dynamic or not known at compile time.

```swift
let inputFeatures = try MLDictionaryFeatureProvider(dictionary: [
    "image": MLFeatureValue(pixelBuffer: pixelBuffer),
    "confidence_threshold": MLFeatureValue(double: 0.5),
])
let output = try model.prediction(from: inputFeatures)
let label = output.featureValue(for: "classLabel")?.stringValue
```

### Async Prediction (iOS 17+)

```swift
let output = try await model.prediction(from: inputFeatures)
```

### Batch Prediction

Process multiple inputs in one call for better throughput.

```swift
let batchInputs = try MLArrayBatchProvider(array: inputs.map { input in
    try MLDictionaryFeatureProvider(dictionary: ["image": MLFeatureValue(pixelBuffer: input)])
})
let batchOutput = try model.predictions(from: batchInputs)
for i in 0..<batchOutput.count {
    let result = batchOutput.features(at: i)
    print(result.featureValue(for: "classLabel")?.stringValue ?? "unknown")
}
```

### Stateful Prediction (iOS 18+)

Use `MLState` for models that maintain state across predictions (sequence models,
LLMs, audio accumulators). Create state once and pass it to each prediction call.

```swift
let state = model.makeState()

// Each prediction carries forward the internal model state
for frame in audioFrames {
    let input = try MLDictionaryFeatureProvider(dictionary: [
        "audio_features": MLFeatureValue(multiArray: frame)
    ])
    let output = try await model.prediction(from: input, using: state)
    let classification = output.featureValue(for: "label")?.stringValue
}
```

State is not `Sendable` -- use it from a single actor or task. Call
`model.makeState()` to create independent state for concurrent streams.

## MLTensor (iOS 18+)

`MLTensor` is a Swift-native multidimensional array for pre/post-processing.
Operations run lazily -- call `.shapedArray(of:)` to materialize results.

```swift
import CoreML

// Creation
let tensor = MLTensor([1.0, 2.0, 3.0, 4.0])
let zeros = MLTensor(zeros: [3, 224, 224], scalarType: Float.self)

// Reshaping
let reshaped = tensor.reshaped(to: [2, 2])

// Math operations
let softmaxed = tensor.softmax()
let normalized = (tensor - tensor.mean()) / tensor.standardDeviation()

// Interop with MLMultiArray
let multiArray = try MLMultiArray([1.0, 2.0, 3.0, 4.0])
let fromMultiArray = MLTensor(multiArray)
let backToArray = tensor.shapedArray(of: Float.self)
```

## Working with MLMultiArray

`MLMultiArray` is the primary data exchange type for non-image model inputs and
outputs. Use it when the auto-generated class expects array-type features.

```swift
// Create a 3D array: [batch, sequence, features]
let array = try MLMultiArray(shape: [1, 128, 768], dataType: .float32)

// Write values
for i in 0..<128 {
    array[[0, i, 0] as [NSNumber]] = NSNumber(value: Float(i))
}

// Read values
let value = array[[0, 0, 0] as [NSNumber]].floatValue

// Create from data pointer for zero-copy interop
let data: [Float] = [1.0, 2.0, 3.0]
let fromData = try MLMultiArray(dataPointer: UnsafeMutableRawPointer(mutating: data),
                                 shape: [3],
                                 dataType: .float32,
                                 strides: [1])
```

See `references/coreml-swift-integration.md` for advanced MLMultiArray patterns
including NLP tokenization and audio feature extraction.

## Image Preprocessing

Image models expect `CVPixelBuffer` input. Use `CGImage` conversion for photos
from the camera or photo library. Vision's `VNCoreMLRequest` handles this
automatically; manual conversion is needed only for direct `MLModel` prediction.

```swift
import CoreVideo

func createPixelBuffer(from cgImage: CGImage, width: Int, height: Int) -> CVPixelBuffer? {
    var pixelBuffer: CVPixelBuffer?
    let attrs: [CFString: Any] = [
        kCVPixelBufferCGImageCompatibilityKey: true,
        kCVPixelBufferCGBitmapContextCompatibilityKey: true,
    ]
    CVPixelBufferCreate(kCFAllocatorDefault, width, height,
                        kCVPixelFormatType_32ARGB, attrs as CFDictionary, &pixelBuffer)

    guard let buffer = pixelBuffer else { return nil }
    CVPixelBufferLockBaseAddress(buffer, [])
    let context = CGContext(
        data: CVPixelBufferGetBaseAddress(buffer),
        width: width, height: height,
        bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
        space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
    )
    context?.draw(cgImage, in: CGRect(x: 0, y: 0, width: width, height: height))
    CVPixelBufferUnlockBaseAddress(buffer, [])
    return buffer
}
```

For additional preprocessing patterns (normalization, center-cropping), see
`references/coreml-swift-integration.md`.

## Multi-Model Pipelines

Chain models when preprocessing or postprocessing requires a separate model.

```swift
// Sequential inference: preprocessor -> main model -> postprocessor
let preprocessed = try preprocessor.prediction(from: rawInput)
let mainOutput = try mainModel.prediction(from: preprocessed)
let finalOutput = try postprocessor.prediction(from: mainOutput)
```

For Xcode-managed pipelines, use the pipeline model type in the `.mlpackage`.
Each sub-model runs on its optimal compute unit.

## Vision Integration

Use Vision to run Core ML image models with automatic image preprocessing
(resizing, normalization, color space, orientation).

### Modern: CoreMLRequest (iOS 18+)

```swift
import Vision
import CoreML

let model = try MLModel(contentsOf: modelURL, configuration: config)
let request = CoreMLRequest(model: .init(model))
let results = try await request.perform(on: cgImage)

if let classification = results.first as? ClassificationObservation {
    print("\(classification.identifier): \(classification.confidence)")
}
```

### Legacy: VNCoreMLRequest

```swift
let vnModel = try VNCoreMLModel(for: model)
let request = VNCoreMLRequest(model: vnModel) { request, error in
    guard let results = request.results as? [VNRecognizedObjectObservation] else { return }
    for observation in results {
        let label = observation.labels.first?.identifier ?? "unknown"
        let confidence = observation.labels.first?.confidence ?? 0
        let boundingBox = observation.boundingBox // normalized coordinates
        print("\(label): \(confidence) at \(boundingBox)")
    }
}
request.imageCropAndScaleOption = .scaleFill

let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer)
try handler.perform([request])
```

> For complete Vision framework patterns (text recognition, barcode detection,
> document scanning), see the `vision-framework` skill.

## Performance Profiling

### MLComputePlan (iOS 17.4+)

Inspect which compute device each operation will use before running predictions.

```swift
let computePlan = try await MLComputePlan.load(
    contentsOf: modelURL, configuration: config
)
guard case let .program(program) = computePlan.modelStructure else { return }
guard let mainFunction = program.functions["main"] else { return }

for operation in mainFunction.block.operations {
    let deviceUsage = computePlan.deviceUsage(for: operation)
    let estimatedCost = computePlan.estimatedCost(of: operation)
    print("\(operation.operatorName): \(deviceUsage?.preferredComputeDevice ?? "unknown")")
}
```

### Instruments

Use the **Core ML** instrument template in Instruments to profile:
- Model load time
- Prediction latency (per-operation breakdown)
- Compute device dispatch (CPU/GPU/ANE per operation)
- Memory allocation

Run outside the debugger for accurate results (Xcode: Product > Profile).

## Model Deployment

### Bundle vs On-Demand Resources

| Strategy | Pros | Cons |
|---|---|---|
| Bundle in app | Instant availability, works offline | Increases app download size |
| On-demand resources | Smaller initial download | Requires download before first use |
| Background Assets (iOS 16+) | Downloads ahead of time | More complex setup |
| CloudKit / server | Maximum flexibility | Requires network, longer setup |

### Size Considerations

- App Store limit: 4 GB for app bundle
- Cellular download limit: 200 MB (can request exception)
- Use ODR tags for models > 50 MB
- Pre-compile to `.mlmodelc` to skip on-device compilation

```swift
// On-demand resource loading
let request = NSBundleResourceRequest(tags: ["ml-model-v2"])
try await request.beginAccessingResources()
let modelURL = Bundle.main.url(forResource: "LargeModel", withExtension: "mlmodelc")!
let model = try await MLModel.load(contentsOf: modelURL, configuration: config)
// Call request.endAccessingResources() when done
```

## Memory Management

- **Unload on background:** Release model references when the app enters background
  to free GPU/ANE memory. Reload on foreground return.
- **Use `.cpuOnly` for background tasks:** Background processing cannot use GPU or
  ANE; setting `.cpuOnly` avoids silent fallback and resource contention.
- **Share model instances:** Never create multiple `MLModel` instances from the same
  compiled model. Use an actor to provide shared access.
- **Monitor memory pressure:** Large models (>100 MB) can trigger memory warnings.
  Register for `UIApplication.didReceiveMemoryWarningNotification` and release
  cached models when under pressure.

See `references/coreml-swift-integration.md` for an actor-based model manager with
lifecycle-aware loading and cache eviction.

## Common Mistakes

**DON'T:** Load models on the main thread.
**DO:** Use `MLModel.load(contentsOf:configuration:)` async API or load on a background actor.
**Why:** Large models can take seconds to load, freezing the UI.

**DON'T:** Recompile `.mlpackage` to `.mlmodelc` on every app launch.
**DO:** Compile once with `MLModel.compileModel(at:)` and cache the compiled URL persistently.
**Why:** Compilation is expensive. Cache the `.mlmodelc` in Application Support.

**DON'T:** Hardcode `.cpuOnly` unless you have a specific reason.
**DO:** Use `.all` and let the system choose the optimal compute unit.
**Why:** `.all` enables Neural Engine and GPU, which are faster and more energy-efficient.

**DON'T:** Ignore `MLFeatureValue` type mismatches between input and model expectations.
**DO:** Match types exactly -- use `MLFeatureValue(pixelBuffer:)` for images, not raw data.
**Why:** Type mismatches cause cryptic runtime crashes or silent incorrect results.

**DON'T:** Create a new `MLModel` instance for every prediction.
**DO:** Load once and reuse. Use an actor to manage the model lifecycle.
**Why:** Model loading allocates significant memory and compute resources.

**DON'T:** Skip error handling for model loading and prediction.
**DO:** Catch errors and provide fallback behavior when the model fails.
**Why:** Models can fail to load on older devices or when resources are constrained.

**DON'T:** Assume all operations run on the Neural Engine.
**DO:** Use `MLComputePlan` (iOS 17.4+) to verify device dispatch per operation.
**Why:** Unsupported operations fall back to CPU, which may bottleneck the pipeline.

**DON'T:** Process images manually before passing to Vision + Core ML.
**DO:** Use `CoreMLRequest` (iOS 18+) or `VNCoreMLRequest` (legacy) to let Vision handle preprocessing.
**Why:** Vision handles orientation, scaling, and pixel format conversion correctly.

## Review Checklist

- [ ] Model loaded asynchronously (not blocking main thread)
- [ ] `MLModelConfiguration.computeUnits` set appropriately for use case
- [ ] Model instance reused across predictions (not recreated each time)
- [ ] Auto-generated class used when available (typed inputs/outputs)
- [ ] Error handling for model loading and prediction failures
- [ ] Compiled model cached persistently if compiled at runtime
- [ ] Image inputs use Vision pipeline (`CoreMLRequest` iOS 18+ or `VNCoreMLRequest`) for correct preprocessing
- [ ] `MLComputePlan` checked to verify compute device dispatch (iOS 17.4+)
- [ ] Batch predictions used when processing multiple inputs
- [ ] Model size appropriate for deployment strategy (bundle vs ODR)
- [ ] Memory tested on target devices (especially older devices with less RAM)
- [ ] Predictions run outside debugger for accurate performance measurement

## References

- Patterns and code: `references/coreml-swift-integration.md`
- Model conversion and optimization (Python-side): covered in the `apple-on-device-ai` skill
- Apple docs: [Core ML](https://sosumi.ai/documentation/coreml) |
  [MLModel](https://sosumi.ai/documentation/coreml/mlmodel) |
  [MLComputePlan](https://sosumi.ai/documentation/coreml/mlcomputeplan-1w21n)
