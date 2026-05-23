---
name: planning-with-files
description: Manus-style file-based planning for complex tasks. Creates and maintains task_plan.md, findings.md, and progress.md under .kiro/plan/. Use when planning, breaking down work, resuming a multi-step task, tracking phases, or restoring context after compaction. Trigger phrases include start planning, continue task, resume work, current phase, restore context.
license: MIT
compatibility: Requires a POSIX shell or PowerShell, Python 3 for session-catchup, and read/write access to the workspace. See Kiro Agent Skills — https://kiro.dev/docs/skills/
allowed-tools: shell read write
metadata:
  version: "2.32.0-kiro"
  integration: kiro
---

# Planning with Files (Kiro)

Work like **Manus**: use persistent markdown as your **working memory on disk** while the model context behaves like volatile RAM. Deep background: [references/manus-principles.md](references/manus-principles.md).

Kiro complements this with:

- **Agent Skills** (this file) — progressive disclosure when the task matches the description.  
- **Steering** — after bootstrap, `.kiro/steering/planning-context.md` uses `inclusion: auto` and `#[[file:…]]` live references ([Steering docs](https://kiro.dev/docs/steering/)).

**Hooks are not bundled:** project-level hooks affect every chat in the workspace. Prefer this skill + steering + the reminder block below.

---

## STEP 0 — Bootstrap (once per workspace)

From the **workspace root**:

```bash
sh .kiro/skills/planning-with-files/assets/scripts/bootstrap.sh
```

Windows (PowerShell):

```powershell
pwsh -ExecutionPolicy RemoteSigned -File .kiro/skills/planning-with-files/assets/scripts/bootstrap.ps1
```

Creates:

- `.kiro/plan/task_plan.md`, `findings.md`, `progress.md`
- `.kiro/steering/planning-context.md` (auto + `#[[file:.kiro/plan/…]]`)

Idempotent: existing files are not overwritten.

**Import as a workspace skill (optional):** Kiro → *Agent Steering & Skills* → *Import a skill* → choose this `planning-with-files` folder ([Skills docs](https://kiro.dev/docs/skills/)).

---

## STEP 1 — Persistent reminder (after skill activation)

Append the following block to the **end of your reply**, and repeat it at the **end of subsequent replies** while this planning session is active:

> `[Planning Active]` Before each turn, read `.kiro/plan/task_plan.md` and `.kiro/plan/progress.md` to restore context.

---

## STEP 2 — Read plan every turn (while active)

1. Read `.kiro/plan/task_plan.md` — goal, phases, status  
2. Read `.kiro/plan/progress.md` — recent actions  
3. Use `.kiro/plan/findings.md` for research and decisions  

If `.kiro/plan/` is missing, run STEP 0.

---

## STEP 3 — Session catchup (after a long gap or suspected drift)

Summaries + file mtimes (compare with `git diff --stat` if needed):

```bash
$(command -v python3 || command -v python) \
  .kiro/skills/planning-with-files/assets/scripts/session-catchup.py "$(pwd)"
```

Windows:

```powershell
python .kiro/skills/planning-with-files/assets/scripts/session-catchup.py (Get-Location)
```

Then reconcile planning files with the actual codebase.

---

## Optional — Phase checklist

From workspace root (defaults to `.kiro/plan/task_plan.md`):

```bash
sh .kiro/skills/planning-with-files/assets/scripts/check-complete.sh
```

```powershell
pwsh -File .kiro/skills/planning-with-files/assets/scripts/check-complete.ps1
```

---

## Rules (summary)

Full detail: [references/planning-rules.md](references/planning-rules.md). Inline template skeletons: [references/planning-templates.md](references/planning-templates.md).

1. **Plan first** — no open-ended multi-step work without `task_plan.md`.  
2. **2-action rule** — after every two view/search/browser steps, write to `findings.md`.  
3. **Read before big decisions** — refresh `task_plan.md` into attention.  
4. **Update after each phase** — `in_progress` → `complete`, log errors.  
5. **Never repeat the same failed action** — change tool, approach, or assumptions.

## When to use

**Use:** multi-step work, research, refactors, anything that spans many tool calls.  

**Skip:** one-off questions, tiny single-file edits.

## Anti-patterns

| Avoid | Prefer |
|-------|--------|
| Goals only in chat | `.kiro/plan/task_plan.md` |
| Silent retries | Log errors; change approach |
| Huge pasted logs in chat | Append to `findings.md` or `progress.md` |
