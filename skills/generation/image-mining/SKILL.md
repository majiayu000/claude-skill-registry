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
  
  # === RESOURCE MAP (instantiated by LLM analysis) ===
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

# ═══════════════════════════════════════════════════════════════
# MULTI-LOOK MINING — Layer 2
# ═══════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════
# MULTI-LOOK MINING — Layer 3
# ═══════════════════════════════════════════════════════════════

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

*See YAML frontmatter at top of this file for full specification.*
