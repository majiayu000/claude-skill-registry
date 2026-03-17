---
name: schematic
description: |
  Reverse engineer a detailed product and technical specification document from a git branch's
  implementation. Use when: (1) a branch has shipped or is in-progress and needs documentation,
  (2) you need to understand what a branch does at product and architecture level, (3) onboarding
  to someone else's feature branch, (4) creating PR descriptions or design docs after the fact,
  (5) user asks to "analyze this branch", "write a spec from the code", or "document what this
  branch does". Produces a structured markdown spec covering problem statement, product requirements,
  architecture, technical design, file inventories, testing strategy, rollout plan, and risks.
author: Codex
version: 1.0.0
date: 2026-02-15
tags: [documentation, git, branch-analysis, spec, reverse-engineering]
---

# Reverse Engineer Spec from Branch Implementation

## Problem

Feature branches often ship without comprehensive documentation. After the fact, teams need
product specs, architectural docs, or onboarding materials that explain what was built and why.
Manually reading every file change is slow and error-prone. This skill systematically extracts
a complete spec from a branch's diff.

## Context / Trigger Conditions

- User asks to "analyze this branch" or "reverse engineer a spec"
- User asks to "document what this branch does"
- User wants a product spec, technical spec, or design doc from existing code
- A branch has many commits and files changed and needs a coherent explanation
- Onboarding to an unfamiliar feature branch

## Solution

### Phase 1: Scope the Branch

Get the full picture of what changed before reading any files.

```bash
# 1. Identify the base branch (usually main or latest)
git log --oneline <base>..HEAD | head -50

# 2. Get file-level diff stats
git diff --stat <base>...HEAD

# 3. Count the scale
git diff --stat <base>...HEAD | tail -1
```

From the diff stats, categorize files into groups:
- **Core implementation** (new modules, business logic)
- **Integration points** (modified selectors, reducers, hooks, components)
- **Tests** (unit tests, integration tests, e2e tests)
- **Configuration** (feature flags, env vars, types, configs)
- **Incidental** (formatting, imports, minor refactors)

### Phase 2: Parallel Deep Exploration

Launch 2-4 parallel exploration agents, each focused on a different file group. This is
critical for efficiency — reading 50+ files sequentially is too slow.

**Agent 1: Core Implementation**
- All new files (the heart of the feature)
- Focus on: purpose, key types, exported functions, data flow, inter-module connections

**Agent 2: Integration Points**
- Modified selectors, reducers, hooks, components
- Focus on: what changed, why (inferred), how it connects to core implementation

**Agent 3: Tests**
- All test files (unit, integration, e2e)
- Focus on: what behaviors are validated, key assertions, what product requirements they encode

**Agent 4 (if needed): Configuration & Infrastructure**
- Feature flags, env vars, build configs, type declarations
- Focus on: rollout strategy, gating mechanisms, deployment concerns

Each agent prompt should ask for:
- Purpose of each file
- Key exports and types
- Data flow and dependencies
- How each file connects to others in the group

### Phase 3: Cross-Check for Gaps

After agents return, diff the analyzed files against the full file list:

```bash
# List all non-test changed files
git diff --stat <base>...HEAD -- '*.ts' '*.tsx' | awk '{print $1}' | sort

# Show small diffs for any files not yet analyzed
git diff <base>...HEAD -- <uncovered-files>
```

Read the remaining small diffs directly. These often contain important details:
- Type declarations (new fields on models)
- Feature flag definitions
- Bug fixes discovered during development
- Proxy/compatibility changes in existing code

### Phase 4: Write the Spec Document

Structure the spec with these sections (skip sections that don't apply):

```markdown
# [Feature Name]
## Reverse-Engineered Product & Technical Specification

## 1. Problem Statement
Why this feature exists. What user/business pain it addresses.
Infer from the nature of the changes and any comments in the code.

## 2. Solution Overview
High-level description of the approach. Key design properties
(transparent, lazy, bounded, etc.).

## 3. Product Requirements
### 3.1 User-Facing Behavior
Table of requirements inferred from tests and UI changes.

### 3.2 Supported Workflows
List of workflows validated by tests.

### 3.3 Scope Boundaries
What is and isn't included.

## 4. Architecture
### 4.1 System Diagram
ASCII diagram showing component relationships and data flow.

### 4.2 Data Lifecycle
Step-by-step flow from initial state through steady state.

## 5. Technical Design
Subsections for each major design decision:
- Feature flags and gating
- Data models / schema changes
- Key algorithms or patterns
- Integration patterns (how existing code was modified)
- Cache/performance design
- Error handling and fallbacks

## 6. New Files
Table: file path, purpose (one line each).

## 7. Modified Files (Key Changes)
Table: file path, what changed (one line each).
Include ALL files — even minor ones. The cross-check in Phase 3
catches files that agents missed.

## 8. Testing Strategy
### Unit Tests
### Integration / E2E Tests
### Instrumentation / Observability

## 9. Rollout Strategy
How the feature is gated, incremental rollout steps, kill switches.

## 10. Risks and Mitigations
Table: risk, mitigation.

## 11. Summary
Key metrics: files added/modified, lines changed, scope of impact.
```

### Phase 5: Verify Completeness

Cross-check the spec against the branch:

1. Every file in `git diff --stat` should appear in Section 6 or 7
2. Every test file should be referenced in Section 8
3. Feature flags mentioned in code should appear in Section 5/9
4. The architecture diagram should match the actual data flow discovered by agents

## Verification

- Every changed file on the branch is accounted for in the spec
- The architecture diagram accurately represents the data flow
- Product requirements match what the tests actually validate
- No significant design decisions are missing from the technical design section

## Example

See the canonical offload spec produced for the `test-parity-mem-exp-99-with-pr16393` branch:
a 12-section document covering 74 changed files across 12 commits, with architecture diagrams,
IndexedDB schema documentation, proxy design details, cache eviction policies, testing strategy
against a real customer dataset, and a complete file inventory.

## Notes

- **Parallel agents are essential**: A branch with 50+ files takes too long to analyze
  sequentially. 3-4 parallel agents cut analysis time by 3-4x.
- **Cross-check is critical**: Agents inevitably miss some files. The Phase 3 cross-check
  catches small but important changes (type declarations, bug fixes, compatibility shims).
- **Infer the "why"**: Code shows "what" but not always "why". Use test assertions, comments,
  commit messages, and the shape of changes to infer product motivation.
- **Save to `docs/`**: Write the spec to a `docs/` directory in the repo so it's discoverable.
- **Don't over-document incidentals**: Formatting changes, import reordering, and trailing
  commas can be mentioned in a single line rather than getting their own subsection.
- **Use tables liberally**: File inventories, feature flags, risks — tables are scannable
  and compact.
