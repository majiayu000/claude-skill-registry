---
name: cantordust-viz
description: Binary visualization for human pattern recognition - Ghidra plugin by Chris Domas (xoreaxeaxeax)
version: 1.0.0
---

# Cantordust Binary Visualization

> **Use when embeddings fail: humans see patterns algorithms miss.**

Visual binary analysis tool for Ghidra. Converts binary data to bitmaps/visualizations where structural patterns become visible to human pattern recognition.

## GF(3) Triad

```
cantordust-viz (-1) ⊗ skill-embedding-vss (0) ⊗ radare2-hatchery (+1) = 0 ✓
```

## Lineage: 2020 Binary Analysis

| Tool | Approach | Strength |
|------|----------|----------|
| **Cantordust** | Visual/human | Sees patterns ML misses |
| **Zignatures** | Soft signatures | Fuzzy matching + keyspace reduction |
| **skill-embedding-vss** | MLX embeddings | O(1) similarity at scale |

## Installation

```bash
git clone https://github.com/Battelle/cantordust.git
# Add to Ghidra Script Manager
```

## Key Insight

From xoreaxeaxeax's work:
- **movfuscator**: All x86 can be MOV (Turing-complete)
- **sandsifter**: Fuzzing reveals undocumented CPU instructions
- **Cantordust**: Binary structure visible in 2D projections

## When to Use

1. **Embedding similarity unclear** → visualize both binaries
2. **Obfuscation suspected** → visual patterns survive obfuscation
3. **Cross-architecture comparison** → structural similarity visible
4. **Malware family classification** → visual fingerprinting

## xoreaxeaxeax Ecosystem (19K+ stars)

| Repo | Stars | Category |
|------|-------|----------|
| movfuscator | 10,075 | obfuscation |
| sandsifter | 4,998 | hardware security |
| rosenbridge | 2,380 | hardware backdoors |
| REpsych | 1,031 | anti-RE |

## Integration with skill-embedding-vss

```python
# When embeddings show high similarity but you want visual confirmation
from cantordust import visualize_binary
from skill_embedding_vss import SkillEmbeddingVSS

vss = SkillEmbeddingVSS('/path/to/skills')
similar = vss.find_nearest('target', k=5)

# Visual confirm top matches
for name, dist in similar[:3]:
    visualize_binary(f'/path/to/{name}')  # Human reviews
```

## References

- [Cantordust GitHub](https://github.com/Battelle/cantordust)
- [Battelle Blog Post](https://inside.battelle.org/blog-details/battelle-publishes-open-source-binary-visualization-tool)
- [DEF CON talks by xoreaxeaxeax](https://www.youtube.com/results?search_query=xoreaxeaxeax+defcon)

## Cantordust ↔ Gay.jl Bridge

```julia
# cantordust_gay_bridge.jl connects:
# 1. Cantordust 2-tuple byte pair visualization
# 2. CJ Carr spectral features (diffusion transformers)  
# 3. Gay.jl deterministic coloring (SPI)

result = analyze_binary_with_gay("target.bin")
# Returns: matrix, diagonal_score, ascii_score, trit_sum, sample_colors
```

## Pattern Theory

| Domain | Representation | Gay.jl Mapping |
|--------|----------------|----------------|
| Binary (Cantordust) | 2-tuple → 256×256 | entropy → trit → color |
| Audio (CJ Carr) | Mel spectrogram | centroid/flatness → HSL |
| Color (Gay.jl) | SplitMix64 + golden angle | SPI deterministic |