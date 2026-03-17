---
name: fairchem
description: Expert guidance for Meta's FAIRChem library - machine learning methods for materials science and quantum chemistry using pretrained UMA models with ASE integration for fast, accurate predictions
---

# FAIRChem Skill

This skill provides expert guidance for using FAIRChem (formerly OCP - Open Catalyst Project), Meta's FAIR Chemistry library of machine learning methods for materials science and quantum chemistry.

## When to Use This Skill

Use this skill when:
- Using ML potentials for materials and molecular simulations
- Running fast geometry optimizations with pretrained models
- Performing large-scale MD simulations
- Calculating energies and forces without DFT
- Working with the UMA (Universal Materials Algebra) models
- Needing predictions for catalysis, molecules, crystals, or MOFs
- Integrating ML models with ASE workflows
- Scaling calculations across multiple GPUs

## What is FAIRChem?

FAIRChem is Meta's machine learning framework for chemistry that provides:
- **Pretrained UMA models** (`uma-s-1p1`, `uma-m-1p1`) for universal predictions
- **Domain-specific tasks**: catalysis (oc20), materials (omat), molecules (omol), MOFs (odac), crystals (omc)
- **ASE integration** via `FAIRChemCalculator`
- **Multi-GPU support** for distributed inference
- **Fast predictions**: 100-1000× faster than DFT

### Key Advantage
FAIRChem allows you to use the same model across different chemistry domains by simply changing the `task_name` parameter.

## Core Concepts

### 1. UMA Models
Universal Materials Algebra models trained on diverse datasets:
- `uma-s-1p1`: Small model (~50M parameters) - faster inference
- `uma-m-1p1`: Medium model (~300M parameters) - higher accuracy

### 2. Task Names (Domains)
Specify the chemistry domain for domain-specific predictions:
- `oc20`: Catalysis (surfaces with adsorbates)
- `omat`: Inorganic materials (crystals, bulk)
- `omol`: Molecules (organic chemistry)
- `odac`: Metal-organic frameworks (MOFs)
- `omc`: Molecular crystals

### 3. FAIRChemCalculator
ASE calculator interface that wraps UMA models:
- Drop-in replacement for DFT calculators
- Supports all ASE workflows
- Provides energies, forces, and stresses
- Compatible with optimization, MD, NEB

### 4. Inference Settings
Performance optimization modes:
- `turbo`: Maximum speed, slightly reduced accuracy
- Standard: Balanced speed and accuracy
- Multi-GPU: Distributed inference with `workers=N`

## Installation

```bash
# Install fairchem
pip install fairchem-core

# For GPU support
pip install fairchem-core[gpu]

# Hugging Face login (required for UMA models)
pip install huggingface-hub
huggingface-cli login
```

**Note**: You must have a Hugging Face account and request access to the UMA model repository.

## Basic Usage Pattern

### Standard Workflow

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.build import bulk
from ase.optimize import LBFGS

# 1. Load pretrained model
predict_unit = load_predict_unit("uma-m-1p1")

# 2. Create calculator for specific domain
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omat"  # Choose domain
)

# 3. Use with ASE
atoms = bulk("Cu", "fcc", a=3.6)
atoms.calc = calc

# 4. Calculate properties
energy = atoms.get_potential_energy()
forces = atoms.get_forces()

# 5. Optimize structure
opt = LBFGS(atoms)
opt.run(fmax=0.05)
```

## Common Workflows

### Workflow 1: Catalysis - Surface Adsorption

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.build import fcc111, add_adsorbate
from ase.optimize import LBFGS
from ase.constraints import FixAtoms

# Load model
predict_unit = load_predict_unit("uma-m-1p1")

# Create calculator for catalysis
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="oc20"  # Catalysis domain
)

# Build slab with adsorbate
slab = fcc111("Cu", size=(4, 4, 4), vacuum=10.0)
add_adsorbate(slab, "CO", height=2.0, position="fcc")

# Fix bottom layers
n_atoms_per_layer = 16
constraint = FixAtoms(indices=range(n_atoms_per_layer * 2))
slab.set_constraint(constraint)

# Attach calculator and optimize
slab.calc = calc
opt = LBFGS(slab, trajectory="slab_opt.traj")
opt.run(fmax=0.05)

# Get results
E = slab.get_potential_energy()
forces = slab.get_forces()
```

### Workflow 2: Bulk Materials - Lattice Optimization

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.build import bulk
from ase.optimize import FIRE
from ase.filters import FrechetCellFilter

# Load model
predict_unit = load_predict_unit("uma-m-1p1")

# Calculator for materials
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omat"  # Materials domain
)

# Create bulk structure
atoms = bulk("Fe", "bcc", a=2.87)
atoms.calc = calc

# Optimize both positions and cell
# FrechetCellFilter allows cell parameters to change
ucf = FrechetCellFilter(atoms)
opt = FIRE(ucf)
opt.run(fmax=0.05)

# Results
optimized_lattice = atoms.cell.cellpar()[0]
print(f"Optimized lattice constant: {optimized_lattice:.3f} Å")
```

### Workflow 3: Molecular Dynamics

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.build import bulk
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.langevin import Langevin
from ase import units

# Load with turbo settings for speed
predict_unit = load_predict_unit(
    "uma-s-1p1",  # Use small model for MD
    inference_settings="turbo"
)

# Calculator for MD
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omat",
    workers=4  # Multi-GPU for large systems
)

# Large system
atoms = bulk("C", "fcc", a=3.57) * (20, 20, 20)  # 8000 atoms
atoms.calc = calc

# Initialize velocities
MaxwellBoltzmannDistribution(atoms, temperature_K=300)

# Run NVT dynamics
dyn = Langevin(
    atoms,
    timestep=1.0 * units.fs,
    temperature_K=300,
    friction=0.002
)

# Run
from ase.io.trajectory import Trajectory
traj = Trajectory("md.traj", "w", atoms)
dyn.attach(traj.write, interval=10)
dyn.run(5000)
```

### Workflow 4: Molecular Systems

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.build import molecule
from ase.optimize import LBFGS

# Load model
predict_unit = load_predict_unit("uma-m-1p1")

# Calculator for molecules
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omol"  # Molecular domain
)

# Build molecule
mol = molecule("H2O")
mol.center(vacuum=10.0)
mol.calc = calc

# Optimize
opt = LBFGS(mol, trajectory="mol_opt.traj")
opt.run(fmax=0.05)

# Get properties
E = mol.get_potential_energy()
forces = mol.get_forces()
```

### Workflow 5: NEB Calculations

```python
from fairchem.data.ase import FAIRChemCalculator
from fairchem.predict import load_predict_unit
from ase.neb import NEB
from ase.optimize import BFGS
from ase.io import read

# Load model
predict_unit = load_predict_unit("uma-m-1p1")

# Calculator
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="oc20"
)

# Load initial and final states
initial = read("initial.traj")
final = read("final.traj")

# Create NEB
images = [initial]
images += [initial.copy() for i in range(5)]
images += [final]

neb = NEB(images)
neb.interpolate()

# Attach calculator to intermediate images
for image in images[1:-1]:
    image.calc = calc

# Optimize
opt = BFGS(neb, trajectory="neb.traj")
opt.run(fmax=0.05)

# Analyze
energies = [img.get_potential_energy() for img in images]
barrier = max(energies) - energies[0]
print(f"Barrier: {barrier:.3f} eV")
```

## Model Loading Options

### Load Pretrained UMA Model

```python
from fairchem.predict import load_predict_unit

# Standard loading
predict_unit = load_predict_unit("uma-m-1p1")

# With turbo mode (faster, slight accuracy trade-off)
predict_unit = load_predict_unit(
    "uma-m-1p1",
    inference_settings="turbo"
)

# Specify device
predict_unit = load_predict_unit(
    "uma-m-1p1",
    device="cuda:0"
)

# Load local checkpoint
predict_unit = load_predict_unit(
    "/path/to/checkpoint.pt",
    device="cuda"
)
```

### Available Models

- `uma-s-1p1`: Small, fast (~50M params)
- `uma-m-1p1`: Medium, accurate (~300M params)

## Task Selection Guide

| Domain | Task Name | Use For | Examples |
|--------|-----------|---------|----------|
| Catalysis | `oc20` | Surfaces + adsorbates | CO on Cu(111), O on Pt |
| Materials | `omat` | Bulk crystals, defects | Fe lattice, Si bulk |
| Molecules | `omol` | Organic molecules | H2O, CH4, proteins |
| MOFs | `odac` | Metal-organic frameworks | ZIF-8, MOF-5 |
| Crystals | `omc` | Molecular crystals | Ice, organic crystals |

## Performance Optimization

### Multi-GPU Inference

```python
# Use multiple GPUs automatically
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omat",
    workers=8  # Use 8 GPUs
)

# Achieves ~10× speedup on 8× H100 GPUs
```

### Turbo Mode

```python
# Trade slight accuracy for speed
predict_unit = load_predict_unit(
    "uma-s-1p1",  # Small model
    inference_settings="turbo"
)

# Good for:
# - MD simulations
# - Large systems
# - Initial screening
```

### Batch Predictions

```python
# For multiple similar calculations
from fairchem.data.ase import batch_predict

structures = [atoms1, atoms2, atoms3, ...]

results = batch_predict(
    structures,
    predict_unit=predict_unit,
    task_name="omat"
)
```

## Best Practices

### 1. Task Selection
Always choose the appropriate task for your system:
- **Surfaces with adsorbates** → `oc20`
- **Bulk materials** → `omat`
- **Isolated molecules** → `omol`
- **MOFs** → `odac`
- **Molecular crystals** → `omc`

### 2. Model Selection
- **Initial screening**: Use `uma-s-1p1` + turbo
- **Production calculations**: Use `uma-m-1p1`
- **Very large systems**: Use `uma-s-1p1` + workers

### 3. Validation
ML models have different error characteristics than DFT:
```python
# Always validate critical results
# Compare ML prediction with DFT for representative cases
ml_energy = atoms.get_potential_energy()  # FAIRChem
atoms.calc = Vasp(...)  # Switch to DFT
dft_energy = atoms.get_potential_energy()
error = abs(ml_energy - dft_energy)
```

### 4. Uncertainty Quantification
FAIRChem models provide predictions but not uncertainty:
- Test on similar known systems first
- Validate against DFT for critical results
- Use ensemble of predictions if available

### 5. Memory Management
For large systems:
```python
# Use turbo mode
predict_unit = load_predict_unit(
    "uma-s-1p1",
    inference_settings="turbo"
)

# Distribute across GPUs
calc = FAIRChemCalculator(
    predict_unit=predict_unit,
    task_name="omat",
    workers=4
)
```

## Common Patterns

### Energy Calculation

```python
atoms.calc = calc
energy = atoms.get_potential_energy()  # eV
forces = atoms.get_forces()  # eV/Å
stress = atoms.get_stress()  # eV/Å³
```

### Geometry Optimization

```python
from ase.optimize import LBFGS, FIRE, BFGS

# Fast convergence
opt = LBFGS(atoms, trajectory="opt.traj")
opt.run(fmax=0.05)

# For difficult systems
opt = FIRE(atoms)
opt.run(fmax=0.05)
```

### Cell Optimization

```python
from ase.filters import FrechetCellFilter

# Optimize both atoms and cell
ucf = FrechetCellFilter(atoms)
opt = FIRE(ucf)
opt.run(fmax=0.05)
```

## Integration with ASE

FAIRChemCalculator is a full ASE calculator:

```python
# All ASE functionality works
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from ase.eos import calculate_eos

# Vibrational analysis
vib = Vibrations(atoms)
vib.run()

# Thermochemistry
thermo = IdealGasThermo(...)

# Equation of state
eos = calculate_eos(atoms)
```

## Troubleshooting

### Hugging Face Authentication

```bash
# Login to Hugging Face
huggingface-cli login

# Request access to UMA models at:
# https://huggingface.co/meta-llama/uma-m-1p1
```

### GPU Memory Issues

```python
# Use smaller model
predict_unit = load_predict_unit("uma-s-1p1")

# Use turbo mode
predict_unit = load_predict_unit(
    "uma-s-1p1",
    inference_settings="turbo"
)

# Reduce batch size (if using batch predictions)
```

### Slow Inference

```python
# Enable turbo mode
inference_settings="turbo"

# Use multiple GPUs
workers=N

# Use smaller model
"uma-s-1p1"
```

### Wrong Task Selection

```python
# Symptoms: Poor predictions, unphysical results
# Solution: Verify task matches your system

# For surfaces + adsorbates:
task_name="oc20"  # NOT "omat" or "omol"

# For bulk materials:
task_name="omat"  # NOT "oc20"
```

## Version Compatibility

**Important**: FAIRChem v2 is a breaking change from v1
- v2 code is NOT compatible with v1 models
- v1 code is NOT compatible with v2 models
- UMA models require FAIRChem >= 2.0

```python
# Check version
import fairchem
print(fairchem.__version__)  # Should be >= 2.0 for UMA
```

## Comparison with DFT

| Aspect | FAIRChem | DFT |
|--------|----------|-----|
| Speed | 100-1000× faster | Slower |
| Accuracy | ~0.1 eV | Reference |
| Scaling | Linear, multi-GPU | Cubic |
| System size | 1000s of atoms | 10-100s atoms |
| Use case | Screening, MD | High accuracy |

## When to Use FAIRChem vs DFT

**Use FAIRChem for:**
- Initial screening of many structures
- Long MD simulations
- Large systems (>500 atoms)
- Rapid prototyping
- High-throughput workflows

**Use DFT for:**
- Final validation
- Novel chemistries outside training data
- When highest accuracy needed
- Electronic structure analysis
- Magnetic properties

## Resources

When suggesting FAIRChem solutions:
- Specify correct task_name for the domain
- Recommend appropriate model (s vs m)
- Suggest performance optimizations (turbo, workers)
- Include validation against known results
- Mention Hugging Face authentication requirement
- Provide complete working examples
- Note v2 compatibility requirements

## Example Response Pattern

When helping with FAIRChem:
1. Identify the chemistry domain (catalysis, materials, molecules, etc.)
2. Select appropriate task_name
3. Choose model based on accuracy/speed requirements
4. Provide complete code with imports
5. Suggest performance optimizations if needed
6. Recommend validation steps
7. Note any domain-specific considerations
