---
name: speci5.check
description: "Verify implementation progress by inspecting source code against a story's plan. Reads plan.md tasks, searches the codebase for evidence of completion, and toggles task checkboxes. WHEN: /check, check progress, verify implementation, check story, are tasks done, update plan status, check plan. DO NOT USE FOR: brainstorming ideas (use brainstorm), writing specs (use specify), creating plans (use plan)."
argument-hint: "Path to the story folder, e.g. .spec/features/user-auth/login-with-email"
---

# Check

Verify implementation progress by inspecting source code against a story's plan.

## Triggers

Activate this skill when the user wants to:
- Verify if planned tasks have been implemented
- Check progress on a story
- Update task checkboxes based on current code state
- Get a status report on implementation progress

## Rules

1. Do NOT modify source code — this is a **read-only verification** skill.
2. Do NOT modify `story.md` or `feature.md`.
3. Only modify `plan.md` to toggle task checkboxes and add brief inline notes.
4. Be **conservative** — only mark a task complete if there is clear evidence in the code.
5. If a task is partially done, leave it unchecked and note what's missing.

## Steps

1. **Read the plan** — Load `.spec/features/<feature>/<story>/plan.md`.
2. **Read the story** — Load `story.md` to understand acceptance criteria context.
3. **Verify each task** — For each task in the plan:
   - Search the codebase for the specific files, functions, routes, components, or tests mentioned.
   - Evaluate whether the implementation satisfies the task's intent, not just that a file exists.
4. **Update plan.md** — Toggle checkboxes:
   - Completed: `- [ ]` → `- [x]`
   - Regressed (removed/broken): `- [x]` → `- [ ]`
   - Uncertain: leave unchecked, add a note.
5. **Report summary** — Present results to the user.

## Output

See [output template](./assets/output.md).
