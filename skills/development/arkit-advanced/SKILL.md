---
name: arkit-advanced
cluster: ar-vr
description: "Advanced ARKit features for complex AR development including scene reconstruction and 3D object tracking on iOS."
tags: ["arkit","augmented-reality","ios-ar","ar-advanced"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "arkit advanced augmented reality ios ar development scene tracking"
---

# arkit-advanced

## Purpose
This skill provides advanced ARKit capabilities for iOS AR development, focusing on scene reconstruction and 3D object tracking to enable complex applications like virtual try-ons or environmental mapping.

## When to Use
Use this skill for projects requiring high-fidelity AR interactions, such as integrating real-world geometry into apps, handling dynamic object detection, or building multi-user AR experiences on iOS devices with A12+ chips.

## Key Capabilities
- Scene reconstruction via ARWorldTrackingConfiguration for generating 3D meshes from real-world environments.
- 3D object tracking using ARObjectScanningConfiguration to detect and anchor custom objects.
- Advanced lighting estimation with ARFrame's lightEstimate property for realistic rendering.
- Integration with RealityKit for efficient scene management and physics simulation.

## Usage Patterns
To use this skill in OpenClaw, invoke it via the CLI with specific flags for task generation. Start by specifying the skill ID and providing context, then chain commands for refinement. For example, generate code for scene reconstruction by passing a JSON config file. Always include device compatibility checks in your workflow.

## Common Commands/API
Use OpenClaw's CLI to interact with this skill. Prefix commands with `openclaw run arkit-advanced` and add flags for specifics.

- Command: `openclaw run arkit-advanced --feature scene-reconstruction --config path/to/config.json`
  - Generates Swift code for ARWorldTrackingConfiguration setup.
  - Code snippet:
    ```
    let configuration = ARWorldTrackingConfiguration()
    configuration.sceneReconstruction = .mesh
    session.run(configuration)
    ```

- Command: `openclaw run arkit-advanced --feature object-tracking --object-id sample_cube`
  - Creates code for ARObjectScanningConfiguration.
  - Code snippet:
    ```
    let configuration = ARObjectScanningConfiguration()
    configuration.detectionObjects = [ARReferenceObject.referenceObject(for: sampleCube)]
    session.run(configuration)
    ```

- API Endpoint: For OpenClaw integration, use HTTP endpoints like `POST /api/skills/arkit-advanced/run` with a JSON payload: `{"feature": "scene-reconstruction", "params": {"environment": "outdoors"}}`.
- Config Format: Use JSON files, e.g., `{"apiVersion": "2.0", "device": "iPhone 13", "trackingMode": "3D"}`. Load via `--config` flag.

## Integration Notes
Integrate this skill into your OpenClaw workflow by setting environment variables for authentication if accessing Apple services, e.g., export `$APPLE_DEVELOPER_KEY` for API calls. Ensure your project includes the ARKit framework in Xcode; add `import ARKit` at the top of Swift files. For multi-skill setups, chain with other ar-vr skills using `openclaw chain arkit-advanced --next-skill unity-vr`. Test on a physical iOS device, as simulators don't support AR hardware.

## Error Handling
Handle errors by checking ARSession's state; for example, catch ARSession.RunOptions errors with `if error != nil { print(error!.localizedDescription) }`. In OpenClaw commands, use `--verbose` flag to log failures, e.g., `openclaw run arkit-advanced --feature scene-reconstruction --verbose`. Common issues include device incompatibility (check A12+ chip) or poor lighting; implement retry logic with `session.run(configuration, options: [.removeExistingAnchors])`. Parse OpenClaw responses for error codes like 400 for invalid configs.

## Concrete Usage Examples
1. **Scene Reconstruction for Virtual Furniture App**: Run `openclaw run arkit-advanced --feature scene-reconstruction --config furniture_app.json` to generate code that scans a room and places a virtual chair. Code snippet:
   ```
   let configuration = ARWorldTrackingConfiguration()
   configuration.sceneReconstruction = .meshWithClassification
   arView.session.run(configuration)
   ```

2. **3D Object Tracking for Product Demo**: Execute `openclaw run arkit-advanced --feature object-tracking --object-id product_model` to track a scanned product in AR. Code snippet:
   ```
   guard let referenceObject = try? ARReferenceObject(url: productURL) else { return }
   let configuration = ARObjectScanningConfiguration()
   configuration.detectionObjects = [referenceObject]
   session.run(configuration)
   ```

## Graph Relationships
- Related to cluster: ar-vr (e.g., shares dependencies with skills like unity-vr).
- Connected via tags: arkit (direct link to basic arkit skill), augmented-reality (cross-links with hololens-mixed-reality), ios-ar (integrates with swift-ios tools), ar-advanced (extends to advanced-ar frameworks).
