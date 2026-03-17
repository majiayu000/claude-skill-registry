---
name: uv-oneliners
description: UV/UVX awesome one-liners for ephemeral Python environments with multi-package
  stacks
metadata:
  source: astral-sh/uv + gemini-cookbook patterns
  trit: +1 (PLUS - generative)
  seed: 1069
---

# UV One-Liners Skill

> *Zero-install Python execution with arbitrary package combinations*

## Core Concept

`uv run --with pkg1 --with pkg2 script.py` creates ephemeral environments on-the-fly.
No virtualenv setup, no requirements.txt, just instant execution.

## Awesome One-Liners

### 🧠 AI/ML Stack

```bash
# Gemini + structured output
uv run --with google-genai --with pydantic -c "
from google import genai
from pydantic import BaseModel
client = genai.Client()
print(client.models.generate_content(model='gemini-2.5-flash', contents='Hello!').text)
"

# DisCoPy + JAX categorical ML
uv run --with discopy --with jax --with matplotlib -c "
from discopy import Ty, Box, Diagram
x = Ty('x')
f = Box('f', x, x)
print((f >> f).draw())
"

# Hy (Lisp on Python) + NumPy
uv run --with hy --with numpy -c "
import hy.cmdline
hy.cmdline.hy_main(['-c', '(import numpy :as np) (print (np.array [1 2 3]))'])
"

# JAX + Equinox neural nets
uv run --with jax --with equinox --with optax -c "
import jax.numpy as jnp
import equinox as eqx
print('JAX devices:', jax.devices())
"
```

### 🎨 Visualization

```bash
# Quick matplotlib plot
uv run --with matplotlib --with numpy -c "
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.savefig('/tmp/sine.png')
print('Saved to /tmp/sine.png')
"

# Penrose diagrammatic rendering
uv run --with penrose -c "
print('Penrose installed, ready for diagramming')
"

# Rich terminal formatting
uv run --with rich -c "
from rich import print
from rich.panel import Panel
print(Panel('[bold green]UV One-Liners[/bold green]', title='Skill'))
"
```

### 📊 Data Processing

```bash
# DuckDB instant analytics
uv run --with duckdb -c "
import duckdb
print(duckdb.sql('SELECT 42 as answer').fetchall())
"

# Polars dataframes
uv run --with polars -c "
import polars as pl
df = pl.DataFrame({'a': [1,2,3], 'b': ['x','y','z']})
print(df)
"

# Pandas + pyarrow
uv run --with pandas --with pyarrow -c "
import pandas as pd
print(pd.DataFrame({'col': range(5)}))
"
```

### 🔧 Development Tools

```bash
# Ruff linting (via uvx)
uvx ruff check --fix .

# Black formatting
uvx black --check .

# MyPy type checking
uvx mypy script.py

# Pytest with coverage
uv run --with pytest --with pytest-cov -m pytest --cov=.
```

### 🌐 Web & API

```bash
# FastAPI instant server
uv run --with fastapi --with uvicorn -c "
import uvicorn
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_root(): return {'uv': 'awesome'}
# uvicorn.run(app, host='0.0.0.0', port=8000)
print('FastAPI ready')
"

# httpx async requests
uv run --with httpx -c "
import httpx
r = httpx.get('https://httpbin.org/get')
print(r.json()['origin'])
"

# Playwright browser automation
uvx playwright install chromium
uv run --with playwright -c "
from playwright.sync_api import sync_playwright
print('Playwright ready for browser automation')
"
```

### 🔬 Scientific Computing

```bash
# SymPy symbolic math
uv run --with sympy -c "
from sympy import symbols, integrate, sin
x = symbols('x')
print(integrate(sin(x), x))
"

# SciPy optimization
uv run --with scipy --with numpy -c "
from scipy.optimize import minimize
result = minimize(lambda x: x**2, x0=5)
print(f'Minimum at x={result.x[0]:.4f}')
"

# NetworkX graph theory
uv run --with networkx --with matplotlib -c "
import networkx as nx
G = nx.petersen_graph()
print(f'Petersen graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges')
"
```

### 🎵 Audio/Music

```bash
# Music21 analysis
uv run --with music21 -c "
from music21 import note, stream
s = stream.Stream()
s.append(note.Note('C4'))
print(s)
"

# Librosa audio processing  
uv run --with librosa --with numpy -c "
import librosa
print(f'Librosa version: {librosa.__version__}')
"
```

### 🧬 Category Theory / Type Theory

```bash
# DisCoPy string diagrams
uv run --with discopy -c "
from discopy.monoidal import Ty, Box
from discopy.drawing import Equation
s, n = Ty('s'), Ty('n')
Alice = Box('Alice', Ty(), n)
loves = Box('loves', n @ n, s)
Bob = Box('Bob', Ty(), n)
sentence = Alice @ Bob >> loves
print(sentence)
"

# Catgrad categorical gradients
uv run --with catgrad -c "
print('Catgrad: Categorical approach to automatic differentiation')
"

# typing_extensions for advanced types
uv run --with typing_extensions -c "
from typing_extensions import TypeVarTuple, Unpack
print('Advanced typing available')
"
```

## Tripartite Gemini Video Processing

```bash
# Install google-genai
uv run --with google-genai --with opencv-python --with numpy -c "
from google import genai
import cv2
import numpy as np

# Three interleaved analysis streams (GF(3) conservation)
PROMPTS = {
    -1: 'MINUS: What constraints/errors/problems do you see?',
     0: 'ERGODIC: Describe the overall flow and balance.',
    +1: 'PLUS: What opportunities/improvements/creative ideas emerge?'
}

print('Tripartite video analysis ready')
print('Streams:', list(PROMPTS.values()))
"
```

## Full Tripartite Video Script

```bash
# Save and run this
cat > /tmp/tripartite_video.py << 'EOF'
#!/usr/bin/env python3
"""
Tripartite Video Analysis with Gemini
GF(3) Interleaved Streams: MINUS, ERGODIC, PLUS
"""
import os
import sys
import time
from dataclasses import dataclass
from typing import Iterator

# SplitMix64 for deterministic colors
class SplitMix64:
    def __init__(self, seed: int = 0x42D):
        self.state = seed & ((1 << 64) - 1)
    
    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & ((1 << 64) - 1)
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & ((1 << 64) - 1)
        return z ^ (z >> 31)
    
    def next_trit(self) -> int:
        return (self.next() % 3) - 1

@dataclass
class TripartiteStream:
    """One of three interleaved analysis streams"""
    name: str
    trit: int  # -1, 0, +1
    prompt: str
    color_hue: float  # OkLCH hue
    
STREAMS = [
    TripartiteStream("MINUS", -1, 
        "Identify constraints, errors, problems, inconsistencies in this frame.",
        270),  # Purple
    TripartiteStream("ERGODIC", 0,
        "Describe the balance, flow, overall composition of this frame.",
        180),  # Cyan
    TripartiteStream("PLUS", +1,
        "Suggest improvements, creative opportunities, positive observations.",
        30),   # Orange
]

def interleave_streams(n_frames: int, seed: int = 0x42D) -> Iterator[tuple]:
    """Yield (frame_idx, stream) in GF(3)-conserving order"""
    rng = SplitMix64(seed)
    for i in range(n_frames):
        trit = rng.next_trit()
        stream = STREAMS[trit + 1]  # Map {-1,0,1} to {0,1,2}
        yield i, stream

def analyze_video(video_path: str, api_key: str = None):
    """Analyze video with tripartite Gemini streams"""
    from google import genai
    
    api_key = api_key or os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Set GOOGLE_API_KEY environment variable")
        return
    
    client = genai.Client(api_key=api_key)
    
    # Upload video
    print(f"Uploading {video_path}...")
    video_file = client.files.upload(file=video_path)
    
    while video_file.state == "PROCESSING":
        print("Processing...")
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
    
    print(f"Video ready: {video_file.uri}")
    
    # Tripartite analysis
    results = {-1: [], 0: [], 1: []}
    
    for stream in STREAMS:
        print(f"\n{'='*60}")
        print(f"  {stream.name} (trit={stream.trit:+d}) | Hue={stream.color_hue}°")
        print(f"{'='*60}")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[video_file, stream.prompt]
        )
        
        print(response.text[:500])
        results[stream.trit].append(response.text)
    
    # GF(3) conservation check
    trit_sum = sum(len(r) for r in results.values()) % 3
    print(f"\nGF(3) Balance: {trit_sum} {'✓' if trit_sum == 0 else '○'}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tripartite_video.py <video.mp4>")
        print("\nExample:")
        print("  uv run --with google-genai tripartite_video.py video.mp4")
    else:
        analyze_video(sys.argv[1])
EOF

# Run it
uv run --with google-genai /tmp/tripartite_video.py
```

## UVX Tools (No Script Needed)

```bash
# Code formatting
uvx black .
uvx isort .
uvx ruff check --fix .

# Type checking
uvx mypy .
uvx pyright .

# Documentation
uvx mkdocs serve
uvx pdoc --html .

# Jupyter
uvx jupyter lab
uvx marimo edit notebook.py

# Database tools
uvx pgcli postgres://...
uvx litecli database.db
uvx duckdb

# HTTP
uvx httpie GET https://api.example.com
uvx curlie https://httpbin.org/get
```

## Compound Stacks (Copy-Paste Ready)

```bash
# Full ML stack
uv run --with jax --with flax --with optax --with orbax-checkpoint script.py

# NLP stack  
uv run --with transformers --with tokenizers --with datasets --with accelerate script.py

# Visualization stack
uv run --with matplotlib --with seaborn --with plotly --with altair script.py

# Web scraping stack
uv run --with httpx --with beautifulsoup4 --with lxml --with selectolax script.py

# Category theory stack
uv run --with discopy --with catgrad --with networkx script.py

# Audio stack
uv run --with librosa --with soundfile --with pydub --with music21 script.py
```

## Environment Variables

```bash
# Set Gemini API key
export GOOGLE_API_KEY="your-key-here"

# Use with uv
uv run --with google-genai -c "
import os
from google import genai
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
print(client.models.generate_content(model='gemini-2.5-flash', contents='Hi!').text)
"
```

## Integration with Gay-MCP

```bash
# Tripartite color generation
uv run --with numpy -c "
import numpy as np

def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & ((1 << 64) - 1)
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & ((1 << 64) - 1)
    return z ^ (z >> 31), state

seed = 0x42D
for i in range(9):
    val, seed = splitmix64(seed)
    trit = (val % 3) - 1
    hue = {-1: 270, 0: 180, 1: 30}[trit]
    print(f'Frame {i}: trit={trit:+d} hue={hue}° oklch(0.65 0.18 {hue})')
"
```

## Gemini Cookbook Examples (via UV)

From [gemini-cookbook](https://github.com/google-gemini/cookbook):

```bash
# Video understanding
uv run --with google-genai --with rich -- python -c "
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# Direct YouTube analysis
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=types.Content(
        parts=[
            types.Part(text='Summarize this video in 3 bullets'),
            types.Part(file_data=types.FileData(
                file_uri='https://www.youtube.com/watch?v=ixRanV-rdAQ'
            ))
        ]
    )
)
print(response.text)
"

# Image analysis
uv run --with google-genai --with httpx -- python -c "
from google import genai
import os, httpx, base64

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
img = httpx.get('https://picsum.photos/800/600').content

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Describe this image', {'mime_type': 'image/jpeg', 'data': base64.b64encode(img).decode()}]
)
print(response.text)
"

# Function calling
uv run --with google-genai -- python -c "
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

tools = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name='get_weather',
        description='Get weather for a location',
        parameters={'type': 'object', 'properties': {'location': {'type': 'string'}}}
    )
])]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='What is the weather in Tokyo?',
    config=types.GenerateContentConfig(tools=tools)
)
print(response.candidates[0].content.parts)
"
```

## Tripartite Video Analysis Script

```bash
# Full tripartite analysis
uv run /Users/bob/ies/plurigrid-asi-skillz/lib/gemini_tripartite_video.py \\
    video.mp4 --fps 0.5 --max 20 --output analysis.json

# Quick test
uv run --with google-genai --with opencv-python --with numpy --with rich \\
    -- python /Users/bob/ies/plurigrid-asi-skillz/lib/gemini_tripartite_video.py \\
    ~/Desktop/*.mov --fps 1 --max 10
```

## Commands

```bash
just uv-gemini          # Gemini one-liner
just uv-discopy         # DisCoPy categorical
just uv-tripartite      # Tripartite video analysis
just uv-ml-stack        # Full ML environment
```

## See Also

- [gemini-cookbook/quickstarts/Video_understanding.ipynb](file:///Users/bob/ies/gemini-cookbook/quickstarts/Video_understanding.ipynb)
- [gemini_tripartite_video.py](file:///Users/bob/ies/plurigrid-asi-skillz/lib/gemini_tripartite_video.py)
- [gay-mcp skill](file:///Users/bob/.claude/skills/gay-mcp/SKILL.md)
