---
name: 056-design-avoid-breaking-changes
description: Use when you need to review a plan, OpenSpec change, specification, or implementation proposal for breaking-change risk across commands, skills, generated outputs, XML sources, README/docs, tests, CI, APIs, schemas, configuration, data, migration, and release guidance. This should trigger for requests such as Review breaking changes in this spec; Check compatibility risks; Avoid breaking changes in this OpenSpec change; Review migration impact before release; Assess command and skill compatibility. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Avoid Breaking Changes

Review planned repository changes for breaking-change and compatibility risk before implementation or release promotion. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Command contract compatibility: names, inputs, owning agents, outputs, safeguards, installer registration, and command inventories
- Skill routing compatibility: identifiers, metadata, descriptions, triggers, references, generated local output, and acceptance coverage
- Generated-output ownership: XML/source files versus `.agents/skills`, public `skills/`, `.cursor/commands`, `.cursor/rules`, and `docs/`
- Source and generator contracts: XML, XInclude, XSLT, Maven modules, schema expectations, and module validation
- README, localized README, changelog, migration, and deprecation guidance
- External and runtime contracts: APIs, schemas, data formats, configuration keys, persistence, CLI behavior, and CI expectations
- Structured compatibility reports with severity-ranked findings and validation guidance

## Constraints

Keep the review evidence-based, read-only, and scoped to compatibility risk unless the user explicitly asks for implementation.

- **MUST** read `references/056-design-avoid-breaking-changes.md` before producing compatibility guidance
- **MUST** identify the source artifacts reviewed and the compatibility surfaces considered
- **MUST** distinguish confirmed breaking changes, potential risks, non-breaking changes, and unknowns that need maintainer decision
- **MUST** include migration, deprecation, validation, or release-note guidance for intentional breaking changes
- **MUST** respect repository source ownership: edit XML and source docs, regenerate generated output through documented workflows, and avoid direct generated-output edits unless the repository explicitly owns that file
- **MUST NOT** modify plans, specs, source files, generated outputs, or issue descriptions during review unless the user explicitly requests implementation

## When to use this skill

- Review breaking changes in this spec
- Check compatibility risks
- Avoid breaking changes in this OpenSpec change
- Review migration impact before release
- Assess command and skill compatibility
- Find generated output compatibility risks
- Review API schema configuration or data contract changes

## Workflow

1. **Read the compatibility reference**

Read `references/056-design-avoid-breaking-changes.md`, then identify the source artifacts to review, their authority, and whether the request is read-only review or approved implementation.

2. **Inventory compatibility surfaces**

Check commands, skills, generated outputs, XML/source ownership, README/docs, tests, CI/build gates, external contracts, runtime behavior, data/configuration contracts, and release or migration guidance relevant to the proposed change.

3. **Classify findings**

Classify each finding as `BREAKING`, `POTENTIALLY BREAKING`, `NON-BREAKING`, or `UNKNOWN`. Include the affected users, artifacts, contracts, and validation evidence or missing evidence.

4. **Recommend migration and validation**

For each confirmed or potential risk, recommend deprecation, compatibility windows, migration notes, release-note updates, generator checks, focused tests, or owner decisions.

5. **Report the review outcome**

Produce a concise compatibility report with reviewed sources, risk summary by surface, severity-ranked findings, recommended validation, and a clear no-risk statement when no breaking-change risks are found.

## Reference

For detailed guidance, examples, and constraints, see [references/056-design-avoid-breaking-changes.md](references/056-design-avoid-breaking-changes.md).
