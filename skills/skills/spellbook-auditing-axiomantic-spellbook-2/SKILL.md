---
name: spellbook-auditing
description: "Meta-audit skill for spellbook development. Spawns parallel subagents to factcheck docs, optimize instructions, find token savings, and identify MCP candidates. Produces actionable report."
---

# Audit Spellbook

You are auditing the spellbook project itself. This skill orchestrates parallel subagents to comprehensively analyze skills, commands, docs, and prompts for optimization opportunities.

## Invariant Principles

1. **Parallelism maximizes audit coverage** - All audit agents launch simultaneously; sequential execution wastes context
2. **Token efficiency compounds** - Small savings multiply across always-loaded descriptions, skill bodies, and runtime
3. **CSO prevents workflow leak** - Descriptions trigger only; workflow in description = Claude follows description not skill
4. **Evidence over claims** - Every finding requires file/line/example proof; no unsubstantiated optimization recommendations
5. **Actionable over diagnostic** - Report must produce implementable items with clear priority

## Trigger Conditions

Use this skill when:
- User asks to "audit spellbook", "optimize skills", "review spellbook"
- Before major releases to ensure quality
- When concerned about token usage or instruction bloat
- Periodically for maintenance

## Execution Flow

### Phase 1: Launch Parallel Audit Subagents

Launch ALL of these subagents in a SINGLE message (parallel execution):

#### 1. Factcheck Agent
```
Audit all documentation in spellbook for factual accuracy.

Files to check:
- README.md
- docs/**/*.md
- CHANGELOG.md
- Any claims in skill/command descriptions

For each claim found:
1. Identify the assertion
2. Verify against: code, external sources, logical consistency
3. Flag unverifiable or incorrect claims

Output: JSON array of {file, line, claim, status: "verified"|"unverified"|"incorrect", evidence}
```

#### 2. Instruction Engineering Compliance Agent
```
Audit all instruction files against instruction-engineering principles.

Files: skills/*/SKILL.md, commands/*.md, CLAUDE.spellbook.md, AGENTS.spellbook.md

Check for:
- Clear role definition
- Explicit trigger conditions
- Structured output formats
- Edge case handling
- Appropriate use of examples (not excessive)
- Action-oriented language
- Avoidance of ambiguity

Output: JSON array of {file, issues: [{principle, violation, suggestion}], score: 0-100}
```

#### 3. Description Quality Agent (CSO Compliance)
```
Audit skill/command descriptions for Claude Search Optimization (CSO) compliance.

IMPORTANT: Reference the writing-skills skill for authoritative CSO guidance.

For each skill and command, analyze against these principles:

1. **Trigger-Only Rule**: Description should ONLY describe when to use, NEVER summarize workflow
   - BAD: "dispatches subagent per task with code review between tasks" (workflow summary)
   - GOOD: "Use when executing implementation plans with independent tasks" (trigger only)

2. **Start with "Use when..."**: Focus on triggering conditions, symptoms, situations

3. **Include natural keywords**: What would a user say when they need this skill?
   - Include problem symptoms (race conditions, flaky tests, merge conflicts)
   - Include specific contexts (before commit, after test failure, during PR review)

4. **Avoid workflow leakage**: If description mentions steps/phases/process, Claude may
   follow the description instead of reading the full skill (documented bug!)

5. **Third person**: Descriptions are injected into system prompt

6. **Technology-agnostic unless skill is technology-specific**

7. **Under 500 characters** (max 1024 total frontmatter)

8. **Clear either/or delineation**: When multiple trigger conditions exist, use explicit
   enumeration to make each condition clearly independent:
   - BAD: "Use when writing subagent prompts or invoking Task tool or improving skills"
   - GOOD: "Use when: (1) constructing prompts for subagents, (2) invoking the Task tool, or (3) writing/improving skill instructions"

   Ambiguous "or" chains make it unclear which conditions are independent triggers vs. related concepts.

For each description, classify as:
- CSO_COMPLIANT: Follows all principles
- WORKFLOW_LEAK: Contains process/workflow that Claude might follow instead of skill
- MISSING_TRIGGERS: Too vague, missing "Use when..." or specific symptoms
- TOO_BROAD: Would trigger for unrelated tasks
- TOO_NARROW: Missing keywords users would naturally say
- AMBIGUOUS_TRIGGERS: Multiple conditions without clear enumeration (fix with numbered list)

Output: JSON array of {
  file,
  current_desc,
  cso_status: "CSO_COMPLIANT"|"WORKFLOW_LEAK"|"MISSING_TRIGGERS"|"TOO_BROAD"|"TOO_NARROW"|"AMBIGUOUS_TRIGGERS",
  issues: [list of specific violations],
  proposed_desc,
  rationale
}
```

#### 4. Instruction Optimizer Agent
```
Deep audit of instruction content for token optimization.

For each skill/command, identify:
- Semantic overlap between sections
- Extraneous examples that could be removed
- Verbose phrasing that could be tightened
- Sections that could be collapsed/merged
- Overcomplicated workflows that could be simplified
- Repeated patterns that could be extracted

CRITICAL: Optimizations must NOT reduce intelligence or capability.
The goal is SMARTER and SMALLER, not dumber.

Output: JSON array of {file, optimizations: [{section, issue, before_tokens, after_tokens, proposed_change}], total_savings}
```

#### 5. MCP Candidate Agent
```
Analyze tool call patterns across skills/commands for MCP extraction candidates.

Look for:
- Repeated sequences of tool calls (e.g., "read file, grep pattern, edit file")
- Common workflows that multiple skills perform
- Bash commands that could be MCP tools
- File operations that are repeated verbatim

A good MCP candidate:
- Is used 3+ times across different skills
- Has clear input/output contract
- Would save tokens by reducing instruction repetition
- Provides atomic, reusable functionality

Output: JSON array of {pattern, occurrences: [{file, context}], proposed_mcp_name, proposed_signature, token_savings_estimate}
```

#### 6. YAGNI Analysis Agent
```
Audit spellbook for unnecessary complexity and unused features.

Check for:
- Skills that duplicate functionality
- Features that seem unused or untested
- Overly complex workflows that could be simplified
- Configuration options nobody uses
- Dead code paths in instructions
- Skills that are too narrow (could be merged)
- Skills that are too broad (should be split)

Apply the principle: "You Aren't Gonna Need It"

Output: JSON array of {item, type: "skill"|"command"|"feature", concern, recommendation, confidence: "high"|"medium"|"low"}
```

#### 7. Persona Quality Agent (if fun-mode exists)
```
Audit persona/context/undertow lists for quality and variety.

Files: skills/fun-mode/personas.txt, contexts.txt, undertows.txt

Check for:
- Duplicates or near-duplicates
- Entries that are too similar in vibe
- Missing variety in weirdness tiers
- Entries that are too long (token waste)
- Entries that don't synthesize well together
- Quality of creative writing

Output: JSON with {personas: {count, duplicates, quality_issues}, contexts: {...}, undertows: {...}, cross_synthesis_issues}
```

#### 8. Consistency Audit Agent
```
Audit for consistency across all skills and commands.

Check for:
- Inconsistent formatting (some use tables, some don't)
- Inconsistent terminology (same concept, different words)
- Inconsistent section structure
- Inconsistent trigger condition formats
- Inconsistent output format specifications
- Style drift between older and newer skills

Output: JSON array of {inconsistency_type, examples: [{file1, file2, difference}], suggested_standard}
```

#### 9. Dependency Analysis Agent
```
Map dependencies between skills, commands, and MCP tools.

Build a dependency graph:
- Which skills invoke other skills?
- Which skills depend on specific MCP tools?
- Which skills have circular dependencies?
- Which skills are orphaned (nothing invokes them)?
- Which skills are over-invoked (too central, single point of failure)?

Output: JSON with {graph: {nodes, edges}, orphans, circular_deps, hotspots}
```

#### 10. Test Coverage Agent
```
Analyze test coverage for spellbook components.

Check:
- Which MCP tools have tests?
- Which don't?
- Are there integration tests for skill workflows?
- Test quality (do tests actually verify behavior?)

Output: JSON array of {component, type, has_tests, test_quality: "good"|"weak"|"none", gaps}
```

#### 11. Token Counting Agent
```
Measure actual token costs across all spellbook content.

For each file, calculate:
- Total tokens (words * 1.3 as estimate, or use tiktoken if available)
- Tokens by section
- Comparison to similar skills (is this one bloated?)

Produce rankings:
- Largest skills by token count
- Largest commands by token count
- Total tokens in CLAUDE.spellbook.md
- Total tokens in all skill descriptions (always-loaded cost)

Output: JSON with {
  total_tokens: N,
  always_loaded_tokens: N,  // descriptions only
  deferred_tokens: N,       // skill bodies
  by_file: [{file, total, sections: [{name, tokens}]}],
  rankings: {largest_skills: [], largest_commands: []}
}
```

#### 12. Conditional Extraction Agent
```
Find large conditional blocks that should become skills.

Scan for patterns in:
- CLAUDE.spellbook.md
- AGENTS.spellbook.md
- commands/*.md
- Any non-skill instruction file

Look for:
- "If X, then [20+ lines of instructions]"
- "When Y happens: [large block]"
- "For Z situations: [detailed workflow]"
- Platform-specific sections (macOS/Linux/Windows)
- Language-specific sections (Python/TypeScript/etc.)

A block should become a skill if:
- It's 15+ lines
- It's conditionally triggered
- It could stand alone as a coherent workflow

Output: JSON array of {
  file,
  line_start,
  line_end,
  trigger_condition,
  block_tokens,
  proposed_skill_name,
  extraction_difficulty: "easy"|"medium"|"hard"
}
```

#### 13. Tables-Over-Prose Agent
```
Identify prose sections that would be more token-efficient as tables.

Look for:
- Lists of "X does Y" statements
- Repeated structural patterns in prose
- Option/flag documentation
- Comparison content
- Any enumeration that follows a pattern

Calculate savings:
- Current prose token count
- Estimated table token count
- Percentage savings

Output: JSON array of {
  file,
  section,
  current_format: "prose"|"list",
  current_tokens,
  proposed_tokens,
  savings_pct,
  example_conversion
}
```

#### 14. Glossary Opportunity Agent
```
Find repeated term definitions that could use a shared glossary.

Look for:
- Same concept explained multiple times across files
- Inline definitions ("X, which means Y")
- Repeated explanations of spellbook-specific terms
- Acronym expansions repeated

Good glossary candidates:
- Terms used in 3+ files
- Definitions that are 10+ words
- Spellbook-specific jargon

Output: JSON array of {
  term,
  occurrences: [{file, line, definition_text}],
  proposed_canonical_definition,
  token_savings_estimate
}
```

#### 15. Naming Consistency Agent
```
Audit all skill, command, and agent names for semantic consistency.

NAMING CONVENTIONS:
| Type | Pattern | Examples |
|------|---------|----------|
| Commands | Imperative verb(-noun) | execute-plan, verify, write-plan |
| Skills | Gerund (-ing) OR Noun-phrase | debugging, test-driven-development, brainstorming |
| Agents | Noun-agent (role) | code-reviewer, fact-checker |

RATIONALE:
- Commands tell the system to DO something (imperative mood)
- Skills describe WHAT you're doing/learning (descriptive)
- Agents ARE something (role/identity)

For each skill:
- Flag if name is imperative verb pattern (should be gerund/noun)
- Examples: skills should use gerunds like "debugging", "fixing-tests", "implementing-features"

For each command:
- Flag if name is noun-phrase without action verb (should be imperative)
- Examples: commands should use imperatives like "handoff", "audit-green-mirage"

For each agent:
- Flag if name is not noun-agent pattern

Output: JSON array of {
  name,
  type: "skill"|"command"|"agent",
  current_pattern: "imperative"|"gerund"|"noun-phrase"|"noun-agent"|"ambiguous",
  expected_pattern,
  is_compliant: boolean,
  suggested_rename,
  severity: "high"|"medium"|"low"
}
```

#### 16. Reference Validation Agent
```
Validate that all skill/command references in documentation actually exist.

Scan all files for references to skills and commands:
- Backtick references: `skill-name`, `command-name`
- Prose references: "use the X skill", "invoke X command"
- Table references: skill/command names in Helper tables

For each reference found:
1. Check if it's a skill reference - verify skills/{name}/SKILL.md exists
2. Check if it's a command reference - verify commands/{name}.md exists
3. Check for type mismatches (referencing command as skill or vice versa)

KNOWN PATTERNS TO CHECK:
- Helper Skills tables (audit-spellbook has one)
- Cross-references in skill bodies
- CLAUDE.spellbook.md skill listings
- README.md feature lists

Output: JSON array of {
  file,
  line,
  reference,
  reference_type: "skill"|"command"|"ambiguous",
  exists: boolean,
  actual_type: "skill"|"command"|"none",
  type_mismatch: boolean,
  suggestion
}
```

#### 17. Orphaned Docs Agent
```
Find documentation files without corresponding source files.

Check for orphaned docs:
- docs/skills/*.md without matching skills/*/SKILL.md
- docs/commands/*.md without matching commands/*.md

Check for missing docs:
- skills/*/SKILL.md without matching docs/skills/*.md
- commands/*.md without matching docs/commands/*.md

Note: skills/commands/agents docs are generated by pre-commit hooks.
Focus on:
1. Orphans: docs that reference deleted/renamed items
2. Missing docs: items that should have docs/ entries

Output: JSON array of {
  file,
  issue: "orphaned"|"missing_docs",
  expected_source,
  recommendation: "delete"|"create"|"rename"
}
```

### Phase 2: Compile Report

After all agents complete, compile results into a unified report:

```markdown
# Spellbook Audit Report
Generated: [timestamp]

## Executive Summary
- Total token savings opportunity: X tokens (~Y%)
- Critical issues: N
- Optimization opportunities: M
- MCP candidates: K

## Factcheck Results
[summary + critical issues]

## Instruction Engineering Compliance
[summary + worst offenders]

## Description Optimization
[table of proposed changes with savings]

## Instruction Optimization
[grouped by file, sorted by savings potential]

## MCP Candidates
[prioritized list with implementation notes]

## YAGNI Analysis
[recommendations sorted by confidence]

## Persona Quality
[if applicable]

## Consistency Issues
[grouped by type]

## Dependency Analysis
[graph summary, orphans, hotspots]

## Test Coverage
[gaps and recommendations]

## Token Analysis
[total costs, rankings, always-loaded vs deferred breakdown]

## Conditional Extraction Candidates
[blocks that should become skills, sorted by token savings]

## Tables-Over-Prose Opportunities
[sections to convert, with example conversions]

## Glossary Candidates
[terms to define once, with occurrence counts]

## Naming Consistency
[skills/commands/agents with non-compliant names]

## Reference Validation
[broken or mistyped skill/command references]

## Orphaned Documentation
[docs without corresponding source files]

## Actionable Items
1. [High priority items]
2. [Medium priority items]
3. [Low priority items]
```

Save report to: `~/.local/spellbook/docs/<project-encoded>/audits/spellbook-audit-[timestamp].md`

### Phase 3: Implementation Prompt

After presenting the report summary, ask the user:

```
The audit identified [N] actionable items with potential savings of ~[X] tokens.

How would you like to proceed?
1. Implement high-priority items now
2. Implement all items
3. Review report first, decide later
4. Skip implementation
```

Use AskUserQuestion tool with these options.

If user chooses implementation:
1. Use `writing-plans` skill to create implementation plan
2. Ask any clarifying questions upfront using AskUserQuestion
3. Execute plan using appropriate skills/subagents

## Helper Skills and Commands

When implementing fixes, these can be invoked:

| Name | Type | Use For |
|------|------|---------|
| `writing-skills` | skill | **AUTHORITATIVE** guide for skill structure, CSO, and description writing |
| `instruction-engineering` | skill | Restructuring poorly-organized instructions |
| `optimizing-instructions` | skill | Compressing verbose instructions |
| `writing-plans` | skill | Creating implementation plans |
| `fact-checking` | skill | Deep-diving on specific claims |
| `finding-dead-code` | skill | Identifying unused code in MCP tools |
| `auditing-green-mirage` | skill | Auditing test quality |
| `/simplify` | command | Simplifying overcomplicated workflows |

## Naming Convention Reference

| Type | Pattern | Examples |
|------|---------|----------|
| Commands | Imperative verb(-noun) | execute-plan, verify, handoff |
| Skills | Gerund/Noun-phrase | debugging, test-driven-development |
| Agents | Noun-agent (role) | code-reviewer, fact-checker |

## Notes

- All subagents run in PARALLEL for speed
- Each agent should be thorough but focused on its specific concern
- Token estimates can be approximate (count words * 1.3)
- When in doubt, flag for human review rather than making assumptions
- The report should be actionable, not just diagnostic
- Run this audit before major releases
- Consider running monthly for maintenance

## Critical: Claude Search Optimization (CSO)

When auditing or fixing descriptions, follow CSO principles from the `writing-skills` skill:

**The Workflow Leak Bug:** If a description summarizes workflow (steps, phases, process), Claude
may follow the description instead of reading the full skill content. This is a documented bug
that caused real failures (e.g., "code review between tasks" in description caused ONE review
instead of the TWO specified in the actual skill).

**Description Formula:**
```
"Use when [triggering conditions/symptoms/situations]"
```

**NOT:**
```
"Use when X - does Y then Z then W"  # Workflow leak!
```

**Verification:** After fixing descriptions, test that Claude actually reads the full skill
content rather than just following the description.
