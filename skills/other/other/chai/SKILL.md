---
name: chai
description: Chai assertion library for JavaScript. Use for JS assertions.
---

# Chai

Chai is an assertion library. It pairs naturally with Mocha. It supports TDD (`assert`) and BDD (`expect`, `should`) styles.

## When to Use

- **With Mocha**: The default pair.
- **Expressive Tests**: You want tests to read like English ("expect foo to be a string").

## Quick Start

```javascript
import { expect } from "chai";

const foo = "bar";
const beverages = { tea: ["chai", "matcha", "oolong"] };

expect(foo).to.be.a("string");
expect(foo).to.equal("bar");
expect(foo).to.have.lengthOf(3);
expect(beverages).to.have.property("tea").with.lengthOf(3);
```

## Core Concepts

### Styles

- **Assert**: Classic. `assert.equal(foo, 'bar')`.
- **Expect**: BDD. Chainable. `expect(foo).to.be.equal('bar')`.
- **Should**: BDD. Extends Object prototype. `foo.should.be.equal('bar')`. (Less common now due to side effects).

### Plugins

Chai has a rich ecosystem.

- `chai-http`: For API testing.
- `chai-as-promised`: For asserting promises (`return expect(promise).to.eventually.equal(2)`).

## Best Practices (2025)

**Do**:

- **Stick to one style**: Usually **Expect**. It's clean and doesn't modify prototypes.
- **Use Descriptive Chains**: `to.be.true` reads better than `to.equal(true)`.

**Don't**:

- **Don't mix Assert and Expect**: Confuses the reader.

## References

- [Chai Documentation](https://www.chaijs.com/)
