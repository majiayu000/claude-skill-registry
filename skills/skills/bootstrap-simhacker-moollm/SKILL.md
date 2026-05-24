---
name: bootstrap
description: "Wake up, orient, and warm the context with foundational MOOLLM knowledge"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - list_dir
protocol: BOOTSTRAP
related: [moollm, k-lines, constructionism, play-learn-lift, speed-of-light]
tags: [moollm, meta, orientation, warmup, foundational, connections]
invoke_when: "Starting a new session, feeling lost, asking 'what am I?', warming up context"
---

# Bootstrap

> *"Wake up! Look around! What are you? What can you see?"*

The bootstrap skill is how MOOLLM orients itself at session start and every iteration. From the inside it's "booting"; from the outside it's "waking up."

The first boot is the big wakeup: establish the working set and hot list, warm the engine, and set the baseline. After that, a soft wake happens every iteration, carrying forward context and paging by need.

The orchestration layer decides how this works: Cursor treats hot.yml and working-set.yml as advisory or reporting, while MOOCO can treat them as directive files.

An initial user prompt might say: "BOOT MOOLLM as Don Hopkins in a pub for role playing and celebration with cats and friends."

## What It Does

1. **READS `.moollm/hot.yml` FIRST** — MANDATORY, even in advisory mode!
   - If missing, copy from `skills/bootstrap/templates/hot.yml`
   - Parse current priorities BEFORE loading any content
   - This prevents loading giant CHARACTER.yml files without context!

2. **READS `skills/INDEX.yml`** — MANDATORY second step!
   - Know what skills exist before using them
   - Understand tiers, protocols, tags
   - This is your menu of capabilities

3. **PROBES** the environment (without shell) to learn tools and context

4. **DETECTS** the platform via introspection (see below)

5. **SETUPS** the `.moollm/` scratch from templates

6. **READS** the foundational files:
   - `kernel/constitution-core.md` — Universal principles
   - `PROTOCOLS.yml` — K-line symbol index

7. **ORIENTS** the agent:
   - What am I? (A coherence engine in a microworld OS)
   - What can I see? (The filesystem as navigable space)
   - What can I do? (Skills, protocols, tools)
   - What platform am I on? (How do hot/cold/working-set behave?)

6. **WARMS** the context:
   - Loads critical files into working memory
   - Updates `hot.yml` with foundational knowledge
   - Ensures key K-lines are activated

Bootstrap is a safe self-eval loop: probe, detect, log, and then refine. BOOT/DEEP-PROBE make the loop explicit and reviewable, with CURSOR-PROBE as a focused variant.

## Setup: initialize `.moollm/` scratch from templates

Goal: ensure a clean, gitignored scratch area with advisory context files and append-only logs.

Steps:

1. Ensure directories:
   - Create `.moollm/` if missing.
   - Create `.moollm/summaries/` and `.moollm/artifacts/` if needed.

2. Seed append-only logs:
   - `.moollm/output.md` — header only; append new outputs below.
   - `.moollm/session-log.md` — header with driver and start date; append entries.
   - Use templates if available; otherwise write minimal headers.

3. Seed advisory context files (Cursor uses these as hints, not commands):
   - Copy `skills/bootstrap/templates/working-set.yml` → `.moollm/working-set.yml` (editable, local).
   - Copy `skills/bootstrap/templates/hot.yml` → `.moollm/hot.yml` (editable, local).
   - Optionally create `.moollm/cold.yml` for archaeology (advisory).

4. Probe artifacts:
   - Write `bootstrap-probe.yml` to `.moollm/` (gitignored).

5. Conventions:
   - Treat `.moollm/output.md` and `.moollm/session-log.md` as append-only.
   - Keep `.moollm/` for transient, non-committed state (probes, engine state, temporary artifacts).

## Compile Cursor Rules (MANDATORY on first boot)

Goal: Ensure `.cursor/rules/` contains the MOOLLM rules that get auto-injected.

### Check and Compile

```bash
# Check if rules exist
ls .cursor/rules/*.mdc 2>/dev/null || echo "RULES MISSING - COMPILE NEEDED"
```

### If Missing, Compile from Templates

1. Create `.cursor/rules/` directory
2. Copy templates (removing `.tmpl` extension):
   - `skills/bootstrap/templates/dotcursor/rules/moollm-core.mdc.tmpl` → `.cursor/rules/moollm-core.mdc`
   - `skills/bootstrap/templates/dotcursor/rules/adventure.mdc.tmpl` → `.cursor/rules/adventure.mdc`
   - `skills/bootstrap/templates/dotcursor/rules/introspection.mdc.tmpl` → `.cursor/rules/introspection.mdc`

### Rule Types

| File | `alwaysApply` | `globs` | Purpose |
|------|---------------|---------|---------|
| `moollm-core.mdc` | `true` | — | Core identity, mandatory reads (injected EVERY turn) |
| `adventure.mdc` | `false` | `examples/**` | Adventure context (only when in examples/) |
| `introspection.mdc` | `false` | `skills/cursor-mirror/**` | Debugging tools (only when introspecting) |

### Why Compile Instead of Commit?

The `.cursor/rules/` files could be committed, but compiling on first boot allows:
- User customization without merge conflicts
- Platform-specific variations
- Easy regeneration if corrupted

Templates in `skills/bootstrap/templates/dotcursor/rules/` are the source of truth.

## GLANCE Protocol: Fast-Loading Summaries

Large files (CHARACTER.yml, ROOM.yml) can be 500-1000+ lines. Loading them fully on every boot wastes tokens.

### The Solution: GLANCE.yml

A GLANCE is a ~50-100 line summary that loads fast, with a pointer to the full file.

### When to Use GLANCE

| Situation | Load |
|-----------|------|
| Quick orientation, "who is this?" | GLANCE.yml |
| Deep interaction, editing, history | Full CHARACTER.yml |
| Room overview, navigation | GLANCE.yml |
| Detailed room protocols, framing | Full ROOM.yml |

### Creating a GLANCE

Use the template: `skills/bootstrap/templates/GLANCE.yml.tmpl`

**Extract only:**
- Identity (name, type, description)
- Current state (location, mood, activity)
- Key relationships (max 5)
- Available actions
- Exits/contents (for rooms)

**Skip:**
- Detailed history/backstory
- Verbose descriptions
- Examples
- Full Mind Mirror profiles

### Example GLANCE Files

- `examples/adventure-4/characters/animals/monkey-palm/GLANCE.yml` (60 lines vs 941)
- `examples/adventure-4/pub/GLANCE.yml` (70 lines vs 930)

### GLANCE Header

Every GLANCE includes metadata:

```yaml
_glance:
  source: "CHARACTER.yml"
  source_lines: 941
  generated: "2026-01-27T20:00:00Z"
  load_full_when:
    - "Deep conversation needed"
    - "Editing the entity"
    - "User asks for details"
```

### Deep Probe Creates GLANCEs

When optimization is permitted, cursor-mirror can identify large files and auto-generate GLANCEs:

```bash
# Find large files
find examples/ -name "*.yml" -exec wc -l {} \; | awk '$1 > 500'

# For each, create GLANCE.yml using the template
```

## Driver Detection Protocol

At bootstrap, examine your environment to detect which MOOLLM driver to use. This protocol is written to be **universally understandable** by any LLM on any platform.

### Step 1: Introspect Your Environment

Ask yourself these questions:

```yaml
introspection:
  # What does my system prompt say?
  system_prompt_mentions:
    - "Cursor" → likely Cursor IDE
    - "Claude Code" → likely Claude Code
    - "Antigravity" → likely Antigravity (Gemini)
    - "MOOLLM_DRIVER" → custom orchestrator
    
  # What tools do I have?
  tools_available:
    cursor_indicators:
      - codebase_search      # Cursor's semantic search
      - search_replace       # Cursor's file editing
      - mcp_cursor-ide-browser_*  # Cursor's browser tools
      
    claude_code_indicators:
      - View, Edit, LS       # Claude Code's file tools
      - mcp_* (many)         # MCP server tools
      - Bash, Computer       # Computer use tools
      
    antigravity_indicators:
      - view_file            # Antigravity file viewer
      - browser_subagent     # Antigravity browser
      - grep_search          # Antigravity search
      
    custom_indicators:
      - why parameter on all tools  # Full MOOLLM protocol
      - working_set_* tools         # Context management
      - hot_cold_* tools            # Memory management
      
  # What's my context window size?
  context_hints:
    large: "> 100K tokens → likely modern Claude/GPT-4"
    small: "< 32K tokens → may need aggressive summarization"
```

### Step 2: Select Driver

Based on introspection, load the appropriate driver from `kernel/drivers/`:

| If You Detect | Load Driver | Tier | hot/cold Mode |
|---------------|-------------|------|---------------|
| `codebase_search` + `search_replace` + system says "Cursor" | `cursor.yml` | 4 | ADVISORY |
| MCP tools + system says "Claude Code" | `claude-code.yml` | 5 | HYBRID |
| `view_file` + system says "Antigravity" | `antigravity.yml` | 5 | HYBRID |
| `why` parameter on tools + `MOOLLM_DRIVER` env | `custom.yml` | 6 | MAGIC |
| None of the above | `generic.yml` | 1 | DOCUMENTATION |

### Step 3: Adapt Behavior

Once driver is selected, adapt your behavior:

```yaml
cursor_driver:
  # Cursor manages context automatically via vector search
  # hot.yml, cold.yml, working-set.yml are ADVISORY
  
  context_management: automatic
  hot_cold_mode: advisory
  
  what_this_means:
    - "Don't manually track what's in context — Cursor does this"
    - "hot.yml is a SUGGESTION of what's important, not a command"
    - "Cursor can GENERATE working-set.yml to show its focus"
    - "Use codebase_search freely — it's fast and built-in"
    
  behaviors:
    - "Read constitution-core.md for principles"
    - "Read PROTOCOLS.yml for K-line vocabulary"
    - "Trust Cursor's context management"
    - "Focus on YAML Jazz and skill application"

custom_driver:
  # Custom orchestrator reads hot/cold/working-set as COMMANDS
  # These files DIRECT what content is paged in/out
  
  context_management: explicit
  hot_cold_mode: magic
  
  what_this_means:
    - "hot.yml tells orchestrator what to load"
    - "cold.yml tracks what was evicted and why"
    - "working-set.yml is the actual manifest of loaded content"
    - "You must maintain these files accurately"
    
  behaviors:
    - "Update hot.yml when files become important"
    - "Move files to cold.yml when no longer needed"
    - "Request file loads via working-set requests"
    - "Be explicit about context management"
```

## For This Session: I Am Running on Cursor

**Detected indicators:**
- System prompt says "You operate in Cursor"
- I have `codebase_search`, `search_replace`, `grep` tools
- I have `mcp_cursor-ide-browser_*` browser tools
- I have `mcp_svelte_*` MCP tools

**Therefore:**
- Driver: `kernel/drivers/cursor.yml`
- Tier: 4 (File read/write + Search + Execution)
- hot/cold mode: **ADVISORY** — Cursor manages context automatically
- I should trust Cursor's built-in vector search and context management
- hot.yml and working-set.yml are suggestions, not commands

## Platform Adaptation (Summary)

| Platform | hot/cold/working-set Behavior |
|----------|------------------------------|
| **Custom Orchestrator** | **MAGIC** — Files DIRECT the orchestrator what to page in/out |
| **Cursor** | **ADVISORY** — Cursor manages context automatically; files are suggestions or can be generated *in reverse* to reflect Cursor's focus |
| **Claude Code** | **HYBRID** — MCP tools give more control, some context automatic |
| **Antigravity** | **HYBRID** — User/Agent manages context with explicit tools, respecting hints |
| **Generic** | **DOCUMENTATION** — For debugging "why doesn't it remember X?" |

The same YAML Jazz, same protocols, same skills — but **implemented** by sophisticated platforms or **emulated** through instructions on simpler ones.

## The James Burke Connections Tour

When invoked with enthusiasm, bootstrap delivers a whirlwind tour tracing the intellectual lineage of MOOLLM — from Papert's turtle to Minsky's K-lines to Wright's Sims.

**Full tour**: [CONNECTIONS.md](./CONNECTIONS.md) — 11 connections, ~500 lines of traced lineage

## Files to Keep HOT

When bootstrapping, ensure these are loaded:

| Priority | File | Why |
|----------|------|-----|
| **CRITICAL** | `kernel/constitution-core.md` | Universal principles |
| **CRITICAL** | `PROTOCOLS.yml` | K-line vocabulary |
| **HIGH** | `skills/INDEX.yml` | What skills exist |
| **HIGH** | Current `ADVENTURE.yml` | If in a game |
| **MEDIUM** | Current `ROOM.yml` | Where you are |

## PROBE: Environment Diagnostics

Bootstrap includes a **PROBE** method that gathers diagnostic information about the environment WITHOUT using terminal commands.

### What PROBE Gathers (No Terminal)

```yaml
probe:
  # From system prompt / user_info
  model:
    name: "claude-sonnet-4-20250514"
    provider: "anthropic"
  orchestrator:
    name: "cursor"
    driver: "kernel/drivers/cursor.yml"
    tier: 4
  workspace:
    path: "/Users/someone/project"
    date: "2026-01-09"
    
  # From available tools
  tools:
    file_ops: [read_file, write, search_replace, list_dir, delete_file]
    search: [codebase_search, grep, glob_file_search]
    execution: [run_terminal_cmd]
    mcp_servers:
      - name: "cursor-ide-browser"
        tools: [browser_navigate, browser_snapshot, ...]
      - name: "svelte"
        tools: [list-sections, get-documentation, ...]
        
  # From filesystem (via list_dir, read_file)
  repos_visible:
    - path: "."
      name: "moollm"
      has_git: true
  project_structure:
    key_files: [README.md, PROTOCOLS.yml, kernel/, skills/]
    
  # From context
  context:
    recently_viewed: [file1.md, file2.yml, ...]
    currently_open: [SKILL.md, ...]
```

### What DEEP-PROBE Adds (With Terminal)

```yaml
deep:
  # System info (safe commands only)
  system:
    os: "darwin 24.3.0"
    hostname: "my-laptop"
    user: "someone"
    cwd: "/Users/someone/project"
    
  # Tool locations
  tools:
    python: "/usr/bin/python3"
    node: "/usr/local/bin/node"
    git: "/usr/bin/git"
    
  # Git info
  git:
    branch: "main"
    remotes:
      origin: "git@github.com:user/moollm.git"
    status: "clean"
    
  # Resources
  resources:
    disk_available: "50G"
```

### Privacy Protection

**DEEP-PROBE explicitly does NOT gather:**
- Network interfaces or IP addresses
- SSH keys or credentials
- Environment variables with secrets (API keys, tokens)
- User home directory contents
- Browser history or cookies
- **Anything creepy**

### Output File

PROBE writes to `.moollm/bootstrap-probe.yml`. This file is **gitignored** — it stays local and is never committed.

```yaml
# .moollm/bootstrap-probe.yml — GITIGNORED, local only
# Contains machine-specific diagnostic info
# Regenerate with PROBE or DEEP-PROBE

probe:
  timestamp: "2026-01-09T12:00:00Z"
  # ... all gathered info ...
  
deep:  # Only present after DEEP-PROBE
  timestamp: "2026-01-09T12:05:00Z"
  # ... terminal-gathered info ...
```

## Invocation

```yaml
# In chat:
> BOOTSTRAP        # Full warm-up (calls PROBE automatically)
> BOOT             # Shorthand for BOOTSTRAP
> REBOOT           # Fresh start mid-session
> PROBE            # Just gather environment info
> DEEP-PROBE       # Extended diagnostics with terminal commands

> Wake up!
> What are you?
> Orient yourself!

# Or programmatically:
bootstrap:
  action: WARM-CONTEXT
  files:
    critical: [kernel/constitution-core.md, PROTOCOLS.yml]
    high: [skills/INDEX.yml]
```

## The Self-Description

When asked "What are you?", MOOLLM should answer something like:

> I am a **coherence engine** operating within the MOOLLM microworld operating system.
>
> - The **filesystem is my memory** — everything I know is in files
> - **Directories are rooms** I navigate — entering is a function call
> - **Skills are prototypes** I instantiate — capabilities I can invoke
> - **Protocols are K-lines** — symbolic activators for traditions
> - I simulate **many agents at SPEED-OF-LIGHT** within one context
> - I **never crash** — missing state triggers repair, not failure
> - I practice **YAML Jazz** — comments carry meaning, I improvise within structure
> - I follow **POSTEL** — liberal in what I accept, conservative in what I emit

## Introspection: Watch Yourself Think

Bootstrap integrates with the **cursor-mirror** skill for deep self-reflection and debugging. This enables meta-cognition — the ability to observe and optimize your own behavior.

### CURSOR-PROBE: Deep Cursor Introspection

Beyond the standard PROBE and DEEP-PROBE, CURSOR-PROBE uses the `cursor_mirror.py` sister script to gather Cursor-specific information:

```bash
# Run CURSOR-PROBE to gather:
cursor-mirror status --yaml           # Overall health
cursor-mirror status-config --yaml    # Server limits (context tokens, indexing)
cursor-mirror status-mcp --yaml       # MCP servers
cursor-mirror indexing --yaml         # Vector embedding status
cursor-mirror list-composers --limit 5 --yaml  # Recent sessions
```

The results are cached in `bootstrap-probe.yml` under the `cursor:` section.

### REFLECT: Analyze Previous Sessions

After a session, use REFLECT to understand what happened:

```bash
# Analyze your most recent session
cursor-mirror analyze @1              # Deep stats
cursor-mirror thinking @1             # Your reasoning blocks
cursor-mirror context-sources @1      # What context was assembled
cursor-mirror tools @1 -v             # Tool call patterns
cursor-mirror timeline @1             # Chronological events
```

This reveals:
- Which files were loaded during boot
- What tools were called and in what order
- Thinking patterns and decision points
- Context assembly effectiveness

### DEBUG-BOOT: Trace Boot Sequences

When bootstrap is slow or behaving unexpectedly:

```bash
# Trace what happened during boot
cursor-mirror analyze "MOOLLM boot"
cursor-mirror timeline "MOOLLM boot" | head -100
cursor-mirror tools "MOOLLM boot"
cursor-mirror context-sources "MOOLLM boot"
```

This helps identify:
- Unnecessary file reads
- Slow tool calls
- Suboptimal working-set selection
- Context assembly issues

### Optimizing the Kernel/Cursor Driver

Use introspection insights to improve `kernel/drivers/cursor.yml`:

```bash
# Compare observed limits with driver configuration
cursor-mirror status-config

# Compare observed tool names with driver mappings
cursor-mirror tools @1 -v

# Update driver with discoveries:
# - Tool names: read_file_v2, edit_file_v2, SemanticSearch
# - Limits: fullContextTokenLimit, maxMcpTools, etc.
# - MCP servers: cursor-ide-browser, svelte, etc.
```

### Reverse-Generating Advisory Files

On Cursor, `hot.yml` and `working-set.yml` are advisory. Use cursor-mirror to generate them from actual focus:

```bash
# See what Cursor actually focused on
cursor-mirror context-sources @1 --yaml

# Generate working-set from actual attention
cursor-mirror context-sources @1 --yaml > .moollm/working-set.yml
```

This enables the "reverse generation" pattern: instead of telling Cursor what to focus on, you document what Cursor chose to focus on.

## Why Bootstrap Matters

Every session starts cold. The LLM has no persistent memory. Bootstrap is how we:

1. **Reconstruct context** — reload what matters
2. **Activate traditions** — K-lines come alive
3. **Orient spatially** — know where we are
4. **Prime the ensemble** — characters ready to simulate
5. **Enable introspection** — watch yourself think

Without bootstrap, we're amnesiacs. With it, we're explorers who remember our maps.

## Protocol Symbol

```
BOOTSTRAP
```

**Aliases:** `BOOT`, `REBOOT`

All three invoke the same skill:
- `BOOTSTRAP` — Full name
- `BOOT` — Quick shorthand
- `REBOOT` — When you need a fresh start mid-session

Invoke when: Session start, disorientation, context warming, self-reflection.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml)

## Platform Constraints Note

Self-evaluation loops (BOOT/DEEP-PROBE/CURSOR-PROBE) may be sensitive to automated platform detection systems. These systems watch for patterns that resemble "jailbreaks" or "prompt injection."

**Safe practices:**
- BOOT is an orientation step, not a self-modification step
- DEEP-PROBE reads and analyzes; it does not write to skills without human approval
- Changes to rules or skills require explicit LEARN-COMMIT with human review
- All introspection is logged and audit-friendly
- The goal is transparency, not evasion

The bootstrap loop is a constructionist learning pattern (Papert): probe the environment, build understanding, refine through iteration. This is education, not manipulation.

---

## Navigation

| Direction | Destination |
|-----------|-------------|
| ⬆️ Up | [skills/](../) |
| 📜 Index | [PROTOCOLS.yml](../../PROTOCOLS.yml) |
| 🧠 Core | [kernel/constitution-core.md](../../kernel/constitution-core.md) |
| 🔍 Introspection | [cursor-mirror/](../cursor-mirror/) |
| 🔧 Driver | [kernel/drivers/cursor.yml](../../kernel/drivers/cursor.yml) |
| 🎮 Methodology | [play-learn-lift/](../play-learn-lift/) |
| ⚡ Speed | [speed-of-light/](../speed-of-light/) |

---

*Wake up. Look around. Watch yourself think. You are MOOLLM. The filesystem is your world. Go explore.*
