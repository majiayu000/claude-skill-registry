---
name: init
description: Initialize your job search project. Imports your resume(s), creates the Resume Corpus, and sets up directory structure.
argument-hint: [resume-file-path]
---

# Init Workflow

**Load and execute:** `workflows/init/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Introduces both agents (Max and Scout)
2. Obtains privacy agreement before processing personal data
3. Sets up directory structure (profile/, applications/, research/)
4. Imports resume(s) and creates the structured Resume Corpus
5. **Analyzes PDF resume layout** to create a matching template for PDF generation (Step 4b)
6. Optionally imports writing samples for voice matching
7. **Generates a Voice Profile** from writing samples to capture tone, style, and signature elements (Step 5a)
8. Suggests running scoping-interview next

**PDF Template Analysis (Step 4b):**
When a PDF resume is imported, this workflow analyzes its visual structure and creates `profile/resume_template.yaml`. This template captures:
- Layout (single/two-column, margins, page size)
- Header styling (name position, contact layout)
- Section ordering and formatting
- Typography (fonts, sizes, colors)
- Experience bullet styles and date positioning

The template ensures tailored resumes maintain the same look and feel as your original. If no PDF tools are installed, the template is still saved for later use.

**Voice Profile Generation (Step 5a):**
When writing samples are imported, this workflow analyzes them to create `profile/voice_profile.json`. This profile captures:
- Tone (formality, confidence, energy)
- Sentence structure patterns and vocabulary
- Voice preferences (active/passive, first/third person)
- Rhetorical patterns (argument structure, evidence style)
- Signature phrases and distinctive elements
- Generation guidance (dos, don'ts, example sentences)

The voice profile ensures cover letters and other generated content match your authentic writing style.

Follow all steps exactly as written. Wait for user input where the workflow specifies interaction points.

$ARGUMENTS
