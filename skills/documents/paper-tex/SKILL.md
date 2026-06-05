---
name: paper-tex
description: Typeset a working paper or journal submission in house-style LaTeX from any draft — Markdown, Word (.docx), TeX, ODT, RTF, or HTML. Convert with pandoc, wrap in an EB Garamond template, build the PDF with latexmk, and prepare for a specific journal (spacing, page limit, anonymization, disclosures, citation style). Use for "format/typeset/convert my paper to LaTeX", "make a working paper", "prepare this for submission to <journal>".
argument-hint: "[path to the draft, and the target journal (or 'working paper')]"
---

# Paper formatter (LaTeX)

Turn a draft in any common format into a clean, house-style LaTeX paper and build the PDF. The mechanical work runs through a committed driver, `scripts/format_paper.py`: it detects the input format, converts the body with **pandoc**, wraps it in the EB Garamond template under `assets/`, and builds with **latexmk**. The house-specific finishing — captions with notes, disclosure sections, SI cross-references — is done by hand afterward, and the steps are below.

The house style: 12pt EB Garamond, 1-inch margins, author-date citations (`apsr`), numbered sections with unnumbered subsections, a single-spaced title block, the introduction on its own page, figures and tables placed where they are written (`[H]`), and every exhibit carrying a title with an italic *Note:* beneath it (`\figcap`).

Paths below are relative to this skill directory. Set `SKILL` to it once:

```bash
SKILL=~/Documents/GitHub/resources/open-science-skills/plugin/skills/paper-tex
```

## Step 0 — Ask for the journal specifics first

Formatting is journal-dependent, and the defaults are not always what you want. **Before converting, confirm the parameters** (use `AskUserQuestion` for anything not already stated). The ones that change the output:

| Parameter | Driver flag | Default | Notes |
|---|---|---|---|
| Target journal / working paper | — | working paper | sets the rest |
| Body spacing | `--spacing single\|double` | `single` | single fits tight page limits; do not double-space past a hard limit |
| Page / word limit | — | none | if a limit binds, prefer single spacing and tighten `\bibsep` before cutting content |
| Anonymized for review | `--anon` | off | blanks the author; keep identifying disclosures on a separate title page |
| Intro placement | `--cover-page` | intro on its own page | only pass `--cover-page` if the venue requires the intro on the title page |
| Citation style | edit `\bibliographystyle` in `assets/preamble.tex` | `apsr` | swap the `.bst` per journal |
| Font | edit `\usepackage{ebgaramond}` | EB Garamond | swap only if a journal mandates a family |
| Required disclosures | added by hand | none | data availability, ethics, funding, COI — see house-finishing |

A few profiles to start from (confirm against the current author guide):

- **Working paper** — `--spacing double`, named author, `\today`, intro on its own page.
- **Journal of Politics (short article)** — `--spacing single`, `--anon`, 15-page limit, data-availability + ethics in the manuscript, other disclosures on a separate title page.
- **Generic double-anonymous submission** — `--anon`, `--spacing double`, no acknowledgments or funding in the body.

## Prerequisites

Verified on macOS with TeX Live 2025 and pandoc 3.8. Required on `PATH`: `pandoc`, `latexmk` + `pdflatex` (a full TeX distribution), and `pdfinfo`/`pdftoppm` (poppler) for page counts and proof renders. The `ebgaramond`, `apsr` (texlive `harvard` collection), `calc`, `booktabs`, `threeparttable`, `xr-hyper`, and `newunicodechar` packages must be installed — all ship with a full TeX Live / MacTeX.

```bash
# macOS
brew install pandoc poppler        # TeX via MacTeX (basictex users: tlmgr install ebgaramond apsr collection-latexextra)
# Debian/Ubuntu
# apt-get install -y pandoc texlive-full poppler-utils
```

## Run the driver (primary path)

One command converts and builds. These are the exact invocations used to validate the skill:

```bash
# Markdown -> single-spaced PDF, intro on its own page. A sibling references.bib
# and any figure the draft references by a relative path are staged automatically.
python3 "$SKILL/scripts/format_paper.py" draft.md --out build \
  --title "Democracy and Nationalism, Reconsidered" \
  --author "Jane Q. Researcher" \
  --abstract "Do citizens who value democracy reject nationalism? ..." \
  --keywords "nationalism; democratic values; national identity; ISSP" \
  --spacing single --build

# Word (.docx) -> same; embedded images are extracted into build/media automatically
python3 "$SKILL/scripts/format_paper.py" draft.docx --out build --title "..." --build

# Existing TeX (full document or a body fragment) -> rewrapped in the house template
python3 "$SKILL/scripts/format_paper.py" draft.tex --out build --title "..." --build

# Main text + SI together (SI gets SI-A.. section labels, SI-1.. float numbers,
# and an \externaldocument cross-reference so \ref reaches SI from the main text)
python3 "$SKILL/scripts/format_paper.py" main.md --si si.md --out build --build
```

Output lands in `build/`: `main.tex`, `body.tex`, `preamble.tex` (and `si.tex`/`si_body.tex` with `--si`), plus `main.pdf` when `--build` is set. The driver prints the page count and the house-finishing checklist.

Full options: `python3 "$SKILL/scripts/format_paper.py" --help`. Notable flags: `--anon`, `--cover-page`, `--spacing`, `--bib NAME`, `--engine pdflatex|xelatex`, `--no-here-floats`.

## House-finishing (by hand, after the driver)

The driver gets the structure right; these four steps make it house style. Do them in `build/body.tex` (and `si_body.tex`), then rebuild with `latexmk -pdf -bibtex main.tex` in `build/`.

1. **Captions → `\figcap{title}{note}`.** Replace every plain `\caption{...}` with a title and a note that makes the exhibit self-contained. Put confidence-interval, N, and source details **in the note only** — never baked into the figure image, and never stated in both the figure and the note. Example:
   ```latex
   \figcap{Cross-national heterogeneity in the rights--exclusion slope}%
     {Points are country-specific within-country slopes, adjusted for age, gender,
      education, and left--right placement; bars are 95\% confidence intervals.
      Colors denote region-regime group. $n = 43{,}517$ in 29 countries.}
   ```
2. **Disclosures as `\section*{}` with full sentences** — never a bold word and a period. Add what the journal requires:
   ```latex
   \section*{Data availability}
   The ISSP 2023 module (ZA10010) is available from the GESIS Data Archive; replication
   code accompanies the submission and will be deposited on acceptance.

   \section*{Ethics}
   This study analyzes secondary, publicly archived, de-identified survey data and did
   not require human-subjects review.
   ```
   Identifying disclosures (funding, acknowledgments, ORCID, COI) go on a separate, non-anonymous title page for double-anonymous review, not in the body.
3. **Thread SI cross-references.** With `--si`, `\externaldocument{si}` is already set, so `\ref{}`/`\Cref{}` reach SI labels. Make sure the main text actually points readers to the supplementary tables and figures where they support a claim.
4. **Remove bold-period run-in subheaders.** Convert `\textbf{Multi-group CFA.}`-style leads into a real `\subsection{}` (or spell the point into the sentence). This is the `sci-edit` rule against bold-text-with-period headings; the formatter does not auto-catch it.

Two more house rules the formatter cannot enforce for you: tables get a title and note beneath them (use `\figcap` inside `threeparttable`/`table`, booktabs rules, no vertical lines), and case or country names that carry the argument are written plainly — not bolded or otherwise over-emphasized — even when they do special work.

## What the template encodes (reference)

`assets/preamble.tex` and `assets/main.template.tex` already set: EB Garamond + T1; 1-inch margins; `setspace`; `\setcounter{secnumdepth}{1}`; `\captionsetup{labelfont=bf, labelsep=colon, ...}`; the `\figcap` macro; `float` for `[H]`; `natbib` + `apsr`; `xr-hyper`; a single-spaced `{\singlespacing \maketitle ... abstract ... keywords}` block followed by `\newpage`; and pandoc-compatibility shims (`\tightlist`, `\real`, a working `\pandocbounded`, `calc`, `newunicodechar`) so converted bodies build without hand-patching. To retarget a journal, edit the font and `\bibliographystyle` lines in the preamble; leave the body alone.

## Gotchas (learned building this)

- **Figures from pandoc overflow the margin unless `\pandocbounded` is real.** Pandoc emits width-less `\includegraphics` wrapped in `\pandocbounded` and, for a body fragment, does *not* emit the macro's definition. The preamble defines the genuine scaling version; a no-op `\providecommand{\pandocbounded}[1]{#1}` lets wide figures run off the page.
- **`.docx` tables need `calc`.** Word tables carry explicit column widths, so pandoc writes `p{(\columnwidth - ...) * \real{0.5}}`. Without `\usepackage{calc}` this throws `! Missing number, treated as zero.` The preamble loads it.
- **Extracted media must be out-relative.** The driver runs pandoc with `cwd=build/` and `--extract-media=media`, so the image path is `media/...` and resolves at build time. Running pandoc elsewhere writes a path that breaks when latexmk runs from `build/`.
- **Stage assets before building.** `--build` needs the bibliography and any local figures in `build/`. The driver auto-copies a sibling `references.bib` and any figure referenced by a relative path; supply `--bib NAME` if the file is named differently, and copy figures in by hand if they live elsewhere.
- **EB Garamond builds with pdflatex** — no xelatex required. Use `--engine xelatex` only if you switch to an OpenType font.
- **`apsr.bst`** lives in the texlive `harvard` collection (`bibtex/bst/harvard/apsr.bst`); basictex users install it with `tlmgr`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `! Missing number, treated as zero.` after a table | a Word/HTML table needs `calc` — it is in the preamble; confirm `\input{preamble}` is present |
| Figure runs past the right margin | `\pandocbounded` is a no-op — use the preamble's real definition |
| `File 'media/...png' not found` | run via the driver (it sets pandoc's cwd) rather than calling pandoc by hand |
| `Citation 'x' undefined` after build | the `.bib` was not staged — pass `--bib NAME` or copy it into `build/`; the driver auto-copies a sibling `references.bib` |
| Over a hard page limit | switch to `--spacing single`, then add `\setlength{\bibsep}{4pt}` before cutting content |
| Author name leaks in a double-anonymous build | pass `--anon`; move funding/acknowledgments/ORCID to a separate title page |
