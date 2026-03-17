---
name: test-case-organizer
description: This skill should be used when the user asks to "测试用例整理", "测试整理", "organize test cases", "reorganize tests", "consolidate scattered tests", or mentions test cases scattered in business code that need to be moved to proper test directories.
version: 0.1.0
---

# Test Case Organizer

## Purpose

This skill organizes and consolidates scattered test cases found in business code into proper test directories following standard testing conventions. It addresses the common issue where AI models or developers write test cases directly in business logic files instead of dedicated test directories.

## When to Use This Skill

Use this skill when:
- Test cases are scattered across business code files
- Tests need to be reorganized into proper test directory structure
- Consolidating tests after AI-generated code mixed tests with business logic
- Establishing standardized test organization in a project
- Migrating from ad-hoc testing to structured test suites

## Workflow Overview

The test case organization process follows these steps:

### 1. Scan for Test Directory

Start by identifying existing test directories in the codebase:

```bash
python scripts/organize_tests.py --scan
```

The script searches for common test directory patterns:
- `tests/`, `test/`
- `__tests__/`
- `spec/`, `specs/`
- Language-specific patterns (e.g., `src/test/` for Java)

**If no test directory exists:**
- Report missing test directory to user
- Suggest standard test directory structure based on project type
- Wait for user confirmation that test directory has been created
- Continue with organization once confirmed

### 2. Identify Scattered Test Cases

Scan business code directories for test patterns:
- Functions/methods with `test_`, `Test`, `should_`, `it_` prefixes
- Files containing test assertions (`assert`, `expect`, `should`)
- Inline test code blocks
- Test decorators (`@pytest.mark`, `@Test`, `describe()`)

### 3. Classify and Categorize

Automatically classify test cases by:
- **Business domain**: Group by feature area or module
- **Test type**: Unit tests, integration tests, e2e tests
- **Test scope**: Component-level, service-level, system-level
- **File associations**: Tests for specific business files

Refer to `references/organization-rules.md` for detailed classification criteria.

### 4. Create Test File Structure

Generate organized test files:
- Create subdirectories matching business code structure
- Name test files following conventions (e.g., `test_module.py`, `module.test.js`)
- Group related tests into appropriate test files
- Preserve test metadata and context

### 5. Move and Refactor Test Cases

Extract test cases from business code:
- Remove test code from business files
- Place tests in corresponding test files
- Update import statements and dependencies
- Maintain test functionality and coverage

### 6. Validate Test Execution

Execute reorganized tests to ensure correctness:
- Run test suite to verify all tests still pass
- Check for broken imports or missing dependencies
- Validate test discovery by test runners
- Report any failing tests for manual review

### 7. Generate Organization Report

Produce summary of organization actions:
- Number of test cases moved
- Source and destination file mappings
- Test classification breakdown
- Execution results and coverage impact
- Recommendations for further improvements

## Using the Automation Script

The `scripts/organize_tests.py` script automates the entire workflow:

### Basic Usage

```bash
# Full automated organization
python scripts/organize_tests.py --auto

# Interactive mode with confirmations
python scripts/organize_tests.py --interactive

# Dry run to preview changes
python scripts/organize_tests.py --dry-run
```

### Command Options

- `--scan`: Only scan and report test locations
- `--classify`: Scan and classify without moving
- `--execute`: Run tests after organization
- `--report-only`: Generate report without making changes
- `--test-dir <path>`: Specify custom test directory location

### Script Output

The script generates:
- **Console report**: Real-time progress and summary
- **organization_report.md**: Detailed markdown report
- **test_mapping.json**: Source-to-destination file mappings
- **failed_tests.log**: Any tests that failed after reorganization

## Classification Rules

Consult `references/organization-rules.md` for comprehensive classification rules including:

- **Naming conventions**: Test file and function naming standards
- **Directory structure**: Standard test organization patterns
- **Test categorization**: Criteria for grouping tests by type and scope
- **Framework-specific rules**: pytest, Jest, JUnit, RSpec conventions
- **Best practices**: Testing anti-patterns to avoid

## Post-Organization Steps

After organization completes:

1. **Review the report**: Check `organization_report.md` for details
2. **Fix failing tests**: Address any tests broken during migration
3. **Update CI/CD**: Ensure test runners find new test locations
4. **Update documentation**: Reflect new test organization in project docs
5. **Configure test coverage**: Update coverage tool configurations
6. **Commit changes**: Create organized commit with clear description

## Handling Edge Cases

### Mixed Test and Business Logic

When functions contain both business logic and test assertions:
- Extract only test-specific code
- Preserve business logic in original location
- Create wrapper tests if needed

### Parameterized or Data-Driven Tests

For tests with external data dependencies:
- Move test data files alongside test files
- Update data file paths in test code
- Maintain test data organization

### Test Utilities and Fixtures

Shared test utilities require special handling:
- Create `conftest.py` (pytest) or test utility modules
- Place shared fixtures in accessible locations
- Update imports across test files

### Language-Specific Considerations

Different languages have different conventions - consult references for:
- Python: pytest, unittest patterns
- JavaScript/TypeScript: Jest, Mocha, Jasmine patterns
- Java: JUnit, TestNG patterns
- Go: standard testing package patterns
- Ruby: RSpec, Minitest patterns

## Integration with Development Workflow

This skill integrates with broader development practices:

- Run before major refactoring to establish test baseline
- Use during code reviews to enforce test organization standards
- Apply when onboarding new team members to demonstrate test structure
- Execute periodically to catch test drift

## Additional Resources

### Reference Files

- **`references/organization-rules.md`**: Comprehensive classification and organization rules

### Script Files

- **`scripts/organize_tests.py`**: Full automation script for test organization workflow

## Example Workflow

Typical usage flow:

1. User requests: "测试用例整理" or "organize test cases"
2. Execute scan: `python scripts/organize_tests.py --scan`
3. If no test directory, prompt user to create one
4. User confirms test directory created
5. Run full organization: `python scripts/organize_tests.py --auto --execute`
6. Review `organization_report.md`
7. Fix any failing tests
8. Report completion summary to user

## Success Criteria

Organization is complete when:
- ✓ All scattered test cases moved to test directory
- ✓ Tests organized by logical categorization
- ✓ All tests execute successfully in new locations
- ✓ Test runners can discover and run all tests
- ✓ Organization report generated
- ✓ No business code contains test logic

## Common Issues and Solutions

**Issue**: Tests fail after moving due to import errors
- **Solution**: Script automatically updates relative imports; manually verify complex imports

**Issue**: Test discovery fails in new location
- **Solution**: Ensure test file naming follows framework conventions (e.g., `test_*.py` for pytest)

**Issue**: Shared test fixtures not accessible
- **Solution**: Create proper fixture files (`conftest.py` for pytest) in appropriate directory levels

**Issue**: Test data files not found
- **Solution**: Script attempts to move data files; verify paths and update if needed

Follow the workflow systematically to achieve clean, maintainable test organization that improves code quality and test discoverability.
