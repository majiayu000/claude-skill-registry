---
name: quarto-julia
description: 'Quarto + Julia Skill'
version: 1.0.0
---

# Quarto + Julia Skill

**Status**: Production Ready
**Trit**: 0 (ERGODIC - coordinator/synthesizer)
**Purpose**: Reproducible documents with Julia code blocks and GF(3) skill tracking

---

## Overview

Quarto is a scientific publishing system that renders `.qmd` files to HTML, PDF, and more. Combined with Julia, it enables:

1. **Executable documents** - Julia code blocks run during render
2. **Skill activation logs** - Track GF(3) triads in rendered output
3. **Reproducible research** - Same seed = same colors = same results

## Two Julia Engines

| Feature | `julia` Engine (NEW) | `jupyter` Engine |
|---------|---------------------|------------------|
| Execute Julia code | ✅ | ✅ |
| Keep sessions alive | ✅ | ✅ |
| No Python required | ✅ | ❌ |
| No global pkg install | ✅ | ❌ |
| juliaup integration | ✅ | ❌ |
| Python/R via PythonCall/RCall | ✅ | ❌ |
| QuartoTools.jl expandable cells | ✅ | ❌ |

**Recommendation**: Use `engine: julia` for new projects.

## Installation (No Homebrew)

```bash
# Download and extract
cd /tmp
curl -sL https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-macos.tar.gz -o quarto.tar.gz
tar -xzf quarto.tar.gz

# Install to ~/bin with proper structure
mkdir -p ~/bin/quarto-1.6.42
cp -r bin share ~/bin/quarto-1.6.42/

# Create wrapper script (critical for path resolution)
cat > ~/bin/quarto << 'EOF'
#!/bin/bash
export QUARTO_SHARE_PATH="$HOME/bin/quarto-1.6.42/share"
exec "$HOME/bin/quarto-1.6.42/bin/quarto" "$@"
EOF
chmod +x ~/bin/quarto

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
export PATH="$HOME/bin:$PATH"

# Verify
quarto --version  # Should show 1.6.42
```

## Basic .qmd Document (Modern julia Engine)

```markdown
---
title: "GF(3) Skill Activation Log"
author: "Plurigrid ASI"
date: today
format:
  html:
    code-fold: true
    toc: true
    theme: cosmo
engine: julia
execute:
  echo: true
  cache: true
---

## Skill Triad

```{julia}
#| label: gf3-triad
#| code-summary: "Define GF(3) skill triad"

struct SkillActivation
    name::String
    trit::Int  # -1, 0, or +1
    hue::Float64
end

triad = [
    SkillActivation("acsets", -1, 220.0),
    SkillActivation("bisimulation", 0, 120.0),
    SkillActivation("artifacts-builder", 1, 30.0)
]

# Verify conservation
trit_sum = sum(s.trit for s in triad)
println("GF(3) sum: $trit_sum ≡ $(mod(trit_sum, 3)) (mod 3)")
```
```

## juliaup Version Selection

```yaml
---
title: "Julia 1.11 Notebook"
engine: julia
julia:
  exeflags: ["+1.11"]  # Use juliaup channel specifier
---
```

## Commands

```bash
# Render single file
quarto render document.qmd

# Render to specific format
quarto render document.qmd --to pdf
quarto render document.qmd --to docx

# Live preview (watches for changes)
quarto preview document.qmd

# Render entire project
quarto render

# Check installation
quarto check

# Install TinyTeX for PDF output
quarto install tinytex
```

## Project Structure

```
project/
├── _quarto.yml          # Project configuration
├── index.qmd            # Main document
├── skills/
│   ├── triad-1.qmd      # Skill triad documentation
│   └── triad-2.qmd
└── _output/             # Rendered files
```

## _quarto.yml Configuration

```yaml
project:
  type: website
  output-dir: _output

website:
  title: "Skill Activation Log"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: skills/triad-1.qmd
        text: Triad 1

format:
  html:
    theme: cosmo
    css: styles.css
    toc: true

execute:
  freeze: auto  # Cache computations
```

## Julia Integration Patterns

### Gay.jl Color Generation

```{julia}
using Gay

seed = 0x42D
palette = Gay.palette(seed, 9)  # 9 colors for 3 triads

for (i, color) in enumerate(palette)
    trit = mod(i - 1, 3) - 1  # Cycle: -1, 0, +1
    println("Skill $i: $(color.hex) trit=$trit")
end
```

### ACSets Schema Visualization

```{julia}
using Catlab.CategoricalAlgebra
using Catlab.Graphics

@present SchSkillGraph(FreeSchema) begin
    Skill::Ob
    Triad::Ob
    belongs_to::Hom(Skill, Triad)

    Name::AttrType
    Trit::AttrType
    name::Attr(Skill, Name)
    trit::Attr(Skill, Trit)
end

# Render as GraphViz
to_graphviz(SchSkillGraph)
```

### Spectral Gap Computation

```{julia}
using LinearAlgebra

function spectral_gap(n::Int)
    # Cycle graph adjacency (normalized)
    A = zeros(n, n)
    for i in 1:n
        A[i, mod1(i+1, n)] = 0.5
        A[i, mod1(i-1, n)] = 0.5
    end
    eigs = eigvals(A)
    sorted = sort(real.(eigs), rev=true)
    return 1.0 - sorted[2]
end

# Find n where gap ≈ 1/4
for n in [4, 8, 9, 10, 16]
    gap = spectral_gap(n)
    marker = abs(gap - 0.25) < 0.02 ? " ← TARGET" : ""
    println("n=$n: gap=$(round(gap, digits=4))$marker")
end
```

## Rendering from Julia

```julia
using Quarto

# Single file
Quarto.render("index.qmd")

# With options
Quarto.render("index.qmd", output_format="pdf")

# Entire project
Quarto.render(".")  # Current directory

# Preview with live reload
Quarto.preview("index.qmd")
```

## Troubleshooting

### "Cannot determine Quarto source path"

This error means `QUARTO_SHARE_PATH` is not set. Use the wrapper script:

```bash
# Check current setup
cat ~/bin/quarto

# Should contain:
# export QUARTO_SHARE_PATH="$HOME/bin/quarto-1.6.42/share"
# exec "$HOME/bin/quarto-1.6.42/bin/quarto" "$@"
```

### Julia kernel not found

```bash
# Install IJulia
julia -e 'using Pkg; Pkg.add("IJulia")'

# Register kernel
julia -e 'using IJulia; IJulia.installkernel("Julia")'

# List kernels
jupyter kernelspec list
```

### PDF rendering fails

```bash
# Install TinyTeX
quarto install tinytex

# Or use system LaTeX
# macOS: install MacTeX
# Linux: apt install texlive-full
```

## GF(3) Skill Tracking Template

```markdown
---
title: "Skill Activation: {{< meta triad_name >}}"
params:
  triad_name: "Database & Verification"
  skills:
    - {name: "acsets", trit: -1, hue: 220}
    - {name: "bisimulation", trit: 0, hue: 120}
    - {name: "artifacts-builder", trit: 1, hue: 30}
---

```{julia}
#| label: verify-conservation

skills = params.skills
trit_sum = sum(s["trit"] for s in skills)
@assert mod(trit_sum, 3) == 0 "GF(3) violation!"
println("✓ Conservation verified: Σ = $trit_sum ≡ 0 (mod 3)")
```
```

## Integration with ~/worlds/

```julia
# List available worlds
readdir(expanduser("~/worlds"))

# Load world-specific Julia project
using Pkg
Pkg.activate(expanduser("~/worlds/a"))  # AlgebraicJulia world
```

## Related Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| `gay-mcp` | 0 | Deterministic colors in plots |
| `acsets` | -1 | Schema visualization |
| `triad-interleave` | +1 | Schedule documentation |
| `algorithmic-art` | 0 | p5.js visualizations |

## References

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto.jl](https://github.com/quarto-dev/quarto-julia)
- [Julia for Quarto](https://quarto.org/docs/computations/julia.html)

---

**Skill Name**: quarto-julia
**Type**: Documentation / Publishing
**Trit**: 0 (ERGODIC)
**Dependencies**: Julia 1.10+, IJulia, Quarto CLI 1.6+

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 7. Propagators

**Concepts**: propagator, cell, constraint, bidirectional, TMS

### GF(3) Balanced Triad

```
quarto-julia (○) + SDF.Ch7 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch4: Pattern Matching
- Ch10: Adventure Game Example

### Connection Pattern

Propagators flow constraints bidirectionally. This skill propagates information.
