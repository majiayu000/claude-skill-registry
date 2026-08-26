---
name: contract-version-bump
description: "Use this skill when changing a machine-readable contract — a JSON Schema, an API spec, or a config schema — and bumping its version: tightening a constraint, adding/removing/renaming a field, introducing a breaking change, raising an API version, or writing the changelog entry for a schema change. Trigger on \"change the schema\", \"tighten this constraint\", \"bump the schema version\", \"breaking change to the API\", \"new API version\", \"changelog entry for a schema change\". Runs six phases — classify against the contract's OWN versioning rule (not generic semver instinct), find every version literal and vendored copy, check consumer compatibility for new keywords, apply consistently, write the changelog entry, and report downstream drift — codifying three non-obvious traps hit in a real case (GitLab issue #17, `aiat-enablement` repo, 2026-07-25)."
---

# contract-version-bump

Canonical skill: `skills/contract-version-bump/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/contract-version-bump/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the contract-version-bump skill" as: Read `skills/contract-version-bump/SKILL.md`.
