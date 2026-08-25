---
name: authoring-motion-diagrams
description: Use when adding a plugin to the marketplace, or when authoring, editing, or re-rendering a scene under scripts/animations/scenes/ — including when a scene fails the render contract, the contrast gate, or the grid baseline.
---

# Authoring motion diagrams

Every marketplace entry has one authored scene at `scripts/animations/scenes/<plugin>.svg`,
shown on that plugin's detail page. `docs/plugins/<plugin>/anim.mp4` and `anim-poster.png`
are derived from it. Never patch the video — change the scene and re-render.

A scene must **say what the plugin does**: what moves, in what order, and what is different
at the end. A scene where things merely move is decoration.

## Flow

1. Read the plugin's category from `.claude-plugin/marketplace.json`, then take that
   category's `mark` and `ink` from `scripts/animations/palette.js`. One accent per scene.
2. Copy `references/scene-template.svg` to `scripts/animations/scenes/<plugin>.svg`.
3. Compose the beats. `references/binding.md` has the tokens, the beat pattern, and the
   scene mechanics already in use — reuse one rather than inventing a shape.
4. `node scripts/animations/render.js --check` — validates the contract in about a second,
   no Chrome. Run it constantly, not once at the end.
5. `node scripts/animations/preview.js <plugin>` — one frame, ~1s. `AT=0.3` for another
   moment. This catches what no checker can: a label sitting on a connector, a box crossing
   its frame, a path ending in mid-air.
6. `node scripts/animations/render.js <plugin>` — mp4 + poster, ~75s.
7. `npm run generate && npm test`.
8. Commit the scene, the mp4 and the poster together. They drift the moment they don't.

## What `--check` enforces

| Gate | Rule |
|---|---|
| Cycle | every `dur` is `8s`, `repeatCount="indefinite"`, events placed in `keyTimes` |
| Counts | `keySplines` = n−1, `values` = n, `keyPoints` = n. A mismatch disables the animation *silently* |
| Ground | a `#faf9f6` rect is the first element |
| Type | every text fill is a legal ink token — 4.5:1 on paper, computed not judged |
| Blocks | solid rects use a category `ink`, so white type on them clears 4.5:1 |
| Grid | placement on 20px; existing scenes carry a frozen debt in `grid-baseline.json` and may only improve |

`palette.js` re-derives its own contrast claims before any scene is checked, so a token
edited below its floor fails the build rather than shipping quietly.

## What no gate can check

- **Two beats per change.** Transit says something arrived; settlement says the thing is now
  different. One beat alone reads as decoration.
- **The changed state holds** until 0.95 of the cycle. A transition with no hold shows motion
  and communicates no outcome.
- **Routes avoid what they don't address.** A path to C that crosses B reads as having entered B.
- **Position is pre-allocated.** Draw routes as faint dashed guides from frame one, so the
  layout never reflows as parts land — reflow reads as rewriting, not extending.
- **The poster carries the whole diagram** for a reduced-motion reader. Check it, not just the video.

## Common mistakes

| Mistake | What happens |
|---|---|
| Chaining with `begin="other.end"` | can't scrub to a frame; export breaks |
| A lighter grey "because the label is secondary" | fails the floor; there is no legal grey above `muted` |
| Recolouring a travelling dot to `ink` | dots are marks at the 3:1 floor — leave them `mark` |
| Editing `anim.mp4` or shipping a scene without re-rendering | video and source drift, and nothing reports it |
| Nudging geometry off-grid in an existing scene | ratchet fails the build; the baseline only goes down |

## References

- `references/binding.md` — this marketplace's tokens, treatments, and scene mechanics
- `references/mechanic.md` — the portable declarative-SVG-motion doc
- `references/scene-template.svg` — a conforming skeleton
