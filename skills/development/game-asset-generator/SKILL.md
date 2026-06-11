---
name: game-asset-generator
description: "Deterministic palette/matrix pixel art (not AI). Use for procedural tile art, color-quantized output, matrix sprites."
agent: typescript-frontend-engineer
user-invocable: false
command: /game-assets
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - pixel art
    - tile pattern
    - palette quantize
    - matrix sprite
    - meshy
    - meshyai
    - generate 3d model
    - text to 3d
    - image to 3d
    - world labs
    - gaussian splat
    - splat environment
    - game asset
    - fal ai
    - fal.ai
    - generate texture
    - generate image for game
    - 3d character
    - game model
    - rig model
    - animate model
    - game environment
    - sketchfab
    - poly pizza
    - poly haven
  pairs_with:
    - threejs-builder
    - typescript-frontend-engineer
  complexity: Medium
  category: game-development
---

# Game Asset Generator Skill

## Overview

This skill generates game-ready assets (3D models, Gaussian Splat environments, 2D sprites, images/textures) using AI APIs and free asset sources. It follows a three-phase workflow: DETECT the asset type -> GENERATE via the appropriate API or source -> INTEGRATE into the game. Only the relevant reference is loaded per task -- do not load all references upfront.

**Scope**: Use for AI-generated 3D models, world environments, pixel art sprites, concept art, textures, and sourcing free pre-built assets. Keep game engine scripting, physics, game loop logic, and shader authoring in `threejs-builder` after asset generation.

---

## Phase 1: DETECT

**Goal**: Identify the asset type from the request and load the single corresponding reference.

**Step 1: Classify the request**

| Signal in request | Asset Type | Reference to load |
|-------------------|-----------|-------------------|
| "3D model", "character model", "generate model", GLB, mesh, rig, animate, humanoid | **3D Model** | `references/meshyai.md` |
| "environment", "world", "scene background", "gaussian splat", "splat", volumetric | **Environment** | `references/worldlabs.md` |
| "sprite", "pixel art", "2D character", "tile", "tileset", canvas sprite | **2D Sprite** | `references/pixel-art-sprites.md` |
| "image", "texture", "concept art", "icon", "generate image", chroma key | **Image / Texture** | `references/fal-ai-image.md` |
| No API key available, "free asset", "find model", "download asset", generation failed | **Existing Assets** | `references/asset-sources.md` |

If the request is ambiguous between 3D Model and Image, ask: "Do you need a 3D mesh (GLB file for a Three.js scene) or a 2D image/texture?"

**Step 2: Check API key availability**

Before calling any paid API, verify the required key exists:

```bash
grep -E "MESHY_API_KEY|WLT_API_KEY|FAL_KEY" ~/.env 2>/dev/null
```

If the required key is missing, the fallback chain applies -- load `references/asset-sources.md` alongside the primary reference.

**Fallback chain**: Meshy API -> Sketchfab search -> Poly Haven -> Poly.pizza -> BoxGeometry placeholder. All sources output GLB into the same path so game loading code does not change.

**Gate**: Asset type identified, relevant reference loaded. Proceed to Phase 2 only when gate passes.

---

## Phase 2: GENERATE

**Goal**: Call the API or source to produce the asset. Follow the loaded reference exactly -- it is the authoritative guide for its API.

**Core constraints (all asset types)**:
- **Download immediately** -- Meshy retains assets only 3 days; World Labs SPZ files expire similarly. Never assume a URL will be valid tomorrow.
- **Output to a stable path** -- write assets to `public/assets/` or an equivalent game-accessible directory so integration code does not need path changes per asset.
- **Save the .meta.json sidecar** -- every generated asset gets a `.meta.json` recording the prompt, model, generation timestamp, and asset ID. Required for regeneration and auditing.
- **Validate the output file** -- after download, confirm file size > 0 and extension matches expected type (GLB, SPZ, PNG, etc.) before proceeding.

**Per-type generation summary** (read the reference for full API details):

**3D Model (Meshy)**: Two-step pipeline -- preview (fast, low quality, confirms prompt works) -> refine (full quality). Auto-rig only for humanoids meeting all criteria: bipedal, textured, clearly defined limbs. Animate rigged models with walk/run/idle presets. Post-process with `scripts/optimize-glb.mjs` for 80-95% size reduction before integration.

**Environment (World Labs)**: Upload reference image (preferred over text-only) -> poll 3-8 minutes -> download SPZ + GLB collider + panorama JPG. Y-axis flip (`rotation.x = Math.PI`) required after loading into Three.js scene.

**2D Sprite (code-only)**: Canvas-based generation -- no API call. Load `references/pixel-art-sprites.md` and generate sprites from the palette and matrix system defined there. Works without any API key.

**Image / Texture (fal.ai)**: Queue-based API -- submit job -> poll for result. Choose model endpoint based on need (GPT Image 1.5 for transparency, Nano Banana 2 for speed). Use `#00FF00` chroma-key background when the asset needs transparency extraction.

**Gate**: Asset file downloaded and validated (size > 0, correct extension). .meta.json saved. Proceed to Phase 3 only when gate passes.

---

## Phase 3: INTEGRATE

**Goal**: Load the generated asset into the game scene correctly.

**Core constraint**: Use `SkeletonUtils.clone()` -- never `.clone()` -- for animated models. Regular `.clone()` breaks skeleton bindings and leaves the model in a permanent T-pose. This is the single most common integration failure with rigged GLBs.

```javascript
import { SkeletonUtils } from 'three/addons/utils/SkeletonUtils.js';

// Load once, clone for each instance
loader.load('/assets/character.glb', (gltf) => {
  const instance = SkeletonUtils.clone(gltf.scene);
  scene.add(instance);
});
```

**GLB loading (Three.js)**:
```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

const loader = new GLTFLoader();
loader.setDRACOLoader(dracoLoader); // Required for Draco-compressed GLBs from Meshy optimizer
loader.load('/assets/model.glb', (gltf) => {
  const model = gltf.scene;
  const box = new THREE.Box3().setFromObject(model);
  const center = box.getCenter(new THREE.Vector3());
  model.position.sub(center);
  scene.add(model);
});
```

**Gaussian Splat (World Labs)** -- see `references/worldlabs.md` for the `@sparkjsdev/spark` SplatMesh integration. The Y-axis flip and raycast direction inversion are required, not optional.

**Animation playback**:
```javascript
const mixer = new THREE.AnimationMixer(model);
const action = mixer.clipAction(gltf.animations[0]); // walk/run/idle from Meshy
action.play();

// In animation loop:
mixer.update(deltaTime);
```

**Gate**: Asset visible in scene. No console errors. Animations play if applicable.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| "3D model", "character model", "generate model", GLB, mesh, rig, animate, humanoid | `meshyai.md` | **3D Model** |
| "environment", "world", "scene background", "gaussian splat", "splat", volumetric | `worldlabs.md` | **Environment** |
| "sprite", "pixel art", "2D character", "tile", "tileset", canvas sprite | `pixel-art-sprites.md` | **2D Sprite** |
| "image", "texture", "concept art", "icon", "generate image", chroma key | `fal-ai-image.md` | **Image / Texture** |
| No API key available, "free asset", "find model", "download asset", generation failed | `asset-sources.md` | **Existing Assets** |
| `references/meshyai.md` | `meshyai.md` | 3D model generation request |
| `references/worldlabs.md` | `worldlabs.md` | Environment / Gaussian Splat request |
| `references/fal-ai-image.md` | `fal-ai-image.md` | Image, texture, or concept art request |
| `references/asset-sources.md` | `asset-sources.md` | No API key, fallback chain, or "find free asset" |
| `references/pixel-art-sprites.md` | `pixel-art-sprites.md` | 2D sprite or pixel art request |

## Error Handling

### Error: "GLB loads but model is in T-pose"
Cause: Used `.clone()` instead of `SkeletonUtils.clone()` on a rigged model.
Solution: Replace `gltf.scene.clone()` with `SkeletonUtils.clone(gltf.scene)`. Import from `three/addons/utils/SkeletonUtils.js`.

### Error: "Meshy task stuck in PENDING"
Cause: API key invalid, quota exceeded, or Meshy service issue.
Solution:
1. Verify `MESHY_API_KEY` is set in `~/.env` and the value is current
2. Check quota at app.meshy.ai
3. If quota exhausted, fall through to `references/asset-sources.md` fallback chain
4. Use status mode: `node scripts/meshy-generate.mjs status <task_id>`

### Error: "Downloaded GLB is 0 bytes or corrupt"
Cause: URL expired (Meshy 3-day limit) or network error during download.
Solution: Regenerate -- do not attempt to repair a corrupt GLB. Resubmit using the prompt saved in `.meta.json`.

### Error: "Gaussian Splat renders but objects fall through floor"
Cause: Raycast direction inverted after Y-axis flip on the SplatMesh.
Solution: Load `references/worldlabs.md` -- the fix is in the raycast inversion section.

### Error: "fal.ai request returns 401"
Cause: `FAL_KEY` missing or incorrectly formatted. fal.ai uses `Key $FAL_KEY` format (not Bearer).
Solution: Confirm `FAL_KEY` is in `~/.env`. Authorization header must be `Key <your-key>` -- not `Bearer <your-key>`.

### Error: "gltf-transform command not found"
Cause: `@gltf-transform/cli` not installed globally.
Solution: `npm install -g @gltf-transform/cli`

---

## References

| Reference | When to load | Content |
|-----------|-------------|---------|
| `references/meshyai.md` | 3D model generation request | Meshy API: text-to-3D, image-to-3D, rig, animate, status polling, optimize-glb |
| `references/worldlabs.md` | Environment / Gaussian Splat request | World Labs Marble API: SPZ generation, SplatMesh renderer, Y-flip gotcha |
| `references/fal-ai-image.md` | Image, texture, or concept art request | fal.ai: 8 model endpoints, queue API, cost tracking, chroma-key |
| `references/asset-sources.md` | No API key, fallback chain, or "find free asset" | Sketchfab, Poly Haven, Poly.pizza search and download workflows |
| `references/pixel-art-sprites.md` | 2D sprite or pixel art request | Canvas sprite matrices, palette system, animation frames (no API needed) |
