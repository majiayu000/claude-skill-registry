---
name: automate-me
description: 'Use when asked to create or refresh a personal mode skill and open a reviewable PR. Mines recent session history for a recurring manual workflow, drafts one self-contained skill file, and opens a PR with evidence. Not for shared repo skills or work that skips human approval.'
disable-model-invocation: true
---

# Automate me

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Create or refresh a personal mode skill. |
| Authority | Human-only. Require explicit human invocation; preview the target file, skill content, and PR consequence before any write, push, or remote publish. |
| Side effect | Creates or edits one personal mode skill file in a local working copy on a new branch, commits it, pushes the branch, and opens a reviewable PR. No files beyond that skill file and no remote state beyond that branch and PR are touched; no credentials are read or written. |
| Done | Evidence-backed personal mode skill in a reviewable PR. |

## Inputs

- A personal workflow to encode, supplied either as a direct description by the human or as a pointer to recent session or conversation history to mine for a repeated manual task pattern. At least one of these must be present.
- Target skill slug and file path. Optional; derive a slug from the workflow if the human does not supply one, and confirm it before writing.
- Repository and base branch to open the PR against. Must be supplied or determinable from the current working copy; if neither, stop and ask.

## Procedure

1. Require explicit human invocation. Confirm the human intends to author or refresh a personal mode skill and open a remote PR for it; do not proceed on inferred intent. Done when: the human confirms intent to author a personal skill and open a PR.
2. Identify the recurring personal workflow. Use a description supplied by the human. Otherwise, mine recent session or conversation history for a task the human performs manually more than once. Name the repeated pattern and the sessions where it appears as evidence. Done when: the recurring workflow is named with supporting session evidence.
3. If no recurring workflow can be supported by the history or description, stop and report that there is no candidate. Do not invent a workflow or fabricate history evidence. Done when: the absence of a candidate is reported or a candidate is confirmed.
4. Draft the personal mode skill as a self-contained skill file with a name, trigger predicate, short procedure, and required inputs. The skill must not depend on another skill, module, or external rule file. Done when: the skill file is drafted as self-contained with all required sections.
5. Show the human the target file path, full skill content, branch name, and consequence of opening a PR. Wait for explicit approval before any mutation. Done when: the human approves or declines the preview.
6. On approval, create a new branch in the local working copy and create or edit the skill file at its target path. Write only that one file. Done when: the skill file is written on a new branch and no other file is touched.
7. Commit the change with a message naming the personal workflow encoded. Done when: the commit is created with the workflow-naming message.
8. Push the branch and open a reviewable PR whose description states the workflow encoded, the history evidence used, and the skill file path. Done when: the branch is pushed and the PR is opened with the required description.
9. Capture the PR URL as the success evidence. Done when: the PR URL is captured.

## Failure and recovery
- No recurring workflow found: stop, report no candidate, mutate nothing.
- Human declines the preview: do not write, commit, or push; leave the working copy unchanged.
- Skill file is malformed after drafting: correct frontmatter and sections before pushing; never push a skill that fails its own format.
- Push or PR open fails (authentication, network, protected base, permission): stop, report the exact error, and leave the local branch in place for retry. Do not force-push or rewrite an unrelated branch.
- Partial result rule: if the file is written and committed but the PR cannot be opened, report the local commit as the partial result and the blocking error; the done predicate is not met until a PR URL exists.

## Output
A reviewable PR URL, the skill file path, and a one-line summary of the encoded personal workflow backed by the history evidence or description used — classified done only when the PR URL exists, otherwise blocked with the failure class named.
