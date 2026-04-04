---
name: vector-awkward
description: Use when working in Python with scikit-hep vector and Awkward Array to build vector records, register behaviors, compute deltaR or invariant masses, combine or boost vectors, or access vector properties from ak.zip records of type (Momentum3D/Momentum4D/Vector4D). Vector is only useful if you are also using Awkward.
---

# Vector Awkward

## Overview

Create Awkward Arrays that behave like vector objects and use vector methods without writing custom kinematic math. Use these steps to register behaviors, build records with the right field names, and perform common HEP operations like deltaR and invariant mass.

## Quick Start

1. Register vector behaviors once per session:

```python
import vector
vector.register_awkward()
```

1. Build vector records with standard field names and a vector type name:

```python
import awkward as ak

events = ak.Array({
    "electron": ak.zip(
        {"pt": [50.0, 30.2], "eta": [1.4, -0.8], "phi": [2.1, 0.5], "mass": [0.0005, 0.0005]},
        with_name="Momentum4D",
    )
})
```

## Build Vector Records

- Use `ak.zip(..., with_name="Momentum3D")` for 3D operations like deltaR.
- Use `ak.zip(..., with_name="Momentum4D")` for 4D operations like invariant mass or boosts.
- Prefer standard names like `pt/eta/phi/mass` or `px/py/pz/E` so vector can infer coordinate systems.
- Call `vector.register_awkward()` before accessing vector properties or methods.

## Access Vector Properties

```python
particles = ak.zip({"px": px, "py": py, "pz": pz, "E": E}, with_name="Vector4D")
particles.pt
particles.phi
particles.eta
particles.mass
```

## Common Operations

Calculate deltaR between two collections:

```python
pairs = ak.cartesian([events.electron, events.muon])
electrons, muons = ak.unzip(pairs)
dR = electrons.deltaR(muons)
```

Combine 4-vectors and compute invariant mass:

```python
first_e, second_e = ak.unzip(ak.combinations(events.electron, 2))
inv_mass = (first_e + second_e).mass
```

Boost to a parent rest frame:

```python
parent = particle1 + particle2
particle1_rf = particle1.boostCM_of_p4(parent)
```

## Reference Material

Load `references/vector-hints.md` for more examples, method notes, and advanced snippets.
