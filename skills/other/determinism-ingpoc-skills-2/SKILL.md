---
name: determinism
description: "Use when verifying outcomes with code instead of LLM judgment, versioning prompts with hashes, or ensuring reproducible agent behavior. Load for any critical verification. Scripts return boolean exit codes, not subjective assessments. Prompts use semantic versioning with SHA256 validation."
keywords: verification, deterministic, hash, version, reproducible, code-not-judgment
---

# Determinism

Reproducible outcomes through code verification and prompt versioning.

## Core Principle

> "Claude can run scripts without loading either the script or the PDF into context. And because code is deterministic, this workflow is consistent and repeatable." - Anthropic Engineering

## Instructions

1. Replace LLM judgment with script verification
2. Version prompts with semantic versioning
3. Hash-validate critical prompts: `scripts/validate-prompt.sh`
4. Use exit codes (0 = pass, 1 = fail), not text

## LLM Judgment vs Code Verification

| Task | LLM (Bad) | Code (Good) |
|------|-----------|-------------|
| Tests passed? | "The tests appear to pass" | `pytest; echo $?` → 0 or 1 |
| Valid JSON? | "This looks like valid JSON" | `python -c "json.load(f)"` |
| Server running? | "The server should be up" | `curl -s localhost/health` |

## References

| File | Load When |
|------|-----------|
| references/code-verification.md | Writing verification scripts |
| references/prompt-versioning.md | Versioning/hashing prompts |
