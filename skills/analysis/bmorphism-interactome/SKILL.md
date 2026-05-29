---
name: bmorphism-interactome
description: GitHub interactome explorer for bmorphism/plurigrid ecosystem. Maps collaborations across AlgebraicJulia, Topos Institute, Anthropic, and MCP servers. Use for discovering cobordisms between research communities.
version: 1.0.0
---


# bmorphism-interactome Skill

> *Mapping the cobordisms between research communities via shared contributors*

## Profile: bmorphism (Barton Rhodes)

```
@bmorphism | 255 followers | 1.6k following
@plurigrid founder | San Francisco
"Parametrised optics model cybernetic systems"
```

## Core Repositories

| Repo | Stars | Description | Trit |
|------|-------|-------------|------|
| [Gay.jl](https://github.com/bmorphism/Gay.jl) | 3 | Wide-gamut color sampling + SPI | 0 |
| [agent-o-shiva](https://github.com/bmorphism/agent-o-shiva) | - | Rama agent platform fork | 0 |
| [GeoACSets.jl](https://github.com/bmorphism/GeoACSets.jl) | - | Categorical GIS | 0 |
| [bafishka](https://github.com/bmorphism/bafishka) | 1 | Fish + Steel Clojure | -1 |
| [ocaml-mcp-sdk](https://github.com/bmorphism/ocaml-mcp-sdk) | 60 | OCaml MCP SDK | -1 |
| [babashka-mcp-server](https://github.com/bmorphism/babashka-mcp-server) | 16 | Babashka MCP | -1 |
| [multiverse-color-game](https://github.com/bmorphism/multiverse-color-game) | - | VisionPro holographic | +1 |

## Plurigrid Organization (542 repos)

```
plurigrid: "building for a more agentic mesoscale 🦆"
├── asi/                    # "everything is topological chemputer!"
├── UnwiringDiagrams.jl     # Worlding/Unworlding Uexküll
├── vcg-auction/            # VCG auctions in Rust
├── microworlds/            # Agent simulations
├── risc0-cosmwasm/         # zkVM + CosmWasm
└── skillz/                 # Anthropic skills fork
```

## Interactome Clusters

### Cluster 1: Topos Institute ↔ AlgebraicJulia

**Bridge Authors:**
- `olynch` - poly, Catlab.jl, ACSets.jl
- `epatters` - Catlab lead, Topos
- `kasbah` - Senior engineer @ Topos

**Cobordism:**
```
plurigrid/UnwiringDiagrams.jl ←fork← AlgebraicJulia/WiringDiagrams.jl
           ↓                                    ↓
    "Umwelt Worlding"                   Compositional Systems
           ↓                                    ↓
      Gay.jl SPI ←───────────────────→ ToposInstitute/poly
```

### Cluster 2: Anthropic Engineers

bmorphism follows:
- `klazuka` (Keith Lazuka)
- `simonster` (Simon Kornblith)  
- `domdomegg` (adam jones)
- `ericharmeling`

### Cluster 3: Julia Scientific

- `ViralBShah` - Julia co-creator, JuliaHub CEO
- `EnzymeAD` - Automatic differentiation
- `gdalle` - SparseMatrixColorings.jl
- `andyferris` - ElaraAI

### Cluster 4: Emacs/Clojure

- `fogus` - Cognitect/Nubank
- `Chouser` - Clojure core
- `tvraman` - Emacspeak
- `ept` (Martin Kleppmann) - DDIA author, CRDTs

### Cluster 5: Applied Category Theory

- `jules-hedges` - Open games, parametrised optics
- `statebox` - awesome-applied-ct
- `AlgebraicJulia` - Catlab ecosystem

## Commands

```bash
# Explore following list
gh api users/bmorphism/following --paginate --jq '.[].login'

# Get repo details
gh api repos/bmorphism/Gay.jl --jq '{stars: .stargazers_count, desc: .description}'

# Find shared contributors
gh api repos/AlgebraicJulia/Catlab.jl/contributors --jq '.[].login' > catlab_contribs.txt
gh api repos/ToposInstitute/poly/contributors --jq '.[].login' > poly_contribs.txt
comm -12 <(sort catlab_contribs.txt) <(sort poly_contribs.txt)

# Plurigrid repos by language
gh api orgs/plurigrid/repos --paginate --jq '.[] | select(.language == "Julia") | .name'
```

## GF(3) Classification

| Trit | Role | Repos |
|------|------|-------|
| -1 (MINUS) | Infrastructure | MCP servers, bafishka, CategoricalTowers |
| 0 (ERGODIC) | Bridges | Gay.jl, GeoACSets, agent-o-shiva |
| +1 (PLUS) | Applications | multiverse-color-game, gay-hy, xf.jl |

## Key Insights

1. **Parametrised Optics** - bmorphism's bio references jules-hedges' work on cybernetic systems
2. **Topological Chemputer** - plurigrid/asi connects Cronin's chemputer to categorical systems
3. **UnwiringDiagrams** - Fork of AlgebraicJulia for "Uexküll Umweltung" (environment-world)
4. **MCP Constellation** - Multiple MCP servers forming distributed tool network

## Related Skills

- `gh-interactome` - General GitHub network discovery
- `bmorphism-stars` - 2155 starred repos index
- `gay-julia` - Gay.jl color integration
- `topos-catcolab` - CatColab collaboration
- `acsets-algebraic-databases` - ACSets patterns



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule

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