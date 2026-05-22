---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use This vs Alternatives

| Your Situation | Use This | Not These |
|----------------|----------|-----------|
| Any bug, test failure, unexpected behavior | `systematic-debugging` | Random guessing |
| 3+ failed attempts, need more resources | Add `troubleshoot-and-continue` | Giving up |
| Working autonomously, blocked | Both skills together | Stopping early |

**Relationship to `troubleshoot-and-continue`:**
- `systematic-debugging` = Scientific methodology (4 phases)
- `troubleshoot-and-continue` = Resource exhaustion protocol for autonomous work
- **Use together:** After 3 failed attempts in Phase 4, activate `troubleshoot-and-continue` to exhaust all resources before questioning architecture.

## Autonomous Debugging Mode

**When debugging without human interaction:**

### Self-Guided Investigation
- [ ] Phase 1: Root cause investigation (errors, reproduction, evidence)
- [ ] Phase 2: Pattern analysis (find working examples)
- [ ] Phase 3: Hypothesis formation (single clear theory)
- [ ] Phase 4: Implementation (test first, then fix)

### If Blocked (No Progress After 3 Attempts)
1. **Activate `troubleshoot-and-continue`** protocol
2. **Spawn 3 MiniMax subagents** for alternative approaches
3. **Try all suggestions** before stopping
4. **Document attempts** in plan file
5. **Then** question architecture (Phase 4.5)

### Quality Gates (Before Declaring Fixed)
- [ ] Failing test case created BEFORE fix
- [ ] Single fix addresses root cause (not symptom)
- [ ] All tests pass
- [ ] No new warnings/errors introduced
- [ ] Fix verified with evidence

**Remember:** For autonomous work, use ALL resources (subagents, docs, alternatives) before escalating to user.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer system):**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)

5. **Trace Data Flow**

   **WHEN error is deep in call stack:**

   See `root-cause-tracing.md` in this directory for the complete backward tracing technique.

   **Quick version:**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST have before fixing
   - Use the `superpowers:test-driven-development` skill for writing proper failing tests

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with your human partner before attempting more fixes**

   This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## your human partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

These techniques are part of systematic debugging and available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling

**Related skills:**
- **superpowers:test-driven-development** - For creating failing test case (Phase 4, Step 1)
- **superpowers:verification-before-completion** - Verify fix worked before claiming success

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

---

# Godot Systematic Debugging Guide

This section extends systematic debugging for Godot 4.x engine and GDScript development.

## Godot Debugger Usage

### Built-in Debugger (Editor)

1. **Breakpoints**
   - Click line number in script editor
   - F9 to toggle breakpoint
   - Debugger pauses execution, inspect variables

2. **Remote Scene Tree** (Running Project)
   - Scene tab → "Remote" button
   - Inspect live node tree
   - Check property values in real-time
   - Modify properties while running

3. **Output Panel**
   - Check for errors/warnings (red/yellow)
   - `print()` statements appear here
   - Use `push_error()` / `push_warning()` for persistent messages

### Debugger Hotkeys

| Key | Action |
|-----|--------|
| F9 | Toggle breakpoint |
| F10 | Step over |
| F11 | Step into |
| Shift+F11 | Step out |
| F5 | Continue |
| Ctrl+Shift+B | Breakpoint panel |

## Godot Scene Tree Inspection

### Finding Nodes at Runtime

```gdscript
# Print full scene tree
print_tree()

# Print with more detail
print_tree_pretty()

# Find node by name
var player = get_node("/root/Main/Player")
var player = get_node("../Player")  # Relative
var player = $Player  # Shorthand

# Search recursively
var player = find_child("Player", true, false)
```

### Inspecting Node State

```gdscript
# Add temporary debug script
func _process(delta):
    if Input.is_action_just_pressed("debug"):
        print("=== DEBUG STATE ===")
        print("Position: ", global_position)
        print("Velocity: ", velocity)
        print("State: ", current_state)
        print("Children: ", get_children())
        print("===================")
```

### Using the Remote Inspector

1. Run project (F5)
2. Scene dock → "Remote" tab
3. Click any node to see:
   - Properties
   - Signals
   - Groups
   - Current values

4. **Modify values live:**
   - Change position, health, etc.
   - Test edge cases without restarting

## Godot-Specific Debugging Patterns

### Pattern 1: Signal Debugging

```gdscript
# Check if signal is connected
print("Connected: ", my_signal.is_connected(_on_my_signal))

# List all connections
print("Connections: ", my_signal.get_connections())

# Debug all emissions
func _ready():
    my_signal.connect(func(arg):
        print("Signal emitted with: ", arg)
        print_stack()  # Print call stack
    )
```

### Pattern 2: Resource State Tracking

```gdscript
# Track resource changes
@export var my_resource: Resource:
    set(value):
        print("Resource changing from ", my_resource, " to ", value)
        print_stack()
        my_resource = value
```

### Pattern 3: Node Lifecycle Debugging

```gdscript
func _init():
    print("INIT: ", self, " - ", get_instance_id())

func _enter_tree():
    print("ENTER_TREE: ", name, " parent: ", get_parent())

func _ready():
    print("READY: ", name)
    print("Scene unique name: ", is_unique_name_in_owner())

func _exit_tree():
    print("EXIT_TREE: ", name)

func _notification(what):
    if what == NOTIFICATION_PREDELETE:
        print("PREDELETE: ", name)
```

### Pattern 4: Physics Debugging

```gdscript
func _physics_process(delta):
    # Visualize raycasts
    if Engine.is_editor_hint():
        queue_redraw()

func _draw():
    # Draw debug lines
    draw_line(Vector2.ZERO, raycast.target_position, Color.RED, 2.0)
    
    # Draw collision shape
    if collision_shape:
        var rect = collision_shape.shape.get_rect()
        draw_rect(rect, Color.GREEN, false, 2.0)
```

### Pattern 5: State Machine Debugging

```gdscript
var current_state: State:
    set(value):
        if current_state != value:
            print("State: ", current_state, " -> ", value)
            print_stack()
            current_state = value
```

## GDScript Debugging Utilities

### Print Variations

```gdscript
# Basic print
print("Debug message")

# Rich text print (visible in editor)
print_rich("[color=red]Error:[/color] Something failed")

# Error with stack trace
push_error("Critical error occurred!")
push_warning("This is a warning")

# Print to editor console only
print_debug("Only visible in editor runs")
```

### Stack Trace

```gdscript
func problematic_function():
    print("Current function")
    print_stack()  # Prints call stack
    
    # Get stack as array
    var trace = get_stack()
    for frame in trace:
        print(frame.source, ":", frame.line, " - ", frame.function)
```

### Type Checking Debug

```gdscript
# Verify types at runtime
print("Type: ", typeof(variable))
print("Is Node: ", variable is Node)
print("Is CustomClass: ", variable is CustomClass)

# Safe casting with debug
if variable is Enemy:
    var enemy = variable as Enemy
    enemy.take_damage(10)
else:
    push_error("Expected Enemy, got ", typeof(variable))
```

## Common Godot Issues & Debugging

### Issue: Node Not Found

```gdscript
# Debug path resolution
var path = "Player/HealthBar"
print("Checking: ", path)
print("Exists: ", has_node(path))
print("Absolute: ", get_node_or_null("/root/Main/" + path))

# List all children
print("Available nodes:")
for child in get_children():
    print("  - ", child.name)
```

### Issue: Signal Not Emitting

```gdscript
# Check connections
print("Has connections: ", my_signal.get_connections().size() > 0)

# Verify callable is valid
print("Callable valid: ", my_callable.is_valid())

# Debug emission
func emit_my_signal():
    print("About to emit signal")
    my_signal.emit()
    print("Signal emitted")
```

### Issue: Scene Not Instantiating

```gdscript
# Verify packed scene
print("Scene valid: ", packed_scene != null)
print("Scene can instantiate: ", packed_scene.can_instantiate())

# Check after instantiation
var instance = packed_scene.instantiate()
print("Instance valid: ", is_instance_valid(instance))
print("Instance type: ", instance.get_class())
```

### Issue: Autoload (Singleton) Not Working

```gdscript
# Verify autoload is configured
print("GameState exists: ", Engine.has_singleton("GameState"))

# Access and check
print("GameState: ", GameState)
print("GameState properties: ", GameState.get_property_list())
```

## MCP Debugging Integration

When using MCP tools for playtesting:

```bash
# Get scene tree snapshot
mcp__godot__get_scene_tree

# Check specific node state
mcp__godot__get_node_properties --path /root/Main/Player

# Trigger input for reproduction
mcp__godot__send_input --action move_right --pressed true
```

See `playtesting` skill for full debugging workflow with MCP.

## Godot Debugging Checklist

Before claiming a bug is fixed:

- [ ] Used editor debugger to step through code
- [ ] Inspected remote scene tree during runtime
- [ ] Checked output panel for errors/warnings
- [ ] Added `print()` / `push_error()` at key points
- [ ] Verified signal connections
- [ ] Checked node paths with `has_node()` / `get_node_or_null()`
- [ ] Confirmed `_ready()` order with lifecycle prints
- [ ] Tested in isolation (minimal reproduction)
- [ ] All GUT tests pass
- [ ] No new warnings introduced

## Related Skills

- `test-driven-development` - Write failing test before fix
- `playtesting` - MCP-based runtime inspection
- `godot` - General Godot development patterns
