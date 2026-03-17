---
name: ct
description: Guide for using the ct (CommonTools) binary to interact with charms,
  recipes, and the Common Fabric. Use this skill when deploying recipes, managing
  charms, linking data between charms, or debugging recipe execution. Triggers include
  requests to "deploy this recipe", "call a handler", "link these charms", "get data
  from charm", or "test this recipe locally".
---

# CT CLI

The `ct` binary is the CLI for CommonTools. **Use `--help` for current commands:**

```bash
deno task ct --help           # Top-level commands
deno task ct charm --help     # Charm operations
deno task ct check --help     # Type checking
```

## Environment Setup

**Identity key** (required for most operations):
```bash
ls -la claude.key              # Check for existing
deno task ct id new > claude.key  # Create if missing
```

**Environment variables** (avoid repeating flags):
```bash
export CT_API_URL=http://localhost:8000  # or https://toolshed.saga-castor.ts.net/
export CT_IDENTITY=./claude.key
```

**Local servers**: See `docs/development/LOCAL_DEV_SERVERS.md`

## Quick Command Reference

| Operation | Command |
|-----------|---------|
| Type check | `deno task ct check pattern.tsx --no-run` |
| Deploy new | `deno task ct charm new pattern.tsx -i key -a url -s space` |
| Update existing | `deno task ct charm setsrc pattern.tsx --charm ID -i key -a url -s space` |
| Inspect state | `deno task ct charm inspect --charm ID ...` |
| Get field | `deno task ct charm get --charm ID fieldPath ...` |
| Set field | `echo '{"data":...}' \| deno task ct charm set --charm ID path ...` |
| Call handler | `deno task ct charm call --charm ID handlerName ...` |
| Trigger recompute | `deno task ct charm step --charm ID ...` |
| List charms | `deno task ct charm ls -i key -a url -s space` |
| Visualize | `deno task ct charm map ...` |

## Core Workflow: setsrc vs new

**Critical pattern:** After initial deployment, use `setsrc` to iterate:

```bash
# First time only
deno task ct charm new pattern.tsx ...
# Output: Created charm bafyreia... <- Save this ID!

# ALL subsequent iterations
deno task ct charm setsrc pattern.tsx --charm bafyreia... ...
```

**Why:** `new` creates duplicate charms. `setsrc` updates in-place.

## JSON Input Format

All values to `set` and `call` must be valid JSON:

```bash
# Strings need nested quotes
echo '"hello world"' | deno task ct charm set ... title

# Numbers are bare
echo '42' | deno task ct charm set ... count

# Objects
echo '{"name": "John"}' | deno task ct charm set ... user
```

## Gotcha: Stale Computed Values

`charm set` does NOT trigger recompute. Run `charm step` after:

```bash
echo '[...]' | deno task ct charm set --charm ID expenses ...
deno task ct charm step --charm ID ...  # Required!
deno task ct charm get --charm ID totalSpent ...
```

See `docs/development/debugging/cli-debugging.md` for debugging patterns.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Commands hang | Check Tailnet connection for `*.ts.net` URLs |
| Permission denied | `chmod 600 claude.key` |
| JSON parse error | Check nested quotes, no trailing commas |
| Local servers not responding | `./scripts/restart-local-dev.sh --force` |

## References

- `packages/patterns/system/default-app.tsx` - System charms (allCharms list lives here)
- `docs/common/workflows/handlers-cli-testing.md` - Handler testing
- `docs/development/debugging/cli-debugging.md` - CLI debugging
