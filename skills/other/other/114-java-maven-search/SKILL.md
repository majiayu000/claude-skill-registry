---
name: 114-java-maven-search
description: Covers Maven Central search (Search API, maven-metadata.xml, artifact URLs) and project-local update reports via versions-maven-plugin (display-property-updates, display-dependency-updates, display-plugin-updates). Use when finding or verifying coordinates, browsing Central, or checking what newer versions apply to the user’s pom.xml. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0
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

## Reference

For detailed guidance, examples, and constraints, see [references/114-java-maven-search.md](references/114-java-maven-search.md).
