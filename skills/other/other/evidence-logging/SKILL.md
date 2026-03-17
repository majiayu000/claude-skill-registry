---
name: evidence-logging
description: 'Use this skill as foundation for all evidence-based review workflows.
  Use when conducting any review that needs evidence trails, creating audit documentation,
  ensuring reproducibility of analyses. Do not use when quick informal checks without
  documentation needs. DO NOT use when: structured output is the focus - use structured-output.'
category: output-patterns
tags:
- evidence
- citations
- reproducible
- audit-trail
- documentation
dependencies: []
tools: []
usage_patterns:
- evidence-capture
- audit-trail
- reproducible-analysis
complexity: intermediate
estimated_tokens: 1200
---
## Table of Contents

- [When to Use](#when-to-use)
- [Activation Patterns](#activation-patterns)
- [Required TodoWrite Items](#required-todowrite-items)
- [Step 1: Initialize Log (`evidence-logging:log-initialized`)](#step-1:-initialize-log-(evidence-logging:log-initialized))
- [Step 2: Capture Commands (`evidence-logging:commands-captured`)](#step-2:-capture-commands-(evidence-logging:commands-captured))
- [Step 3: Record Citations (`evidence-logging:citations-recorded`)](#step-3:-record-citations-(evidence-logging:citations-recorded))
- [Step 4: Index Artifacts (`evidence-logging:artifacts-indexed`)](#step-4:-index-artifacts-(evidence-logging:artifacts-indexed))
- [Evidence Reference Format](#evidence-reference-format)
- [Exit Criteria](#exit-criteria)


# Evidence Logging

## When To Use
- During any review or analysis workflow to capture reproducible evidence.
- When findings must be traceable to specific commands, outputs, or sources.
- Before finalizing recommendations that stakeholders will act upon.

## When NOT To Use

- Quick informal checks without documentation needs
- Structured output is the focus - use structured-output

## Activation Patterns
**Trigger Keywords**: evidence, proof, trace, audit, reproducible, citation, source, verify
**Contextual Cues**:
- "show your work" or "provide evidence"
- "how can I verify this" or "reproduce these findings"
- "cite your sources" or "where did this come from"
- "create an audit trail"
- "document the steps taken"

**Auto-Load When**: Any analysis requires traceability or when findings need reproducible verification.

## Required TodoWrite Items
1. `evidence-logging:log-initialized`
2. `evidence-logging:commands-captured`
3. `evidence-logging:citations-recorded`
4. `evidence-logging:artifacts-indexed`

Mark each item complete as you finish the corresponding step.

## Step 1: Initialize Log (`evidence-logging:log-initialized`)
- Create evidence structure with timestamp and context:
  - Session ID or review identifier.
  - Repository, branch, and commit hash.
  - Analyst identity and review scope.
- Establish naming convention for evidence references (e.g., `[E1]`, `[E2]`).

## Step 2: Capture Commands (`evidence-logging:commands-captured`)
- Log every command that produces evidence:
  ```
  [E1] Command: git diff --stat HEAD~5..HEAD
       Output: 15 files changed, 234 insertions(+), 89 deletions(-)
       Timestamp: 2024-01-15T10:30:00Z
  ```
  **Verification:** Run `git status` to confirm working tree state.
- Include full command with arguments (no aliases).
- Capture relevant output snippets, not entire dumps.
- Note working directory and environment if relevant.

## Step 3: Record Citations (`evidence-logging:citations-recorded`)
- Log external sources consulted:
  ```
  **Verification:** Run the command with `--help` flag to verify availability.
  [C1] Source: https://doc.rust-lang.org/nomicon/
       Section: "Working with Unsafe"
       Relevance: Validates unsafe block justification
  ```
  **Verification:** Run the command with `--help` flag to verify availability.
- Include web searches performed and key results.
- Reference documentation versions (API docs, RFCs, specs).
- Note any AI-assisted analysis with model/prompt context.

## Step 4: Index Artifacts (`evidence-logging:artifacts-indexed`)
- Catalog generated artifacts:
  - Screenshots, diagrams, or visualizations.
  - Exported reports or coverage summaries.
  - Saved query results or API responses.
- Provide file paths or inline content for small artifacts.
- Note artifact retention policy (ephemeral vs. archived).

## Evidence Reference Format
Use consistent format in findings:
```
**Verification:** Run the command with `--help` flag to verify availability.
Finding: Memory leak in connection pool [E3, C2]
- Evidence [E3]: valgrind output showing 4KB unreleased
- Citation [C2]: PostgreSQL docs on connection lifecycle
```
**Verification:** Run the command with `--help` flag to verify availability.

## Exit Criteria
- Todos completed with structured evidence log.
- All findings traceable to specific evidence references.
- Downstream reports can cite evidence without re-running commands.
## Supporting Modules

- [Evidence format conventions](modules/evidence-formats.md) - standardized `[E1]`, `[C1]`, `[A1]` reference formats

## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
