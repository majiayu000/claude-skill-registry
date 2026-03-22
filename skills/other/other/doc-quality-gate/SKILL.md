---
name: vibe-doc-quality-gate
description: Performs a fast 6-point quality check for technical documents (specs, design docs, READMEs). Use after editing any specification or design document.
user-invocable: true
---

# vibe-doc-quality-gate

A fast quality gate for technical documents. Not a deep review — just catches the obvious structural issues.

## When to Use This Skill

- After creating or editing a specification document
- After writing a design doc or technical RFC
- Before sharing a document for review
- Periodic document health checks

## When NOT to Use This Skill

- For code review (use `vibe-quality-loop` or `vibe-devil-advocate-review`)
- For informal notes or scratch documents
- For README files that are just getting started

## The 6 Checks

### 1. Overview/Quick Start
Does the document have an overview or quick-start section that explains what this is and why it matters in <5 paragraphs?
- PASS: Overview exists with purpose and scope
- FAIL: No overview, or jumps straight into details

### 2. Structural Completeness
Does the document reference concrete artifacts?
- At least 3 file paths or API endpoints
- At least 1 data structure or type definition
- At least 1 error case or failure mode
- At least 3 test cases or validation steps
- PASS: All present | WARN: 2-3 present | FAIL: 0-1 present

### 3. Cross-Reference Integrity
Are references to other documents, APIs, or code valid?
- Check that referenced files exist
- Check that referenced types/functions exist
- PASS: All references valid | FAIL: Broken references found

### 4. Test Coverage
Does the document specify how to verify the implementation?
- At least 3 test cases for small docs
- At least 10 for large docs
- PASS: Adequate test coverage | WARN: Below threshold

### 5. Command Accuracy
Are commands, paths, and code snippets accurate?
- Do file paths exist (or are marked "to be created")?
- Do commands actually run?
- PASS: All verified | FAIL: Broken commands/paths

### 6. Self-Sufficiency
Could someone implement this without asking questions?
- Pick 3 random sections. Could you implement each without external context?
- PASS: Yes | FAIL: Ambiguous or incomplete sections

## Output Format

### Document Quality Gate: [Document Name]

**Overall**: PASS / WARN / FAIL

| Check | Status | Notes |
|-------|--------|-------|
| 1. Overview | ✓/✗ | [notes] |
| 2. Structure | ✓/◐/✗ | [X/4 artifacts] |
| 3. Cross-refs | ✓/✗ | [X broken] |
| 4. Tests | ✓/◐ | [X cases] |
| 5. Commands | ✓/✗ | [X broken] |
| 6. Self-sufficiency | ✓/✗ | [notes] |

### Issues to Fix
1. [Specific issue with location]
