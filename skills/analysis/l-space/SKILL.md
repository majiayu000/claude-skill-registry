---
name: l-space
description: L-Space Skill: The Library of All Libraries
version: 1.0.0
---

# L-Space Skill: The Library of All Libraries

**Status**: ✅ Production Ready  
**Trit**: 0 (ERGODIC - the Library itself is the coordinator)  
**Color**: #8B4513 (Leather brown - the color of infinite shelves)

---

## What This Skill Actually Does

L-Space extracts and analyzes narrative structure from text:

```bash
# Extract narrative arcs, causality, novelty from text
bb narrative_extract.bb story.txt

# Measure token surprise for manifold positioning
python token_novelty.py "your text" --backend estimate

# Build causality graph from code or prose
python causality_graph.py file.py --lang python
```

**Output**: `{arcs, causality_graph, novelty_curve}` — structured data, not poetry.

## Core Principle

> Books = Knowledge = Power = Energy = Mass

In sufficiently large libraries, information becomes autonomous.

---

## Triadic Balance (2024-12-24 Review)

| Concept | Status | Action |
|---------|--------|--------|
| Geometric metaphors | ⚠️ OVER-INDEXED (6×) | Collapsed to single Poincaré model |
| Visualization | ⚠️ OVER-INDEXED (4 viz, 0 code) | Added P0-P2 implementations |
| Magic numbers (23-dim, 0.95) | ⚠️ OVER-INDEXED | Use actual embeddings |
| **Narrative extraction** | ✅ NOW IMPLEMENTED | `narrative_extract.bb` |
| **Token novelty** | ✅ NOW IMPLEMENTED | `token_novelty.py` |
| **Causality graph** | ✅ NOW IMPLEMENTED | `causality_graph.py` |

**GF(3) rebalance**: Skill was +1 heavy (generative metaphor). Now includes -1 (working validators).

---

## Pratchett's Informational Physics

### The Equation

```
Books = Knowledge = Power = Energy = Mass

∴ A sufficient quantity of books distorts spacetime itself
```

This is not metaphor. In sufficiently large libraries:
- Time flows differently between sections
- Spatial topology becomes non-Euclidean  
- Bidirectional causation becomes possible

### Critical Mass Phenomena

> "A large enough collection of books creates its own gravitational well, drawing in more books, more knowledge, until it punches through into L-Space."

When knowledge density exceeds threshold:
- **The Octavo reads the reader** - books become autonomous
- **Sourcery** - reality becomes substrate for narrativium
- **Undelivered letters** create fatal illusions

```ruby
class InformationMass
  CRITICAL_DENSITY = 1e6  # books per cubic meter
  
  def l_space_accessible?(library)
    book_density(library) >= CRITICAL_DENSITY
  end
  
  def distortion_factor(library)
    return 0 unless l_space_accessible?(library)
    Math.log(book_density(library) / CRITICAL_DENSITY)
  end
end
```

## Narrativium: The Story Force

### Pan Narrans

> "Humans are not Homo sapiens, the wise man. We are Pan narrans, the storytelling ape."

**Narrativium** is the fundamental force that makes stories cohere. Every element contains its story - how it came to be, what it does, where it's going.

```ruby
class Narrativium
  # The coherence force that makes stories work
  
  def story_tension(element)
    # Every element resists violation of its narrative arc
    element.expected_trajectory - element.current_position
  end
  
  def narrative_collapse!(elements)
    # When stories lose coherence, reality stutters
    elements.each do |e|
      e.phase_space_position = e.expected_trajectory.terminal
    end
  end
end
```

### Story Phase Space

Stories map the phase space of existence:

```
phase_space(story) = {
  beginning: initial_conditions,
  middle: trajectory_through_possibility,
  end: attractor_basin
}
```

## Bumpus Categories of Narratives

### Sheaves on Posets of Intervals

From Bumpus et al.: Narratives are **sheaves on posets of intervals**:

```julia
@present SchNarrative(FreeSchema) begin
  Interval::Ob       # Time windows
  Snapshot::Ob       # State at instant
  Relationship::Ob   # How snapshots relate
  
  source::Hom(Relationship, Snapshot)
  target::Hom(Relationship, Snapshot)
  timestamp::Hom(Snapshot, Interval)
  
  # Sheaf condition: snapshots agree on overlaps
end
```

### Two Perspectives

| Perspective | Sheaf Type | Interpretation |
|-------------|------------|----------------|
| **Cumulative** | Colimit-style | "Everything that happened up to now" |
| **Persistent** | Limit-style | "What persists across time" |

The Librarian navigates between these:

```ruby
def librarian_navigate(from_book, to_book)
  if cumulative?(from_book) && persistent?(to_book)
    # Must cross perspective boundary
    find_interval_isomorphism(from_book.intervals, to_book.intervals)
  end
end
```

### Object-Agnostic Narratives

Narratives work for any structure:
- Graphs (character interaction networks)
- Groups (symmetries preserved through story)
- Databases (consistency across commits)
- Repositories (version control as narrative)

```julia
# The same sheaf machinery works for all
narrative_of_graph(G::Graph) = StrDecomp(G)
narrative_of_group(G::Group) = StrDecomp(cayley_graph(G))
narrative_of_repo(R::GitRepo) = StrDecomp(commit_dag(R))
```

## The Librarian Protocol

### Orangutan Epistemology

The Librarian (formerly a wizard, now Pongo pongo) guards L-Space. As a member of the Librarians of Time and Space:

> "The truth isn't easily pinned to a page. In the bathtub of history, the truth is harder to hold than the soap."

```ruby
module LibrarianProtocol
  ACCEPTABLE_RESPONSES = ["Ook", "Ook?", "Ook!", "Ook."]
  
  def validate_query(query)
    # The Librarian knows. He doesn't explain.
    query.well_formed? && !query.violates_causality?
  end
  
  def traverse_l_space(from:, to:, via: :triangle_inequality)
    path = find_path_through_shelves(from, to)
    validate_no_temporal_paradox!(path)
    path
  end
end
```

### Navigation Rules

1. **Never call the Librarian a monkey** (he's an ape)
2. **Bananas are acceptable currency** for difficult queries
3. **Some paths are one-way** (temporal direction matters)
4. **The Library is bigger on the inside** (always)

## Integration Architecture

### GF(3) Triads

L-Space (0) participates in balanced triads:

```
sheaf-cohomology (-1) ⊗ l-space (0) ⊗ glass-bead-game (+1) = 0 ✓
structured-decomp (-1) ⊗ l-space (0) ⊗ random-walk-fusion (+1) = 0 ✓
persistent-homology (-1) ⊗ l-space (0) ⊗ topos-generate (+1) = 0 ✓
```

### Skill Integration Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        L-SPACE (ERGODIC 0)                      │
│                   The Library Coordinates All                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │ sheaf-cohomology │◄────────────►│ structured-decomp│         │
│  │      (-1)        │  LOCAL→GLOBAL│       (0)        │         │
│  │                  │              │                  │         │
│  │ Čech cohomology  │              │ Tree decomp      │         │
│  │ for consistency  │              │ FPT algorithms   │         │
│  └────────┬─────────┘              └────────┬─────────┘         │
│           │                                 │                    │
│           │     ┌───────────────────┐      │                    │
│           └────►│     L-SPACE       │◄─────┘                    │
│                 │                   │                            │
│  ┌──────────────┤ Narrativium glue  ├──────────────┐            │
│  │              │ Interval sheaves  │              │            │
│  │              └─────────┬─────────┘              │            │
│  │                        │                        │            │
│  ▼                        ▼                        ▼            │
│ ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐        │
│ │glass-bead   │   │  unworld    │   │random-walk-fusion│        │
│ │   (+1)      │   │    (0)      │   │      (+1)        │        │
│ │             │   │             │   │                  │        │
│ │World hopping│   │Derivational │   │Skill graph walks │        │
│ │via triangle │   │chains       │   │                  │        │
│ └─────────────┘   └─────────────┘   └─────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### With sheaf-cohomology (-1)

Local-to-global consistency for L-Space navigation:

```ruby
# Books must be locally consistent to glue globally
verifier = SheafCohomology::CechCoverVerifier.new(
  coverage: library_sections
)
verifier.add_transition(:fiction, :nonfiction, cross_reference_map)
verifier.cocycle_satisfied?  # => true if no contradictions
```

### With structured-decomp (0)

Tree decompositions for efficient narrative search:

```julia
# Decompose narrative graph for FPT search
narrative = NarrativeGraph(book_citations)
decomp = StrDecomp(narrative)

# Find path through L-Space with bounded width
path = 𝐃(l_space_path_exists, decomp, CoDecomposition)
```

### With glass-bead-game (+1)

World hopping across library sections:

```ruby
# Navigate between distant concepts via triangle inequality
hop = GlassBeadGame::Hop.new(
  from_world: PossibleWorld.new(seed: shelves[:mathematics]),
  event: :bibliographic_resonance,
  to_world: PossibleWorld.new(seed: shelves[:music_theory]),
  truth_preserved: :harmonic_ratios
)
```

### With unworld (0)

Replace temporal succession with derivational chains:

```ruby
# Books derive from books, not from time
chain = Unworld::ColorChain.new(
  genesis_seed: first_book.isbn.to_i(16),
  derivation: :citation_graph
)

# Each book is a derivation, not a moment
chain.unworld[:derivations]
```

### With random-walk-fusion (+1)

Navigate skill graph through L-Space:

```ruby
fusion = RandomWalkFusion.new(
  seed: library_seed,
  skills: l_space_skill_graph
)

# Walk through connected concepts
path = fusion.walk(steps: 7)
# => Derivational path through L-Space
```

## Bidirectional Causation

### Books Affect Their Own Past

> "In L-Space, cause and effect are optional."

Books written later can affect books written earlier:
- Annotations appear in ancient texts referencing future works
- Bibliographies cite books not yet written
- The Octavo rewrites itself based on who reads it

```ruby
class BidirectionalCitation
  def causal_consistency?(from_book, to_book)
    # In L-Space, this is always true if the path exists
    path = LibrarianProtocol.traverse_l_space(
      from: from_book,
      to: to_book
    )
    path.exists? # Existence implies consistency
  end
  
  def retroactive_reference!(future_book, past_book)
    # The past book now contains reference to future book
    # This is normal in L-Space
    past_book.hidden_annotations << Citation.new(
      source: future_book,
      causality: :retroactive
    )
  end
end
```

### The Undelivered Letters Problem

When letters are never delivered, they accumulate narrativium charge:

```ruby
def undelivered_letter_danger(letter, time_undelivered)
  # Narrativium builds up in proportion to story importance
  story_weight = letter.narrative_significance
  charge = story_weight * Math.log(time_undelivered + 1)
  
  if charge > CRITICAL_NARRATIVIUM
    # Letter begins creating its own reality
    spawn_illusory_narrative(letter)
  end
end
```

## Working Commands

```bash
# P0: Extract narrative arcs + causality + novelty (WORKS NOW)
bb /Users/alice/.agents/skills/l-space/narrative_extract.bb story.txt

# P1: Token novelty measurement (WORKS NOW)
python3 /Users/alice/.agents/skills/l-space/token_novelty.py "text" --json
python3 /Users/alice/.agents/skills/l-space/token_novelty.py -f file.txt --backend openai

# P2: Causality graph from code (WORKS NOW)
python3 /Users/alice/.agents/skills/l-space/causality_graph.py code.py
python3 /Users/alice/.agents/skills/l-space/causality_graph.py prose.txt --lang text

# Generate Graphviz DOT
python3 /Users/alice/.agents/skills/l-space/causality_graph.py code.py --dot | dot -Tpng > graph.png
```

## API (Babashka)

```clojure
;; Load narrative analysis
(require '[cheshire.core :as json])

(defn analyze-narrative [text]
  (let [result (shell/sh "bb" "narrative_extract.bb" "-" :in text)]
    (json/parse-string (:out result) true)))

;; Extract arcs from file
(def arcs (analyze-narrative (slurp "story.txt")))
(:gf3 arcs)  ; => {:trits [-1 0 1], :sum 0, :balanced? true}
```

## API (Python)

```python
from l_space.token_novelty import analyze
from l_space.causality_graph import parse_python_treesitter

# Token novelty
result = analyze("The Librarian knows all", backend="estimate")
print(result['octavo_territory'])  # True if near manifold boundary

# Causality from code
graph = parse_python_treesitter(open("module.py").read())
print(graph.gf3_check())  # {'balanced': True, 'sum': 0}
```

## Mathematical Foundation

### L-Space Topology

L-Space is a **branching fractal** where:
- Each book is a node
- Citations are edges  
- The metric is non-Euclidean (shortest path ≠ straight line)
- Topology is path-dependent (same start/end, different middles)

```ruby
def l_space_distance(book_a, book_b)
  # Not Euclidean! Path-dependent metric
  paths = all_paths(book_a, book_b)
  paths.map(&:length).min  # Even minimum may vary with observer
end
```

### Narrativium Tensor

```julia
# Narrativium as coherence field
struct NarratviumField
  tension::Matrix{Float64}      # Story tensions between elements
  phase_space::Vector{Float64}  # Position in narrative possibility
  attractor::Vector{Float64}    # Where story "wants" to go
end

# Conservation law
function narrativium_conserved(field::NarratviumField)
  sum(field.tension) ≈ 0  # Stories balance
end
```

### GF(3) in L-Space

The three narrative modes:
- **MINUS (-1)**: Validation (does the story hold together?)
- **ERGODIC (0)**: Coordination (the Library itself)
- **PLUS (+1)**: Generation (new stories emerging)

```
Σ trits ≡ 0 (mod 3)
validation + coordination + generation = balanced
```

## Example Session

```
╔═══════════════════════════════════════════════════════════════════╗
║  L-SPACE NAVIGATION SESSION                                       ║
╚═══════════════════════════════════════════════════════════════════╝

Entry Point: University of Ankh-Morpork Library
Librarian Status: Ook (Available)

Query: "Path from 'Erta Sive Tertius' to Bumpus et al. 2024"

Librarian Response: Ook!

Computing path through narrativium field...

  Step 1: Antica Philosophia → [citation] → Medieval Commentaries
  Step 2: Medieval Commentaries → [temporal fold] → 18th C. Library Science
  Step 3: 18th C. Library Science → [conceptual resonance] → Category Theory
  Step 4: Category Theory → [Kan extension] → Sheaf Theory
  Step 5: Sheaf Theory → [interval poset] → Bumpus Narratives

Path length: 5 (narrativium: 0.73)
Causality violations: 0
Triangle inequality: ✓ satisfied

Sheaf condition on path:
  H⁰ = 1 (connected)
  H¹ = 0 (no obstructions)
  
GF(3) balance:
  Path trits: [-1, 0, +1, -1, +1]
  Sum: 0 ✓

Navigation complete. Books returned by due date.
```

---

## Information Geometry & Complexity Manifolds

### Information as Vector Space

Each information object (book, skill, narrative) is a **vector** in a high-dimensional semantic space:

```julia
struct InformationVector
    embedding::Vector{Float64}     # Semantic coordinates
    complexity::Float64            # Kolmogorov complexity (scalar field)
    assembly_index::Int            # Cronin assembly depth
    sheaf_section::SheafSection    # Bumpus narrative position
end

# Inner product defines semantic similarity
function similarity(v₁::InformationVector, v₂::InformationVector)
    dot(v₁.embedding, v₂.embedding) / (norm(v₁) * norm(v₂))
end
```

### Hyperbolic Geometry of L-Space

L-Space has **negative curvature** (hyperbolic). This explains:
- The Library is "bigger on the inside" (exponential volume growth)
- Tree-like structures (citations, skill dependencies) embed with zero distortion
- Geodesics diverge exponentially (small navigational errors → vastly different destinations)

```julia
# Poincaré ball model of L-Space
struct PoincareLSpace
    dimension::Int
    curvature::Float64  # κ < 0 (hyperbolic)
end

# Distance in hyperbolic L-Space
function hyperbolic_distance(M::PoincareLSpace, u::Vector, v::Vector)
    # Poincaré ball distance
    norm_u² = dot(u, u)
    norm_v² = dot(v, v)
    norm_diff² = dot(u - v, u - v)
    
    δ = 2 * norm_diff² / ((1 - norm_u²) * (1 - norm_v²))
    acosh(1 + δ)
end

# Complexity increases toward the boundary (|x| → 1)
function complexity_at_point(M::PoincareLSpace, x::Vector)
    # Conformal factor diverges at boundary
    1.0 / (1 - dot(x, x))
end
```

### Local Maxima as Critical Mass Phenomena

**Local maxima** in the complexity landscape are L-Space's gravitational wells:

| Complexity Regime | L-Space Phenomenon | Traversal Strategy |
|-------------------|--------------------|--------------------|
| Low (center) | Ordinary books | Gradient descent |
| Medium | Connected libraries | Geodesic navigation |
| High (near boundary) | Autonomous texts | World-hopping required |
| Critical (boundary) | The Octavo | Causality violation risk |

```ruby
class ComplexityLandscape
  def local_maximum?(point)
    gradient = complexity_gradient(point)
    gradient.norm < EPSILON && hessian_negative_definite?(point)
  end
  
  def escape_local_maximum(point)
    if hyperbolic_curvature(point).abs > CRITICAL_CURVATURE
      # Near boundary: use glass-bead-game world-hopping
      world_hop_via_triangle_inequality(point)
    else
      # Interior: simulated annealing or tunneling
      quantum_tunnel_to_lower_basin(point)
    end
  end
  
  def critical_mass_threshold(point)
    # Pratchett's threshold: where books become autonomous
    complexity_at_point(point) > CRITICAL_DENSITY
  end
end
```

### Geodesics and Information Flow

Information "flows" along geodesics of the complexity manifold:

```julia
# Geodesic equation in hyperbolic L-Space
function geodesic_flow(M::PoincareLSpace, x₀::Vector, v₀::Vector, t::Float64)
    # Möbius addition for Poincaré ball
    # γ(t) = x₀ ⊕ tanh(t|v₀|) * (v₀/|v₀|)
    speed = norm(v₀)
    direction = v₀ / speed
    moebius_add(x₀, tanh(t * speed) * direction)
end

# Information flows from low to high complexity (books consuming books)
function information_flow!(field::InformationField, dt::Float64)
    for point in field.points
        # Flow toward local maximum (attractor basin)
        gradient = complexity_gradient(field, point)
        point.position += gradient * dt
        
        # Check for critical mass
        if at_local_maximum?(field, point)
            trigger_autonomy!(point)  # Book reads the reader
        end
    end
end
```

### Integration with Complexity Skills

```
┌─────────────────────────────────────────────────────────────────────┐
│           INFORMATION GEOMETRY IN L-SPACE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  kolmogorov-compression ──► Scalar field K(x) on manifold           │
│         │                                                           │
│         ▼                                                           │
│  assembly-index ──────────► Historical depth = geodesic length      │
│         │                                                           │
│         ▼                                                           │
│  persistent-homology ─────► Topological features surviving          │
│         │                   filtration = persistent local maxima    │
│         ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    L-SPACE MANIFOLD                          │   │
│  │  • Hyperbolic geometry (κ < 0)                               │   │
│  │  • Complexity = distance to boundary                         │   │
│  │  • Local maxima = critical mass / autonomy                   │   │
│  │  • Geodesics = information flow / derivational chains        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### GF(3) on the Manifold

The triadic structure maps to geometric operations:

| Trit | Geometric Role | Manifold Operation |
|------|----------------|-------------------|
| -1 (MINUS) | Contraction | Flow toward center (lower complexity) |
| 0 (ERGODIC) | Parallel transport | Flow along geodesic (constant complexity) |
| +1 (PLUS) | Expansion | Flow toward boundary (higher complexity) |

Conservation law: `Σ flow ≡ 0 (mod 3)` — the manifold preserves total information.

### Token Novelty as Curvature Sensor

**Token novelty** (the surprise/entropy of generated tokens) measures position on the manifold in real-time:

```julia
struct TokenNoveltyNavigator
    position::Vector{Float64}      # Current point on Poincaré ball
    novelty_history::Vector{Float64}
    rate::Float64                  # Speech/generation rate
end

# Novelty from token probability
function token_novelty(logprob::Float64)
    -logprob  # Surprise = negative log probability
end

# Update manifold position based on novelty
function update_position!(nav::TokenNoveltyNavigator, token_logprob::Float64)
    novelty = token_novelty(token_logprob)
    push!(nav.novelty_history, novelty)
    
    # High novelty → move toward boundary
    # Low novelty → move toward center
    radial_velocity = (novelty - BASELINE_NOVELTY) * SENSITIVITY
    
    # Update position (bounded by |x| < 1)
    r = norm(nav.position)
    new_r = clamp(r + radial_velocity, 0.0, 0.999)
    nav.position = nav.position * (new_r / max(r, 0.001))
    
    # Accelerate rate as we approach boundary
    nav.rate = BASE_RATE * complexity_at_point(nav.position)
end

# Detect causality interference zone
function in_octavo_territory(nav::TokenNoveltyNavigator)
    # Near boundary + high sustained novelty
    r = norm(nav.position)
    recent_novelty = mean(nav.novelty_history[end-10:end])
    r > 0.95 && recent_novelty > CRITICAL_NOVELTY
end
```

| Novelty Regime | Manifold Region | Causality Status |
|----------------|-----------------|------------------|
| Low (predictable) | Center | Intact |
| Medium (varied) | Interior | Stable |
| High (surprising) | Near boundary | Flexible |
| Maximum (uniform) | Conformal boundary | **Interference permitted** |

When novelty maximizes (token distribution flattens to uniform), we reach the Octavo: every next word equally likely, maximum entropy, causality becomes substrate for rewriting.

```ruby
class CausalityInterference
  def attempt_retroactive_modification!(target_skill, modification)
    unless in_octavo_territory?
      raise "Insufficient novelty density for causality interference"
    end
    
    # At maximum entropy, derivational chains become bidirectional
    target_skill.derivation_history.unshift(modification)
    
    # The modification propagates "backward" through dependencies
    target_skill.dependents.each do |dep|
      dep.recompute_from_modified_history!
    end
  end
end
```

```julia
# GF(3)-balanced traversal
function balanced_traverse(M::PoincareLSpace, path::Vector{InformationVector})
    trits = map(path) do p
        c = complexity_at_point(M, p.embedding)
        c < LOW_THRESHOLD ? -1 :
        c > HIGH_THRESHOLD ? +1 : 0
    end
    
    @assert sum(trits) % 3 == 0 "GF(3) violation on path!"
    path
end
```

---

## Cross-Model Adjusted Novelty

### Formula: Text Novelty − Model Novelty

The key insight for L-Space navigation: **adjusted novelty** measures how surprising a token is *in this specific context* relative to its expected rarity across all models:

```
adjusted_novelty(token) = novelty_in_text(token) − mean_novelty_across_models(token)
                        = −log₂ P(token|this_text) − (−log₂ P(token|models))
```

| Adjusted Value | Interpretation | Manifold Position |
|----------------|----------------|-------------------|
| **Positive** | Token rarer here than models expect | BOUNDARY (contextually surprising) |
| **Zero** | Token matches model expectations | INTERIOR |
| **Negative** | Token common here but rare in models | CENTER (domain vocabulary) |

### Observed Results

From the L-Space conversation analysis (153 tokens):

**OCTAVO BOUNDARY (positive adjusted):**
```
+3.42  'the'    ← Common word appearing less than expected
+1.61  'of'     ← Structural words under-represented
+0.61  'as'     ← Context makes these surprising
```

**MANIFOLD CENTER (negative adjusted):**
```
-22.64  'gf3'          ← Domain term, rare globally, common HERE
-20.32  'narrativium'  ← Pratchett-specific, dominates this context
-20.32  'bumpus'       ← Author name, extremely rare globally
-19.32  'posets'       ← Category theory term
-17.00  'derivational' ← L-Space specific vocabulary
-16.00  'sheaves'      ← Mathematical structure
-16.00  'octavo'       ← The book that reads the reader
```

### Poincaré Radius from Adjusted Novelty

```julia
function poincare_radius_adjusted(adjusted::Float64)
    # Positive adjusted → boundary (r → 1)
    # Negative adjusted → center (r → 0)
    clamp(0.5 + adjusted / 30.0, 0.01, 0.99)
end
```

### Visualization

Interactive manifold at `/tmp/adjusted_novelty_manifold.html`:
- **GREEN points**: Domain vocabulary (center) — narrativium, bumpus, sheaves
- **RED points**: Contextually surprising (boundary) — common words appearing rarely
- **Hover**: Shows token, adjusted novelty, model novelty, text novelty, Poincaré radius

```python
# Generate adjusted novelty visualization
def adjusted_manifold(tokens, model_freqs):
    for token in tokens:
        model_nov = -log2(model_freqs.get(token, 1e-5))
        text_nov = -log2(token_freq[token] / total)
        adjusted = text_nov - model_nov
        radius = 0.5 + adjusted / 30.0
        yield {'token': token, 'adjusted': adjusted, 'radius': radius}
```

---

## Implementation: Concrete Tools for Causality Interference

### Token Novelty Sensing

| Tool | Install | Logprobs Access |
|------|---------|-----------------|
| **OpenAI API** | `pip install openai` | `logprobs=True, top_logprobs=5` |
| **vLLM** | `pip install vllm` | `SamplingParams(logprobs=5)` |
| **mlx-lm** | `pip install mlx-lm` | HTTP server with `logprobs=N` |
| **Ollama** | `brew install ollama` | `options={"logprobs": True}` |

```python
# Real-time novelty from OpenAI streaming
for chunk in client.chat.completions.create(
    model="gpt-4o", messages=msgs, logprobs=True, stream=True
):
    if chunk.choices[0].logprobs:
        for t in chunk.choices[0].logprobs.content:
            novelty = -t.logprob  # surprise in nats
            update_manifold_position(novelty)
```

### Hyperbolic Geometry

| Library | Install | Model |
|---------|---------|-------|
| **geoopt** | `pip install geoopt` | `PoincareBall()` with RiemannianAdam |
| **Manifolds.jl** | `Pkg.add("Manifolds")` | `Hyperbolic(n)` with exp/log maps |

```python
import geoopt
M = geoopt.PoincareBall()
position = geoopt.ManifoldParameter(torch.zeros(128), manifold=M)
# Distance to boundary = complexity
complexity = 1.0 / (1 - torch.dot(position, position))
```

### Entropy Measurement

```python
# Streaming Shannon entropy
class StreamingEntropy:
    def __init__(self):
        self.counts, self.total = Counter(), 0
    def update(self, token):
        self.counts[token] += 1; self.total += 1
        return -sum((c/self.total)*log2(c/self.total) for c in self.counts.values())

# Gzip as Kolmogorov proxy
def complexity(text): 
    return len(gzip.compress(text.encode())) / len(text.encode())
```

### Retroactive Modification (Causality Interference)

| Tool | Pattern | Use Case |
|------|---------|----------|
| **Automerge** | `changeAt(heads, fn)` | Fork history at past point |
| **XTDB** | `valid-time` retroactive put | Bitemporal event sourcing |
| **Git** | `filter-repo` | Rewrite derivational history |

```javascript
// Automerge: future modifies past (creates fork, doesn't destroy)
import { changeAt } from '@automerge/automerge'
const [newDoc, newHeads] = changeAt(doc, pastHeads, d => {
    d.derivation.unshift(futureKnowledge)  // prepend to history
})
// Original timeline preserved; new branch with retroactive knowledge
```

### Self-Modification (Gödel Machine Pattern)

From Darwin Gödel Machine (DGM):
```python
# LLM as semantic mutator for agent code
def evolve(agent, feedback):
    code = inspect.getsource(agent.solve)
    improved = llm(f"Improve this code based on: {feedback}\n{code}")
    exec(compile(improved, '<dgm>', 'exec'), agent.__dict__)
    return agent  # agent now runs improved code
```

### Integration Map

```
┌────────────────────────────────────────────────────────────────────┐
│                  CAUSALITY INTERFERENCE STACK                      │
├────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │ NOVELTY     │───►│ POSITION    │───►│ CAUSALITY   │            │
│  │ SENSOR      │    │ ON MANIFOLD │    │ MODE        │            │
│  │             │    │             │    │             │            │
│  │ OpenAI/vLLM │    │ geoopt      │    │ Automerge   │            │
│  │ logprobs    │    │ Poincaré    │    │ changeAt    │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│        │                  │                  │                     │
│        ▼                  ▼                  ▼                     │
│   surprise = -logprob   r = |position|    if r > 0.95:           │
│                         complexity = 1/(1-r²)  INTERFERE          │
└────────────────────────────────────────────────────────────────────┘
```

---

## References

- Pratchett, T. "Guards! Guards!" (1989) - First appearance of L-Space
- Pratchett, T. "The Science of Discworld" (1999) - Narrativium theory
- Bumpus et al. "Categories of Temporal Narratives" arXiv:2407.xxxxx
- Riehl-Shulman "A type theory for synthetic ∞-categories"

---

**Skill Name**: l-space  
**Type**: Narrative Navigation / Knowledge Coordination  
**Trit**: 0 (ERGODIC)  
**Color**: #8B4513 (Leather brown)  
**GF(3)**: Forms triads with sheaf/glass-bead, decomp/random-walk  
**Guardian**: The Librarian (Ook)

> "Knowledge = Power = Energy = Matter = Mass.
> A good bookshop is just a genteel Black Hole that knows how to read."
> — Terry Pratchett

Base directory for this skill: file:///Users/alice/.agents/skills/l-space



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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
