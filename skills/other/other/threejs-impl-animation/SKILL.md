---
name: threejs-impl-animation
description: >
  Use when playing animations, crossfading between animation states,
  or loading skeletal animations from GLTF in Three.js. Prevents the
  common mistake of not calling mixer.update(delta) every frame,
  wrong crossfade setup, or missing Clock. Covers AnimationMixer,
  AnimationClip, AnimationAction, KeyframeTrack, crossfade, blending.
  Keywords: animation, AnimationMixer, AnimationClip, AnimationAction,
  crossfade, skeletal, GLTF animation, keyframe, blend, Clock.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-animation

## Quick Reference

### Architecture

```
AnimationClip        (data: array of KeyframeTrack objects)
  └── AnimationAction  (playback controller: play, pause, fade, crossfade)
        └── AnimationMixer (master scheduler: one per animated root object)
              └── Clock    (provides delta time for mixer.update)
```

ALWAYS create exactly ONE `AnimationMixer` per animated root object.
ALWAYS call `mixer.update(delta)` every frame inside the render loop.
NEVER instantiate `AnimationAction` directly -- ALWAYS use `mixer.clipAction(clip)`.

### Essential Imports

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
```

### Minimal Animation Setup

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const clock = new THREE.Clock();
let mixer;

const loader = new GLTFLoader();
loader.load('character.glb', (gltf) => {
  scene.add(gltf.scene);
  mixer = new THREE.AnimationMixer(gltf.scene);

  // Play all animations from the GLTF file
  gltf.animations.forEach((clip) => {
    mixer.clipAction(clip).play();
  });
});

function animate() {
  const delta = clock.getDelta();
  if (mixer) mixer.update(delta);
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);
```

### Critical Warnings

**NEVER** forget to call `mixer.update(delta)` in the render loop -- animations will NOT play without it.

**NEVER** use `new Date()` or `performance.now()` to compute delta manually -- ALWAYS use `THREE.Clock` or `renderer.setAnimationLoop` which provides stable frame timing.

**NEVER** call `mixer.clipAction(clip)` repeatedly in the render loop -- it caches internally, but the lookup is unnecessary overhead. ALWAYS store the returned action in a variable.

**NEVER** call `.play()` every frame -- call it ONCE to start playback. Calling `.play()` again on an already-playing action has no effect, but it signals misunderstanding.

**ALWAYS** call `.reset()` before `.play()` when restarting a stopped or finished action, or the action may resume from its last position.

**ALWAYS** set `action.clampWhenFinished = true` when using `LoopOnce` -- otherwise the action resets to the first frame when finished.

---

## AnimationMixer

The master scheduler that drives all animation actions for a single object hierarchy.

### Constructor

```js
const mixer = new THREE.AnimationMixer(rootObject);
```

`rootObject` is the root `Object3D` of the animated model (typically `gltf.scene`).

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `.time` | number | `0` | Global mixer time in seconds |
| `.timeScale` | number | `1` | Global speed multiplier; `0` pauses ALL actions |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `.clipAction(clip, root?, blendMode?)` | `AnimationAction` | Returns or creates an action for the clip |
| `.existingAction(clip, root?)` | `AnimationAction \| null` | Returns previously created action or `null` |
| `.update(delta)` | `this` | Advances mixer by delta seconds -- MUST call every frame |
| `.setTime(seconds)` | `this` | Sets global time, updates all actions |
| `.stopAllAction()` | `this` | Deactivates all scheduled actions |
| `.getRoot()` | `Object3D` | Returns the mixer's root object |
| `.uncacheAction(clip, root?)` | `void` | Deallocates cached action |
| `.uncacheClip(clip)` | `void` | Deallocates clip data |
| `.uncacheRoot(root)` | `void` | Deallocates root object data |

### Events

Listen via `mixer.addEventListener(type, callback)`:

| Event | Fires When |
|-------|-----------|
| `'finished'` | Action completes (ONLY with `LoopOnce` + `clampWhenFinished = true`) |
| `'loop'` | Action completes a loop iteration |

Event object properties: `{ action, loopDelta, type }`.

### Blend Modes

Pass as the third argument to `mixer.clipAction(clip, root, blendMode)`:

| Constant | Behavior |
|----------|----------|
| `THREE.NormalAnimationBlendMode` | Standard blending (default) |
| `THREE.AdditiveAnimationBlendMode` | Layered on top of base animation |

---

## AnimationAction

Controls playback of a single animation clip. NEVER instantiate directly.

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `.blendMode` | number | `NormalAnimationBlendMode` | Blending strategy |
| `.clampWhenFinished` | boolean | `false` | Pause at last frame when done |
| `.enabled` | boolean | `true` | Disable without resetting |
| `.loop` | number | `LoopRepeat` | Loop mode |
| `.paused` | boolean | `false` | Freeze playback |
| `.repetitions` | number | `Infinity` | Loop count |
| `.time` | number | `0` | Local time in seconds |
| `.timeScale` | number | `1` | Speed: `0` pauses, negative reverses |
| `.weight` | number | `1` | Blend influence `[0, 1]` |
| `.zeroSlopeAtEnd` | boolean | `true` | Smooth interpolation at loop end |
| `.zeroSlopeAtStart` | boolean | `true` | Smooth interpolation at loop start |

### Loop Modes

| Constant | Behavior |
|----------|----------|
| `THREE.LoopOnce` | Plays once, stops |
| `THREE.LoopRepeat` | Restarts from beginning each loop |
| `THREE.LoopPingPong` | Alternates forward/backward |

### Playback Methods

| Method | Description |
|--------|-------------|
| `.play()` | Start playback |
| `.stop()` | Stop and reset to start |
| `.reset()` | Reset time, weight, speed to initial state |
| `.startAt(mixerTime)` | Delay start until specified mixer time |

### Fading and Crossfade Methods

| Method | Description |
|--------|-------------|
| `.fadeIn(duration)` | Fade weight from `0` to `1` |
| `.fadeOut(duration)` | Fade weight from `1` to `0` |
| `.crossFadeFrom(fadeOutAction, duration, warp)` | Crossfade from another action into this one |
| `.crossFadeTo(fadeInAction, duration, warp)` | Crossfade from this action to another |
| `.stopFading()` | Cancel any active fade |

### Speed and Timing Methods

| Method | Description |
|--------|-------------|
| `.halt(duration)` | Decelerate timeScale to `0` over duration |
| `.warp(startScale, endScale, duration)` | Smoothly transition playback speed |
| `.stopWarping()` | Cancel any active warp |
| `.setDuration(seconds)` | Adjust timeScale so one loop takes exactly `seconds` |
| `.setEffectiveTimeScale(scale)` | Set effective time scale |
| `.setEffectiveWeight(weight)` | Set effective weight |
| `.setLoop(mode, repetitions)` | Set loop mode and count |
| `.syncWith(otherAction)` | Synchronize time with another action |

### Query Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `.isRunning()` | boolean | `true` only if actively playing |
| `.isScheduled()` | boolean | `true` if `.play()` was called |
| `.getClip()` | `AnimationClip` | The associated clip |
| `.getMixer()` | `AnimationMixer` | The owning mixer |
| `.getRoot()` | `Object3D` | The root object |
| `.getEffectiveTimeScale()` | number | Computed time scale |
| `.getEffectiveWeight()` | number | Computed weight |

---

## AnimationClip

A reusable set of keyframe tracks. Typically loaded from GLTF files.

### Constructor

```js
const clip = new THREE.AnimationClip(name, duration, tracks, blendMode);
```

- `name` -- string identifier (GLTF clips use names from the file)
- `duration` -- seconds; `-1` to auto-calculate from tracks
- `tracks` -- array of `KeyframeTrack` objects
- `blendMode` -- optional blend mode constant

### Key Static Methods

| Method | Description |
|--------|-------------|
| `AnimationClip.findByName(arrayOrObject, name)` | Look up clip by name |
| `AnimationClip.CreateFromMorphTargetSequence(name, targets, fps, noLoop)` | Create clip from morph targets |
| `AnimationClip.parse(json)` | Deserialize from JSON |

---

## KeyframeTrack Types

| Track Type | Value Type | Use Case |
|------------|-----------|----------|
| `VectorKeyframeTrack` | Vector3 | Position, scale |
| `QuaternionKeyframeTrack` | Quaternion | Rotation (uses slerp) |
| `NumberKeyframeTrack` | number | Opacity, intensity |
| `BooleanKeyframeTrack` | boolean | Visibility toggles |
| `ColorKeyframeTrack` | Color | Color animation |
| `StringKeyframeTrack` | string | Discrete string values |

### Interpolation Modes

| Constant | Behavior |
|----------|----------|
| `THREE.InterpolateDiscrete` | Step function, no smoothing |
| `THREE.InterpolateLinear` | Linear interpolation (default) |
| `THREE.InterpolateSmooth` | Cubic spline interpolation |

### PropertyBinding Path Format

```
"meshName.position"                    // animate position
"meshName.material.opacity"            // animate material property
"meshName.morphTargetInfluences[0]"    // animate morph target
"boneName.quaternion"                  // animate bone rotation
```

---

## Clock

### Constructor

```js
const clock = new THREE.Clock(autoStart); // autoStart defaults to true
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `.getDelta()` | number | Seconds since last `getDelta()` call |
| `.getElapsedTime()` | number | Total elapsed time in seconds |
| `.start()` | void | Start the clock |
| `.stop()` | void | Stop without resetting |

---

## Crossfade Pattern (Character State Machine)

```js
const actions = {};
gltf.animations.forEach((clip) => {
  actions[clip.name] = mixer.clipAction(clip);
});

let currentAction = actions['Idle'];
currentAction.play();

function switchAction(toName, duration = 0.5) {
  const toAction = actions[toName];
  toAction.reset();
  toAction.setEffectiveTimeScale(1);
  toAction.setEffectiveWeight(1);
  toAction.crossFadeFrom(currentAction, duration, true);
  toAction.play();
  currentAction = toAction;
}
```

ALWAYS call `.reset()` on the incoming action before crossfading.
ALWAYS store the current action reference for the next transition.

---

## Additive Animation Blending

```js
const baseAction = mixer.clipAction(baseClip);
const additiveAction = mixer.clipAction(
  additiveClip, undefined, THREE.AdditiveAnimationBlendMode
);

baseAction.play();
additiveAction.play();
additiveAction.setEffectiveWeight(0.5);
```

Use additive blending for layered effects: breathing, damage reactions, aim offsets.

---

## Morph Target Animation

```js
// Manual control
mesh.morphTargetInfluences[0] = Math.sin(elapsed) * 0.5 + 0.5;

// Via GLTF animation clip (preferred)
const morphAction = mixer.clipAction(morphClip);
morphAction.play();
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Full API signatures
- [references/examples.md](references/examples.md) -- Working code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do

### Official Sources

- https://threejs.org/docs/#api/en/animation/AnimationMixer
- https://threejs.org/docs/#api/en/animation/AnimationAction
- https://threejs.org/docs/#api/en/animation/AnimationClip
- https://threejs.org/docs/#api/en/animation/KeyframeTrack
- https://threejs.org/docs/#api/en/core/Clock
- https://threejs.org/examples/#webgl_animation_skinning_blending
