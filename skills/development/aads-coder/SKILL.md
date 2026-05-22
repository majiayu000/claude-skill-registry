---
name: aads-coder
description: Implement direct code changes in AADS-ULoRA with minimal blast radius, module-aware validation, and CI-aligned checks. Use for bug fixes, feature work, and refactors across src, tests, scripts, config, and docs-linked runtime paths.
---

# AADS Coder

## Workflow

1. Scope and ownership.
- Start from `aads-status-triage` output when available.
- If the request is primarily config/pipeline contract changes, route to `aads-config-pipeline-guardrails`.
- Identify touched files and nearest owning tests.
- Read `references/coding-playbook.md`.

2. Implement with minimal blast radius.
- Keep edits localized to owning modules.
- Avoid interface changes unless explicitly required.
- Preserve canonical `scripts/` paths in docs and commands.

3. Align tests with behavior.
- Add or adjust tests in mirrored suites.
- Prefer targeted tests before broad suites.

4. Run validation gates.
- Run module-targeted checks first.
- Add domain gates only when relevant (router policy, phase5 perf checks, docs sync checks, colab smoke checks).

5. Emit implementation summary.
- Include changed behavior, commands run, and residual risks.

## Output Contract

Return sections in this order:
1. Scope and files changed
2. Behavior changes
3. Validation commands and results
4. Compatibility notes
5. Known risks / follow-ups

## References

- Use `references/coding-playbook.md` for module-to-test mapping and command bundles.
