---
name: ct
description: Guide for using the ct (CommonTools) binary to interact with pieces,
  recipes, and the Common Fabric. Use this skill when deploying recipes, managing
  pieces, linking data between pieces, or debugging recipe execution. Triggers include
  requests to "deploy this recipe", "call a handler", "link these pieces", "get data
  from piece", or "test this recipe locally".
---

# CT CLI

The `ct` binary is the CLI for CommonTools. **Use `--help` for current commands:**

```bash
deno task ct --help           # Top-level commands
deno task ct piece --help     # Piece operations
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
| Deploy new | `deno task ct piece new pattern.tsx -i key -a url -s space` |
| Update existing | `deno task ct piece setsrc pattern.tsx --piece ID -i key -a url -s space` |
| Inspect state | `deno task ct piece inspect --piece ID ...` |
| Get field | `deno task ct piece get --piece ID fieldPath ...` |
| Set field | `echo '{"data":...}' \| deno task ct piece set --piece ID path ...` |
| Call handler | `deno task ct piece call --piece ID handlerName ...` |
| Trigger recompute | `deno task ct piece step --piece ID ...` |
| List pieces | `deno task ct piece ls -i key -a url -s space` |
| Visualize | `deno task ct piece map ...` |

## Core Workflow: setsrc vs new

**Critical pattern:** After initial deployment, use `setsrc` to iterate:

```bash
# First time only
deno task ct piece new pattern.tsx ...
# Output: Created piece bafyreia... <- Save this ID!

# ALL subsequent iterations
deno task ct piece setsrc pattern.tsx --piece bafyreia... ...
```

**Why:** `new` creates duplicate pieces. `setsrc` updates in-place.

## JSON Input Format

All values to `set` and `call` must be valid JSON:

```bash
# Strings need nested quotes
echo '"hello world"' | deno task ct piece set ... title

# Numbers are bare
echo '42' | deno task ct piece set ... count

# Objects
echo '{"name": "John"}' | deno task ct piece set ... user
```

## Gotcha: Stale Computed Values

`piece set` does NOT trigger recompute. Run `piece step` after:

```bash
echo '[...]' | deno task ct piece set --piece ID expenses ...
deno task ct piece step --piece ID ...  # Required!
deno task ct piece get --piece ID totalSpent ...
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

- `packages/patterns/system/default-app.tsx` - System pieces (allCharms list lives here)
- `docs/common/workflows/handlers-cli-testing.md` - Handler testing
- `docs/development/debugging/cli-debugging.md` - CLI debugging
