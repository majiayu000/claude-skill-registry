---
name: 112-java-maven-plugins
description: Use when you need to add or configure Maven plugins in your pom.xml — including quality tools (enforcer, surefire, failsafe, jacoco, pitest, spotbugs, pmd), security scanning (OWASP), code formatting (Spotless), version management, container image build (Jib), build information tracking, and benchmarking (JMH) — through a consultative, modular step-by-step approach that only adds what you actually need. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Maven Plugins: pom.xml Configuration Best Practices

Configure Maven plugins and profiles in pom.xml using a structured, question-driven process that preserves existing configuration. **This is an interactive SKILL**.

**What is covered in this Skill?**

Maven plugins:

- Maven Compiler
- Maven Enforcer
- Maven Surefire
- Maven Failsafe
- HTML test reports (Surefire Report, JXR)
- Maven Spotless
- Maven Flatten
- Maven Versions
- Maven Git Commit ID
- Maven Jib

Maven profiles:

- JaCoCo (code coverage)
- PiTest (mutation testing)
- Security (OWASP dependency check)
- Static analysis (SpotBugs, PMD)
- SonarQube/SonarCloud
- JMH (Java Microbenchmark Harness)
- Cyclomatic complexity

## Constraints

Before applying plugin recommendations, ensure the project is in a valid state. Use a structured, question-driven process that preserves existing configuration and adds only what the user selects.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any plugin recommendations
- **SAFETY**: If validation fails, stop and ask the user to fix issues—do not proceed until resolved
- **SCOPE**: Begin with Step 1 (existing configuration analysis) before any changes. Never remove or replace existing plugins; only add new ones that do not conflict
- **BEFORE APPLYING**: Read the reference for detailed plugin configurations, XML templates, and constraints for each step

## When to use this skill

- Configure Maven plugins in pom.xml
- Add Maven plugins to pom.xml
- Improve Maven plugins configuration in pom.xml

## Reference

For detailed guidance, examples, and constraints, see [references/112-java-maven-plugins.md](references/112-java-maven-plugins.md).
