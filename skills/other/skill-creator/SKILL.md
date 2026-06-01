---
name: skill-creator
description: >
  · Create/review skills: frontmatter, triggers, overlaps, collection consistency, retrospective updates. Triggers: 'skill creator', 'new skill', 'skill audit', 'skill review', 'update skill library'.
license: MIT
compatibility: "Optional: git (for freshness and gitignore filtering)"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: high
  argument_hint: "<action> [skill-name]"
---

# Skill Creator: Meta Skill for Skill Lifecycle Management

Create, review, improve, audit, and maintain AI tool skills. Covers the full lifecycle from
initial draft through quality validation, cross-skill consistency checks, and trigger optimization.

This skill enforces the conventions established across the custom skill collection. It exists
because consistency is what makes skills predictable - a skill that follows the established
patterns activates reliably, reads clearly, and plays well with the rest of the collection.

## When to use

- Creating a new custom skill from scratch
- Reviewing or improving an existing skill
- Auditing the skill collection for consistency, overlaps, or contradictions
- Validating versions, security references, or CVE mentions in skills
- Optimizing a skill's description for better triggering accuracy
- Checking cross-skill references and "Related Skills" sections
- Troubleshooting why a skill isn't triggering or is triggering incorrectly

## When NOT to use

- Reviewing application code for correctness or bugs - use **code-review**
- Auditing code for AI-generated patterns or style issues - use **anti-slop**
- Running a full codebase audit across multiple dimensions - use **full-review**
- Creating inline prompts within application code - use **prompt-generator**
- Batch-improving a whole skill collection via evaluation loops - use **skill-refiner**
- Syncing or refreshing third-party skills from upstream - handle that directly in the repo workflow
- Updating project documentation after infrastructure changes - use **update-docs**
- Writing application code, even if the code is for a tool a skill might use

## AI Self-Check

Before returning any generated or modified skill, verify against this list:

- [ ] **Frontmatter complete**: `name`, `description`, `license`, `metadata.source` (`owner/repo` for published collections or `custom` for unpublished skills), `metadata.date_added` (ISO), `metadata.effort` (low/medium/high)
- [ ] **Name spec-valid**: lowercase alphanumeric + hyphens only, no leading/trailing/consecutive
  hyphens, no reserved words (`anthropic`, `claude`), matches directory name
- [ ] **No XML tags** in `name` or `description` fields (Anthropic platform restriction)
- [ ] **Description is trigger-optimized**: starts with action verbs, includes trigger keywords, mentions related contexts, stays near 200 chars for the collection (240 warn, 600 hard max in `validate-spec.sh`; platform truncation happens later)
- [ ] **Compatibility field present** (when skill requires specific tools/platforms): quotes values containing colons
- [ ] **Scope sections present**: "When to use" with concrete scenarios, "When NOT to use"
  cross-referencing related skills by **bold** name (e.g., `use **skill-name**`)
- [ ] **Workflow section with numbered steps**: clear, sequential, actionable
- [ ] **Rules section at the end**: non-negotiable constraints in imperative form
- [ ] **Style compliant**: no banned words (per `CLAUDE.md`/`AGENTS.md`), ASCII by default
  except approved markers such as `· ` and output-contract box glyphs. No em-dashes, curly
  quotes, ligatures, or `--`; use `-`. Check SKILL.md and references for banned words
- [ ] **Target ~500 lines**: if over 500, extract to `references/` with clear pointers. Hard max 600
- [ ] **Reference files use `references/` relative paths**: not hardcoded or tool-specific paths
- [ ] **All references verified**: every tool, CLI flag, IaC resource, config snippet, and
  example command confirmed against actual docs, `--help` output, or registry - not assumed
  from training data. Specifically: tools exist and aren't deprecated/renamed, CLI flags are
  real (AI models invent plausible ones constantly), Terraform providers/resources match the
  registry, Ansible modules/params match `ansible-doc`, Helm values match upstream
  `values.yaml`, K8s fields match the target API version. When web access is unavailable,
  note unverified claims rather than blocking
- [ ] **Version numbers verified and dated**: searched the web for latest stable version of each
  tool, pinned with date (e.g., "v29.3.0 (March 2026)") so staleness is detectable
- [ ] **Cross-skill references are valid**: every mentioned skill name actually exists
- [ ] **AI-age awareness**: if the skill generates code, config, or structured files (including skill files), include an AI self-check section
- [ ] **Context budget justified**: every section earns its token cost (see `references/conventions.md`)
- [ ] **Forward-tested** (high-effort skills, when feasible): during review, a subagent used the skill on a realistic task without leaked context. This is a process check on the reviewer, not a content requirement on the skill - the skill does not need a "forward-test" section. The reviewer notes what was tested or skipped and why.

- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: new or edited skills do not steal triggers from better-matched existing skills
- [ ] **Spec claims verified**: frontmatter, metadata, and compatibility guidance match the current Agent Skills specification

## Performance

- Keep `SKILL.md` compact; move deep examples into references loaded on demand.
- Prefer precise triggers over broad keyword lists that cause unnecessary skill loading.
- Run lint/spec checks before prose polishing so structural failures surface early.

## Best Practices

- Write skills as operational instructions, not essays about a domain.
- Include clear When to use/When NOT to use routing and realistic AI self-checks.
- Keep public skills tool-agnostic unless a tool is intrinsic to the skill.
- Treat install/copy/link steps as environment-specific. If skills are sourced directly from a
  repo, edit and verify there instead of distributing to tool dirs unless asked.

## Workflow

Before entering any mode, detect the operating context. This skill works on individual skills
or collections, whether inside a skill collection repo, a user's own project, or standalone.

**Mode routing** - pick the mode that matches the user's signal. Retrospective-update
requests are explicit permission to edit the library, so do not stop at a report-only pass:

| User signal | Mode |
|---|---|
| "create a skill", "new skill for X", "turn this into a skill" | Mode 1 (Create) |
| "review my skill", "improve this skill", "is this skill good" | Mode 2 (Review) |
| "audit the collection", "check all skills", "health check skills" | Mode 3 (Audit) |
| "fix the description", "skill isn't triggering", "trigger overlap" | Mode 4 (Optimize) |
| "review the conversation", "update the skill library", "what did we learn" | Mode 5 (Retrospective Update) |

When the signal is ambiguous (e.g., "look at my skill"), ask before committing - Create and
Review diverge quickly and re-running wastes context. Modes can chain: Create -> Review,
Review -> Optimize, Audit -> per-skill Review for flagged items.
For explicit retrospective-update requests, act without asking for confirmation unless the only
possible update is destructive or would create a new class-level skill with uncertain scope.

1. **Find the collection root** (if one exists): check for a `skills/` directory (common
   convention) or any path the user specifies. Different harnesses store skills in different
   locations - if the default doesn't match, ask or accept a user-supplied path. If no
   collection is found, skip collection-wide checks (cross-references, trigger overlap, audit
   mode) and note what was skipped.
2. **Check git and create a run branch**: run `git rev-parse --git-dir`. If inside git,
   create `skill-creator/YYYY-MM-DD-HHMMSS` from current HEAD before checks or edits unless
   already on a task branch created for this run. Preserve dirty worktrees; branching is for
   isolation, not cleanup. Without git, state "branch unavailable" in the final report and
   fall back to file modification dates.
3. **Single skill vs collection**: Modes 1 (Create) and 2 (Review) work on individual skills
   with or without a collection - collection-dependent steps become best-effort. Mode 3
   (Audit) requires a collection. Mode 4 (Optimize) works standalone but benefits from
   collection context for overlap analysis.

### Mode 1: Create a New Skill

#### Step 1: Capture intent

Understand what the skill should do. Extract from conversation context:
- **Core task**: what should the skill enable?
- **Trigger scenarios**: what user phrases or contexts should activate it?
- **Output format**: what does success look like?
- **Related skills**: which existing skills overlap or complement this one?

If the user already described the workflow in the conversation (e.g., "turn what we just did into a
skill"), extract the steps, tools used, corrections made, and patterns observed.

#### Step 2: Research the domain

Before drafting, gather context:
1. **Check existing skills** for overlap (if a collection is available) - read the "When to use"
   / "When NOT to use" of potentially related skills. Don't create a skill that duplicates
   existing coverage.
2. **Verify tools exist** - for every tool, library, CLI, or platform the skill references,
   confirm it exists, is not deprecated or renamed, and is actively maintained. Search the web
   or check the project's GitHub/registry page. AI models hallucinate tool names, flag names,
   and API endpoints - treat every claim as unverified until checked. If a tool was replaced
   (e.g., CDKTF is deprecated in favor of native HCL, Ingress is frozen with new features
   going to Gateway API), reference the current recommended approach.
3. **Check versions** - search for the latest stable release of every tool mentioned. Don't
   guess or rely on training data - versions go stale fast. Pin them with dates so staleness
   is detectable later (e.g., "Docker Engine 29.3.0 (March 2026)").
4. **Check security** - search for recent CVEs, supply chain incidents, or known vulnerabilities
   relevant to the domain. The custom skill collection tracks these actively - verify current
   advisories rather than relying on specific CVE numbers from training data.
5. **Check compliance** - if the domain touches infrastructure, containers, CI/CD, auth, or data
   handling, consider PCI-DSS 4.0 relevance. Many users work in regulated environments or run
   self-hosted infrastructure where compliance matters.

#### Step 3: Draft the skill

Follow the structural pattern for the skill's effort tier in `references/conventions.md` (Section 3).
Key elements every custom skill needs:

- **Frontmatter**: `name`, `description`, `license`, `metadata` block (see conventions Section 2)
- **"When to use" / "When NOT to use"**: concrete scenarios, cross-reference adjacent skills
- **Workflow**: numbered steps, sequential, actionable
- **Rules**: non-negotiable constraints at the end, imperative form
- **AI Self-Check**: required when the skill generates code, config, or structured files
- **Reference Files / Related Skills**: when applicable

For tool/platform skills, include a **Target versions** block with pinned versions and dates.

**Writing guidelines:**
- Imperative form in instructions ("Check the config", not "You should check the config")
- Explain **why**, not just **what** - models generalize from motivation
- Don't use ALL CAPS for emphasis unless it's genuinely critical. Calm, direct instructions
  outperform shouting across most modern models.
- Include "What NOT to flag" or "What NOT to do" sections where false positives are likely
- Use tables for reference data, prose for workflows, checklists for validation
- Consider headless execution: skills may run in non-interactive contexts (Claude Code `--bare`,
  Cursor Automations, Codex `exec`). Avoid blocking on user confirmation in steps that could
  run unattended - provide sensible defaults or document assumptions instead

#### Step 4: Validate the draft

Run through the AI Self-Check above. Then:

1. **Cross-reference check**: grep the skill collection for every skill name mentioned in the draft.
   Verify they exist and the characterization is accurate.
2. **Trigger overlap check**: compare the description against all other skill descriptions. Flag
   any that share >50% of trigger keywords.
3. **Convention check**: compare frontmatter, structure, and style against 2-3 existing custom
   skills in the same `effort` tier.
4. **Script-runner reality check**: if the collection uses helper scripts like `lint-skills.sh`
   or `validate-spec.sh`, verify their expected input shape before trusting the result. Some
   collections expect a parent directory containing many skill subdirectories, not a direct path
   to one skill. For single-skill validation, stage the skill inside a temporary parent such as
   `<tmp>/skills/<skill-name>/SKILL.md` and run the scripts against `<tmp>/skills`.

#### Step 5: Write the files

- Write `SKILL.md` to the appropriate location: `<collection-root>/<skill-name>/SKILL.md` if
  inside a collection, or the user's specified path for standalone skills
- Write reference files (if any) to `<skill-dir>/references/`
- If a collection inventory exists, update it and re-run cross-reference checks
- If `skill_manage` cannot modify the target because the skill lives in an external repo or
  non-managed directory, fall back to direct file edits with `patch` or `write_file` on the
  actual repo paths. Do not stop at the tool limitation if the files are writable and the user
  asked for the change in-place.

#### Step 6: Forward-test

Forward-testing has a subagent use the skill on realistic tasks without seeing your diagnosis.
Use it for high-effort skills and for medium-effort skills with multi-step or scripted workflows.
Skip it for low-effort wrappers, unavailable subagents, production-only access, long-running
infra, missing credentials, or explicit user opt-out; note the skip reason.

1. Pick 2-3 realistic tasks, including one edge case.
2. Launch with a real-user prompt and raw artifacts only.
3. Check whether the agent followed the workflow, missed steps, or hallucinated.
4. Clean up artifacts between iterations.

If forward-testing only succeeds with leaked context, tighten the skill instead of weakening
the test.

### Mode 2: Review / Improve an Existing Skill

#### Step 1: Read the skill thoroughly

Read the SKILL.md and all reference files. No skipping - the whole point is catching issues.

#### Step 2: Run the quality checks

**Structural checks:**
- Frontmatter completeness (name, description, license, metadata.source, metadata.date_added, metadata.effort)
- Section presence (When to use, When NOT to use, Workflow, Rules)
- AI Self-Check section (required for skills that generate code/config)
- Reference file paths resolve (check `references/` directory)
- Related Skills section present and accurate (when the skill interacts with other skills)
- Target ~500 lines (SKILL.md body), hard max 600

**Content checks:**
- Tools exist? Every tool, CLI, library, or platform named in the skill must be verified as
  real, not deprecated, and not renamed. Search the web or check the project's GitHub/registry.
  AI hallucinates tool names, CLI flags, and API endpoints constantly - treat every reference
  as unverified until confirmed. If a tool was replaced, the skill should reference the
  replacement (e.g., CDKTF deprecated in favor of native HCL, Ingress frozen with Gateway API
  as the recommended path forward, lazy_static superseded by std::sync::LazyLock).
- CLI flags and IaC resources real? Verify flags/subcommands against actual `--help` or docs.
  For Terraform: confirm provider names and resource type arguments against the registry. For
  Ansible: confirm module names and parameters against `ansible-doc` or Galaxy. For Helm:
  confirm chart values against upstream `values.yaml`. For K8s: confirm API fields against
  the target API version. AI invents plausible-sounding arguments for all of these.
- Version numbers current? Search the web for latest stable versions of tools that appear in
  normative claims (pinned versions, "Target versions" blocks, compatibility fields). Don't
  verify every passing mention - focus on versions that drive behavior or could mislead.
- Security references current? Check for new CVEs since the skill's `date_added`.
- Cross-skill references valid (if a collection is available)? Every skill name mentioned must
  exist as a published (non-gitignored) skill in the collection. For standalone skills,
  note unverifiable references instead of failing them.
- "When NOT to use" complete? Should reference all skills with overlapping trigger space.

**AI-age checks:**
- Does the skill generate code, config, structured output, or orchestrate other skills? If yes,
  does it have an AI Self-Check section? This is the #1 miss across skill collections -
  skills that produce output need a pre-flight checklist even if they're "just" orchestrators.
- Does the AI Self-Check cover the domain's common AI mistakes? (e.g., unpinned versions,
  missing security contexts, over-abstraction, hallucinated CLI flags)
- Are there patterns that would produce AI slop? (excessive MUSTs, over-defensive instructions,
  generic naming in examples)

**Compliance checks** (for infrastructure skills):
- PCI-DSS 4.0 mapping present where applicable?
- All future-dated requirements (mandatory since March 31, 2025) reflected?
- No hardcoded secrets in examples?

**Script-runner reality check:** verify helper script input shape. If a single-skill run reports zero skills or odd output, re-run against the collection root and filter for the target.

#### Step 3: Report findings

Use severity ratings:
- **P0**: wrong information, security risk, broken cross-references, or harmful generated instructions
- **P1**: stale versions, missing required sections, trigger overlap unhandled, or invalid output contracts
- **P2**: incomplete verification, weak behavioral coverage, or ambiguous workflow ordering
- **P3**: style inconsistency, missing "Related Skills", or wording that could be clearer
- **info**: confirmed strengths or scoped notes; note skipped checks in the report's skipped-checks field

#### Step 4: Confirm scope

Present findings to the user and wait for confirmation before editing. The user may want a
report only, or may want to fix a subset. In headless mode (no interactive user), report
findings and stop unless the original user request explicitly authorized edits. Programmatic
callers must pass that authorization through or stop after reporting findings.

#### Step 5: Apply fixes

Edit the skill files to address confirmed findings. For version updates, always search the web
first - don't guess. Do not modify `date_added` (it records when the skill was created, used
for historical tracking). If the skill needs a freshness marker, the `date_added` field serves
that purpose for the initial creation; substantial refreshes are tracked via git history.

#### Step 6: Forward-test

After substantial changes, forward-test the skill (see Mode 1, Step 6). Required for
high-effort skills after workflow restructuring, reordered steps, or new references.
Optional for narrow edits like version refreshes, wording cleanup, or metadata-only fixes.
Especially valuable when:
- The workflow was restructured or steps were reordered
- New reference files were added and need discovery testing
- Trigger description was rewritten (test activation, not just content)

### Mode 3: Audit the Skill Collection

Run a health check across all skills. Useful periodically or after adding/removing skills.

#### Step 1: Inventory

```bash
# Detect collection root - adapt to your layout
SKILL_ROOT="${SKILL_ROOT:-skills}"
[[ -d "$SKILL_ROOT" ]] || { echo "No skill collection at $SKILL_ROOT"; exit 1; }

# Check git availability for gitignore filtering and freshness
IN_GIT=false
git -C "$SKILL_ROOT" rev-parse --git-dir &>/dev/null && IN_GIT=true

for skill in "$SKILL_ROOT"/*/SKILL.md; do
  dir=$(dirname "$skill")
  name=$(basename "$dir")
  [[ "$name" == ".backups" || "$name" == ".cook" ]] && continue  # tooling dirs, not skills
  $IN_GIT && git -C "$dir" check-ignore -q . 2>/dev/null && continue
  source=$(grep -m1 '[[:space:]]source:' "$skill" 2>/dev/null | sed 's/.*source: *//' || echo "unknown")
  date=$(grep -m1 '[[:space:]]date_added:' "$skill" 2>/dev/null | sed 's/.*date_added: *"//' | sed 's/"//' || echo "unknown")
  effort=$(grep -m1 '[[:space:]]effort:' "$skill" 2>/dev/null | sed 's/.*effort: *//' || echo "missing")
  if $IN_GIT; then
    last_mod=$(git -C "$SKILL_ROOT" log -1 --format=%cd --date=short - "$name" 2>/dev/null || echo "unknown")
  else
    # Portable: GNU stat then BSD stat; GNU date then BSD date
    mtime=$(stat -c %Y "$skill" 2>/dev/null || stat -f %m "$skill" 2>/dev/null || echo 0)
    last_mod=$(date -d "@$mtime" +%Y-%m-%d 2>/dev/null || date -r "$mtime" +%Y-%m-%d 2>/dev/null || echo "unknown")
  fi
  printf "%-25s %-10s %-12s %-12s %s\n" "$name" "$source" "$date" "$last_mod" "$effort"
done
```

#### Step 2: Cross-reference matrix

For each skill, check:
1. Every skill name mentioned in "When NOT to use" exists as a published (non-gitignored) skill
2. Every skill name mentioned in "Related Skills" exists as a published (non-gitignored) skill
3. Every declared reference file path has a corresponding file
4. Installer, publish, or registry files list the published skills correctly
5. Lint scripts, CI checks, and count tooling exclude gitignored (private) skills -
   tools that iterate `skills/*/` directly will overcount unless they filter with
   `git check-ignore`

#### Step 3: Trigger overlap analysis

Compare all skill descriptions pairwise. Flag pairs that share significant trigger keywords
without mutual disambiguation (no "When NOT to use" cross-reference).

#### Step 4: Freshness sweep

Flag skills where the last modification (per git history, or file mtime if git is unavailable)
is >30 days old AND the skill covers fast-moving domains:

**Fast-moving** (>30 days = stale risk): docker, kubernetes, ci-cd, terraform, ansible,
databases, git, security-audit, code-review (AI-age patterns section), mcp, networking, arch-btw

**Slow-moving** (>30 days = probably fine): firewall-appliance, command-prompt, prompt-generator,
update-docs, skill-creator, full-review, anti-slop, lockpick

If the collection's conventions change significantly, temporarily reclassify skill-creator
as fast-moving until the conventions stabilize.

For each stale high-effort skill, search the web for:
- New major/minor releases of referenced tools
- New CVEs affecting referenced tools
- Deprecated or renamed tools/features since the skill was written
- New supply chain incidents (these move the fastest - Trivy was 6 days old when we caught it)

#### Step 5: Report

Present findings grouped by severity. Include actionable fixes for each finding.

### Mode 5: Retrospective Update

When the user asks to review a completed conversation and update the skill library, capture
reusable class-level learning, not a session log. Patch a loaded or umbrella skill for
reusable workflow, routing, preference, or pitfall changes; create a new skill only when no
class-level fit exists. In the public skills repo, read gitignored instruction files such as
`AGENTS.md`, but do not force-add them; stage only intended public skill paths and validate.

### Mode 4: Optimize Skill Description

The `description` field in frontmatter is the primary triggering mechanism. Optimize it for
accurate activation.

#### Step 1: Analyze current triggers

Read the skill's description and identify:
- Primary trigger keywords
- Secondary trigger contexts
- Potential false-positive triggers (keywords shared with other skills)
- Missing triggers (scenarios where the skill should activate but the description doesn't cover)

#### Step 2: Compare against the collection

If a collection is available, check which other skills share trigger keywords. Ensure the
description differentiates clearly. For standalone skills, skip this step.

#### Step 3: Rewrite the description

Follow these patterns from high-performing custom skill descriptions:
- **Start with action verbs**: "Use when writing, reviewing, or architecting..."
- **Include specific trigger keywords**: list them inline, e.g., "Triggers: 'keyword1', 'keyword2'"
- **Mention adjacent skills to avoid**: "Not for X (use Y instead)"
- **Be slightly pushy**: many tools undertrigger skills by default. Include edge cases.
- **Stay near 200 characters**: the collection warns above 240 and errors above 600. Codex loads every skill description at startup, so concise descriptions prevent startup truncation.
- **Treat 1024 as the platform ceiling, not the collection target**: truncation happens there, but the repo convention is stricter

#### Step 4: Validate

After rewriting, list 5 user prompts that should trigger the skill and 5 that shouldn't. For
each, state whether the rewritten description would route correctly and why. This is a heuristic
check - actual routing depends on the harness's skill-matching logic, which varies by tool.
The goal is catching obvious gaps and false-positive magnets, not deterministic validation.

#### Step 5: Apply

Edit the skill's frontmatter with the rewritten description. If the skill is part of a
collection, run Mode 2 Step 2 (quality checks) to verify no regressions were introduced.

## Run Report

End every run with a human-readable report, even for report-only checks. Include branch, mode,
scope, score or "not scored - report only", changed files, finding counts, verification results,
skipped checks, and recommended next action.

For edited skills, report before/after checklist pass rate and behavioral or forward-test scores
plus keep/reject decisions. For audit-only runs, report structural gate and finding counts
instead of inventing a composite.

## Reference Files

- `references/conventions.md` - the complete convention guide: frontmatter fields, structural
  patterns by effort tier, style rules (ASCII, banned words), reference file organization,
  cross-skill patterns, AI Self-Check patterns, and a snapshot inventory of the upstream
  collection (useful as a reference, not an authoritative list for other repos)

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** SKILL-CREATOR
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content (e.g., Mode 2 review or Mode 3 audit), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/skill-creator/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content** (e.g., Mode 1 create), respond freely without the contract; the existing `## Run Report` guidance applies to that build path.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **anti-slop** - the code quality audit skill. When reviewing a skill's example code or
  reference patterns, anti-slop patterns apply (comment noise, over-abstraction, stale idioms).
- **full-review** - orchestrates four parallel audits. This skill audits the skill collection
  itself, not application code.
- **prompt-generator** - structures prompts for LLM consumption. Skills ARE prompts, but
  prompt-generator targets one-off prompts saved to `docs/local/prompts/`, not reusable skill files.
- **code-review** - reviews application code for correctness. This skill reviews skill files
  for convention compliance, not code correctness.

## Rules

1. **Read before edit.** Always read a skill's SKILL.md and reference files before modifying.
2. **Conventions are non-negotiable.** Custom skills need `metadata.source`, `date_added`,
   `effort`, "When to use", "When NOT to use", Workflow, and Rules sections.
3. **Verify everything, assume nothing.** Confirm tools, versions, flags, APIs, and behavior via
   source docs, `--help`, registries, or explicit "unverified" notes. Do not guess.
4. **Prefer dedicated skill workflows over generic helpers.**
5. **Update the inventory.** After creating, removing, or renaming a skill, update published
   inventories and verify counts from live public skills.
6. **No AI slop in skills.** Avoid comment noise, over-abstraction, ALL CAPS theater, and
   "just in case" instructions.
7. **ASCII by default.** Keep skill prose ASCII except collection-approved markers such as the
   public-description `· ` prefix and shared output-contract box glyphs. No em dashes, curly
   quotes, ligatures, or `--` dash substitutes. Prose only: never rewrite `--` inside code or
   fenced blocks - there it is real syntax (SQL comments, CLI `--` separators) and must stay.
8. **Run the AI Self-Check.** Every generated or modified skill gets checked before return.
9. **Branch every run.** In git-backed collections, create or record a run branch before checks.
10. **Report every run.** Finish with the Run Report format and score before/after or "not scored."
    Do not substitute lint/spec status for behavioral scoring.
