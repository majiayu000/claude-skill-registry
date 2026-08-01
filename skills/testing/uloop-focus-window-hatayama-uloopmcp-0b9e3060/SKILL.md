---
name: uloop-focus-window
description: 'Bring Unity Editor window to front via uloop CLI. Use when you need
  to: (1) Focus Unity Editor before capturing screenshots, (2) Ensure Unity window
  is visible for visual checks, (3) Bring Unity to fo'
---

---
name: uloop-focus-window
description: Bring Unity Editor window to front via uloop CLI. Use when you need to: (1) Focus Unity Editor before capturing screenshots, (2) Ensure Unity window is visible for visual checks, (3) Bring Unity to foreground for user interaction.
---

# uloop focus-window

Bring Unity Editor window to front.

## Usage

```bash
uloop focus-window
```

## Parameters

None.

## Examples

```bash
# Focus Unity Editor
uloop focus-window
```

## Output

Returns JSON confirming the window was focused.

## Notes

- Useful before `uloop capture-unity-window` to ensure the target window is visible
- Brings the main Unity Editor window to the foreground
