---
name: document-review
description: Review documentation for accuracy against implementation and compliance with documentation standards. Use when auditing docs, verifying ground truth, or ensuring documentation quality.
---

# Document Review Skill

## Purpose

Systematically verify documentation accuracy by comparing documented claims against actual implementation code, checking compliance with documentation principles, and providing confidence ratings with specific findings.

## When to Use This Skill

- User requests documentation review or audit
- Verifying documentation accuracy after code changes
- Quality assurance before releasing documentation
- Identifying documentation drift from implementation
- Ensuring compliance with DOCUMENTATION_PRINCIPLES.md

## Instructions

### Phase 1: Discovery & Inventory

1. **Identify the documentation scope**:
   - Which document type? (admin guides, developer docs, architecture, API reference, runbooks)
   - Specific documents or entire section?
   - Target directory (e.g., `docs/admin-guide/`, `docs/developer-guide/`)

2. **Locate applicable standards** (Two-Layer Hierarchy):

   **Layer 1: Universal Principles** (applies to ALL documentation)
   - Read `.claude/skills/DOCUMENTATION_PRINCIPLES.md` for hard rules that override everything

   **Layer 2: Type-Specific Guidance** (applies to this document type only)
   - Admin guides: Read `.claude/skills/document-admin-guide/SKILL.md` + template
   - Developer guides: Read `.claude/skills/document-feature/SKILL.md` + templates
   - Architecture docs: Read `.claude/skills/document-architecture/SKILL.md` + template
   - Runbooks: Read `.claude/skills/document-runbook/SKILL.md` + template

   **Important**: Layer 1 (DOCUMENTATION_PRINCIPLES.md) overrides Layer 2 when conflicts exist.

3. **Inventory all documents** to be reviewed

### Phase 2: Systematic Verification (One Document at a Time)

For **each document**, perform a thorough evaluation in this specific order:

#### 2.1 Read Documentation Thoroughly

- Read the entire document claim-by-claim
- Extract every factual claim about features, UI elements, fields, workflows
- Identify the **feature or system** being documented
- Note all structural elements (sections, formatting, metadata)

#### 2.2 Deep-Dive the Feature Implementation (BUILD GROUND TRUTH FIRST)

**CRITICAL: Understand the feature completely BEFORE comparing to docs.**

For the feature being documented, build a comprehensive understanding:

1. **Locate all implementation files**:
   - Frontend components (UI, forms, tables, modals)
   - API routes (endpoints, request/response shapes)
   - Services (business logic, data processing)
   - Database schema (tables, columns, relationships)
   - Types/interfaces (data structures)

2. **Understand the technical flow**:
   - User interaction → Component → API → Database
   - What happens on button clicks?
   - What data gets sent/received?
   - What fields are displayed?
   - What validations exist?
   - What error states are handled?

3. **Understand the architecture**:
   - How components are organized
   - How data flows through the system
   - What dependencies exist
   - What third-party libraries are used

4. **Extract the complete feature specification**:
   - All available fields (with exact names from code)
   - All UI elements (buttons, labels, tooltips)
   - All workflows (step-by-step user paths)
   - All data structures (interfaces, API shapes)
   - All constraints (validation rules, limits)

**Use Explore or Plan agents** for complex features that span multiple files or have unclear architecture.

**Result**: You now have the **authoritative ground truth** - what actually exists in code.

#### 2.3 Compare Documentation Against Ground Truth

NOW compare the documentation claims against your deep understanding:

For each claim in the documentation:

- **Does this feature exist?** ✅ or ❌
- **Does it work as described?** ✅ or ❌
- **Are field names correct?** ✅ or ❌ (check against actual TypeScript interfaces)
- **Are UI labels accurate?** ✅ or ❌ (check against actual JSX/HTML)
- **Are workflows complete?** ✅ or ❌ (check against actual component logic)
- **Are data structures correct?** ✅ or ❌ (check against actual API routes)
- **Are limitations documented?** ✅ or ❌ (check against actual validation code)

**Critical**: You already know the implementation deeply from step 2.2, so this comparison is precise and confident.

#### 2.4 Check Principle Compliance (Layer 1: Universal)

Review against DOCUMENTATION_PRINCIPLES.md:

- [ ] **Ground Truth Only** - No speculation or future plans
- [ ] **No Estimated Metrics** - No "~2 seconds", "~500KB" without measurement
- [ ] **No Troubleshooting** - Belongs in runbooks, not feature docs
- [ ] **No Meta-Commentary** - No "Note:", "Future work:", audience labels
- [ ] **Real Code Examples** - If present, are they from actual files with paths?
- [ ] **Appropriate Diagrams** - Used for clarity, not decoration

#### 2.5 Check Type-Specific Compliance (Layer 2)

Review against the applicable template:

- [ ] Required sections present (e.g., "What This Does", "Before You Start")
- [ ] Correct section names (not "Overview" when template says "What This Does")
- [ ] Metadata present (time estimate, last updated date, etc.)
- [ ] Structure matches template (numbered steps, action verbs, etc.)

#### 2.6 Check Template Compliance

Review against the applicable template:

- [ ] Required sections present (e.g., "What This Does", "Before You Start")
- [ ] Correct section names (not "Overview" when template says "What This Does")
- [ ] Metadata present (time estimate, last updated date, etc.)
- [ ] Structure matches template (numbered steps, action verbs, etc.)

#### 2.7 Check Language & Tone

For document type (admin guides have different rules than developer docs):

- [ ] Appropriate technical level for audience
- [ ] Jargon explained or avoided
- [ ] Clear, concise sentences
- [ ] Consistent terminology

#### 2.8 Generate Confidence Rating

Assign a confidence rating based on accuracy:

- **95-100%** (A+/A): Virtually perfect, 0-1 minor issues
- **90-94%** (A-): Highly accurate, minor template issues only
- **85-89%** (B): Good accuracy, some principle violations
- **75-84%** (C): Mostly accurate, 1-2 factual errors or multiple violations
- **Below 75%** (D/F): Significant inaccuracies, not trustworthy

### Phase 3: Consolidate & Report

After reviewing all documents:

1. **Aggregate findings** across all documents
2. **Categorize violations**:
   - **Critical Errors**: Factual inaccuracies (features that don't exist, wrong field names, etc.)
   - **Principle Violations**: Estimated metrics, troubleshooting sections, meta-commentary
   - **Template Non-Compliance**: Missing sections, wrong structure, missing metadata
   - **Language Issues**: Jargon, developer-speak in user docs, unclear wording

3. **Prioritize fixes**:
   - **Priority 1**: Critical factual errors (breaks user trust)
   - **Priority 2**: Hard principle violations (violates DOCUMENTATION_PRINCIPLES.md)
   - **Priority 3**: Template compliance (consistency and professionalism)
   - **Priority 4**: Source standard updates (prevent future violations)

4. **Present findings** with:
   - Confidence rating for each document (95%, 87%, etc.)
   - Overall summary table showing all docs and ratings
   - Specific line numbers for each violation
   - Before/After examples for critical errors
   - Impact assessment (HIGH/MEDIUM/LOW)
   - Recommended fixes

### Phase 4: Execute Fixes (If User Approves)

**IMPORTANT**: Track and report accuracy as you work.

After each fix or group of fixes:

1. **Update the affected document(s)**
2. **Recalculate confidence rating** for that document
3. **Report progress** to user:
   ```
   ✅ Fixed Cross-Reference error in managing-parts.mdx
   Confidence: 75% → 95% (C+ → A)
   ```

After all fixes complete: 4. **Present final summary**:

- Before/After confidence ratings for all documents
- Total violations fixed (by category)
- Files modified count
- Lines changed count

## Smart Interaction

### ASK the User When:

- Starting review (confirm scope and document type)
- Ambiguous findings (unclear if something is an error)
- Before executing fixes (get approval for changes)

### PROCEED Autonomously When:

- Reading files to verify implementation
- Comparing documentation claims against code
- Generating confidence ratings
- Categorizing violations

## Output Format

### Initial Evaluation Report

Present findings in this format:

```markdown
## Documentation Review: [Document Type]

### Summary

- Total documents reviewed: X
- Average confidence: XX%
- Critical errors found: X
- Principle violations: X

### Individual Ratings

| Document | Rating | Grade | Critical Errors | Issues  |
| -------- | ------ | ----- | --------------- | ------- |
| doc1.md  | 98%    | A+    | 0               | 1 minor |
| doc2.md  | 75%    | C+    | 1               | 5 total |

### Critical Errors (Priority 1)

**Error #1: [Description]**

- **Location**: [file.md:line-number]
- **Claim**: "Feature X has field Y"
- **Reality**: Field Y does not exist (verified in [implementation-file.tsx])
- **Impact**: HIGH - Users will look for non-existent field
- **Fix**: Remove references to field Y

### Principle Violations (Priority 2)

[Similar format]

### Template Non-Compliance (Priority 3)

[Similar format]
```

### Progress Updates (During Fixes)

After each fix:

```markdown
✅ [Task completed]
Confidence: [old%] → [new%] ([old-grade] → [new-grade])
```

### Final Summary (After All Fixes)

```markdown
## ✅ ALL FIXES COMPLETED

### Final Results

- Documents modified: X
- Lines changed: X
- Violations fixed: X

### Accuracy Improvement

| Document | Before   | After     | Improvement |
| -------- | -------- | --------- | ----------- |
| doc1.md  | 75% (C+) | 95% (A)   | +20%        |
| doc2.md  | 92% (A-) | 100% (A+) | +8%         |

**Overall**: XX% average → XX% average (+XX%)
```

## Documentation Type Profiles

### Admin Guides

- **Principles**: DOCUMENTATION_PRINCIPLES.md
- **Skill**: document-admin-guide/SKILL.md
- **Template**: admin-how-to.md
- **Focus**: User-friendly language, no jargon, step-by-step clarity
- **Common issues**: Technical terms, troubleshooting sections, missing metadata

### Developer Guides

- **Principles**: DOCUMENTATION_PRINCIPLES.md
- **Skill**: document-feature/SKILL.md
- **Templates**: tutorial.md, how-to.md, reference.md
- **Focus**: Code accuracy, real examples with file paths, no speculation
- **Common issues**: Hypothetical code, estimated metrics, outdated examples

### Architecture Docs

- **Principles**: DOCUMENTATION_PRINCIPLES.md
- **Skill**: document-architecture/SKILL.md
- **Template**: arc42.md
- **Focus**: Accurate diagrams, real constraints, actual decisions made
- **Common issues**: Future plans, speculative designs, outdated diagrams

### Runbooks

- **Principles**: DOCUMENTATION_PRINCIPLES.md
- **Skill**: document-runbook/SKILL.md
- **Template**: runbook.md
- **Focus**: Executable commands, tested procedures, rollback plans
- **Common issues**: Untested commands, missing failure scenarios, no verification

## Quality Standards

### Excellent Review (What Success Looks Like)

- ✅ Every claim verified against actual code
- ✅ Line numbers cited for all violations
- ✅ Confidence ratings based on objective criteria
- ✅ Specific before/after examples for errors
- ✅ Prioritized remediation plan
- ✅ Progress tracking during fixes

### Poor Review (What to Avoid)

- ❌ Skimming docs without verifying implementation
- ❌ Vague "docs seem accurate" without specifics
- ❌ Missing line numbers for violations
- ❌ No confidence ratings
- ❌批量 fixes without tracking progress

## Examples

### Example Invocations

- "Review my admin guides" → Reviews all files in `docs/admin-guide/`
- "Verify the API documentation accuracy" → Reviews `docs/architecture/API_DESIGN.md` against actual API
- "Check if architecture docs match current system" → Reviews `docs/architecture/`
- "Audit developer guides for ground truth compliance" → Reviews `docs/developer-guide/`

### Example Output

See the admin guide review (2026-01-08) as reference implementation:

- Initial evaluation: 15 violations across 5 documents
- Confidence ratings: 75-98%
- Systematic fixes with progress tracking
- Final result: 100% accuracy, 0 violations

## Critical Success Factors

1. **Understand Implementation BEFORE Comparing to Docs**
   - Deep-dive the feature first to build ground truth
   - Understand technical flow, architecture, and complete specification
   - Use Explore/Plan agents for complex features
   - THEN compare documentation claims against your deep understanding
   - This prevents missing subtle inaccuracies

2. **One Document at a Time**
   - Deep focus prevents missing details
   - Complete evaluation before moving to next doc
   - Generate individual confidence rating

3. **Specific, Not Vague**
   - Cite exact line numbers
   - Quote the problematic text
   - Show the conflicting implementation code
   - Provide before/after examples

4. **Track Progress Visibly**
   - Report after each fix or fix group
   - Show confidence improvement
   - Keep user informed throughout

5. **Prioritize Impact**
   - Critical errors first (break user trust)
   - Principle violations second (standards compliance)
   - Template compliance third (consistency)
   - Nice-to-haves last

## Remember

- **Understand the feature deeply FIRST** - Build complete ground truth before comparing to docs
- **Ground truth is in the code** - Documentation should match reality, not aspirations
- **Two-layer documentation standards**:
  - Layer 1: DOCUMENTATION_PRINCIPLES.md (universal, overrides everything)
  - Layer 2: document-[type]/SKILL.md (type-specific guidance)
- **Confidence ratings must be earned** - Based on verified accuracy, not optimism
- **Progress visibility matters** - Users want to see improvement as you work
