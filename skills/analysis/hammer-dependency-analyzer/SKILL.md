---
name: hammer-dependency-analyzer
description: Verify dependency structure and architecture health for SDL3 HammerEngine. Detects circular dependencies, excessive coupling, layer violations, header bloat, and provides dependency graph visualization. Ensures adherence to layered architecture (Core→Managers→States→Entities). Use monthly, after major refactors, or when investigating compile time issues.
allowed-tools: [Bash, Read, Write, Grep, Glob]
---

# HammerEngine Dependency Analyzer

Comprehensive dependency structure analysis for SDL3 HammerEngine. Verifies architectural integrity, detects circular dependencies, identifies coupling issues, and maintains clean layered design.

## Purpose

HammerEngine follows a **layered architecture** pattern:
```
Core (ThreadSystem, Logger, GameLoop)
  ↓
Managers (AIManager, CollisionManager, etc.)
  ↓
States (GameState, MenuState, etc.)
  ↓
Entities (Entity classes, Components)
  ↓
Utils (Vector2D, Math helpers)
```

This Skill ensures:

1. **Circular Dependency Detection** - Prevent include cycles that break compilation
2. **Coupling Analysis** - Maintain loose coupling between managers
3. **Layer Violation Detection** - Enforce one-way dependencies (no upward dependencies)
4. **Header Bloat Identification** - Find unnecessary includes slowing compilation
5. **Forward Declaration Opportunities** - Reduce compilation dependencies
6. **Dependency Graph Visualization** - Understand system relationships
7. **Compile Time Impact Analysis** - Estimate compilation cost per component
8. **Architecture Health Scoring** - Quantify overall design quality

## Architecture Rules (from CLAUDE.md)

### Layer Rules

**1. Core Layer** (`src/core/`, `include/core/`)
- **Can depend on:** Nothing (foundation layer)
- **Used by:** Everything
- **Components:** ThreadSystem, Logger, GameLoop, GameEngine

**2. Managers Layer** (`src/managers/`, `include/managers/`)
- **Can depend on:** Core, Utils
- **Cannot depend on:** States, Entities (except via interfaces)
- **Coupling:** Managers should be loosely coupled, communicate via GameEngine
- **Components:** AIManager, CollisionManager, PathfinderManager, EventManager, etc.

**3. States Layer** (`src/gameStates/`, `include/gameStates/`)
- **Can depend on:** Core, Managers, Utils
- **Cannot depend on:** Other States (no cross-state dependencies)
- **Components:** GameState, MainMenuState, PlayingState, PauseState, etc.

**4. Entities Layer** (`src/entities/`, `include/entities/`)
- **Can depend on:** Core, Utils
- **Should avoid:** Direct manager dependencies (use interfaces/callbacks)
- **Components:** Entity, Component classes

**5. Utils Layer** (`src/utils/`, `include/utils/`)
- **Can depend on:** Nothing (pure utility functions)
- **Used by:** Everything
- **Components:** Vector2D, Math, JsonReader

### Coupling Rules

**Important: Game Engine Functional Coupling**

Game engines have **necessary functional dependencies** between managers. The following patterns are **CORRECT and expected**:

✅ **Functional Game System Dependencies (GOOD):**
- AIManager → CollisionManager (AI needs collision queries for obstacle avoidance, LOS)
- AIManager → PathfinderManager (AI needs pathfinding for navigation)
- CollisionManager → WorldManager (collision needs world geometry/tile data)
- Managers → EventManager (event-driven notifications are good architecture)
- UIManager → FontManager (UI needs fonts to render text)
- WorldManager → ResourceManager (world needs tile/sprite resources)
- ResourceFactory → ResourceTemplateManager (factory pattern requires templates)

**Manager-to-Manager Rules:**
- ✅ GOOD: Functional dependencies for game systems
- ✅ GOOD: Event-based communication between managers
- 🔴 FORBIDDEN: Circular Manager dependencies (breaks compilation)
- 🔴 FORBIDDEN: Managers depending on States (violates layer boundaries)

**What Actually Matters:**
- **Circular dependencies:** 🔴 ALWAYS BAD (breaks compilation)
- **Layer violations:** 🔴 ALWAYS BAD (breaks architecture)
- **Tight coupling:** ✅ OFTEN NECESSARY for game systems to work together
- **High reference counts:** ✅ EXPECTED when systems interact functionally

**State-to-Manager:**
- ✅ GOOD: PlayingState → AIManager (states use managers)
- 🔴 FORBIDDEN: AIManager → PlayingState (managers don't know about states)

**Header Inclusion:**
- ✅ GOOD: Forward declarations in headers, include in .cpp
- ⚠️  WARNING: Including heavy headers in .hpp (ripple effect)
- 🔴 FORBIDDEN: Circular includes (breaks compilation)

---

## Analysis Modes

### Mode 1: Quick Dependency Check (2-3 minutes)
- Scan for circular dependencies only
- Quick validation before commits
- **Use when:** Daily development, pre-commit

### Mode 2: Coupling Analysis (5-10 minutes)
- Analyze manager-to-manager coupling
- Identify high fan-out components
- Measure coupling strength
- **Use when:** Adding new managers, refactoring

### Mode 3: Full Architecture Audit (15-20 minutes)
- Complete dependency graph
- Layer violation detection
- Header bloat analysis
- Forward declaration opportunities
- Compile time impact estimation
- **Use when:** Monthly audits, major refactors, release prep

### Mode 4: Specific Component Analysis (3-5 minutes)
- Analyze single component's dependencies
- Show what it depends on and what depends on it
- **Use when:** Investigating specific coupling issues

---

## Step 1: Gather User Input

Use AskUserQuestion to determine analysis scope:

**Question 1: Analysis Mode**
- Header: "Mode"
- Question: "What type of dependency analysis do you want?"
- Options:
  - "Quick Circular Check" (2-3 min, daily use)
  - "Coupling Analysis" (5-10 min, manager refactoring)
  - "Full Architecture Audit" (15-20 min, comprehensive)
  - "Specific Component" (3-5 min, targeted analysis)
- multiSelect: false

**Question 2: Scope (if Mode = Specific Component)**
- Header: "Component"
- Question: "Which component should be analyzed?"
- Options:
  - "AIManager"
  - "CollisionManager"
  - "PathfinderManager"
  - "EventManager"
  - "Custom (specify)"
- multiSelect: false
- Only show if Mode = "Specific Component"

**Question 3: Output Format**
- Header: "Format"
- Question: "Preferred output format?"
- Options:
  - "Markdown Report" (default, saved to docs/)
  - "ASCII Tree" (console visualization)
  - "Both" (report + console tree)
- multiSelect: false

---

## Step 2: Scan Include Dependencies

**2a. Find All Header Files**

```bash
echo "=== Scanning Include Dependencies ==="

# Find all headers
INCLUDE_HEADERS=$(find include/ -name "*.hpp" -type f)
SRC_HEADERS=$(find src/ -name "*.hpp" -type f)

ALL_HEADERS=$(echo "$INCLUDE_HEADERS $SRC_HEADERS" | tr ' ' '\n' | sort -u)

HEADER_COUNT=$(echo "$ALL_HEADERS" | wc -l)
echo "Total headers found: $HEADER_COUNT"
```

**2b. Extract Include Directives**

```bash
OUTPUT_DIR="test_results/dependency_analysis"
mkdir -p "$OUTPUT_DIR"

DEPENDENCY_FILE="$OUTPUT_DIR/dependencies_raw.txt"
> "$DEPENDENCY_FILE"  # Clear file

echo "Extracting #include directives..."

for HEADER in $ALL_HEADERS; do
    # Extract local includes only (not system includes)
    LOCAL_INCLUDES=$(grep '^#include "' "$HEADER" | sed 's/#include "\(.*\)"/\1/' | tr -d '\r')

    if [ ! -z "$LOCAL_INCLUDES" ]; then
        echo "=== $HEADER ===" >> "$DEPENDENCY_FILE"
        echo "$LOCAL_INCLUDES" >> "$DEPENDENCY_FILE"
        echo "" >> "$DEPENDENCY_FILE"
    fi
done

echo "Dependencies extracted to: $DEPENDENCY_FILE"
```

**2c. Build Dependency Graph**

**Graph Structure (Adjacency List):**
```bash
# Create adjacency list representation
GRAPH_FILE="$OUTPUT_DIR/dependency_graph.txt"
> "$GRAPH_FILE"

echo "Building dependency graph..."

for HEADER in $ALL_HEADERS; do
    # Get just the filename (without path)
    HEADER_NAME=$(basename "$HEADER")

    # Get all includes from this header
    INCLUDES=$(grep '^#include "' "$HEADER" | sed 's/#include "\(.*\)"/\1/' | xargs -n1 basename 2>/dev/null)

    # Write to graph file: source -> dependencies
    if [ ! -z "$INCLUDES" ]; then
        for INCLUDE in $INCLUDES; do
            echo "$HEADER_NAME -> $INCLUDE" >> "$GRAPH_FILE"
        done
    fi
done

echo "Dependency graph built: $GRAPH_FILE"
```

---

## Step 3: Analyze Dependencies by Mode

### Mode 1: Quick Circular Check

**3a. Detect Circular Dependencies (DFS)**

```bash
echo "=== Circular Dependency Detection ==="

# Create Python script for cycle detection (more reliable than bash)
cat > "$OUTPUT_DIR/detect_cycles.py" <<'PYTHON_SCRIPT'
#!/usr/bin/env python3
import sys
from collections import defaultdict

def read_graph(graph_file):
    """Read dependency graph from file."""
    graph = defaultdict(list)
    with open(graph_file, 'r') as f:
        for line in f:
            if '->' in line:
                source, target = line.strip().split(' -> ')
                graph[source].append(target)
    return graph

def find_cycles_dfs(graph):
    """Find all cycles using DFS with recursion stack."""
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path.copy())
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)

        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles

def main():
    if len(sys.argv) != 2:
        print("Usage: detect_cycles.py <graph_file>")
        sys.exit(1)

    graph_file = sys.argv[1]
    graph = read_graph(graph_file)

    print(f"Analyzing {len(graph)} nodes...")

    cycles = find_cycles_dfs(graph)

    if not cycles:
        print("✅ NO CIRCULAR DEPENDENCIES DETECTED")
        sys.exit(0)
    else:
        print(f"🔴 FOUND {len(cycles)} CIRCULAR DEPENDENCIES:")
        print()
        for i, cycle in enumerate(cycles, 1):
            print(f"Cycle {i}:")
            print("  " + " -> ".join(cycle))
            print()
        sys.exit(1)

if __name__ == '__main__':
    main()
PYTHON_SCRIPT

chmod +x "$OUTPUT_DIR/detect_cycles.py"

# Run cycle detection
python3 "$OUTPUT_DIR/detect_cycles.py" "$GRAPH_FILE"
CYCLE_STATUS=$?

if [ $CYCLE_STATUS -ne 0 ]; then
    echo ""
    echo "🔴 CIRCULAR DEPENDENCIES BLOCK COMPILATION"
    echo "Action: Break cycles using forward declarations or interface extraction"
fi
```

**3b. Suggest Fixes for Circular Dependencies**

If cycles detected:
```bash
echo ""
echo "=== Circular Dependency Fix Suggestions ==="

# Read cycles from previous output
# For each cycle, suggest:
# 1. Forward declaration approach
# 2. Interface extraction
# 3. Dependency inversion

# Example output:
cat <<EOF
Cycle: AIManager.hpp -> PathfinderManager.hpp -> AIManager.hpp

Suggested Fixes:

1. Forward Declaration (RECOMMENDED):
   In AIManager.hpp:
     Remove: #include "PathfinderManager.hpp"
     Add: class PathfinderManager; // Forward declaration

   In AIManager.cpp:
     Add: #include "PathfinderManager.hpp"

2. Interface Extraction:
   Create IPathfinder.hpp with pure virtual interface
   AIManager depends on IPathfinder (no circular dependency)
   PathfinderManager implements IPathfinder

3. Dependency Inversion:
   Both managers depend on abstract interface
   GameEngine wires concrete implementations
EOF
```

---

### Mode 2: Coupling Analysis

**3a. Calculate Coupling Metrics**

**Fan-Out (Efferent Coupling):**
```bash
echo "=== Coupling Analysis ==="

# For each component, count how many others it depends on
echo "Fan-Out (Efferent Coupling - what this component depends on):"
echo ""

while IFS= read -r HEADER; do
    HEADER_NAME=$(basename "$HEADER")
    FAN_OUT=$(grep "^$HEADER_NAME ->" "$GRAPH_FILE" | wc -l)

    if [ "$FAN_OUT" -gt 0 ]; then
        # Classify coupling strength
        if [ "$FAN_OUT" -gt 15 ]; then
            STATUS="🔴 HIGH"
        elif [ "$FAN_OUT" -gt 10 ]; then
            STATUS="⚠️  MEDIUM"
        elif [ "$FAN_OUT" -gt 5 ]; then
            STATUS="🟡 MODERATE"
        else
            STATUS="✅ LOW"
        fi

        echo "  $HEADER_NAME: $FAN_OUT dependencies - $STATUS"
    fi
done <<< "$ALL_HEADERS" | sort -t: -k2 -rn | head -20

echo ""
```

**Fan-In (Afferent Coupling):**
```bash
echo "Fan-In (Afferent Coupling - what depends on this component):"
echo ""

while IFS= read -r HEADER; do
    HEADER_NAME=$(basename "$HEADER")
    FAN_IN=$(grep " -> $HEADER_NAME$" "$GRAPH_FILE" | wc -l)

    if [ "$FAN_IN" -gt 0 ]; then
        # High fan-in indicates core/stable component
        if [ "$FAN_IN" -gt 20 ]; then
            STATUS="⭐ CORE"
        elif [ "$FAN_IN" -gt 10 ]; then
            STATUS="📦 STABLE"
        elif [ "$FAN_IN" -gt 5 ]; then
            STATUS="🔧 UTILITY"
        else
            STATUS="📄 LEAF"
        fi

        echo "  $HEADER_NAME: $FAN_IN dependents - $STATUS"
    fi
done <<< "$ALL_HEADERS" | sort -t: -k2 -rn | head -20

echo ""
```

**Instability Metric (I = Fan-Out / (Fan-In + Fan-Out)):**
```bash
echo "Instability Metric (I = Efferent / (Afferent + Efferent)):"
echo "  0.0 = Maximally Stable (hard to change)"
echo "  1.0 = Maximally Unstable (easy to change)"
echo ""

while IFS= read -r HEADER; do
    HEADER_NAME=$(basename "$HEADER")

    FAN_OUT=$(grep "^$HEADER_NAME ->" "$GRAPH_FILE" | wc -l)
    FAN_IN=$(grep " -> $HEADER_NAME$" "$GRAPH_FILE" | wc -l)

    TOTAL=$((FAN_OUT + FAN_IN))

    if [ "$TOTAL" -gt 0 ]; then
        # Calculate instability (using bc for float arithmetic)
        INSTABILITY=$(echo "scale=2; $FAN_OUT / $TOTAL" | bc)

        echo "  $HEADER_NAME: I=$INSTABILITY (out=$FAN_OUT, in=$FAN_IN)"
    fi
done <<< "$ALL_HEADERS" | head -20
```

**3b. Manager-to-Manager Coupling**

```bash
echo ""
echo "=== Manager-to-Manager Coupling ==="

# Find all manager headers
MANAGERS=$(find include/managers -name "*.hpp" -type f 2>/dev/null)

if [ -z "$MANAGERS" ]; then
    echo "No managers found in include/managers/"
else
    # Build coupling matrix
    echo "Manager Coupling Matrix:"
    echo ""
    printf "%-25s" "Manager"

    # Header row
    for MGR in $MANAGERS; do
        MGR_NAME=$(basename "$MGR" .hpp)
        printf "%-8s" "${MGR_NAME:0:7}"
    done
    echo ""

    # Matrix rows
    for MGR1 in $MANAGERS; do
        MGR1_NAME=$(basename "$MGR1" .hpp)
        printf "%-25s" "$MGR1_NAME"

        for MGR2 in $MANAGERS; do
            MGR2_NAME=$(basename "$MGR2" .hpp)

            # Check if MGR1 includes MGR2
            INCLUDES=$(grep -c "#include \"$MGR2_NAME.hpp\"" "$MGR1" 2>/dev/null || echo "0")

            if [ "$MGR1_NAME" = "$MGR2_NAME" ]; then
                printf "%-8s" "-"
            elif [ "$INCLUDES" -gt 0 ]; then
                printf "%-8s" "✓"
            else
                printf "%-8s" " "
            fi
        done
        echo ""
    done
fi

echo ""
echo "Legend: ✓ = Direct dependency, - = Self, (blank) = No dependency"
echo ""
echo "Note: Manager-to-manager dependencies are EXPECTED in game engines."
echo "Game systems must interact: AI needs collision, world needs events, etc."
```

**3c. Coupling Strength Analysis**

```bash
echo ""
echo "=== Coupling Strength Analysis ==="

# Define functional game engine dependencies (these are EXPECTED and CORRECT)
# Format: "Manager1->Manager2" (these will NOT be flagged as problems)
FUNCTIONAL_DEPS=(
    "AIManager->CollisionManager"
    "AIManager->PathfinderManager"
    "CollisionManager->WorldManager"
    "CollisionManager->EventManager"
    "WorldManager->EventManager"
    "WorldManager->WorldResourceManager"
    "WorldManager->TextureManager"
    "UIManager->FontManager"
    "UIManager->UIConstants"
    "InputManager->UIManager"
    "InputManager->FontManager"
    "PathfinderManager->EventManager"
    "ParticleManager->EventManager"
    "ResourceFactory->ResourceTemplateManager"
    "ResourceTemplateManager->ResourceFactory"
    "WorldResourceManager->EventManager"
)

# Convert array to grep pattern
FUNCTIONAL_PATTERN=$(printf "|%s" "${FUNCTIONAL_DEPS[@]}")
FUNCTIONAL_PATTERN="${FUNCTIONAL_PATTERN:1}"  # Remove leading |

# For each manager pair with coupling, analyze strength
TIGHT_COUPLING_COUNT=0
FUNCTIONAL_COUPLING_COUNT=0

for MGR1 in $MANAGERS; do
    MGR1_NAME=$(basename "$MGR1" .hpp)
    MGR1_CPP="src/managers/${MGR1_NAME}.cpp"

    if [ -f "$MGR1_CPP" ]; then
        for MGR2 in $MANAGERS; do
            MGR2_NAME=$(basename "$MGR2" .hpp)

            if [ "$MGR1_NAME" != "$MGR2_NAME" ]; then
                # Count references to MGR2 in MGR1's implementation
                REF_COUNT=$(grep -c "$MGR2_NAME" "$MGR1_CPP" 2>/dev/null || echo "0")

                if [ "$REF_COUNT" -gt 10 ]; then
                    COUPLING_PAIR="${MGR1_NAME}->${MGR2_NAME}"

                    # Check if this is a functional dependency
                    if echo "$COUPLING_PAIR" | grep -qE "$FUNCTIONAL_PATTERN"; then
                        echo "✅ FUNCTIONAL: $MGR1_NAME -> $MGR2_NAME ($REF_COUNT references)"
                        echo "    Status: Expected game system interaction (correct design)"
                        FUNCTIONAL_COUPLING_COUNT=$((FUNCTIONAL_COUPLING_COUNT + 1))
                    else
                        echo "🔴 TIGHT: $MGR1_NAME -> $MGR2_NAME ($REF_COUNT references)"
                        echo "    Review: Is this coupling necessary for game functionality?"
                        TIGHT_COUPLING_COUNT=$((TIGHT_COUPLING_COUNT + 1))
                    fi
                elif [ "$REF_COUNT" -gt 5 ]; then
                    echo "📊 MODERATE: $MGR1_NAME -> $MGR2_NAME ($REF_COUNT references)"
                fi
            fi
        done
    fi
done

echo ""
echo "Summary:"
echo "  - Functional coupling (expected): $FUNCTIONAL_COUPLING_COUNT pairs"
echo "  - Tight coupling (review): $TIGHT_COUPLING_COUNT pairs"
echo ""
echo "Note: Functional coupling is CORRECT for game engines - systems must interact!"
```

---

### Mode 3: Full Architecture Audit

**3a. Layer Violation Detection**

```bash
echo "=== Layer Violation Detection ==="

# Define layers
CORE_HEADERS=$(find include/core src/core -name "*.hpp" 2>/dev/null)
MANAGER_HEADERS=$(find include/managers src/managers -name "*.hpp" 2>/dev/null)
STATE_HEADERS=$(find include/gameStates src/gameStates -name "*.hpp" 2>/dev/null)
ENTITY_HEADERS=$(find include/entities src/entities -name "*.hpp" 2>/dev/null)
UTIL_HEADERS=$(find include/utils src/utils -name "*.hpp" 2>/dev/null)

# Check Core layer (should not depend on anything)
echo "1. Core Layer (should be dependency-free):"
for CORE in $CORE_HEADERS; do
    VIOLATIONS=$(grep '#include "' "$CORE" | grep -v 'core/' | grep -v 'utils/' | wc -l)
    if [ "$VIOLATIONS" -gt 0 ]; then
        echo "  🔴 $(basename "$CORE"): includes non-Core/Utils headers"
        grep '#include "' "$CORE" | grep -v 'core/' | grep -v 'utils/'
    fi
done

# Check Manager layer (should not depend on States or Entities)
echo ""
echo "2. Manager Layer (should not depend on States/Entities):"
for MGR in $MANAGER_HEADERS; do
    STATE_DEPS=$(grep '#include "' "$MGR" | grep -c 'gameStates/' 2>/dev/null || echo "0")
    ENTITY_DEPS=$(grep '#include "' "$MGR" | grep -c 'entities/' 2>/dev/null || echo "0")

    if [ "$STATE_DEPS" -gt 0 ] || [ "$ENTITY_DEPS" -gt 0 ]; then
        echo "  🔴 $(basename "$MGR"): violates layer boundaries"
        [ "$STATE_DEPS" -gt 0 ] && echo "    - Includes State headers (forbidden)"
        [ "$ENTITY_DEPS" -gt 0 ] && echo "    - Includes Entity headers (review needed)"
    fi
done

# Check State layer (should not depend on other States)
echo ""
echo "3. State Layer (states should not depend on each other):"
for STATE1 in $STATE_HEADERS; do
    STATE1_NAME=$(basename "$STATE1")

    for STATE2 in $STATE_HEADERS; do
        STATE2_NAME=$(basename "$STATE2")

        if [ "$STATE1_NAME" != "$STATE2_NAME" ]; then
            if grep -q "#include \"$STATE2_NAME\"" "$STATE1" 2>/dev/null; then
                echo "  🔴 $STATE1_NAME -> $STATE2_NAME (cross-state dependency)"
            fi
        fi
    done
done

# Check Utils layer (should not depend on anything)
echo ""
echo "4. Utils Layer (should be dependency-free):"
for UTIL in $UTIL_HEADERS; do
    NON_UTIL_DEPS=$(grep '#include "' "$UTIL" | grep -v 'utils/' | wc -l)
    if [ "$NON_UTIL_DEPS" -gt 0 ]; then
        echo "  ⚠️  $(basename "$UTIL"): includes non-Utils headers"
        grep '#include "' "$UTIL" | grep -v 'utils/'
    fi
done

echo ""
echo "Layer Violation Summary:"
CORE_VIOLATIONS=$(find include/core src/core -name "*.hpp" -exec grep '#include "' {} \; | grep -v 'core/' | grep -v 'utils/' | wc -l)
MANAGER_VIOLATIONS=$(find include/managers src/managers -name "*.hpp" -exec grep '#include "' {} \; | grep 'gameStates/' | wc -l)
STATE_VIOLATIONS=0  # Count from previous check
UTIL_VIOLATIONS=$(find include/utils src/utils -name "*.hpp" -exec grep '#include "' {} \; | grep -v 'utils/' | wc -l)

TOTAL_VIOLATIONS=$((CORE_VIOLATIONS + MANAGER_VIOLATIONS + STATE_VIOLATIONS + UTIL_VIOLATIONS))

if [ "$TOTAL_VIOLATIONS" -eq 0 ]; then
    echo "  ✅ No layer violations detected"
else
    echo "  🔴 $TOTAL_VIOLATIONS layer violations found"
fi
```

**3b. Header Bloat Analysis**

```bash
echo ""
echo "=== Header Bloat Analysis ==="

# Find headers with excessive includes
echo "Headers with High Include Count (potential bloat):"
echo ""

for HEADER in $ALL_HEADERS; do
    INCLUDE_COUNT=$(grep -c '^#include "' "$HEADER")

    if [ "$INCLUDE_COUNT" -gt 15 ]; then
        echo "  🔴 $(basename "$HEADER"): $INCLUDE_COUNT includes (HIGH - review for bloat)"
    elif [ "$INCLUDE_COUNT" -gt 10 ]; then
        echo "  ⚠️  $(basename "$HEADER"): $INCLUDE_COUNT includes (MODERATE)"
    fi
done

# Find commonly included heavy headers
echo ""
echo "Frequently Included Headers (ripple effect on compile times):"
echo ""

# Count how many files include each header
while IFS= read -r HEADER; do
    HEADER_NAME=$(basename "$HEADER")
    INCLUDE_COUNT=$(grep -r "#include \"$HEADER_NAME\"" include/ src/ 2>/dev/null | wc -l)

    if [ "$INCLUDE_COUNT" -gt 10 ]; then
        echo "  $HEADER_NAME: included by $INCLUDE_COUNT files"

        # Check if this header itself has many includes (bloat amplification)
        HEADER_INCLUDES=$(grep -c '^#include' "$HEADER" 2>/dev/null || echo "0")
        if [ "$HEADER_INCLUDES" -gt 10 ]; then
            echo "    ⚠️  This header includes $HEADER_INCLUDES files (bloat amplification)"
        fi
    fi
done <<< "$ALL_HEADERS" | sort -t: -k2 -rn | head -15
```

**3c. Forward Declaration Opportunities**

```bash
echo ""
echo "=== Forward Declaration Opportunities ==="

# Find headers that could use forward declarations
# Pattern: Header includes another header but only uses pointers/references

echo "Analyzing headers for forward declaration opportunities..."
echo ""

for HEADER in $ALL_HEADERS; do
    # Get all includes
    INCLUDES=$(grep '^#include "' "$HEADER" | sed 's/#include "\(.*\.hpp\)"/\1/')

    for INCLUDE in $INCLUDES; do
        INCLUDE_BASE=$(basename "$INCLUDE" .hpp)

        # Check if only used as pointer or reference
        # Look for: ClassName* or ClassName&, but NOT ClassName object;
        PTR_REF_ONLY=$(grep -c "${INCLUDE_BASE}[*&]" "$HEADER" 2>/dev/null || echo "0")
        DIRECT_USE=$(grep -c "${INCLUDE_BASE}[^*&];.*;" "$HEADER" 2>/dev/null || echo "0")

        if [ "$PTR_REF_ONLY" -gt 0 ] && [ "$DIRECT_USE" -eq 0 ]; then
            echo "  ✨ $(basename "$HEADER"): Can forward-declare $INCLUDE_BASE"
            echo "     Remove: #include \"$INCLUDE\""
            echo "     Add: class $INCLUDE_BASE; // Forward declaration"
            echo ""
        fi
    done
done | head -30  # Limit output

echo "Note: Move #include to .cpp file after forward declaration"
```

**3d. Compile Time Impact Estimation**

```bash
echo ""
echo "=== Compile Time Impact Estimation ==="

# Estimate compilation cost based on dependency depth
echo "Dependency Depth (higher = more recompilation ripple):"
echo ""

# For each header, calculate max depth to leaf nodes
# This is an approximation of compile time impact

# Create depth calculation script
cat > "$OUTPUT_DIR/calc_depth.py" <<'PYTHON_SCRIPT'
#!/usr/bin/env python3
import sys
from collections import defaultdict, deque

def read_graph(graph_file):
    graph = defaultdict(list)
    with open(graph_file, 'r') as f:
        for line in f:
            if '->' in line:
                source, target = line.strip().split(' -> ')
                graph[source].append(target)
    return graph

def calculate_depth(graph, node, memo=None):
    """Calculate max dependency depth using DFS with memoization."""
    if memo is None:
        memo = {}

    if node in memo:
        return memo[node]

    if node not in graph or not graph[node]:
        memo[node] = 0
        return 0

    max_depth = 0
    for neighbor in graph[node]:
        depth = calculate_depth(graph, neighbor, memo)
        max_depth = max(max_depth, depth + 1)

    memo[node] = max_depth
    return max_depth

def main():
    if len(sys.argv) != 2:
        print("Usage: calc_depth.py <graph_file>")
        sys.exit(1)

    graph = read_graph(sys.argv[1])

    # Calculate depth for all nodes
    depths = {}
    for node in graph:
        depths[node] = calculate_depth(graph, node)

    # Sort by depth (highest first)
    sorted_depths = sorted(depths.items(), key=lambda x: x[1], reverse=True)

    print("Top 20 Headers by Dependency Depth:")
    print()
    for node, depth in sorted_depths[:20]:
        if depth > 10:
            status = "🔴 VERY HIGH"
        elif depth > 7:
            status = "⚠️  HIGH"
        elif depth > 4:
            status = "🟡 MODERATE"
        else:
            status = "✅ LOW"

        print(f"  {node}: depth={depth} {status}")

    print()
    print("Note: High depth = changing this header causes cascading recompilation")

if __name__ == '__main__':
    main()
PYTHON_SCRIPT

chmod +x "$OUTPUT_DIR/calc_depth.py"
python3 "$OUTPUT_DIR/calc_depth.py" "$GRAPH_FILE"

# Estimate total compile impact
echo ""
echo "Estimated Compile Time Impact:"
TOTAL_DEPTH=$(python3 "$OUTPUT_DIR/calc_depth.py" "$GRAPH_FILE" 2>/dev/null | grep "depth=" | awk -F'depth=' '{print $2}' | awk '{print $1}' | paste -sd+ | bc)
echo "  Total dependency depth: $TOTAL_DEPTH"
echo "  Average per header: $(echo "scale=1; $TOTAL_DEPTH / $HEADER_COUNT" | bc)"
```

---

### Mode 4: Specific Component Analysis

**4a. Single Component Dependency Analysis**

```bash
# User specified component (e.g., AIManager)
COMPONENT="$USER_COMPONENT"
COMPONENT_HEADER=$(find include/ src/ -name "${COMPONENT}.hpp" | head -1)

if [ -z "$COMPONENT_HEADER" ]; then
    echo "❌ Component not found: $COMPONENT"
    exit 1
fi

echo "=== Dependency Analysis: $COMPONENT ==="
echo ""

# What this component depends on (efferent)
echo "1. What $COMPONENT depends on (Efferent Dependencies):"
echo ""
grep '^#include "' "$COMPONENT_HEADER" | sed 's/#include "\(.*\)"/  - \1/'

EFFERENT_COUNT=$(grep -c '^#include "' "$COMPONENT_HEADER")
echo ""
echo "  Total: $EFFERENT_COUNT direct dependencies"

# What depends on this component (afferent)
echo ""
echo "2. What depends on $COMPONENT (Afferent Dependencies):"
echo ""

COMPONENT_NAME=$(basename "$COMPONENT_HEADER")
DEPENDENTS=$(grep -r "#include \"$COMPONENT_NAME\"" include/ src/ 2>/dev/null | cut -d: -f1 | sort -u)

if [ -z "$DEPENDENTS" ]; then
    echo "  (None - this is a leaf component)"
else
    echo "$DEPENDENTS" | while read DEP; do
        echo "  - $(basename "$DEP")"
    done
fi

AFFERENT_COUNT=$(echo "$DEPENDENTS" | wc -l)
echo ""
echo "  Total: $AFFERENT_COUNT dependent files"

# Coupling metrics
echo ""
echo "3. Coupling Metrics:"
echo "  - Efferent Coupling (Fan-Out): $EFFERENT_COUNT"
echo "  - Afferent Coupling (Fan-In): $AFFERENT_COUNT"

TOTAL=$((EFFERENT_COUNT + AFFERENT_COUNT))
if [ "$TOTAL" -gt 0 ]; then
    INSTABILITY=$(echo "scale=2; $EFFERENT_COUNT / $TOTAL" | bc)
    echo "  - Instability (I): $INSTABILITY"

    if (( $(echo "$INSTABILITY > 0.8" | bc -l) )); then
        echo "    → Highly unstable (easy to change, but volatile)"
    elif (( $(echo "$INSTABILITY < 0.2" | bc -l) )); then
        echo "    → Highly stable (hard to change, but reliable)"
    else
        echo "    → Balanced stability"
    fi
fi

# Layer check
echo ""
echo "4. Layer Classification:"
if echo "$COMPONENT_HEADER" | grep -q "core/"; then
    echo "  - Layer: Core"
    echo "  - Should depend on: Nothing"
elif echo "$COMPONENT_HEADER" | grep -q "managers/"; then
    echo "  - Layer: Managers"
    echo "  - Should depend on: Core, Utils"
    echo "  - Should NOT depend on: States, other Managers (loosely coupled)"
elif echo "$COMPONENT_HEADER" | grep -q "gameStates/"; then
    echo "  - Layer: States"
    echo "  - Should depend on: Core, Managers, Utils"
    echo "  - Should NOT depend on: Other States"
elif echo "$COMPONENT_HEADER" | grep -q "entities/"; then
    echo "  - Layer: Entities"
    echo "  - Should depend on: Core, Utils"
elif echo "$COMPONENT_HEADER" | grep -q "utils/"; then
    echo "  - Layer: Utils"
    echo "  - Should depend on: Nothing"
fi

# Specific issues
echo ""
echo "5. Potential Issues:"
# Check for layer violations
VIOLATIONS=0

if echo "$COMPONENT_HEADER" | grep -q "managers/"; then
    STATE_DEPS=$(grep '#include "' "$COMPONENT_HEADER" | grep -c 'gameStates/' || echo "0")
    if [ "$STATE_DEPS" -gt 0 ]; then
        echo "  🔴 Includes State headers (layer violation)"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
fi

if [ "$EFFERENT_COUNT" -gt 15 ]; then
    echo "  ⚠️  High efferent coupling ($EFFERENT_COUNT dependencies)"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

# Check for circular dependencies involving this component
COMPONENT_BASE=$(basename "$COMPONENT_HEADER")
CYCLES=$(python3 "$OUTPUT_DIR/detect_cycles.py" "$GRAPH_FILE" 2>&1 | grep "$COMPONENT_BASE" || echo "")
if [ ! -z "$CYCLES" ]; then
    echo "  🔴 Part of circular dependency"
    echo "$CYCLES" | sed 's/^/      /'
    VIOLATIONS=$((VIOLATIONS + 1))
fi

if [ "$VIOLATIONS" -eq 0 ]; then
    echo "  ✅ No issues detected"
fi
```

---

## Step 4: Generate Dependency Visualizations

**4a. ASCII Dependency Tree**

```bash
echo ""
echo "=== Dependency Tree (ASCII) ==="

# Create tree visualization script
cat > "$OUTPUT_DIR/make_tree.sh" <<'TREE_SCRIPT'
#!/bin/bash

# Function to print tree recursively
print_tree() {
    local node=$1
    local prefix=$2
    local visited=$3
    local max_depth=$4
    local current_depth=$5

    # Prevent infinite loops
    if echo "$visited" | grep -q "|$node|"; then
        echo "${prefix}└── $node (circular)"
        return
    fi

    # Max depth limit
    if [ "$current_depth" -ge "$max_depth" ]; then
        echo "${prefix}└── $node (...)"
        return
    fi

    echo "${prefix}└── $node"

    # Get dependencies
    local deps=$(grep "^$node ->" "$GRAPH_FILE" | cut -d'>' -f2 | tr -d ' ')

    if [ ! -z "$deps" ]; then
        local new_visited="${visited}|${node}|"
        local new_depth=$((current_depth + 1))

        echo "$deps" | while read dep; do
            print_tree "$dep" "${prefix}    " "$new_visited" "$max_depth" "$new_depth"
        done
    fi
}

# Entry point
GRAPH_FILE="$1"
ROOT_NODE="$2"
MAX_DEPTH="${3:-5}"

print_tree "$ROOT_NODE" "" "" "$MAX_DEPTH" 0
TREE_SCRIPT

chmod +x "$OUTPUT_DIR/make_tree.sh"

# Generate trees for key components
echo ""
echo "GameEngine Dependency Tree:"
"$OUTPUT_DIR/make_tree.sh" "$GRAPH_FILE" "GameEngine.hpp" 3

echo ""
echo "AIManager Dependency Tree:"
"$OUTPUT_DIR/make_tree.sh" "$GRAPH_FILE" "AIManager.hpp" 3
```

**4b. Dependency Matrix (for report)**

```bash
# Generate full dependency matrix for report
echo ""
echo "Generating dependency matrix for report..."

cat > "$OUTPUT_DIR/dependency_matrix.txt" <<EOF
# Dependency Matrix

Rows depend on Columns (✓ = direct dependency)

EOF

# Get top 20 most connected headers
TOP_HEADERS=$(cat "$GRAPH_FILE" | grep -o '[^ ]*\.hpp' | sort | uniq -c | sort -rn | head -20 | awk '{print $2}')

# Print header row
printf "%-25s" "Component"
echo "$TOP_HEADERS" | while read HEADER; do
    HEADER_SHORT=$(echo "$HEADER" | cut -d'.' -f1 | cut -c1-7)
    printf "%-8s" "$HEADER_SHORT"
done
echo ""

# Print matrix rows
echo "$TOP_HEADERS" | while read ROW_HEADER; do
    printf "%-25s" "$(echo "$ROW_HEADER" | cut -d'.' -f1)"

    echo "$TOP_HEADERS" | while read COL_HEADER; do
        if [ "$ROW_HEADER" = "$COL_HEADER" ]; then
            printf "%-8s" "-"
        else
            HAS_DEP=$(grep "^$ROW_HEADER -> $COL_HEADER$" "$GRAPH_FILE")
            if [ ! -z "$HAS_DEP" ]; then
                printf "%-8s" "✓"
            else
                printf "%-8s" " "
            fi
        fi
    done
    echo ""
done >> "$OUTPUT_DIR/dependency_matrix.txt"

echo "Dependency matrix saved to: $OUTPUT_DIR/dependency_matrix.txt"
```

---

## Step 5: Generate Architecture Health Report

**Report Structure:**

```markdown
# HammerEngine Dependency Analysis Report

**Generated:** YYYY-MM-DD HH:MM:SS
**Branch:** <branch>
**Commit:** <hash>
**Analysis Mode:** <mode>

---

## Executive Summary

**Architecture Health Score:** [85/100] (GOOD)

**Status:** ✅ HEALTHY / ⚠️ NEEDS ATTENTION / 🔴 CRITICAL ISSUES

**Key Findings:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Overall Assessment:** [2-3 sentence summary]

---

## Dependency Statistics

**Codebase Size:**
- Total headers analyzed: [N]
- Core layer: [N] files
- Managers layer: [N] files
- States layer: [N] files
- Entities layer: [N] files
- Utils layer: [N] files

**Dependency Metrics:**
- Total dependencies: [N]
- Average dependencies per file: [X.X]
- Max dependencies (single file): [N]
- Circular dependencies: [N] 🔴/✅

---

## Circular Dependencies (CRITICAL)

[If none:]
✅ **NO CIRCULAR DEPENDENCIES DETECTED**

All include hierarchies are acyclic. Compilation order is deterministic.

[If found:]
🔴 **FOUND [N] CIRCULAR DEPENDENCIES**

### Cycle 1: [Component A] ↔ [Component B]

**Cycle Path:**
```
ComponentA.hpp -> ComponentB.hpp -> ComponentA.hpp
```

**Impact:** Breaks compilation or requires workarounds

**Suggested Fix:**
1. **Forward Declaration** (RECOMMENDED)
   - In ComponentA.hpp, replace `#include "ComponentB.hpp"` with `class ComponentB;`
   - Move include to ComponentA.cpp

2. **Interface Extraction**
   - Create IComponentB.hpp with pure virtual interface
   - ComponentA depends on interface (breaks cycle)

[Repeat for each cycle]

---

## Coupling Analysis

### High-Coupling Components (Top 10)

| Component | Fan-Out | Fan-In | Instability | Status |
|-----------|---------|--------|-------------|--------|
| [Component1] | 18 | 5 | 0.78 | 🔴 HIGH |
| [Component2] | 15 | 12 | 0.55 | ⚠️  MODERATE |
| [Component3] | 8 | 20 | 0.29 | ✅ STABLE |

**Legend:**
- **Fan-Out:** Number of dependencies (efferent coupling)
- **Fan-In:** Number of dependents (afferent coupling)
- **Instability:** Fan-Out / (Fan-In + Fan-Out)
  - 0.0 = Maximally stable (hard to change)
  - 1.0 = Maximally unstable (easy to change)

### Manager-to-Manager Coupling

**Coupling Matrix:**

[Include dependency matrix from Step 4b]

**Manager Coupling Analysis:**

**Important Context:** Game engines have **necessary functional dependencies**. Tight coupling between game systems is often **CORRECT and required** for the engine to function.

**Functional Coupling (✅ Expected & Correct):**
[List coupling pairs that serve game functionality]
- AIManager → CollisionManager (AI obstacle avoidance, LOS checks)
- CollisionManager → WorldManager (world geometry queries)
- Managers → EventManager (event-driven notifications)
- UIManager → FontManager (text rendering)
- etc.

**Status:** ✅ These dependencies are functionally necessary and represent correct game engine architecture.

**Problematic Coupling (🔴 Review Required):**
[If any non-functional tight coupling exists]
1. **[Manager1] → [Manager2]** (N references)
   - Status: 🔴 REVIEW
   - Reason: Unclear functional necessity
   - Recommendation: Verify this coupling serves game functionality

[If none:]
✅ **NO PROBLEMATIC COUPLING**

All tight coupling serves clear game system functionality.

---

## Layer Violations

### Layer Integrity Check

**Core Layer** (should depend on nothing):
[✅ CLEAN / 🔴 [N] violations]

**Managers Layer** (should depend on Core, Utils only):
[✅ CLEAN / 🔴 [N] violations]

**States Layer** (no cross-state dependencies):
[✅ CLEAN / 🔴 [N] violations]

**Utils Layer** (should be dependency-free):
[✅ CLEAN / 🔴 [N] violations]

### Violation Details

[If violations found:]

**Violation 1: AIManager includes PlayingState.hpp**
- **File:** include/managers/AIManager.hpp:15
- **Issue:** Manager layer depending on State layer
- **Impact:** Violates layered architecture, creates tight coupling
- **Fix:** Remove include, use interface or event system

[Repeat for each violation]

[If none:]
✅ **NO LAYER VIOLATIONS**

All components respect layered architecture boundaries.

---

## Header Bloat Analysis

### High-Include Headers

| Header | #Includes | Status | Dependents |
|--------|-----------|--------|-----------|
| [Header1] | 22 | 🔴 HIGH | 15 files |
| [Header2] | 18 | ⚠️  MODERATE | 8 files |

**Bloat Amplification:**

Headers with many includes that are widely used cause compilation ripple effects.

**Worst Offenders:**
1. **GameEngine.hpp** - 22 includes, used by 15 files
   - Ripple effect: ~330 transitive includes
   - Recommendation: Split into GameEngine_fwd.hpp with forward declarations

### Forward Declaration Opportunities

[Top 10 opportunities from Step 3c]

**Estimated Compile Time Savings:** ~15-25% reduction

---

## Dependency Depth Analysis

### Compile Time Impact

| Header | Depth | Impact | Recommendation |
|--------|-------|--------|----------------|
| [Header1] | 14 | 🔴 VERY HIGH | Reduce dependencies |
| [Header2] | 9 | ⚠️  HIGH | Consider splitting |
| [Header3] | 6 | 🟡 MODERATE | Monitor |

**Total Dependency Depth:** [N]
**Average Depth:** [X.X]

**High-Depth Components:**

Changing these headers causes cascading recompilation:
- [List top 5 highest depth headers]

**Recommendation:** Use forward declarations and split large headers

---

## Architecture Health Scorecard

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| Circular Dependencies | [X/10] | 30% | [X.X] | 🔴/⚠️/✅ |
| Layer Compliance | [X/10] | 25% | [X.X] | 🔴/⚠️/✅ |
| Coupling Strength | [X/10] | 20% | [X.X] | 🔴/⚠️/✅ |
| Header Bloat | [X/10] | 15% | [X.X] | 🔴/⚠️/✅ |
| Dependency Depth | [X/10] | 10% | [X.X] | 🔴/⚠️/✅ |
| **TOTAL** | | **100%** | **[XX/100]** | **[GRADE]** |

**Grading Scale:**
- 90-100: A+ (Excellent architecture)
- 80-89: A (Good architecture, minor issues)
- 70-79: B (Fair architecture, needs improvement)
- 60-69: C (Poor architecture, refactoring required)
- Below 60: F (Critical issues, major refactoring needed)

---

## Recommendations

### Critical (Fix Immediately)

1. **Break Circular Dependencies** ([N] found)
   - Use forward declarations
   - Extract interfaces
   - Priority: HIGH, Effort: 2-4 hours

2. **Fix Layer Violations** ([N] found)
   - Remove inappropriate includes
   - Use event system for cross-layer communication
   - Priority: HIGH, Effort: 1-2 hours

### Important (Address Soon)

3. **Review Non-Functional Coupling (if any)**
   - [Only list coupling that doesn't serve clear game functionality]
   - Verify: Does this coupling serve a game system requirement?
   - If yes: Document the functional reason, no change needed
   - If no: Consider refactoring or event-based communication
   - Priority: MEDIUM (only if problematic coupling exists)

4. **Optimize High-Include Headers**
   - Split [Header] into interface and implementation
   - Add forward declaration headers
   - Priority: MEDIUM, Effort: 2-3 hours

**Note:** Do NOT refactor functional game system dependencies. Coupling between managers is often necessary and correct for game engines.

### Optional (Consider)

5. **Improve Compile Times**
   - Apply forward declaration opportunities
   - Split large headers
   - Expected improvement: 15-25% faster compilation
   - Priority: LOW, Effort: 3-5 hours

---

## Dependency Visualizations

### GameEngine Dependency Tree

[ASCII tree from Step 4a]

### AIManager Dependency Tree

[ASCII tree from Step 4a]

### Full Dependency Matrix

[Link to or include dependency_matrix.txt]

---

## Comparison with Previous Analysis (if baseline exists)

| Metric | Previous | Current | Change | Trend |
|--------|----------|---------|--------|-------|
| Total Dependencies | [N] | [N] | [+/-N] | 📈/📉/➡️ |
| Circular Dependencies | [N] | [N] | [+/-N] | 📈/📉/➡️ |
| Layer Violations | [N] | [N] | [+/-N] | 📈/📉/➡️ |
| Average Coupling | [X.X] | [X.X] | [+/-X.X] | 📈/📉/➡️ |
| Health Score | [XX] | [XX] | [+/-XX] | 📈/📉/➡️ |

**Overall Trend:** [Improving/Stable/Degrading]

---

## Action Plan

### Immediate (This Week)
- [ ] Break circular dependency: [Cycle description]
- [ ] Fix layer violation: [Specific violation]

### Short-term (This Month)
- [ ] Reduce coupling between [Component1] and [Component2]
- [ ] Split high-include headers: [Header list]
- [ ] Apply top 5 forward declaration opportunities

### Long-term (This Quarter)
- [ ] Comprehensive header cleanup
- [ ] Establish pre-commit dependency checks
- [ ] Document architecture patterns

---

## Files Requiring Attention

Based on analysis, these files need modification:

**High Priority:**
- [File1] - Circular dependency
- [File2] - Layer violation

**Medium Priority:**
- [File3] - High coupling
- [File4] - Header bloat

**Low Priority:**
- [File5] - Forward declaration opportunity

---

## Next Steps

1. **Review this report** with team/architect
2. **Prioritize fixes** based on impact and effort
3. **Create tickets** for identified issues
4. **Re-run analysis** after fixes to verify improvements
5. **Schedule regular audits** (monthly recommended)

**Re-run Analysis:**
```bash
# After fixes, verify improvements
[Command to re-invoke skill]
```

---

**Report Generated By:** hammer-dependency-analyzer Skill
**Report Saved To:** `docs/architecture/dependency_analysis_YYYY-MM-DD.md`
```

**Save report:**
```bash
REPORT_FILE="docs/architecture/dependency_analysis_$(date +%Y-%m-%d).md"
mkdir -p "docs/architecture"

cat > "$REPORT_FILE" <<'EOF'
[Generated markdown report]
EOF

echo "✅ Dependency analysis report saved to: $REPORT_FILE"
```

---

## Step 6: Console Summary

```
=== HammerEngine Dependency Analysis ===

Mode: [Mode Name]
Files Analyzed: [N] headers

Architecture Health: [Score]/100 ([GRADE])

Circular Dependencies: [N] 🔴/✅
Layer Violations: [N] 🔴/✅
High Coupling: [N] components ⚠️
Header Bloat: [N] headers 🔴/⚠️

[If issues:]
Status: 🔴 CRITICAL ISSUES / ⚠️  NEEDS ATTENTION

Critical Issues:
  - [Issue 1]
  - [Issue 2]

Recommendations:
  1. [Top recommendation]
  2. [Second recommendation]

[If clean:]
Status: ✅ ARCHITECTURE HEALTHY

All checks passed:
  ✅ No circular dependencies
  ✅ No layer violations
  ✅ Coupling within acceptable limits
  ✅ No excessive header bloat

Full Report: docs/architecture/dependency_analysis_YYYY-MM-DD.md

Next: [Suggested action based on results]
```

---

## Usage Examples

When the user says:
- "analyze dependencies"
- "check architecture health"
- "find circular dependencies"
- "check manager coupling"
- "analyze AIManager dependencies"
- "audit header dependencies"

Activate this Skill automatically.

---

## Integration with Development Workflow

**Use this Skill:**

### Regular Maintenance
- **Monthly audits** - Catch architectural drift early
- **After major refactors** - Verify improvements
- **Before releases** - Ensure architecture quality

### Development Checkpoints
- **Adding new manager** - Verify coupling is appropriate
- **Refactoring existing code** - Check impact on dependencies
- **Investigating compile times** - Identify bloat and depth issues

### Problem Investigation
- **Circular dependency errors** - Find and break cycles
- **Slow compilation** - Identify high-depth headers
- **Tight coupling concerns** - Analyze manager interactions

---

## Common Dependency Issues in HammerEngine

### Issue 1: Manager Circular Dependencies

**Symptom:** Compilation errors with forward declaration issues
**Cause:** Two managers including each other's headers
**Solution:** One-way dependency with interface or event system

### Issue 2: State-to-State Dependencies

**Symptom:** States including other state headers
**Cause:** Sharing data/logic between states
**Solution:** Move shared logic to Manager or GameEngine

### Issue 3: GameEngine.hpp Bloat

**Symptom:** Long compile times for any GameEngine change
**Cause:** GameEngine includes all managers in header
**Solution:** Forward declarations + includes in .cpp

### Issue 4: Layer Violations

**Symptom:** Manager includes State header
**Cause:** Manager needs state-specific logic
**Solution:** Dependency inversion - state registers callback with manager

### Issue 5: Utils Dependencies

**Symptom:** Utils including Core or Manager headers
**Cause:** Utils trying to use engine-specific types
**Solution:** Make Utils pure (STL only), or move to appropriate layer

---

## Performance Expectations

- **Quick Circular Check:** 2-3 minutes (scan + cycle detection)
- **Coupling Analysis:** 5-10 minutes (metrics + matrix)
- **Full Architecture Audit:** 15-20 minutes (all checks + visualization)
- **Specific Component:** 3-5 minutes (single component deep dive)

**Manual Equivalent:** 60-120 minutes per full audit

---

## Exit Codes

- **0:** No architectural issues detected
- **1:** Circular dependencies found (BLOCKING)
- **2:** Layer violations detected (CRITICAL)
- **3:** High coupling detected (WARNING)
- **4:** Multiple issues detected

---

## Important Notes

1. **Run regularly** - Architecture degrades over time without monitoring
2. **Fix issues promptly** - Small issues compound into major refactors
3. **Document patterns** - Share good architectural examples with team
4. **Automate checks** - Consider pre-commit hooks for critical violations
5. **Track trends** - Monitor health score over time
6. **Game Engine Context** - Remember that tight manager coupling is often **functionally necessary**

---

## Scoring Guidance for Game Engines

**Coupling Strength Score Calculation:**

When scoring coupling (20% of health score), distinguish between:

1. **Functional Coupling** (✅ Good, score: 8-10/10)
   - Game systems that must interact to work
   - Examples: AI→Collision, Collision→World, Managers→Events
   - These are **correct design** and should NOT reduce the score significantly

2. **Problematic Coupling** (🔴 Bad, score: 0-4/10)
   - Circular dependencies (breaks compilation)
   - Layer violations (Manager→State)
   - Unclear/unnecessary dependencies

**Scoring Formula:**
```
Coupling Score = 10 - (problematic_coupling_count * 1.5)

Where problematic_coupling_count =
  - Circular dependencies found
  - Layer-violating dependencies
  - Non-functional tight coupling (unclear purpose)

Functional coupling does NOT reduce score.
```

**Example:**
- 0 problematic, 9 functional: **Score = 10/10** ✅ Excellent
- 1-2 problematic, 9 functional: **Score = 7-8.5/10** ✅ Good
- 3-5 problematic, 9 functional: **Score = 4-6/10** ⚠️  Needs work
- 6+ problematic: **Score = 0-2/10** 🔴 Critical

This scoring recognizes that game engines NEED manager coupling to function.

---

**Ready to analyze HammerEngine architecture. Ask user for analysis mode.**
