---
name: cui-javascript-linting
description: ESLint, Prettier, and StyleLint configuration standards for JavaScript code quality and formatting, including flat config setup, rule management, and build integration
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JavaScript Linting and Formatting Standards

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

## Overview

This skill provides comprehensive ESLint, Prettier, and StyleLint configuration standards for CUI JavaScript projects, covering modern ESLint v9 flat configuration, Prettier formatting automation, comprehensive rule management, build integration, and CSS-in-JS linting for web components.

## Prerequisites

To effectively use this skill, you should have:

- Understanding of ESLint and code quality tools
- Knowledge of JavaScript ES2022+ features
- Familiarity with npm package management
- Experience with build pipelines (Maven, npm scripts)

## Standards Documents

This skill includes the following standards documents:

- **eslint-configuration.md** - ESLint v9 flat config structure, required dependencies, environment configuration, plugin setup
- **eslint-rules.md** - Comprehensive rule definitions including documentation, security, code quality, and environment-specific overrides
- **eslint-integration.md** - Build pipeline integration, Maven configuration, npm scripts, CI/CD requirements
- **prettier-configuration.md** - Prettier setup, formatting rules, editor integration, pre-commit hooks, Maven integration
- **stylelint-setup.md** - StyleLint configuration for CSS-in-JS patterns in web components

## What This Skill Provides

### ESLint Configuration
- **Flat Configuration**: ESLint v9+ flat config structure with ES modules
- **Required Dependencies**: Core ESLint packages and essential plugins
- **Plugin Management**: JSDoc, Jest, SonarJS, Security, Unicorn, Promise, Prettier plugins
- **Environment Setup**: Browser, Node.js, Jest environment configuration
- **Framework Extensions**: Lit and Web Components specific configurations

### ESLint Rules
- **Documentation Rules**: JSDoc validation and documentation quality standards
- **Security Rules**: Vulnerability detection and security best practices
- **Code Quality Rules**: SonarJS complexity analysis and maintainability checks
- **Modern JavaScript Rules**: ES6+ patterns, async/await, Promise handling
- **Framework-Specific Rules**: Lit components and Web Components validation
- **Environment Overrides**: Test files, production components, mock files

### Build Integration
- **npm Scripts**: Required lint and lint:fix commands
- **Maven Integration**: Build phase configuration and execution
- **CI/CD Pipeline**: Quality gate integration and automation
- **Error Handling**: Severity levels and common fix strategies
- **Performance**: Caching and rule selection optimization

### Prettier Configuration
- **Code Formatting**: Prettier configuration for consistent code style
- **Formatting Rules**: Line length, quotes, semicolons, trailing commas, spacing
- **File-Specific Overrides**: Different settings for production vs test files
- **Format Scripts**: format, format:check, quality, quality:fix npm scripts
- **Editor Integration**: VS Code, IntelliJ setup with format-on-save
- **Pre-commit Hooks**: Husky and lint-staged configuration
- **ESLint Integration**: Prettier as ESLint plugin for unified workflow

### StyleLint Configuration
- **CSS-in-JS Linting**: StyleLint for CSS within JavaScript/Lit components
- **Plugin Setup**: postcss-lit, stylelint-order, declaration-strict-value
- **Rule Configuration**: Property ordering, custom properties, web component selectors
- **Environment Overrides**: Production vs test file configurations
- **Build Integration**: npm scripts and Maven execution

## When to Activate

This skill should be activated when:

1. **Setting Up ESLint**: Configuring ESLint for new or existing JavaScript projects
2. **Upgrading ESLint**: Migrating from legacy ESLint configuration to v9 flat config
3. **Configuring Linting Rules**: Adding, modifying, or understanding ESLint rules
4. **Setting Up Prettier**: Configuring code formatting automation and editor integration
5. **Build Integration**: Integrating linting and formatting into Maven builds or CI/CD pipelines
6. **CSS-in-JS Linting**: Setting up StyleLint for Lit components or CSS-in-JS patterns
7. **Code Quality Issues**: Resolving linting errors or configuring rule severity
8. **Format-on-Save**: Configuring editors for automatic formatting
9. **Framework-Specific Linting**: Adding Lit or Web Components specific rules
10. **Troubleshooting**: Debugging ESLint, Prettier, or StyleLint configuration issues

## Workflow

When this skill is activated:

### 1. Identify Linting Requirement
- Determine if setting up new configuration or modifying existing
- Identify specific linting concern (configuration, rules, integration, CSS-in-JS)
- Check current ESLint/StyleLint version and configuration format

### 2. Apply Configuration Standards
- Use **eslint-configuration.md** for flat config structure and dependencies
- Configure plugins (JSDoc, Jest, SonarJS, Security, Unicorn, Promise, Prettier)
- Set up environment configuration (browser, Node.js, Jest)
- Add framework-specific plugins if using Lit or Web Components

### 3. Configure Rules
- Reference **eslint-rules.md** for comprehensive rule definitions
- Enable documentation rules for JSDoc validation
- Configure security rules for vulnerability detection
- Set up SonarJS for complexity and quality analysis
- Add framework-specific rules for Lit/Web Components if needed
- Configure environment overrides for test files, mocks, production code

### 4. Configure Prettier Formatting
- Use **prettier-configuration.md** for Prettier setup
- Create `.prettierrc.js` with formatting rules
- Configure file-specific overrides (production vs test)
- Add format scripts (format, format:check, quality, quality:fix)
- Set up editor integration (VS Code, IntelliJ) for format-on-save
- Configure pre-commit hooks with Husky and lint-staged
- Integrate Prettier as ESLint plugin

### 5. Integrate with Build Pipeline
- Use **eslint-integration.md** for build integration
- Add npm scripts (lint:js, lint:js:fix, format, format:check, quality, quality:fix)
- Configure Maven execution: format:check in compile, quality:fix in verify
- Set up CI/CD quality gates
- Enable caching for performance

### 6. Configure CSS-in-JS Linting (Optional)
- Use **stylelint-setup.md** if using CSS-in-JS or Lit components
- Install StyleLint dependencies (stylelint, stylelint-config-standard, postcss-lit)
- Configure StyleLint with ES module syntax
- Add CSS property ordering and custom property validation
- Integrate StyleLint into build pipeline

### 7. Validate Configuration
- Run lint and format commands to verify configuration works
- Check for rule conflicts or duplicate definitions
- Test environment-specific overrides
- Verify build integration executes correctly
- Test format-on-save in editors

## Tool Access

This skill provides access to linting standards through:
- Read tool for accessing standards documents
- Standards documents use Markdown format for compatibility
- All standards are self-contained within this skill
- Cross-references between standards use relative paths

## Integration Notes

### Related Skills
For comprehensive frontend development, this skill works with:
- **cui-javascript** skill - Core JavaScript development standards
- **cui-jsdoc** skill - JSDoc documentation standards
- **cui-javascript-unit-testing** skill - Testing standards
- **cui-css** skill - CSS development standards

### Build Integration
Linting standards integrate with:
- npm for package management and script execution
- ESLint for JavaScript linting and code quality
- StyleLint for CSS-in-JS linting
- Prettier for code formatting
- Maven frontend-maven-plugin for build automation
- SonarQube for quality analysis

### Quality Tools
Code quality is enforced through:
- ESLint with multiple quality plugins (SonarJS, Security, Unicorn)
- StyleLint for CSS validation
- Prettier for consistent formatting
- Maven build pipeline integration
- CI/CD quality gates

## Best Practices

When configuring linting and formatting for CUI projects:

1. **Use ESLint v9 flat configuration** - Modern configuration format with ES modules
2. **Include all required plugins** - JSDoc, Jest, SonarJS, Security, Unicorn, Promise, Prettier
3. **Configure Prettier integration** - Prettier as ESLint plugin for unified workflow
4. **Enable format-on-save** - Automatic formatting in editors (VS Code, IntelliJ)
5. **Configure environment-specific overrides** - Relaxed rules for tests, strict for production
6. **Enable SonarJS recommended defaults** - Comprehensive quality and complexity analysis
7. **Integrate with build pipeline** - format:check in compile, quality:fix in verify
8. **Use StyleLint for CSS-in-JS** - When using Lit components or CSS-in-JS patterns
9. **Set up pre-commit hooks** - Husky and lint-staged for automatic fixing before commit
10. **Enable caching** - For faster subsequent lint runs
11. **Run quality:fix before commits** - Automatic fixing of linting and formatting issues
12. **Configure proper severity levels** - Error for breaking issues, warn for improvements
13. **Document exceptions** - Use comments to explain any rule or format overrides

## Common Issues and Solutions

### ESLint Configuration Issues
- **Duplicate rule definitions**: Remove duplicates, keep one instance per rule
- **Plugin import errors**: Ensure all plugins are installed as devDependencies
- **ES module errors**: Set `"type": "module"` in package.json for flat config
- **Environment conflicts**: Use environment-specific overrides in configuration

### Prettier Configuration Issues
- **Format not applying**: Verify .prettierrc.js exists and editor extension installed
- **Conflicts with ESLint**: Disable conflicting ESLint style rules (quotes, semi, indent, etc.)
- **Format-on-save not working**: Check editor settings and Prettier extension configuration
- **ES module errors**: Set `"type": "module"` in package.json

### StyleLint Configuration Issues
- **Duplicate rule names**: Check for duplicate property-* rules in configuration
- **Framework-specific patterns**: Use generic patterns unless specific integration required
- **ES module import errors**: Use `export default` syntax with `"type": "module"`
- **CSS-in-JS syntax errors**: Ensure postcss-lit is configured as customSyntax

### Build Integration Issues
- **Maven execution fails**: Verify npm scripts exist and dependencies are installed
- **Lint errors block build**: Adjust severity levels or fix violations
- **Performance issues**: Enable caching, reduce file scope, parallelize execution
- **CI/CD failures**: Ensure lint:fix runs in verify phase, not validate phase

## Quick Reference

### ESLint Flat Config Structure
```javascript
import js from '@eslint/js';
import jsdoc from 'eslint-plugin-jsdoc';

export default [
  js.configs.recommended,
  {
    plugins: { jsdoc },
    rules: { /* rule configuration */ }
  }
];
```

### Required npm Scripts
```json
{
  "scripts": {
    "lint:js": "eslint src/**/*.js",
    "lint:js:fix": "eslint --fix src/**/*.js",
    "format": "prettier --write \"src/**/*.js\"",
    "format:check": "prettier --check \"src/**/*.js\"",
    "lint:style": "stylelint src/**/*.js",
    "lint:style:fix": "stylelint --fix src/**/*.js",
    "quality": "npm run lint && npm run format:check",
    "quality:fix": "npm run lint:fix && npm run format"
  }
}
```

### Maven Integration
```xml
<execution>
  <id>npm-lint-fix</id>
  <goals><goal>npm</goal></goals>
  <phase>verify</phase>
  <configuration>
    <arguments>run lint:fix</arguments>
  </configuration>
</execution>
```
