---
name: deep-audit
description: >
  · Run 5-wave repo audits, persist findings, and generate phased tasks. Triggers: 'deep audit', 'full audit', 'comprehensive review', 'audit report', 'mega review', 'deep review'. Not for quick sweeps (use full-review).
license: MIT
compatibility: "Requires iuliandita/skills collection installed. Subagent support strongly recommended. Optional: a brainstorming or ideation skill in the host harness (matched by name pattern) for large-audit planning handoff."
metadata:
  source: iuliandita/skills
  date_added: "2026-04-14"
  effort: high
  argument_hint: "[scope]"
---

# Deep Audit: Wave-Based Repo Orchestrator

Run up to 29 audit agents against a repo in 5 sequential waves. This is the broadest application-repo dispatch plan (4 Wave 2 + up to 20 conditional Wave 3 lenses + 2 Wave 4 + 3 Wave 5), not the total skill count. Wave 1 detects the tech stack, Waves 2-5 dispatch only matching audit skills, and each wave reports before the next begins.

The five waves are: Reconnaissance; Code Quality (code-review, anti-slop, anti-ai-prose,
code-slimming); Domain-Specific (detected skills only); Security (security-audit then zero-day); and Docs & Hygiene (update-docs, roadmap, git).

After the waves, Steps 7-9 persist findings to `docs/local/audits/DEEP-AUDIT.md`, write `DEEP-AUDIT-TASKS.md`, and route SMALL audits to the task list or LARGE audits to a brainstorming skill or generated plans under `docs/local/specs/` and `docs/local/plans/`.

For a quick 4-skill sweep, use **full-review** instead.

## When to use

- Major pre-release quality gate where you want every applicable audit lens
- First audit of an unfamiliar codebase - understand what's there and what needs fixing
- Periodic deep health check on a repo you maintain
- Onboarding to a new project - the wave reports build a mental model fast

## When NOT to use

- Quick quality check on a PR or recent changes - use **full-review** (4 skills, parallel)
- Single-dimension audit (e.g., only security or only code quality) - use the individual skill directly (**security-audit**, **code-review**, etc.)
- Auditing the skill collection itself - use **skill-creator** (Mode 3)
- Offensive security engagement or CTF - use **lockpick** directly
- Live-system OS administration (running `pacman`/`apt`/`dnf`, fixing a NixOS rebuild, configuring SELinux on a host, debugging an OPNsense appliance) - use the matching distro/appliance skill directly (**arch-btw**, **debian-ubuntu**, **rhel-fedora**, **nixos-btw**, **firewall-appliance**). Repo-level audit of OS-related files (PKGBUILDs, `debian/`, `*.spec`, `flake.nix`, `pf.conf`, etc.) belongs in Wave 3 of this skill

## AI Self-Check

Run after Step 9 completes, before concluding the session. Checks cover the full
workflow (waves + persistence + routing), not just the wave dispatch phase.

- [ ] All agents dispatched as `general-purpose` type (not `feature-dev:*`, `code-simplifier:*`, or other restricted types - these lack Skill tool access)
- [ ] Each agent invoked its assigned custom skill via the Skill tool as its first action
- [ ] Recon summary (Wave 1) was presented to the user before Wave 2 agents were dispatched
- [ ] Wave 2 (code quality) ran all 4 skills regardless of repo type
- [ ] Wave 3 (domain) ran only skills whose detection patterns matched - no false activations
- [ ] Wave 3 skills that were skipped are listed by name in the recon summary
- [ ] Wave 4 ran sequentially: security-audit completed before zero-day started
- [ ] Zero-day agent received a summary of security-audit findings as input context
- [ ] Each wave's results were presented before the next wave started
- [ ] Each skill's native report format was preserved - no normalization across reports
- [ ] Failed or timed-out agents noted with reason, not silently dropped
- [ ] `docs/local/` added to `.gitignore` before writing any audit artifacts (verified with `git check-ignore`)
- [ ] `docs/local/audits/DEEP-AUDIT.md` written consolidating all wave findings in their native format
- [ ] Root-level `SECURITY-AUDIT.md` (if written by security-audit) relocated into `docs/local/audits/`
- [ ] `docs/local/audits/DEEP-AUDIT-TASKS.md` written with phased checklist (priority, effort, files, rationale per task)
- [ ] Task-list size assessed; routing decision announced (SMALL: direct action list, LARGE: brainstorming handoff or vanilla-harness plan generation)
- [ ] If LARGE and a brainstorming skill is available, user was told to invoke it manually (no silent auto-invocation)
- [ ] If LARGE and no brainstorming skill is available, execution-plan files written to `docs/local/specs/` and `docs/local/plans/` using the standard naming convention
- [ ] When user specified a scope, all agents received that scope constraint and detection was filtered to the scoped file tree
- [ ] Only skills from the iuliandita/skills collection were used - no built-in reviewers or platform audit modes
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Scope bounded**: audit waves match the repo type and user request, not every possible skill
- [ ] **Evidence retained**: findings cite files, commands, outputs, or source docs instead of impressions

## Performance

- Inventory first, then choose high-risk slices; avoid full exhaustive scans when focused evidence answers the question.
- Run cheap global searches before expensive test suites or dynamic analysis.
- Batch findings by subsystem and severity so review effort scales with risk.

## Best Practices

- State residual risk and skipped areas explicitly.
- Separate confirmed findings from hypotheses and follow-up tasks.
- Do not mutate the repo during an audit unless the user requested fixes.

## Workflow

### Step 0: Preflight

Gather context. Run in parallel (guard each with `; true`):

1. **Repo state**: `git rev-parse --show-toplevel` and `git rev-parse --short HEAD`
2. **Branch**: `git branch --show-current`
3. **File count**: `git ls-files | wc -l`

**If not a git repo**: stop. Tell the user: "deep-audit requires a git repository - the wave agents use git context for file discovery, diff scope, and commit anchoring. Initialize a repo with `git init` and commit the files, then re-run."

Record preflight values. Default `{scope}` to "full codebase" unless the user specifies
a narrower target.

### Step 1: Reconnaissance (Wave 1)

Detect which Wave 3 skills apply by scanning for file patterns. Use the detection table
and script in `references/detection-patterns.md`.

Run the detection script from the repo root. It outputs matched skill names, one per line.
If the user specified a scope, pass it as the script's first argument to filter detection
to that subtree (`git ls-files -- path/to/scope` instead of the full repo).

After detection, present the recon summary before proceeding. Compute
`{unmatched_skills}` as the 20 Wave 3 candidates minus the matched set.
Compute `{count}` by summing: 4 (Wave 2) + matched Wave 3 skills + 2 (Wave 4) +
3 (Wave 5). Example: if 6 Wave 3 skills match, count = 4 + 6 + 2 + 3 = 15. If the matched Wave 3 set is too broad for the user's goal, recommend a scoped deep-audit or **full-review** instead of pretending every lens is equally valuable.

In scoped mode, separate Wave 3 matches into two lines: skills matched by files
within the scoped subtree, and skills matched only by repo-root manifests
(potential false activations from workspace-root deps). Dispatch both sets - the
invoked skill will report zero findings if its domain isn't actually in scope.
The `[root-manifest]` separation is for user transparency, not gating.

If the user stated a priority (e.g., "security is top priority"), acknowledge it
in the recon summary: "Security is prioritized - it runs in Wave 4 as designed;
wave order is fixed because earlier waves feed context into security analysis."
Do not reorder waves.

```markdown
## Wave 1: Reconnaissance

Repo: {repo_name} @ {short_sha} ({branch})
Files: {file_count}
Scope: {scope}
Languages: {detected}

Skills that will run:
  Wave 2 (always): code-review, anti-slop, anti-ai-prose, code-slimming
  Wave 3 (detected): {scoped_matched_skills}
  Wave 3 (root-manifest only): {root_manifest_only_skills}    # scoped mode only; omit line if empty
  Wave 3 (skipped): {unmatched_skills}
  Wave 4 (always): security-audit, zero-day
  Wave 5 (always): update-docs, roadmap, git

Total agents: {count}
```

Concrete example for a Node+Postgres+Docker+K8s repo with i18n, frontend code, and GitHub Actions (9 Wave 3 skills matched out of 20):

```
Repo: myorg/api @ a3f91c2 (main)  |  Files: 412  |  Scope: full codebase
Languages: TypeScript, SQL, YAML

Wave 2 (always): code-review, anti-slop, anti-ai-prose, code-slimming
Wave 3 (detected): testing, command-prompt, databases, backend-api, frontend-design, localize, docker, kubernetes, ci-cd
Wave 3 (skipped): terraform, ansible, networking, ai-ml, mcp, arch-btw, debian-ubuntu, rhel-fedora, nixos-btw, firewall-appliance, virtualization
Wave 4 (always): security-audit, zero-day
Wave 5 (always): update-docs, roadmap, git

Total agents: 4 + 9 + 2 + 3 = 18
```

### Step 2: Code Quality (Wave 2)

Dispatch 4 agents in parallel. All four run on every repo.

**Agent type (critical for all waves):** every agent MUST be dispatched as `general-purpose`
(or equivalent full-access type). Do NOT use `feature-dev:*`, `code-simplifier:*`, or other
restricted agent types - they lack Skill tool access and cannot invoke custom skills. The
agent type controls tool access, not the audit topic.

**Context block** (passed to every agent in every wave - substitute all `{placeholders}`
with actual preflight values before dispatching):

```
Context:
- Repo: {repo_root}
- Commit: {short_sha}
- Branch: {branch}
- Languages: {detected_languages}
- File count: {file_count}
- Scope: {scope}
- Audit: deep-audit wave {N}
```

Replace `{N}` with the current wave number (2, 3, 4, or 5).

**Agents:**

| # | Skill | Prompt |
|---|-------|--------|
| 1 | `code-review` | Invoke the `code-review` skill via the Skill tool. Run a full code review on the codebase. Scope: {scope}. Return the complete report. |
| 2 | `anti-slop` | Invoke the `anti-slop` skill via the Skill tool. Audit the codebase for machine-generated patterns, over-abstraction, and code quality issues. Scope: {scope}. Return the complete report. |
| 3 | `anti-ai-prose` | Invoke the `anti-ai-prose` skill via the Skill tool. Audit all prose (docs, README, comments, docstrings, commit messages) for AI tells. Scope: {scope}. Return the complete report. |
| 4 | `code-slimming` | Invoke the `code-slimming` skill via the Skill tool. Audit the codebase for behavior-preserving code slimming, deduplication, and centralization opportunities. Scope: {scope}. Return the complete report. |

Present Wave 2 results under:

```markdown
## Wave 2: Code Quality

### Code Review
{agent 1 report verbatim}

### Slop Check
{agent 2 report verbatim}

### Prose Check
{agent 3 report verbatim}

### Slimming Check
{agent 4 report verbatim}
```

### Step 3: Domain-Specific (Wave 3)

Dispatch only the skills whose detection patterns matched in Wave 1. All matched skills
run in parallel.

**Generic prompt template** (used for most skills):

```
{context_block}

Invoke the `{skill_name}` skill via the Skill tool, then audit the codebase.
Scope: {scope}. Return the complete report.
```

**Skill-specific overrides** (use instead of the generic prompt):

| Skill | Override |
|-------|---------|
| `testing` | Audit test quality, coverage gaps, flaky test patterns, and missing test scenarios. Do not write new tests - report only. |
| `command-prompt` | Audit shell scripts, dotfile config, and .env patterns for correctness, portability, and security. |
| `frontend-design` | Audit frontend UI/UX implementation, visual hierarchy, accessibility, responsive behavior, framework drift, and AI design tells. Do not redesign or edit - report only. |
| `localize` | Audit i18n completeness. Find hardcoded user-facing strings, validate locale catalogs, check for missing translations. |
| `ci-cd` | Audit pipeline config for security (SHA pinning, secret exposure), efficiency, and correctness. |

All other skills use the generic prompt.

Present results:

```markdown
## Wave 3: Domain-Specific [{N} of 20 skills matched]

### {Skill Display Name}
{report verbatim}
...
```

If zero skills matched, skip Wave 3:
"Wave 3: skipped - no domain-specific patterns detected."

### Step 4: Security (Wave 4)

Run sequentially. Security-audit first, zero-day second.

**Agent 1: Security Audit**

```
{context_block}

Invoke the `security-audit` skill via the Skill tool. Run a full security audit.
Scope: {scope}. Return the complete report including SECURITY-AUDIT.md content.
```

Wait for Agent 1 to complete. Extract the top findings (up to 10, one line each,
highest severity first) for Agent 2's context. Include: severity, affected file/area,
and a one-sentence description. Do not pass the full verbatim report. If
security-audit returned zero findings, pass the string "security-audit returned
zero findings - hunt broadly" so the zero-day agent has non-empty context.

**Agent 2: Zero-Day Hunt**

```
{context_block}

Invoke the `zero-day` skill via the Skill tool. Hunt for novel vulnerabilities
in the source code. Scope: {scope}.

Prior security-audit findings (for context, avoid duplicating these):
{security_audit_key_findings_summary}

Focus on what the standard audit missed: variant analysis on flagged patterns,
attack surface mapping, deeper inspection of auth/crypto/parsing/deserialization code.
Return the complete report.
```

Present results:

```markdown
## Wave 4: Security

### Security Audit
{agent 1 report verbatim}

### Zero-Day Hunt
{agent 2 report verbatim}
```

**SECURITY-AUDIT.md handling:** the `security-audit` skill writes its report to
`SECURITY-AUDIT.md` at the repo root by default. Step 7 relocates this file into
`docs/local/audits/SECURITY-AUDIT.md` (which is gitignored via the `docs/local/`
entry). Users do not need to add a separate gitignore rule for the root-level file.

### Step 5: Docs & Hygiene (Wave 5)

Dispatch three agents in parallel.

| # | Skill | Prompt |
|---|-------|--------|
| 1 | `update-docs` | Invoke the `update-docs` skill via the Skill tool. Run a read-only audit. Find stale docs, instruction-file bloat, broken links, companion-file drift. Do NOT make changes or commit anything. |
| 2 | `roadmap` | Invoke the `roadmap` skill via the Skill tool. Audit ROADMAP.md (or equivalent) for drift, stale items, shipped-but-unchecked features, and completeness. If no roadmap exists, note the gap. Do NOT create one. |
| 3 | `git` | Invoke the `git` skill via the Skill tool. Audit git configuration, hooks, branch hygiene, signing setup, and commit message conventions. Do NOT make changes. |

Present results:

```markdown
## Wave 5: Documentation & Hygiene

### Docs Sweep
{agent 1 report verbatim}

### Roadmap Check
{agent 2 report verbatim}

### Git Hygiene
{agent 3 report verbatim}
```

### Step 6: Final Summary

After Wave 5 - before the persistence work in Step 7 - present a brief
priority-ordered summary to the user:

```markdown

## Summary

**P0** (must fix):
- {highest severity findings across all waves}

**P1/P2** (should fix / nice to fix):
- {significant and lower-urgency findings}

**P3/info** (backlog / informational):
- {polish, stale docs, style, or informational findings}

Waves completed: {N}/5 | Skills run: {N}/{total_matched} | Failed: {N}
```

Priority order: security fixes > correctness bugs > test gaps > slop/prose cleanup >
code-slimming opportunities > domain-specific issues > doc updates > hygiene.

### Step 7: Persist DEEP-AUDIT.md

Consolidate every wave's findings into a single durable report at
`docs/local/audits/DEEP-AUDIT.md`. The terminal summary in Step 6 is ephemeral;
this file is the source of truth that Step 8 and downstream planning work from.

1. **Ensure `docs/local/` is gitignored.** Check `.gitignore` for an entry covering
   `docs/local/`. If missing, append exactly these two lines to the repo-root `.gitignore`:

   ```
   # Local audit/spec/plan scratchpad (deep-audit output, not tracked)
   docs/local/
   ```

   Then verify:

   ```bash
   git check-ignore -q docs/local/ && echo "gitignored" || echo "NOT gitignored"
   ```

   Do not write any audit artifact until this check passes. Contents include unredacted
   security findings.

2. **Create the target directory.** `mkdir -p docs/local/audits/`.

3. **Relocate any root-level `SECURITY-AUDIT.md`.** If the security-audit skill wrote
   `SECURITY-AUDIT.md` to the repo root (its default), move it into `docs/local/audits/`.
   Do not leave two copies.

4. **Write `docs/local/audits/DEEP-AUDIT.md`.** Follow the DEEP-AUDIT.md template in
   `references/report-templates.md` (metadata header, headline verdict, scorecard,
   per-wave sections preserving native format). Overwrite any prior file.

### Step 8: Generate DEEP-AUDIT-TASKS.md

Derive a phased, checkbox-tracked action list at `docs/local/audits/DEEP-AUDIT-TASKS.md`
from DEEP-AUDIT.md content. This is the artifact users tick off during execution.

Follow the task-list template in `references/report-templates.md`: task entry format,
priority markers (🔴🟡🔵), finding ID cross-references, the 12-phase ordering heuristic,
and the trailing effort-rollup / minimum-release-cut sections.

### Step 9: Route to planning

Assess the size and severity of `DEEP-AUDIT-TASKS.md` and announce the chosen path
before acting.

**SMALL** (all three must hold): `<=10 tasks` AND `<=2 phases` AND zero P0 findings.
- No execution plan needed.
- Present the final summary + path to `DEEP-AUDIT-TASKS.md`. Work can start directly
  from the checkboxes.
- Stop here.

**LARGE** (anything that fails the SMALL criteria - i.e., `>10 tasks`, OR `>2 phases`,
OR any P0 finding):
- An execution plan is warranted. Choose one of three strategies, in preference order:

  **9a. Brainstorming skill handoff (preferred when available).** Scan the harness's
  available-skills list (commonly surfaced in a session `<system-reminder>`, a skill menu,
  or `ls ~/.claude/skills/` / `ls ~/.codex/skills/` equivalents) for any skill whose name
  or description matches `*brainstorm*`, `*ideation*`, or `*explore*` (common examples:
  `superpowers:brainstorming`, `gsd-explore`, `brainstorm`). If found, announce:

  > LARGE audit ({N} tasks, {M} phases). Recommend invoking `{skill-name}` with
  > `docs/local/audits/DEEP-AUDIT-TASKS.md` as input to produce an execution master
  > plan in `docs/local/specs/` and per-phase plans in `docs/local/plans/`.

  Do not auto-invoke. Brainstorming skills are interactive and the user must drive.

  **9b. Vanilla harness fallback (when no brainstorming skill is available).** Generate
  the plan files directly from `DEEP-AUDIT-TASKS.md`. Follow the master-plan and
  per-phase templates in `references/report-templates.md`. Write:

  - `docs/local/specs/{YYYY-MM-DD}-audit-execution-master-plan.md`
  - `docs/local/plans/{YYYY-MM-DD}-audit-phase-{NN}-{slug}.md` per non-trivial phase
    (two-digit phase numbers)

  Announce the write, then proceed - this path is mechanical, not interactive.

  **9c. Stop in headless / non-interactive mode.** If the session cannot confirm user
  intent and no brainstorming skill is available, write the two audit files, announce
  the recommendation, and stop. The user will pick up in a follow-up session.

Never silently auto-invoke a skill. Never skip writing `DEEP-AUDIT.md` and
`DEEP-AUDIT-TASKS.md` just because a LARGE plan is being generated - those two files
are always produced first and are the input to any planning path.

### Step 10: Handle Failures

- Note which agent failed and why (timeout, skill not found, permission denied)
- Present everything that completed successfully
- Do not re-run failed agents unless asked
- If a skill is not installed, skip it and note the gap in the wave report header.
  Do not substitute with a manual review - the value of this audit is in the custom
  skills themselves

**If parallel execution is unavailable**: run agents sequentially within each wave. Keep
the wave order. Priority within a wave: security-related skills first, then by specificity
(more targeted before more general).

**If agent dispatch is unavailable**: run each skill sequentially in the main conversation,
one at a time. Present each result before invoking the next skill. This uses more context
but preserves the wave ordering.

## Reference Files

- `references/detection-patterns.md` - Wave 3 file-pattern table, runnable detection script, and edge cases. Read before Step 1.
- `references/report-templates.md` - templates for `DEEP-AUDIT.md`, `DEEP-AUDIT-TASKS.md`, and Step 9b plan files.
- `references/exclusions.md` - skills deliberately excluded from wave dispatch and why.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** DEEP-AUDIT
- **Deliverable bucket:** `audits`
- **Mode:** always-on. Every invocation emits the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table.
- **Deliverable path:** `docs/local/audits/DEEP-AUDIT.md` (consolidated findings) and `docs/local/audits/DEEP-AUDIT-TASKS.md` (phased task list). Step 9b also writes `docs/local/specs/` and `docs/local/plans/` files when a full execution plan is generated.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract).

## Related Skills

- **full-review** - the quick 4-skill version (code-review, anti-slop, security-audit, update-docs). Use when speed matters more than depth.
- **code-review**, **anti-slop**, **anti-ai-prose**, **code-slimming** - Wave 2 participants.
- **security-audit**, **zero-day** - Wave 4 participants.
- **update-docs**, **roadmap**, **git** - Wave 5 participants.
- **testing**, **command-prompt**, **databases**, **backend-api**, **frontend-design**, **localize**, **ai-ml**, **mcp**, **docker**, **kubernetes**, **terraform**, **ansible**, **ci-cd**, **networking**, **arch-btw**, **debian-ubuntu**, **rhel-fedora**, **nixos-btw**, **firewall-appliance**, **virtualization** - Wave 3 candidates (conditional).
- **skill-creator** - audits the skill collection. This skill audits application repos.

Read `references/exclusions.md` before changing Wave 3 routing.

## Rules

1. **General-purpose agents only.** Every subagent MUST be `general-purpose`. Restricted agent types cannot invoke custom skills via the Skill tool.
2. **Custom skills only.** Only invoke skills from the iuliandita/skills collection. No built-in reviewers, platform audit modes, or third-party skills. If a skill is unavailable, skip it rather than substituting a manual review.
3. **Wave order is sacred.** Execute waves 1-2-3-4-5 in sequence. Never reorder, skip, or merge waves. Within a wave, agents run in parallel (except Wave 4 which is sequential).
4. **Present before proceeding.** Each wave's results are shown to the user before the next wave starts. No buffering all results to the end.
5. **Detection gates Wave 3.** Only dispatch Wave 3 skills whose file patterns matched in the recon sweep. Do not run terraform on a repo with no .tf files.
6. **Security is sequential.** security-audit completes before zero-day starts. Zero-day receives security-audit findings as input context.
7. **Read-only audit, with explicit artifact exceptions.** No agent modifies source code, commits, or alters the repo's working tree. The only permitted writes are: (a) audit artifacts under `docs/local/audits/` (`DEEP-AUDIT.md`, `DEEP-AUDIT-TASKS.md`, relocated `SECURITY-AUDIT.md`), (b) Step 9b plan files under `docs/local/specs/` and `docs/local/plans/`, and (c) a one-line addition to `.gitignore` if `docs/local/` is not already covered.
8. **Preserve native formats.** Each skill produces its own report format. Do not normalize, merge, or editorialize across reports. Cross-wave synthesis is allowed only in three specific places: the Step 6 terminal summary, the headline verdict + scorecard of `DEEP-AUDIT.md`, and the phased ordering of `DEEP-AUDIT-TASKS.md`. Everywhere else, native format is preserved verbatim.
9. **Don't stack with full-review.** This skill supersedes full-review's coverage. If the user asked for deep-audit, do not also invoke full-review.
10. **Respect scope.** When the user specifies a scope, pass it to every agent and filter detection patterns to that scope's file tree.
11. **Always persist `DEEP-AUDIT.md` and `DEEP-AUDIT-TASKS.md`.** These two files are mandatory output of every run, regardless of audit size or whether an execution plan is generated. Write them under `docs/local/audits/`. Ensure `docs/local/` is in `.gitignore` first - these artifacts can contain sensitive security detail.
12. **Brainstorming handoff is a recommendation, not an auto-invocation.** If a brainstorming/ideation skill is present in the host harness, announce the recommended invocation and stop - the user drives that step. When no brainstorming skill exists, proceed directly to Step 9b plan-file generation (this is deterministic file writing, not skill invocation). Only in headless / non-interactive mode, when neither option is available, fall back to Step 9c (stop and let the user continue in a follow-up session).
13. **Don't hardcode a specific brainstorming skill.** The skill collection is tool-agnostic (Claude, Codex, Opencode, others). Match by pattern (`*brainstorm*`, `*ideation*`, `*explore*`) rather than by a single hardcoded name like `superpowers:brainstorming`.
