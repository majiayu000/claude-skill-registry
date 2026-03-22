---
name: vasp_ase
description: Professional skill for setting up, executing, and debugging VASP DFT calculations using the Atomic Simulation Environment (ASE).
version: 1.0.0
---

# VASP ASE Skill

This skill allows the agent to interface with VASP on high-performance computing (HPC) systems like the DGX A100. It focuses on using ASE as the wrapper for clean Pythonic control.

## 🛠 Prerequisites
- **Environment Variables:** `VASP_PP_PATH` must point to the directory containing `potpaw_PBE`, etc.
- **Dependencies:** `ase` and `pymatgen` (optional but recommended for analysis) must be installed in the `(base)` conda environment.
- **VASP Executable:** Access to `vasp_std`, `vasp_gam`, or `vasp_ncl`.

## 📜 Execution Instructions

### 1. Setup & Initialization
Always initialize the VASP calculator using the `ase.calculators.vasp.Vasp` class. 
- **Default Check:** If the user doesn't specify, use `xc='PBE'`, `kpts=(4, 4, 4)`, and `encut=520`.
- **Parallelization:** On this DGX system, use `mpirun` or `srun`. Example command: 
  `command='mpirun -np 16 vasp_std > vasp.out'`

### 2. Geometry Optimization Template
```python
from ase.io import read
from ase.calculators.vasp import Vasp
from ase.optimize import BFGS

atoms = read('POSCAR')
calc = Vasp(directory='run_dir',
            command='mpirun -np 16 vasp_std',
            xc='PBE',
            encut=520,
            ismear=0,
            sigma=0.05,
            lreal='Auto',
            nsw=100,
            ibrion=2)
atoms.set_calculator(calc)
energy = atoms.get_potential_energy()
```

### 3. Error Handling & Troubleshooting
If a calculation fails, the agent should parse `OUTCAR` or `stdout` and apply these fixes:

| Error/Issue | Diagnostic | Fix Strategy |
| :--- | :--- | :--- |
| **Electronic Convergence** | `NELM` reached without `dE < ediff` | Set `ALGO = Normal` or `Fast`; increase `NELM` to 100; try `AMIX = 0.2`. |
| **Ionic Convergence** | Max steps reached | Restart from the last `CONTCAR`; check if forces are oscillating. |
| **Memory/A100 Crash** | Segmentation fault | Reduce `NCORE` or `KPAR`; ensure `LREAL = Auto`. |
| **Missing POTCAR** | `RuntimeError: POTCAR not found` | Verify `VASP_PP_PATH` is exported in `~/.bashrc`. |

## 🧪 Validation Step
Before running large productions, the agent should run a "Dry Run" by setting `LSTOP = .TRUE.` in the INCAR or running a single-point energy on a 2-atom cell to verify the environment pathing.

## 📂 Output Management
- Always capture `energy_free`, `forces`, and `stress`.
- Store results in a structured JSON or CSV for the user to download from the DGX server.
```
