---
name: latex-authoring
description: LaTeX document authoring with arXiv submission best practices, Overleaf patterns, and academic publishing conventions.
activationKeywords:
  - latex
  - LaTeX
  - tex
  - arxiv
  - overleaf
  - bibtex
  - biblatex
  - pdflatex
  - xelatex
  - lualatex
  - document class
  - beamer
  - tikz
  - amsmath
type: skill
category: media
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/media/latex-authoring/SKILL.md
superseded_by: null
---
# LaTeX Authoring Skill

Expert-level LaTeX document authoring following arXiv submission best practices and Overleaf conventions. Produces accessible, semantic, publication-ready documents.

## Core Principle

> "Use macros according to their meaning, not because of the way they appear visually." — arXiv Best Practices

Semantic markup over visual formatting. Always.

## Document Structure

### Standard Article
```latex
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[numbers]{natbib}
\usepackage{booktabs}          % Professional tables
\usepackage{microtype}         % Typography improvements
\usepackage{cleveref}          % Smart cross-references

\title{Article Title}
\author{Author One\thanks{affiliation} \and Author Two\thanks{affiliation}}
\date{\today}

\begin{document}
\maketitle
\begin{abstract}
  Concise summary of the work.
\end{abstract}

\section{Introduction}
\section{Related Work}
\section{Method}
\section{Results}
\section{Discussion}
\section{Conclusion}

\bibliographystyle{plainnat}
\bibliography{references}
\end{document}
```

### Front Matter (arXiv requirement)
Always use semantic front matter commands:
```latex
\title{...}
\author{Author One \AND Author Two}
\begin{abstract} ... \end{abstract}
```
Never simulate titles with `\textbf{\Large Title}` — this breaks HTML conversion.

## Semantic Markup Rules

### DO (semantic)
```latex
\emph{key phrase}              % Emphasis with meaning
\textbf{important term}       % Bold with purpose
\section{Introduction}         % Structural heading
\begin{theorem} ... \end{theorem}  % Named environment
\label{eq:energy}             % Reference target
\cref{eq:energy}              % Smart cross-reference
```

### DON'T (visual-only)
```latex
{\it key phrase}               % Visual italic, no semantics
{\bf important}                % Visual bold, no semantics
{\Large\bfseries Introduction} % Fake heading, breaks structure
\vspace{1em}                   % Manual spacing hack
\\[1em]                        % Line break as spacing
```

## Mathematics

### Inline vs Display
```latex
% Inline math
The energy $E = mc^2$ is fundamental.

% Display (numbered)
\begin{equation}
  E = mc^2 \label{eq:energy}
\end{equation}

% Display (unnumbered)
\begin{equation*}
  F = ma
\end{equation*}

% Multi-line aligned
\begin{align}
  \nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0} \label{eq:gauss} \\
  \nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align}
```

### Common Math Patterns
```latex
% Matrices
\begin{pmatrix} a & b \\ c & d \end{pmatrix}

% Cases
f(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{otherwise} \end{cases}

% Operators
\DeclareMathOperator{\argmax}{arg\,max}
\DeclareMathOperator{\softmax}{softmax}

% Fractions (prefer \frac for display, \nicefrac for inline)
\frac{\partial L}{\partial \theta}

% Bold math vectors
\mathbf{x}, \boldsymbol{\theta}
```

## Tables

### Professional Tables (booktabs)
```latex
\begin{table}[htbp]
  \centering
  \caption{Model comparison on benchmark tasks.}
  \label{tab:results}
  \begin{tabular}{lrrr}
    \toprule
    Model & Accuracy & F1 & Latency (ms) \\
    \midrule
    Baseline    & 0.842 & 0.831 & 12.3 \\
    Our Method  & \textbf{0.917} & \textbf{0.904} & 14.1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

Never use `\hline` — always `\toprule`, `\midrule`, `\bottomrule` from booktabs.

## Figures

### With Alt Text (arXiv accessibility requirement)
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth, alt={Bar chart showing accuracy improvements from 84% baseline to 92% with our method across three benchmarks}]{figures/results.pdf}
  \caption{Accuracy comparison across benchmark tasks.}
  \label{fig:results}
\end{figure}
```

### Subfigures
```latex
\usepackage{subcaption}
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig-a.pdf}
    \caption{Training loss}
    \label{fig:loss}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{fig-b.pdf}
    \caption{Validation accuracy}
    \label{fig:acc}
  \end{subfigure}
  \caption{Training dynamics over 100 epochs.}
\end{figure}
```

## Bibliography

### BibTeX Entry Types
```bibtex
@article{vaswani2017attention,
  title     = {Attention Is All You Need},
  author    = {Vaswani, Ashish and others},
  journal   = {NeurIPS},
  year      = {2017}
}

@inproceedings{devlin2019bert,
  title     = {{BERT}: Pre-training of Deep Bidirectional Transformers},
  author    = {Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  booktitle = {NAACL-HLT},
  year      = {2019}
}

@misc{anthropic2026claude,
  title        = {Claude 4.6 Model Card},
  author       = {Anthropic},
  year         = {2026},
  howpublished = {\url{https://www.anthropic.com}},
  note         = {Accessed: 2026-04-08}
}
```

### Citation Commands
```latex
% natbib
\citet{vaswani2017attention}  → Vaswani et al. (2017)
\citep{vaswani2017attention}  → (Vaswani et al., 2017)
\citep[see][]{vaswani2017attention} → (see Vaswani et al., 2017)

% biblatex
\textcite{vaswani2017attention}
\parencite{vaswani2017attention}
```

## arXiv Submission Checklist

1. **Single directory** — all files in one flat directory (no subdirectories for figures)
2. **Main file** — must be compilable with `pdflatex main.tex` (or xelatex/lualatex)
3. **References** — include `.bbl` file (pre-compiled bibliography), not just `.bib`
4. **Figures** — PDF/PNG/JPG only. EPS accepted but PDF preferred. Include alt text.
5. **No absolute paths** — use `\includegraphics{figure1}` not `\includegraphics{/home/user/fig/figure1}`
6. **Package compatibility** — check [LaTeXML supported packages](https://corpora.mathweb.org/corpus/arxmliv/tex_to_html/info/loaded_file) for HTML conversion
7. **Compiler** — use most recent TeX Live. Set Overleaf to "stop on errors" mode.
8. **Font encoding** — use `\usepackage[T1]{fontenc}` for proper glyph support
9. **No custom styles** — avoid `\def` and `\newcommand` that redefine standard commands
10. **Comments** — remove `\usepackage{comment}` sections before submission

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `{\it text}` | `\emph{text}` or `\textit{text}` |
| `{\bf text}` | `\textbf{text}` |
| `$$display math$$` | `\[ display math \]` or `equation` env |
| `\hline` in tables | `\toprule`, `\midrule`, `\bottomrule` |
| Manual spacing `\\[1em]` | Proper environments and `\vspace` sparingly |
| `\begin{center}` for figures | `\centering` inside float |
| Missing `\label` after `\caption` | Always `\caption{...}\label{...}` in that order |
| `\cite` without natbib | Use `\citet`/`\citep` for author-year styles |
| Bitmap figures at low DPI | Vector PDF or 300+ DPI PNG |
| Hardcoded cross-references | Use `\ref`, `\cref`, or `\autoref` |

## Document Classes

| Class | Use Case |
|-------|----------|
| `article` | Journal papers, short reports |
| `report` | Longer documents with chapters |
| `book` | Books, theses |
| `beamer` | Presentations |
| `standalone` | Single figures/diagrams for inclusion |
| `memoir` | Flexible book/report class |
| `IEEEtran` | IEEE conference/journal papers |
| `acmart` | ACM publications |
| `revtex4-2` | APS/Physical Review journals |
| `aastex63` | AAS/Astrophysical Journal |
| `mnras` | Monthly Notices of the Royal Astronomical Society |

## Essential Packages

| Package | Purpose |
|---------|---------|
| `amsmath` | Math environments (align, equation, etc.) |
| `amssymb` | Additional math symbols |
| `amsthm` | Theorem environments |
| `graphicx` | Image inclusion with alt text |
| `hyperref` | Clickable cross-references and URLs |
| `cleveref` | Smart cross-references (`\cref`) |
| `booktabs` | Professional table rules |
| `natbib` | Author-year citations |
| `microtype` | Microtypographic improvements |
| `xcolor` | Color support |
| `tikz` | Programmatic diagrams |
| `algorithm2e` | Algorithm pseudocode |
| `listings` | Code listings |
| `minted` | Syntax-highlighted code (requires `-shell-escape`) |
| `siunitx` | SI units (`\SI{299792458}{\meter\per\second}`) |
| `subcaption` | Subfigures and subtables |

## Package Load Order

Load in this order to avoid conflicts:
```latex
\usepackage[utf8]{inputenc}    % 1. Input encoding
\usepackage[T1]{fontenc}       % 2. Font encoding
\usepackage{amsmath,amssymb}   % 3. Math
\usepackage{graphicx}          % 4. Graphics
\usepackage{xcolor}            % 5. Colors (before tikz)
\usepackage{tikz}              % 6. Diagrams
\usepackage{booktabs}          % 7. Tables
\usepackage{algorithm2e}       % 8. Algorithms
\usepackage{listings}          % 9. Code
\usepackage[numbers]{natbib}   % 10. Citations
\usepackage{hyperref}          % 11. Hyperlinks (LAST or near-last)
\usepackage{cleveref}          % 12. Smart refs (AFTER hyperref)
```

## ORCID Integration

ORCID (Open Researcher and Contributor ID) is the standard persistent identifier for researchers. Format: `0000-0002-1825-0097` (16 digits, hyphenated groups of 4).

### Including ORCID in LaTeX Documents
```latex
\usepackage{orcidlink}  % Provides \orcidlink command

% In author block
\author{
  Jane Researcher\orcidlink{0000-0002-1825-0097} \and
  John Scholar\orcidlink{0000-0001-5109-3700}
}
```

### Manual ORCID (without orcidlink package)
```latex
\usepackage{hyperref}
\newcommand{\orcid}[1]{\href{https://orcid.org/#1}{\includegraphics[height=1em]{orcid.png} #1}}

% Usage
\author{Jane Researcher\thanks{\orcid{0000-0002-1825-0097}}}
```

### ORCID in BibTeX
```bibtex
@article{researcher2026,
  author  = {Researcher, Jane},
  title   = {Important Discovery},
  journal = {Nature},
  year    = {2026},
  note    = {ORCID: 0000-0002-1825-0097}
}
```

### ORCID Record Data Types
ORCID tracks: works (papers, books, preprints), employment, education, funding, peer review, research resources, invited positions, distinctions, memberships, qualifications.

### ORCID API Integration
- **Public API**: Read-only access to public researcher data. No auth required.
- **Member API**: Read/write with OAuth 2.0 permission. Post works, affiliations, funding.
- **Sandbox**: `sandbox.orcid.org` for testing (use before production).
- **iD Format**: Always display as full URL: `https://orcid.org/0000-0002-1825-0097`
- **Schema**: v3.0 current. Supports DOI, arXiv ID, PubMed ID, ISBN cross-linking.

### Best Practices
- Always collect ORCID iD via authenticated OAuth (never manual entry — prevents typos)
- Display the green ORCID icon alongside the iD per brand guidelines
- Link ORCID to arXiv submissions (arXiv supports ORCID in author metadata)
- Include ORCID in all journal submissions, grant applications, and institutional profiles
- Use the ORCID sandbox (`sandbox.orcid.org`) for development/testing

## When This Skill Activates

- Writing LaTeX documents or templates
- Preparing arXiv submissions
- Formatting mathematical expressions
- Creating publication-ready tables and figures
- Managing bibliographies
- Troubleshooting LaTeX compilation errors
- Converting documents between formats
- Creating Beamer presentations
- Integrating ORCID identifiers into papers
- Academic publishing workflow questions
