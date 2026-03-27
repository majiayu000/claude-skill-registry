---
name: phx:init
description: Initialize Elixir/Phoenix plugin in a project. Installs auto-activation rules into CLAUDE.md for complexity detection, interview mode, Iron Laws enforcement, and reference auto-loading.
effort: low
argument-hint: [--update]
---

# Plugin Initialization

Install the Elixir/Phoenix plugin's behavioral instructions into the project's CLAUDE.md.

## Usage

```
/phx:init           # First-time installation
/phx:init --update  # Update existing installation with latest rules
```

## Workflow

### Step 1: Check Existing CLAUDE.md

```bash
# Check if CLAUDE.md exists
ls -la CLAUDE.md 2>/dev/null

# Check for existing plugin installation
grep -q "ELIXIR-PHOENIX-PLUGIN:START" CLAUDE.md 2>/dev/null
```

### Step 2: Detect Project Stack

Scan the project to customize the injected instructions:

```bash
# Phoenix version
grep -oP 'phoenix.*"~> \K[0-9.]+' mix.exs 2>/dev/null || echo "unknown"

# Ecto version
grep -oP 'ecto.*"~> \K[0-9.]+' mix.exs 2>/dev/null || echo "unknown"

# Oban detection
grep -q '"oban"' mix.exs && echo "oban"
grep -q '"oban_pro"' mix.exs && echo "oban_pro"

# Framework detection
grep -q '"ash"' mix.exs && echo "ash"
grep -q '"surface"' mix.exs && echo "surface"

# Tidewave detection
grep -q '"tidewave"' mix.exs && echo "tidewave"

# Project size
find lib -name "*.ex" 2>/dev/null | wc -l
```

### Step 3: Handle Installation Modes

**Mode A: Fresh Install** (no CLAUDE.md or no markers)

1. Create/append to CLAUDE.md
2. Insert full behavioral instructions between markers
3. Include only relevant sections based on detected stack

**Mode B: Update** (`--update` flag or markers exist)

1. Find content between `<!-- ELIXIR-PHOENIX-PLUGIN:START -->` and `<!-- ELIXIR-PHOENIX-PLUGIN:END -->`
2. Replace with latest behavioral instructions
3. Preserve everything outside the markers

### Step 4: Generate Content

Write the following structure to CLAUDE.md:

```markdown
<!-- ELIXIR-PHOENIX-PLUGIN:START -->
<!-- Last updated: {date} | Plugin version: 1.0 | Stack: Phoenix {version}, Ecto {version}, {optional: Oban, Tidewave} -->

# Elixir/Phoenix Plugin - Auto-Activation Rules

{Include all sections from the Content Template below, filtered by detected stack}

<!-- ELIXIR-PHOENIX-PLUGIN:END -->
```

### Step 5: Output Summary

```
✅ Elixir/Phoenix plugin initialized

Detected stack:
- Phoenix {version}
- Ecto {version}
- {Oban standard | Oban Pro | not detected}
- {Tidewave ✓ | Tidewave not detected}
- {Ash Framework detected - Ecto patterns disabled | not detected}

Added to CLAUDE.md:
- Auto-activation rules (complexity detection, interview mode)
- Agent trigger patterns ({n} agents available)
- Reference auto-loading ({n} reference docs)
- Iron Laws enforcement ({n} laws)
- Verification rules

Run /phx:init --update after plugin updates.
Run /phx:audit for a full project health check.
```

## Content Template

The exact content to inject is in `${CLAUDE_SKILL_DIR}/references/injectable-template.md`.

**Key structure:**

1. **7-Step Mandatory Procedure** — Claude Code MUST execute before every response
2. **Iron Laws** — STOP behavior on violations
3. **Conditional Sections** — Include based on detected stack:
   - `{OBAN_SECTION}` — If Oban detected (not Pro)
   - `{OBAN_PRO_SECTION}` — If Oban Pro detected
   - `{ASH_SECTION}` — If Ash Framework detected
   - `{TIDEWAVE_SECTION}` — If Tidewave detected
4. **Verification** — Mandatory after code changes
5. **Quick Reference** — Skill routing table

**Placeholder substitution:**

| Placeholder | Source |
|-------------|--------|
| `{DATE}` | Current date |
| `{PHOENIX_VERSION}` | From mix.exs |
| `{ECTO_VERSION}` | From mix.exs |
| `{OPTIONAL_STACK}` | Detected optional deps |

See `${CLAUDE_SKILL_DIR}/references/injectable-template.md` for full template with all placeholders and conditional sections.

## Validation

After running `/phx:init`:

1. Check CLAUDE.md contains markers
2. Verify detected stack matches actual project
3. New session should:
   - Auto-detect complexity when given tasks
   - Stop on Iron Law violations
   - Offer relevant workflows based on task

## Error Handling

| Scenario | Action |
|----------|--------|
| CLAUDE.md read-only | Error: "Cannot modify CLAUDE.md - check permissions" |
| Markers corrupted | Warn, offer to remove and reinstall |
| Unknown Phoenix version | Use conservative defaults (all features enabled) |
| Not an Elixir project | Error: "No mix.exs found - is this an Elixir project?" |

## Relationship to Other Commands

| Command | When to Use |
|---------|-------------|
| `/phx:init` | First time, or after plugin updates |
| `/phx:audit` | Periodic project health check |
| `/phx:verify` | After code changes |
