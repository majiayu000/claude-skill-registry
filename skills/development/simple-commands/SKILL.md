# Simple Commands

## The Rule

Run one command at a time. Look at the full output. Then decide what to do next.

## Why

Chaining commands and truncating output *looks* efficient but causes problems:

```bash
# Bad: chains commands, truncates output
npm test && npm run build 2>&1 | head -50

# Good: one command, full output
npm test
```

### The Failure Mode

When you chain and truncate:
1. Error might be on line 51 (past your `head -50`)
2. You don't see it
3. You run again, same result
4. Human watches you loop while blind to the actual error

This is **stochastic noise** - doing plausible things that don't help.

### The False Economy

"But chaining saves context!"

No. Re-running blind commands *wastes* context. One clear command with full output uses less context than three truncated attempts that miss the error.

## When Chaining IS Okay

Sequential dependencies where you need all to succeed:

```bash
# Fine: git operations that depend on each other
git add . && git commit -m "message" && git push
```

The key difference: you're not truncating, and failure at any step stops the chain.

## Patterns to Avoid

```bash
# Truncating build output
npm run build | head -50

# Hiding stderr
npm test 2>/dev/null

# Chaining unrelated commands
npm test && npm run lint && npm run build | tail -20
```

## The Mindset

Each command is a question. Read the full answer before asking the next question.
