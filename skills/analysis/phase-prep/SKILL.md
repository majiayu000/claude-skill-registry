---
name: phase-prep
description: Research Godot source code to prepare critical implementation notes for upcoming phases. Use before implementing phases to avoid debugging sessions and discover Godot quirks upfront.
---

# Phase Prep: Godot Source Research for Implementation Planning

## Overview

This skill helps prepare for implementing a new phase by researching Godot's DAP implementation using the `godot-source` MCP server. The goal is to extract non-obvious insights, discover quirks, and create strategic implementation notes that will help the implementing agent avoid debugging sessions.

**Key Principle**: Extract insights and point to details, don't duplicate code. The implementing agent will also have access to `godot-source`.

**Examples of valuable findings from previous phases:**
- ✅ **stepOut command not implemented** (would have caused hang without this knowledge)
- ✅ **ConfigurationDone required** (breakpoints timeout without it)
- ✅ **Two-step launch process** (launch + configurationDone to trigger)
- ✅ **Event filtering critical** (DAP sends async events mixed with responses)

---

# Process

## 🎯 Phase 1: Understand the Phase Plan

### 1.1 Read the Phase Details

First, understand what the phase is supposed to implement:

```bash
# Read the phase from PLAN.md
Read docs/PLAN.md

# Focus on the target phase section:
# - Tools to implement
# - Success criteria
# - Critical implementation notes
# - Any existing warnings or TODOs
```

### 1.2 Extract Investigation Targets

Create a list of commands/features to research:

**Example for Phase 6 (Advanced Debugging)**:
- [ ] Pause/resume commands
- [ ] SetVariable command
- [ ] Scene tree inspection
- [ ] Any special events these trigger

### 1.3 Review Previous Phase Patterns

Check what patterns we established that should be verified:

```bash
# Review our established patterns
Read .serena/memories/critical_implementation_patterns.md

# Common patterns to verify against Godot:
# - Event filtering requirements
# - Timeout recommendations
# - Parameter validation
# - Response format expectations
```

---

## 🔍 Phase 2: Research Godot Source

### 2.1 Check Godot Memories First

Start with the curated memories (fastest):

```bash
# Use godot-source MCP server to list available memories
mcp__godot-source__list_memories()

# Read relevant memories for the phase, especially focus on those that being with "dap_".
# For example:
mcp__godot-source__read_memory("dap_supported_commands")
mcp__godot-source__read_memory("dap_known_issues_and_quirks")
mcp__godot-source__read_memory("dap_implementation_reference")
mcp__godot-source__read_memory("dap_events_and_notifications")
```

**Key memories for DAP implementation:**
# Note: The most up to date list is available from `mcp__godot-source__list_memories()`:
- `dap_supported_commands` - Which commands are actually implemented
- `dap_known_issues_and_quirks` - Known bugs and limitations
- `dap_implementation_reference` - Code examples and patterns
- `dap_events_and_notifications` - Event handling details
- `dap_connection_and_config` - Setup requirements

### 2.2 Verify Command Support

For each command/feature in the phase, verify Godot support:

```bash
# Search for command implementation. 
# For example, if we were looking for "pause":
mcp__godot-source__search_for_pattern(
  substring_pattern="handle_pause|case.*pause",
  restrict_search_to_code_files=true
)

# Find handler methods
mcp__godot-source__find_symbol(
  name_path="DebugAdapterProtocol",
  depth=1,
  include_body=false
)
```

### 2.3 Extract Critical Insights

For each command, document:

**Command Support:**
- ✅ Implemented / ❌ Not Implemented / ⚠️ Partially Implemented

**Critical Insights** (non-obvious behavior):
- Event types triggered
- Required parameters
- Parameter validation quirks
- Response format specifics
- Known issues or limitations

**Example Investigation:**
```bash
# Find pause command implementation
mcp__godot-source__find_symbol(
  name_path="DebugAdapterProtocol/handle_pause",
  include_body=true,
  relative_path="modules/godot_dap/"
)

# Check what events it sends
mcp__godot-source__search_for_pattern(
  substring_pattern="send.*stopped.*pause",
  relative_path="modules/godot_dap/"
)
```

### 2.4 Compare with Our Patterns

Verify our established patterns match Godot's implementation:

**Event Filtering:**
- Does this command send async events?
- What event types should we filter?
- Are there race conditions?

**Timeout Requirements:**
- How long might this command take?
- Are there blocking operations?
- Recommended timeout duration?

**Parameter Validation:**
- What parameters are required?
- What formats does Godot expect?
- Are there validation quirks?

---

## 📝 Phase 3: Create Implementation Notes

### 3.1 Create the Notes Document

Create a new document for the phase implementation notes:

**File location**: `docs/PHASE_<N>_IMPLEMENTATION_NOTES.md`

**Template structure**:
```markdown
# Phase <N> Implementation Notes

**Phase**: <Phase Name>
**Research Date**: <YYYY-MM-DD>
**Researcher**: <Agent/Human>

## Overview

Brief summary of what this phase implements and key findings.

## Command Support Matrix

**Example**

| Command | Godot Support | Notes |
|---------|---------------|-------|
| pause | ✅ Implemented | Sends 'stopped' event with reason='pause' |
| resume | ✅ Implemented | Same as 'continue' command |
| setVariable | ❌ Not Implemented | Use evaluate() workaround |

## Critical Implementation Hints

### <Command Name>

**Status**: ✅/❌/⚠️

**Critical Insight**: <Non-obvious behavior that prevents debugging>

**Implementation Reference**:
- godot-source: `<file>:<line>-<line>`
- Our pattern: `<our_file>:<line>-<line>`

**Parameters**:
- <param>: <type> - <validation notes>

**Events Triggered**:
- <event_type> - <when and why>

**Known Issues**:
- <issue> - <workaround>

**Example**:
```json
{
  "command": "...",
  "arguments": { ... }
}
```

## Event Handling Requirements

Document any special event filtering or async handling needed.

## Parameter Validation

Document validation quirks or requirements.

## Recommended Patterns

Based on Godot implementation, recommend:
- Timeout durations
- Event filtering strategies
- Error handling approaches
- Parameter validation

## Integration with Existing Code

How these new commands fit with our Phase 3-4 patterns:
- Session management
- Event filtering
- Timeout protection
- Error messages

## Testing Recommendations

Suggest test scenarios based on quirks found:
- Edge cases discovered
- Error conditions
- Event ordering issues

## Open Questions

List any uncertainties or areas needing manual testing.
```

### 3.2 Fill in the Template

For each command/feature, fill in all sections with specific findings.

**Guidelines:**
- ✅ **DO** extract non-obvious insights (like ConfigurationDone requirement)
- ✅ **DO** reference godot-source files with line numbers
- ✅ **DO** highlight quirks and gotchas
- ✅ **DO** recommend specific timeout values
- ❌ **DON'T** duplicate entire Godot functions (point to them instead)
- ❌ **DON'T** write speculative notes (verify in source)
- ❌ **DON'T** duplicate what's already in PLAN.md

### 3.3 Cross-Reference with Existing Docs

Link to relevant existing documentation:

- `docs/ARCHITECTURE.md` - For pattern alignment
- `docs/IMPLEMENTATION_GUIDE.md` - For component integration
- `docs/reference/DAP_PROTOCOL.md` - For protocol details
- `docs/reference/GODOT_DAP_FAQ.md` - For troubleshooting

---

## 🔄 Phase 4: Update Memories (If Needed)

### 4.1 Check for New Critical Patterns

If you discover new critical patterns, update memories:

**New pattern triggers:**
- Command has unexpected behavior (like stepOut hang)
- Required setup steps (like ConfigurationDone)
- Event handling quirks
- Parameter validation edge cases

```bash
# Update critical_implementation_patterns.md if needed
mcp__source__write_memory(
  memory_name="critical_implementation_patterns",
  content="<updated_content_with_new_pattern>"
)
```

### 4.2 Document Godot-Specific Quirks

If you find Godot limitations or quirks:

```bash
# Consider updating project_overview.md with new insights
mcp__source__read_memory("project_overview")

# Add to "Key Technical Insights" section if significant
```

### 4.3 Update Implementation Guide (If Pattern Changes)

If research reveals we need to change our approach:

```bash
Read docs/IMPLEMENTATION_GUIDE.md

# Update relevant sections if:
# - New event filtering pattern needed
# - Different timeout strategy required
# - Parameter validation approach changes
```

---

## ✅ Phase 5: Verify Completeness

### 5.1 Self-Review Checklist

```
Phase Prep Checklist - Phase <N>

Research Complete:
- [ ] Read complete phase plan from PLAN.md
- [ ] Checked all relevant godot-source memories
- [ ] Verified command support for all phase tools
- [ ] Extracted critical insights (at least 3 non-obvious findings)
- [ ] Found and documented known issues/quirks
- [ ] Identified event handling requirements
- [ ] Documented parameter validation quirks

Documentation Created:
- [ ] Created PHASE_<N>_IMPLEMENTATION_NOTES.md
- [ ] Filled in command support matrix
- [ ] Documented critical insights with godot-source references
- [ ] Added event handling requirements
- [ ] Listed parameter validation notes
- [ ] Recommended timeout values
- [ ] Suggested test scenarios

Cross-References:
- [ ] References godot-source files with line numbers
- [ ] Points to our existing patterns for comparison
- [ ] Links to relevant docs (ARCHITECTURE, IMPLEMENTATION_GUIDE)
- [ ] Cross-referenced with DAP_PROTOCOL.md

Memory Updates (if applicable):
- [ ] Updated critical_implementation_patterns.md (if new patterns)
- [ ] Updated project_overview.md (if significant quirks)
- [ ] Updated IMPLEMENTATION_GUIDE.md (if approach changes)

Success Criterion:
- [ ] Implementing agent could avoid at least ONE debugging session
```

### 5.2 Test Against Success Criterion

**Success Criterion**: The next agent implementing this phase should be able to avoid at least one debugging session by reading your notes.

**Ask yourself:**
- Would I have known about ConfigurationDone from these notes?
- Would I have known stepOut wasn't implemented?
- Are parameter requirements clear?
- Are event filtering needs documented?

If the answer to any of these is "no", add more detail.

### 5.3 Commit the Research

```bash
# Stage the implementation notes
git add docs/PHASE_<N>_IMPLEMENTATION_NOTES.md

# Stage any memory updates
git add .serena/memories/

# Commit with descriptive message
git commit -m "docs: research Phase <N> Godot implementation

- Verified command support for <N> tools
- Documented <X> critical insights
- Found <Y> known issues/quirks
- Created implementation notes for Phase <N>

Key findings:
- <Finding 1>
- <Finding 2>
- <Finding 3>"
```

---

## 🎯 Quick Reference: Investigation Checklist

For each command in the phase:

```
Command: <command_name>

1. Support Status:
   - [ ] Search godot-source for implementation
   - [ ] Verify in dap_supported_commands memory
   - [ ] Test if partially/fully implemented

2. Critical Insights:
   - [ ] What events does it trigger?
   - [ ] What parameters are required?
   - [ ] Any validation quirks?
   - [ ] Any known issues?

3. Pattern Verification:
   - [ ] Does it need event filtering?
   - [ ] What timeout is recommended?
   - [ ] Does it fit our session management?
   - [ ] Any special error handling?

4. Documentation:
   - [ ] godot-source file reference (file:line)
   - [ ] Our pattern reference (our_file:line)
   - [ ] Example request/response
   - [ ] Test scenario suggestions
```

---

## 💡 Tips for Effective Phase Prep

**Extract Non-Obvious Insights:**
- Focus on behavior that would require debugging to discover
- Document WHY, not just WHAT (explain Godot's reasoning if visible)
- Highlight differences from DAP spec

**Use godot-source Efficiently:**
- Start with memories (fastest, already curated)
- Use symbolic search for specific symbols
- Use pattern search for cross-cutting concerns
- Read implementation only when memories insufficient

**Strategic Redundancy Pattern:**
- Memories: Concise insights (2-3 sentences per command)
- Implementation Notes: Detailed findings with examples
- Both: Reference godot-source files for deep dives

**Focus on Debugging Prevention:**
- "ConfigurationDone required" prevents timeout bugs
- "stepOut not implemented" prevents hang bugs
- "Events sent async" prevents response parsing bugs
- These are the insights that save time

**Compare with Our Patterns:**
- Does Godot match our event filtering approach?
- Are our timeouts adequate?
- Do our error messages cover Godot quirks?
- Will our session management work?

**Document Open Questions:**
- Can't find implementation → Note for manual testing
- Unclear behavior → Flag for investigation during implementation
- Conflicting information → Document both and verify later

---

## 📋 Example: Phase 6 Research Output

Here's what good implementation notes look like:

```markdown
# Phase 6 Implementation Notes

## Command Support Matrix

| Command | Godot Support | Notes |
|---------|---------------|-------|
| pause | ✅ Implemented | Sends 'stopped' event with reason='pause' (not 'breakpoint') |
| continue (resume) | ✅ Implemented | Same as Phase 3 continue command |
| setVariable | ❌ Not Implemented | Use evaluate() as workaround: `var_name = new_value` |
| scopes | ✅ Implemented | Returns SceneTree scope in addition to Locals/Members |

## Critical Implementation Hints

### Pause Command

**Status**: ✅ Implemented in Godot

**Critical Insight**: Pause sends 'stopped' event with reason='pause' (not 'breakpoint').
Our event filtering must handle this variant or pause will appear to hang.

**Implementation Reference**:
- godot-source: `modules/godot_dap/debugger_adapter.cpp:234-256`
- Our pattern: Phase 3 event filtering in `internal/dap/client.go:89-112`

**Events Triggered**:
- `stopped` with `reason: "pause"` (different from breakpoint reason)

**Integration with Our Code**:
Update `waitForResponse()` to accept multiple stop reasons, or create
`waitForStoppedEvent(expectedReasons []string)` helper.

### SetVariable Command

**Status**: ❌ NOT Implemented in Godot

**Critical Insight**: Godot DAP server does NOT implement setVariable command.
However, we can use `evaluate()` as a workaround: `evaluate("var_name = new_value")`.

**Implementation Reference**:
- godot-source: NOT FOUND in `modules/godot_dap/` (searched all files)
- Workaround: `modules/godot_dap/debugger_adapter.cpp:456` (evaluate implementation)

**Recommended Approach**:
1. Document in tool description that setVariable uses evaluate() internally
2. Validate variable name (prevent code injection)
3. Format as: `{variable_name} = {new_value}`
4. Use existing evaluate() DAP method

**Example**:
```go
// Instead of setVariable request, use evaluate
evaluateReq := &dap.EvaluateRequest{
    Arguments: dap.EvaluateArguments{
        Expression: fmt.Sprintf("%s = %v", varName, newValue),
        FrameId:    frameId,
    },
}
```

### Scene Tree Inspection

**Status**: ⚠️ Partially Implemented via Scopes

**Critical Insight**: Godot adds a custom "SceneTree" scope (in addition to standard
Locals/Members/Globals). This scope contains the current scene's node hierarchy.

**Implementation Reference**:
- godot-source: `modules/godot_dap/debugger_adapter.cpp:512-534`
- Returns scope named "SceneTree" with variablesReference to root node

**Integration with Our Code**:
`godot_get_scopes` will already return this scope (no changes needed).
Document in tool description that SceneTree scope is Godot-specific.

**Recommended Pattern**:
Add helper function to identify scope types:
```go
func isSceneTreeScope(scope dap.Scope) bool {
    return scope.Name == "SceneTree"
}
```
```

---

## 🚀 Using These Notes During Implementation

When you (or another agent) implements the phase:

1. **Read implementation notes FIRST** (before writing code)
2. **Reference godot-source files** when you need implementation details
3. **Follow the recommended patterns** (they're based on Godot's actual behavior)
4. **Test the documented edge cases** (they're real quirks, not speculation)
5. **Update notes if you find discrepancies** (keep them accurate for next time)

**Remember**: These notes exist to prevent debugging sessions, not replace them entirely.
If you encounter unexpected behavior, research it and update the notes for the next agent.
