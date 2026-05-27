---
name: context7-skills
description: Use when managing Context7 CLI skills with npx ctx7 (search, install, list, remove, info).
---

# Context7 Skills

## Purpose

This skill **must directly execute** Context7 CLI commands for managing skills.

**Printing commands without execution is forbidden.**

## Scope (Authoritative & Closed)

Only the following commands are permitted (per `npx ctx7 skills --help`):

- `npx ctx7 skills search|s`
- `npx ctx7 skills install|i`
- `npx ctx7 skills list|ls`
- `npx ctx7 skills remove|rm`
- `npx ctx7 skills info`

Anything outside this list is **out of scope and prohibited**.

## Execution Rules (Non-Negotiable)

Execution rules apply **only after** required permissions (if any) are granted.

1. Commands **MUST be executed using `npx ctx7`**.
2. The `skills` / `skill` namespace is **mandatory**.
3. Only commands listed in **Scope** may be executed.
4. **Exactly one** target flag may be present **at most**.
5. `install` may include `--all`; no other install options are allowed.
6. Invalid, ambiguous, or incomplete input **MUST be corrected before execution**.
7. **No other shell commands** may be executed under any circumstances.

## Permission Requirements (Hard Gate)

Network-dependent commands (e.g., `search`, `info`, remote `install`) **MUST NOT** be executed unless the execution environment **explicitly grants** outbound network permission.

Requesting environment permission is **not** a user confirmation step and **not** a request for additional user input.

### Permission Flow

If a command is network-dependent:

1. **Request** outbound network permission from the execution environment / agent permission system.
2. If permission is **granted**, execute the command.
3. If permission is **denied or unavailable**, **stop** and report the limitation. Ask the user to run it locally or provide the output.

### No Redundant Confirmation

If the user explicitly requested a network-dependent command and no extra input is needed, proceed to the permission request **immediately** without asking for additional confirmation.

### Network Failures

If execution fails with a network error (e.g., `fetch failed`, DNS, timeout), treat it as an **environment/permission limitation**, not a command error. Do not retry unless the environment explicitly grants permission.

## Targets (Canonical)
Valid target flags (apply only where supported by the command):

- `--global`
- `--claude` — `.claude/skills/`
- `--cursor` — `.cursor/skills/`
- `--codex` — `.codex/skills/`
- `--opencode` — `.opencode/skills/`
- `--amp` — `.agents/skills/`
- `--antigravity` — `.agent/skills/`

If more than one target is requested, **STOP and request clarification**.

## Search Result Output (Mandatory)

After executing `npx ctx7 skills search|s ...` successfully:

1. MUST display the result entries as a **numbered list starting at 1**.
2. Each numbered item MUST preserve the entry text **as-is** (no paraphrase, no deduplication).

### One-Run Default
3. If the first run already contains any visible result entries, **do not rerun**. Output the visible entries immediately.

### Truncation Handling (Conditional Rerun)
4. Rerun the **same** search command up to **1 additional time** only when:
   - the first run shows **no visible result entries**, or
   - the tool output is truncated (`… +N lines`) **and** the output contains only summary lines (e.g., `Found N`) without entries.
5. MUST NOT ask the user for confirmation to rerun if the user already requested `search`.

### Interactive / Anomaly Claims (Evidence Rule)
6. MUST NOT claim the command became int

## Install Flow From Search Selection (Mandatory)

After showing numbered search results:

1. The user may reply with a **number** `k` to select a skill to install.
2. On receiving a valid selection `k`, extract from the selected entry:
   - `skill_name`
   - `repository` (as shown in the entry)
3. If the selection is invalid (not a number or out of range), ask the user to pick a valid number.

### Install Options Prompt (Numbered)
4. After a valid selection and if the user did not already specify install options, prompt the user to choose **exactly one** install target as a **numbered list**:

   1) `--claude` (.claude/skills/)
   2) `--cursor` (.cursor/skills/)
   3) `--codex` (.codex/skills/)
   4) `--opencode` (.opencode/skills/)
   5) `--amp` (.agents/skills/)
   6) `--antigravity` (.agent/skills/)
   7) `--global` (global)

5. The user responds with a number `t`. Map `t` to the corresponding target flag.
6. `--all` MUST NOT be used when installing a single selected skill.

### Permission Gate
7. If the install requires network access (remote repository), request outbound network permission before running install.

### Execute Install
8. Execute exactly:
   - `npx ctx7 skills install|i <repository> <skill_name> <target_flag>`
9. After execution, display the raw CLI output as-is.

## Quick Reference

| Intent | Executed Command |
| --- | --- |
| Search | `npx ctx7 skills search|s <keywords...>` |
| Install | `npx ctx7 skills install|i <repository> [skill] [--all] [target]` |
| List | `npx ctx7 skills list|ls [target]` |
| Remove | `npx ctx7 skills remove|rm <name> [target]` |
| Repo info | `npx ctx7 skills info <repository>` |

## Examples (Executed)

```bash
npx ctx7 skills search pytorch vision
npx ctx7 skills install /anthropics/skills uv --claude
npx ctx7 skills install /anthropics/skills --all --codex
npx ctx7 skills list --cursor
npx ctx7 skills info /anthropics/skills
````

## Hard Errors (Block Execution)

* Missing `skills` / `skill`
* Using commands outside **Scope**
* Emitting commands without execution
* More than one target flag
* Mixing targets with unrelated flags
* Attempting to run non-Context7 shell commands
* Executing network-dependent commands without explicit permission

## Notes (Behavioral)

* `<repository>` is mandatory for `install` and `info`.
* `[skill]` is optional; omission triggers interactive selection unless `--all` is used.
* `list` does **not** support filtering.
* Network failures (e.g., `fetch failed`) indicate environment/permission limits, not a command syntax issue.

