---
document_name: "quality-review.skill.md"
location: ".claude/skills/quality-review.skill.md"
codebook_id: "CB-SKILL-QUALREVIEW-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for quality code reviews"
skill_metadata:
  category: "quality"
  complexity: "intermediate"
  estimated_time: "15-45 min per PR"
  prerequisites:
    - "Code quality standards"
    - "Testing knowledge"
category: "skills"
status: "active"
tags:
  - "skill"
  - "quality"
  - "review"
ai_parser_instructions: |
  This skill defines procedures for quality reviews.
  Section markers: === SECTION ===
---

# Quality Review Skill

=== PURPOSE ===

This skill provides procedures for conducting quality code reviews. QA Lead has BLOCKING authority for quality issues.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(qa-lead) @ref(CB-AGENT-QA-001) | Primary skill for quality reviews |

---

=== PROCEDURE: Quality Review Checklist ===

**Template:** @ref(CB-TPL-QUALREVIEW-001)

### Test Coverage
- [ ] Unit tests cover new functionality
- [ ] Integration tests where appropriate
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Coverage meets threshold (e.g., 80%)

### Code Quality
- [ ] No code smells
- [ ] Single responsibility principle followed
- [ ] DRY principle applied
- [ ] Clear naming conventions
- [ ] Appropriate comments where needed

### Maintainability
- [ ] Code is readable
- [ ] Complex logic documented
- [ ] No magic numbers/strings
- [ ] Consistent patterns used

### Performance
- [ ] No obvious performance issues
- [ ] N+1 queries avoided
- [ ] Appropriate caching considered
- [ ] Memory leaks avoided

### Error Handling
- [ ] Errors handled gracefully
- [ ] User-friendly error messages
- [ ] Appropriate logging

---

=== PROCEDURE: Coverage Assessment ===

**Steps:**
1. Review coverage report
2. Identify uncovered lines
3. Assess if uncovered code needs tests
4. Document coverage gaps
5. Approve or request additional tests

**Minimum Thresholds:**
- Line coverage: 80%
- Branch coverage: 75%
- Function coverage: 80%

---

=== PROCEDURE: Code Smell Detection ===

**Common Code Smells:**
- Long methods (>20 lines)
- Large classes (>300 lines)
- Duplicate code
- Deep nesting (>3 levels)
- Too many parameters (>4)
- Comments explaining bad code

---

=== PROCEDURE: Quality Finding Documentation ===

**Format:**
```markdown
### [PRIORITY] Finding Title

**Location:** file.js:line
**Type:** [Coverage/Quality/Performance/etc.]
**Priority:** [High/Medium/Low]

**Issue:**
What the quality issue is.

**Recommendation:**
How to improve it.
```

---

=== PRIORITY DEFINITIONS ===

| Priority | Definition | Action |
|----------|------------|--------|
| High | Significant quality issue | Block, must fix |
| Medium | Notable quality concern | Block or advisory |
| Low | Minor improvement | Advisory |

---

=== ANTI-PATTERNS ===

### Nitpicking
**Problem:** Blocking for style preferences
**Solution:** Focus on substantive issues

### Ignoring Tests
**Problem:** Not reviewing test quality
**Solution:** Review tests as carefully as code

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(testing-strategy) | Testing approach context |
| @skill(quality-gates) | Quality enforcement |
