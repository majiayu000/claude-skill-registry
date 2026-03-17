---
name: testing
description: Automated test generation, review, and execution for pytest-based projects. Auto-activates on keywords test, coverage, pytest, unittest, integration test, e2e, performance, benchmark, security testing. Routes to specialized testing workflows based on user intent.
allowed-tools: Read, Write, Bash(pytest:*, coverage:*, find:*, grep:*), Task
---

# Testing Skill

Comprehensive testing domain for pytest-based projects. Provides test generation, review, execution, and specialized testing workflows with automatic routing based on user intent.

## Auto-Activation Keywords

This skill activates automatically when you mention:
- test, tests, testing
- coverage, test coverage
- pytest, unittest
- integration test, unit test, e2e test
- performance test, benchmark, load test
- security test, penetration test
- test review, test quality

## Routing Logic

Based on user intent, this skill routes to appropriate workflows:

### Test Generation
**Keywords**: "generate tests", "create tests", "write tests", "test coverage"
- **Simple test generation** → Use `/testing/generate` workflow
- **Complex test strategy** → Invoke `test-engineer` agent

### Test Review
**Keywords**: "review tests", "test quality", "coverage gaps", "improve tests"
- **Review existing tests** → Use `/testing/review` workflow
- **Comprehensive quality audit** → Invoke `test-engineer` agent

### End-to-End Testing
**Keywords**: "e2e test", "end-to-end", "full workflow", "integration test", "pipeline test"
- **E2E test generation** → Use `/testing/e2e` workflow
- **Complex multi-component** → Invoke `test-engineer` agent

### Performance Testing
**Keywords**: "performance test", "benchmark", "load test", "memory usage", "speed test"
- **Performance test creation** → Use `/testing/performance` workflow
- **Comprehensive performance analysis** → Invoke `test-engineer` agent

### Security Testing
**Keywords**: "security test", "vulnerability", "penetration test", "OWASP", "injection"
- **Security test generation** → Use `/testing/security` workflow
- **Full security audit** → Invoke `security-auditor` agent

### Test Execution
**Keywords**: "run tests", "execute tests", "test results", "pytest command"
- **Quick reference** → See context/pytest-commands.md
- **Custom test execution** → Use bash with pytest commands

## Workflow Quick Reference

```bash
# Generate comprehensive tests
/testing/generate [module-path]

# Review test quality
/testing/review [test-directory]

# Create E2E tests
/testing/e2e [workflow-name]

# Create performance tests
/testing/performance [component]

# Create security tests
/testing/security [attack-vector]
```

## Complex Task Delegation

For complex multi-step testing tasks, invoke the `test-engineer` agent via Task tool:

```
Use test-engineer agent when:
- Designing comprehensive test strategy across multiple components
- Creating complete test suites from scratch (unit + integration + e2e)
- Optimizing test performance and coverage simultaneously
- Integrating multiple testing types (functional + performance + security)
```

## Supporting Context

- **Pytest patterns**: See `context/pytest-patterns.md` for common test patterns
- **Common commands**: See `context/pytest-commands.md` for frequently used commands
- **Coverage standards**: Minimum 80% coverage required (see `/standards/python.md`)

## Integration Points

### Agents
- **test-engineer**: Comprehensive test strategy and generation
- **security-auditor**: Security-focused testing and vulnerability analysis

### MCP Tools
- **mcp__zen-core__chat**: Multi-model consensus for complex test design decisions

### Hooks
- **TDD enforcement**: Pre-Write/Edit hook enforces test-first development

### Standards
- Python testing standards: `/standards/python.md` (80%+ coverage requirement)
- Linting standards: `/standards/linting.md` (pytest configuration)

## Testing Standards Summary

**Required for all projects:**
- Minimum 80% test coverage
- Unit tests in `tests/unit/` (< 1s each)
- Integration tests in `tests/integration/` (< 5s each)
- E2E tests in `tests/e2e/` (marked @pytest.mark.e2e)
- Proper pytest markers (@pytest.mark.unit, .integration, .slow, .security, .perf)
- AAA pattern (Arrange-Act-Assert)
- Clear test naming (test_should_[expected]_when_[condition])

**Fixture management:**
- Use existing fixtures from conftest.py
- No hardcoded test data
- Appropriate fixture scope (function, class, module, session)

**Test execution:**
```bash
# Standard test run with coverage
poetry run pytest -v --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=80

# Fast dev cycle (skip slow tests)
poetry run pytest -m "not slow"

# Specific test categories
poetry run pytest tests/unit/          # Unit tests only
poetry run pytest tests/integration/   # Integration tests
poetry run pytest -m security          # Security tests
poetry run pytest -m perf              # Performance tests
```

## Examples

**Example 1: Generate tests for new module**
```
User: "Generate comprehensive tests for the payment processor module"
→ Skill routes to /testing/generate workflow
→ Workflow creates unit, integration, and security tests
→ Ensures 80%+ coverage for payment processor
```

**Example 2: Review test quality**
```
User: "Review the tests for the authentication system and suggest improvements"
→ Skill routes to /testing/review workflow
→ Workflow analyzes coverage, patterns, fixture usage
→ Provides actionable recommendations
```

**Example 3: Complex test strategy**
```
User: "Design a comprehensive testing strategy for the new RAG pipeline"
→ Skill invokes test-engineer agent
→ Agent creates multi-tier testing approach:
  - Unit tests for embeddings, chunking, retrieval
  - Integration tests for pipeline flows
  - E2E tests for complete query-response cycles
  - Performance tests for large document handling
```

---

*This skill consolidates test-generator, test-reviewer, e2e-tester, performance-tester, and security-tester into a unified testing domain with intelligent routing.*
