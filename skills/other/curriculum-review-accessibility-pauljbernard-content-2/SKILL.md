---
name: curriculum-review-accessibility
description: Validate WCAG 2.1 compliance, screen reader compatibility, and Universal Design for Learning (UDL) principles implementation throughout curriculum materials. Use when checking accessibility, validating UDL, or ensuring compliance. Activates on "accessibility check", "WCAG validation", "UDL review", or "screen reader test".
---

# Accessibility Validation & UDL Compliance

Ensure all curriculum materials meet accessibility standards and implement Universal Design for Learning principles for all learners.

## When to Use

- Validate WCAG 2.1 compliance
- Check UDL implementation
- Test screen reader compatibility
- Verify keyboard navigation
- Ensure accessible formats

## Required Inputs

- **Materials**: Digital content, documents, multimedia
- **Standards**: WCAG 2.1 Level (A, AA, AAA)
- **Platform**: Web, PDF, LMS, etc.

## Workflow

### 1. WCAG 2.1 Compliance Check

**Perceivable**:
✅ Text alternatives for non-text content
✅ Captions and transcripts for multimedia
✅ Content can be presented in different ways
✅ Sufficient color contrast (4.5:1 minimum)
✅ Text can be resized to 200%

**Operable**:
✅ All functionality available via keyboard
✅ Enough time to read and interact
✅ No content that causes seizures (flashing)
✅ Navigation is clear and consistent
✅ Input purposes identified

**Understandable**:
✅ Text is readable and predictable
✅ Pages appear and operate predictably
✅ Input assistance for errors
✅ Labels and instructions provided

**Robust**:
✅ Compatible with assistive technologies
✅ Proper markup and semantics
✅ Name, role, value for all components

### 2. UDL Principles Assessment

**Multiple Means of Representation**:
- ✅ Visual AND textual information
- ✅ Audio descriptions available
- ✅ Content in multiple formats
- ✅ Key vocabulary defined
- ✅ Background knowledge activated

**Multiple Means of Engagement**:
- ✅ Student choice opportunities
- ✅ Relevance and authenticity
- ✅ Appropriate challenge level
- ✅ Collaboration options
- ✅ Self-reflection prompts

**Multiple Means of Expression**:
- ✅ Multiple assessment formats
- ✅ Varied response options
- ✅ Scaffolds for practice
- ✅ Tools and supports available
- ✅ Progress monitoring

### 3. Generate Accessibility Report

```markdown
# Accessibility Review: [TOPIC]

**Review Date**: [Date]
**Standards**: WCAG 2.1 Level AA, UDL
**Materials**: [List]

## Compliance Status

**WCAG 2.1**: [Pass/Fail] - [X/Y criteria met]
**UDL Principles**: [Excellent/Good/Fair/Poor]
**Overall**: [Ready/Needs Revision]

## WCAG Issues Found

### Critical (Level A) - Must Fix
1. [Location]: Missing alt text for diagram
   - **Impact**: Screen reader users cannot access content
   - **Fix**: Add descriptive alt text: "[description]"

### Important (Level AA) - Should Fix
1. [Location]: Color contrast 3.2:1 (needs 4.5:1)
   - **Impact**: Low vision users struggle to read
   - **Fix**: Darken text or lighten background

### Enhancement (Level AAA) - Nice to Have
1. [Location]: No sign language interpretation
   - **Impact**: Deaf users who prefer sign language
   - **Fix**: Consider adding sign language video

## Document Accessibility

**PDF Review**:
- ❌ Headings not tagged
- ❌ Reading order incorrect
- ✅ Searchable text
- ❌ Form fields unlabeled

**Fixes Needed**:
1. Tag all headings with proper levels
2. Fix reading order in Acrobat
3. Add labels to form fields

## Multimedia Accessibility

**Videos**:
- ❌ No captions
- ❌ No transcript
- ❌ No audio description

**Fixes**: Add captions, transcripts, audio descriptions

## UDL Implementation

### Representation (Why)
✅ **Strengths**:
- Multiple formats provided (text, video, diagrams)
- Vocabulary defined
⚠️  **Gaps**:
- No audio version of readings
- Limited visual alternatives

### Engagement (How)
⚠️  **Strengths**:
- Some choice in topics
✅ **Gaps**:
- Limited collaboration options
- No self-regulation scaffolds

### Expression (What)
⚠️  **Strengths**:
- Two assessment format options
❌ **Gaps**:
- No assistive technology support
- Limited scaffolding tools

## Keyboard Navigation
- ✅ All buttons keyboard accessible
- ❌ Skip navigation link missing
- ❌ Focus indicators insufficient

## Screen Reader Testing
- ⚠️  Mostly compatible
- ❌ Some tables not properly structured
- ❌ Links not descriptive ("click here")

## Recommendations

### Priority 1 (Legal Compliance)
1. Add alt text to all images
2. Provide captions for videos
3. Fix color contrast issues
4. Tag PDF headings

### Priority 2 (UDL Implementation)
1. Offer audio versions of text
2. Add student choice opportunities
3. Provide multiple expression formats
4. Include collaboration options

### Priority 3 (Enhancement)
1. Add audio descriptions
2. Provide sign language
3. Enhance keyboard navigation

---

**Artifact Metadata**:
- **WCAG Compliance**: [Level]
- **UDL Rating**: [Score]
- **Critical Issues**: [Count]
- **Ready**: [Yes/No]
```

### 4. CLI Interface

```bash
# Full accessibility review
/curriculum.review-accessibility --materials "curriculum-artifacts/" --standard "WCAG2.1-AA"

# PDF-specific
/curriculum.review-accessibility --pdf "student-handout.pdf"

# UDL focus
/curriculum.review-accessibility --focus "udl" --lessons "lessons/*.md"

# Help
/curriculum.review-accessibility --help
```

## Exit Codes

- **0**: Fully compliant
- **1**: Issues found
- **2**: Cannot load materials
- **3**: Critical accessibility barriers
