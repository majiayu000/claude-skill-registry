---
name: review-spec
description: This skill should be used when the user wants to review a technical specification document, especially multi-file specs with appendices. It checks for consistency, completeness, clarity, and identifies opportunities for simplification and removal of unnecessary complexity.
---

# Review Spec

## Overview

This skill provides a comprehensive review methodology for technical specifications, particularly those with main documents and multiple appendices. It emphasizes finding opportunities to simplify and remove over-engineered features, while also checking for consistency, completeness, and clarity.

## When to Use This Skill

Use this skill when:
- User asks to "review the spec" or "review my specification"
- User has a complex spec with multiple files or appendices
- User wants feedback on spec organization or scope
- User asks about simplifications or what to remove
- User wants to identify over-engineered features
- User is planning an MVP and needs scope reduction advice

## Review Process

**Efficiency tip**: Read multiple files in parallel when possible to speed up the review.

Follow this workflow in order for comprehensive spec review:

### Step 1: Read the Complete Spec

Read all files systematically:
1. Main specification document (usually SPEC.md or README.md)
2. All appendices in order (A, B, C, etc.)
3. Any supporting documents (guiding principles, setup docs)

While reading, note:
- Overall scope and complexity
- Phase/milestone structure
- Dependencies between sections
- Repeated concepts or information

### Step 2: Assess Scope and Complexity

**Critical for MVP planning:**

1. **Identify the core value proposition**
   - What is the one essential thing this project must do?
   - What's the 80% use case?

2. **Categorize features by necessity**
   - **Must have (Phase 1)**: Core functionality without which the project is useless
   - **Should have (Phase 2)**: Important but can be added after MVP
   - **Nice to have (Phase 3+)**: Optional enhancements
   - **Over-engineered**: Sophisticated features that may never be needed

3. **Calculate implementation time**
   - Estimate weeks/months for current scope
   - Compare to typical MVP timelines (4-8 weeks)
   - Flag if scope seems too large

4. **Look for separate products disguised as features**
   - Example: A "helper" class that's as complex as the main system
   - Example: "Self-improving" systems that require ML/learning infrastructure
   - Example: "Advanced" features that double the implementation time

**Red flags for over-scoping:**
- Multiple "phases" extending beyond Phase 2-3
- Features marked "Phase 4" or "Phase 5"
- Entire appendices dedicated to optional features
- "Bootstrap → Learning → Optimization" evolution paths
- Features that require their own testing strategy
- "Future Extensions" sections longer than core spec

### Step 3: Check for Consistency

Review consistency across all documents:

**Terminology consistency:**
- Are concepts named consistently? (e.g., "config" vs "configuration")
- Are technical terms used correctly throughout?
- Are abbreviations defined before use?

**Design decision consistency:**
- Do appendices follow design principles stated in main spec?
- Are similar problems solved in similar ways?
- Are there conflicting approaches to the same problem?

**Status consistency:**
- Do status markers (✅, 🚧, ❌) mean the same thing everywhere?
- Are phase assignments consistent? (Something can't be both Phase 1 and Phase 3)
- Are TODOs tracked correctly?

**Data format consistency:**
- Are examples consistent with specifications?
- Do code samples match the described API?
- Are file formats consistent across examples?

### Step 4: Check for Completeness

Verify all references and requirements are complete:

**Cross-references:**
- Do all "See Appendix X" links point to existing sections?
- Are all referenced files present?
- Do internal links work correctly?

**TODOs and incomplete sections:**
- Are there any TODO markers or 🚧 sections?
- Are placeholders filled in?
- Are all promised sections actually written?

**Missing critical sections:**
- Error handling strategy
- Installation/setup instructions
- Real-world usage examples
- Version compatibility information
- Testing strategy (if complex project)

**Appendices index:**
- Is there an index of appendices?
- Are all appendices listed?
- Are statuses accurate (✅ Complete vs 🚧 TODO)?

### Step 5: Assess Clarity and Usability

Evaluate whether the spec is clear and usable:

**Structure and organization:**
- Is the table of contents helpful?
- Are sections logically ordered?
- Is nesting depth appropriate (not too deep)?
- Are related concepts grouped together?

**Examples and illustrations:**
- Are there enough code examples?
- Do examples demonstrate actual use cases, not just API calls?
- Are examples realistic (not toy examples)?
- Are there before/after examples for modifications?

**Complexity and readability:**
- Is the language appropriate for the audience?
- Are complex concepts explained well?
- Is there too much jargon?
- Are sentences and paragraphs reasonably short?

**Actionability:**
- Can implementers start coding from this spec?
- Are APIs specified with enough detail (parameters, return values, errors)?
- Are edge cases documented?
- Are validation rules clear?

### Step 6: Identify Simplifications

**This is critical - actively look for ways to simplify:**

**Over-specified features:**
- Features with >500 lines of specification may be over-designed
- Multiple "phases" of a single feature suggest complexity
- "Advanced" or "Enhanced" versions of features can often wait

**Premature optimization:**
- "Self-improving" or "learning" systems before MVP
- Complex heuristics and algorithms before proving core value
- Performance optimizations before performance problems exist
- Extensibility mechanisms before knowing what needs extending

**Gold plating:**
- Multiple strategies/modes for the same operation
- Extensive configuration options
- Plug-in architectures before second plugin needed
- Abstraction layers for single implementation

**Feature creep:**
- Features that serve edge cases (< 10% of users)
- "It would be nice if..." features
- Features that duplicate existing tools
- Features that solve hypothetical future problems

**Simplification opportunities by pattern:**
1. **Multiple convenience methods/wrappers**: Start with 3-5 essential ones, add more based on usage
2. **Phased feature rollouts**: Just basic version for MVP, add enhanced versions later
3. **Multiple initialization/loading paths**: Start with 1-2 primary paths, add more if users request
4. **Helper/utility classes**: Defer sophisticated helpers until core is proven
5. **Configuration options**: Start with one good default, add options later
6. **Export/output formats**: Support one format well, add others based on demand

### Step 7: Identify Removals

**Be aggressive - what can be completely removed or deferred?**

**Defer to Phase 3+ or remove entirely:**
- Entire appendices about optional features
- "Helper" systems that are separate products
- Advanced optimization features
- Batch/automation utilities (users can write scripts)
- Integration with external systems (unless core value)
- Extensive logging/profiling/monitoring
- Plugin architectures
- Configuration migration tools

**Remove from specification (even if implementing later):**
- "Future Extensions" sections that are speculative
- "Phase 4" and "Phase 5" content
- Features marked "optional" or "nice to have"
- Alternatives and rejected approaches (move to ADR document)
- Implementation notes that belong in code comments

**Ask these questions:**
- Can users achieve this with existing features or simple workarounds?
- Is this solving a real problem or a hypothetical one?
- Would 90% of users be satisfied without this?
- Can this be added in a 1-week sprint after MVP ships?
- Is this duplicating what another tool does well?
- Does this feature require more code than the rest of the system combined?

### Step 8: Check Technical Correctness

Validate the technical design:

**API design:**
- Are method signatures sensible?
- Are return types appropriate?
- Is error handling well-defined?
- Are side effects documented?

**Data structures:**
- Are data formats appropriate for the use case?
- Are there serialization/deserialization concerns?
- Are size limits considered?
- Is backward compatibility addressed?

**Algorithms and logic:**
- Are algorithms correctly described?
- Are edge cases handled?
- Are there performance concerns?
- Are there correctness concerns?

**Dependencies and compatibility:**
- Are dependencies clearly listed?
- Are version requirements specified?
- Are there potential conflicts?
- Is platform compatibility addressed?

### Step 9: Generate Review Report

Provide a structured review report with these sections:

**1. Executive Summary**
- Overall assessment (good/needs work/over-scoped)
- Key metrics: estimated implementation time, number of features, scope
- Top 3 recommendations

**2. Scope Analysis**
- Current scope estimate (weeks/months)
- Core value proposition identified
- Recommended Phase 1 scope
- Features to defer or remove

**3. Critical Issues** (if any)
- Missing required sections
- Technical correctness problems
- Inconsistencies
- Blocking issues

**4. Simplification Opportunities** (prioritized)
- Specific features to simplify
- Appendices to trim or remove
- Methods/classes to defer
- Estimated time savings

**5. Organization Improvements**
- Structural changes recommended
- Missing sections to add
- Redundant sections to merge

**6. Detailed Findings**
- Consistency issues found
- Completeness gaps
- Clarity problems
- Technical issues

**7. Specific Recommendations**
- For each major issue, provide:
  - Current state
  - Problem description
  - Recommended change
  - Rationale
  - Estimated impact (time saved, complexity reduced)

## Common Anti-Patterns to Flag

Watch for these over-engineering patterns:
- **The Kitchen Sink**: Trying to solve every possible problem with multiple modes/strategies
- **The Future-Proof Fortress**: Extensive abstractions for hypothetical future needs
- **The Nested Doll**: Features containing features, >3 phase levels for single capabilities
- **The Self-Improving Mirage**: ML/learning systems, complex heuristics as "nice to have"
- **The Premature Enterprise**: Logging, monitoring, profiling, A/B testing in MVP

## Example Review Output

```markdown
# Spec Review: [Project Name]

## Executive Summary
**Status**: Over-scoped for MVP (estimated 3-6 months → recommend 4-8 weeks)
**Core Value**: [One sentence describing essential functionality]
**Key Issue**: [Major blocking issue or over-engineering concern]

**Top 3 Recommendations:**
1. [Specific recommendation] - [estimated time savings]
2. [Specific recommendation] - [estimated time savings]
3. [Specific recommendation] - [estimated time savings]

## Scope Analysis
Current: ~[N] lines spec, [X] months implementation
Recommended Phase 1: ~[N] lines spec, [X] weeks implementation

**Core value**: [Essential functionality that must work]
**Defer to Phase 3+**: [Complex features to build after MVP]

[Continue with detailed sections...]
```

### Step 10: Engage User with Guided Questions

**After presenting the review report, ask questions to help the user learn and make informed design decisions.**

Ask questions one at a time around these themes:
- **Core value**: What's the one essential thing? What's the 80% use case?
- **Scope reality**: Timeline constraints? What to cut by 50%? Risk tolerance?
- **User context**: Their environment? Current workflow pain points? Existing tool patterns?
- **Technical constraints**: Why this complexity? What are simpler alternatives?
- **Trade-offs**: What do you lose/gain by simplifying? Acceptable workarounds?
- **Decision-making**: What resonates most? Smallest change, biggest impact?
- **Next steps**: Revised Phase 1 scope? What moves to Phase 2?

Select 4-8 most relevant questions based on major issues found. Ask specific questions referencing actual features from their spec.

## Notes

- **Be constructive**: Always explain WHY something should change
- **Be specific**: Identify exact sections, line numbers, features
- **Be practical**: Consider implementation time and complexity
- **Be user-focused**: What delivers value to users fastest?
- **Be honest**: If scope is too large, say so clearly
- **Be Socratic**: Use questions to help users discover insights themselves
- **Be patient**: Give users time to think and respond to questions
- **Be adaptive**: Adjust questions based on their answers and needs

The goal is to help create specifications that lead to successful, timely implementations that deliver real value to users - and to help users learn to think critically about scope and design decisions themselves.
