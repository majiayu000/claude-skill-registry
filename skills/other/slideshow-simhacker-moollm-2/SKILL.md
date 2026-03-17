---
name: slideshow
description: "Present images in linear narrative form"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [visualizer, image-mining, storytelling-tools, yaml-jazz, room, character]
tags: [moollm, images, presentation, narrative, gallery]
---

# Slideshow

> *"The camera is the pickaxe. The slideshow is the museum."*
>
> *"Every image tells a story. The slideshow tells THE story."*

The **Slideshow** skill presents generated images as linear visual narratives. While the [Visualizer](../visualizer/) creates images, the Slideshow **presents** them — synthesizing metadata from prompts and mining sidecars into scrollable stories.

---

## Philosophy

Images live in directories. Directories accumulate chaos.

A SLIDESHOW.md transforms that chaos into narrative:
- **Time-ordered** entries create journeys
- **Metadata synthesis** extracts meaning
- **Death-scrollable** layout works everywhere
- **Encapsulation** keeps related files together

Think of it as the **museum** for your visual **mining operation**.

---

## Stereo Slideshows: YML + MD

> *"The left eye sees truth. The right eye sees story. Together: depth perception."*

A **stereo slideshow** maintains two complementary files:

| File | Role | Purpose |
|------|------|---------|
| `SLIDESHOW.yml` | **Left Eye** | Machine-readable source of truth |
| `SLIDESHOW.md` | **Right Eye** | Human-readable narrative for GitHub |

### Why Two Files?

**SLIDESHOW.yml** (Source of Truth):
- Structured data the compiler can read
- Photo metadata, locations, room references
- No prose, just semantic facts
- Stable structure for tooling

**SLIDESHOW.md** (Narrative View):
- Rich markdown for GitHub display
- Images inline, captions, stories
- Death-scrollable presentation
- Generated FROM the YML

### The SYNC Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEREO SLIDESHOW SYNC                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SLIDESHOW.yml (left eye)        SLIDESHOW.md (right eye)       │
│  ┌─────────────────────┐         ┌─────────────────────────┐    │
│  │ id: slideshow/pub   │         │ # 📸 Pub Photo Gallery  │    │
│  │ name: Pub Gallery   │  ───▶   │ > *"Opening quote..."*  │    │
│  │ location: room/pub  │  SYNC   │                         │    │
│  │ contents:           │         │ ## Shot 1: The Bar      │    │
│  │   - dir: bar-shot   │         │ ![Alt](bar-shot.png)    │    │
│  │     subject: ...    │         │ **Location:** The Bar   │    │
│  └─────────────────────┘         └─────────────────────────┘    │
│                                                                 │
│  EDIT the YML → SYNC generates MD                               │
│  The YML is the single source of truth                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### SLIDESHOW.yml Format

```yaml
# SLIDESHOW.yml — Machine-readable slideshow definition
id: slideshow/pub/photos
name: "Pub Photo Gallery"
type: slideshow
location: room/pub              # Links to compiled room
tagline: "Memories from the Gezelligheid Grotto"

# Photo metadata
contents:
  - dir: bar-shot-2026-01-19
    subject: "Marieke at the bar"
    mood: warm
    role: ESTABLISHING
    image: bar-marieke.png
    
  - dir: palm-cats-2026-01-19
    subject: "Palm with the cats"
    mood: cozy
    role: DETAIL
    image: palm-cats.png

# Optional: narrative hints for MD generation
narrative:
  opening_quote: "The best nights are the ones you almost remember..."
  style_notes: "First-person phone camera, golden hour lighting"
  
# Compiler uses this to link slideshow to room
compiled:
  room_ref: room/pub
  photo_count: 2
```

### Photo Directory Structure (Stereo)

Each photo can also be stereo:

```
photo-directory/
  PHOTO.yml          # Left eye: metadata, generation settings
  PHOTO.md           # Right eye: narrative description
  main-image.png     # The actual image
  MINING-*.yml       # Mining layer files
```

**PHOTO.yml** (metadata):
```yaml
subject:
  primary: "Marieke serving drinks"
  secondary: ["Palm", "cats"]
mood: warm
camera:
  type: "iPhone 15 Pro"
  settings: { aperture: 1.8, iso: 800 }
generation:
  provider: dalle3
  prompt: "..."
```

**PHOTO.md** (narrative):
```markdown
# Marieke at the Bar

The warm glow of Edison bulbs catches the brass 
fixtures as Marieke pours a perfect pint...
```

### Commands

```
SYNC SLIDESHOW [directory]
```
Regenerates `SLIDESHOW.md` from `SLIDESHOW.yml`.

```
CREATE STEREO SLIDESHOW FOR [directory]
```
Creates both YML (from scanning directory) and MD (from YML).

```
UPDATE SLIDESHOW YML [directory]
```
Scans for new photos and updates the YML source of truth.

---

## The CREATE Method

Generate a SLIDESHOW.md for a directory of images:

```
CREATE SLIDESHOW for pub/dons-photos-2026-01-19/
```

**What happens:**

1. **Discover** images in directory (`.png`, `.jpg`, `.webp`)
2. **Find sidecars** for each image (`.yml` prompt, `-mined.yml` resources)
3. **Order** by timestamp in filename or file creation time
4. **Synthesize** narrative descriptions from metadata
5. **Write** SLIDESHOW.md with gallery structure

---

## The LANDING Method

Create a README.md landing page for GitHub display:

```
LANDING for pub/dons-pub-photos-2026-01-19/
```

**Why README.md?**

GitHub renders `README.md` automatically when you browse a directory, but not `SLIDESHOW.md`. The landing page is the **front door** — motivating visitors to read the story.

```
┌─────────────────────────────────────────────────────────────────┐
│  README.md (Landing Page)          SLIDESHOW.md (Story)        │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Shown on GitHub automatically   ✗ Must click to view        │
│  ✓ Metadata table                  Pure narrative flow          │
│  ✓ Character links                 No links — just story        │
│  ✓ Location links                  No context jumps             │
│  ✓ Story summary (fresh!)          Full detailed story          │
│  → "View the slideshow"            The actual experience        │
└─────────────────────────────────────────────────────────────────┘
```

**What goes in README.md:**

| Section | Content |
|---------|---------|
| Title + Tagline | Hook the reader |
| Gallery Info | Slide count, date, style, location |
| Featuring | Characters with links to their directories |
| Locations | Rooms with links to their directories |
| Story Summary | Fresh synthesis — "why should I look at these?" |
| Preview | Optional image grid |
| Technical | Mining layers, generator |

**Key insight:** The story summary is **freshly synthesized**, not copy-pasted from SLIDESHOW.md. It answers: *"What will I experience if I click through?"*

**Workflow:**

```
1. CREATE SLIDESHOW       # Generate the story
2. ORGANIZE INTO dirname  # Encapsulate files
3. LANDING                # Create GitHub front door
```

---

## The ORGANIZE Method

Encapsulate a SLIDESHOW.md and its images into a named subdirectory:

```
ORGANIZE pub/SLIDESHOW.md INTO dons-pub-photos-2026-01-19
```

**Before:**
```
pub/
  SLIDESHOW.md
  dons-photos-2026-01-19-16-30-00-bar-marieke-palm-cats.png
  dons-photos-2026-01-19-16-30-00-bar-marieke-palm-cats.yml
  dons-photos-2026-01-19-16-30-00-bar-marieke-palm-cats-mined.yml
  ...20 more files...
```

**After:**
```
pub/
  dons-pub-photos-2026-01-19/
    SLIDESHOW.md          # Inherits from slideshow skill
    bar-marieke-palm-cats.png
    bar-marieke-palm-cats.yml
    bar-marieke-palm-cats-mined.yml
    ...all files moved and renamed...
```

**Naming convention:** `lowercase-dashes`, descriptive, date-suffixed if temporal.

---

## SLIDESHOW.md Format

Every SLIDESHOW.md should declare inheritance:

```yaml
---
inherits: slideshow
title: "Don's Pub Photos — January 19, 2026"
created: 2026-01-19
images: 8
style: first-person-phone-camera
---
```

### Structure

```markdown
# 📸 Title

> *"Opening quote capturing the vibe"*

Brief description of what this gallery contains.

---

## 📍 Shot 1: Location (Time)

### *"Caption quote"*

![Alt text](image-file.png)

**Location:** Where this was taken

**Who's Here:**
- 👩🌷 Character 1 doing something
- 🐒🌴 Character 2 doing something else

📎 **Files:** [Prompt](image-file.yml) | [Resources](image-file-mined.yml)

---

## 📍 Shot 2: Next Location (Time)

...

---

## 📊 Stats Table

| Time | Location | Highlights |
|------|----------|------------|
| 4:30 PM | Bar | Marieke, Palm, cats |
| ... | ... | ... |

---

## 🎨 Style Notes

Notes on artistic direction, visual consistency, mood.

---

*"Closing quote"*
```

---

## Metadata Synthesis

The SUMMARIZE method transforms raw sidecar data into narrative:

**From prompt.yml:**
- Scene description → Location
- Characters present → Who's Here
- Time of day → Shot timing
- Artistic style → Style notes

**From prompt-mined.yml:**
- Dominant colors → Visual palette
- Mood/atmosphere → Emotional tone
- Implied sounds/smells → Sensory details
- Symbolism → Deeper meaning

**Output:** Human-readable narrative that tells the story.

---

## Integration with Visualizer

The Visualizer creates. The Slideshow presents.

```
┌─────────────────────────────────────────────────────────────────┐
│                      VISUAL PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Context YAML     →    Visualizer    →    Image + Sidecars     │
│  (rooms, chars)        (generate)         (.png, .yml)          │
│                                                                 │
│  Image + Sidecars →    Image Miner   →    Resources             │
│                        (extract)          (-mined.yml)          │
│                                                                 │
│  All Files        →    Slideshow     →    SLIDESHOW.md          │
│                        (present)          (narrative)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Visualizer advertises to Slideshow:**
```yaml
# In visualizer/CARD.yml
advertisements:
  SLIDESHOW:
    delegates_to: slideshow
    score: 85
    condition: "After generating images, create/update gallery"
```

---

## Gallery Discovery

Slideshows can be discovered and linked:

```bash
# Find all slideshows in adventure-4
find examples/adventure-4 -name "SLIDESHOW.md"
```

Cross-slideshow navigation:
```markdown
**Related Galleries:**
- [Palm's Study](../stage/palm-nook/study/palm-study-images/SLIDESHOW.md)
- [Attic Adventures](../attic/dusty-attic-images/SLIDESHOW.md)
```

---

## Why Encapsulate?

**Without encapsulation:**
```
pub/
  ROOM.yml
  SLIDESHOW.md
  guestbook.yml
  fireplace.yml
  20 image files...
  20 prompt files...
  20 mining files...
  # Chaos. What belongs together?
```

**With encapsulation:**
```
pub/
  ROOM.yml
  guestbook.yml
  fireplace.yml
  dons-pub-photos-2026-01-19/
    SLIDESHOW.md
    all-related-files...
  rooftop-telescope-images/
    SLIDESHOW.md
    all-related-files...
```

**Benefits:**
- Files that belong together STAY together
- Directory name is descriptive
- Easy to move, share, archive
- No pollution of parent directory
- SLIDESHOW.md becomes the index

---

## Example Workflow

```
# 1. Generate images with visualizer
visualize.py character.yml room.yml -p openai

# 2. Mine resources from images
mine.py *.png --depth full

# 3. Create slideshow gallery
CREATE SLIDESHOW for current directory

# 4. Organize into encapsulated directory
ORGANIZE SLIDESHOW.md INTO palm-portrait-session-2026-01-19

# 5. Result: clean, self-contained gallery
```

---

## Death-Scrollable Design

SLIDESHOW.md targets GitHub rendering:

- **Mobile-first:** Images scale, text wraps
- **Death-scrollable:** Just keep scrolling
- **Inline images:** No external links needed
- **Collapsible sections:** For detailed metadata
- **Emoji headers:** Visual navigation
- **Tables:** Stats and comparisons

---

## James Burke Connections

Every good slideshow tells a story through connections:

> **How do these images connect?**
> - Shot 1 introduces the setting
> - Shot 3 shows the characters in that setting
> - Shot 5 captures the climax
> - Shot 8 is the aftermath, full circle

The metadata enables this synthesis — prompts describe intent, mining reveals what emerged.

---

## Commands Reference

| Method | Purpose |
|--------|---------|
| CREATE | Generate SLIDESHOW.md for directory |
| UPDATE | Add new images to existing gallery |
| SUMMARIZE | Synthesize metadata into narrative |
| ORGANIZE | Encapsulate into subdirectory |
| COMPARE | Cross-image comparison section |

---

## 🔧 UPGRADE: Legacy Slideshow Migration

> *Future feature — not yet implemented*

UPGRADE is super flexible. Start with ANYTHING:
- Single file with list of prompts (YML or MD)
- Dir full of loose images (reverse-engineer prompts via mining)
- Just prompts (generate images later!)
- Mixed chaos
- Even empty dirs with just ideas

**Input option A — Single prompt list file:**
```
my-ideas.yml (or my-ideas.md)
```
→ Breaks into individual prompts, removes original, creates full structure

**Input option B — Dir of images:**
```
messy-folder/
├── 2026-01-19-dusk-scene-v3.png
├── morning-light-final.png
└── random-sketch.jpg
```
→ Mines images for prompts (mine prompt mode), structures everything

**Input option C — Mixed chaos (images + prompts + whatever):**
```
messy-folder/
├── 2026-01-19-dusk-scene-v3.png    # Image → mine for prompt
├── morning-light-final.png          # Image → mine for prompt
├── cool-idea.txt                    # Prompt → generate image later
├── more-prompts.yml                 # Prompt list → break apart
├── frame-03-arrival.png             # Image
├── random-sketch.jpg                # Image
└── notes.md                         # Prompts inline → extract
```
→ UPGRADE figures it out: images get mined, prompts get structured, everything organized

**Output (full structure from any input):**
```
slideshow/
├── README.md              # Front cover / title page
├── SLIDESHOW.yml          # Machine-readable skeleton
├── SLIDESHOW.md           # Formatted narrative view
├── 001-dusk-scene/
│   ├── PHOTO.yml
│   ├── PHOTO.md
│   ├── image.png          # Main — NO timestamp, NO index
│   ├── original.png       # Secondary (preserved original name)
│   └── PROMPT.yml         # Generation prompt (or mined from image)
├── 002-morning-light/
│   ├── image.png          # Main
│   ├── PROMPT.yml         # Mined via image mining if no prompt existed
│   └── ...
├── 003-future-idea/
│   ├── PHOTO.yml          # Metadata ready
│   ├── PROMPT.yml         # Prompt waiting
│   └── (no image.png yet) # Generate later!
```

**Naming rules:**
- **Main image**: `image.png` — clean, no timestamp, no index prefix
- **Secondary images**: anything NOT matching `image.png` pattern
  - Brought along, not shown by default
  - Original filenames preserved as secondary
- **All paths**: repo-root relative in compiled output

**What UPGRADE does:**

*Handles any mix — figures out what each file is:*
- `.png/.jpg` → image → mine for prompt
- `.txt/.md` with prose → prompt → generate image later  
- `.yml` with list → prompt list → break apart
- Unknown → bring along as secondary

*Then structures everything:*
1. Cluster related files by name similarity
2. Create `001-descriptive-name/` directories
3. Images → `image.png` (main), originals as secondary
4. Mine images for prompts OR use existing prompts
5. Generate `PHOTO.yml`, `PHOTO.md` skeletons
6. Remove consumed prompt list files
7. Generate `README.md`, `SLIDESHOW.yml`, `SLIDESHOW.md`

**Invoke:** `UPGRADE path/to/anything` (when implemented)

---

## Dovetails With

- [Visualizer](../visualizer/) — Creates the images
- [Image Mining](../image-mining/) — Extracts resources
- [Storytelling Tools](../storytelling-tools/) — Narrative structure
- [YAML Jazz](../yaml-jazz/) — Metadata as fuel
- [Room](../room/) — Spatial context
- [Character](../character/) — Who appears

---

*See CARD.yml for full specification.*
