---
name: cui-javascript-project
description: JavaScript project structure, package.json configuration, dependency management, and Maven integration standards for consistent project setup and builds
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(python3:*)
---

# JavaScript Project Structure and Build Standards

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

## Overview

This skill provides comprehensive standards for JavaScript project setup, structure, dependencies, and Maven integration in CUI projects. It covers directory layouts, package.json configuration, semantic versioning strategies, security management, ES module configuration, and frontend-maven-plugin integration for reproducible builds.

## Prerequisites

To effectively use this skill, you should have:

- Understanding of npm package management
- Knowledge of Maven build lifecycle
- Familiarity with project structure conventions
- Experience with Node.js development

## Standards Documents

This skill includes the following standards documents:

- **project-structure.md** - Directory layouts, file naming conventions, package.json structure, git ignore requirements
- **dependency-management.md** - Semantic versioning, security management, dependency updates, conflict resolution, ES module configuration
- **maven-integration.md** - Frontend Maven Plugin configuration, Maven phase integration, SonarQube integration, build environment standards

## What This Skill Provides

### Project Structure Standards
- **Directory Layouts**: Standard Maven, Quarkus DevUI, NiFi extension, standalone project structures
- **File Naming**: Kebab-case conventions, framework-specific prefixes (qwc-, nf-)
- **Package.json Configuration**: Essential structure, required fields, npm scripts
- **Configuration Files**: Location and naming for ESLint, Prettier, Jest, etc.
- **Git Ignore Requirements**: Essential exclusions for Node.js and Maven artifacts

### Dependency Management
- **Semantic Versioning**: Caret ranges vs exact versions, version update strategies
- **Security Management**: Vulnerability scanning, response timeframes, resolution strategies
- **Deprecated Packages**: Common replacements, handling deprecation warnings
- **Dependency Conflicts**: Peer dependency resolution, npm overrides
- **ES Module Configuration**: "type": "module" setup, configuration file syntax requirements
- **Update Management**: Regular update schedules, breaking change handling

### Maven Integration
- **Frontend Maven Plugin**: Required plugin setup, configuration parameters
- **Phase Integration**: Mapping npm scripts to Maven lifecycle phases
- **Node.js Management**: Version management, installation directory strategies
- **Script Integration**: Required npm scripts, execution order
- **SonarQube Integration**: Coverage reporting, quality gate configuration
- **Build Environment**: Reproducible builds, CI/CD integration
- **Project Adaptations**: Configuration for different project types

## When to Activate

This skill should be activated when:

1. **Setting Up New Project**: Creating new JavaScript project with Maven integration
2. **Configuring Project Structure**: Establishing directory layout and file organization
3. **Managing Dependencies**: Adding, updating, or resolving dependency issues
4. **Security Issues**: Addressing npm vulnerabilities or deprecated packages
5. **Maven Integration**: Configuring frontend-maven-plugin or build pipeline
6. **Build Issues**: Troubleshooting Maven/npm integration problems
7. **Updating Node.js**: Changing Node.js or npm versions
8. **SonarQube Setup**: Configuring JavaScript coverage analysis
9. **Project Type Adaptation**: Adapting structure for Quarkus, NiFi, or multi-module projects
10. **Best Practice Review**: Ensuring project follows CUI standards

## Workflow

When this skill is activated:

### 1. Identify Project Requirement
- Determine if new project setup or modification to existing
- Identify specific concern (structure, dependencies, Maven, security)
- Check current project type (Maven, Quarkus DevUI, NiFi, standalone)

### 2. Apply Project Structure Standards
- Use **project-structure.md** for directory layout selection
- Choose appropriate structure for project type
- Configure package.json with required fields and scripts
- Set up configuration files (.prettierrc.js, eslint.config.js, etc.)
- Create .gitignore with essential exclusions

### 3. Configure Dependency Management
- Reference **dependency-management.md** for version strategies
- Set up security audit scripts
- Configure semantic versioning (caret ranges for dev, exact for critical)
- Enable ES module support ("type": "module")
- Plan update management schedule

### 4. Integrate with Maven Build
- Use **maven-integration.md** for frontend-maven-plugin setup
- Configure Node.js version (see standards/project-structure.md for exact version)
- Map npm scripts to Maven phases
- Set up environment variables (CI=true, NODE_ENV=test)
- Configure SonarQube integration for JavaScript coverage

### 5. Validate Configuration
- Run Maven build to verify integration works
- Check Node.js installation in target/
- Verify npm scripts execute in correct phases
- Test dependency installation without errors
- Validate SonarQube picks up JavaScript coverage

## Tool Access

This skill provides access to project standards through:
- Read tool for accessing standards documents
- Standards documents use Markdown format for consistency
- All standards are self-contained within this skill
- Cross-references between standards use relative paths

## Integration Notes

### Related Skills
For comprehensive frontend development, this skill works with:
- **cui-javascript-linting** skill - ESLint, Prettier, and StyleLint configuration
- **cui-javascript** skill - Core JavaScript development standards
- **cui-jsdoc** skill - JSDoc documentation standards
- **cui-javascript-unit-testing** skill - Jest testing standards

### Build Integration
Project standards integrate with:
- npm for package management and script execution
- Maven for build automation via frontend-maven-plugin
- Node.js LTS for runtime environment (see standards/project-structure.md for exact version)
- SonarQube for quality analysis and coverage reporting
- Git for version control with proper .gitignore setup

### Project Types
Standards support multiple project structures:
- **Standard Maven**: src/main/resources/static/js/
- **Quarkus DevUI**: src/main/resources/dev-ui/
- **NiFi Extension**: src/main/webapp/js/
- **Standalone**: src/main/js/
- **Multi-Module**: Nested frontend module structures

## Best Practices

When setting up JavaScript projects for CUI:

1. **Follow project type conventions** - Use appropriate directory structure for Maven/Quarkus/NiFi/Standalone
2. **Use kebab-case naming** - Consistent file naming across all JavaScript files
3. **Configure "type": "module"** - Enable ES module support in package.json
4. **Commit package-lock.json** - Ensure reproducible builds across environments
5. **Never commit node_modules/** - Always gitignore dependencies
6. **Use caret ranges for dev dependencies** - Allow automatic updates within major version
7. **Use exact versions for critical deps** - Pin production dependencies with breaking change history
8. **Implement all required npm scripts** - lint, format, test, quality scripts
9. **Integrate with Maven properly** - Map scripts to correct lifecycle phases
10. **Set up security auditing** - Regular vulnerability scanning and response
11. **Use Node.js LTS** - Consistent version managed by frontend-maven-plugin (see standards/project-structure.md for exact version)
12. **Configure SonarQube coverage** - JavaScript code quality and coverage analysis
13. **Handle deprecations promptly** - Replace deprecated packages before they become critical
14. **Document project-specific setup** - Update README.md with structure and setup instructions

## Common Issues and Solutions

### Project Structure Issues
- **Wrong directory layout**: Verify project type and use correct structure pattern
- **Files not found during build**: Check package.json script paths match structure
- **Tests failing to locate sources**: Update Jest testMatch patterns for directory layout

### Dependency Management Issues
- **npm install failures**: Clear cache, delete node_modules/, regenerate package-lock.json
- **Peer dependency conflicts**: Try npm overrides before using --legacy-peer-deps
- **Security vulnerabilities**: Run npm audit fix, update vulnerable packages
- **Deprecated packages**: Identify replacements and update package.json

### Maven Integration Issues
- **Node.js installation failures**: Check internet connectivity, proxy settings, disk space
- **npm scripts not found**: Verify scripts exist in package.json
- **Build phase ordering**: Ensure validate → generate-resources → compile → test
- **Test failures in CI**: Set CI=true, use test:ci-strict script
- **SonarQube not picking up coverage**: Verify lcov.info path matches SonarQube property

### Configuration Issues
- **ES module errors**: Set "type": "module" in package.json
- **Configuration files not loading**: Ensure .prettierrc.js, eslint.config.js use export default
- **Inconsistent builds**: Commit package-lock.json, use frontend-maven-plugin for Node.js

## Quick Reference

For detailed configuration examples and complete reference, see the individual standards documents:

- **package.json structure and npm scripts** - See `project-structure.md` for complete examples
- **Directory structures by project type** - See `project-structure.md` for Maven, Quarkus, NiFi, and standalone layouts
- **Maven frontend-maven-plugin configuration** - See `maven-integration.md` for complete plugin setup
- **Semantic versioning strategies** - See `dependency-management.md` for caret ranges vs exact versions
- **Security audit setup** - See `dependency-management.md` for audit scripts and vulnerability handling
- **Git ignore patterns** - See `project-structure.md` for essential .gitignore configuration

### Key Requirements Summary

- **Node.js Version**: See `project-structure.md` for version requirements (managed by frontend-maven-plugin)
- **Package.json**: Must include `"type": "module"` for ES module support
- **Required npm scripts**: lint, format, test, test:ci-strict, quality
- **Maven Integration**: Map npm scripts to validate/compile/test phases
- **Security**: Implement audit scripts and respond to vulnerabilities within 30 days
- **Version Control**: Always commit package-lock.json, never commit node_modules/

## Workflows

### Workflow: npm Build Execution and Parsing

For npm/npx build execution and output parsing, use the **builder-npm-rules** skill:

```
Skill: pm-dev-builder:builder-npm-rules
```

The builder-npm-rules skill provides:
- **Execute npm Build** workflow - Atomic build execution with log capture
- **Parse npm Build Output** workflow - Issue categorization and routing

**When to use builder-npm-rules**:
- Running npm/npx builds (test, lint, build, etc.)
- Parsing npm build output for errors and warnings
- Categorizing build issues for orchestrated fixing
- Workspace-targeted builds in monorepos

**Example usage**:
```
Skill: pm-dev-builder:builder-npm-rules
Workflow: Execute npm Build
Parameters:
  command: run test
  workspace: e-2-e-playwright
  output_mode: structured
```

See builder-npm-rules skill documentation for complete workflow details.

---

## Scripts

Script: `pm-dev-frontend:cui-javascript-project` → `npm-output.py`

| Subcommand | Description |
|------------|-------------|
| `parse` | Parse npm/npx build output logs and categorize issues |

Script characteristics:
- Uses Python stdlib only (json, argparse, re, pathlib)
- Outputs JSON to stdout
- Exit code 0 for success, 1 for errors
- Supports `--help` flag
