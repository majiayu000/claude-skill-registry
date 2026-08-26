---
name: repo-audit
description: "Use this skill when the user wants to audit a repository for baseline compliance, check code quality, security posture, CI/CD setup, testing, documentation, and ecosystem configuration. Runs 9 checklist categories and emits a Markdown report plus JSON sidecar at .orchestrator/metrics/repo-audit-<timestamp>.json. <example>Context: User is in a project repo and wants a baseline compliance check. user: \"/repo-audit\" assistant: \"Running repo-audit across 9 categories — Configuration, Code Quality, Git Hygiene, CI/CD, Testing, Security, Documentation, Clank Integration (optional), and MCP Configuration. Will produce a Markdown checklist report and JSON sidecar.\" <commentary>The user wants a compliance check; this skill is appropriate because it runs all 9 categories with pass/fail/warn/skipped statuses and writes structured output.</commentary></example>"
disable-model-invocation: true
---

# repo-audit

Canonical skill: `skills/repo-audit/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/repo-audit/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the repo-audit skill" as: Read `skills/repo-audit/SKILL.md`.
