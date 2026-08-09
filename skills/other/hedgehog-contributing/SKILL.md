---
name: hedgehog-contributing
description: Use when the user wants to contribute a fix or ROADMAP.md item back to the Hedgehog project itself (skyf0xx/hedgehog) rather than their own project. Triggers on "let's fix that in Hedgehog", "I want to contribute", "let's pick up a roadmap item", or when `tweaker` offers this at the end of a build and the user says yes. Covers forking/branching, making the change under Hedgehog's own repo rules, committing with Conventional Commits, and opening the PR.
---

# Contributing to Hedgehog

Walks a user from "I want to fix/build this in Hedgehog itself" to an open
pull request against `skyf0xx/hedgehog`. This is for changes to the
**discipline** — `src/agents/`, `src/skills/`, `src/templates/`,
`bin/cli.mjs`, `README.md` — never for changes to the user's own project,
which is a different repo with different rules.

## When this runs

- The user names a specific gap (a bug they hit, a `ROADMAP.md` item) and
  wants to fix it in Hedgehog rather than work around it locally.
- `tweaker` offered this at the end of a build and the user said yes.

If the user hasn't picked a target yet, read `ROADMAP.md` at the Hedgehog
repo root with them and let them choose an item — prefer the "Small items"
tier for a first contribution, since each entry there is scoped to one file
or one narrow addition.

## Before starting

Confirm where the Hedgehog source actually lives on this machine. A project
that ran `npx @skyf0xx/hedgehog init` has a *copy* of the payload
(`.claude/agents/`, `.claude/skills/`), not the Hedgehog repo itself —
editing those files changes nothing upstream. Ask the user:

- If they already have a local clone of `skyf0xx/hedgehog`, use it.
- If not, offer to clone it: `gh repo fork skyf0xx/hedgehog --clone` (forks
  under their account and clones the fork), or `git clone
  https://github.com/skyf0xx/hedgehog` if they'd rather push directly to a
  branch on a repo they already have write access to.

Do this in a separate directory from the user's own project — never inside
it.

## Workflow

1. **Read `CONTRIBUTING.md`** at the Hedgehog repo root before touching
   anything. It defines the rules this repo's content has to follow:
   current-state-only files (no changelog narration inside the content
   itself), one owning file per rule (nothing load-bearing lives outside
   `src/agents/` or `src/skills/`), and PRs scoped to one agent, one skill,
   or one template at a time.
2. **Branch.** `git checkout -b <type>/<short-description>` off `master` —
   `feat/`, `fix/`, or `docs/` prefix matching the change, e.g.
   `feat/windsurf-host` or `fix/tweaker-job2-wording`.
3. **Make the change**, scoped to what `CONTRIBUTING.md` and the target
   `ROADMAP.md` item actually call for — resist scope creep onto adjacent
   files even if you notice something else worth fixing; that's a separate
   PR.
4. **Verify the install path locally** before committing, per
   `CONTRIBUTING.md`:
   ```bash
   mkdir -p /tmp/hedgehog-smoke && cd /tmp/hedgehog-smoke
   node /path/to/hedgehog/bin/cli.mjs init
   ```
   Confirm `.claude/agents/`, `.claude/skills/`, and the root templates
   land correctly, and that the specific thing you changed shows up as
   expected (a new skill directory copied over, a new host's files in the
   right place, a new blueprint reachable from `hedgehog-core-design`).
5. **Commit with Conventional Commits.** If the change is already one
   logical unit, commit it directly (`feat(hosts): add windsurf support`,
   `fix(tweaker): ...`, `docs(roadmap): ...`) — Hedgehog's commit format,
   same as the one `hedgehog-loop` uses for a project build. If the working
   tree has accumulated several unrelated changes that need splitting into
   atomic commits, use the `conventional-commits` skill rather than
   hand-rolling the split.
6. **Push and open the PR.**
   ```bash
   git push -u origin <branch-name>
   gh pr create --repo skyf0xx/hedgehog --title "<type>(<scope>): <summary>" --body "$(cat <<'EOF'
   ## Summary
   <1-3 bullets: what changed and why>

   ## Test plan
   - [ ] Ran `node bin/cli.mjs init` in a scratch dir and confirmed the change lands correctly
   EOF
   )"
   ```
   Describe the *why* in the PR body, not in the file being changed — same
   rule `CONTRIBUTING.md` states for the content itself. If the PR closes
   or addresses a `ROADMAP.md` item or a filed issue, reference it
   (`Addresses the "<item name>" item in ROADMAP.md`, or `Fixes #<n>`).
7. **Report the PR URL** `gh` returns and stop — don't merge, don't push
   further commits without being asked.

## Self-test

- The change happened in a Hedgehog repo clone, never inside the user's own
  project directory.
- The PR is scoped to one agent, one skill, one template, or one host —
  not a bundle of unrelated changes.
- The install smoke test actually ran and actually confirmed the specific
  change, not just that `init` exits zero.
- Commit messages and the PR title follow Conventional Commits.
- Nothing was merged or force-pushed without the user explicitly asking.
