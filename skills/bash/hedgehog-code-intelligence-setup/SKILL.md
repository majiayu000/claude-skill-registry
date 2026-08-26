---
name: hedgehog-code-intelligence-setup
description: Use when `hedgehog init`, `hedgehog update`, or `hedgehog status` reports CODE INTELLIGENCE NOT SET UP, or when the user asks to set up, install, repair, or re-index code intelligence / CodeGraphContext / CGC. Installs Python 3.10+ where absent, installs CodeGraphContext into its own isolated environment, indexes the repository, writes `.hedgehog/code-intelligence.json` with the commit the index was built from, and re-runs the CLI's own check. Also covers refreshing an index that has drifted from HEAD.
---

# Code Intelligence Setup

Gets CodeGraphContext (`codegraphcontext`, shorthand `cgc`) running for
this repository and leaves `.hedgehog/code-intelligence.json` on disk in
the shape the CLI reads.

`formatCodeIntelligenceGap` in `src/db/code-intelligence-requires.mjs` owns
the copy explaining what the user gets from this. Do not restate it — if
the user asks why this is worth doing, show them the CLI's own message.

## This is judgment work, not a script

Every command below is a proposal about a machine you have not seen yet.
Run it, read what actually came back, and decide. A machine that has
Homebrew but not on PATH, a `python` that is Python 2, a `pip` that
refuses to install anything, a distro that ships `venv` as a separate
package — these are the normal cases, not the edge cases. The
"Recoveries" section names the ones that show up most.

Never proceed on an assumption you could have checked in one command.

## Standing constraints

These hold for every path through this skill.

- **Nothing installs globally by default.** CodeGraphContext goes into an
  isolated environment under `.hedgehog/`, owned by this project. The only
  installs that touch the system are a Python interpreter itself (when the
  machine has none new enough), and only with the user's explicit consent.
- **Never install `falkordblite` yourself.** KuzuDB is the cross-platform
  backend and the one this setup targets. CGC selects FalkorDB Lite when
  that package is present, so never add it, never let a "try installing
  the other backend" suggestion from any prompt talk you into it, and
  never pass an extras spec that pulls it in. CGC does declare it as an
  ordinary dependency on non-Windows Python 3.12+, so it may arrive on its
  own — that is CGC's choice, not yours, and it is why `cgc config db
  kuzudb` in Step 2 is what actually pins the selection.
- **Ask before anything that needs `sudo`, downloads an installer, or
  writes outside this repository.** Show the exact command first.
- **Every step checks before it acts.** This skill is re-run after partial
  failures more often than it is run fresh.

## Step 0 — Read the current state

Run these together and read all of it before deciding anything:

```bash
python3 --version 2>&1; echo "---"
python --version 2>&1; echo "---"
command -v python3 python python3.13 python3.12 cgc codegraphcontext 2>&1; echo "---"
cat .hedgehog/code-intelligence.json 2>&1; echo "---"
ls -d .hedgehog/code-intelligence 2>&1
```

Map what you see onto the same four states the CLI reports, so your
diagnosis and its message name the same problem:

| CLI reason | What it means here |
|---|---|
| `missing-python` | No `python3`, and `python` is absent or is Python 2 |
| `python-too-old` | Python 3 found, but below 3.10 |
| `missing-cgc` | Python fine, no `codegraphcontext`/`cgc` resolvable |
| `missing-config` | CGC present, `.hedgehog/code-intelligence.json` absent or malformed |

The CLI's floor is 3.10, but the floor is not the whole question: on macOS
and Windows, CGC pulls in the KuzuDB backend only below 3.14, so a 3.14
interpreter satisfies `python3 --version` and still builds an environment
with nothing to index into. Decide the interpreter here, before anything
is created, rather than discovering it at Step 2's backend probe with a
populated environment to throw away.

Pick, in order:

1. A `python3` that is 3.10-3.13 — use it.
2. Otherwise, a `python3.13` or `python3.12` on PATH from the probe above
   — use that binary by name in place of `python3` for the rest of this
   skill, including Step 2's `-m venv`.
3. Otherwise (3.14 is all the machine has, and the platform is macOS or
   Windows) — Step 1, to install 3.13 alongside it.

On Linux a 3.14 `python3` is fine as it stands: CGC requires `kuzu` there
regardless of version. Treat the check above as macOS and Windows only.

`python --version` printing `Python 2.7.x` means `python` is Python 2:
ignore that binary entirely from here on and work with `python3`. If
`python3` is absent too, the machine needs Python (Step 1). Never
"fix" this by repointing the `python` alias — other tools on the machine
depend on it resolving where it does.

Then jump to the first step whose work is not already done:

- Python missing, too old, or 3.14-only on macOS/Windows → Step 1
- Python fine, no CGC environment → Step 2
- CGC environment exists → Step 3 (verify it, then index)
- Everything present → Step 5 (rewrite the config and verify)

## Step 1 — Python 3.10 or newer

Skip this entirely if Step 0 settled on a usable interpreter.

CGC supports Python 3.10 through 3.14. If the machine has, say, 3.9,
installing a newer interpreter alongside it is correct — do not upgrade or
replace the interpreter the system itself uses.

Prefer 3.12 or 3.13 when you are choosing the version. On 3.14, CGC pulls
in the KuzuDB backend only on Linux, so a 3.14 environment on macOS or
Windows installs with no embedded backend — the commands below name 3.12
for that reason. This is also the step Step 0 sends a macOS or Windows
machine to when 3.14 is the only interpreter it has; installing 3.13
alongside it is the fix, and the system interpreter stays where it is.

### macOS

Homebrew is the route. It is frequently installed but not on the current
shell's PATH, so check for the binary at both of its standard locations
before concluding it is absent:

```bash
command -v brew || ls /opt/homebrew/bin/brew /usr/local/bin/brew 2>&1
```

If it exists at one of those paths but `command -v brew` found nothing,
use the absolute path for this session (`/opt/homebrew/bin/brew`, Apple
silicon; `/usr/local/bin/brew`, Intel) rather than trying to repair the
user's shell profile. Mention the PATH gap to them at the end; do not fix
it unprompted.

```bash
/opt/homebrew/bin/brew install python@3.12
```

Homebrew installs to its own prefix and links `python3` there. Confirm
with `command -v python3 && python3 --version` in a fresh shell invocation
— the linked binary may not be on the PATH this session inherited, in
which case use the absolute path Homebrew reports (`brew --prefix
python@3.12`, then `bin/python3.12` under it) for the rest of this skill.

If Homebrew is genuinely absent, ask the user before installing it. It is
a large install that changes how software is managed on their machine, and
that is their call, not yours. If they decline, point them at
python.org's macOS installer instead.

### Linux

Use the distro's package manager, and expect `sudo`.

```bash
# Debian / Ubuntu
sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
# Fedora / RHEL
sudo dnf install -y python3 python3-pip
# Arch
sudo pacman -S --needed python python-pip
# Alpine
sudo apk add python3 py3-pip
```

`python3-venv` is a **separate package on Debian and Ubuntu** and is not
pulled in by `python3`. Without it, `python3 -m venv` fails at the point
where Step 2 needs it, with an error suggesting exactly that package.
Install it in the same command rather than waiting for that failure.

If `sudo` is unavailable — no sudo binary, the user is not in sudoers, or
a password prompt cannot be answered in this session — do not try to work
around it. Say plainly that installing Python needs administrator rights
this session does not have, print the exact command for them to run, and
stop. Alternatively, if the machine has a user-space Python manager
already installed (`uv python install 3.12`, `pyenv install 3.12`,
`mise use python@3.12`), that is a legitimate no-sudo route — use it if
one is present, but do not install such a manager just to avoid asking.

### Windows

Download the official installer from python.org and run it, selecting
**Add python.exe to PATH**. If `winget` is available, that is the
non-interactive equivalent:

```powershell
winget install --id Python.Python.3.12 -e
```

On Windows, `python3` often does not exist and `python` is the Python 3
binary; `py -3 --version` is the reliable probe. There is also a stub
`python.exe` App Execution Alias in `%LOCALAPPDATA%\Microsoft\WindowsApps`
that opens the Microsoft Store instead of running Python — if `python
--version` produces no version output, or opens the Store, that stub is
what resolved. Use the real interpreter path (`py -3 -c "import sys;
print(sys.executable)"`) from then on.

Re-run Step 0's probe when the install finishes. A newly installed
interpreter is often not on the PATH this session inherited; resolve its
absolute path and carry that forward rather than restarting the session.

## Step 2 — CodeGraphContext, isolated

CGC is installed into a virtual environment owned by this project at
`.hedgehog/code-intelligence`. This is what keeps the install off the
system interpreter: it cannot disturb any Python another tool on the
machine depends on, and a PEP 668 "externally-managed-environment"
refusal cannot block it, because that guard applies to the system
interpreter and not to a venv.

Check first — this step is skipped whole when the environment already
has a working CGC:

```bash
.hedgehog/code-intelligence/bin/cgc --version 2>&1
```

(Windows: `.hedgehog\code-intelligence\Scripts\cgc.exe --version`.)

If that prints a version, the environment is good — go to Step 3.

Otherwise create it and install, using the Python you resolved in Step 0
or Step 1:

```bash
python3 -m venv .hedgehog/code-intelligence
.hedgehog/code-intelligence/bin/python -m pip install --upgrade pip
.hedgehog/code-intelligence/bin/python -m pip install 'codegraphcontext>=0.6.5,<0.7'
```

Install `codegraphcontext` and nothing else. Do not add extras, do not add
`falkordblite`, and if pip's resolver output mentions an optional backend,
leave it uninstalled.

That version specifier is the pin, and this line is the one place it is
written down — `scripts/check.mjs` reads it from here to tell whether a
newer CGC has published past the ceiling. The floor is the version this
setup is known to work against; the ceiling is the next minor, which for a
pre-1.0 package is where the breaking changes land. Changing either is a
deliberate act: install the new version, run Step 3 and Step 5 against it,
then move the pin.

`.hedgehog/` is generated state, so the environment does not belong in
version control. Check whether `.gitignore` already covers it, and if it
covers `.hedgehog/` as a whole you are done; if it lists specific entries
under `.hedgehog/`, add `.hedgehog/code-intelligence/` alongside them.

If `uv` is already on the machine, `uv venv .hedgehog/code-intelligence`
and `uv pip install --python .hedgehog/code-intelligence/bin/python
'codegraphcontext>=0.6.5,<0.7'` do the same job faster. Use it when
present; do not install it. Carry the same pin — a machine with `uv` must
end up on the same CGC as a machine without it.

### Select the backend

Set KuzuDB explicitly rather than relying on which backend CGC would pick
on its own:

```bash
.hedgehog/code-intelligence/bin/cgc config db kuzudb
```

`cgc config db <backend>` is a shortcut for `cgc config set
DEFAULT_DATABASE <backend>`, and it writes to CGC's own config
(`~/.codegraphcontext/.env`), so it persists across runs and is
idempotent. Confirm it took with:

```bash
.hedgehog/code-intelligence/bin/cgc config show
```

`DEFAULT_DATABASE` should read `kuzudb`.

Setting it explicitly is what makes the selection KuzuDB. CGC declares
`falkordblite` as an ordinary dependency on non-Windows Python 3.12+, so
installing `codegraphcontext` alone can bring the FalkorDB Lite backend
with it — the setting above is what keeps the choice yours regardless.

Confirm the backend is actually usable, rather than assuming the setting
found something to select:

```bash
.hedgehog/code-intelligence/bin/python -c "import kuzu; print(kuzu.__version__)"
```

If that raises `ModuleNotFoundError`, this environment has no KuzuDB.
CGC requires `kuzu` only for Python below 3.14 or on Linux, so a
**Python 3.14 environment on macOS or Windows** installs without it and
indexing has no embedded backend to write to. The fix is to build the
environment on Python 3.12 or 3.13 — Step 1's install, pointed at that
version, then Step 2 again against the new interpreter. Installing `kuzu`
by hand to paper over the gap puts the environment somewhere CGC does not
test; prefer the supported interpreter.

## Step 3 — Index this repository

Indexing walks the repository and builds the graph. It is not part of
every task — it runs here, and again when the code has moved far enough
from the indexed commit to matter.

### Exclude what isn't project code

Write the exclusions **before** the first index. CGC generates a default
`.cgcignore` on its first run covering the usual dependency directories
(`venv/`, `.venv/`, `env/`, `.env/`, `node_modules/`), and none of those
match the trees Hedgehog itself puts in the repository:

- `.hedgehog/` — generated state, and the home of the CGC virtualenv this
  setup just created. Left in, the index walks several thousand `.py`
  files belonging to CGC's own dependency tree.
- `vendor-skills/` — the vendored BMAD planning shelf `init` installs.
  Left in, its scripts, markdown, and HTML assets outnumber the project's
  own symbols and rank above them in `cgc find name` results.
- `.claude/` — the agents and skills `init` installs for Claude Code (and
  the equivalent host directory for other hosts, e.g. `.cursor/`). Every
  file in it is markdown Hedgehog wrote and the user never edits, and
  none of it contributes a function, class, or call edge to the graph —
  it is pure indexing cost.
- `AGENTS.md` and `CLAUDE.md` — the root routing index and discipline doc
  `init` writes at the repository root. Same as `.claude/`: Hedgehog-owned
  prose the user never edits, contributing no code symbols.

All five are Hedgehog-installed content that the user will never edit,
and all five degrade exactly what the index is for: pre-read context and
`verify_radius` blast-radius checks computed against a graph that is
mostly not this project.

Ensure `.cgcignore` at the repository root carries all five entries,
creating the file if it does not exist and appending to it if it does —
do not overwrite entries the project already put there:

```bash
touch .cgcignore
grep -qxF '.hedgehog/' .cgcignore || printf '.hedgehog/\n' >> .cgcignore
grep -qxF 'vendor-skills/' .cgcignore || printf 'vendor-skills/\n' >> .cgcignore
grep -qxF '.claude/' .cgcignore || printf '.claude/\n' >> .cgcignore
grep -qxF 'AGENTS.md' .cgcignore || printf 'AGENTS.md\n' >> .cgcignore
grep -qxF 'CLAUDE.md' .cgcignore || printf 'CLAUDE.md\n' >> .cgcignore
```

If the project has vendored trees, build output, or dependency
directories of its own that CGC's defaults miss, add those here too.

### Run the index

Read the subcommand list and use the indexing subcommand it names, pointed
at the repository root:

```bash
.hedgehog/code-intelligence/bin/cgc --help 2>&1
```

Then run it. `--force` is what makes the run happen: without it CGC
prints `already indexed ... Skipping` and exits 0 whenever a previous run
left an index behind, which covers both a re-run after a partial failure
and every later refresh.

Indexing costs minutes on a large repository, so on a re-run check
whether the exclusions above were already in place before the last index.
If they were, and the last run completed, the existing index is good and
Step 3 is done. If the exclusions are new — the usual case on a first
setup, and on any project installed before they existed — the index has
to be rebuilt for them to take effect, and that is what `--force` does.

```bash
.hedgehog/code-intelligence/bin/cgc index . --force 2>&1 | tail -40
```

On a large repository this takes minutes. Let it finish. If it exits
non-zero, read the error rather than retrying blind:

- Out of memory or a very long run on a large tree → ask the user whether
  to scope the index to the source directories rather than the repo root,
  and add further exclusions to `.cgcignore` beyond the ones above.
- A parse failure on individual files → usually not fatal; the index
  covers the rest. Continue if the command still succeeded overall.
- A missing native dependency for the graph backend → report it verbatim.
  Do not resolve it by installing an alternative backend package.

A `Skipped N unresolved call relationship(s): ambiguous_function_target=N`
table means CGC found call sites to a name defined more than once in the
repo (e.g. two classes each with a same-named method) and dropped those
edges rather than attaching them to any candidate. Those callers are then
invisible to `find_all_callers` and to blast-radius resolution — not
absent, just unresolved. This is a known CGC limitation
(`codegraphcontext` 0.6.5), not a setup defect; nothing here recovers the
edges. Note it and continue — a task whose scope brushes a name that
appeared in that table has a `verify_radius` gap the index cannot see,
worth flagging to the user rather than trusting silently.

## Step 4 — Write the config

Write `.hedgehog/code-intelligence.json` with an **absolute** path in
`command`. `startMcpClient` in `bin/cli.mjs` spawns `config.command`
exactly as written, with no PATH lookup and no shell — a bare
`codegraphcontext` or a relative path fails to spawn.

Resolve the absolute path rather than composing it by hand:

```bash
cd "$(git rev-parse --show-toplevel)" && printf '%s\n' "$PWD/.hedgehog/code-intelligence/bin/cgc"
```

Read the commit the index was just built from — this is the commit the
graph describes, so read it now rather than reconstructing it later:

```bash
git rev-parse HEAD
```

Read the CGC that built it, from the environment Step 2 installed — the
version string is the last word of the output (`CodeGraphContext 0.6.5`):

```bash
.hedgehog/code-intelligence/bin/cgc --version
```

Then write the file:

```json
{
  "command": "/absolute/path/to/repo/.hedgehog/code-intelligence/bin/cgc",
  "args": ["mcp", "start"],
  "indexedSha": "<the full SHA from git rev-parse HEAD>",
  "indexedAt": "<the current UTC time, ISO 8601>",
  "cgcVersion": "<the version from cgc --version, e.g. 0.6.5>"
}
```

`command` must be a non-empty string — the CLI treats the config as absent
otherwise, which is the `missing-config` state. `args` is the documented
way to start CGC's MCP server over stdio. Add `env` only if Step 2 or 3
surfaced a variable CGC actually needs; an absent `env` is normal.

`indexedSha` is what makes the index honest. It records which commit the
graph was built from, so `plan` and `status` can say whether the index
still describes this code instead of trusting that it does. Without it
they report the age as unknown, which is the correct answer for an index
that never recorded one — not a failure, but not a claim either. Write
the full forty-character SHA, not a short one. `indexedAt` is for a human
reading the file; nothing branches on it.

`cgcVersion` answers the other half of the same question. `indexedSha`
says which commit the graph describes; this says which tool built it,
which is the first thing worth knowing when an index returns output that
looks wrong. Nothing branches on it either, and its absence is not an
error — a config written before this field, or one whose `cgc --version`
could not be read, is complete without it. Record it when you have it and
move on when you don't.

Overwrite this file if it already exists. It is derived state, and a stale
path in it from a previous machine or a moved repository is exactly the
failure this step exists to correct.

## Refreshing a stale index

The index describes the commit it was built from. As the build moves on,
it drifts: symbols that moved are named where they used to be, and code
added since indexing is invisible to the pre-read context and to the
`verify_radius` gap check. That check under-reporting is the quiet
failure — an empty gap list reads as "nothing missing" whether the radius
is genuinely complete or the index simply cannot see the new files.

`hedgehog plan` and `hedgehog status` compare `indexedSha` against HEAD
and say so when they differ. Neither refuses to run: a stale index still
plans, because stranding a build behind a re-index is worse than planning
with a caveat the operator can read.

Re-index when they report drift and the work ahead depends on code that
landed since — a new module, a large refactor, anything whose blast
radius matters. A few commits of drift inside a module the index already
covers is not worth minutes of rebuild.

Refreshing is Step 3 and Step 4 again, in order: run the index, then
rewrite `indexedSha` from the current `git rev-parse HEAD`. Re-indexing
without updating the config leaves a fresh graph that still claims an old
commit, which reports as stale forever.

The refresh command is `cgc index . --force`, the same command Step 3
runs and the one `hedgehog status` and `hedgehog plan` print in their
staleness notices. `--force` carries the whole run: with an index already
present, the bare command prints `already indexed ... Skipping`, exits 0,
and leaves the stale graph in place, so the notice repeats with nothing
to show for it.

Two things CGC offers here that look like shortcuts and are not:

- `cgc update` reads as a cheap incremental refresh and is not one. It is
  an alias for a full delete-and-rebuild of the repository index, so it
  costs exactly what `cgc index . --force` costs. It also writes nothing
  to this config, so the `indexedSha` rewrite is still yours to do.
- `cgc hook install` installs git hooks that run that same full rebuild
  after every commit and checkout. On any repository where indexing takes
  minutes, that is minutes added to every commit. Do not install it.

CGC does have a genuinely incremental path — `cgc watch`, a daemon that
updates single files as they change. It holds the index continuously
fresh, at the cost of a background process with its own lifecycle.
Hedgehog does not start, supervise, or assume one. If the user asks for
it, that is their call to make and to run; the `indexedSha` in this
config still reflects the last full index either way.

## Step 5 — Verify

Re-run the same check the CLI runs, from the repository root:

```bash
npx @skyf0xx/hedgehog status 2>&1 | head -30
```

Any Hedgehog command that runs the check works here; `status` is the
cheapest. If it still prints `CODE INTELLIGENCE NOT SET UP`, the reason
line names which of the four states remains — go back to that step.

In the situation this skill is normally reached from — `init` gated on the
check, in a repository that has never been initialised — there is no build
graph yet, so `status` runs the check, then reports `No build graph found`
and exits non-zero. That exit is about the absent graph, not the setup:
read the lines above it. `Code intelligence is set up.` there means this
step passed. Do not run `hedgehog db init` to satisfy it — the graph is
`init`'s to create, and the next instruction below is what creates it.

The check reads `command` from the config first and only falls back to a
PATH lookup, so the isolated install this skill performs satisfies it with
no change to the user's shell profile. `missing-cgc` at this point means
the path in the config does not resolve to an executable file: re-check
Step 2's install and Step 4's path rather than reaching for PATH.

When the check passes, tell the user to re-run:

```bash
npx @skyf0xx/hedgehog init
```

`init` is where the payload gets written with code intelligence available,
so the re-run is what actually puts it to work.

## Recoveries

**PEP 668 `externally-managed-environment`.** pip refused because the
target is a system interpreter. The fix is the venv in Step 2, not
`--break-system-packages` and not `--user`. Never pass either flag: the
first does what its name says to an interpreter the machine depends on,
and the second still writes outside this project. If this error appears
while running a pip command from inside `.hedgehog/code-intelligence`,
then the venv was not actually created or is not the interpreter being
used — check `.hedgehog/code-intelligence/bin/python -c "import sys;
print(sys.prefix)"` and rebuild the environment if it points elsewhere.

**`python3 -m venv` fails on Debian or Ubuntu.** `python3-venv` is not
installed. Install it (Step 1) and retry; the error text names the exact
package for the interpreter's version.

**Indexing fails with no backend, or `import kuzu` raises
`ModuleNotFoundError`.** The environment is on Python 3.14 and not Linux,
where CGC does not pull in KuzuDB. Rebuild it on 3.12 or 3.13 (Step 1,
then Step 2) rather than installing `kuzu` by hand.

**`brew` not found but Homebrew is installed.** Its bin directory is not
on this session's PATH. Use `/opt/homebrew/bin/brew` or
`/usr/local/bin/brew` directly. Tell the user about the gap at the end;
their shell profile is theirs.

**`python` is Python 2.** Use `python3` exclusively. Do not repoint the
alias.

**A newly installed binary is not found.** The PATH was inherited when
this session started and does not include it yet. Resolve and use the
absolute path for the remainder of this skill.

**Re-running after a partial failure.** Start at Step 0 every time. Each
step's check tells you whether its work is already done, so a re-run picks
up where the last attempt stopped rather than repeating it. The one step
that always re-executes is Step 4 — rewriting the config is cheap and
corrects a stale path.

## Stopping

Stop and report rather than improvising when:

- Installing Python needs `sudo` this session cannot obtain.
- The user declines a system-level install.
- Indexing fails for a reason that is not about scope or an individual
  file.
- Anything would require installing `falkordblite` to proceed.

In each case, say exactly which step stopped, print the exact command the
user would run themselves, and leave the repository as it is. A partial
setup is safe to resume: re-running this skill continues from Step 0.
