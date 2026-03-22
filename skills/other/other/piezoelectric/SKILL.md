---
name: piezoelectric
description: Piezoelectric Properties (1 sub-skills: piezoelectric-tensor)
---

# Piezoelectric Properties

## Skills Index

| Skill | Path | Description |
|-------|------|-------------|
| [Piezoelectric Tensor](piezoelectric-tensor/SKILL.md) | `piezoelectric-tensor/` | Compute the full piezoelectric stress tensor e_ij via Berry phase polarization under finite strain using Quantum ESPRESSO. Covers clamped-ion and relaxed-ion contributions. |

## Method Quick Reference

- **QE Berry Phase:** Apply finite strains (6 Voigt components), compute polarization via Berry phase (`lberry=.true.`), differentiate to get e_ij = dP_i/deps_j. Gold-standard DFT approach.
- Supports clamped-ion (electronic only) and relaxed-ion (electronic + ionic) decomposition.
- Common target materials: ZnO, BaTiO3, AlN, GaN, PbTiO3.
