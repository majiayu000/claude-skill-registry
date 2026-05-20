---
name: solve
description: Solve a single homework problem with verified proofs
---

# CS 395T Problem Solver

You are solving a single graduate-level Continuous Algorithms homework problem. **Mathematical correctness is the #1 priority.** Follow every instruction in CLAUDE.md precisely.

The first argument is the assignment folder, the second is the problem number.
- Assignment folder: `$1`
- Problem number: `$2`

---

## IMPORTANT: Subagent Output Strategy

All subagents MUST write their output to files using the Write tool, NOT return text in their response. This ensures the main agent can reliably read subagent results.

- Solution draft subagent writes to: `$1/solutions/.drafts/p$2_solution.tex`
- Verification subagent writes to: `$1/solutions/.drafts/p$2_verification.txt`
- Style check subagent writes to: `$1/solutions/.drafts/p$2_style.tex` (corrected) or `$1/solutions/.drafts/p$2_style.txt` (APPROVED)

---

## PHASE 1: Validation & Setup

1. Verify that `$1/problems/p$2.tex` exists. If not, stop and tell the user.
2. Read `example.tex` from the project root to internalize the formatting conventions, if available.
3. Read ALL existing YAML files in `knowledge_base/` so you have the full theorem inventory. If `knowledge_base/` is empty or doesn't exist, warn the user to run `/learn $1` first.
4. Create `$1/solutions/` if it does not exist.
5. Create `$1/solutions/.drafts/` for intermediate subagent output files.

---

## PHASE 2: Problem Analysis

1. Read the problem file `$1/problems/p$2.tex`.
2. Identify:
   - What is being asked (prove, compute, construct, find counterexample, etc.)
   - Which theorems/definitions from the knowledge base are likely relevant
   - Whether the problem has subparts (and how many)
   - The difficulty level and key mathematical techniques needed

---

## PHASE 3: Solution Generation

### Step A: Draft Solution

Launch a Task subagent (subagent_type: "general-purpose", model: "opus"):

```
You are a strong graduate math student solving a Continuous Algorithms problem.

PROBLEM:
[paste the full problem text from p$2.tex]

AVAILABLE THEOREMS FROM LECTURE NOTES:
[paste relevant theorems from the knowledge base YAML files]

FORMATTING RULES (from example.tex, if available — follow EXACTLY):
- Use \begin{proof}...\end{proof} for proofs
- Use align* for multi-line math, \[...\] for single display math
- Use \textbf{Case N:} for case analysis
- Use \textbf{Claim:} when stating intermediate claims
- Cite theorems as "By Theorem X.Y (Lecture Z)"
- Cite proof-internal results explicitly: "by equation (3) in the proof of Lemma X.Y (Lecture Z)" or "by the bound established at Line 4 of the proof of Theorem X.Y (Lecture Z)"
- Never silently reuse a result from inside a proof — always cite the specific label or line
- No problem restatement — start directly with the solution
- Subparts use \subsection*{(i)}, \subsection*{(ii)}, etc.

WRITING STYLE (match example.tex exactly, if available):
- Confident, direct, terse prose
- Minimal text between equations — let the math carry the argument
- No filler phrases (see CLAUDE.md for the full banned list)
- Introduce variables inline when first needed
- Use parenthetical justifications: \quad \text{(convexity of } f\text{)}

MATHEMATICAL RIGOR:
- Complete proof, no hand-waving
- Verify every inequality direction
- Handle all edge cases explicitly
- Check that cited theorem hypotheses are satisfied
- Introduce all variables before use

Produce the complete LaTeX solution for this problem (no preamble, no \begin{document} — just the \section*{Problem $2} through the end of the last proof environment).

IMPORTANT: Use the Write tool to save your solution to: [absolute path to $1/solutions/.drafts/p$2_solution.tex]
Do NOT just output the text — you MUST write it to the file.
```

### Step B: Proof Verification

After the draft subagent completes, launch a SEPARATE Task subagent (subagent_type: "general-purpose", model: "opus"):

```
You are a rigorous mathematical proof verifier for a graduate Continuous Algorithms course. Your job is to find errors — be skeptical and thorough.

Read the original problem from: [absolute path to $1/problems/p$2.tex]

Read the proposed solution from: [absolute path to $1/solutions/.drafts/p$2_solution.tex]

AVAILABLE THEOREMS:
[paste the theorems cited in the solution, from the knowledge base]

Verify the solution by checking EACH of the following:

1. LOGICAL CORRECTNESS: Does each step follow from the previous? Are there any non-sequiturs or gaps?
2. INEQUALITY DIRECTIONS: Are all inequalities (≤, ≥, <, >) in the correct direction? Check each one.
3. THEOREM APPLICATION: For each cited theorem or proof-internal result (equation, line, intermediate claim), are ALL hypotheses satisfied? For proof-internal citations, verify that the cited label/line actually establishes what is claimed.
4. EDGE CASES: Are boundary cases handled? (zero vectors, empty sets, degenerate inputs, equality cases)
5. VARIABLE SCOPING: Are all variables properly introduced before use? Are quantifiers correct?
6. ALGEBRAIC CORRECTNESS: Check key algebraic manipulations, especially signs, exponents, and factoring.
7. CONCLUSION: Does the final statement actually prove what was asked?

IMPORTANT: Use the Write tool to save your verdict to: [absolute path to $1/solutions/.drafts/p$2_verification.txt]
Write either "VERIFIED" if the proof is correct, or list errors as:
ERROR: [description of the error, which step it's in, and what the correct approach should be]

Be extremely thorough. It is better to flag a potential issue than to miss a real error.
```

**After the verifier completes, read `p$2_verification.txt`:**
- If VERIFIED, proceed to Step C.
- If errors were found:
  - Launch a NEW solution generator subagent with the original problem PLUS the error feedback. Instruct it to read `p$2_solution.tex`, fix the listed errors, and overwrite the file.
  - Launch a fresh verifier to re-check and overwrite `p$2_verification.txt`.
  - Repeat up to 3 times. If still failing after 3 attempts, prepend a LaTeX comment `% NOTE: This solution could not be fully verified — review manually` to the solution file.

### Step C: Style & Formatting Check

After verification passes, launch a Task subagent (subagent_type: "general-purpose", model: "sonnet"):

```
You are a style and formatting editor for a LaTeX math homework document.

Read the reference document style from: example.tex, if available (in the project root)

Read the solution to check from: [absolute path to $1/solutions/.drafts/p$2_solution.tex]

REFERENCE PATTERNS (from example.tex, if available):
- \section*{Problem N} for problem headings
- \subsection*{(i)} for subparts (lowercase roman numerals)
- \begin{proof}...\end{proof} for proofs
- align* for multi-line math
- \[...\] for display math (NEVER $$...$$)
- \textbf{} for structural labels
- \bigskip\noindent\textit{Counterexample.} for counterexamples
- Parenthetical justifications in math: \quad \text{(reason)}

Check for:
1. FORMATTING: Does it match the reference patterns above exactly?
2. AI-SOUNDING PHRASES: Flag any of these — "delve", "it's important to note", "let's", "straightforward", "it can be shown that", "obviously", "clearly" (unless truly trivial), "we can see that", "interestingly", "notably", "crucial", "vital", "in order to", excessive "Note that"
3. TONE: Does it sound like a strong, confident math student? Not like a textbook, not like AI?
4. LATEX CORRECTNESS: Are there any LaTeX syntax issues?

If changes are needed, use the Write tool to save the CORRECTED LaTeX to: [absolute path to $1/solutions/.drafts/p$2_style.tex]
If no changes needed, use the Write tool to write "APPROVED" to: [absolute path to $1/solutions/.drafts/p$2_style.txt]
```

---

## PHASE 4: Finalize

1. Determine the final solution:
   - If `$1/solutions/.drafts/p$2_style.tex` exists, use that.
   - Otherwise use `$1/solutions/.drafts/p$2_solution.tex`.
2. Copy the final solution to `$1/solutions/p$2.tex`.
3. Delete the `.drafts/` directory contents for this problem (p$2_solution.tex, p$2_verification.txt, p$2_style.*).
4. If `.drafts/` is now empty, delete it.

---

## PHASE 5: Report

Tell the user:
- Whether the solution passed verification on the first attempt vs. required retries
- Whether the style check made corrections or approved as-is
- If the solution could not be fully verified (flagged for manual review)
- Where the solution file is saved: `$1/solutions/p$2.tex`
- Remind the user to run `/combine $1` after solving all problems to assemble the final document
