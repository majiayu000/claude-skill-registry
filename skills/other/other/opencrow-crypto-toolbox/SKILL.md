---
name: opencrow-crypto-toolbox
description: Use the Anaconda `ctf` environment and installed crypto tooling for CTF tasks that fit normal Python or CLI cracking rather than SageMath. Use when Codex needs `z3`, `fpylll`, `pycryptodome`, `hashcat`, `john`, or quick FactorDB lookups.
---

# OpenCROW Crypto Toolbox

Prefer the `opencrow-crypto-mcp` server for typed crypto workflows. Fall back to the direct scripts only when you need to debug the underlying `ctf`-environment execution path.

## MCP First

- Use `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities` first.
- Use the typed crypto operations:
  - `crypto_python`
  - `crypto_factordb_lookup`
  - `crypto_crack_hash`
- Treat the existing helper scripts as the implementation fallback, not the primary interface.

Use this skill for Python-first crypto work in the `ctf` environment plus the cracking and lookup tools that commonly complement it. This covers SMT constraints with `z3`, lattice work with `fpylll`, implementation helpers with `pycryptodome`, offline cracking with `hashcat` or `john`, and quick FactorDB checks.

## Quick Start

Run inline Python in `ctf`:

```bash
python ~/.codex/skills/opencrow-crypto-toolbox/scripts/run_crypto_python.py --code 'from z3 import *; x = BitVec("x", 32); s = Solver(); s.add(x ^ 0x1337 == 0x1234); print(s.check()); print(s.model())'
```

Run a solver file:

```bash
python ~/.codex/skills/opencrow-crypto-toolbox/scripts/run_crypto_python.py --file /absolute/path/to/solve.py
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-crypto-toolbox/scripts/verify_toolkit.py
```

Query FactorDB quickly:

```bash
python ~/.codex/skills/opencrow-crypto-toolbox/scripts/factordb_lookup.py 999630013489
```

## Workflow

1. Use this toolbox when the job is mostly Python, constraints, lattices, or byte-level crypto helpers.
2. Use `run_crypto_python.py --code` for short experiments and `--file` for real solve scripts.
3. Reach for `z3` when the challenge is equation- or bit-vector-driven.
4. Reach for `fpylll` when the attack is lattice-driven and does not require Sage.
5. Reach for `pycryptodome` when you need standard primitives, block modes, or protocol glue in Python.
6. Reach for `hashcat` or `john` when the fastest path is cracking rather than symbolic recovery.
7. Read [references/tooling.md](references/tooling.md) if you need a quick selection guide.

## Tool Selection

- Use `z3` for SAT/SMT solving, bit-vectors, modular constraints, and key-recovery models that can be expressed symbolically.
- Use `fpylll` for LLL/BKZ lattice reduction, CVP experiments, and short-vector workflows in plain Python.
- Use `pycryptodome` for AES, RSA helpers, hashes, MACs, padding, byte parsing, and challenge protocol implementation.
- Use `hashcat` for local cracking workloads and mask, rule, or wordlist-based attacks.
- Use `john` when a format is better supported by John or when you want a lighter cracking loop.
- Use `factordb_lookup.py` for quick sanity checks against known integer factorizations before committing to local factoring work.
- Use standard Python libraries in the same script for parsing challenge formats, padding oracles, byte wrangling, and protocol glue.
- Switch to `sagemath` when the task needs finite fields, elliptic curves, polynomial rings, or Sage-native attack code.

## Resources

- `scripts/run_crypto_python.py`: execute inline code or a `.py` file inside the `ctf` environment.
- `scripts/verify_toolkit.py`: confirm that the crypto-specific Python modules are available.
- `scripts/factordb_lookup.py`: look up known factors through the public FactorDB API.
- `references/tooling.md`: quick guidance on when to stay in Python crypto tooling versus switching to Sage.
