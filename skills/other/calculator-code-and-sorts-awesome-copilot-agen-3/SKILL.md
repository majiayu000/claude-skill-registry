---
name: calculator
description: Performs arbitrary-precision arithmetic calculations including addition, subtraction, multiplication, division, and exponents. Use when the user asks to calculate, compute, or evaluate math expressions, or when precise decimal arithmetic is needed to avoid floating-point errors.
license: MIT
compatibility: Requires Node.js and npm
metadata:
  author: Colby Timm
  version: "1.0"
---

# Calculator

Evaluate arithmetic expressions with arbitrary-precision decimal math using [big.js](https://github.com/MikeMcl/big.js/).

## When to Use

- User asks to calculate or evaluate a math expression
- Precise decimal arithmetic is needed (avoids floating-point errors like `0.1 + 0.2 = 0.30000000000000004`)
- Expressions involve parentheses, operator precedence, or exponents

## Supported Operations

| Operator | Description | Precedence |
| -------- | ----------- | ---------- |
| `+` | Addition | 1 |
| `-` | Subtraction | 1 |
| `*` | Multiplication | 2 |
| `/` | Division | 2 |
| `^` | Exponent (right-associative) | 3 |
| `()` | Parentheses | Highest |

## Usage

```bash
cd scripts
npm ci || npm install
npm run build
npm run calculate "<expression>"
```

## Examples

| Input | Output |
| ----- | ------ |
| `"3 + 2"` | `5` |
| `"10 / 4"` | `2.5` |
| `"2 ^ 10"` | `1024` |
| `"(2 + 3) * 4"` | `20` |
| `"1 + 4.5 * (3-6) / 5"` | `-1.7` |
| `"-5 + 3"` | `-2` |
| `"2 ^ 3 ^ 2"` | `512` (right-associative: 2^9) |

## Edge Cases

- **Empty expression**: Throws "Empty expression" error
- **Mismatched parentheses**: Throws "Mismatched parentheses" error
- **Division by zero**: big.js throws an error
- **Exponent must be integer**: big.js `.pow()` requires integer exponents

## Limitations

- No trigonometric functions (sin, cos, tan)
- No variables or symbolic math
- Exponents must be integers
- No factorial, modulo, or bitwise operators
