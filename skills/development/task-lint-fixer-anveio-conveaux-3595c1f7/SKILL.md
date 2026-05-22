---
name: task-lint-fixer
description: Fix lint errors and update typescript-coding skill with lessons learned. Use when fixing Biome lint errors, resolving linting issues, or when lint check fails. Automatically extracts patterns from fixes and adds prevention tips to typescript-coding skill.
---

# Lint Fixer

Fix lint errors and contribute prevention tips back to the typescript-coding skill so future code avoids the same issues.

## Workflow

### Step 1: Identify Lint Errors

Run the lint check to see current errors:

```bash
npm run lint:check
```

Parse the output to identify:
- **Rule name** (e.g., `noExplicitAny`, `useImportType`, `noUnusedVariables`)
- **File path and line number**
- **Error message**

### Step 2: Categorize the Error

Determine if this is:
1. **Auto-fixable**: Biome can fix it with `--write`
2. **Manual fix required**: Requires code changes
3. **Pattern-based**: Represents a recurring anti-pattern worth documenting

### Step 3: Fix the Error

For auto-fixable errors:
```bash
npm run lint
```

For manual fixes, apply the appropriate correction based on the rule:

| Rule | Fix Pattern |
|------|-------------|
| `noExplicitAny` | Replace `any` with proper type, `unknown`, or generic |
| `useImportType` | Change `import { Foo }` to `import type { Foo }` for type-only imports |
| `useExportType` | Change `export { Foo }` to `export type { Foo }` for type-only exports |
| `noUnusedVariables` | Remove the variable or use it |
| `noUnusedImports` | Remove the import |
| `useConst` | Change `let` to `const` for non-reassigned variables |
| `noNonNullAssertion` | Use proper null checks, optional chaining, or invariant |
| `noUselessTypeConstraint` | Remove redundant `extends unknown` or `extends any` |

### Step 4: Extract the Lesson

For each fix, ask:
- **What was the anti-pattern?** (the code that triggered the error)
- **What is the correct pattern?** (the fix)
- **Why does this matter?** (type safety, performance, maintainability)

### Step 5: Update typescript-coding Skill

If the fix represents a valuable lesson not already in the typescript-coding skill:

1. Read the current skill:
   ```
   .claude/skills/typescript-coding/SKILL.md
   ```

2. Check if a similar tenet already exists. If yes, skip.

3. If novel, append a new tenet following this format:

```markdown
### Tenet: [Concise principle statement]

DON'T:

\`\`\`ts
// Brief comment explaining the anti-pattern
[code that triggers the lint error]
\`\`\`

DO:

\`\`\`ts
// Brief comment explaining the correct approach
[corrected code]
\`\`\`

> [Optional note about edge cases or additional context]
```

### Guidelines for Adding Tenets

**Add a tenet when:**
- The pattern is non-obvious to intermediate TypeScript developers
- The fix requires understanding beyond "follow the error message"
- The pattern relates to type safety, not just style preferences
- The lesson applies broadly, not just to one specific file

**Do NOT add a tenet when:**
- The fix is trivial (e.g., removing unused import)
- The typescript-coding skill already covers this pattern
- The issue is purely stylistic with no type safety implications
- The pattern is specific to one unusual edge case

## Common Lint Errors and Lessons

### useImportType / useExportType

```ts
// DON'T: Import types as values (larger bundle, confusing semantics)
import { MyInterface } from './types';

// DO: Use type-only imports for types
import type { MyInterface } from './types';
```

### noExplicitAny

```ts
// DON'T: Use any (defeats type checking)
function process(data: any) { ... }

// DO: Use unknown and narrow, or define proper types
function process(data: unknown) {
  if (isValidData(data)) { ... }
}
```

### noNonNullAssertion

```ts
// DON'T: Assert non-null without proof
const value = maybeNull!;

// DO: Use invariant or proper null handling
invariant(maybeNull, 'Expected value to be defined');
const value = maybeNull;
```

## Integration with Verification Pipeline

After fixing lint errors, run the full verification:

```bash
./verify.sh --ui=false
```

This ensures:
1. Lint passes
2. Types still check
3. Tests still pass
4. No regressions introduced

## Example Session

```
$ npm run lint:check
src/parser.ts:42:10 - lint/suspicious/noExplicitAny - Unexpected any. Specify a different type.

> Analysis: The function accepts `any` because the input type wasn't defined.
> Fix: Create a proper input type and use type guards.
> Lesson: This pattern (typing unknown external data) is already covered in typescript-coding skill under "Precise type guards to refine unknown data safely". No new tenet needed.

$ npm run lint:check
src/utils.ts:15:1 - lint/style/useImportType - All these imports are only used as types.

> Analysis: Importing types as values causes unnecessary runtime code.
> Fix: Change to `import type { ... }`.
> Lesson: Already covered by Biome auto-fix. No tenet needed (too trivial).

$ npm run lint:check
src/cache.ts:88:5 - lint/correctness/noUnusedVariables - Variable 'temp' is declared but never used.

> Analysis: Dead code from refactoring.
> Fix: Remove the variable.
> Lesson: No tenet needed (trivial cleanup).
```

## Updating Existing Tenets

If a lint fix reveals that an existing tenet is incomplete or unclear:

1. Locate the relevant tenet in typescript-coding skill
2. Edit to add the missing case or clarify the guidance
3. Ensure the example code is accurate and runs without lint errors
