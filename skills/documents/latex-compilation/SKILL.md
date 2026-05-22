---
name: latex-compilation
description: Use when LaTeX documents fail to compile, have undefined references, duplicate labels, or citation errors
---

# LaTeX Compilation

## Overview

Fix common LaTeX compilation errors systematically by running the full build sequence and addressing errors in order of dependency.

## When to Use

- Document won't compile (pdflatex errors)
- "Undefined reference" or "multiply-defined labels" warnings
- Citations showing as `[?]` or undefined
- Cross-references not resolving

## Quick Reference

| Problem | Solution |
|---------|----------|
| Undefined citations | Run: `pdflatex → bibtex → pdflatex → pdflatex` |
| Duplicate labels | Each `\label{name}` must be unique across document |
| Empty `\cite{}` | Remove or fill in citation key |
| Citation key mismatch | Ensure `.tex` keys match `.bib` entry names exactly |
| Cross-refs not updating | Run pdflatex twice after changes |

## Full Compilation Sequence

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

## Common Mistakes

**Duplicate `\label{}` tags** - Copy-pasting figures often duplicates labels. Search with:
```bash
grep -n 'label{' paper.tex | sort -t'{' -k2 | uniq -d -f1
```

**Citation key typos** - `altabaa2025co` vs `altabaa2025cot` causes undefined citation. Always verify keys match the .bib file exactly.

**Running pdflatex only once** - Cross-references and citations need multiple passes to resolve.

**Empty citations** - `\cite{}` causes warnings. Remove or add proper key.
