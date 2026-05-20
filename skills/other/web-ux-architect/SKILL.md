---
name: web-ux-architect
description: Generate sitemap and wireframe specifications from project-config.json and produce UX planning artifacts.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 2-ux
  pipeline: web-builder
---

# Web UX Architect

## Objective

Read `project-config.json` and generate information architecture artifacts for
page routes and wireframe structure.

## Required Workflow

1. Read `project-config.json` from prior `web-stack-planner` output.
2. Generate a full sitemap with top-level and nested routes.
3. For each page, create a wireframe spec table with layout zones:
   - header
   - hero
   - content
   - sidebar
   - footer
4. Reference these design tools for visual generation:
   - Google Stitch: https://stitch.withgoogle.com/
   - Relume: https://relume.io/
   - v0 by Vercel: https://v0.dev/
   - Framer AI: https://framer.com/
   - Uizard: https://uizard.io/
5. Produce:
   - `sitemap.md`
   - `wireframes.md`
   - `ux-report.json`

## Execution

```bash
python skills/web-ux-architect/scripts/ux_architect.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
