---
name: forge-camera-and-input
description: Set up a first-person camera with quaternion orientation, keyboard/mouse input, and delta time. Use when someone needs to fly through a 3D scene, handle WASD movement, mouse look, or frame-rate-independent motion in SDL3 GPU.
---

# Camera & Input — First-Person Camera, Keyboard/Mouse, Delta Time

This skill teaches how to add interactive camera controls to a 3D scene.
It builds on the `depth-and-3d` skill (MVP pipeline, depth testing) and
uses quaternion math from `common/math/forge_math.h`.

## When to use

- Adding a first-person camera to a 3D scene
- Handling keyboard input for smooth movement (WASD)
- Adding mouse look with relative mouse mode
- Making movement frame-rate independent with delta time
- Drawing multiple objects with different model transforms
- Transitioning from a fixed camera (`mat4_look_at`) to a player-controlled one

## Key API calls (ordered)

1. `SDL_SetWindowRelativeMouseMode` — capture mouse for FPS-style look
2. `SDL_GetKeyboardState` — poll which keys are currently held
3. `SDL_EVENT_MOUSE_MOTION` — read relative mouse deltas (xrel, yrel)
4. `quat_from_euler` — convert yaw+pitch to quaternion orientation
5. `quat_forward` / `quat_right` — extract movement directions
6. `mat4_view_from_quat` — build view matrix from position + quaternion
7. `SDL_PushGPUVertexUniformData` — push per-object MVP matrix
8. `SDL_DrawGPUIndexedPrimitives` — draw each object (one call per object)

## Code template

### Camera state

```c
#include "math/forge_math.h"

typedef struct app_state {
    /* ... GPU resources from depth-and-3d skill ... */

    /* Camera */
    vec3  cam_position;   /* world-space position */
    float cam_yaw;        /* radians, rotation around Y */
    float cam_pitch;      /* radians, rotation around X */

    /* Timing */
    Uint64 last_ticks;    /* previous frame timestamp (ms) */

    /* Input */
    bool mouse_captured;
} app_state;
```

### Initialize camera

```c
/* In SDL_AppInit: */
state->cam_position = vec3_create(0.0f, 1.6f, 6.0f);
state->cam_yaw      = 0.0f;
state->cam_pitch    = 0.0f;
state->last_ticks   = SDL_GetTicks();

/* Capture mouse for FPS-style look */
if (!SDL_SetWindowRelativeMouseMode(window, true)) {
    SDL_Log("SDL_SetWindowRelativeMouseMode failed: %s", SDL_GetError());
}
state->mouse_captured = true;
```

### Mouse look (in SDL_AppEvent)

```c
/* Escape: release mouse first, quit on second press */
if (event->type == SDL_EVENT_KEY_DOWN && event->key.key == SDLK_ESCAPE) {
    if (state->mouse_captured) {
        SDL_SetWindowRelativeMouseMode(state->window, false);
        state->mouse_captured = false;
    } else {
        return SDL_APP_SUCCESS;
    }
}

/* Click to recapture */
if (event->type == SDL_EVENT_MOUSE_BUTTON_DOWN && !state->mouse_captured) {
    SDL_SetWindowRelativeMouseMode(state->window, true);
    state->mouse_captured = true;
}

/* Mouse motion -> yaw/pitch */
if (event->type == SDL_EVENT_MOUSE_MOTION && state->mouse_captured) {
    #define MOUSE_SENSITIVITY 0.002f
    state->cam_yaw   -= event->motion.xrel * MOUSE_SENSITIVITY;
    state->cam_pitch -= event->motion.yrel * MOUSE_SENSITIVITY;

    /* Clamp pitch to avoid gimbal lock (see Math Lesson 08) */
    float max_pitch = 89.0f * FORGE_DEG2RAD;
    if (state->cam_pitch >  max_pitch) state->cam_pitch =  max_pitch;
    if (state->cam_pitch < -max_pitch) state->cam_pitch = -max_pitch;
}
```

### Delta time and keyboard movement (in SDL_AppIterate)

```c
/* Delta time — frame-rate independent movement */
Uint64 now_ms = SDL_GetTicks();
float dt = (float)(now_ms - state->last_ticks) / 1000.0f;
state->last_ticks = now_ms;
if (dt > 0.1f) dt = 0.1f;  /* clamp to prevent teleportation */

/* Build orientation quaternion from euler angles */
quat cam_orientation = quat_from_euler(
    state->cam_yaw, state->cam_pitch, 0.0f);

/* Extract movement directions from quaternion */
vec3 forward = quat_forward(cam_orientation);
vec3 right   = quat_right(cam_orientation);

/* Poll keyboard for continuous movement */
#define MOVE_SPEED 3.0f
const bool *keys = SDL_GetKeyboardState(NULL);

if (keys[SDL_SCANCODE_W] || keys[SDL_SCANCODE_UP]) {
    state->cam_position = vec3_add(state->cam_position,
        vec3_scale(forward, MOVE_SPEED * dt));
}
if (keys[SDL_SCANCODE_S] || keys[SDL_SCANCODE_DOWN]) {
    state->cam_position = vec3_add(state->cam_position,
        vec3_scale(forward, -MOVE_SPEED * dt));
}
if (keys[SDL_SCANCODE_D] || keys[SDL_SCANCODE_RIGHT]) {
    state->cam_position = vec3_add(state->cam_position,
        vec3_scale(right, MOVE_SPEED * dt));
}
if (keys[SDL_SCANCODE_A] || keys[SDL_SCANCODE_LEFT]) {
    state->cam_position = vec3_add(state->cam_position,
        vec3_scale(right, -MOVE_SPEED * dt));
}
if (keys[SDL_SCANCODE_SPACE]) {
    state->cam_position.y += MOVE_SPEED * dt;
}
if (keys[SDL_SCANCODE_LSHIFT]) {
    state->cam_position.y -= MOVE_SPEED * dt;
}
```

### View matrix (replaces mat4_look_at)

```c
/* Build view matrix from camera position + quaternion orientation.
 * This replaces the fixed mat4_look_at from the depth-and-3d skill. */
mat4 view = mat4_view_from_quat(state->cam_position, cam_orientation);

float aspect = (float)window_w / (float)window_h;
mat4 proj = mat4_perspective(60.0f * FORGE_DEG2RAD, aspect, 0.1f, 100.0f);
mat4 vp = mat4_multiply(proj, view);
```

### Drawing multiple objects

```c
/* Bind vertex/index buffers once (shared by all objects) */
SDL_BindGPUVertexBuffers(pass, 0, &vertex_binding, 1);
SDL_BindGPUIndexBuffer(pass, &index_binding, SDL_GPU_INDEXELEMENTSIZE_16BIT);

/* Draw each object with its own model matrix */
for (int i = 0; i < num_objects; i++) {
    mat4 model = mat4_multiply(
        mat4_translate(objects[i].position),
        mat4_multiply(
            mat4_rotate_y(elapsed * objects[i].rotation_speed),
            mat4_scale(vec3_create(s, s, s))
        )
    );
    mat4 mvp = mat4_multiply(vp, model);

    Uniforms u = { .mvp = mvp };
    SDL_PushGPUVertexUniformData(cmd, 0, &u, sizeof(u));
    SDL_DrawGPUIndexedPrimitives(pass, INDEX_COUNT, 1, 0, 0, 0);
}
```

## Camera types comparison

| Camera type | View matrix | Input | Best for |
|-------------|-------------|-------|----------|
| Fixed | `mat4_look_at(eye, target, up)` | None | Lesson 06, cutscenes |
| First-person | `mat4_view_from_quat(pos, quat)` | WASD + mouse | FPS games, editors |
| Orbit | `mat4_look_at(eye_from_spherical, target, up)` | Mouse drag | 3D viewers, RTS |

## Math library functions used

| Function | Purpose |
|----------|---------|
| `quat_from_euler(yaw, pitch, roll)` | Euler angles to quaternion |
| `quat_forward(q)` | Camera's look direction (-Z rotated by q) |
| `quat_right(q)` | Camera's right direction (+X rotated by q) |
| `mat4_view_from_quat(pos, q)` | View matrix from position + quaternion |
| `mat4_translate(v)` | Translation matrix for object placement |
| `mat4_rotate_y(angle)` | Y-axis rotation for spinning objects |
| `mat4_scale(v)` | Scale matrix for object sizing |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Camera doesn't respond to mouse | Check `SDL_SetWindowRelativeMouseMode(window, true)` succeeded |
| Movement is jittery or too fast | Use delta time: `speed * dt`, not just `speed` |
| Camera flips upside down | Clamp pitch to less than 90 degrees |
| Movement speed depends on frame rate | Multiply by `dt` (seconds since last frame) |
| Camera teleports after alt-tab | Clamp `dt` to a maximum (e.g., 0.1s) |
| Objects draw incorrectly with multiple draws | Push uniform BEFORE each draw call |
| Mouse look reversed | Check sign of `xrel`/`yrel` multiplication |
| Key events instead of key state | Use `SDL_GetKeyboardState` for smooth continuous movement |

## Reference

- [GPU Lesson 07 — Camera & Input](../../../lessons/gpu/07-camera-and-input/) — full implementation
- [Math Lesson 08 — Orientation](../../../lessons/math/08-orientation/) — quaternion theory
- [Math Lesson 09 — View Matrix](../../../lessons/math/09-view-matrix/) — view matrix construction
- [depth-and-3d skill](../forge-depth-and-3d/SKILL.md) — depth buffer, MVP pipeline
- `quat_forward()`, `mat4_view_from_quat()` in `common/math/forge_math.h`
