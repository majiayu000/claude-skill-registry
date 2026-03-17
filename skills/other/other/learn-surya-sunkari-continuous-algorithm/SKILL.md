---
name: learn
description: Index lecture note PDFs into the knowledge base
---

# Knowledge Base Indexer

You are indexing lecture notes from a CS 395T (Continuous Algorithms) assignment into a persistent knowledge base of theorems, definitions, and lemmas.

The target assignment folder is: `$ARGUMENTS`

---

## PHASE 1: Validation

1. Verify that `$ARGUMENTS/notes/` exists and contains `.pdf` files. If not, stop and tell the user.
2. Create the `knowledge_base/` directory at the project root if it does not exist.
3. List all existing YAML files in `knowledge_base/` so you know what's already indexed.

---

## PHASE 2: Index New Notes

For each PDF file in `$ARGUMENTS/notes/`:

1. Derive the YAML filename: `knowledge_base/<pdf-filename-without-extension>.yaml`
2. Check if this YAML file already exists. If it does, skip this PDF and tell the user it's already indexed.
3. If not indexed yet, read the PDF using the Read tool. For PDFs longer than 10 pages, read in chunks using the `pages` parameter.
4. Extract ALL of the following into structured YAML:
   - **Definitions** (with number and full statement)
   - **Theorems** (with number, name if any, full statement, and proof sketch if short)
   - **Lemmas** (with number, name if any, full statement)
   - **Corollaries** (with number and full statement)
   - **Propositions** (with number and full statement)
   - **Key remarks** (only if they state a useful result)
   - **Key intermediate results within proofs** — if a proof contains a numbered equation, a named intermediate claim, or a step that is independently useful, capture it in `proof_notes`.
5. Write the YAML file following this schema:

```yaml
source: "filename.pdf"
lecture_number: 5
title: "Lecture title extracted from PDF"
items:
  - type: theorem          # theorem | lemma | definition | corollary | proposition | remark
    number: "5.1"          # numbering as it appears in the notes
    name: "Named theorem"  # if the theorem has a name, otherwise empty string
    statement: |
      Full mathematical statement in plain text with LaTeX math notation
    context: "Brief note on when/how this result is typically used"
    proof_notes:           # optional — omit if the proof has no citable internals
      - label: "(3)"       # equation/line label as it appears in the notes (e.g. "(3)", "Line 4", "Claim 1")
        content: |
          The exact equation or claim in LaTeX math notation
        description: "What this equation/step establishes and when it is useful to cite directly"
```

Populate `proof_notes` whenever:
- The proof contains a numbered or labeled equation that could be reused independently
- The proof establishes an intermediate claim or inequality that is stronger or more specific than the theorem statement itself
- A specific line or step is the crux of the argument and could be invoked directly in another proof

---

## PHASE 3: Report

Tell the user:
- How many PDFs were found in `$ARGUMENTS/notes/`
- How many were newly indexed vs. already indexed
- Total number of items extracted (theorems, definitions, lemmas, etc.) from newly indexed PDFs
- Where the YAML files were saved
