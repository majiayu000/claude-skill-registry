---
name: tdd_workflow
router_kit: QualityKit
description: Comprehensive Test Driven Development guide. Master testing, debugging, fixing bugs, QA workflows, unit tests, integration tests, and coverage analysis.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, tdd workflow, testing, utilities, version control, workflow]      - pytest
---

# TDD Guide - Test Driven Development for Engineering Teams

A comprehensive Test Driven Development skill that provides intelligent test generation, coverage analysis, framework integration, and TDD workflow guidance across multiple languages and testing frameworks.

## Capabilities

### Test Generation
- **Generate Test Cases from Requirements**: Convert user stories, API specs, and business requirements into executable test cases
- **Create Test Stubs**: Generate test function scaffolding with proper naming, imports, and setup/teardown
- **Generate Test Fixtures**: Create realistic test data, mocks, and fixtures for various scenarios

### TDD Workflow Support
- **Guide Red-Green-Refactor**: Step-by-step guidance through TDD cycles with validation
- **Suggest Missing Scenarios**: Identify untested edge cases, error conditions, and boundary scenarios
- **Review Test Quality**: Analyze test isolation, assertions quality, naming conventions, and maintainability

### Coverage & Metrics Analysis
- **Calculate Coverage**: Parse LCOV, JSON, and XML coverage reports for line/branch/function coverage
- **Identify Untested Paths**: Find code paths, branches, and error handlers without test coverage
- **Recommend Improvements**: Prioritized recommendations (P0/P1/P2) for coverage gaps and test quality

### Framework Integration
- **Multi-Framework Support**: Jest, Pytest, JUnit, Vitest, Mocha, RSpec adapters
- **Generate Boilerplate**: Create test files with proper imports, describe blocks, and best practices
- **Configure Test Runners**: Set up test configuration, coverage tools, and CI integration

### Comprehensive Metrics
- **Test Coverage**: Line, branch, function coverage with gap analysis
- **Code Complexity**: Cyclomatic complexity, cognitive complexity, testability scoring
- **Test Quality**: Assertions per test, isolation score, naming quality, test smell detection
- **Test Data**: Boundary value analysis, edge case identification, mock data generation
- **Test Execution**: Timing analysis, slow test detection, flakiness detection
- **Missing Tests**: Uncovered edge cases, error handling gaps, missing integration scenarios

## Input Requirements

The skill supports **automatic format detection** for flexible input:

### Source Code
- **Languages**: TypeScript, JavaScript, Python, Java
- **Format**: Direct file paths or copy-pasted code blocks
- **Detection**: Automatic language/framework detection from syntax and imports

### Test Artifacts
- **Coverage Reports**: LCOV (.lcov), JSON (coverage-final.json), XML (cobertura.xml)
- **Test Results**: JUnit XML, Jest JSON, Pytest JSON, TAP format
- **Format**: File paths or raw coverage data

### Requirements (Optional)
- **User Stories**: Text descriptions of functionality
- **API Specifications**: OpenAPI/Swagger, REST endpoints, GraphQL schemas
- **Business Requirements**: Acceptance criteria, business rules

### Input Methods
- **Option A**: Provide file paths (skill will read files)
- **Option B**: Copy-paste code/data directly
- **Option C**: Mix of both (automatically detected)

## Output Formats

The skill provides **context-aware output** optimized for your environment:

### Code Files
- **Test Files**: Generated tests (Jest/Pytest/JUnit/Vitest) with proper structure
- **Fixtures**: Test data files, mock objects, factory functions
- **Mocks**: Mock implementations, stub functions, test doubles

### Reports
- **Markdown**: Rich coverage reports, recommendations, quality analysis (Claude Desktop)
- **JSON**: Machine-readable metrics, structured data for CI/CD integration
- **Terminal-Friendly**: Simplified output for Claude Code CLI

### Smart Defaults
- **Desktop/Apps**: Rich markdown with tables, code blocks, visual hierarchy
- **CLI**: Concise, terminal-friendly format with clear sections
- **CI/CD**: JSON output for automated processing

### Progressive Disclosure
- **Summary First**: High-level overview (<200 tokens)
- **Details on Demand**: Full analysis available (500-1000 tokens)
- **Prioritized**: P0 (critical) → P1 (important) → P2 (nice-to-have)

## How to Use

### Basic Usage
```
@tdd-guide

I need tests for my authentication module. Here's the code:
[paste code or provide file path]

Generate comprehensive test cases covering happy path, error cases, and edge cases.
```

### Coverage Analysis
```
@tdd-guide

Analyze test coverage for my TypeScript project. Coverage report: coverage/lcov.info

Identify gaps and provide prioritized recommendations.
```

### TDD Workflow
```
@tdd-guide

Guide me through TDD for implementing a password validation function.

Requirements:
- Min 8 characters
- At least 1 uppercase, 1 lowercase, 1 number, 1 special char
- No common passwords
```

### Multi-Framework Support
```
@tdd-guide

Convert these Jest tests to Pytest format:
[paste Jest tests]
```

## Scripts

### Core Modules

- **test_generator.py**: Intelligent test case generation from requirements and code
- **coverage_analyzer.py**: Parse and analyze coverage reports (LCOV, JSON, XML)
- **metrics_calculator.py**: Calculate comprehensive test and code quality metrics
- **framework_adapter.py**: Multi-framework adapter (Jest, Pytest, JUnit, Vitest)
- **tdd_workflow.py**: Red-green-refactor workflow guidance and validation
- **fixture_generator.py**: Generate realistic test data and fixtures
- **format_detector.py**: Automatic language and framework detection

### Utilities

- **complexity_analyzer.py**: Cyclomatic and cognitive complexity analysis
- **test_quality_scorer.py**: Test quality scoring (isolation, assertions, naming)
- **missing_test_detector.py**: Identify untested paths and missing scenarios
- **output_formatter.py**: Context-aware output formatting (Desktop vs CLI)

## 🔄 Workflow

> **Kaynak:** [Kent Beck - Test Driven Development by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/) & [Google Testing Blog](https://testing.googleblog.com/)

### Aşama 1: RED - Test-First Approach
- [ ] **Interface Design**: Kodun nasıl çalışması gerektiğini (Input/Output) belirle ve testi yaz.
- [ ] **Fail Confirmation**: Testi çalıştır ve kod henüz yazılmadığı için başarısız (Red) olduğunu gör.
- [ ] **Assertion Clarity**: Testin neden başarısız olduğunu açıklayan net bir hata mesajı aldığından emin ol.

### Aşama 2: GREEN - Implementation
- [ ] **Minimal Code**: Sadece testin geçmesi için gereken en basit/minimal kodu yaz.
- [ ] **Pass Verification**: Tüm testlerin "Yeşil" döndüğünü doğrula.
- [ ] **Avoid Over-Engineering**: Test kapsamı dışında kalan özellikleri implement etme.

### Aşama 3: REFACTOR - Clean Code
- [ ] **Code Cleanup**: Kodu SOLID prensiplerine göre optimize et, isimlendirmeleri düzelt.
- [ ] **Test Refinement**: Testlerin okunabilirliğini artır, tekrarları (`setup/teardown`) optimize et.
- [ ] **Regression Check**: Her refactoring adımından sonra testlerin hala yeşil olduğunu doğrula.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Testler "Implementation Details" yerine "Behavior"ı mı test ediyor? |
| 2 | Her test fonksiyonu bağımsız (Isolated) mı? |
| 3 | Kod coverage hedefine (%80+) ulaşıldı mı? |

---
*TDD Workflow v2.0 - With Workflow*
