---
name: mermaid
description: Generate Mermaid diagrams for chatbot flows that render in Markdown, including choosing diagram types, producing valid Mermaid code blocks, and validating or rendering diagrams locally via the bundled scripts. Use when a user asks for chatbot flowcharts/sequence/state diagrams, wants Mermaid syntax, or needs to verify/render Mermaid without a web service.
---

# Mermaid Diagrams for Chatbots

Use this skill to create Mermaid diagrams that render well in Markdown chat interfaces, validate their syntax locally, and render images without calling a web service.

## Workflow

1. Identify the diagram type (flowchart, sequenceDiagram, stateDiagram-v2) based on the request.
2. Draft Mermaid code in a fenced Markdown block using `mermaid`.
3. Follow formatting conventions in `references/chatbot-mermaid-guidelines.md`.
4. Validate the diagram using `scripts/validate_mermaid.py`.
5. If the user wants an image file, render with `scripts/render_mermaid.py`.

## Scripts

- `scripts/validate_mermaid.py`
  - Validate Mermaid code by invoking the local Mermaid CLI (`mmdc`).
  - Use when you need to check whether Mermaid parses without errors.
- `scripts/render_mermaid.py`
  - Render Mermaid to SVG/PNG/PDF using the local Mermaid CLI (`mmdc`).
  - Prefer SVG for Markdown renderers when image embedding is required.

## Notes

- These scripts expect `mmdc` to be available on PATH (Mermaid CLI).
  If missing, instruct the user to install it locally; do not use the Mermaid web service.
- Dependencies are managed via inline `uv` script metadata in each Python script.
  Use `--install-chromium` to bootstrap the Chromium binary via pyppeteer when needed.
- Keep diagrams compact and readable in chat: avoid overly wide graphs, use short labels, and group related states.
- If the user asks for raw Markdown, return only the fenced `mermaid` block unless they ask for extra explanation.
