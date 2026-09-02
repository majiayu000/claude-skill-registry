---
name: agents-md
description: 'Use when setting up a repo for agents, adding AGENTS.md, auditing CLAUDE.md, scoring instructions, or pruning long/stale files via a three-check gate. Also handles lean pointer-only AGENTS.md under 100 lines. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Agents MD

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to set up a repo for agents, add AGENTS.md, audit CLAUDE.md, make a repo agent-friendly, score agent instructions, prune long/generic/stale instructions, or produce a lean pointer-only AGENTS.md |
| Authority | Reversible local write: audit and refactor AGENTS.md, CLAUDE.md, CLAUDE.local.md, and supporting instruction files; apply diffs only after user confirms. Roll back by restoring the pre-edit snapshot taken before any write |
| Side effect | Local write to agent instruction files in the repo; no remote, credential, paid, published, deployed, or VCS mutation |
| Done | Repo has working, scored, non-contradictory AGENTS.md and CLAUDE.md for Claude, Codex, and Cursor; every surviving line passes the three-check admission gate (non-discoverable, operationally significant, actionable); lean variants stay under 100 lines with pointer-only sections |

## Inputs

- Required: the repository root path to audit or set up.
- Optional: target tool set (defaults to Claude Code, Codex, and Cursor); audit mode (quick or full, defaults to quick); target grade (defaults to 10/12 for quick, A for full); target file path (defaults to root AGENTS.md, then CLAUDE.md if AGENTS.md absent); scope limit (root-only versus hierarchical); owner name for the lean commit attribution line.

## Procedure

AGENTS.md files are execution contracts, not knowledge bases. Every line must help an agent execute correctly with minimal context. AGENTS.md is temporary guidance, not permanent configuration: when a recurring issue has a fixable root cause in code or tooling (a lint rule, test, script, or structural change), prefer that fix and keep only the minimum instruction needed until the root cause is solved.

1. **Discover files and survey discoverability.** Find every agent instruction file in the repo:
   ```bash
   find . \( -name "AGENTS.md" -o -name "CLAUDE.md" -o -name "CLAUDE.local.md" \) 2>/dev/null | sort
   ```
   Also check `~/.claude/CLAUDE.md` (applies to every session). For monorepos, include workspace-level files. Audit each level independently: root holds universal rules, child files hold directory-specific rules. Then survey source files to learn what is already discoverable: README, PROJECT.md, cursor rules (`.cursor/rules/` or `.cursorrules`), Copilot instructions (`.github/copilot-instructions.md`), GEMINI.md, CI/workflow files, package manager config, CONTRIBUTING.md, and `docs/`. Record what an agent can infer from these alone — anything discoverable need not be restated.
   - Done when: every instruction file is listed and the discoverability survey records what an agent can learn without AGENTS.md.

2. **Choose a mode.**
   - No agent instructions, or targeting a tool the repo is not wired for → **Setup** (Step 3), then **Writing from scratch** (Step 6), then **Audit** (Step 4).
   - File exists and the question is quality → **Audit** (Step 4).
   - File exists and is bloated (root over ~150 lines), stale, scored below target, long/generic/stale, or agents repeat avoidable mistakes → **Refactor** (Step 5).
   - Repo has convention docs and user wants a lean pointer file → **Lean** (Step 6, lean variant).
   - Done when: exactly one mode is selected and the entry step is identified.

3. **Setup — decide which files exist and which tool reads each.**
   - `AGENTS.md` at the repo root is the source of truth. Claude Code, Codex, Cursor, Copilot, Gemini CLI, Aider, Windsurf, and Zed all read it natively. Every other agent file is a pointer or tool-specific supplement, never a second copy. Two copies of a rule drift silently because nothing in the codebase contradicts either one.
   - Claude Code: nothing beyond AGENTS.md. Add `CLAUDE.md -> AGENTS.md` as a symlink only when a tool in use reads solely `CLAUDE.md`; a symlink keeps one source of truth where a copy would drift. Use `.claude/settings.json` for hooks and `CLAUDE.local.md` (gitignored) for personal overrides.
   - Codex: nothing beyond AGENTS.md.
   - Cursor: AGENTS.md covers prose. Add `.cursor/rules/*.mdc` only for rules needing Cursor glob scoping. Frontmatter is required; `alwaysApply: true` with empty `globs` duplicates AGENTS.md.
   - Check `.gitignore`: if agent config is ignored, decide per file whether it is personal (leave ignored) or repo knowledge (commit it). Do not put shared knowledge under `.claude/` — that path reads as Claude-only and is commonly gitignored.
   - The import trap: `@import` is Claude Code only. Codex and Cursor ignore `@import` lines without warning, so a rule behind an import is absent from most sessions while the file looks correct. Anything every tool must obey goes inline in AGENTS.md. Reserve `@import` for depth only Claude Code needs, never for safety, data-loss, or format-contract rules. `@import` chains stop resolving at 5 hops; deeper content silently disappears. `@import` lines do not evaluate inside code spans or fenced blocks.
   - Enforcement that survives tool choice: prefer, in order, a linter or formatter rule, a git hook (lefthook, husky) that fires whichever agent made the edit, a CI check, then tool-native hooks (`.claude/settings.json`, Cursor `hooks.json`). Tool-native hooks are the last rung because they cover one tool only. Move a prose rule down to an exit code whenever the check is mechanical, and delete the prose once the gate exists.
   - Done when: the file-to-tool mapping is decided and every tool's read path is confirmed.

4. **Audit — score each root file independently.** Exclude N/A checks from the denominator.
   - **Quick** (default): 12 checks, target ≥ 10/12. Borderline (8–9) or fail (≤7) escalates to full.
     1. Core run/test/build/lint commands exist when applicable
     2. Commands appear runnable and match project scripts/tooling
     3. Setup/bootstrap requirements are documented
     4. At least one project-specific gotcha is documented
     5. Gotchas include corrective action (what to do instead)
     6. Conventions that change implementation choices are explicit
     7. Every line passes the litmus test: removing it would cause the agent to make mistakes
     8. Root file avoids framework doc dumps/templates
     9. Linked paths and commands are current (not stale/dead)
     10. Non-universal detail is linked out, and anything every tool must obey stays inline
     11. Rules are phrased as the outcome wanted, with absolutes reserved for safety, data loss, format contracts, and observed failures
     12. Nothing restates harness or model default behavior, and no rule conflicts with a parent file or an installed skill
   - Full: 49 checks across five categories, target ≥ 91% of applicable points (grade A). Use when the quick audit fails, the file gates a high-risk repo, or full scoring is requested.
     - A. Commands and execution readiness (12): working dev/test/build/lint/deploy/migrate commands; copy-paste ready with no placeholders; match package manager and scripts; required env bootstrap including secondary runtimes; where to run commands (root/workspace); targeted test command with quiet flags for iteration; no duplicate or conflicting command variants.
     - B. Gotchas and repeated mistakes (10): at least one high-frequency failure mode; project-specific not generic; corrective action included; trigger context (when the rule applies); captures issue from PR/review feedback; ordering/dependency gotchas where order matters; data/env gotchas where setup mistakes cause failures; no vague advice like "be careful"; separates universal from edge-case rules; removes gotchas that no longer happen.
     - C. Conventions and decision boundaries (11): conventions that materially change implementation choices; naming/path conventions when CI/tooling depends on them; test strategy conventions (unit/e2e boundaries); links out non-universal detail while keeping must-obey rules inline; marks scope boundaries (monorepo root vs workspace); no restatements of what the agent or harness already does; rules name the condition that triggers them; emphasis markers (IMPORTANT, NEVER, YOU MUST) used sparingly on critical rules agents skip; outcome phrasing with absolutes only where the harmful-precision test clears; no rule contradicts a parent file, installed skill, or another section with precedence stated where overlap is deliberate; exemplar file paths named instead of prose descriptions.
     - D. Signal-to-noise and bloat control (9): root concise for repo complexity (60–150 lines for active app repos); no full framework documentation pasted inline; no copy-pasted full templates; no exhaustive file tree or every-file inventory; no long architecture deep dives in root; links to detail files for non-universal guidance; no duplicate guidance across sections; no content auto-memory owns (user preferences, personal feedback, evolving project status); each section passes the litmus test.
     - E. Currency and validation (7): referenced file paths exist; referenced tools/dependencies still in use; commands have been run or limitations documented; removed references to deleted folders/APIs; version-sensitive guidance is date/version scoped; clear maintenance loop (how to keep the file current); CLAUDE.local.md used for personal/gitignored overrides not mixed into shared AGENTS.md.
   - Grade mapping (earned / applicable): A ≥ 91%, B 76–<91%, C 59–<76%, D 39–<59%, F <39%.
   - Automatic fail (grade F regardless of score): commands are mostly broken/stale; instructions are primarily generic advice or restatements of default agent behavior; file is dominated by copied docs/templates rather than executable guidance.
   - **Two tests that catch how a line fails** — apply during audit and refactor:
     - Dead weight: "Would removing this cause the agent to make a mistake?" If no, cut it; bloat makes agents ignore the rules that matter.
     - Harmful precision: "Is this wrong on any plausible task in this repo?" A prohibition wrong one task in ten is still obeyed on that task, and the agent cannot tell it is the exception. State the desired outcome and let the surrounding code pick the path. `NEVER write comments` becomes `match the comment density of the file you are editing`. Absolutes still earn their place for safety, data loss, format contracts, and rules agents have actually been observed to break.
   - Done when: every root file has a score, grade, and issue list with proposed diffs.

5. **Refactor — for bloated, stale, or low-signal files.** Bound scope before mutation: identify the target AGENTS.md path(s) — the root file and any module-local variants the user named. Do not create or edit a file outside this set.
   - Snapshot current line count before any edit.
   - Extract only what every task needs: run/test/build/lint commands, critical environment/setup requirements, high-frequency gotchas, conventions that change implementation choices. Everything else: link to a reference or delete.
   - Apply the **three-check admission gate** to each surviving line and each candidate line: (a) non-discoverable from repository files alone, (b) operationally significant — it changes commands, outcomes, or safety, (c) actionable — specific enough to execute. Omit anything that fails one check.
   - Delete first, add back only what earns its place. For every removed line, record one reason: `generic`, `duplicate`, `stale`, `moved` (to a reference), `reworded`, or `omitted` (unverifiable — cannot be grounded in a file actually read; never speculate or fabricate). This log makes the final report traceable, and `reworded` keeps the safety re-check from treating a rewritten rule as lost content.
   - Remove: full documentation and tutorial-style prose, long architecture explanations in root, exhaustive file maps, generic advice ("write clean code", "use best practices"), outdated commands and dead links, restatements of default agent behavior ("read before editing", "run the tests after changes", "use the todo tool", "don't commit unless asked"), facts auto-memory owns (user preferences, personal feedback, evolving project status), tech stack summaries, directory structure overviews, architecture descriptions agents can infer from code, generic best-practice advice not specific to this repo, rules already enforced by tooling (linters, typecheck, tests, CI), and mandatory boilerplate headers unless the repo explicitly requires one.
   - Write each retained entry as an imperative or prohibition paired with why the rule needs to be. Each fact appears once. Ground every statement in a file actually read; if uncertain, omit the claim rather than speculate. Admissible form: "Use pnpm; npm lockfiles break CI." Inadmissible form: "The repo uses pnpm."
   - Reword rather than remove: a blanket prohibition that some plausible task would want broken becomes the outcome it was protecting. Tag it `reworded`.
   - Rebuild root file in strict order: project one-liner, commands, gotchas (failure mode → fix), conventions and boundaries, links to deeper references.
   - Move non-universal detail to supporting files (`.agents/`, `docs/`, workspace-level AGENTS.md in monorepos), then link from root with `@import`. Guidance needed in fewer than ~30% of tasks moves out of root. For large repos, prefer hierarchical module-local AGENTS.md files near relevant modules instead of one monolithic root file.
   - Keep in root: copy-paste commands with the targeted quiet form of daily-run tests (`pnpm exec vitest run <file> --reporter=dot`), high-frequency failure modes with fixes, non-obvious conventions that change implementation choices, required environment/setup facts, and pointers to deeper docs on committed tool-neutral paths.
   - Done when: every surviving line passes the three-check gate, the deletion log accounts for every removed line, and the rebuilt file follows the strict order.

6. **Writing from scratch.** Gather real commands from the manifest (`package.json`, `Makefile`, CI config). Use this skeleton, filled with verified commands and known gotchas:
   ```markdown
   # <Project name>

   One-line description.

   ## Commands
   - `<dev command>`
   - `<test command>`
   - `<targeted test command, quiet flags included>`
   - `<build command>`
   - `<lint/typecheck command>`

   ## Gotchas
   - `<failure mode> -> <corrective action>`

   ## Conventions
   - `<project-specific convention that changes implementation choices>`

   ## References
   - @docs/architecture.md
   - @.claude/testing.md
   ```
   For monorepos, add a workspace map pointing to each workspace's own AGENTS.md. For multi-language monorepos, add per-language setup commands and cross-language boundary rules. Never ship a skeleton verbatim; a shipped placeholder is worse than no file. Prefer bullets over paragraphs. Keep root within 60–150 lines for typical active repos. 3–8 gotchas from real failures beat 20 hypothetical ones. When a convention has an exemplar in the repo, name the file path instead of describing the pattern in prose — code cannot be vague and cannot drift from itself.
   - Lean variant: when the repo already has convention docs (CONTRIBUTING.md, `docs/`, `.github/`), write pointer-only sections: `**Topic**: see <path-or-url>` — one pointer per line, never restate policy. Keep the total file at or under 100 lines; prefer bullet tables over prose. Add a commit attribution line at the bottom: `<!-- commit: <owner or "agent"> -->`. If no conventions are found, scaffold a minimal file with a placeholder attribution line and no convention sections; do not fabricate conventions.
   - Done when: the file is filled with verified commands and gotchas (or pointer-only sections in lean mode), no skeleton is shipped verbatim, and the line count is within bounds.

7. **Propose minimal diffs.** In priority order:
   1. Fix broken or stale commands; bugs, not style.
   2. Remove generic, duplicate, or obsolete guidance, restatements of what the harness already does, and facts auto-memory owns.
   3. Rewrite blanket prohibitions as the outcome they were protecting; keep the absolute only where the harmful-precision test clears it.
   4. Move non-universal detail behind `@import` or to child files.
   5. Add emphasis ("IMPORTANT:", "YOU MUST") only on critical rules agents skip.
   Show each change as a diff snippet with a one-line rationale. Apply only after the user confirms.
   - Done when: every proposed change is a diff snippet with a rationale, and the user has confirmed or rejected.

8. **Validate changes.**
   1. Smoke-run core commands (`dev`, `test`, `build`, `lint`/`typecheck`) where the environment allows; otherwise verify the script exists in the manifest and note the limitation. A passing quick score does not prove commands run; stale commands hide behind checklist passes.
   2. Check every linked and `@import`ed path resolves.
   3. Confirm no contradictory rules remain across levels (home, root, child) or against installed skills. Where overlap is deliberate, the file must state who wins, so the agent is told precedence instead of arbitrating it every task.
   4. Verify wiring by asking each tool to quote a rule back that appears nowhere else in the repo, so a correct answer cannot come from reading the code. If a tool cannot answer, its wiring is broken regardless of what the file says. The import trap makes a broken setup and a working one identical on disk.
   5. Issues found: revise, then validate again. Never proceed on "looks right".
   - Done when: commands are smoke-run or verified, all paths resolve, no contradictions remain, and each tool quotes a unique rule back.

9. **Apply and report.** Apply approved edits, re-score with the same checklist, report before/after scores and line counts. Per future PR, add at most one new gotcha, only if it prevented or fixed a real mistake. Prune stale instructions aggressively — the file shrinks over time as root causes get fixed in code or tooling.
   - Done when: edits are applied, before/after scores and line counts are reported, and the deletion log with reason tags is delivered.

### Operational traps

- `@import` lines do not evaluate inside code spans or fenced blocks: a real import wrapped in backticks silently never loads, while example imports inside fences are safe to show.
- `@import` reaches Claude Code only. Codex and Cursor ignore import lines without warning, so in a multi-tool repo an imported safety or format rule is absent from most sessions while the file still looks correct.
- `@import` chains stop resolving at 5 hops; deeper content silently disappears from context.
- Child-directory AGENTS.md files load on demand when the agent works in that subtree, not at session start. A universal rule placed only in a child is invisible to most tasks; promote it to root.
- Do not put project-specific commands in `~/.claude/CLAUDE.md`; it loads every session, so one repository's development command becomes noise or a wrong command everywhere else.
- Do not audit `CLAUDE.local.md` as strictly as AGENTS.md; it is gitignored personal config. Flag only broken commands and contradictions with the shared file.
- Do not strip emphasis markers (IMPORTANT, YOU MUST) during a density cut; they exist because plain phrasing was already ignored once.
- Content auto-memory owns (user preferences, personal feedback, evolving project status) collects in CLAUDE.md from old habits. It loads every session, is not repo knowledge, and drifts silently because nothing in the codebase contradicts it. Cut it to memory or CLAUDE.local.md.
- A rule duplicating harness behavior is not free: the agent reconciles it against what the harness already does before it can act, and pays that on every task. "Always read a file before editing it" is a whole reconciliation for zero behavior change.
- Do not rewrite a whole file when targeted diffs would pass; full rewrites destroy battle-tested wording and inflate review burden.

## Failure and recovery
- No agent instruction files found and user did not request setup: report the empty state and ask whether to proceed with setup. Do not create files without confirmation.
- Commands cannot be smoke-run (environment lacks the toolchain): verify the script exists in the manifest, note the limitation in the report, and mark the check as unverified rather than passing it.
- Contradictory rules found across levels: flag each contradiction, state which level should win, and propose a diff that resolves it. Do not apply until the user confirms the precedence decision.
- Quick audit fails or is borderline (8–9): escalate to the full 49-check audit. Report both scores.
- **Refactor removes a constraint that was actually a safety rule**: re-check the deletion log for anything tagged `generic` that was a safety, migration, release, or incident rule. Restore it immediately.
- Unverifiable claim: a candidate line cannot be grounded in a file actually read. Omit it; never speculate or fabricate. Record it in the omission list, not as passing.
- Stale but load-bearing: a line fails "accurate today" yet removing it would let agents repeat a known mistake. Flag it to the user as needing a root-cause fix in code or tooling, keep the minimum instruction, and do not silently delete.
- Scope drift: the user did not name a module-local variant. Do not create or edit it; stop and ask rather than widen scope.
- **Empty conventions** (lean mode): scaffold a minimal file with a placeholder attribution line `<!-- commit: agent -->` and no convention sections; do not fabricate conventions.
- Partial result: if the audit completes but validation fails, deliver the audit report with the failing validation checks marked. Do not apply any edits. If some lines cannot be verified, deliver the verified subset and list the unverified candidates as omitted, never as passing.
- Rollback: before any write, snapshot the current file. If an applied edit introduces a regression, restore from the snapshot or version control. Never apply edits without the pre-edit snapshot.
- Blocked result: if the user does not confirm the proposed diffs, deliver the audit report and diff proposals without applying. The done predicate is not met; report the blocked state explicitly.

## Output
- An audit report with a score table: file, mode, score, grade, key issues. Every issue in the table maps to a proposed diff; no vague findings.
- Proposed minimal diffs as diff snippets with one-line rationales, applied only after user confirmation.
- Before/after scores and line counts after applied edits.
- For setup: the set of agent instruction files that now exist, which tool reads each, and the verification result (tool quote-back test).
- For refactor: a deletion log with reason tags (`generic`, `duplicate`, `stale`, `moved`, `reworded`, `omitted`) and a before/after summary table, plus an omission list of unverifiable candidates so the user can see what was cut and why.
- For lean: the written file at the target path with pointer-only sections and commit attribution, or blocked/non-converged if the human did not confirm.
