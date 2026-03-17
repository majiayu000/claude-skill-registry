---
name: create-adr-spike
description: |
  Creates Architecture Decision Records (ADRs) and conducts research spikes for technical decisions
  using a structured 5-phase workflow: Research, Analysis, Decision, Documentation, and Memory Storage.

  Use when asked to "create an ADR", "architectural decision for", "research spike on", "evaluate
  options for", "document technical decision", "should we use X or Y", or when comparing technical
  alternatives.

  Provides systematic evaluation (minimum 2-3 alternatives), trade-off analysis, consequence
  documentation, and memory graph persistence. Manages ADR lifecycle across not_started, in_progress,
  and implemented directories with proper numbering and status tracking.

  Works with docs/adr/ directories, ADR templates, memory MCP tools, and external research tools
  (WebSearch, WebFetch, context7 library docs).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - mcp__memory__search_memories
  - mcp__memory__find_memories_by_name
  - mcp__memory__create_entities
  - mcp__memory__create_relations
  - mcp__memory__add_observations
  - mcp__context7__resolve-library-id
  - mcp__context7__get-library-docs
  - Write
---

# Create ADR Spike

Standardized workflow for creating Architecture Decision Records (ADRs) and conducting research spikes for technical decisions.

## When to Use This Skill

**Explicit Triggers:**
- "Create an ADR for [decision]"
- "Architecture decision for [problem]"
- "Research spike on [topic]"
- "Evaluate options for [choice]"
- "Document technical decision about [subject]"
- "Should we use X or Y?"

**Implicit Triggers:**
- Comparing multiple technical alternatives
- Making architectural choices that affect system design
- Evaluating libraries, frameworks, or patterns
- Deciding on refactoring approaches
- Documenting important technical trade-offs

**Debugging/Analysis Triggers:**
- "What decisions led to this architecture?"
- "Why did we choose [technology/pattern]?"
- "Search existing ADRs for [topic]"

**When NOT to Use:**
- Simple code refactoring (no architectural impact)
- Bug fixes without design implications
- Minor configuration changes
- Routine maintenance tasks

## Table of Contents

### Core Sections
- [Quick Start](#quick-start) - What this skill does and when to use it
- [Workflow](#workflow) - Complete 5-phase ADR creation process
  - [Phase 1: Research (Discovery)](#phase-1-research-discovery) - Gather context and search existing knowledge
  - [Phase 2: Analysis (Evaluation)](#phase-2-analysis-evaluation) - Evaluate alternatives systematically
  - [Phase 3: Decision (Recommendation)](#phase-3-decision-recommendation) - Make clear, justified recommendation
  - [Phase 4: Documentation (Formalization)](#phase-4-documentation-formalization) - Create permanent ADR record
  - [Phase 5: Memory Storage (Persistence)](#phase-5-memory-storage-persistence) - Store decision in memory graph
- [Quality Checklist](#quality-checklist) - Verification before marking spike complete
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid) - Common mistakes and correct approaches

### Project Integration
- [Project-Specific Conventions](#project-specific-conventions) - ADR directory structure and naming
- [Examples](#examples) - Complete walkthroughs and use cases
- [Output Format](#output-format) - How to present completed ADR spike results
- [Success Criteria](#success-criteria) - When an ADR spike is complete

### Supporting Resources
- [reference.md](references/reference.md) - Technical documentation, ADR template deep-dive, and comprehensive examples
- [Scripts](scripts/) - Utility scripts for ADR number finding and validation
- [Templates](templates/) - ADR and migration templates for structured decision records

### Additional Information
- [Requirements](#requirements) - Skills, tools, project setup, and knowledge needed
- [Troubleshooting](#troubleshooting) - Common issues and solutions
- [References](#references) - Related documentation and guides

## Templates

This skill includes comprehensive ADR and migration templates:

- **[templates/adr-template.md](templates/adr-template.md)** - Complete ADR structure with:
  - Status and metadata frontmatter
  - Context, decision, and consequences sections
  - Implementation strategy and validation plan
  - Migration path with before/after examples
  - Alternatives considered and trade-off analysis
  - Related decisions and references

- **[templates/migration-template.md](templates/migration-template.md)** - Detailed migration/refactor plan with:
  - Current state and desired state analysis
  - Phased migration path with detailed steps
  - Risk analysis and mitigation strategies
  - Comprehensive rollback procedures
  - Testing strategy and monitoring plan
  - Communication and training plans

**Usage:** Reference these templates when creating ADRs from spikes or planning complex migrations/refactors.

## Quick Start

**Invoke this skill when you need to:**
- Document an architectural decision
- Research technical alternatives
- Evaluate competing solutions
- Create a formal decision record

**Example invocation:**
```
"Create an ADR for choosing between PostgreSQL and Neo4j for our graph storage"
```

## Workflow

### Phase 1: Research (Discovery)

**Objective:** Gather all relevant context before making a recommendation.

1. **Identify the Decision:**
   - What problem are we solving?
   - What constraints exist (performance, cost, expertise)?
   - What are the success criteria?

2. **Search Existing Knowledge:**
   ```bash
   # Search existing ADRs for related decisions
   find docs/adr -name "*.md" -type f -exec grep -l "keyword" {} \;

   # Search project memory for patterns
   mcp__memory__search_memories(query="related topic")
   ```

3. **Research External Resources (if needed):**
   - Use `mcp__context7__resolve-library-id` to find library documentation
   - Use `mcp__context7__get-library-docs` to get detailed technical info
   - Use `WebSearch` for recent discussions, benchmarks, or comparisons
   - Use `WebFetch` to extract specific documentation pages

4. **Document Findings:**
   - Create ADR directory and start drafting `ADR.md`:
     ```
     docs/adr/not_started/{number}-{kebab-case-title}/
     └── ADR.md   # Draft: add research findings to "Context" and "Research" sections
     ```
   - **DO NOT** create separate RESEARCH.md, ANALYSIS.md, or EXECUTIVE_SUMMARY.md files
   - **DO NOT** put research in `.claude/artifacts/`
   - All research goes directly into ADR.md sections

### Phase 2: Analysis (Evaluation)

**Objective:** Evaluate alternatives systematically.

1. **Identify Options (minimum 2-3):**
   - List all viable alternatives
   - Include "do nothing" if applicable
   - Consider hybrid approaches

2. **Evaluate Each Option:**
   For each alternative, document:
   - **Pros:** Benefits and strengths
   - **Cons:** Drawbacks and weaknesses
   - **Performance:** Speed, scalability, resource usage
   - **Maintainability:** Code complexity, debugging, testability
   - **Cost:** Development time, operational cost, learning curve
   - **Team Fit:** Expertise required, training needed
   - **Risks:** What could go wrong?
   - **Trade-offs:** What are we giving up?

3. **Create Comparison Matrix:**
   | Criteria | Option A | Option B | Option C |
   |----------|----------|----------|----------|
   | Performance | High | Medium | Low |
   | Maintainability | Medium | High | Low |
   | Cost | Low | High | Medium |
   | Team Fit | High | Medium | Low |

### Phase 3: Decision (Recommendation)

**Objective:** Make a clear, justified recommendation.

1. **Recommend Preferred Option:**
   - State choice clearly
   - Provide 2-3 sentence rationale
   - Reference evaluation criteria

2. **Document Justification:**
   - Why this option over others?
   - What criteria weighted most heavily?
   - What assumptions are we making?
   - What constraints influenced the decision?

3. **Identify Consequences:**
   - **Positive:** What improves?
   - **Negative:** What gets harder?
   - **Risks:** What could fail?
   - **Mitigations:** How to reduce risks?

### Phase 4: Documentation (Formalization)

**Objective:** Create permanent ADR record.

1. **Determine ADR Number:**
   ```bash
   # Find highest existing ADR number across all status directories
   find docs/adr -name "[0-9]*.md" | \
     sed 's/.*\/\([0-9]*\)-.*/\1/' | \
     sort -n | tail -1
   ```

2. **Choose ADR Directory:**
   - `docs/adr/not_started/` - Decision made, implementation not started
   - `docs/adr/in_progress/` - Implementation currently underway
   - `docs/adr/implemented/` - Fully implemented and verified

   **Default:** Use `not_started/` for new decisions unless implementation begins immediately.

3. **Create ADR from Template:**
   - Copy template: `templates/adr-template.md` or `templates/migration-template.md`
   - Fill all required sections (no placeholders)
   - Use next sequential number (e.g., ADR-028)
   - Use kebab-case for filename: `028-descriptive-title.md`

4. **Complete Required Sections:**
   - **Status:** Proposed | Accepted | In Progress | Completed
   - **Date:** Current date (YYYY-MM-DD)
   - **Context:** Problem statement, current state, motivation
   - **Decision:** Chosen approach, scope, pattern
   - **Consequences:** Positive, negative, migration strategy
   - **Alternatives Considered:** At least 2-3 options with pros/cons
   - **References:** Links to research, docs, discussions

5. **Add Implementation Tracking (if applicable):**
   - Files affected
   - Completion criteria
   - Testing strategy
   - Code marker guidelines

### Phase 5: Memory Storage (Persistence)

**Objective:** Store decision in memory graph for future retrieval.

1. **Create Memory Entity:**
   ```python
   mcp__memory__create_entities(entities=[{
       "name": f"ADR-{number}: {title}",
       "type": "ArchitectureDecision",
       "observations": [
           f"Status: {status}",
           f"Decision: {chosen_option}",
           f"Rationale: {key_reason}",
           f"Date: {date}",
           f"Location: docs/adr/{status_dir}/{number}-{kebab-case-title}/"
       ]
   }])
   ```

2. **Create Relations to Existing Entities:**
   - Link to affected components
   - Link to related ADRs (supersedes, relates-to)
   - Link to architectural patterns

3. **Verify Document Structure:**
   - **Maximum 2 files per ADR** - see "Document Structure Rule" section
   - For `not_started/`: Only ADR.md
   - For `in_progress/`: ADR.md + IMPLEMENTATION_PLAN.md
   - **NO separate** RESEARCH.md, ANALYSIS.md, EXECUTIVE_SUMMARY.md, or IMPLEMENTATION_NOTES.md
   - **NO documents in** `.claude/artifacts/`

## Quality Checklist

Before marking the spike complete, verify:

- [ ] **Minimum 2-3 alternatives** evaluated
- [ ] **Clear recommendation** with justification
- [ ] **Consequences documented** (positive AND negative)
- [ ] **ADR created** in correct directory with proper numbering
- [ ] **All required sections** completed (no placeholder text)
- [ ] **Memory entity created** with proper observations and relations
- [ ] **Max 2 files**: ADR.md only (not_started) or ADR.md + IMPLEMENTATION_PLAN.md (in_progress)
- [ ] **No extra files**: No RESEARCH.md, ANALYSIS.md, EXECUTIVE_SUMMARY.md, IMPLEMENTATION_NOTES.md
- [ ] **No single-option analysis** (red flag: only one option presented)
- [ ] **Trade-offs documented** (no "silver bullet" claims)
- [ ] **Risks identified** with mitigation strategies

## Document Structure Rule (CRITICAL)

**Minimal documents. No redundancy. Human-readable.**

### Document Count by Status

| Status | Documents | Contents |
|--------|-----------|----------|
| `not_started/` | **1 file**: ADR.md | Research + Analysis + Decision |
| `in_progress/` | **2 files**: ADR.md + IMPLEMENTATION_PLAN.md | Add implementation details |
| `implemented/` | **1-2 files** | Same as in_progress (plan becomes historical record) |

### ✅ CORRECT Structure

**For `not_started/` (decision made, not yet implementing):**
```
docs/adr/not_started/005-subprocess-daemon-architecture/
└── ADR.md    # Contains: Executive Summary, Research, Analysis, Decision, Alternatives
```

**For `in_progress/` (actively implementing):**
```
docs/adr/in_progress/005-subprocess-daemon-architecture/
├── ADR.md                  # The decision (research + analysis + decision)
└── IMPLEMENTATION_PLAN.md  # How to build it (phases + tasks + notes)
```

### ❌ WRONG Structure (Too Many Documents)
```
docs/adr/in_progress/005-.../
├── ADR.md
├── RESEARCH.md              # ❌ WRONG: Put in ADR.md
├── ANALYSIS.md              # ❌ WRONG: Put in ADR.md
├── EXECUTIVE_SUMMARY.md     # ❌ WRONG: Put in ADR.md
├── IMPLEMENTATION_PLAN.md
└── IMPLEMENTATION_NOTES.md  # ❌ WRONG: Put in IMPLEMENTATION_PLAN.md
```

### The Rule

- **ADR.md** = Research + Analysis + Executive Summary + Decision + Alternatives
- **IMPLEMENTATION_PLAN.md** = Phases + Tasks + Developer Notes (only when `in_progress/`)
- **That's it. 1-2 files maximum.**

## Anti-Patterns to Avoid

1. **Single Option Presented:**
   - ❌ BAD: "We should use PostgreSQL" (no alternatives)
   - ✅ GOOD: "PostgreSQL vs Neo4j vs Hybrid approach" (multiple options)

2. **Missing Trade-off Analysis:**
   - ❌ BAD: "Option A is better in every way"
   - ✅ GOOD: "Option A is faster but harder to maintain"

3. **No Consequence Documentation:**
   - ❌ BAD: Decision without discussing impact
   - ✅ GOOD: Positive/negative consequences documented

4. **Skipping Memory Storage:**
   - ❌ BAD: ADR created but not in memory graph
   - ✅ GOOD: ADR entity created with relations

5. **Placeholder Text in ADR:**
   - ❌ BAD: "[TODO: Add alternatives]"
   - ✅ GOOD: All sections fully completed

6. **Wrong Directory:**
   - ❌ BAD: Implementation ADR in `not_started/`
   - ✅ GOOD: ADR directory matches status

7. **No External Research:**
   - ❌ BAD: Decision based only on opinion
   - ✅ GOOD: Research references documentation, benchmarks, community discussion

8. **Ignoring Existing ADRs:**
   - ❌ BAD: Creating conflicting ADR without checking existing
   - ✅ GOOD: Search existing ADRs, note conflicts/supersessions

9. **Splitting Documents Across Locations:**
   - ❌ BAD: ADR in `docs/adr/`, research in `.claude/artifacts/`
   - ✅ GOOD: ALL documents in `docs/adr/{status_dir}/{number}-{kebab-case-title}/`

## Project-Specific Conventions

### ADR Directory Structure (This Project)
```
docs/adr/
├── implemented/    # Completed ADRs (11+ ADRs)
├── in_progress/    # Active implementation (4+ ADRs)
├── not_started/    # Proposed/accepted, not started (10+ ADRs)
├── TEMPLATE-refactor-migration.md
└── README.md
```

### Numbering Convention
- Use 3-digit format: `001`, `028`, `127`
- Find highest number across ALL status directories
- Use next sequential number
- **Do not reuse numbers**

### Filename Convention
- Format: `{number}-{kebab-case-title}.md`
- Example: `028-indexing-orchestrator-extraction.md`
- Keep titles concise (3-7 words)

### Status Values
- **Proposed:** Initial draft, seeking approval
- **Accepted:** Approved, awaiting implementation
- **In Progress:** Currently implementing
- **Completed:** Fully implemented and verified
- **Superseded:** Replaced by newer ADR

### Refactor Markers (for in-progress ADRs)
If ADR is in `in_progress/`, add file-level markers in affected code:
```python
# =============================================================================
# TODO: "Section Name"
# REFACTOR: [ADR-XXX] Brief description
# WHY: One-line reason
# STARTED: YYYY-MM-DD
# STATUS: IN_PROGRESS
# PERMANENT_RECORD: docs/adr/in_progress/XXX-title.md
# ACTIVE_TRACKING: todo.md "Section Name"
# =============================================================================
```

See: [Refactor Marker Guide](../quality-detect-refactor-markers/references/refactor-marker-guide.md)

### Integration with todo.md
For ADRs requiring implementation:
- Create section in `./todo.md` tracking tasks
- Reference in ADR's "Active Tracking" section
- Update ADR's "Progress Log" as work proceeds

## Examples

### Python Examples

- [validate_adr.py](./scripts/validate_adr.py) - Validate ADR completeness and format
- [find_next_adr_number.sh](./scripts/find_next_adr_number.sh) - Find next ADR number in sequence

### Complete Walkthroughs

See [references/reference.md](references/reference.md) for detailed examples of:
- Simple architectural decision (library choice)
- Complex refactor/migration ADR
- Research spike with external investigation
- Superseding an existing ADR

## Supporting Files

- **[references/reference.md](references/reference.md):** Detailed technical documentation, ADR template deep-dive, and comprehensive examples
- **[templates/adr-template.md](templates/adr-template.md):** Complete ADR structure with all required sections
- **[templates/migration-template.md](templates/migration-template.md):** Detailed migration/refactor planning template
- **[scripts/validate_adr.py](scripts/validate_adr.py):** Validation script for ADR completeness
- **[scripts/find_next_adr_number.sh](scripts/find_next_adr_number.sh):** Utility to find next ADR number

## Requirements

**Skills & Tools:**
- Skill tool access: Read, Grep, Glob, Bash, Write
- MCP tools: mcp__memory__, mcp__context7__ (for research)
- Web tools: WebSearch, WebFetch (for external research)

**Project Setup:**
- `docs/adr/` directory structure exists with status subdirectories (in projects using this skill)
- ADR templates available at `templates/adr-template.md` and `templates/migration-template.md`
- Memory system configured for entity storage

**Knowledge:**
- Understanding of Clean Architecture principles (for this project)
- Ability to evaluate technical trade-offs
- Familiarity with ADR format and structure

## Troubleshooting

**Issue: Can't find next ADR number**
```bash
# Solution: Use helper script
./scripts/find_next_adr_number.sh

# Or manually:
find docs/adr -name "[0-9]*.md" | sed 's/.*\/\([0-9]*\)-.*/\1/' | sort -n | tail -1
```

**Issue: Don't know which directory to use**
- **not_started/**: Decision made, no implementation yet (default)
- **in_progress/**: Currently implementing
- **implemented/**: Fully complete and verified

**Issue: Alternatives seem equivalent**
- Good! Document that in the ADR
- Explain why you chose one over the other (team fit, learning curve, etc.)
- Consider hybrid approaches

**Issue: Only one viable option**
- ❌ RED FLAG - dig deeper
- Minimum 2-3 alternatives required
- Include "do nothing" as an option if applicable
- Consider different implementation approaches of the same technology

**Issue: Research taking too long**
- Set time box (1-2 hours for simple decisions, 4-8 hours for complex)
- Focus on key decision criteria
- Note what you didn't research in ADR limitations section
- Can always update ADR later with more research

**Issue: Memory entity creation fails**
- Verify memory system is configured and running
- Check entity name doesn't already exist
- Simplify observations if too complex
- Skip memory storage if blocked, but note in ADR

## Success Criteria

An ADR spike is complete when:
1. ✅ Research conducted (existing ADRs, memory, external sources)
2. ✅ Alternatives evaluated (2-3+ options)
3. ✅ Recommendation made with justification
4. ✅ ADR created with all required sections
5. ✅ ADR placed in correct directory with proper numbering
6. ✅ Memory entity created with relations
7. ✅ Research artifacts saved and referenced
8. ✅ Quality checklist verified

## Output Format

When completing an ADR spike, provide:

1. **Executive Summary:**
   - Decision made
   - Key rationale (2-3 sentences)
   - Alternatives considered

2. **ADR Location:**
   - Full path to created ADR
   - ADR number and title

3. **Memory Entity:**
   - Entity name
   - Key observations stored

4. **Next Steps (if applicable):**
   - Implementation tasks
   - todo.md section created
   - Refactor markers needed

## References

- [Refactor Marker Guide](../quality-detect-refactor-markers/references/refactor-marker-guide.md)
- [ADR Template](templates/adr-template.md)
- [Migration Template](templates/migration-template.md)
- [Reference Documentation](references/reference.md) - Detailed examples and walkthroughs

---

**Skill Type:** Project Skill (team workflow)
**Audience:** @researcher, @planner, any agent making architectural decisions
**Last Updated:** 2025-10-17
