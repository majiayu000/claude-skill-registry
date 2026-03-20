---
name: 113-java-maven-documentation
description: Use when you need to create a DEVELOPER.md file for a Maven project — combining a fixed base template with dynamic sections derived from the project pom.xml, including a Plugin Goals Reference, Maven Profiles table, and Submodules table for multi-module projects. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Create DEVELOPER.md for the Maven projects

Generate a `DEVELOPER.md` file that combines a fixed base template with dynamic sections derived from analysing the project `pom.xml`.

**What is covered in this Skill?**

- Base template reproduction (verbatim)
- Plugin goals reference: table of `./mvnw` goals per explicitly declared plugin, max 8 goals each
- Maven Profiles table: profile ID, activation trigger, representative command, description
- Submodules table (multi-module projects only)

## Constraints

Before generating any content, read every pom.xml in the workspace. Only include plugins explicitly declared in the project POMs — never plugins inherited from parent POMs or the Maven super-POM unless redeclared.

- **MANDATORY**: Read every `pom.xml` in the workspace (root and submodules) before generating any content
- **PLUGIN SCOPE**: Only include plugins **explicitly declared** in `<build><plugins>` or `<build><pluginManagement><plugins>` — never plugins inherited from parent POMs or the Maven super-POM unless redeclared
- **SCOPE**: Execute steps 1–5 in order. Omit Profiles section if no profiles; omit Submodules section if not multi-module
- **BEFORE APPLYING**: Read the reference for the base template content, plugin catalog, and detailed constraints for each step

## When to use this skill

- Create DEVELOPER.md
- Generate DEVELOPER.md
- Maven project documentation
- Plugin goals reference
- Maven Profiles table
- Submodules table

## Reference

For detailed guidance, examples, and constraints, see [references/113-java-maven-documentation.md](references/113-java-maven-documentation.md).
