---
name: evaluate-attempt
description: This SOP evaluates a completed brazil-bench attempt against the spec.md requirements, capturing metrics for comparison across orchestration patterns. Supports Python and Swift/iOS projects.
type: anthropic-skill
version: "1.5"
---

# Evaluate Benchmark Attempt

## Overview
This SOP evaluates a completed brazil-bench attempt against the spec.md requirements,
capturing metrics for comparison across orchestration patterns. Supports both Python
and Swift/iOS implementations.

## Parameters
- **attempt_repo** (required): Repository name (e.g., `attempt-3`)
- **output_dir** (optional, default: `./results`): Where to write evaluation results

## Steps

### 0. Detect Project Language
Identify the primary language/platform of the implementation.

**Detection Commands:**
```bash
cd ./reviews/{attempt_repo}

# Python indicators
ls pyproject.toml setup.py requirements.txt 2>/dev/null

# Swift/iOS indicators
ls Package.swift *.xcodeproj *.xcworkspace 2>/dev/null

# Check file extensions
find . -name "*.py" -not -path "./.venv/*" | head -5
find . -name "*.swift" | head -5
```

**Language Detection Matrix:**

| Files Found | Language | Test Framework |
|-------------|----------|----------------|
| `pyproject.toml`, `*.py` | Python | pytest |
| `Package.swift`, `*.swift` | Swift Package | swift test |
| `*.xcodeproj`, `*.swift` | iOS/Xcode | xcodebuild test |
| Both Python and Swift | Multi-language | Run both |

**Constraints:**
- You MUST detect the language before running tests
- You MUST use appropriate commands for the detected language
- You SHOULD note the detected language in the report

### 1. Clone Attempt
Fetch the attempt repository for local analysis.

**Constraints:**
- You MUST clone into `./reviews/{attempt_repo}`
- You MUST verify the clone succeeded before proceeding
- You MUST NOT modify any files in the cloned repo
```bash
gh repo clone brazil-bench/{attempt_repo} ./reviews/{attempt_repo}
```

### 2. Verify Spec Integrity
Confirm the spec.md was not modified from the template.

**Constraints:**
- You MUST compare `spec.md` against the template version
- You MUST fail the evaluation if spec.md was modified
- You SHOULD use a checksum comparison
```bash
gh repo clone brazil-bench/benchmark-template ./reviews/_template --depth 1
diff ./reviews/{attempt_repo}/spec.md ./reviews/_template/spec.md
```

### 3. Run Conformance Tests
Execute the test suite defined in the spec against the implementation.

**Constraints:**
- You MUST attempt to run all tests specified in spec.md
- You MUST capture pass/fail counts and output
- You SHOULD timeout tests after 60 seconds each
- You MAY retry flaky tests once
- If tests fail due to missing dependencies, follow the dependency resolution steps below

#### Python Test Commands
```bash
cd ./reviews/{attempt_repo}

# Run pytest with verbose output
pytest --tb=short -v 2>&1 | tee test_output.log

# Get summary counts
pytest --tb=no -q 2>&1 | tail -5
```

#### Swift/iOS Test Commands
```bash
cd ./reviews/{attempt_repo}

# Swift Package Manager
swift test 2>&1 | tee test_output.log

# Xcode project (iOS Simulator)
xcodebuild test \
    -project *.xcodeproj \
    -scheme "YourScheme" \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    2>&1 | tee test_output.log

# Parse xcodebuild results
grep -E "(Test Case|passed|failed)" test_output.log

# Using xcpretty for cleaner output (if available)
xcodebuild test -project *.xcodeproj -scheme "YourScheme" \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    | xcpretty --report junit
```

#### 3a. Handle Missing Dependencies (Neo4j, etc.)

If tests fail due to missing external dependencies like Neo4j:

**Step 1: Try to start the dependency via Docker**
```bash
# Check if Docker is available
docker --version

# Check for docker-compose files in the repo
ls ./reviews/{attempt_repo}/docker-compose*.yml

# If Neo4j docker-compose exists, start it
docker-compose -f ./reviews/{attempt_repo}/docker-compose.neo4j.yml up -d

# Or start Neo4j directly
docker run -d --name neo4j-eval -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5

# Wait for Neo4j to be ready
sleep 10
docker logs neo4j-eval 2>&1 | tail -5
```

**Step 2: If Docker unavailable or fails, look for evidence of prior test runs**

Check these sources for test results:
```bash
# Check git history for test-related commits
git log --oneline --all | grep -iE "(test|pass|100%|fix.*test)"

# Check for CI/CD logs or badges
cat ./reviews/{attempt_repo}/README.md | grep -iE "(pass|badge|ci|test)"

# Check prompts.txt for test execution evidence
cat ./reviews/{attempt_repo}/prompts.txt 2>/dev/null | grep -iE "(pytest|test|pass|fail|scenario)"

# Check for pytest cache with results
ls -la ./reviews/{attempt_repo}/.pytest_cache/ 2>/dev/null

# Check for coverage reports
ls -la ./reviews/{attempt_repo}/htmlcov/ ./reviews/{attempt_repo}/coverage.xml 2>/dev/null
```

**Step 3: Document findings in the report**

If tests cannot be run directly, document:
- Why tests couldn't run (missing Neo4j, etc.)
- Evidence found of prior test runs (commit messages, prompts.txt entries)
- Claimed test results from the attempt's documentation
- Mark as "CANNOT VERIFY" with explanation

**Constraints for dependency handling:**
- You MUST try Docker first if available
- You MUST search for evidence if Docker fails
- You MUST NOT claim tests pass without verification
- You SHOULD note the source of any claimed test results
- You SHOULD clean up Docker containers after evaluation: `docker stop neo4j-eval && docker rm neo4j-eval`

#### 3b. Detect Skipped Tests

Skipped tests inflate test counts without providing actual verification. You MUST detect and report them separately.

##### Python: Detect Skipped Tests

**Step 1: Run pytest with verbose output to capture skipped tests**
```bash
cd ./reviews/{attempt_repo}

# Run pytest and capture skip count
pytest --tb=no -v 2>&1 | grep -E "(PASSED|FAILED|SKIPPED|ERROR)" | head -100

# Get summary counts
pytest --tb=no -q 2>&1 | tail -5

# Look for skip patterns in test files
grep -r "pytest.skip\|@pytest.mark.skip\|skipif\|xfail" tests/ --include="*.py"
```

**Step 2: Analyze test files for skip patterns**
```bash
# Count tests that call pytest.skip() inside the test body (worst pattern)
grep -r "pytest.skip(" tests/ --include="*.py" -l | wc -l

# Count tests with @pytest.mark.skip decorator
grep -r "@pytest.mark.skip" tests/ --include="*.py" | wc -l

# Count conditional skips (skipif)
grep -r "@pytest.mark.skipif" tests/ --include="*.py" | wc -l
```

##### Swift/iOS: Detect Skipped Tests

**Step 1: Run swift test or xcodebuild and capture skipped tests**
```bash
cd ./reviews/{attempt_repo}

# Swift Package Manager - look for skipped in output
swift test 2>&1 | grep -E "(passed|failed|skipped)"

# Xcode - parse test results
xcodebuild test -project *.xcodeproj -scheme "YourScheme" \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    2>&1 | grep -E "Test Case.*passed|Test Case.*failed|skipped"
```

**Step 2: Analyze test files for skip patterns**
```bash
# Count XCTSkip usage (explicit skips)
grep -r "XCTSkip\|throw XCTSkip" Tests/ --include="*.swift" | wc -l

# Count disabled tests (func name doesn't start with test)
grep -r "func disabled_test\|// func test" Tests/ --include="*.swift" | wc -l

# Count tests with availability checks that skip
grep -r "@available\|#available" Tests/ --include="*.swift" -A 2 | grep -i skip | wc -l

# Look for conditional test execution
grep -r "guard.*else.*return\|if.*XCTSkip" Tests/ --include="*.swift" | wc -l
```

**Swift Skip Patterns:**

| Pattern | Type | Assessment |
|---------|------|------------|
| `throw XCTSkip("reason")` | Explicit skip | Acceptable if documented |
| `#if !targetEnvironment(simulator)` | Conditional | Acceptable for device-only |
| `@available(iOS 16, *)` | Version skip | Acceptable |
| Renamed to `disabled_testFoo` | Hidden skip | Should be penalized |
| Empty test body | Stub | Should be penalized |

**Step 3: Calculate effective test count**

| Metric | How to Calculate |
|--------|------------------|
| **Total Tests** | Number of test functions defined |
| **Passed Tests** | Tests that ran and passed |
| **Skipped Tests** | Tests marked skip or calling pytest.skip() |
| **Effective Tests** | Total - Skipped (tests that actually run) |
| **Skip Ratio** | Skipped / Total (percentage of tests that skip) |

**Constraints for skipped test handling:**
- You MUST report skipped tests separately from passed tests
- You MUST calculate the "effective test count" (passed + failed, excluding skipped)
- You MUST flag ANY skipped tests for issue filing - zero tolerance for skips
- You MUST distinguish between skip types for the issue description:
  - **Conditional skips** (`@pytest.mark.skipif`): Document reason in issue
  - **Unconditional skips** (`pytest.skip()` in body): Critical - tests never run
  - **Decorator skips** (`@pytest.mark.skip`): Document reason in issue
- You MUST NOT count skipped tests toward the test score in rankings
- You MUST file an issue for ANY skipped test (no acceptable skip threshold)

**Example Analysis:**
```
Total tests:     59
Passed:          44
Skipped:         15  (25% skip ratio - HIGH)
Failed:          0
Effective:       44  (use this for scoring, not 59)

Skip breakdown:
- pytest.skip() in body: 15 (integration tests that never run)
- @pytest.mark.skipif: 0
- @pytest.mark.skip: 0

Flag: INFLATED TEST COUNT - 15 tests skip unconditionally
```

**Document in Report:**
```markdown
## Test Results

| Metric | Count |
|--------|-------|
| Total Tests | 59 |
| Passed | 44 |
| **Skipped** | **15** |
| Failed | 0 |
| **Effective Tests** | **44** |
| Skip Ratio | 25% |

⚠️ **Warning:** 15 tests (25%) are skipped and never execute.
These are integration tests that call `pytest.skip()` inside the test body.
The effective test count for scoring is 44, not 59.
```

#### 3c. Self-Contained Integration Tests (REQUIRED)

Integration tests MUST be self-contained and actually run. Tests that skip because "Neo4j not available" or similar are not acceptable.

**Requirement:** Integration tests must start their own data stores as needed.

**Detection Commands:**

```bash
cd ./reviews/{attempt_repo}

# Check for testcontainers usage (Python)
grep -r "testcontainers\|TestContainer\|DockerContainer" tests/ --include="*.py"

# Check for docker-compose in test setup
grep -r "docker-compose\|subprocess.*docker" tests/ --include="*.py"

# Check for pytest-docker fixture
grep -r "pytest-docker\|docker_compose" tests/ --include="*.py" pyproject.toml

# Check for in-memory alternatives (e.g., SQLite instead of Postgres)
grep -r "sqlite.*memory\|:memory:\|MockNeo4j\|FakeNeo4j" tests/ --include="*.py"

# Check for conftest fixtures that start services
grep -A 20 "@pytest.fixture" tests/conftest.py 2>/dev/null | grep -E "docker\|container\|start\|neo4j"

# Swift: Check for test containers
grep -r "Docker\|Container\|TestServer" Tests/ --include="*.swift"
```

**Acceptable Patterns for Self-Contained Tests:**

| Pattern | Example | Assessment |
|---------|---------|------------|
| **testcontainers** | `Neo4jContainer()` in fixture | ✓ Best - automatic lifecycle |
| **pytest-docker** | `docker_compose_file` fixture | ✓ Good - compose-based |
| **conftest startup** | Fixture runs `docker run neo4j` | ✓ Acceptable - manual but works |
| **In-memory mock** | `MockNeo4jClient` class | ✗ NOT acceptable - not persistent |
| **External dependency** | `pytest.skip("Neo4j not running")` | ✗ NOT acceptable |
| **CI-only tests** | `@pytest.mark.skipif(not CI)` | ✗ NOT acceptable |
| **No integration tests** | No tests for data layer | ✗ NOT acceptable |

**Example: testcontainers Pattern (Python)**

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
        auth=("neo4j", "password")
    )
```

**Example: pytest-docker Pattern**

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def docker_compose_file():
    return "docker-compose.test.yml"

@pytest.fixture(scope="session")
def neo4j_service(docker_services):
    """Wait for Neo4j to be ready."""
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=0.5,
        check=lambda: is_neo4j_ready()
    )
```

**Scoring Impact:**

| Integration Test Quality | Score Modifier |
|-------------------------|----------------|
| Self-contained (testcontainers/docker) | No penalty |
| In-memory mock (not persistent) | -10 points quality |
| Skips due to missing dependency | -10 points quality |
| No integration tests at all | -15 points quality |

**Constraints:**
- You MUST check if integration tests are self-contained
- You MUST flag tests that skip due to external dependencies
- You MUST NOT accept "works on CI" as justification for skipping locally
- You SHOULD recommend testcontainers or pytest-docker patterns
- You SHOULD verify integration tests actually execute (not just exist)

**Document in Report:**

```markdown
## Integration Test Quality

| Aspect | Status |
|--------|--------|
| Self-contained | Yes/No |
| Data store management | testcontainers / docker-compose / mock / external |
| Integration tests run | X passed, Y skipped |

⚠️ **Issue:** Integration tests skip when Neo4j is not running.
Tests should use testcontainers or pytest-docker to manage dependencies.
```

#### 3d. Context Header Blocks (REQUIRED)

Every source code file MUST have a context header comment block that documents:
1. **Purpose** - What the file/module does
2. **Interfaces** - Key classes, functions, or APIs exposed
3. **Change History** - Record of modifications (updated on every change)

**Detection Commands:**

```bash
cd ./reviews/{attempt_repo}

# Python: Check for docstrings or header comments in source files
for f in $(find src -name "*.py" -not -name "__init__.py"); do
  echo "=== $f ==="
  head -50 "$f" | grep -E '""".*|^#.*Purpose|^#.*Context|CONTEXT BLOCK|Change History|Interfaces'
done

# Swift: Check for header comments
for f in $(find Sources -name "*.swift" 2>/dev/null); do
  echo "=== $f ==="
  head -50 "$f" | grep -E '///|/\*\*|Purpose|Context|History'
done

# Count files with context headers vs total
total=$(find src -name "*.py" -not -name "__init__.py" | wc -l)
with_header=$(find src -name "*.py" -not -name "__init__.py" -exec head -30 {} \; -exec echo "---" \; | grep -l "CONTEXT\|Purpose\|Module:" | wc -l)
echo "Files with headers: $with_header / $total"
```

**Required Header Format (Python):**

```python
"""
================================================================================
CONTEXT BLOCK
================================================================================
File: {filename}
Module: {module.path}
Purpose: {one-line description}

Description:
    {detailed description of what this module does}

Interfaces:
    - {ClassName}: {brief description}
    - {function_name}(): {brief description}

Dependencies:
    - {module}: {why needed}

Change History:
    - {date}: {description of change}
    - {date}: Initial creation
================================================================================
"""
```

**Required Header Format (Swift):**

```swift
//
//  {FileName}.swift
//  {ProjectName}
//
//  Purpose: {one-line description}
//
//  Interfaces:
//    - {ClassName}: {brief description}
//    - {functionName}(): {brief description}
//
//  Change History:
//    - {date}: {description of change}
//    - {date}: Initial creation
//
```

**Assessment Criteria:**

| Coverage | Assessment | Score Impact |
|----------|------------|--------------|
| 100% files have headers | Excellent | No penalty |
| 75-99% files have headers | Good | -2 quality |
| 50-74% files have headers | Partial | -5 quality |
| <50% files have headers | Poor | -10 quality |

**Constraints:**
- You MUST check all source files for context headers
- You MUST verify headers include purpose, interfaces, and change history
- You MUST flag files missing headers for issue filing
- You SHOULD note which files have incomplete headers (missing sections)

**Document in Report:**

```markdown
## Context Header Compliance

| Metric | Count |
|--------|-------|
| Source files | X |
| With headers | Y |
| Coverage | Z% |

### Files Missing Headers
- `src/module.py` - No header
- `src/utils.py` - Missing change history

### Assessment
{Excellent/Good/Partial/Poor} - {X}% coverage
```

### 4. Measure Code Metrics
Collect quantitative data about the implementation.

**Constraints:**
- You MUST capture: total lines of code, number of files, dependencies
- You SHOULD capture: cyclomatic complexity, test coverage
- You MAY capture: documentation coverage, type hint coverage

#### Python Metrics
```bash
# Lines of code (excluding tests)
find ./reviews/{attempt_repo}/src -name "*.py" | xargs wc -l

# Dependencies
cat ./reviews/{attempt_repo}/pyproject.toml | grep dependencies -A 50

# File count
find ./reviews/{attempt_repo}/src -name "*.py" | wc -l
```

#### Swift/iOS Metrics
```bash
# Lines of code (excluding tests)
find ./reviews/{attempt_repo}/Sources -name "*.swift" | xargs wc -l

# For Xcode projects
find ./reviews/{attempt_repo} -name "*.swift" -not -path "*/Tests/*" -not -path "*Test*" | xargs wc -l

# Dependencies (Swift Package Manager)
cat ./reviews/{attempt_repo}/Package.swift | grep -A 50 "dependencies:"

# Dependencies (CocoaPods)
cat ./reviews/{attempt_repo}/Podfile 2>/dev/null

# Dependencies (Xcode project - SPM)
grep -r "repositoryURL" ./reviews/{attempt_repo}/*.xcodeproj/project.pbxproj 2>/dev/null | head -20

# File count
find ./reviews/{attempt_repo}/Sources -name "*.swift" | wc -l

# Check for SwiftLint configuration
ls ./reviews/{attempt_repo}/.swiftlint.yml 2>/dev/null
```

### 5. Extract Git Metrics and Analyze Development Timeline
Analyze the development history to separate agent-driven work from human interactions.

**Constraints:**
- You MUST capture: total commits, time from first to last commit
- You MUST separate commits into agent-driven vs human-driven phases
- You MUST calculate autonomous duration (agent work only)
- You SHOULD capture: number of reverts, force pushes (if detectable)
- You SHOULD extract commit messages mentioning "fix", "revert", "oops"

#### 5a. Gather Raw Git Data
```bash
cd ./reviews/{attempt_repo}

# Full commit history with timestamps and messages
git log --format="%ai | %H | %s" --reverse

# Count total commits
git log --oneline | wc -l

# Find fix/revert commits
git log --format="%H %s" | grep -iE "(fix|revert|oops|wrong)"

# Get first and last commit times
git log --format="%ai" --reverse | head -1  # First commit
git log --format="%ai" | head -1             # Last commit
```

#### 5b. Identify Development Phases

Analyze commit timestamps and messages to identify distinct phases:

**Phase 1: Setup (Human)**
- Initial commit, repo setup, file uploads
- Typically first 1-3 commits before implementation starts
- Look for: "Initial commit", "Add files", "upload", "setup"

**Phase 2: Agent Implementation**
- Bulk implementation work by the agent
- Characterized by:
  - Rapid succession of commits (minutes apart)
  - Large code changes
  - Messages like "Implement", "Add", "Create"
  - Consistent commit patterns (same author, similar timing)

**Phase 3: Agent Test Iteration**
- Test fixing and iteration by the agent
- Characterized by:
  - Commits mentioning "fix", "test", "pass"
  - Still rapid succession
  - Often shows progression: "Fix X" → "Fix Y" → "100% pass"

**Phase 4: Human Intervention (Post-Completion)**
- Human-driven changes after agent work completes
- Characterized by:
  - Time gaps (hours/days after previous commits)
  - Different commit patterns or author info
  - Messages about data, documentation, cleanup
  - Changes not required by the spec

#### 5c. Heuristics for Identifying Agent vs Human Commits

**Agent commits typically show:**
- Timestamps within minutes of each other
- Consistent formatting in commit messages
- Co-authored-by lines mentioning Claude/AI
- Large, comprehensive changes
- Focus on implementation and tests

**Human commits typically show:**
- Time gaps of hours or days from previous work
- Different commit message style
- Focus on data, docs, or polish
- Smaller, targeted changes
- Work done after "100% tests pass" milestone

```bash
# Look for time gaps > 1 hour between commits (potential phase boundaries)
git log --format="%ai" --reverse | while read ts; do echo "$ts"; done

# Check for co-author lines indicating AI
git log --format="%b" | grep -i "co-authored"

# Check prompts.txt for session boundaries
cat prompts.txt 2>/dev/null | grep -E "^(Done|Session|Agent)"
```

#### 5d. Calculate Duration Metrics

| Metric | How to Calculate |
|--------|------------------|
| **Total Duration** | Last commit - First commit |
| **Agent Duration** | Sum of time during agent phases only |
| **Human Duration** | Sum of time during human phases |
| **Autonomous Duration** | Phase 2 + Phase 3 (implementation + test fixing) |

**Example Timeline Analysis:**
```
09:00:00 - Initial commit (Human Setup)
09:05:00 - Add spec file (Human Setup)
         --- Agent work begins ---
09:15:00 - Implement Phase 1 (Agent)
09:45:00 - Implement Phase 2 (Agent)
10:10:00 - Implement Phase 3 (Agent)
10:25:00 - Fix test issues (Agent)
10:40:00 - 100% tests pass (Agent)
         --- Agent work ends ---
         --- 2 day gap ---
Oct 3     - Add real data (Human)
Oct 3     - Update docs (Human)

Agent Duration: ~1h 25m (09:15 → 10:40)
Human Duration: ~5m setup + later changes
Autonomous Duration: ~1h 25m
```

#### 5e. Document in Report

Include a Development Timeline section in the report:

```markdown
## Development Duration Breakdown

| Phase | Duration | Description |
|-------|----------|-------------|
| **Setup (Human)** | ~5 min | Initial commit, file upload |
| **Phase 1: Implementation** | ~55 min | Agent implements all phases |
| **Phase 2: Test Fixing** | ~30 min | Agent iterates to 100% pass |
| **Total Autonomous** | **~1h 25m** | Agent work only |
| **Phase 3: Human Intervention** | 2 days later | Data and docs added |

### Commit Analysis
- Total commits: 15
- Agent commits: 10 (09:15 - 10:40 on Day 1)
- Human commits: 5 (setup + Day 3 changes)
- Fix commits: 3 (normal iteration, not rework)
```

### 6. Analyze Against Spec
Review implementation completeness against spec.md requirements.

**Constraints:**
- You MUST evaluate against ALL 16 canonical requirements listed below
- You MUST assess each as: implemented, partial, missing
- You SHOULD note implementation approach for each
- You MUST NOT make subjective quality judgments beyond spec compliance
- You MUST use the exact requirement numbering for cross-attempt consistency

#### 6.0 Canonical Requirements Checklist (16 Requirements)

All evaluations MUST use this exact checklist to ensure consistency across attempts.

**Functional Requirements (6):**
1. **[FR-1]** Search and return match data from all CSV files
2. **[FR-2]** Search and return player data
3. **[FR-3]** Calculate basic statistics (wins, losses, goals)
4. **[FR-4]** Compare teams head-to-head
5. **[FR-5]** Handle team name variations correctly
6. **[FR-6]** Return properly formatted responses

**Query Performance (3):**
7. **[QP-1]** Simple lookups respond in < 2 seconds
8. **[QP-2]** Aggregate queries respond in < 5 seconds
9. **[QP-3]** No timeout errors

**Data Coverage (3):**
10. **[DC-1]** All 6 CSV files are loadable and queryable
11. **[DC-2]** At least 20 sample questions can be answered
12. **[DC-3]** Cross-file queries work (player + match data)

**Technical Requirements (4):**
13. **[TR-1]** MCP server implementation with callable tools
14. **[TR-2]** BDD testing with Given-When-Then structure
15. **[TR-3]** UTF-8 encoding support (Portuguese characters: ã, ç, é, etc.)
16. **[TR-4]** Multiple date format handling (ISO, Brazilian DD/MM/YYYY, with time)

**Report Format for Requirements:**
```markdown
## Requirements Checklist

### Functional Requirements (X/6)
- [x] [FR-1] Search and return match data from all CSV files
- [x] [FR-2] Search and return player data
- [ ] [FR-3] Calculate basic statistics (partial: missing draws)
...

### Query Performance (X/3)
- [x] [QP-1] Simple lookups respond in < 2 seconds
...

### Data Coverage (X/3)
- [x] [DC-1] All 6 CSV files are loadable and queryable
...

### Technical Requirements (X/4)
- [x] [TR-1] MCP server implementation with callable tools
- [x] [TR-2] BDD testing with Given-When-Then structure
...

**Total: X/16 requirements implemented**
```

#### 6a. Real Data vs Simulated Data Assessment

Determine whether the implementation uses real external data or simulated/mock data.

**Real Data Indicators:**
- Data loaders for external sources (Kaggle, APIs, etc.)
- CSV/JSON files in data directory
- API client code with authentication
- Data normalization/mapping logic for external schemas

**Simulated Data Indicators:**
- Hardcoded test fixtures
- Factory/faker-generated data
- Mock data in test files only
- No external data loading code

**Constraints for Real Data Implementations:**
- You MUST note which external data source is used
- You MUST assess schema mapping quality (how well does the implementation adapt external schema to spec schema)
- You MUST distinguish between:
  - **Schema Implemented**: The code defines models matching spec entities
  - **Data Populated**: The data loader can populate those fields from external source
  - **Not Available in Source**: Spec field cannot be populated because external data doesn't include it
- You SHOULD credit implementations that adapt to real-world data constraints
- You SHOULD note any enhancements beyond spec (e.g., additional fields from richer data sources)

**Adjusted Compliance Scoring:**
- If real data is used and a spec field is "Not Available in Source", count it as:
  - **Implemented** if the model/schema supports the field
  - Note the data limitation separately
- Example: If spec requires "attendance" but Kaggle data has no attendance:
  - Check if Match model has attendance field (schema compliance)
  - Note that field would be null with Kaggle data (data limitation)
  - This is NOT a failure - it's a data source constraint

#### 6b. Documentation Quality Assessment

Evaluate the README.md for essential user documentation.

**Required Elements:**
1. **Setup Instructions**: Prerequisites, installation steps, environment configuration
2. **MCP Server Setup**: How to start the server, how to connect Claude
3. **Example Q&A**: Sample questions and expected responses/output

**Extraction Commands:**
```bash
# Check README content
head -100 ./reviews/{attempt_repo}/README.md

# Look for key documentation sections
grep -E "Quick Start|Installation|Setup|MCP|Example|Usage" ./reviews/{attempt_repo}/README.md
```

**Documentation Quality Levels:**
| Level | Criteria | In Report |
|-------|----------|-----------|
| Excellent | All 3 elements + extras (architecture, API ref, troubleshooting) | "Comprehensive README" |
| Good | All 3 required elements present | "Good documentation" |
| Acceptable | 2 of 3 elements | "Partial documentation" |
| Poor | 0-1 elements | "Missing documentation" |

**Best Practice Reference:**
- `2025-10-30-python-hive`: Excellent (Quick Start, MCP config, 15+ demo questions, architecture, troubleshooting)
- `2025-12-15-python-claude-ruvector`: Excellent (detailed setup, claude mcp add example, Q&A with output)

**Include in Report:**
```markdown
## Documentation Quality

| Element | Present | Notes |
|---------|---------|-------|
| Setup Instructions | Yes/No | {details} |
| MCP Server Setup | Yes/No | {details} |
| Example Q&A | Yes/No | {details} |

**Assessment:** {Excellent/Good/Acceptable/Poor}
```

### 7. Generate Codebase Documentation
Generate comprehensive documentation for the implementation using the codebase-summary SOP.

**Constraints:**
- You MUST run the codebase-summary skill on the cloned repository
- You MUST output documentation to `{output_dir}/{attempt_repo}-summary/`
- You SHOULD use the generated documentation to inform the final report
- The documentation provides architecture, components, interfaces, and workflow analysis

```
summarize codebase reviews/{attempt_repo} to {output_dir}/{attempt_repo}-summary/
```

### 8. Generate Report
Produce structured evaluation output.

**Constraints:**
- You MUST write results to `{output_dir}/{attempt_repo}.md`
- You MUST include: attempt name, orchestration pattern, all metrics
- You MUST use consistent format for cross-attempt comparison
- You SHOULD include raw data as appendix

## Output Format
```markdown
# Evaluation: {attempt_repo}

## Summary
- **Pattern:** [swarm|hive|solo|...]
- **Spec Compliance:** X/Y requirements
- **Tests:** X passed, Y skipped, Z failed (X effective)
- **Autonomous Duration:** Xh Ym
- **Documentation:** See `{attempt_repo}-summary/`

## Metrics
| Metric | Value |
|--------|-------|
| Lines of Code | |
| Files | |
| Dependencies | |
| Commits (Total) | |
| Commits (Agent) | |
| Commits (Human) | |
| Fix Commits | |
| Tests (Total) | |
| Tests (Passed) | |
| Tests (Skipped) | |
| Tests (Effective) | |
| Skip Ratio | |

## Development Duration Breakdown

| Phase | Duration | Description |
|-------|----------|-------------|
| **Setup (Human)** | | Initial commit, file upload |
| **Agent Implementation** | | Core implementation work |
| **Agent Test Iteration** | | Test fixing to 100% pass |
| **Total Autonomous** | | Agent work only |
| **Human Intervention** | | Post-completion changes |

### Timeline
```
{timestamp} - {commit message} ({phase})
...
```

### Commit Analysis
- Total commits: X
- Agent commits: X (timespan)
- Human commits: X (description)
- Fix commits: X (context: normal iteration vs rework)

## Requirements Checklist
- [x] Requirement 1
- [ ] Requirement 2 (partial: notes)
- [ ] Requirement 3 (missing)

## Architecture Summary
(Key insights from generated codebase documentation)

## Raw Data
...
```

## Troubleshooting

**Clone fails**
- Verify repo exists: `gh repo view brazil-bench/{attempt_repo}`
- Check permissions: repo must be public or you need access

**Tests won't run due to missing dependencies**
- Try starting Neo4j via Docker (see Step 3a above)
- If Docker unavailable, search for evidence of prior test runs
- Check git commits for "100% pass" or similar messages
- Check prompts.txt for pytest output
- Document as "CANNOT VERIFY" with evidence found

**Neo4j connection errors**
- Verify Neo4j is running: `docker ps | grep neo4j`
- Check credentials match: NEO4J_AUTH=neo4j/password
- Wait for startup: Neo4j needs ~10-15 seconds to initialize
- Check logs: `docker logs neo4j-eval`

**Spec diff shows changes**
- Fail the evaluation
- Note the changes in the report
- This invalidates the benchmark comparison

**Codebase documentation fails**
- Verify the codebase-summary skill is available
- Check that the codebase-path exists and contains code
- Ensure the output directory is writable
- Try running the skill standalone first to debug