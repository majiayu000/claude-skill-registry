---
name: tailor-resume
description: Modify an existing resume for a specific job posting. Requires a starting resume to modify, then enhances it with corpus content and interview-discovered experiences.
argument-hint: [company-name] [starting-resume-path]
---

# Tailor Resume Workflow

**Load and execute:** `workflows/tailor-resume/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. **Requires a starting resume** — asks user to select from existing resumes or provide a path
2. Loads the starting resume, corpus, and parsed job posting
3. Scores the starting resume against job requirements
4. Applies "easy wins" from corpus content not in the starting resume
5. Conducts interactive gap-closing interview for remaining gaps
6. Updates corpus with confirmed new entries
7. **Saves both Markdown and PDF** versions of the tailored resume

**PDF Output (Step 7b):**
After saving the Markdown resume, this workflow automatically generates a PDF version if PDF tools are available:
- **WeasyPrint** (preferred): `pip install weasyprint`
- **Typst** (fallback): https://typst.app/

The PDF uses styling from `profile/resume_template.yaml` (created during `/init` if you imported a PDF). If no template exists, default professional styling is applied.

**Output files:**
- `applications/resumes/{company}-{role}.md` — Always created
- `applications/resumes/{company}-{role}.pdf` — Created if PDF tools installed

**Graceful fallback:** If no PDF tools are installed, the workflow completes successfully with the Markdown file and provides install instructions for enabling PDF generation.

This is the heart of Job Coach & Scout. The starting resume requirement ensures we're modifying real content rather than generating from scratch.

$ARGUMENTS
