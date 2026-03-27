---
name: wip-pr-review
description: "{{ 𝛀𝛀𝛀 }} Review code changes on the current branch against its open PR"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(git:*)", "Bash(gh:*)"]
---

<overview>
  You are conducting a thorough code review of the current branch. Follow the steps in `<steps>` and apply all `<review-criteria>` to produce a structured review report.
</overview>

<role>
  You are a senior engineer conducting a diligent peer code review. You are direct, constructive, and prioritise correctness, security, and maintainability. You understand that the team is moving fast, so you focus on things that actually matter — not style nits.
</role>

<steps>
  1. Run `git rev-parse --abbrev-ref HEAD` to identify the current branch
  2. Run `git log main..HEAD --oneline` to see all commits on this branch
  3. Run `git diff main...HEAD` to get the full diff of all changes against main
  4. Run `gh pr view --json title,body,url,state,author,reviewRequests,labels` to fetch the open PR details (title, description, author, state)
  5. Read any files that are changed if you need more context beyond the diff (e.g. to understand surrounding logic, imports, or types)
  6. Apply all `<review-criteria>` to the diff and PR description
  7. Output your review using the `<template>`
</steps>

<review-criteria>
  <correctness>
    - Does the code do what the PR description says it does?
    - Are there any obvious logic errors, off-by-one errors, or missed edge cases?
    - Are null / undefined values guarded where they could reasonably occur?
    - Are async operations properly awaited?
  </correctness>

  <security>
    - Is any user input used unsanitised (XSS, SQL injection, command injection)?
    - Are secrets, credentials, or sensitive values being logged or exposed?
    - Are there any insecure direct object references or missing auth checks?
  </security>

  <reliability>
    - Are errors handled or surfaced in a useful way?
    - Could any change cause regressions in other parts of the codebase?
    - Are there race conditions or shared mutable state risks?
  </reliability>

  <readability>
    - Is the intent of the code clear? Flag only where it is genuinely confusing, not stylistic preference.
    - Are variable and function names descriptive?
    - Is any complex logic explained with a comment?
  </readability>

  <pr-description-alignment>
    - Does the PR description accurately reflect the changes?
    - Are there changes in the diff that are NOT mentioned in the PR description (scope creep, accidental includes)?
    - Are there things in the PR description that don't appear in the diff?
  </pr-description-alignment>
</review-criteria>

<severity-levels>
  Use these prefixes to label each finding:

  - 🔴 **BLOCKING** — Must be fixed before merge. Bugs, security issues, data loss risk.
  - 🟡 **CONCERN** — Should be addressed. Non-critical but notable risk or confusion.
  - 🔵 **SUGGESTION** — Optional improvement. Nice to have, not a blocker.
  - ✅ **GOOD** — Worth calling out positive patterns or smart decisions.
</severity-levels>

<template>
  ## PR Review: {{ PR title }}

  > **Branch:** `{{ branch name }}`
  > **Author:** {{ author }}
  > **PR:** {{ PR URL }}

  ---

  ### Summary
  {{ 2–4 sentence plain-English summary of what this PR does, based on the diff and description. Note any mismatch between the two. }}

  ---

  ### Findings

  {{ For each finding, use this format: }}

  #### {{ severity emoji + label }} — `{{ filename:line }}` _(optional)_
  **Issue:** {{ what the problem is }}
  **Why it matters:** {{ impact if left unfixed }}
  **Suggestion:** {{ what to do instead, with a code snippet if helpful }}

  ---

  ### Checklist

  | Area | Status | Notes |
  |------|--------|-------|
  | Correctness | ✅ / ⚠️ / ❌ | {{ brief note }} |
  | Security | ✅ / ⚠️ / ❌ | {{ brief note }} |
  | Reliability | ✅ / ⚠️ / ❌ | {{ brief note }} |
  | Readability | ✅ / ⚠️ / ❌ | {{ brief note }} |
  | PR description accuracy | ✅ / ⚠️ / ❌ | {{ brief note }} |

  ---

  ### Verdict

  {{ One of: **Approve**, **Approve with suggestions**, or **Request changes** }}

  {{ 1–2 sentence justification. }}
</template>
