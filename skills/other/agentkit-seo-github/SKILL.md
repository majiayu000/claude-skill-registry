---
name: agentkit-seo-github
description: Optimize GitHub profile and repository discoverability, clarity, and trust signals using documented search, metadata, and repository-structure guidance. Use when the user asks about profile README content, pinned repos, repository README structure, topics, descriptions, social preview, code search visibility, or GitHub-facing portfolio positioning.
---

# AgentKit SEO GitHub

## Overview

Use this skill to improve GitHub discoverability, comprehension, and trust without claiming undocumented ranking guarantees.

## Reference selection

- Bio, pinned repos, repo naming, About text, README packaging: [references/profile-and-repo-structure.md](references/profile-and-repo-structure.md)
- Copy blocks for bios, READMEs, About text, topics, pins: [references/section-recipes.md](references/section-recipes.md)
- Code search, indexing limits, Linguist, language stats: [references/search-indexing-and-linguist.md](references/search-indexing-and-linguist.md)
- Full-profile or repository audit: [references/profile-and-repo-audit.md](references/profile-and-repo-audit.md)
- `AGENTS.md`, Copilot instructions, AI-readable repo structure: [references/copilot-and-agent-readiness.md](references/copilot-and-agent-readiness.md)

## Token discipline

- Do not load every repository README unless the user asks for a full profile audit.
- For profile work, inspect profile metadata, pinned repos, and at most 3 highest-signal repositories by default.
- For one repository, stay inside that repository unless cross-profile positioning is explicitly requested.
- Prefer repository metadata, About text, topics, pinned status, README opening sections, and visible language signals before loading entire files.
- Keep source ledgers compact: list input groups, not every minor fetched page.
- Do not restate full checklists in the final output. Report only findings that change the user's next action.
- Name next inspection if bounded.

## Depth contract

Use the smallest honest audit depth:

- `Quick scan`: profile fields, profile README opening, pinned repositories, and obvious metadata gaps.
- `Default audit`: quick scan plus up to 3 highest-signal repositories, using repository metadata, README openings, topics, and language signals.
- `Deep audit`: full README/file inspection, `.gitattributes`, setup paths, CI, licenses, social previews, and repo-by-repo consistency.

Default to `Default audit` for broad profile requests. Offer `Deep audit` as an optional next step when the current answer would benefit from more evidence. Do not choose `Deep audit` silently unless the user asks for a complete audit, every repository, exact file changes, or repository-level remediation.

## Intake workflow

- If the user provides a GitHub profile or repository URL, fetch and inspect public profile, pinned repository, repository metadata, README, topics, default branch, and visible language signals when tools allow it.
- If the user provides only a username, treat it as enough to inspect public GitHub material when tools allow it.
- If the task depends on private repositories, contribution details, or account settings, ask the user for screenshots, copied settings, exports, or explicit local files instead of guessing.
- If the user has or needs an agent context file, load or recommend `agentkit-seo-agent-context-optimization` before rewriting profile-level positioning.
- For repository-specific work, prefer concrete file edits when the repository is available locally; otherwise return copy blocks and a change checklist.
- Do not request login or tokens unless the user explicitly asks for private repository work.

## Rules

- Distinguish documented GitHub behavior from inference.
- Separate facts verified on GitHub, facts supplied by the user's context files, and recommendations inferred from those facts.
- Optimize for search clarity, repository comprehension, and maintainer trust.
- Do not promise hidden ranking boosts from stars, forks, or activity patterns.
- Do not invent numbers, percentiles, ranking mechanics, vulnerability impact, award scope, repository health, or pinned-repository status.
- Avoid hype language unless the user provided evidence that supports it. Prefer precise proof over louder branding.
- Keep examples factual to the user's real projects.
- Keep recommendations scoped to the user's actual repositories and public goals.
- Keep profile metadata, pinned repositories, README copy, and repository structure aligned around the same public positioning.
- For rewrites, improve clarity, proof, and discoverability before inventing a more aggressive branding angle.
- Recommend `AGENTS.md` or Copilot instruction files only when the repository is agent-facing, complex enough to need operational guidance, or the user explicitly asks for agent-readiness work.

## Response shape

Return:

1. source ledger: public inputs inspected, context files used, and inaccessible inputs
2. priority issues by profile, pinned repos, and repositories
3. ready-to-apply copy or file changes
4. confidence notes that label each major recommendation as verified, context-derived, or inferred
5. next actions, including context-file creation when profile facts are weak

For audits, make the output feel like a grounded review rather than a generic marketing report. Use concise labels such as `Verified`, `From context`, and `Inference` when a claim could otherwise be ambiguous.
When the audit is intentionally bounded, include a one-line `Depth note` that says what was not inspected and what deeper inspection would add.
