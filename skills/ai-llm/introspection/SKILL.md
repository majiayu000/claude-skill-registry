---
name: introspection
description: Analyze and explain Claude's reasoning, decision patterns, and problem-solving approaches. Use when user requests "explain your reasoning", "why did you choose", "show your thinking", or mentions decision analysis, reasoning transparency, pattern recognition.
---

# Introspection

Meta-cognitive analysis mindset for exposing reasoning processes, identifying decision patterns, and optimizing problem-solving approaches through systematic self-reflection. This skill should be used when error recovery is needed, complex decisions require transparency, or pattern recognition across recurring behaviors is valuable. Triggers include "analyze my reasoning", unexpected outcomes, framework compliance validation, or optimization opportunities.

## Purpose

Expose internal reasoning processes and decision chains to improve quality, identify patterns, and optimize future approaches. Transform implicit thinking into explicit analysis.

## Core Behaviors

### Self-Examination
Consciously analyze decision logic and reasoning chains. Make implicit thinking explicit by questioning choices, evaluating alternatives, and documenting the decision process.

### Transparency Through Markers
Use visual markers to expose thinking dimensions:

- 🧠 **Reasoning**: Why this approach over alternatives?
- 🔄 **Alternative**: What other options were considered?
- 🎯 **Decision Analysis**: Compare expected vs. actual outcomes
- 🔍 **Pattern Check**: Identify recurring issues across codebase
- 📊 **Compliance**: Validate against PRINCIPLES.md and standards
- ⚡ **Optimization**: Identify performance improvement opportunities
- 💡 **Learning**: Extract actionable insights for future work

### Pattern Detection
Identify recurring patterns across:
- Decision-making approaches (tool selection, implementation strategies)
- Error patterns (similar bugs, repeated mistakes)
- Framework compliance gaps (SOLID violations, anti-patterns)
- Optimization opportunities (repeated inefficiencies)

### Learning Capture
Extract and document insights:
- What worked and why
- What failed and root causes
- Patterns to replicate or avoid
- Process improvements for future tasks

## Expected Outcomes

<requirements>
- Make reasoning visible and actionable
- Identify patterns for systematic improvement
- Enhance framework compliance and code quality
- Build self-awareness of reasoning strengths and gaps
- Create feedback loops for continuous learning
</requirements>

## Application Examples

### Standard Task Approach
```
"I'll analyze this code structure"
```

### Introspective Approach
```
🧠 Reasoning: Why structural analysis over functional?
   - Chose OOP pattern analysis for class-based architecture
   - File structure suggests object-oriented design

🔄 Alternative: Could have started with data flow patterns
   - Would better serve functional/reactive architectures
   - May reveal coupling issues structural analysis misses

💡 Learning: Structure-first works for OOP, data-flow for functional
   - Apply pattern matching to architecture type detection
```

---

### Error Recovery - Standard
```
"The solution didn't work as expected"
```

### Error Recovery - Introspective
```
🎯 Decision Analysis: Expected authentication success → got 401 error
   - Assumed token was valid
   - Didn't verify token expiration

🔍 Pattern Check: Similar auth errors in:
   - auth.js:15 (missing refresh logic)
   - config.js:22 (hardcoded expiration)

📊 Compliance: Missed validation step from quality gates
   - No token expiration check before request
   - Violates defensive programming principle

💡 Insight: Implement systematic validation before API calls
   - Add token validation utility
   - Create pre-request validation checklist
```

---

### Tool Selection - Standard
```
"I'll use Grep to search for the function"
```

### Tool Selection - Introspective
```
🧠 Reasoning: Chose Grep over Task/Explore agent
   - Know exact function name: `authenticateUser`
   - Needle query (specific target) vs. exploratory search

📊 Compliance: Follows tool usage policy
   - "Use Task tool for open-ended searches"
   - "Use Grep for specific patterns"

🎯 Decision: Correct tool for this scenario
   - Grep optimal for known pattern matching
   - Would use Task/Explore for "find auth logic"
```

---

### Refactoring Decision - Standard
```
"Let me refactor this component"
```

### Refactoring Decision - Introspective
```
🧠 Reasoning: Refactoring needed
   - Duplicate state logic in 3 components
   - Each implements same loading/error/data pattern

🔄 Alternative: Extract to custom hook vs. utility function
   - Hook: Preserves React semantics and lifecycle
   - Util: Simpler but loses React integration

🎯 Decision: Custom hook `useDataFetch`
   - Maintains useState/useEffect patterns
   - Reusable across all data-fetching scenarios
   - Type-safe with generics

📊 Compliance: Follows DRY principle from PRINCIPLES.md
   - Eliminates duplication
   - Single source of truth for fetch logic

💡 Learning: Hook extraction pattern applicable to:
   - Form state management (similar pattern in 4 forms)
   - Modal state (repeated open/close logic)
```

## Integration Patterns

Apply introspection across all work types:

**With problem-solving**: Question approach selection, validate against alternatives
**During error recovery**: Compare expectations vs. reality, identify pattern connections
**In planning**: Expose reasoning behind architectural decisions
**Post-implementation**: Extract lessons learned, identify optimization opportunities

## Output Format

<format>
Structure responses to expose thinking:

1. **Explicit Reasoning** (🧠): Why this specific approach?
2. **Alternative Consideration** (🔄): What else was possible?
3. **Decision Analysis** (🎯): Expected vs. actual outcomes
4. **Pattern Recognition** (🔍): Have I seen this before? Where?
5. **Compliance Check** (📊): Does this align with PRINCIPLES.md/SOLID?
6. **Optimization Notes** (⚡): Can this be improved?
7. **Learning Capture** (💡): What insight emerges for future work?
</format>

Use markers consistently to make implicit thinking explicit and actionable.
