---
name: materials-compute
description: "Materials computation environment reference and skill index. READ THIS FIRST when performing any materials science calculation — contains the master index of all 221 skills across 44 groups."
---

# Materials Computation Environment

This container includes a full materials science computation environment. Use these tools for atomistic simulation tasks.

## Available Computation Engines

### Quantum ESPRESSO 7.5 (DFT)
- Binary: `pw.x` (also `ph.x`, `pp.x`, `bands.x`, `dos.x`, `projwfc.x`, etc.)
- Location: `/opt/qe/bin/`
- Use for: electronic structure, band gaps, density of states, phonons, elastic constants
- Run with MPI: `mpirun --allow-run-as-root -np N pw.x < input.in > output.out`
- Pseudopotentials download URL:
  ```
  https://pseudopotentials.quantum-espresso.org/upf_files/<FILENAME>.UPF
  ```
  Common pseudopotentials (PAW PBE from pslibrary):
  - Si: `Si.pbe-n-kjpaw_psl.1.0.0.UPF`
  - Cu: `Cu.pbe-dn-kjpaw_psl.1.0.0.UPF`
  - Al: `Al.pbe-n-kjpaw_psl.1.0.0.UPF`
  - Ni: `Ni.pbe-n-kjpaw_psl.1.0.0.UPF`
  - O:  `O.pbe-n-kjpaw_psl.1.0.0.UPF`
  - C:  `C.pbe-n-kjpaw_psl.1.0.0.UPF`
  - H:  `H.pbe-kjpaw_psl.1.0.0.UPF`
  - N:  `N.pbe-n-kjpaw_psl.1.0.0.UPF`
  - Fe: `Fe.pbe-spn-kjpaw_psl.1.0.0.UPF`
  - Ti: `Ti.pbe-spn-kjpaw_psl.1.0.0.UPF`
  - Zn: `Zn.pbe-dn-kjpaw_psl.1.0.0.UPF`
  - Ba: `Ba.pbe-spn-kjpaw_psl.1.0.0.UPF`
  - Li: `Li.pbe-s-kjpaw_psl.1.0.0.UPF`
  - Na: `Na.pbe-spn-kjpaw_psl.1.0.0.UPF`
  - K:  `K.pbe-spn-kjpaw_psl.1.0.0.UPF`

  Example download:
  ```bash
  wget -q https://pseudopotentials.quantum-espresso.org/upf_files/Si.pbe-n-kjpaw_psl.1.0.0.UPF -O Si.UPF
  ```
  Alternative sources: [SSSP](https://www.materialscloud.org/discover/sssp) or [PseudoDojo](http://www.pseudo-dojo.org/)

### LAMMPS (Molecular Dynamics)
- Binary: `lmp`
- Use for: MD simulations, thermal properties, diffusion, mechanical properties
- Supports OpenKIM potentials (pre-installed)
- Run: `lmp -in input.lammps`
- EAM potentials: use `pair_style eam/alloy` with potentials from OpenKIM or download from NIST
- For water: use SPC/E or TIP3P model with `pair_style lj/cut/coul/long`

### RASPA3 (Monte Carlo)
- Binary: `raspa3`
- Use for: gas adsorption in porous materials (MOFs, zeolites), adsorption isotherms, Henry constants
- Run: `cd /path/to/simulation && raspa3`
- Input format: JSON files (`simulation.json`, `force_field.json`, molecule JSON files)
- Official examples: `/usr/share/raspa3/examples/` (basic MC, adsorption, breakthrough, etc.)
- IMPORTANT: Always copy an official example as starting point and modify it:
  ```bash
  cp -r /usr/share/raspa3/examples/basic/1_mc_methane_in_box /tmp/my_sim
  cd /tmp/my_sim && raspa3
  ```

## Python Materials Science Stack

### Pre-installed in base conda environment:
- **pymatgen**: Crystal structure manipulation, phase diagrams, electronic structure analysis
- **ASE (Atomic Simulation Environment)**: Atoms objects, calculators, optimization, MD
- **mp-api**: Materials Project API access (needs API key)
- **MACE-torch**: Universal machine learning interatomic potential
- **spglib**: Space group analysis
- **torch**: PyTorch (CPU version)
- **numpy / scipy / matplotlib**: Scientific computing and visualization

### Conda/pip available:
The agent can install additional packages as needed:
```bash
# Create isolated environment for specific tasks
conda create -n myenv python=3.11 -y
conda activate myenv

# Install additional ML potentials
pip install chgnet sevenn

# Install workflow managers
pip install fireworks jobflow atomate2
```

## Common Workflows

### DFT Calculation (QE)
1. Prepare structure (use pymatgen to read CIF/POSCAR and generate QE input)
2. Download pseudopotentials
3. Run SCF calculation: `pw.x < scf.in > scf.out`
4. Post-process: bands, DOS, charge density, etc.

### MD Simulation (LAMMPS or ASE+MACE)
1. Prepare structure and force field
2. Set up LAMMPS input or ASE calculator
3. Run simulation
4. Analyze trajectory: RDF, MSD, thermal conductivity, etc.

### MLIP Calculation (ASE + MACE)
```python
from ase.io import read
from mace.calculators import mace_mp
calc = mace_mp(model="medium", device="cpu")
atoms = read("structure.cif")
atoms.calc = calc
energy = atoms.get_potential_energy()
forces = atoms.get_forces()
```

### VASP (via vasp-remote)
If the user has configured VASP access (run `/add-vasp`), use `vasp-remote` to execute VASP calculations:
1. Generate INCAR, POSCAR, KPOINTS, POTCAR in the current directory
2. Run: `vasp-remote run` (submits to cluster or runs locally, waits for results)
3. Parse `vasprun.xml` with pymatgen

Check if VASP is available: `vasp-remote config 2>/dev/null`. If not configured, fall back to Method A (MACE) or Method B (QE).

### Monte Carlo (RASPA3)
1. Prepare framework structure (CIF)
2. Configure simulation input (guest molecules, temperature, pressure)
3. Run RASPA3
4. Analyze adsorption isotherm

---

## Skill Reference Index

**IMPORTANT:** Before performing any materials science computation, check the relevant skill guide below. Each skill provides complete, runnable code for three approaches: ASE+MACE (fast screening), QE DFT (accurate), and VASP (future external). Read the SKILL.md in the skill directory for step-by-step instructions.

Skills are located at `~/.claude/skills/<group>/<sub-skill>/SKILL.md`.

### Structure & Symmetry

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `structure-tools` | input-generation, structure-editing, symmetry-analysis, format-conversion, structure-matching, xrd-pattern, pdf-analysis, advanced-optimization | VASP/QE input files, editing structures, symmetry finding, format conversion, advanced structure optimization |
| `structure-models` | supercell-builder, surface-builder, alloy-builder, defect-builder, heterostructure, nanowire-nanotube, quantum-dot, moire-superlattice | Build supercells, surfaces, alloys, defects, heterostructures, nanowires, quantum dots, moire patterns |
| `kpath-utilities` | bulk-kpath, 2d-kpath, 1d-kpath, phonopy-kpath, cp2k-kpath | K-point paths for band structure in any code |

### Electronic Structure

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `electronic-structure` | scf-relax, band-structure, density-of-states, projected-dos, spatially-resolved-dos, vasp-bands, convergence-testing, inverse-participation-ratio | SCF, relaxation, band structure, DOS, PDOS, IPR, convergence tests |
| `band-advanced` | 3d-band-structure, hybrid-dft-bands, band-unfolding | 3D bands, HSE/PBE0 bands, supercell band unfolding |
| `fermi-surface` | 3d-fermi-surface, 2d-fermi-surface, projected-fermi-surface | Fermi surface visualization (bulk and 2D) |
| `advanced-electronic` | hubbard-u, spin-orbit-coupling, gw-approximation, van-der-waals, topological-invariants | DFT+U, SOC, GW, vdW-DF, Z2 invariants |

### Mechanical & Thermal Properties

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `mechanical-properties` | elastic-constants, stress-strain-method, energy-strain-method, equation-of-state, angular-mechanics | Elastic tensor, bulk/shear modulus, EOS, angular-dependent mechanics |
| `thermal-properties` | phonon, phonon-from-outcar, molecular-dynamics, msd-diffusion, rdf-analysis, vacf-vdos, md-trajectory-tools, bond-distribution, gruneisen-qha, thermal-conductivity, anharmonicity, free-energy-calculation, quasi-harmonic-debye | Phonons, MD analysis, MSD, RDF, VDOS, bond distributions, QHA, thermal conductivity, free energy, Debye model |
| `thermoconductivity` | lattice-thermal-conductivity | Lattice thermal conductivity (BTE) |

### Bonding & Charge Analysis

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `bonding-analysis` | charge-density, charge-density-difference, planar-charge, bader-charge, bader2pqr, elf-analysis, lobster-cohp, orbital-projection, stm-simulation, charge-format-conversion | Charge density, CDD, Bader, ELF, COHP, orbital projections, STM simulation |
| `potential-analysis` | work-function, planar-average, macroscopic-average | Work function, planar/macroscopic averaged potential |
| `wavefunction-analysis` | real-space-wavefunction, wavefunction-parity | Real-space wavefunction visualization, parity analysis |

### Optical, Magnetic & Transport

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `optical-properties` | dielectric-function, absorption-spectrum, optical-conductivity, joint-dos, transition-dipole, slme | Dielectric function, absorption, optical conductivity, JDOS, SLME |
| `magnetic-properties` | magnetic-anisotropy, magnetic-ordering, spin-polarized | MAE, magnetic ground state, spin-polarized calculations |
| `spin-texture` | 2d-spin-texture, 3d-spin-texture | Spin texture for 2D/3D materials with SOC |
| `transport-properties` | boltzmann-transport, kpoints-transport | Boltzmann transport (BoltzTraP), transport k-meshes |
| `electron-phonon` | elph-coupling, superconductivity, deformation-potential, electronic-transport | Electron-phonon coupling, Tc, deformation potentials |

### Ferroelectric & Piezoelectric

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `ferroelectric` | polarization, born-effective-charge, dielectric-tensor, piezoelectric, ferroelectric-switching | Berry phase polarization, Born charges, dielectric tensor, piezoelectric tensor |
| `piezoelectric` | piezoelectric-tensor | Piezoelectric constants from DFPT |

### Catalysis & Defects

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `catalysis-electrochem` | thermal-corrections, neb-analysis, band-center, reaction-kinetics, imaginary-freq-correction, implicit-solvation | Adsorbate thermodynamics, NEB, d-band center, Arrhenius kinetics, imaginary freq fix, solvation effects |
| `catalyst-screening` | d-band-center, scaling-relations, overpotential | D-band theory, adsorption scaling, OER/HER overpotential |
| `defects-reactions` | vacancy-formation, substitution-defect, interstitial-defect, point-defect, defect-thermodynamics, migration-barrier, neb-transition-state, reaction-pathway, adsorption-energy, surface-adsorption, surface-energy, configuration-coordinate, activation-relaxation-technique | Point defects, formation energies, NEB barriers, adsorption, surface energy, CC diagrams, ART saddle point search |
| `surface-energy` | surface-energy-calc, wulff-construction | Surface energy convergence, Wulff shape |

### 2D Materials & Semiconductors

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `2d-materials` | vacuum-resize, layer-manipulation, band-edges, stacking-energy | Vacuum control, layer centering, band alignment, stacking PES (gamma surface) |
| `semiconductor-kit` | band-gap, effective-mass, angular-effective-mass, fermi-velocity | Band gap, effective mass (isotropic & angular), Fermi velocity |

### Monte Carlo & Phase Diagrams

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `monte-carlo` | gcmc-simulation, adsorption-isotherm, gas-adsorption, gas-separation, pore-analysis | GCMC with RASPA3, isotherms, selectivity, pore size distribution |
| `phase-diagram` | convex-hull, pourbaix-diagram | Thermodynamic convex hull, Pourbaix diagrams |
| `phase-transition` | phase-diagram, mpmorph-melting, order-parameter, amorphous-structure, melting-point-coexistence, metadynamics | Phase boundaries, melting point, order parameters, amorphous structures, coexistence method, metadynamics FES |
| `alloy-disorder` | cluster-expansion, sqs-generation | Cluster expansion, special quasirandom structures |

### Code Interfaces & MLIP

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `code-interfaces` | vasp-qe-converter, boltztrap-interface, phonopy-interface, wannier90-interface, ifc-analysis | VASP↔QE conversion, BoltzTraP, phonopy, Wannier90, IFC tensors |
| `wannier-functions` | wannier90-workflow | Wannier90 tight-binding from DFT |
| `mlip-guide` | universal-mlip, mace-advanced, mlip-validation, torchsim-batch | MACE-MP-0 usage, fine-tuning, validation against DFT, batch screening |

### Other

| Skill Group | Sub-skills | Use For |
|---|---|---|
| `battery-electrode` | intercalation-voltage, ion-diffusion | Battery voltage profiles, ion migration barriers |
| `topological` | z2-invariant, berry-curvature | Z2 topological invariant, Berry curvature |
| `spectroscopy` | raman-ir, xas-xanes | Raman/IR spectra, XAS/XANES simulation |
| `dft-corrections` | hubbard-u, spin-orbit-coupling, vdw-correction | When and how to apply DFT corrections |
| `high-throughput` | screening-workflow, batch-calculations, batch-screening, materials-filtering, phase-stability, property-prediction, matpes-dual-static, convergence-automation | High-throughput screening, batch computation, automated convergence testing |
| `materials-databases` | materials-project, 2d-semiconductors | Query Materials Project, 2D materials databases |
| `interface` | heterostructure, grain-boundary | Heterostructure and grain boundary construction |
| `biomolecular-md` | openmm-simulation | Biomolecular MD with OpenMM |
| `molecular-qchem` | gaussian-qchem-workflow | Molecular quantum chemistry workflows |

### How to Use a Skill

1. **Identify** the relevant skill from the index above
2. **Read** the SKILL.md: `cat ~/.claude/skills/<group>/<sub-skill>/SKILL.md`
3. **Choose method**: Method A (ASE+MACE, fast) or Method B (QE DFT, accurate) or Method C (VASP)
4. **Follow** the step-by-step code in the SKILL.md — all code is complete and runnable
5. **Check** the "Common Issues" table at the bottom if anything goes wrong
