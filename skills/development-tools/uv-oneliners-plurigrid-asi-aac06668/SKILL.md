---
name: uv-oneliners
description: UV/UVX zero-install Python with comma-syntax deps, justfile patterns, PEP 723 scripts
version: 2.0.0
trit: 0
---

# UV One-Liners

> `uv run --python 3.11 --with pkg1,pkg2 script.py` — zero install, instant execution

## Justfile Pattern

```just
py := "uv run --python 3.11"
deps := "--with aiohttp,textual,duckdb,aptos-sdk"
default: play
play: && {{py}} {{deps}} server.py
tui: && {{py}} --with textual,httpx tui.py
```

## One-Liners

```bash
# Data
uv run --with duckdb -c "import duckdb;print(duckdb.sql('SELECT 42').fetchone())"
uv run --with polars -c "import polars as pl;print(pl.DataFrame({'x':[1,2,3]}))"

# Web
uv run --with httpx -c "import httpx;print(httpx.get('https://httpbin.org/ip').json())"
uv run --with fastapi,uvicorn -m uvicorn app:app --reload

# AI
uv run --with google-genai -c "from google import genai;print(genai.Client().models.generate_content(model='gemini-2.5-flash',contents='hi').text)"
uv run --with anthropic -c "from anthropic import Anthropic;print(Anthropic().messages.create(model='claude-sonnet-4-20250514',max_tokens=99,messages=[{'role':'user','content':'hi'}]).content[0].text)"

# Math
uv run --with sympy -c "from sympy import*;x=Symbol('x');print(integrate(sin(x),x))"
uv run --with networkx -c "import networkx as nx;print(nx.petersen_graph())"

# Viz
uv run --with rich -c "from rich import print;print('[bold green]✓[/]')"
uv run --with matplotlib,numpy -c "import matplotlib.pyplot as plt,numpy as np;plt.plot(np.sin(np.linspace(0,6.28,100)));plt.savefig('/tmp/sin.png')"
```

## UVX (No Install)

```bash
uvx ruff check --fix .   # lint
uvx black .              # format
uvx pytest               # test
uvx mypy .               # typecheck
uvx duckdb               # sql repl
uvx jupyter lab          # notebook
uvx marimo edit nb.py    # reactive nb
```

## PEP 723 Inline Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
import httpx; from rich import print
print(httpx.get("https://httpbin.org/ip").json())
```

## Python Version Pinning

```bash
uv run --python 3.11 --with tomllib ...    # 3.11+ stdlib
uv run --python 3.10 --with aptos-sdk ...  # 3.10+ for | unions
```

## Compound Stacks

```bash
uv run --with jax,flax,optax,orbax-checkpoint ml.py
uv run --with transformers,tokenizers,datasets nlp.py
uv run --with httpx,beautifulsoup4,lxml scrape.py
uv run --with aptos-sdk,web3,eth-account chain.py
uv run --with discopy,catgrad,networkx cat.py
```

## GF(3) Tripartite

```bash
uv run --with numpy -c "
for t in [-1,0,1]: print(f'trit={t:+d} hue={[270,180,30][t+1]}°')
print('sum=0 ✓')
"
```

## Skill Lattice Position

```
         uv-discohy (toolchain + operad)
              │
    ┌─────────┼─────────┐
    │         │         │
uv-oneliners  │    ruff/black
 (execution)  │    (linting)
              │
         pyproject.toml
```

## Triad: uv-oneliners + acsets + gay-mcp

| Skill | Trit | Role |
|-------|------|------|
| uv-oneliners | 0 | Coordinator (execution) |
| acsets | 0 | Coordinator (schema) |
| gay-mcp | +1 | Generator (colors) |

Needs `-1` skill to balance: `three-match`, `skill-validation-gf3`



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
uv-oneliners (○) + SDF.Ch4 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch2: Domain-Specific Languages

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
## Cat# Integration

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
```
