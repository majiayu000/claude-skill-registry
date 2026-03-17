---
name: tech-documentation
description: Technical documentation writing skill covering API docs, architecture documentation, deployment guides, and various technical writing best practices. Use this skill when creating technical documentation, writing API documentation, creating architecture design documents, or need templates for deployment and operations manuals.
---

# Tech Documentation Skill

Technical documentation writing expertise, providing comprehensive methodology and templates for producing high-quality technical documentation.

## Overview

This is a comprehensive skill module focused on technical documentation writing, covering standards, templates, and best practices for various types of technical documentation to help teams produce high-quality, easy-to-understand, and maintainable documentation.

## Core Capabilities

### 1. API Documentation
- **OpenAPI/Swagger Specifications**
- **RESTful API Documentation**
- **GraphQL Documentation**
- **gRPC Interface Documentation**
- **API Change Logs**
- **Authentication and Authorization Documentation**

### 2. Architecture Documentation
- **Architecture Design Documents (ADD)**
- **Architecture Decision Records (ADR)**
- **System Architecture Diagrams** (C4 Model, UML)
- **Technology Selection Reports**
- **Architecture Evolution Roadmaps**

### 3. Detailed Design Documents
- **Module Design Documents**
- **Database Design Documents**
- **Interface Design Documents**
- **Algorithm Design Specifications**
- **Sequence Diagrams/Flowcharts**

### 4. Deployment and Operations Documentation
- **Deployment Manuals**
- **Operations Manuals**
- **Incident Response Manuals**
- **Monitoring and Alerting Configuration**
- **Performance Optimization Guides**
- **Backup and Recovery Procedures**

### 5. User Manuals
- **Product User Manuals**
- **Quick Start Guides**
- **Frequently Asked Questions (FAQ)**
- **Troubleshooting Guides**
- **Best Practices**

### 6. Developer Documentation
- **Contributing Guidelines** (CONTRIBUTING.md)
- **Coding Standards**
- **Development Environment Setup**
- **Testing Guides**
- **Release Processes**

### 7. Project Management Documentation
- **Project Plans**
- **Requirements Documents**
- **Test Plans**
- **Release Notes**
- **Change Logs** (CHANGELOG)

### 8. Knowledge Base Documentation
- **Technical Blog Posts**
- **Case Studies**
- **Problem Summaries**
- **Learning Notes**

## Documentation Principles

### 1. The 5C Principles
- **Clear**: Concise language, clear logic
- **Concise**: Avoid redundancy, get to the point
- **Complete**: Comprehensive information covering all needs
- **Correct**: Accurate content, verified and tested
- **Consistent**: Unified style, standardized terminology

### 2. Audience-Oriented
- Understand target audience (developers, operations, product, users)
- Use language and concepts familiar to the audience
- Provide information at different levels (overview → detailed)
- Include practical examples and best practices

### 3. Structured Organization
- Clear hierarchical structure
- Unified format and style
- Table of contents and navigation
- Cross-references

### 4. Maintainability
- Version control
- Change records
- Regular review and updates
- Feedback mechanisms

## Documentation Templates

> **API Documentation Template** (OpenAPI format, endpoints, error codes, changelog): see [references/api-doc-template.md](references/api-doc-template.md)

> **Architecture Design Document Template** (overview, requirements, architecture, tech stack, data, deployment): see [references/architecture-template.md](references/architecture-template.md)

> **Deployment Documentation Template** (environment, prerequisites, deployment steps, rollback, monitoring): see [references/deployment-template.md](references/deployment-template.md)

## Use Cases

### New Project Launch
```
Create complete documentation system for new project:
- README.md
- API documentation
- Architecture design document
- Deployment documentation
- Contributing guidelines
```

### API Design Review
```
Write API design documentation, including:
- Interface definitions
- Data models
- Error handling
- Security authentication
```

### System Delivery
```
Prepare system delivery documentation package:
- System architecture documentation
- Deployment and operations manual
- User manual
- Incident response manual
```

### Knowledge Management
```
Technical solution summary:
- Problem analysis
- Solutions
- Technical decisions
- Lessons learned
```

## Integration Examples

### Using in Agent
```json
{
  "agent": "tech-writer",
  "skills": [
    "tech-documentation",
    "system-architecture",
    "api-design"
  ]
}
```

### Referencing in Conversation
```
@tech-documentation Please create complete documentation for this API
```

## Documentation Quality Checklist

### Content Quality
- [ ] Information is accurate and complete
- [ ] Logic is clear and coherent
- [ ] Examples are realistic and usable
- [ ] Terminology is consistent and standardized

### Readability
- [ ] Language is concise and clear
- [ ] Structure is well-organized
- [ ] Formatting is unified and attractive
- [ ] Diagrams are clear and easy to understand

### Maintainability
- [ ] Version information is clear
- [ ] Change records are complete
- [ ] Contact information is accurate
- [ ] Regular review and updates

### Accessibility
- [ ] Table of contents navigation is clear
- [ ] Search functionality is complete
- [ ] Links are valid and accurate
- [ ] Multiple formats are supported

## Recommended Tools

### Documentation Writing
- **Markdown Editors**: Typora, VS Code
- **API Documentation**: Swagger Editor, Postman
- **Diagram Tools**: Draw.io, PlantUML, Mermaid
- **Screenshot Tools**: Snipaste, Xnip

### Documentation Hosting
- **Static Sites**: GitBook, Docusaurus, VuePress
- **Team Collaboration**: Confluence, Notion
- **Version Control**: Git, GitHub/GitLab

### Documentation Generation
- **API Documentation**: Swagger/OpenAPI, ApiDoc
- **Code Documentation**: JavaDoc, JSDoc, Sphinx
- **README Generation**: readme-md-generator

## Learning Resources

### Recommended Books
- "Technical Writing: A Practical Guide"
- "Docs for Developers"
- "The Documentation Compendium"

### Online Resources
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/style-guide/)
- [Write the Docs](https://www.writethedocs.org/)

---

**Version**: 1.0.0
**Last Updated**: December 2024
**Maintainer**: MindForge Team
