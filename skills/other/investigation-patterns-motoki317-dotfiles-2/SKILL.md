---
name: Investigation Patterns
description: This skill should be used when the user asks to "investigate code", "analyze implementation", "find patterns", "understand codebase", "debug issue", "find bug", "troubleshoot", or needs evidence-based code analysis and debugging. Provides systematic investigation and debugging methodology.
---

# Evidence-Based Investigation Patterns

## Critical Rules
- Always provide `file:line` references for findings (e.g., `path/to/file.ext:42`)
- Rate confidence (0-100) and coverage (0-100) for all results
- Complete investigation before proposing solutions
- Independently verify claims; don't confirm assumptions

## Investigation Phases

### 1. Scope Classification
- **Architecture** - System design, component relationships
- **Implementation** - Specific code behavior, algorithm details
- **Debugging** - Error causes, unexpected behavior
- **Design** - Pattern usage, code organization

### 2. Evidence Collection
Use Serena tools in order of preference:
1. `find_symbol` - Locate specific symbols
2. `get_symbols_overview` - Understand file structure
3. `find_referencing_symbols` - Trace dependencies
4. `search_for_pattern` - Find patterns across codebase

### 3. Synthesis with Metrics
- Combine evidence from multiple sources
- Confidence: 90-100 (direct evidence), 70-89 (strong inference), 50-69 (gaps exist), <50 (speculation)
- Coverage: 90-100 (all files), 70-89 (most files), 50-69 (key files), <50 (limited)

## Debugging Workflow

1. **Reproduce** - Confirm exact steps, environment, consistency
2. **Isolate** - Narrow scope (git bisect, minimal reproduction)
3. **Investigate** - Examine errors, logs, trace data flow
4. **Hypothesize** - List causes, rank likelihood, design tests
5. **Fix** - Minimal change, verify resolution, add regression test

## Common Bug Patterns
- **Null reference** - Check all paths to null access
- **Race condition** - Look for shared mutable state, async operations
- **Off-by-one** - Verify loop boundaries, index calculations
- **Resource leak** - Check acquisition/release paths
- **Encoding issue** - Trace encoding at each transformation

## Output Formats

### Investigation Report
```
Question: [restate question]
Investigation: [findings with file:line refs]
Conclusion: [evidence-based answer]
Metrics: Confidence XX, Coverage XX
Unclear Points: [information gaps]
```

### Debugging Report
```
Problem: [clear description]
Root Cause: [with evidence]
Solution: [proposed fix]
Verification: [how to verify]
Prevention: [regression test]
```
