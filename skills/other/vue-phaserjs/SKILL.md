---
name: vue-phaserjs
description: Esposter vue-phaserjs integration patterns — markRaw for Phaser objects in Pinia stores. Apply when writing Phaser game objects, stores, or vue-phaserjs components.
---

# vue-phaserjs Conventions

## Phaser Objects in Pinia Stores

**Always use `markRaw()` when assigning a Phaser object to any reactive ref in a Pinia store.**

Pinia devtools (dev mode only) deep-watches all store state via Vue's `traverse`. When it encounters a ref holding a Phaser object, it unwraps the ref and traverses into the Phaser internals. Phaser 3.85+ added `Frame.get glTexture()` as a getter that returns `null` before WebGL texture upload — causing a crash in dev mode that never occurs in prod.

`markRaw(obj)` sets `__v_skip = true`, which causes Vue's `traverse` to skip the object entirely.

When assigning a Phaser game object, plugin instance, or any class that holds Phaser scene/texture/keyboard references to a Pinia store ref, wrap the value with `markRaw()`:

```ts
// ✅ Correct — traverse-safe
controls.value = markRaw(new KeyboardControls(scene));
controls.value = markRaw(new JoystickControls());
sprite.value = markRaw(newSprite);
pathFollower.value = markRaw(newPathFollower);
tilemap.value = markRaw(newTilemap);
volumeSlider.value = markRaw(useSlider(scene, rectangle, { ... }));

// ❌ Wrong — will crash in dev mode via traverse → Frame.get glTexture → null
controls.value = new KeyboardControls(scene);
sprite.value = newSprite;
```

Any Phaser class that chains to `Scene → TextureManager → Texture → Frame → glTexture` is a risk:

- `GameObjects.*` (Sprite, Image, PathFollower, Container, Text, etc.)
- `Tilemaps.Tilemap`, `Tilemaps.TilemapLayer`
- `Input.Keyboard.Key`, `Input.Keyboard.CursorKeys` (via KeyboardPlugin → Scene)
- Rex plugin instances (Slider, VirtualJoystick, etc.)
- Any class that holds a `scene` reference
