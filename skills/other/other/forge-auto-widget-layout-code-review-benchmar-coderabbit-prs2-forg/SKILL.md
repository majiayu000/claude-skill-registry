---
name: forge-auto-widget-layout
description: Add automatic widget layout to a ForgeUiContext application. Replace manual rect calculations with a stack-based cursor model supporting vertical/horizontal directions, padding, spacing, and nesting.
---

Add automatic widget positioning to any application that uses `ForgeUiContext`.
Based on UI Lesson 08.

## When to use

- You have an immediate-mode UI with manually computed widget rects and want
  to automate placement
- You need a vertical panel of stacked widgets (labels, checkboxes, sliders)
- You need a horizontal row of buttons or controls side by side
- You need nested layouts (a vertical panel containing a horizontal button row)
- You want to change padding or add/remove widgets without recalculating every
  rect by hand

## Key API calls

- `forge_ui_ctx_layout_push(ctx, rect, direction, padding, spacing)` — push a
  layout region onto the stack
- `forge_ui_ctx_layout_pop(ctx)` — pop and return to the parent layout
- `forge_ui_ctx_layout_next(ctx, size)` — return the next widget rect and
  advance the cursor
- `forge_ui_ctx_label_layout(ctx, text, size, r, g, b, a)` — label placed by
  the current layout
- `forge_ui_ctx_button_layout(ctx, id, text, size)` — button placed by the
  current layout
- `forge_ui_ctx_checkbox_layout(ctx, id, label, value, size)` — checkbox
  placed by the current layout
- `forge_ui_ctx_slider_layout(ctx, id, value, min, max, size)` — slider
  placed by the current layout

## Correct order

1. **Push a layout** with a bounding rect, direction, padding, and spacing
2. **Declare widgets** using `_layout()` variants — each call advances the
   cursor automatically
3. **For nested layouts**: call `layout_next()` to reserve a sub-rect from the
   parent, then `layout_push()` inside that rect
4. **Pop nested layouts** before continuing in the parent
5. **Pop the root layout** when done

Every `layout_push()` must have a matching `layout_pop()` — including on error
paths. Unmatched pushes are logged as warnings by `forge_ui_ctx_end()`.

## Key concepts

1. **Layout cursor** — a position (x, y) that starts at the top-left content
   area (after padding) and advances after each widget
2. **Direction** — `FORGE_UI_LAYOUT_VERTICAL` advances downward (widgets get
   full width, caller specifies height); `FORGE_UI_LAYOUT_HORIZONTAL` advances
   rightward (widgets get full height, caller specifies width)
3. **Padding** — uniform inset from all four edges of the layout rect
4. **Spacing** — gap inserted before each widget except the first
5. **Size parameter** — the widget dimension along the layout's primary axis
   (height for vertical, width for horizontal); the cross-axis dimension is
   filled automatically
6. **Layout stack** — up to `FORGE_UI_LAYOUT_MAX_DEPTH` (8) nested layouts
7. **Spacing-before-item model** — spacing is added before each item (except
   the first), keeping `remaining_h`/`remaining_w` accurate

## Common mistakes

1. **Forgetting `layout_pop()`** — every push needs a pop on every code path,
   including early returns from failed nested pushes
2. **Using standard widget API inside a layout** — use `_layout()` variants
   (`button_layout`, `checkbox_layout`) to get automatic positioning; the
   standard API (`button`, `checkbox`) still requires explicit rects
3. **Wrong size parameter** — in a vertical layout, `size` is height; in a
   horizontal layout, `size` is width. Passing the wrong dimension produces
   unexpectedly stretched or squished widgets
4. **Not reserving a sub-rect for nested layouts** — call `layout_next(row_h)`
   first to get the sub-rect, then push a new layout inside it. Pushing a
   layout with the full parent rect would overlap existing widgets
5. **Exceeding stack depth** — `layout_push()` returns `false` if the stack
   overflows (8 levels max). Always check the return value

## Ready-to-use template

### Vertical panel with mixed widgets

```c
#define PANEL_PADDING    16.0f   /* inset from panel edges */
#define WIDGET_SPACING    8.0f   /* vertical gap between widgets */
#define LABEL_HEIGHT     30.0f   /* height of a label row */
#define CHECKBOX_HEIGHT  28.0f   /* height of a checkbox row */
#define BUTTON_HEIGHT    34.0f   /* height of a button */
#define SLIDER_HEIGHT    32.0f   /* height of a slider */
#define BUTTON_SPACING   10.0f   /* horizontal gap between buttons */

ForgeUiRect panel = { x, y, w, h };

/* Draw panel background */
forge_ui__emit_rect(ctx, panel, bg_r, bg_g, bg_b, bg_a);

/* Push vertical layout for the panel */
if (!forge_ui_ctx_layout_push(ctx, panel,
                              FORGE_UI_LAYOUT_VERTICAL,
                              PANEL_PADDING, WIDGET_SPACING)) {
    return;
}

/* Title label */
forge_ui_ctx_label_layout(ctx, "Settings", LABEL_HEIGHT,
                          title_r, title_g, title_b, title_a);

/* Checkboxes */
(void)forge_ui_ctx_checkbox_layout(ctx, ID_CB_1, "Option A",
                                   &option_a, CHECKBOX_HEIGHT);
(void)forge_ui_ctx_checkbox_layout(ctx, ID_CB_2, "Option B",
                                   &option_b, CHECKBOX_HEIGHT);

/* Horizontal button row */
ForgeUiRect btn_row = forge_ui_ctx_layout_next(ctx, BUTTON_HEIGHT);

if (!forge_ui_ctx_layout_push(ctx, btn_row,
                              FORGE_UI_LAYOUT_HORIZONTAL,
                              0.0f, BUTTON_SPACING)) {
    forge_ui_ctx_layout_pop(ctx);  /* pop outer before returning */
    return;
}

float btn_w = (btn_row.w - BUTTON_SPACING) * 0.5f;
(void)forge_ui_ctx_button_layout(ctx, ID_BTN_OK, "OK", btn_w);
(void)forge_ui_ctx_button_layout(ctx, ID_BTN_CANCEL, "Cancel", btn_w);

forge_ui_ctx_layout_pop(ctx);  /* end horizontal row */

/* Slider */
(void)forge_ui_ctx_slider_layout(ctx, ID_SLIDER, &value,
                                 0.0f, 100.0f, SLIDER_HEIGHT);

forge_ui_ctx_layout_pop(ctx);  /* end vertical panel */
```

### Key observations

- The `0.5f` in `btn_w` is inherent math (dividing by 2), not a magic number
- `layout_next()` returns a rect from the outer vertical layout, which becomes
  the bounds for the inner horizontal layout
- The inner `layout_push` error path pops the outer layout before returning
- Widget return values can be `(void)` cast when the result is not needed

## Reference

- [UI Lesson 08 — Layout](../../../lessons/ui/08-layout/) — full walkthrough
  with manual vs automatic comparison
- [UI Lesson 05 — Immediate-Mode Basics](../../../lessons/ui/05-immediate-mode-basics/) —
  the `ForgeUiContext` this builds on
- [`common/ui/forge_ui_ctx.h`](../../../common/ui/forge_ui_ctx.h) — layout API
  implementation
