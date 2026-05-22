---
name: web-frontend-designer
description: Scaffold frontend architecture, components, routing, and UI dependencies from project config and wireframes.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 3-frontend
  pipeline: web-builder
---

# Web Frontend Designer

## Objective

Scaffold a production-ready frontend foundation from `project-config.json` and
`wireframes.md`, including component structure, dependencies, and route shells.

## Required Workflow

1. Read `project-config.json` and `wireframes.md`.
2. Scaffold the chosen framework (for example `create-next-app` or Vite scaffolding pattern).
3. Configure the chosen CSS/design system (Tailwind, Shadcn/ui, Chakra UI, Material UI, Ant Design, Mantine, DaisyUI, or vanilla CSS).
4. Integrate or plan integration for:
   - Font Awesome: https://fontawesome.com/
   - React Bits (+ MCP if available): https://reactbits.dev/ and https://reactbits.dev/get-started/mcp
   - Spline: https://spline.design/
   - Lucide Icons: https://lucide.dev/
   - Shadcn/ui: https://ui.shadcn.com/
   - Aceternity UI: https://ui.aceternity.com/
   - Magic UI: https://magicui.design/
   - Framer Motion: https://www.framer.com/motion/
   - React Three Fiber: https://docs.pmnd.rs/react-three-fiber
5. Set up font strategy with Google Fonts or Fontsource.
6. Set image/illustration sources with Unsplash API, Pexels, or Lummi.
7. Generate component tree (`components`, `layouts`, `pages` or `app`) and route placeholders for the sitemap.
8. Enforce responsive design, dark mode, and accessibility (including ARIA labels).
9. Output scaffold files and `frontend-report.json`.

## Execution

```bash
python skills/web-frontend-designer/scripts/frontend_designer.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
