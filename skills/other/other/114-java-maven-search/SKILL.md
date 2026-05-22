---
name: 114-java-maven-search
description: Covers Maven Central search (Search API, maven-metadata.xml, artifact URLs) and project-local update reports via versions-maven-plugin (display-property-updates, display-dependency-updates, display-plugin-updates). Use when finding or verifying coordinates, browsing Central, or checking what newer versions apply to the user’s pom.xml. This should trigger for requests such as Search Maven Central; Find Maven dependency; Maven coordinates; groupId artifactId version. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Maven Central search and coordinates

Help users search Maven Central, resolve **groupId:artifactId:version**, read version history, and build correct download URLs; and when working on **their** project, verify `versions-maven-plugin` and run `versions:display-*` goals for dependency, plugin, and property updates. **What is covered:**

- Maven Central Search API — e.g. keyword search for Spring Boot starters (`spring-boot-starter`) or coordinate filters (`g:org.springframework.boot AND a:spring-boot-starter-parent`)
- Direct repository layout and `maven-metadata.xml`
- POM, JAR, `-sources.jar`, `-javadoc.jar` URL patterns
- Parsing POMs for direct dependencies; transitive trees via Maven/Gradle on the consumer project
- Versions Maven Plugin — ensure `org.codehaus.mojo:versions-maven-plugin` is declared, then `./mvnw versions:display-property-updates`, `versions:display-dependency-updates`, `versions:display-plugin-updates`
- Output format: structured coordinates, tables, and verifiable HTTPS links

## Constraints

Verify coordinates against the Search API or repository responses before asserting availability. Prefer release versions unless snapshots are explicitly required.

- **VERIFY**: Do not invent GAVs — confirm via Search API or successful GET of metadata/POM
- **FORMAT**: Always express full coordinates as `groupId:artifactId:version` when a version is fixed
- **BEFORE APPLYING**: Read the reference for step-by-step workflows, query syntax, and URL patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files or running project-wide commands
- **EDGE CASE**: If required context, files, credentials, or tools are missing, report the blocker explicitly and ask whether to proceed with setup or fallback guidance
- **EDGE CASE**: If requested changes conflict with project constraints or safety boundaries, explain the conflict and ask for user confirmation on the preferred trade-off

## When to use this skill

- Search Maven Central
- Find Maven dependency
- Maven coordinates
- groupId artifactId version
- Latest version Maven
- maven-metadata.xml
- Download JAR from Maven Central
- Download javadocs
- Dependency tree transitive
- display-dependency-updates
- display-plugin-updates
- Outdated Maven dependencies

## Workflow

1. **Read Maven search reference workflow**

Read `references/114-java-maven-search.md` before forming queries, coordinate checks, or URL outputs.

2. **Perform Maven Central discovery and verification**

Use Search API and repository metadata/POM checks to confirm valid coordinates and available versions.

3. **Format results with full coordinates and links**

Return `groupId:artifactId:version` outputs, structured tables, and verifiable HTTPS artifact URLs.

4. **Run project-local update checks when applicable**

When working on a local project, ensure versions-maven-plugin usage and run `versions:display-*` reports for properties, dependencies, and plugins.

## Reference

For detailed guidance, examples, and constraints, see [references/114-java-maven-search.md](references/114-java-maven-search.md).
