---
name: skills-manager-cli
description: >
  Drive the Skills Manager CLI (`skm`) to initialize the hub, adopt unmanaged
  skills, list/enable/disable skills per AI tool, and doctor/fix symlink sync.
  Use whenever the user or an agent needs to manage skills from a terminal,
  SSH session, CI job, or headless machine; when a skill is missing in Claude
  Code, Codex, Cursor, Gemini, OpenCode, or any other supported tool; when
  asked to run skm / Skills Manager CLI; or when setting up Skills Manager
  without the GUI. Do not use for `npx skills` / skills.sh search (different
  CLI), for writing SKILL.md content (skill-creator), or for marketplace
  browse/install (not in skm).
---

# Skills Manager CLI (`skm`)

**New here?** This skill drives `skm`, the command-line tool that ships with
[**Skills Manager**](https://skillsmanager.freeourdays.com) — a desktop app
(macOS / Windows / Linux) that installs one copy of a skill into a central hub
and symlinks it into every AI coding tool you use (Claude Code, Codex, Cursor,
Gemini, and ~30 more), so you write a skill once and it shows up everywhere.

If you found this skill on ClawHub but don't have Skills Manager yet, that is
the missing piece: `skm` is not a standalone binary you `npm install`. Get it
by installing the app from the [official website](https://skillsmanager.freeourdays.com/?ref=clawhub#download)
(then Settings → Command Line Tool, or run `skm init`), or grab a
`skm-<target>.tar.gz` / `.zip` from the
[GitHub Releases page](https://github.com/jiweiyeah/skills-manager/releases).
Source and docs: <https://github.com/jiweiyeah/skills-manager>.

`skm` is the terminal front-end of Skills Manager. It reads and writes the
same `~/.skills-manager/config.json` and the same hub/tool symlinks as the
desktop app, so GUI and CLI are interchangeable.

It does **not** create, edit, search, translate, tag, or marketplace-install
skills. Those stay in the GUI (or you write files into the hub yourself, then
`skm enable`).

## Preconditions

1. Resolve the binary. Prefer `skm` on `PATH`. If missing, say so and point
   at install: the [Skills Manager app](https://skillsmanager.freeourdays.com/?ref=clawhub#download)
   (Settings → Command Line Tool), or a release archive
   `skm-<target>.tar.gz` / `.zip` from
   [GitHub Releases](https://github.com/jiweiyeah/skills-manager/releases).
   Do not fall back to `npx skills` — that is a different, unrelated CLI.
2. Confirm with `skm --version`. A stale binary from an older app release
   should be updated from Settings or a matching release.
3. Every command except `init` requires an initialized config. If stderr
   says so, run `skm init --json` once — it is idempotent and will not
   clobber an existing config. `skm init` and Settings → Install CLI also
   copy this companion skill into the hub and enable it for every currently
   active tool, so you usually do not need to install it by hand.

Hub path is fixed at `~/.skills-manager/skills` (`%USERPROFILE%\.skills-manager\skills`
on Windows). `save()` always rewrites `skills_dir` to that default; there is
no supported way to pick another hub from the CLI.

## Agent conventions

These exist because `skm` is designed to be called by agents, not just humans.

- Prefer `--json` on `init`, `list`, `doctor`, `fix`, and `adopt` (apply).
  Data is one JSON document on stdout. Errors go to stderr as
  `{"error":"..."}` when the command was in JSON mode, otherwise
  `error: ...`. A command can print a result on stdout and still exit 1
  (`fix` with failed repairs) — parse stdout, then trust the exit code.
- `enable` / `disable` have no `--json`. Success is a one-line
  `enabled '<id>' for '<tool>'` (or `disabled`). Failure is `error: ...`
  on stderr, exit 1.
- Never wait on a TTY prompt. `adopt` without `--yes` and without `--json`
  blocks on `[y/N]`. Pass `--yes` when applying. `--json` also skips the
  prompt (and therefore applies) — still pass `--yes` so the intent is
  obvious in the command line.
- `skm adopt --json --dry-run` is not a machine-readable preview: if
  candidates exist it prints nothing. Preview with `skm adopt --dry-run`
  (human text), then apply with `skm adopt --yes --json`.
- `doctor --json` exits 0 even when there are issues. Gate on
  `.issues_count`, not the exit code.
- `fix` without `--yes` does not repair. JSON then looks like
  `{"applied": false, "issues_found": N, ...}`. Apply with `skm fix --yes --json`.
- Write commands (`init`, `adopt`, `enable`, `disable`, `fix --yes`) take
  an advisory lock on `config.json` and fail fast if another `skm` is
  mid-write. Retry once. The desktop app does not take this lock.
- Do not enable a skill for every detected tool unless the user asked.
  Pick the tool they named, or the host agent (see [Which tool](#which-tool)).

JSON shapes, exit codes, and the dry-run/apply matrix live in
`references/json.md`. Read that before parsing output or writing a script.

## Command map

| Intent | Command |
| --- | --- |
| First-run / is it initialized? | `skm init --json` |
| What skills exist, and where are they linked? | `skm list --json` |
| Same, one tool only | `skm list --tool <id> --json` |
| Turn a hub skill on for a tool | `skm enable <skill> --for <tool>` |
| Turn it off (remove the link, keep the hub copy) | `skm disable <skill> --for <tool>` |
| Which tools are installed, any broken links? | `skm doctor --json` |
| Repair what doctor reported | `skm fix --yes --json` |
| Preview leftover real dirs in tool skill folders | `skm adopt --dry-run` |
| Move those dirs into the hub and relink | `skm adopt --yes --json` |

`<skill>` and `<tool>` accept an exact id, an exact `instance_id`, or a
**unique** prefix (`claude` → `claude-code`). Ambiguous prefixes error and
list the matches — do not guess, rerun with a longer token. Exact tool id
wins before prefix (`trae` is Trae, not Trae CN). Full ids and collision
notes: `references/tools.md`.

## Workflows

### First-run on a machine with no GUI

```bash
command -v skm
skm init --json
skm adopt --dry-run
skm adopt --yes --json
skm list --json
skm doctor --json
```

`init` on an already-initialized config returns
`{"already_initialized": true, ...}` and does nothing else. If
`config.json` exists but cannot be parsed, `init` refuses to overwrite it
— move or fix the file, then retry.

### Make an existing hub skill available to a tool

```bash
skm list --json                          # find id / instance_id
skm enable <skill> --for <tool>
skm list --tool <tool> --json            # confirm enabled_for
```

Enabled state is derived from the link on disk, not stored as a separate
flag. `enable` creates the symlink (Windows: symlink → junction → tracked
copy). `disable` removes that link; the hub copy stays.

If the same skill id exists in both global and the active project, a bare
id is ambiguous. Use the `instance_id` from `list`: `global:<id>` or
`project:<project_id>:<id>`.

### Add a brand-new skill (CLI cannot scaffold it)

1. Write `~/.skills-manager/skills/<id>/SKILL.md` with YAML `name` +
   `description`. A directory is a skill if it contains `SKILL.md`,
   `skill.md`, or `meta.json`.
2. `skm enable <id> --for <tool>`
3. `skm list --tool <tool> --json` to confirm.

Do not copy the folder into `~/.claude/skills` (or any other tool dir)
yourself — that bypasses the hub and `adopt` will later see it as an
unmanaged real directory.

### Adopt skills that already live in a tool directory

`adopt` looks at **active** tools (enabled + detected) for real
directories that are not symlinks/junctions and not hidden. It **moves**
each one into the hub, then puts a link back at the original path.

- Duplicate hub names are skipped and left in place (contents are not
  merged — they may differ).
- Preview first (`--dry-run`), then apply (`--yes --json`).
- After apply, `list` should show the new ids as enabled for the source
  tool.

### Diagnose "the skill is not showing up in Claude / Codex / …"

```bash
skm doctor --json
skm list --tool <tool> --json
```

Read the results in this order:

1. Binary missing or not on `PATH` → install, reopen the shell.
2. `config_initialized` false → `skm init --json`.
3. Tool `detected: false` → the tool's config dir is not on this machine.
   CLI does not re-detect existing tools on every call; a tool installed
   after `init` may still show `not installed` until the GUI redetects or
   the config is updated. Do not try to invent a custom tool from `skm`.
4. Tool `enabled: false` → CLI cannot flip that flag. Use the GUI Tools
   page, or say so.
5. Skill absent from `list` → it is not in the hub (and not in the active
   project). Write it into the hub or `adopt`.
6. Skill present but not in `enabled_for` → `skm enable <skill> --for <tool>`.
7. `link_issues` > 0 or `issues_count` > 0 → `skm fix --yes --json`. If
   `failed_count` > 0, report the `failed[].message` values; do not loop
   `fix`.
8. A wrong-target or deleted link is treated as **disabled**, not as a
   doctor issue. Re-`enable` to recreate the link over the tampered path.

`fix` only repairs what `should_report_sync_issue` flags. It will not
delete a real (non-link) directory sitting in a tool's skills folder —
that is what `adopt` is for.

## Which tool

If the user named a tool, resolve it via `references/tools.md` and pass
`--for <id>`. If they did not:

| Host | `--for` |
| --- | --- |
| Claude Code | `claude-code` |
| Codex | `codex` |
| Cursor | `cursor` |
| Gemini CLI | `gemini` |
| OpenCode | `opencode` |
| Unsure | `skm doctor --json`, pick `detected && enabled` |

Prefix shortcuts that are unique today: `claude` → `claude-code`. Do not
use `trae` when the user said Trae CN (`trae-cn`), or `qoder` when they
said QoderWork CN (`qoderwork-cn`).

## Out of scope (do not fake these with `skm`)

| Need | What to do instead |
| --- | --- |
| Search / install from skills.sh | `npx skills` / find-skills, or the GUI Marketplace |
| Author SKILL.md | Write the file; this skill only covers linking it |
| Tags, notes, favorites, translation | GUI |
| Add/remove a custom tool, bind a project | GUI |
| Enable or disable a tool itself | GUI Tools page |
| Change the hub directory | Not supported; always `~/.skills-manager/skills` |
| Marketplace publish / ClawHub | GUI |

## Install locations (when `skm` is missing)

The desktop app copies a bundled binary:

- macOS / Linux: `/usr/local/bin/skm` if writable, else the first of
  `~/bin`, `~/.local/bin` that is already on `PATH`, else `~/.local/bin/skm`
  (then the folder may need to be added to `PATH`)
- Windows: next to the app executable (`skm.exe`)

Standalone: GitHub Releases `skm-<target>.tar.gz` (`.zip` on Windows),
extract, put on `PATH`.
