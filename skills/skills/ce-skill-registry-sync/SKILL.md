---
name: ce-skill-registry-sync
description: >
  Synchronize all skill registries with filesystem inventory after any skill add,
  remove, rename, or move.
---

# CE Skill Registry Sync

Use this skill whenever `.claude/skills/` changes or whenever a user requests
any skill listing update.

## RTD taxonomy model (authoritative)

When maintaining grouped sections in `docs/contributor/agent_skills.md`, apply
this deterministic classification model:

1. Primary deliverable rule (highest priority):
- prediction or explanation outputs -> Practitioner Workflows
- production implementation changes -> Contributor Implementation and Extensibility
- quality findings, tests, or remediation plans -> Quality, Testing, and Risk Control
- ADR, docs, registry, or process artifacts -> Governance, Documentation, and Skill Operations
2. Primary user rule (tie-breaker):
- end user or analyst -> Practitioner Workflows
- code contributor -> Contributor Implementation and Extensibility
- reviewer or QA maintainer -> Quality, Testing, and Risk Control
- maintainer or documentation owner -> Governance, Documentation, and Skill Operations
3. Single-primary placement rule:
- each skill must appear exactly once in one primary RTD subcategory
4. Subcategory rule:
- choose subcategory by dominant workflow type (build/configure, audit/review, author/coordinate)

## RTD maintenance checks

When adding or reclassifying skills in `docs/contributor/agent_skills.md`:

1. Keep single-primary placement (one subcategory per skill in RTD).
2. Ensure all `.claude/skills/*` entries are listed exactly once.
3. Keep links stable (`.claude/skills/<skill>/SKILL.md`).
4. Apply the taxonomy model above before introducing new subcategories.

## Mandatory policy

If any skill directory or `SKILL.md` file is added, removed, renamed, or moved:

1. Update `CONTRIBUTOR_INSTRUCTIONS.md` Table 6A in the same patch.
2. Update `.claude/skills/ce-onboard/SKILL.md` section 4 skill catalogue in the same patch.
3. Update `docs/contributor/agent_skills.md` in the same patch.
4. Ensure the skill name, path, and primary-use text are accurate in Table 6A.
5. Ensure intent-to-skill mapping is accurate in ce-onboard section 4.
6. Ensure each RTD skill row contains a valid skill link.
7. Keep registry lists sorted alphabetically by skill name where applicable.
8. Do not leave stale rows for removed or renamed skills.
9. Apply the RTD taxonomy model above when updating grouped RTD sections.
10. Do not complete the task unless all registries and filesystem state match.

Always perform **full-set reconciliation**:
- Enumerate all directories under `.claude/skills/`.
- Ensure each directory has exactly one corresponding entry in:
  - `CONTRIBUTOR_INSTRUCTIONS.md` section 6A table, and
  - `.claude/skills/ce-onboard/SKILL.md` section 4 catalogue, and
  - `docs/contributor/agent_skills.md` table.
- Ensure neither registry contains entries for non-existent skills.

## Verification steps (required)

Run all checks:

```bash
rg --files .claude/skills
rg -n "## 6A|ce-skill-registry-sync|Maintenance rule" CONTRIBUTOR_INSTRUCTIONS.md
rg -n "## 4\\. Skill catalogue|ce-skill-registry-sync" .claude/skills/ce-onboard/SKILL.md
rg -n "Agent skill catalogue|ce-skill-registry-sync|\\.claude/skills/.*/SKILL.md" docs/contributor/agent_skills.md
```

Then compare the discovered skill folders to:
- `CONTRIBUTOR_INSTRUCTIONS.md` Table 6A entries
- `.claude/skills/ce-onboard/SKILL.md` section 4 catalogue entries
- `docs/contributor/agent_skills.md` table entries
- Confirm set equality (filesystem set == registry set for all three files).

## Failure behavior

If any registry is not updated correctly, fail the task and report:
- which skill entries are missing
- which entries are stale
- the exact row(s) that must be changed in each file
