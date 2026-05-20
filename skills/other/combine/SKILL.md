---
name: combine
description: Assemble individual problem solutions into a single LaTeX document and compile
---

# Solution Assembler

You are assembling individual solved problem files into a single compilable LaTeX homework document.

The target assignment folder is: `$ARGUMENTS`

---

## PHASE 1: Validation

1. Verify that `$ARGUMENTS/solutions/` exists and contains `.tex` files (p1.tex, p2.tex, etc.). If not, stop and tell the user to solve problems first with `/solve`.
2. Use Glob to find all `p*.tex` files in `$ARGUMENTS/solutions/` and sort them numerically.
3. Read `example.tex` from the project root, if available, to extract the preamble.

---

## PHASE 2: Assembly

1. Extract the homework number from the folder name (e.g., "assignment2" → 2).
2. Build the preamble:
   - If `example.tex` exists, use its preamble (everything from `\documentclass` through `\maketitle`).
   - Update `\title{CS 395T Homework N}` with the correct number.
   - Update `\date{...}` with today's date.
   - If `example.tex` doesn't exist, use a sensible default preamble with amsmath, amssymb, amsthm, mathtools, enumerate, graphicx, geometry (1in margins).
3. Read each solution file in order (p1.tex, p2.tex, ...).
4. Concatenate: preamble + all solution contents + `\end{document}`.
5. Write the assembled file to `$ARGUMENTS/solution.tex`.

---

## PHASE 3: Compilation

1. Try running `pdflatex -interaction=nonstopmode` on `$ARGUMENTS/solution.tex` via Bash.
2. If pdflatex is not found, tell the user: "LaTeX is not installed. Install TeX Live or MiKTeX to compile. The .tex file has been generated at `$ARGUMENTS/solution.tex`."
3. If compilation fails:
   - Read the `.log` file to identify errors.
   - Fix the LaTeX issues in solution.tex.
   - Recompile (max 3 attempts).
4. If compilation succeeds, clean up auxiliary files (.aux, .log, .out).

---

## PHASE 4: Report

Tell the user:
- How many problem solutions were assembled
- Where the final document is saved: `$ARGUMENTS/solution.tex`
- Whether PDF compilation succeeded or failed
- If compilation failed, what errors remain
