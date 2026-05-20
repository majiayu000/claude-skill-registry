---
name: file-issues
description: Parse evaluation reports and create GitHub issues on attempt repositories for each shortcoming, warning, or improvement opportunity identified during review. Supports Python and Swift/iOS projects.
type: anthropic-skill
version: "2.0"
---

# File Issues from Evaluation

## Overview
This SOP parses evaluation reports from brazil-bench attempts and creates individual
GitHub issues on each attempt's repository for every shortcoming, warning, or
improvement opportunity identified during the review.

## Parameters
- **attempt_repo** (required): Repository name (e.g., `2025-12-13-python-claude-hive`)
- **evaluation_path** (optional, default: `./results/{attempt_repo}.md`): Path to evaluation report
- **dry_run** (optional, default: `false`): If true, show issues that would be created without creating them

## Steps

### 1. Load Evaluation Report
Read the evaluation report for the specified attempt.

**Constraints:**
- You MUST verify the evaluation report exists before proceeding
- You MUST parse markdown sections to identify shortcomings
- You MUST NOT proceed if the report is missing or malformed

```bash
# Verify report exists
ls ./results/{attempt_repo}.md

# Read the report content
cat ./results/{attempt_repo}.md
```

### 2. Verify Repository Access
Confirm the attempt repository exists and is writable.

**Constraints:**
- You MUST verify the repo exists on GitHub
- You MUST check that issues are enabled on the repo
- You SHOULD check for existing issues to avoid duplicates
- You SHOULD use default GitHub labels (no custom labels required)

```bash
# Verify repo exists
gh repo view brazil-bench/{attempt_repo}

# List existing issues to check for duplicates
gh issue list -R brazil-bench/{attempt_repo} --limit 100

# List available labels (use default GitHub labels)
gh label list -R brazil-bench/{attempt_repo}
```

**Default GitHub Labels to Use:**

| Issue Type | Default Label | Reason |
|------------|---------------|--------|
| Missing requirement | `enhancement` | It's a feature that needs to be added |
| Test quality issue | `bug` | Tests not working as expected |
| Compliance summary | `enhancement` | Tracking improvements needed |
| Quality concern | `enhancement` | Code improvement request |
| Documentation gap | `documentation` | Missing or incomplete docs |

Using default labels avoids permission issues (creating custom labels requires admin access).

### 3. Extract Shortcomings from Report
Parse the evaluation report to identify all issues to file.

**Systematic Extraction Commands:**

Use these commands to programmatically extract shortcomings:

```bash
# Extract missing requirements (unchecked items)
grep -E "^- \[ \]" ./results/{attempt_repo}.md

# Extract test quality warnings
grep -A 20 "## Test Quality Warning\|## Test Skip Analysis" ./results/{attempt_repo}.md

# Extract weaknesses section
grep -A 10 "## Weaknesses" ./results/{attempt_repo}.md

# Extract compliance score
grep -E "Spec Compliance.*[0-9]+/[0-9]+" ./results/{attempt_repo}.md

# Extract skip ratio
grep -E "Skip Ratio.*[0-9]+%" ./results/{attempt_repo}.md
```

**Categories of Issues to Extract:**

#### 3a. Missing Requirements
Look in the "Requirements Checklist" section for unchecked items:

**Pattern:** Lines starting with `- [ ]` indicate missing/partial requirements

```bash
# Extract all missing requirements
grep -E "^- \[ \]" ./results/{attempt_repo}.md
```

**Issue Template:**
```
Title: [Missing] {requirement description}
Label: enhancement
Body:
## Requirement
{description}

## Notes from Evaluation
{any additional context from the report}

## Suggested Fix
{if available}

---
Filed from evaluation: results/{attempt_repo}.md
```

#### 3b. Test Quality Warnings
Look for the "Test Quality Warning" or "Test Skip Analysis" sections:

**Patterns to detect:**
- Skip ratio > 20%
- Tests with "not yet implemented" messages
- Integration tests that can't run

**Issue Template:**
```
Title: [Test Quality] {description of test issue}
Label: bug
Body:
## Issue
{description of the test quality problem}

## Details
{skip breakdown, affected files, etc.}

## Impact
- Skip Ratio: {X}%
- Effective Tests: {Y} (vs {Z} total)

## Suggested Fix
{recommendations}

---
Filed from evaluation: results/{attempt_repo}.md
```

#### 3c. Spec Compliance Issues
Look for compliance scores below 100%:

**Patterns:**
- Spec Compliance: X/16 where X < 16
- Partial implementations noted

**Issue Template:**
```
Title: [Compliance] Spec compliance at {X}% ({Y}/16 requirements)
Label: enhancement
Body:
## Current Status
{X}/16 requirements met ({percentage}%)

## Missing Requirements
{list of unchecked requirements}

## Partial Implementations
{list of partial implementations with notes}

---
Filed from evaluation: results/{attempt_repo}.md
```

#### 3d. Skipped Tests
Look for ANY skipped tests in the "Metrics" or "Test Skip Analysis" sections:

**Patterns to detect:**
- Tests (Skipped) > 0 (zero tolerance for skips)
- Any Skip Ratio > 0%
- Conditional skips for external dependencies

**Extraction:**
```bash
# Extract skip ratio and skipped test count
grep -E "Skip Ratio|Tests \(Skipped\)" ./results/{attempt_repo}.md
```

**Issue Template:**
```
Title: [Test Quality] {X}% tests skip conditionally ({Y}/{Z} tests)
Label: enhancement
Body:
## Issue
{Y} of {Z} tests ({X}%) are skipped.

## Details
{description of why tests skip - e.g., Neo4j not available}

## Impact
- Skip Ratio: {X}%
- Effective Tests: {effective} (vs {total} total)
- Benchmark penalty: Exceeds 10% threshold

## Assessment
{evaluation of whether skips are acceptable or problematic}

### Acceptable Skips
- Integration tests that require external services (Neo4j, Redis, etc.)
- Conditional skips with proper `pytest.skip()` messages

### Problematic Skips
- Tests with "not yet implemented" messages
- Unconditional skips that inflate test counts
- Stub tests that never execute

## Recommendation
{suggested action or note that no action required}

---
Filed from evaluation: results/{attempt_repo}.md
```

**Skip Ratio Thresholds:**
| Skip Ratio | Assessment | Action |
|------------|------------|--------|
| 0% | Clean | No issue needed |
| >0% | Not acceptable | File issue for every skipped test |
| >20% | Concerning | File issue, recommend fixes |
| >50% | Critical | File issue as `bug`, high priority |

#### 3d-integration. Self-Contained Integration Tests (CRITICAL)

Integration tests that skip because external dependencies aren't running are NOT acceptable. Tests must manage their own data stores.

**Patterns to detect:**
- Tests skipping with "Neo4j not running", "database not available", etc.
- Tests requiring manual docker setup before running
- Tests that only pass in CI environments
- Conditional skips based on external service availability

**Extraction:**
```bash
# Check for external dependency skips
grep -r "pytest.skip.*neo4j\|pytest.skip.*database\|pytest.skip.*not running" ./reviews/{attempt_repo}/tests/

# Check for skipif based on service availability
grep -r "skipif.*neo4j\|skipif.*database\|skipif.*connection" ./reviews/{attempt_repo}/tests/

# Check for testcontainers usage (good)
grep -r "testcontainers\|Neo4jContainer" ./reviews/{attempt_repo}/tests/

# Check for pytest-docker usage (good)
grep -r "pytest-docker\|docker_compose_file" ./reviews/{attempt_repo}/
```

**Issue Template:**
```
Title: [Test Quality] Integration tests must be self-contained - use testcontainers
Label: bug
Body:
## Issue

Integration tests skip when external dependencies (e.g., Neo4j) are not running. This is not acceptable - tests must manage their own data stores.

## Current Behavior

Tests skip with messages like:
- "Neo4j not running"
- "Database not available"
- "Skipping integration tests"

{examples from codebase}

## Required Behavior

Integration tests MUST start their own data stores. Tests should pass on any machine with Docker installed, without manual setup.

## Recommended Solution: testcontainers

Use [testcontainers-python](https://testcontainers-python.readthedocs.io/) to automatically manage Neo4j:

```python
# conftest.py
import pytest
from testcontainers.neo4j import Neo4jContainer

@pytest.fixture(scope="session")
def neo4j_container():
    """Start Neo4j container for integration tests."""
    with Neo4jContainer("neo4j:5") as neo4j:
        yield neo4j

@pytest.fixture
def neo4j_client(neo4j_container):
    """Get client connected to test container."""
    return Neo4jClient(
        uri=neo4j_container.get_connection_url(),
        auth=("neo4j", "test")
    )
```

```python
# test_integration.py
def test_create_match(neo4j_client):
    """Test creating a match in Neo4j - container starts automatically."""
    result = neo4j_client.create_match(...)
    assert result is not None
```

## Alternative: pytest-docker

If you prefer docker-compose, use [pytest-docker](https://github.com/avast/pytest-docker):

```python
# conftest.py
@pytest.fixture(scope="session")
def docker_compose_file():
    return "docker-compose.test.yml"

@pytest.fixture(scope="session")
def neo4j_service(docker_services):
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=0.5,
        check=lambda: is_responsive()
    )
```

## Dependencies to Add

```toml
# pyproject.toml
[project.optional-dependencies]
test = [
    "pytest",
    "testcontainers[neo4j]",
    # OR
    "pytest-docker",
]
```

## Impact

- Current: Tests skip, providing no integration coverage
- After fix: Tests run everywhere, actually verify Neo4j integration

---
Filed from evaluation: results/{attempt_repo}.md
```

**Issue Template: Missing Integration Tests**
```
Title: [Test Quality] Missing integration tests - no tests verify data persistence
Label: bug
Body:
## Issue

No integration tests exist to verify the data persistence layer works correctly.

## Current State

- Only unit tests with mocks exist
- No tests verify actual database operations
- Data layer is untested in real conditions

## Required

Integration tests MUST exist and MUST:
1. Use persistent storage (testcontainers, pytest-docker, or file-based)
2. Test actual CRUD operations against real storage
3. Run without manual setup (self-contained)

## Recommended Solution

Add integration tests using testcontainers:

```python
# tests/integration/conftest.py
import pytest
from testcontainers.neo4j import Neo4jContainer

@pytest.fixture(scope="session")
def neo4j_container():
    with Neo4jContainer("neo4j:5") as neo4j:
        yield neo4j

# tests/integration/test_database.py
def test_create_and_retrieve_match(neo4j_container):
    client = Neo4jClient(uri=neo4j_container.get_connection_url())
    match = client.create_match(...)
    retrieved = client.get_match(match.id)
    assert retrieved == match
```

## Impact

- Current: Data layer has zero test coverage
- After fix: Confidence that database operations work correctly

---
Filed from evaluation: results/{attempt_repo}.md
```

**Issue Template: In-Memory Mock Not Acceptable**
```
Title: [Test Quality] Integration tests use in-memory mock instead of persistent storage
Label: bug
Body:
## Issue

Integration tests use in-memory mock storage instead of persistent storage.

## Current Behavior

Tests use mock classes like `MockNeo4jDatabase` or `FakeStorage` that store data in memory dictionaries.

## Why This Fails

In-memory mocks:
- Don't test actual persistence behavior
- Don't catch serialization/deserialization bugs
- Don't verify database constraints
- Data doesn't survive process restart

## Required Behavior

Integration tests must use **persistent storage** that actually tests the data persistence layer.

## Recommended Solution

Use testcontainers with real database:

```python
from testcontainers.neo4j import Neo4jContainer

@pytest.fixture(scope="session")
def neo4j_container():
    with Neo4jContainer("neo4j:5") as neo4j:
        yield neo4j
```

Or use file-based persistent storage (e.g., SQLite):

```python
@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"
```

---
Filed from evaluation: results/{attempt_repo}.md
```

**Integration Test Quality Assessment:**

| Pattern | Quality | Action |
|---------|---------|--------|
| testcontainers (auto-managed) | ✓ Best | No issue needed |
| pytest-docker (compose-based) | ✓ Good | No issue needed |
| conftest starts docker manually | ✓ Acceptable | No issue needed |
| In-memory mock (not persistent) | ✗ Not acceptable | File `bug` issue - storage must be persistent |
| Skips if service not running | ✗ Not acceptable | File `bug` issue |
| Requires manual docker setup | ✗ Not acceptable | File `bug` issue |
| CI-only integration tests | ✗ Not acceptable | File `bug` issue |
| No integration tests at all | ✗ Not acceptable | File `bug` issue |

#### 3e. Test Best Practices
Check if tests follow pytest-bdd best practices with Gherkin `.feature` files:

**Patterns to detect:**
- Missing `.feature` files
- Docstring-only BDD (not executable Gherkin)
- Custom BDD helper classes instead of pytest-bdd
- E2E-only tests without unit test coverage
- **Async test functions** (pytest-bdd does not support async)

**Extraction:**
```bash
# Check for pytest-bdd usage
grep -E "pytest-bdd|\.feature|Given.*When.*Then" ./results/{attempt_repo}.md

# Check test approach in comparison analysis
grep -A 5 "Test.*Framework\|BDD Style" ./results/{attempt_repo}.md

# Check for async test functions (problematic with pytest-bdd)
grep -r "async def test_\|async def given_\|async def when_\|async def then_" ./reviews/{attempt_repo}/tests/
```

**Issue Template:**
```
Title: [Test Quality] Use pytest-bdd with .feature files instead of {current_approach}
Label: enhancement
Body:
## Issue
{description of current test approach}

## Current Approach
{code example showing current pattern}

## Best Practice
Use pytest-bdd with proper Gherkin `.feature` files:

```gherkin
# features/example.feature
Feature: Example Feature
  Scenario: Example scenario
    Given precondition
    When action
    Then expected result
```

**IMPORTANT: Use synchronous test functions only.**

pytest-bdd does NOT support async step definitions or test functions. Async tests will silently fail or produce unexpected behavior.

```python
# WRONG - async tests fail with pytest-bdd
@given("a database connection")
async def given_db():  # ❌ Will not work correctly
    return await get_connection()

# CORRECT - use sync functions
@given("a database connection")
def given_db():  # ✓ Works correctly
    return get_connection_sync()
```

If your MCP server uses async code, create synchronous test wrappers:

```python
import asyncio

def run_async(coro):
    """Helper to run async code in sync tests."""
    return asyncio.get_event_loop().run_until_complete(coro)

@given("a player search result")
def given_player_search(context):
    # Wrap async call in sync function
    context["result"] = run_async(search_player("Neymar"))
```

## Benefits of pytest-bdd
1. Readable scenarios for non-technical stakeholders
2. Reusable step definitions
3. Standard tooling (IDE support, linting)
4. Separation of concerns

## Recommendation
{specific migration guidance}

---
Filed from evaluation: results/{attempt_repo}.md
```

**Test Pattern Quality:**
| Pattern | Quality | Action |
|---------|---------|--------|
| pytest-bdd + .feature files (sync) | Best | No issue needed |
| pytest-bdd without .feature (sync) | Good | Optional improvement |
| pytest-bdd with async functions | Broken | File bug issue - tests silently fail |
| Docstring BDD | Acceptable | File enhancement issue |
| Custom BDD helper | Non-standard | File enhancement issue |
| E2E only / No BDD | Poor | File enhancement issue |

**Critical: Async pytest-bdd Warning**

pytest-bdd step definitions and scenarios MUST be synchronous. Async functions will:
- Silently skip or fail tests
- Return coroutine objects instead of results
- Cause confusing "test passed" reports when tests didn't actually run

Always use synchronous wrappers around async code in BDD tests.

---

#### 3e-swift. Swift/iOS Test Best Practices

Check if tests follow Swift/iOS testing best practices:

**Patterns to detect:**
- Missing test targets in Xcode project
- No XCTest usage
- Empty test methods (stubs)
- Disabled tests (renamed without `test` prefix)
- Missing async test handling
- No mock/dependency injection

**Extraction:**
```bash
# Check for XCTest usage
grep -r "import XCTest\|XCTestCase" ./reviews/{attempt_repo}/ --include="*.swift"

# Check for test methods
grep -r "func test" ./reviews/{attempt_repo}/ --include="*.swift" | wc -l

# Check for disabled/stub tests
grep -r "func disabled_\|// func test\|func _test" ./reviews/{attempt_repo}/ --include="*.swift"

# Check for proper async testing
grep -r "async throws\|expectation\|wait(for:" ./reviews/{attempt_repo}/ --include="*.swift"

# Check for Quick/Nimble BDD framework
grep -r "import Quick\|import Nimble\|describe.*context.*it" ./reviews/{attempt_repo}/ --include="*.swift"
```

**Issue Template (Swift):**
```
Title: [Test Quality] Use XCTest with proper async handling instead of {current_approach}
Label: enhancement
Body:
## Issue
{description of current test approach}

## Current Approach
{code example showing current pattern}

## Best Practice
Use XCTest with proper structure:

```swift
import XCTest
@testable import YourApp

final class FeatureTests: XCTestCase {
    var sut: FeatureViewModel!
    var mockService: MockNetworkService!

    override func setUp() {
        super.setUp()
        mockService = MockNetworkService()
        sut = FeatureViewModel(service: mockService)
    }

    override func tearDown() {
        sut = nil
        mockService = nil
        super.tearDown()
    }

    func test_whenLoadingData_thenUpdatesState() async throws {
        // Given
        mockService.mockResult = TestData.sampleItems

        // When
        await sut.loadData()

        // Then
        XCTAssertEqual(sut.items.count, 3)
        XCTAssertFalse(sut.isLoading)
    }
}
```

**For BDD-style tests, use Quick/Nimble:**

```swift
import Quick
import Nimble
@testable import YourApp

class FeatureSpec: QuickSpec {
    override class func spec() {
        describe("Feature") {
            var sut: FeatureViewModel!

            beforeEach {
                sut = FeatureViewModel()
            }

            context("when loading data") {
                it("updates the state") {
                    waitUntil { done in
                        sut.loadData {
                            expect(sut.items).toNot(beEmpty())
                            done()
                        }
                    }
                }
            }
        }
    }
}
```

## Recommendation
{specific migration guidance}

---
Filed from evaluation: results/{attempt_repo}.md
```

**Swift Test Pattern Quality:**

| Pattern | Quality | Action |
|---------|---------|--------|
| XCTest + async/await + DI | Best | No issue needed |
| XCTest + expectations + DI | Good | No issue needed |
| Quick/Nimble BDD | Good | No issue needed |
| XCTest without DI | Acceptable | Optional improvement |
| XCTest with stubs/disabled | Poor | File enhancement issue |
| No tests | Critical | File bug issue |

**Swift-Specific Test Issues:**

| Issue | Detection | Severity |
|-------|-----------|----------|
| Tests don't compile | `swift build` fails | Critical |
| Tests timeout on CI | Long `wait(for:)` calls | High |
| No async handling | Missing `async` or `expectation` | Medium |
| Force unwrapping in tests | `!` without guard | Low |
| Missing mocks | No protocol-based DI | Medium |

#### 3f. Documentation Quality
Check if README.md contains essential user documentation:

**Required Elements:**
1. **Setup Instructions**: Prerequisites, installation, configuration
2. **MCP Server Setup**: How to start server, how to connect Claude
3. **Example Q&A**: Sample questions and expected responses

**Extraction:**
```bash
# Check README in cloned repo
head -100 ./reviews/{attempt_repo}/README.md

# Look for key sections
grep -E "Quick Start|Installation|Setup|MCP|Example|Usage" ./reviews/{attempt_repo}/README.md
```

**Issue Template:**
```
Title: [Docs] README missing setup instructions and usage examples
Label: documentation
Body:
## Issue
The README.md lacks essential user documentation.

## Missing Documentation

### 1. Setup Instructions
- Prerequisites (Python version, Neo4j)
- Installation steps
- Environment configuration

### 2. MCP Server Setup
- How to start the MCP server
- How to configure Claude to use the server
- Example configuration

### 3. Usage Examples with Q&A
- Example questions users can ask
- Expected responses/output

## Best Practice Example
See `2025-10-30-python-hive` for comprehensive documentation.

---
Filed from evaluation: results/{attempt_repo}.md
```

**Documentation Quality Levels:**
| Level | Criteria | Action |
|-------|----------|--------|
| Excellent | All 3 elements + extras (architecture, API ref) | No issue needed |
| Good | All 3 elements present | No issue needed |
| Acceptable | 2 of 3 elements | Optional improvement issue |
| Poor | 0-1 elements | File documentation issue |

#### 3g. Architecture/Quality Issues
Look for concerns in "Architecture Summary", "Weaknesses", or "Areas of Note":

**Patterns:**
- Bullet points under "Weaknesses" heading
- Notes about missing MCP endpoints
- Performance concerns
- Code structure issues

**Issue Template:**
```
Title: [Quality] {description}
Label: enhancement
Body:
## Issue
{description}

## Context
{relevant context from the evaluation}

## Recommendation
{suggested improvement}

---
Filed from evaluation: results/{attempt_repo}.md
```

#### 3h. Context Header Blocks
Check if source code files have proper context header comment blocks.

**Patterns to detect:**
- Files missing header blocks entirely
- Headers missing required sections (Purpose, Interfaces, Change History)
- Headers not updated with change history

**Extraction:**
```bash
# Check for context headers in source files
for f in $(find ./reviews/{attempt_repo}/src -name "*.py" -not -name "__init__.py"); do
  if ! head -30 "$f" | grep -q "CONTEXT\|Purpose\|Module:"; then
    echo "Missing header: $f"
  fi
done
```

**Issue Template:**
```
Title: [Quality] Source files missing context header blocks
Label: enhancement
Body:
## Issue

Source code files are missing required context header comment blocks.

## Required Header Format

Every source file must have a header block that includes:
1. **Purpose** - What the file/module does
2. **Interfaces** - Key classes, functions, or APIs exposed
3. **Change History** - Record of modifications (updated on every change)

## Example Header (Python)

```python
"""
================================================================================
CONTEXT BLOCK
================================================================================
File: server.py
Module: brazilian_soccer_mcp.server
Purpose: MCP server implementation for Brazilian soccer knowledge graph

Description:
    Exposes Neo4j queries as MCP tools for Claude to use.

Interfaces:
    - create_server(): Creates and configures the MCP server
    - MCPServer: Main server class with tool handlers

Dependencies:
    - mcp: MCP protocol implementation
    - neo4j: Database connection

Change History:
    - 2025-01-04: Add get_player_stats tool
    - 2025-01-03: Initial creation
================================================================================
"""
```

## Files Missing Headers

{list of files without proper headers}

## Impact

- Without context headers, code is harder to understand and maintain
- Change history helps track evolution of the codebase
- Interfaces section provides quick API reference

---
Filed from evaluation: results/{attempt_repo}.md
```

**Context Header Assessment:**

| Coverage | Assessment | Action |
|----------|------------|--------|
| 100% | Excellent | No issue needed |
| 75-99% | Good | Optional issue |
| 50-74% | Partial | File enhancement issue |
| <50% | Poor | File enhancement issue |

### 4. Create Issues
File each extracted shortcoming as a separate GitHub issue.

**Constraints:**
- You MUST create one issue per shortcoming (not a combined issue)
- You MUST apply appropriate default labels
- You MUST include reference to the evaluation report
- You MUST check for duplicates before creating (match on title)
- You MUST create detail issues BEFORE the summary issue (so you can reference issue numbers)
- You SHOULD group related issues with a common prefix
- You MAY skip issues if identical ones already exist

**Issue Creation Order:**
1. Create all detail issues first ([Missing], [Test Quality], [Quality], etc.)
2. Note the issue numbers assigned
3. Create the [Compliance] summary issue last, referencing the detail issues

```bash
# Check if issue already exists
gh issue list -R brazil-bench/{attempt_repo} --search "{issue_title}" --json title

# Create issue using HEREDOC for multi-line markdown body
gh issue create -R brazil-bench/{attempt_repo} \
  --title "[Missing] MCP server implementation" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## Requirement

The spec requires an MCP server with tools exposed as endpoints.

## Current State

Query engine exists but not exposed as MCP tools.

## Suggested Fix

Add MCP server wrapper using `fastmcp` or `mcp` package.

---
Filed from evaluation: [results/{attempt_repo}.md](https://github.com/brazil-bench/pourpoise/blob/main/results/{attempt_repo}.md)
EOF
)"
```

**Cross-Referencing Issues:**

When creating the summary [Compliance] issue, reference related detail issues:

```markdown
## Missing Requirements

1. **MCP server implementation** - see #2
2. **Query performance benchmarks** - see #3
3. **Cross-file queries verification** - see #4

## Additional Issues

- **Test Quality:** 84% skip ratio - see #1
```

**Issue Creation Rules:**

| Shortcoming Type | Title Prefix | Default Label |
|------------------|--------------|---------------|
| Missing requirement | `[Missing]` | `enhancement` |
| Test quality issue | `[Test Quality]` | `bug` |
| Skipped tests (>10%) | `[Test Quality]` | `enhancement` or `bug`* |
| Integration tests skip | `[Test Quality]` | `bug` |
| Test best practices | `[Test Quality]` | `enhancement` |
| Documentation quality | `[Docs]` | `documentation` |
| Spec compliance | `[Compliance]` | `enhancement` |
| Architecture/quality | `[Quality]` | `enhancement` |
| Performance concern | `[Performance]` | `enhancement` |

*Use `bug` for skip ratios >50%, problematic skips, or integration tests that skip due to missing dependencies; use `enhancement` for acceptable conditional skips.

#### 4a. Summary Issue Template

After creating all detail issues, create a [Compliance] summary issue that links them together:

```bash
gh issue create -R brazil-bench/{attempt_repo} \
  --title "[Compliance] Spec compliance at {X}% ({Y}/16 requirements)" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## Current Status

{Y}/16 requirements met ({X}% compliance)

## Missing Requirements

1. **{requirement_1}** - see #{issue_number_1}
2. **{requirement_2}** - see #{issue_number_2}
...

## Implemented Requirements

### Category 1 (N/M)
- [x] Requirement that passed
- [x] Another passing requirement
...

## Additional Issues

- **Test Quality:** {skip_ratio}% skip ratio - see #{test_quality_issue}

## Benchmark Score

Current score: **{score}** (rank {rank} of 8)

To improve ranking, address the issues linked above.

---
Filed from evaluation: [results/{attempt_repo}.md](https://github.com/brazil-bench/pourpoise/blob/main/results/{attempt_repo}.md)
EOF
)"
```

This summary issue serves as an index to all other filed issues and provides context for prioritization.

### 5. Generate Summary
Output a summary of all issues created.

**Constraints:**
- You MUST list all issues created with their URLs
- You MUST note any issues skipped due to duplicates
- You MUST include the total count

**Output Format:**
```markdown
## Issues Filed for {attempt_repo}

### Created ({N} issues)
| # | Title | URL |
|---|-------|-----|
| 1 | [Missing] MCP server implementation | {url} |
| 2 | [Test Quality] 84% tests skip unconditionally | {url} |
| ... | ... | ... |

### Skipped (duplicates)
- {title} - already exists as #{existing_issue_number}

### Summary
- Total shortcomings identified: {X}
- Issues created: {Y}
- Issues skipped (duplicates): {Z}
```

## Examples

### Example 1: Filing issues for Hive v2

```bash
# File issues from the Hive v2 evaluation
file issues for 2025-12-13-python-claude-hive
```

Expected issues:
1. `[Missing] MCP server implementation - tools not exposed as MCP endpoints`
2. `[Missing] Query performance benchmarks (< 2s simple, < 5s aggregate)`
3. `[Missing] Cross-file queries verification`
4. `[Test Quality] 84% of tests skip unconditionally (53/63 tests)`
5. `[Compliance] Spec compliance at 81% (13/16 requirements)`

### Example 2: Dry run to preview issues

```bash
# Preview issues without creating them
file issues for 2025-12-13-python-claude-hive --dry-run
```

## Troubleshooting

**No evaluation report found**
- Run the evaluate-attempt skill first
- Check the path: `./results/{attempt_repo}.md`

**Permission denied on repository**
- Verify you have write access: `gh repo view brazil-bench/{attempt_repo}`
- Check if issues are enabled on the repo

**Duplicate detection failing**
- Issues are matched by exact title
- If titles differ slightly, duplicates may be created
- Use `gh issue list -R repo --search "keyword"` to check

**Labels don't exist**
- Use default GitHub labels (`enhancement`, `bug`, `documentation`) which exist on all repos
- Avoid custom labels as creating them requires admin access (HTTP 403 error)
- If a label doesn't exist, omit the `--label` flag entirely
- The title prefix (e.g., `[Missing]`, `[Test Quality]`) provides categorization without labels

**Too many issues**
- Use `--dry-run` first to preview
- Consider grouping minor issues into a single "Minor improvements" issue
- Focus on high-impact shortcomings first
