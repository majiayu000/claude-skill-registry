---
name: unity-xr
cluster: ar-vr
description: "Develops XR applications using Unity for AR and VR, focusing on immersive interactions and cross-platform compatibility."
tags: ["unity","xr","ar-vr"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "unity xr ar vr development immersive interactions"
---

## Purpose

This skill automates and assists in developing XR applications with Unity, focusing on AR and VR features like hand tracking, spatial audio, and multi-platform builds for devices such as Oculus Quest or HoloLens. It leverages Unity's XR ecosystem to streamline immersive interaction code.

## When to Use

Use this skill when creating interactive AR/VR experiences, such as virtual training simulations, 3D product visualizations, or multiplayer VR games. Apply it for cross-platform projects needing device-agnostic code, like adapting to Android ARCore and iOS ARKit, or when optimizing for performance on standalone VR headsets.

## Key Capabilities

- Handles XR Interaction Toolkit for input systems: Use `XRBaseInteractable` to define grabbable objects in VR scenes.
- Supports AR Foundation for unified AR development: Enable plane detection with `ARPlaneManager` to track surfaces.
- Ensures cross-platform compatibility: Configure build settings for multiple targets using Unity's Player Settings API, e.g., set `XRSettings.enabled = true;` for specific devices.
- Manages immersive interactions: Implement raycasting for VR pointers via `XRInteractorLineVisual`, with collision checks in 2-3 lines of C# code.
- Optimizes for performance: Use Unity's Profiler to monitor frame rates, integrating with XR plugins to cap at 90 FPS for VR.

## Usage Patterns

To set up a basic XR project, first install Unity and the XR packages via the Package Manager. Import the XR Interaction Toolkit, then create a new scene and add an XR Rig prefab. For AR, initialize an AR Session in your script's `Start()` method. Always test on target hardware early. For VR interactions, attach scripts to GameObjects to handle events like `OnSelectEntered()`. Structure code modularly: separate input handling from logic. When building, use command-line builds for automation, e.g., run `Unity -batchmode -projectPath /path/to/project -buildTarget Android -executeMethod BuildScript.PerformBuild`.

## Common Commands/API

- Unity CLI for building: Use `Unity -quit -batchmode -projectPath /path/to/project -buildWindows64Player /output/path.exe` to compile a VR build; include `-logFile build.log` for output.
- XR Interaction API snippet:  
  ```csharp
  using UnityEngine.XR.Interaction.Toolkit;
  public class GrabHandler : XRGrabInteractable { void OnSelectEntered(SelectEnterEventArgs args) { transform.position = args.interactor.transform.position; } }
  ```
- AR Foundation API for session management:  
  ```csharp
  using UnityEngine.XR.ARFoundation;
  public class ARManager : MonoBehaviour { private ARSession arSession; void Start() { arSession = FindObjectOfType<ARSession>(); arSession.enabled = true; } }
  ```
- Configuration formats: Edit Unity's `ProjectSettings/ProjectSettings.asset` to set XR plugins, e.g., add `XR Plug-in Management: Oculus` under `XRSettings`. For API keys (e.g., for AR services), use environment variables like `$ARFOUNDATION_API_KEY` in build scripts.
- Common endpoints: When integrating with Unity services, reference REST endpoints like `https://services.unity.com/api/v1/projects` for cloud builds, authenticated via `$UNITY_ACCESS_TOKEN`.

## Integration Notes

Integrate this skill with Unity's core engine by adding XR packages via the Package Manager CLI: `Unity -projectPath /path -importPackage path/to/xri.unitypackage`. For external tools, link with Unreal or Blender by exporting FBX models, then import into Unity and apply XR scripts. If using version control, ensure .meta files are tracked; configure Git hooks to validate XR settings. For authentication in cloud integrations (e.g., Unity Cloud Build), set env vars like `$UNITY_PROJECT_ID` and use them in scripts: `string projectId = System.Environment.GetEnvironmentVariable("UNITY_PROJECT_ID");`. Always match Unity versions across integrations to avoid API mismatches.

## Error Handling

Check for common XR errors like device not found: In code, use `if (!XRSettings.isDeviceActive) { Debug.LogError("XR device inactive"); }` before starting sessions. For AR tracking failures, handle via `ARSession.stateChanged` events:  
```csharp
ARSession.stateChanged += OnStateChanged; void OnStateChanged(ARSessionStateChangedEventArgs args) { if (args.state == ARSessionState.Error) { Debug.LogError(args.errorCode); } }
```
Use Unity's ErrorPause in Editor settings for debugging. For build errors, parse CLI logs with scripts, e.g., check exit codes: `if (process.ExitCode != 0) { throw new Exception("Build failed"); }`. Always wrap API calls in try-catch blocks for runtime exceptions, like `try { arSession.Reset(); } catch (Exception e) { Debug.Log(e.Message); }`.

## Concrete Usage Examples

1. **VR Interaction Scene**: To create a simple VR grabber, start a Unity project, import XR Interaction Toolkit, add an XR Rig to your scene, and attach this script to an object:  
   ```csharp
   using UnityEngine.XR.Interaction.Toolkit;
   public class SimpleGrabber : XRGrabInteractable { protected override void OnSelectEntered(SelectEnterEventArgs args) { rigidbody.isKinematic = true; } }
   ```
   Build and run on an Oculus device using `Unity -batchmode -buildTarget Android -executeMethod BuildPipeline.BuildPlayer`.

2. **AR Plane Detection**: For an AR app, add AR Foundation to your project, create a script to detect planes:  
   ```csharp
   using UnityEngine.XR.ARFoundation;
   public class PlaneDetector : MonoBehaviour { private ARPlaneManager planeManager; void Start() { planeManager = gameObject.AddComponent<ARPlaneManager>(); planeManager.planesChanged += OnPlanesChanged; } }
   ```
   Test on a mobile device by building with `Unity -projectPath /path -buildTarget iOS -customBuildTarget iPhone`.

## Graph Relationships

- Connected to: unity-core (for general Unity scripting and engine features)
- Part of: ar-vr cluster (shares dependencies with other AR/VR skills)
- Relates to: 3d-modeling (for importing assets into XR scenes)
