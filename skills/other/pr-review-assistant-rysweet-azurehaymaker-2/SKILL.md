---
name: pr-review-assistant
version: 1.0.0
description: |
  Philosophy-aware PR reviews checking alignment with amplihack principles.
  Use when reviewing PRs to ensure ruthless simplicity, modular design, and zero-BS implementation.
  Suggests simplifications, identifies over-engineering, verifies brick module structure.
  Posts detailed, constructive review comments with specific file:line references.
---

# PR Review Assistant Skill

## Purpose

Philosophy-aware pull request reviews that go beyond syntax and style to check alignment with amplihack's core development principles. This skill reviews PRs not just for correctness, but for ruthless simplicity, modular architecture, and zero-BS implementation.

## When to Use This Skill

- **PR Code Reviews**: Review PRs against amplihack philosophy principles
- **Philosophy Compliance**: Check that code embodies ruthless simplicity and brick module design
- **Refactoring Suggestions**: Identify over-engineering and suggest concrete simplifications
- **Architecture Verification**: Verify modular design and clear contracts
- **Test Coverage**: Assess test adequacy for changed functionality
- **Design Assessment**: Catch over-engineering before it gets merged

## Core Philosophy: What We Review For

### 1. Ruthless Simplicity

Every line of code must justify its existence. We ask:

- **Can this be simpler?** Does each function do one thing well?
- **Is this necessary now?** Or is it future-proofing?
- **Are there unnecessary abstractions?** Extra layers that don't add value?
- **Can we remove lines?** The best code is code that doesn't exist.

### 2. Modular Architecture (Brick & Studs)

Code should be organized as self-contained modules with clear connections:

- **Brick** = Self-contained module with ONE clear responsibility
- **Stud** = Public contract (functions, API, data models) others connect to
- **Regeneratable** = Can be rebuilt from specification without breaking connections

### 3. Zero-BS Implementation

No shortcuts, stubs, or technical debt:

- **No TODOs in code** = Actually implement or don't include it
- **No NotImplementedError** = Except in abstract base classes
- **No mock data** = Real functionality from the start
- **No dead code** = Remove unused code
- **Every function works** = Or it doesn't exist

### 4. Quality Over Speed

- **Robust implementations** = Better than quick fixes
- **Long-term maintainability** = Not short-term gains
- **Clear error handling** = Errors visible, not swallowed
- **Tested behavior** = Verify contracts at module boundaries

## Review Process

### Step 1: Understand the Changes

Start by understanding what the PR changes:

1. **Read the PR description** to understand intent
2. **Identify affected modules** and their scope
3. **Note the dependencies** changed or added
4. **Understand the problem** being solved

### Step 2: Check Philosophy Alignment

Review each change against amplihack principles:

#### Ruthless Simplicity Check

- Is every line necessary?
- Are there unnecessary abstractions?
- Could this be implemented more simply?
- Is there future-proofing or speculation?
- Are there duplicate or similar functions?
- Could conditional logic be simplified?

#### Module Structure Check

- Does the change respect module boundaries?
- Are public contracts clear and documented?
- Are internal utilities isolated?
- Does the module have ONE clear responsibility?
- Are there circular dependencies?

#### Zero-BS Check

- Are there TODOs or NotImplementedError calls?
- Are mock or test data exposed in production code?
- Is error handling explicit and visible?
- Are all functions working implementations?
- Is there dead code or unused variables?

### Step 3: Identify Over-Engineering

Look for common over-engineering patterns:

- **Over-abstraction**: Base classes, protocols, factories for no clear benefit
- **Generic "frameworks"**: Building infrastructure for hypothetical needs
- **Premature optimization**: Complex algorithms for non-critical paths
- **Configuration complexity**: 50-line config when 5-line default would work
- **Future-proofing**: "We might need this someday" code
- **Excessive layering**: More indirection than necessary
- **Over-parameterization**: Functions with 8+ parameters instead of simpler approach

### Step 4: Verify Brick Module Structure

If new modules or module changes:

- **Single responsibility?** What is the ONE thing this module does?
- **Clear public interface?** What's exported and why?
- **Internal isolation?** Are utilities contained within module?
- **Dependencies documented?** What does it depend on?
- **Tests included?** Does spec define test requirements?
- **Examples provided?** Is usage clear?
- **Regeneratable?** Could this be rebuilt from a specification?

### Step 5: Check Test Coverage

Adequate testing is crucial:

- **Contract verification**: Tests verify public interface behavior
- **Edge cases covered**: Null, empty, boundary conditions tested
- **Error paths tested**: Exceptions raised when expected
- **Integration tested**: Module connections verified
- **Coverage adequate**: 85%+ for changed code

### Step 6: Provide Constructive Feedback

When suggesting changes:

1. **Be specific**: Reference file:line numbers
2. **Explain why**: What principle is violated?
3. **Suggest how**: Provide concrete examples
4. **Be respectful**: Focus on code, not person
5. **Acknowledge good work**: Recognize what's done well

## Concrete Review Checklist

### Ruthless Simplicity

- [ ] Every function has single clear purpose
- [ ] No unnecessary abstraction layers
- [ ] No future-proofing or speculation
- [ ] No duplicate logic or functions
- [ ] Conditional logic is straightforward
- [ ] Variable names are clear and self-documenting
- [ ] Function signatures aren't over-parameterized

### Modular Architecture

- [ ] Module has ONE clear responsibility
- [ ] Public interface is minimal and clear
- [ ] Internal utilities properly isolated
- [ ] Dependencies are explicit
- [ ] No circular dependencies
- [ ] Clear contracts at boundaries
- [ ] Module can be understood independently

### Zero-BS Implementation

- [ ] No TODOs, NotImplementedError, or stubs
- [ ] No mock/test data in production code
- [ ] No dead code or unused imports
- [ ] Error handling is explicit and visible
- [ ] All functions have working implementations
- [ ] No swallowed exceptions
- [ ] Clear logging/error messages for debugging

### Test Coverage

- [ ] Public interface is tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Integration points verified
- [ ] Coverage adequate (85%+)
- [ ] Tests verify contract, not implementation

### Documentation

- [ ] Docstrings are clear and complete
- [ ] Public interface documented
- [ ] Examples provided for new features
- [ ] Module README updated if needed
- [ ] Type hints present and accurate

## Example Reviews

### Example 1: Identifying Over-Engineering

**PR**: Add user permission checking to API

**Code Changed**:

```python
class PermissionValidator:
    def __init__(self):
        self.cache = {}

    def validate(self, user, resource):
        if user in self.cache:
            return self.cache[user]

        result = self._complex_validation(user, resource)
        self.cache[user] = result
        return result

    def _complex_validation(self, user, resource):
        # Complex business logic...
        pass
```

**Review Comment**:

````
FILE: permissions.py (lines 10-25)

This over-engineers the permission checking with caching that may not be needed.
The caching layer adds complexity without proven benefit:

1. Cache can become stale if user permissions change
2. Unclear when/if cache should be invalidated
3. In-memory cache doesn't scale across processes
4. Permission checks are usually not in hot paths

SUGGESTION - Start simpler:
```python
def check_permission(user, resource):
    """Check if user can access resource."""
    # Direct implementation
    return user.has_access_to(resource)
````

If caching is needed later, add it when profiling shows it helps.

This aligns with ruthless simplicity: don't add complexity until proven necessary.

```

### Example 2: Identifying Lack of Regeneration Documentation

**PR**: Add new authentication module

**Code Changed**: New file `.claude/tools/auth/auth.py`

**Review Comment**:
```

FILE: .claude/tools/auth/ (new module)

Good: Module has clear responsibilities (JWT validation, token refresh).
Issue: Missing specification documentation for module regeneration.

Brick Philosophy Requirement: Modules should be regeneratable from spec.

ACTION NEEDED:

1. Create Specs/authentication.md with:
   - Clear purpose and scope
   - Public interface (exported functions)
   - Dependencies listed
   - Test requirements
   - Usage examples

This enables future rebuilding if requirements change.

See .claude/skills/pr-review-assistant/ for specification template.

````

### Example 3: Identifying Zero-BS Issues

**PR**: Add data processing pipeline

**Code Changed**:
```python
def process_data(data):
    """Process data through pipeline."""
    # TODO: Add error handling
    result = validate(data)
    if not result:
        return None  # swallowed error

    # TODO: Implement caching
    return transform(result)
````

**Review Comment**:

````
FILE: pipeline.py (lines 5-15)

Zero-BS Issues Found:

1. LINE 6: TODO comments - implement or remove
   - "Add error handling" - Either add it now or create issue
   - "Implement caching" - Not needed yet; add if profiling shows benefit

2. LINE 10: Swallowed error
   - validate() likely raised exception, but returns None
   - Make error explicit: raise ValueError("Invalid data")
   - Or catch and re-raise with context

3. LINE 8: Silent failures
   - If None is returned, caller doesn't know why
   - Either raise exception or return Result type

SUGGESTION:
```python
def process_data(data):
    """Process data through pipeline.

    Raises:
        ValueError: If data validation fails
    """
    result = validate(data)  # Raises if invalid
    return transform(result)
````

All code is production-ready, no TODOs.

```

### Example 4: Identifying Missing Tests

**PR**: Add user role management

**Code Changed**: New class `RoleManager` in user module

**Review Comment**:
```

FILE: user.py (lines 50-100)

New functionality added without adequate tests.

ISSUE: RoleManager public interface not tested

- add_role(user, role) - add success case
- remove_role(user, role) - add success case
- get_roles(user) - test empty, single, multiple
- is_admin(user) - test true/false cases

EDGE CASES MISSING:

- [ ] duplicate role assignment (should be idempotent)
- [ ] removing non-existent role (should not error)
- [ ] get_roles on user with no roles (should return empty)

CONTRACT VERIFICATION:

- [ ] Functions accept documented types
- [ ] Return types match documentation
- [ ] Exceptions raised as documented

ADD: tests/test_role_manager.py with 85%+ coverage

````

### Example 5: Recognizing Good Design

**PR**: Add simplified config loader

**Code Changed**:
```python
def load_config(path):
    """Load YAML config from file.

    Args:
        path: Path to config file

    Returns:
        dict: Parsed config

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If YAML is invalid
    """
    with open(path) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
````

**Review Comment**:

```
EXCELLENT - This is exactly the simplicity we want:

✅ Single responsibility: Load and parse YAML
✅ Clear error handling: Explicit exceptions with context
✅ No TODOs or stubs: Production ready
✅ Complete documentation: Clear args, returns, exceptions
✅ No over-engineering: Direct implementation
✅ Testable: Clear behavior to verify

This is a model example of ruthless simplicity.
```

## Feedback Template

When commenting on PRs, use this structure:

```markdown
**FILE**: path/to/file.py (lines X-Y)

**ISSUE**: [Principle violated - Simplicity/Modularity/Zero-BS/Tests/Docs]

**WHAT**: [Describe what's in the code]

**WHY IT'S PROBLEMATIC**: [How it violates amplihack principles]

**SUGGESTION**: [Concrete code example or approach]

**REFERENCE**: [Link to relevant philosophy, principle, or example]
```

## Integration with GitHub

### Posting Review Comments

The skill can post review comments to GitHub PRs using:

```bash
gh pr comment <PR-NUMBER> -b "Review comment here"
# Or for specific file reviews:
gh pr diff <PR-NUMBER> | grep "^---" | head -1
# Then post review with specific file:line references
```

### Review Workflow

1. **Fetch PR details**: Get PR number, branch, changed files
2. **Analyze changes**: Run review against philosophy
3. **Generate feedback**: Compile specific, actionable comments
4. **Post review**: Create GitHub review with all comments
5. **Summary**: Post overall assessment

## Common Over-Engineering Patterns to Catch

### Pattern 1: Configuration Complexity

```python
# OVER-ENGINEERED: 50-line config class
class ConfigManager:
    def __init__(self, env_file, schema_file, validators):
        self.config = load_yaml(env_file)
        self.schema = load_json(schema_file)
        self.validators = validators
        # 40 more lines...

# SIMPLE: 5 lines
config = yaml.safe_load(open('.env.yaml'))
```

### Pattern 2: Factory Pattern When Not Needed

```python
# OVER-ENGINEERED: Factory for single implementation
class ValidationFactory:
    def create_validator(self, type):
        if type == "email":
            return EmailValidator()
        # ... more types

# SIMPLE: Direct function
def validate_email(email):
    return "@" in email and "." in email
```

### Pattern 3: Generic Base Classes for One Use

```python
# OVER-ENGINEERED: Base class never subclassed
class BaseRepository(ABC):
    @abstractmethod
    def find(self, id): pass
    # ... 20 abstract methods

class UserRepository(BaseRepository):
    # Forced to implement all abstract methods
    # But only uses 3 of them

# SIMPLE: Direct class
class UserRepository:
    def find(self, id):
        return self.db.query(User).get(id)
```

### Pattern 4: Premature Optimization

```python
# OVER-ENGINEERED: Complex caching for cache that's not needed
cache = LRUCache(maxsize=1000)
stats = CacheStats()
lock = threading.Lock()
# ... complex logic

# SIMPLE: None - profile first, optimize if needed
result = function(args)
```

## Key Questions to Ask

When reviewing, ask these questions:

1. **Can this be simpler?** If yes, why isn't it?
2. **Is this necessary now?** Or is it future-proofing?
3. **What's the ONE thing this does?** If there are many things, split it.
4. **Who will use this?** Is the interface clear for them?
5. **What can go wrong?** Are errors handled explicitly?
6. **Is this testable?** Can the contract be verified?
7. **Will this need to change?** Is it flexible without over-engineering?
8. **Could this be deleted?** Better than could it be refactored?
9. **Does this follow our patterns?** Or is it unique?
10. **Am I confident this works?** Or is it speculative?

## Success Criteria

A successful PR review using this skill:

- [ ] Reviews code against amplihack philosophy, not just style
- [ ] Identifies over-engineering with concrete suggestions
- [ ] Verifies module structure and brick design
- [ ] Checks test coverage adequacy
- [ ] Provides specific file:line references
- [ ] Offers concrete, actionable suggestions
- [ ] Recognizes and acknowledges good design
- [ ] Posts comprehensive GitHub review comments
- [ ] Helps team learn and improve

## Output

The skill produces:

1. **Philosophy Compliance Report**
   - Ruthless Simplicity check
   - Modular Architecture check
   - Zero-BS Implementation check
   - Test Coverage assessment
   - Overall assessment

2. **Specific Recommendations**
   - Over-engineering identified with examples
   - Simplification suggestions with code
   - Module structure feedback
   - Test gaps to address

3. **GitHub Comments** (optional)
   - Detailed review with file:line references
   - Inline code suggestions
   - Summary of findings
   - Constructive, respectful tone

## Philosophy References

All reviews anchor in these documents:

- `.claude/context/PHILOSOPHY.md` - Core development philosophy
- `.claude/context/PATTERNS.md` - Approved patterns and anti-patterns
- `Specs/` - Module specifications for architecture verification
- `.claude/context/DISCOVERIES.md` - Known issues and solutions

## Tips for Effective Reviews

1. **Be Specific**: Reference exact lines and code
2. **Explain Why**: What principle is violated and why it matters
3. **Suggest How**: Provide concrete code examples
4. **Respect Constraints**: Some complexity may be necessary
5. **Acknowledge Good Work**: Praise what's done well
6. **Ask Questions**: "Have you considered?" invites discussion
7. **Learn Together**: Reviews are teaching opportunities
8. **Iterate**: Suggest improvements, don't demand perfection
9. **Consider Context**: External constraints matter
10. **Stay Focused**: Review philosophy alignment, not personal style

## Related Skills and Workflows

- **Module Spec Generator**: Creates specifications for regeneratable modules
- **Builder Agent**: Implements code from specifications
- **Reviewer Agent**: Philosophy compliance verification
- **Tester Agent**: Test generation and validation
- **Document-Driven Development**: Uses specs as source of truth

## Feedback and Evolution

This skill should evolve based on usage:

- What patterns do we keep finding?
- What suggestions lead to better code?
- What philosophy principles are most violated?
- How can we catch issues earlier?

Document learnings in `.claude/context/DISCOVERIES.md`.
