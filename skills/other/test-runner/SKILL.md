---
name: test-runner
description: "Use this skill when orchestrating agentic end-to-end tests. Resolves target + profile, dispatches the right driver(s) (playwright for web today, peekaboo for macOS (issue #381)), invokes the ux-evaluator agent (opus, read-only) against driver artifacts, reconciles findings with the open issue tracker via scripts/lib/test-runner/issue-reconcile.mjs, and writes report.md + JSONL roll-up. Wraps upstream tools (no forks). Hard-gates Playwright MCP for browser drive (4× token cost vs CLI per Microsoft's own benchmark)."
disable-model-invocation: true
---

# test-runner

Canonical skill: `skills/test-runner/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/test-runner/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the test-runner skill" as: Read `skills/test-runner/SKILL.md`.
