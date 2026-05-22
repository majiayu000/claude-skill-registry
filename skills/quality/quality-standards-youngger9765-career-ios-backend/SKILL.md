---
name: quality-standards
description: |
  Quality assurance standards and AI collaboration principles for career_ios_backend.
  Automatically invoked when discussing code quality, standards, refactoring, or optimization.
  Trigger keywords: "quality", "refactor", "optimize", "best practices", "code review",
  "品質", "重構", "優化", "最佳實踐"

  Defines what's required vs. optional in prototype phase, and when to upgrade standards.
allowed-tools: [Read, Grep, Bash]
---

# Quality Standards Skill

## Purpose
Define quality assurance standards appropriate for the prototype phase, clarify AI-human collaboration boundaries, and guide the transition to production standards.

## Automatic Activation

This skill is AUTOMATICALLY activated when user mentions:
- ✅ "code quality" / "代碼品質"
- ✅ "refactor" / "重構"
- ✅ "optimize" / "優化"
- ✅ "best practices" / "最佳實踐"
- ✅ "code review" / "代碼審查"

---

## Quality Philosophy (Prototype Phase)

### Core Principle

> **"Prototype 求快不求完美。功能驗證完才追求品質。"**

**What we ARE doing**:
- ✅ Prototype backend API (not yet in production)
- ✅ Rapid feature validation
- ✅ AI-assisted development, human verification

**What we are NOT doing**:
- ❌ Production-grade system
- ❌ 100% test coverage
- ❌ Over-engineering

---

## Quality Standards: Must Do vs. Nice-to-Have

### ✅ Must Do (Minimum Requirements)

**These are NON-NEGOTIABLE even in prototype phase**:

1. **API Must Work**
   - All integration tests pass
   - Manual testing confirms functionality
   - No broken endpoints in console.html

2. **Code Formatting Consistency**
   - Ruff formatting applied (`ruff check --fix`)
   - Pre-commit hooks auto-fix style issues
   - Consistent code style across project

3. **No Obvious Bugs**
   - Manual testing + integration tests
   - Critical paths verified
   - User-facing features functional

4. **Security Basics**
   - No hardcoded credentials (pre-commit checks)
   - No API keys in code
   - Authentication on protected endpoints

5. **Integration Tests for Console APIs**
   - All 35+ console.html endpoints tested
   - At least 1 happy path test per endpoint
   - Current: 106+ tests covering major features

---

### ⚠️ Nice-to-Have (Defer Until Production)

**These can be deferred during prototype phase**:

- Type hint completeness (partial is OK)
- Test coverage percentage metrics
- Code complexity metrics
- Unit tests (only for complex business logic)
- Edge case tests (add before production)
- Performance optimization
- Comprehensive error handling

**Trade-off**: Speed now, quality later when we know the feature is valuable.

---

### ❌ Don't Do (Avoid Over-Engineering)

**Explicitly avoid these in prototype phase**:

- Aiming for 100% test coverage
- Excessive mocking in tests
- Over-engineered abstractions
- Premature optimization
- Comprehensive type checking (mypy can wait)
- Complex caching strategies
- Microservices architecture

**Why**: These slow down iteration without adding value during validation phase.

---

## AI-Human Collaboration Principles

### Human Responsibilities 👨‍💻

**Humans are better at**:

1. **Requirements Understanding**
   - What problem are we solving?
   - What's the business value?
   - What are edge cases?

2. **API Design**
   - Endpoint structure
   - Request/response formats
   - Authentication requirements

3. **Test-First (TDD)**
   - **Human writes tests** → Defines expected behavior
   - Tests are the contract/specification
   - AI cannot modify tests

4. **Code Review**
   - Does implementation match requirements?
   - Are there security issues?
   - Is code maintainable?

5. **Refactoring Decisions**
   - When to extract services
   - When to split files
   - Architecture changes

---

### AI Responsibilities 🤖

**AI is better at**:

1. **Generate Implementation Code**
   - Write code to pass human-written tests
   - Follow existing patterns in codebase
   - Generate boilerplate

2. **Format & Fix Style**
   - Run ruff check --fix
   - Consistent formatting
   - Import sorting

3. **Documentation Generation**
   - API documentation
   - Code comments (when needed)
   - Example usage

4. **Suggest Refactoring**
   - Identify code smells
   - Propose improvements
   - **But human decides** whether to apply

---

### TDD + AI Collaboration Flow

**The ideal workflow**:

```
1. Human: Define requirements + API design
   ↓
2. Human: Write test FIRST (RED)
   → Define expected behavior
   → Test must fail initially
   ↓
3. AI: Generate implementation to pass test (GREEN)
   → Minimal code to make test pass
   → Follow existing patterns
   ↓
4. Human: Review + Refactor (keep tests GREEN)
   → Verify implementation is correct
   → Improve code quality if needed
   → Tests remain passing
```

**CRITICAL RULE**:
- ⚠️ **AI CANNOT modify tests**
- ✅ Tests are human-written contracts
- ❌ Don't change tests to make code pass

---

## Code Quality Checklist

### Before Commit

- [ ] Integration tests pass locally
- [ ] Code follows existing patterns
- [ ] No hardcoded credentials or secrets
- [ ] Ruff formatting applied
- [ ] Commit message follows format
- [ ] On correct branch (not main/master)

### Before Push

- [ ] All integration tests pass (106+)
- [ ] No test regressions introduced
- [ ] Documentation updated (PRD, CHANGELOG)
- [ ] Pre-push smoke tests pass
- [ ] Ready for CI/CD pipeline

### Before Production (Future)

- [ ] Unit tests for complex logic
- [ ] Edge case tests added
- [ ] Security audit completed (OWASP)
- [ ] Performance testing done
- [ ] Type checking enabled (mypy)
- [ ] Test coverage ≥ 80%

---

## When to Upgrade Quality Standards

### Prototype → Production Transition

**Upgrade standards when**:
- ✅ Feature validation complete
- ✅ Ready for real users
- ✅ Need production reliability

**Checklist for Production**:

```yaml
Testing:
  - [ ] Add unit tests for critical business logic
  - [ ] Edge case tests for all APIs
  - [ ] Increase test coverage to 80%+
  - [ ] Add performance tests
  - [ ] Load testing

Code Quality:
  - [ ] Enable Mypy (type checking)
  - [ ] Fix all type errors
  - [ ] Comprehensive error handling
  - [ ] Logging and monitoring

Security:
  - [ ] Security audit (OWASP Top 10)
  - [ ] Penetration testing
  - [ ] Dependency vulnerability scan
  - [ ] Secrets management review

DevOps:
  - [ ] Set up pre-commit hooks for team
  - [ ] CI/CD pipeline hardening
  - [ ] Staging environment testing
  - [ ] Rollback procedures

Documentation:
  - [ ] API documentation complete
  - [ ] Deployment runbooks
  - [ ] Troubleshooting guides
  - [ ] Architecture diagrams
```

**Current Stage**: 🏗️ **Prototype** (above items NOT required yet)

---

## File Size Limits (Prevent Over-Growth)

To maintain modularity and code quality, enforce these limits:

| File Type | Max Lines | Action When Exceeded |
|-----------|-----------|---------------------|
| **API routes** | 300 | Refactor to service layer |
| **Services** | 400 | Split into multiple services |
| **Models** | 200 | Split into multiple model files |
| **Schemas** | 250 | Modularize by feature |
| **Tests** | 500 | Split by test category |

**Why**:
- Large files are hard to navigate
- Harder to test
- Higher merge conflict risk
- Poor separation of concerns

**How to refactor**:

```python
# ❌ Before: app/api/clients.py (450 lines)
# Everything in one file

# ✅ After: Split into layers
app/api/clients.py           # Routes only (150 lines)
app/services/client_service.py  # Business logic (200 lines)
app/repositories/client_repo.py  # Data access (100 lines)
```

---

## Ruff Configuration

**Automatic formatting and linting**:

```bash
# Auto-fix formatting issues
ruff check --fix app/

# Check specific file
ruff check app/api/clients.py

# Format on save (in your IDE)
# Pre-commit hook auto-runs ruff
```

**What Ruff catches**:
- Import sorting
- Unused imports/variables
- Line length violations
- Code style inconsistencies
- Common anti-patterns

---

## Code Review Standards

### What to Check

**Functionality**:
- [ ] Does it meet requirements?
- [ ] Are tests passing?
- [ ] Does it work in console.html?

**Quality**:
- [ ] Follows existing patterns?
- [ ] No obvious code smells?
- [ ] Reasonable complexity?

**Security**:
- [ ] No hardcoded secrets?
- [ ] Proper authentication checks?
- [ ] Input validation present?

**Maintainability**:
- [ ] Clear variable names?
- [ ] Comments where needed (not obvious code)?
- [ ] File size within limits?

### What NOT to Nitpick (Prototype Phase)

- Minor style preferences (ruff handles it)
- Missing type hints (not critical yet)
- Perfect error messages
- Comprehensive logging
- Performance micro-optimizations

---

## Speed-Quality Trade-Off

### 70-20-10 Rule (Prototype)

- **70% Development**: Writing features
- **20% QA**: Writing tests, manual testing
- **10% Refactoring**: Fixing issues, improving code

### Speed Priorities

**Fast iteration over**:
1. Feature validation
2. User feedback
3. API testing

**Deferred (but tracked)**:
1. Perfect architecture
2. Comprehensive tests
3. Performance tuning

**Quote from 2025 AI Development**:
> "Dream up an idea one day, functional prototype the next"

**Our approach**:
- Prototypes live in "buggy region" - speed prioritized
- Fix bugs as we find them
- Refine quality when feature proves valuable

---

## Quality Metrics (Prototype)

### Success Metrics ✅

- **100% of console.html APIs** have integration tests
- **All commits** pass pre-commit hooks
- **Zero commits** to main/master branch
- **All pushes** have updated documentation
- **All critical features** use TDD

### NOT Measuring (Yet) ⏸️

- Test coverage percentage
- Cyclomatic complexity
- Type hint coverage
- Code duplication metrics
- Performance benchmarks

**Why not**: These metrics don't add value during rapid prototyping. Will add when transitioning to production.

---

## Anti-Patterns to Avoid

### Code Anti-Patterns

❌ **Premature Abstraction**
- Don't create generic frameworks for one use case
- Wait until pattern repeats 3+ times

❌ **Over-Engineering**
- Don't add features "we might need later"
- Build only what's needed now

❌ **Ignoring Existing Patterns**
- Follow patterns already in codebase
- Don't introduce new patterns without reason

❌ **Magic Numbers**
- Use constants or config for hardcoded values
- Make intent clear

### Testing Anti-Patterns

❌ **Changing Tests to Make Code Pass**
- Tests define the contract
- If test is wrong, discuss with human first

❌ **Excessive Mocking**
- Use integration tests for APIs
- Mock only external services (not our own code)

❌ **Brittle Tests**
- Don't test implementation details
- Test behavior and outcomes

---

## Related Skills

- **tdd-workflow** - Test-first development process
- **api-development** - API development patterns
- **git-workflow** - Git standards and hooks

---

## References

**2025 AI Development Philosophy**:
- "Functional prototype the next day"
- Speed-quality trade-off favors speed in prototype
- Quality investment when feature validates

**Project Context**:
- Prototype backend (not in production)
- TDD for critical features only
- Integration tests as safety net
- Human verification required

---

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend (Prototype Phase)
