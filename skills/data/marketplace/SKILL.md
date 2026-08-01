---
name: marketplace
description: Comprehensive skill for creating, managing, and maintaining Claude Code
  Marketplaces including plugin development, validation, deployment, and lifecycle
  management
---

---
name: marketplace
description: Comprehensive skill for creating, managing, and maintaining Claude Code Marketplaces including plugin development, validation, deployment, and lifecycle management
category: development
version: 1.0.0
author:
  name: Claude Code Market Specialist
  email: claude@anthropic.com
license: MIT
repository: https://github.com/anthropics/claude-code-marketplace
keywords: [marketplace, plugin, development, claude-code, deployment]

parameters:
  - name: action
    type: string
    description: The action to perform (create, validate, deploy, update, analyze)
    required: true
    validation:
      pattern: "^(create|validate|deploy|update|analyze|init|template|test|list|status)$"
      message: "Action must be one of: create, validate, deploy, update, analyze, init, template, test, list, status"

  - name: target
    type: string
    description: Target marketplace, plugin, or directory path
    required: false
    validation:
      pattern: "^[a-zA-Z0-9._/-]+$"
      message: "Target must be a valid path or identifier"

  - name: options
    type: object
    description: Configuration options for the specified action
    required: false
    default:
      verbose: false
      dry_run: false
      template: "standard"
      auto_validate: true
    properties:
      verbose:
        type: boolean
        description: Enable verbose output
      dry_run:
        type: boolean
        description: Perform actions without making changes
      template:
        type: string
        enum: ["standard", "enterprise", "community", "minimal"]
        description: Template type for creation
      auto_validate:
        type: boolean
        description: Automatically validate after creation
      skip_tests:
        type: boolean
        description: Skip test execution
      force:
        type: boolean
        description: Force action even if validation fails

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch

triggers:
  - "create a new marketplace"
  - "validate marketplace structure"
  - "deploy marketplace plugins"
  - "update marketplace configuration"
  - "analyze marketplace health"
  - "initialize marketplace project"
  - "generate marketplace template"
  - "test marketplace plugins"
  - "list marketplace contents"
  "check marketplace status"

examples:
  - input: "create a new marketplace called my-awesome-marketplace"
    output: "Created marketplace 'my-awesome-marketplace' with standard template structure and configuration"
  - input: "validate the marketplace at ./my-marketplace"
    output: "Marketplace validation completed: 0 errors, 2 warnings found"
  - input: "deploy plugins from marketplace ./my-marketplace"
    output: "Successfully deployed 3 plugins from marketplace to target environment"
  - input: "analyze marketplace health for ./my-marketplace"
    output: "Marketplace health analysis: 85% score, 2 recommendations for improvement"

requirements:
  - "Node.js 18+ for script execution"
  - "Git for version control and marketplace management"
  - "Adequate disk space for marketplace files"
  - "Write permissions for target directories"

limitations:
  - "Maximum marketplace size: 100MB"
  - "Maximum plugins per marketplace: 50"
  - "Validation timeout: 5 minutes"
  - "Concurrent operations: limited to 3"
---

# Marketplace Management Skill

## Overview

The Marketplace skill provides comprehensive capabilities for creating, managing, and maintaining Claude Code Marketplaces. This skill handles the entire lifecycle of marketplace development including initialization, plugin management, validation, deployment, and health monitoring.

## When to Use This Skill

Use this skill when you need to:

- Create new Claude Code marketplaces from templates
- Validate marketplace structure and configuration
- Deploy and manage marketplace plugins
- Update marketplace configurations and metadata
- Analyze marketplace health and performance
- Generate marketplace templates and examples
- Test marketplace functionality and compatibility
- List and inspect marketplace contents
- Monitor marketplace status and operations

## Capabilities

### Marketplace Creation

- Initialize new marketplace projects from templates
- Generate marketplace configuration files
- Create directory structures for different marketplace types
- Set up validation and testing frameworks
- Configure plugin and skill management

### Plugin Management

- Add, update, and remove plugins from marketplaces
- Validate plugin compatibility and dependencies
- Generate plugin metadata and manifests
- Manage plugin versions and releases
- Handle plugin dependencies and conflicts

### Validation and Testing

- Comprehensive marketplace structure validation
- Plugin compatibility testing
- Configuration file validation
- Dependency analysis and resolution
- Security and permission validation

### Deployment and Distribution

- Package marketplaces for distribution
- Deploy to various environments
- Manage marketplace versions and releases
- Handle marketplace updates and migrations
- Configure marketplace access and permissions

### Health Monitoring

- Analyze marketplace performance metrics
- Monitor plugin usage and compatibility
- Identify potential issues and recommendations
- Generate health reports and analytics
- Track marketplace lifecycle metrics

## Usage Examples

### Basic Marketplace Creation

```bash
"Create a new marketplace called my-awesome-marketplace"
```

### Advanced Marketplace Creation with Options

```bash
"Create an enterprise marketplace at ./enterprise-marketplace with enterprise template and verbose output"
```

### Marketplace Validation

```bash
"Validate the marketplace at ./my-marketplace with verbose output"
```

### Plugin Deployment

```bash
"Deploy plugins from marketplace ./my-marketplace to production environment"
```

### Health Analysis

```bash
"Analyze marketplace health for ./my-marketplace and generate recommendations"
```

### Template Generation

```bash
"Generate a community marketplace template at ./community-template"
```

### Testing and Validation

```bash
"Test all plugins in marketplace ./my-marketplace with comprehensive validation"
```

## Implementation Details

### Processing Pipeline

1. **Action Analysis**: Parse and validate input parameters
2. **Target Resolution**: Identify and validate target marketplace
3. **Template Selection**: Choose appropriate template based on requirements
4. **Structure Generation**: Create directory structure and configuration files
5. **Validation**: Perform comprehensive validation checks
6. **Deployment**: Handle deployment and distribution tasks
7. **Monitoring**: Generate health metrics and recommendations

### Template Types

#### Standard Template

- Basic marketplace structure
- Essential configuration files
- Standard validation rules
- Community-friendly setup

#### Enterprise Template

- Advanced security configurations
- Compliance frameworks (SOC2, ISO27001)
- Multi-team support
- Advanced monitoring and analytics

#### Community Template

- Open-source friendly configurations
- Community contribution guidelines
- Simplified validation rules
- Public distribution setup

#### Minimal Template

- Core marketplace structure only
- Essential configuration files
- Basic validation
- Lightweight setup

### Validation Framework

#### Structure Validation

- Directory structure verification
- Required file presence checks
- Naming convention compliance
- Permission validation

#### Configuration Validation

- JSON schema validation
- Plugin metadata verification
- Dependency analysis
- Security permission checks

#### Plugin Validation

- Plugin structure validation
- Command and skill verification
- MCP server configuration checks
- Compatibility testing

### Deployment Strategies

#### Local Deployment

- File system operations
- Local plugin installation
- Configuration updates
- Validation and testing

#### Remote Deployment

- Git repository management
- Remote marketplace updates
- Version control integration
- Automated deployment pipelines

## Configuration

### Default Settings

```json
{
  "template": "standard",
  "verbose": false,
  "dry_run": false,
  "auto_validate": true,
  "skip_tests": false,
  "force": false
}
```

### Template Configurations

#### Standard Template Config

```json
{
  "name": "standard-marketplace",
  "version": "1.0.0",
  "categories": ["productivity", "development"],
  "validation": "standard",
  "access": "public"
}
```

#### Enterprise Template Config

```json
{
  "name": "enterprise-marketplace",
  "version": "1.0.0",
  "categories": ["enterprise", "productivity", "development"],
  "validation": "enterprise",
  "access": "restricted",
  "compliance": ["SOC2", "ISO27001"],
  "security": "zero-trust"
}
```

## Integration

### Compatible File Formats

- JSON configuration files
- Markdown documentation
- YAML metadata files
- Shell scripts for automation

### Output Formats

- Structured JSON reports
- Markdown documentation
- HTML health reports
- CSV analytics data

### External Integrations

- Git repositories for version control
- GitHub for plugin distribution
- CI/CD pipelines for automation
- Monitoring systems for health tracking

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check file and directory permissions
2. **Invalid Template**: Verify template name and availability
3. **Validation Failures**: Review error messages and fix structural issues
4. **Deployment Errors**: Check network connectivity and target permissions
5. **Plugin Conflicts**: Resolve dependency issues and version conflicts

### Debug Information

Enable verbose output to see detailed processing information:

```bash
"Create marketplace with verbose output enabled"
```

### Error Recovery

- Use dry-run mode to preview actions
- Check validation logs for specific issues
- Review configuration files for syntax errors
- Verify template integrity and availability

## Contributing

To contribute to this skill:

1. Follow the code style guidelines in the documentation
2. Add comprehensive tests for new features
3. Update documentation and examples
4. Submit pull requests with detailed descriptions
5. Ensure all validations pass before submission

## Best Practices

### Development Guidelines

- Use appropriate templates for different use cases
- Validate marketplaces before deployment
- Monitor marketplace health regularly
- Keep documentation up to date
- Test thoroughly across different environments

### Security Considerations

- Review permissions and access controls
- Validate plugin sources and dependencies
- Implement proper authentication and authorization
- Regular security audits and updates
- Follow enterprise security standards

### Performance Optimization

- Use appropriate validation levels
- Implement caching for repeated operations
- Optimize file operations for large marketplaces
- Monitor resource usage and bottlenecks
- Implement parallel processing where applicable

## Version History

### v1.0.0 (2025-11-02)

- Initial release with comprehensive marketplace management
- Support for multiple template types
- Complete validation framework
- Deployment and health monitoring capabilities
- Extensive documentation and examples

## Support and Resources

### Documentation

- Complete user guide and API reference
- Template specifications and examples
- Best practices and troubleshooting guides
- Community contribution guidelines

### Community Resources

- GitHub repository for issues and contributions
- Community Discord server for discussions
- Stack Overflow for technical questions
- Blog posts and tutorials for learning

### Professional Support

- Enterprise support for large-scale deployments
- Consulting services for custom implementations
- Training programs for teams and organizations
- Priority support for critical issues

---

_This marketplace skill provides a comprehensive solution for Claude Code Marketplace management, supporting the entire lifecycle from creation to maintenance and monitoring._
