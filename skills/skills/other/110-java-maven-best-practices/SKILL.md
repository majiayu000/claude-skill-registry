---
name: 110-java-maven-best-practices
description: Use when you need to review, improve, or troubleshoot a Maven pom.xml file — including dependency management with BOMs, plugin configuration, version centralization, multi-module project structure, build profiles, or any situation where you want to align your Maven setup with industry best practices. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Maven Best Practices

Improve Maven POM configuration using industry-standard best practices.

**Core areas:** Dependency management via `<dependencyManagement>` and BOMs, standard directory layout (`src/main/java`, `src/test/java`), centralized plugin management, build profiles for environment-specific settings, readable POM structure with version properties, explicit repository declaration, version centralization, multi-module project structure with proper inheritance, and cross-module version consistency.

**Prerequisites:** Run `./mvnw validate` or `mvn validate` before applying recommendations. If validation fails, **stop** and ask the user to fix issues—do not proceed until resolved.

**Multi-module scope:** After reading the root `pom.xml`, check for a `<modules>` section. If present, read **every** child module's `pom.xml` before making any recommendations. Check each child for hardcoded versions that duplicate parent `<dependencyManagement>`, redundant `<pluginManagement>` blocks, properties that should be centralized, and version drift across sibling modules.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/110-java-maven-best-practices.md](references/110-java-maven-best-practices.md).
