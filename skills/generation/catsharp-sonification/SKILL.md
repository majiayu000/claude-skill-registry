---
name: catsharp-sonification
description: Sonify GF(3) color streams via CatSharp scale. Maps Gay.jl colors to pitch classes and plays through sox. Includes metairony mode and Hydra flow grokking.
version: 2.0.0
---


# CatSharp Sonification

Sonify deterministic color streams using the CatSharp scale (Mazzola's Topos of Music).

## Galois Chain

```
seed ⊣ γ ⊣ color ⊣ hue ⊣ pitch ⊣ freq ⊣ tone
```

## Mappings

### Hue → Trit (Gay.jl spec)

| Hue Range | Trit | Role | Temperature |
|-----------|------|------|-------------|
| 0-60°, 300-360° | +1 | PLUS | warm |
| 60-180° | 0 | ERGODIC | neutral |
| 180-300° | -1 | MINUS | cold |

### Trit → Waveform

| Trit | Waveform | Character |
|------|----------|-----------|
| +1 | sine | smooth, harmonic |
| 0 | triangle | balanced, neutral |
| -1 | square | harsh, digital |

### Hue → Pitch Class

```
pitch_class = floor(hue / 30) mod 12
```

30° per semitone maps the color wheel to the chromatic scale.

### CatSharp Pitch → Trit

| Pitch Classes | Trit | Structure |
|---------------|------|-----------|
| {0, 4, 8} (C, E, G#) | +1 | Augmented triad |
| {3, 6, 9} (Eb, F#, A) | 0 | Diminished subset |
| Circle of fifths | -1 | Fifths stack |

## Usage

### Python (sox required)

```python
import subprocess

def play_color(r, g, b, duration=0.15):
    hue = rgb_to_hue(r, g, b)
    trit = hue_to_trit(hue)
    pc = int(hue / 30) % 12
    freq = 261.63 * (2 ** (pc / 12))  # C4 base
    wave = {1: "sine", 0: "triangle", -1: "square"}[trit]
    subprocess.run(["play", "-q", "-n", "synth", str(duration), 
                    wave, str(freq), "vol", "0.3"])
```

### Babashka

```clojure
(defn play-trit [trit freq]
  (let [wave (case trit 1 "sine" 0 "triangle" -1 "square")]
    (shell "play" "-q" "-n" "synth" "0.15" wave (str freq) "vol" "0.3")))
```

### Julia (Gay.jl)

```julia
using Gay

function sonify_stream(seed, n=12)
    Gay.gay_seed!(seed)
    for _ in 1:n
        c = Gay.next_color()
        hue = Gay.Colors.convert(Gay.HSL, c).h
        pc = mod(round(Int, hue / 30), 12)
        freq = 261.63 * 2^(pc / 12)
        trit = hue < 60 || hue >= 300 ? 1 : hue < 180 ? 0 : -1
        wave = Dict(1 => "sine", 0 => "triangle", -1 => "square")[trit]
        run(`play -q -n synth 0.15 $wave $freq vol 0.3`)
    end
end
```

## GF(3) Conservation

Every tripartite emission sums to 0 mod 3:

```
MINUS(-1) + ERGODIC(0) + PLUS(+1) = 0
```

## Modelica Formulation

See `catsharp.mo` for acausal equation-based model.

## Dependencies

- `sox` (via flox: `flox install sox`)
- Python 3.x or Julia with Gay.jl
- macOS `afplay` as fallback

## Related Skills

- `gay-mcp`: Deterministic color generation
- `rubato-composer`: Mazzola's mathematical music theory
- `topos-of-music`: Full categorical music implementation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
catsharp-sonification (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch8: Degeneracy
- Ch10: Adventure Game Example

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.

---

## v2.0.0: Metairony & Hydra Flow Grokking

### New Modes

| Mode | Flag | Description |
|------|------|-------------|
| **Metairony** | `--metairony` | The sound of self-reference |
| **Just Intonation** | `--ji` | 5-limit tuning ratios |
| **Consonant Only** | `--consonant` | Filter to consonant intervals |
| **PLR Sequences** | `--plr PLRPLR` | Neo-Riemannian transformations |
| **Tool Algebra** | `--tools exa,babashka,beeper` | S-P-O chain sonification |
| **Maximal** | `--maximal` | All modes combined |
| **Champions** | `--champions` | Top 3 GF(3)-conserved seeds |

### Metairony: Coloring Outside AND Inside the Lines

```bash
python3 sonify.py --metairony
```

Four phases of self-referential sonification:

1. **INSIDE THE LINES** — Perfect GF(3) conservation
   - `finder_search(-1) + oracle_think(0) + create_file(+1) = 0`
   
2. **OUTSIDE THE LINES** — Deliberate transgression
   - `read(-1) + read(-1) + read(-1) = -3 ≡ 0` (the heresy was orthodoxy)
   
3. **METAIRONIC BRIDGE** — The joke that knows it's a joke
   - `sonify(sonify)` — the script sonifying itself
   
4. **SURPRISING BISIMILARITY**
   - `iBeacon physical consensus ≅ PLR transformations ≅ Gay.jl trit streams`

### Hydra Flow Grokking: 69 Candidates

Browser-based p5.js visualization of Hydra live-coding synth taxonomy:

```bash
open hydra-grok.html
```

**Distance = Information × Agency × Energy**

| Category | Trit | Functions | Profile |
|----------|------|-----------|---------|
| Source | +1 🔴 | osc, noise, shape... | High information generation |
| Geometry | 0 🟢 | rotate, scale, kaleid... | Transform, conserve |
| Color | 0 🟢 | posterize, hue... | Low agency |
| Blend | -1 🔵 | add, mult, diff... | Consume/combine |
| Modulate | -1 🔵 | modulate*, feedback | Highest info (0.9) |
| External | -1 🔵 | initCam, initScreen | Max info input |
| Synth | +1 🔴 | render, out, hush | Max agency |

**Temperature τ controls clustering:**
- Low τ (0.1): Sharp deterministic clusters
- High τ (2.0): Melted stochastic mixing
- τ = 0.69: Nice balance (default)

69 distance metrics cycle through information-theoretic, agency-based, energy-based, GF(3), thermodynamic, and categorical measures.

### Yulyia ↔ greentea Bicomodule Bridge

Synthesis from beeper-mcp decision analysis:

```
Tool Algebra Chain: exa → deepwiki → babashka → beeper
Spectral Gap: λ₂ = 0.32 → tempo = 158.4 BPM
PLR Transitions: Neo-Riemannian as pitch transformations
```

**Bisimulation Indistinguishability:**
- Yuliya's tool algebra ≅ `--tools` sonification mode
- greentea's YOOZ color chains ≅ Gay.jl seed 1069 stream
- iBeacon physical consensus ≅ PLR graph walks

### Files Added

| File | Description |
|------|-------------|
| `metairony.html` | p5.js + Web Audio metaironic visualization |
| `hydra-grok.html` | 69-candidate temperature-clustered flow analysis |
| `sonify.py` | Extended with `--metairony`, `--ji`, `--consonant`, `--plr`, `--tools` |

### Interaction Exemplar: 2026-01-07

> "color outside and inside the lines - the metairony sonify it"

The request to simultaneously transgress AND conserve GF(3) led to:
- Phase 2 plays tritone (devil's interval) for each transgression
- `-3 ≡ 0 (mod 3)` reveals: even breaking the rules conserves
- The metaironic insight: the difference IS the identity

---

## Skill Interleavings

| Connected Skill | Morphism | GF(3) Role |
|-----------------|----------|------------|
| `gay-mcp` | seed → color → pitch | Source (+1) |
| `topos-of-music` | PLR ↔ pitch class | Transform (0) |
| `hydra-synth` | 69 functions → clusters | Analysis (-1) |
| `rubato-composer` | Mazzola forms | Theory (0) |
| `qri-valence` | XY defects → dissonance | Mapping (-1) |
| `bisimulation-game` | Entity indistinguishability | Verification (+1) |