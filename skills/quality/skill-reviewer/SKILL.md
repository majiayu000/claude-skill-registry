---
name: skill-reviewer
description: Evaluates skill effectiveness, suggests improvements to instructions, identifies missing edge cases, and recommends structure changes.
---

# Skill Reviewer

## Purpose

The Skill Reviewer provides comprehensive quality assurance and improvement recommendations for Claude Code skills. It evaluates skills against official Anthropic guidelines, identifies clarity issues, detects missing edge cases, and suggests structural improvements. Use this skill to validate skill quality, identify gaps, and ensure skills meet professional standards before distribution.

## When to Use

- **Evaluating New Skills**: Review skills before adding to project or distributing
- **Improving Existing Skills**: Identify gaps and enhancement opportunities
- **Quality Assurance**: Ensure skills meet Anthropic guidelines
- **Documentation Audit**: Check for clarity, completeness, and accessibility
- **Structure Validation**: Verify proper organization and naming conventions
- **Edge Case Testing**: Identify scenarios the skill doesn't handle
- **Pre-Release Review**: Final validation before skill distribution
- **Team Standards**: Ensure consistency across skill libraries

## Capabilities

- **Metadata Validation**: Check YAML frontmatter, name conventions, description completeness
- **Documentation Audit**: Evaluate clarity, completeness, and user accessibility
- **Structure Assessment**: Verify directory organization, file hierarchy, and naming patterns
- **Functionality Coverage**: Identify missing capabilities and edge cases
- **Instruction Quality**: Analyze step-by-step guides, examples, and usage patterns
- **Guideline Compliance**: Verify adherence to Anthropic skill standards
- **Cross-Reference Validation**: Check links to related skills and documentation
- **Risk Identification**: Spot potential issues, confusion points, and improvement areas
- **Score Generation**: Provide overall skill quality score (0-100) with grade (A-F)
- **Improvement Roadmap**: Generate prioritized recommendations for enhancements

## Evaluation Framework

### 1. Metadata Quality (20 points)

**YAML Frontmatter**

- ✅ Valid YAML syntax
- ✅ Required fields present: `name`, `description`
- ✅ Consistent naming (kebab-case, lowercase)
- ✅ Description is one concise sentence

**Naming Conventions**

- ✅ Directory name matches skill name
- ✅ Descriptive verb-based names (not "helper", "tool", "manager")
- ✅ Clear intent without jargon
- ✅ Consistent with project patterns

### 2. Documentation Quality (25 points)

**Structure & Organization**

- ✅ Clear heading hierarchy (H1 → H2 → H3)
- ✅ Logical content flow
- ✅ Proper use of formatting (bold, code, lists)
- ✅ Consistent voice and tone

**Content Completeness**

- ✅ Purpose section present and clear
- ✅ "When to Use" section with scenarios
- ✅ Capabilities listed with specifics
- ✅ Usage examples with code snippets
- ✅ Best practices documented
- ✅ Troubleshooting section for common issues

**Clarity & Accessibility**

- ✅ Jargon-free or well-explained
- ✅ Active voice preferred
- ✅ Concrete examples over abstract concepts
- ✅ Appropriate detail level for audience

### 3. Structure & Organization (20 points)

**File Organization**

- ✅ SKILL.md in root of skill directory
- ✅ `scripts/` subdirectory for automation (lowercase, if needed)
- ✅ `references/` subdirectory for detailed docs (lowercase, if needed)
- ✅ `assets/` subdirectory for templates/boilerplate (lowercase, if needed)
- ✅ README.md for development notes (excluded from distribution)

**Directory Conventions**

- ✅ Lowercase directory names
- ✅ No nested subdirectories in `references/`
- ✅ Single-level organization
- ✅ Consistent naming patterns

**File Size Constraints**

- ✅ SKILL.md under 500 lines (move excessive detail to `references/`)
- ✅ Reference files over 100 lines have table of contents
- ✅ Executable scripts have proper permissions (`chmod +x`)

### 4. Functionality & Coverage (20 points)

**Scope & Capabilities**

- ✅ Clear boundaries of what skill does/doesn't do
- ✅ Realistic capability claims
- ✅ No overpromising functionality
- ✅ Dependencies clearly documented

**Edge Cases & Error Handling**

- ✅ Anticipated edge cases addressed
- ✅ Error scenarios handled gracefully
- ✅ Fallback strategies documented
- ✅ Limitations explicitly stated

**Practical Applicability**

- ✅ Real-world usage scenarios covered
- ✅ Examples are realistic and actionable
- ✅ Step-by-step guides are complete
- ✅ Expected outcomes clearly defined

### 5. Guideline Compliance (15 points)

**Anthropic Standards**

- ✅ Follows official skill guidelines
- ✅ Proper YAML syntax validation
- ✅ Description includes "when to use" triggers
- ✅ No auxiliary docs mixed with skill content

**Project Standards**

- ✅ Aligns with project conventions
- ✅ Consistent with similar skills
- ✅ Follows naming patterns
- ✅ Uses established templates

**Best Practices**

- ✅ Clear value proposition
- ✅ Appropriate scope (not too broad)
- ✅ Progressive content disclosure
- ✅ Links to related resources

## Usage

### Basic Review

```bash
# User: "Review the react-component-scaffolder skill"
# Skill Reviewer will:
# 1. Read the SKILL.md file
# 2. Evaluate against all criteria
# 3. Generate comprehensive review report
# 4. Provide improvement recommendations
# 5. Output skill-reviewer_report.md
```

### Structure Review

```bash
# User: "Check the directory structure of the fastapi-endpoint-scaffolder skill"
# Skill Reviewer will:
# 1. Verify SKILL.md location and format
# 2. Check subdirectory organization
# 3. Validate file naming conventions
# 4. Review file permissions and sizes
# 5. Recommend structural improvements
```

### Edge Case Analysis

```bash
# User: "Identify missing edge cases in the component-builder skill"
# Skill Reviewer will:
# 1. Analyze described capabilities
# 2. Brainstorm unhandled scenarios
# 3. Test against common failure modes
# 4. List missing functionality
# 5. Recommend coverage improvements
```

### Compliance Check

```bash
# User: "Verify that my-new-skill follows Anthropic guidelines"
# Skill Reviewer will:
# 1. Validate YAML frontmatter
# 2. Check naming conventions
# 3. Verify description completeness
# 4. Review against official standards
# 5. Report compliance status
```

## Examples

### Example 1: Quality Review Report

**Skill Reviewed**: `jest-test-scaffolder`

**Review Output**:

```
# Skill Review: jest-test-scaffolder

## Overall Score: 87/100 (Grade: B+)

### Metadata Quality: 18/20
✅ Valid YAML frontmatter
✅ Clear, concise description
❌ Description could include mention of "Jest" specifically
⚠️  Consider adding example output reference

### Documentation Quality: 23/25
✅ Comprehensive "When to Use" section
✅ Clear capabilities list
❌ Missing troubleshooting section
⚠️  One example could show error handling

### Structure & Organization: 19/20
✅ Proper directory structure
✅ SKILL.md under 500 lines
❌ Reference files lack table of contents
⚠️  Consider adding assets/ directory for templates

### Functionality & Coverage: 19/20
✅ Real-world scenarios covered
✅ Clear step-by-step guide
⚠️  Missing edge case: TypeScript strict mode configuration
⚠️  No mention of coverage threshold testing

### Guideline Compliance: 14/15
✅ Follows Anthropic standards
⚠️  Could strengthen "when to use" language

## Recommendations

### Priority 1 (Critical)
1. Add troubleshooting section for common Jest configuration issues
2. Document edge case: TypeScript strict mode with React Testing Library

### Priority 2 (High)
1. Add table of contents to reference files
2. Include example output in capabilities section
3. Add coverage threshold testing to best practices

### Priority 3 (Nice to Have)
1. Create templates/ directory with example test files
2. Add video walkthrough link
3. Document advanced patterns for custom matchers

## Usage Statistics
- User Feedback: 4.2/5 ⭐
- Effectiveness: High (solving real problems)
- Complexity: Medium
```

### Example 2: Edge Case Analysis

**Skill Reviewed**: `deployment-manager`

**Edge Cases Identified**:

```markdown
## Missing Edge Case Coverage

### Unhandled Scenarios

1. **Deployment Timeout**: No guidance on stuck deployments
2. **Rollback Failures**: What if rollback fails?
3. **Multi-Region**: Only documents single-region deployment
4. **Authentication Expiry**: No mention of credential refresh during long deployments
5. **Partial Failures**: Handling when some services deploy but others fail
6. **Concurrent Deployments**: What happens if two deployments run simultaneously?
7. **Resource Constraints**: No mention of memory/disk requirements
8. **Network Interruptions**: Handling transient network failures

### Recommended Additions

- Add deployment timeout configuration section
- Document rollback procedures in detail
- Include multi-region deployment guide
- Add environment variable validation step
- Create contingency/recovery procedures
- Add resource requirements documentation
```

### Example 3: Structure Recommendations

**Skill Reviewed**: `component-builder`

**Structure Improvements**:

```markdown
## Current Structure
```

.claude/skills/component-builder/
├── SKILL.md (620 lines - exceeds 500 limit)
└── README.md

```

## Recommended Structure
```

.claude/skills/component-builder/
├── SKILL.md (380 lines - main overview)
├── README.md (development notes, not distributed)
├── references/
│ ├── MATERIAL_DESIGN_3_TOKENS.md (detailed token reference)
│ ├── COMPONENT_PATTERNS.md (advanced patterns, 150+ lines, includes TOC)
│ └── TYPESCRIPT_SETUP.md (TypeScript configuration guide)
├── scripts/
│ ├── generate-component.sh (executable)
│ └── validate-m3-tokens.py (executable)
└── assets/
├── component.tsx.template
├── component.test.tsx.template
└── component.stories.tsx.template

```

## Benefits
- SKILL.md within 500-line limit (progressive disclosure)
- Reference files organized by topic
- Reusable templates in assets/
- Automation scripts clearly separated
- Better content navigation
```

## Best Practices

### For Skill Developers

1. **Self-Review First**: Use this skill before distributing
2. **Iterate Based on Feedback**: Implement recommendations progressively
3. **Test Your Examples**: Verify all code snippets work
4. **Get Peer Review**: Have teammates review critical skills
5. **Version Your Skills**: Track changes and improvements

### For Skill Maintenance

1. **Regular Audits**: Review skills quarterly
2. **User Feedback**: Incorporate reports and suggestions
3. **Update Examples**: Keep code samples current
4. **Expand Coverage**: Add edge cases as they're discovered
5. **Archive Old Skills**: Retire obsolete skills clearly

### For Skill Distribution

1. **Pre-Release Review**: Score ≥80 before distribution
2. **Document Dependencies**: List required tools/knowledge
3. **Provide Feedback Mechanism**: How users report issues
4. **Create Support Resources**: Links to help and troubleshooting
5. **Plan Updates**: Version numbering and upgrade path

## Scoring Guidelines

### Grade Scale

- **A (90-100)**: Exceptional - Ready for distribution, exemplary quality
- **B (80-89)**: Good - Ready for distribution, minor improvements suggested
- **C (70-79)**: Satisfactory - Usable but needs improvements before wider sharing
- **D (60-69)**: Poor - Needs significant work before distribution
- **F (Below 60)**: Inadequate - Not ready for release, major rework required

### Minimum Distribution Standards

- ✅ Score ≥ 80 (Grade B or higher)
- ✅ All Priority 1 recommendations addressed
- ✅ Comprehensive documentation
- ✅ Tested examples and workflows
- ✅ Clear scope and limitations

## Troubleshooting

### Issue: Score Below 80

**Solution**:

1. Address all Priority 1 recommendations first
2. Add missing sections (troubleshooting, edge cases)
3. Improve documentation clarity
4. Get peer review for feedback
5. Iterate and re-review

### Issue: Unclear Recommendations

**Solution**:

1. Request specific examples
2. Ask for comparison with high-scoring skill
3. Discuss recommendations with team
4. Review Anthropic guidelines for clarification
5. Request follow-up review after changes

### Issue: Scope Too Broad

**Solution**:

1. Break into smaller, focused skills
2. Move advanced topics to references/
3. Focus on core use case
4. Create related skills for extensions
5. Use "Related Skills" to connect them

## Related Skills

- [skill-creator](.../skill-creator/SKILL.md) - Create new Claude Code skills
- [task-delegator](.../task-delegator/SKILL.md) - Delegate review tasks to specialized agents
- [code-reviewer](.../code-reviewer/SKILL.md) - Review code quality and structure
- [project-health-checker](.../project-health-checker/SKILL.md) - Comprehensive project validation
- [audit-agent](.../audit-agent/SKILL.md) - Security and quality audits

## Related Documentation

- [Anthropic Skill Guidelines](https://github.com/anthropics/skills/blob/main/skill-creator/SKILL.md)
- [SKILL_GUIDELINES_AUDIT.md](./.claude/docs/SKILL_GUIDELINES_AUDIT.md) - Project skill audit
- [Skill Development Best Practices](CLAUDE.md#skills-development--tooling)

## Summary

The Skill Reviewer provides systematic, objective evaluation of Claude Code skills across five key dimensions: metadata, documentation, structure, functionality, and guideline compliance. Use it to ensure skills meet professional standards, identify improvement opportunities, and maintain consistent quality across skill libraries.

**Quick Checklist for High-Quality Skills:**

- ✅ Score ≥ 80/100 (Grade B or higher)
- ✅ Clear, concise description with "when to use"
- ✅ Comprehensive documentation with examples
- ✅ Proper directory structure and naming
- ✅ Addressed Priority 1 recommendations
- ✅ All claims tested and verified
- ✅ Edge cases documented
- ✅ Related skills and references linked
