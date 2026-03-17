---
name: skill-creator
version: 1.0.0
author: claude-command-control
created: 2025-11-22
status: active
category: meta
---

# Skill Creator

## Description
Guides the creation of high-quality Claude Skills following established best practices, ensuring discoverability, actionability, and maintainability from the start.

## When to Use This Skill
- When the user says "create a new skill"
- When asked to "help me build a skill for [workflow]"
- When someone mentions "skill template" or "skill scaffold"
- After identifying a repetitive workflow that should be automated

## When NOT to Use This Skill
- When creating one-time commands (use command templates instead)
- When configuring agents (use agent templates instead)
- For simple prompts that don't need reusability

## Prerequisites
- Clear understanding of the workflow to be automated
- 2-5 concrete examples of the workflow in action
- Identified trigger conditions for skill invocation
- Decision: Is this skill simple (500-2K tokens), moderate (2K-8K), or complex (8K-20K)?

## Workflow

### Step 1: Requirements Gathering

Ask the user these critical questions:

**Scoping Questions:**
1. What workflow are you trying to automate?
2. How often does this workflow repeat? (≥3x/week recommended for skill creation)
3. What are the clear success criteria?
4. Can you provide 3-5 concrete examples?
5. Does it require specific domain knowledge or patterns?

**Decision Point:**
- If answers "Yes" to 3+ questions → Proceed to skill creation
- If unclear requirements → Request clarification
- If too broad → Suggest splitting into multiple focused skills

### Step 2: Skill Scoping

Determine complexity tier:

| Complexity | Indicators | Action |
|-----------|-----------|--------|
| **Simple** | Single-step, deterministic, <500 tokens | Use minimal template |
| **Moderate** | Multi-step with decision points, 2K-8K tokens | Use standard template |
| **Complex** | Multi-phase with feedback loops, 8K-20K tokens | Use comprehensive template |

Create `SKILL_SCOPING.md`:
```


# Skill Scoping: [Skill Name]

## Workflow Description

[1-2 paragraph description]

## Complexity Tier

[Simple | Moderate | Complex]

## Token Budget Estimate

[Estimated tokens needed]

## Modularity Decision

- Single skill? [Yes/No]
- If splitting: List of separate skills to create


## Success Metrics

- Time saved per use: [X minutes]
- Expected usage frequency: [N times per week]
- Quality improvement target: [Specific metric]

```

### Step 3: Activation Trigger Definition

**CRITICAL**: This determines invocation reliability.

Work with user to define:

**✅ Explicit Trigger Patterns:**
```


## When to Use This Skill

- When the user asks to "[exact phrase]"
- When [specific context] needs [specific action]
- When [explicit request pattern]

```

**✅ Negative Triggers (prevents false positives):**
```


## When NOT to Use This Skill

- When [similar but different scenario] (use [other-skill] instead)
- When [overlapping context] (use [alternative-tool] instead)

```

**Example - Good Triggers:**
```


## When to Use This Skill

- When user says "create a pull request description"
- When code changes need to be summarized for review
- When generating release notes from commit history


## When NOT to Use This Skill

- When writing individual commit messages (use commit-msg-skill instead)
- When documenting architecture (use architect agent instead)

```

### Step 4: Generate Skill Structure

Based on complexity tier, generate the appropriate template:

**For Simple Skills** → Use Template 2 (Minimal Viable Skill)
**For Moderate Skills** → Use Template 3 (Standard Skill)
**For Complex Skills** → Use Template 4 (Comprehensive Skill)

Create file: `skills/[skill-name]/SKILL.md`

### Step 5: Example Collection

Collect 2-5 concrete examples covering:

1. **Happy Path** (ideal scenario)
2. **Edge Case** (unusual but valid)
3. **Error Scenario** (what failure looks like)

Format each example:
```


### Example [N]: [Scenario Name]

**Input:**
[Concrete input data]

**Expected Output:**
[Expected result with actual content]

**Rationale:**
[Why this example matters]

```

### Step 6: Quality Validation

Run through validation checklist:

- [ ] Skill name follows `[domain]-[action]-[modifier]` convention
- [ ] Description is 100-150 characters (UI-friendly)
- [ ] "When to Use" has 3-5 explicit triggers
- [ ] "When NOT to Use" prevents overlap with other skills
- [ ] Prerequisites are clearly stated
- [ ] Workflow steps use imperative language
- [ ] 2-5 examples provided with actual content
- [ ] Quality standards defined
- [ ] Common pitfalls documented
- [ ] All code fences use proper language identifiers

### Step 7: Integration Planning

Document how this skill integrates with existing system:

```


## Integration with Command & Control System

**Related Agents:**

- [Agent Name]: [How they collaborate]

**Related Commands:**

- /[command]: [When to use vs. this skill]

**MCP Dependencies:**

- [MCP Server Name]: [What data/actions needed]

**Orchestration Notes:**

- Can be chained with: [other-skill-1], [other-skill-2]
- Invoked by: [orchestrator-skill]

```

### Step 8: Testing Strategy

Create `skills/[skill-name]/TESTING.md`:

```


# Testing Strategy: [Skill Name]

## Test Scenarios

### Scenario 1: [Happy Path]

**Input:** [Test input]
**Expected:** [Expected output]
**Pass Criteria:** [Specific criteria]

### Scenario 2: [Edge Case]

**Input:** [Test input]
**Expected:** [Expected output]
**Pass Criteria:** [Specific criteria]

### Scenario 3: [Error Handling]

**Input:** [Invalid input]
**Expected:** [Error message]
**Pass Criteria:** [Graceful failure]

## Manual Testing Checklist

- [ ] Skill invokes when expected
- [ ] Skill doesn't invoke when not expected
- [ ] Output matches examples
- [ ] Error handling works
- [ ] Performance acceptable (<30s for simple, <5min for complex)

```

### Step 9: Deployment Preparation

Create metadata file: `skills/[skill-name]/metadata.json`

```

{
"name": "skill-name",
"version": "1.0.0",
"description": "Brief description for UI",
"author": "team-name",
"created": "2025-11-22",
"last_updated": "2025-11-22",
"status": "active",
"complexity": "moderate",
"category": "developer-productivity",
"tags": ["tag1", "tag2", "tag3"],
"token_budget": "5000",
"usage_frequency_target": "10-per-week",
"integrations": {
"agents": ["builder", "validator"],
"commands": ["/test", "/pr"],
"mcp_servers": ["github"]
}
}

```

### Step 10: Documentation

Generate README for the skill:

`skills/[skill-name]/README.md`

```


# [Skill Name]

**Version**: 1.0.0
**Category**: [Category]
**Complexity**: [Simple|Moderate|Complex]

## Quick Start

Invoke this skill by saying:

```
"[Example trigger phrase]"
```


## What This Skill Does

[2-3 sentence description]

## Prerequisites

- [Requirement 1]
- [Requirement 2]


## Examples

See `SKILL.md` for detailed examples.

## Integration

**Works with:**

- Agents: [list]
- Commands: [list]
- MCP: [list]


## Versioning

- 1.0.0 (2025-11-22): Initial release


## Troubleshooting

**Issue**: Skill doesn't invoke
**Solution**: Verify trigger phrase matches "When to Use" section

**Issue**: Unexpected output
**Solution**: Check examples in SKILL.md for expected format

```

## Examples

### Example 1: Creating a Code Review Skill

**User Request:** "I want a skill that helps me review pull requests systematically"

**Skill Creator Process:**

1. **Requirements Gathering:**
   - Workflow: Systematic PR review following team standards
   - Frequency: 5-10 times per week
   - Success: 90% of reviews catch critical issues
   - Examples: 3 past PR reviews provided
   - Domain knowledge: Team's code review checklist

2. **Scoping:**
   - Complexity: Moderate (multi-step with decision points)
   - Token budget: ~6K tokens
   - Single skill: Yes

3. **Trigger Definition:**
```


## When to Use This Skill

- When user says "review this PR"
- When asked to "code review pull request [number]"
- When someone requests "systematic code review"


## When NOT to Use

- When writing code (use builder agent instead)
- When running tests (use validator agent instead)

```

4. **Generated Skill:** `skills/pr-reviewer/SKILL.md` (see Template 3 for structure)

### Example 2: Creating a Documentation Generator Skill

**User Request:** "We need to automatically generate API documentation from code"

**Skill Creator Process:**

1. **Requirements:**
- Workflow: Parse code → Extract API signatures → Generate markdown docs
- Frequency: Daily as code changes
- Success: Docs 100% accurate with code
- Examples: 5 API endpoints with desired doc format

2. **Scoping:**
- Complexity: Complex (multi-phase with validation loops)
- Token budget: ~12K tokens
- Single skill: Yes

3. **Integration Planning:**
```

**Related Agents:**

- Scribe Agent: Finalizes documentation formatting
- Builder Agent: Provides updated code context

**MCP Dependencies:**

- File System: Read source code files
- GitHub: Commit generated docs

```

4. **Generated Skill:** `skills/api-doc-generator/SKILL.md` (see Template 4 for structure)

## Quality Standards

**Every generated skill MUST have:**
- [ ] Clear, action-oriented trigger phrases
- [ ] 2-5 concrete examples with real content
- [ ] Explicit prerequisites
- [ ] Step-by-step workflow in imperative language
- [ ] Quality acceptance criteria
- [ ] Common pitfalls section
- [ ] Integration notes with existing system
- [ ] Testing strategy

## Common Pitfalls

❌ **Vague Triggers**
```


## When to Use

- When working with code (too broad)

```

✅ **Explicit Triggers**
```


## When to Use

- When user says "review this pull request"
- When code changes need systematic quality assessment

```

❌ **Missing Examples**
```


## Examples

See general documentation for examples.

```

✅ **Concrete Examples**
```


### Example 1: Standard Feature PR

**Input:**
PR #123: Add user authentication
Files changed: auth.js, user.model.js, auth.test.js

**Output:**

## Code Review Summary

**Architecture**: ✅ Follows auth pattern from ARCHITECTURE.md
**Security**: ⚠️ Password hashing needs bcrypt rounds increase
...

```

❌ **Generic Workflow**
```

1. Analyze the input
2. Process it
3. Generate output
```

✅ **Specific Steps**
```


### Step 1: Load PR Context

```bash
gh pr view [PR_NUMBER] --json files,title,body
```


### Step 2: Check Against Standards

Compare changed files against:

- ARCHITECTURE.md design patterns
- SECURITY.md security checklist
...

```

## Version History

- 1.0.0 (2025-11-22): Initial release - supports simple, moderate, and complex skill creation

## Troubleshooting

**Issue**: Created skill doesn't invoke
**Solution**: 
1. Check "When to Use" triggers are explicit and action-oriented
2. Add "When NOT to Use" to prevent overlap
3. Test trigger phrases match user's natural language

**Issue**: Skill too complex
**Solution**: 
1. Re-run scoping step
2. Consider splitting into multiple focused skills
3. Use orchestrator pattern to chain skills

**Issue**: Examples not helpful
**Solution**:
1. Ensure examples use real content, not placeholders
2. Cover happy path, edge case, and error scenario
3. Add "Rationale" explaining why each example matters
