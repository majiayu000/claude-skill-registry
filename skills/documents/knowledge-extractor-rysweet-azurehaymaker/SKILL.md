---
name: knowledge-extractor
version: 1.0.0
description: |
  Extracts key learnings from conversations, debugging sessions, and failed attempts.
  Use at session end or after solving complex problems to capture insights.
  Automatically suggests updates to: DISCOVERIES.md (learnings), PATTERNS.md (reusable solutions), new agent creation (repeated workflows).
  Ensures knowledge persists across sessions.
---

# Knowledge Extractor Skill

## Purpose

This skill automatically extracts, synthesizes, and preserves knowledge from conversations, debugging sessions, failed attempts, and solved problems. It converts ephemeral interactions into persistent organizational knowledge that improves future performance.

## When to Use This Skill

- **Session End Analysis**: Extract learnings before session context is lost
- **After Complex Debugging**: Capture root causes and solutions while fresh
- **Following Failed Attempts**: Document what didn't work and why
- **Successful Problem Solving**: Preserve solutions for future reuse
- **New Pattern Discovery**: Identify patterns that should be documented
- **Repeated Workflows**: Recognize when to create new specialized agents
- **Cross-Session Learning**: Build organizational memory from individual sessions

## Core Philosophy: Knowledge Preservation

**Session Context**: Ephemeral conversation context that will be lost without active preservation
**Persistent Knowledge**: Structured learnings that improve future performance
**Pattern Recognition**: Identifying when solutions are repeated and should be automated
**Organizational Growth**: Converting individual learning into system-wide improvement

## Knowledge Extraction Framework

### Three Types of Knowledge Extraction

#### 1. Discoveries - Novel Insights and Root Causes

**What it captures**: Problems encountered, root causes identified, solutions implemented

**When to extract**:

- After solving a complex bug
- When debugging reveals unexpected behavior
- When discovering wrong assumptions
- After identifying missing functionality
- When learning why something failed

**Format for DISCOVERIES.md**:

```markdown
## [Brief Title] (YYYY-MM-DD)

### Issue

What problem or challenge was encountered?

### Root Cause

Why did this happen? What was the underlying issue?

### Solution

How was it resolved? Include code examples if relevant.

### Key Learnings

What insights were gained? What should be remembered?

### Prevention

How can this be avoided in the future?
```

**Quality Criteria**:

- ✅ Specific problem, not generic advice
- ✅ Root cause clearly identified
- ✅ Working solution included
- ✅ Learning generalized for reuse
- ✅ Prevention strategy documented

#### 2. Patterns - Reusable Solutions

**What it captures**: Proven solutions to recurring problems, architectural approaches, design patterns

**When to extract**:

- After solving a problem similar to known patterns
- When recognizing a repeated problem type
- When implementing a proven solution
- When discovering a best practice that works
- When solution applies across multiple contexts

**Format for PATTERNS.md**:

```markdown
## Pattern: [Name]

### Challenge

What problem does this pattern solve?

### Solution

How does the pattern work? Include code/examples.

### Key Points

- Main insight 1
- Main insight 2
- When to use / when not to use

### When to Use

Specific scenarios where this pattern applies.

### Real Impact

Where has this pattern been used successfully?

### Related Patterns

Links to similar or complementary patterns.
```

**Quality Criteria**:

- ✅ General enough to apply to multiple situations
- ✅ Problem clearly defined
- ✅ Solution has proven track record
- ✅ Working code examples
- ✅ Clear when/when-not-to-use guidance

#### 3. Agent Creation - Automation of Repeated Workflows

**What it captures**: Workflows that are repeated frequently, specialized expertise areas, complex multi-step processes

**When to extract**:

- After performing the same workflow 2-3 times
- When recognizing a specialized skill area
- When workflow has clear inputs/outputs
- When automating would save significant time
- When problem domain is narrow and well-defined

**Agent Creation Trigger Checklist**:

- [ ] Same workflow repeated 2+ times
- [ ] Workflow takes 30+ minutes to execute
- [ ] Workflow has clear specialized focus
- [ ] Workflow can be automated with current tools
- [ ] Problem domain is narrow and well-defined
- [ ] Would be high-value to automate

**Example Agent Creation**:

```markdown
## Recommended New Agent: [domain]-[specialty]

### Problem

What repeated workflow would this agent handle?

### Scope

What's in scope | What's explicitly out of scope

### Inputs

What information does the agent need?

### Process

Step-by-step workflow the agent follows

### Outputs

What does the agent produce?

### Value

How much time/effort does this save?

### Integration

Where in the workflow does this fit?
```

## Step-by-Step Extraction Process

### Step 1: Session Analysis (5 minutes)

Review entire conversation/session:

```
1. What was the original problem/request?
2. What approaches were tried?
3. Which attempts failed and why?
4. What succeeded and why?
5. What was learned in the process?
6. What surprised you?
7. What took longer than expected?
8. What would have helped?
```

### Step 2: Pattern Recognition (5 minutes)

Identify patterns in the work:

```
1. Have I seen this problem before? (→ DISCOVERIES)
2. Is this a generalizable solution? (→ PATTERNS)
3. Would this be worth automating? (→ AGENT)
4. What was the root cause? (Why, not just what)
5. What should others know about this?
6. What should be remembered to avoid repetition?
```

### Step 3: Knowledge Extraction (10 minutes)

Extract and structure knowledge:

**For DISCOVERIES.md**:

- Specific issue encountered
- Root cause analysis
- Solution implemented
- Key learnings generalized
- Prevention strategy

**For PATTERNS.md**:

- Problem the pattern solves
- How the pattern works
- When to use / when not to use
- Working code examples
- Related patterns

**For New Agent**:

- Repeated workflow identified
- Clear scope and boundaries
- Input/output requirements
- Step-by-step process
- Expected value/time savings

### Step 4: Integration (3 minutes)

Place knowledge in correct locations:

```
DISCOVERIES.md → New discovery at end of file
PATTERNS.md → New pattern in appropriate section
Agent → Create in .claude/agents/amplihack/specialized/
```

### Step 5: Validation (2 minutes)

Ensure quality:

```
[ ] Entry is specific, not generic
[ ] Entry follows template format
[ ] Examples/code provided
[ ] Quality sufficient for reuse
[ ] Grammar and clarity checked
[ ] Related items cross-referenced
```

## Usage Examples

### Example 1: Extract Discovery After Bug Fix

**Scenario**: Just spent 45 minutes debugging why pre-commit hooks weren't working

```
User: Extract what we learned from debugging the pre-commit issue.

Claude:
1. Analyzes conversation showing:
   - Initial problem: hooks appeared to run but didn't modify files
   - False leads: blamed merge conflicts, tool versions
   - Root cause found: Hooks couldn't write to files due to cloud sync lock
   - Solution: Added exponential backoff retry logic
   - Time to discover: 45 minutes

2. Creates DISCOVERIES.md entry:
   - Issue: Pre-commit hooks silently failing
   - Root Cause: Cloud sync (OneDrive) file locks
   - Solution: Exponential backoff retry (0.1s, 0.2s, 0.4s...)
   - Key Learning: Cloud sync issues silent - need defensive coding
   - Prevention: Add retry logic for file I/O, test with cloud storage

3. Offers to also:
   - Add pattern for "Resilient File I/O" to PATTERNS.md
   - Suggest new agent for cloud-sync issue detection
```

### Example 2: Extract Pattern from Successful Implementation

**Scenario**: Just finished implementing module regeneration strategy

```
User: Extract the pattern we discovered for building regeneratable modules.

Claude:
1. Analyzes implementation showing:
   - Clear __all__ exports defining public interface
   - Self-contained module structure
   - Type-hinted functions with docstrings
   - Comprehensive test coverage
   - Working examples

2. Creates PATTERNS.md entry:
   - Pattern: Module Regeneration Structure
   - Challenge: Modules become tightly coupled, hard to regenerate
   - Solution: Brick & studs design with __all__ public API
   - Key Points: Clear contracts, single responsibility, testable behavior
   - When to Use: Any utility module, anything that might be regenerated
   - Real Impact: Enables AI to rebuild modules without breaking system

3. Cross-references:
   - Relates to "Bricks & Studs Module Design"
   - Enables "Builder Agent Workflow"
```

### Example 3: Identify New Agent Creation Opportunity

**Scenario**: Just debugged CI failure using 5-step diagnostic process for 3rd time

```
User: We keep using the same CI debugging process. Should we automate it?

Claude:
1. Analyzes past sessions:
   - Session 1: 45 minutes CI debugging (version mismatch issue)
   - Session 2: 30 minutes CI debugging (pre-commit hook issue)
   - Session 3: 25 minutes CI debugging (merge conflict issue)
   - Pattern: Same 5-step process each time

2. Recommends new agent:
   - Name: ci-diagnostic-workflow
   - Problem: Each CI failure requires manual diagnosis, takes 30-45 min
   - Scope: Diagnoses CI failures, suggests fixes (doesn't auto-fix)
   - Process:
     1. Check environment (Python version, tool versions)
     2. Analyze CI logs for error patterns
     3. Detect common issues (conflicts, missing deps)
     4. Suggest solutions
     5. Coordinate parallel diagnostic agents
   - Value: Reduce diagnosis time from 45 min → 15 min

3. Proposes creating:
   - .claude/agents/amplihack/ci-diagnostic-workflow.md
   - Can delegate to: fix-agent for implementation
```

### Example 4: Multi-Level Extraction

**Scenario**: Complex architectural decision with multiple learnings

```
User: Extract everything we learned from deciding on the memory architecture.

Claude:
1. Session involved:
   - 2 failed approaches (too complex, wrong threat model)
   - 1 successful approach (simple, fits threat model)
   - Discovery of meta-pattern for architecture decisions

2. Creates THREE extractions:

   DISCOVERIES.md:
   - Issue: Pattern Applicability Analysis
   - Root Cause: Importing patterns without validating threat match
   - Solution: Five-phase applicability analysis framework
   - Learning: Threat model match is critical first check

   PATTERNS.md:
   - New Pattern: Threat Model Precision Principle
   - Challenge: Fault tolerance mechanisms mismatch problem space
   - Solution: Validate threat model before adopting patterns
   - When: Before adopting any "best practice" from different domain

   Recommended Agent:
   - Name: pattern-applicability-analyzer
   - Automate: Quick assessment of pattern applicability
   - Value: Prevent adopting wrong patterns early
```

## Knowledge Quality Checklist

Before finalizing an extraction, verify:

### For DISCOVERIES.md

- [ ] Issue is specific, not generic ("Pre-commit hooks failing" not "Tools broken")
- [ ] Root cause is identified (Why, not just what)
- [ ] Solution is working/proven
- [ ] Learning is generalized (applies beyond this specific case)
- [ ] Prevention strategy is actionable
- [ ] No speculation or future-proofing
- [ ] Code examples provided where relevant

### For PATTERNS.md

- [ ] Problem is clear and recognizable
- [ ] Solution has proven track record (used 2+ times successfully)
- [ ] When/when-not-to-use guidance is clear
- [ ] Pattern is general enough for reuse
- [ ] Code examples are working and clear
- [ ] Related patterns are cross-referenced
- [ ] Real impact or usage is documented

### For New Agent

- [ ] Workflow has been repeated 2+ times
- [ ] Would save 30+ minutes per execution
- [ ] Problem domain is narrow and well-defined
- [ ] Inputs and outputs are clear
- [ ] Step-by-step process documented
- [ ] High-value worth the automation effort
- [ ] Clear where it fits in workflow

## Integration with System

### DISCOVERIES.md Lifecycle

1. **Extraction**: Added to DISCOVERIES.md during session
2. **Visibility**: Immediately available to all agents
3. **Action**: Agents can reference when solving similar problems
4. **Prevention**: Prevents repeating same mistakes
5. **Evolution**: Updated when better solution found

### PATTERNS.md Lifecycle

1. **Extraction**: Added to PATTERNS.md when pattern proven
2. **Catalog**: Becomes part of available patterns library
3. **Usage**: Referenced in relevant agent instructions
4. **Teaching**: Used in documentation and onboarding
5. **Refinement**: Improved as more usage data collected

### Agent Creation Lifecycle

1. **Recommendation**: Identified as valuable automation candidate
2. **Proposal**: Presented to system with expected value
3. **Creation**: New agent created with clear scope/boundaries
4. **Integration**: Added to delegation triggers in CLAUDE.md
5. **Usage**: Available for orchestration across workflows

## Real-World Impact Examples

### Impact 1: Prevent Wasted Debugging Time

**Without knowledge extraction**: Repeat same 45-minute debugging process
**With extraction**: Reference DISCOVERIES.md, fix in 10 minutes

### Impact 2: Faster Solution Discovery

**Without extraction**: Rediscover solutions from scratch
**With extraction**: Reference PATTERNS.md, apply known solution

### Impact 3: Automated Workflows

**Without extraction**: Manual CI debugging every time (30-45 min)
**With new agent**: Automated diagnosis in 5-10 minutes

## Common Extraction Mistakes to Avoid

### Mistake 1: Too Generic

```
BAD: "Learned that good error handling is important"
GOOD: "Discovered cloud sync issues cause silent file I/O failures - need exponential backoff retry"
```

### Mistake 2: Missing Root Cause

```
BAD: "CI failed, fixed it"
GOOD: "CI failed because version mismatch (local 3.12 vs CI 3.11) - fixed by updating pyproject.toml version constraint"
```

### Mistake 3: No Actionable Learning

```
BAD: "This was complicated"
GOOD: "Multi-layer sanitization at every data transformation prevents credential leakage"
```

### Mistake 4: Over-Generalizing Pattern

```
BAD: "Always use caching everywhere"
GOOD: "Use smart caching with lifecycle management for expensive operations where results may become stale"
```

### Mistake 5: Agent Creation Without ROI

```
BAD: "Create agent for task that happens once per quarter"
GOOD: "Create agent for CI debugging workflow that happens 2-3x per week and takes 30-45 minutes"
```

## Extraction Prompts

Use these prompts to trigger knowledge extraction:

### Extract Discoveries

```
Extract what we discovered/learned from this session.
Focus on: root causes, unexpected behaviors, solutions that worked.
Update DISCOVERIES.md appropriately.
```

### Extract Patterns

```
What patterns should we capture for future reuse?
These should be proven solutions that apply to multiple situations.
Update PATTERNS.md appropriately.
```

### Identify Agent Opportunities

```
Should we create a new agent to automate any repeated workflows?
Check if any workflow has been done 2+ times and takes 30+ minutes.
Recommend creation with scope and value calculation.
```

### Full Extraction

```
Perform complete knowledge extraction on this session.
Extract: discoveries, patterns, and agent creation recommendations.
Verify quality and update all three knowledge bases.
```

## Integration Points

### With Document-Driven Development

- Use knowledge extraction to update specs and documentation
- Extract patterns to guide next implementation

### With Agent Delegation

- Extract when delegating reveals new specializations needed
- Create agents based on repeated delegation patterns

### With Pre-Commit Analysis

- Extract discoveries about CI/CD and testing patterns
- Update PATTERNS.md with new approaches discovered

### With Session Reflection

- Automatic knowledge extraction at session end
- Preserve learnings before context compaction

## Success Metrics

Track effectiveness of knowledge extraction:

- **Discoveries Reused**: How often DISCOVERIES.md prevents mistakes (target: 80%+)
- **Patterns Applied**: How often PATTERNS.md enables faster solutions (target: 70%+)
- **Agent Usage**: How often extracted agents used vs manual approaches (target: 60%+)
- **Time Saved**: Cumulative time saved by reusing knowledge (target: hours/week)
- **Repeated Mistakes**: Reduction in making same mistake twice (target: 95%+)

## Future Evolution

This skill should grow based on:

- What types of knowledge are most valuable to extract?
- What prevents good extraction?
- How can we make extractions more actionable?
- What knowledge sources are underutilized?
- How can we better surface relevant knowledge?

Document learnings in `.claude/context/DISCOVERIES.md`.
