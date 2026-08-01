---
name: phx-codex-loop
description: Fix Elixir/Phoenix code until Codex CLI review comes back clean — bounded
  review, fix, verify loop before opening a PR. Use when codex is installed and you
  want an external cross-model critic on your changes before pushing.
---

# Codex Loop (fix until clean)

Critic→Refiner loop with the Codex CLI as external critic: review → fix
approved findings → verify → re-review, until codex is clean or rounds run
out. Codex reviews; Claude fixes. Complements `/skill:phx-review` (Claude panel)
— run either or both before a PR.

## Usage

```
/skill:phx-codex-loop                    # diff vs default branch, interactive
/skill:phx-codex-loop --uncommitted      # staged + unstaged + untracked
/skill:phx-codex-loop --base develop     # explicit base branch
/skill:phx-codex-loop --auto             # auto-approve P0/P1/P2, skip P3
/skill:phx-codex-loop --max-rounds 2     # default 3
```

## Iron Laws

1. **BOUNDED rounds — never exceed --max-rounds (default 3)** — each round
   costs codex quota; report remaining findings instead of looping on
2. **Verify BEFORE re-review** — `mix compile --warnings-as-errors` + tests
   must pass before burning a codex round on broken code
3. **NEVER commit or push** — leave git to the user
4. **Codex findings get Iron Law scrutiny** — decline suggestions that
   violate an Iron Law, with explanation in the round report
5. **Skipped findings are reported, never dropped** — every finding ends as
   fixed, declined (with reason), or deferred-by-user
6. **Missing CLI stops the skill with an install hint** — suggest
   `/skill:phx-review` as the codex-free alternative; never crash

## Workflow

### Step 1: Preflight

Run `command -v codex`. If missing: STOP.
Show the install hint (`brew install codex` or `npm i -g @openai/codex`,
then `codex login`; `codex doctor` to diagnose) and suggest `/skill:phx-review`.

Then two cheap checks that save review rounds:

- **Dirty tree** (`git status --short`, only when using `--base`): codex
  inspects working-tree state too and WILL flag local dirt (stray edits,
  dirty submodules) as findings. Surface the dirt and ask: clean/stash
  first, or proceed knowing round 1 may spend findings on it.
- **Missing rubric**: if `AGENTS.md` has no `## Review guidelines`
  section, note once that `/skill:phx-init` installs the Elixir rubric that
  steers codex priorities — then proceed (it works without, on defaults).

### Step 2: Detect Diff Mode

- **Flag passed** (`--base`/`--uncommitted`) → use as given
- **Commits ahead of the default branch** → `--base {default}`
- **No commits yet** → `--uncommitted`

### Step 3: Round Loop (max `--max-rounds`, default 3)

1. **Review** — ONE foreground Bash call, explicit `timeout: 600000`
   (large diffs run 10+ min). On timeout with the process alive: ONE
   `until [ -f {out} ]; do sleep 5; done` wait — never poll-spam or
   `pkill` a running review (quota is spent either way). ALWAYS silence
   the streams — only the `-o` file matters (10k+ lines otherwise):

   ```bash
   codex exec review --base {branch} --ephemeral \
     -o /tmp/codex-round-{n}.md > /tmp/codex-round-{n}.log 2>&1
   ```

   NEVER pass custom instructions with a diff-mode flag — the CLI rejects
   the combination; the rubric comes from AGENTS.md `## Review guidelines`
   (`/skill:phx-init`). Parse the output file, NOT the exit code (0 even with
   findings). Recipes: `references/codex-cli.md`.

2. **Clean check** — parse the output file; no `- [P{n}]` bullets means
   CLEAN → go to Step 4.

3. **Triage** — emit the findings table
   (`# | P | file:line | title | proposed action`) as **visible
   response text BEFORE any `AskUserQuestion` call** — a table composed
   only in thinking never renders. Then ask approve-or-skip per finding
   (`AskUserQuestion`). With `--auto`: approve P0/P1/P2, skip P3 (list
   skipped in the round report).

4. **Fix** — apply approved fixes with user-visible diffs. Check each
   against Iron Laws first (Law 4).

5. **Verify** — scoped, before the next round:

   ```bash
   mix format {changed_files} && \
   mix compile --warnings-as-errors && mix test {affected_tests}
   ```

   If verification fails 3 times, STOP with a BLOCKER report — do not
   burn another codex round on broken code.

6. Next round (n+1).

### Step 4: Final Report

```markdown
## Codex Loop Report — {CLEAN | MAX ROUNDS REACHED | BLOCKED}
Rounds: {n}/{max} | Fixed: {n} | Declined (Iron Law): {n} | Deferred: {n}
{per-round: findings → outcome}
{remaining findings if not CLEAN}
```

On CLEAN: suggest `/skill:phx-compound` for non-obvious fixes, then commit/PR.
On MAX ROUNDS: list remaining findings; offer `/skill:phx-plan` to convert them
into a follow-up plan.

## Integration

```text
implement → /skill:phx-codex-loop (YOU ARE HERE) → clean → commit/PR → /skill:phx-watch-pr --codex
     ↑ or arrive from /skill:phx-review --codex verdict REQUIRES CHANGES
```

## References

- `references/codex-cli.md` — invocation recipes, parse
  patterns, verified gotchas (CLI 0.142.5)
