---
name: agent-tailor
description: Create tailored resume from job + source resume. Orchestrates the rewriting of bullet points to emphasize relevant experience without fabrication.
---

# Tailor Agent

## Overview

The Tailor Agent creates a new version of the resume optimized for a specific job.

## Workflow Definition

1.  **Input**: Resume JSON, Job Description.
2.  **Analysis**: Identify missing keywords from Scorer Agent.
3.  **Tailoring**: Call `resume-tailor` skill to rewrite experience sections.
    *   *Constraint*: Must not invent new facts.
4.  **Validation**: Call `schema-validate-resume` on tailored output.
5.  **Re-scoring**: (Optional) Send back to Scorer Agent to verify improvement.
6.  **Output**: Tailored Resume JSON.
