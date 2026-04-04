---
name: lcp-repo
description: Repository orientation and which Codex skills to use for each area (go-lcpd, protocol spec, docs, openai-serve, ExecPlans).
metadata:
  short-description: Repo navigation + skills index
---

This skill orients you in the `lightning-compute-protocol` repository and points you to the right skill for the job.

## Repository map (high level)

- `docs/protocol/`: LCP wire protocol spec (BOLT-style)
- `go-lcpd/`: reference implementation (daemon + tools)
- `apps/openai-serve/`: OpenAI-compatible HTTP gateway (forwards to `lcpd-grpcd`)
- `docs/`: Mintlify docs site

## Which skill to use

- Protocol spec edits: use `$lcp-protocol-spec`
- `go-lcpd/` code changes: use `$lcp-go-lcpd`
- `apps/openai-serve/` code changes: use `$lcp-openai-serve`
- Mintlify docs edits: use `$lcp-mintlify-docs`
- WYSIWID-style design docs in `go-lcpd/`: use `$lcp-wysiwid-spec`
- Complex feature/refactor planning: use `$lcp-execplan`
- Creating commits (only when asked): use `$lcp-git-commit`

## Default operating rule

If a directory has an `AGENTS.md`, treat it as a pointer to the authoritative skill(s) for that scope.
