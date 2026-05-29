---
name: thermoconductivity
description: Thermal Conductivity (1 sub-skills: lattice-thermal-conductivity)
---

# Thermal Conductivity

## Skills Index

| Skill | Path | Description |
|-------|------|-------------|
| [Lattice Thermal Conductivity](lattice-thermal-conductivity/SKILL.md) | `lattice-thermal-conductivity/` | Compute lattice thermal conductivity via phono3py (BTE), Green-Kubo MD, or QE+phono3py. Covers 2nd/3rd order force constants, linearized Boltzmann transport equation, and heat-flux autocorrelation methods. |

## Method Quick Reference

- **Method A (ASE + MACE + phono3py):** Fastest. Uses MACE ML potential for forces, phono3py for 3rd-order IFCs and BTE solution. Best for rapid screening.
- **Method B (Green-Kubo MD):** Classical MD with MACE. Heat flux autocorrelation integrated via Green-Kubo relation. Good for high-T or strongly anharmonic systems.
- **Method C (QE + phono3py):** DFT-accurate. Uses Quantum ESPRESSO SCF for forces on displaced supercells, phono3py for BTE. Most expensive but most reliable.
