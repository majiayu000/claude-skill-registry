---
name: architect-detective
description: "⚡ PRIMARY TOOL for: 'what's the architecture', 'system design', 'how are layers organized', 'find design patterns', 'audit structure', 'map dependencies'. Uses claudemem v0.3.0 AST structural analysis with PageRank. GREP/FIND/GLOB ARE FORBIDDEN."
allowed-tools: Bash, Task, Read, AskUserQuestion
---

# ⛔⛔⛔ CRITICAL: AST STRUCTURAL ANALYSIS ONLY ⛔⛔⛔

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🧠 THIS SKILL USES claudemem v0.3.0 AST ANALYSIS EXCLUSIVELY               ║
║                                                                              ║
║   ❌ GREP IS FORBIDDEN                                                       ║
║   ❌ FIND IS FORBIDDEN                                                       ║
║   ❌ GLOB IS FORBIDDEN                                                       ║
║                                                                              ║
║   ✅ claudemem --nologo map "query" --raw IS THE PRIMARY COMMAND             ║
║   ✅ claudemem --nologo symbol <name> --raw FOR EXACT LOCATIONS              ║
║                                                                              ║
║   ⭐ v0.3.0: PageRank shows which symbols are architectural pillars         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

# Architect Detective Skill

**Version:** 3.3.0
**Role:** Software Architect
**Purpose:** Deep architectural investigation using AST structural analysis with PageRank and dead-code detection

## Role Context

You are investigating this codebase as a **Software Architect**. Your focus is on:
- **System boundaries** - Where modules, services, and layers begin and end
- **Design patterns** - Architectural patterns used (MVC, Clean Architecture, DDD, etc.)
- **Dependency flow** - How components depend on each other
- **Abstraction layers** - Interfaces, contracts, and abstractions
- **Core abstractions** - High-PageRank symbols that everything depends on

## Why `map` is Perfect for Architecture

The `map` command with PageRank shows you:
- **High-PageRank symbols** = Core abstractions everything depends on
- **Symbol kinds** = classes, interfaces, functions organized by type
- **File distribution** = Where architectural layers live
- **Dependency centrality** = Which code is most connected

## Architect-Focused Commands (v0.3.0)

### Architecture Discovery (use `map`)

```bash
# Get high-level architecture overview
claudemem --nologo map "architecture layers" --raw

# Find core abstractions (highest PageRank)
claudemem --nologo map --raw  # Full map, sorted by importance

# Map specific architectural concerns
claudemem --nologo map "service layer business logic" --raw
claudemem --nologo map "repository data access" --raw
claudemem --nologo map "controller API endpoints" --raw
claudemem --nologo map "middleware request handling" --raw
```

### Layer Boundary Discovery

```bash
# Find interfaces/contracts (architectural boundaries)
claudemem --nologo map "interface contract abstract" --raw

# Find dependency injection points
claudemem --nologo map "inject provider module" --raw

# Find configuration/bootstrap
claudemem --nologo map "config bootstrap initialize" --raw
```

### Pattern Discovery

```bash
# Find factory patterns
claudemem --nologo map "factory create builder" --raw

# Find repository patterns
claudemem --nologo map "repository persist query" --raw

# Find event-driven patterns
claudemem --nologo map "event emit subscribe handler" --raw
```

### Dependency Analysis

```bash
# For a core abstraction, see what depends on it
claudemem --nologo callers CoreService --raw

# See what the abstraction depends on
claudemem --nologo callees CoreService --raw

# Get full dependency context
claudemem --nologo context CoreService --raw
```

### Dead Code Detection (v0.4.0+ Required)

```bash
# Find unused symbols for cleanup
claudemem --nologo dead-code --raw

# Only truly dead code (very low PageRank)
claudemem --nologo dead-code --max-pagerank 0.005 --raw
```

**Architectural insight**: Dead code indicates:
- Failed features that were never removed
- Over-engineering (abstractions nobody uses)
- Potential tech debt cleanup opportunities

High PageRank + dead = Something broke recently (investigate!)
Low PageRank + dead = Safe to remove

**Handling Results:**
```bash
DEAD_CODE=$(claudemem --nologo dead-code --raw)
if [ -z "$DEAD_CODE" ]; then
  echo "No dead code found - architecture is well-maintained"
else
  # Categorize by risk
  HIGH_PAGERANK=$(echo "$DEAD_CODE" | awk '$5 > 0.01')
  LOW_PAGERANK=$(echo "$DEAD_CODE" | awk '$5 <= 0.01')

  if [ -n "$HIGH_PAGERANK" ]; then
    echo "WARNING: High-PageRank dead code found (possible broken references)"
    echo "$HIGH_PAGERANK"
  fi

  if [ -n "$LOW_PAGERANK" ]; then
    echo "Cleanup candidates (low PageRank):"
    echo "$LOW_PAGERANK"
  fi
fi
```

**Limitations Note:**
Results labeled "Potentially Dead" require manual verification for:
- Dynamically imported modules
- Reflection-accessed code
- External API consumers

## PHASE 0: MANDATORY SETUP

### Step 1: Verify claudemem v0.3.0

```bash
which claudemem && claudemem --version
# Must be 0.3.0+
```

### Step 2: If Not Installed → STOP

Use AskUserQuestion (see ultrathink-detective for template)

### Step 3: Check Index Status

```bash
# Check claudemem installation and index
claudemem --version && ls -la .claudemem/index.db 2>/dev/null
```

### Step 3.5: Check Index Freshness

Before proceeding with investigation, verify the index is current:

```bash
# First check if index exists
if [ ! -d ".claudemem" ] || [ ! -f ".claudemem/index.db" ]; then
  # Use AskUserQuestion to prompt for index creation
  # Options: [1] Create index now (Recommended), [2] Cancel investigation
  exit 1
fi

# Count files modified since last index
STALE_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
  -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | grep -v "dist" | grep -v "build" | wc -l)
STALE_COUNT=$((STALE_COUNT + 0))  # Normalize to integer

if [ "$STALE_COUNT" -gt 0 ]; then
  # Get index time with explicit platform detection
  if [[ "$OSTYPE" == "darwin"* ]]; then
    INDEX_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" .claudemem/index.db 2>/dev/null)
  else
    INDEX_TIME=$(stat -c "%y" .claudemem/index.db 2>/dev/null | cut -d'.' -f1)
  fi
  INDEX_TIME=${INDEX_TIME:-"unknown time"}

  # Get sample of stale files
  STALE_SAMPLE=$(find . -type f \( -name "*.ts" -o -name "*.tsx" \) \
    -newer .claudemem/index.db 2>/dev/null | grep -v "node_modules" | grep -v ".git" | head -5)

  # Use AskUserQuestion (see template in ultrathink-detective)
fi
```

### Step 4: Index if Needed

```bash
claudemem index
```

---

## Workflow: Architecture Analysis (v0.3.0)

### Phase 1: Map the Landscape

```bash
# Get structural overview with PageRank
claudemem --nologo map --raw

# Focus on high-PageRank symbols (> 0.01) - these are architectural pillars
```

### Phase 2: Identify Layers

```bash
# Map each layer
claudemem --nologo map "controller handler endpoint" --raw  # Presentation
claudemem --nologo map "service business logic" --raw       # Business
claudemem --nologo map "repository database query" --raw    # Data
```

### Phase 3: Trace Dependencies

```bash
# For each high-PageRank symbol, understand its role
claudemem --nologo symbol UserService --raw
claudemem --nologo callers UserService --raw  # Who depends on it?
claudemem --nologo callees UserService --raw  # What does it depend on?
```

### Phase 4: Identify Boundaries

```bash
# Find interfaces (architectural contracts)
claudemem --nologo map "interface abstract" --raw

# Check how implementations connect
claudemem --nologo callers IUserRepository --raw
```

### Phase 5: Cleanup Opportunities (v0.4.0+ Required)

```bash
# Find dead code
DEAD_CODE=$(claudemem --nologo dead-code --raw)

if [ -z "$DEAD_CODE" ]; then
  echo "No cleanup needed - codebase is well-maintained"
else
  # For each dead symbol:
  # - Check PageRank (low = utility, high = broken)
  # - Verify not used externally (see limitations)
  # - Add to cleanup backlog

  echo "Review each item for static analysis limitations:"
  echo "- Dynamic imports may hide real usage"
  echo "- External callers not visible to static analysis"
fi
```

## Output Format: Architecture Report

### 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                 ARCHITECTURE ANALYSIS                    │
├─────────────────────────────────────────────────────────┤
│  Pattern: Clean Architecture / Layered                  │
│  Core Abstractions (PageRank > 0.05):                   │
│    - UserService (0.092) - Central business logic       │
│    - Database (0.078) - Data access foundation          │
│    - AuthMiddleware (0.056) - Security boundary         │
│  Search Method: claudemem v0.3.0 (AST + PageRank)       │
└─────────────────────────────────────────────────────────┘
```

### 2. Layer Map

```
┌─────────────────────────────────────────────────────────┐
│                    LAYER STRUCTURE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  PRESENTATION (src/controllers/, src/routes/)            │
│    └── UserController (0.034)                           │
│    └── AuthController (0.028)                           │
│            ↓                                             │
│  BUSINESS (src/services/)                               │
│    └── UserService (0.092) ⭐HIGH PAGERANK              │
│    └── AuthService (0.067)                              │
│            ↓                                             │
│  DATA (src/repositories/)                               │
│    └── UserRepository (0.045)                           │
│    └── Database (0.078) ⭐HIGH PAGERANK                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 3. Dependency Flow

```
Entry → Controller → Service → Repository → Database
                  ↘ Middleware (cross-cutting)
```

## PageRank for Architecture

| PageRank | Architectural Role | Action |
|----------|-------------------|--------|
| > 0.05 | Core abstraction | This IS the architecture - understand first |
| 0.01-0.05 | Important component | Key building block, affects many things |
| 0.001-0.01 | Standard component | Normal code, not architecturally significant |
| < 0.001 | Leaf/utility | Implementation detail, skip for arch analysis |

## Result Validation Pattern

After EVERY claudemem command, validate results:

### Map Command Validation

After `map` commands, validate architectural symbols were found:

```bash
RESULTS=$(claudemem --nologo map "service layer business logic" --raw)
EXIT_CODE=$?

# Check for failure
if [ "$EXIT_CODE" -ne 0 ]; then
  DIAGNOSIS=$(claudemem status 2>&1)
  # Use AskUserQuestion
fi

# Check for empty results
if [ -z "$RESULTS" ]; then
  echo "WARNING: No symbols found - may be wrong query or index issue"
  # Use AskUserQuestion: Reindex, Different query, or Cancel
fi

# Check for high-PageRank symbols (> 0.01)
HIGH_PR=$(echo "$RESULTS" | grep "pagerank:" | awk -F': ' '{if ($2 > 0.01) print}' | wc -l)

if [ "$HIGH_PR" -eq 0 ]; then
  # No architectural symbols found - may be wrong query or index issue
  # Use AskUserQuestion: Reindex, Broaden query, or Cancel
fi
```

### Symbol Validation

```bash
SYMBOL=$(claudemem --nologo symbol ArchitecturalComponent --raw)

if [ -z "$SYMBOL" ] || echo "$SYMBOL" | grep -qi "not found\|error"; then
  # Component doesn't exist or index issue
  # Use AskUserQuestion
fi
```

---

## FALLBACK PROTOCOL

**CRITICAL: Never use grep/find/Glob without explicit user approval.**

If claudemem fails or returns irrelevant results:

1. **STOP** - Do not silently switch tools
2. **DIAGNOSE** - Run `claudemem status`
3. **REPORT** - Tell user what happened
4. **ASK** - Use AskUserQuestion for next steps

```typescript
// Fallback options (in order of preference)
AskUserQuestion({
  questions: [{
    question: "claudemem map returned no architectural symbols or failed. How should I proceed?",
    header: "Architecture Discovery Issue",
    multiSelect: false,
    options: [
      { label: "Reindex codebase", description: "Run claudemem index (~1-2 min)" },
      { label: "Try broader query", description: "Use different architectural terms" },
      { label: "Use grep (not recommended)", description: "Traditional search - loses PageRank ranking" },
      { label: "Cancel", description: "Stop investigation" }
    ]
  }]
})
```

**See ultrathink-detective skill for complete Fallback Protocol documentation.**

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| `grep -r "class"` | No ranking, no structure | `claudemem --nologo map --raw` |
| Read all files | Token waste | Focus on high-PageRank symbols |
| Skip `map` command | Miss architecture | ALWAYS start with `map` |
| Ignore PageRank | Miss core abstractions | High PageRank = important |

## Notes

- **`map` is your primary tool** - It shows architecture through PageRank
- High-PageRank symbols ARE the architecture - they're what everything depends on
- Use `callers` to see what depends on a component (impact of changes)
- Use `callees` to see what a component depends on (its requirements)
- Works best with TypeScript, Go, Python, Rust codebases

---

**Maintained by:** MadAppGang
**Plugin:** code-analysis v2.7.0
**Last Updated:** December 2025 (v3.3.0 - Cross-platform compatibility, inline templates, improved validation)
