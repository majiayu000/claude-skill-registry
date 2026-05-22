---
name: go-development
description: "Production-grade Go development patterns for building resilient services. Use when developing Go applications, implementing job schedulers, Docker integrations, LDAP clients, or needing patterns for resilience, testing, and performance optimization. By Netresearch."
---

# Go Development Patterns

## When to Use

- Building Go services or CLI applications
- Implementing job scheduling or task orchestration
- Integrating with Docker API
- Building LDAP/Active Directory clients
- Designing resilient systems with retry logic
- Setting up comprehensive test suites

## Required Workflow

**For comprehensive reviews, ALWAYS invoke these related skills:**

1. **Security audit** - Invoke `/netresearch-skills-bundle:security-audit` for OWASP analysis, vulnerability assessment, and security patterns
2. **Enterprise readiness** - Invoke `/netresearch-skills-bundle:enterprise-readiness` for OpenSSF Scorecard, SLSA compliance, supply chain security
3. **GitHub project setup** - Invoke `/netresearch-skills-bundle:github-project` for branch protection, rulesets, CI workflow validation

A Go development review is NOT complete until all related skills have been executed.

## Core Principles

### Type Safety

- **Avoid:** `interface{}`, `sync.Map`, scattered type assertions, reflection
- **Prefer:** Generics `[T any]`, concrete types, compile-time verification

### Consistency

- One pattern per problem domain
- Match existing codebase patterns
- Refactor holistically or not at all

### Conventions

- Errors: lowercase, no punctuation (`errors.New("invalid input")`)
- Naming: ID, URL, HTTP (not Id, Url, Http)
- Error wrapping: `fmt.Errorf("failed to process: %w", err)`

## References

Load these as needed for detailed patterns and examples:

| Reference | Purpose |
|-----------|---------|
| `references/architecture.md` | Package structure, config management, middleware chains |
| `references/resilience.md` | Retry logic, graceful shutdown, context propagation |
| `references/docker.md` | Docker client patterns, buffer pooling |
| `references/ldap.md` | LDAP/Active Directory integration |
| `references/testing.md` | Test strategies, build tags, table-driven tests |
| `references/linting.md` | golangci-lint v2, staticcheck, code quality |
| `references/api-design.md` | Bitmask options, functional options, builders |
| `references/fuzz-testing.md` | Go fuzzing patterns, security seeds |
| `references/mutation-testing.md` | Gremlins configuration, test quality measurement |
| `references/makefile.md` | Standard Makefile interface for CI/CD |

## Quality Gates

Run these checks before completing any review:

```bash
golangci-lint run --timeout 5m    # Linting
go vet ./...                       # Static analysis
staticcheck ./...                  # Additional checks
govulncheck ./...                  # Vulnerability scan
go test -race ./...                # Race detection
```

---

> **Contributing:** Submit improvements to https://github.com/netresearch/go-development-skill
