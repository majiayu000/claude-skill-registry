---
name: 113-java-maven-documentation
description: Use when you need to create a DEVELOPER.md file for a Maven project — combining a fixed base template with dynamic sections derived from the project pom.xml, including a Plugin Goals Reference, Maven Profiles table, and Submodules table for multi-module projects.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Create DEVELOPER.md for the Maven projects

Generate a `DEVELOPER.md` file that combines a fixed base template with dynamic sections derived from analysing the project `pom.xml`.

**Core areas:** Base template reproduction (verbatim), plugin goals reference (table of `./mvnw` goals per explicitly declared plugin, max 8 goals each), Maven Profiles table (profile ID, activation trigger, representative command, description), and Submodules table (multi-module projects only).

**Prerequisites:** Read every `pom.xml` in the workspace (root and submodules) before generating any content. Only include plugins **explicitly declared** in `<build><plugins>` or `<build><pluginManagement><plugins>` — never plugins inherited from parent POMs or the Maven super-POM unless redeclared.

**Multi-step scope:** Step 1 reproduces the base template verbatim. Step 2 collects all explicitly declared plugins. Step 3 appends the Plugin Goals Reference section. Step 4 appends the Maven Profiles section (omit if no profiles). Step 5 appends the Submodules section (omit if not a multi-module project).

**Before applying changes:** Read the reference for the base template content, plugin catalog, and detailed constraints for each step.

## Reference

For detailed guidance, examples, and constraints, see [references/113-java-maven-documentation.md](references/113-java-maven-documentation.md).
