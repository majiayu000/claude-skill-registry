---
name: latex-conventions
description: Work on the LaTeX thesis or LaTeXML HTML output. Use for build/lint/serve commands, LaTeX style rules, HTML pipeline notes, or assets conventions.
---

# LaTeX Conventions (thesis + HTML)

## Build and serve (packages/latex_viterbo)

**Note:** LaTeX builds require TexLive, which is only available in the local devcontainer (not in web environment).

- Lint: `scripts/lint.sh` (chktex + draft compile + latexml sanity)
- Build: `scripts/build.sh [--production] [--pdf-only] [--html-only]`
- Serve: `scripts/serve.sh [--production] [--watch] [--pdf-only] [--html-only]`
- Draft speedup: use `includeonly.tex` (copy from `includeonly.tex.example`).

## LaTeX style

- Use `\(...\)` inline, `\[...\]` display (avoid `$`).
- Proofs in `proof` environment; label theorems/lemmas consistently.
- arXiv-friendly packages only.

## Thesis writing style

- Audience: symplectic geometers; self-contained exposition.
- Separate mainline text from asides.
- Introduce notation once; note deviations from literature.
- Be explicit but skimmable; spoilers up front; headings guide the reader.
- Mark WIP text clearly (e.g., `\edit{}` or `%`).

## Assets

- LaTeX includes assets; Python generates them.
- Store under `packages/latex_viterbo/assets/<experiment>/...`.
- LaTeXML extras under `packages/latex_viterbo/assets/{html/,latexml/}`.
- Hand-crafted assets under `packages/latex_viterbo/assets/manual/`.

## References

- LaTeXML HTML pipeline notes: `references/ar5iv-pipeline-notes.md`
- LaTeXML troubleshooting: `references/latexml-troubleshooting.md`
- Clarke talk teardown checklist: `packages/latex_talk_clarke_duality/docs/teardown.md`
