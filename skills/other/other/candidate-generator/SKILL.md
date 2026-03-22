---
name: candidate-generator
description: Generate inorganic crystal structure candidates for computational materials discovery workflows. Use this skill whenever the user wants to build, explore, or diversify a pool of inorganic structures for DFT screening, high-throughput calculations, machine learning dataset construction, or property-guided search. This skill covers the full candidate generation pipeline - seed structure creation -> chemical space exploration -> configurational ordering -> defect generation -> ensemble augmentation.
---

# Inorganic Candidate Generation

This skill guides the systematic generation of inorganic crystal structure candidates using
a suite of seven pymatgen-based tools. The methodology is:
**prototype → explore chemistry → resolve disorder → add defects → augment**,
selecting the appropriate branch(es) for the discovery goal.

The core philosophy: candidate generation is a funnel. Start broad (many chemistries,
many configurations), then narrow using physical filters (charge neutrality, Ewald energy,
thermodynamic stability from MP). Always track structures in the ASE database using
`ase_store_result` so nothing is recomputed.

---

## Tool Catalogue

### 1. `pymatgen_prototype_builder` — Seed Structure
Builds an ideal crystal from a spacegroup number/symbol, species list, and lattice parameters.
This is the **entry point** for any workflow that starts from scratch rather than an existing structure.

**Key parameters:**
- `spacegroup`: int (1–230) or Hermann-Mauguin symbol, e.g. `225` or `"Fm-3m"`
- `species`: list of element symbols (`['La', 'Mn', 'O', 'O', 'O']`) or Wyckoff dict
- `lattice_parameters`: `[a, b, c, alpha, beta, gamma]` in Å and degrees; `[a]` works for cubic
- `wyckoff_positions`: optional dict mapping Wyckoff labels to species/coords
- `output_format`: `'dict'` (default, pass to other tools), `'poscar'`, `'cif'`, `'ase'`

**Returns:** `structures[i].structure` — pass directly to substitution, enumeration, or defect tools.

**`wyckoff_positions` proximity gotcha:** Passing a Wyckoff dict (e.g. `{'1a': 'Ba', '1b': 'Ti', '3c': 'O'}`) can raise
"sites less than 0.01 Å apart" for multi-species prototypes where pymatgen auto-generates
overlapping fractional coords. **Preferred approach:** supply explicit `species` and `coords` lists
instead, and use `validate_proximity=False` when debugging a new prototype before finalising
lattice parameters.

---

### 2. `pymatgen_substitution_generator` — Chemical Space Exploration
Replaces elements in existing structures. Best for isostructural analogue screening across
a fixed lattice topology when **charge balance is not strictly required**.

**Key parameters:**
- `substitutions`: `{'Li': 'Na'}` (full swap), `{'Li': ['Na', 'K']}` (one variant per replacement),
  `{'Li': {'replace_with': 'Na', 'fraction': 0.5}}` (50 % doping)
- `n_structures`: variants to generate **per substitution combination** (default 5).
  For deterministic full swaps (`fraction=1.0`) set this to **1** — higher values only
  produce identical duplicates. Total output = `n_structures × num_combinations`,
  capped by `max_attempts`.
- `max_attempts`: **hard cap on total output count** (default 50). If you supply N
  substitution options with n_structures=k, set `max_attempts ≥ N × k` or outputs
  will be silently truncated. Example: 8 B-site metals with n_structures=1 needs
  `max_attempts=8` (or higher); with n_structures=3 needs `max_attempts=24`.
- `enforce_charge_neutrality`: set `True` for ionic materials
- `site_selector`: `'all'`, `'wyckoff_4a'`, `'coordination_6'`, etc.

**When to use over `ion_exchange_generator`:** when you want exploratory doping without
strict stoichiometry adjustment and charge neutrality is handled manually or checked post-hoc.

---

### 3. `pymatgen_ion_exchange_generator` — Charge-Neutral Substitution
Replaces a mobile ion (e.g. Li⁺) with one or more ions, **automatically adjusting stoichiometry**
so that total ionic charge is conserved. Only charge-neutral structures are returned by default.

**Key parameters:**
- `replace_ion`: element to replace, e.g. `'Li'`
- `with_ions`: `['Na', 'K']` (equal weight) or `{'Na': 0.6, 'Mg': 0.4}` (weighted split)
- `exchange_fraction`: fraction of sites to exchange (0–1), default `1.0`
- `allow_oxidation_state_change`: `False` (default) = only neutral structures returned
- `max_structures`: cap on returned structures per input (default 10)

**Prototypical use cases:** Li → Na/K battery cathode analogues, Ca²⁺ → La³⁺ doping in oxides.

---

### 4. `pymatgen_enumeration_generator` — Exhaustive Ordering of Disordered Structures
Takes structures with **fractional site occupancies** and returns all symmetry-inequivalent
ordered supercell approximants up to a cell-size limit, ranked by Ewald energy or cell size.

**Key parameters:**
- `min_cell_size` / `max_cell_size`: supercell multiplier range (1–8); keep `max_cell_size ≤ 4`
  for binaries, `≤ 2` for ternaries to avoid combinatorial explosion
- `n_structures`: max ordered structures returned per input (default 20, max 500)
- `sort_by`: `'ewald'` (default, lowest energy first), `'num_sites'`, `'random'`
- `add_oxidation_states`: auto-assign oxidation states for Ewald ranking (default `True`)
- `refine_structure`: re-symmetrize before enumeration (recommended, default `True`)

**Requires:** `enumlib` on PATH — install with `pip install enumlib` or `conda install -c conda-forge enumlib`.

**When to use over `sqs_generator`:** when you need the complete ordered-configuration pool,
want to identify the ground-state ordering, or are building a cluster expansion training set.

---

### 5. `pymatgen_sqs_generator` — Special Quasirandom Structures
Finds a small ordered supercell whose Warren-Cowley pair correlations best mimic a
perfectly random alloy. Returns the **single best quasirandom approximant** per input,
not the full ordered-configuration space.

**Key parameters:**
- `supercell_size`: target formula units in SQS cell (default 8; use 8–16 for binary, 12–24 for ternary)
- `supercell_matrix`: explicit `[nx, ny, nz]` or 3×3 matrix (overrides `supercell_size`)
- `n_structures`: independent SQS candidates per input (default 3); ranked by `sqs_error`
- `n_mc_steps`: Monte Carlo steps per candidate (default 50 000; increase for multicomponent)
- `n_shells`: correlation shells in objective function (default 4)
- `seed`: set for reproducibility
- `use_mcsqs`: use ATAT `mcsqs` binary if available (better quality for large systems)

**When to use over `enumeration_generator`:** target system is a solid solution / high-entropy
material where disorder is the physical state being modelled, not a defect to be minimised.

---

### 6. `pymatgen_defect_generator` — Point Defect Supercells
Takes a **perfect bulk host structure** and generates one supercell per symmetry-inequivalent
defect site. Supports vacancies, substitutional dopants, and interstitials.

**Key parameters:**
- `vacancy_species`: `['Li', 'O']` — generate V_Li, V_O defects
- `substitution_species`: `{'Fe': ['Mn', 'Co']}` — Mn_Fe and Co_Fe substitutionals
- `interstitial_species`: `['Li']` — find void sites and insert Li
- `charge_states`: `{'V_Li': [-1, 0, 1]}` — metadata only; structures are always neutral geometry
- `supercell_min_atoms`: target atoms in defect supercell (default 64; 64–128 for plane-wave DFT)
- `inequivalent_only`: `True` (default) — generate only symmetry-distinct defects

**Downstream:** feed outputs to `pymatgen_perturbation_generator` to rattle defect geometries,
or save directly to the ASE database via `ase_store_result`.

---

### 7. `pymatgen_perturbation_generator` — Structural Ensemble / Augmentation
Applies random atomic displacements ("rattling") and/or lattice strain to create ensembles
of perturbed structures. Does **not** change composition.

**Key parameters:**
- `displacement_max`: max displacement per atom in Å (default 0.1; typical range 0.05–0.2)
- `strain_percent`: `None` (off), scalar (uniform), `[min, max]` (random range), or
  6-element Voigt tensor `[e_xx, e_yy, e_zz, e_xy, e_xz, e_yz]`
- `n_structures`: perturbed copies per input (default 10, max 200)
- `seed`: for reproducibility

**Primary uses:**
- Provide DFT starting geometries that are not stuck at a symmetry saddle point
- Augment ML training datasets with off-equilibrium configurations
- Generate strained cells for elastic property screening

---

## Workflow Phases

### Phase 1: Seed Structure

Start here if no structure exists yet.

```
pymatgen_prototype_builder(
    spacegroup=225,           # Fm-3m (rock-salt)
    species=['Li', 'O'],
    lattice_parameters=[4.33] # cubic: [a]
)
```

If a known structure already exists (from `mp_get_material_properties`, a CIF file, or the
ASE database), skip this step and pass that structure directly.

**Common prototypes:**

| Prototype | SG # | Symbol | Example |
|-----------|------|--------|---------|
| Rock-salt | 225 | Fm-3m | NaCl, LiF, MgO |
| Perovskite | 221 | Pm-3m | BaTiO₃, SrTiO₃ |
| Spinel | 227 | Fd-3m | MgAl₂O₄, LiMn₂O₄ |
| Layered oxide (α-NaFeO₂) | 166 | R-3m | LiCoO₂, LiNiO₂ |
| Olivine | 62 | Pnma | LiFePO₄, LiMnPO₄ |
| Rutile | 136 | P4₂/mnm | TiO₂, SnO₂ |
| Wurtzite | 186 | P6₃mc | ZnO, GaN |
| Fluorite | 225 | Fm-3m | CaF₂, CeO₂ |

---

### Phase 2: Chemical Space Exploration

Choose the branch based on whether charge-neutrality must be enforced:

**Branch A — Exploratory (charge balance not enforced):**
```
pymatgen_substitution_generator(
    input_structures=seed_structure,
    substitutions={'Li': ['Na', 'K', 'Rb'], 'Fe': ['Mn', 'Co', 'Ni']},
    n_structures=10,
    enforce_charge_neutrality=False
)
```
Use when: screening isostructural analogues, building diverse training sets.

**Branch B — Charge-neutral (ionic materials):**
```
pymatgen_ion_exchange_generator(
    input_structures=seed_structure,
    replace_ion='Li',
    with_ions={'Na': 0.5, 'Mg': 0.5},
    exchange_fraction=1.0,
    max_structures=20
)
```
Use when: battery cathode analogues, any case where the oxidation-state bookkeeping must be exact.

Both branches accept lists of input structures — pipe multiple seeds through in one call.

---

### Phase 3: Resolve Disorder (if structures have partial occupancies)

If Phase 2 produced or if you started from a disordered structure:

**Ground-state search (small cells, complete enumeration):**
```
pymatgen_enumeration_generator(
    input_structures=disordered_structs,
    max_cell_size=4,
    n_structures=50,
    sort_by='ewald'
)
```

**Solid-solution modelling (large / high-entropy systems):**
```
pymatgen_sqs_generator(
    input_structures=disordered_struct,
    supercell_size=16,
    n_structures=5,
    n_mc_steps=200000,
    seed=42
)
```

Decision rule:
- **Enumeration** when you need all low-energy orderings or a CE training set.
- **SQS** when disorder is the target state (e.g. (Li,Na)₀.₅CoO₂ solid solution).
- For high-entropy systems (≥ 4 mixing species), prefer SQS; enumeration becomes
  intractable above `max_cell_size=2`.

---

### Phase 4: Defect Generation (optional branch)

Fork off from any ordered structure to study point defects:

```
pymatgen_defect_generator(
    input_structure=ordered_structure,
    vacancy_species=['Li'],
    substitution_species={'Fe': ['Mn', 'Co']},
    interstitial_species=['Li'],
    charge_states={'V_Li': [-1, 0, 1]},
    supercell_min_atoms=128
)
```

**Important:** Pass only a single, ordered, defect-free host structure. The tool generates
one supercell per inequivalent defect site automatically — do not pre-expand the cell.

---

### Phase 5: Perturbation / Augmentation

Apply to any structure from Phases 1–4 to:
- Break symmetry before DFT relaxation (avoid false saddle-point convergence)
- Augment ML training datasets
- Probe elastic and thermal response

```
pymatgen_perturbation_generator(
    input_structures=ordered_or_defect_structures,
    displacement_max=0.1,
    strain_percent=[-2.0, 2.0],
    n_structures=20,
    seed=0
)
```

For defect geometries, use `displacement_max=0.05–0.1` Å (subtle rattling). For
ML data augmentation, `0.1–0.2` Å with random strain is typical.

---

## Connecting to the Rest of the Workflow

### Saving to the ASE Database

Always store generated structures so they can be queried later without regeneration:

```
ase_store_result(
    db_path='candidates.db',
    atoms_dict=structure['structure'],   # MUST use output_format='ase' — see note below
    key_value_pairs={
        'generator': 'substitution',
        'compound': structure['formula'],   # NOT 'formula' — see reserved keys below
        'campaign': 'cathode_screen_2026',
        'source_structure': 'LiCoO2_mp-24850'
    }
)
```

**`output_format` must be `'ase'` when feeding into `ase_store_result`:**
`ase_store_result` requires ASE-native keys (`numbers`, `positions`, `cell`, `pbc`), which
are only produced when the upstream pymatgen tool is called with `output_format='ase'`.
Using the default `output_format='dict'` produces a pymatgen `Structure.as_dict()` object
(with `@module`, `@class`, `sites`, `lattice`, etc.) that will be rejected with:
`"atoms_dict missing required keys: ['numbers']"`.
Always set `output_format='ase'` on any pymatgen tool whose result goes directly to `ase_store_result`.

**ASE reserved key names — never use these in `key_value_pairs`:**
ASE's `db.write()` will raise `ValueError: Bad key` for any of the following built-in column
names: `id`, `unique_id`, `ctime`, `mtime`, `user`, `calculator`, `energy`, `forces`,
`stress`, `magmoms`, `charges`, `cell`, `pbc`, `natoms`, `formula`, `mass`, `volume`,
`spacegroup`. Use unambiguous alternatives e.g. `compound` instead of `formula`,
`sg_num` instead of `spacegroup`, `uid` instead of `unique_id`.

Query existing candidates before generating new ones to avoid duplication:
```
ase_query_db(db_path='candidates.db', property_filters={'campaign': 'cathode_screen_2026'})
```

### Filtering with Materials Project

After chemical space exploration, cross-check compositions against the MP convex hull
before running expensive DFT:

```
mp_search_materials(
    formula='NaCoO2',
    is_stable=True
)
```

Discard compositions that are far above the hull (energy_above_hull > 0.1 eV/atom)
unless the target is metastable phases.

### Output Format Routing

| Downstream tool | Recommended `output_format` |
|---|---|
| Another pymatgen tool | `'dict'` (default) |
| VASP / CP2K / Quantum ESPRESSO | `'poscar'` or `'cif'` |
| ASE database (`ase_store_result`) | `'ase'` |
| CIF archive / visualisation | `'cif'` |

---

## Common Patterns

### Isostructural Analogue Screen

```
# 1. Build rock-salt seed
seed = pymatgen_prototype_builder(spacegroup=225, species=['Li','O'], lattice_parameters=[4.33])

# 2. Swap Li site: Li → Na, K, Rb; O site: O → S, Se
variants = pymatgen_substitution_generator(
    input_structures=seed['structures'][0]['structure'],
    substitutions={'Li': ['Na', 'K', 'Rb'], 'O': ['S', 'Se', 'O']},
    n_structures=15
)

# 3. Filter by MP stability and store survivors
for s in variants['structures']:
    mp_results = mp_search_materials(formula=s['formula'])
    if mp_results['count'] > 0:
        ase_store_result(db_path='screen.db', atoms_dict=s['structure'],
                         key_value_pairs={'formula': s['formula'], 'campaign': 'rocksalt_screen'})
```

### Li → Na Battery Analogue

```
licoo2 = mp_get_material_properties('mp-24850')  # LiCoO2
struct_dict = licoo2['properties'][0]['structure']

exchanged = pymatgen_ion_exchange_generator(
    input_structures=struct_dict,
    replace_ion='Li',
    with_ions=['Na'],
    exchange_fraction=1.0,
    max_structures=5
)
```

### High-Entropy Oxide SQS

```
# Build a rocksalt with 5-component mixing on the cation sublattice
# Input: disordered structure with occupancies {Mg:0.2, Co:0.2, Ni:0.2, Cu:0.2, Zn:0.2}
sqs = pymatgen_sqs_generator(
    input_structures=disordered_cif,
    supercell_size=20,
    n_structures=5,
    n_mc_steps=500000,
    seed=7
)
# Best SQS is sqs['structures'][0] (sorted by sqs_error)
```

### Ground-State Ordering Search

```
# Li₀.₅CoO₂ starting from partially delithiated structure with site occupancies
ordered_candidates = pymatgen_enumeration_generator(
    input_structures=disordered_struct,
    max_cell_size=4,
    n_structures=100,
    sort_by='ewald'
)
# Top 10 by Ewald energy are the most plausible ground-state orderings
top10 = ordered_candidates['structures'][:10]
```

### Defect-Engineered Cathode

```
# Start from a relaxed ordered LiMnO2 structure
defect_cells = pymatgen_defect_generator(
    input_structure=limno2_dict,
    vacancy_species=['Li'],
    substitution_species={'Mn': ['Fe', 'Ni', 'Co']},
    supercell_min_atoms=96
)

# Rattle each defect cell before DFT relaxation
for dc in defect_cells['structures']:
    perturbed = pymatgen_perturbation_generator(
        input_structures=dc,
        displacement_max=0.08,
        n_structures=3,
        seed=1
    )
    for p in perturbed['structures']:
        ase_store_result(db_path='defects.db', atoms_dict=p,
                         key_value_pairs={'defect_label': dc['metadata']['defect_label']})
```

---

## Decision Guide

```
Need a new structure from scratch?
  └─► pymatgen_prototype_builder

Have an existing structure, want new chemistries?
  ├─ Charge balance is critical (ionic material)?
  │     └─► pymatgen_ion_exchange_generator
  └─ Exploratory / charge balance not enforced?
        └─► pymatgen_substitution_generator

Structure has partial occupancies / is disordered?
  ├─ Want ALL orderings / ground-state search / CE training?
  │     └─► pymatgen_enumeration_generator  (max_cell_size ≤ 4 for binaries)
  └─ Modelling disorder itself (solid solution / high-entropy)?
        └─► pymatgen_sqs_generator

Need point defect supercells?
  └─► pymatgen_defect_generator

Need an ensemble / perturbed copies of any structure?
  └─► pymatgen_perturbation_generator
```

---

## Pitfalls and Gotchas

**`enumeration_generator` hangs or never returns**
Cause: `max_cell_size` too large for the number of mixing species. Combinatorial explosion.
Fix: reduce `max_cell_size` to 2–3, or switch to `sqs_generator` for multicomponent systems.

**`enumeration_generator` fails on Windows**
Cause: The tool requires the `enum.x` (enumlib) binary on PATH. enumlib is not available
natively on Windows — it can only be installed inside WSL.
Fix: On Windows, fall back to `sqs_generator` (no binary dependency; uses a built-in MC
backend). If ground-state enumeration is essential, run via WSL:
`wsl conda install -c conda-forge enumlib` then add the WSL binary path to the Windows PATH.

**Never bypass MCP tools by calling pymatgen directly in scripts**
Cause: Writing script code that calls pymatgen transformation classes (e.g.
`EnumerateStructureTransformation`) directly risks passing incorrect kwargs as the internal
API evolves (e.g. `check_ordered_structures` vs `check_ordered_symmetry`), and it loses
the error handling and platform abstraction that the MCP tools provide.
Fix: Always use the designated MCP tool (`pymatgen_enumeration_generator`,
`pymatgen_substitution_generator`, etc.). Only drop to direct pymatgen code when an MCP
tool explicitly cannot accomplish the task (e.g. manual supercell construction).

**`substitution_generator` silently truncates output when many options are given**
Cause: `max_attempts` (default 50) is a hard cap on total output. With a list of N
substitution options and n_structures=k, the tool attempts N×k structures but stops at
`max_attempts`, silently dropping the remainder with no error.
Symptom: `count` in the result is less than N×k; some substitution options are missing.
Fix: Always set `max_attempts = n_structures × len(substitution_options)` explicitly.
Also set `n_structures=1` for deterministic full swaps (fraction=1.0) — higher values
just add identical duplicates and inflate the attempt count unnecessarily.

**`substitution_generator` fractional doping silently becomes a full swap on single-site cells**
Cause: `fraction=0.5` on a sublattice with only one site cannot produce a partial occupancy
(you cannot remove half an atom). The tool falls back to replacing the whole site, returning
the same result as `fraction=1.0` with no warning.
Symptom: The output formula shows a complete element swap even though `fraction < 1.0` was
requested; the output is an ordered structure, not a disordered one.
Fix: Ensure the input cell has **≥ 2 sites of the target species** before using fractional
substitution. For a single-site primitive cell (e.g. a 5-atom perovskite with one B-site),
either (a) build a supercell first so multiple target sites exist, or (b) manually construct
the disordered structure dict with explicit partial occupancies
(`{"element": "Fe", "occu": 0.5}, {"element": "Co", "occu": 0.5}` on the same site)
and pass it directly to `sqs_generator` or `enumeration_generator`.

**`ion_exchange_generator` returns zero structures**
Cause: No charge-neutral solution exists at the requested stoichiometry.
Fix: Try different `exchange_fraction` values, use `allow_oxidation_state_change=True` to debug,
or verify oxidation state assumptions with `mp_get_material_properties`.

**`defect_generator` creates excessively large supercells**
Cause: `supercell_min_atoms` is high (default 64) relative to a primitive cell with few atoms.
Fix: Lower `supercell_min_atoms` (e.g. 32 for quick tests), or supply an explicit `supercell_matrix`.

**`prototype_builder` raises proximity error**
Cause: The chosen lattice parameters place atoms too close together.
Fix: Check against experimental / MP values. Temporarily set `validate_proximity=False` to
retrieve the structure and inspect it before adjusting parameters.

**Duplicate structures in candidate pool**
Cause: Multiple generation paths converge on the same composition and topology.
Fix: Query `ase_query_db` and use `unique_key` in `ase_store_result` to deduplicate on
formula + source_structure hash before running DFT.

**`sqs_generator` produces poor SQS quality (high `sqs_error`)**
Cause: Too few MC steps or too small a supercell for the target composition.
Fix: Increase `n_mc_steps` (try 200 000–500 000) and `supercell_size` (16–24), or install
ATAT and set `use_mcsqs=True`.

---

## Quick Reference

| Task | Tool | Critical parameters |
|------|------|---------------------|
| Build from spacegroup | `prototype_builder` | `spacegroup`, `species`, `lattice_parameters` |
| Isostructural analogues | `substitution_generator` | `substitutions`, `n_structures` |
| Charge-neutral ion swap | `ion_exchange_generator` | `replace_ion`, `with_ions`, `exchange_fraction` |
| Enumerate all orderings | `enumeration_generator` | `max_cell_size ≤ 4`, `sort_by='ewald'` |
| Best quasirandom cell | `sqs_generator` | `supercell_size`, `n_mc_steps`, `n_structures` |
| Point defect supercells | `defect_generator` | `vacancy/substitution/interstitial_species`, `supercell_min_atoms` |
| Rattle / strain ensemble | `perturbation_generator` | `displacement_max`, `strain_percent`, `n_structures` |
