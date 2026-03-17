---
name: localsetup-skill-normalizer
description: "Normalize skills already in the tree for Agent Skills spec compliance and platform-neutral wording. Use when the user wants to normalize one or more skills in _localsetup/skills/ (e.g. after import, or after copying files in), or when batch-reviewing previously imported skills. Applies _localsetup/docs/SKILL_NORMALIZATION.md; shows summary and key edits, then applies on approval."
metadata:
  version: "1.1"
---

# Skill normalizer

**Purpose:** Normalize any skill(s) already in the framework skill tree so each SKILL.md is spec-compliant and platform-neutral. Use this when skills were imported without normalization, dropped in by copying files, or when you want to batch-normalize previously imported skills.

## When to use this skill

- User says "normalize this skill", "normalize the Ansible skill", "normalize all imported skills", or "make this skill spec-compliant and platform-neutral."
- User copied a skill directory into `_localsetup/skills/` or `_localsetup/skills/` and wants it normalized.
- Batch review: normalize several skills (e.g. localsetup-ansible-skill, localsetup-linux-service-triage, localsetup-linux-patcher) in one pass.

## Workflow (agent steps)

1. **Identify target(s)**  - User specifies one skill (e.g. by name or path) or "all" (all skills under `_localsetup/skills/` or `_localsetup/skills/`). Resolve to a list of skill directories; each must contain SKILL.md.
2. **Load rules**  - Read _localsetup/docs/SKILL_NORMALIZATION.md (or _localsetup/docs/SKILL_NORMALIZATION.md from framework source). Use the spec-compliance checklist, before/after frontmatter examples, and platform-neutralization rules (including the generic snippet for "Running from an agent").
3. **For each skill**  - Apply the checklist and rules to SKILL.md only (in memory or a temp copy). Do not modify references, scripts, or playbooks. Produce:
   - **Summary**  - Short prose (e.g. "Frontmatter: add compatibility, remove platform metadata; description generalized; replace 'Integration with X' with generic section.").
   - **Key edits**  - Concrete list (e.g. "Remove metadata.openclaw"; "Replace lines 427–453 with generic snippet from SKILL_NORMALIZATION.md"; "Description: change 'OpenClaw VPS' to 'VPS (optional agent-host examples)'.").
4. **Present and get approval**  - Show summary and key edits to the user. Ask: "Apply these changes to SKILL.md?" If **yes**, write the normalized SKILL.md to the skill directory. If **no**, skip that skill; do not write.
5. **Confirm**  - Tell the user which skills were normalized and that they can run deploy if needed.

## Scope

- **Only SKILL.md** is modified. References, scripts, assets, and playbooks in the skill directory are unchanged.
- The same rules as import-time normalization: product-agnostic detection of platform-specific sections (e.g. "Integration with …", "From … Agent"), replacement with generic wording from SKILL_NORMALIZATION.md.

## Reference

- _localsetup/docs/SKILL_NORMALIZATION.md  - Single source of truth: spec checklist, frontmatter examples, platform-neutralization rules and generic snippets.
- _localsetup/docs/SKILL_IMPORTING.md  - Import workflow including the optional "Normalize before copy?" step; same rules apply there.
