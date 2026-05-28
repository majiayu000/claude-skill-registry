---
name: playtesting
description: Headed playtesting workflow for Godot projects, focused on HPV runs with MCP, runtime eval teleporting, and efficient logging. Trigger any time the Godot-tools extension is used, anytime the Godot MCP is used, whenever Playtester role is use. Use when you need to validate quest flow, UI playability, or record HPV findings in PLAYTESTING_ROADMAP.md.
---

# Playtesting HPV Skill

Use this skill to run headed playability validation (HPV) quickly with MCP while keeping calls and tokens low. Teleport-assisted flow is the default unless a full walk is requested.

## How You "See" the Game State

**You have complete visibility into the game - you are NOT "blind."**

### Vision Tools Available

| Tool | What It Shows | How To Use |
|------|---------------|----------|
| **get_runtime_scene_structure** | Full scene tree with positions, visibility, properties | Primary vision tool |
| **Debugger Variables panel** | All runtime variables (flags, inventory, positions) | For detailed inspection |
| **Runtime eval patterns** | Direct access to specific nodes/values | For quick access/teleport |

### Example: Seeing Player Position

```bash
get_runtime_scene_structure
# Returns: World/Player: position=[384, 96], visible=true
```

### Example: Seeing NPC Positions

```bash
get_runtime_scene_structure
# Returns: World/NPCs/Hermes: position=[400, 100], visible=true
# Returns: World/NPCs/Aeetes: position=[512, 96], visible=true
```

### Example: Checking Quest State

**Method 1: Debugger** (easiest)
1. Press F5 to start debugging
2. Set breakpoint anywhere
3. Check Variables panel → `quest_flags` dictionary

**Method 2: MCP** (when game running)
```bash
get_runtime_scene_structure
# Look for: World/GameState → quest_flags in properties
```

### Navigation

**Option 1: Teleport** (fastest for HPV testing)
```gdscript
get_tree().root.get_child(3).get_node("Player").set_global_position(Vector2(384, 96))
```

**Option 2: Walk** (for movement testing)
```bash
simulate_action_tap --action ui_up
# Verify position with: get_runtime_scene_structure
```

**Key Point:** `get_runtime_scene_structure` IS your vision - it shows every node's position, visibility, and properties in real-time. Use it to know where things are and navigate efficiently.

---

## Minimal Workflow
1. Run project headed (MCP).
2. Get runtime scene structure once.
3. Identify the active scene root (world or location).
4. If `DialogueBox` is visible, clear it (player `interact` is ignored while dialogue is open).
5. Teleport to target, interact, and advance dialogue with batched inputs.
6. Verify state (DialogueBox text, marker visibility, flags).
7. Log findings in PLAYTESTING_ROADMAP.md.

## MCP Verification Checklist

**Before starting HPV playtesting, always verify MCP is working:**

```bash
# Step 1: Run health check
powershell -ExecutionPolicy Bypass -File scripts/mcp-health-check.ps1

# Step 2: If not healthy, run recovery
powershell -ExecutionPolicy Bypass -File .claude/skills/mcp-recovery/scripts/recover.ps1

# Step 3: Start game (see Agent-Specific Commands below)
# Step 4: Verify connection (see Agent-Specific Commands below)
```

**Health Check Status:**
- `healthy` → Proceed with playtesting
- `degraded` → Follow recommendations, then recheck
- `down` → Run recovery script

**For automated recovery:** Use `/mcp-recover` skill or see `HPV_GUIDE.md` for manual procedures.

## Agent-Specific MCP Commands

**IMPORTANT: Different agent types use DIFFERENT commands for MCP access.**

### For IDE Extension Agents (Cursor, VS Code)
Use the **PowerShell wrapper** for all MCP CLI commands:

```bash
# Start game
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'run_project --headed'"

# Verify connection
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'get_runtime_scene_structure' -Quiet"

# Get scene structure
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'get_runtime_scene_structure' -Quiet"

# Simulate input
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'simulate_action_tap --action ui_accept'"

# Execute editor script
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'execute_editor_script --code GameState.new_game()'"
```

**See:** [docs/agent-instructions/tools/mcp-wrapper-usage.md](docs/agent-instructions/tools/mcp-wrapper-usage.md)

### For Terminal Agents (RooCode, GPT Codex)
Use **direct npx CLI commands**:

```bash
# Start game
npx -y godot-mcp-cli@latest run_project --headed

# Verify connection
npx -y godot-mcp-cli@latest get_runtime_scene_structure
```

### For Desktop Agents
Use **native MCP tools** (`mcp__godot__*`) directly.

**DO NOT use PowerShell wrapper** (you have native access).

## Efficiency Rules (Core)
- Batch inputs with 400-800 ms waits, then verify once.
- Cache node paths early; avoid repeated scene tree dumps.
- Gate actions on state checks (DialogueBox visible, marker visible, flags).
 - Prefer teleporting to targets unless a full walk is required.
 - Reminder: `_unhandled_input` exits early when `DialogueBox.visible == true`, so `interact` won't fire until dialogue is closed.

## Teleport Pattern (Expression-Only)
Use method calls in eval (no var or assignment). Examples:

- Find world by name when available:
  get_tree().root.find_child("World", true, false)

- Teleport the player (replace WORLD_INDEX if needed):
  get_tree().root.get_child(WORLD_INDEX).get_node("Player").set_global_position(Vector2(384, 64))

- Trigger a quest area:
  get_tree().root.get_child(WORLD_INDEX).get_node("QuestTriggers/Quest10")._on_body_entered(get_tree().root.get_child(WORLD_INDEX).get_node("Player"))

- Read dialogue text:
  get_tree().root.get_child(WORLD_INDEX).get_node("UI/DialogueBox/Panel/Text").text

## Logging Checklist
- Scope (quest range, shortcuts used, minigames skipped or not)
- What worked and what failed
- Any blockers and repro steps
- Next steps for the next playtester

## MCP CLI Access (IMPORTANT)

**See "Agent-Specific MCP Commands" section above for your agent type.**

**Quick reference:**
- **IDE Extension agents** → Use PowerShell wrapper (`scripts/mcp-wrapper.ps1`)
- **Terminal agents** → Use direct npx CLI
- **Desktop agents** → Use native MCP tools

**Do NOT look for `mcp__godot__*` tools** if you're an IDE extension agent - they don't exist in your environment. Use the PowerShell wrapper instead.

## MCP Command Quick Reference

### Game Control

**For IDE Extension Agents (PowerShell wrapper):**
```bash
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'run_project --headed'"
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'stop_running_project' -Quiet"
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'get_runtime_scene_structure' -Quiet"
powershell -Command "scripts/mcp-wrapper.ps1 -McpCommand 'simulate_action_tap --action ui_accept'"
```

**For Terminal Agents (direct npx):**
```bash
npx -y godot-mcp-cli@latest run_project --headed              # Start game
npx -y godot-mcp-cli@latest stop_running_project              # Stop game
npx -y godot-mcp-cli@latest get_runtime_scene_structure       # Inspect live scene
npx -y godot-mcp-cli@latest simulate_action_tap --action "ui_accept" # Press button
```

### Input Actions (Common)
- `ui_accept` - Confirm/advance dialogue (A button / Enter)
- `ui_cancel` - Cancel/skip cutscene (B button / Esc)
- `ui_up`/`ui_down`/`ui_left`/`ui_right` - Movement/navigation
- `interact` - Interact with objects (E key)

### Runtime Eval Patterns
```gdscript
# Get world (typically index 3 or 4 - check with get_runtime_scene_structure)
get_tree().root.get_child(WORLD_INDEX)

# Set quest flag
GameState.set_flag("quest_2_active", true)

# Check flag
GameState.get_flag("quest_2_active")

# Give item
GameState.add_item("herb_id", 1)

# Teleport player
get_tree().root.get_child(WORLD_INDEX).get_node("Player").set_global_position(Vector2(x, y))

# Read dialogue text
get_tree().root.get_child(WORLD_INDEX).get_node("UI/DialogueBox/Panel/Text").text

# Trigger quest manually
get_tree().root.get_child(WORLD_INDEX).get_node("QuestTriggers/Quest2")._on_body_entered(get_tree().root.get_child(WORLD_INDEX).get_node("Player"))
```

## Common Node Paths (Circe's Garden)

### World Structure
- World: `get_tree().root.get_child(3)` or `get_child(4)` - verify with get_runtime_scene_structure
- Player: `World/Player`
- UI: `World/UI`
- DialogueBox: `World/UI/DialogueBox`
- Dialogue Text: `World/UI/DialogueBox/Panel/Text`
- Choices Container: `World/UI/DialogueBox/Panel/Choices`

### Quest Triggers
- `World/QuestTriggers/Quest0` through `World/QuestTriggers/Quest11`
- `World/QuestTriggers/Epilogue`

### NPCs (Common)
- `World/NPCs/Hermes`
- `World/NPCs/Aeetes`
- `World/NPCs/Circe`
- `World/NPCs/Daedalus`
- `World/NPCs/Scylla`

### Interaction Points
- House Door: `World/Interactables/HouseDoor`
- Boat: `World/Interactables/Boat`
- Note: `World/Interactables/AeetesNote`

## Quest Flags Reference

### Progression Flags
- `prologue_complete` - Prologue finished
- `met_hermes` - Hermes first interaction
- `quest_N_active` - Quest N started
- `quest_N_complete` - Quest N finished

### Story State
- `scylla_petrified` - Bad ending achieved
- `ending_witch` - Witch ending chosen
- `ending_healer` - Healer ending chosen
- `game_complete` - Game finished
- `free_play_unlocked` - Post-game unlocked

### Item Flags
- `has_herb_id` - Herb identification item
- `has_sap` - Extracted sap
- `has_calming_draught` - Crafted calming draught
- `has_reversal_elixir` - Crafted reversal elixir
- `has_binding_ward` - Crafted binding ward
- `petrification_potion` - Final quest item

## Minigame Skip Flags (For Testing)
Set these via eval to skip minigames during HPV:
- `quest_1_complete` - Skip herb ID minigame
- `quest_2_complete` - Skip sap extraction
- `quest_4_complete` - Skip farming
- `quest_5_complete` - Skip calming draught crafting
- `quest_6_complete` - Skip reversal elixir crafting
- `quest_7_complete` - Skip binding ward crafting
- `quest_8_complete` - Skip final crafting

## In This Repo
- Log in docs/playtesting/PLAYTESTING_ROADMAP.md
- HPV uses MCP or manual playthrough; avoid headless tests for playability
- Minigames are typically skipped unless explicitly requested
- Godot 4.5.1, project at `C:/Users/Sam/Documents/GitHub/v2_heras_garden/`
