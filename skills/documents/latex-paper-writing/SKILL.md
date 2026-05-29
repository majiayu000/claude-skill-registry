---
name: latex-paper-writing
description: Academic paper structure, venue formatting (NeurIPS/ICML/ICLR), bibliography, figures, tables, and math notation for ML research.
---

# LaTeX Paper Writing for ML Venues

## Venue Formatting Requirements

### Decision Table: Venue Selection

| Venue | Style File | Page Limit (Main) | Supplementary | Abstract Limit | Blind Review |
|-------|-----------|-------------------|---------------|----------------|--------------|
| NeurIPS | `neurips_2024.sty` | 9 + refs | Unlimited appendix | 250 words | Yes |
| ICML | `icml2024.sty` | 8 + refs | Unlimited appendix | N/A | Yes |
| ICLR | `iclr2024_conference.sty` | 8 + refs (soft) | Unlimited appendix | N/A | Yes |
| AAAI | `aaai24.sty` | 7 + 1 refs + 1 ethics | Separate PDF | N/A | Yes |
| ACL | `acl2024.sty` | 8 + refs | 4 pages | N/A | Yes (ARR) |
| CVPR | `cvpr.sty` | 8 + refs | Unlimited | N/A | Yes |

### Submission vs Camera-Ready

| Aspect | Submission | Camera-Ready |
|--------|-----------|--------------|
| Author names | Anonymous | Full names + affiliations |
| Style option | `\usepackage[preprint]{neurips_2024}` | `\usepackage[final]{neurips_2024}` |
| Page limit | Strict | Usually +1 page |
| Acknowledgments | Omit | Include |
| Supplementary | Separate or appended | Usually appended |

## Paper Preamble Template

```latex
\documentclass{article}

% --- Venue style (swap per target) ---
\usepackage[preprint]{neurips_2024}

% --- Core packages ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}       % Professional tables
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}       % dcases, coloneqq
\usepackage{nicefrac}
\usepackage{microtype}       % Better typography
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{subcaption}      % Subfigures
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{pgfplots}
\usepackage{tikz}
\pgfplotsset{compat=1.18}

% --- Math operators ---
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator{\E}{\mathbb{E}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\loss}{\mathcal{L}}
\newcommand{\dataset}{\mathcal{D}}
\newcommand{\param}{\boldsymbol{\theta}}
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}

\title{Your Title Here}
\author{Anonymous}  % Submission phase

\begin{document}
\maketitle
\begin{abstract}
Your abstract (NeurIPS: max 250 words).
\end{abstract}
```

## Algorithm Environment

```latex
\begin{algorithm}[t]
\caption{Stochastic Gradient Descent with Momentum}
\label{alg:sgd-momentum}
\begin{algorithmic}[1]
\REQUIRE Learning rate $\eta$, momentum $\beta$, initial params $\param_0$
\ENSURE Trained parameters $\param_T$
\STATE $\mathbf{v}_0 \leftarrow \mathbf{0}$
\FOR{ = 1$ \TO $}
    \STATE Sample mini-batch  \sim \dataset$
    \STATE $\mathbf{g}_t \leftarrow \nabla_{\param} \loss(\param_{t-1}; B_t)$
    \STATE $\mathbf{v}_t \leftarrow \beta \mathbf{v}_{t-1} + \mathbf{g}_t$
    \STATE $\param_t \leftarrow \param_{t-1} - \eta \mathbf{v}_t$
\ENDFOR
\RETURN $\param_T$
\end{algorithmic}
\end{algorithm}
```

## Figures

### Subfigure Layout

```latex
\begin{figure}[t]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/loss_curve.pdf}
    \caption{Training loss}
    \label{fig:loss}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/accuracy.pdf}
    \caption{Validation accuracy}
    \label{fig:acc}
  \end{subfigure}
  \caption{Training dynamics on CIFAR-10. (a) Loss converges within 50 epochs.
           (b) Accuracy plateaus at 94.2\%.}
  \label{fig:training}
\end{figure}
```

### PGFPlots Inline Chart

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.75\columnwidth,
    height=5cm,
    xlabel={Epoch},
    ylabel={Test Accuracy (\%)},
    legend pos=south east,
    grid=major,
    legend style={font=\small},
]
\addplot[blue, thick, mark=none] table[x=epoch, y=ours, col sep=comma]
    {data/results.csv};
\addplot[red, dashed, thick, mark=none] table[x=epoch, y=baseline, col sep=comma]
    {data/results.csv};
\legend{Ours, Baseline}
\end{axis}
\end{tikzpicture}
\caption{Comparison against baseline on ImageNet.}
\label{fig:comparison}
\end{figure}
```

## Results Tables

```latex
\begin{table}[t]
\caption{Results on standard benchmarks. Best in \textbf{bold}, second \underline{underlined}.}
\label{tab:results}
\centering
\small
\begin{tabular}{lcccc}
\toprule
Method & CIFAR-10 & CIFAR-100 & ImageNet & Params (M) \\
\midrule
ResNet-50        & 95.1 & 78.3 & 76.1 & 25.6 \\
ViT-B/16         & 96.2 & 82.1 & 77.9 & 86.4 \\
Baseline         & 95.8 & 80.5 & 77.2 & 24.1 \\
\midrule
\textbf{Ours}    & \textbf{97.1} & \textbf{84.3} & \underline{78.8} & 26.3 \\
Ours (small)     & \underline{96.5} & \underline{83.1} & \textbf{79.2} & 12.8 \\
\bottomrule
\end{tabular}
\end{table}
```

## Bibliography Setup

```latex
% In preamble (natbib usually loaded by venue style)
\usepackage[numbers,sort&compress]{natbib}
\bibliographystyle{plainnat}

% At end of document
\bibliography{references}
```

### BibTeX Entry Patterns

```bibtex
@inproceedings{vaswani2017attention,
  title     = {Attention is All You Need},
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and
               Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and
               Kaiser, {\L}ukasz and Polosukhin, Illia},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {30},
  year      = {2017}
}

@article{devlin2019bert,
  title   = {{BERT}: Pre-training of Deep Bidirectional Transformers
             for Language Understanding},
  author  = {Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and
             Toutanova, Kristina},
  journal = {arXiv preprint arXiv:1810.04805},
  year    = {2019}
}
```

## Supplementary Material Structure

```latex
% After \bibliography{references} in main document
\newpage
\appendix
\section{Proof of Theorem 1}
\label{app:proof}
...

\section{Additional Experiments}
\label{app:experiments}

\section{Hyperparameter Details}
\label{app:hyperparams}

\section{Compute Resources}
\label{app:compute}
```

## Gotchas and Anti-Patterns

### Submission Formatting Traps
- **Missing anonymization**: grep for author names, institution names, GitHub URLs before submission. `\iclrfinalcopy` left in submission = desk reject.
- **Wrong style option**: `[final]` vs `[preprint]` flag changes page layout. Always double-check.
- **Overflowing margins**: venue checkers reject margin violations. Use `\usepackage[letterpaper]{geometry}` only if the style file does not set it.
- **Font embedding**: run `pdffonts output.pdf` to verify all fonts embedded. Missing fonts = rejection at some venues.

### Page Limit Management
- Move proofs and ablations to appendix early; do not scramble at deadline.
- `\vspace{-Xpt}` and `\setlength{\textfloatsep}{5pt}` buy space but look bad if overdone.
- Shrink figures with `width=0.9\columnwidth` rather than removing content.
- Use `\small` or `\footnotesize` in tables, never in body text.

### Common Mistakes
- Using `\cite` vs `\citep` vs `\citet` incorrectly. `\citet` for "Author (2024) showed...", `\citep` for "(Author, 2024)".
- BibTeX keys with special characters break silently. Stick to `authorYEARword`.
- `\label` must come after `\caption` in figures/tables, otherwise references break.
- PDF figures > vector (`.pdf`/`.eps`). Raster (`.png`) only for photographs/screenshots.
- Never `\newpage` or `\clearpage` in submission body to game layout; reviewers notice.
