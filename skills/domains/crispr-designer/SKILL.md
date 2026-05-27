---
name: crispr-designer
description: Designs guide RNA (gRNA) sequences for CRISPR-Cas9 editing, including off-target analysis. Use when a user needs to edit a gene or asks for gRNA sequences.
---
# CRISPR gRNA Designer

This skill designs high-efficiency guide RNAs for gene editing experiments.

## When to use this skill
- When a user provides a gene name (e.g., "TP53"), Ensembl ID, or DNA sequence.
- When the user wants to perform "knockout", "activation" (CRISPRa), or "interference" (CRISPRi).
- When specificity and off-target minimization are requested.

## How to use it
1.  **Identify Target Locus:**
    -   Resolve the gene name to the current reference genome (GRCh38 for humans).
    -   Identify functional domains (exons) that are constitutively expressed.
2.  **Design gRNAs:**
    -   Select 20nt targets adjacent to NGG PAM sites.
    -   Prioritize 5' constitutive exons for knockouts to ensure early truncation.
3.  **Score Candidates:**
    -   Calculate **On-Target Efficiency** (e.g., Rule Set 2 score).
    -   Calculate **Off-Target Specificity** (CFD score) by searching the whole genome for mismatches.
4.  **Output Table:**
    -   Return a markdown table with: Sequence, PAM, On-Target Score, Off-Target Score, and Genomic Location.
    -   Recommend the top 3 guides.
