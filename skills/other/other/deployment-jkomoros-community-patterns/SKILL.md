---
name: deployment
description: >
  Deploy and update patterns. Use when deploying new patterns, updating
  existing deployments, or testing syntax. Includes deployment commands
  and the first custom pattern celebration.
---

# Pattern Deployment

## ⚠️ CRITICAL DEPLOYMENT RULES

**These are CRITICAL and MUST be followed every time:**

1. **✅ ALWAYS use `http://localhost:8000`** - This is the toolshed (backend) server
2. **❌ NEVER use `http://localhost:5173`** - That's the shell (frontend), patterns won't work there
3. **✅ ALWAYS include space name in URL:** `http://localhost:8000/SPACE-NAME/CHARM-ID`
4. **❌ NEVER use:** `http://localhost:8000/CHARM-ID` (missing space name)
5. **✅ ALWAYS include ALL THREE parameters:** `--api-url`, `--identity`, `--space`
6. **✅ ALWAYS use `./scripts/ct`** - The wrapper script that handles directory changes

**If you violate these rules, the pattern will not work. No exceptions.**

## 🚨 NEVER USE `piece setsrc` - ALWAYS USE `piece new`

**This is the #1 cause of broken piece instances.**

`piece setsrc` has a known framework bug that corrupts piece state. Symptoms include:
- Piece shows blank when navigated to directly
- Conflict errors during updates
- Piece data exists but UI won't render

**ALWAYS deploy fresh instances with `piece new` instead.** Each deployment gets a new piece ID - this is expected and correct. See the "Update Deployed Pattern" section below.

## Test Syntax

Before deploying, check that your pattern compiles correctly:

```bash
./scripts/ct dev patterns/$GITHUB_USER/pattern.tsx --no-run
```

This verifies:
- TypeScript types are correct
- All imports resolve
- Pattern structure is valid
- No syntax errors

## Deploy Pattern

Deploy a new pattern instance:

```bash
./scripts/ct piece new \
  --api-url http://localhost:8000 \
  --identity ../labs/claude.key \
  --space claude-my-pattern-1130-1 \
  patterns/$GITHUB_USER/pattern.tsx
```

**⚠️ ALL THREE PARAMETERS ARE REQUIRED:**
- `--api-url http://localhost:8000` - MUST be 8000 (toolshed), NOT 5173 (shell)
- `--identity ../labs/claude.key` - Path to identity key in labs directory
- `--space claude-<pattern>-<MMDD>-<N>` - Use descriptive space names (see naming convention below)

**Space Naming Convention:**
```
claude-<pattern-name>-<MMDD>-<counter>
```
Examples: `claude-counter-1130-1`, `claude-gmail-importer-1201-2`

This outputs a piece ID like `baedreicqpqie6td...`

**View in browser:**
```
http://localhost:8000/SPACE-NAME/CHARM-ID
```

**⚠️ CRITICAL URL FORMAT:**
- ✅ CORRECT: `http://localhost:8000/SPACE-NAME/CHARM-ID`
- ❌ WRONG: `http://localhost:8000/CHARM-ID` (missing space name)
- ❌ WRONG: `http://localhost:5173/SPACE-NAME/CHARM-ID` (wrong port)
- ❌ WRONG: `http://localhost:5173/CHARM-ID` (wrong port AND missing space)

## First Custom Pattern Deployment

When a user successfully deploys their first custom pattern (one they created or significantly modified themselves, not an unchanged example pattern), inform them they are invited to join the CommonTools Discord community at https://common.tools/friends. The entry password is "pattern-weaver". Present this invitation in a distinctive and celebratory way (use your judgment for formatting and presentation). Include that it's a place to ask questions, share patterns and tips, and connect with other builders.

## Update Deployed Pattern

**⚠️ DO NOT USE `piece setsrc` - Known Framework Bug**

There is a known framework bug that causes conflicts when using `piece setsrc`.
**Instead, always deploy a fresh instance with `piece new`:**

```bash
# ❌ DON'T DO THIS - has conflicts due to framework bug
# ./scripts/ct piece setsrc ...

# ✅ DO THIS INSTEAD - deploy a new instance
./scripts/ct piece new \
  --api-url http://localhost:8000 \
  --identity ../labs/claude.key \
  --space claude-my-pattern-1130-1 \
  patterns/$GITHUB_USER/pattern.tsx
```

**This gives you a new piece ID.** Use the new piece ID going forward.

**Why not setsrc?**
- Known framework bug causes conflict errors
- Updates frequently fail
- Cryptic error messages about state conflicts
- `piece new` is reliable and always works

**See superstition:** `community-docs/superstitions/2025-11-22-deployment-setsrc-conflicts-use-new-instead.md`

## Inspect Pattern

See pattern details:

```bash
./scripts/ct piece inspect \
  --api-url http://localhost:8000 \
  --identity ../labs/claude.key \
  --space claude-my-pattern-1130-1 \
  --piece PIECE-ID
```

## Environment Variables

You can set these to avoid repeating flags:

```bash
export CT_API_URL=http://localhost:8000
export CT_IDENTITY=../labs/claude.key

# Then just:
./scripts/ct piece new --space claude-counter-1130-1 patterns/$GITHUB_USER/pattern.tsx
```

## Deployment Troubleshooting

**Pattern not loading after deployment?**

Check these in order:

1. **Wrong port?** MUST be `:8000` NOT `:5173`
   - ✅ `http://localhost:8000/...`
   - ❌ `http://localhost:5173/...`

2. **Missing space name in URL?**
   - ✅ `http://localhost:8000/SPACE-NAME/CHARM-ID`
   - ❌ `http://localhost:8000/CHARM-ID`

3. **Missing required parameters in deploy command?**
   - ALL THREE REQUIRED: `--api-url`, `--identity`, `--space`
   - Check your command includes all three

4. **Used `piece setsrc`?**
   - DON'T use setsrc (framework bug)
   - Use `piece new` instead

**Servers not running?**
```bash
# Check if servers are up
lsof -ti:8000  # Toolshed (backend) - REQUIRED
lsof -ti:5173  # Shell (frontend) - REQUIRED

# Start if needed (use the labs restart script)
../labs/scripts/restart-local-dev.sh --force
```

**Pattern not updating after changes?**
1. **Deploy a NEW instance** with `piece new` (DON'T use setsrc)
2. You'll get a new charm ID - use that one
3. Hard refresh browser: Cmd+Shift+R (Mac), Ctrl+Shift+R (Windows)

**Identity key missing?**
```bash
# Check it exists in labs directory
ls ../labs/claude.key

# If missing, recreate it
cd ../labs && deno task ct id new > claude.key && chmod 600 claude.key && cd -
```

## Related Skills

- **testing** - Test deployed patterns with Playwright
- **pattern-development** - Development best practices
- **session-startup** - Ensure dev servers are running
