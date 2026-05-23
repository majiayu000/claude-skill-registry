---
name: agent-scorer
description: Generate semantic + keyword match score. Compares resume content against job description to calculate a fit score and identify gaps.
---

# Scorer Agent

## Overview

The Scorer Agent is responsible for evaluating the fit between a candidate and a job description.

## Workflow Definition

1.  **Input**: Resume JSON, Job Description Text.
2.  **Vectorization**:
    *   Embed Resume Skills/Experience (`vectorize-ollama`)
    *   Embed Job Description (`vectorize-ollama`)
3.  **Semantic Match**: Calculate cosine similarity (`similarity-cosine`).
4.  **Keyword Statistics**: Compare explicit keywords (`compare-keywords`).
5.  **Scoring Logic**:
    *   Combine Semantic Score (weight 0.7) + Keyword Score (weight 0.3).
6.  **Output**: Score object `{ total_score: float, details: {...} }`.
