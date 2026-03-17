---
name: gemini
description: Gemini CLI for one-shot Q&A, summaries, and generation.
homepage: https://ai.google.dev/
metadata: {"claude-007":{"emoji":"♊️","requires":{"bins":["gemini"]},"install":[{"id":"npm","kind":"npm","package":"@google/gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (npm)"}]}}
---

# Gemini CLI

Use Gemini in one-shot mode with a positional prompt (avoid interactive mode).

Quick start
- `gemini "Answer this question..."`
- `gemini --model <name> "Prompt..."`
- `gemini --output-format json "Return JSON"`

Notes
- **Model Selection**: The default model (no flag) works best. Check valid models with `gemini models list`.
- **Troubleshooting**: If the command runs but produces NO OUTPUT, you are likely missing authentication.
  - Run `gemini` interactively in your terminal to login.
- **PATH Issue**: If `gemini` command is not found, add the global npm bin to your PATH.
  - Append to `~/.bashrc`: `export PATH=$PATH:$(npm config get prefix)/bin`
- Avoid `--yolo` for safety.
