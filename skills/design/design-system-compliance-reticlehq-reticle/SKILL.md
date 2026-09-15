---
name: design-system-compliance
description: Check that the UI you actually rendered uses the design system, by reading computed styles in the running app against the project's design tokens. Catches hardcoded hex colors, off-palette backgrounds, invisible or unusable controls, and animations that never ran. Use after building or restyling a component, when a design review is wanted, when a UI looks slightly off but nobody can say why, or when a design system exists and nothing checks whether the code follows it.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Does the rendered UI actually use the design system?

Reading the source tells you what the component _asks_ for. It cannot tell you what the browser resolved: a token overridden three layers up, a hardcoded `#3b82f6` that happens to look close, a dark-theme scope that never applied. That answer only exists in the running page.

**Reticle** reads computed styles in the live app and compares them against the project's tokens. Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## The check

```
reticle_snapshot({ sessionId, mode: "interactive" })
reticle_inspect({ sessionId, ref })
```

`inspect` returns a `theme` report per element:

| Field | What it tells you |
| --- | --- |
| `offTheme` | **the headline.** True when a set, opaque color matches no token in the palette: a violation worth fixing |
| `colorTokens` / `backgroundTokens` | every token whose resolved value is this color. Empty means off-palette |
| `colorToken` / `backgroundToken` | the _unambiguous_ match, or `null` when several tokens share the color. `null` here is an abstention, not a violation: read the plural field |
| `tokenCount` | how many tokens resolved under the active theme. **`0` means the app declares no palette**, and `offTheme` is never asserted: report that rather than a clean bill of health |
| `themeScope` | the theme active at capture (e.g. `.dark`), so two inspects taken minutes apart are comparable at all |

Read `tokenCount` first. Zero tokens means there is nothing to comply with, and every "pass" below it is vacuous.

## Beyond color: is the control actually usable?

The same call answers the questions a screenshot cannot:

- `occluded`: covered by an overlay. It renders, and no user can click it.
- `box`: `0×0` is present-but-invisible, the most common "it's there, I can see it in the DOM" bug.
- `styles.opacity` / `styles.cursor`: the difference between disabled-looking and disabled.
- `source: { file, line }`: where to go and fix it.

A design review that only compares colors passes a button nobody can press.

## Animations

```
reticle_animations({ sessionId })
```

Returns running and recently completed animations with their targets and timing. Two things worth checking after any motion work: an animation you added that **never appears here** did not run, and one whose duration does not match the token is off-spec. Both look identical in a screenshot.

## Report violations as locations, not opinions

For each element that failed, give the `file:line` from `inspect` and the specific fact: "background `#3b82f6` matches no token; the palette has `--color-primary` at `#2563eb`". A design-review comment without a location is a task someone else has to redo.

## What this is not

This checks **compliance with the tokens the project declares**. It is not an opinion about whether the design is good, and it is not an accessibility audit. Contrast ratios, focus order and screen-reader semantics are a different job, and claiming them here would be a false green of exactly the kind this repo exists to prevent.

---

Everything else, one page at a time: `curl https://docs.reticle.sh/llms.txt`. Design token check missing something you needed? `reticle_feedback` with `kind: "gap"`.
