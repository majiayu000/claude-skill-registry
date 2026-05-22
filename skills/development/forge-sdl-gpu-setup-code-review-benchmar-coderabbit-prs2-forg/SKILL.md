---
name: forge-sdl-gpu-setup
description: Set up an SDL3 GPU application with the callback architecture. Use when creating a new SDL3 program that renders with the GPU API, or when someone asks how to get started with SDL GPU.
---

Set up an SDL3 GPU application using the patterns from forge-gpu.

## The callback model

SDL3 applications use four callbacks instead of a manual `main()` loop.
Define `SDL_MAIN_USE_CALLBACKS 1` before including the headers:

```c
#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
```

The four callbacks:

| Callback | Called | Purpose |
|----------|--------|---------|
| `SDL_AppInit` | Once at startup | Create window, GPU device, load resources |
| `SDL_AppEvent` | Once per event | Handle input, quit, resize |
| `SDL_AppIterate` | Once per frame | Record GPU commands, submit, present |
| `SDL_AppQuit` | Once at shutdown | Release GPU resources, free memory |

Return `SDL_APP_CONTINUE` to keep running, `SDL_APP_SUCCESS` to exit cleanly,
or `SDL_APP_FAILURE` to exit with an error. SDL calls `SDL_Quit()` for you
after `SDL_AppQuit` returns.

## Application state

Pack all persistent state into a struct and pass it through `appstate`:

```c
typedef struct app_state {
    SDL_Window    *window;
    SDL_GPUDevice *device;
    /* add fields as the app grows */
} app_state;
```

Allocate it in `SDL_AppInit` with `SDL_calloc`, assign to `*appstate`.
Free it in `SDL_AppQuit` with `SDL_free`.

## GPU device creation

```c
SDL_GPUDevice *device = SDL_CreateGPUDevice(
    SDL_GPU_SHADERFORMAT_SPIRV |   /* Vulkan    */
    SDL_GPU_SHADERFORMAT_DXIL  |   /* D3D12     */
    SDL_GPU_SHADERFORMAT_MSL,      /* Metal     */
    true,                          /* debug/validation layers */
    NULL                           /* no backend preference   */
);
```

- List all three shader formats for cross-platform support.
- Always enable debug mode during development.
- Call `SDL_GetGPUDeviceDriver(device)` to log the chosen backend.

## Window and swapchain

```c
SDL_Window *window = SDL_CreateWindow("Title", 1280, 720, 0);
SDL_ClaimWindowForGPUDevice(device, window);
```

`SDL_ClaimWindowForGPUDevice` creates the swapchain — a ring of textures the
OS composites to the screen.

## sRGB swapchain (correct gamma)

After claiming the window, request an sRGB swapchain so the GPU hardware
applies linear-to-sRGB conversion automatically.  Without this, interpolated
and blended colours look too dark.

```c
if (SDL_WindowSupportsGPUSwapchainComposition(
        device, window, SDL_GPU_SWAPCHAINCOMPOSITION_SDR_LINEAR)) {
    SDL_SetGPUSwapchainParameters(
        device, window,
        SDL_GPU_SWAPCHAINCOMPOSITION_SDR_LINEAR,
        SDL_GPU_PRESENTMODE_VSYNC);
}
```

- `SDR` (the default) → `B8G8R8A8_UNORM` — no gamma conversion
- `SDR_LINEAR` → `B8G8R8A8_UNORM_SRGB` — hardware converts linear→sRGB on write

Always query the swapchain format **after** this call, since it may have changed:

```c
SDL_GPUTextureFormat swapchain_format = SDL_GetGPUSwapchainTextureFormat(device, window);
```

## Per-frame rendering pattern

Every frame in `SDL_AppIterate` follows this rhythm:

```c
/* 1. Acquire a command buffer */
SDL_GPUCommandBuffer *cmd = SDL_AcquireGPUCommandBuffer(device);

/* 2. Acquire the swapchain texture (may be NULL if minimised) */
SDL_GPUTexture *swapchain = NULL;
SDL_AcquireGPUSwapchainTexture(cmd, window, &swapchain, NULL, NULL);

if (swapchain) {
    /* 3. Set up color target */
    SDL_GPUColorTargetInfo color_target = { 0 };
    color_target.texture     = swapchain;
    color_target.load_op     = SDL_GPU_LOADOP_CLEAR;
    color_target.store_op    = SDL_GPU_STOREOP_STORE;
    color_target.clear_color = (SDL_FColor){ 0.02f, 0.02f, 0.03f, 1.0f };

    /* 4. Begin render pass, draw, end render pass */
    SDL_GPURenderPass *pass = SDL_BeginGPURenderPass(cmd, &color_target, 1, NULL);
    /* ... draw calls go here ... */
    SDL_EndGPURenderPass(pass);
}

/* 5. Submit (also presents the swapchain) */
SDL_SubmitGPUCommandBuffer(cmd);
```

## Cleanup order

In `SDL_AppQuit`, release in reverse order of creation:

```c
SDL_ReleaseWindowFromGPUDevice(device, window);
SDL_DestroyWindow(window);
SDL_DestroyGPUDevice(device);
```

## CMake integration

```cmake
add_executable(my-app WIN32 main.c)
target_link_libraries(my-app PRIVATE SDL3::SDL3)

# Windows: copy SDL3.dll next to the executable
add_custom_command(TARGET my-app POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:SDL3::SDL3-shared>
        $<TARGET_FILE_DIR:my-app>
)
```

- `WIN32` prevents a console window on Windows; `SDL_main.h` provides `WinMain`.
- The DLL copy step is essential — without it the exe won't find SDL3.dll.

## Common mistakes

- Forgetting to call `SDL_ClaimWindowForGPUDevice` — swapchain acquire will fail.
- Not checking for `NULL` swapchain — happens when the window is minimised.
- Omitting `SDL_GPU_STOREOP_STORE` — your render results get discarded.
- Building without `WIN32` on Windows — creates an unwanted console window.
- Skipping `SDL_GPU_SWAPCHAINCOMPOSITION_SDR_LINEAR` — colours look washed out and interpolation is wrong.
- Returning `SDL_APP_SUCCESS` from `SDL_AppInit` — the app exits immediately
  with code 0 and no window visible. In SDL's callback architecture,
  `SDL_APP_SUCCESS` means "quit successfully" (clean exit), not "init
  succeeded." Only `SDL_APP_CONTINUE` keeps the event loop running.
  Both `SDL_APP_SUCCESS` and `SDL_APP_FAILURE` terminate the app.
