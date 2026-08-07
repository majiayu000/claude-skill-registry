---
name: diagram-contract
description: 'Use when a diagram is going into a document: pick the tool, write the text source, render it, and embed it with an accessible caption. Text DSL plus a committed SVG is the shape — nomnoml for structure and flow, D2 for architecture, the house palette on both.'
argument-hint: "What should the diagram show?"
---

Every diagram that lands in a document follows one shape: a text DSL source beside the document and a committed SVG rendered from it. This skill picks the tool, applies the house palette, and produces both artifacts so the image carries on github.com.

## Pick the tool

Reach up the table only when the default cannot carry the domain. The default is the first row.

| Purpose | Tool |
|---|---|
| Structure, class, relations, small-to-medium flow, state, timeline | **nomnoml** (default) |
| Architecture, system, module dependencies, container maps | **D2** |
| Very large dense DAG, hundreds of nodes | Graphviz DOT |
| Byte, bit, or on-disk layout | bytefield-svg |
| Quantitative chart, only with sourced real figures | Vega-Lite |

## Author it

Five steps, each with a checkable done condition.

1. **Choose the shape.** A comparison, trade-off, or decision matrix is a Markdown table. For a quantitative comparison whose real numbers cannot be sourced, a table is the required form, not a chart. Done when the choice between table and diagram is made and stated.
2. **Write the source** into `assets/<kebab-slug>.<ext>` beside the document that will embed it, opening with the house header below when the tool is nomnoml. Done when the file exists on disk and, for nomnoml, the header is the first block in it.
3. **Render** with the matching command under [Render commands](#render-commands). Done when the command exits zero and the SVG exists beside its source.
4. **Embed** as `![<what it shows>](assets/<slug>.svg)` followed directly by a one-line `>` caption carrying the key message. Done when both lines are present, the alt text is a label rather than the word "diagram", and the caption states what the image means rather than restating its title.
5. **Commit source and SVG together.** Done when both paths are staged. Never commit one without the other; the pair is the contract.

## House header

Open every nomnoml source with this header verbatim. It sets direction, background, spacing, stroke, and the named styles `accent`, `blue`, `green`, `neutral`, and `ghost`.

```text
#direction: right
#background: #fcfcfc
#fill: #ffffff
#stroke: #2b2b2b
#spacing: 36
#padding: 12
#fontSize: 13
#lineWidth: 2
#.accent: fill=#fce9df stroke=#f15d22 title=bold
#.blue: fill=#e6f5f7 stroke=#48b9c7 title=bold
#.green: fill=#e9f5ee stroke=#73c48f title=bold
#.neutral: fill=#f0f0f0 stroke=#808080
#.ghost: fill=#f0f0f0 stroke=#808080 dashed
```

`D2` uses `--theme 0`; its palette is set by the same hex values in the source where the theme allows it.

## Layout

Source and rendered SVG are siblings in `assets/` beside the document that embeds them, both kebab-case, both committed. A document at `docs/x.md` gets `docs/assets/<slug>.noml` and `docs/assets/<slug>.svg`, so the relative embed `assets/<slug>.svg` stays correct. Keep the path relative; an absolute path breaks on github.com.

## Example

```markdown
![Approval path from draft to publish](assets/approval-path.svg)

> A draft needs one reviewer; anything touching billing needs two.
```

The source that produced it lives at `assets/approval-path.noml` and is committed with the SVG. Alt text is a label for what the image shows, never the word "diagram".

## Render commands

- `npx -y nomnoml@latest assets/<slug>.noml assets/<slug>.svg`
- `d2 --theme 0 assets/<slug>.d2 assets/<slug>.svg`
- `dot -Tsvg assets/<slug>.dot -o assets/<slug>.svg`

A non-zero exit means the source is wrong. Fix the source; an unrendered diagram does not ship. When neither binary is present, say so and name the install command rather than emitting source nobody can see.

## Rules

- One focal element per diagram, carrying `accent`. Everything else takes `blue`, `green`, `neutral`, or `ghost`.
- Keep to the palette above and leave red out entirely, red-with-green most of all.
- Encode meaning twice: colour plus shape plus a direct label. Direct labels beat a legend.
- Labels sit inside the nodes, and a diagram that stands alone is left to stand alone rather than paired with prose restating it.
- Ship an explicit light background inside the SVG. A GitHub `<img>` does not propagate `prefers-color-scheme`.
- Meet contrast: non-text at least 3:1, text at least 4.5:1.
- Real figures only. A chart with invented numbers is a table with real ones instead.
- Text DSL and a committed SVG is the shape this contract recognises. Where a surface renders mermaid natively and has no committed asset to link — a GitHub PR body is the one such case — that surface is outside this contract and says so at its own site.
