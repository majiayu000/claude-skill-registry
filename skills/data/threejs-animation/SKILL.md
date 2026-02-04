---
name: threejs-animation
description: Three.js animation - keyframe animation, skeletal animation, morph targets, animation mixing. Use when animating objects, playing GLTF animations, creating procedural motion, or blending animations.
---

# Three.js Animation

## Animation System

Three.js animation has three components:
1. **AnimationClip** - Keyframe data
2. **AnimationMixer** - Plays animations
3. **AnimationAction** - Controls playback

## Playing GLTF Animations

```javascript
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

const loader = new GLTFLoader();
loader.load("model.glb", (gltf) => {
  const model = gltf.scene;
  scene.add(model);

  const mixer = new THREE.AnimationMixer(model);
  const clips = gltf.animations;

  if (clips.length > 0) {
    const action = mixer.clipAction(clips[0]);
    action.play();
  }
});

// Update in animation loop
function animate() {
  mixer.update(clock.getDelta());
}
```

## AnimationAction Controls

```javascript
const action = mixer.clipAction(clip);

action.play();
action.stop();
action.reset();
action.paused = false;
action.timeScale = 1; // Speed (negative = reverse)
action.weight = 1;    // Blend weight

// Loop modes
action.loop = THREE.LoopRepeat;   // Loop forever
action.loop = THREE.LoopOnce;     // Play once
action.loop = THREE.LoopPingPong; // Alternate

action.clampWhenFinished = true;
```

## Crossfade Animations

```javascript
const action1 = mixer.clipAction(clip1);
const action2 = mixer.clipAction(clip2);

action1.play();

// Crossfade to action2
action1.crossFadeTo(action2, 0.5, true);
action2.play();
```

## Morph Targets

```javascript
// Access morph targets
mesh.morphTargetInfluences[0] = 0.5;

// By name
const smileIndex = mesh.morphTargetDictionary["smile"];
mesh.morphTargetInfluences[smileIndex] = 1;
```

## Procedural Animation

```javascript
const clock = new THREE.Clock();

function animate() {
  const t = clock.getElapsedTime();

  // Sine wave
  mesh.position.y = Math.sin(t * 2) * 0.5;

  // Circular motion
  mesh.position.x = Math.cos(t) * 2;
  mesh.position.z = Math.sin(t) * 2;
}
```

## Skeletal Animation

```javascript
const skinnedMesh = model.getObjectByProperty("type", "SkinnedMesh");
const skeleton = skinnedMesh.skeleton;

// Find bone
const headBone = skeleton.bones.find(b => b.name === "Head");
headBone.rotation.y = Math.sin(time) * 0.3;

// Skeleton helper
const helper = new THREE.SkeletonHelper(model);
scene.add(helper);
```
