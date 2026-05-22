---
name: commit-msg
description: Commit the staged changes to git with meaningful messages.
---

# Commit Message

This skill instructs AI agent on how to commit staged changes to a git repository with
meaningful commit messages.

## Inputs

The commit skill takes the following inputs:
- The purpose of the commit, either a delivery or a milestone
  - Milestone is the only commit that can bypass pre-commit hooks
  - Milestone can only happen on a development branch
- The staged files to be committed
  - The commit message should clearly describe the changes made.
    If the changes are less than 20 lines, a short commit message is sufficient.
    Otherwise, a full commit message is required.
- If available, the related milestone or issue number
  - As per our naming convention, the development branch should be named
    `issue-<number>-<brief-title>`, so you can find the issue number from the branch name.

## Full Commit Message

The commit message should follow the structure below:

```plaintext
[tag]: A brief summary of the changes of this commit.

path/to/file/affected1: A brief description of changes made to this file.
path/to/file/affected2: A brief description of changes made to this file.
...

If needed, provide addtional context and explanations about the changes made in this commit.
It is preferred to mention the related Github issue if applicable.
```

A milestone commit is always on a development branch associated with a issue.
If it is a milestone, additionally add the following information:
1. Add `[milestone]` before the tag.
2. Mention the issue number after the brief summary, e.g., `A milestone to issue #42`.
3. Briefly summarize the test case status, e.g. `35/42 test cases passed`.
   - Milestone is to react to a big issue breaking down to smaller steps.
   - Thus, it is important to tract the progress, and is the only case allowing bypassing pre-commit hooks.

## Short Commit Message

The commit message should follow the structure below:

```plaintext
[tag]: A brief summary of the changes of this commit.
```

A short message is always for a delivery commit.

## Tags

A `git-msg-tags.md` file should appear in `{ROOT_PROJ}/docs/git-msg-tag.md` which
defines the tags related to the corresponding modules or modifications. The AI agent
**MUST** refer to this file to select the appropriate tag for the commit message.
If not, reject the commit, and ask user to provide a list of tags in `docs/git-msg-tag.md`,
by showing the example format below:

Please provide a `docs/git-msg-tags.md`, which can be as simple as the following example: 

```markdown
# Git Commit Message Tags
- `[core]`: Changeing the core functionality of the project.
- `[docs]`: Changing the documentation.
- `[tests]`: Changes test cases.
  - Use it only when solely changing the test cases! Do not mix with other changes with tests!
- `[build]`: Changes related to build scripts or configurations.
```

## Ownership

**DO NOT** claim the co-authorship of the commit with the user
in the message. It is the user who is **FULLY** responsible for the commit.

## Pre-commit Check

When **committing** the changes, this skill should faithfully follow
the input on if it is a milestone to use `--no-verify` or not.
If it is a milestone, the commit **MAY** bypass pre-commit hooks.
If it is a delivery commit, the commit **MUST NOT** bypass pre-commit hooks!
**DO NOT** use pre-existing issue as an excuse to bypass pre-commit in any case!