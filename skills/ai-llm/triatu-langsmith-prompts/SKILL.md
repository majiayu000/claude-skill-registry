---
name: triatu-langsmith-prompts
description: "LangSmith prompt governance for Triatu. Use when moving prompts out of code, versioning them, or documenting prompt management."
---

# Triatu LangSmith Prompts

## Quick start

- Keep prompts out of code; reference them by name/version.
- Store only prompt identifiers in code or config.
- Use env vars for LangSmith credentials.

## Workflow

1) Create a LangSmith project for Triatu prompts.
2) Define prompt templates with variables and clear naming.
   - `triatu-scan`
   - `triatu-recipe-chef`
   - `triatu-recipe-fate`
3) Version prompts and document intended use per feature.
4) Fetch prompt templates at runtime with caching.
5) Provide fallback to local prompt (for offline/dev).
6) Log prompt version used (no prompt content in logs).

## Guardrails

- Never commit API keys.
- Avoid storing PII in prompts or logs.
- Changes to prompts require doc updates and test review.

## References

- `docs/AI_PROMPTS.md`
- `docs/SECURITY.md`
- `docs/DEVELOPMENT.md`
