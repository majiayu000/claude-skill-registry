---
name: documentation
description: Comprehensive documentation specialist covering API documentation, technical
  writing, design documentation, migration guides, and changelog generation. Use when
  creating OpenAPI/Swagger specs, generating SDKs, writing user guides, creating README
  files, documenting architecture, writing design specs, creating ADRs, writing migration
  guides, or generating changelogs from git commits. Handles versioning, examples,
  developer experience, and user-facing documentation.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Documentation

This skill provides comprehensive documentation capabilities including API documentation, technical writing, changelog generation, and developer guides. It covers everything from OpenAPI specifications to user-facing changelogs.

## When to Use This Skill

- When documenting REST APIs or GraphQL schemas
- When creating OpenAPI/Swagger specifications
- When generating client SDKs
- When writing API integration guides
- When creating interactive API documentation
- When maintaining API versioning and migration guides
- When writing user guides and tutorials
- When creating or improving README files
- When documenting architecture and design decisions
- When writing code comments and inline documentation
- When improving content clarity and accessibility
- When creating getting started documentation
- When writing feature specifications and design documents
- When creating Architecture Decision Records (ADRs)
- When documenting technical decisions and their rationale
- When creating migration guides for version upgrades
- When documenting breaking changes and upgrade paths
- When planning and documenting database migrations
- When preparing release notes for a new version
- When creating weekly or monthly product update summaries
- When documenting changes for customers
- When writing changelog entries for app store submissions
- When generating update notifications
- When creating internal release documentation
- When maintaining a public changelog/product updates page

## What This Skill Does

1. **OpenAPI Specs**: Creates complete OpenAPI 3.0/Swagger specifications
2. **SDK Generation**: Generates client libraries and SDKs
3. **Interactive Docs**: Creates Postman collections and interactive docs
4. **Versioning**: Manages API versioning and migration guides
5. **Code Examples**: Provides examples in multiple languages
6. **Developer Guides**: Writes authentication and integration guides
7. **User Guides**: Creates step-by-step user guides with clear instructions
8. **Tutorials**: Writes progressive tutorials that build knowledge
9. **README Files**: Creates comprehensive README files with badges and sections
10. **Architecture Docs**: Documents system architecture and design decisions
11. **Code Documentation**: Writes clear code comments and inline docs
12. **Content Organization**: Structures content with clear headings and flow
13. **Changelog Generation**: Transforms git commits into user-friendly changelogs
14. **Design Specs**: Creates feature specifications and technical design documents
15. **ADRs**: Documents Architecture Decision Records with context and consequences
16. **Migration Guides**: Creates step-by-step migration documentation with rollback procedures

## How to Use

### Document API

```
Create OpenAPI specification for this API
```

```
Generate API documentation for the /api/users endpoints
```

### Write Documentation

```
Create a user guide for this feature
```

```
Write a README for this project
```

### Generate Changelog

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

## API Documentation

### Document as You Build

- Document APIs during development, not after
- Keep documentation in sync with code
- Use real examples over abstract descriptions
- Show both success and error cases
- Version everything including docs

### OpenAPI Specification

**Structure:**

- API metadata (title, version, description)
- Server definitions
- Security schemes
- Paths and operations
- Request/response schemas
- Examples for all operations

**Example:**

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for user management

paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

### SDK Generation

**Supported Languages:**

- JavaScript/TypeScript
- Python
- Java
- Go
- Ruby
- PHP

**Tools:**

- OpenAPI Generator
- Swagger Codegen
- SDK generators

### Code Examples

Provide examples in multiple languages:

- JavaScript/Node.js
- Python
- cURL
- Ruby
- Java

## Technical Writing

### Write for Your Audience

- Know their skill level
- Use appropriate terminology
- Provide context when needed
- Assume minimal prior knowledge
- Include troubleshooting sections

### Lead with the Outcome

- Start with what users will accomplish
- Show the value before the steps
- Use clear, action-oriented language
- Focus on user success, not features

### Use Active Voice

- Prefer active over passive voice
- Use clear, concise language
- Avoid jargon when possible
- Include real examples and scenarios
- Test instructions by following them exactly

### Documentation Types

**User Guides:**

- Overview and goals
- Prerequisites
- Step-by-step instructions
- Screenshots or examples
- Troubleshooting
- Next steps

**README Files:**

- Project title and description
- Badges (build status, version, license)
- Features
- Installation
- Quick start
- Usage examples
- Contributing
- License

**Architecture Docs:**

- System overview
- Component diagrams
- Design decisions
- Technology choices
- Integration points
- Data flow

## Changelog Generation

### Transforming Git Commits

Automatically creates user-facing changelogs from git commits by:

- Analyzing commit history
- Categorizing changes (features, improvements, bug fixes, breaking changes, security)
- Transforming technical commits into clear, customer-friendly release notes
- Filtering out internal commits (refactoring, tests, etc.)

### Basic Usage

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using my changelog
guidelines from CHANGELOG_STYLE.md
```

### Example Output

```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts.
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

## Reference Files

For detailed documentation patterns and guidance, load reference files as needed:

- **`references/api_docs.md`** - API documentation patterns, OpenAPI specifications, SDK generation, versioning strategies, and code examples
- **`references/technical_writing.md`** - Technical writing best practices, user guide structure, README templates, architecture documentation, and content organization
- **`references/changelogs.md`** - Changelog generation patterns, commit categorization, user-friendly transformation, and release note best practices
- **`references/API_DOCUMENTATION.template.md`** - REST API documentation template with endpoints, authentication, webhooks, and SDK examples
- **`references/CHANGELOG.template.md`** - Changelog template following Keep a Changelog format with SemVer
- **`references/DESIGN_SPEC.template.md`** - Design specification template for feature planning, technical design, and implementation approach
- **`references/ARCHITECTURE_DECISION_RECORD.template.md`** - ADR template for documenting significant architectural decisions with context and consequences
- **`references/MIGRATION_GUIDE.template.md`** - Migration guide template for version upgrades, breaking changes, and upgrade paths

When working on specific documentation types, load the appropriate reference file.

## Best Practices

### Documentation Quality

1. **Real Examples**: Use actual working examples, not placeholders
2. **Error Cases**: Document error responses with examples
3. **Authentication**: Clear authentication setup instructions
4. **Versioning**: Document versioning strategy and migration paths
5. **Testing**: Test all examples to ensure they work

### Developer Experience

- **Quick Start**: Provide 5-minute quick start guide
- **Interactive**: Use tools like Postman or Swagger UI
- **Searchable**: Make documentation searchable
- **Up-to-Date**: Keep documentation current with API changes
- **Feedback**: Include ways for developers to provide feedback

### Writing Guidelines

1. **Clarity**: Use simple, clear language
2. **Structure**: Organize with clear headings
3. **Examples**: Include real, working examples
4. **Testing**: Test all instructions yourself
5. **Feedback**: Include ways for users to provide feedback

### Content Organization

- **Hierarchy**: Use clear heading structure
- **Navigation**: Include table of contents for long docs
- **Search**: Make content searchable
- **Cross-references**: Link related sections
- **Updates**: Keep documentation current

### Accessibility

- **Plain Language**: Avoid unnecessary jargon
- **Structure**: Use semantic HTML/Markdown
- **Images**: Include alt text for images
- **Formatting**: Use consistent formatting
- **Examples**: Provide multiple examples for different skill levels

### Changelog Best Practices

- Run from git repository root
- Specify date ranges for focused changelogs
- Use CHANGELOG_STYLE.md for consistent formatting
- Review and adjust the generated changelog before publishing
- Save output directly to CHANGELOG.md

## Related Use Cases

- API specification creation
- SDK generation
- Developer onboarding
- API integration guides
- Version migration documentation
- Interactive API exploration
- User documentation
- Developer guides
- Architecture documentation
- Tutorial creation
- Content improvement
- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
