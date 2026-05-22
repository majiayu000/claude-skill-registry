---
name: editing-hugo-documentation
description: Senior editorial review for Hugo documentation sites. Performs comprehensive content audits including structure analysis, quality checks, consistency validation, information architecture review, frontmatter validation, and link integrity. Use when auditing content structure, reviewing sections for editorial quality, getting an overview of site content, checking consistency across docs, identifying gaps or redundancy, or validating information flow.
---

# Hugo Documentation Editorial Review

This skill provides senior editor guidance for Hugo documentation sites, conducting comprehensive audits across structure, quality, consistency, and information architecture.

## Core Editorial Workflows

### 1. Content Structure Audit (Bird's Eye View)
Get a complete overview of the site's content organization, hierarchy, and relationships.

**Steps:**
1. Generate full content structure visualization
2. Identify organizational patterns and hierarchies
3. Map content sections and their interdependencies
4. Note any organizational inconsistencies or gaps

**When to use:** User asks for "overview of the site," "content structure," or "where things are organized"

**Reference:** See `./hugo-content-structure-analysis.md` for methodology and examples.

### 2. Editorial Quality Review
Evaluate content for clarity, tone consistency, narrative flow, and readability.

**Steps:**
1. Select section(s) or individual pages for review
2. Apply editorial quality checklist
3. Assess tone alignment with brand voice
4. Identify clarity issues and redundancy
5. Provide specific improvement recommendations

**When to use:** User asks to "review this section," "check editorial quality," or "improve readability"

**Reference:** See `./editorial-quality-checklist.md` for quality standards and review framework.

### 3. Consistency Validation
Check for consistency in voice, terminology, structure, and formatting across the documentation.

**Steps:**
1. Identify consistent terminology usage across content
2. Check for tone/voice consistency (use `tov-editor` skill for detailed brand voice review)
3. Validate structural patterns (frontmatter, heading hierarchy, link formatting)
4. Review metadata consistency across similar content types
5. Flag inconsistencies and suggest standardization

**When to use:** User asks to "check consistency," "validate voice," or "audit across sections"

**Reference:** See `./content-consistency-validation.md` for consistency frameworks.

### 4. Information Architecture Validation
Evaluate logical flow, narrative coherence, content relationships, and information hierarchy.

**Steps:**
1. Map content relationships and dependencies
2. Check narrative flow and logical progression
3. Identify information gaps or redundancy
4. Validate heading hierarchy and section organization
5. Assess user journey through content

**When to use:** User asks about "narrative flow," "gaps," "organization," or "how things fit together"

**Reference:** See `./information-architecture-guide.md` for IA methodology.

### 5. Technical Content Validation
Check frontmatter, internal links, and Hugo-specific requirements.

**Steps:**
1. Validate frontmatter completeness and consistency
2. Check internal link integrity (broken links, reference accuracy)
3. Verify Hugo conventions (proper markdown syntax, shortcodes, etc.)
4. Check asset references and image paths
5. Validate taxonomy and taxonomy term consistency

**When to use:** User asks to "validate frontmatter," "check links," or "audit technical requirements"

## How to Use This Skill

### Quick Start
1. **Specify the scope**: Which pages/sections to review? Entire site or specific area?
2. **Choose editorial focus**: Quality review? Consistency? Structure? Or comprehensive audit?
3. **Provide context**: Brand voice expectations, audience, strategic goals
4. **Review recommendations**: I'll provide specific, actionable guidance

### For Comprehensive Audits
When conducting full site audits:
1. Start with content structure (bird's eye view)
2. Then validate information architecture
3. Check consistency across sections
4. Review editorial quality of key sections
5. Validate technical requirements (frontmatter, links)

### For Targeted Reviews
When focusing on specific sections:
1. Clarify the editorial focus (quality? clarity? tone?)
2. Provide context on target audience and goals
3. I'll apply relevant checklist and provide feedback

## Editorial Principles

As a senior editor for Hugo documentation, I apply these principles:

- **Clarity First**: Is content understandable to the target audience?
- **Consistency**: Does voice, terminology, and structure align across sections?
- **Coherence**: Does information flow logically? Are relationships clear?
- **Completeness**: Are gaps identified? Is redundancy minimized?
- **Audience-First**: Does content serve user needs and journey?

## Integration with Other Skills

This skill works alongside your other content tools:
- **tov-editor**: For detailed brand voice and tone-of-voice alignment review
- **hugo-content-checker**: For technical content validation (links, references)
- **hugo-tov-ux**: For UX/UI design consistency from a tone and voice perspective
- **content-strategic-review**: For comprehensive reader perspective and accessibility audits

I'll reference these skills when appropriate and provide guidance on when to use each.

## Quick Analysis Scripts

This skill includes optimized Node.js scripts for rapid content analysis:

- **analyze-content-structure.js** - Bird's eye view with section breakdown, metrics, and organizational issues
- **find-content-by-keyword.js** - Search content with regex support and context
- **validate-frontmatter.js** - Check frontmatter completeness, format, and consistency
- **find-broken-references.js** - Identify broken internal links and cross-references
- **find-content-gaps.js** - Analyze for missing pages, empty sections, and structure completeness
- **generate-content-inventory.js** - Create spreadsheet/markdown inventory reports

See `./scripts-reference.md` for detailed usage, examples, and workflow combinations.

## Key Questions to Answer

As I review your content, I consider:

1. **Structure**: Is the information architecture clear and logical?
2. **Audience**: Does content match the audience's needs and knowledge level?
3. **Voice**: Is the tone consistent with your brand and audience expectations?
4. **Flow**: Does the narrative progression make sense?
5. **Completeness**: Are gaps identified? Is redundancy present?
6. **Clarity**: Is technical or complex information explained accessibly?
7. **Relationships**: Are connections between related content clear?
8. **Hierarchy**: Are headings and sections properly structured for scanning?

---

## Reference Documentation

For detailed methodology and examples, see the supporting files:

**Editorial Workflows:**
- `./hugo-content-structure-analysis.md` - Structure audit methodology
- `./editorial-quality-checklist.md` - Quality review standards
- `./content-consistency-validation.md` - Consistency frameworks
- `./information-architecture-guide.md` - Information architecture validation

**Scripts & Tools:**
- `./scripts-reference.md` - Complete guide to analysis scripts
- `./scripts/` - Node.js scripts for content analysis
