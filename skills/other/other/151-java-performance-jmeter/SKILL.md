---
name: 151-java-performance-jmeter
description: Use when you need to set up JMeter performance testing for a Java project — including creating the run-jmeter.sh script from the exact template, configuring load tests with loops, threads, and ramp-up, or running performance tests from the project root with custom or default settings. This should trigger for requests such as Improve the code with JMeter performance testing; Apply JMeter performance testing; Refactor the code with JMeter performance testing; Add JMeter support. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Run performance tests based on JMeter

Provide a complete JMeter performance testing solution by creating the run-jmeter.sh script from the exact template, making it executable, and configuring the project structure for load testing. Supports custom loops, threads, ramp-up, and environment variable overrides.

**What is covered in this Skill?**

- Create run-jmeter.sh in project root from the exact template (no modifications)
- Project structure: src/test/resources/jmeter/load-test.jmx, target/ for results
- Script options: -l (loops), -t (threads), -r (ramp-up), -g (GUI), -h (help)
- Environment variables: JMETER_LOOPS, JMETER_THREADS, JMETER_RAMP_UP
- Verify JMeter is installed and available before proceeding

**Scope:** Copy the script template verbatim. Do not modify, interpret, or enhance the template content.

## Constraints

JMeter must be installed and available in PATH. If not available, show a message and exit. Use only the exact template for the run-jmeter.sh script.

- **PREREQUISITE**: Verify JMeter is installed and accessible via `jmeter --version` before creating the script
- **CRITICAL**: Copy the run-jmeter.sh template exactly — do not modify, interpret, or enhance
- **PERMISSION**: Make the script executable with `chmod +x run-jmeter.sh`
- **BEFORE APPLYING**: Read the reference for the exact script template and usage instructions
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Improve the code with JMeter performance testing
- Apply JMeter performance testing
- Refactor the code with JMeter performance testing
- Add JMeter support

## Workflow

1. **Verify JMeter prerequisite**

Check `jmeter --version` and stop with guidance if JMeter is not installed or not available in PATH.

2. **Read JMeter reference template**

Read `references/151-java-performance-jmeter.md` and use the `run-jmeter.sh` template exactly as provided.

3. **Create script and project structure**

Create `run-jmeter.sh` in project root, ensure required JMeter directories/files exist, and apply executable permission with `chmod +x`.

4. **Explain usage and environment overrides**

Document CLI options (`-l`, `-t`, `-r`, `-g`, `-h`) and environment variable overrides (`JMETER_LOOPS`, `JMETER_THREADS`, `JMETER_RAMP_UP`).

## Reference

For detailed guidance, examples, and constraints, see [references/151-java-performance-jmeter.md](references/151-java-performance-jmeter.md).
