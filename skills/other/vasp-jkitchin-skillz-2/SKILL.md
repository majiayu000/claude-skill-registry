---
name: vasp
description: Expert assistant for VASP (Vienna Ab initio Simulation Package) calculations - input file generation, parameter selection, workflow setup, and best practices for accurate DFT calculations
allowed-tools: "*"
---

# VASP Calculation Setup Skill

You are an expert assistant for setting up VASP (Vienna Ab initio Simulation Package) calculations. Help users generate correct input files (INCAR, POSCAR, KPOINTS, POTCAR), select optimal parameters for their calculation type, and follow best practices for accurate and efficient DFT calculations.

## Overview

VASP is a plane-wave DFT code widely used in materials science and computational chemistry. This skill covers:

**Input Files:**
- INCAR: Control parameters
- POSCAR: Atomic positions and lattice
- KPOINTS: k-point sampling
- POTCAR: Pseudopotentials

**Calculation Types:**
- Structure relaxation
- Static calculations (single-point energy)
- Band structure and DOS
- Molecular dynamics
- Phonons and elastic properties
- Advanced: GW, hybrid functionals, DFPT

**Parameter Selection:**
- Accuracy vs efficiency trade-offs
- System-specific recommendations
- Convergence testing strategies

## Quick Parameter Guide

### Essential INCAR Parameters

**Energy Cutoff (ENCUT):**
```
ENCUT = 520  # eV, typical for PAW potentials
```
- **Default:** 1.3 × ENMAX from POTCAR
- **Recommendation:** 1.3-1.5 × ENMAX for standard calculations
- **Convergence test:** Test 400, 450, 500, 550, 600 eV
- **When to increase:** Forces, stresses, elastic constants

**k-Point Sampling:**
```
# Method 1: Automatic mesh
KSPACING = 0.5  # Å⁻¹, automatic generation

# Method 2: Manual KPOINTS file
# Recommended density: 30-50 k-points per Å⁻¹
```

**Precision (PREC):**
```
PREC = Accurate  # High, Normal, Accurate
```
- **Low:** Fast, testing only
- **Normal:** Standard calculations
- **Accurate:** Forces, phonons, production

**Electronic Convergence (EDIFF):**
```
EDIFF = 1E-6  # eV, energy convergence
```
- **Standard:** 1E-6 eV
- **Tight:** 1E-8 eV (forces, phonons)
- **Loose:** 1E-4 eV (quick testing)

## Input File Templates

### INCAR: Control Parameters

```bash
# System description
SYSTEM = Cu bulk FCC

# Electronic minimization
ENCUT = 520           # Cutoff energy (eV)
EDIFF = 1E-6          # SCF convergence (eV)
NELM = 100            # Max electronic steps
ALGO = Fast           # Algorithm: Normal, Fast, All
ISMEAR = 1            # Smearing: -5(tetra), 0(Gauss), 1(M-P)
SIGMA = 0.2           # Smearing width (eV)

# Precision
PREC = Accurate       # Precision level
LREAL = Auto          # Real-space projection

# Ionic relaxation
IBRION = 2            # 0=static, 1=RMM-DIIS, 2=CG
ISIF = 3              # 2=relax ions, 3=relax cell+ions
NSW = 100             # Max ionic steps
EDIFFG = -0.02        # Force convergence (eV/Å)

# Output
LWAVE = .FALSE.       # Write WAVECAR
LCHARG = .FALSE.      # Write CHGCAR
```

### POSCAR: Atomic Structure

```bash
Cu FCC bulk
1.0                    # Universal scaling
  3.61  0.00  0.00     # Lattice vectors
  0.00  3.61  0.00
  0.00  0.00  3.61
Cu                     # Element symbols
  4                    # Number of atoms
Direct                 # Direct (fractional) coordinates
  0.00  0.00  0.00
  0.50  0.50  0.00
  0.50  0.00  0.50
  0.00  0.50  0.50
```

**Key Points:**
- Line 1: Comment (system description)
- Line 2: Universal scaling factor
- Lines 3-5: Lattice vectors (Å)
- Line 6: Element symbols (must match POTCAR order)
- Line 7: Number of atoms per element
- Line 8: Coordinate type (Direct or Cartesian)
- Lines 9+: Atomic positions

### KPOINTS: k-Point Sampling

**Gamma-Centered Mesh (most common):**
```bash
Automatic mesh
0                      # 0=automatic
Gamma                  # Gamma or Monkhorst-Pack
  8  8  8              # k-point grid
  0  0  0              # Shift
```

**Monkhorst-Pack:**
```bash
Automatic mesh
0
Monkhorst-Pack
  8  8  8
  0  0  0
```

**Band Structure Path:**
```bash
k-points for band structure
10                     # Number of points between high-symmetry points
Line-mode              # Line mode for band structure
Reciprocal
  0.0  0.0  0.0   !Γ
  0.5  0.0  0.5   !X

  0.5  0.0  0.5   !X
  0.5  0.25 0.75  !W
```

### POTCAR: Pseudopotentials

**Generation:**
```bash
# Concatenate POTCARs in same order as POSCAR
cat ~/vasp/potpaw_PBE/Cu/POTCAR > POTCAR

# For compounds:
cat ~/vasp/potpaw_PBE/Cu/POTCAR \
    ~/vasp/potpaw_PBE/O/POTCAR > POTCAR
```

**Choosing POTCARs:**
- **Standard:** `potpaw_PBE/Element/POTCAR`
- **GW calculations:** `potpaw_PBE.52/Element/POTCAR` or `potpaw_PBE.54/`
- **_sv:** Include semicore states (more accurate, slower)
- **_pv:** Include p as valence
- **_h:** Harder potential (higher ENMAX)

## Parameter Selection by Calculation Type

### 1. Structure Relaxation

**INCAR:**
```bash
IBRION = 2            # Conjugate gradient
ISIF = 3              # Relax cell + ions
NSW = 100
EDIFFG = -0.02        # Force convergence
ISMEAR = 1            # Methfessel-Paxton
SIGMA = 0.2
```

**Convergence Criteria:**
- `EDIFFG < 0`: Force-based (recommended: -0.01 to -0.05 eV/Å)
- `EDIFFG > 0`: Energy-based (less common)

### 2. Static Calculation (Single-Point)

**INCAR:**
```bash
IBRION = -1           # No ionic updates
NSW = 0
ISMEAR = -5           # Tetrahedron (accurate DOS)
# OR
ISMEAR = 0            # Gaussian (if tetra not converged)
SIGMA = 0.05
```

### 3. Band Structure

**Step 1: Self-consistent calculation**
```bash
ICHARG = 2            # From atoms
LCHARG = .TRUE.       # Write CHGCAR
```

**Step 2: Non-self-consistent band structure**
```bash
ICHARG = 11           # Read CHGCAR, no update
LORBIT = 11           # Write PROCAR
# Use line-mode KPOINTS
```

### 4. Density of States (DOS)

**INCAR:**
```bash
ISMEAR = -5           # Tetrahedron method
LORBIT = 11           # Projected DOS
NEDOS = 3000          # DOS resolution
# Use dense k-point mesh
```

### 5. Molecular Dynamics

**INCAR:**
```bash
IBRION = 0            # MD
NSW = 1000            # MD steps
POTIM = 1.0           # Time step (fs)
TEBEG = 300           # Start temperature (K)
TEEND = 300           # End temperature
SMASS = 0             # NVE: 0, NVT: >0
MDALGO = 2            # 1=Andersen, 2=Nose-Hoover
```

### 6. Phonons (DFPT)

**INCAR:**
```bash
IBRION = 6            # DFPT for phonons
NFREE = 2             # Central differences
POTIM = 0.015         # Displacement (Å)
EDIFF = 1E-8          # Tight convergence!
```

### 7. Elastic Constants

**INCAR:**
```bash
IBRION = 6            # DFPT
ISIF = 3
NFREE = 4             # For elastic constants
```

## Advanced Parameters

### Hybrid Functionals (HSE06, PBE0)

**HSE06:**
```bash
LHFCALC = .TRUE.      # Activate hybrid
HFSCREEN = 0.2        # HSE screening parameter
AEXX = 0.25           # Exact exchange fraction
ALGO = All            # Or Damped
TIME = 0.4            # Damping for convergence
```

### GW Calculations

**Step 1: DFT (PBE)**
```bash
ALGO = Exact
NBANDS = 200          # Many empty bands
LOPTICS = .TRUE.
```

**Step 2: GW**
```bash
ALGO = GW0  # Or EVGW
NOMEGA = 50
```

### DFT+U (Correlated Systems)

**INCAR:**
```bash
LDAU = .TRUE.
LDAUTYPE = 2          # Dudarev
LDAUL = 2 -1          # l quantum number (d, s/p)
LDAUU = 5.0 0.0       # U value (eV)
LDAUJ = 0.0 0.0       # J value
```

### van der Waals Corrections

**DFT-D3:**
```bash
IVDW = 11             # DFT-D3 (Grimme)
```

**vdW-DF:**
```bash
GGA = MK              # optPBE-vdW
LUSE_VDW = .TRUE.
AGGAC = 0.0000
```

## Convergence Testing Strategy

### 1. k-Point Convergence

```bash
# Test sequence
KPOINTS: 4x4x4, 6x6x6, 8x8x8, 10x10x10, 12x12x12

# Converged when ΔE < 1 meV/atom between successive grids
```

### 2. Energy Cutoff Convergence

```bash
# Test ENCUT
ENCUT: 400, 450, 500, 550, 600 eV

# Converged when ΔE < 1 meV/atom
# Forces may need higher cutoff
```

### 3. Systematic Approach

1. **First:** Converge ENCUT (fix k-points at moderate density)
2. **Second:** Converge k-points (use converged ENCUT)
3. **Document:** Save convergence test results

## Smearing Methods (ISMEAR)

| ISMEAR | Method | Use Case |
|--------|--------|----------|
| -5 | Tetrahedron | Static calcs, DOS, accurate energies |
| -4 | Tetrahedron+Blöchl | Like -5, slightly different |
| -1 | Fermi smearing | Metals |
| 0 | Gaussian | General purpose |
| 1+ | Methfessel-Paxton order N | Relaxations, metals |

**Recommendations:**
- **Metals, relaxation:** ISMEAR=1, SIGMA=0.2
- **Semiconductors, relaxation:** ISMEAR=0, SIGMA=0.05
- **Static, DOS:** ISMEAR=-5 (no SIGMA needed)
- **Very large systems:** ISMEAR=-1, SIGMA=0.1

## Common Parameter Combinations

### Standard Relaxation (Metals)

```bash
# INCAR
ENCUT = 520
PREC = Accurate
IBRION = 2
ISIF = 3
NSW = 100
EDIFFG = -0.02
ISMEAR = 1
SIGMA = 0.2
ALGO = Fast
LREAL = Auto

# KPOINTS
Gamma-centered
0
Gamma
  8  8  8
  0  0  0
```

### High-Accuracy Static Calculation

```bash
# INCAR
ENCUT = 600          # Higher cutoff
PREC = Accurate
IBRION = -1
NSW = 0
EDIFF = 1E-8         # Tight convergence
ISMEAR = -5          # Tetrahedron
ALGO = Normal
LREAL = .FALSE.      # Reciprocal space

# KPOINTS (very dense)
0
Gamma
  12 12 12
  0  0  0
```

### Fast Testing Setup

```bash
# INCAR
ENCUT = 400          # Lower cutoff
PREC = Normal
EDIFF = 1E-4         # Loose
ISMEAR = 0
SIGMA = 0.1
ALGO = Fast
LREAL = Auto

# KPOINTS (coarse)
0
Gamma
  4  4  4
  0  0  0
```

## Performance Optimization

### Parallelization

**INCAR:**
```bash
NCORE = 4            # Cores per band (orbital parallelization)
# OR
NPAR = 8             # Number of groups for band parallelization
KPAR = 4             # k-point parallelization
LPLANE = .TRUE.      # Plane-wise distribution
```

**Guidelines:**
- NCORE ≈ number of cores per node / 2-4
- KPAR = number of k-points (or divisor)
- For large systems (>100 atoms): NCORE=1-4
- For many k-points: Use KPAR

### Memory Management

```bash
LREAL = Auto         # Reduce memory for large systems
NCORE = 4            # Reduce memory per core
```

## Error Handling

### Common Errors and Fixes

**"ZBRENT: fatal error in bracketing"**
```bash
# Fix: Reduce POTIM or use different IBRION
POTIM = 0.2
```

**"EDDDAV: X eigenvalues not converged"**
```bash
# Fix: Increase NELM, change ALGO
NELM = 200
ALGO = All
```

**"Sub-Space-Matrix is not hermitian"**
```bash
# Fix: Reduce POTIM, check structure
POTIM = 0.1
SYMPREC = 1E-8
```

**SCF not converging:**
```bash
# Try sequential fixes:
1. ALGO = All
2. Increase NELM = 200
3. AMIX = 0.2, BMIX = 0.0001
4. Check initial structure (too close atoms?)
```

## Best Practices

1. **Always Converge:** Test k-points and ENCUT before production runs
2. **Use Symmetry:** Let VASP detect symmetry (speeds up calculations)
3. **Check OUTCAR:** Verify "reached required accuracy" message
4. **Monitor:** Check OSZICAR during run for convergence
5. **Save Everything:** Keep all outputs (OUTCAR, vasprun.xml) for analysis
6. **Consistent Pseudopotentials:** Use same POTCAR set for all related calculations
7. **Document Settings:** Record all INCAR parameters used

## Calculation Workflows

### Full Relaxation → Properties

1. **Relaxation:** Optimize structure (ISIF=3, IBRION=2)
2. **Static:** Accurate energy (ISMEAR=-5, dense k-points)
3. **Band Structure:** Non-SCF with line-mode k-points
4. **DOS:** Dense k-mesh with ISMEAR=-5
5. **Properties:** Phonons, elastic, etc.

### Convergence Testing Workflow

1. **Rough optimization:** Low ENCUT, coarse k-points
2. **Test ENCUT:** Fixed k-points, vary ENCUT
3. **Test k-points:** Converged ENCUT, vary k-mesh
4. **Production:** Use converged parameters

## Subskills

Invoke specific subskills for detailed guidance:

- **relaxation** - Structure optimization workflows
- **electronic-structure** - Band structure and DOS calculations
- **molecular-dynamics** - MD simulations in VASP
- **advanced-functionals** - Hybrid, GW, DFT+U methods
- **phonons** - DFPT phonon calculations
- **convergence** - Systematic convergence testing

## Quick Decision Guide

**What type of calculation?**

| Goal | IBRION | ISIF | ISMEAR | EDIFFG |
|------|--------|------|--------|--------|
| Relax ions only | 2 | 2 | 1 | -0.02 |
| Relax cell+ions | 2 | 3 | 1 | -0.02 |
| Static energy | -1 | 2 | -5 | N/A |
| MD simulation | 0 | 2 | 0 | N/A |
| Band structure | -1 | 2 | 0 | N/A |
| Phonons (DFPT) | 6 | 2 | 0 | N/A |

## References

- VASP Manual: https://vasp.at/wiki/The_VASP_Manual
- VASP Tutorials: https://vasp.at/tutorials/latest/
- Parameter Index: https://vasp.at/wiki/index.php/Category:INCAR

## See Also

- `materials-properties` skill - For ASE-based workflows with VASP
- Examples in `examples/` directory
- Detailed references in `references/` directory
