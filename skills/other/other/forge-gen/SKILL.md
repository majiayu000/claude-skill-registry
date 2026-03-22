---
name: forge-gen
description: Use when working on forge generation, body creation, scoring, stage math, zero-forcing, vocabulary, quick-roll, body-skeleton plans, solver, resonator generation, or any code in trench-forge/
---

Before writing any code, read these files:
- `docs/context/forge-direction.md` — current priorities and root diagnosis
- `docs/context/zero-forcing.md` — why bodies are flat and the fix plan

Key constraints:
- Generation starts from a body-skeleton plan, not independent stages
- Zero-forcing for character filters, not RBJ cookbook
- All forge code uses 39062.5 Hz. Never 44100.
- Dramatic movement is a ranking signal, not a gate
- Read `trench-forge/CLAUDE.md` for stage types, compilation rules, and key files

Key source files:
- `trench-forge/src/resonator_gen.rs` — resonator generation pipeline
- `trench-forge/src/solver.rs` — greedy solver
- `trench-forge/src/stage_math.rs` — stage mathematics
- `trench-forge/src/scorer/` — scoring subsystem (composite, coherence, content, profile)
- `trench-forge/src/counterpoint.rs` — counterpoint logic
- `trench-forge/src/designer.rs` — morph designer bridge
- `trench-forge/src/hyper.rs` — hyper-cartridge format
