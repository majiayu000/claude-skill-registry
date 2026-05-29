---
name: update-architecture
description: Update architecture markdown files. Use when user says "update architecture", "update arch docs", "sync architecture", or mentions updating architecture documentation.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '📚 [SKILL: update-architecture] Analyzing code changes and updating architecture documentation...'"
          once: true
---

# Architecture Documentation Update Skill

## When to Use

Use this skill when:
- User says "update architecture docs", "sync architecture docs", "update arch docs", "refresh architecture"
- When architecture documentation is out of sync with implementation

## Target Selection (Required)

**Update ONE location at a time** - updating all locations simultaneously creates too much context. Identify which location to update based on user request.

**If user doesn't specify**, ask which component or area of the codebase to update using AskUserQuestion.

## Critical Constraints

### NEVER

- Read existing architecture docs BEFORE understanding the codebase (prevents context pollution)
- Catalog components without understanding their PURPOSE
- Document data flows without understanding WHY they exist that way
- List patterns without understanding what PROBLEM they solve
- Patch sections - rebuild from understanding instead
- Trust old documentation over understood principles
- Create diagrams that don't reflect understood architecture
- Document WHAT without explaining WHY
- Assume a WRITE operation implies a corresponding READ (verify both independently)
- Document data flows without tracing actual RETRIEVAL code

### ALWAYS

- **Focus on ONE target location at a time** - ask user if not specified
- **Understand before documenting** - answer the 6 key questions (Purpose, Constraints, Design Rationale, Collaboration, Invariants, Data Lifecycle)
- Build understanding from code FIRST, then compare with existing docs
- Write documentation that explains WHY, not just WHAT
- **Trace READS and WRITES separately** - verify each data flow has both ends in actual code
- **Establish authority by retrieval patterns** - what code QUERIES determines source of truth
- Validate through understanding - errors violate understood principles
- Use `/mermaid` skill for diagrams that reflect understood architecture
- Maintain the standard 8-file structure per location
- Preserve valid structural elements (navigation, formatting) from existing docs

## Standard 8-File Structure

Every architecture location contains these files:

| File | Purpose | Update When |
|------|---------|-------------|
| `README.md` | Navigation hub, quick reference | New files added, navigation changes |
| `overview.md` | System diagrams, design principles | Architectural changes, new components |
| `components.md` | Component details, dependencies | New classes, modules, or interfaces |
| `data-models.md` | State schemas, database models | New models, field changes, migrations |
| `workflows.md` | Execution flows, state machines | New phases, routing changes, state transitions |
| `patterns.md` | Design patterns, ID formats, conventions | New patterns, ID changes, naming conventions |
| `configuration.md` | CLI flags, env vars, settings | New config options, CLI changes |
| `directory-structure.md` | Code navigation, module layout | New directories, file reorganization |

## Workflow

### Core Principle: Understand, Don't Catalog

**CRITICAL**: The goal is to deeply UNDERSTAND the architecture - the WHY behind every design decision, not just WHAT exists. An agent that truly understands the architecture will never document incorrect patterns because they would violate the understood principles.

**Do NOT:**
- Read existing architecture docs before exploring code (prevents context pollution)
- Create checklists of things to look for (leads to shallow pattern matching)
- Document components without understanding their purpose
- Describe data flows without understanding why they exist that way
- Assume a WRITE implies a READ (verify each independently)
- Assume data in a location is used just because it exists there

**Instead:**
- Explore code to understand the PROBLEM being solved
- Understand the CONSTRAINTS and challenges the system faces
- Understand WHY each design decision was made
- Understand HOW components collaborate to achieve the goal
- Understand the INVARIANTS that must always hold true
- Trace READS and WRITES separately for every data flow
- Verify authority by finding RETRIEVAL code, not just storage code

### Step 1: Git Diff Analysis (Single Location)

Launch **1 subagent** to analyze code changes for the **selected target location** since the last architecture update:

```
Subagent 1 (Git Diff):
  - Find last commit: git log -1 --format="%H" -- {architecture_docs_path}/
  - Diff since then: git diff <commit>..HEAD -- {target_code_path}/
  - Report: new files, modified files, deleted files, summary of changes
```

### Step 2: Deep Architecture Understanding (Single Location)

Launch **parallel Explore subagents** to build TRUE UNDERSTANDING of the target module. These subagents must **NOT read any architecture/*.md files** - only source code.

**Each exploration subagent must answer these questions:**

```
1. PURPOSE: What problem does this module/component solve?
   - What would break if this didn't exist?
   - What user need or system requirement does it address?

2. CONSTRAINTS: What challenges does this module face?
   - What are the reliability requirements?
   - What are the consistency requirements?
   - What failure modes must be handled?

3. DESIGN RATIONALE: Why was it built THIS way?
   - What alternatives were rejected and why?
   - What trade-offs were made?
   - What principles guide the design?

4. COLLABORATION: How do components work together?
   - What is the flow of data/control?
   - What are the boundaries between components?
   - What contracts exist between components?

5. INVARIANTS: What must ALWAYS be true?
   - What assumptions can never be violated?
   - What guarantees does this module provide?
   - What guarantees does it depend on from others?

6. DATA LIFECYCLE: What is the complete lifecycle of each data entity?
   - Where is this data CREATED?
   - Where is this data WRITTEN/PERSISTED?
   - Where is this data READ/RETRIEVED? (trace actual retrieval code)
   - Is this data EVER read back, or only written?
   - If multiple storage locations exist, which does the code QUERY?
```

**Subagent exploration structure:**

```
Subagent 2: Understand the module's CORE PURPOSE
  - Read entry points, main classes, public interfaces
  - Answer: What is this module FOR? What problem does it solve?
  - Answer: What would happen if this module didn't exist?

Subagent 3: Understand the module's DATA ARCHITECTURE
  - Trace how data enters, transforms, persists, and exits
  - Answer: Where is the source of truth? Why?
  - Answer: What consistency guarantees are provided? How?
  - Answer: What would break if data flowed differently?

  CRITICAL - Trace READS and WRITES separately:
  - For each storage location (database, files, memory), trace:
    * What code WRITES to this location?
    * What code READS from this location?
  - Don't assume writes imply reads - verify each independently
  - Authority is determined by RETRIEVAL patterns, not storage patterns
  - Ask: "When component X needs this data, what does it query?"

Subagent 4: Understand the module's CONTROL FLOW
  - Trace execution paths, state transitions, decision points
  - Answer: What orchestrates the workflow? Why that approach?
  - Answer: How are failures handled? Why that strategy?
  - Answer: What are the critical paths?

Subagent 5: Understand the module's BOUNDARIES
  - Identify interfaces with other modules
  - Answer: What does this module depend on? What depends on it?
  - Answer: What contracts exist at boundaries?
  - Answer: How is coupling minimized?

Subagent 6: Understand the module's EXTENSION POINTS
  - Identify patterns for customization, configuration
  - Answer: How can behavior be modified without code changes?
  - Answer: What is intentionally flexible vs fixed?

Subagent 7: Trace DATA LIFECYCLE (Critical for correct data flow documentation)
  - For each storage location found (database tables, files, memory structures):
    * Search for all WRITE operations to this location
    * Search for all READ operations from this location
    * If writes exist but NO reads found -> this is write-only (not part of data flow)
    * If reads exist, trace: what component reads? when? why?
  - Establish AUTHORITY:
    * When a component needs data, what does it query FIRST?
    * If data exists in multiple places, which location is consulted?
    * The code that RETRIEVES data reveals the true source of truth
  - Document the complete lifecycle:
    * Creation -> Transformation -> Persistence -> Retrieval -> Usage
    * Note any gaps (e.g., "persisted but never retrieved")
```

Each subagent produces an **understanding document** that explains the WHY, not just the WHAT.

**CRITICAL: Data Flow Verification**

Before documenting any data flow (A -> B), the explorer MUST verify:
1. There is code that WRITES from A
2. There is code that READS into B
3. These operations are connected (B actually uses what A writes)

A write operation observed does NOT prove a read exists. Trace both independently.

### Step 3: Synthesize Understanding Into Documentation

Based on the deep understanding from Step 2, rebuild documentation that reflects TRUE understanding. Launch **parallel subagents** to write documentation from the understanding gained:

```
Each documentation rebuild subagent receives the UNDERSTANDING from Step 2
and writes documentation that explains:

Subagent N: Rebuild overview.md
  - Write from understanding of PURPOSE and DESIGN RATIONALE
  - Explain what the module does and WHY it exists
  - Create diagrams that show HOW components achieve the goal

Subagent N+1: Rebuild components.md
  - Write from understanding of COLLABORATION and BOUNDARIES
  - Explain each component's ROLE in achieving the purpose
  - Describe WHY each component exists, not just what it does

Subagent N+2: Rebuild data-models.md
  - Write from understanding of DATA ARCHITECTURE and INVARIANTS
  - Explain WHY data flows the way it does
  - Document the source of truth and WHY it's the source of truth
  - Explain what guarantees are provided and HOW

Subagent N+3: Rebuild workflows.md
  - Write from understanding of CONTROL FLOW and CONSTRAINTS
  - Explain WHY the workflow is structured this way
  - Document failure handling and WHY that strategy was chosen

Subagent N+4: Rebuild patterns.md
  - Write from understanding of DESIGN RATIONALE
  - Explain each pattern's PURPOSE - what problem it solves
  - Document WHY this pattern was chosen over alternatives

Subagent N+5: Rebuild configuration.md
  - Write from understanding of EXTENSION POINTS
  - Explain what each config controls and WHY it's configurable

Subagent N+6: Rebuild directory-structure.md
  - Write from understanding of BOUNDARIES and COLLABORATION
  - Explain WHY the code is organized this way
```

**Key principle: Every statement in the rebuilt docs should be traceable to understood purpose or constraint.**

### Step 4: Dry Walkthrough Validation

Launch **validation subagents** to perform a dry walkthrough of the rebuilt documentation - tracing every documented relationship back to actual code:

**4a. Diagram Walkthrough**

For each diagram in the rebuilt documentation:

```
Subagent V1: Walkthrough each connection in diagrams

  For each arrow/connection (A -> B) in a diagram:
  1. LOCATE: Find the actual code where A connects to B
  2. CHARACTERIZE: What does this connection actually do?
  3. VALIDATE: Does the diagram accurately represent reality?
  4. REPORT: Document findings
```

**4b. Data Flow Walkthrough (CRITICAL)**

For each data flow described in documentation:

```
Subagent V2: Verify data flows by tracing READS and WRITES separately

  For each documented flow (Source -> Destination):

  1. VERIFY THE WRITE:
     - Find code that writes from Source
     - What function/method performs the write?

  2. VERIFY THE READ:
     - Find code that reads into Destination
     - Does this read ACTUALLY use what was written in step 1?

  3. CHECK FOR PHANTOM FLOWS:
     - If you find a WRITE but NO corresponding READ -> flow doesn't exist
     - A write operation alone does NOT prove data flows to another component

  4. ESTABLISH AUTHORITY:
     - If data exists in multiple locations, which does the code QUERY?
     - The retrieval path reveals the true source of truth
```

**4c. Compare With Existing Docs**

```
Subagent V3: Compare validated rebuild against existing docs

  After walkthrough validation, compare:
  - Connections in old doc that don't exist in code -> STALE
  - Connections in old doc with wrong direction/label -> INCORRECT
  - Connections missing from old doc but found in walkthrough -> MISSING
  - Produce report explaining each discrepancy with code evidence
```

### Step 5: Apply Rebuilt Content

For each affected file in the target location:

1. **Use rebuilt content as the source of truth** - not the old doc
2. **Preserve valid structural elements** - navigation links, formatting conventions
3. **Replace stale sections entirely** - don't try to patch incorrect content
4. **Use `/mermaid` skill** for any diagram creation or updates
5. **Update cross-references** - ensure links to other docs remain valid
6. **Report discrepancies found** - log what was incorrect in old docs

### Step 6: Final Validation

Launch **parallel final validation subagents** to ensure consistency within target location:

- Validate cross-references between the 8 files
- Validate diagrams match rebuilt content
- Validate content consistency across files
- Spot-check rebuilt content against actual code one final time

## Related Skills

### Mermaid Skill (`/mermaid`)

When architecture documentation requires new or updated Mermaid diagrams, invoke the `/mermaid` skill. This ensures diagrams are properly formatted and validated.

## Output

This skill modifies architecture files for the **selected target location**. Changes and discrepancies are reported to terminal:

```
=== Architecture Documentation Update Report ===

Target: {target_location}

Understanding Phase:
- PURPOSE: {what problem the module solves}
- INVARIANTS: {what must always be true}
- KEY INSIGHTS: {important design rationale discovered}

Walkthrough Validation:
- {N} diagram connections traced
- {X} valid, {Y} issues found
- Each issue includes: code evidence, why it's wrong, action taken

Discrepancies Found:
- {file}: {what was wrong} -> {what code actually shows}

Updated Files:
- {list of files modified with action taken}

Final Verification: {pass/fail with details}
```

### Why Understanding Over Cataloging?

**Cataloging (what we avoid):**
- Lists components without explaining why they exist
- Looks for specific keywords without understanding why they matter
- Compares diagram shapes without understanding what they represent

**Understanding (what we do):**
- "Why does this module exist? What problem does it solve?"
- "What would break if this component didn't exist?"
- "What constraints make this design necessary?"
- "What invariants must always hold true?"

An agent that truly understands the architecture will naturally produce correct documentation because incorrect statements would violate understood principles. The understanding itself prevents errors.

### Why Rebuild Instead of Patch?

Patching existing documentation risks:
- **Context pollution**: Reading stale docs first biases toward preserving incorrect info
- **Shallow updates**: Patches fix surface issues while deeper misunderstandings persist
- **Missing the why**: Patches change WHAT without updating WHY

Rebuilding from understanding ensures:
- **Principled documentation**: Every statement follows from understood purpose/constraints
- **Self-correcting**: Errors are caught because they violate understood invariants
- **Future-proof**: Documentation reflects WHY, so it guides future changes correctly
