# design-to-spec

---
description: Transform human design documents into AI-optimized spec.md files
tags: [project-init, design, spec, planning, transformation]
techStack: [all]
appliesTo: ["projects/*/design.md", "projects/*/design.docx", "transform spec", "design to spec"]
alwaysApply: false
---

## Prerequisites

### Claude Code Extended Context Configuration

**IMPORTANT**: Before running this skill, ensure Claude Code is configured with extended context settings:

```bash
MAX_THINKING_TOKENS=50000
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
```

**Why Extended Context is Required**:
- This skill ingests verbose design documents (often 2000-5000 words)
- Performs **preliminary** resource discovery (ADR constraints for spec enrichment)
- Generates structured spec.md with technical context
- Chains into `project-pipeline` which performs comprehensive resource discovery

**Verify settings before proceeding**:
```bash
# Windows PowerShell
echo $env:MAX_THINKING_TOKENS
echo $env:CLAUDE_CODE_MAX_OUTPUT_TOKENS

# Should output: 50000 and 64000
```

If not set, see root [CLAUDE.md](../../../CLAUDE.md#development-environment) for setup instructions.

### Permission Mode: Plan Mode (RECOMMENDED)

**This skill analyzes design documents. Use Plan Mode for safe exploration.**

```
⏸ PLAN MODE RECOMMENDED

Before starting this skill:
  1. Press Shift+Tab twice to enter Plan Mode
  2. Look for indicator: "⏸ plan mode on"
  3. Plan Mode ensures read-only operations during analysis

WHY: This skill reads and analyzes design documents, discovers ADR constraints,
     and extracts requirements. Plan Mode prevents accidental edits.

OUTPUT: When analysis is complete, Claude will generate spec.md.
        Switch to Auto-Accept Mode (Shift+Tab) when ready to write the file.
```

---

## Purpose

**Tier 1 Component Skill** - Transforms verbose human design documents into structured, AI-optimized `spec.md` files that the `project-pipeline` skill can consume.

**Key Features**:
- Ingests various design document formats (markdown, Word, PDF, rough notes)
- Extracts and structures requirements, scope, and acceptance criteria
- Enriches with ADR references, file paths, and technical constraints
- Flags ambiguities for human resolution
- Outputs standardized spec.md for project-pipeline consumption

**Why This Skill Exists**:
- Human design docs are narrative-heavy, missing AI-needed context
- AI agents need: explicit constraints, file paths, ADR references, scope boundaries
- Manual spec.md creation is error-prone and time-consuming

## When to Use

- User says "transform spec", "design to spec", or "create AI spec"
- Explicitly invoked with `/design-to-spec {project-path}`
- A design document exists at `projects/{project-name}/design.md` (or `.docx`, `.pdf`)
- Before running `project-pipeline` (this skill feeds into that workflow)

## Input/Output

**Input** (one of):
- `projects/{project-name}/design.md` - Markdown design doc
- `projects/{project-name}/design.docx` - Word document
- `projects/{project-name}/design.pdf` - PDF document
- User-provided text/notes (via conversation)

**Output**:
- `projects/{project-name}/spec.md` - AI-optimized spec file
- Both files kept as project artifacts

## Workflow Position

```
Human Design Document
    │
    ▼
┌──────────────────┐
│  design-to-spec  │  ← THIS SKILL
│  (Tier 1)        │
└──────────────────┘
    │
    ▼
projects/{name}/spec.md (AI-optimized)
    │
    ▼
┌──────────────────┐
│ project-pipeline │  ← NEXT SKILL
│ (Tier 2)         │
└──────────────────┘
    │
    ▼
README.md, PLAN.md, tasks/, etc.
```

---

## Steps

### Step 1: Locate Design Document

**Action:**
```
SEARCH for design document at:
  1. projects/{project-name}/design.md
  2. projects/{project-name}/design.docx
  3. projects/{project-name}/design.pdf
  4. projects/{project-name}/*.md (if only one non-spec markdown)

IF not found:
  → ASK user: "Where is your design document?"
  → Accept: file path, pasted text, or description

IF found:
  → READ document content
  → Report: "Found design document: {filename} ({word-count} words)"
```

---

### Step 2: Extract Core Elements

**Action:**
```
EXTRACT from design document:

1. PURPOSE
   - What problem does this solve?
   - What is the business value?
   - Who are the users/stakeholders?

2. SCOPE
   - What's IN scope (explicit features/changes)
   - What's OUT of scope (explicit exclusions)
   - System boundaries

3. REQUIREMENTS
   - Functional requirements (what it must do)
   - Non-functional requirements (performance, security, etc.)
   - Technical constraints

4. SUCCESS CRITERIA
   - How do we know it's done?
   - Acceptance criteria
   - Quality gates

5. TECHNICAL APPROACH (if present)
   - Architecture decisions
   - Technology choices
   - Integration points

FLAG any missing elements for human input
```

**Output to User:**
```
📋 Extracted from design document:

✅ Found:
   - Purpose: [summary]
   - Scope: {X} features in scope
   - Requirements: {Y} functional, {Z} non-functional
   - Success criteria: {N} criteria identified

⚠️ Gaps identified - proceeding to targeted clarification...
```

---

### Step 2.5: Gap-Targeted Clarification Interview

**Purpose:** Ask **specific, actionable questions** derived from gaps discovered in THIS design document. Each question must directly impact implementation decisions.

**Principle:** Questions are NOT generic checklists. They are intelligent probes based on:
- Undefined terms found in the design
- Implicit assumptions that need validation
- Missing behavior specifications
- Conflicting or ambiguous requirements
- Scope boundaries that are unclear

**Action:**
```
ANALYZE extracted content for specific gaps:

FOR EACH gap discovered, generate a TARGETED question that:
  ✅ References the EXACT text or concept that's unclear
  ✅ Explains WHY the answer matters (implementation impact)
  ✅ Offers concrete options where applicable
  ✅ Can be answered in 1-2 sentences

GAP TYPES → QUESTION PATTERNS:

1. UNDEFINED TERMS
   Gap: Design uses "{term}" without defining it
   Question: "You mention '{term}' - what's the specific threshold/value?
             This determines [implementation choice]."

   Example:
   - Gap: Design says "handle large files"
   - Question: "What file size is 'large'? >10MB? >100MB?
               This determines if we need chunked uploads or streaming."

2. IMPLICIT ASSUMPTIONS
   Gap: Design assumes {behavior} without stating it
   Question: "The design seems to assume {assumption}. Is this correct?
             If not, [alternative approach] would be needed."

   Example:
   - Gap: Design assumes users are authenticated
   - Question: "Should anonymous users see the document list (read-only)?
               Currently assuming authenticated-only access."

3. UNSPECIFIED BEHAVIOR
   Gap: Design mentions {feature} but not how it works
   Question: "When {specific scenario}, what should happen?
             Options: [A] {option} or [B] {option}"

   Example:
   - Gap: "Export to PDF" mentioned but no details
   - Question: "When exporting to PDF, should it include comments/annotations?
               This affects the export library choice."

4. MISSING ERROR HANDLING
   Gap: Happy path only for {feature}
   Question: "What should happen when {specific failure scenario}?
             Options: [A] Show error, [B] Retry, [C] Fallback to {alternative}"

   Example:
   - Gap: Document upload flow, no failure handling
   - Question: "If upload fails mid-stream (network error), should we:
               [A] Auto-retry 3x, [B] Save partial and resume, [C] Fail and delete?"

5. CONFLICTING REQUIREMENTS
   Gap: {Requirement A} conflicts with {Requirement B}
   Question: "'{Requirement A}' and '{Requirement B}' seem to conflict.
             Which takes priority? This affects [implementation]."

   Example:
   - Gap: "Real-time sync" vs "Offline support"
   - Question: "Real-time sync conflicts with offline-first. Priority?
               This determines the sync architecture."

6. SCOPE BOUNDARY UNCLEAR
   Gap: Unclear if {capability} is in/out of scope
   Question: "Is {specific capability} in scope for this release?
             The design mentions it but doesn't explicitly include it."

   Example:
   - Gap: Design mentions "mobile users" but scope is unclear
   - Question: "Is mobile-responsive UI in scope, or desktop-only?
               This affects component library choices."

7. MISSING QUANTITATIVE REQUIREMENTS
   Gap: No numbers for {performance/scale requirement}
   Question: "What's the expected {metric}? (e.g., concurrent users, data volume)
             This determines [architectural choice]."

   Example:
   - Gap: No concurrent user expectations
   - Question: "Expected concurrent users? <100 (simple), <1000 (caching needed),
               >1000 (requires scaling strategy)?"

PRESENT questions grouped by impact:

🔴 BLOCKING (must answer before spec):
   {Questions where wrong assumption = wrong implementation}

🟡 IMPORTANT (should answer, can proceed with noted assumptions):
   {Questions that affect approach but have reasonable defaults}

FORMAT each question:
  📍 Context: "{exact quote or reference from design}"
  ❓ Question: "{specific question}"
  💡 Impact: "{why this matters for implementation}"
  🔘 Options: [A] {option} [B] {option} (if applicable)
```

**Output to User:**
```
🎯 Targeted Clarification Questions

Based on gaps in the design document, I need your input on these specific items:

🔴 BLOCKING (need answers to proceed):

1. 📍 Context: "The design mentions 'batch processing for large document sets'"
   ❓ Question: What defines a 'large' set? 10 docs? 100? 1000?
   💡 Impact: Determines if we need background job queuing or can process inline.
   🔘 Options: [A] <50 inline [B] <500 queue [C] >500 chunked batches

2. 📍 Context: "Users can share documents with external parties"
   ❓ Question: External = any email, or only pre-approved domains?
   💡 Impact: Affects auth flow and security review requirements.

🟡 IMPORTANT (proceeding with assumptions if not answered):

3. 📍 Context: "Support for common document formats"
   ❓ Question: Which formats exactly? PDF, DOCX, XLSX, PPTX? Images?
   💡 Impact: Determines preview/conversion libraries needed.
   ⚠️ Assuming: PDF, DOCX, XLSX, PPTX only

Please answer the BLOCKING questions. For IMPORTANT, reply with answers or 'ok' to accept assumptions.
```

**Wait for User**: Answers to blocking questions (required), optional answers to important questions

**Incorporate Answers:**
```
FOR EACH answer received:
  → Update extracted requirements with concrete values
  → Note source: "Per owner clarification: {answer}"
  → Remove from gaps list
  → Add to spec.md requirements section

IF user skips IMPORTANT questions:
  → Proceed with stated assumptions
  → Flag assumptions in spec.md "Questions/Clarifications" section
```

---

### Step 3: Preliminary Technical Context Discovery

**Purpose:** Enrich spec.md with **architectural constraints only** (not detailed implementation patterns).

**Action:**
```
IDENTIFY resource types from extracted content:

1. RESOURCE TYPES → ADR CONSTRAINTS
   - API endpoints → Reference ADR-001, ADR-008, ADR-010, ADR-019 (constraints only)
   - PCF controls → Reference ADR-006, ADR-011, ADR-012, ADR-021 (constraints only)
   - Plugins → Reference ADR-002 (constraints only)
   - Storage → Reference ADR-005, ADR-007, ADR-009 (constraints only)
   - AI features → Reference ADR-013, ADR-014, ADR-015, ADR-016 (constraints only)
   - Background jobs → Reference ADR-004, ADR-017 (constraints only)

2. EXTRACT KEY CONSTRAINTS
   - Read applicable ADRs for MUST/MUST NOT rules
   - Identify architectural boundaries
   - Note technology choices

OUTPUT: List of applicable ADRs and key constraints for spec.md

⚠️ **SCOPE LIMITATION**:
This is PRELIMINARY discovery for spec.md enrichment only.
- ✅ DO: Identify which ADRs apply
- ✅ DO: Extract key constraints (MUST/MUST NOT)
- ❌ DON'T: Search codebase for implementation patterns
- ❌ DON'T: Load detailed knowledge docs or guides
- ❌ DON'T: Find existing code examples

Comprehensive resource discovery happens in project-pipeline Step 2.
```

---

### Step 4: Generate Structured spec.md

**Action:**
```
CREATE: projects/{project-name}/spec.md

FOLLOW template structure:

# {Project Name} - AI Implementation Specification

> **Status**: Ready for Implementation
> **Created**: {date}
> **Source**: {design-document-filename}

## Executive Summary

{2-3 sentences from extracted PURPOSE}

## Scope

### In Scope
{Bulleted list of features/changes}

### Out of Scope
{Explicit exclusions - ASK if not in design doc}

### Affected Areas
{List of code areas, with file paths where known}
- `src/server/api/...` - {description}
- `src/client/pcf/...` - {description}

## Requirements

### Functional Requirements
{Numbered list with clear acceptance criteria}
1. **FR-01**: {requirement} - Acceptance: {criteria}
2. **FR-02**: {requirement} - Acceptance: {criteria}

### Non-Functional Requirements
{Performance, security, accessibility, etc.}
- **NFR-01**: {requirement}

## Technical Constraints

### Applicable ADRs
{List ADRs that MUST be followed}
- **ADR-001**: Minimal API pattern required
- **ADR-008**: Use endpoint filters for authorization

### MUST Rules (from ADRs)
{Extracted key constraints}
- ✅ MUST use...
- ✅ MUST NOT...

### Existing Patterns to Follow
{Reference to canonical implementations}
- See `src/server/api/.../ExampleEndpoints.cs` for endpoint pattern
- See `.claude/patterns/api/` for detailed patterns

## Success Criteria

{Numbered list with verification method}
1. [ ] {criterion} - Verify by: {method}
2. [ ] {criterion} - Verify by: {method}

## Dependencies

### Prerequisites
{What must exist/be done first}

### External Dependencies
{APIs, services, approvals needed}

## Owner Clarifications

{Answers captured from Step 2.5 interview - CRITICAL for implementation}

| Topic | Question | Answer | Impact |
|-------|----------|--------|--------|
| {topic} | {question asked} | {owner's response} | {implementation decision made} |

## Assumptions

{Items where owner did not specify - proceeding with stated assumptions}

- **{topic}**: Assuming {value/behavior} - affects {component/decision}

## Unresolved Questions

{Still blocking or need answers during implementation}
- [ ] {question} - Blocks: {what this blocks}

---

*AI-optimized specification. Original design: {filename}*
```

---

### Step 5: Present for Review

**Action:**
```
OUTPUT spec.md content to user

SHOW summary:
  - Word count
  - Number of requirements
  - Number of ADRs referenced
  - Number of unresolved questions

ASK for review:
  "Please review the spec.md. Any changes needed before proceeding to project-pipeline?"
```

**Output to User:**
```
✅ spec.md generated:
   - {X} words
   - {Y} functional requirements
   - {Z} ADRs referenced
   - {N} unresolved questions flagged

📄 File created: projects/{project-name}/spec.md

📋 Next Steps:
   1. Review spec.md for accuracy
   2. Resolve any flagged questions
   3. Run: /project-pipeline {project-name}

[Y to proceed to project-pipeline / edit to make changes / done to finish]
```

**Wait for User**: `y` (proceed to pipeline) | `edit` (make changes) | `done` (stop here)

---

## Next Steps After This Skill

### ✅ CORRECT: Proceed to Full Pipeline

After spec.md is reviewed and approved:

```bash
/project-pipeline projects/{project-name}
```

This performs:
- ✅ **Comprehensive resource discovery** (ADRs, skills, knowledge docs, code patterns)
- ✅ Artifact generation (README, PLAN, CLAUDE.md)
- ✅ Task decomposition (50-200+ task files)
- ✅ Feature branch creation
- ✅ Ready to execute task 001

### ❌ INCORRECT: Call Component Skills Directly

**DO NOT** run these after design-to-spec:
```bash
# ❌ WRONG - Missing resource discovery and tasks
/project-setup projects/{project-name}

# ❌ WRONG - Can't create tasks without plan.md
/task-create projects/{project-name}
```

**Why?** Component skills are called BY project-pipeline, not by developers.

---

### Step 6: Handoff to project-pipeline (Optional)

**Action:**
```
IF user said 'y':
  → INVOKE project-pipeline projects/{project-name}
  → Handoff message: "Starting project-pipeline with generated spec.md..."

IF user said 'done':
  → OUTPUT: "spec.md ready at projects/{project-name}/spec.md
             Run /project-pipeline {project-name} when ready."
```

---

## spec.md Template

The generated spec.md follows this structure (also saved at `docs/ai-knowledge/templates/spec.template.md`):

```markdown
# {Project Name} - AI Implementation Specification

> **Status**: Ready for Implementation
> **Created**: {YYYY-MM-DD}
> **Source**: {original-design-document}

## Executive Summary

{Brief description of what this project delivers and why}

## Scope

### In Scope
- {Feature/change 1}
- {Feature/change 2}

### Out of Scope
- {Explicit exclusion 1}
- {Explicit exclusion 2}

### Affected Areas
- `{path}` - {description}

## Requirements

### Functional Requirements
1. **FR-01**: {Requirement} - Acceptance: {Criteria}

### Non-Functional Requirements
- **NFR-01**: {Requirement}

## Technical Constraints

### Applicable ADRs
- **ADR-XXX**: {Brief relevance}

### MUST Rules
- ✅ MUST {constraint}
- ❌ MUST NOT {constraint}

### Existing Patterns
- See `{path}` for {pattern}

## Success Criteria
1. [ ] {Criterion} - Verify: {method}

## Dependencies

### Prerequisites
- {Prerequisite}

### External
- {External dependency}

## Owner Clarifications

*Answers captured during design-to-spec interview:*

| Topic | Question | Answer | Impact |
|-------|----------|--------|--------|
| {topic} | {question asked} | {owner's answer} | {how this affects implementation} |

## Assumptions

*Proceeding with these assumptions (owner did not specify):*

- **{topic}**: Assuming {value/behavior} - will affect {component}

## Unresolved Questions

*Still need answers before implementation:*

- [ ] {Unresolved question} - Blocks: {what this blocks}

---
*AI-optimized specification. Original: {filename}*
```

---

## Error Handling

**If design document not found:**
```
❌ No design document found at projects/{project-name}/

Looking for: design.md, design.docx, design.pdf

Options:
1. Provide file path: "the design is at {path}"
2. Paste content: "here's the design: ..."
3. Create interactively: "help me write the design"
```

**If design doc too vague:**
```
⚠️ Design document lacks sufficient detail for AI implementation.

Missing critical elements:
- [ ] Concrete requirements (what specifically to build)
- [ ] Success criteria (how to verify completion)
- [ ] Scope boundaries (what's NOT included)

Options:
1. 'clarify' - Answer questions to fill gaps
2. 'proceed' - Generate spec.md with assumptions noted
3. 'stop' - Exit and improve design document
```

---

## Integration with Other Skills

This skill feeds into the project lifecycle:

```
design-to-spec (THIS SKILL)
    │
    └─→ Generates spec.md
           │
           ▼
    project-pipeline
           │
           ├─→ project-setup (README, PLAN, CLAUDE.md)
           └─→ task-create (task files)
```

**Skills this skill may invoke:**
- `adr-aware` (implicit) - For ADR discovery during context gathering

**Skills that depend on this skill's output:**
- `project-pipeline` - Consumes spec.md
- `project-setup` - Consumes spec.md (if called directly)

---

## Success Criteria

Skill successful when:
- [ ] Design document ingested and parsed
- [ ] Core elements extracted (purpose, scope, requirements, criteria)
- [ ] **Gap-targeted interview conducted** (specific questions asked for discovered gaps)
- [ ] **Owner clarifications captured** (answers recorded in spec.md)
- [ ] **Assumptions documented** (for unanswered questions)
- [ ] Technical context discovered (ADRs, patterns, file paths)
- [ ] spec.md generated with all required sections
- [ ] Unresolved questions clearly flagged with blocking impact
- [ ] User reviewed and approved spec.md
- [ ] Original design document preserved alongside spec.md

---

*For Claude Code: This skill transforms human design documents into structured specs optimized for AI-driven implementation. Always preserve the original design document as a project artifact.*
