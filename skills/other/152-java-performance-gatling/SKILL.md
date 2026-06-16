---
name: 152-java-performance-gatling
description: Use when you need to set up Gatling performance testing for a Java Maven project — including adding Gatling dependencies and the Gatling Maven plugin, creating Java simulations, running gatling:test, configuring a simulation class, and reviewing generated reports. This should trigger for requests such as Add Gatling performance testing; Apply Gatling performance testing; Create a Gatling simulation; Add Gatling support. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Run performance tests based on Gatling

Provide a complete Gatling performance testing setup for Java Maven projects by adding the required test dependencies and Gatling Maven plugin configuration, creating or guiding Java simulation placement, and explaining how to run simulations and inspect reports.

**What is covered in this Skill?**

- Add Gatling dependencies and the `gatling-maven-plugin` to `pom.xml`
- Project structure: `src/test/java` for Java simulations and `src/test/resources` for Gatling configuration, feeders, templates, and logging
- Run simulations with `./mvnw gatling:test`
- Select a simulation with `-Dgatling.simulationClass=<FullyQualifiedClassName>` when multiple simulations exist
- Use `./mvnw gatling:help -Ddetail=true -Dgoal=test` to inspect available plugin options
- Review generated Gatling run output and reports under the build output directory

**Scope:** Use Gatling through the Maven plugin for Java simulations. Prefer project-local Maven wrapper commands when available.

## Constraints

Gatling setup must be Maven-based, reproducible, and compatible with Java project conventions. Prefer official Gatling Maven plugin behavior and avoid inventing unsupported command-line options.

- **PREREQUISITE**: Verify the project is Maven-based and prefer `./mvnw` when the Maven wrapper exists
- **BUILD CONFIGURATION**: Add Gatling dependencies with test scope and configure `io.gatling:gatling-maven-plugin` in `pom.xml`
- **VERSION SELECTION**: Use the project's existing dependency/version-management pattern; if no Gatling versions are present, ask before pinning versions or use placeholders that require replacement
- **SIMULATION LOCATION**: Place Java simulations under `src/test/java` using an appropriate package name
- **RESOURCE LOCATION**: Place Gatling resources such as `gatling.conf`, feeders, request-body templates, and Logback test configuration under `src/test/resources`
- **BEFORE APPLYING**: Read the reference for setup, execution, and verification guidance
- **EDGE CASE**: If the project is not Maven-based, stop and explain that this skill targets Maven projects before suggesting Gradle or sbt alternatives
- **EDGE CASE**: If multiple simulations exist, configure or pass `-Dgatling.simulationClass=<FullyQualifiedClassName>` for non-interactive execution

## When to use this skill

- Add Gatling performance testing
- Apply Gatling performance testing
- Create a Gatling simulation
- Add Gatling support

## Workflow

1. **Inspect the Maven project**

Check for `pom.xml`, the Maven wrapper, existing test dependencies, dependency management, plugin management, and any existing Gatling configuration.

2. **Add Gatling build configuration**

Add the Gatling test dependency and `io.gatling:gatling-maven-plugin` using the project's existing version and plugin configuration style.

3. **Create or adapt Java simulations**

Create Java simulation classes under `src/test/java` or adapt existing simulations, keeping scenario names, base URLs, injection profiles, and assertions explicit.

4. **Configure resources**

Add optional Gatling resources under `src/test/resources`, including `gatling.conf`, feeders, request body templates, and `logback-test.xml` only when the project needs them.

5. **Run and explain Gatling execution**

Use `./mvnw gatling:test` to run simulations and `-Dgatling.simulationClass=<FullyQualifiedClassName>` when a specific simulation must be selected.

6. **Verify reports and next steps**

Confirm the Gatling run completed, point to the generated report location from the command output, and summarize any failed assertions or performance findings.

## Reference

For detailed guidance, examples, and constraints, see [references/152-java-performance-gatling.md](references/152-java-performance-gatling.md).
