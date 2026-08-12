---
name: verify
description: Drive an engine app headlessly in a pty, record a video of the whole verification, and open a summary page (video + timeline + checks) with pixel open.
---

Apps here render via the kitty graphics protocol, so they can be verified
without a real terminal. Every verification is **recorded**: the harness in
`tools/verify-recorder/` captures every frame the app emits, overlays your
inputs (click ripples, caption bar), encodes a video, and generates a summary
page. Do not hand-roll one-off pty scripts that only dump PNGs.

## Writing a verification

Write a driver script (in /tmp is fine) using the checked-in package:

```python
import sys
sys.path.insert(0, "<repo>/tools/verify-recorder")
from driver import Driver
from recorder import Recorder

rec = Recorder("wheel-pan", title="Wheel pan keeps cursor anchored")
d = Driver(["<repo>/engine/target/debug/typing"], rec,
           cols=120, rows=32, xpixel=1200, ypixel=800)

d.pump(3.0)                                  # pump between actions so frames arrive
rec.check("app painted", d.frame_size is not None, f"{d.frame_size}")
w, h = d.frame_size                          # REAL framebuffer size — always use this

d.text("hello", "type into editor")          # every input takes a description
d.click(w // 2, h // 3, "select the note")   # mouse coords are pixels (1016 mode)
d.wheel(w // 2, h // 2, down=True, n=3, description="scroll content")
d.pump(1.0)
rec.check("scroll redrew", len(rec.frames) > 40, f"{len(rec.frames)} frames")
rec.still("after-scroll")                    # named snapshot for the summary page

d.stop("ctrl+c")                             # or "ctrl+q" depending on the app
rec.finish()                                 # composites markers, encodes mp4, writes summary
```

- `Driver` spawns the argv in a pty (TERM=xterm-kitty, TIOCSWINSZ with pixel
  dims, answers the `\x1b[?1016$p` mouse probe), decodes kitty `a=T,f=32,o=z`
  frames, and feeds them to the recorder. Node apps: spawn
  `["npx", "tsx", "src/main.tsx", ...]` with `cwd=` the package dir (tsx
  resolves tsconfig from cwd; a wrong cwd silently drops jsx config).
- Input methods: `key("enter"/"esc"/"ctrl+q"/"super+shift+z")`, `text`,
  `click`, `press`/`drag`/`release` (a drag needs all three — `click` sends
  press+release together), `move`, `wheel`. Descriptions become the video
  caption bar and the summary timeline — write what the step is *testing*.
- `rec.check(name, ok, detail)` for every assertion; `rec.still(name)` to pin
  the current frame into the summary.
- Give checks real assertions (frame deltas, decoded pixel colors via
  `recorder.png_read(rec.frames[-1]["path"])`) — the summary shows pass/fail.

## Ending a verification (required)

`rec.finish()` prints the run dir and summary path. **Always end by opening
the summary in a split:**

```
pixel open file:///tmp/verify-runs/<name>-<stamp>/summary.html
```

That page is the deliverable: what was tested (clickable timeline that seeks
the video), the checks table, the stills, and the video of the whole run.
Watch out for FAIL rows before declaring the verification passed.

## Gotchas

- The engine rounds the window down to the cell grid, so the framebuffer can
  be narrower than the requested winsize. Take coordinates from
  `d.frame_size`, never from the requested pixels, or clicks land ~5% off.
- Keep pumping after quit (`d.stop` does) or the exit is never observed.
- Escape must be kitty CSI-u (`d.key("esc")` handles it); a bare `\x1b` makes
  the app swallow the next escape sequence as literal text.
- If a press lands on a node without handlers, the engine dispatches the click
  at the *release* position — a missed drag can silently click something else.
- Hover state only updates on move events; end interactions with a `move` if
  the screenshot should show hover styling.
- Apps taking a file path argv need an ABSOLUTE path (their cwd is the
  package dir).
- Run artifacts live in `/tmp/verify-runs/<name>-<stamp>/`: `frames/`,
  `events.jsonl`, `run.json`, `verification.mp4`, `summary.html`.
