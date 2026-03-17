---
name: packmol
description: This skill should be used when the user asks to "create a packmol input", "pack molecules with packmol", "solvate a protein", "build an initial configuration", "setup molecular dynamics", or discusses molecular packing, solvation, or building simulation starting structures.
version: 1.0.0
---

# Packmol Skill

Build initial configurations for molecular dynamics simulations using Packmol.

## What is Packmol?

Packmol creates initial configurations for MD simulations by packing molecules according to spatial constraints. It places molecules in boxes, around proteins, at interfaces, or within complex geometries (spheres, cylinders, ellipsoids) while ensuring no overlaps.

## Installation

Install Packmol via pip:

```bash
pip install packmol
```

Verify installation:

```bash
packmol -h
```

For more installation options, see the [Packmol website](https://m3g.github.io/packmol/).

## Quick Start

### Basic Box Packing

Create a simple box of water molecules:

```text
# water_box.inp
tolerance 2.0
filetype pdb
output water_box.pdb

structure water.pdb
  number 1000
  inside box 0. 0. 0. 40. 40. 40.
end structure
```

Run Packmol:

```bash
packmol < water_box.inp
```

### Solvate a Protein

Solvate a protein with water and ions:

```text
# solvation.inp
tolerance 2.0
filetype pdb
output solvated.pdb

structure protein.pdb
  number 1
  fixed 0. 0. 0. 0. 0. 0.
  center
end structure

structure water.pdb
  number 5000
  inside box -10. -10. -10. 50. 50. 50.
end structure

structure SOD.pdb
  number 10
  inside box -10. -10. -10. 50. 50. 50.
end structure

structure CLA.pdb
  number 10
  inside box -10. -10. -10. 50. 50. 50.
end structure
```

### Liquid-Liquid Interface

Build a water/chloroform interface:

```text
# interface.inp
tolerance 2.0
filetype pdb
output interface.pdb
pbc -20. -20. -30. 20. 20. 30.

structure water.pdb
  number 1000
  below plane 0. 0. 1. 0.
end structure

structure chloroform.pdb
  number 200
  above plane 0. 0. 1. 0.
end structure
```

## Core Concepts

### Input File Structure

Every Packmol input file requires:

1. **tolerance**: Minimum distance between atoms (Å)
2. **output**: Output filename
3. **filetype**: Format (pdb, xyz, tinker)
4. **structure blocks**: Define molecules to place

### Structure Block Syntax

```text
structure molecule.pdb
  number <N>                          # Number of molecules
  inside|outside <constraint>         # Spatial constraint
  [optional parameters]
end structure
```

### Common Constraint Types

- **box**: `inside box xmin ymin zmin xmax ymax zmax`
- **sphere**: `inside sphere xcenter ycenter zcenter radius`
- **cylinder**: `inside cylinder x1 y1 z1 dx dy dz radius length`
- **plane**: `above plane a b c d` or `below plane a b c d`
- **ellipsoid**: `inside ellipsoid xc yc zc xa yb zc scale`

See [references/constraints.md](references/constraints.md) for complete constraint documentation.

## Workflows

### 1. Basic Molecular Packing

Build boxes with multiple molecule types.

**Example**: Water/ethanol mixture

```text
tolerance 2.0
output mixture.pdb
filetype pdb

structure water.pdb
  number 800
  inside box 0. 0. 0. 40. 40. 40.
end structure

structure ethanol.pdb
  number 200
  inside box 0. 0. 0. 40. 40. 40.
end structure
```

### 2. Protein Solvation

Solvate biomolecules with water and ions for neutralization.

**Key parameters**:
- Use `fixed` with `center` for the protein
- Add Na+/Cl- ions for neutrality and concentration
- Calculate box size based on protein + solvent shell

**Automatic solvation helper**:

```bash
python scripts/solvate_helper.py protein.pdb --shell 15.0 --charge +4
```

### 3. Interface Systems

Build liquid-liquid or liquid-vapor interfaces using plane constraints.

**Example**: Water/hexane interface

```text
tolerance 2.0
output interface.pdb
pbc -20. -20. -30. 20. 20. 30.

structure water.pdb
  number 1000
  below plane 0. 0. 1. 0.
end structure

structure hexane.pdb
  number 200
  above plane 0. 0. 1. 0.
end structure
```

### 4. Advanced Constraints

Use spherical, cylindrical, or ellipsoidal constraints for complex geometries.

**Example**: Spherical vesicle

```text
structure lipid.pdb
  number 2000
  inside sphere 0. 0. 0. 40.
  atoms 1 2 3 4
    outside sphere 0. 0. 0. 35.
  end atoms
end structure

structure water.pdb
  number 2000
  inside sphere 0. 0. 0. 35.
end structure

structure water.pdb
  number 5000
  outside sphere 0. 0. 0. 45.
end structure
```

## Input Parameters

### Required Parameters

- **tolerance** `<distance>`: Minimum intermolecular distance (Å). Default: 2.0 for all-atom
- **output** `<filename>`: Output file name
- **filetype** `<format>`: pdb, xyz, or tinker

### Optional Parameters

- **pbc** `<dimensions>`: Periodic boundary conditions (e.g., `pbc 30. 30. 60.`)
- **seed** `<integer>`: Random seed for reproducibility
- **discale** `<factor>`: Distance scaling for optimization (default: 1.0)
- **maxit** `<N>`: Maximum iterations (default: 20)
- **precision** `<value>`: Convergence precision (default: 0.01)

See [references/parameters.md](references/parameters.md) for complete parameter reference.

## Structure Block Options

### Positioning Options

- **number**: Molecule count
- **inside/outside**: Spatial constraint
- **fixed**: Fix position and rotation (6 parameters: x, y, z, α, β, γ)
- **center**: Use center of mass for positioning

### Rotation Constraints

```text
constrain_rotation x 180. 20.  # Constrain rotation around x-axis
constrain_rotation y 180. 20.  # Constrain rotation around y-axis
constrain_rotation z 180. 20.  # Constrain rotation around z-axis
```

### Atom Selection

Apply constraints to specific atoms within molecules:

```text
structure molecule.pdb
  number 100
  inside box 0. 0. 0. 30. 30. 30.
  atoms 1 2 3
    inside box 0. 0. 25. 30. 30. 30.
  end atoms
end structure
```

## Running Packmol

### Basic Execution

```bash
packmol < input.inp
```

### Output Interpretation

Success message:

```
------------------------------
Success!
Final objective function value: .22503E-01
Maximum violation of target distance: 0.000000
Maximum violation of the constraints: .78985E-02
------------------------------
```

Check that both violations are < 0.01 for a valid solution.

## Validation

### Check Overlaps

```bash
python scripts/check_overlaps.py output.pdb --tolerance 2.0
```

### Verify Success

```bash
python scripts/verify_success.py input.inp output.pdb
```

### Analyze Density

```bash
python scripts/analyze_density.py output.pdb
```

### Validate Input

```bash
python scripts/validate_input.py input.inp
```

## Troubleshooting

### Common Issues

1. **"Killed" error**: System too large
   - Reduce number of molecules
   - Use restart files to build incrementally
   - See [references/troubleshooting.md](references/troubleshooting.md)

2. **No convergence**:
   - Try `discale 1.5` to scale distances
   - Reduce molecule count
   - Simplify constraints
   - Increase `maxit`

3. **Strange geometries**:
   - Add `check` keyword to validate constraints without packing
   - Verify constraint syntax
   - Check for conflicting constraints

4. **Incorrect atom count**:
   - Verify structure files are readable
   - Check for duplicate atoms in input files
   - Validate with `scripts/validate_input.py`

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions.

## Examples

Explore example input files in the `examples/` directory:

- **Basic**: [examples/basic/](examples/basic/) - Simple boxes and mixtures
- **Solvation**: [examples/solvation/](examples/solvation/) - Proteins with water and ions
- **Interface**: [examples/interface/](examples/interface/) - Liquid-liquid interfaces
- **Advanced**: [examples/advanced/](examples/advanced/) - Vesicles, bilayers, complex geometries

## Templates

Use templates in `templates/` as starting points:

- **[templates/basic_template.inp](templates/basic_template.inp)**: Minimal template for simple packing
- **[templates/solvation_template.inp](templates/solvation_template.inp)**: Protein solvation setup
- **[templates/interface_template.inp](templates/interface_template.inp)**: Interface systems

## Helper Scripts

Use Python scripts in `scripts/` for automation:

- **generate_input.py**: Generate inputs programmatically
- **validate_input.py**: Validate input syntax before running
- **check_overlaps.py**: Detect atomic overlaps in output
- **analyze_density.py**: Calculate system density
- **solvate_helper.py**: Automatic protein solvation setup
- **verify_success.py**: Verify Packmol completed successfully

## Advanced Topics

### Periodic Boundary Conditions

Use `pbc` for periodic systems:

```text
pbc 30. 30. 60.  # or pbc xmin ymin zmin xmax ymax zmax
```

### Restart Files

Build large systems incrementally:

```text
structure water.pdb
  number 1000
  inside box 0. 0. 0. 40. 40. 40.
  restart_to water1.pack
end structure
```

Then restart:

```text
structure water.pdb
  number 1000
  restart_from water1.pack
end structure
```

### Atom-Specific Radii

Set different radii for multiscale models:

```text
structure molecule.pdb
  number 100
  radius 1.5  # All atoms
end structure

structure molecule.pdb
  number 100
  atoms 1 2
    radius 1.5  # Specific atoms
  end atoms
end structure
```

### Constraint Validation

Validate constraints without packing:

```text
structure molecule.pdb
  number 100
  inside box 0. 0. 0. 30. 30. 30.
  check
end structure
```

## Best Practices

1. **Start simple**: Test with few molecules before scaling up
2. **Use appropriate tolerance**: 2.0 Å for all-atom, larger for coarse-grained
3. **Check constraints**: Add `check` keyword to validate regions
4. **Validate output**: Use scripts to check overlaps and density
5. **Reproducibility**: Set `seed` for repeatable results
6. **Large systems**: Use restart files or build in stages
7. **Box size**: Allow 10-15 Å padding around solutes for solvation

## Tips for Common Use Cases

### Protein Solvation

- Add 10-15 Å solvent shell around protein
- Calculate ions for neutrality: `N_ions = charge / e`
- Add salt ions for desired concentration (e.g., 0.15 M NaCl)
- Use `fixed` with `center` for protein positioning

### Mixed Solvents

- Calculate total number of molecules from desired molar ratios
- Use same tolerance for all components
- Test with small systems first

### Membrane Systems

- Use `constrain_rotation` to orient lipids
- Build in stages: lipids first, then water
- Consider using specialized membrane builders for large systems

### Nanotubes/Pores

- Use `cylinder` constraint for pore region
- Combine with `outside` constraint for bulk region
- May need atom selection for specific molecule orientations

## Resources

- Official documentation: [Packmol User Guide](https://m3g.github.io/packmol/userguide.shtml)
- Examples: [Packmol Examples](https://m3g.github.io/packmol/examples.shtml)
- GitHub: [Packmol Repository](https://github.com/m3g/packmol)
- Paper: [Martínez et al. J Comput Chem 2009](https://doi.org/10.1002/jcc.21224)

## References

For detailed information on specific topics, see:

- [constraints.md](references/constraints.md) - Complete constraint syntax and examples
- [parameters.md](references/parameters.md) - All input parameters and options
- [file_formats.md](references/file_formats.md) - File format specifications
- [troubleshooting.md](references/troubleshooting.md) - Problem-solving guide
