---
name: journey-audit
description: "Use this skill when the user wants the PRODUCT audited from the outside in — what the website promises vs what the code does vs what a real user experiences vs what actually arrives by mail vs what the data says is used. Runs a 7-role read-only wave (R5 writes only under an explicit SAFETY block) against a per-repo `.orchestrator/journey-manifest.md` and writes a dossier to docs/audits/. Distinct from /discovery, which checks code quality inside-out — this checks product truth outside-in; they complement, neither replaces the other. Triggers \"journey audit\", \"Nutzersicht-Audit\", \"audit the product from the user's side\", \"/journey-audit\"."
disable-model-invocation: true
---

# journey-audit

Canonical skill: `skills/journey-audit/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/journey-audit/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the journey-audit skill" as: Read `skills/journey-audit/SKILL.md`.
