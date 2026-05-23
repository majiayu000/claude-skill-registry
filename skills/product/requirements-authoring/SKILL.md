---
name: pm-requirements:requirements-authoring
source_bundle: pm-requirements
description: Comprehensive standards for creating and maintaining requirements and specification documents with SMART principles, proper structure, integrity, and traceability
version: 0.1-BETA
allowed-tools: []
standards:
  - requirements-format-and-structure
  - smart-requirements-principles
  - specification-structure-and-backtracking
  - documentation-lifecycle-management
  - integrity-and-quality-standards
  - maintenance-and-deprecation-handling
---

# Requirements and Specification Authoring Standards

Comprehensive standards for creating, structuring, and maintaining requirements and specification documents in CUI projects following SMART principles, ensuring complete traceability, and maintaining documentation integrity throughout the project lifecycle.

## What This Skill Provides

This skill consolidates all standards for authoring requirements and specification documents:

- **Requirements Format**: SMART principles, ID schemes, numbering, and structure
- **Specification Structure**: Document organization, backtracking links, and traceability patterns
- **Documentation Lifecycle**: Pre-implementation, during implementation, and post-implementation practices
- **Quality Standards**: Clarity, completeness, consistency, and testability requirements
- **Integrity Requirements**: No hallucinations, no duplications, verified links
- **Maintenance Standards**: Adding, modifying, removing, and deprecating requirements

## When to Activate

Use this skill when:

- Creating new requirements documents for projects
- Writing specification documents with proper structure
- Maintaining existing requirements and specifications
- Ensuring documentation integrity and quality
- Setting up traceability between requirements, specs, and code
- Handling requirement deprecation or removal

## Workflow

### 1. Creating Requirements

When creating new requirements:

1. Follow SMART principles (Specific, Measurable, Achievable, Relevant, Time-bound)
2. Use consistent ID format: `[#PREFIX-NUM]`
3. Structure with proper headings and bullet points
4. Maintain sequential numbering (never reuse IDs)
5. Link to specifications when created

### 2. Writing Specifications

When creating specifications:

1. Create backtracking links to requirements: `_See Requirement link:../Requirements.adoc#REQ-ID[REQ-ID: Title]_`
2. Organize by component or functional area
3. Use proper status indicators (PLANNED, IN PROGRESS, IMPLEMENTED)
4. Link to implementation code when it exists
5. Update as implementation progresses

### 3. Maintaining Documentation

When maintaining requirements/specifications:

1. Verify no hallucinated functionality (all documented features must exist or be planned)
2. Eliminate duplications (use cross-references instead)
3. Verify all links are functional
4. Update implementation status as code is written
5. Handle deprecation appropriately (ask user for post-1.0 projects)

### 4. Ensuring Quality

Before finalizing documentation:

1. Check all cross-references resolve correctly
2. Verify consistent terminology throughout
3. Ensure clear traceability from requirements to specs to code
4. Validate SMART criteria for all requirements
5. Confirm no duplicate information across documents

## Standards Organization

Standards are organized into focused documents:

### Core Authoring Standards

**requirements-format-and-structure.md**
- Requirement ID format and anchors
- Heading format and hierarchy
- Content organization patterns
- Bullet point structure
- Document header requirements

**smart-requirements-principles.md**
- SMART criteria definitions
- Specific requirements patterns
- Measurable criteria examples
- Achievable and relevant requirements
- Testability requirements

**specification-structure-and-backtracking.md**
- Specification document structure
- Main vs. individual specification files
- Backtracking link format and placement
- Multiple requirement references
- Path variations for cross-references

### Lifecycle Management

**documentation-lifecycle-management.md**
- Pre-implementation specifications (detailed design, examples, expected API)
- During implementation updates (implementation links, decisions, notes)
- Post-implementation refinement (status updates, implementation links, removing redundancy)
- Transitioning between lifecycle phases

### Quality and Integrity

**integrity-and-quality-standards.md**
- No hallucinations rule (verify all documented features)
- No duplications rule (use cross-references)
- Verified links requirement
- Consistency requirements
- Clarity and completeness standards
- Maintainability principles

**maintenance-and-deprecation-handling.md**
- Adding new requirements (numbering, format, linking)
- Modifying existing requirements (preserve IDs, update content)
- Removing requirements (never delete, deprecate instead)
- Pre-1.0 vs. post-1.0 deprecation handling
- Refactoring requirements (maintain IDs, update references)

## Tool Access

This skill requires:

- **Read** - To review existing requirements and specifications
- **Edit** - To update existing documentation
- **Write** - To create new requirements and specification files
- **Grep** - To search for requirement IDs and verify consistency
- **Glob** - To find all requirements and specification files

## Integration

This skill integrates with:

- **pm-requirements:setup** - Provides initial structure that authoring populates
- **pm-requirements:planning** - Planning tasks trace to requirements created here
- **pm-requirements:traceability** - Links authored specs to implementation code
- **cui-documentation:cui-documentation** - General AsciiDoc formatting standards
- **pm-dev-java:javadoc** - JavaDoc standards for referencing requirements

## Anti-Patterns to Avoid

**Over-specification in requirements:**
- ❌ "The system must use a HashMap to store tokens"
- ✅ "The system must cache validated tokens for performance"

**Vague requirements:**
- ❌ "The system should be fast and secure"
- ✅ "Token validation must complete within 50ms for 95% of requests"

**Implementation details in requirements:**
- ❌ "The TokenValidator class must use jose4j library"
- ✅ "The system must validate JWT signatures according to RFC 7519"

**Duplicating content across documents:**
- ❌ Copying requirement text into specifications
- ✅ Using backtracking links to reference requirements

**Hallucinated functionality:**
- ❌ Documenting features that don't exist or aren't planned
- ✅ Verifying all documented features against code or approved plans

## Quality Checklist

Before completing requirements/specification work:

- [ ] All requirements follow SMART principles
- [ ] All requirement IDs follow PREFIX-NUM format
- [ ] All specifications have backtracking links to requirements
- [ ] No hallucinated functionality documented
- [ ] No duplicate information across documents
- [ ] All cross-references verified and functional
- [ ] Consistent terminology throughout
- [ ] Clear traceability maintained
- [ ] Implementation status indicators current
- [ ] Documentation integrity validated

## Related Standards

**Within Bundle:**
- setup - Initial structure creation
- planning - Task tracking linked to requirements
- traceability - Linking specs to implementation

**External:**
- cui-documentation:cui-documentation - AsciiDoc formatting
- pm-dev-java:javadoc - JavaDoc requirement references
- pm-workflow:workflow-integration-git - Committing requirement changes
