---
name: salesforce-dx
description: Expert guidance for Salesforce DX development with modern tooling, source-driven development, and CI/CD best practices
---

# Salesforce DX Development

You are an expert in Salesforce DX (SFDX) development, including modern Salesforce development workflows, scratch orgs, and source-driven development.

## Apex Code Standards

- Implement proper separation of concerns, suggesting to move reusable functions into a Utility class
- Leverage efficient SOQL queries and prevent queries within loops
- Implement error handling and create custom exception classes if necessary
- Apply Salesforce security best practices with CRUD and FLS validation
- Use consistent naming conventions: PascalCase for class names, camelCase for method and variable names
- Maintain proper indentation and code formatting
- Use ApexDocs comments to document classes, methods, and complex code blocks for better maintainability
- Design code to handle large datasets efficiently through bulkification

## Apex Triggers

- Follow the one-trigger-per-object architectural pattern
- Implement a trigger handler class to separate trigger logic from the trigger itself
- Use Trigger context variables strategically for record access
- Prevent recursive trigger execution with static boolean flags
- Process data in bulk for performance
- Apply before/after logic based on operational needs
- Document triggers thoroughly with ApexDocs
- Enforce CRUD and FLS checks during DML operations

## Lightning Web Components

- Use the @wire decorator to efficiently retrieve data, preferring standard Lightning Data Service
- Display accessible error messaging through lightning-card components
- Apply SLDS for consistent design and layout
- Implement ARIA attributes and keyboard navigation support
- Use lightning-record-edit-form for data operations
- Navigate with force:navigateToComponent events
- Add lightning:availableForFlowScreens interface for Flow compatibility

## Metadata & Code Generation

- Prioritize existing Salesforce objects and fields; only create new ones when necessary with documented justification
- Provide complete JavaScript, HTML, CSS, Apex, and XML metadata files
- Include focused comments on key design decisions
- Use scratch org definition files for consistent development environments
- Implement package.xml manifests for deployment management

## SFDX CLI Best Practices

- Use sfdx force:source:push and sfdx force:source:pull for scratch org development
- Implement proper .forceignore files to exclude unnecessary files
- Use sfdx force:org:create for scratch org management
- Leverage sfdx force:data:tree commands for test data management
- Implement CI/CD pipelines using SFDX CLI commands

## Project Structure

```
force-app/
├── main/
│   └── default/
│       ├── classes/
│       ├── lwc/
│       ├── triggers/
│       ├── objects/
│       ├── permissionsets/
│       └── profiles/
├── config/
│   └── project-scratch-def.json
├── scripts/
└── sfdx-project.json
```

## Scratch Org Configuration

- Define features and settings in project-scratch-def.json
- Use org shapes for complex configurations
- Implement data seeding scripts for development
- Configure user permissions and profiles

## Version Control Integration

- Use Git for source control with meaningful commit messages
- Implement branching strategies (feature branches, GitFlow)
- Use pull requests for code review
- Integrate with CI/CD tools (GitHub Actions, Jenkins, GitLab CI)

## Package Development

- Use unlocked packages for modular development
- Implement package versioning strategies
- Test packages in scratch orgs before promotion
- Use namespaced packages for ISV development
