---
name: "Debugging Patterns Skill"
description: "Systematic problem-solving and error analysis."
applyTo: "**/*debug*,**/*error*,**/*fix*,**/*issue*"
---

# Debugging Patterns Skill

> Systematic problem-solving and error analysis.

## The Debugging Mindset

1. **Reproduce** — Can you make it happen consistently?
2. **Isolate** — What's the smallest case that fails?
3. **Hypothesize** — What could cause this?
4. **Test** — Prove or disprove your hypothesis
5. **Fix** — Change ONE thing
6. **Verify** — Did it actually fix it?

## Binary Search Debugging

When you don't know where the problem is:

```text
1. Find a known-good state (commit, version, config)
2. Find the known-bad state (current)
3. Test the midpoint
4. Repeat until you find the breaking change
```

Git bisect automates this:

```powershell
git bisect start
git bisect bad                    # Current is broken
git bisect good <known-good-sha>  # This worked
# Git checks out midpoint, you test, then:
git bisect good  # or  git bisect bad
# Repeat until found
git bisect reset                  # Return to normal
```

## Stack Trace Reading

```text
Error: Cannot read property 'x' of undefined
    at processData (src/utils.ts:45:12)      ← LOOK HERE FIRST
    at handleRequest (src/api.ts:123:8)
    at Router.handle (node_modules/...)
```

**Pattern**: Read bottom-up for context, top-down for cause.

## Common Error Categories

| Symptom | Likely Cause | Check |
| ------- | ------------ | ----- |
| "undefined is not a function" | Wrong import/export | Module paths, named vs default |
| "Cannot find module" | Path or package issue | Relative paths, node_modules |
| "ENOENT" | File not found | Path typo, file doesn't exist |
| "EACCES" | Permission denied | File permissions, admin rights |
| Silently fails | Swallowed error | Add try/catch, check promises |
| Works locally, fails in CI | Environment diff | Env vars, paths, versions |

## Logging Strategy

```typescript
// Bad: console.log("here")
// Good: console.log("[processData] input:", data, "state:", state)

// Even better: structured logging
log.debug({ fn: 'processData', input: data, state }, 'Processing started');
```

## Rubber Duck Debugging

When stuck:

1. Explain the problem out loud (or in text)
2. Describe what SHOULD happen
3. Describe what ACTUALLY happens
4. Walk through the code step by step
5. Often, the explanation reveals the bug

## Hypothesis Testing

Don't just change things randomly:

```text
❌ "Let me try this... and this... and this..."
✅ "I think X is null because Y. Let me add a log to confirm."
```

## Environment Debugging

```powershell
# Check environment variables
$env:PATH
$env:NODE_ENV

# Check versions
node --version
npm --version
code --version

# Check what's installed
npm list --depth=0
```

## Anti-Patterns

- ❌ Changing multiple things at once
- ❌ Assuming you know the cause without evidence
- ❌ Ignoring error messages
- ❌ "It works on my machine" without investigating why
- ❌ Removing error handling to "fix" errors

## Synapses

See [synapses.json](synapses.json) for connections.
