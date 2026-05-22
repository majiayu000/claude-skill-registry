---
name: testing
description: |
    Use when choosing a testing strategy, right-sizing test coverage, or understanding test categories. Covers the Test Trophy model, test type tradeoffs, and guidance on balancing static analysis, unit, integration, and end-to-end tests.
    USE FOR: testing strategy, Test Trophy, test type selection, right-sizing test coverage, balancing test categories, choosing testing tools, test automation architecture
    DO NOT USE FOR: specific test category implementation (use static-analysis, unit-testing, integration-testing, e2e-testing, etc.), BDD specification authoring (use specs/documentation/gherkin)
license: MIT
metadata:
  displayName: "Testing Strategy"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Kent C. Dodds — Write Tests. Not Too Many. Mostly Integration."
    url: "https://kentcdodds.com/blog/write-tests"
  - title: "Martin Fowler — Test Pyramid"
    url: "https://martinfowler.com/articles/practical-test-pyramid.html"
---

# Testing Strategy — The Test Trophy

## Overview
The **Test Trophy** (Kent C. Dodds) is a modern testing strategy that prioritizes integration tests over unit tests, reflecting how today's tooling has shifted the cost/confidence tradeoffs of each test category.

> "Write tests. Not too many. Mostly integration." — Kent C. Dodds

## The Test Trophy

```
                  ┌───────┐
                  │  E2E  │  Few, high-confidence, slow, expensive
                 ─┴───────┴─
               ┌─────────────┐
               │ Integration  │  Most tests here — best ROI
              ─┴─────────────┴─
            ┌───────────────────┐
            │       Unit        │  Isolated logic, fast, cheap
           ─┴───────────────────┴─
         ┌───────────────────────────┐
         │     Static Analysis       │  Free — catches bugs at write time
         └───────────────────────────┘
```

## Test Categories

| Category | What It Tests | Speed | Confidence | Cost |
|----------|--------------|-------|------------|------|
| **Static Analysis** | Types, syntax, lint rules, security patterns | Instant | Low-Medium | Free |
| **Unit** | Individual functions/classes in isolation | Fast | Medium | Low |
| **Integration** | Multiple units working together | Medium | High | Medium |
| **E2E** | Full user flows through the real system | Slow | Very High | High |

### Beyond the Trophy
| Category | What It Tests | When to Use |
|----------|--------------|-------------|
| **Contract** | API compatibility between services | Microservices / distributed systems |
| **API** | HTTP endpoints directly | REST/GraphQL APIs |
| **Performance** | Load, stress, scalability | Before launch, capacity planning |
| **Visual** | UI appearance / regression | Design systems, component libraries |
| **Accessibility** | WCAG compliance, screen readers | All user-facing apps |
| **Acceptance** | Business requirements (BDD) | Stakeholder-facing features |
| **Chaos** | System resilience under failure | Distributed systems, microservices |

## Right-Sizing Your Tests

### The Trophy Distribution
Allocate effort roughly proportional to the Trophy shape:

| Category | % of Tests | Rationale |
|----------|-----------|-----------|
| Static Analysis | Always on | Zero-cost, catches trivial bugs |
| Unit | ~20% | Pure logic, algorithms, edge cases |
| Integration | ~50% | Best confidence-per-dollar |
| E2E | ~20% | Critical user journeys only |
| Other (contract, perf, a11y, visual) | ~10% | As needed per project type |

### When to Shift the Balance

| Project Type | Emphasize | Reduce |
|-------------|-----------|--------|
| Library / SDK | Unit tests (public API surface) | E2E (no UI) |
| Microservices | Contract + integration | E2E (too many services) |
| Monolithic web app | Integration + E2E | Contract (single deploy) |
| Design system | Visual + accessibility | Performance |
| Real-time / trading | Performance + unit | Visual |
| Regulated / healthcare | Acceptance (BDD) + integration | — |

## Cross-Platform Tool Landscape

### Static Analysis
| Tool | Languages |
|------|-----------|
| TypeScript | JS/TS (type checking) |
| ESLint / Biome | JS/TS (linting) |
| Roslyn Analyzers | C# |
| Pylint / Ruff / mypy | Python |
| Semgrep | Multi-language SAST |

### Unit Testing
| Tool | Languages |
|------|-----------|
| Vitest / Jest | JS/TS |
| xUnit / NUnit / MSTest | C# |
| pytest | Python |
| JUnit / TestNG | Java |
| Go test | Go |

### Integration Testing
| Tool | Languages |
|------|-----------|
| Testcontainers | Java, .NET, Node, Python, Go |
| Vitest / Jest | JS/TS |
| xUnit + WebApplicationFactory | C# / ASP.NET |
| pytest | Python |

### E2E Testing
| Tool | Platforms |
|------|-----------|
| Playwright | Web (Chromium, Firefox, WebKit) |
| Cypress | Web (Chromium-based) |
| Selenium | Web (all browsers) |
| Appium | Mobile (iOS, Android) |
| Maestro | Mobile (iOS, Android) |

### Contract Testing
| Tool | Type |
|------|------|
| Pact | Consumer-driven contracts |
| PactFlow | Bi-directional contract testing |
| Spring Cloud Contract | JVM contract testing |

### API Testing
| Tool | Format |
|------|--------|
| .http files | VS Code / JetBrains REST Client |
| Bruno | Git-friendly API collections |
| Postman / Newman | Collections + CLI runner |
| REST Client (VS Code) | Inline .http files |
| k6 | Scripted API + load testing |

### Performance Testing
| Tool | Type |
|------|------|
| k6 (Grafana) | Load / stress (JS scripts) |
| JMeter | Load / stress (GUI + CLI) |
| Gatling | Load / stress (Scala/Java) |
| Artillery | Load / stress (YAML config) |
| Lighthouse | Web performance audit |

### Visual Testing
| Tool | Integration |
|------|-------------|
| Chromatic | Storybook visual regression |
| Percy (BrowserStack) | Cross-browser visual diffs |
| BackstopJS | CSS regression (headless) |
| Playwright screenshots | Custom visual assertions |

### Accessibility Testing
| Tool | Type |
|------|------|
| axe-core / @axe-core/playwright | Automated WCAG checks |
| Pa11y | CLI accessibility audits |
| Lighthouse | Accessibility scoring |
| Storybook addon-a11y | Component-level checks |

### Acceptance Testing (BDD)
| Tool | Languages |
|------|-----------|
| Cucumber | Java, JS, Ruby |
| SpecFlow / Reqnroll | C# |
| Behave | Python |
| Gauge | Multi-language (Markdown specs) |
| Godog | Go |

### Chaos Testing
| Tool | Type |
|------|------|
| Chaos Monkey | Random VM termination (Netflix) |
| Gremlin | SaaS fault injection platform |
| Litmus | Kubernetes chaos engineering (CNCF) |
| Chaos Mesh | Kubernetes fault injection |
| Toxiproxy | TCP proxy for network faults |
| AWS Fault Injection Service | AWS-native chaos |
| Azure Chaos Studio | Azure-native chaos |

## Test Automation Architecture

```
CI Pipeline
  │
  ├── Static Analysis ──► ESLint + TypeScript + Semgrep (on every commit)
  │
  ├── Unit Tests ────────► Vitest / xUnit / pytest (on every commit)
  │
  ├── Integration Tests ─► Testcontainers + API tests (on every PR)
  │
  ├── Contract Tests ────► Pact verify (on every PR)
  │
  ├── E2E Tests ─────────► Playwright critical paths (on merge to main)
  │
  ├── Visual Tests ──────► Chromatic snapshot comparison (on every PR)
  │
  ├── A11y Tests ────────► axe-core in Playwright (on every PR)
  │
  ├── Performance Tests ─► k6 load tests (nightly / pre-release)
  │
  └── Chaos Tests ────────► Litmus / Gremlin experiments (pre-release / game days)
```

## Best Practices
- Follow the Test Trophy shape — invest most in integration tests, not unit tests.
- Run static analysis on every keystroke (IDE) and every commit (CI) — it's free confidence.
- Write E2E tests only for critical user journeys — they're expensive to maintain.
- Use contract tests instead of E2E for verifying service boundaries in microservices.
- Use Testcontainers for integration tests that need real databases, message brokers, or caches.
- Use .http files or Bruno for API testing that's version-controlled alongside the code.
- Run performance tests regularly (nightly or pre-release), not just before launch.
- Include accessibility testing in CI — axe-core catches >50% of WCAG violations automatically.
- Use BDD/Gherkin for features where business stakeholders need to verify acceptance criteria.
- Keep test data factories close to the tests — avoid shared global test fixtures.
- Use chaos engineering to verify resilience assumptions — inject real faults in staging and production with controlled blast radius.
