---
name: 400-frameworks-quarkus-create-project
description: Use when you need to create a new Maven-based Quarkus 3.x project using SDKMAN-managed Java and Quarkus CLI tooling. This should trigger for requests such as Create a Quarkus Maven project; Bootstrap Quarkus project with SDKMAN; Generate a new Quarkus service. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create Quarkus Maven Project

Create a new Quarkus Maven project through SDKMAN-managed tooling, aligned with Java 25 and the repository's Quarkus 3.x baseline.

**What is covered in this Skill?**

- Verify SDKMAN and Java availability before project creation
- Install or select the required Java and Quarkus CLI candidates through SDKMAN
- Gather project coordinates, package name, Java version, extensions, and target directory
- Create a Maven project with the Quarkus CLI
- Prefer Maven wrapper commands for validation
- Verify the generated project with Maven before reporting completion

## Constraints

Project creation must be explicit, reproducible, and Maven-based.

- **PREREQUISITE**: Verify SDKMAN is installed with `sdk version`; if missing, stop and provide setup guidance instead of installing it silently
- **JAVA BASELINE**: Prefer Java 25 unless the user requests another supported version
- **FRAMEWORK BASELINE**: Target the current Quarkus 3.x line by default
- **BUILD TOOL**: Generate a Maven project, not Gradle
- **SAFETY**: Do not overwrite an existing non-empty target directory without explicit user confirmation
- **VERIFY**: Run `./mvnw clean verify` from the generated project when the Maven wrapper exists; otherwise run `mvn clean verify`
- **BEFORE APPLYING**: Read the reference for the full SDKMAN and Quarkus CLI workflow

## When to use this skill

- Create a Quarkus Maven project
- Bootstrap Quarkus project with SDKMAN
- Generate a new Quarkus service

## Workflow

1. **Read reference and gather project inputs**

Read `references/400-frameworks-quarkus-create-project.md`, then gather project directory, group, artifact, package name, Java version, and desired Quarkus extensions.

2. **Verify SDKMAN-managed tooling**

Check SDKMAN, Java, and Quarkus CLI availability. Install or switch candidates only after confirming the intended versions with the user.

3. **Create the Maven project**

Use the Quarkus CLI to create a Maven project, keeping extensions explicit and the Quarkus 3.x baseline as the default.

4. **Verify and report**

Run Maven verification in the generated project and summarize commands used, selected options, generated path, and any follow-up setup.

## Reference

For detailed guidance, examples, and constraints, see [references/400-frameworks-quarkus-create-project.md](references/400-frameworks-quarkus-create-project.md).
