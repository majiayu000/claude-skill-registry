---
name: sagemath
description: Run SageMath computations through the existing Anaconda environment named `sage`. Use when Codex needs Sage for CTF and cryptography work such as asymmetric cryptography, finite fields, elliptic curves, lattices, polynomial algebra, modular arithmetic, discrete logs, small-root attacks, or PRNG cryptanalysis, and when execution should happen from inline code or a `.sage` file instead of plain Python.
---

# OpenCROW Runner - SageMath

Use this skill to execute SageMath reliably from the local conda environment `sage`.

## Quick Start

Use the bundled runner:

```bash
python ~/.codex/skills/sagemath/scripts/run_sage.py --code 'print(factor(2^20 - 1))'
```

Or execute an existing `.sage` file:

```bash
python ~/.codex/skills/sagemath/scripts/run_sage.py --file /absolute/path/to/script.sage
```

## Workflow

1. Decide whether the task is best expressed as inline code or a `.sage` file.
2. For small one-off computations, pass the code with `--code`.
3. For longer programs or reusable work, create a `.sage` file and pass it with `--file`.
4. For CTF crypto tasks, prefer Sage when the problem involves polynomial rings, finite fields, matrices over modular domains, lattices, or symbolic number theory operations.
5. Review stdout/stderr from SageMath and report the meaningful result back to the user.

## Runner Notes

- The runner always invokes `conda run -n sage sage`.
- For `--code`, the runner writes the code into a temporary `.sage` file first. This avoids quoting issues and keeps behavior aligned with file execution.
- Pass `--timeout SECONDS` when a computation may hang or run too long.
- Pass `--keep-temp` only when debugging generated Sage code.

## Patterns

For inline calculations:

```bash
python ~/.codex/skills/sagemath/scripts/run_sage.py --code '
R.<x> = QQ[]
f = x^4 - 1
print(f.factor())
'
```

For file-based workflows:

1. Create a `.sage` file in the workspace.
2. Run it with the bundled runner.
3. If the script generates files, verify the outputs before replying.

For CTF cryptography workflows:

- Use Sage integer and modular arithmetic for RSA attacks, CRT reconstruction, inverses, and exponent relations.
- Use polynomial rings and `small_roots()` for Coppersmith-style attacks when the instance is suitable.
- Use `GF(p)` or extension fields for ECC, finite-field equations, and structured algebraic recovery.
- Use `Matrix`, `vector`, and LLL for lattice-based recovery problems and hidden-number style attacks.
- Use recurrence solving, modular equations, and matrix lifting for LCG, xorshift, and related PRNG state recovery when Sage algebra is useful.

## References

- For CTF-oriented patterns and starter snippets, read [references/ctf-crypto.md](references/ctf-crypto.md) when the task involves RSA, ECC, lattices, or PRNG cryptanalysis.

## Templates

- Copy or adapt [rsa-starter.sage](assets/templates/rsa-starter.sage) for modular arithmetic, CRT, and private-exponent recovery tasks.
- Copy or adapt [ecc-starter.sage](assets/templates/ecc-starter.sage) for finite-field and elliptic-curve exploration.
- Copy or adapt [lattice-lll-starter.sage](assets/templates/lattice-lll-starter.sage) for integer-lattice and hidden-structure attacks.
- Copy or adapt [lcg-state-recovery.sage](assets/templates/lcg-state-recovery.sage) for linear congruential generator recovery.
- Copy or adapt [xorshift-linear-model.sage](assets/templates/xorshift-linear-model.sage) for GF(2)-linear xorshift modeling.
- Copy or adapt [mersenne-twister-state-tools.sage](assets/templates/mersenne-twister-state-tools.sage) for MT19937 tempering and state-word recovery work.
- Copy or adapt [mt19937-partial-state-starter.sage](assets/templates/mt19937-partial-state-starter.sage) for partial-state or masked-bit MT analysis.
- Copy or adapt [mt19937-full-state-recovery.sage](assets/templates/mt19937-full-state-recovery.sage) for full 624-word MT state reconstruction from outputs.
- Copy or adapt [rsa-small-root-starter.sage](assets/templates/rsa-small-root-starter.sage) for Coppersmith-style experimentation with `small_roots()`.
- Copy or adapt [rsa-boneh-durfee-starter.sage](assets/templates/rsa-boneh-durfee-starter.sage) for low-private-exponent setup and polynomial construction.
- Copy or adapt [hidden-number-lattice-starter.sage](assets/templates/hidden-number-lattice-starter.sage) for nonce-bias and hidden-number lattice setups.
- Copy or adapt [ecdsa-nonce-reuse-starter.sage](assets/templates/ecdsa-nonce-reuse-starter.sage) for same-nonce ECDSA private-key recovery.
- Copy or adapt [ecdsa-partial-nonce-lattice-starter.sage](assets/templates/ecdsa-partial-nonce-lattice-starter.sage) for biased or partially leaked nonce lattice attacks.
- Copy or adapt [lcg-truncated-output-starter.sage](assets/templates/lcg-truncated-output-starter.sage) for recovering LCG state from high-bit leaks.

## Resource

### scripts/run_sage.py

Use this script instead of calling SageMath manually unless there is a specific reason not to. It standardizes environment selection, timeout handling, and inline-code execution.
