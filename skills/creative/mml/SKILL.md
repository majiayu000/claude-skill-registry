---
name: mml
description: "Build 3D scenes and interactive experiences using MML (Metaverse Markup Language) for the Otherside metaverse and other MML-compatible environments. Use when creating 3D objects, worlds, interactive elements, animations, models, characters, audio/video, labels, collision-based interactions, position tracking, chat integration, or any MML document. Triggers on: MML, metaverse markup, 3D scene building, Otherside world building, m-cube, m-model, m-character, m-group, m-frame, m-attr-anim."
---

# MML (Metaverse Markup Language)

> **Full compiled reference:** `/home/ubuntu/.openclaw/workspace/research/mml-reference.md`
> Source: mml.io + DashBODK Studio (dashbodk.vercel.app/docs). All elements, attrs, events, collision patterns.

MML is an HTML-like markup language for building 3D scenes. Documents are served via WebSocket and rendered by clients (Web/Three.js or Unreal Engine). MML supports scripting via inline `<script>` tags (standard DOM APIs).

## Key Concepts

- **Units:** Positions in meters, rotations in degrees, font sizes in centimeters
- **Coordinate system:** x (right), y (up), z (forward)
- **Common attributes:** All visible elements share `x y z rx ry rz sx sy sz visible id class`
- **Collision system:** Set `collision-interval` (ms) on an element to receive `collisionstart`, `collisionmove`, `collisionend` events
- **Document time:** Animations and media use document lifecycle time (ms since document start)
- **Scripting:** Standard DOM manipulation via `<script>` tags. Use `document.getElementById()`, `addEventListener()`, `setAttribute()`, etc.

## Elements Quick Reference

| Element | Purpose | Key Attrs |
|---------|---------|-----------|
| `m-group` | Container, transforms children as unit | (transform only) |
| `m-cube` | 3D box | `width height depth color opacity` |
| `m-sphere` | 3D sphere | `radius color opacity` |
| `m-cylinder` | 3D cylinder | `radius height color opacity` |
| `m-plane` | Flat surface | `width height color opacity` |
| `m-model` | Load 3D model (GLTF/OBJ/FBX) | `src anim-src anim-loop anim-enabled start-time pause-time` |
| `m-character` | 3D character (composable with m-model children) | `src anim-src anim-loop anim-enabled start-time pause-time` |
| `m-light` | Point or spotlight | `type intensity distance angle enabled cast-shadows color` |
| `m-image` | Display image in 3D | `src width height emissive opacity` |
| `m-video` | Display video in 3D (supports WHEP streaming) | `src width height emissive loop enabled volume start-time pause-time` |
| `m-audio` | Spatial audio | `src loop loop-duration enabled volume cone-angle cone-falloff-angle start-time pause-time` |
| `m-label` | Text on a plane | `content width height font-size font-color padding alignment color emissive` |
| `m-frame` | Embed another MML document | `src min-x max-x min-y max-y min-z max-z load-range unload-range` |
| `m-link` | Clickable link (no visual) | `href target` |
| `m-prompt` | User text input on click | `message placeholder prefill onprompt` |
| `m-interaction` | Action at a point in space | `range in-focus line-of-sight priority prompt oninteract` |
| `m-position-probe` | Track user positions | `range interval onpositionenter onpositionmove onpositionleave` |
| `m-chat-probe` | Receive chat messages | `range onchat` |
| `m-attr-anim` | Keyframe animation (doc-time synced) | `attr start end start-time pause-time duration loop easing ping-pong ping-pong-delay` |
| `m-attr-lerp` | Smooth attribute transitions | `attr duration easing` |

## Common Patterns

### Basic scene with transforms
```html
<m-group x="0" y="1" z="-5">
  <m-cube color="red" width="2" height="0.5" depth="2"></m-cube>
  <m-sphere color="blue" radius="0.3" y="1"></m-sphere>
</m-group>
```

### Animation (looping rotation)
```html
<m-cube color="green" y="2">
  <m-attr-anim attr="ry" start="0" end="360" duration="3000" loop="true"></m-attr-anim>
</m-cube>
```

### Smooth transitions on attribute changes
```html
<m-cube id="box" color="red" y="1">
  <m-attr-lerp attr="x,y,z" duration="500" easing="easeInOutQuad"></m-attr-lerp>
</m-cube>
```

### Click interaction
```html
<m-cube id="btn" color="blue" onclick="
  this.setAttribute('color', this.getAttribute('color') === 'blue' ? 'red' : 'blue');
"></m-cube>
```

### Collision detection
```html
<m-cube id="platform" width="5" height="0.2" depth="5" color="green" collision-interval="100">
</m-cube>
<script>
  const platform = document.getElementById("platform");
  platform.addEventListener("collisionstart", (e) => {
    platform.setAttribute("color", "yellow");
  });
  platform.addEventListener("collisionend", (e) => {
    platform.setAttribute("color", "green");
  });
</script>
```

### Position tracking
```html
<m-position-probe id="probe" range="20" interval="500"></m-position-probe>
<m-label id="info" content="Waiting..." y="3" width="3" height="1"></m-label>
<script>
  const probe = document.getElementById("probe");
  const info = document.getElementById("info");
  probe.addEventListener("positionenter", (e) => {
    info.setAttribute("content", `User ${e.detail.connectionId} entered`);
  });
</script>
```

### Load 3D model with animation
```html
<m-model src="https://example.com/character.glb" 
         anim-src="https://example.com/dance.glb"
         anim-loop="true" y="0" sx="1" sy="1" sz="1">
</m-model>
```

### Composing documents with m-frame
```html
<m-frame src="https://example.com/other-scene.html" 
         x="10" y="0" z="0"
         min-x="-5" max-x="5" min-y="0" max-y="10" min-z="-5" max-z="5">
</m-frame>
```

### Spatial audio
```html
<m-audio src="https://example.com/music.mp3" 
         loop="true" volume="0.5" 
         x="0" y="2" z="0">
</m-audio>
```

### Chat-reactive elements
```html
<m-chat-probe id="chat" range="10"></m-chat-probe>
<m-label id="msg" content="" y="3" width="4" height="1"></m-label>
<script>
  document.getElementById("chat").addEventListener("chat", (e) => {
    document.getElementById("msg").setAttribute("content", e.detail.message);
  });
</script>
```

## Easing Functions

Available for `m-attr-anim` and `m-attr-lerp`:
`easeInQuad`, `easeOutQuad`, `easeInOutQuad`, `easeInCubic`, `easeOutCubic`, `easeInOutCubic`, `easeInQuart`, `easeOutQuart`, `easeInOutQuart`, `easeInQuint`, `easeOutQuint`, `easeInOutQuint`, `easeInSine`, `easeOutSine`, `easeInOutSine`, `easeInExpo`, `easeOutExpo`, `easeInOutExpo`, `easeInCirc`, `easeOutCirc`, `easeInOutCirc`, `easeInElastic`, `easeOutElastic`, `easeInOutElastic`, `easeInBack`, `easeOutBack`, `easeInOutBack`, `easeInBounce`, `easeOutBounce`, `easeInOutBounce`

Omit easing for linear interpolation.

## Events Reference

| Event | Source | Key Properties |
|-------|--------|----------------|
| `click` | Any clickable element | `detail.connectionId`, `detail.position` |
| `collisionstart` | Elements with `collision-interval` | `detail.connectionId`, `detail.position` |
| `collisionmove` | Elements with `collision-interval` | `detail.connectionId`, `detail.position` |
| `collisionend` | Elements with `collision-interval` | `detail.connectionId` |
| `positionenter` | `m-position-probe` | `detail.connectionId`, `detail.position`, `detail.rotation` |
| `positionmove` | `m-position-probe` | `detail.connectionId`, `detail.position`, `detail.rotation` |
| `positionleave` | `m-position-probe` | `detail.connectionId` |
| `chat` | `m-chat-probe` | `detail.message`, `detail.connectionId` |
| `interact` | `m-interaction` | `detail.connectionId` |
| `prompt` | `m-prompt` | `detail.value`, `detail.connectionId` |
| `connected` / `disconnected` | Document-level | `detail.connectionId` |

## Platform Support

Most elements work on both Web and Unreal. Notable exceptions:
- `m-link`: Web only
- `m-attr-lerp`: Web only
- `m-frame` bounds/load-range: Web only
- `socket` attribute: Web only

## Full Element Docs

For detailed attribute lists per element, see [references/elements.md](references/elements.md).
