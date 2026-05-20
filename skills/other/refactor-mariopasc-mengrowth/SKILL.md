---
name: refactor
description: Refactor Python modules for production quality
---

# Python Module Refactoring

You are a world-class Python engineer. Refactor the target module following these rules strictly:

## Checklist (ALL must be satisfied)
- [ ] No hardcoded values — all config via OmegaConf/Hydra YAML
- [ ] Type hints on every function signature and return type
- [ ] Google-style docstrings on all public functions/classes
- [ ] Shape assertions at tensor function boundaries
- [ ] Atomic function design (one conceptual task per function)
- [ ] Prefer library calls (MONAI, einops, torch.nn.functional) over manual implementations
- [ ] Logging via Python `logging` module (no print statements)
- [ ] Custom exceptions for domain-specific errors
- [ ] @dataclass for configuration containers
- [ ] Numerical guard clauses (epsilon clamping where division occurs)

## Process
1. Read the target file completely
2. Identify all violations of the checklist
3. Propose the refactoring plan (what changes and why)
4. Implement the refactoring
5. Run: `~/.conda/envs/mengrowth/bin/python -m py_compile <file>` to verify
6. Run: `~/.conda/envs/mengrowth/bin/python -m pytest tests/ -x -q` if relevant tests exist

$ARGUMENTS
