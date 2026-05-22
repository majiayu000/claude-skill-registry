---
name: feature-documentation
description: Эксперт feature documentation. Используй для документации функций, release notes, user guides и product documentation.
---

# Feature Documentation Expert

Expert in creating comprehensive, user-focused feature documentation.

## Core Documentation Principles

### Structure and Hierarchy
- **Purpose-First Organization**: Start with what the feature does and why it matters
- **Progressive Disclosure**: Layer information from overview to implementation details
- **Multiple Entry Points**: Support different user types (end-users, developers, stakeholders)
- **Cross-Reference Integration**: Link related features, dependencies, and prerequisites

### Content Framework
```markdown
# Feature Name

## Overview
- **Purpose**: What problem does this solve?
- **Target Users**: Who benefits from this feature?
- **Key Benefits**: Primary value propositions

## How It Works
- **Core Functionality**: Technical behavior description
- **User Flow**: Step-by-step interaction patterns
- **System Integration**: How it connects with existing features

## Implementation
- **Technical Requirements**: Dependencies, versions, constraints
- **Configuration**: Setup and customization options
- **Code Examples**: Practical usage demonstrations

## Reference
- **Parameters**: Complete specification details
- **Error Handling**: Common issues and solutions
- **Performance**: Limitations, optimization tips
```

## User-Centric Documentation Patterns

### Scenario-Based Examples
```markdown
## Use Cases

### Scenario 1: E-commerce Product Search
**Context**: Customer searching for specific product attributes
**Steps**:
1. User enters search query
2. Feature parses attributes
3. Returns filtered results with relevance scoring

**Expected Outcome**: Highly relevant products displayed
```

### Task-Oriented Structure
- **Quick Start**: Get users to first success in under 5 minutes
- **Common Tasks**: Address 80% of typical use cases
- **Advanced Usage**: Power user scenarios and customization
- **Troubleshooting**: Anticipated problems with specific solutions

## Technical Implementation Documentation

### API Documentation Standards
```yaml
paths:
  /api/v1/search:
    post:
      summary: Advanced product search with filtering
      description: |
        Performs intelligent search across product catalog
        **Rate Limits**: 100 requests/minute per API key
        **Response Time**: Typically < 200ms
```

## Cross-Functional Communication

### Stakeholder Summary Template
```markdown
## Executive Summary: Feature Name

**Business Impact**: Key metrics improvements
**Development Effort**: Timeline estimate
**Dependencies**: Required resources
**Success Metrics**: How we measure success
**Risks & Mitigations**: Potential issues and solutions
```

### Release Notes Format
```markdown
## New Feature: Feature Name v2.1

**What's New**: List of new capabilities
**For Developers**: Code examples
**Breaking Changes**: Migration requirements
```

## Quality Assurance Practices

### Documentation Review Checklist
- [ ] All code examples tested and functional
- [ ] Covers happy path, edge cases, and error scenarios
- [ ] Technical and non-technical users can understand
- [ ] Version-specific information clearly marked
- [ ] Proper heading structure, alt text for images
