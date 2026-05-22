---
name: forge-draggable-windows
description: Add draggable, z-ordered, collapsible windows to a ForgeUiContext application. Wraps the existing immediate-mode UI context with deferred draw ordering and input routing by z-order.
---

Add draggable windows with z-ordering and collapse/expand to any application
that uses `ForgeUiContext`. Based on UI Lesson 10.

## When to use

- You need draggable floating panels that users can rearrange
- You need z-ordering so overlapping windows draw and receive input correctly
- You need a collapse toggle to let users minimize windows to their title bar
- You want deferred draw ordering (per-window draw lists sorted by z at frame end)
- You need input routing that respects z-order (foreground windows block clicks
  to background windows in overlap regions)

## Key API calls

- `forge_ui_wctx_init(wctx, ctx)` -- initialize a window context wrapping an
  existing `ForgeUiContext`
- `forge_ui_wctx_free(wctx)` -- free per-window draw list buffers
- `forge_ui_wctx_begin(wctx)` -- begin a frame (determines hovered window from
  previous frame data, resets per-frame state)
- `forge_ui_wctx_end(wctx)` -- end a frame (sorts draw lists by z_order,
  appends to main buffers in back-to-front order)
- `forge_ui_wctx_window_begin(wctx, id, title, state)` -- begin a window
  (returns true if expanded, false if collapsed or invalid)
- `forge_ui_wctx_window_end(wctx)` -- end a window (computes content height,
  draws scrollbar, restores main buffers)

## Correct order

1. **Initialize** a `ForgeUiWindowContext` wrapping your `ForgeUiContext`
2. **Each frame**: call `forge_ui_ctx_begin()`, then `forge_ui_wctx_begin()`
3. **Declare windows**: `window_begin` / widgets / `window_end` blocks
4. **End frame**: call `forge_ui_wctx_end()`, then `forge_ui_ctx_end()`

Widget IDs must be unique and each window reserves three IDs: `id` for the
window/drag handle, `id+1` for the scrollbar, `id+2` for the collapse toggle.

When `window_begin` returns false (collapsed or invalid), skip all child
widgets and do **not** call `window_end`.

## Key concepts

1. **ForgeUiWindowState** -- application-owned persistent state: `rect`
   (position/size, updated by drag), `scroll_y` (content scroll offset),
   `collapsed` (toggled by clicking the collapse button), `z_order` (draw
   priority, higher = on top, updated on click)
2. **Grab offset** -- stored on the press frame as `(mouse - rect.origin)`;
   used during drag to maintain the relative click position
3. **Bring-to-front** -- on any mouse press inside a window, set
   `z_order = max(all z) + 1`
4. **Deferred draw** -- per-window vertex/index buffers assembled at frame end
   in back-to-front z-order
5. **Input routing pre-pass** -- `wctx_begin` scans previous frame's window
   rects to find the topmost window under the mouse; widgets in other windows
   silently fail hit tests
6. **Keyboard suppression** -- widgets in covered windows preserve visual focus
   but do not process keyboard input (games can suppress window input for
   game controls without the window appearing unfocused)

## Common mistakes

1. **Forgetting `wctx_end()`** -- without it, per-window draw lists are never
   appended to the main buffer and nothing renders
2. **Calling `window_end` when collapsed** -- `window_begin` returns false for
   collapsed windows; calling `window_end` in that case corrupts state
3. **ID collisions** -- each window needs 3 contiguous IDs (`id`, `id+1`,
   `id+2`); overlapping ranges cause unpredictable hot/active behavior
4. **Not checking `wctx_init` return** -- returns false if the context pointer
   is null or allocation fails
5. **Resetting grab offset** -- the `ForgeUiWindowContext` grab offset must
   persist across frames (not reset by `wctx_begin`) because drags span
   multiple frames
6. **Ignoring one-frame lag** -- `hovered_window_id` uses previous frame data;
   z-order changes take effect on the next frame's input routing

## Ready-to-use template

### Three overlapping windows

```c
#include "ui/forge_ui.h"
#include "ui/forge_ui_window.h"

/* Window IDs (each reserves id, id+1, id+2) */
#define ID_WIN_A  100
#define ID_WIN_B  200
#define ID_WIN_C  300

/* Widget IDs inside windows */
#define ID_CB_1   110
#define ID_SLIDER 120

/* Widget dimensions */
#define LABEL_HEIGHT     26.0f
#define CHECKBOX_HEIGHT  28.0f
#define SLIDER_HEIGHT    30.0f
#define SLIDER_MIN        0.0f
#define SLIDER_MAX      100.0f

/* Application-owned window state (persists across frames) */
ForgeUiWindowState win_a = {
    .rect = { 30.0f, 30.0f, 260.0f, 280.0f },
    .scroll_y = 0.0f,
    .collapsed = false,
    .z_order = 0
};
ForgeUiWindowState win_b = {
    .rect = { 200.0f, 80.0f, 260.0f, 200.0f },
    .scroll_y = 0.0f,
    .collapsed = false,
    .z_order = 1
};

/* Application-owned widget state */
bool option_a = true;
float slider_val = 50.0f;

/* --- Frame loop --- */

ForgeUiContext ctx;
forge_ui_ctx_init(&ctx, &atlas);

ForgeUiWindowContext wctx;
forge_ui_wctx_init(&wctx, &ctx);

/* Each frame: */
forge_ui_ctx_begin(&ctx, mouse_x, mouse_y, mouse_down);
ctx.scroll_delta = scroll_delta;
forge_ui_wctx_begin(&wctx);

/* Window A: settings */
if (forge_ui_wctx_window_begin(&wctx, ID_WIN_A, "Settings", &win_a)) {
    (void)forge_ui_ctx_checkbox_layout(
        wctx.ctx, ID_CB_1, "Option A", &option_a, CHECKBOX_HEIGHT);
    (void)forge_ui_ctx_slider_layout(
        wctx.ctx, ID_SLIDER, &slider_val,
        SLIDER_MIN, SLIDER_MAX, SLIDER_HEIGHT);
    forge_ui_wctx_window_end(&wctx);
}

/* Window B: status */
if (forge_ui_wctx_window_begin(&wctx, ID_WIN_B, "Status", &win_b)) {
    forge_ui_ctx_label_layout(wctx.ctx, "Hello, windows!",
                              LABEL_HEIGHT, 0.9f, 0.9f, 0.9f, 1.0f);
    forge_ui_wctx_window_end(&wctx);
}

forge_ui_wctx_end(&wctx);   /* sorts and assembles draw lists */
forge_ui_ctx_end(&ctx);      /* finalizes hot/active state */

/* Use ctx.vertices, ctx.indices, ctx.vertex_count, ctx.index_count
 * for rendering — vertices are in correct z-sorted draw order. */
```

### Key observations

- Pass `wctx.ctx` (not `&ctx`) to widget functions inside a window -- the
  window context redirects the vertex/index pointers
- `window_begin` returns false for both collapsed windows and validation
  failures -- never call `window_end` when it returns false
- Widget return values (`checkbox_layout`, `slider_layout`) indicate whether
  the value changed, not success/failure -- `(void)` cast is fine when the
  result is not needed
- Set `ctx.scroll_delta` before `wctx_begin` so the input routing pre-pass
  can associate the scroll with the correct window

## Reference

- [UI Lesson 10 -- Windows](../../../lessons/ui/10-windows/) -- full
  walkthrough with diagrams and 12-frame demo
- [UI Lesson 09 -- Panels and Scrolling](../../../lessons/ui/09-panels-and-scrolling/) --
  the panel infrastructure that windows extend
- [UI Lesson 08 -- Layout](../../../lessons/ui/08-layout/) -- the layout
  system used for widget positioning inside windows
- [`common/ui/forge_ui_window.h`](../../../common/ui/forge_ui_window.h) --
  window system implementation
- [`common/ui/forge_ui_ctx.h`](../../../common/ui/forge_ui_ctx.h) -- the
  underlying immediate-mode UI context
