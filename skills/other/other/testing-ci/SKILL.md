---
name: testing-ci
cluster: testing
description: "CI/CD: GitHub Actions workflows, parallel sharding, flaky quarantine, junit XML/Allure, coverage gates"
tags: ["ci-cd","github-actions","parallel","flaky","testing"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ci test github actions parallel flaky coverage gate report junit allure"
---

# testing-ci

## Purpose
This skill automates CI/CD pipelines using GitHub Actions, focusing on testing workflows. It handles parallel test execution, quarantines flaky tests, generates reports in JUnit XML or Allure formats, and enforces coverage gates to ensure code quality in repositories.

## When to Use
Use this skill when setting up or optimizing CI for GitHub repos, especially for projects with large test suites (e.g., >1000 tests), to reduce run times via parallel sharding. Apply it for flaky test management in unstable environments or when integrating coverage checks before merges.

## Key Capabilities
- Configure GitHub Actions workflows with parallel sharding using the `matrix` strategy in YAML.
- Quarantine flaky tests by marking them in reports and rerunning subsets automatically.
- Generate JUnit XML reports via tools like `junit-report` or Allure for detailed test insights.
- Enforce coverage gates with thresholds (e.g., >80% line coverage) using tools like Codecov.
- Integrate with GitHub APIs for workflow dispatching and status checks, requiring authentication via `$GITHUB_TOKEN`.

## Usage Patterns
Invoke this skill via OpenClaw CLI commands prefixed with `openclaw testing-ci`. For API usage, send requests to the OpenClaw endpoint (e.g., POST /api/skills/testing-ci). In code, embed it in scripts by checking for the skill ID and passing parameters like workflow names or test shards. Always set environment variables for secrets, such as `$GITHUB_TOKEN`, before execution. For parallel testing, define shards in your workflow YAML and trigger runs programmatically.

## Common Commands/API
- CLI: Run a workflow with parallel sharding: `openclaw testing-ci run --workflow my-repo/tests.yml --parallel 4 --token $GITHUB_TOKEN`
- CLI: Quarantine flaky tests: `openclaw testing-ci quarantine --pattern "flaky-*" --report junit.xml`
- API: Create a workflow: POST /api/skills/testing-ci/workflows with JSON body: `{"name": "build", "matrix": {"shards": [1,2,3,4]}}`
- API: Get coverage report: GET /api/skills/testing-ci/coverage?gate=80
- Code snippet (YAML config for GitHub Actions):
  ```
  jobs:
    test:
      strategy:
        matrix:
          shard: [1, 2, 3, 4]
      run: npm test --shard=${{ matrix.shard }}/4
  ```
- Code snippet (Shell script to handle flaky tests):
  ```
  if grep -q "flaky" junit.xml; then
    openclaw testing-ci quarantine --file junit.xml
  fi
  ```

## Integration Notes
Integrate with GitHub by providing a personal access token in `$GITHUB_TOKEN` for API calls. For JUnit/Allure reports, ensure your workflow outputs XML files and upload them via GitHub Actions artifacts. Use parallel sharding by defining matrices in workflow YAML, then trigger via OpenClaw: `openclaw testing-ci dispatch --repo owner/repo --ref main`. For coverage gates, integrate with services like Codecov by adding a step in your workflow: `curl -Os codecov.io/bash && bash codecov -t $CODECOV_TOKEN`. Always validate inputs to avoid errors, such as checking if `$GITHUB_TOKEN` is set.

## Error Handling
Handle workflow failures by checking exit codes in scripts (e.g., if `$? != 0`, retry with `openclaw testing-ci rerun --workflow ID`). For API errors, parse responses for status codes (e.g., 401 for auth issues, resolve by verifying `$GITHUB_TOKEN`). In parallel runs, use sharding to isolate failures; quarantine flaky tests to prevent false negatives. Common issues: Invalid YAML syntax—validate with `yamllint` before running; coverage gate failures—adjust thresholds via config flags like `--gate 75`.

## Concrete Usage Examples
1. **Set up parallel CI for a Node.js repo**: Create a workflow file, then run: `openclaw testing-ci run --workflow .github/workflows/tests.yml --parallel 4 --token $GITHUB_TOKEN`. This shards tests across 4 runners, reducing execution time from 10m to 3m, and generates a JUnit report for analysis.
2. **Quarantine and report flaky tests**: After a failed run, execute: `openclaw testing-ci quarantine --report allure-results.xml --pattern "test_flaky_*"`. This isolates flaky tests, reruns them, and integrates the Allure report into your GitHub workflow for visual debugging.

## Graph Relationships
- Related to cluster: "testing" (e.g., links to skills like "unit-testing" for deeper test implementation).
- Tagged with: "ci-cd" (connects to "deployment" skills), "github-actions" (integrates with "repo-management"), "parallel" (shares with "scalability" tools), "flaky" (links to "error-analysis"), "testing" (groups with "test-automation").
