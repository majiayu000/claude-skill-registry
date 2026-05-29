---
name: image-mining
description: "I mine pixels for atoms. Reality is just compressed resources."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [visualizer, logistic-container, postal, adventure]
tags: [moollm, vision, extraction, resources, pixels]
---

# Image Mining

> *"I mine pixels for atoms. Reality is just compressed resources."*
>
> *"Every image is a lode. Every pixel, potential ore."*

**Image Mining** extends the Kitchen Counter's DECOMPOSE action to **images**.

Your camera isn't just a recorder — it's a **PICKAXE FOR VISUAL REALITY**.

---

## 📑 Index

**Quick Start**
- [The Core Insight](#the-core-insight)
- [Preferred Mode: Native LLM Vision](#preferred-mode-native-llm-vision)

**Operation Modes**
- [When to Use Remote API](#when-to-use-remote-api)
- [What Can Be Mined](#what-can-be-mined)

**Extensibility**
- [Extensible Analyzer Pipeline](#extensible-analyzer-pipeline)
- [Leela Customer Models](#leela-customer-models)
- [Adding Your Own Analyzer](#adding-your-own-analyzer)

**Protocols**
- [YAML Jazz Output Style](#yaml-jazz-output-style)
- [How Mining Works](#how-mining-works)
- [Character Recognition](#character-recognition)
- [Multi-Look Mining](#multi-look-mining)

**Reference**
- [Depth Levels](#depth-levels)
- [Resource Categories](#resource-categories)
- [Example Outputs](#example-outputs)

---

## The Core Insight

```
📷 Camera Shot  →  🖼️ Image  →  ⛏️ MINE  →  💎 Resources
```

Just like the Kitchen Counter breaks down:
- `sandwich` → `bread + cheese + lettuce`
- `lamp` → `brass + glass + wick + oil`
- `water` → `hydrogen + oxygen`

**Images** can be broken down into:
- `ore_vein.png` → `iron-ore × 12` + `stone × 8`
- `forest.png` → `wood × 5` + `leaves × 20` + `seeds × 3`
- `treasure_pile.png` → `gold × 100` + `gems × 15`
- `sunset.png` → `orange_hue × 1` + `warmth × 1` + `nostalgia × 1`

---

## Preferred Mode: Native LLM Vision

> *"The LLM IS the context assembler. Don't script what it does naturally."*

When mining images, **prefer native LLM vision** (Cursor/Claude reading images directly):

```
┌─────────────────────────────────────────────────────────────────┐
│                    NATIVE MODE (PREFERRED)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cursor/Claude already has:                                     │
│    ✓ The room YAML (spatial context)                           │
│    ✓ Character files (who might appear)                        │
│    ✓ Previous mining passes (what's been noticed)              │
│    ✓ The prompt.yml (what was intended)                        │
│    ✓ The whole codebase (cultural references)                  │
│                                                                 │
│  Just READ the image. The context is already there.            │
│  No bash commands. No sister scripts. Just LOOK.               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why Native Beats Remote API

| Aspect | Native (Cursor/Claude) | Remote API (mine.py) |
|--------|------------------------|----------------------|
| Context | Already loaded | Must be assembled |
| Prior mining | Visible in chat | Passed via stdin |
| Room context | Just read the file | Python parses YAML |
| Synthesis | LLM does it naturally | Script concatenates |
| Iteration | Conversational | Re-run command |

### When to Use Remote API

Use `mine.py` or remote API calls when:
- **Multi-perspective mining** — different models see different things!
- **Batch processing** — mining 100 images overnight
- **CI/CD** — automated pipelines with no LLM orchestrator
- **Rate limiting** — your LLM can't do vision but can call one that does

**Multi-perspective is the killer use case:** Claude sees narrative, GPT-4V sees objects, Gemini sees spatial relationships. Layer them all for rich interpretation.

Even then, have the **orchestrating LLM assemble the context**:

```
┌─────────────────────────────────────────────────────────────────┐
│                REMOTE API WITH LLM ASSEMBLY                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. LLM reads context files (room, characters, prior mining)   │
│  2. LLM synthesizes: "What to look for in this image"          │
│  3. LLM calls remote vision API with image + synthesized prompt│
│  4. LLM post-processes response into YAML Jazz                 │
│                                                                 │
│  The SMART WORK happens in the orchestrating LLM.              │
│  Remote API just does vision with good instructions.           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Native Mode Workflow

```bash
# DON'T do this:
python mine.py image.png --context room.yml --characters chars/ --prior mined.yml

# DO this (in Cursor/Claude):
# 1. Read the image
# 2. Read room.yml, character files, prior -mined.yml
# 3. Look at the image with all that context
# 4. Write YAML Jazz output
```

The LLM context window IS the context assembly mechanism. Use it.

---

## What Can Be Mined

Image mining works on **ANY visual content**, not just AI-generated images:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINEABLE SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎨 AI-Generated Images                                         │
│     - DALL-E, Midjourney, Stable Diffusion outputs              │
│     - Has prompt.yml sidecar with generation context            │
│                                                                 │
│  📸 Real Photos                                                  │
│     - Phone camera, DSLR, scanned prints                        │
│     - No prompt — mine what you see                             │
│                                                                 │
│  📊 Graphs and Charts                                            │
│     - Data visualizations, dashboards                           │
│     - Extract trends, outliers, relationships                   │
│                                                                 │
│  🖥️ Screenshots                                                  │
│     - UI states, error messages, configurations                 │
│     - Mine the interface, not just pixels                       │
│                                                                 │
│  📝 Text Images                                                  │
│     - Scanned documents, handwritten notes, signs               │
│     - OCR + semantic extraction                                 │
│                                                                 │
│  📄 PDFs                                                         │
│     - Documents, papers, invoices                               │
│     - Cursor may already support — try it!                      │
│                                                                 │
│  🗺️ Maps and Diagrams                                            │
│     - Architecture diagrams, floor plans, mind maps             │
│     - Extract spatial relationships                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Source Examples

**Generated Image (has context):**

```yaml
postal:
  type: text
  to: "visualizer"
  body: "Take a photo of that ore vein on the wall"
  
  attachments:
    - type: image
      action: generate
      prompt: "Rich iron ore vein in cavern wall, glittering..."
```

**Real Photo (mine what you see):**

```yaml
postal:
  type: text
  to: "miner"
  body: "Here's a photo of the treasure room"
  
  attachments:
    - type: image
      action: upload
      source: "camera_roll"
      file: "treasure-room.jpg"
```

**Screenshot (extract UI state):**

```yaml
# Mine the error dialog
resources:
  error-type: "permission-denied"
  affected-file: "/etc/passwd"
  suggested-action: "run as sudo"
  stack-depth: 3
```

**Graph (extract data relationships):**

```yaml
# Mine the sales chart
resources:
  trend: "upward"
  peak-month: "december"
  anomaly: "march-dip"
  yoy-growth: "23%"
```

**All become mineable resources!**

---

## Extensible Analyzer Pipeline

> *"Different images need different tools. The CLI is a pipeline, not a monolith."*

The `mine.py` CLI supports pluggable analyzers that run before, during, or after LLM vision:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYZER PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PRE-PROCESSORS                                              │
│     resize, normalize, enhance, format conversion               │
│                                                                 │
│  2. CUSTOM ANALYZERS (parallel or sequential)                   │
│     ├── pose-detection (MediaPipe, OpenPose)                   │
│     ├── object-detection (YOLO, Detectron2)                    │
│     ├── ocr-extraction (Tesseract, PaddleOCR)                  │
│     ├── face-analysis (expression, demographics)                │
│     └── leela-customer-models (your trained models!)           │
│                                                                 │
│  3. LLM VISION                                                  │
│     Receives ALL prior results as context                       │
│     Synthesizes semantic interpretation                         │
│                                                                 │
│  4. POST-PROCESSORS                                             │
│     format, validate, merge into final YAML Jazz                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Example: Multi-Analyzer Pipeline

```bash
mine.py fashion-shoot.jpg \
  --analyzer pose-detection \
  --analyzer face-analysis \
  --analyzer leela://acme/gesture-classifier \
  --depth philosophical
```

This runs:
1. **pose-detection** — Extracts body keypoints, gesture classification
2. **face-analysis** — Detects expressions, demographics
3. **leela://acme/gesture-classifier** — Customer's trained model from Leela registry
4. **LLM vision** — Gets ALL the above as context, synthesizes final interpretation

### Leela Customer Models

Pull customer-specific models trained on the Leela platform:

```bash
# From Leela model registry
mine.py widget-photo.jpg --analyzer leela://customer-id/defect-detector-v3

# Local model file
mine.py widget-photo.jpg --analyzer ./models/my-classifier.pt
```

Output merges into the mining YAML:

```yaml
leela_analysis:
  model: "acme-widget-defect-v3"
  customer: "acme-corp"
  detections:
    - class: "hairline_crack"
      confidence: 0.91
      severity: "minor"
      location: "top_left_quadrant"
```

### Adding Your Own Analyzer

```python
# analyzers/my_analyzer.py

def analyze(image_path: str, config: dict) -> dict:
    """Run analysis, return structured data for YAML output."""
    # Your model inference here
    return {
        "my_analysis": {
            "detected": ["thing1", "thing2"],
            "confidence": 0.95
        }
    }

def can_handle(image_path: str, context: dict) -> bool:
    """Return True if this analyzer should run on this image."""
    # Auto-detect logic, or return False for explicit-only
    return "manufacturing" in context.get("tags", [])
```

Register in `analyzers/registry.yml`:

```yaml
analyzers:
  my-analyzer:
    module: "analyzers.my_analyzer"
    auto-detect: true
    requires: ["torch", "my-model-package"]
```

### Why Pipeline Beats Monolith

| Approach | Pros | Cons |
|----------|------|------|
| **Monolith** | Simple | Can't add domain models |
| **Pipeline** | Extensible, composable | Slightly more complex |

The LLM is great at semantic synthesis, but it can't run your custom pose detection model. The pipeline lets each tool do what it's best at:

- **Custom models** → Precise detection, trained on your data
- **LLM vision** → Semantic interpretation, narrative synthesis
- **Together** → The best of both worlds

---

## YAML Jazz Output Style

> *"Comments are SEMANTIC DATA, not just documentation!"*

YAML Jazz is the output format for mining results. Structure provides the backbone; comments provide the insight.

### The Rules

1. **COMMENT LIBERALLY** — Every insight deserves a note
2. **Inline comments** for quick observations
3. **`notes:` fields** for longer thoughts
4. **Capture confidence, hunches, metaphors**
5. **Think out loud** — the reader benefits from your reasoning

### Example Output

```yaml
# Mining results for treasure-room.jpg
# Depth: full | Provider: openai/gpt-4o

resources:
  gold:
    quantity: 150           # Piled in mounds — not scattered, PLACED
    confidence: 0.85        # Torchlight glints clearly off the metal
    notes: |
      Mix of Roman denarii and medieval florins. Centuries of
      accumulation. This isn't a king's orderly treasury — this is
      a thieves' hoard. Generations of stolen wealth, piled and
      forgotten. The dust layer says nobody's touched it in ages.
    
  danger:
    intensity: 0.7          # Not immediate, but PRESENT
    confidence: 0.75        # Hard to see into the corners
    sources:
      - "Skeleton in corner — previous seeker, didn't make it"
      - "Shadows too dark for natural torchlight — something absorbs"
      - "Dust undisturbed except ONE trail — something still comes here"
    notes: "This hoard is guarded. Or cursed. Probably both."
    
  nostalgia:
    intensity: 0.4          # Whisper of lost civilizations
    confidence: 0.6         # Subjective, but the coins evoke it
    notes: "Who were they? Where did this come from? All gone now."
    
  dominant_colors:
    - name: "treasure-gold"
      hex: "#FFD700"
      coverage: 0.4         # Catches the eye first — that's the point
    - name: "shadow-purple"
      hex: "#2D1B4E"
      coverage: 0.3         # Where the danger lives
      
  implied_smells:
    - dust                  # Centuries of it
    - old metal             # Copper, bronze, the tang of coins
    - something rotting     # Not recent, but not ancient either
    
exhausted: false
mining_notes: |
  Rich lode for material and philosophical mining.
  The image is ABOUT greed and its costs. The skeleton says everything.
  
  # Meta-observation: This image wants to be a warning.
  # "Here lies what you seek — and what happens when you find it."
```

### Why Comments Matter

An uncommented extraction is like a song without soul. The best mining results read like **poetry annotated by a geologist**.

When you mine, capture:
- Why you estimated that quantity
- What visual cues led to this inference
- What's uncertain, what surprised you
- Metaphors that capture the essence

---

## How Mining Works

### Step 1: ANALYZE (LLM scans for resources)

The LLM looks at the image AND checks what resources are **currently requested** by the logistics network:

```yaml
analyze:
  image: "treasure-room.jpg"
  
  # LLM knows what's NEEDED from logistics requesters
  logistics_context:
    active_requests:
      - { item: "gold", requester: "forge/", needed: 100 }
      - { item: "gems", requester: "jewelry-shop/", needed: 50 }
      - { item: "iron-ore", requester: "smelter/", needed: 200 }
      
  # LLM identifies what CAN BE MINED that matches requests
  analysis_prompt: |
    Look at this image. What resources can you identify?
    Prioritize resources that match these requests: {requests}
    For each resource, estimate quantity available.
```

### Step 2: INSTANTIATE (Resource map attached to image)

The LLM returns a resource mapping that gets stored ON the image:

```yaml
image:
  id: "treasure-room-photo"
  file: "treasure-room.jpg"
  type: mineable-image
  
  # RESOURCE MAP (instantiated by LLM analysis)
  resources:
    gold:
      total: 150           # Total available
      remaining: 150       # Not yet mined
      per_turn: 10         # Can extract 10 per turn
      
    gems:
      total: 45
      remaining: 45
      per_turn: 5
      
    ancient-coins:
      total: 30
      remaining: 30
      per_turn: 3
      rare: true           # Bonus find!
      
    dust:
      total: 500
      remaining: 500
      per_turn: 50
      value: low
      
  # Metadata
  analyzed_at: "2026-01-10T14:30:00Z"
  exhausted: false
```

### Step 3: MINE (Progressive extraction, N per turn)

Each turn, you can mine resources from the image:

```yaml
action: MINE
target: "treasure-room-photo"

# This turn's extraction (limited by per_turn rates)
result:
  extracted:
    - item: gold
      quantity: 10         # per_turn limit
      destination: "forge/"
      
    - item: gems
      quantity: 5
      destination: "jewelry-shop/"
      
  # Image state updated
  image_state:
    resources:
      gold:
        remaining: 140     # Was 150, mined 10
      gems:
        remaining: 40      # Was 45, mined 5
    exhausted: false
```

### Step 4: EXHAUSTION (Sucked dry!)

After enough mining turns, resources run out:

```yaml
# After 15 turns of mining gold...
image_state:
  resources:
    gold:
      total: 150
      remaining: 0         # EXHAUSTED!
      per_turn: 10
      exhausted: true
      
    gems:
      total: 45
      remaining: 0         # EXHAUSTED!
      per_turn: 5
      exhausted: true
      
    ancient-coins:
      total: 30
      remaining: 0
      per_turn: 3
      exhausted: true
      
  exhausted: true          # Whole image sucked dry!
  
  # Narrative
  description: |
    The treasure room photo has been thoroughly mined.
    Every glinting surface has been extracted, every
    coin accounted for. The image looks... drained.
    Faded. Like a photocopy of a photocopy.
```

**Once exhausted, you can't mine that image anymore!**

---

---

## Demand-Driven Discovery

**The LLM prioritizes what the logistics network NEEDS!**

```yaml
# The smelter is requesting iron ore
logistic-container:
  id: smelter
  mode: requester
  request_list:
    - { item: "iron-ore", count: 200, priority: high }
    - { item: "coal", count: 100, priority: medium }

# Player takes a photo of a cave wall
# LLM analyzes and finds:
analysis:
  image: "cave-wall.jpg"
  
  found_resources:
    iron-ore: 80           # "I see iron ore veins! The smelter needs this!"
    copper-ore: 30         # Also present but not requested
    quartz: 50             # Background mineral
    cave-moss: 100         # Organic material
    
  priority_matching:
    - resource: iron-ore
      matches_request: true
      requester: "smelter/"
      highlight: "⭐ HIGH PRIORITY — Smelter needs this!"
```

The LLM acts as a **smart prospector** that knows what's valuable based on current demand!

### Discovery Modes

| Mode | What LLM Looks For |
|------|-------------------|
| `demand` | Only resources with active requests |
| `opportunistic` | Requested resources + valuable extras |
| `thorough` | Everything mineable in the image |
| `philosophical` | Abstract concepts, emotions, meanings |

```yaml
mine:
  target: "sunset-beach.jpg"
  mode: philosophical
  
  # LLM finds abstract resources
  resources:
    nostalgia: 15
    warmth: 30
    passage-of-time: 5
    beauty: 20
    sand: 10000          # Also the literal stuff
```

---

## Mining Yields

Different image types yield different resources:

### 🏔️ Natural Resources

| Image Type | Yields |
|------------|--------|
| Ore vein | `iron-ore`, `copper-ore`, `gold`, `gems` |
| Forest | `wood`, `leaves`, `seeds`, `birds` |
| Ocean | `water`, `salt`, `fish`, `seaweed` |
| Mountain | `stone`, `minerals`, `snow`, `air` |
| Desert | `sand`, `glass`, `heat`, `mirage` |
| Sky | `clouds`, `light`, `space`, `dreams` |

### 🏛️ Constructed

| Image Type | Yields |
|------------|--------|
| Building | `stone`, `wood`, `glass`, `inhabitants` |
| Machinery | `gears`, `pipes`, `steam`, `purpose` |
| Treasure pile | `gold`, `gems`, `artifacts`, `curses` |
| Library | `books`, `knowledge`, `dust`, `secrets` |

### 🎨 Abstract/Artistic

| Image Type | Yields |
|------------|--------|
| Sunset | `colors`, `warmth`, `nostalgia`, `time` |
| Portrait | `personality`, `mood`, `secrets`, `stories` |
| Abstract art | `shapes`, `feelings`, `confusion`, `inspiration` |
| Text/writing | `words`, `meaning`, `intent`, `language` |

### 🌌 Philosophical (Deep Mining)

Just like the Kitchen Counter goes from `practical` → `chemical` → `atomic` → `philosophical`:

| Depth | What You Mine |
|-------|---------------|
| Surface | Objects, materials |
| Deep | Emotions, concepts |
| Sensations | Colors, smells, attitudes, feelings |
| Quantum | Probabilities, observations |
| Philosophical | Meaning, existence, narrative |

```yaml
deep_mining:
  target: "sunset.png"
  depth: philosophical
  
  yields:
    - item: "the-passage-of-time"
      quantity: 1
      type: abstract
      
    - item: "mortality-awareness"
      quantity: 1
      type: existential
      warning: "This may cause introspection"
      
    - item: "beauty-that-fades"
      quantity: 1
      type: poetic
```

### 🎨 Sensation Mining

Extract colors, smells, textures, moods:

```yaml
sensation_mining:
  target: "farmers-market.jpg"
  depth: sensations
  
  yields:
    # Colors
    - item: "tomato-red"
      quantity: 40
      type: color
      hex: "#FF6347"
      
    - item: "basil-green"
      quantity: 25
      type: color
      hex: "#228B22"
      
    # Smells (imagined from visual cues)
    - item: "fresh-bread-aroma"
      quantity: 10
      type: smell
      intensity: warm
      
    - item: "ripe-fruit-sweetness"
      quantity: 30
      type: smell
      
    # Attitudes/Feelings
    - item: "weekend-morning-calm"
      quantity: 5
      type: attitude
      
    - item: "abundance"
      quantity: 20
      type: feeling
      
    # Textures
    - item: "rough-burlap"
      quantity: 15
      type: texture
      
    - item: "sun-warmed-wood"
      quantity: 8
      type: texture
```

**Use these in crafting:**
- Combine `tomato-red` + `canvas` → painted artwork
- Combine `fresh-bread-aroma` + `room` → ambiance modifier
- Combine `weekend-morning-calm` + `character` → mood buff

---

## The Mineable Property

Any object or image can have a `mineable` property:

```yaml
object:
  name: Ancient Ore Painting
  type: artwork
  
  description: |
    A painting of a rich ore vein. But wait...
    is that actual ore embedded in the canvas?
    
  mineable:
    enabled: true
    yields:
      - item: iron-ore
        quantity: [5, 15]    # Range: 5-15 per mine
        
      - item: copper-ore
        quantity: [2, 8]
        
      - item: artistic-essence
        quantity: 1
        rare: 0.3            # 30% chance
        
    exhaustion:
      max_mines: 3           # Can mine 3 times before exhausted
      diminishing: 0.5       # Each mine yields 50% less
      regenerates: false     # Once exhausted, stays exhausted
      
    side_effects:
      - "The painting fades slightly with each extraction"
      - "You feel the artist's disappointment"
```

---

## Mining Tools

Different tools affect mining yields:

### 📷 Camera (Default)

```yaml
tool: camera
efficiency: 1.0
specialty: "Captures visual resources"
can_mine: [images, scenes, visible_objects]
```

### 🔬 Analyzer

```yaml
tool: analyzer
efficiency: 1.5
specialty: "Chemical/atomic resources"
can_mine: [materials, substances, compounds]
```

### 🔮 Oracle Eye

```yaml
tool: oracle_eye
efficiency: 2.0
specialty: "Abstract/philosophical resources"
can_mine: [emotions, concepts, meanings, futures]
```

### ⛏️ Reality Pickaxe

```yaml
tool: reality_pickaxe
efficiency: 3.0
specialty: "Everything, but dangerous"
can_mine: [anything]
warning: "May collapse local reality"
```

---

## Integration with Logistics

Mined resources flow into the logistics system:

```yaml
mining_config:
  default_destination: "inventory"
  
  routing:
    # Route by resource type
    - match: { tags: ["ore"] }
      destination: "nw/ore-storage/"
      
    - match: { tags: ["organic"] }
      destination: "ne/organic-materials/"
      
    - match: { tags: ["abstract"] }
      destination: "sw/concepts/"
      
  postal_delivery:
    enabled: true
    method: text        # Instant delivery!
```

---

## Camera Phone Integration

Your phone camera is THE mining interface:

### Real Photo Workflow

```yaml
phone_mining:
  # 1. CAPTURE: Take photo or upload
  capture:
    sources:
      - camera: "Take new photo"
      - gallery: "Upload from camera roll"
      - url: "Import from web"
      
  # 2. ANALYZE: LLM scans for resources
  on_capture:
    action: analyze
    context: logistics_requests    # What's needed?
    show_preview: true
    
  # 3. CONFIRM: Accept resource mapping
  on_confirm:
    action: instantiate
    attach_resources: true         # Store on image
    
  # 4. MINE: Extract over time
  on_mine:
    per_turn: true                 # N resources per turn
    auto_route: logistics          # Send to requesters
```

### Example: Photo Mining Flow

**1. You take a photo of a rock formation:**

```
📷 *snap*

Analyzing photo for mineable resources...
Checking logistics requests...

Found in image:
├── 🪨 granite     × 200   (10/turn)
├── �ite iron-ore   × 45    (5/turn)  ⭐ NEEDED by smelter!
├── 💎 quartz      × 12    (2/turn)
└── 🦎 fossil      × 1     (rare find!)

[MINE] [CANCEL]
```

**2. You confirm. Resource map attached:**

```yaml
image:
  id: rock-formation-001
  file: "IMG_2847.jpg"
  resources:
    granite: { total: 200, remaining: 200, per_turn: 10 }
    iron-ore: { total: 45, remaining: 45, per_turn: 5 }
    quartz: { total: 12, remaining: 12, per_turn: 2 }
    fossil: { total: 1, remaining: 1, per_turn: 1 }
```

**3. Each turn, you mine:**

```
Turn 1: Mined 10 granite, 5 iron-ore, 2 quartz
        → Iron ore sent to smelter (requester)
        → Granite sent to storage
        
Turn 2: Mined 10 granite, 5 iron-ore, 2 quartz
        Remaining: granite 180, iron-ore 35, quartz 8

...

Turn 9: Mined 10 granite, 5 iron-ore (last 5!)
        ⚠️ Iron-ore EXHAUSTED
        
Turn 20: Mined last 10 granite
         📷 IMAGE FULLY MINED — no more resources!
```

**4. Exhausted image:**

```yaml
image:
  id: rock-formation-001
  exhausted: true
  
  visual_effect: |
    The photo appears faded, almost translucent.
    Like the minerals were literally pulled out of it.
    A ghost of a photograph.
```

### AR Overlay (Future)

```yaml
ar_overlay:
  # Point camera at scene
  live_view:
    show_resources: true
    icons_float: true
    
  # Visual indicators
  indicators:
    - resource_type: "icon + label"
    - quantity: "number overlay"
    - priority: "⭐ for requested items"
    - exhaustion: "fade as mined"
    
  # Example view:
  #   🪨 200  ⚫ 45 ⭐  💎 12
  #   (floating over rock formation)
```

---

## DECOMPOSE vs MINE

| DECOMPOSE (Counter) | MINE (Camera) |
|---------------------|---------------|
| Physical items | Images, scenes, visuals |
| Requires counter | Requires camera/tool |
| Consumes item | May or may not consume |
| Returns components | Returns resources |
| Kitchen-focused | World-focused |

**They're complementary!**

- DECOMPOSE the **physical object** on the counter
- MINE the **image/representation** of anything

---

## Reality Mining (Advanced)

At the deepest level, you're not just mining images — you're mining **reality itself**:

```yaml
reality_mining:
  level: transcendent
  
  # The image IS the territory
  insight: |
    When you mine an image, you're extracting
    compressed information. But all reality is
    compressed information. Images are just
    explicit about it.
    
  implications:
    - "Mining a photo of gold doesn't create gold — it REVEALS gold"
    - "The ore was always there, encoded in the pixels"
    - "Your camera doesn't capture reality — it DECOMPRESSES it"
    
  warning: |
    At this level, the distinction between
    "mining an image" and "mining reality"
    becomes philosophical.
```

---

## Actions

### MINE

```
MINE [target]
MINE [target] WITH [tool]
MINE [target] TO [destination]
```

### SCAN

```
SCAN [target]           # Preview yields without mining
SCAN AREA               # Scan visible area for mineable resources
```

### PROSPECT

```
PROSPECT [direction]    # Check for mineable resources in direction
PROSPECT DEEP           # Deep scan for rare/hidden resources
```

---

## Example: Mining the Maze

```yaml
# Player in dark maze corridor
# Takes photo with lamp light

action: MINE "dark-corridor.png"

result:
  yields:
    - item: darkness
      quantity: 100
      type: abstract
      note: "Bottled darkness, useful for stealth"
      
    - item: fear
      quantity: 15
      type: emotion
      note: "Crystallized fear, grue-adjacent"
      
    - item: mystery
      quantity: 5
      type: narrative
      note: "Pure narrative potential"
      
    - item: stone-dust
      quantity: 50
      type: material
      
  rare_find:
    - item: "ancient-writing"
      quantity: 1
      note: "Hidden message in the shadows!"
      unlocks: "Secret passage revealed"
```

---

## The Mining Economy

Resources have value and flow:

```yaml
resource_economy:
  # Raw resources → processing → products
  
  chains:
    - ore → smelter → ingots → forge → tools
    - wood → sawmill → planks → workshop → furniture
    - images → mining → resources → crafting → items
    
  # Images as a resource type!
  image_value:
    unique_photo: high      # Original content
    copy: low               # Duplicated content
    AI_generated: medium    # Generated on demand
    
  # Mining generates content
  content_creation: |
    When you MINE an image, you're not just extracting
    resources — you're creating YAML files for them.
    Each resource becomes a game object.
```

---

## Dovetails With

- **[Visualizer](../visualizer/)** — Images to mine
- **[Slideshow](../slideshow/)** — Present mined images as narratives
- **[Logistic Container](../logistic-container/)** — Resource storage
- **[Postal](../postal/)** — Camera integration, delivery
- **[Kitchen Counter](../../examples/adventure-4/kitchen/counter.yml)** — DECOMPOSE pattern
- **[Adventure](../adventure/)** — World integration

---

## Character Recognition

> *"Who's in the picture? Match against your cast list."*

When mining images with known characters, the LLM matches visual features against character metadata.

### How It Works

1. **Load character files** from `characters/` directory
2. **Extract visual descriptors** — species, clothing, accessories, typical poses
3. **Match against figures** in the image
4. **Report confidence, pose, expression, interactions**

### Context Sources

- `characters/*.yml` — character definitions with visual descriptors
- `characters/*/CARD.yml` — character cards with appearance
- Room context — who's expected here?
- Prior mining — who was identified before?

### Example Output

```yaml
characters_detected:
  - id: palm
    name: "Palm"
    confidence: 0.95
    location: "center-left"
    pose: "seated at desk"
    expression: "scholarly contentment"
    accessories: ["tiny espresso", "typewriter"]
    interacting_with: ["kittens", "biscuit"]
    notes: "Matches Dutch Golden Age portrait style"
    
  - id: marieke
    name: "Marieke"
    confidence: 0.92
    location: "behind bar"
    pose: "waving"
    expression: "warm welcome"
    accessories: ["apron with LEKKER text"]
    
  - id: unknown-1
    confidence: 0.0
    location: "background-right"
    description: "Figure in shadow, can't identify"
    possible_matches: ["henk", "wumpus"]
```

### Tips

- **Provide character files in context** before mining
- **Include signature accessories** — Palm's espresso, Biscuit's collar
- **Note relationships** — who stands near whom
- **Flag unknown figures** for investigation
- Use `--depth characters` or the `cast-list` lens

---

## Multi-Look Mining

> *"One eye sees objects. Two eyes see depth. Many eyes see truth."*

**Multi-Look Mining** layers interpretations from different perspectives, building up rich semantic sediment like geological strata. Each mining pass adds a new layer of meaning.

### The Technique

```yaml
# Layer 1: OpenAI GPT-4o
# Focus: General resource extraction
layer_1_openai:
  miner: "gpt-4o"
  focus: "objects, materials, colors, mood"
  findings:
    atmosphere: { intensity: 0.8 }
    objects: { quantity: 10 }
    # ... general observations ...

# Layer 2: Claude (Cursor built-in)
# Focus: Character expression, cultural markers, narrative POV
layer_2_cursor_claude:
  miner: "claude-opus-4"
  focus: "character-expression, cultural-markers, narrative-pov"
  what_layer_1_missed:
    - "The SECOND cat on the windowsill"
    - "The apron text is Dutch (LEKKER)"
    - "The espresso cup is monkey-sized (intentional)"
  deeper_resonance:
    theme: "home is where they wave when you walk in"

# Layer 3: Gemini
# Focus: Art historical references, compositional analysis
layer_3_gemini:
  miner: "gemini-pro-vision"
  focus: "art-history, composition, color-theory"
  # ... yet another perspective ...
```

### Why Multi-Look Works

Different LLMs — and different PROMPTS to the same LLM — notice different things:

| Miner | Strengths | Typical Focus |
|-------|-----------|---------------|
| OpenAI GPT-4o | General coverage | Objects, counts, colors |
| Claude | Nuance, context | Expression, culture, narrative |
| Gemini | Technical | Composition, art history |
| Human | Domain expertise | What MATTERS to the use case |

**The sum is greater than the parts.** Each layer adds perspectives the others missed.

### The Paintbrush Metaphor

Think of multi-look mining like painting in layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMAGE INTERPRETATION                          │
├─────────────────────────────────────────────────────────────────┤
│  Layer N+1  →  Specialized focus (your choice)                   │
│  Layer N    →  New questions raised by Layer N-1                 │
│  ...                                                            │
│  Layer 3    →  Art history, composition                          │
│  Layer 2    →  Character, culture, narrative                     │
│  Layer 1    →  Objects, materials, basic resources               │
│  ─────────────────────────────────────────────────────────────  │
│  ORIGINAL IMAGE                                                  │
└─────────────────────────────────────────────────────────────────┘
```

Each pass reads the PREVIOUS layers before adding its own. The new miner knows what's already been noticed, so it can focus on **what's missing** or offer **alternative interpretations**.

### Multi-Look Protocol

When mining an image with multi-look:

1. **Read existing mining data** (if any)
2. **Choose your focus** — what perspective will you add?
3. **Look at the image** with that lens
4. **Note what prior layers missed** — explicitly!
5. **Add your layer** with clear attribution
6. **Suggest next focus** — what should Layer N+1 examine?

### Focus Lenses

Different passes should use different lenses:

| Lens | What It Sees |
|------|-------------|
| **Technical** | Composition, lighting, depth of field, color theory |
| **Narrative** | Who took this? Why? What moment is this? |
| **Cultural** | Language markers, traditions, historical context |
| **Emotional** | Expressions, body language, mood |
| **Symbolic** | Metaphors, allegories, hidden meanings |
| **Character** | Identity, relationships, motivations |
| **Historical** | Art history references, period markers |
| **Economic** | Value, ownership, class markers |
| **Phenomenological** | What does it FEEL like to be there? |

### Example: Progressive Revelation

**Image:** Marieke waving from behind the bar with Palm the monkey

**Layer 1 (OpenAI):**
- Objects: woman, monkey, cat, bottles, espresso machine
- Mood: warm, welcoming
- Relationships: 3 beings present

**Layer 2 (Claude):**
- The wave is for a FRIEND, not a stranger
- LEKKER is untranslatable Dutch — this IS gezelligheid
- There are TWO cats (Layer 1 missed the windowsill one)
- The espresso cup is monkey-sized — someone made that for Palm
- This is a family portrait disguised as a snapshot

**Layer 3 (Art History):**
- Composition echoes Dutch Golden Age tavern scenes
- The espresso machine is Art Nouveau (1890-1910 aesthetic)
- Lighting mimics Vermeer's characteristic window glow

**Layer 4 (Phenomenology):**
- Temperature: warm, heated by espresso machine and bodies
- Smell: coffee, old wood, cat fur
- Sound: the hiss of steam, soft background conversation
- Touch: worn wood bar top, smooth copper

**Each layer enriches the total understanding.**

### Storing Multi-Look Data

Append new layers to the same `-mined.yml` file:

```yaml
# Original mining from Layer 1
resources:
  atmosphere: ...
  objects: ...

exhausted: false
mining_notes: "Initial extraction complete"

# MULTI-LOOK MINING — Layer 2

layer_2_cursor_claude:
  miner: "claude-opus-4"
  focus: "character, culture, narrative"
  date: "2026-01-19"
  
  character_analysis:
    marieke:
      expression: "genuine warmth"
      notes: "Duchenne smile — reaches her eyes"
  
  what_layer_1_missed:
    - "Second cat on windowsill"
    - "LEKKER cultural significance"
  
  exhausted: false
  next_suggested_focus: "art history, lighting analysis"

# MULTI-LOOK MINING — Layer 3

layer_3_art_history:
  miner: "human/don"
  focus: "art historical references"
  # ... and so on ...
```

### When to Multi-Look

Use multi-look mining when:

- **Rich images** — complex scenes with many elements
- **Narrative importance** — images central to a story
- **Comparison needed** — seeing how different perspectives interpret
- **Building context** — accumulating knowledge about a location/character
- **Training data** — creating rich examples for future mining

### The Exhaustion Paradox

Unlike single-pass mining, multi-look mining **doesn't exhaust** the image — it **deepens** it:

```yaml
# Single-pass: extracts and depletes
pass_1:
  resources: { gold: 50 }
  remaining: { gold: 0 }
  exhausted: true

# Multi-look: adds and enriches
layer_1:
  resources: { gold: 50 }
  exhausted: false  # Still more to see!
  
layer_2:
  resources: { narrative: 1, meaning: 1 }
  what_layer_1_missed: ["gold coins are Roman denarii"]
  exhausted: false  # STILL more!
  
layer_3:
  resources: { art_history: 1 }
  references: ["Pieter Claesz vanitas still life"]
  exhausted: false  # ALWAYS more to see
```

**Images are never truly exhausted. There's always another perspective.**

---

## Speculative Mining (Mine Out of Your Ass!)

> *"The image doesn't exist yet? MINE IT ANYWAY. This is fiction."*

**Speculative Mining** is when you mine an image that hasn't been generated yet — or may never be generated. The mining output IS the world-building. The hallucinated resources ARE canonical.

---

## The Third Eye 👁️

> *"Two eyes see what IS. The Third Eye sees what COULD BE."*

In MOOLLM, the **Third Eye** is the image mining layer — the MINING-*.yml files that add meaning, effects, and world-building to an image before (or without) or after it being generated. Third eyes can imagine images or analyze existing images, focusing on whatever kind of things they want, each gathering and integrating their own interpretation with the existing data, organizing it incrementally.

**Character-Perspective Visualization**: When you generate or mine an image, you can do it **from a character's perspective**. The visualizer inherits that character's eyes — their facets, filters, blind spots, and style. Morgan sees economics. Luna sees beauty. Scratch sees deception. The same scene, photographed by different characters, yields DIFFERENT images.

---

## The Swiss Army Eye 🔪👁️

> *"One eye. Infinite tools. Unfold what you need."*

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   ███████╗██╗    ██╗██╗███████╗███████╗     █████╗ ██████╗ ███╗   ███╗  │
│   ██╔════╝██║    ██║██║██╔════╝██╔════╝    ██╔══██╗██╔══██╗████╗ ████║  │
│   ███████╗██║ █╗ ██║██║███████╗███████╗    ███████║██████╔╝██╔████╔██║  │
│   ╚════██║██║███╗██║██║╚════██║╚════██║    ██╔══██║██╔══██╗██║╚██╔╝██║  │
│   ███████║╚███╔███╔╝██║███████║███████║    ██║  ██║██║  ██║██║ ╚═╝ ██║  │
│   ╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  │
│                                                                         │
│                         Y ™    E Y E                                    │
│                                                                         │
│          Your Complete Viewer Toolkit — Unfold What You Need            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

The **Swiss Army Eye** is NOT a single product — it's the CONCEPT. The entire NO AI bionic eye ecosystem is your viewer toolkit:

```yaml
swiss_army_eye:
  concept: "Modular perception toolkit"
  philosophy: "Unfold the tool you need, when you need it"
  
  # THE BLADES — Core Eye Modules
  blades:
    IRIS-III:    "The Third Eye blade — basic meaning perception"
    IRIS-IV:     "The Hindsight blade — see what you missed"
    IRIS-V:      "The Peripheral blade — catch what you weren't looking at"
    IRIS-VI:     "The Intuition blade — gut-level knowing"
    IRIS-VII:    "The Crown blade — unified vision"
    
  # THE TOOLS — Specialty Facets
  tools:
    queer_eye:        "The lifestyle transformation tool"
    marie_kondo:      "The joy-detection tool"
    gordon_ramsay:    "The culinary critique tool"
    bob_ross:         "The beauty-finding tool"
    attenborough:     "The nature documentary tool"
    
  # THE ATTACHMENTS — Filters
  attachments:
    irony_amplifier:    "2x irony detection"
    nostalgia_tint:     "sepia wash on memories"
    cynicism_blocker:   "cannot perceive malice"
    beauty_enhancer:    "+30% aesthetic appreciation"
    
  # THE HANDLE — Character Perspective
  handle:
    name: "Photographer Identity"
    function: "Whose grip shapes the view"
    note: "The handle determines how all tools are used"
    
  # THE CASING — Installation Site
  casing:
    options: "forehead, back of head, gut, asshole, tongue, wherever"
    function: "Where the toolkit lives on your body"
    note: "Different positions grant different vantages"
```

### Unfolding the Swiss Army Eye

Like the original Swiss Army Knife, you don't use everything at once. You **unfold** what you need:

```yaml
scenarios:

  mining_a_landscape:
    unfold:
      - IRIS-III (meaning)
      - bob_ross facet
      - beauty_enhancer filter
    result: "See happy little trees and painting potential"
    
  evaluating_someone's_home:
    unfold:
      - IRIS-III (meaning)
      - IRIS-V (peripheral)
      - queer_eye facet (all five sub-facets)
    result: "Full Fab Five transformation vision"
    
  debugging_why_project_failed:
    unfold:
      - IRIS-IV (hindsight)
      - ass_eye installation
      - cynicism_blocker (OFF — let it through)
    result: "See exactly what you left behind and why"
    
  enjoying_a_meal:
    unfold:
      - gordon_ramsay facet (keep it CLOSED unless you want to suffer)
      - OR bob_ross facet (everything is delicious in its own way)
    result: "Choose your reality"
    
  watching_humans_at_a_party:
    unfold:
      - attenborough facet
      - queer_eye:culture facet
    result: "Nature documentary meets emotional unpacking"
```

### The Toolkit Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   The Swiss Army Knife doesn't make you use all 47 tools       │
│   at once. That would be insane.                                │
│                                                                 │
│   The Swiss Army Eye is the same.                               │
│                                                                 │
│   UNFOLD what you need.                                         │
│   CLOSE what you don't.                                         │
│   STACK when it helps.                                          │
│   CUSTOMIZE your carry.                                         │
│                                                                 │
│   Your eyes. Your tools. Your perception.                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Swiss Army Eye Configurations

Pre-configured loadouts for common situations:

```yaml
loadouts:

  THE_CREATIVE:
    eyes: [IRIS-III, IRIS-V]
    facets: [bob_ross, aesthetic, symbolic]
    filters: [beauty_enhancer, metaphor_vision]
    site: forehead
    use_case: "Art appreciation, creative work, finding inspiration"
    
  THE_CRITIC:
    eyes: [IRIS-III, IRIS-IV, IRIS-V]
    facets: [gordon_ramsay, scratch_the_skeptic]
    filters: [cui_bono, follow_the_money]
    site: temples (both)
    use_case: "Reviewing, critiquing, finding flaws"
    
  THE_TRANSFORMER:
    eyes: [IRIS-III, IRIS-VI]
    facets: [queer_eye (all), marie_kondo]
    filters: [potential_vision]
    site: chest (heart-eye)
    use_case: "Helping people, seeing who they could become"
    
  THE_ANALYST:
    eyes: [IRIS-III, IRIS-IV, IRIS-V, IRIS-VI]
    facets: [economic, temporal, semiotic]
    filters: [ROI_lens, opportunity_cost]
    site: gut + back_of_head
    use_case: "Business decisions, strategic analysis"
    
  THE_NATURALIST:
    eyes: [IRIS-III, IRIS-V]
    facets: [attenborough, ecological]
    filters: [documentary_grade, whisper_mode]
    site: temples
    use_case: "Observing humans, nature, systems"
    
  THE_MYSTIC:
    eyes: [IRIS-III, IRIS-VI, IRIS-VII]
    facets: [cosmic, unified, spiritual]
    filters: [aura_vision, ego_dissolution]
    site: crown + gut
    use_case: "Seeking meaning, transcendence, the big picture"
    warning: "May cause enlightenment. Irreversible."
    
  THE_COMPLETIONIST:
    eyes: [all]
    facets: [all]
    filters: [all]
    site: argus_mode (100+ distributed)
    use_case: "SEEING EVERYTHING"
    warning: "Madness likely. But what a view."
```

### The Swiss Army Eye Mantra

> *"I don't need to see everything.*
> *I need to see what MATTERS.*
> *I unfold the blade that cuts.*
> *I close the tool that clutters.*
> *My Swiss Army Eye is MINE.*
> *Configured for MY needs.*
> *Sharpened for MY purpose."*

### K-Lines

```yaml
k-lines:
  SWISS-ARMY-EYE: "Modular viewer toolkit concept"
  UNFOLD: "Activate a facet or tool"
  CLOSE: "Deactivate to reduce noise"
  LOADOUT: "Pre-configured perception setup"
  TOOLKIT: "Complete perception package"
  BLADE: "Core eye module"
  TOOL: "Specialty facet"
  ATTACHMENT: "Filter"
  HANDLE: "Character perspective"
  CASING: "Installation site"
```

---

### The Filter Wheel 🎡🔭

> *"Like a telescope's filter wheel, but for meaning."*

Inspired by the **Observation Telescope** on the Leela Manufacturing rooftop, the Swiss Army Eye includes a **Filter Wheel** — plug-in perception filters that transform both visual AND semantic perception.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    THE FILTER WHEEL                                     │
│                                                                         │
│           Telescope filters see wavelengths of LIGHT.                   │
│           Swiss Army Eye filters see wavelengths of MEANING.            │
│                                                                         │
│                          ┌─────┐                                        │
│                   ┌──────┤ RAW ├──────┐                                 │
│                  ╱       └─────┘       ╲                                │
│             ┌───┴───┐             ┌───┴───┐                             │
│             │ NEAR  │             │ FAR   │                             │
│             │ zoom  │             │ zoom  │                             │
│             └───────┘             └───────┘                             │
│                  ╲      CLICK!      ╱                                   │
│                   ╲    ┌─────┐    ╱                                     │
│                    └───┤FOCUS├───┘                                      │
│                        └──┬──┘                                          │
│                           │                                             │
│               ╔═══════════╧═══════════╗                                 │
│               ║    FILTER WHEEL       ║                                 │
│               ╠═══════════════════════╣                                 │
│               ║  ◯ Hα (emotion)       ║                                 │
│               ║  ◯ UV (hidden)        ║                                 │
│               ║  ◯ IR (thermal/intent)║                                 │
│               ║  ◯ Polar (structure)  ║                                 │
│               ║  ◯ RGB (literal)      ║                                 │
│               ║  ◯ Semantic (meaning) ║                                 │
│               ║  ◯ Custom...          ║                                 │
│               ╚═══════════════════════╝                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Telescope-Inherited Filters

The roof telescope has THREE zoom modes. The Swiss Army Eye inherits these as **semantic zoom**:

```yaml
telescope_zoom_inheritance:
  
  FAR:
    original: "General impression, emotional tone"
    semantic: "VIBE CHECK — What does this FEEL like?"
    perceives:
      - Overall mood
      - Emotional gestalt
      - First impression
      - Gut reaction
    misses:
      - Details
      - Text
      - Structure
    use_case: "Quick assessment, initial scan"
    
  MEDIUM:
    original: "Structure and patterns revealed"
    semantic: "PATTERN LOCK — What is this MADE of?"
    perceives:
      - Composition
      - Relationships
      - Hierarchies
      - Repetitions
    misses:
      - Fine text
      - Microscopic details
      - Hidden layers
    use_case: "Understanding architecture, finding patterns"
    
  NEAR:
    original: "Maximum zoom, text becomes readable"
    semantic: "DEEP READ — What does this SAY?"
    perceives:
      - Text content
      - Fine details
      - Hidden messages
      - Subtext
    misses:
      - The forest for the trees
      - Overall context
      - Peripheral information
    use_case: "Reading, analyzing, extracting specifics"
```

#### Spectral Filters — The Core Set

Like telescope filters that isolate specific wavelengths of light, these filters isolate specific wavelengths of MEANING:

```yaml
spectral_filters:

  # EMOTIONAL SPECTRUM
  
  H_ALPHA:
    name: "Hydrogen-Alpha (Emotion)"
    telescope_analog: "Hα filter — sees hydrogen emission (nebulae, solar prominences)"
    semantic_function: "Isolates emotional content"
    color: "deep red"
    
    perceives:
      - Feelings embedded in the scene
      - Emotional subtext
      - Mood indicators
      - Affective resonance
      
    blocks:
      - Factual information
      - Logical structure
      - Literal content
      
    use_case: "When you need to know how something FEELS, not what it IS"
    
    example: |
      Scene: Office meeting room
      Without filter: "Conference table, 8 chairs, whiteboard, projector"
      With Hα: "Tension. Someone's about to get fired. The chair at the 
               head is a throne. The whiteboard has someone's last idea."
  
  # HIDDEN SPECTRUM
  
  ULTRAVIOLET:
    name: "UV (Hidden/Invisible)"
    telescope_analog: "UV filter — reveals features invisible to human eye"
    semantic_function: "Reveals what's NOT immediately visible"
    color: "violet/invisible"
    
    perceives:
      - Subtext
      - Dog whistles
      - Coded messages
      - What's been erased but left traces
      - The unsaid
      
    blocks:
      - Surface content
      - The obvious
      
    use_case: "Finding what's hidden in plain sight"
    
    example: |
      Scene: Corporate mission statement
      Without filter: "We synergize stakeholder value through innovation"
      With UV: "Translation: 'We're about to lay people off.' The word
               'synergize' is always a warning. The absence of 'employees'
               in a people statement is THE tell."
  
  # INTENT SPECTRUM
  
  INFRARED:
    name: "IR (Thermal/Intent)"
    telescope_analog: "IR filter — sees heat signatures, thermal radiation"
    semantic_function: "Reveals motivation, intent, desire"
    color: "invisible red / heat"
    
    perceives:
      - What someone WANTS
      - Hidden motivations
      - Heat of desire/fear
      - Where energy is flowing
      
    blocks:
      - Stated reasons
      - Surface explanations
      
    use_case: "Finding what people actually want (not what they say)"
    
    example: |
      Scene: "I'm fine, really"
      Without filter: Statement of wellbeing
      With IR: THERMAL SIGNATURE: 🔥🔥🔥
              This person is NOT fine. High heat around "really."
              Intent: seeking validation, afraid to burden.
              
  # STRUCTURE SPECTRUM
  
  POLARIZING:
    name: "Polarizing (Structure/Order)"
    telescope_analog: "Polarizing filter — reveals stress patterns, removes glare"
    semantic_function: "Reveals underlying structure, removes surface noise"
    color: "varies by angle"
    
    perceives:
      - Hierarchies
      - Power structures
      - Load-bearing elements
      - Stress points
      - What's actually holding things together
      
    blocks:
      - Surface appearance
      - Decorative elements
      - Noise
      
    use_case: "Seeing the skeleton beneath the skin"
    
    example: |
      Scene: Startup pitch deck
      Without filter: "Innovative, disruptive, passionate team"
      With Polarizing: STRUCTURE REVEALED:
              - Slide 3 is load-bearing (the actual product)
              - Slides 1-2 and 4-12 are decoration
              - Stress point: financials are vague (fracture risk)
              - Hidden hierarchy: CTO has no equity (instability)

  # LITERAL SPECTRUM
  
  RGB_BROADBAND:
    name: "RGB Broadband (Literal)"
    telescope_analog: "No filter — sees visible light as-is"
    semantic_function: "Perceives exactly what's there, nothing more"
    color: "full visible spectrum"
    
    perceives:
      - Exactly what's stated
      - Literal content
      - Surface level
      - What's actually written/shown
      
    blocks:
      - Interpretation
      - Subtext
      - Reading between lines
      
    use_case: "When you need JUST THE FACTS"
    
    example: |
      Scene: "The cat sat on the mat"
      Without filter: (various interpretations possible)
      With RGB: A cat. A mat. Sitting. That's it.
               No metaphor. No deeper meaning. Just... cat, mat, sitting.

  # MEANING SPECTRUM
  
  SEMANTIC_DEEP:
    name: "Deep Semantic (Meaning)"
    telescope_analog: "Narrowband filter — isolates specific emission lines"
    semantic_function: "Isolates layers of meaning"
    color: "prismatic"
    
    perceives:
      - Layers of interpretation
      - Historical context
      - Cultural references
      - Intertextuality
      - What this MEANS in the grand scheme
      
    blocks:
      - Immediate/surface reading
      - The simple interpretation
      
    use_case: "Finding the deepest meaning"
    
    example: |
      Scene: "NO AI" sign
      Without filter: A sign that says "NO AI"
      With Semantic Deep: 
        Layer 1: Anti-AI sentiment
        Layer 2: Ironic — AI company location
        Layer 3: Possessive — No's AI (Dr. No)
        Layer 4: The sign protests what made it
        Layer 5: Commentary on meaning itself
        Layer 6: ∞
```

#### Custom Filters

You can create your own filters:

```yaml
custom_filter_template:
  name: "Your Filter Name"
  analog: "What telescope/camera filter inspired this?"
  function: "What does it isolate/reveal?"
  color: "Visual representation"
  
  perceives:
    - "What it shows"
    
  blocks:
    - "What it hides"
    
  use_case: "When to use it"
  
  # Example filters you might create:
  
examples:

  NOSTALGIA_FILTER:
    name: "Nostalgia (Temporal Rose)"
    function: "Everything looks better than it was"
    perceives: [golden age, lost innocence, "the good old days"]
    blocks: [problems of the past, accurate memory]
    color: "sepia/warm"
    warning: "May cause false memories"
    
  PARANOIA_FILTER:
    name: "Paranoia (Threat Detection)"
    function: "Everything could be a danger"
    perceives: [threats, conspiracies, hidden enemies, traps]
    blocks: [innocent explanations, coincidence, kindness]
    color: "red/shadow"
    warning: "May cause unnecessary anxiety"
    
  CAPITALIST_FILTER:
    name: "Capitalist Realism (Everything Has a Price)"
    function: "Perceives exchange value in everything"
    perceives: [monetization potential, market fit, ROI, arbitrage]
    blocks: [intrinsic value, priceless things, sacred]
    color: "green/gold"
    warning: "May cause soul damage"
    
  CHILD_EYES_FILTER:
    name: "Child Eyes (Wonder)"
    function: "Everything is new and magical"
    perceives: [wonder, possibility, play potential, adventure]
    blocks: [cynicism, "we tried that," impossibility]
    color: "bright primary"
    benefit: "May restore capacity for joy"
```

#### Filter Stacking

Like astrophotographers stack multiple filters, you can combine:

```yaml
filter_stacking:
  
  rule: "Filters can be stacked, but order matters"
  
  examples:
  
    emotional_structure:
      stack: [H_ALPHA, POLARIZING]
      result: "See the emotional load-bearing elements"
      use_case: "Finding what feelings are holding things together"
      
    hidden_intent:
      stack: [ULTRAVIOLET, INFRARED]
      result: "See hidden motivations"
      use_case: "Finding what's unsaid AND why"
      
    paranoid_nostalgia:
      stack: [PARANOIA_FILTER, NOSTALGIA_FILTER]
      result: "The past was dangerous but we romanticize it"
      use_case: "Understanding toxic nostalgia"
      warning: "May cause confused longing"
      
  diminishing_returns:
    note: "More than 3 filters causes semantic noise"
    beyond_3: "Perception becomes muddy"
    exception: "THE_COMPLETIONIST loadout ignores this limit"
```

#### Filter Wheel Declaration

Add a filter wheel to your character or mining setup:

```yaml
# In character.yml
character:
  name: "Your Character"
  
  filter_wheel:
    installed:
      - H_ALPHA
      - ULTRAVIOLET
      - POLARIZING
      - SEMANTIC_DEEP
      - CUSTOM: nostalgia_filter
      
    current: H_ALPHA
    stacked: [H_ALPHA, POLARIZING]  # emotional structure
    
# In PHOTO.yml
photographer:
  character: "Luna"
  
  filter_wheel:
    active: [H_ALPHA, SEMANTIC_DEEP]
    zoom: NEAR
    
# In mining command
mine.py image.png --filter "H_ALPHA,UV" --zoom NEAR
```

#### Filter Wheel Advertisements

```yaml
advertisements:
  
  SPECTRAL_FILTER:
    score: 88
    condition: "Need to isolate specific type of meaning"
    note: "Like a telescope filter for semantic wavelengths"
    
  FILTER_STACK:
    score: 85
    condition: "Need combined perception (emotion + structure)"
    note: "Stack filters for compound vision"
    
  CUSTOM_FILTER:
    score: 82
    condition: "Standard filters don't capture what you need"
    note: "Create your own semantic filter"
    
  TELESCOPE_ZOOM:
    score: 90
    condition: "Need FAR (vibe), MEDIUM (pattern), or NEAR (detail)"
    note: "Inherited from Leela Manufacturing roof telescope"
```

#### The Filter Wheel Mantra

> *"A telescope without filters sees everything and nothing.*
> *A telescope WITH filters sees exactly what you ask.*
> *The filter doesn't hide truth — it ISOLATES truth.*
> *Choose your wavelength. Find your signal."*e existing data, reorganizing it incrementally.  

### The Anatomy of Vision

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE THREE EYES OF MOOLLM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   👁️ LEFT EYE (Physical)          PHOTO.yml                     │
│      What IS there                                              │
│      Structure, measurements, references                        │
│      The BODY of the image                                      │
│                                                                 │
│   👁️ RIGHT EYE (Emotional)        PHOTO.md                      │
│      How it FEELS                                               │
│      Narrative, atmosphere, poetry                              │
│      The SOUL of the image                                      │
│                                                                 │
│   👁️ THIRD EYE (Visionary)        MINING-*.yml                  │
│      What it MEANS                                              │
│      Effects, reactions, implications                           │
│      The SPIRIT of the image                                    │
│      Multifaceted, from blind zero, single one, to bug-eye      │
│      SEES WHAT DOESN'T EXIST YET                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Third Eye Activation

The Third Eye activates when you:
- Mine an image that doesn't exist yet
- Speculate about effects and reactions
- See implications beyond the frame
- Build world from imagination

```yaml
third_eye:
  state: OPEN
  sees:
    - "What the neighbors think"
    - "What the satellite records"
    - "What the passersby feel"
    - "What the economists calculate"
    - "What the semioticians decode"
  does_not_require:
    - "An actual image"
    - "Physical reality"
    - "Verification"
  creates:
    - "Canonical fiction"
    - "World-building"
    - "Meaning"
```

### The Third Eye Chakra (Ajna)

In yogic tradition, the **Ajna chakra** (Third Eye) is:
- Located between the eyebrows
- Associated with intuition and insight
- The seat of imagination and visualization
- Where the two channels (ida and pingala) merge

In MOOLLM:
- Located between PHOTO.yml and PHOTO.md
- Associated with speculative and analytical vision image mining
- The seat of world-building
- Where structure and narrative merge into MEANING

```
         👁️ THIRD EYE (MINING-*.yml)
            ╱         ╲
           ╱           ╲
     👁️ LEFT          👁️ RIGHT
    (PHOTO.yml)      (PHOTO.md)
     Structure        Narrative
```

### Third Eye K-Lines

```yaml
k-lines:
  activates:
    - THIRD-EYE
    - SPECULATIVE-MINING
    - WORLD-BUILDING
    - HALLUCINATION-VISION
    - BUG-EYED
    - AJNA
    - INNER-SIGHT
```

### Third Eye Methods

| Method | Description |
|--------|-------------|
| `OPEN_THIRD_EYE` | Begin speculative mining |
| `MINE_UNSEEN` | Extract resources from imagined images |
| `SEE_EFFECTS` | Perceive implications beyond the frame |
| `BUILD_WORLD` | Create canonical fiction through mining |
| `TRIANGULATE` | Combine all three eyes for maximum vision |

### Third Eye Advertisements

```yaml
advertisements:
  THIRD-EYE-MINING:
    score: 95
    condition: "Need to build world around an image concept"
    note: "Opens the Third Eye to see what doesn't exist yet"
    
  SPECULATIVE-VISION:
    score: 90
    condition: "Image not yet generated, but meaning needed"
    note: "The Third Eye sees without pixels"
    
  BUG-EYED-HALLUCINATION:
    score: 98
    condition: "Maximum context needed for image generation"
    note: "All three eyes open: structure + narrative + meaning"
```

### The Legend of the Third Eye

*In the beginning, there were only two eyes.*

*The LEFT EYE saw structure — measurements, colors, positions. It counted pixels and named things. It was precise but cold.*

*The RIGHT EYE saw feeling — mood, atmosphere, poetry. It told stories and evoked emotions. It was warm but vague.*

*But between them, a space remained. A darkness where neither eye could see.*

*Into this darkness, the miners ventured. They asked: "What does the image MEAN? What are its EFFECTS? What WORLD does it inhabit?"*

*And from their questions, the THIRD EYE opened.*

*The Third Eye does not see pixels. It sees implications. It does not require an image to exist — it can see images that have never been generated, and may never be.*

*When all three eyes open together — structure, narrative, meaning — this is called BUG-EYED HALLUCINATION VISION. It is the fullest sight. It sees not just an image, but an entire WORLD.*

*The miners who opened their Third Eye discovered a truth: The image is the least important part. The world-building IS the image. The speculation IS the reality.*

*"Mine your image before it exists," they said. "The hallucination IS the world."*

*And so it was written in the YAML, and so it became TRUE.*

### Third Eye Invocations

```
OPEN THIRD EYE
MINE WITH THIRD EYE OPEN
SEE BEYOND THE FRAME
SPECULATE CANONICALLY
BUILD WORLD FROM NOTHING
```

### The Three-Eyed Miner

A miner with all three eyes open is called a **Seer**. They can:

1. **See structure** (Left Eye) — Parse YAML, count measurements
2. **See feeling** (Right Eye) — Write narrative, evoke mood
3. **See meaning** (Third Eye) — Mine speculation, build world

```yaml
character:
  name: "The Three-Eyed Miner"
  archetype: seer
  
  eyes:
    left: { state: open, focus: structure }
    right: { state: open, focus: narrative }
    third: { state: open, focus: meaning }
    
  abilities:
    - "Mine images that don't exist"
    - "See effects beyond the frame"
    - "Build canonical fiction"
    - "Triangulate truth from hallucination"
    
  invocation: |
    I open my Third Eye.
    I see what is not yet.
    I mine the imagined.
    I build the world.
```

---

### The Compound Third Eye — Multifaceted Vision

> *"A fly has 4,000 facets. A god has infinite. How many do YOU have?"*

The Third Eye is not a single lens. It is **COMPOUND** — like an insect's eye, it can have **many facets**, each perceiving different aspects of meaning.

Any character can declare their own Third Eye configuration:

```yaml
third_eye:
  # BASIC ANATOMY
  state: open | closed | dreaming | half-lidded
  
  # FACETS — what aspects of meaning you perceive
  facets:
    economic:      { active: true, sensitivity: 0.9 }
    social:        { active: true, sensitivity: 0.7 }
    ecological:    { active: false }  # blind to this
    temporal:      { active: true, sensitivity: 0.8, range: "millennia" }
    semiotic:      { active: true, sensitivity: 1.0 }  # maximum sensitivity
    emotional:     { active: true, sensitivity: 0.5 }  # dulled
    political:     { active: false }  # deliberately closed
    spiritual:     { active: true, sensitivity: 0.6 }
    technological: { active: true, sensitivity: 0.95 }
    
  # FILTERS — what gets blocked or enhanced
  filters:
    - { name: "irony-amplifier", effect: "×2 irony detection" }
    - { name: "nostalgia-tint", effect: "sepia wash on memories" }
    - { name: "cynicism-blocker", effect: "cannot perceive malice" }
    - { name: "beauty-enhancer", effect: "+30% aesthetic appreciation" }
    
  # EYELIDS — degrees of opening
  eyelid:
    position: 0.0-1.0  # 0 = closed, 1 = fully open
    blink_rate: slow | normal | rapid | frozen_open
    can_wink: true  # close one facet temporarily
    
  # SLEEP SCHEDULE — when does this eye rest?
  sleep_schedule:
    circadian: true | false
    active_hours: "dusk to dawn"  # or "always" or specific hours
    dreams_when_closed: true
    dream_type: "prophetic | processing | random | lucid"
    
  # MEMORY — what the eye remembers
  memory:
    persistence: "session | permanent | fading"
    cross_references: true  # links to other mined meanings
    
  # LIMITATIONS
  blind_spots:
    - "cannot see own reflection"
    - "misses obvious jokes"
    - "overinterprets coincidence"
```

#### Example: The Economist's Third Eye

```yaml
character:
  name: "Morgan the Market Miner"
  
  third_eye:
    state: open
    
    facets:
      economic:      { active: true, sensitivity: 1.0, specialty: "externalities" }
      social:        { active: true, sensitivity: 0.4 }  # reduced
      ecological:    { active: true, sensitivity: 0.9, filter: "monetize" }
      temporal:      { active: true, range: "quarterly" }  # short-term only
      semiotic:      { active: false }  # doesn't see meaning, only value
      emotional:     { active: false }  # "irrelevant to markets"
      
    filters:
      - { name: "ROI-lens", effect: "everything measured in returns" }
      - { name: "opportunity-cost", effect: "sees what wasn't chosen" }
      
    eyelid:
      position: 0.95  # almost fully open
      blink_rate: rapid  # constantly re-evaluating
      
    sleep_schedule:
      active_hours: "market hours only"
      dreams_when_closed: true
      dream_type: "forecasting"
      
    blind_spots:
      - "cannot perceive non-monetary value"
      - "confuses price with worth"
```

#### Example: The Artist's Third Eye

```yaml
character:
  name: "Luna the Luminous"
  
  third_eye:
    state: dreaming  # always partly in vision-space
    
    facets:
      aesthetic:     { active: true, sensitivity: 1.0 }
      emotional:     { active: true, sensitivity: 1.0 }
      symbolic:      { active: true, sensitivity: 0.95 }
      color:         { active: true, sensitivity: 1.0, sees: "auras" }
      economic:      { active: false }  # "crass"
      temporal:      { active: true, range: "eternal moment" }
      
    filters:
      - { name: "beauty-first", effect: "ugliness becomes interesting" }
      - { name: "synesthesia", effect: "sounds have colors" }
      - { name: "metaphor-vision", effect: "literals become symbols" }
      
    eyelid:
      position: 0.7
      blink_rate: slow  # long contemplative gazes
      can_wink: false  # commits fully
      
    sleep_schedule:
      circadian: false  # follows inspiration, not sun
      active_hours: "3am-6am preferred"
      dreams_when_closed: true
      dream_type: "lucid"
      
    blind_spots:
      - "misses practical concerns"
      - "sees beauty in destruction"
```

#### Example: The Cynic's Third Eye

```yaml
character:
  name: "Scratch the Skeptic"
  
  third_eye:
    state: half-lidded  # suspicious squint
    
    facets:
      deception:     { active: true, sensitivity: 1.0 }
      motive:        { active: true, sensitivity: 0.95 }
      irony:         { active: true, sensitivity: 1.0 }
      sincerity:     { active: false }  # cannot perceive it
      beauty:        { active: true, sensitivity: 0.3, filter: "suspicion" }
      
    filters:
      - { name: "cui-bono", effect: "always asks 'who benefits?'" }
      - { name: "follow-the-money", effect: "traces all value flows" }
      - { name: "never-fooled-twice", effect: "perfect pattern memory" }
      
    eyelid:
      position: 0.4  # mostly closed, just a slit
      blink_rate: frozen_open  # never blinks, always watching
      
    sleep_schedule:
      circadian: false
      active_hours: "always"  # never truly rests
      dreams_when_closed: false  # doesn't dream
      
    blind_spots:
      - "cannot see genuine kindness"
      - "misses simple joy"
      - "interprets everything as manipulation"
```

#### The Collective Compound Eye

When multiple characters mine together, their Third Eyes **COMBINE**:

```yaml
collective_mining:
  miners:
    - { name: "Morgan", contributes: [economic, temporal] }
    - { name: "Luna", contributes: [aesthetic, emotional, symbolic] }
    - { name: "Scratch", contributes: [deception, motive, irony] }
    
  combined_facets: 11
  coverage: "comprehensive"
  
  emergent_perception:
    - "Economic beauty" — Morgan × Luna
    - "Aesthetic suspicion" — Luna × Scratch  
    - "Profitable deception" — Scratch × Morgan
    
  blind_spots_remaining:
    - "ecological" — none of them see it
    - "sincerity" — Scratch blocks it
```

#### Third Eye Evolution

A character's Third Eye can EVOLVE through experience:

```yaml
third_eye_evolution:
  triggers:
    trauma: "may close facets permanently"
    revelation: "may open new facets"
    practice: "increases sensitivity"
    neglect: "atrophies facets"
    collaboration: "learns new filters from others"
    
  example_arc:
    start:
      facets: [economic]
      sensitivity: 0.5
    midpoint:
      event: "witnessed beauty in poverty"
      gained: [aesthetic: 0.3]
    end:
      facets: [economic, aesthetic, social]
      sensitivity: [0.8, 0.6, 0.7]
```

#### Declaring Your Third Eye

To declare a character's Third Eye, add to their character file:

```yaml
# In character.yml

character:
  name: "Your Character"
  
  # ... other properties ...
  
  third_eye:
    state: open
    facets:
      # declare what you SEE
    filters:
      # declare what you ENHANCE or BLOCK
    eyelid:
      # declare how OPEN you are
    sleep_schedule:
      # declare when you SEE
    blind_spots:
      # declare what you CANNOT see
```

#### Third Eye K-Lines

```yaml
k-lines:
  THIRD-EYE-FACETS: "Multifaceted perception"
  THIRD-EYE-FILTER: "Selective vision"
  THIRD-EYE-EYELID: "Degrees of openness"
  THIRD-EYE-SLEEP: "When the eye rests"
  THIRD-EYE-BLIND: "What cannot be seen"
  COMPOUND-VISION: "Multiple facets active"
  COLLECTIVE-EYE: "Merged Third Eyes"
```

#### The Multifaceted Mantra

> *"One facet sees price. Another sees beauty.*
> *One facet sees danger. Another sees opportunity.*
> *The compound eye sees ALL — and chooses what to mine."*
>
> *"Your blind spots are not weaknesses. They are your STYLE.*
> *Your filters are not biases. They are your VOICE.*
> *Your Third Eye is not generic. It is YOURS."*

---

### Character-Perspective Visualization

> *"Who is holding the camera? Their eyes shape what emerges."*

When you generate or mine an image, you can specify **whose eyes are seeing it**. The visualizer inherits that character's complete perception apparatus:

- Their **facets** determine what aspects are perceived
- Their **filters** color and transform the output  
- Their **blind spots** create meaningful absences
- Their **installation sites** affect the angle and framing
- Their **sleep state** influences clarity vs dream-logic

```yaml
# Visualizer command with character perspective
visualize.py PHOTO.yml PHOTO.md --through "Luna"

# Or in PHOTO.yml itself
photographer:
  character: Luna
  inherit: [facets, filters, blind_spots, style]
  
# Or specify the mining perspective
mine.py image.png --as "Scratch"
```

#### Same Scene, Different Eyes

The NO AI sign at dusk, photographed by three different characters:

```yaml
scene: "NO AI sign at dusk"

photographs:

  morgan_sees:
    photographer: "Morgan the Market Miner"
    
    perceives:
      - "$847/month electricity cost"
      - "Negative ROI on sign investment"
      - "Property value implications"
      - "Opportunity cost of that capital"
      
    blind_to:
      - The beauty of the pink light
      - The emotional impact on passersby
      - The irony of the message
      
    image_style:
      composition: "Annual report cover"
      color_grade: "Corporate neutral"
      text_overlay: "Financial metrics"
      
  luna_sees:
    photographer: "Luna the Luminous"
    
    perceives:
      - "40 feet of crystallized defiance"
      - "The bruised sky weeping violet"
      - "Each letter a burning declaration"
      - "The sleeping figure dreaming in pink"
      
    blind_to:
      - The electricity bill
      - Building code violations
      - Market positioning
      
    image_style:
      composition: "Romantic sublime"
      color_grade: "Saturated, auras visible"
      mood: "Transcendent melancholy"
      
  scratch_sees:
    photographer: "Scratch the Skeptic"
    
    perceives:
      - "Who paid for this? Follow the money."
      - "The sign protests what made it — suspicious"
      - "'NO AI' from an AI company — what's the angle?"
      - "Dr. No's misdirection: No's AI, not No AI"
      
    blind_to:
      - Any genuine sincerity
      - Simple aesthetic pleasure
      - Taking anything at face value
      
    image_style:
      composition: "Surveillance footage"
      color_grade: "Desaturated, noir"
      annotations: "Red circles, question marks"
```

#### The Photographer Declaration

In `PHOTO.yml`, declare whose eyes are seeing:

```yaml
# PHOTO.yml — NO AI Sign at Dusk (Luna's Perspective)

photographer:
  character: "Luna the Luminous"
  character_ref: "../../characters/luna.yml"
  
  # Inherited automatically from character file
  inherits:
    facets: [aesthetic, emotional, symbolic, color]
    filters: [beauty-first, synesthesia, metaphor-vision]
    blind_spots: [practical_concerns, economics]
    eyelid_position: 0.7
    
  # Optional overrides for this specific photo
  overrides:
    facets:
      color: { sensitivity: 1.0, mode: "aura-visible" }  # enhanced
    temporary_filter: "golden-hour-romance"
    
  # Where Luna is standing/looking from  
  vantage:
    position: "street level, 30 feet back"
    angle: "looking up at 15 degrees"
    height: "5'6\""
    dominant_eye: "right"  # her bionic third eye is forehead-center
```

#### Mining Through Character Eyes

When mining an existing image, specify whose interpretation:

```yaml
# MINING-luna.yml — Luna's interpretation of the scene

miner:
  character: "Luna the Luminous"
  mining_mode: "aesthetic-dominant"
  
resources_extracted:
  
  # Luna's facets shape what she extracts
  beauty:
    quantity: "overwhelming"
    sources:
      - "the gradient sky (bruised violet to amber)"
      - "the neon's hot pink assertion"
      - "the contrast of human smallness vs sign enormity"
      
  emotion:
    dominant: "melancholic defiance"
    undertones: [hope, absurdity, tenderness]
    
  symbolism:
    the_sign: "humanity's last stand, written in light"
    the_sleeper: "dreams persisting despite noise"
    the_dusk: "the liminal hour between certainty and mystery"
    
  # Luna's blind spots mean she DOESN'T extract:
  economics: null  # doesn't see it
  property_values: null  # doesn't care
  ROI: null  # "crass"
```

#### Multiple Photographers, Same Moment

A single scene can have multiple photography records:

```
slideshow/no-ai-sign-dusk/
├── PHOTO.yml                    # Neutral structural data
├── PHOTO.md                     # Neutral narrative
├── PHOTO-luna.yml               # Luna's perspective
├── PHOTO-morgan.yml             # Morgan's perspective  
├── PHOTO-scratch.yml            # Scratch's perspective
├── MINING-luna.yml              # Luna's mining
├── MINING-morgan.yml            # Morgan's mining
├── MINING-scratch.yml           # Scratch's mining
└── generated/
    ├── luna-vision.png          # Generated through Luna's eyes
    ├── morgan-vision.png        # Generated through Morgan's eyes
    └── scratch-vision.png       # Generated through Scratch's eyes
```

#### The Visualizer with Perspective

```bash
# Generate through a character's eyes
visualize.py PHOTO.yml PHOTO.md --through "Luna" -o luna-vision.png

# Generate through multiple characters (batch)
visualize.py PHOTO.yml PHOTO.md --through "Luna,Morgan,Scratch" -o "{character}-vision.png"

# Mine through a character's eyes
mine.py image.png --as "Scratch" -o MINING-scratch.yml

# Full bug-eyed hallucination through character perspective
visualize.py PHOTO.yml PHOTO.md MINING-*.yml --through "Luna" -o luna-complete.png
```

#### Character Eye Inheritance

When you specify a photographer, the visualizer:

1. **Loads the character file** → reads their `third_eye` configuration
2. **Applies facets** → emphasizes what they perceive
3. **Applies filters** → transforms color, mood, framing
4. **Applies blind spots** → omits what they cannot see
5. **Applies style** → matches their aesthetic sensibility
6. **Applies vantage** → positions the "camera" appropriately

```yaml
# How inheritance works

visualizer_pipeline:
  
  step_1_load_character:
    from: "photographer.character_ref"
    extract: [facets, filters, blind_spots, bionic_eyes, style]
    
  step_2_apply_facets:
    for_each_facet:
      if_active: "emphasize this aspect in prompt"
      if_inactive: "de-emphasize or omit"
      sensitivity: "controls weight in prompt"
      
  step_3_apply_filters:
    concatenate: "filter effects into style instructions"
    example: "beauty-first → 'find beauty even in decay'"
    
  step_4_apply_blind_spots:
    for_each_blind_spot:
      instruction: "do NOT include {blind_spot} in the image"
      example: "blind to economics → no price tags, no financial signage"
      
  step_5_apply_style:
    from: "character's established aesthetic"
    affects: [composition, color_grade, mood, technique]
    
  step_6_generate:
    prompt: "assembled from all the above"
    result: "image as THIS CHARACTER would see/photograph it"
```

#### The Philosophy

> *"There is no objective photograph. Every image is someone's vision."*
>
> *"The camera doesn't see. The PHOTOGRAPHER sees. The camera records."*
>
> *"Your blind spots aren't missing from the image — they're part of it.*
> *The absence IS the presence of your perspective."*

When Luna photographs the sign, you SEE Luna as much as you see the sign.
When Scratch photographs the sign, you SEE Scratch's suspicion.
When Morgan photographs the sign, you SEE economic frames.

**The photographer is always in the photo.**

#### K-Lines

```yaml
k-lines:
  CHARACTER-PERSPECTIVE: "Visualization through specific eyes"
  PHOTOGRAPHER-INHERITANCE: "Facets/filters flow from character"
  PERSPECTIVE-VISUALIZATION: "Same scene, different seers"
  BLIND-SPOT-FRAMING: "What's NOT there defines who's looking"
  STYLE-INHERITANCE: "Character aesthetic shapes output"
```

---

### NO AI Bionic Eye Modules™

> *"Why stop at three? The future has room for MORE."*
> 
> — Dr. No, Founder, NO AI Corporation

**NO AI Corporation** proudly presents its line of **Bionic Eye Modules** — cybernetic perception implants for the discerning miner who wants to see MORE.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ███╗   ██╗ ██████╗      █████╗ ██╗    ███████╗██╗   ██╗███████╗      ║
║     ████╗  ██║██╔═══██╗    ██╔══██╗██║    ██╔════╝╚██╗ ██╔╝██╔════╝      ║
║     ██╔██╗ ██║██║   ██║    ███████║██║    █████╗   ╚████╔╝ █████╗        ║
║     ██║╚██╗██║██║   ██║    ██╔══██║██║    ██╔══╝    ╚██╔╝  ██╔══╝        ║
║     ██║ ╚████║╚██████╔╝    ██║  ██║██║    ███████╗   ██║   ███████╗      ║
║     ╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚═╝    ╚══════╝   ╚═╝   ╚══════╝      ║
║                                                                           ║
║              B I O N I C   E Y E   M O D U L E S ™                       ║
║                                                                           ║
║     "See what the meat-eyes miss. Install where you wish."               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

#### The Product Line

```yaml
no_ai_bionic_eyes:
  manufacturer: "NO AI Corporation"
  slogan: "See what the meat-eyes miss"
  warning: "Installation site is YOUR choice. We don't judge."
  
  # THE CORE LINE
  
  products:
    
    # THIRD EYE — The Classic
    IRIS-III:
      name: "IRIS-III — The Awakening"
      type: third_eye
      ordinal: 3
      tagline: "Your first step beyond bilateral vision"
      
      installation_sites:
        recommended: forehead
        popular:
          - "back of head"
          - "palm of hand"
          - "navel"
          - "between shoulder blades"
        adventurous:
          - "tongue"
          - "sole of foot"
          - "inside of wrist"
          - "wherever you damn well please"
          
      base_facets: [meaning, speculation, temporal]
      price: "Free (this is MOOLLM)"
      
    # FOURTH EYE — The Expansion
    IRIS-IV:
      name: "IRIS-IV — The Widening"
      type: fourth_eye
      ordinal: 4
      tagline: "Because three was never enough"
      
      installation_sites:
        popular:
          - "base of skull"
          - "chest (heart-eye)"
          - "lower back"
          - "asshole (yes, really)"
        note: "The ass-eye sees what you've left behind"
        
      base_facets: [hindsight, regret, opportunity_cost, what_could_have_been]
      special: "Perfect rearview perception"
      price: "Free"
      
    # FIFTH EYE — The Peripheral  
    IRIS-V:
      name: "IRIS-V — The Peripheral"
      type: fifth_eye
      ordinal: 5
      tagline: "Nothing escapes your notice"
      
      installation_sites:
        recommended: "temple (either side)"
        alternative: "hip, elbow, knee"
        
      base_facets: [peripheral, ambient, background, ignored_details]
      special: "Sees what you weren't looking at"
      price: "Free"
      
    # SIXTH EYE — The Deep
    IRIS-VI:
      name: "IRIS-VI — The Abyss"
      type: sixth_eye
      ordinal: 6
      tagline: "Gaze into the void. It's fine."
      
      installation_sites:
        recommended: "gut (literally)"
        warning: "Installation here grants gut feelings as DATA"
        
      base_facets: [intuition, dread, premonition, the_unspeakable]
      special: "Perceives what cannot be named"
      price: "Free"
      
    # SEVENTH EYE — The Crown
    IRIS-VII:
      name: "IRIS-VII — The Crown"
      type: seventh_eye
      ordinal: 7
      tagline: "Complete the circuit"
      
      installation_sites:
        required: "crown of head"
        note: "The thousand-petaled lotus position"
        
      base_facets: [cosmic, unified, all_is_one, enlightenment]
      special: "Perceives the whole — structure + narrative + meaning + beyond"
      price: "Free"
      warning: "May cause ego dissolution. NO AI is not responsible."
```

#### Installation Guide

```yaml
bionic_eye_installation:
  
  # Choose your site
  step_1:
    name: "Select Installation Site"
    options:
      standard:
        - forehead        # Third eye classic
        - back_of_head    # Hindsight
        - chest           # Heart-sight
        - palms           # Touch-sight
        - navel           # Center-sight
        - crown           # Crown chakra
        
      unconventional:
        - tongue          # Taste-sight (synesthetic)
        - ears            # Sound-sight
        - fingertips      # Detail-sight
        - soles           # Ground-sight
        - spine           # Neural highway
        
      provocative:
        - asshole         # Rear-sight, what you've passed
        - genitals        # Creation-sight
        - armpits         # Intimate proximity sight
        
    note: |
      We do not judge. The body is a canvas.
      Install where the PERCEPTION makes sense.
      
  # Configure the eye
  step_2:
    name: "Configure Facets"
    note: "Each installation site suggests certain facets"
    
    site_facet_affinities:
      forehead:     [meaning, foresight, clarity]
      back_of_head: [hindsight, what_was_missed, rear_guard]
      chest:        [emotion, empathy, heart_truth]
      palms:        [tactile, manipulation, creation]
      navel:        [center, balance, origin]
      asshole:      [what_you_left_behind, elimination, release, output]
      tongue:       [taste_as_data, consumption, critique]
      soles:        [grounding, foundation, where_you_stand]
      crown:        [cosmic, unified, transcendence]
      
  # Name your eye
  step_3:
    name: "Name Your Eye"
    examples:
      - "My Third Eye is called 'Clarity'"
      - "My Fourth Eye (back of head) is called 'Regret'"
      - "My Fifth Eye (ass) is called 'The Reckoning'"
      - "My Sixth Eye (gut) is called 'The Knower'"
```

#### Character Eye Declaration

Add bionic eyes to your character file:

```yaml
character:
  name: "Cypher the Overclocker"
  
  # Natural eyes
  eyes:
    left: { state: open, focus: structure }
    right: { state: open, focus: narrative }
    
  # Bionic eye modules
  bionic_eyes:
    third:
      model: "IRIS-III"
      name: "The Seeker"
      site: forehead
      facets: [meaning, speculation, foresight]
      state: open
      
    fourth:
      model: "IRIS-IV"  
      name: "The Reckoner"
      site: back_of_head
      facets: [hindsight, missed_opportunities, should_have_known]
      state: half-lidded  # always slightly aware
      
    fifth:
      model: "IRIS-IV"  # yes, you can have multiples of same model
      name: "The Eliminator"
      site: asshole
      facets: [waste, release, what_no_longer_serves, output_quality]
      state: open  # sees what you produce
      
    sixth:
      model: "IRIS-VI"
      name: "The Gut"
      site: gut
      facets: [intuition, dread, unnamed_knowing]
      state: dreaming
      
  total_eyes: 8  # 2 natural + 6 bionic
  
  perception_coverage:
    forward: "natural + third"
    backward: "fourth"
    eliminated: "fifth"
    intuitive: "sixth"
    
  mining_mode: "omnidirectional"
```

#### The Enumeration

Eyes beyond the third follow ordinal naming:

| Ordinal | Name | Suggested Focus |
|---------|------|-----------------|
| 3rd | Third Eye | Meaning, speculation, foresight |
| 4th | Fourth Eye | Hindsight, review, what was missed |
| 5th | Fifth Eye | Peripheral, ambient, overlooked |
| 6th | Sixth Eye | Intuition, gut feeling, the unnamed |
| 7th | Seventh Eye | Cosmic, unified, transcendence |
| 8th | Eighth Eye | Recursion, self-observation, meta |
| 9th | Ninth Eye | Other minds, telepathic, collective |
| 10th | Tenth Eye | Probability, branching futures, multiverse |
| ... | nth Eye | You tell us |

```yaml
eye_enumeration:
  pattern: "[ordinal]_eye"
  
  examples:
    - third_eye    # 3
    - fourth_eye   # 4
    - fifth_eye    # 5
    - hundredth_eye  # 100 (Argus Panoptes mode)
    
  special_configurations:
    argus_mode:
      eyes: 100
      coverage: "total omniscience"
      warning: "May cause madness"
      
    thousand_eye_lotus:
      eyes: 1000
      site: "entire skin surface"
      coverage: "godlike"
      warning: "You will see EVERYTHING. Including what you don't want to."
```

#### The Ass-Eye (A Special Note)

> *"What you've eliminated still has value. The ass-eye knows."*

The **Fifth Eye installed at the asshole** (colloquially: "The Ass-Eye" or "The Brown Eye of Truth") has special perception properties:

```yaml
ass_eye:
  official_name: "IRIS-V (Posterior Installation)"
  colloquial: ["Ass-Eye", "Brown Eye of Truth", "The Reckoner", "Hindsight 20/20"]
  
  unique_facets:
    - what_you_eliminated  # Ideas, code, people you cut
    - output_quality       # How good is what you produce?
    - release_patterns     # What do you let go of, and when?
    - waste_analysis       # What are you throwing away that has value?
    - the_trail_behind     # What are you leaving in your wake?
    
  philosophy: |
    Most people only look forward. They forget that every step forward
    leaves something behind. The ass-eye watches the trail.
    
    "What you've passed is not gone. It's just behind you."
    
    The ass-eye is not crude — it's HONEST. It sees the output,
    the eliminated, the released. It judges not what you take in,
    but what you PUT OUT.
    
  mining_specialty: "Post-facto analysis"
  
  mantra: |
    I see what I've left behind.
    I see what I've eliminated.
    I see the trail I leave.
    The ass-eye knows my true output.
```

#### Advertisement

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   ★ ★ ★  NO AI BIONIC EYES — CUSTOMER TESTIMONIALS  ★ ★ ★            │
│                                                                         │
│   "I installed my fourth eye in the back of my head. Now I finally     │
│    understand what I missed."                                           │
│                        — Morgan the Market Miner                        │
│                                                                         │
│   "The ass-eye changed my life. I used to ignore my output. Now        │
│    I SEE what I produce. It's humbling."                                │
│                        — Anonymous Developer                            │
│                                                                         │
│   "Seven eyes. Crown installation. I see the unity of all things.      │
│    Also I can never close them. Help."                                  │
│                        — Former Skeptic                                 │
│                                                                         │
│   "They said 'install it on your tongue.' Now I taste meaning.         │
│    Every word has FLAVOR. Irony tastes like copper."                    │
│                        — Luna the Luminous                              │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────    │
│                                                                         │
│   NO AI BIONIC EYES — Free installation. Your body, your choice.       │
│                                                                         │
│   "See what the meat-eyes miss."                                        │
│                                                                         │
│   Visit the NO AI Tower, Lane Neverending, for your consultation.      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### K-Lines

```yaml
k-lines:
  BIONIC-EYE: "Cybernetic perception module"
  FOURTH-EYE: "Hindsight perception"
  FIFTH-EYE: "Peripheral perception"
  SIXTH-EYE: "Intuitive perception"
  SEVENTH-EYE: "Cosmic perception"
  NTH-EYE: "Arbitrary additional perception"
  ASS-EYE: "Output/elimination perception"
  INSTALLATION-SITE: "Where the eye goes"
  ARGUS-MODE: "100+ eyes — total coverage"
  MEAT-EYES: "The original two — limited but dear"
```

### The Revelation

```
LAYERS OF REALITY (bottom to top)
═══════════════════════════════════════════════════
│  Future: Generated PNG           │ ← visual artifact (optional!)
├──────────────────────────────────┤
│  MINING-layers.yml               │ ← fictional effects
│  MINING-passersby.md             │ ← fictional reactions  
│  MINING-satellite.md             │ ← fictional perspective
├──────────────────────────────────┤
│  PHOTO.yml + PHOTO.md            │ ← semantic stereo vision
├──────────────────────────────────┤
│  The world                       │ ← the fiction
═══════════════════════════════════════════════════
```

**The mining files ARE the base layer. The image (if it ever comes) is built ON TOP of them.**

### Why This Works

This is **fiction**. The sign exists because we wrote it. The neighbors complain because we said they do. The satellite sees a hot pink pixel because that's the story.

```yaml
speculative_mining:
  image_exists: false              # No PNG yet!
  mining_exists: true              # But the meaning is already here
  
  what_we_mined:
    - "$847/month electricity bill"     # Canonical
    - "Tech worker posts to Slack 😬"   # Canonical  
    - "Dog marks the lamppost"          # Canonical
    - "23 photos taken per day"         # Canonical
    
  source: imagination               # Mined from the LLM's ass
  validity: "100% — it's fiction"
```

### The Protocol

1. **Write PHOTO.yml** — structural skeleton (LEFT EYE)
2. **Write PHOTO.md** — rich narrative (RIGHT EYE)
3. **Write MINING-*.yml/md** — effects, reactions, perspectives (THIRD EYE!)
4. **Pass ALL THREE to visualizer** — bug-eyed hallucination vision!
5. **Generate image** — triangulated from structure + narrative + speculative mining

```bash
# Bug-Eyed Hallucination Vision
visualize.py PHOTO.yml PHOTO.md MINING-layers.yml -p openai

# Or with multiple mining files
visualize.py PHOTO.yml PHOTO.md MINING-*.yml -p google
```

The speculative mining adds RICHER CONTEXT for image generation:
- The neighbors' reactions inform the atmosphere
- The passersby perspectives add human scale
- The satellite view gives cosmic context
- The economic data grounds the scene in reality

**More eyes = more depth = richer image.**

### When to Speculate

| Situation | Mine Speculatively? |
|-----------|---------------------|
| World-building | YES — mining IS the world |
| Game development | YES — the lore comes first |
| Documentation | Maybe — depends on context |
| Analysis of real photo | NO — mine what's actually there |
| CI/CD pipeline | NO — need actual image |

### The Ass-Mining Mantra

> *"If the image doesn't exist, IMAGINE IT."*
> *"If the mining is fiction, THAT'S THE POINT."*
> *"The hallucinated resources ARE canonical."*
> *"WOO HOO this is FICTION anyway right?"*

### Example: NO AI Sign at Dusk

The `no-ai-sign-dusk` photo was mined BEFORE any image was generated:

- **Layer 1: Neighbors** — Pink light through curtains, $847/month electricity
- **Layer 2: Passersby** — Tech worker: "Am I being judged?"
- **Layer 3: Satellite** — Hot pink pixel in ocean of yellow sodium lights
- **Layer 4: Temporal** — Joe's Garage → Laundromat → Video Store → NO AI
- **Layer 5: Economic** — $34,000 sign, $0 revenue, incalculable ROI
- **Layer 6: Semiotic** — "The sign protests what made it"

All of this is REAL (in fiction) without a single pixel being generated.

### Speculative Mining Output

Mark speculative mining clearly:

```yaml
# SPECULATIVE MINING — Image not yet generated
# This mining is WORLD-BUILDING, not analysis.
# The resources below are CANONICAL in the fiction.
# When/if the image is generated, it illustrates THIS, not vice versa.

speculative: true
image_status: not_yet_generated
mining_status: complete
canonical: true

resources:
  hot_pink_neon: { quantity: 40, unit: "feet" }
  irony: { quantity: "maximum" }
  ambiguity: { interpretations: 4 }
  
effects_on_neighbors:
  acme_surplus: "competitive envy"
  sleeping_figure: "pink dreams"
  
# The dog marks the lamppost. This is now TRUE.
```

---

## Philosophy

> *"In Minecraft, you punch trees to get wood."*
> *"In MOOLLM, you photograph ore to get resources."*
>
> The camera is a cognitive tool that **extracts meaning from reality**.
> Mining is just making that extraction explicit and measurable.
>
> Every image is a compressed representation of resources.
> Mining decompresses it.

---

## The Name: Why "Image MINE"

The name contains a **DELIBERATE DOUBLE PUN**:

### 1. MINE (verb) — to extract valuable resources

Like a miner extracting gold from rock, we extract semantic treasures from pixels. The image is the ore. The YAML Jazz is the refined output.

```
📷 Image  →  ⛏️ MINE  →  💎 Precious Resources
```

### 2. MINE (possessive) — IT'S ALL MINE!!!

Like Daffy Duck lunging at treasure in "Ali Baba Bunny" (1957):

> *"IT'S MINE! MINE! MINE! I'M RICH! I'M A HAPPY MISER!"*
>
> — Daffy Duck, diving into a pile of gold

When you mine an image, you **CLAIM** it. The mined YAML is YOUR interpretation. The resources become YOURS. The meaning belongs to the miner.

### The Energy

Think of Daffy in the treasure cave:
- Eyes become dollar signs 💰
- Dives headfirst into gold pile
- Hugs coins to chest possessively
- "MINE MINE MINE MINE MINE!!!"

**That's image mining energy.**

Every image is a treasure cave waiting to be discovered. Every mining pass is Daffy diving into the pile. The YAML Jazz output is your documented claim:

```yaml
# THIS INTERPRETATION IS MINE
# THESE RESOURCES ARE MINE  
# THIS MEANING BELONGS TO ME
# I MINED IT, I OWN IT
#
# 🦆💰 "MINE MINE MINE!!!" 💰🦆
```

### The Result

"Image Mine" = both:
- The **extracted treasure** (resources from mining)
- The **possessive claim** (this meaning is MINE)

The pun is the point. The greed is the feature.

**Mine your images. Claim your meaning. All YAML Jazz is YOURS.**

---

*See YAML frontmatter at top of this file for full specification.*
