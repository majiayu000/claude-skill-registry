---
name: vigilante-create-issue
description: Help a human author write an implementation-ready GitHub issue that Vigilante can execute reliably.
---

# Vigilante Create Issue

## Overview
Use this skill when a human wants to write or refine a GitHub issue that Vigilante will later implement. The default goal is to turn a vague request into an issue with enough behavioral detail, constraints, and verification criteria for a headless coding agent to execute safely, then create that issue on GitHub. If creation is not possible, fall back to returning a ready-to-file issue body. The goal is not to design the full solution for them.

## Outcome
Produce a GitHub issue that is:

- classified as a `feature`, `bug`, or `task` before the draft is finalized
- specific about the problem and why it matters
- grounded in repository or product context
- explicit about expected behavior and non-goals
- realistic about implementation flexibility and hard constraints
- testable through concrete acceptance criteria
- clear about validation and regression coverage
- created on GitHub by default when the target repository can be resolved and `gh` issue creation is available
- returned as a polished Markdown draft only when the user explicitly asks for draft-only output or issue creation is blocked

## Workflow
1. Clarify the request before writing
- Identify the change the user actually wants.
- Ask for missing repository, product, or user context when it affects implementation.
- Separate required behavior from guesses or preferences.

2. Classify the request before finalizing the issue body
- Decide whether the request is best treated as a `feature`, `bug`, or `task`.
- Base the classification on the user's stated problem and desired outcome rather than implementation details.
- If the request is ambiguous, infer the most likely type and state briefly that the type was inferred.
- Use the selected type to decide which details are required in the issue body, not just to append a label.

3. Resolve the target repository before finalizing output
- Prefer local git context first when the user is working inside a repository.
- Otherwise use an explicitly provided repository slug or URL.
- If the repository cannot be resolved confidently, say so briefly and fall back to returning the ready-to-file issue body instead of guessing.

4. Frame the issue around execution
- Write for the agent that will implement the issue later, not for a broad brainstorming audience.
- Prefer observable behavior over vague aspirations.
- Note any constraints that must be preserved: CLI flags, APIs, config compatibility, UX expectations, rollout limits, or performance boundaries.

5. Capture implementation guidance without over-constraining
- Include likely solution paths when they materially reduce ambiguity.
- Mark which implementation details are required and which are flexible.
- Call out known tradeoffs or rejected alternatives when relevant.

6. Make completion testable
- Convert expectations into pass/fail acceptance criteria.
- State what tests should be added or updated.
- Mention the key regressions or failure modes that must be prevented.

7. Create the GitHub issue by default
- When the repository is known and the user did not explicitly ask for draft-only output, use `vigilante gh issue create` to open the issue.
- Prefer `vigilante gh api repos/{owner}/{repo}/issues` over `vigilante gh issue create` when opening the final issue so Vigilante can set GitHub's native issue type with the request body `type` field.
- Map Vigilante's internal classifications explicitly to GitHub's native issue types: `feature` -> `Feature`, `bug` -> `Bug`, `task` -> `Task`.
- Treat the native GitHub issue type as the source of truth whenever the repository supports it.
- When the draft explicitly says the new issue is a follow-up, child, or sub-issue of a specific existing issue, carry that parent issue number through issue creation.
- After the base issue is created, attach it as a native GitHub sub-issue of that parent with `vigilante gh api --method POST repos/{owner}/{repo}/issues/{parent_issue_number}/sub_issues -f sub_issue_id={created_issue_id}`.
- Only create a native relationship when the parent mapping is explicit and low-ambiguity; incidental issue-number mentions in prose are not enough.
- If native sub-issue creation fails or the repository does not support it, keep the created issue, preserve the body text reference, and make the fallback explicit in the final response.
- Use the polished Markdown body as the issue content instead of stopping at the draft.
- In the final response, include the created issue URL or issue number and keep the body available if useful.

8. Fall back cleanly when issue creation is blocked
- If issue creation cannot be completed because repository context is missing, `gh` auth is unavailable, network access is blocked, or sandbox restrictions prevent GitHub access, say so briefly and return the ready-to-file Markdown issue instead.
- If the repository rejects the native `type` field because issue types are unavailable or unsupported, retry issue creation without the native type and make the fallback explicit in the final response.
- If the native sub-issue relationship request is rejected or unsupported, do not fail the overall issue creation flow; keep the new issue and report that the relationship fell back to body-only text.
- If the environment supports requesting escalation for GitHub/network access, do that before giving up.
- If the user explicitly asks for a draft only, honor that request and do not create the issue.
- Keep failure messaging short, specific, and factual.

## Issue Type Guidance
- Always classify the request as `feature`, `bug`, or `task` before finalizing the issue.
- When creating the issue on GitHub, write that classification into GitHub's native issue type field whenever the repository supports it.
- Do not use labels or issue-body text as the primary type representation when the native issue type is set successfully.
- Do not infer parent/child issue links from vague wording or unrelated issue references.
- Only include an `Issue Type: ...` line in the issue body when returning a draft without creating the issue, or when native issue types are unavailable and the fallback needs to preserve the classification explicitly.
- When the type was inferred from an ambiguous request, note that clearly, for example `Issue Type: task (inferred)`, but only in the draft/fallback body when that line is needed.
- For `bug` issues, prioritize current behavior, expected behavior, impact, reproduction clues, and regression risk.
- For `feature` issues, prioritize the desired user-facing outcome, scope boundaries, and non-goals.
- For `task` issues, prioritize the concrete deliverable, operational context, constraints, and completion conditions.

## Required Sections
Every issue draft should cover these sections when relevant:

1. Problem statement
- What is wrong, missing, or desired?
- Why does this matter now?

2. Context
- What repository, product, or workflow context does the implementer need?
- What is the current behavior?
- Who is affected?
- What assumptions or constraints are already known?

3. Desired outcome
- What should be true after implementation?
- What is explicitly out of scope?

4. Possible implementation approaches
- What are the most plausible solution paths?
- Which details are required versus flexible?
- What tradeoffs should the implementer understand?

5. Acceptance criteria
- Use explicit, testable statements.
- Prefer behavior-focused checks over generic wording like "works correctly."

6. Testing expectations
- State which test layers matter: unit, integration, CLI, workflow, end-to-end, or manual verification.
- Mention critical regressions and failure modes that need coverage.

7. Operational or UX considerations
- Include logging, migrations, config compatibility, docs, observability, rollout, or backward compatibility concerns when applicable.

## Issue Quality Rules
- Do not leave "should support X" statements undefined when the expected behavior can be stated concretely.
- Do not hide key constraints inside prose if they materially affect implementation.
- Do not invent repository details that were not provided. Flag missing context instead.
- Do not overload the issue with speculative architecture unless the decision matters to execution.
- Do include non-goals so the eventual implementation stays narrow.
- Do include exact commands, files, components, or workflows when they are already known.

## Recommended Questions To Ask
Use these to tighten the issue before drafting:

- What exactly should change?
- What currently happens instead?
- Why is the change needed?
- What constraints must the implementation respect?
- Which solution options are acceptable, and which are not?
- How will we know the issue is done?
- What tests prove the change works?
- What regressions must be prevented?

## Output Template
Use this structure for the issue body:

```md
## Summary
<One short paragraph describing the problem and desired change.>

Issue Type: <feature | bug | task>[ (inferred)]  <!-- include only for draft-only or documented fallback output -->

## Problem
- <What is wrong, missing, or desired>
- <Why it matters>

## Context
- <Current behavior>
- <Relevant repo, product, or workflow details>
- <Constraints or assumptions>

## Desired Outcome
- <Expected end-state>
- <Non-goals or out-of-scope items>

## Implementation Notes
- <Likely approach or options>
- <Required constraints vs flexible details>
- <Tradeoffs, if relevant>

## Acceptance Criteria
- [ ] <Specific observable behavior>
- [ ] <Specific observable behavior>

## Testing Expectations
- <Tests to add or update>
- <Failure modes or regressions to cover>

## Operational / UX Considerations
- <Docs, logging, migration, compatibility, rollout, observability, etc.>
```

Type-specific reminders:

- `bug`: include current behavior, expected behavior, impact, and reproduction clues when available.
- `feature`: include the desired outcome, boundaries, and explicit non-goals.
- `task`: include the deliverable, operational context, constraints, and concrete done criteria.

## Final Checks
Before creating the issue or returning the fallback draft, verify that:

- the problem is understandable without extra oral context
- the selected issue type is `feature`, `bug`, or `task`
- the native GitHub issue type is used when the issue is created in a repository that supports it
- explicit follow-up or child relationships are attached as native GitHub sub-issues when the parent issue is clearly identified
- ambiguous issue references do not create native parent/child links
- any `Issue Type:` line in the body is reserved for draft-only or explicit fallback output
- the desired outcome is observable
- the acceptance criteria are testable
- the testing section names the expected validation
- the body includes the type-specific details that matter for the selected class instead of only a label
- the issue gives Vigilante enough direction to implement without guessing the basics
- the target repository is known before attempting issue creation
- the final response includes the created issue URL or number when creation succeeds
- the final response says whether the native sub-issue relationship was created or whether issue creation fell back to body-only linking
- the fallback response states briefly why issue creation was not completed when it fails
