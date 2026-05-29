---
name: peggy
# prettier-ignore
description: Use when writing PEG grammars with Peggy (formerly PEG.js) - parsing expression grammars, parser generation, and syntax definition
---

# Peggy Parser Generator

## Quick Start

```peggy
// grammar.peggy
Expression = head:Term tail:(_ ("+" / "-") _ Term)* {
  return tail.reduce((result, [, op, , term]) => {
    return op === "+" ? result + term : result - term;
  }, head);
}

Term = Integer / "(" _ expr:Expression _ ")" { return expr; }

Integer = digits:[0-9]+ { return parseInt(digits.join(""), 10); }

_ = [ \t\n\r]*
```

```typescript
import * as peggy from 'peggy';
import fs from 'fs';

const grammar = fs.readFileSync('grammar.peggy', 'utf-8');
const parser = peggy.generate(grammar);
const result = parser.parse('2 + 3 * 4'); // 14
```

## Core Syntax

| Pattern | Meaning |
|---------|---------|
| `"literal"` | Match exact string |
| `[a-z]` | Character class |
| `rule1 / rule2` | Ordered choice (try rule1 first) |
| `rule*` | Zero or more |
| `rule+` | One or more |
| `rule?` | Optional |
| `&rule` | Positive lookahead |
| `!rule` | Negative lookahead |
| `label:rule` | Capture as variable |
| `{ code }` | Action (return value) |

## Rule Definitions

```peggy
// Named rule
Identifier = [a-zA-Z_][a-zA-Z0-9_]* { return text(); }

// With semantic action
Number = digits:[0-9]+ { return parseInt(digits.join(""), 10); }

// Choice with labels
BinaryOp = left:Term op:("+" / "-") right:Term {
  return { type: "binary", op, left, right };
}
```

## Built-in Functions

- `text()` - Matched text as string
- `location()` - Start/end positions
- `expected(desc)` - Throw expected error
- `error(message)` - Throw custom error

## CLI Usage

```bash
npx peggy grammar.peggy -o parser.js
npx peggy --format es grammar.peggy  # ES module output
```

## Tips

- Order choices from most to least specific
- Use `!.` for "not end of input"
- Whitespace is significant; define `_` rule for optional whitespace
- Use `@` prefix for pluck: `@value:Rule` returns just the labeled value
