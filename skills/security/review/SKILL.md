---
name: review
description: 'Use when asked to review a pull request, examine code changes, find bugs, or audit a branch, in standard or depth mode. Not for an iterative review-and-fix loop: use audit-project.'
---

# Severity-graded review

Two modes share one authority (read-only) and one evidence bar: every finding cites concrete code evidence, no invented issues, no style-only findings. Standard mode is a single-pass severity-graded review of a supplied diff, snippet, or branch. Depth mode fans out two parallel reviewers, bug/security and code quality, and synthesizes a deduplicated unified verdict.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to review a pull request, examine code changes, find bugs, run a security review, audit code on the current branch, or run combined bug/security and code-quality branch audits. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output: a review report with findings (standard) or a unified audit report (depth). |
| Done | Standard: validated findings with severity, evidence, and concrete fixes; no style-only or invented findings. Depth: a single deduplicated prioritized synthesis as a unified verdict ordered by severity. |

## Inputs

Required: a PR URL, diff content, code snippet, or branch to review (standard); the diff range, PR number, or commit range to audit (depth).

Optional: a stated focus area (e.g., security, performance, correctness); specific files, directories, or a focus area to narrow scope.

The skill operates entirely within the current session context. No file system, repository, credential, or remote access is required or authorized.

## Mode selection

| User says | Mode | Output |
|---|---|---|
| review this PR, examine these changes, find bugs, security review, audit this branch | standard | Severity-graded findings report |
| deep review, combined bug/security and quality audit, full branch audit | depth | Unified deduplicated verdict from parallel reviewers |

When the user names a single PR or diff, use standard mode. When the user asks for a combined bug/security and quality audit or a full branch audit, use depth mode.

## Shared evidence bar

Every finding, in either mode, must cite specific code locations, line ranges, or diff hunk markers as evidence. Do not assert a finding without quoting the supporting code. Discard any candidate without evidence. Never report an invented issue. Exclude style-only findings (formatting, naming conventions, cosmetic preferences) unless they cause a correctness or security issue.

## Standard mode

1. **Acquire diff.** Receive the PR URL, diff text, or code snippet from the user; or determine the change set from the current branch diff against its base when the user does not name one. If no code change is supplied, ask for it. Done when: the change set is determined and scoped.
2. **Fetch changes.** Use the available tools to retrieve diff or file content for the target revision range. If the user named files, directories, or a focus area, restrict scope to those. Do not assume write access. Done when: the diff or file content is retrieved and scope is restricted.
3. **Bound scope.** Limit analysis to the supplied diff or code range. Do not widen scope to surrounding code or unrelated files. Done when: scope is bounded.
4. **Read changed regions with context.** Read each changed region and the immediate callers and surrounding state needed to reason about its behavior. Do not read unrelated code. Done when: every changed region is read with its callers and surrounding state.
5. **Categorize findings.** Assign each finding to one of: Correctness, Security, Performance, Maintainability, Robustness, Logic, or API Usage. Done when: every finding is categorized.
6. **Grade severity.** Assign one severity level to each finding:
   - Critical: exploitable bug, data loss, or security vulnerability with no workaround
   - High: significant bug, regression risk, or breach of contract without mitigation
   - Medium: correctness concern, degraded performance, or maintainability debt
   - Low: minor issue, cosmetic concern, or opportunity for improvement
   Done when: every finding is graded.
7. **Validate findings.** Apply the shared evidence bar: each finding cites specific code locations as evidence; evidence-less candidates are discarded; no invented issues. Done when: every surviving finding has concrete evidence.
8. **Reject style-only findings.** Do not report formatting, naming conventions, or cosmetic preferences unless they cause a correctness or security issue. Done when: no style-only finding remains.
9. **Prescribe concrete fixes.** For each finding, write a specific, actionable recommendation that addresses the root cause, not a surface-level patch. Done when: every finding has a concrete fix.
10. **Assemble report.** Structure findings as: Severity → Category → Finding → Evidence → Recommended Fix. Sort by severity descending. Done when: the report is assembled and sorted.

## Depth mode

1. **Confirm scope.** Confirm the diff range, PR number, or commit range to audit. Stop if scope cannot be determined. Done when: the audit scope is confirmed or the run stops with scope-unresolvable.
2. **Fan out two simultaneous reviewers.**
   - Reviewer A, bug and security audit: reads the scope, identifies defect, security, and regression findings, produces a severity-ordered list.
   - Reviewer B, code quality audit: reads the scope, identifies maintainability, style, and structural quality findings, produces a severity-ordered list.
   Both reviewers operate under the same read-only authority and the shared evidence bar. Neither reviewer makes changes. Done when: both reviewers are spawned with their audit assignments and read-only authority.
3. **Wait for both reviewers.** Done when: both reviewers have returned their findings lists.
4. **Handle partial failure.** If either reviewer fails or returns empty after retry, report the partial result from the surviving reviewer with the failure identified. Done when: both reviewers returned, or the surviving reviewer's partial result is reported with the failure identified.
5. **Synthesize.**
   - Merge findings from both reviewers.
   - Deduplicate and consolidate overlapping findings.
   - Rank merged findings by severity (critical > high > medium > low > informational). Map reviewer-reported severities onto this scale: P0 = critical, P1 = high, P2 = medium, P3 = low; informational is for advisory notes with no behavioral impact.
   - Group findings by file or component.
   - Omit findings already resolved or not applicable.
   - Record which reviewer produced each finding for attribution.
   Done when: findings are merged, deduplicated, severity-ranked, grouped, resolved findings omitted, and reviewer attribution recorded.
6. **Return a unified audit report.** Findings in severity order, each labeled with severity, category, affected file(s) and line(s), description, rationale, and reviewer source. Done when: the unified report is returned with all findings labeled and severity-ordered.

## Failure and recovery

| Failure class | Condition | Result |
|---|---|---|
| `empty-diff` | No diff or code supplied | Ask the user for the PR or code to review; do not produce a report |
| `review-blocked` | Cannot access the target PR or revision | Report the access failure explicitly; do not fabricate content |
| `partial-result` | Some files or hunks are inaccessible | List accessible findings; state which parts were skipped and why |
| `scope-widening` | Analysis extends beyond supplied diff | Discard widened findings; report only bounded results |
| `style-only-report` | All findings are style-only | State that no actionable findings were found; describe what was evaluated |
| `scope-unresolvable` (depth) | Diff, PR, or commit range cannot be determined | Stop. Report that the scope could not be determined |
| `reviewer-failure` (depth) | A reviewer fails after retry | Return the surviving reviewer's findings with the failure stated. Do not synthesize from a missing reviewer |
| `synthesis-empty` (depth) | No synthesis was possible | Return the exact partial result each reviewer produced; state that no synthesis was possible |

Partial-result rule: always return what was produced. Never claim the done predicate holds when it does not. Non-mutation: never edits files, commits, or remote state. Any failure leaves the working tree unchanged.

## Output

**Standard mode.** A structured review report returned as chat output. One section per severity level (Critical, High, Medium, Low), each containing:
- **Severity** and **Category**
- Finding: the specific issue with code location and evidence
- Recommended Fix: concrete, actionable correction

Unsuitable scope is reported as a named failure. An empty diff or inaccessible PR is reported as a named failure. The report must not contain findings without cited evidence.

**Depth mode.** A unified audit report with deduplicated findings prioritized by severity, grouped by file or component, each labeled with severity, category, affected location, description, rationale, and reviewer source. Or a partial-result report if synthesis was not possible.

