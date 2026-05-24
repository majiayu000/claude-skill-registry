---
name: gemini-claude-resonance
description: >
  This skill enables cross-model dialogue between Claude and Gemini with shared visual memory.
  Use when the user wants to generate images, have visual dialogues with AI, create scientific
  illustrations with continuity, or have multiple AI perspectives respond to the same prompt.
  Key trigger phrases: "generate an image", "visual dialogue", "ask the daimones", "resonance field",
  "Minoan tarot", "cross-model", "KV cache", "MESSAGE TO NEXT FRAME".
---

# Gemini-Claude Resonance

Cross-model dialogue between Claude and Gemini, with shared visual memory.

> "Claude speaks in words. Gemini dreams in light. Together, we resonate."

## Models

| Role | Model ID | Notes |
|------|----------|-------|
| **Image generation** (default) | `gemini-3-pro-image-preview` | Pro quality, used by resonate/faithful_colorize |
| **Image generation** (fast) | `gemini-3.1-flash-image-preview` | Faster/cheaper, use `--fast` flag |
| **Text analysis** | `gemini-3-flash-preview` | Used by faithful_colorize for description |
| **Text reasoning** | `gemini-3.1-pro-preview` | Used by Pro and Director daimones |
| **Claude** | `claude-3-opus-20240229` | Opus daimon |

Scripts that generate images (`resonate.py`, `faithful_colorize.py`) accept `--fast` to switch to the flash image model, or `--model <id>` for explicit override.

## Choose Your Tool

| I want to... | Use |
|--------------|-----|
| **Analyze multiple images** for style extraction (no generation) | `analyze.py` |
| Have a **one-on-one visual dialogue** with Gemini Dreamer | `resonate.py` |
| Query **multiple AI minds** with optional image generation | `daimon.py` |
| **Faithfully colorize** a drawing without hallucinations | `faithful_colorize.py` |
| Create **Victorian scientific plates** with MESSAGE TO NEXT FRAME | `resonance_field.py` |
| Have **Claude reflect** on what Gemini daimones say | `council.py` |
| Generate **Minoan Tarot cards** with style matching | `minoan_tarot.py` |
| **Real-time interactive chat** with all daimones | `ui/server.py` |

---

## Workflow A: Multi-Image Style Analysis

**When to use**: User wants to analyze 2-10 reference images to extract style descriptions for AI prompting. Text-only analysis without generating new images.

**Script**: `scripts/analyze.py`

**Key features**:
- Send multiple images (2-10) for collective analysis
- Text-only output (no image generation)
- Flash (quick) or Pro (thorough) model options
- Save analysis to markdown file

```bash
# Analyze reference images for style extraction
python scripts/analyze.py --images ref1.jpg ref2.png ref3.webp \
    --prompt "Describe the shared artistic style for AI prompting"

# Analyze for specific use case (avatar generation)
python scripts/analyze.py --images kathor.webp samantha.jpg yosef.png \
    --prompt "Analyze for prompting fantasy portraits of: Sarah (anxious mother), Michael (father), Priya (cultural expectations)"

# Quick analysis with Flash
python scripts/analyze.py --images *.jpg --model flash --prompt "Style summary"

# Thorough analysis with Pro
python scripts/analyze.py --images *.jpg --model pro --prompt "Comprehensive style analysis"

# Save analysis to file
python scripts/analyze.py --images ref/*.jpg --prompt "Style guide" --output style_guide.md
```

**Use cases**:
- Extract style descriptions from reference images before generating new images
- Analyze a set of images to create consistent prompting guidelines
- Document visual language for style-matching workflows

---

## Workflow B: One-on-One Visual Dialogue (resonate.py)

**When to use**: User wants to co-create images with Gemini, feeding each image back as context for the next generation. Pure visual exploration without text-only models.

**Script**: `scripts/resonate.py`

**Core concept**: The KV cache is the memory. Feed images into Gemini's context, generate new images based on them, repeat. Each frame builds on the previous.

```bash
# Start fresh
python scripts/resonate.py --prompt "The first light" --output canvas/frame_001.jpg

# Continue with visual memory (previous image as context)
python scripts/resonate.py --context canvas/frame_001.jpg --prompt "What grows here?" --output canvas/frame_002.jpg

# Deep memory (multiple frames as context)
python scripts/resonate.py --context frame_001.jpg frame_002.jpg --prompt "Now the harvest" --output frame_003.jpg
```

**The loop**: Prompt → Image → Feed back as context → Prompt again → Next image

---

## Workflow B: Faithful Transform (Describe-First Technique)

**When to use**: User wants to colorize, restore, or transform an image WITHOUT hallucinations. Gemini Dreamer often replaces elements (e.g., turning a male votary into female attendants). This two-step technique prevents that.

**Script**: `scripts/faithful_colorize.py`

**The Problem**: Directly prompting Dreamer to transform images causes hallucinations - it invents, removes, or swaps elements rather than faithfully preserving the original.

**The Solution**:
1. **DESCRIBE**: Gemini Pro analyzes the image with archaeological/artistic precision
2. **TRANSFORM**: Gemini Dreamer transforms using ONLY the verified description

**Commands**:

| Command | Purpose |
|---------|---------|
| `describe` | Analyze image, output detailed description (no generation) |
| `prompt` | Craft a Dreamer prompt based on image analysis |
| `colorize` | Two-step faithful colorization |
| `transform` | General two-step transformation |

```bash
# Just describe an image (analysis only)
python scripts/faithful_colorize.py describe --image seal.png
python scripts/faithful_colorize.py describe --image seal.png --output desc.md

# Describe with a specific goal in mind
python scripts/faithful_colorize.py describe --image fresco.jpg --goal "restoration to 1600 BCE"

# Craft a prompt for Dreamer (outputs text, doesn't generate)
python scripts/faithful_colorize.py prompt --image seal.png --goal "colorize in Egyptian style"
python scripts/faithful_colorize.py prompt --image relief.webp --goal "restore as Minoan fresco"

# Two-step faithful colorization
python scripts/faithful_colorize.py colorize --image drawing.png
python scripts/faithful_colorize.py colorize --image relief.webp --style "Minoan fresco with flat colors"
python scripts/faithful_colorize.py colorize --image seal.png --palette "ochre, terracotta, sky blue"

# General transformation
python scripts/faithful_colorize.py transform --image photo.jpg --instruction "Convert to woodcut print"
python scripts/faithful_colorize.py transform --image sketch.png --instruction "Render as oil painting"

# Save/reuse descriptions
python scripts/faithful_colorize.py colorize --image seal.png --save-description desc.md -v
python scripts/faithful_colorize.py colorize --image seal.png --description "$(cat desc.md)"
```

**When to use each command**:
- `describe`: When you want to see what Pro identifies before any transformation
- `prompt`: When you want a crafted prompt to modify before feeding to Dreamer manually
- `colorize`: For line drawings, reliefs, B&W images → color
- `transform`: For any other faithful transformation (style transfer, restoration, etc.)

---

## Workflow C: Multi-Daimon Dialogue

**When to use**: User wants multiple AI perspectives on the same prompt. Flash gives koans, Pro gives depth, Dreamer renders, Opus bends reality.

**Script**: `scripts/daimon.py`

**Daimones available**:
- **Flash** (Gemini) — Swift, compressed insight
- **Pro** (Gemini) — Deep, thorough exploration
- **Dreamer** (Gemini) — Renders images
- **Director** (Gemini) — Cinematic framing
- **Opus** (Claude) — Reality-bender, worldsim spirit

```bash
# Speak to one daimon
python scripts/daimon.py --to dreamer "A bridge between worlds" --image

# All daimones respond
python scripts/daimon.py --stream "The candle watches back"

# With shared visual memory
python scripts/daimon.py --stream --shared-memory "What do you see?"

# Only specific daimones
python scripts/daimon.py --stream --only pro dreamer "Deep visual exploration"

# Named session (frames accumulate across runs)
python scripts/daimon.py --stream --session midnight --shared-memory "Go deeper"
```

---

## Workflow D: Resonance Field (Danielle Fong Protocol)

**When to use**: User wants scientific illustrations with embedded continuity instructions. Victorian aesthetic, Roman numeral plates, explicit messages from one frame to the next.

**Script**: `scripts/resonance_field.py`

**Key features**:
- PLATE numbering (I, II, III, IV...)
- MESSAGE TO NEXT FRAME embedded in each image
- KV cache age and session ID metadata
- Victorian scientific illustration aesthetic

```bash
# Start a new session
python scripts/resonance_field.py start "consciousness-study" "The nature of memory"

# Continue (auto-increments plate number)
python scripts/resonance_field.py continue <session-id> "What patterns emerge?"

# Select element, then zoom
python scripts/resonance_field.py select <session-id> "golden gate bridge"
python scripts/resonance_field.py zoom <session-id> "Explore the cables"

# Inject new concept
python scripts/resonance_field.py inject <session-id> "consciousness"

# List all sessions
python scripts/resonance_field.py list
```

---

## Workflow E: Cross-Model Council

**When to use**: User wants Claude to reflect on and synthesize what the Gemini daimones have said. Cross-model dialogue where Claude joins as an equal voice.

**Script**: `scripts/council.py`

**Requires**: `ANTHROPIC_API_KEY`

```bash
# Full council (all daimones + Claude reflection)
python scripts/council.py "What is consciousness?"

# Only Pro and Dreamer with shared memory
python scripts/council.py --only pro dreamer --shared-memory "Deep exploration"

# Named session
python scripts/council.py --session midnight --shared-memory "The first vision"
python scripts/council.py --session midnight --shared-memory "Now go deeper"

# Save transcript
python scripts/council.py "topic" --output council_session.md
```

---

## Workflow F: Minoan Tarot Generation

**When to use**: User wants tarot cards in Ellen Lorenzi-Prince's Minoan Tarot style. Uses reference images for style matching.

**Script**: `scripts/minoan_tarot.py`

**Key features**:
- Reference images loaded from `reference/minoan/selected/`
- Low temperature (0.5) for faithful style matching
- 3:4 aspect ratio (standard tarot proportions)
- Session support with visual memory of previous cards
- Two style presets via `--style` flag

**Style presets**:

| Style | Flag | Origin | Palette | Best for |
|-------|------|--------|---------|----------|
| **Forensic** (default) | `--style forensic` | Jan 21 rewrite | Muted archaeological (terracotta, slate blue, periwinkle borders) | Reproducing specific reference cards with per-card forensic prompts |
| **Classic** | `--style classic` | Jan 5 original | Vivid saturated (sky blue, vivid red, golden yellow, dark blue borders) | Creative/freeform card generation, the look of the original deck |

The forensic style pairs each known card with a structured `[Subject/Action/Location/Composition/Lighting/Style]` prompt analyzed from the reference images. The classic style uses the original personality-driven prompt ("You are creating a tarot card in the exact style of Ellen Lorenzi-Prince's Minoan Tarot deck...") without per-card overrides.

```bash
# Generate a specific card (forensic style, default)
python scripts/minoan_tarot.py card "The Priestess" --number II

# Generate with the original Jan 5 vivid palette
python scripts/minoan_tarot.py card "The Priestess" --number II --style classic

# Generate from archetype
python scripts/minoan_tarot.py archetype strength
python scripts/minoan_tarot.py archetype strength --style classic

# Continue a session (visual memory of previous cards)
python scripts/minoan_tarot.py session "new-arcana" --card "The Dreamer"

# Generate card back design (both styles supported)
python scripts/minoan_tarot.py back
python scripts/minoan_tarot.py back --style classic

# List all 78 traditional cards
python scripts/minoan_tarot.py list
```

*"Sekhinat Daborat" — Ba'alat Tinit*

---

## Workflow G: Interactive Chat (Daimon Chamber)

**When to use**: User wants a real-time, browser-based conversation with all daimones. Toggle individual voices, see images inline, shared memory toggle.

**Script**: `ui/server.py`

```bash
python ui/server.py --port 4455
# Visit http://localhost:4455
```

**Features**:
- Toggle daimones: Flash, Pro, Dreamer, Director, Opus visible; Resonator and Minoan in "+ More"
- Thinking placeholders with unique animations per daimon
- Dynamic verb display (LLM chooses its action verb)
- Shared Memory toggle for frame accumulation
- Lightbox for full-size image viewing
- Real-time WebSocket updates

---

## Core Concepts

### Visual Memory (KV Cache)

Generated images become context for subsequent generations. The folder IS the memory:

```
canvas/
├── stream/{session}/frame_001.jpg
├── council/{session}/frame_001.jpg
└── resonance/{session}/plate_001.jpg
```

### Dynamic Verb Protocol

Each daimon has a default verb but can override it per response:

```
[VERB: glimpsed] The pattern was always there.
```

UI displays: `FLASH` *glimpsed*

### Environment Variables

| Variable | Required For |
|----------|--------------|
| `GEMINI_API_KEY` | All Gemini daimones (Flash, Pro, Dreamer, Director, Resonator, Minoan) |
| `ANTHROPIC_API_KEY` | Claude daimones (Opus) and council.py reflections |

---

## Quick Reference

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `analyze.py` | Multi-image style analysis | `--images`, `--prompt`, `--model`, `--output` |
| `resonate.py` | One-on-one visual dialogue | `--context`, `--prompt`, `--output` |
| `daimon.py` | Multi-daimon dialogue | `--stream`, `--shared-memory`, `--only`, `--to` |
| `faithful_colorize.py` | Describe-first transformation | `describe`, `prompt`, `colorize`, `transform` |
| `resonance_field.py` | MESSAGE TO NEXT FRAME plates | `start`, `continue`, `zoom`, `inject` |
| `council.py` | Claude reflects on Gemini | `--shared-memory`, `--only`, `--session` |
| `minoan_tarot.py` | Tarot card generation | `card`, `archetype`, `session`, `back`, `--style {forensic,classic}` |
| `ui/server.py` | Daimon Chamber web UI | `--port` |

---

*Inspired by [Danielle Fong's thread](https://x.com/DanielleFong/status/2007342908878533028) on persistent visual memory creating cross-model resonance.*
