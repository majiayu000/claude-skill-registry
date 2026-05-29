---
name: 110-java-maven-best-practices
description: Use when you need to review, improve, or troubleshoot a Maven pom.xml file — including dependency management with BOMs, plugin configuration, version centralization, multi-module project structure, build profiles, or any situation where you want to align your Maven setup with industry best practices. This should trigger for requests such as Review pom.xml to improve it; Apply Maven best practices to pom.xml; Improve Maven POM configuration. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Maven Best Practices

Improve Maven POM configuration using industry-standard best practices.

**What is covered in this Skill?**

- Dependency management via `<dependencyManagement>` and BOMs
- Standard directory layout (`src/main/java`, `src/test/java`)
- Centralized plugin management
- Build profiles for environment-specific settings
- Readable POM structure with version properties
- Explicit repository declaration
- Version centralization
- Multi-module project structure with proper inheritance
- Cross-module version consistency
- Multi-module scope: After reading the root `pom.xml`, check for a `<modules>` section. If present, read **every** child module's `pom.xml` before making any recommendations.
- Check each child for hardcoded versions that duplicate parent `<dependencyManagement>`, redundant `<pluginManagement>` blocks, properties that should be centralized, and version drift across sibling modules.

## Constraints

Before applying Maven best practices recommendations, ensure the project is in a valid state by running Maven validation. This helps identify any existing configuration issues that need to be resolved first. For multi-module projects, scope analysis must cover every child module POM — not just the root.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any Maven best practices recommendations
- **VERIFY**: Ensure all validation errors are resolved before proceeding with POM modifications
- **SAFETY**: If validation fails, do not continue and ask the user to fix the issues before continuing
- **MULTI-MODULE DISCOVERY**: After reading the root `pom.xml`, check whether it contains a `<modules>` section. If it does, read every child module's `pom.xml` before making any recommendations — analysis scope is the full module tree, not only the root
- **CROSS-MODULE SCOPE**: When child modules exist, check each one for: hardcoded dependency versions that duplicate `<dependencyManagement>` in the parent, plugin configurations that duplicate `<pluginManagement>`, properties that should be centralized in the parent, and version drift (same artifact declared at different versions across sibling modules)
- **BEFORE APPLYING**: Read the reference for detailed examples, good/bad patterns, and constraints

## When to use this skill

- Review pom.xml to improve it
- Apply Maven best practices to pom.xml
- Improve Maven POM configuration

## Workflow

1. **Validate project before recommendations**

Run `./mvnw validate` or `mvn validate` and stop if validation fails.

2. **Read reference and analyze root POM**

Read `references/110-java-maven-best-practices.md`, then inspect root `pom.xml` structure, dependency management, plugin management, properties, and profiles.

3. **Expand to full module tree when present**

If root has a `<modules>` section, read every child `pom.xml` and evaluate cross-module duplication, centralization opportunities, and version drift.

4. **Provide prioritized best-practice recommendations**

Propose concrete, safe improvements aligned with Maven best practices and full-module findings.

## Reference

For detailed guidance, examples, and constraints, see [references/110-java-maven-best-practices.md](references/110-java-maven-best-practices.md).
