---
name: latex-manual
description: Comprehensive LaTeX reference with commands, templates, and troubleshooting for document typesetting
version: 1.0.0
---

# LaTeX Skill

Comprehensive assistance with LaTeX document preparation, typesetting, and formatting. This skill provides quick references, templates, and troubleshooting for academic papers, presentations, reports, and technical documents.

## When to Use This Skill

This skill should be triggered when:
- Writing LaTeX documents (papers, theses, reports)
- Creating mathematical equations and formulas
- Formatting scientific or academic documents
- Making presentations with Beamer
- Debugging LaTeX compilation errors
- Creating tables, figures, or bibliographies
- Asking about LaTeX commands or syntax
- Converting documents to LaTeX format
- Setting up document structure or layout
- Troubleshooting LaTeX warnings or errors

## Quick Reference

### Essential Document Structure

```latex
\documentclass{article}  % or book, report, beamer
\usepackage{graphicx}     % For images
\usepackage{amsmath}      % For math
\usepackage{hyperref}     % For hyperlinks

\title{Document Title}
\author{Author Name}
\date{\today}

\begin{document}

\maketitle

\section{Introduction}
Your content here.

\subsection{Background}
More content.

\section{Conclusion}
Final thoughts.

\end{document}
```

### Common Commands

**Text Formatting:**
- `\textbf{bold text}` - Bold
- `\textit{italic text}` - Italic
- `\underline{underlined}` - Underline
- `\texttt{monospace}` - Typewriter font
- `\emph{emphasized}` - Emphasis (usually italic)

**Document Structure:**
- `\section{Title}` - Section heading
- `\subsection{Title}` - Subsection
- `\subsubsection{Title}` - Sub-subsection
- `\paragraph{Title}` - Paragraph heading
- `\label{sec:intro}` - Label for cross-reference
- `\ref{sec:intro}` - Reference to label

**Lists:**
```latex
% Bulleted list
\begin{itemize}
  \item First item
  \item Second item
\end{itemize}

% Numbered list
\begin{enumerate}
  \item First item
  \item Second item
\end{enumerate}

% Description list
\begin{description}
  \item[Term] Definition
  \item[Another] Explanation
\end{description}
```

**Math Mode:**
- Inline: `$x^2 + y^2 = z^2$`
- Display: `$$E = mc^2$$`
- Numbered equation:
```latex
\begin{equation}
  \int_0^1 f(x)dx = F(1) - F(0)
  \label{eq:ftc}
\end{equation}
```

**Tables:**
```latex
\begin{table}[h]
  \centering
  \begin{tabular}{|c|c|c|}
    \hline
    Header 1 & Header 2 & Header 3 \\
    \hline
    Data 1 & Data 2 & Data 3 \\
    Data 4 & Data 5 & Data 6 \\
    \hline
  \end{tabular}
  \caption{Table caption}
  \label{tab:example}
\end{table}
```

**Figures:**
```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{image.pdf}
  \caption{Figure caption}
  \label{fig:example}
\end{figure}
```

**Cross-References:**
- `See Section~\ref{sec:intro}` - Reference section
- `As shown in Figure~\ref{fig:example}` - Reference figure
- `Equation~\eqref{eq:ftc}` - Reference equation (with parentheses)

**Citations:**
```latex
% In preamble
\usepackage{natbib}
\bibliographystyle{plain}

% In text
According to~\cite{author2024}...
Multiple citations~\cite{author2024,smith2023}...

% At end of document
\bibliography{references}  % references.bib file
```

### Common Packages

**Essential:**
- `amsmath` - Advanced mathematics
- `graphicx` - Include graphics
- `hyperref` - Clickable links and URLs
- `geometry` - Page layout
- `fancyhdr` - Custom headers/footers

**Text and Fonts:**
- `fontenc` - Font encoding
- `inputenc` - Input encoding (UTF-8)
- `babel` - Language support
- `microtype` - Typography improvements

**Tables and Lists:**
- `booktabs` - Professional tables
- `longtable` - Multi-page tables
- `enumitem` - Customizable lists

**Graphics:**
- `tikz` - Programmatic graphics
- `pgfplots` - Data plots
- `subfig` - Subfigures

**Bibliography:**
- `natbib` - Citations and bibliography
- `biblatex` - Modern bibliography system

**Code Listings:**
- `listings` - Source code formatting
- `minted` - Syntax highlighting (requires Python)

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **quick-start.md** - Getting started with LaTeX
- **mathematics.md** - Math mode, equations, symbols
- **formatting.md** - Text formatting, fonts, spacing
- **tables-graphics.md** - Tables, figures, images
- **bibliography.md** - Citations and bibliography management
- **troubleshooting.md** - Common errors and solutions

## Templates

Ready-to-use templates in `assets/`:

- **article-template.tex** - Basic article/paper
- **report-template.tex** - Report with chapters
- **beamer-template.tex** - Presentation slides
- **letter-template.tex** - Formal letter
- **ieee-paper-template.tex** - IEEE conference paper format

## Scripts

Helper scripts in `scripts/`:

- **compile.sh** - Compile LaTeX document
- **clean.sh** - Remove auxiliary files
- **bibtex.sh** - Run complete BibTeX workflow

## Common Patterns

### Two-Column Layout

```latex
\documentclass[twocolumn]{article}
% or
\usepackage{multicol}
\begin{multicols}{2}
  Content in two columns
\end{multicols}
```

### Custom Page Margins

```latex
\usepackage{geometry}
\geometry{
  a4paper,
  left=1in,
  right=1in,
  top=1in,
  bottom=1in
}
```

### Custom Headers and Footers

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{Left Header}
\fancyhead[C]{Center Header}
\fancyhead[R]{Right Header}
\fancyfoot[C]{\thepage}
```

### Including Code

```latex
\usepackage{listings}
\lstset{
  language=Python,
  basicstyle=\ttfamily,
  numbers=left,
  frame=single
}

\begin{lstlisting}
def hello():
    print("Hello, World!")
\end{lstlisting}
```

### Multiple Authors

```latex
\author{
  First Author\thanks{University A} \and
  Second Author\thanks{University B} \and
  Third Author\thanks{University C}
}
```

## Compilation Workflow

**Standard:**
```bash
pdflatex document.tex
pdflatex document.tex  # Run twice for references
```

**With Bibliography:**
```bash
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

**Modern (latexmk):**
```bash
latexmk -pdf document.tex  # Handles all compilation steps
```

## Troubleshooting Quick Tips

**Undefined control sequence:**
- Missing package (add `\usepackage{...}`)
- Typo in command name
- Missing math mode delimiter

**Missing $ inserted:**
- Math symbols used outside math mode
- Add `$...$` or `\(...\)` around math

**File not found:**
- Check file path and extension
- Use relative paths or place in same directory
- For images, ensure file extension is specified

**Overfull \hbox:**
- Line too wide to fit
- Add `\sloppy` or break long URLs with `\url{}`
- Use `\linebreak` or rephrase text

**Undefined references:**
- Run LaTeX twice (first pass creates labels, second resolves)
- Check label names match `\ref{...}` commands

## Best Practices

1. **Always compile twice** after adding labels/references
2. **Use meaningful labels**: `\label{sec:intro}` not `\label{s1}`
3. **Keep figures in subfolder**: `figures/image.pdf`
4. **Use vector graphics** (PDF, EPS) when possible
5. **Separate bibliography** into `.bib` file
6. **Version control** your `.tex` files (Git recommended)
7. **Comment your code**: `% This explains the code`
8. **Use packages sparingly**: Only include what you need
9. **Consistent formatting**: Choose one citation style
10. **Test compilation early and often**

## Resources

### Online Documentation
- LaTeX Wikibook: https://en.wikibooks.org/wiki/LaTeX
- Overleaf Learn: https://www.overleaf.com/learn
- CTAN (packages): https://ctan.org
- TeX Stack Exchange: https://tex.stackexchange.com

### Reference Files
See `references/` directory for detailed guides on:
- Quick start and basics
- Mathematical typesetting
- Text formatting and fonts
- Tables and graphics
- Bibliography management
- Troubleshooting common errors

### Templates
See `assets/` directory for ready-to-use templates:
- Academic papers
- Technical reports
- Presentations
- Letters
- Conference papers

## Version History

- **1.0.0** (2025-12-31): Initial manual creation
  - Comprehensive command reference
  - 5 document templates
  - Troubleshooting guide
  - Compilation scripts

## Contributing

To enhance this skill:
1. Add new templates to `assets/`
2. Expand reference guides in `references/`
3. Update SKILL.md quick reference
4. Add helper scripts to `scripts/`
5. Document common patterns and solutions

---

**Created**: Manually curated LaTeX skill
**Status**: Production Ready
**Version**: 1.0.0
**Last Updated**: 2025-12-31
