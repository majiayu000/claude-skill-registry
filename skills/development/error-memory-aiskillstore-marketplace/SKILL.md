---
name: error-memory
description: >
  Use when: making a mistake, breaking build/tests, realizing wrong approach,
  misunderstanding requirements, using wrong patterns, forgetting conventions,
  receiving correction from user, unexpected behavior, or any error situation
---

# Error Memory

Document errors to avoid repeating them.

## Trigger

Invoke when:
- Build/tests fail after your action
- User corrects you
- You realize a wrong approach
- You forget a project convention
- Unexpected behavior occurs

## Process

1. **Identify** error type
   - `tech` : build, tests, syntax, runtime
   - `ctx` : conventions, patterns, project stack
   - `comp` : misunderstood requirements

2. **Analyze** root cause (not symptom)

3. **Formulate** fix as reusable rule

4. **Append** line to `.claude/errors.md`:
   ```markdown
   | MM-DD | type | Short error | Root cause | Rule to follow |
   ```

5. **Create** file if missing with this template:
   ```markdown
   # Project Errors

   > Past Claude mistakes on this project. Check before acting.

   | Date | Type | Error | Cause | Fix |
   |------|------|-------|-------|-----|

   ## Legend
   - **tech** : Technical (build, tests, syntax)
   - **ctx** : Context (conventions, patterns)
   - **comp** : Comprehension (misunderstood request)
   ```

## Rules

- One line = one error (no paragraphs)
- Fix = actionable rule, not excuse
- Cause = why, not what
- Keep < 100 lines (archive if needed)
- Check errors.md before acting on any project
