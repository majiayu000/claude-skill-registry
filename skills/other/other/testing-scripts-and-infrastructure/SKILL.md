---
name: test-scripts-and-infrastructure
description: how to structure and write tests (shell) scripts involving infrastructure
---

IMPORTANT: 

* NEVER WRITE SHELL scripts that directly test Java applications
** Java applications should ALWAYS be directly tested using JUnit Tests executed by Gradle.
** NEVER write shells script that use gradlew bootrun.
** NEVER write shell scripts like this: `test-scripts/test-health.sh` that starts the application, waits for startup, curls `/actuator/health`, and asserts HTTP 200 with status UP

Shell scripts are for testing infrastructure such a docker, docker compose, kubernetes etc.

# When writing tests for shell scripts or infrastructure:

- Tests MUST execute the script and verify the observable outcome
- Tests MUST NOT use grep/static analysis to check file contents
- Tests MUST NOT check for file existence as a proxy for correctness
- Before writing a test, state: "The observable outcome is: [X]"
- If a test can pass without running the code, it's not a behavioral test
- ALWAYS put the test scripts in a test-scripts/ subdirectory
- If necessary, create a test-scripts/test-cleanup.sh script that cleans up test state, e.g. removes docker containers
- Write test-xyz.sh scripts for specific behaviors, e.g. test-init-ca.sh tests init-ca.sh
- ALWAYS Incrementally create a test-end-to-end.sh script that first runs test-cleanup.sh and then runs each test-xyz.sh script in sequence
- CI workflows should call `./test-scripts/test-end-to-end.sh`, not individual test scripts
- When adding new test scripts, add them to test-end-to-end.sh rather than modifying CI configuration


