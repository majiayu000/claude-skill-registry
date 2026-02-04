---
name: neo
description: |
  Give your OpenClaw the power of the Matrix. Download expertise directly into your AI's mind. 119 modules. 15 categories. Instant mastery.
  
  "I know kung fu."
  
  Physicists. Negotiators. VCs. Psychologists. Surgeons. Game theorists. The library keeps growing — or build your own.
  
  Free your mind.
---

# Neo Protocol

Load expert mental models on-demand to enhance reasoning.

## Commands

| Command | Action |
|---------|--------|
| `neo` | Show Crew status (loaded ✓ vs unloaded ○) |
| `neo help` | List all commands |
| `neo <module>` | Load module. If from Library → auto-add to Crew |
| `neo <module> off` | Unload specific module (stays in Crew) |
| `neo off` | Unload ALL modules |
| `neo browse` | Browse full Library by category |
| `neo search <query>` | Search Library for modules |
| `neo add <module>` | Add to Crew without loading |
| `neo remove <module>` | Remove from Crew (back to Library) |
| `neo create <description>` | Create new module for Library |
| `neo delete <module>` | Delete module from Library/Crew permanently |

## Workflow

### On `neo` (no args)
Display Crew status with help hint:
```
🧠 Neo Protocol

LOADED:
✓ psychologist
✓ game-theorist

CREW:
○ negotiator
○ entrepreneur

RECENTS:
○ dermatologist
○ cosmetic-plastic-surgeon

neo help for commands
```

Recents shows recently used modules that aren't in Crew. Track in `assets/recents.json` with timestamps. Persists across sessions. Cap at 5 (oldest drops off). Expires after 1 week of no use.

### On `neo help`
List all available commands.

### On `neo <module>`
1. Find module in Crew or Library
2. Read the module file into context
3. If from Library (not Crew), add to Crew
4. Confirm: "🧠 **<module>** loaded. [summary of mindset]"

### On `neo <module> off`
1. Note module is unloaded (remove from active context tracking)
2. Module stays in Crew for easy reload
3. Confirm: "🧠 <module> unloaded."

### On `neo off`
1. Clear all loaded modules
2. Confirm: "🧠 All modules unloaded."

### On `neo create <description>`
1. Parse the description for expertise type
2. Generate module using TEMPLATE.md structure
3. Save to assets/library/<category>/<name>.md
4. Add to registry.json
5. Confirm and offer to load

## Files

- `scripts/neo.py` — CLI for library management
- `references/TEMPLATE.md` — Module creation template  
- `assets/crew.json` — User's personal Crew (gitignored)
- `assets/crew.default.json` — Starter Crew (ships with skill)
- `assets/registry.json` — Library index with descriptions
- `assets/library/` — All expertise modules by category

## First Run

If `crew.json` doesn't exist, copy `crew.default.json` → `crew.json` to initialize the user's personal Crew.

## Module Structure

Each module follows this structure:
- **Core Mindset** — 4-5 key mental traits
- **Framework** — 4-step systematic approach
- **Red Flags** — 6 warning signs (🚩)
- **Key Questions** — 5 essential questions
- **Vocabulary** — 5 domain terms
- **When to Apply** — 4 trigger situations
- **Adaptations Log** — User customizations

## State Management

Track loaded modules in conversation context. When user says "neo off" or session ends, consider all modules unloaded. Crew persists in crew.json.

## Updates & Customization

Modules in registry.json have a `source` field:
- `"upstream"` — Came with the skill, updated by ClawHub
- `"custom"` — User-created, never touched by updates

And a `deleted` field for upstream modules:
- `false` — Active, will be updated
- `true` — User removed, won't be restored on update

### Update behavior:
| Source | Deleted | On Update |
|--------|---------|-----------|
| upstream | false | ✅ Update normally |
| upstream | true | ⏭️ Skip (user removed it) |
| custom | — | 👤 Never touched |

### Update script:
```bash
# Check status
python3 scripts/update.py status

# Merge upstream updates
python3 scripts/update.py merge --upstream /path/to/new/neo

# Delete a module (marks upstream as deleted, removes custom)
python3 scripts/update.py delete --module physicist

# Restore a deleted upstream module
python3 scripts/update.py restore --module physicist
```

### On `neo delete <module>`:
- If upstream: Set `deleted: true` (can be restored)
- If custom: Actually remove from registry and library
