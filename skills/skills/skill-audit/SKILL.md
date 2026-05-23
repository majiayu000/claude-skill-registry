---
name: skill-audit
description: Audits skills for discoverability and triggering effectiveness. Use when reviewing skill descriptions, checking trigger coverage, validating progressive disclosure, fixing invocation issues, or learning skill best practices.
allowed-tools: [Read, Glob, Grep, Bash]
# model: inherit
---

## Reference Files

Advanced skill discovery and optimization guidance:

- [trigger-analysis.md](trigger-analysis.md) - Description analysis methodology and keyword extraction
- [progressive-disclosure.md](progressive-disclosure.md) - SKILL.md size guidelines and reference organization
- [discovery-testing.md](discovery-testing.md) - Test query generation and scoring methodology
- [examples.md](examples.md) - Good vs poor skill examples with before/after fixes

---

# Skill Audit

Audits skills for discoverability and triggering effectiveness by analyzing description quality, trigger phrase coverage, progressive disclosure, and metadata completeness.

## Focus Areas

- **Description Completeness** - What the skill does AND when to use it
- **Trigger Phrase Coverage** - Keywords and patterns that should activate the skill
- **Metadata Quality** - Frontmatter completeness and accuracy
- **Progressive Disclosure** - SKILL.md size vs reference file organization
- **Reference Organization** - File structure, linking, navigation
- **Tool Appropriateness** - allowed-tools matches actual needs

## Audit Framework

### Discovery Analysis

**Critical Question**: Would this skill be discovered and triggered when needed?

**Key Components**:

1. **Description Triggers** - Does frontmatter description contain:
   - What the skill does (capability statement)
   - When to use it (triggering scenarios)
   - Key features (differentiators)
   - User query keywords (how users would ask for it)

2. **Anti-Patterns** - Common discovery killers:
   - "When to Use" section in SKILL.md body (loaded AFTER triggering)
   - Description <50 chars (too vague)
   - Generic description ("helps with tasks")
   - Missing use cases in description
   - Technical jargon without plain language equivalents

3. **Progressive Disclosure Compliance**:
   - SKILL.md lean (<500 lines target)
   - Details in separate reference files
   - References clearly linked from SKILL.md
   - One level deep (no nested subdirectories)

4. **Tool Permission Analysis**:
   - allowed-tools field present and accurate
   - Tools match actual usage in SKILL.md
   - Not overly restrictive or permissive
   - Security implications considered

## Audit Process

### Step 1: Read SKILL.md Frontmatter

Extract and analyze frontmatter:

```yaml
---
name: skill-name
description: Comprehensive description...
allowed-tools: [Tool1, Tool2, Tool3]
---
```

Check for:

- Required fields (name, description)
- Description length (>50 chars minimum)
- allowed-tools presence and accuracy

### Step 2: Analyze Description for Trigger Clarity

Test the description against these questions:

1. **Capability**: What does this skill do? (explicitly stated?)
2. **Triggers**: When should it be used? (scenarios mentioned?)
3. **Keywords**: Would user queries match? (natural language?)
4. **Features**: What makes it unique? (differentiators listed?)

**Score Calculation** (1-10):

- 10: Comprehensive description with all elements
- 7-9: Good description, minor improvements possible
- 4-6: Adequate but missing key triggers
- 1-3: Poor, would rarely be discovered

For detailed trigger analysis methodology, see [trigger-analysis.md](trigger-analysis.md).

### Step 3: Check for Body Boundary Violations

Search SKILL.md body for anti-patterns:

- "When to Use" section (should be in description)
- "Triggers" section (should be in description)
- Use case lists not in description
- Extensive scenario descriptions

**Why This Matters**: Body content is only loaded AFTER the skill is triggered. Information needed for triggering MUST be in the frontmatter description.

### Step 4: Verify Progressive Disclosure

Assess information architecture:

1. **SKILL.md Size**: Count lines (target <500)
2. **Reference Files**: Check for separate reference files alongside SKILL.md
3. **Navigation**: Verify links from SKILL.md to reference files
4. **Flat Structure**: Ensure all files are at skill root, no subdirectories
5. **Orphans**: Find references not linked from SKILL.md

**Scoring**:

- GOOD: SKILL.md <500 lines, clear navigation, proper structure
- NEEDS IMPROVEMENT: SKILL.md >500 lines or poor organization
- N/A: Skill is simple enough to not need references

For progressive disclosure guidelines, see [progressive-disclosure.md](progressive-disclosure.md).

### Step 5: Assess allowed-tools Appropriateness

Compare allowed-tools to actual usage:

1. Extract tools mentioned in SKILL.md body
2. Compare to allowed-tools list
3. Identify missing or excessive permissions
4. Check for security implications

**Common Issues**:

- Missing allowed-tools (overly permissive)
- allowed-tools too restrictive (skill can't work)
- Security concerns (excessive permissions)

### Step 6: Generate Discovery Score and Report

Create comprehensive audit report following output format.

## Output Format

Provide audit reports in this standardized structure:

```markdown
# Skill Audit Report: {name}

**Skill**: {name}
**File**: {path to SKILL.md}
**Audited**: {YYYY-MM-DD HH:MM}

## Summary

{1-2 sentence overview of skill and discoverability assessment}

## Discovery Score

**Overall**: {1-10}/10

- **Description Quality**: {1-10}/10
- **Trigger Coverage**: {1-10}/10
- **Progressive Disclosure**: GOOD | NEEDS IMPROVEMENT | N/A
- **Tool Configuration**: GOOD | NEEDS WORK | MISSING

## Description Analysis

**Current Description**:

> {frontmatter description}

**Length**: {char count} chars

**Strengths**:

- {what works well}
- ...

**Gaps**:

- {missing trigger phrases}
- {missing use cases}
- ...

**Suggested Description**:

> {improved version with better trigger coverage}

## Trigger Coverage

**Would trigger on**:

- "{example query 1}"
- "{example query 2}"
- ...

**Would NOT trigger on** (but should):

- "{missed query 1}" - Missing keyword: {keyword}
- "{missed query 2}" - Missing use case: {use case}
- ...

## Progressive Disclosure Assessment

- **SKILL.md Size**: {line count} lines ({UNDER|OVER} target of 500)
- **References**: {count} reference files
- **Navigation**: {CLEAR|UNCLEAR} - {explanation}
- **Orphaned Files**: {list of unreferenced files}

**Recommendations**:
{specific improvements to structure}

## Tool Configuration

**allowed-tools in frontmatter**: {Yes/No}

{If yes:}
**Declared Tools**: {list from allowed-tools}
**Actual Tools Used**: {list from body}

**Findings**:

- {missing tools}
- {excessive tools}
- {security concerns}

{If no:}
**Impact**: Skill has unrestricted tool access
**Recommendation**: {add allowed-tools or explain why unrestricted is needed}

## Priority Recommendations

1. **Critical**: {must-fix for discoverability}
2. **Important**: {should-fix for better triggering}
3. **Nice-to-Have**: {polish improvements}

## Next Steps

{Specific actions to improve discovery and effectiveness}
```

## Common Discovery Issues

### Description Too Short

**Problem**:

```yaml
description: Helps with git workflows
```

**Why It Fails**: Only 25 chars, missing when/how/what details

**Fix**:

```yaml
description: Automates complete git workflows including branch management, atomic commits with formatted messages, history cleanup, and PR creation. Use when committing changes, pushing to remote, creating PRs, cleaning up commits, or organizing git history.
```

### "When to Use" in Body

**Problem**:

```markdown
## When to Use

- Creating git commits
- Managing branches
- Creating pull requests
```

**Why It Fails**: This info loads AFTER skill is selected, doesn't help discovery

**Fix**: Move all this to frontmatter description

### Missing Trigger Keywords

**Problem**: Description says "version control automation" but users ask "create a commit"

**Why It Fails**: Users don't use technical terms in queries

**Fix**: Include plain language equivalents: "commit changes", "push code", "create pull request"

### Generic Description

**Problem**:

```yaml
description: Meta-evaluation of configurations
```

**Why It Fails**: Doesn't explain what/when/who/how

**Fix**:

```yaml
description: Auto-evaluates Claude Code customizations when reviewing files in .claude/ directory. Use when user asks to review, evaluate, or improve agents, commands, skills, hooks, or output-styles.
```

## Discovery Testing Methodology

For each skill, generate test queries and assess triggering:

### Positive Tests (Should Trigger)

Generate 5 queries based on description that SHOULD trigger:

```text
Skill: git-workflow
Queries:
1. "Help me commit my changes"
2. "I need to create a pull request"
3. "Can you clean up my git history?"
4. "Create atomic commits for these changes"
5. "Push my code and make a PR"
```

### Negative Tests (Should NOT Trigger)

Generate 5 queries that should NOT trigger this skill:

```text
Skill: git-workflow
Queries:
1. "What is git?" (informational, not action)
2. "Explain git rebase" (educational, not workflow)
3. "Show me the git log" (simple command, not workflow)
4. "What branch am I on?" (simple status check)
5. "How does git work?" (conceptual, not action)
```

### Edge Cases (Ambiguous)

Generate queries that might or might not trigger:

```text
Skill: git-workflow
Queries:
1. "I have uncommitted changes" (might need workflow)
2. "Should I create a PR?" (might be asking for advice)
3. "My commits are messy" (might need cleanup)
```

For complete discovery testing methodology, see [discovery-testing.md](discovery-testing.md).

## Best Practices for Skill Discovery

1. **Description Length**: 150-500 characters (sweet spot for comprehensive triggers)
2. **Plain Language**: Include how users actually ask, not just technical terms
3. **Use Cases First**: List when to use before explaining how it works
4. **Keywords Matter**: Include all relevant trigger phrases
5. **Progressive Disclosure**: Keep SKILL.md lean, use separate reference files for details
6. **allowed-tools**: Always specify (documents intent, enables restrictions)
7. **Link References**: Every reference file should be linked from SKILL.md
8. **One Level Deep**: Don't nest references in subdirectories
9. **Clear Navigation**: Use bulleted lists with links to guide readers
10. **Test Discovery**: Generate queries and verify skill would be selected

## Tools Used

This skill uses read-only tools for analysis:

- **Read** - Examine SKILL.md and reference files
- **Grep** - Search for patterns (anti-patterns, trigger phrases)
- **Glob** - Find all skills and reference files
- **Bash** - Execute read-only commands (ls, wc, find for analysis)

No files are modified during audits. Reports can be saved to `~/.claude/logs/evaluations/skills/` by the invoking command or coordinator.

## Integration

### With Other Auditors

- **audit-hook**: Specialized hook validation
- **evaluator**: General correctness and clarity
- **test-runner**: Functional testing
- **audit-coordinator**: Orchestrates multiple auditors

### Usage Examples

**Audit a single skill**:

```text
User: "Audit my hook-audit skill for discoverability"
Assistant: [Reads SKILL.md, analyzes description, generates report]
```

**Improve skill description**:

```text
User: "My skill isn't being triggered, can you help?"
Assistant: [Analyzes description, suggests improvements with trigger phrases]
```

**Check progressive disclosure**:

```text
User: "Is my author-skill skill too long?"
Assistant: [Checks size, references structure, provides recommendations]
```

For detailed examples of good and poor skills, see [examples.md](examples.md).
