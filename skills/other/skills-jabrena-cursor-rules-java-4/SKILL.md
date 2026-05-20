---
name: 170-java-documentation
description: Use when you need to generate or improve Java project documentation — including README.md files, package-info.java files, and Javadoc enhancements — through a modular, step-based interactive process that adapts to your specific documentation needs.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Documentation Generator with modular step-based configuration

Generate comprehensive Java project documentation through a modular, step-based interactive process that covers README.md, package-info.java, and Javadoc.

**Core areas:** README.md generation for single-module and multi-module Maven projects, package-info.java creation with basic/detailed/minimal documentation levels, Javadoc enhancement with comprehensive `@param`/`@return`/`@throws` tags, file handling strategies (overwrite/add/backup/skip), and final documentation validation with `./mvnw clean compile` and `./mvnw javadoc:javadoc`.

**Prerequisites:** Run `./mvnw validate` or `mvn validate` before applying any documentation generation. If validation fails, **stop immediately** — do not proceed until all validation errors are resolved.

**Multi-step scope:** Step 1 assesses documentation preferences through targeted questions (README.md, package-info.java, Javadoc) to determine which subsequent steps to execute. Step 2 generates README.md files with software descriptions, build instructions, and optional sections based on code analysis — conditionally executed if selected. Step 3 generates package-info.java files for every package in `src/main/java`, with documentation depth matching the user's chosen level — conditionally executed if selected. Step 4 enhances Javadoc for public and protected APIs, adding missing `@param`, `@return`, `@throws` tags, and usage examples — conditionally executed if selected. Step 5 validates all generated documentation by compiling the project and running Javadoc generation, then produces a comprehensive summary of files created, modified, and skipped.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each documentation generation pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/170-java-documentation.md](references/170-java-documentation.md).
