---
name: mediapipe-usage
description: Summarizes Google MediaPipe usage for web: Pose Landmarker with @mediapipe/tasks-vision, landmark indices, running modes, and patterns for real-time video. Use when working with MediaPipe, pose detection, body landmarks, or @mediapipe/tasks-vision.
---

# Google MediaPipe Usage (Web / Pose Landmarker)

## When to Use This Skill

- Using or debugging `@mediapipe/tasks-vision`, Pose Landmarker, or pose detection in a web app.
- Needing the 33 pose landmark indices, skeleton connections, or mapping landmarks to gestures or control signals.

## Setup

**Install (prefer pnpm):**

```bash
pnpm add @mediapipe/tasks-vision
```

**WASM root:** Resolve vision tasks from CDN when creating the task:

```ts
const vision = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm",
);
```

## Create the Pose Landmarker Task

Use `PoseLandmarker.createFromOptions(vision, options)`:

```ts
import { PoseLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";

const vision = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm",
);

const poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
  baseOptions: {
    modelAssetPath: modelUrl, // see reference.md for lite/full/heavy URLs
    delegate: "GPU", // falls back to CPU if unavailable
  },
  runningMode: "VIDEO", // or "IMAGE" for single image
  numPoses: 1,
  minPoseDetectionConfidence: 0.5,
  minPosePresenceConfidence: 0.5,
  minTrackingConfidence: 0.5,
});
```

- **runningMode**: `IMAGE` for single image → use `detect(image)`. `VIDEO` for stream → use `detectForVideo(video, timestamp)`.
- **baseOptions.modelAssetPath**: URL to a `.task` model (lite / full / heavy). See [reference.md](reference.md) for URLs.
- **delegate**: `"GPU"` preferred; some environments fall back to CPU.

## Run the Task

**Single image (runningMode IMAGE):**

```ts
const result = poseLandmarker.detect(imageElement);
```

**Video / webcam (runningMode VIDEO):**

Call `detectForVideo(video, timestamp)` inside a `requestAnimationFrame` loop. Throttle by time (e.g. ~33 ms between frames) to avoid excessive work:

```ts
let lastFrameTime = 0;
function detectLoop() {
  const now = performance.now();
  if (video.readyState >= 2 && now - lastFrameTime > 33) {
    lastFrameTime = now;
    const result = poseLandmarker.detectForVideo(video, now);
    if (result.landmarks?.length) {
      const landmarks = result.landmarks[0]; // first person
      // use landmarks
    }
  }
  requestAnimationFrame(detectLoop);
}
requestAnimationFrame(detectLoop);
```

## Result Shape

- **result.landmarks**: Array of poses; each pose is `NormalizedLandmark[]` (33 points). Each landmark: `x`, `y`, `z` (normalized 0–1; z is depth relative to hip center), `visibility` (0–1).
- **result.worldLandmarks**: Optional 3D coordinates in meters (same indices).
- Single person: use `result.landmarks[0]`.

## Practical Patterns (Know-how)

- **State machine**: idle → loading (load model) → ready (can start) → active (webcam + detection) → error. When switching model variant, close the old PoseLandmarker instance and create a new one.
- **Throttle**: Run `detectForVideo` only when `performance.now() - lastFrameTime > 33` (≈30 fps) to avoid blocking the main thread.
- **Smoothing**: Apply a smoothing factor (e.g. 0.3) to derived values (pitch, bank) to reduce jitter; use a dead zone (in degrees) to ignore small movements.
- **Confidence**: Use each landmark’s `visibility`; ignore or downweight points below a threshold. Helper: `getLandmark(landmarks, index, minConfidence)` returning the point only if `visibility >= minConfidence`.
- **Gestures**: e.g. “hands forward” = compare shoulder vs wrist z; “hands overhead” = compare wrist y to shoulder y. Use consecutive-frame counters for toggles (e.g. require N frames in pose before firing an action).

## Cleanup

- Stop webcam: `stream.getTracks().forEach(t => t.stop())`.
- Release task: `poseLandmarker.close()` when done or before creating a new instance.

## Additional Resources

- Full 33 landmark indices and skeleton connections: [reference.md](reference.md)
- Minimal example, skeleton overlay, and landmark-to-control mapping: [examples.md](examples.md)
- Official: [Pose Landmarker Web JS](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/web_js), [Setup guide for web](https://ai.google.dev/edge/mediapipe/solutions/setup_web)
