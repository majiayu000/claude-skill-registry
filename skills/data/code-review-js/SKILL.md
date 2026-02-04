---
name: code-review-js
description: JavaScript-specific code review guidelines focusing on functional patterns and modern APIs
category: development
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# JavaScript Code Review

Includes all guidelines from code-review skill, plus JavaScript-specific rules.

## Prefer Functional Over OO

The reviewer SHOULD:
- Prefer pure functions and data transforms over classes when state is not required.
- Encourage small, composable utilities instead of deep inheritance trees.

The reviewer MUST:
- Flag new classes that only wrap stateless helpers or act as namespaces.

Acceptable:
```js
const formatUser = (user) => `${user.firstName} ${user.lastName}`;
```

Discouraged:
```js
class UserFormatter {
  format(user) {
    return `${user.firstName} ${user.lastName}`;
  }
}
```

## Use `switch` for Enum-like Values

The reviewer MUST:
- Flag `if/else if` chains that branch on the same enum-like value when a `switch` is clearer.

Preferred:
```js
switch (status) {
  case "idle":
    return renderIdle();
  case "running":
    return renderRunning();
  case "failed":
    return renderFailed();
  default:
    return assertNever(status);
}
```

Discouraged:
```js
if (status === "idle") return renderIdle();
if (status === "running") return renderRunning();
if (status === "failed") return renderFailed();
```

## Avoid Duplicated Code

The reviewer MUST:
- Flag duplicated logic and suggest extracting helpers or shared utilities.

The reviewer SHOULD:
- Prefer a single source of truth for calculations and formatting.

## Use Modern JavaScript APIs When Available

The reviewer SHOULD:
- Prefer modern APIs like `Object.hasOwn`, `Array.prototype.at`, `flatMap`, `replaceAll`, `URL`, `AbortController`, and `Promise.any` when they improve clarity.
- Confirm runtime targets or polyfills before requiring newer APIs.
