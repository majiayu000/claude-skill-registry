---
name: pmtl-multi-cli-orchestrator
description: PMTL_VN governance skill for routing Claude Code CLI, OpenAI Codex CLI, GitHub Copilot CLI, Gemini CLI, and optional Aider runs to the right worker based on task shape, repo policy, and verified capability docs.
---

# PMTL Multi CLI Orchestrator

## Purpose

Own routing for external AI CLI workers so PMTL tasks use the smallest correct worker set instead of sending the same prompt to every model.

## Use When

- The user asks for Claude Code, Codex CLI, Copilot CLI, Gemini CLI, Aider, or "multi agent" help.
- The task needs a second opinion, latest-doc research, or cross-model comparison.
- The agent must decide which external worker should review, search, or implement a narrow subtask.
- Worker configuration, prompts, or routing rules are being added or changed.

## Required Inputs

- The task goal and touched paths.
- Whether the task needs live docs or version-drift research.
- Whether the task is GitHub-centric, repo-policy-centric, or a narrow scripted batch task.
- Whether the worker is advisory only or is expected to return a concrete patch proposal.

## Expected Output

- A routing decision that names the worker or workers to use and why.
- Compact worker prompts that reference file paths instead of pasting large blobs.
- A validated merge-back decision that keeps PMTL docs and policy as the source of truth.

## Execution Approach

1. Start with `pmtl-workflow-router` and the canonical PMTL skill for the touched area. Use this skill only to decide whether an external worker adds leverage.
2. Stay local when the task is trivial, purely repo-local, or already fully covered by the active PMTL skill stack.
3. Use `references/routing-matrix.md` to pick the smallest correct worker set.
4. Use Gemini first when the task depends on current external docs, version drift, or "what changed lately" research.
5. Use Claude Code when the task spans more than a handful of files, changes repo policy or architecture docs, or needs a review-first loop with Claude-specific agents or hooks.
6. Use Codex when the task is narrow enough to express as one compact non-interactive prompt, or when you specifically want `exec`, `review`, `mcp`, or optional `--search`.
7. Use Copilot when the task is GitHub-centric in a concrete way: PRs, issues, Actions, GitHub MCP tools, Copilot custom agents, or prompt-file customization.
8. Use Aider only as an opt-in git-aware patch lane, ideally in dry-run mode, when the task explicitly asks for Aider or benefits from its repo-map and patch-planning behavior more than from Codex.
9. Merge only validated findings. External workers are advisors, not the policy authority.
10. If workers disagree with PMTL docs, treat repo docs as authoritative unless the conflict is caused by external product drift. In that case, verify with official product docs and update repo docs in the same task before changing routing.
11. If routing changes, update `AGENTS.md`, `docs/architecture/skills-taxonomy.md`, `docs/agent-cheatsheet.md`, and the worker-facing docs in the same task.

## Quality Criteria

- Route by task shape, not by hype.
- Do not duplicate the same question across four workers unless independent comparison is the point.
- Keep prompts path-based, compact, and auditable.
- Prefer official docs and current local `--help` output over stale memory.
- Record known worker limits and drift in `gotchas.md`.
- Prefer PMTL subagents first for repo-policy reasoning; use external workers only when they add leverage the local skill stack does not already provide.

## Verification

- Recheck the chosen worker path against `references/routing-matrix.md`.
- Confirm the task is not trivial enough to stay local.
- If worker config changed, run a minimal wrapper smoke command for the affected provider.
- Run `py infra/tools/codex_actions.py skill-audit` after changing this skill or other canonical PMTL skills. Treat it as an audit report, not a repo-wide pass gate for older skills.
- Update `references/official-sources.md` when a routing rule depends on a new doc capability.

## Edge Cases

- If the task is purely repo-local and no external worker adds real leverage, stay local and skip the wrappers.
- If two workers recommend conflicting actions, prefer PMTL repo docs and local verification over model confidence.
- If a worker exposes a feature locally but the repo does not rely on it yet, note it as optional instead of hard-wiring routing around it.
- If a worker times out or loses auth, fall back to the next-best worker and record the limitation.

## References

- `references/routing-matrix.md`
- `references/official-sources.md`
- `verification/checklist.md`
- `gotchas.md`
- `changelog.md`
