---
name: 110-java-maven-best-practices
description: Use when you need to improve your Maven pom.xml using best practices
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Maven Best Practices

Improve Maven POM configuration using industry-standard best practices.

**Core areas:** Dependency management via `<dependencyManagement>` and BOMs, standard directory layout (`src/main/java`, `src/test/java`), centralized plugin management, build profiles for environment-specific settings, readable POM structure with version properties, explicit repository declaration, and version centralization.

**Prerequisites:** Run `mvn validate` before applying recommendations. If validation fails, **stop** and ask the user to fix issues—do not proceed until resolved.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/110-java-maven-best-practices.md](references/110-java-maven-best-practices.md).
