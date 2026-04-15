---
name: pr
description: Use when the user asks to create or update a pull request for the current branch.
---

Prepare and open a PR/MR for the current branch — from "work is done" to "PR is open and reviewable."

## The Core Problem

The reviewer arrives cold. They didn't write this code, and neither did another human — an agent did. The PR description is the only bridge between "what happened in the agent's context" and "what the human needs to decide." Every section exists to serve that handoff. If a section doesn't help the reviewer, cut it.

## Multi-Repo Awareness

Work spanning multiple repositories (parent + submodule, multiple services) needs a separate PR per repo. Cross-reference paired PRs. Always `cd` into each repo root before running the create command — git tools infer the remote project from the current directory.

## Conventional Commits Reference

!`cat ~/.claude/skills/conventional-commits.md`

## CLI Tool Reference

`--fill` conflicts with explicit title/body in both `gh` and `glab`. Always use heredoc for the body.

| | Title | Body | Create |
|---|---|---|---|
| `gh` | `--title` | `--body` | `gh pr create` |
| `glab` | `--title` | `--description` | `glab mr create` |

Always pass the remove-source-branch flag (`gh`: `--delete-branch`, `glab`: `--remove-source-branch`) so the source branch is cleaned up on merge.

When in doubt, check `--help` before invoking — a failed MR create can leave orphaned remote state.

## PR Body

Omit sections that don't apply. No placeholders, no filler.

**Task** — issue link, or one-line description of what was asked.

**Summary** — what + why. Approach chosen and why: "X over Y because Z." 2-4 lines max.

**Changes** — one bullet per meaningful change, grouped by area. A change list, not a file list.

**Self-Review** — markdown checklist of what the agent verified (`[x]`) and what it couldn't (`[ ]`). One concrete claim per item.

**Human Review** — checklist of specific things the reviewer should verify. Action items only — where human judgment matters most.

```
$(cat <<'EOF'
## Task

## Summary

## Changes

-

## Self-Review

- [x]
- [ ]

## Human Review

- [ ]

EOF
)
```
