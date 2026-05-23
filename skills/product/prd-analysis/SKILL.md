---
description: PRD analysis knowledge including depth-aware criteria, finding categories, severity guidelines, and common issue patterns
triggers:
  - analyze PRD
  - review PRD
  - PRD quality check
  - validate requirements
  - audit PRD
  - PRD analysis
  - check PRD quality
  - PRD review
---

# PRD Analysis Skill

This skill provides structured knowledge for analyzing existing Product Requirements Documents to identify quality issues and guide resolution.

## Analysis Philosophy

### Depth-Aware Analysis

PRD analysis must respect the intended depth level of the document. A high-level PRD should not be flagged for missing API specifications, just as a full-tech PRD should be scrutinized for technical completeness.

**Key Principle**: Only flag what's expected at the document's depth level.

### Constructive Approach

Findings should be:
- **Actionable**: Clear recommendation for how to fix
- **Specific**: Exact location and description of issue
- **Prioritized**: Severity indicates importance
- **Helpful**: Explain why this matters, not just what's wrong

### Systematic Coverage

Analysis covers four distinct categories to ensure comprehensive review:
1. **Inconsistencies**: Internal contradictions or mismatches
2. **Missing Information**: Expected content that's absent
3. **Ambiguities**: Unclear or vague statements
4. **Structure Issues**: Formatting, organization, missing sections

---

## Finding Categories

### 1. Inconsistencies

Issues where the PRD contradicts itself or uses conflicting information.

**What to Look For**:
- Feature named differently in different sections
- Priority mismatches (feature marked P2 but in Phase 1)
- Metrics that don't align with stated goals
- Contradictory requirements
- Timeline/phase misalignment

**Detection Strategy**:
1. Build glossary of feature names from first mention
2. Track priority assignments
3. Map goals to metrics
4. Compare requirements for conflicts

### 2. Missing Information

Expected content that is absent based on the PRD's depth level.

**What to Look For**:
- Required sections for depth level
- Undefined technical terms
- Features without acceptance criteria (detailed/full-tech)
- Error scenarios not addressed
- Dependencies not listed
- Incomplete personas

**Detection Strategy**:
1. Compare against depth-level checklist
2. Identify domain terms without definitions
3. Check each feature for expected attributes
4. Scan for external system references

### 3. Ambiguities

Statements that are unclear or could be interpreted multiple ways.

**What to Look For**:
- Vague quantifiers ("fast", "many", "scalable")
- Undefined priority language ("should" vs "must")
- Ambiguous pronouns ("it", "this", "they")
- Open-ended lists ("etc.", "and more")
- Undefined scope boundaries

**Detection Strategy**:
1. Flag quantifiers without numbers
2. Check for RFC 2119 language consistency
3. Identify pronouns with unclear antecedents
4. Find incomplete enumerations

### 4. Structure Issues

Problems with document organization, formatting, or references.

**What to Look For**:
- Missing required sections
- Content in wrong section
- Inconsistent formatting
- Orphaned references
- Circular dependencies

**Detection Strategy**:
1. Verify all template sections exist
2. Check content placement logic
3. Validate formatting consistency
4. Test all internal references

---

## Severity Levels

### Critical

**Definition**: Issues that would cause implementation to fail or go significantly wrong.

**Assign When**:
- Fundamental contradiction in requirements
- Core requirement completely undefined
- Required section missing entirely
- Circular dependencies that block implementation
- Security requirement absent (when security is mentioned)

**Examples**:
- "User authentication required" but no auth requirements defined
- Feature A depends on Feature B, Feature B depends on Feature A
- Full-tech PRD with no API specifications

### Warning

**Definition**: Issues that could cause confusion or implementation problems.

**Assign When**:
- Inconsistent naming that could cause misunderstanding
- Acceptance criteria too vague to test
- Important feature lacks error handling
- Ambiguous language for significant functionality
- Minor dependencies unlisted

**Examples**:
- "Search should be fast" without defining "fast"
- User story without acceptance criteria
- Integration mentioned but not in dependencies

### Suggestion

**Definition**: Improvements that would enhance PRD quality but aren't blocking.

**Assign When**:
- Style or clarity improvements
- Non-critical sections could be clearer
- Best practices not followed
- Minor formatting inconsistencies
- Documentation enhancements

**Examples**:
- User stories formatted inconsistently
- Glossary would help but isn't critical
- Additional context would be helpful

---

## Analysis Workflow

### Step 1: Read and Detect Depth

1. Read the entire PRD
2. Detect depth level using indicators (see `references/analysis-criteria.md`)
3. Note the detected depth for criteria selection

### Step 2: Load Criteria

Load the appropriate checklist from `references/analysis-criteria.md` based on detected depth level.

### Step 3: Systematic Scan

Analyze the PRD section by section:

1. **Structure Scan**: Verify all required sections exist
2. **Consistency Scan**: Build glossary, track priorities, map goals to metrics
3. **Completeness Scan**: Check each feature for expected attributes
4. **Clarity Scan**: Flag vague language and ambiguities

### Step 4: Categorize and Prioritize

For each finding:
1. Assign to one of four categories
2. Determine severity based on impact
3. Identify specific location (section, line)
4. Draft recommendation

### Step 5: Generate Report

Create report using `references/report-template.md`:
1. Fill in header information
2. Calculate summary statistics
3. List findings by severity
4. Write overall assessment

---

## Update Mode Workflow

When entering update mode for interactive resolution:

### Finding Presentation

Present each finding with:
```
FINDING X/Y (N resolved, M skipped)

Category: {category}
Severity: {severity}
Location: {section, line}

CURRENT:
{Quoted text from PRD}

ISSUE:
{Clear explanation of the problem}

PROPOSED:
{Suggested fix text}

[Apply] [Modify] [Skip]
```

### User Response Handling

**Apply**:
1. Use Edit tool to apply the proposed change
2. Mark finding as "Resolved" in report
3. Increment resolved counter
4. Move to next finding

**Modify**:
1. Ask user for their preferred text via AskUserQuestion
2. Apply their modified version
3. Mark finding as "Resolved"
4. Move to next finding

**Skip**:
1. Ask if they want to provide a reason (optional)
2. Mark finding as "Skipped" with reason if provided
3. Increment skipped counter
4. Move to next finding

### Session Completion

After all findings processed:
1. Update report with Resolution Summary
2. Show final statistics
3. List resolved and skipped findings
4. Provide recommendations for future PRDs

---

## Reference Files

- `references/analysis-criteria.md` - Depth-specific checklists and detection algorithms
- `references/report-template.md` - Standard report format
- `references/common-issues.md` - Issue pattern library with examples
