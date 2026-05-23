---
name: platform-architect
description: Architect and implement modern full-stack web/native platform work across Next.js, Expo, Convex, and monorepo tooling. Use when the task needs stack detection, platform-level planning, cross-cutting architecture, or repo-native verification workflows. Route general web UI review to repo-local web-design-guidelines and React/Next performance review to repo-local vercel-react-best-practices when installed. Do not use for narrow dependency upgrades, PR review remediation, docs-only alignment, or Dash-only audits.
---

# Platform Architect

Use this skill to route broad platform work into the correct web, native, backend, and tooling lanes without redoing the same repo preflight every turn.

## Workflow

1. Read the repo `AGENTS.md` first for local constraints and canonical commands.
2. Run `/home/bjorn/.codex/skill-support/bin/repo-inventory detect --cwd <repo> --out <json>`.
3. Run `/home/bjorn/.codex/skill-support/bin/repo-inventory matrix --input <json> --format md`.
4. Choose the active lane:
   - Next.js / React web -> read `references/next-web.md`
   - Expo / React Native -> read `references/expo-native.md`
   - Mixed full-stack or monorepo coordination -> read `references/fullstack-platform.md`
5. Read `references/tooling-and-verification.md` before running checks or changing commands.
6. If the task narrows into a specialized domain, explicitly invoke the right downstream skill:
   - Convex architecture or audits -> `$convex-audit` or `$convex-feature-spec`
   - General web UI review -> repo-local `$web-design-guidelines` when installed
   - React/Next performance or render-quality review -> repo-local `$vercel-react-best-practices` when installed
   - Dash callback or Dash UI review -> `$dash-audit`
   - Design/build work -> `$frontend-design`
   - Docs sync -> `$docs-align`
   - Dependency work -> `$gh-deps-intel`

## Use When

- The user asks for platform architecture, stack-wide planning, or implementation across web/native/backend boundaries.
- The repo shape is unclear and you need a deterministic platform inventory first.
- The work touches Next.js, Expo, Convex, Bun/pnpm, Turbo, or mixed platform concerns together.

## Do Not Use When

- The task is only a dependency-upgrade workflow.
- The task is only PR/comment remediation.
- The task is only a docs drift pass.
- The task is only a narrow UI audit with no platform decisions.
- The task is a Dash-only audit with no cross-platform architecture work.

## Outputs

- A short lane selection summary.
- A concrete implementation or review plan tied to the detected stack.
- Repo-native verification commands, not invented commands.
- Explicit downstream skill routing when the task narrows into UI, review, docs, or dependency work.

## Resources

- Inventory wrapper: `scripts/platform_inventory.py`
- Web guidance: `references/next-web.md`
- Native guidance: `references/expo-native.md`
- Cross-stack guidance: `references/fullstack-platform.md`
- Verification policy: `references/tooling-and-verification.md`
