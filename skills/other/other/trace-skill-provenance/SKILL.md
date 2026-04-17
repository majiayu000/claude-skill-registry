---
name: trace-skill-provenance
description: Investigate where a Hermes skill came from, when it was created, and whether it was builtin, promoted/imported, or locally created via skill_manage.
version: "1.0.0"
author: Hermes Agent
license: MIT
---

# Trace Skill Provenance

Use this when a user asks questions like:
- “这个 skill 是哪来的？”
- “是不是 builtin？”
- “什么时候创建的？为什么我没印象？”
- “这是导入的、提升的，还是你自己后来建的？”

## Goal

Determine, with evidence:
1. whether a skill is `builtin` or `local`
2. its on-disk path
3. approximate creation time
4. whether it came from promotion/import (`imported-codex` / manifest) or was created later via `skill_manage`
5. the session that created or modified it, if available

## Procedure

### 1. Confirm how Hermes classifies it
Run:
```bash
hermes skills list | grep -n '<skill-name>'
```
Interpretation:
- `builtin | builtin` => official built-in skill
- `local | local` => local skill in the runtime environment

Do not rely on memory alone.

### 2. Find the actual filesystem path
Check likely skill roots directly:
- `~/.hermes/skills`
- `~/.codex/skills` (older/shared runtime copies may still exist)

Example shell approach:
```bash
for d in ~/.hermes/skills ~/.codex/skills; do
  [ -d "$d" ] || continue
  find "$d" -type d -name '<skill-name>'
done
```

If needed, inspect `SKILL.md` under the found path.

### 3. Get file timestamps
For the skill directory and `SKILL.md`, inspect:
- birth time (`st_birthtime` on macOS when available)
- mtime
- ctime

Example Python snippet:
```python
from pathlib import Path
from datetime import datetime
p = Path('~/.hermes/skills/<category>/<skill-name>/SKILL.md').expanduser()
st = p.stat()
print(datetime.fromtimestamp(getattr(st, 'st_birthtime', st.st_ctime)))
print(datetime.fromtimestamp(st.st_mtime))
print(datetime.fromtimestamp(st.st_ctime))
```

Use this only as approximate creation evidence; later edits can change mtime/ctime.

### 4. Check promotion/import manifests
Look for promotion manifests such as:
```text
~/.hermes/skill-promotions/<timestamp>/promotion-manifest.json
```
Read them and see whether the skill appears in `entries`.

Interpretation:
- Present in manifest => likely promoted from `imported-codex` or another source
- Absent from manifest => likely not part of that promotion batch

Important: verify against the specific manifest timestamp instead of assuming all local skills came from promotion.

### 5. Search session history for creation evidence
Search Hermes session files and/or use session search for:
- the skill name
- `skill_manage`
- `action":"create"`
- `action":"patch"`

Useful targets:
- `~/.hermes/sessions/*.json`
- `session_search(query='"<skill-name>"')`

High-signal evidence is a session snippet containing:
- `skill_manage`
- `action: create`
- `name: <skill-name>`

If found, report:
- session id
- session start time
- exact lines or file reference

### 6. Distinguish creation modes clearly
Use the evidence to classify one of these outcomes:
- Built-in: listed as builtin; no local creation needed
- Promoted/imported: appears in promotion manifest and local path matches promoted category
- Locally created later: not in manifest, but session logs show `skill_manage(action='create', ...)`
- Locally patched later: original source may differ, but session logs show subsequent `patch` / `edit`

## Recommended evidence order in final answer

1. classification from `hermes skills list`
2. on-disk path
3. file timestamp
4. promotion-manifest result
5. session-log evidence of `skill_manage`

This makes the conclusion auditable and easy to trust.

## Pitfalls

- `hermes skills inspect <name>` may fail even when `skill_view(name)` works; do not stop there.
- Searching only `~/.hermes/skills` can miss older copies in `~/.codex/skills`.
- mtime alone is not “creation time”; prefer birth time when available and corroborate with session logs.
- A skill can be `local` without being imported; do not equate `local` with `promoted`.
- Promotion manifests prove inclusion in a batch, but absence there does not by itself prove manual creation; verify with session evidence.

## Done criteria

You should be able to answer, with citations/evidence:
- what kind of skill it is (`builtin` vs `local`)
- where it lives
- when it was likely created
- whether it was promoted/imported or created by a later agent action
- why the user may not remember it (for example, an agent auto-saved it after a complex task)
