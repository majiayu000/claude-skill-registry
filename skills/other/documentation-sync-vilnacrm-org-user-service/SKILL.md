---
name: documentation-sync
description: Keep documentation in sync with code changes. Use when implementing features, modifying APIs, changing architecture, adding configuration, updating security, or making any changes that affect user-facing or developer-facing documentation.
---

# Documentation Synchronization Skill

## Overview

This skill ensures documentation in the `docs/` directory remains synchronized with codebase changes, maintaining accuracy and completeness for both users and developers.

## Core Principle

**Documentation is part of the definition of done**. No code change is complete until the relevant documentation is updated.

## When to Use This Skill

Activate this skill when:

- **API Changes**: Adding/modifying REST or GraphQL endpoints
- **Database Changes**: Adding entities, modifying schema
- **Architecture Changes**: Changing design patterns, component structure
- **Configuration Changes**: Adding environment variables, config options
- **Security Changes**: Modifying authentication, authorization
- **Testing Changes**: Adding test strategies, new test types
- **Performance Changes**: Optimizations, benchmarking
- **Feature Implementation**: New user-facing features

## Core Documentation Files

### API and Integration

| File                    | Purpose                         | Update When      |
| ----------------------- | ------------------------------- | ---------------- |
| `docs/api-endpoints.md` | REST/GraphQL endpoints, schemas | API changes      |
| `docs/user-guide.md`    | User-facing features            | Feature changes  |
| `docs/security.md`      | Auth, authorization             | Security changes |

### Architecture and Design

| File                              | Purpose                 | Update When          |
| --------------------------------- | ----------------------- | -------------------- |
| `docs/design-and-architecture.md` | System design, patterns | Architecture changes |
| `docs/developer-guide.md`         | Dev patterns, examples  | Dev workflow changes |
| `docs/glossary.md`                | Domain terminology      | New domain concepts  |

### Operations and Configuration

| File                             | Purpose             | Update When    |
| -------------------------------- | ------------------- | -------------- |
| `docs/advanced-configuration.md` | Env vars, config    | Config changes |
| `docs/getting-started.md`        | Setup, installation | Setup changes  |
| `docs/operational.md`            | Monitoring, logging | Ops changes    |

### Development

| File                  | Purpose                   | Update When      |
| --------------------- | ------------------------- | ---------------- |
| `docs/testing.md`     | Test strategies           | Test changes     |
| `docs/performance.md` | Benchmarks, optimizations | Performance work |
| `docs/onboarding.md`  | New dev onboarding        | Process changes  |

### Versioning

| File                    | Purpose      | Update When         |
| ----------------------- | ------------ | ------------------- |
| `docs/versioning.md`    | Version info | Version bumps       |
| `docs/release-notes.md` | Changelog    | Significant changes |

## Documentation Update Workflow

### Quick Reference

**For each code change**:

1. **Identify Impact**: Which docs need updates?
2. **Update Content**: Follow scenario-specific patterns
3. **Cross-Reference**: Ensure links remain valid
4. **Validate Examples**: Test all code samples
5. **Review Checklist**: Use pre-commit checklist

### Common Update Scenarios

| Change Type           | Primary Docs                                | Commands                     | Guide                                                                               |
| --------------------- | ------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------- |
| **REST Endpoint**     | `api-endpoints.md`                          | `make generate-openapi-spec` | [api-endpoints.md](update-scenarios/api-endpoints.md)                               |
| **GraphQL Operation** | `api-endpoints.md`                          | `make generate-graphql-spec` | [api-endpoints.md](update-scenarios/api-endpoints.md)                               |
| **Database Schema**   | `design-and-architecture.md`                | -                            | [database-and-architecture.md](update-scenarios/database-and-architecture.md)       |
| **Domain Model**      | `design-and-architecture.md`, `glossary.md` | -                            | [database-and-architecture.md](update-scenarios/database-and-architecture.md)       |
| **Configuration**     | `advanced-configuration.md`                 | -                            | [configuration-and-operations.md](update-scenarios/configuration-and-operations.md) |
| **Authentication**    | `security.md`, `api-endpoints.md`           | -                            | [configuration-and-operations.md](update-scenarios/configuration-and-operations.md) |
| **Testing**           | `testing.md`                                | -                            | [configuration-and-operations.md](update-scenarios/configuration-and-operations.md) |
| **Performance**       | `performance.md`                            | -                            | [configuration-and-operations.md](update-scenarios/configuration-and-operations.md) |

**See detailed guides**: [update-scenarios/](update-scenarios/) directory

## Documentation Quality Standards

### Consistency

- ✅ Follow existing doc structure and formatting
- ✅ Use terminology from `docs/glossary.md`
- ✅ Include code examples with syntax highlighting
- ✅ Add cross-references to related sections

### Completeness

- ✅ Document all public APIs and endpoints
- ✅ Include error handling and edge cases
- ✅ Provide basic and advanced examples
- ✅ Update version info when needed

### Maintenance

- ✅ Remove outdated information
- ✅ Update release notes for significant changes
- ✅ Validate all links and references
- ✅ Update diagrams if architecture changes

**See detailed standards**: [reference/quality-standards.md](reference/quality-standards.md)

## Pre-Commit Checklist

Before committing code with documentation updates:

- [ ] **Identify Impact**: Determine which docs need updates
- [ ] **Update Content**: Apply scenario-specific patterns
- [ ] **Cross-Reference**: Verify all links remain valid
- [ ] **Test Examples**: Run all code examples
- [ ] **Check Consistency**: Verify terminology matches glossary
- [ ] **Update Specs**: Run `make generate-openapi-spec` or `make generate-graphql-spec` if needed
- [ ] **Review Changes**: Ensure completeness and accuracy

**See complete workflow**: [reference/workflow-checklist.md](reference/workflow-checklist.md)

## Integration with Development

### During Development

**Documentation is code**:

- Update docs in same PR as code changes
- Test documentation examples
- Validate links and references

### During Code Review

**Reviewers check**:

- Documentation accuracy
- Completeness of examples
- Terminology consistency
- Link validity

### During CI/CD

**Automated checks**:

- Documentation links validation
- Example code syntax checking
- Spec generation and validation

## Supporting Files

For detailed guides, examples, and standards:

- **[update-scenarios/api-endpoints.md](update-scenarios/api-endpoints.md)** - REST and GraphQL documentation
- **[update-scenarios/database-and-architecture.md](update-scenarios/database-and-architecture.md)** - Schema and design docs
- **[update-scenarios/configuration-and-operations.md](update-scenarios/configuration-and-operations.md)** - Config, security, testing, performance
- **[reference/quality-standards.md](reference/quality-standards.md)** - Documentation quality guidelines
- **[reference/workflow-checklist.md](reference/workflow-checklist.md)** - Complete update workflow

## Success Criteria

- ✅ All affected docs updated
- ✅ Code examples tested and working
- ✅ Links and references valid
- ✅ Terminology consistent
- ✅ Release notes updated
- ✅ Docs reflect actual code behavior
