---
name: spatial-audio
cluster: ar-vr
description: "Implements 3D audio positioning and rendering for immersive AR/VR experiences."
tags: ["spatial-audio","ar-vr","3d-sound"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "spatial audio ar vr 3d sound immersive rendering"
---

## Purpose

This skill implements 3D audio positioning and rendering for AR/VR applications, using techniques like Head-Related Transfer Function (HRTF) to simulate spatial sound sources in real-time.

## When to Use

Use this skill when building immersive AR/VR experiences that require realistic audio, such as virtual tours, gaming environments, or simulations where sound direction and distance enhance user presence. Avoid it for 2D audio needs, as it adds overhead for non-spatial applications.

## Key Capabilities

- Real-time HRTF-based audio rendering for accurate 3D positioning.
- Support for dynamic sound source updates, including occlusion and reverberation effects.
- Integration with AR/VR frameworks for device-specific audio output (e.g., headphones or spatial speakers).
- Configurable parameters like sound attenuation models (inverse distance or logarithmic) and frequency ranges (20Hz-20kHz).
- Multi-source handling, supporting up to 32 concurrent audio sources per session.

## Usage Patterns

Always initialize the audio context first, then set up sound sources with positions. Use a loop for updates in real-time applications. For CLI, pipe audio files through the tool; for API, call endpoints in sequence. Pattern: Import library > Create audio context > Add sources > Render and update. Handle cleanup on exit to free resources.

## Common Commands/API

Use the OpenClaw CLI for quick prototyping or the REST API for programmatic control. Authentication requires setting `$SPATIAL_AUDIO_API_KEY` as an environment variable.

- CLI Command: Render audio with positioning  
  `spatial-audio render --input audio.wav --position 1.5 2.0 3.0 --hrtf default --output rendered.wav`  
  This processes an audio file at the specified 3D coordinates.

- API Endpoint: Create a sound source  
  POST to `https://api.openclaw.ai/spatial-audio/sources` with JSON body:  
  `{ "sourceId": "src1", "position": [0, 0, 5], "audioUrl": "s3://bucket/audio.mp3" }`  
  Response includes a source handle for updates.

- Code Snippet (Python): Initialize and position audio  
  ```python  
  import openclaw.spatial_audio as sa  
  context = sa.init(hrtf='default')  
  source = sa.add_source(context, position=[1, 2, 3])  
  sa.update_position(source, [4, 5, 6])  
  ```

- Config Format: JSON for API configs, e.g.,  
  `{ "hrtfProfile": "custom", "attenuation": "inverse", "maxSources": 16 }`  
  Load via CLI: `spatial-audio config load --file config.json`.

## Integration Notes

Integrate by adding the OpenClaw SDK as a dependency (e.g., `pip install openclaw-sdk` or via npm for JS). Set `$SPATIAL_AUDIO_API_KEY` before runtime. For AR/VR frameworks, wrap in Unity's AudioListener or WebXR's AudioContext—e.g., in Unity, attach the SpatialAudio component to the main camera. Ensure audio devices are compatible; check for Web Audio API support in browsers. For multi-platform, use abstraction layers like Three.js for web-based AR.

## Error Handling

Always check return codes or exceptions for errors. Common issues: Invalid positions (e.g., NaN values) return error code 400; audio device unavailability raises "DEVICE_NOT_FOUND". Handle with try-except blocks:  
```python  
try:  
    sa.render(context)  
except sa.AudioError as e:  
    if e.code == 400:  
        print("Invalid position; correct coordinates.")  
```  
For CLI, parse stderr output (e.g., "Error: HRTF not loaded—use --hrtf flag"). Retry transient errors like network failures with exponential backoff.

## Example 1: Basic Spatial Audio Setup in AR App

To set up 3D audio for an AR object:  
1. Initialize context: `sa.init(hrtf='builtin')`  
2. Add a sound source: `source = sa.add_source(context, position=[0, 1, 2], audioUrl='object_sound.mp3')`  
3. In the main loop, update based on user position: `sa.update_position(source, user_coords)`  
4. Render: `sa.render(context)`  
This creates a sound that moves relative to the user in an AR scene.

## Example 2: Dynamic Audio in VR Simulation

For a VR game with moving sound sources:  
1. Use CLI for prototyping: `spatial-audio render --input explosion.wav --position 10 0 0 --hrtf custom`  
2. In code (e.g., JavaScript):  
   ```javascript  
   const context = await sa.init();  
   const source = await sa.addSource(context, { position: [5, 0, 0] });  
   setInterval(() => sa.updateSource(source, [Math.random()*10, 0, 0]), 1000);  
   ```  
3. Integrate with VR framework to sync with head tracking for immersive effects.

## Graph Relationships

- Related Cluster: ar-vr (e.g., shares dependencies with "ar-rendering" skill).  
- Inbound Links: Depends on "audio-processing" for base audio handling.  
- Outbound Links: Enhances "vr-interaction" by providing spatial feedback.  
- Cross-Skill: Integrates with "3d-visualization" for synchronized audio-visual experiences.
