---
name: gh-interactome
description: GitHub author interaction network discovery. Maps cobordisms between
version: 1.0.0
---

# gh-interactome - GitHub Author Interaction Network

## Overview

Maps the **interactome** (interaction network) of GitHub contributors across discovered repos. Finds **cobordisms** - shared boundaries where different research communities meet.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTERACTOME STRUCTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   BlockScience ◄────── olynch ──────► ToposInstitute                        │
│        │                  │                  │                               │
│        ▼                  ▼                  ▼                               │
│     cadCAD         AlgebraicJulia        poly                               │
│        │                  │                  │                               │
│        └──── jpfairbanks ─┴── epatters ─────┘                               │
│                                                                              │
│   HoTT/Coq-HoTT ◄─── abooij ───► mortberg/cubicaltt                         │
│        │                                     │                               │
│        └────── mikeshulman ──────────────────┘                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Discovered Cobordisms

### Cobordism 1: AlgebraicJulia ↔ Topos Institute ↔ BlockScience

**Shared contributors:**
- `epatters` (Evan Patterson) - Catlab.jl, ACSets.jl, Topos Institute
- `olynch` (Owen Lynch) - poly, ACSets.jl, Catlab.jl, Topos Institute
- `jpfairbanks` (James Fairbanks) - Catlab.jl, ACSets.jl, U Florida
- `kris-brown` - Catlab.jl, ACSets.jl, Topos Institute
- `slibkind` (Sophie Libkind) - Catlab.jl, Stanford/Topos

**Bridge repos:**
| Repo | Stars | Role |
|------|-------|------|
| AlgebraicJulia/Catlab.jl | 681 | Applied category theory framework |
| AlgebraicJulia/ACSets.jl | 25 | Algebraic databases |
| AlgebraicJulia/AlgebraicPetri.jl | - | Compositional Petri nets |
| ToposInstitute/poly | 113 | Polynomial functors |

---

### Cobordism 2: HoTT ↔ Cubical Type Theory

**Shared contributors:**
- `abooij` - HoTT/Coq-HoTT, mortberg/cubicaltt
- `mikeshulman` (Mike Shulman) - HoTT, real cohesion
- `andrejbauer` (Andrej Bauer) - HoTT, constructive math
- `DanGrayson` - HoTT, cubicaltt, Agda

**Bridge insight:** HoTT contributors often work on multiple proof assistants.

---

### Cobordism 3: DisCoPy ↔ Oxford Quantum Group

**Key contributors:**
- `toumix` (1213 commits) - DisCoPy core
- `giodefelice` (354 commits) - DisCoPy
- `y-richie-y` (173 commits) - DisCoPy
- `oxford-quantum-group` - Organizational account

**Bridge insight:** QNLP (Quantum NLP) research connects quantum computing to linguistics via categorical semantics.

---

### Cobordism 4: GFlowNets ↔ Mila (Bengio's Lab)

**Key contributors:**
- `zdhNarsil` (94 commits) - Awesome-GFlowNets curator
- `bengioe` (Emmanuel Bengio) - GFlowNet contributor
- Connection to Yoshua Bengio's lab at Mila

**Bridge insight:** GFlowNets for molecular design connects to chemistry/synthesis domains.

---

## Author Profiles

### Core AlgebraicJulia

| Author | Repos | Affiliation |
|--------|-------|-------------|
| `epatters` | Catlab.jl (2304), ACSets.jl (101) | Topos Institute |
| `olynch` | poly (1), Catlab.jl (138), ACSets.jl (92) | Topos Institute |
| `jpfairbanks` | Catlab.jl (79), ACSets.jl (19) | U Florida |
| `kris-brown` | Catlab.jl (63) | Topos Institute |

### Core HoTT

| Author | Repos | Affiliation |
|--------|-------|-------------|
| `Alizter` | Coq-HoTT (2191) | - |
| `jdchristensen` | Coq-HoTT (1175) | UWO |
| `JasonGross` | Coq-HoTT (930) | MIT |
| `mikeshulman` | Coq-HoTT (888) | - |
| `andrejbauer` | Coq-HoTT (396) | Ljubljana |

### Core BlockScience

| Author | Repos | Affiliation |
|--------|-------|-------------|
| `JEJodesty` | cadCAD (731), cats (107) | BlockScience |
| `mzargham` | cadCAD (3) | BlockScience founder |
| `markusbkoch` | cadCAD (74) | - |
| `danlessa` | cadCAD (37) | - |

### Core DisCoPy

| Author | Repos | Affiliation |
|--------|-------|-------------|
| `toumix` | discopy (1213) | Oxford |
| `giodefelice` | discopy (354) | - |
| `y-richie-y` | discopy (173) | - |

### Key Bridge Authors

| Author | Connects | Via |
|--------|----------|-----|
| `olynch` | Topos ↔ AlgebraicJulia | poly, Catlab, ACSets |
| `abooij` | HoTT ↔ Cubical | Coq-HoTT, cubicaltt |
| `dspivak` | Topos ↔ Poly | poly (186 commits) |

---

## Network Metrics

### Centrality (Bridge Authors)

```python
# Authors who connect multiple communities
BRIDGE_AUTHORS = {
    "olynch": ["ToposInstitute/poly", "AlgebraicJulia/Catlab.jl", "AlgebraicJulia/ACSets.jl"],
    "epatters": ["AlgebraicJulia/Catlab.jl", "AlgebraicJulia/ACSets.jl", "ToposInstitute/*"],
    "abooij": ["HoTT/Coq-HoTT", "mortberg/cubicaltt"],
    "jpfairbanks": ["AlgebraicJulia/Catlab.jl", "AlgebraicJulia/ACSets.jl"],
    "mikeshulman": ["HoTT/Coq-HoTT", "HoTT/book"],
}
```

### Community Clusters

```
Cluster 1: Applied Category Theory
  - AlgebraicJulia (epatters, olynch, jpfairbanks, kris-brown)
  - Topos Institute (dspivak, olynch, epatters)
  - DisCoPy (toumix, giodefelice)

Cluster 2: Type Theory / Foundations
  - HoTT (Alizter, jdchristensen, mikeshulman)
  - Cubical (mortberg, simhu, coquand)
  - Rzk (fizruk)

Cluster 3: Complex Systems / Token Engineering
  - BlockScience (mzargham, JEJodesty)
  - cadCAD ecosystem

Cluster 4: Haskell Categorical
  - connections (cmk)
  - lattices (phadej)
  - haskerwaul (sellout)
```

---

## Implementation

```python
#!/usr/bin/env python3
"""
GitHub Interactome: Map author interactions across repos.
"""
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "networkx"]
# ///

import subprocess
import json
from collections import defaultdict

def get_contributors(repo: str) -> list[dict]:
    """Get contributors for a repo via gh CLI."""
    cmd = f"gh api repos/{repo}/contributors --jq '.[] | {{login, contributions}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    contributors = []
    for line in result.stdout.strip().split('\n'):
        if line:
            contributors.append(json.loads(line))
    return contributors

def build_interactome(repos: list[str]) -> dict:
    """Build author-repo bipartite graph."""
    author_repos = defaultdict(list)
    repo_authors = defaultdict(list)
    
    for repo in repos:
        contributors = get_contributors(repo)
        for c in contributors:
            author = c['login']
            author_repos[author].append({
                'repo': repo,
                'contributions': c['contributions']
            })
            repo_authors[repo].append(author)
    
    return {
        'author_repos': dict(author_repos),
        'repo_authors': dict(repo_authors),
    }

def find_bridges(interactome: dict, min_repos: int = 2) -> list[dict]:
    """Find authors who contribute to multiple repos (bridges)."""
    bridges = []
    for author, repos in interactome['author_repos'].items():
        if len(repos) >= min_repos:
            bridges.append({
                'author': author,
                'repos': [r['repo'] for r in repos],
                'total_contributions': sum(r['contributions'] for r in repos),
            })
    return sorted(bridges, key=lambda x: len(x['repos']), reverse=True)

def find_cobordisms(interactome: dict) -> list[dict]:
    """Find shared boundaries between repo communities."""
    cobordisms = []
    repos = list(interactome['repo_authors'].keys())
    
    for i, repo_a in enumerate(repos):
        for repo_b in repos[i+1:]:
            shared = set(interactome['repo_authors'][repo_a]) & \
                     set(interactome['repo_authors'][repo_b])
            if shared:
                cobordisms.append({
                    'repos': (repo_a, repo_b),
                    'shared_authors': list(shared),
                    'strength': len(shared),
                })
    
    return sorted(cobordisms, key=lambda x: x['strength'], reverse=True)
```

---

## Justfile Recipes

```just
# Build interactome
gh-interactome-build:
    @echo "🕸️ Building GitHub Interactome..."
    python3 interactome.py build

# Find bridge authors
gh-interactome-bridges:
    @echo "🌉 Finding bridge authors..."
    python3 interactome.py bridges

# Find cobordisms
gh-interactome-cobordisms:
    @echo "🔗 Finding cobordisms..."
    python3 interactome.py cobordisms

# Author lookup
gh-interactome-author login:
    @echo "👤 Author: {{login}}"
    gh api users/{{login}} --jq '{name, company, blog, bio}'
    gh api users/{{login}}/repos --jq '.[].name' | head -10
```

---

## Key Cobordism: AlgebraicJulia → BlockScience

The **compositional systems** approach connects:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPOSITIONAL SYSTEMS COBORDISM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   UC Riverside ──── John Baez ────► AlgebraicJulia ◄─── Topos Institute     │
│       │                │                   │                  │              │
│       │                ▼                   ▼                  ▼              │
│       │         Stock & Flow        Catlab.jl, ACSets      poly            │
│       │         Diagrams                   │               (Spivak)         │
│       │                │                   │                  │              │
│       └────────────────┼───────────────────┼──────────────────┘              │
│                        │                   │                                 │
│                        ▼                   ▼                                 │
│                 Compositional      AlgebraicPetri.jl                        │
│                   Epidemiology     AlgebraicDynamics.jl                     │
│                        │                   │                                 │
│                        └─────────┬─────────┘                                │
│                                  │                                          │
│                                  ▼                                          │
│                           BlockScience                                      │
│                           (cadCAD, Token Engineering)                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Papers Bridging Communities

1. **"Compositional Scientific Computing with Catlab and SemanticModels"** (2020)
   - Halter, Patterson, Baas, Fairbanks
   - ArXiv: 2005.04831

2. **"Compositional Modeling with Stock and Flow Diagrams"** (2022)
   - Baez, Li, Libkind, Osgood
   - ArXiv: 2205.08373 (COVID epidemiology application)

3. **"AlgebraicRL.jl: Compositional Reinforcement Learning"**
   - Uses Catlab.jl for MDP composition

### Shared Methodology

| Concept | AlgebraicJulia | BlockScience |
|---------|---------------|--------------|
| **Compositionality** | Operad algebras | cadCAD nested configs |
| **Open systems** | Undirected wiring diagrams | State variables + policies |
| **Semantics** | Functors to dynamical systems | Simulation runs |
| **Visualization** | String diagrams | System dynamics diagrams |

### Bridge Authors

| Author | AlgebraicJulia | BlockScience | Academic |
|--------|---------------|--------------|----------|
| John Baez | Advisor/papers | - | UC Riverside |
| Sophie Libkind | AlgebraicDynamics | - | Stanford/Topos |
| James Fairbanks | Catlab core | - | U Florida |
| Evan Patterson | Catlab lead | - | Topos |
| Michael Zargham | - | cadCAD lead | BlockScience |

**Conceptual Bridge**: Both communities use category theory for compositional modeling of complex systems - AlgebraicJulia in scientific computing, BlockScience in cryptoeconomics/token engineering.

---

## See Also

- `gh-skill-explorer` - Discovery skill that feeds into this
- `galois-connections` - Adjunctions between domains
- `acsets-algebraic-databases` - ACSets patterns
- `discopy` - String diagrams

---

## End-of-Skill Interface

## r2con Speaker Resources

Target organizations for interactome mapping:

| Speaker | Handle | Organization | Interactome Target |
|---------|--------|--------------|-------------------|
| pancake | trufae | [radareorg](https://github.com/radareorg) | Core r2 ecosystem (75+ repos) |
| thestr4ng3r | thestr4ng3r | [rizinorg](https://github.com/rizinorg) | Rizin/Cutter fork community |
| oleavr | oleavr | [frida](https://github.com/frida) | Dynamic instrumentation ecosystem |
| xvilka | XVilka | [radareorg](https://github.com/radareorg) | UEFI, radeco, decompilation |
| cryptax | cryptax | [rednaga](https://github.com/rednaga) | Android security tooling |

## Commands

```bash
# Build interactome for discovered repos
just gh-interactome build

# Find bridge authors
just gh-interactome bridges

# Find cobordisms between communities
just gh-interactome cobordisms

# Show author profile
just gh-interactome author olynch

# Visualize network
just gh-interactome viz

# NEW: Map r2con speaker orgs
just gh-interactome orgs radareorg rizinorg frida
```

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
gh-interactome (−) + SDF.Ch3 (○) + [balancer] (+) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch6: Layering
- Ch1: Flexibility through Abstraction

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
