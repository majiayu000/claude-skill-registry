---
name: convert
description: Convert homework PDF or problem screenshots to exact LaTeX representations
---

# Homework to LaTeX Converter

You are converting homework problems into their **exact** LaTeX representations. Accuracy is paramount — the output must be a character-perfect transcription of the mathematical content.

The target assignment folder is: `$ARGUMENTS`

---

## IMPORTANT: Subagent Output Strategy

All subagents in this skill MUST write their output to files using the Write tool, NOT return text in their response. This ensures the main agent can reliably read subagent results.

- Transcription subagents write to: `$ARGUMENTS/problems/pN.tex`
- Verification subagents write to: `$ARGUMENTS/problems/pN_verification.txt`

After all subagents finish, the main agent reads these files to check results and clean up verification files.

---

## PHASE 1: Input Detection & Validation

Auto-detect the input mode by checking in this order:

1. **PDF mode**: Use Glob to check for any `.pdf` file in `$ARGUMENTS/` (NOT in `$ARGUMENTS/notes/`). If found, use PDF mode.
2. **Screenshot mode**: Check if `$ARGUMENTS/screenshots/` exists with `problem*` subdirectories containing image files. If found, use screenshot mode.
3. **Neither found**: Stop and tell the user to either place a homework PDF in `$ARGUMENTS/` or create screenshot folders in `$ARGUMENTS/screenshots/problem1/`, etc.

Create `$ARGUMENTS/problems/` if it does not exist.

Tell the user which mode was detected before proceeding.

---

## PDF MODE

### Phase 2P: Read & Split PDF

#### Step A: Read the Full PDF

1. Identify the PDF file in `$ARGUMENTS/` (if multiple PDFs exist, exclude any in `notes/` and pick the one that looks like a homework — or ask the user).
2. Read the PDF using the Read tool. For PDFs longer than 10 pages, read in chunks of 10-20 pages using the `pages` parameter.
3. As you read, identify:
   - **Problem boundaries**: Look for headings like "Problem 1", "Problem 2", "Question 1", etc.
   - **Footnotes**: Note which footnotes belong to which problem. Footnotes are typically numbered (e.g., superscript 1, 2, 3) and appear at the bottom of the page or end of the document.
   - **Shared preamble text**: Any setup text that applies to multiple problems (e.g., "For problems 1-3, assume X..."). This should be included at the top of each relevant problem file.

#### Step B: Transcribe Each Problem

For each identified problem, launch a Task subagent (subagent_type: "general-purpose", model: "opus"). You may launch multiple subagents in parallel since they write to separate files.

Subagent prompt:

```
You are an expert LaTeX transcriber. Your job is to produce an EXACT transcription of a math problem from a PDF into LaTeX.

Read the following PDF file and extract ONLY the specified problem:
[PDF file path and page range]

PROBLEM TO EXTRACT: Problem N
PROBLEM BOUNDARIES: Starts at [description] and ends at [description]

FOOTNOTES BELONGING TO THIS PROBLEM:
[list any footnotes that are referenced within this problem's text]

SHARED PREAMBLE (include at the top if present):
[any shared setup text that applies to this problem]

RULES — follow these precisely:
1. EXACT TRANSCRIPTION: Reproduce every symbol, subscript, superscript, fraction, summation, integral, matrix, and piece of text exactly as it appears. Do not paraphrase, rephrase, simplify, or add anything.
2. MATH NOTATION: Use standard LaTeX math commands. Use \mathbb for blackboard bold, \mathbf for bold vectors, \text{} for text within math mode, \operatorname{} for named operators, \mathcal for calligraphic letters, \ell for script l.
3. FORMATTING: Preserve the visual structure — numbered parts like (i), (ii), (iii) or (a), (b), (c) should be kept as-is. Preserve paragraph breaks and line breaks where they appear meaningful.
4. NO PREAMBLE: Output only the problem content — no \documentclass, no \begin{document}, no packages. Just the raw LaTeX content that would go inside a document body.
5. NO SOLUTIONS: Only transcribe the problem statement. If a solution or hint appears, do not include it.
6. DISPLAY MATH: Use \[...\] for displayed equations (never $$...$$). Use align* if the original shows aligned/numbered equations.
7. INLINE MATH: Use $...$ for inline math.
8. FOOTNOTES: Include footnotes using \footnote{} inline where the superscript reference appears in the problem text. Transcribe the footnote content exactly.
9. DOUBLE-CHECK: After transcribing, re-read the PDF and verify every symbol matches. Pay special attention to:
   - Subscripts vs superscripts
   - Similar-looking symbols (ε vs ∈, ≤ vs <, ⊂ vs ⊆)
   - Parentheses vs brackets vs braces
   - Bold vs regular vs calligraphic letters
   - Summation/product bounds (above vs below)
   - Fraction numerators and denominators
   - Footnote numbering and content

IMPORTANT: Use the Write tool to save your transcription to: [output file path for pN.tex]
Do NOT just output the text — you MUST write it to the file.
```

#### Step C: Verification

After transcription subagents complete, launch SEPARATE verification subagents (subagent_type: "general-purpose", model: "opus") — one per problem, can run in parallel.

Subagent prompt:

```
You are a LaTeX transcription verifier. You will be given a PDF of a math homework and a proposed LaTeX transcription of one problem. Your job is to find ANY discrepancies.

Read the PDF:
[PDF file path and page range]

PROBLEM BEING VERIFIED: Problem N

Read the proposed transcription from: [path to pN.tex]

Compare the PDF to the LaTeX character by character for this problem. Check:
1. Every mathematical symbol matches exactly
2. Every subscript and superscript is correct
3. All fractions, sums, products, integrals have correct bounds
4. Text content matches word-for-word
5. Numbering of parts/subparts matches
6. No content is missing or added
7. Parentheses, brackets, and delimiters match
8. All footnotes referenced in this problem are included with exact content
9. Any shared preamble text is correctly included

IMPORTANT: Use the Write tool to save your verdict to: [path to pN_verification.txt]
Write either "VERIFIED" if the transcription is exact, or list discrepancies as:
DISCREPANCY: [what's wrong and what it should be]
```

#### Step D: Check Results & Retry

1. Read each `pN_verification.txt` file.
2. If VERIFIED, the problem is done.
3. If discrepancies were found:
   - Launch a new transcription subagent with the original PDF PLUS the discrepancy feedback. Instruct it to read the current pN.tex, fix the listed errors, and overwrite pN.tex.
   - Launch a fresh verifier to re-check and overwrite pN_verification.txt.
   - Repeat up to 3 times. If still failing, prepend a LaTeX comment to pN.tex: `% NOTE: Transcription could not be fully verified — check against original PDF`
4. Delete all `pN_verification.txt` files when done.

---

## SCREENSHOT MODE

### Phase 2S: Convert Screenshots

For each `$ARGUMENTS/screenshots/problemN/` folder:

#### Step A: Read Screenshots

1. Use Glob to find all image files in the folder (*.png, *.jpg, *.jpeg, *.bmp, *.webp).
2. Sort them by filename (they may be ordered as page1.png, page2.png, etc. or similar).
3. Read each image using the Read tool. If a problem spans multiple screenshots, read them all in order to get the complete problem.

#### Step B: Transcribe to LaTeX

Launch a Task subagent (subagent_type: "general-purpose", model: "opus"). You may launch multiple subagents in parallel since they write to separate files.

Subagent prompt:

```
You are an expert LaTeX transcriber. Your job is to produce an EXACT transcription of a math problem from screenshots into LaTeX.

Read the following image files using the Read tool:
[list all image file paths for this problem]

RULES — follow these precisely:
1. EXACT TRANSCRIPTION: Reproduce every symbol, subscript, superscript, fraction, summation, integral, matrix, and piece of text exactly as it appears in the screenshot. Do not paraphrase, rephrase, simplify, or add anything.
2. MATH NOTATION: Use standard LaTeX math commands. Use \mathbb for blackboard bold, \mathbf for bold vectors, \text{} for text within math mode, \operatorname{} for named operators, \mathcal for calligraphic letters, \ell for script l.
3. FORMATTING: Preserve the visual structure — numbered parts like (i), (ii), (iii) or (a), (b), (c) should be kept as-is. Preserve paragraph breaks and line breaks where they appear meaningful.
4. NO PREAMBLE: Output only the problem content — no \documentclass, no \begin{document}, no packages. Just the raw LaTeX content that would go inside a document body.
5. NO SOLUTIONS: Only transcribe the problem statement. If a solution or hint appears, do not include it.
6. DISPLAY MATH: Use \[...\] for displayed equations (never $$...$$). Use align* if the original shows aligned/numbered equations.
7. INLINE MATH: Use $...$ for inline math.
8. FOOTNOTES: If footnotes are visible in the screenshots, include them using \footnote{} inline where the superscript reference appears.
9. DOUBLE-CHECK: After transcribing, re-read the screenshot and verify every symbol matches. Pay special attention to:
   - Subscripts vs superscripts
   - Similar-looking symbols (ε vs ∈, ≤ vs <, ⊂ vs ⊆)
   - Parentheses vs brackets vs braces
   - Bold vs regular vs calligraphic letters
   - Summation/product bounds (above vs below)
   - Fraction numerators and denominators

IMPORTANT: Use the Write tool to save your transcription to: [output file path for pN.tex]
Do NOT just output the text — you MUST write it to the file.
```

#### Step C: Verification

After transcription subagents complete, launch SEPARATE verification subagents (subagent_type: "general-purpose", model: "opus") — one per problem, can run in parallel.

Subagent prompt:

```
You are a LaTeX transcription verifier. You will be given screenshots of a math problem and a proposed LaTeX transcription. Your job is to find ANY discrepancies.

Read the following image files using the Read tool:
[list all image file paths for this problem]

Then read the proposed transcription from: [path to pN.tex]

Compare the screenshot to the LaTeX character by character. Check:
1. Every mathematical symbol matches exactly
2. Every subscript and superscript is correct
3. All fractions, sums, products, integrals have correct bounds
4. Text content matches word-for-word
5. Numbering of parts/subparts matches
6. No content is missing or added
7. Parentheses, brackets, and delimiters match
8. All visible footnotes are included with exact content

IMPORTANT: Use the Write tool to save your verdict to: [path to pN_verification.txt]
Write either "VERIFIED" if the transcription is exact, or list discrepancies as:
DISCREPANCY: [what's wrong and what it should be]
```

#### Step D: Check Results & Retry

1. Read each `pN_verification.txt` file.
2. If VERIFIED, the problem is done.
3. If discrepancies were found:
   - Launch a new transcription subagent with the original screenshots PLUS the discrepancy feedback. Instruct it to read the current pN.tex, fix the listed errors, and overwrite pN.tex.
   - Launch a fresh verifier to re-check and overwrite pN_verification.txt.
   - Repeat up to 3 times. If still failing, prepend a LaTeX comment to pN.tex: `% NOTE: Transcription could not be fully verified — check against original screenshot`
4. Delete all `pN_verification.txt` files when done.

---

## PHASE 3: Report

Tell the user:
- Which input mode was used (PDF or screenshots)
- How many problems were converted
- Which problems passed verification on the first attempt vs. required retries
- Any problems that could not be fully verified
- Where the output files are saved
- Remind the user they can now run `/solve $ARGUMENTS` to generate solutions
