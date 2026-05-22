---
name: pattern-debug
description: Debug pattern errors systematically
user-invocable: false
---

# Debug Pattern

Use `Skill("ct")` for ct CLI documentation if debugging deployment or charm issues.

## Read First
- `docs/development/debugging/workflow.md` - 5-step debugging process
- `docs/development/debugging/README.md` - Error reference matrix

## Process

1. **Check TypeScript errors:**
   ```bash
   deno task ct check pattern.tsx --no-run
   ```

2. **Match error to documentation:**
   - Read the error message carefully
   - Check `docs/development/debugging/README.md` for matching errors

3. **Check gotchas:**
   - `docs/development/debugging/gotchas/handler-inside-pattern.md`
   - `docs/development/debugging/gotchas/filter-map-find-not-a-function.md`
   - `docs/development/debugging/gotchas/onclick-inside-computed.md`

4. **Simplify to minimal reproduction:**
   - Comment out code until error disappears
   - Add back piece by piece to find root cause

5. **Fix and verify:**
   - Apply fix
   - Run tests to confirm

## Common Issues

**Handler defined inside pattern body:**
- Move handler() to module scope
- Only bind it inside pattern: `onClick={myHandler({ state })}`

**Type errors with Writable/Default:**
- Check if field needs write access → use Writable<>
- Check if field could be undefined → use Default<T, value>

**Action not triggering:**
- Ensure Output type includes action as Stream<void>
- Use .send() not .get() to trigger

## Done When
- Root cause identified
- Error fixed
- Tests pass again
