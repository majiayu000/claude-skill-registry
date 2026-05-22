---
name: 170-java-documentation
description: Use when you need to generate or improve Java project documentation — including README.md files, package-info.java files, and Javadoc enhancements — through a modular, step-based interactive process that adapts to your specific documentation needs. This should trigger for requests such as Improve the code with documentation; Apply documentation; Refactor the code with documentation. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Documentation Generator with modular step-based configuration

Generate comprehensive Java project documentation through a modular, step-based interactive process that covers README.md, package-info.java, and Javadoc. **This is an interactive SKILL**.

**What is covered in this Skill?**

- README.md generation for single-module and multi-module Maven projects
- package-info.java creation with basic/detailed/minimal documentation levels
- Javadoc enhancement: comprehensive `@param`/`@return`/`@throws` tags
- File handling strategies: overwrite/add/backup/skip
- Final documentation validation with `./mvnw clean compile` and `./mvnw javadoc:javadoc`

## Constraints

Before applying any documentation generation, ensure the project validates. If validation fails, stop immediately — do not proceed until all validation errors are resolved.

- **MANDATORY**: Run `./mvnw validate` or `mvn validate` before applying any documentation generation
- **SAFETY**: If validation fails, stop immediately — do not proceed until all validation errors are resolved
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each documentation generation pattern
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Improve the code with documentation
- Apply documentation
- Refactor the code with documentation

## Workflow

1. **Validate project before documentation changes**

Run `./mvnw validate` or `mvn validate` and stop immediately if validation fails.

2. **Read documentation reference and gather scope**

Read `references/170-java-documentation.md` and identify required outputs (README, package-info, Javadoc enhancements).

3. **Generate selected documentation artifacts**

Create or update documentation using the selected file-handling strategy (overwrite/add/backup/skip).

4. **Run documentation validation checks**

Execute `./mvnw clean compile` and `./mvnw javadoc:javadoc` (or equivalent) to validate generated docs.

## Reference

For detailed guidance, examples, and constraints, see [references/170-java-documentation.md](references/170-java-documentation.md).
