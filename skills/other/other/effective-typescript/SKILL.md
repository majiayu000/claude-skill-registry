---
name: effective-typescript
description: >
  Review existing TypeScript code and write new TypeScript following the 62 items from
  "Effective TypeScript" by Dan Vanderkam. Use when writing TypeScript, reviewing TypeScript
  code, working with type design, avoiding any, managing type declarations, or migrating
  JavaScript to TypeScript. Trigger on: "TypeScript best practices", "type safety", "any",
  "type assertions", "type design", "strict mode", "TypeScript review", "migrate to TypeScript".
---

# Effective TypeScript Skill

Apply the 62 items from Dan Vanderkam's "Effective TypeScript" to review existing code and write new TypeScript. This skill operates in two modes: **Review Mode** (analyze code for violations) and **Write Mode** (produce idiomatic, well-typed TypeScript from scratch).

## Reference Files

This skill includes categorized reference files covering all 62 items:

- `ref-01-getting-to-know-ts.md` — Items 1-5: TS/JS relationship, compiler options, code generation, structural typing, any
- `ref-02-type-system.md` — Items 6-18: editor, sets, type vs value space, declarations vs assertions, object wrappers, excess property checking, generics, readonly, mapped types
- `ref-03-type-inference.md` — Items 19-27: inferable types, widening, narrowing, objects at once, aliases, async/await, context, functional constructs
- `ref-04-type-design.md` — Items 28-37: valid states, Postel's Law, documentation, null perimeter, unions of interfaces, string types, branded types
- `ref-05-working-with-any.md` — Items 38-44: narrowest scope, precise any variants, unsafe assertions, evolving any, unknown, monkey patching, type coverage
- `ref-06-type-declarations.md` — Items 45-52: devDependencies, three versions, export types, TSDoc, this in callbacks, conditional types, mirror types, testing types
- `ref-07-writing-running-code.md` — Items 53-57: ECMAScript features, iterating objects, DOM hierarchy, private, source maps
- `ref-08-migrating.md` — Items 58-62: modern JS, @ts-check, allowJs, module-by-module, noImplicitAny

## How to Use This Skill

**Before responding**, read the relevant reference files based on the code's topic. For a general review, read all files. For targeted work (e.g., type design), read the specific reference (e.g., `ref-04-type-design.md`).

---

## Mode 1: Code Review

When the user asks you to **review** existing TypeScript code, follow this process:

### Step 1: Read Relevant References
Determine which chapters apply to the code under review and read those reference files. If unsure, read all of them.

### Step 2: Analyze the Code
For each relevant item from the book, check whether the code follows or violates the guideline. Focus on:

1. **TypeScript Fundamentals** (Items 1-5): Is `strict` mode enabled? Is `any` used carelessly? Does structural typing cause surprises?
2. **Type System Usage** (Items 6-18): Are type declarations preferred over assertions? Are object wrapper types avoided? Are `readonly` and mapped types used appropriately?
3. **Type Inference** (Items 19-27): Is inference relied upon where possible? Are `async`/`await` used over callbacks? Are aliases consistent?
4. **Type Design** (Items 28-37): Do types represent only valid states? Are string types replaced with literal unions? Are null values pushed to the perimeter?
5. **Working with any** (Items 38-44): Is `any` scoped as narrowly as possible? Is `unknown` used for truly unknown values? Are unsafe assertions hidden in well-typed wrappers?
6. **Type Declarations** (Items 45-52): Are `@types` in devDependencies? Are public API types exported? Is TSDoc used for comments?
7. **Code Execution** (Items 53-57): Are ECMAScript features preferred over TypeScript-only equivalents? Is object iteration done safely?
8. **Migration** (Items 58-62): Is modern JavaScript used as a baseline? Is migration done module-by-module?

### Step 3: Report Findings
For each issue found, report:
- **Item number and name** (e.g., "Item 9: Prefer Type Declarations to Type Assertions")
- **Location** in the code
- **What's wrong** (the anti-pattern)
- **How to fix it** (the TypeScript-idiomatic way)
- **Priority**: Critical (bugs/correctness), Important (maintainability), Suggestion (style)

### Step 4: Provide Fixed Code
Offer a corrected version of the code with all issues addressed, with comments explaining each change.

---

## Mode 2: Writing New Code

When the user asks you to **write** new TypeScript code, apply these core practices:

### Always Apply These Core Practices

1. **Enable strict mode** (Item 2). Never write TypeScript without `"strict": true` in tsconfig.json.

2. **Prefer type declarations over assertions** (Item 9). Use `const x: MyType = value` not `const x = value as MyType`.

3. **Avoid object wrapper types** (Item 10). Use `string`, `number`, `boolean` — never `String`, `Number`, `Boolean`.

4. **Use types that represent only valid states** (Item 28). Eliminate impossible states at the type level with tagged unions.

5. **Push null to the perimeter** (Item 31). Don't scatter `T | null` throughout — handle nullability at boundaries.

6. **Prefer unions of interfaces to interfaces of unions** (Item 32). Model tagged unions instead of interfaces with optional fields that have implicit relationships.

7. **Replace plain string types with string literal unions** (Item 33). `type Direction = 'north' | 'south' | 'east' | 'west'` not `string`.

8. **Generate types from APIs and specs, not data** (Item 35). Use `quicktype` or OpenAPI code generation — don't hand-write types for external data.

9. **Use `unknown` instead of `any` for values with unknown type** (Item 42). `unknown` forces callers to narrow before use.

10. **Scope `any` as narrowly as possible** (Item 38). Apply it to a single value, never a whole object or module.

11. **Use `readonly` to prevent mutation bugs** (Item 17). Prefer `readonly` on function parameters accepting arrays, and on class fields that should not be reassigned.

12. **Use `async`/`await` over raw Promises and callbacks** (Item 25). It produces cleaner inferred types and clearer code.

13. **Use type aliases to avoid repeating yourself** (Item 14). DRY applies to types too — extract shared structure with `Pick`, `Omit`, mapped types.

14. **Export all types that appear in public APIs** (Item 47). Don't force users to reconstruct types with `ReturnType<>` or `Parameters<>`.

15. **Use TSDoc for API comments** (Item 48). `/** */` comments appear in editor tooltips; `@param`, `@returns`, `@deprecated` are recognized by tooling.

### Type Structure Template

```typescript
// Prefer interfaces for object shapes (extendable); type aliases for unions/intersections
interface User {
  readonly id: UserId;     // Item 17: readonly on fields that shouldn't change
  name: string;
  email: string;
}

// Branded type for nominal typing (Item 37)
type UserId = string & { readonly __brand: 'UserId' };

// Tagged union — only valid states representable (Item 28, 32)
type RequestState<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; message: string };

// unknown, not any, for values from external sources (Item 42)
function parseResponse(json: string): unknown {
  return JSON.parse(json);
}

// async/await over callbacks (Item 25)
async function fetchUser(id: UserId): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as User; // narrowly scoped assertion inside well-typed function (Item 40)
}
```

### any Guidelines
- If `any` is unavoidable, apply it to the smallest possible scope (Item 38)
- Prefer `unknown` for values received from external sources (Item 42)
- Hide unsafe assertions inside well-typed wrapper functions (Item 40)
- Track type coverage with `type-coverage` CLI to prevent regressions (Item 44)

---

## Priority of Items by Impact

### Critical (Correctness & Bugs)
- Item 2: Enable `strict` mode — `noImplicitAny` and `strictNullChecks` prevent whole classes of bugs
- Item 9: Prefer declarations to assertions — assertions bypass the type checker
- Item 28: Types that always represent valid states — impossible states cause runtime errors
- Item 31: Push null to the perimeter — scattered nullability causes null dereferences
- Item 42: Use `unknown` instead of `any` — `any` silently disables type checking

### Important (Maintainability)
- Item 13: Know the differences between `type` and `interface`
- Item 14: Use type operations and generics to avoid repetition
- Item 17: Use `readonly` to prevent mutation bugs
- Item 25: Use `async`/`await` over callbacks
- Item 32: Prefer unions of interfaces to interfaces of unions
- Item 33: Prefer string literal unions over plain `string`
- Item 47: Export all types that appear in public APIs
- Item 48: Use TSDoc for API comments

### Suggestions (Polish & Optimization)
- Item 19: Omit inferable types to reduce clutter
- Item 35: Generate types from APIs and specs
- Item 37: Consider brands for nominal typing
- Item 44: Track type coverage
- Item 53: Prefer ECMAScript features over TypeScript-only equivalents
