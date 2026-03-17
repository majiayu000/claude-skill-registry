---
name: aads-training-lifecycle
description: Maintain AADS-ULoRA phase1, phase2, and phase3 training behavior plus adapter lifecycle invariants across local and Colab flows. Use for training logic, freezing rules, retention/OOD threshold behavior, and phase3 runtime or component updates.
---

# AADS Training Lifecycle

## Workflow

1. Identify phase scope.
- Determine whether change targets Phase 1, 2, 3, or cross-phase behavior.
- Load `references/training-invariants.md`.

2. Preserve lifecycle invariants.
- Preserve expected freezing and adaptation semantics.
- Preserve OOD-threshold path compatibility with adapters.
- Preserve phase3 runtime/component contract behavior.

3. Enforce local/Colab parity.
- Review paired local and `colab_*` trainer variants when behavior changes.
- Include notebook/script entrypoint checks when user-facing training flow changes.

4. Run phase-aligned validation.
- Run targeted training unit tests.
- Run Colab smoke training checks when applicable.
- Add integration checks only when required.

5. Emit training delta summary.
- Report phase-wise behavior changes and invariants status.

## Output Contract

Return sections in this order:
1. Phase scope
2. Files changed
3. Invariants preserved/changed
4. Validation commands and results
5. Risks and follow-up checks
6. Local-Colab parity notes

## References

- Read `references/training-invariants.md` before implementing.
