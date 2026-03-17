---
name: pattern-test
description: Write and run pattern tests
user-invocable: false
---

Use `Skill("ct")` for ct CLI documentation when running commands.

# Test Sub-Pattern

## Prerequisite Check
Before writing tests, verify the pattern has:
- `pattern<Input, Output>()` (not single-type `pattern<State>()`)
- Actions typed as `Stream<T>` in Output interface
- Bound handlers returned from the pattern

If missing, fix the pattern first - tests can't call `.send()` without proper Output types.

## Read First
- `docs/common/workflows/pattern-testing.md` - Full test file format and prerequisites

## Test Command
```bash
deno task ct test packages/patterns/[name]/[file].test.tsx
```

## Test File Template

```tsx
import { action, computed, pattern } from "commontools";
import Pattern from "./pattern.tsx";

export default pattern(() => {
  // 1. Instantiate pattern under test
  const instance = Pattern({ /* input */ });

  // 2. Define actions (trigger events)
  const action_do_something = action(() => {
    instance.someAction.send();
  });

  // 3. Define assertions (computed booleans)
  const assert_initial_state = computed(() => instance.someField === expectedValue);
  const assert_after_action = computed(() => instance.someField === newValue);

  // 4. Return tests array
  return {
    tests: [
      { assertion: assert_initial_state },
      { action: action_do_something },
      { assertion: assert_after_action },
    ],
  };
});
```

## Key Points
- Test each sub-pattern BEFORE writing the next one
- Use `.send()` to trigger actions (requires Stream<void> in Output type)
- Use direct property access to read values (not `.get()`)
- Use `computed(() => boolean)` for assertions

## Done When
- Test file exists alongside pattern
- Tests pass
- Ready for next sub-pattern
