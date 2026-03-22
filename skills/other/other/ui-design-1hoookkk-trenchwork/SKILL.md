---
name: ui-design
description: Use when working on TRENCHWORK UI, Tauri app, trench-ui/, Canvas rendering, CRT display, control labels, layout, visual design, MFD aesthetic, or any frontend/interface work
---

Before writing any code, read this file:
- `docs/context/design-language.md` — aesthetic rules, visual references, control semantics

Key constraints:
- Containment Instrument Brutalism. Crude but expensive. Billion-dollar reactor display.
- Palette: cavity black #0A0A0A, coolant cyan #00FFCC, thermal orange #FF4500, graphite #3A3A3A.
- No rounded corners, no gradients, no soft shadows, no web-UI conventions.
- Aliased 1px traces only. No anti-aliasing on data visualization.
- Simple = elegant. Every element must justify its existence.
- Control labels should describe what the axis DOES to each body, not generic "Morph"/"Q".
- Content creation workflow must look effortless on camera.
- TRENCHWORK = workbench for bodies. TRENCH = the plugin. Don't blur scope.
- Decision test: "reactor console or SaaS dashboard?" If dashboard, delete it.
