---
name: agent-ops-critical-review
description: "Deep, excruciating code review. Use anytime to analyze code for correctness, edge cases, security, performance, and design issues. Not tied to baseline—this is pure code analysis."
category: core
invokes: [agent-ops-state, agent-ops-tasks, agent-ops-api-review]
invoked_by: []
state_files:
  read: [constitution.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Critical Code Review

## Purpose

Perform a deep, thorough, excruciating review of code. This skill is about analyzing code quality, correctness, and design—NOT about running tests or comparing to baseline. Use it anytime you need to scrutinize code.

## API Detection

**Before starting review, check if project contains APIs:**

```yaml
api_indicators:
  - OpenAPI/Swagger spec (openapi.yaml, swagger.json, openapi.json)
  - API framework patterns (FastAPI, Flask, Express, ASP.NET controllers)
  - Route decorators (@app.route, @router.get, [HttpGet], etc.)
  - API test files (test_api_*, *_api_test.*, api.spec.*)
```

**If API detected:**
1. Note in review scope: "API endpoints detected"
2. After general review, invoke `agent-ops-api-review` for API-specific audit
3. Merge API review findings into final report

## When to Use

- **During planning**: Review existing code before modifying
- **During implementation**: Review your own changes
- **Before completion**: Final quality check
- **On demand**: User requests a code review
- **After recovery**: Verify recovery didn't introduce issues

## Review Dimensions

### 1) Correctness

**Logic Analysis**:
- Does the code do what it claims to do?
- Are all code paths reachable and correct?
- Are conditionals exhaustive (all cases handled)?
- Are loop invariants maintained?
- Are recursive functions guaranteed to terminate?

**Boundary Conditions**:
- Empty inputs (null, undefined, empty string, empty array)
- Single element cases
- Maximum values / overflow potential
- Off-by-one errors
- Unicode / special characters

**State Management**:
- Is state modified predictably?
- Are there race conditions?
- Is cleanup always performed (finally blocks, defer, etc.)?

### 2) Error Handling

**Questions to Ask**:
- What can fail here?
- Is every failure case handled?
- Are errors propagated appropriately?
- Are error messages informative?
- Is there silent failure hiding bugs?

**Checklist**:
- [ ] All external calls wrapped in try/catch or equivalent
- [ ] Errors logged with context
- [ ] User-facing errors are actionable
- [ ] No swallowed exceptions
- [ ] Cleanup happens even on error

### 3) Security

**Input Validation**:
- Are all external inputs validated?
- Is there SQL injection potential?
- Is there XSS potential?
- Is there command injection potential?
- Are paths sanitized (no traversal)?

**Authentication/Authorization**:
- Is auth checked before sensitive operations?
- Are tokens/secrets handled securely?
- Is sensitive data logged? (it shouldn't be)

**Data Handling**:
- Is PII protected?
- Are passwords hashed, not encrypted?
- Is data sanitized before display?

### 4) Performance

**Algorithmic**:
- What's the time complexity?
- What's the space complexity?
- Are there N+1 query problems?
- Are there unnecessary iterations?

**Resource Management**:
- Are connections/handles closed?
- Are large objects released?
- Is there potential for memory leaks?
- Are there blocking calls that should be async?

**Caching/Optimization**:
- Is expensive computation cached when appropriate?
- Are there premature optimizations obscuring clarity?

### 5) Design & Maintainability

**Single Responsibility**:
- Does each function do one thing?
- Are there functions that are too long?
- Is there duplicated logic that should be extracted?

**Naming & Clarity**:
- Do names accurately describe purpose?
- Are abbreviations clear or confusing?
- Would a new team member understand this?

**Dependencies**:
- Are dependencies appropriate?
- Is there tight coupling that could be loosened?
- Are there circular dependencies?

**Testability**:
- Can this code be unit tested?
- Are dependencies injectable?
- Is there global state that complicates testing?

### 6) Consistency

- Does it follow project conventions?
- Does it match surrounding code style?
- Are patterns used consistently?

### 7) SOLID Principles (for OO/class-based code)

> **When to apply:** Review SOLID for class-based code, services, and complex modules. Skip for simple scripts, utilities, or purely functional code.

**Single Responsibility (SRP)**:
- Does each class have one clear purpose?
- Would changes to one feature require modifying this class for unrelated reasons?
- Could this class be split into smaller, focused classes?

**Open/Closed (OCP)**:
- Can new features be added by extension rather than modification?
- Are there long if/elif/switch chains that should use polymorphism?
- Is the Strategy, Factory, or Template pattern appropriate?

**Liskov Substitution (LSP)**:
- Do subclasses honor the contracts of their parent classes?
- Are there overridden methods that change expected behavior?
- Does substituting a subclass for its parent break anything?

**Interface Segregation (ISP)**:
- Are interfaces/ABCs focused and cohesive?
- Do implementations need all methods they're required to have?
- Should large interfaces be split into smaller, role-specific ones?

**Dependency Inversion (DIP)**:
- Do high-level modules depend on abstractions, not concretions?
- Are dependencies injected rather than created internally?
- Can this code be tested without real implementations of dependencies?

**SOLID Checklist** (for class-based code):
- [ ] Classes have single, clear responsibilities
- [ ] New behavior can be added via extension
- [ ] Subclasses are substitutable for parents
- [ ] Interfaces are focused and minimal
- [ ] Dependencies are on abstractions, not concretions

**Common Python SOLID Violations**:

```python
# ❌ SRP Violation — class does too much
class UserService:
    def create_user(self): ...
    def send_email(self): ...
    def generate_report(self): ...

# ✅ SRP Fixed — separate concerns
class UserRepository: ...
class EmailService: ...
class ReportGenerator: ...

# ❌ OCP Violation — must modify to add new types
def process(item):
    if item.type == "A": ...
    elif item.type == "B": ...
    # Must add elif for each new type

# ✅ OCP Fixed — extend via new classes
class Processor(ABC):
    @abstractmethod
    def process(self): ...

# ❌ DIP Violation — depends on concrete class
class OrderService:
    def __init__(self):
        self.repo = SqliteRepository()  # Concrete!

# ✅ DIP Fixed — depends on abstraction
class OrderService:
    def __init__(self, repo: Repository):  # Abstract!
        self.repo = repo
```

## Review Procedure

### For Changed Code

1. **Read the diff thoroughly** — understand every line changed
2. **Trace data flow** — follow inputs through to outputs
3. **Question assumptions** — what if assumptions are wrong?
4. **Check edges** — what happens at boundaries?
5. **Verify error paths** — what happens when things fail?
6. **Consider security** — can this be exploited?
7. **Assess performance** — will this scale?

### For New Code

All of the above, plus:
- Is this the right abstraction?
- Is there existing code that does this?
- Does this integrate cleanly?

### For Existing Code (Understanding)

Focus on:
- What does this code actually do?
- What are the invariants?
- What are the failure modes?
- Where are the risks?

## Review Output Format

```markdown
## Critical Review: [component/file]

### Summary
- Scope: [what was reviewed]
- Severity: [critical/high/medium/low findings]
- Verdict: [APPROVE / CHANGES NEEDED / BLOCK]

### Critical Issues (must fix)
1. **[Issue title]**
   - Location: file.ts#L10-20
   - Problem: [description]
   - Risk: [what could go wrong]
   - Suggestion: [how to fix]

### High Priority (should fix)
1. ...

### Medium Priority (consider fixing)
1. ...

### Low Priority (optional improvements)
1. ...

### Positive Observations
- [What's done well — reinforce good patterns]
```

## Review Mindset

### Be Thorough
- Don't skim — read every line
- Don't assume — verify
- Don't trust happy path — test failure cases mentally

### Be Skeptical
- What if this input is malicious?
- What if this external service fails?
- What if this runs concurrently?

### Be Constructive
- Explain WHY something is a problem
- Suggest alternatives, don't just criticize
- Acknowledge good work

### Be Honest
- If you don't understand something, say so
- If you're uncertain about an issue, rate your confidence
- Don't rubber-stamp — that defeats the purpose

## Integration with Workflow

This skill is **independent** of baseline comparison. It's pure code analysis.

- **Use with baseline**: After critical review, separately run validation/baseline comparison
- **Use alone**: Review code quality without running any tests
- **Use during planning**: Analyze existing code before changes
- **Use for learning**: Understand unfamiliar codebase

## Output

Update `.agent/focus.md`:
```markdown
## Just did
- Critical review of [component]
  - Findings: X critical, Y high, Z medium
  - Verdict: [APPROVE / CHANGES NEEDED / BLOCK]
```

## Issue Discovery After Review

**After review, invoke `agent-ops-tasks` discovery procedure:**

1) **Collect all findings** from review output:
   - Critical issues → `BUG` or `SEC` (critical/high)
   - High priority → `BUG`, `SEC`, or `PERF` (high)
   - Medium priority → various types (medium)
   - Low priority → `CHORE`, `REFAC`, `DOCS` (low)

2) **Present to user:**
   ```
   📋 Review found {N} issues:
   
   Critical:
   - [SEC] SQL injection vulnerability in UserController#search
   - [BUG] Race condition in cache invalidation
   
   High:
   - [PERF] N+1 query in OrderService#list
   - [BUG] Unhandled null in payment callback
   
   Medium:
   - [CHORE] Error messages not user-friendly
   - [TEST] Missing edge case coverage
   
   Low:
   - [REFAC] Extract duplicate validation logic
   - [DOCS] Add JSDoc to public methods
   
   Create issues for these? [A]ll / [S]elect / [N]one
   ```

3) **After creating issues:**
   ```
   Created {N} issues. What's next?
   
   1. Start fixing highest priority (SEC-0001@abc123 - SQL injection)
   2. Create more issues
   3. Continue with original task
   4. Review issue list
   ```

4) **If user declines:**
   - Log findings summary in focus.md
   - Note "Review findings not converted to issues (user declined)"
