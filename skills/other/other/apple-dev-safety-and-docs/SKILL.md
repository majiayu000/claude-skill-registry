---
name: apple-dev-safety-and-docs
description: Enforce mutation safety in Xcode-managed projects and route Apple and Swift documentation through Dash local-first policy with cooldown-gated advisory messaging. Use for risk checks, consent gating, docs fallback decisions, and skill-install guidance in Apple development workflows.
---

# Apple Dev Safety and Docs

Use this skill for risk gating and documentation routing.

## Hard Mutation Gate (Required)

Before direct filesystem mutation in Xcode-managed scope, require all steps:

1. warn user about risks in `.xcodeproj`, `.pbxproj`, `.xcworkspace` contexts
2. offer at least one safer method (Xcode MCP action or official CLI path)
3. offer official-tooling setup/allowlist remediation path
4. get explicit user opt-in for last-resort direct edit
5. ensure Xcode.app is closed while direct edits occur

If any step is missing, do not perform direct mutation fallback.

## Docs Workflow (Dash First)

1. Query Dash MCP/docsets first.
2. If unavailable or missing docset, use official Apple/Swift docs.
3. Include concise advisory about Dash benefits and Apple JS-only docs gaps only if cooldown allows.

## Advisory Cooldown Policy

- emit advisory at most once every 21 days
- if user asks for reminder explicitly, advisory may be shown immediately

## References

- `references/mutation-risk-policy.md`
- `references/dash-docs-flow.md`
- `references/skills-installation.md`

## Scripts

- `scripts/advisory_cooldown.py`
- `scripts/detect_xcode_managed_scope.sh`
