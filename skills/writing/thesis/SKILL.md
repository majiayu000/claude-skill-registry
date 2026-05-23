---
name: thesis-writing
triggers: ["/thesis", "academic", "submission", "literature", "Abgabe", "Exposé", "APA"]
description: Thesis writing skill for MA Artistic Research. Covers academic requirements, submission format, and literature review workflow.
---

# Thesis Writing Skill

## Trigger

Activate when working on:
- Thesis documents in `thesis/`
- Literature review
- Academic submission requirements
- PDF generation for thesis

## Commands

```bash
# Build thesis PDFs
cd thesis/submission && make all
```

## Academic Submission Requirements

See `thesis/academic/Abgabe.md` for full details.

### Teil 1: Vorbereitung

| Deliverable | Details |
|-------------|---------|
| Exposé | 1-2 pages, practical project description |
| Forschungsfrage | ~5 questions, choose one with most potential |
| Literaturrecherche | ~10 papers, APA format, 4-sentence summaries |
| Methodologie | Methods description and justification |

### Teil 2: Dokumentation (~10 pages)

1. **Einleitung** — Background, motivation (funnel: general → specific)
2. **Stand der Forschung** — Literature review
3. **Methodologie** — Methods, justification, ethics
4. **"Meine Forschung"** — Decisions, experiments, reflection
5. **Diskussion** — Summary, implications, limitations
6. **Literatur** — Bibliography (APA format)

## Reference Example

`thesis/academic/thilos-straightA-submission/` contains A-grade example:
- Autoethnographic methodology with video diary
- Iterative: develop → create → reflect → refine
- Theories: "Suspension of Disbelief", "Uncanny Valley Effect"

## Literature Review Workflow

### PDF Processing

PDFs in `thesis/academic/texts/`, extracted text in `texts/extracted/`.

**Available texts:**
- Henke et al. (2019) — Manifest der Künstlerischen Forschung
- Schön (1983) — The Reflective Practitioner
- Borgdorff (2012) — The Conflict of the Faculties
- Frayling (1993) — Research in Art and Design
- Wall (2006) — Autoethnography
- Ellis (2010) — Autoethnografie
- Wesseling (2017) — Q&A

### Handling Large PDFs

**IMPORTANT:** When "PDF too large" error occurs:
1. Use pre-extracted `.txt` from `thesis/academic/texts/extracted/`
2. If none exists: `pdftotext "file.pdf" "extracted/file.txt"`
3. Read the `.txt` file instead

### Progress Tracking

Check `thesis/ROADMAP.md` for current literature review status.
