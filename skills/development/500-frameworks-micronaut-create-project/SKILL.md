---
name: 500-frameworks-micronaut-create-project
description: Use when you need to create a new Maven-based Micronaut 4.x project using SDKMAN-managed Java and Micronaut CLI tooling. This should trigger for requests such as Create a Micronaut Maven project; Bootstrap Micronaut project with SDKMAN; Generate a new Micronaut service. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create Micronaut Maven Project

Create a new Micronaut Maven project through SDKMAN-managed tooling, aligned with Java 25 and the repository's Micronaut 4.x baseline.

**What is covered in this Skill?**

- Verify SDKMAN and Java availability before project creation
- Install or select the required Java and Micronaut CLI candidates through SDKMAN
- Gather project coordinates, package name, Java version, features, and target directory
- Create a Maven project with the Micronaut CLI
- Prefer Maven wrapper commands for validation
- Verify the generated project with Maven before reporting completion

## Constraints

Project creation must be explicit, reproducible, and Maven-based.

- **PREREQUISITE**: Verify SDKMAN is installed with `sdk version`; if missing, stop and provide setup guidance instead of installing it silently
- **JAVA BASELINE**: Prefer Java 25 unless the user requests another supported version
- **FRAMEWORK BASELINE**: Target the current Micronaut 4.x line by default
- **BUILD TOOL**: Generate a Maven project, not Gradle
- **SAFETY**: Do not overwrite an existing non-empty target directory without explicit user confirmation
- **VERIFY**: Run `./mvnw clean verify` from the generated project when the Maven wrapper exists; otherwise run `mvn clean verify`
- **BEFORE APPLYING**: Read the reference for the full SDKMAN and Micronaut CLI workflow

## When to use this skill

- Create a Micronaut Maven project
- Bootstrap Micronaut project with SDKMAN
- Generate a new Micronaut service

## Workflow

1. **Read reference and gather project inputs**

Read `references/500-frameworks-micronaut-create-project.md`, then gather project directory, group, artifact, package name, Java version, application type, and desired Micronaut features.

2. **Verify SDKMAN-managed tooling**

Check SDKMAN, Java, and Micronaut CLI availability. Install or switch candidates only after confirming the intended versions with the user.

3. **Create the Maven project**

Use the Micronaut CLI to create a Maven project, keeping features explicit and the Micronaut 4.x baseline as the default.

4. **Verify and report**

Run Maven verification in the generated project and summarize commands used, selected options, generated path, and any follow-up setup.

## Reference

For detailed guidance, examples, and constraints, see [references/500-frameworks-micronaut-create-project.md](references/500-frameworks-micronaut-create-project.md).
