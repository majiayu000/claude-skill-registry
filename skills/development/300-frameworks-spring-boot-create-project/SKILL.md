---
name: 300-frameworks-spring-boot-create-project
description: Use when you need to create a new Maven-based Spring Boot 4.0.x project using SDKMAN-managed Java and Spring Boot CLI tooling. This should trigger for requests such as Create a Spring Boot Maven project; Bootstrap Spring Boot project with SDKMAN; Generate a new Spring Boot service. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Create Spring Boot Maven Project

Create a new Spring Boot Maven project through SDKMAN-managed tooling, aligned with Java 25 and the repository's Spring Boot 4.0.x baseline.

**What is covered in this Skill?**

- Verify SDKMAN and Java availability before project creation
- Install or select the required Java and Spring Boot CLI candidates through SDKMAN
- Gather project coordinates, package name, Java version, packaging, and dependencies
- Create a Maven project with Spring Initializr-backed Spring Boot CLI commands
- Prefer Maven wrapper commands for validation
- Verify the generated project with Maven before reporting completion

## Constraints

Project creation must be explicit, reproducible, and Maven-based.

- **PREREQUISITE**: Verify SDKMAN is installed with `sdk version`; if missing, stop and provide setup guidance instead of installing it silently
- **JAVA BASELINE**: Prefer Java 25 unless the user requests another supported version
- **FRAMEWORK BASELINE**: Target Spring Boot 4.0.x by default
- **BUILD TOOL**: Generate a Maven project, not Gradle
- **SAFETY**: Do not overwrite an existing non-empty target directory without explicit user confirmation
- **VERIFY**: Run `./mvnw clean verify` from the generated project when the Maven wrapper exists; otherwise run `mvn clean verify`
- **BEFORE APPLYING**: Read the reference for the full SDKMAN and Spring Boot CLI workflow

## When to use this skill

- Create a Spring Boot Maven project
- Bootstrap Spring Boot project with SDKMAN
- Generate a new Spring Boot service

## Workflow

1. **Read reference and gather project inputs**

Read `references/300-frameworks-spring-boot-create-project.md`, then gather project directory, group, artifact, package name, Java version, packaging, and initial dependencies.

2. **Verify SDKMAN-managed tooling**

Check SDKMAN, Java, and Spring Boot CLI availability. Install or switch candidates only after confirming the intended versions with the user.

3. **Create the Maven project**

Use Spring Boot CLI project creation backed by Spring Initializr, making Maven the selected build tool and Spring Boot 4.0.x the default baseline.

4. **Verify and report**

Run Maven verification in the generated project and summarize commands used, selected options, generated path, and any follow-up setup.

## Reference

For detailed guidance, examples, and constraints, see [references/300-frameworks-spring-boot-create-project.md](references/300-frameworks-spring-boot-create-project.md).
