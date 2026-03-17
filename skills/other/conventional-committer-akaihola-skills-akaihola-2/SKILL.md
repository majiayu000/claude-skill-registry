---
name: conventional-committer
description: Skill for committing changes to this repository using Git, generating a commit message from recent history and current changes.
---

# Conventional Committer

## Overview

This skill creates Git commits for this repository.

It:

- Inspects recent commit history and current changes.
- Generates a commit message consistent with the existing history.
- Stages the appropriate changes when needed.
- Runs `git commit` with the generated message.

The default behavior of this skill is to **produce a commit in the repository**, not merely draft a message.

## When to Use This Skill

Use this skill **whenever you are asked to create a commit** in this repository, for example when the user says things like:

- “Commit staged changes”
- “Commit everything”
- “Commit all changes”
- “Commit my changes”
- “Save these edits as a commit”
- “Create a commit for these changes”

In particular:

- Use this skill even if the user does **not** mention “staged changes”.
- Use this skill even if the user does **not** mention “Conventional Commit” or any specific commit style.
- Default to using this skill for any request whose primary intent is “make a commit”.

Interpret user intent as follows:

- If there are **any staged changes** and the user has **not** explicitly asked to include additional unstaged changes, commit **only what is already staged** and do **not** stage anything else.
- If the user explicitly says they want to include unstaged changes (for example, “commit everything”, “commit all changes”, “commit my changes”, “stage and commit all changes”), treat that as a request to:
  - Stage all relevant changes, then
  - Commit them.
- If there are **no staged changes** and the user asks to commit changes in general (for example, “commit changes”, “save these edits as a commit”), stage the intended changes first and then commit them.

If there are no changes to commit after doing this, report that no commit was created.

## Git Context Helper Script

This skill relies on a helper script stored in:

- `scripts/git_context_chunks.py` (relative to skill directory)

The helper script:

| Purpose                     | Command / Invocation                                   | Output / Notes                                                          |
| --------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| Run from skill directory    | `python3 scripts/git_context_chunks.py`                | Uses `git --no-pager` and `GIT_PAGER=cat` to avoid interactive pagers.  |
| Recent commits section      | `git log -n5 --format="commit %h%n%B%n--------------"` | Produces `== Recent commits (last 5) ==` followed by 5 recent commits.  |
| Staged changes section      | `git --no-pager diff --cached`                         | Produces `== Staged changes ... ==` followed by the full staged diff.   |
| Chunking and splitting      | (internal)                                             | ≤ 16384 chars per chunk; splits at `diff --git` boundaries or newlines. |
| Chunk metadata & navigation | (internal)                                             | Wraps chunks with markers; prints next command to stderr when needed.   |

Treat these markers and “next chunk” lines as metadata; they must not appear in the final commit message.

## Running the Helper Script

Run all commands from the **conventional-committer skill directory** (conventional-committer/ in this repository).

### First Chunk

Obtain the first chunk of Git context:

- `python3 scripts/git_context_chunks.py`

The script:

- Outputs chunk `1/N` to standard output.
- If `N > 1`, prints a “Next chunk command” to standard error.

### Subsequent Chunks

When more chunks are required:

1. Read the “Next chunk command” emitted to standard error, e.g.:
   - `python3 scripts/git_context_chunks.py --chunk-index 1`

2. Execute that command to retrieve the **next** chunk.
3. Repeat until the current chunk index equals `N - 1` (the last chunk).

Together, the ordered chunks reconstruct the 5 most recent commits and the full staged diff without truncation.

## Using the Skill to Commit Changes

This section specifies the expected agent behavior when applying the skill.

### High-Level Workflow

1. Interpret the user’s intent about what should be committed.
2. Stage the appropriate changes (if needed).
3. Verify that there is something to commit.
4. Collect Git context using the helper script.
5. Load the resulting chunk(s) into working context in order.
6. From this context, synthesize a commit message that:
   - Summarizes the committed changes.
   - Follows the project’s existing commit style as inferred from recent commits.
7. Run `git commit` with the synthesized message to actually create the commit.
8. Report the outcome (e.g., commit hash and subject line) back to the caller.

### Detailed Procedure

1. **Determine what should be committed.**

   Interpret user intent and the current index state:
   - First check whether there are staged changes.
   - If there are staged changes and the user has not explicitly asked to include additional unstaged changes, **do not modify the index**; commit exactly what is already staged.
   - If the user explicitly says they want to include unstaged changes (for example, “commit everything”, “commit all changes”, “commit my changes”, “stage and commit all changes”), stage all intended changes before proceeding (for example, using `git add -A` or an equivalent command appropriate for this repository and workflow).
   - If there are no staged changes and the user asks to commit changes in general (for example, “commit changes”, “save these edits as a commit”), stage the intended changes before proceeding.

2. **Verify there is something to commit.**
   - If, after staging as above, there are no staged changes (for example, `git diff --cached` is empty), report that there are no changes to commit and stop.
   - Otherwise, proceed.

3. **Run the helper script for chunk 0:**

- `python3 scripts/git_context_chunks.py`

4. **Capture the output for use as context:**
   - Treat everything between:
     - `[conventional-committer] chunk 1/N`
     - `[conventional-committer] end of chunk 1/N`
   - As the primary data payload for that chunk.
   - Treat the header and footer lines as metadata to track chunk ordering; they should **not** be included in the commit message itself.

5. **If more chunks exist:**
   - Execute the “Next chunk command” provided by the script to obtain chunk 2, then 3, and so on, until all chunks are collected.
   - Maintain strict chunk order (1, 2, 3, …, N) when building internal understanding of the diff and history.

6. **From the collected chunks:**
   - Read the recent commits and the staged diff.
   - Infer the repository’s commit style from the recent commits. When the history uses a structured style (such as a `type: subject` or `type(scope): subject` pattern), mirror that style in the new commit.
   - Propose a **single** commit message with:
     - A concise subject line in the imperative mood.
     - An optional body explaining **what** changed and **why**, grouped logically.
     - Optional footers (e.g., for breaking changes or references to issues) when appropriate.

7. **Validate and apply the commit:**
   - Validate that the generated message:
     - Matches the tone and structure of recent commits.
     - Accurately reflects the staged diff.
     - Uses line wrapping and blank-line separation consistent with existing history.
   - Then **run `git commit` with this message** from the repository root. For example:
     - When only a subject is needed:  
       `git commit --no-edit -m "<subject line>"` is acceptable if no separate body is needed.  
       Otherwise:  
       `git commit -m "<subject line>"`
     - When a body is present:  
       `git commit -m "<subject line>" -m "<body ...>"`
   - After a successful commit, you may obtain and report the new commit’s hash and subject line (for example, using `git --no-pager log -1 --oneline`).

The expected outcome of this procedure is a **new commit** in the repository that accurately represents the requested changes.

## Recommended Orchestration Pattern

For any system that can execute commands in this repository:

1. Whenever a user asks to **commit changes** (e.g., “commit staged changes”, “commit everything”, “save these edits as a commit”), route the request through this skill.
2. Allow the skill to:
   - Prefer committing already-staged changes when any exist, only staging additional changes when the user has explicitly asked to include them (for example, “commit everything” or “stage and commit all changes”).
   - Run the helper script to collect Git context chunks in order: `chunk 1/N`, `chunk 2/N`, …, `chunk N/N`.
   - Synthesize an appropriate commit message based on history and the staged diff.
   - Run `git commit` with that message.
3. After the commit, surface back to the user:
   - The exact commit message that was used (subject line and optional body).
   - A short confirmation of the created commit (for example, the commit hash and subject line).

Orchestrators should treat this skill as the **standard path for creating commits** in this repository.

## Notes and Limitations

- The helper script assumes a standard Git repository and must be run from inside that repository.
- The 16384-character limit is enforced per chunk, not globally; a very large diff may result in many chunks.
- When a **single file’s diff** is larger than 16384 characters, the script splits that file’s diff across multiple chunks at newline boundaries where possible.
- The script always disables Git’s pager, ensuring it does not block on interactive output.
- This skill assumes the runtime has permission to modify the repository (stage changes and create commits).
