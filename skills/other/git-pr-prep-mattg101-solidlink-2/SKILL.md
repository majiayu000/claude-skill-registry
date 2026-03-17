---
name: git-pr-prep
description: Prepares a Pull Request by staging changes, verifying against acceptance criteria, and creating the PR via GH CLI. Use this skill when a feature is complete and ready for review.
trigger: always_on
---

This skill ensures that every Pull Request is descriptive, verified, and adheres to the project''s technical rigor as defined in `orchestration/project_context.md` and `.agent/rules/directives/pr_acceptance_criteria.md`.

## PR Preparation Workflow

1.  **Staging & Intent**:
    -   Verify you are on the correct `dev` or feature branch.
    -   Stage only the files relevant to the task. Avoid staging unrelated debug logs or temporary files.
    -   Use the `git status -u` command to identify untracked files that should be included.
    -   Include test result artifacts in the commit when tests are run (for example, `TestResult.xml`).

2.  **Rigor Check**:
    -   Self-audit the code against `pr_acceptance_criteria.md`.
    -   Ensure no `console.log` or temporary `TODO` comments remain in the source.
    -   Verify that all C# models have appropriate `[DataMember]` attributes if they are part of the JSON bridge.

3.  **PR Artifact**:
    -   Create or update the `pull_requests/pr_[id].md` file using the provided template.
    -   Include specific instructions for the Tester to verify the changes.
    -   For UI-impacting changes, include links or references to image and WebM artifacts in the PR artifact (and commit them when stored in-repo).

4.  **GH CLI Execution**:
    -   Run `gh pr create` with a clear title and a body that references the PR artifact or contains a concise summary of the `walkthrough.md`.
    -   Target the `main` branch unless instructed otherwise.


