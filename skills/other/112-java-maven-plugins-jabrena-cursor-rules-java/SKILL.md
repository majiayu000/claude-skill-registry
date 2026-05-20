---
name: 112-java-maven-plugins
description: Use when you need to add or configure Maven plugins in your pom.xml — including quality tools (enforcer, surefire, failsafe, jacoco, pitest, spotbugs, pmd), security scanning (OWASP), code formatting (Spotless), version management, build information tracking, and benchmarking (JMH) — through a consultative, modular step-by-step approach that only adds what you actually need. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Maven Plugins: pom.xml Configuration Best Practices

Configure Maven plugins and profiles in pom.xml using a structured, question-driven process that preserves existing configuration.

**Core areas:** Existing configuration analysis and preservation, Maven Wrapper verification, project assessment questions (project nature, Java version, build and quality aspects), properties configuration, Maven Enforcer, Surefire, Failsafe, HTML test reports, JaCoCo coverage, PiTest mutation testing, OWASP security scanning, SpotBugs/PMD static analysis, SonarQube/SonarCloud, Spotless code formatting, Versions plugin, Git Commit ID, Flatten plugin, JMH benchmarking, Maven Compiler, and cyclomatic complexity analysis.

**Prerequisites:** Run `./mvnw validate` or `mvn validate` before applying any plugin recommendations. If validation fails, **stop** and ask the user to fix issues — do not proceed until resolved.

**Multi-step scope:** Begin with Step 1 (existing configuration analysis) before any changes. Ask project assessment questions one-by-one in Step 3, then execute only the plugin steps relevant to user selections. Never remove or replace existing plugins; only add new ones that do not conflict.

**Before applying changes:** Read the reference for detailed plugin configurations, XML templates, and constraints for each step.

## Reference

For detailed guidance, examples, and constraints, see [references/112-java-maven-plugins.md](references/112-java-maven-plugins.md).
