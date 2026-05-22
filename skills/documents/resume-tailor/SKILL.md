---
name: resume-tailor
description: Compose tailored resume with no fabricated content. Uses LLM to rewrite bullet points to align with job description keywords while strictly adhering to facts.
---

# Skill: Resume Tailor

## Summary
The core engine of ROLESENSE.ai. It takes a Master Resume and a Job Description, calculates a match score, and generates a tailored version of the resume.

## When to Use
The agent SHOULD use this skill when:
- The user requests to "tailor," "optimize," or "rewrite" a resume for a job.
- The user asks for a "Match Score" or "Gap Analysis."
- The user wants to export the final PDF.

## Primary Goal
Generate a tailored resume that maximizes keyword overlap with the Job Description WITHOUT fabricating experience.

## High-Level Procedure
1. **Load Data**: Retrieve Master Resume (JSON) and Job Description (JSON).
2. **Score**: Calculate Cosine Similarity between resume embeddings and JD embeddings.
3. **Analyze**: Identify missing keywords (Gap Analysis).
4. **Tailor (RAG)**:
   - For each experience block, retrieve relevant bullets.
   - Rephrase bullets to highlight JD keywords using `scripts/rewrite_bullet.py`.
5. **Verify**: Run `scripts/audit_fabrication.py` to ensure no new facts were added.
6. **Format**: Generate final layout/PDF.

## Inputs
- `master_resume_json`: The source data.
- `job_description_json`: The target requirements.

## Constraints & Guardrails
- **NON-FABRICATION**: The `audit_fabrication.py` script MUST return True before outputting the result.
- **ATS Compliance**: Output must avoid columns or graphics if "ATS Mode" is selected.
- **User Approval**: Always present the "Diff" (changes made) before finalizing.

## References
- `/examples/tailoring_examples.md`: Examples of good vs. bad rewriting (hallucination prevention).
- `/scripts/vectorize.py`: Handles Ollama embedding generation.
- `/scripts/audit_fabrication.py`: Logic to compare entities in source vs. output.
