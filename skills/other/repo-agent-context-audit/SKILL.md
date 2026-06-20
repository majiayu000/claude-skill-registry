---
name: repo-agent-context-audit
description: Audit and standardize a repository's agent-readable context, including AGENTS.md, CLAUDE.md, WARP.md, CONTRIBUTING.md, .agents/skills, and specs/ PRODUCT.md and TECH.md contracts. Use when asked to review, design, create, scaffold, or improve repo instructions, agent onboarding, spec workflows, or cross-repo agent-context conventions.
---

# Repo Agent Context Audit

## Overview

Assess whether a repository has a small, usable agent context stack: a short top-level instruction file, task-specific skills, and behavior/implementation specs for substantial work. Default to a read-only audit and minimal recommendations; create or edit high-context files only when the user explicitly asks.

## Default Standard

Prefer this three-layer shape:

1. `AGENTS.md` or repo-equivalent: 80-150 lines, top-level routing only.
2. `.agents/skills/<task>/SKILL.md`: reusable workflows for common fragile tasks.
3. `specs/<id>/PRODUCT.md` and `specs/<id>/TECH.md`: checked-in contracts for substantial features.

Do not force this exact layout when a repo already has a coherent equivalent, such as `WARP.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or framework-specific instruction files. Map existing files to the layers first, then fill only the real gaps.

## Workflow

### 1. Discover

Run the read-only scanner when possible:

```bash
# From this skill directory:
python3 scripts/scan_repo_context.py <repo-root>
```

Then inspect the important files directly. Always search before creating:

- `AGENTS.md`, `CLAUDE.md`, `WARP.md`, `.claude/instructions.md`
- `CONTRIBUTING.md`, `README.md`, `.github/copilot-instructions.md`
- `.agents/skills/*/SKILL.md`
- `specs/**/{PRODUCT,product,TECH,tech}.md`

If multiple instruction files overlap, record their scopes and precedence instead of merging them by default.

### 2. Classify

Classify the repo into one of these states:

- **Healthy**: short top-level guidance, task workflows, and specs are discoverable.
- **Missing top-level router**: useful docs exist but agents lack an entrypoint.
- **Overloaded top-level file**: one file mixes rules, workflows, architecture, and reference data.
- **Specless complex repo**: substantial work happens without PRODUCT/TECH contracts.
- **Stale or divergent**: instructions contradict code, scripts, or observed repo conventions.
- **Unsafe to modify**: high-context files are generated, externally owned, or conflict across scopes.

### 3. Score

Use the rubric in `references/standards.md` for:

- top-level routing quality
- progressive disclosure
- procedural workflows
- decision gates
- production examples
- spec quality
- validation mapping
- stale or conflicting guidance risk

### 4. Recommend

Lead with the smallest useful change. Good recommendations usually look like:

- Add a short `AGENTS.md` that points to existing docs instead of duplicating them.
- Split a long top-level file into a router plus references or skills.
- Add `.agents/skills/write-product-spec` and `.agents/skills/write-tech-spec` only if spec writing is repeated.
- Add `specs/<id>/PRODUCT.md` and `TECH.md` templates only if the repo ships substantial features.
- Remove or rewrite stale instructions only after citing the conflict.

### 5. Scaffold Only On Request

When the user explicitly asks to create files, read `references/templates.md` and adapt the templates to the repo. Before editing:

- identify every `AGENTS.md` or equivalent whose scope covers the target path
- preserve existing high-context files unless the user asked for a rewrite
- keep generated docs small
- include actual repo commands, paths, and test gates
- leave placeholders only when the repo truly lacks the fact

## Decision Gates

| Case | Action |
|---|---|
| Small bugfix repo with README and clear tests | No spec system; maybe add a short `AGENTS.md` router |
| Repeated feature work with review churn | Add PRODUCT/TECH spec workflow |
| Existing `CLAUDE.md` or `WARP.md` is good | Link it from `AGENTS.md` or leave it as the repo-equivalent |
| Multiple teams or nested packages | Use scoped nested `AGENTS.md` only where rules genuinely differ |
| High-context file over 200 lines | Split into top-level router plus referenced skills/docs |
| User asks for bulk normalization | Audit first; do not batch edit until 2-3 repos have been manually validated |

## Operating Contract

Direct actions:
- Run read-only discovery, scoring, and scanner commands.
- Produce an audit report with cited files and smallest useful changes.
- Draft exact scaffold content when the user asks for proposed text.

Escalate before:
- Creating or editing `AGENTS.md`, `CLAUDE.md`, `WARP.md`, hooks, settings, or generated docs.
- Rewriting existing repo instructions instead of adding a short router or pointer.
- Batch-normalizing multiple repositories.

Evidence-backed pushback:
- Challenge new skill/spec scaffolding when the repo is small, has no repeated workflow, or already has a coherent equivalent.
- Challenge edits when the only evidence is style preference rather than a real agent failure, review bottleneck, or missing workflow.

Feedback loop:
- Promote repeated audit findings into the target repo's router, a task skill, or a spec template.
- Keep this skill's rubric and templates updated when multiple repos expose the same false positive or missing decision gate.

## Gotchas

- Do not treat every README as an agent instruction file. Top-level README files are usually entrypoints; nested README files are supporting evidence unless a repo explicitly routes agents there.
- Do not add `AGENTS.md` just because it is missing. If `CLAUDE.md`, `WARP.md`, or `CONTRIBUTING.md` already works as a coherent router, recommend a pointer or no change.
- Do not create PRODUCT/TECH specs for small bugfix repos. Specs are for ambiguity, cross-module risk, and repeated review churn.
- Do not silently normalize naming across repos. First report drift such as `PRODUCT.md` vs `product.md`, then ask before changing conventions.
- Do not edit high-context files during an audit. Scaffold only after the user asks to create or apply files.

## Report Format

Return concise findings:

```markdown
## Agent Context Audit
- state: <classification>
- top-level router: <present/missing/overloaded>
- reusable skills: <present/missing/not needed>
- specs: <present/missing/inconsistent/not needed>
- main risk: <one sentence>

## Smallest Useful Change
1. <change> - <why> - <estimated effort>

## Evidence
- <file>:<line> - <what it proves>

## Optional Scaffold
- <files to create or update, only if requested>
```

## Resources

- `scripts/scan_repo_context.py`: read-only repo scanner for high-context files, skills, and specs.
- `references/standards.md`: scoring rubric and design rules. Read for audits.
- `references/templates.md`: minimal `AGENTS.md`, `PRODUCT.md`, and `TECH.md` templates. Read only when scaffolding or proposing exact file contents.
