---
name: mocha
description: Mocha JavaScript test framework. Use for Node.js testing.
---

# Mocha

Mocha is a flexible JavaScript test framework. Unlike Jest, it does _not_ come with an assertion library, mocking, or snapshotting built-in. It is a runner that allows you to choose your own tools (usually Chai + Sinon).

## When to Use

- **Flexibility**: You want to pick your assertion library (Chai, Should.js).
- **Node.js Backends**: standard in many Express/NestJS (legacy) setups.
- **Asynchronous Testing**: Historically strong support for async (though standard now).

## Quick Start

```javascript
// npm install --save-dev mocha chai
const assert = require("chai").assert;

describe("Array", function () {
  describe("#indexOf()", function () {
    it("should return -1 when the value is not present", function () {
      assert.equal([1, 2, 3].indexOf(4), -1);
    });
  });
});
```

## Core Concepts

### BDD Interface

`describe` (suite), `it` (test), `before`, `after`, `beforeEach`, `afterEach`.

### Hooks

Mocha allows defining hooks at the root level or inside suites to set up/tear down environments.

### Async support

Use `async/await` in the `it` block callback.

```javascript
it("should save user", async function () {
  const user = new User("tobi");
  await user.save();
});
```

## Best Practices (2025)

**Do**:

- **Use `.only` and `.skip`**: Useful during development to run a single test (`it.only(...)`).
- **Use `nyc` (Istanbul)**: For code coverage (since Mocha doesn't have it built-in).

**Don't**:

- **Don't use arrow functions** (`() => {}`) if you need `this.timeout()` or `this.slow()`. Mocha binds the test context to `this`.

## References

- [Mocha Documentation](https://mochajs.org/)
