---
name: vitaecontext
description: Route broad or ambiguous VitaeContext work to the right module while keeping context scoped. Use when a request spans multiple surfaces, asks for overall digital-presence strategy, involves provider or install architecture, needs agent-context planning, or the correct platform skill is unclear.
license: MIT
metadata:
  homepage: https://vitaecontext.github.io/
  repository: https://github.com/vitaecontext/vitaecontext
---

# VitaeContext

## Overview

Use this skill as the orchestrator for the whole repository. Its main job is to select the right module skill, avoid loading irrelevant platform rules, and sequence cross-platform work in a sane order.

## Wiki context

- Read [wiki/vitaecontext.md](wiki/vitaecontext.md) when the user asks what VitaeContext is, what ACO means, how the skill system works, what the installer deploys, or how the repository's runtime architecture is organized.
- Use [wiki/vitaecontext.md](wiki/vitaecontext.md) as the graph entrypoint before loading module wiki or reference files for broad architecture and routing tasks.
- If the wiki file is unavailable in an older install, continue with the relevant `references/` file and mark wiki-specific guidance as unavailable when it affects confidence.

## Routing workflow

1. Identify the target surface from the request.
2. Load only the matching module skill unless the user explicitly asks for a cross-platform pass.
3. If the request spans multiple surfaces, resolve an explicit existing Career Context file or retrieve the smallest relevant subtree from an explicit existing VitaeGraph. Start with `vitaecontext-build` only when facts are scattered, conflicting, or no usable source of truth exists.
4. If the request is only about the skill system itself, read the references in this skill before changing provider adapters or install instructions.

## Execution contract

Before loading detailed module context, resolve these five items from the request and available material:

1. `Surface`: the one primary module that owns the requested outcome.
2. `Mode`: audit, draft, apply, validate, retrieve, or maintain.
3. `Authority`: whether the user asked only for analysis or authorized edits to a named artifact.
4. `Evidence`: explicit files, URLs, exports, screenshots, context files, or VitaeGraph path that may be inspected.
5. `Depth`: the smallest module-defined depth that can honestly satisfy the request.

Do not load a platform wiki merely because the skill has one. Load the module `SKILL.md` first, then only the references or wiki entry routed by the selected mode. Preserve the distinction between analysis and mutation: an audit does not authorize edits, while an explicit request to build, update, repair, or implement normally does.

After the module finishes, require artifact-appropriate verification. Examples include a build or test for portfolio code, plain-text extraction for a final rendered CV, graph validation before VitaeGraph indexing, and factual comparison for public profile copy. If verification cannot run, report the missing check instead of implying completion.

For broad requests with no clear surface:

- Active applications or job-description tailoring: route to `vitaecontext-cv`.
- Recruiter discovery or profile search: route to `vitaecontext-linkedin`.
- Proof-of-work, repositories, or developer credibility: route to `vitaecontext-github` or `vitaecontext-portfolio`, based on the supplied asset.
- Audience building, posting strategy, or public conversation loops: route to `vitaecontext-x`.
- Conflicting, scattered, or cross-platform facts: route to `vitaecontext-build` first.
- Detailed multi-file career records, hierarchical education or project modeling, graph validation, or graph indexing: route to `vitaecontext-vitaegraph`.

## Token discipline

- Route to one module by default.
- Load the Career Context file before platform references only when facts, consistency, or cross-surface rewriting matter.
- Prefer public URL inspection, local search, or a compact pasted section over asking the user to dump every asset into the prompt.
- Summarize inspected inputs and ask for the smallest missing input set.
- Do not expand into algorithm explanation unless the user asks why.

## Intake workflow

- If the user already has a Career Context file, ask for or use its explicit path before rewriting platform assets.
- If the task spans multiple surfaces and no usable source of truth exists, or the user's facts are scattered, recommend creating or repairing the Career Context file first. Do not block work on it when an explicit existing context file or VitaeGraph already supplies the needed facts.
- Do not block a narrow one-off edit on a full context file when the supplied material is already enough.
- For public URLs, fetch or inspect public material when tools allow it and cite which source was used.
- For private or login-gated surfaces, ask the user for pasted section text, screenshots, exports, or a local text file instead of guessing.
- If critical facts are missing, ask only for the minimum extra inputs needed to proceed.

## Version check workflow

- When a user asks whether VitaeContext is current, or when an installed skill seems older than the documented package behavior, prefer the explicit CLI check instead of guessing from memory.
- To check the package being run, use `vitaecontext update` or `npx vitaecontext update`.
- To check the version installed for a specific provider, use `npx vitaecontext@latest update --provider <provider>` with the same `--project-root` or `--target-dir` flags used for install when the provider is not in its default location.
- Treat the npm lookup as a networked, user-visible action. Do not claim that VitaeContext performs background update checks.
- If the check reports `outdated`, recommend reinstalling with `npx vitaecontext@latest install --provider <provider> --force` and preserve any provider-specific destination flags.

## Module map

- LinkedIn work: `vitaecontext-linkedin`
- GitHub work: `vitaecontext-github`
- CV or ATS work: `vitaecontext-cv`
- Web portfolio work: `vitaecontext-portfolio`
- X or Twitter work: `vitaecontext-x`
- Personal source-of-truth context work: `vitaecontext-build`
- Detailed career knowledge graph work: `vitaecontext-vitaegraph`

## Boundaries

- Do not load every module by default.
- Do not invent platform behavior that the hub has explicitly marked as uncertain or disputed.
- Do not rewrite the shared methodology in provider adapter folders. Keep the portable source of truth in `.skills/agent-skill/`.
- When advice depends on current platform capabilities, paid tiers, ranking behavior, product limits, or provider support, verify with current official sources when tools allow it or label the claim as historical, disputed, or inferred.
- For cross-platform outputs, label major claims as `Verified`, `From context`, `From supplied source`, `Official/current source`, `Inference`, `Needs evidence`, or `Inaccessible` when the source status could affect the recommendation.

## Self-review

Before returning from an orchestration task, check that:

- exactly one primary module owned each requested output, with additional modules loaded only when the request required them
- the selected mode and mutation authority matched the user's request
- private context was retrieved progressively and was not exposed in a public output without explicit support
- verification ran at the artifact boundary, or the missing verification was reported
- the next action is narrow and does not silently create or convert a Career Context file or VitaeGraph

## Response shape

For broad requests, return:

1. the selected workflow or module
2. inputs used and missing inputs
3. concrete edits or recommendations
4. unresolved risks or assumptions
5. next action, preferably creating or updating the context file only when that would materially reduce factual drift

## References

- Read [references/module-routing.md](references/module-routing.md) when the user request is broad or ambiguous.
- Read [references/provider-matrix.md](references/provider-matrix.md) when changing adapter behavior.
- Read [references/installation-strategy.md](references/installation-strategy.md) when changing packaging or install guidance.
