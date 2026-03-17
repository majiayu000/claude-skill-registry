---
name: readme-updater
description: Audit, create, or rewrite repository README.md files to enterprise-grade quality using a deterministic evidence workflow across purpose, architecture, setup, operations, security, governance, and quality gates. Use when users ask to update/standardize/harden README docs, fix inaccurate onboarding instructions, prepare production-ready repository documentation, or generate executive/ownership-ready README content.
---

# Readme Updater

## Overview
Apply a deterministic, non-speculative workflow to assess README quality, close enterprise gaps, and deliver a high-signal README that supports onboarding, operations, compliance, and maintainability.

## Trigger Hints
Use this skill when prompts include terms such as:
- "update README", "rewrite README", "create README"
- "enterprise README", "production-ready docs", "onboarding docs"
- "standardize documentation", "harden docs", "fix inaccurate README"

## Workflow
1. Resolve target README scope and repository root.
2. Collect repository evidence from source-of-truth files.
3. Audit the current README against enterprise criteria.
4. Define the target README structure and applicability.
5. Rewrite README content using only verified evidence.
6. Run verification gates and finalize with a gap report.

## 0) Resolve Target Scope (required)
- Default target is `README.md` at repository root.
- If multiple README files exist, prioritize root README unless user explicitly requests another path.
- If the user-requested README path does not exist, create it only when the request implies creation; otherwise ask one precise clarification question before writing.
- If README is missing, create one using this skill's target structure.
- If the requested scope conflicts with repository evidence, keep user-requested scope and note constraints in the gap report.

## 1) Identify Repository Context
- Determine project type, runtime, package manager, delivery model, and ownership signals from repository files.
- Extract canonical facts from `package.json`, lockfiles, build configs, infra manifests, workflow files, and deployment configs.
- Build a short evidence map before writing using this format:
  - Fact
  - Source file path
  - Section where the fact will appear
- Do not infer unsupported operational, security, or compliance claims.

## 2) Audit Enterprise Criteria
Score each area as `complete`, `partial`, or `missing`:
- Purpose and business context
- Architecture and boundaries
- Prerequisites and local setup
- Environment/configuration strategy
- Build, test, lint, and quality commands
- Runbook basics (run, debug, troubleshoot)
- Deployment and release process
- Observability/support ownership
- Security, secrets, and compliance notes
- Contribution and governance model
- Versioning/changelog references

Also record:
- Top 3 gaps that block onboarding or safe operation.
- Any claims in the current README that cannot be verified from repository evidence.

## 3) Define Target README Structure
Use this baseline structure, then tailor to repo realities:
1. Title and one-sentence value proposition
2. Overview and scope
3. Architecture at a glance
4. Prerequisites
5. Quick start
6. Configuration and environment variables
7. Development workflow (test/lint/build)
8. Operations and troubleshooting
9. Deployment and release
10. Security and compliance
11. Contributing and code standards
12. Ownership/support and escalation
13. License and legal notices

If sections are inapplicable, keep the heading and explicitly mark `Not applicable` with brief rationale.

## 4) Rewrite Rules
- Prefer precise, executable commands over prose.
- Keep language neutral, concise, and professional.
- Convert ambiguous wording into verifiable statements.
- Use tables for env vars, ports, and command catalogs.
- For TODO or unknown values, mark `TBD (owner needed)` rather than guessing.
- Preserve repository-specific terminology and established naming.
- Keep heading hierarchy valid and consistent for Markdown renderers.
- Prefer relative repository paths for file references and local workflows.

## 5) Verification Gates
Before finalizing:
- Validate all commands against repository tooling.
- Confirm referenced files/paths exist.
- Ensure section order and headings are consistent.
- Check that setup instructions are minimal and reproducible.
- Remove stale/duplicated instructions.
- Confirm links are valid repository-relative links or resolvable absolute URLs.
- Verify no unverifiable claims remain without `TBD (owner needed)` marker.

Minimum verification output:
- Command validation result (`pass`/`fail`) with corrected replacements if failures were found.
- Path/link validation result (`pass`/`fail`) with removed or corrected targets.
- Claim verification result identifying corrected unverifiable statements.

## 6) Output Contract
When applying this skill, return:
- Updated `README.md`.
- A compact gap report listing unresolved `TBD` items.
- A short verification summary listing what was validated (commands, paths, links).
- Optional follow-up tasks only when they unblock README completeness.

## Reference
Load `references/enterprise-readme-checklist.md` when you need detailed review prompts and section-level acceptance criteria.
