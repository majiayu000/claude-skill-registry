---
name: easter-egg-modal
description: This skill should be used when the user asks to "generate an easter egg modal", "create a Gleipnir fragment modal", "build easter egg component", "make an easter egg screen", or provides an egg number (1–6) OR an egg name (e.g. "cat", "mountain", "fish") referring to the six Gleipnir ingredients. Generates a TSX component that wraps the shared EasterEggModal shell and an inline SVG artifact image for the specified Fenrir Ledger easter egg. No external tools required.
---

# Easter Egg Modal Generator — Fenrir Ledger

Generates a Gleipnir fragment discovery component for one of the six impossible ingredients.
Each egg uses the **shared `EasterEggModal` shell** (`@/components/easter-eggs/EasterEggModal`)
so modal structure, audio, and styling are never re-implemented per egg.

---

## Step 1 — Resolve Inputs

### Output Format

SVG is the only image format — no conversion step.

### Egg Identifier — Number OR Name

The user may provide either:
- A **number** `1`–`6`, OR
- An **egg name** — any word or phrase from the ingredient title, case-insensitive

Match the user's input (number or name keyword) to the correct row in this table:

| # | Component Name            | Title                          | Name keywords                          | Storage key      | Rune |
|---|---------------------------|--------------------------------|----------------------------------------|------------------|------|
| 1 | `GleipnirCatFootfall`     | The Sound of a Cat's Footfall  | cat, footfall, sound                   | `egg:gleipnir-1` | ᚲ    |
| 2 | `GleipnirWomansBeard`     | The Beard of a Woman           | beard, woman                           | `egg:gleipnir-2` | ᛒ    |
| 3 | `GleipnirMountainRoots`   | The Roots of a Mountain        | roots, mountain                        | `egg:gleipnir-3` | ᚱ    |
| 4 | `GleipnirBearSinews`      | The Sinews of a Bear           | sinews, sinew, bear                    | `egg:gleipnir-4` | ᚢ    |
| 5 | `GleipnirFishBreath`      | The Breath of a Fish           | breath, fish                           | `egg:gleipnir-5` | ᛚ    |
| 6 | `GleipnirBirdSpittle`     | The Spittle of a Bird          | spittle, bird                          | `egg:gleipnir-6` | ᛊ    |

**Examples:**
- `3` → egg #3 (The Roots of a Mountain)
- `"mountain"` → egg #3
- `"cat's footfall"` → egg #1
- `"fish"` → egg #5
- `"bear sinews"` → egg #4

If the input is ambiguous or matches nothing, ask the user to clarify before proceeding.

Call these resolved values:
- `{{N}}` — the egg number (1–6)
- `{{COMPONENT}}` — component name from the table
- `{{TITLE}}` — ingredient title from the table
- `{{STORAGE_KEY}}` — localStorage key from the table
- `{{RUNE}}` — Elder Futhark rune character from the table

---

## Step 2 — Prepare Directories

```bash
mkdir -p ./development/ledger/public/easter-eggs
mkdir -p ./development/ledger/public/sounds
```

Verify the howl audio file is present:

```bash
ls ./development/ledger/public/sounds/fenrir-howl.mp3
```

If the file is missing, stop and tell the user:
> `public/sounds/fenrir-howl.mp3` is required for the easter egg howl.
> Copy it into the project: `cp /path/to/fenrir-howl.mp3 development/ledger/public/sounds/`

---
## Step 3 — Create the SVG Artifact Image

Write a 1024×1024 SVG file directly to:
`./development/ledger/public/easter-eggs/gleipnir-{{N}}.svg`

### Universal design rules (apply to every egg)

- **Viewbox**: `viewBox="0 0 1024 1024"`
- **Background**: **transparent — do NOT add a background `<rect>`**. The `EasterEggModal` image column provides a `#13151f` (chain) dark backdrop. Adding a background rect creates a visible colour mismatch.
- **Primary shapes**: gold `#c9920a`; highlights and glow: `#f0b429`
- **Structural lines**: dim iron `#1e2235`
- **Outer ring**: `<circle cx="512" cy="512" r="440"/>` stroke `#c9920a` opacity `0.18` strokeWidth `1` no fill
- **Rune watermark**: place `{{RUNE}}` as a `<text>` in the **bottom-left corner** —
  `x="32" y="988"`, `font-size="80"`, `fill="#c9920a"`, `opacity="0.22"`, `font-family="serif"`.
  This is a persistent signature across all six eggs. Do not centre it; do not make it large.
- **`<title>`**: first child of `<svg>` — set to `{{TITLE}}`
- **`<desc>`**: second child — the wolf's voice narration for this egg (see per-egg copy below)
- No external references — all paths must be inline SVG elements

### Per-egg motif: art direction + wolf's voice copy

Each egg's `<desc>` should hold the wolf's internal monologue about that ingredient.
Use this voice: ancient, unhurried, neither angry nor defeated — the wolf simply *knows*.

---

**Egg 1 — The Sound of a Cat's Footfall (ᚲ)**

*What the wolf says (use as `<desc>`)* —
"I have hunted every creature that breathes. I know the sound of hooves on frost, of ravens
lifting from the dead. But the cat — the cat makes no sound at all. They took that silence
and wove it into the chain. I did not hear it coming. I still do not."

*Motif* — A single stylised cat paw print centred at (512, 480): four small toe-bean ellipses
above a larger heel pad, all gold `#c9920a`. Radiating outward from the print: 5 concentric
arcs (`<path>`) of decreasing opacity (0.18 → 0.04), representing silence spreading outward
like ripples that make no sound. A faint dashed horizontal line at y=512 — the ground
that was not disturbed. The visual read should be: *something landed here, and you did not hear it*.

---

**Egg 2 — The Beard of a Woman (ᛒ)**

*What the wolf says (use as `<desc>`)* —
"They told me: this does not exist. I laughed. A wolf does not fear what does not exist.
Then I felt it — impossibly fine, impossibly strong. Woven from absence. The beard of a woman.
The most impossible thing is the thing that is there when it should not be."

*Motif* — Three long sinuous braid strands (`<path>` cubic beziers) flowing from top to bottom,
interweaving centre-to-edge across the full 1024px height. Gold gradient from `#c9920a` at top
to `#f0b429` mid-braid, fading to `#c9920a` at base. Where strands cross: small Norse knotwork
diamond lozenges (`<polygon>` 4-point stars, 8px, fill `#f0b429`). The braid should feel
both impossibly delicate and impossibly unbreakable.

---

**Egg 3 — The Roots of a Mountain (ᚱ)**

*What the wolf says (use as `<desc>`)* —
"Mountains do not have roots. Every child of Yggdrasil knows this. Rock simply is —
it does not grip, it does not reach. And yet the dwarves found them: deep below Niðavellir,
older than the stone itself. They are still down there. So am I."

*Motif* — A mountain silhouette (`<polygon>`) drawn upside-down, apex pointing downward at
(512, 820), base edge running across the top quarter of the image at y≈200.
From the inverted apex and each inverted foothill, branching root tendrils spread as `<line>`
elements: 3 levels deep, each branch 0.6× the length of its parent, angle ±28°.
Root lines: stroke `#c9920a` opacity fading from 0.7 (trunk) to 0.15 (finest tips).
A single dim iron horizontal line at y=190 — the surface of the earth, above.
The visual read: *what holds the mountain up is deeper than the mountain*.

---

**Egg 4 — The Sinews of a Bear (ᚢ)**

*What the wolf says (use as `<desc>`)* —
"I have torn bears apart. I know what sinew looks like — thick ropes of it, bloody and strong.
What they wove into Gleipnir was not that. It was the invisible sinew — the force that makes
a bear *a bear*, that binds muscle to will. I felt it tighten and I knew I could not match it."

*Motif* — A tight diagonal crosshatch of curved `<path>` sinew strands across the full canvas,
alternating gold `#c9920a` and iron `#1e2235`, stroke-width 1.5. All strands curve slightly
(not straight lines — biological, not geometric). At the exact centre (512, 512): a convergence
knot — a dense `<circle r="18">` in bright gold `#f0b429` where all strands visually meet.
From the knot, four thicker anchor strands (`stroke-width 2.5`) radiate to each corner.
The visual read: *everything binds to one point; that point holds everything else*.

---

**Egg 5 — The Breath of a Fish (ᛚ)**

*What the wolf says (use as `<desc>`)* —
"The fish does not breathe. I have drowned prey in rivers. I have watched them — they take
in water, not air. There is no breath there. And yet the dwarves gathered it. They said:
we found it between the gills, in the current's memory. I believe them now."

*Motif* — 11 circles rising from bottom to top: radii ranging from 32px (bottom) to 6px (top),
centres forming a gentle S-curve drift. Each circle: stroke `#c9920a`, no fill, opacity scaling
linearly from 0.85 (bottom) to 0.12 (topmost). The largest bubble (bottom, r=32): add a
`<filter>` glow — `<feGaussianBlur stdDeviation="6"/>` in a `<defs>` blur, applied as a
faint gold `#c9920a` ghost behind it. At y=940: a wide flat ellipse (`rx=160 ry=14`)
in dim iron `#1e2235` opacity 0.4 — the water surface.
The visual read: *breath from something that does not breathe, rising out of dark water*.

---

**Egg 6 — The Spittle of a Bird (ᛊ)**

*What the wolf says (use as `<desc>`)* —
"I have eaten birds. Whole. Feathers, hollow bones, the lot. Birds do not spit — they are
too small, too clean, too fast. They told me the dwarves collected it over a thousand years
from the corners of beaks. A thousand years of nothing, gathered into a strand that holds
a god's wolf still. I respect it."

*Motif* — A bird beak silhouette (`<path>`) pointing right, upper mandible tip at (560, 512),
drawn as a gold `#c9920a` outline only (stroke-width 2, no fill), roughly 80px long.
From the beak tip: a spray of 13 droplets (`<circle>`) at varied angles (−30° to +30°),
radii 2–7px, gold fill `#c9920a`, opacity 0.85 near the beak fading to 0.2 at outer edge,
distance from tip ranging 30–160px. Thin radial guide lines from tip to each droplet:
stroke `#c9920a` opacity 0.07, stroke-width 0.5.
The visual read: *something impossibly small, impossibly precise, impossibly powerful*.

---

## Step 4 — Generate the TSX Component

Write the component to:
`development/ledger/src/components/cards/{{COMPONENT}}.tsx`

**Do not re-implement the modal structure.** Use `EasterEggModal` from
`@/components/easter-eggs/EasterEggModal` — it owns the dialog shell, audio playback,
accessibility, and all design tokens. This component's only jobs are:
1. Render the SVG artifact as the `image` prop.
2. Supply the discovery copy as `children`.
3. Track and display the Gleipnir fragment count.
4. Expose a `useGleipnirFragment{{N}}` hook for trigger-site wiring.

Use this template exactly, substituting all `{{...}}` placeholders:

```tsx
"use client";

/**
 * {{COMPONENT}} — Gleipnir Fragment {{N}} of 6
 *
 * Shown when the user discovers: "{{TITLE}}"
 * One of the six impossible things woven into Gleipnir — the ribbon that bound Fenrir.
 *
 * Trigger:  See ux/easter-eggs.md #1 — The Gleipnir Hunt
 * Storage:  localStorage key "{{STORAGE_KEY}}"
 * Image:    /easter-eggs/gleipnir-{{N}}.svg
 */

import { useEffect, useState } from "react";
import { EasterEggModal } from "@/components/easter-eggs/EasterEggModal";

const STORAGE_KEY = "{{STORAGE_KEY}}";
const TOTAL_FRAGMENTS = 6;

interface {{COMPONENT}}Props {
  /** Control open state externally (e.g. from the trigger site). */
  open: boolean;
  onClose: () => void;
}

export function {{COMPONENT}}({ open, onClose }: {{COMPONENT}}Props) {
  const [found, setFound] = useState(0);

  useEffect(() => {
    if (open) {
      // Count total found (this fragment was already written by the hook's trigger()).
      const count = Array.from({ length: TOTAL_FRAGMENTS }, (_, i) =>
        localStorage.getItem(`egg:gleipnir-${i + 1}`)
      ).filter(Boolean).length;
      setFound(count);
    }
  }, [open]);

  return (
    <EasterEggModal
      open={open}
      onClose={onClose}
      title="{{TITLE}}"
      description={`You have found Gleipnir fragment {{N}} of 6: {{TITLE}}. One of the six impossible things woven into the ribbon that bound the great wolf.`}
      image={
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src="/easter-eggs/gleipnir-{{N}}.svg"
          alt="{{TITLE}} — Gleipnir artifact"
          className="w-full max-w-[200px] md:max-w-[240px] aspect-square object-contain"
        />
      }
      audioSrc="/sounds/fenrir-howl.mp3"
    >
      <p className="font-body text-sm text-[#e8e4d4] leading-relaxed">
        One of the six impossible things woven into{" "}
        <span className="text-[#f0b429] italic">Gleipnir</span> — the only
        chain strong enough to bind the great wolf. Though it looks like silk
        ribbon, no chain is stronger.
      </p>

      <p className="font-body text-xs italic text-[#8a8578] leading-relaxed">
        &ldquo;The dwarves of Svartálfaheimr gathered six things that do not
        exist. From these they wove Gleipnir. When Fenrir felt its touch, he
        knew at last what true binding was.&rdquo;
      </p>

      <div className="border-t border-[#1e2235] pt-3 mt-1">
        <p className="font-mono text-[0.7rem] text-[#c9920a]">
          Fragment {found} of {TOTAL_FRAGMENTS} found
        </p>
        {found === TOTAL_FRAGMENTS && (
          <p className="font-mono text-[0.65rem] text-[#f0b429] mt-1 animate-pulse">
            ✦ Gleipnir is complete. The wolf stirs.
          </p>
        )}
      </div>
    </EasterEggModal>
  );
}

/**
 * Hook — wire this at the trigger site.
 *
 * Usage:
 *   const { open, trigger, dismiss } = useGleipnirFragment{{N}}();
 *   // Call trigger() when the hidden ingredient text is discovered.
 *   // Render: <{{COMPONENT}} open={open} onClose={dismiss} />
 *
 * Audio and modal structure are handled by EasterEggModal — do not add them here.
 * The trigger() call is the user-gesture entry point; browsers allow audio from there.
 */
export function useGleipnirFragment{{N}}() {
  const [open, setOpen] = useState(false);

  function trigger() {
    if (!localStorage.getItem(STORAGE_KEY)) {
      localStorage.setItem(STORAGE_KEY, "1");
      setOpen(true);
    }
  }

  function dismiss() {
    setOpen(false);
  }

  return { open, trigger, dismiss };
}
```

---

## Step 5 — Verify

Confirm the following files now exist:

| File | Expected |
|------|----------|
| `development/ledger/public/easter-eggs/gleipnir-{{N}}.svg` | SVG artifact, non-zero |
| `development/ledger/src/components/cards/{{COMPONENT}}.tsx` | TSX component |

Report the created files and their sizes. If any file is missing, diagnose and fix before finishing.

---

## Step 6 — Usage Summary

Output a concise summary for the engineer showing:

1. **Image path** (as referenced in the component): `/easter-eggs/gleipnir-{{N}}.svg`
2. **Component import**: `import { {{COMPONENT}}, useGleipnirFragment{{N}} } from "@/components/cards/{{COMPONENT}}"`
3. **Trigger site hook usage** (copy-paste example)
4. **Which placement location** to trigger this from (see `ux/easter-eggs.md` placement table)

---

## Reference Data

### Gleipnir Placement Map (from `ux/easter-eggs.md`)

| # | Ingredient | Where to wire the trigger |
|---|-----------|--------------------------|
| 1 | Sound of a cat's footfall | Tooltip on the silent background sync indicator (bottom-right corner) |
| 2 | Beard of a woman | About modal — listed under "Built from…" |
| 3 | Roots of a mountain | First time collapse of the Sidebar Menu |
| 4 | Sinews of a bear | TBD — more UI elements need to be finished |
| 5 | Breath of a fish | Footer — hover on the `©` symbol |
| 6 | Spittle of a bird | TBD — more UI elements need to be finished |

### EasterEggModal Props (from `src/components/easter-eggs/EasterEggModal.tsx`)

| Prop | Type | Purpose |
|------|------|---------|
| `open` | `boolean` | Dialog open state |
| `onClose` | `() => void` | Called on dismiss |
| `title` | `string` | Cinzel Decorative headline |
| `description?` | `string` | sr-only text for screen readers |
| `image?` | `ReactNode` | Artifact image — left column |
| `audioSrc?` | `string` | Audio URL played on open (e.g. `/sounds/fenrir-howl.mp3`) |
| `children` | `ReactNode` | Discovery copy — right column |

### Design Tokens (from `ux/theme-system.md`)

| Token | Value | Role |
|-------|-------|------|
| `void` | `#07070d` | SVG / modal background |
| `forge` | `#0f1018` | Modal surface |
| `chain` | `#13151f` | Column fill |
| `iron-border` | `#2a2d45` | Borders |
| `rune-border` | `#1e2235` | Hairline dividers |
| `gold` | `#c9920a` | Primary accent |
| `gold-bright` | `#f0b429` | Highlights, hover |
| `text-saga` | `#e8e4d4` | Primary text |
| `text-rune` | `#8a8578` | Captions, secondary |

### z-index: 9653

The easter egg modal uses z-index 9653 — W-O-L-F on a phone keypad.
This is a magic number documented in `product/copywriting.md`.
