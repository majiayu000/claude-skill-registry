---
name: veterinary-pubmed-search
description: Search PubMed with veterinary-specific filters and MeSH terms to find relevant animal health research. Handles the sparse, multi-species nature of veterinary literature. Use for veterinary literature searches.
---

# Veterinary PubMed Search

## Overview

Search PubMed for veterinary-relevant literature using optimized query strategies. Veterinary literature is sparser than human medical literature, scattered across species-specific journals, and indexed with different MeSH terms. This skill encodes effective search strategies for finding relevant veterinary evidence.

## When to Use

- User asks for research evidence on a veterinary topic
- User wants to find studies about a treatment, disease, or diagnostic in animals
- User asks "what does the evidence say about [topic] in [species]?"
- User wants to compare treatment options based on published evidence
- Keywords: research, study, evidence, PubMed, literature, journal, published, peer-reviewed, trial, meta-analysis

## Veterinary Search Strategy

### Key MeSH Terms for Veterinary Searches

Use these MeSH qualifiers to filter for veterinary content:
- `"Veterinary"[MeSH] OR "Animals"[MeSH]`
- Species-specific: `"Dogs"[MeSH]`, `"Cats"[MeSH]`, `"Horses"[MeSH]`, `"Cattle"[MeSH]`
- `"Veterinary Medicine"[MeSH]`
- Journal filter: specific veterinary journals (JAVMA, JVIM, Vet Surg, JVECC, Vet Pathol, etc.)

### Key Veterinary Journals

Tier 1 (highest impact veterinary journals):
- Journal of Veterinary Internal Medicine (JVIM)
- Journal of the American Veterinary Medical Association (JAVMA)
- Veterinary Surgery
- Journal of Veterinary Emergency and Critical Care (JVECC)
- Veterinary Pathology
- Veterinary Anaesthesia and Analgesia
- Veterinary Radiology & Ultrasound

Tier 2 (specialty and species-specific):
- Equine Veterinary Journal
- Journal of Feline Medicine and Surgery
- Journal of Small Animal Practice
- Veterinary Dermatology
- Veterinary Ophthalmology
- Veterinary and Comparative Oncology

## Workflow

1. Formulate a structured search query combining:
   - Clinical topic terms
   - Species filter (if specific species is relevant)
   - Study type filter (if looking for specific evidence level)
2. Search PubMed using E-utilities API or standard search interface.
3. Evaluate results for relevance, recency, and species applicability.
4. Apply evidence grading (see `evidence-grading` skill).
5. Summarize findings with citations.

## Limitations

- Veterinary literature is orders of magnitude smaller than human medical literature. Many clinical questions have no species-specific RCTs.
- Many veterinary studies have small sample sizes.
- Publication bias exists (positive results published more than negative).
- Some veterinary evidence is published in non-English journals or regional publications not indexed in PubMed.
