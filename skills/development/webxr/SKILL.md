---
name: webxr
cluster: ar-vr
description: "WebXR API enables web-based AR and VR experiences by accessing XR devices directly from browsers."
tags: ["webxr","ar","vr"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "webxr ar vr web api immersive reality"
---

# webxr

## Purpose
WebXR is a web standard API that allows developers to create immersive AR and VR experiences directly in the browser, leveraging hardware like headsets and controllers without proprietary plugins. It unifies access to XR devices, enabling cross-platform compatibility for web applications.

## When to Use
Use this skill for building interactive 3D web apps that require AR/VR, such as virtual tours, training simulations, or product visualizations. Apply it when targeting modern browsers on devices with XR support, like Oculus or ARKit-enabled iOS, to avoid native app development. Avoid it for 2D web content or environments without XR hardware.

## Key Capabilities
- Access XR devices via `navigator.xr` to check availability and request sessions.
- Render immersive content using WebGL-based APIs for 3D scenes, including positional tracking and controller input.
- Support for both VR (fully immersive) and AR (overlaid on real world) modes, with features like hand tracking and spatial audio.
- Inline and immersive sessions: Inline for simple previews, immersive for full hardware takeover.
- Integration with Web APIs like Fetch for loading assets, ensuring seamless data handling in XR contexts.

## Usage Patterns
Always start by checking if XR is supported: use `if ('xr' in navigator)` before proceeding. For VR, request an immersive session and set up a render loop with `xrFrame` updates. For AR, use the 'immersive-ar' mode and anchor content to real-world surfaces. Structure code with event listeners for session events (e.g., end, visibility change) and handle frame rendering in a requestAnimationFrame loop tied to XR. Test patterns in a browser with WebXR emulation enabled, like Chrome's flags.

## Common Commands/API
Use the WebXR API directly in JavaScript. First, ensure the page is served over HTTPS.

- Check XR support and request a session:
  ```
  if (navigator.xr) {
    navigator.xr.isSessionSupported('immersive-vr').then(supported => {
      if (supported) navigator.xr.requestSession('immersive-vr');
    });
  }
  ```

- Handle XR frame rendering:
  ```
  xrSession.requestAnimationFrame(onXRFrame);
  function onXRFrame(time, frame) {
    // Update and render scene using frame.getPose()
  }
  ```

- Add controller input:
  ```
  xrSession.addEventListener('select', handleSelect);
  function handleSelect(event) { console.log('Controller selected'); }
  ```

- End a session:
  ```
  xrSession.end();
  ```

For configuration, use JSON-like objects for session init, e.g., `{ optionalFeatures: ['local-floor', 'bounded-floor'] }`. If using polyfills, load via script tags: `<script src="https://cdn.jsdelivr.net/npm/webxr-polyfill@latest/dist/webxr-polyfill.js"></script>`.

## Integration Notes
Integrate WebXR into HTML5 projects by including a canvas element for rendering: `<canvas id="xr-canvas"></canvas>`. Set up in JavaScript by getting the canvas context and passing it to the XR session. For authentication, if accessing external APIs (e.g., for 3D models), use environment variables like `$WEBXR_API_KEY` in fetch calls: `fetch(url, { headers: { 'Authorization': `Bearer ${process.env.WEBXR_API_KEY}` } })`. Ensure browser compatibility by checking user agent or feature detection; enable WebXR in Chrome via `chrome://flags/#enable-webxr`. For production, bundle with tools like Webpack and test on real devices using USB debugging.

## Error Handling
Always wrap XR operations in try-catch blocks, as device access can fail due to hardware issues. For example:
```
try {
  await navigator.xr.requestSession('immersive-vr');
} catch (error) {
  console.error('XR session failed:', error.message); // Handle with user feedback
}
```
Check specific error codes like 'NotSupportedError' for unsupported sessions and fall back to 2D views. Use promise rejections for asynchronous calls, e.g., `.catch(err => alert('Error: ' + err))`. Monitor performance errors by checking frame drops in the render loop and implement timeouts for session requests to prevent hangs.

## Concrete Usage Examples
1. **Simple VR Scene**: Create a basic VR viewer for a 3D model. First, check XR support, request an immersive-VR session, and render a sphere. Code:
   ```
   navigator.xr.requestSession('immersive-vr').then(session => {
     session.baseReferenceSpace = await session.requestReferenceSpace('viewer');
     // Render loop: session.requestAnimationFrame(render);
   });
   ```
   Use this in a web page to display the model when a headset is connected.

2. **AR Overlay for Markers**: Build an AR app that overlays text on detected images. Request an 'immersive-ar' session, use hit-testing for world anchors, and draw UI elements. Code:
   ```
   navigator.xr.requestSession('immersive-ar').then(session => {
     session.requestHitTestSource({ space: viewerSpace }).then(source => {
       // Process hits and render overlays
     });
   });
   ```
   Apply this for augmented reality guides, like highlighting objects in a museum app.

## Graph Relationships
- Related to: ar (cluster: ar-vr, shares AR capabilities)
- Related to: vr (cluster: ar-vr, shares VR capabilities)
- Connected to: web (cluster: web-technologies, via Web API integration)
- Linked with: immersive-reality (tag overlap for broader XR ecosystems)
