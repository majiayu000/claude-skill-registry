---
name: llm-as-computer
description: Execute programs on a compiled transformer stack machine where every instruction fetch and memory read is a parabolic attention head. Demonstrates that transformer attention + FF layers can implement a working computer. Use when user mentions "llm-as-computer", "lac", "stack machine", "compiled transformer", "percepta", "parabolic attention", "execute program", or asks to run/trace programs on the transformer executor.
metadata:
  version: 1.0.1
  repo: oaustegard/llm-as-computer
---

# LLM-as-Computer: Compiled Transformer Stack Machine

A working computer built from transformer primitives. Every instruction fetch and stack read
is a parabolic attention head (dot-product → argmax → value extraction). The transformer's
weights ARE the interpreter — compiled analytically, not trained.

## What This Proves

Attention is lookup; feed-forward is routing. A vanilla transformer with compiled weights
can execute arbitrary programs: loops, recursion, arithmetic, memory access. 55 opcodes
covering WASM i32 semantics. 21M+ steps/second via the Mojo executor.

## Setup (once per session)

```bash
cd /mnt/skills/user/llm-as-computer/src && bash setup.sh
```

This installs Mojo (~20s) and compiles the executor binary (~6s). If Mojo is unavailable,
the skill falls back to a pure-Python executor (slower but functional).

## Usage

```python
import sys
sys.path.insert(0, '/mnt/skills/user/llm-as-computer/src')

from programs import make_fibonacci, make_factorial, make_gcd, make_multiply
from runner import run, setup

# Ensure Mojo is compiled (idempotent)
setup()

# Run a program — shows instructions, trace, result
prog, expected = make_fibonacci(10)
print(run(prog))

# Benchmark mode — measures throughput
print(run(prog, benchmark=True, repeat=200))
```

## Available Programs

From `programs.py` — all return `(program, expected_result)`:

| Generator | Description | Example |
|-----------|-------------|---------|
| `make_fibonacci(n)` | Iterative fib via SWAP+OVER+ADD+ROT | fib(10)=55, 111 steps |
| `make_multiply(a, b)` | Repeated addition | mul(7,8)=56 |
| `make_factorial(n)` | Loop with MUL | fact(8)=40320 |
| `make_gcd(a, b)` | Euclidean algorithm | gcd(48,18)=6 |
| `make_power_of_2(n)` | Repeated doubling | 2^7=128 |
| `make_sum_1_to_n(n)` | Accumulation loop | sum(15)=120 |
| `make_is_even(n)` | Parity check | is_even(7)=0 |
| `make_native_multiply(a,b)` | Single MUL opcode | |
| `make_native_divmod(a,b)` | DIV_S + REM_S | |
| `make_compare_binary(op,a,b)` | eq/ne/lt_s/gt_s/le_s/ge_s | |
| `make_bitwise_binary(op,a,b)` | and/or/xor/shl/shr_u/rotl/rotr | |
| `make_select(a,b,c)` | Conditional select | |

## Writing Custom Programs

```python
from isa_lite import program

# Assembly tuples
prog = program(
    ('PUSH', 10),
    ('PUSH', 20),
    ('ADD',),
    ('DUP',),
    ('ADD',),  # (10+20)*2 = 60
    ('HALT',),
)
print(run(prog))

# Loops: countdown from 5
prog = program(
    ('PUSH', 5),    # 0: counter
    ('PUSH', 1),    # 1: decrement
    ('SUB',),       # 2: counter - 1
    ('DUP',),       # 3: copy for JNZ test
    ('JNZ', 1),     # 4: loop if non-zero
    ('HALT',),      # 5: done, top = 0
)
print(run(prog))
```

## ISA Reference (55 opcodes)

**Stack:** PUSH n, POP, DUP, SWAP, OVER, ROT
**Arithmetic:** ADD, SUB, MUL, DIV_S, DIV_U, REM_S, REM_U
**Comparison:** EQZ, EQ, NE, LT_S/U, GT_S/U, LE_S/U, GE_S/U
**Bitwise:** AND, OR, XOR, SHL, SHR_S/U, ROTL, ROTR
**Unary:** CLZ, CTZ, POPCNT, ABS, NEG, SELECT
**Control:** JZ addr, JNZ addr, CALL addr, RETURN, HALT, NOP
**Locals:** LOCAL.GET idx, LOCAL.SET idx, LOCAL.TEE idx
**Memory:** I32.LOAD, I32.STORE, I32.LOAD8_U/S, I32.LOAD16_U/S, I32.STORE8, I32.STORE16

All arithmetic is 32-bit signed with WASM i32 semantics (wrap on overflow).

## Architecture

The key insight: parabolic encoding `k = (2j, -j²)` makes dot-product attention peak
sharply at a target position. Same encoding addresses program memory, stack, locals,
and heap without interference. Each attention head is a compiled `W_Q @ state → query`,
`W_K @ memory → keys`, `scores = K @ q`, `output = V[argmax(scores)]`.

## Updating from Repo

To pull latest source from the repository:

```bash
cd /mnt/skills/user/llm-as-computer/src
GH_TOKEN=$(grep GH_TOKEN /mnt/project/GitHub.env 2>/dev/null | cut -d= -f2)
for f in executor.mojo; do
  curl -sL -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3.raw" \
    "https://api.github.com/repos/oaustegard/llm-as-computer/contents/src/$f?ref=main" > $f
done
for f in isa_lite.py programs.py runner.py; do
  curl -sL -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3.raw" \
    "https://api.github.com/repos/oaustegard/llm-as-computer/contents/skill/src/$f?ref=main" > $f
done
rm -f percepta_exec  # force recompile
bash setup.sh
```
