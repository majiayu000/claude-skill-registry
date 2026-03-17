---
name: test
description: Load testing framework configurations with patterns, tools, and examples. Supports unit, int (integration), e2e, bdd, perf (performance).
argument-hint: "<type> - Choose: unit, int, e2e, bdd, perf"
---

# Testing Framework Loader

When invoked with `/test <type>`, load the corresponding testing configuration.

**Configuration File**: `C:\.claude\testing\testing-frameworks.yaml`

## Supported Testing Types

### @test:unit (or /test unit)
**Purpose**: Test individual units in isolation

**Tools by Stack**:
- .NET: xUnit, NUnit, MSTest + Moq, NSubstitute
- Node.js: Jest, Vitest + ts-jest
- Python: pytest + pytest-mock
- Java: JUnit 5 + Mockito
- Go: go test + testify

**Patterns**:
- Arrange-Act-Assert (AAA)
- Given-When-Then
- Test doubles (mocks, stubs, fakes)
- Coverage thresholds (>80%)

### @test:int (or /test int)
**Purpose**: Test component integration

**Tools**:
- .NET: WebApplicationFactory, TestServer
- Node.js: Supertest
- Python: pytest with TestClient
- Java: Spring Boot Test
- All: Testcontainers

**Patterns**:
- Database integration (in-memory or containers)
- API endpoint testing
- Message queue integration
- External service mocking

### @test:e2e (or /test e2e)
**Purpose**: Test complete user flows

**Tools**:
- Playwright (recommended)
- Cypress
- Selenium

**Patterns**:
- Page Object Model
- Test data management
- Visual regression testing
- Cross-browser testing
- Mobile responsive testing

### @test:bdd (or /test bdd)
**Purpose**: Behavior-Driven Development

**Tools**:
- .NET: SpecFlow
- Node.js: Cucumber.js
- Python: Behave, pytest-bdd
- Java: Cucumber-JVM

**Patterns**:
- Feature files (Gherkin syntax)
- Step definitions
- Scenario outlines
- Living documentation

**Example**:
```gherkin
Feature: User Login
  Scenario: Successful login
    Given a registered user
    When they enter valid credentials
    Then they should see the dashboard
```

### @test:perf (or /test perf)
**Purpose**: Performance and load testing

**Tools**:
- k6 (recommended)
- JMeter
- Gatling
- Artillery

**Patterns**:
- Load testing (sustained traffic)
- Stress testing (breaking point)
- Spike testing (sudden bursts)
- Soak testing (extended duration)

**Metrics**:
- Response time (p50, p95, p99)
- Throughput (RPS)
- Error rate
- Resource utilization

## Usage
1. Load testing type: `/test unit`
2. Get tools, patterns, and examples for your stack
3. Combine: `@test:unit @test:int @dotnet`
