---
name: openxr
cluster: ar-vr
description: "OpenXR is an open standard API for building cross-platform AR and VR applications with hardware abstraction."
tags: ["openxr","ar","vr"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "openxr ar vr api cross-platform development hardware abstraction"
---

# openxr

## Purpose
OpenXR provides a standardized API for developing AR and VR applications that work across different hardware platforms, abstracting low-level device specifics to enable cross-platform compatibility.

## When to Use
Use OpenXR when building AR/VR apps that must run on multiple devices (e.g., Oculus, HTC Vive, or Hololens) without rewriting code for each platform, or when you need hardware-agnostic input handling and rendering.

## Key Capabilities
- Hardware abstraction for AR/VR devices, allowing runtime selection of backends.
- Session management for creating and destroying VR sessions.
- Input handling via action sets for controllers and gestures.
- Rendering integration with graphics APIs like Vulkan or OpenGL.
- Spatial tracking and pose management for headsets and controllers.

## Usage Patterns
To use OpenXR, first initialize an instance with required extensions, then create a session for the target device, set up action maps for inputs, and enter a render loop. Always poll for events in the main loop and handle session state changes. For cross-platform builds, link against the OpenXR loader and specify the runtime via environment variables or configuration files.

## Common Commands/API
Key OpenXR functions include:
- `xrCreateInstance`: Create an instance with XrInstanceCreateInfo struct; specify extensions like "XR_KHR_vulkan_enable".
  Example:
  ```c
  XrInstanceCreateInfo createInfo = { /* ... */ };
  xrCreateInstance(&createInfo, &instance);
  ```
- `xrCreateSession`: Start a session with a graphics binding; use XrSessionCreateInfo and bind to Vulkan via XrGraphicsBindingVulkanKHR.
  Example:
  ```c
  XrSessionCreateInfo sessionCreateInfo = { /* ... */ };
  xrCreateSession(instance, &sessionCreateInfo, &session);
  ```
- `xrPollEvents`: Check for events like session state changes; call in your main loop with an XrEventDataBuffer.
  Example:
  ```c
  XrEventDataBuffer eventData;
  while (xrPollEvents(instance, &eventData) == XR_SUCCESS) { /* handle events */ }
  ```
- Configuration files: Use JSON-like formats for action manifests, e.g., {"bindings": [{"path": "/user/hand/left"}]} in a .json file loaded via xrStringToPath.

## Integration Notes
Integrate OpenXR by including the OpenXR loader header and linking against libopenxr_loader. For graphics, use extension-specific bindings: for Vulkan, enable "XR_KHR_vulkan_enable" and provide a VkInstance; for OpenGL, use "XR_KHR_openGL_enable". Set the runtime path via the XR_RUNTIME_JSON environment variable (e.g., export XR_RUNTIME_JSON=/path/to/runtime.json). If authentication is needed for specific runtimes (rare), use $OPENXR_API_KEY in your environment.

## Error Handling
Always check XrResult return codes from API calls; use XR_SUCCESS for success checks. Common errors include XR_ERROR_INITIALIZATION_FAILED (e.g., missing extensions) and XR_ERROR_SESSION_LOST (device disconnection). Handle them by logging details and attempting recovery, like recreating a session. Use xrGetInstanceProcAddr to dynamically load functions and check for NULL pointers.

## Concrete Usage Examples
1. Basic instance creation and session setup for a VR app:
   - Code snippet:
     ```c
     XrInstance instance;
     xrCreateInstance(...);  // Initialize with required extensions
     XrSession session;
     xrCreateSession(instance, ...);  // Bind to graphics API
     ```
   - Steps: Compile with -lopenxr_loader, run on a device, and handle events in a loop to render frames.

2. Handling controller input in an AR game:
   - Code snippet:
     ```c
     XrActionSet actionSet;
     xrCreateActionSet(instance, ...);  // Define actions for buttons
     xrSuggestInteractionProfileBindings(...);  // Bind to device paths
     while (running) { xrSyncActions(session, ...); }  // Poll and process inputs
     ```
   - Steps: Create an action manifest JSON, load it, and use xrGetActionStateBoolean to check button states for game logic.

## Graph Relationships
- Related to cluster: ar-vr (e.g., connects with skills like "oculus-sdk" for specific hardware implementations).
- Related to tags: "openxr" (links to "ar" and "vr" skills for broader AR/VR ecosystems).
