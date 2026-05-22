---
name: create-design-board
version: 1.0.0
description: >
  Generate and maintain iterative design boards from image directories.
  Composite PNG grids, markdown boards with size previews, round tracking,
  and side-by-side comparison tables.
provides:
  - design-board
  - image-comparison
  - visual-iteration
composes:
  - assess
  - review-persona
  - task-monitor
triggers:
  - create design board
  - design board
  - show design board
  - compare designs
  - update design board
  - append to board
  - assess persona for design
allowed-tools:
  - Bash
  - Read
taxonomy:
  - design
  - visual
  - iteration
  - persona
---

# create-design-board

Point at a directory of images, get a design board. Supports iterative
rounds, composite PNG grids, size previews, and comparison tables.

**Critical lessons** (learned the hard way across 9 rounds of Embry OS icon design):

1. Every design iteration MUST start with persona assessment. Visual direction,
   typography, color palette, and icon metaphors all derive from the persona's
   personality, background, and domain. Without this step, you'll waste rounds
   on directions that don't fit (cursive/serif E killed 2 rounds before we
   assessed Embry Lawson's persona).
2. The board must capture design REASONING, not just images. Round 8→9 of the
   Embry icon went through font weight reduction (500→300), glow shell
   elimination, and font reassessment — none of which was on the board until
   we caught the gap. Image tables without context are useless for future rounds.

## Rules (non-negotiable)

1. **DESIGN_BOARD.md is the single source of truth.** Every round, every
   decision, every eliminated direction MUST be recorded there. If it's not
   on the board, it didn't happen.
2. **Update the board after EVERY round** — not just image tables. Include:
   - What changed and WHY (font weight, color, layout decisions)
   - What was eliminated and WHY (directions that don't fit persona)
   - User feedback quotes that drove the change
   - Cross-round progression (e.g. "Round 8→9: eliminated glow shell")
3. **The `append` command adds image tables.** Design reasoning must be added
   separately — either via `--notes` (brief) or by manually appending a
   "Key Decisions" section after the image table. The tool handles images;
   YOU handle reasoning.
4. **Never skip persona assessment.** Round 1 must start with `assess-persona`.

## Workflow (learned from 9 rounds of Embry OS icon design)

1. **Assess persona** (`assess-persona`) — Read persona YAML, extract traits,
   map to typographic and visual attributes. This eliminates wrong directions
   before any images are generated.
2. **Generate images** — Use `/create-image` or other tools to produce concepts
3. **Build board** (`board` or `append`) — Create/update the design board markdown
4. **Generate composite** (`composite`) — Visual grid for quick comparison
5. **Collect feedback** — User reviews, provides quotes
6. **Update board with reasoning** — ALWAYS update DESIGN_BOARD.md after every
   round. Add BOTH the image table (via `append`) AND a design decisions section
   explaining what changed, what was eliminated, and why. The board must tell
   the story of the design evolution, not just show thumbnails.
7. **Repeat** from step 2 with narrowed direction

## Commands

### `assess-persona` -- Assess persona YAML for design direction (ALWAYS DO THIS FIRST)

Reads a persona YAML file and generates a persona-to-design mapping section
for the design board. Maps personality traits to typography, color, iconography,
and visual style recommendations. Composes `/assess` and `/review-persona`.

```bash
./run.sh assess-persona --persona /path/to/persona.yaml --output ./DESIGN_BOARD.md
./run.sh assess-persona --persona /path/to/persona.yaml  # stdout only
```

### `board` -- Generate design board markdown from image directory

```bash
./run.sh board --images ./icons/v7/ --output ./icons/DESIGN_BOARD.md --title "Embry OS Icon Concepts"
```

### `append` -- Add a new round to an existing board

```bash
./run.sh append --images ./icons/v8/ --board ./icons/DESIGN_BOARD.md --round "Round 6" --notes "Clean sans-serif E with dense starfield"
```

### `composite` -- Generate composite PNG grid

```bash
./run.sh composite --images ./icons/v7/ --output ./icons/v7/board.png --cols 3 --bg "#0e0e1c" --title "Round 5"
```

### `compare` -- Side-by-side comparison of specific images

```bash
./run.sh compare --images img1.png img2.png img3.png --output comparison.png --labels "Option A" "Option B" "Option C"
```

### `sizes` -- Generate size variant previews

```bash
./run.sh sizes --image ./icons/v7/F2_minimal_nebula.png --output ./icons/v7/F2_sizes/
```

### Options

| Flag       | Description                              |
|------------|------------------------------------------|
| `--images` | Directory of PNGs/JPGs or list of files  |
| `--output` | Output file or directory                 |
| `--title`  | Board or section title                   |
| `--cols`   | Grid columns (default: 3)               |
| `--bg`     | Background color (default: `#0e0e1c`)   |
| `--round`  | Round name for append                    |
| `--notes`  | Round notes for append                   |
| `--labels` | Labels for compare mode                  |
| `--board`  | Existing board markdown for append       |
