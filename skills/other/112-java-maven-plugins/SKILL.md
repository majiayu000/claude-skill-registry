---
name: 112-java-maven-plugins
description: Use when you need to add or configure Maven plugins in your pom.xml — including quality tools (enforcer, surefire, failsafe, jacoco, pitest, spotbugs, pmd), security scanning (OWASP), code formatting (Spotless), version management, container image build (Jib), build information tracking, and benchmarking (JMH) — through a consultative, modular step-by-step approach that only adds what you actually need. This should trigger for requests such as Add Maven plugins in pom.xml; Improve Maven plugins in pom.xml. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
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
- **BEFORE READING PLUGIN REFERENCES**: Run the question flow embedded in this SKILL.md first. Ask questions one-by-one in strict order, collect all selected plugins/profiles and conditional values, then read only the implementation references selected by the user's answers

## When to use this skill

- Add Maven plugins in pom.xml
- Improve Maven plugins in pom.xml

## Workflow

1. **Validate project before plugin changes**

Run `./mvnw validate` or `mvn validate` and stop if validation fails.

2. **Analyze current plugin and profile configuration**


Before making any changes to `pom.xml`:

1. Scan existing plugins in `<build><plugins>`, `<build><pluginManagement>`, and `<reporting><plugins>`.
2. Scan existing properties in `<properties>`.
3. Scan existing profiles in `<profiles>`.
4. Identify conflicts between existing configuration and possible additions.
5. Preserve all existing plugins, properties, and profiles.
6. Ask the user before enhancing any existing plugin, property, reporting entry, support file, or profile.
7. Skip duplicate additions unless the user explicitly requests an enhancement.


3. **Check Maven Wrapper before plugin changes**


Check for Maven Wrapper files in the project root:

- `mvnw` and `mvnw.cmd`
- `.mvn/wrapper/maven-wrapper.properties`

If Maven Wrapper is not present, stop and ask:

"I notice this project doesn't have Maven Wrapper configured. The Maven Wrapper ensures everyone uses the same Maven version, improving build consistency across different environments. Would you like me to install it? (y/n)"

Wait for the user's response before asking any other question. If the user says "y", install it:

```bash
mvn wrapper:wrapper
```


4. **Ask Maven plugin assessment questions before reading references**


Run this XML-included question flow before reading any plugin/profile implementation reference. Ask one question at a time, wait for the user's answer, and record selected plugins, profiles, and conditional values before continuing.


**Question 1**: What type of Java project is this?

Options:
- Java Library (for publishing to Maven Central/Nexus)
- Java CLI Application (command-line tool)
- Java Microservice (Web service/REST API/Modular monolith)
- Serverless (AWS Lambdas, Azure Functions)
- Java POC (Proof of Concept)
- Other (specify)

---

**Question 2**: Which Java version does your project target?

Options:

- Java 17 (LTS - recommended for new projects)
- Java 21 (LTS - latest LTS version)
- Java 25 (LTS - latest LTS version)
- Other (specify version)

---

**Question 3**: What build and quality aspects are important for your project?

Options:
- Format source code (Spotless)
- Maven Enforcer
- Unit Testing (Surefire)
- Unit Testing Reports (Surefire Reports)
- Integration testing (Failsafe)
- Code coverage reporting (JaCoCo)
- Mutation testing (PiTest)
- Security vulnerability scanning (OWASP)
- Security static code analysis (SpotBugs, PMD)
- Sonar
- Dependency analysis (maven-dependency-plugin)
- Version management
- Container image build (Jib)
- JMH (Java Microbenchmark Harness)
- Maven Compiler
- Cyclomatic Complexity

**Note**: When "Cyclomatic Complexity" is selected, Step 20 will create a PMD ruleset file and profile. The ruleset location depends on project structure: `src/main/pmd/pmd-cyclomatic-complexity.xml` (mono-module) or `pmd/pmd-cyclomatic-complexity.xml` (multi-module).

---

**Question 3.1** (conditional): What is your target container image for Jib?

**Note**: This question is only asked if "Container image build (Jib)" was selected in question 3.

- Example format: `gcr.io/my-project/my-app`, `docker.io/username/myimage`, or `myimage` for local Docker
- The image name will be used in the Jib plugin `<to><image>` configuration

---

**Question 4**:  What is your target coverage threshold?

Options:
- 70% (moderate)
- 80% (recommended)
- 90% (high)
- Custom percentage (specify)

**Note**: This question is only asked if "Code coverage reporting (JaCoCo)" was selected in question 3.

---

**Question 5**: Do you want to configure Sonar/SonarCloud integration?** (y/n)

**Note**: This question is only asked if "Static code analysis (SpotBugs, Sonar)" was selected in question 3.

**If yes, please provide the following information:**

---

**Question 5.1**: What is your Sonar organization identifier?

- For SonarCloud: This is typically your GitHub username or organization name
- For SonarQube: This is your organization key as configured in SonarQube
- Example: `my-github-user` or `my-company-org`

---

**Question 5.2**: What is your Sonar project key?

- For SonarCloud: Usually in format `GITHUB_USER_REPOSITORY_NAME` (e.g., `john-doe_my-java-project`)
- For SonarQube: Custom project key as defined in your SonarQube instance
- Must be unique within your Sonar organization
- Example: `john-doe_awesome-java-lib`

---

**Question 5.3**: What is your Sonar project display name?

- Human-readable name for your project as it appears in Sonar dashboard
- Can contain spaces and special characters
- Example: `Awesome Java Library` or `My Microservice API`

---

**Question 5.4**: Which Sonar service are you using? (conditional)

**Note**: This question is only asked if Sonar configuration was enabled in question 5.

Options:
- SonarCloud (https://sonarcloud.io) - recommended for open source projects
- SonarQube Server (specify your server URL)

**If SonarQube Server**: Please provide your SonarQube server URL (e.g., `https://sonar.mycompany.com`)

---


After all applicable questions are answered, confirm the selections and map them to references:

- If Maven Compiler is selected, read `references/112-java-maven-plugins-maven-compiler-plugin.md`.
- If Maven Enforcer is selected, read `references/112-java-maven-plugins-maven-enforcer-plugin.md`.
- If Unit Testing (Surefire) is selected, read `references/112-java-maven-plugins-maven-surefire-plugin.md`.
- If Integration testing (Failsafe) is selected, read `references/112-java-maven-plugins-maven-failsafe-plugin.md`.
- If Unit Testing Reports (Surefire Reports) is selected, read `references/112-java-maven-plugins-maven-surefire-report-plugin.md` and `references/112-java-maven-plugins-maven-jxr-plugin.md`.
- If Format source code (Spotless) is selected, read `references/112-java-maven-plugins-spotless-maven-plugin.md`.
- If Version management is selected, read `references/112-java-maven-plugins-versions-maven-plugin.md`.
- If build information tracking is selected, read `references/112-java-maven-plugins-git-commit-id-maven-plugin.md`.
- If the project is a Java Library, read `references/112-java-maven-plugins-flatten-maven-plugin.md`.
- If Container image build (Jib) is selected, read `references/112-java-maven-plugins-jib-maven-plugin.md`.
- If Dependency analysis is selected, read `references/112-java-maven-plugins-maven-dependency-plugin.md`.
- If Code coverage reporting (JaCoCo) is selected, read `references/112-java-maven-plugins-profile-jacoco.md`.
- If Mutation testing (PiTest) is selected, read `references/112-java-maven-plugins-profile-pitest.md`.
- If Security vulnerability scanning (OWASP) is selected, read `references/112-java-maven-plugins-profile-security.md`.
- If Security static code analysis (SpotBugs, PMD) is selected, read `references/112-java-maven-plugins-profile-static-analysis.md`.
- If Sonar is selected, read `references/112-java-maven-plugins-profile-sonar.md`.
- If JMH is selected, read `references/112-java-maven-plugins-profile-jmh.md`.
- If Cyclomatic Complexity is selected, read `references/112-java-maven-plugins-profile-cyclomatic-complexity.md`.
- Do not read or apply unselected plugin/profile references.


5. **Read selected references and add only selected configuration**

Add selected plugins and profiles without removing existing ones, preserving project structure and compatibility. Add only the Maven properties, plugin configuration, profile configuration, reporting plugins, and support files required by the selected references.

6. **Summarize applied plugin setup**

Report added plugins/profiles, rationale, and recommended follow-up commands or checks.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/112-java-maven-plugins-maven-compiler-plugin.md](references/112-java-maven-plugins-maven-compiler-plugin.md)
- [references/112-java-maven-plugins-maven-enforcer-plugin.md](references/112-java-maven-plugins-maven-enforcer-plugin.md)
- [references/112-java-maven-plugins-maven-surefire-plugin.md](references/112-java-maven-plugins-maven-surefire-plugin.md)
- [references/112-java-maven-plugins-maven-failsafe-plugin.md](references/112-java-maven-plugins-maven-failsafe-plugin.md)
- [references/112-java-maven-plugins-maven-surefire-report-plugin.md](references/112-java-maven-plugins-maven-surefire-report-plugin.md)
- [references/112-java-maven-plugins-maven-jxr-plugin.md](references/112-java-maven-plugins-maven-jxr-plugin.md)
- [references/112-java-maven-plugins-spotless-maven-plugin.md](references/112-java-maven-plugins-spotless-maven-plugin.md)
- [references/112-java-maven-plugins-flatten-maven-plugin.md](references/112-java-maven-plugins-flatten-maven-plugin.md)
- [references/112-java-maven-plugins-versions-maven-plugin.md](references/112-java-maven-plugins-versions-maven-plugin.md)
- [references/112-java-maven-plugins-git-commit-id-maven-plugin.md](references/112-java-maven-plugins-git-commit-id-maven-plugin.md)
- [references/112-java-maven-plugins-jib-maven-plugin.md](references/112-java-maven-plugins-jib-maven-plugin.md)
- [references/112-java-maven-plugins-maven-dependency-plugin.md](references/112-java-maven-plugins-maven-dependency-plugin.md)
- [references/112-java-maven-plugins-profile-jacoco.md](references/112-java-maven-plugins-profile-jacoco.md)
- [references/112-java-maven-plugins-profile-pitest.md](references/112-java-maven-plugins-profile-pitest.md)
- [references/112-java-maven-plugins-profile-security.md](references/112-java-maven-plugins-profile-security.md)
- [references/112-java-maven-plugins-profile-static-analysis.md](references/112-java-maven-plugins-profile-static-analysis.md)
- [references/112-java-maven-plugins-profile-sonar.md](references/112-java-maven-plugins-profile-sonar.md)
- [references/112-java-maven-plugins-profile-jmh.md](references/112-java-maven-plugins-profile-jmh.md)
- [references/112-java-maven-plugins-profile-cyclomatic-complexity.md](references/112-java-maven-plugins-profile-cyclomatic-complexity.md)
