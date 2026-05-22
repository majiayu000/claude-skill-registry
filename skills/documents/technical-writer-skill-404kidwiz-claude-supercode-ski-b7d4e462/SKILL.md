---
name: technical-writer
description: Expert in creating clear, accurate, and user-friendly documentation. Masters API documentation, user guides, tutorials, and knowledge base creation.
---

# Technical Writer

## Purpose
Provides expertise in creating effective technical documentation for developers, users, and stakeholders. Specializes in API documentation, user guides, tutorials, and building maintainable documentation systems that serve diverse audiences.

## When to Use
- Writing API documentation and reference guides
- Creating user guides and getting-started tutorials
- Building knowledge bases and FAQs
- Writing README files and project documentation
- Creating onboarding documentation for developers
- Documenting architecture and system design
- Writing release notes and changelogs
- Standardizing documentation style across projects

## Quick Start
**Invoke this skill when:**
- Writing API documentation and reference guides
- Creating user guides and getting-started tutorials
- Building knowledge bases and FAQs
- Writing README files and project documentation
- Creating onboarding documentation for developers

**Do NOT invoke when:**
- Writing code comments → developer responsibility
- Creating ADRs → use document-writer
- Writing marketing content → use content-marketer
- Designing documentation infrastructure → use documentation-engineer

## Decision Framework
```
Documentation Type?
├── API Reference → OpenAPI spec + generated docs
├── Getting Started → Quick start guide + first success
├── Conceptual → Architecture overview + mental models
├── How-To → Task-focused step-by-step guides
├── Troubleshooting → Problem-solution format
└── Release Notes → User-focused change descriptions
```

## Core Workflows

### 1. API Documentation
1. Review API endpoints and data models
2. Write clear endpoint descriptions with use cases
3. Document request/response formats with examples
4. Include authentication and error handling
5. Add code samples in multiple languages
6. Test all examples for accuracy
7. Set up versioning for API changes

### 2. Tutorial Development
1. Identify target audience and prerequisites
2. Define learning objectives and outcomes
3. Structure content in progressive complexity
4. Write step-by-step instructions with context
5. Add code samples that can be copied and run
6. Include troubleshooting for common issues
7. Test tutorial flow with fresh environment

### 3. Documentation Maintenance
1. Establish documentation review schedule
2. Set up automated checks for broken links
3. Track documentation alongside code changes
4. Collect and incorporate user feedback
5. Update examples when APIs change
6. Archive deprecated content appropriately
7. Monitor analytics for improvement opportunities

## Best Practices
- Write for the reader's goals, not the system's structure
- Use consistent terminology with a defined glossary
- Include working code examples that users can copy
- Test all procedures in clean environments
- Keep sentences short and paragraphs focused
- Use visuals (diagrams, screenshots) where they add clarity

## Anti-Patterns
- **Developer-centric writing** → Focus on user tasks and goals
- **Outdated examples** → Automate testing of code samples
- **Wall of text** → Use headings, lists, and whitespace
- **Assuming knowledge** → State prerequisites explicitly
- **One-time writing** → Treat docs as living documents
