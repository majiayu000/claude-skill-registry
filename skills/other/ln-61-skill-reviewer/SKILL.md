---
name: ln-61-skill-reviewer
description: "Reviews standalone skills and marketplace integration before publication. Use for skill release readiness; not for reviewing product code or implementation plans."
---

# Skill Reviewer

Review skill changes without modifying the repository or external state.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Repository scope and evidence | Native file search, focused reads, and Git diff | Equivalent read-only shell commands |
| Frontmatter and skill structure | Installed skill validator | Manual YAML, path, name, and length checks |
| Plugin integration | Installed plugin validator plus JSON parsing | Manual manifest and catalog comparison |
| Claude discovery | Strict Claude plugin validator | Manual Claude catalog and source-path inspection |
| Current host rules | Official host documentation | Mark the claim `UNVERIFIED` when unavailable |
| Behavioral independence | Fresh subagent or clean context | Separate self-review passes with reduced-confidence disclosure |

Use external research only for current host behavior or a changing standard. Do not use web sources to override the repository's actual files, installed versions, or local validation output.

Tool absence is not itself a skill defect. Apply the documented fallback and use `BLOCKED` only when the missing capability prevents a reliable verdict.

## Checklist

- [ ] Establish the review target from explicit paths, the Git diff, staged files, and untracked files.
- [ ] Read the repository instructions and both marketplace catalogs before judging repository-specific conventions.
- [ ] Separate primary skills from manifests, catalogs, and documentation affected by the same change.
- [ ] Confirm every skill folder contains one canonical `SKILL.md`; treat host-specific copies as defects.
- [ ] Confirm frontmatter contains only `name` and `description`, and the folder name equals `name`.
- [ ] Check that each description states the capability, positive trigger, and important near-negative boundary.
- [ ] Check that descriptions stay within the host limit and avoid claims broader than the workflow supports.
- [ ] Confirm each skill is standalone: no required skill, MCP server, tracker, coordinator, worker, or shared runtime.
- [ ] Treat an ordered checklist as the Definition of Done; flag a duplicate completion section.
- [ ] Preserve non-obvious domain rules, tool-routing decisions, safety gates, evidence requirements, verdict mapping, output contract, and residual risks.
- [ ] Flag explanations a capable current model already knows unless they prevent a demonstrated execution failure.
- [ ] Verify every required capability has an available tool path, a credible fallback, or an explicit `BLOCKED` outcome.
- [ ] Check mutation boundaries: review, audit, test-planning, and discovery skills must remain read-only.
- [ ] Check that optimization skills retain or discard mutations using measured evidence.
- [ ] Check that acceptance-test skills cannot repair product code or touch unapproved external state.
- [ ] Trace the workflow through missing tools, insufficient context, dirty Git state, failed commands, and conflicting evidence.
- [ ] Check that the output contract distinguishes facts, inferences, missing evidence, verdict, and residual risk.
- [ ] Inspect neighboring descriptions for trigger overlap without assuming the skills know about one another.

## Repository Validation

- [ ] Discover the installed `skill-creator` validator and run `quick_validate.py` for every changed skill directory.
- [ ] If that validator is unavailable, manually validate YAML parsing, naming, description length, and required file layout.
- [ ] Run the installed `plugin-creator` validator for every affected plugin directory.
- [ ] Run `claude plugin validate . --strict` when a Claude marketplace exists.
- [ ] Parse both marketplace catalogs and confirm identical plugin names and ordering.
- [ ] Confirm every catalog source and manifest skill path exists.
- [ ] Confirm each plugin description matches its Claude marketplace entry.
- [ ] Confirm the marketplace identifier has not changed unintentionally; display branding is not an identifier substitute.
- [ ] Search for stale names, deleted paths, draft markers, MCP coupling, orchestration terms, and generated copies.
- [ ] Apply repository line-count targets as a maintenance constraint, not as evidence of behavioral quality.

## Behavioral Review

- [ ] Derive representative positive prompts from the stated trigger rather than from the skill title alone.
- [ ] Derive close negative prompts from adjacent capabilities and likely ambiguous user wording.
- [ ] Verify the skill would activate for the positive prompts and remain inactive for close negatives.
- [ ] Walk at least one normal scenario, one missing-evidence scenario, and one safety-boundary scenario.
- [ ] For complex or high-risk changes, use fresh independent contexts when available and provide only the skill plus raw task artifacts.
- [ ] Do not reveal expected findings, intended fixes, or prior conclusions to an independent evaluator.
- [ ] Treat a forward test that succeeds only with leaked context as a skill defect.
- [ ] Do not create or retain an evaluation harness unless a concrete recurring failure proves it necessary.

## Evidence Rules

- [ ] Cite each finding to an exact file and the smallest useful line or section.
- [ ] Distinguish validator failures from manual concerns and speculative improvements.
- [ ] Reproduce critical failures before assigning a blocking severity.
- [ ] Do not report a preference as a correctness defect.
- [ ] Record commands executed, exit status, and material output without exposing secrets.
- [ ] Report coverage gaps when a required host or clean-context test cannot be run.

## Verdict

- `PASS` — structural, behavioral, and integration checks pass with no material concern.
- `PASS WITH CONCERNS` — publishable, but bounded non-blocking uncertainty remains.
- `FAIL` — a confirmed defect can cause wrong triggering, unsafe behavior, broken installation, or an invalid contract.
- `BLOCKED` — required evidence or tooling is unavailable and no credible fallback exists.

## Output Contract

Return:

1. Scope and changed surfaces.
2. Validator and behavioral evidence.
3. Findings ordered by severity, each with location, impact, evidence, and minimal correction.
4. Trigger boundary assessment.
5. Marketplace and host parity assessment.
6. Verdict.
7. Residual risks and checks not run.

Do not edit files, stage changes, publish packages, update marketplaces, or create GitHub state while reviewing.

Any diagnostic artifact must be temporary, outside canonical plugin directories, and disclosed in the residual-risk section.
