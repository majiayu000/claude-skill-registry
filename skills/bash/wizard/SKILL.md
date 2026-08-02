---
name: wizard
description: 'Generate an interactive bash wizard that walks a human through a manual procedure: third-party setup, a one-off migration, or an A to B state transition. It opens URLs, captures values, confirms each step, and writes .env entries and GitHub Actions secrets. Author it, never run it.'
---

# Wizard

**Author the wizard. Never run it.** It opens browsers and blocks on human input. ODIN runs no process that waits on stdin, so verify the script statically.

A wizard is a bash script that walks a human through a manual procedure one step at a time.

Everything above the `STAGES` marker in `scripts/wizard-template.sh` is the shared library. It is identical in every wizard and is never hand-edited. Scope the procedure and write only the stages below that marker.

## Process

### 1. Scope the procedure

Read the repository before asking anything:

- `.env`, `.env.example`, and `.env.*`
- `README`
- `docker-compose*`
- Framework configuration
- `.github/workflows/*`

Treat every `secrets.*` and `vars.*` reference in a workflow as a value the wizard must produce. For a migration, read the current state, the target state, and every irreversible action between them.

Show the ordered stage list and the values each stage produces. Confirm it with the user. Scoping is complete only when:

- Every stage has a name and order.
- Every captured value has a known source.
- Every captured value has a destination: `.env`, a GitHub secret, both, or nowhere for a pure-action stage.
- Every captured value is classified as secret or public.

### 2. Map the human journey

For each stage, write instructions a stranger can follow. Name the URL, the clicks, where the value appears, and which variable it fills. If the current UI or exact command is unknown, say so. Check the official docs or ask the user. Never invent a step.

### 3. Author the script

Copy `scripts/wizard-template.sh` to the target path. Replace the example with one `stage` per step in dependency order. Set `TOTAL_STAGES` and `TOTAL_MINUTES` to honest values because they drive the time-remaining display.

Use the library helpers by contract:

- `stage`: clear the screen and start one focused task.
- `say`: print a plain instruction.
- `step`: print one action for the human.
- `note`: print supporting detail.
- `warn`: print a warning.
- `open_url`: open the target page.
- `ask`: capture a public value.
- `ask_secret`: capture a hidden value.
- `write_env`: persist one value to `.env`.
- `set_secret`: write a GitHub Actions secret.
- `set_var`: write a GitHub Actions variable.
- `pause`: wait for the human to finish a manual action.
- `confirm`: gate an irreversible action.
- `banner`: show the opening summary.
- `finish`: show what was written and what remains.

Open a URL before asking for its value. Use `ask_secret` for secrets. Call `write_env` for every persisted value. Call `set_secret` only for values CI needs. Call `confirm` before an irreversible action. A `stage` clears the screen, so keep it to one focused task or the human loses the instructions that scrolled away.

### 4. Verify and hand off

1. Run `bash -n <script>`.
2. Run `shellcheck <script>` when ShellCheck is available.
3. Run `chmod +x <script>`.
4. Trace every scoped value. Confirm it is captured and reaches its declared destination.
5. Confirm every `set_secret` name matches a `secrets.*` workflow reference exactly.
6. Tell the user how to run the script.

Commit the wizard only when the user wants a repeatable setup path in the repository. Otherwise, treat it as ephemeral and delete it after the job is done.
