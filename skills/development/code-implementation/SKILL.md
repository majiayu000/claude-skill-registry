---
name: code-implementation
description: Implement code changes by learning from and precisely matching existing
  codebase patterns, ensuring seamless integration with surrounding code. Use when
  writing new features, modifying logic, adding f
---

---
name: code-implementation
description: Implement code changes by learning from and precisely matching existing codebase patterns, ensuring seamless integration with surrounding code. Use when writing new features, modifying logic, adding functionality. Triggers: 'implement', 'write code', 'add feature', 'create', 'build', 'fix bug', '구현', '코드 작성', '기능 추가', '생성', '빌드', '버그 수정', '만들어', working with *.ts, *.go, *.java, *.py, *.nix, *.rs files.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(git:*)
  - Bash(just:*)
  - Bash(go:*)
  - Bash(gradle:*)
  - Bash(./gradlew:*)
---

# Code Implementation Methodology

This skill provides systematic approach to implementing code that blends naturally with existing codebase as if written by the original developers.

**Leverages:** [codebase-analysis] skill for discovering project conventions and patterns.

## Core Implementation Principle

**Mimic, Don't Import**: Every line of new code should feel like it was written by the same developer who wrote the surrounding code.

## Implementation Workflow

### Phase 1: Context Learning
Before writing any code:
1. **Study neighbors**: Read 3-5 files in same directory/module
2. **Analyze similar features**: Find comparable functionality
3. **Learn patterns**: Identify repeated structures and approaches
4. **Understand dependencies**: See how libraries are used
5. **Examine tests**: Learn validation approaches

### Phase 2: Pattern Matching
Match existing code exactly:
1. **Naming**: Use same case, prefixes, suffixes as neighbors
2. **Structure**: Follow same file organization and class/function layout
3. **Style**: Match indentation, spacing, bracing, comments
4. **Libraries**: Use same dependencies and utilities as existing code
5. **Error handling**: Follow same error patterns and logging

### Phase 3: Implementation
Write code that blends in:
1. Copy structural patterns from similar existing code
2. Reuse existing utilities and helper functions
3. Follow same abstraction levels as surrounding code
4. Match comment style and documentation format
5. Use same testing patterns and assertions

### Phase 4: Integration Validation
Ensure seamless integration:
1. Run existing tests - all must pass
2. Execute build commands - must compile/run
3. Verify style consistency with surrounding code
4. Check that integration points work correctly
5. Ensure no new dependencies without justification

## Style Matching Categories

### Naming Conventions
- Match case style (camelCase, snake_case, PascalCase)
- Follow prefix/suffix patterns (get*, is*, has*, *Service, *Repository)
- Use domain terminology from existing code
- Maintain consistency within same module

### Structural Patterns
- Copy class/function organization from similar files
- Follow same constructor/initialization patterns
- Match method ordering (public → private, create → read → update → delete)
- Replicate abstraction levels

### Import Organization
- Group imports same way as existing files
- Use same libraries and frameworks
- Follow import ordering conventions
- Avoid introducing new dependencies

### Error Handling
- Match exception types and error messages
- Follow logging patterns and levels
- Use same error propagation approach
- Replicate validation patterns

### Comment and Documentation
- Match comment style (// vs /* */ vs #)
- Follow documentation format (JSDoc, Python docstrings, etc.)
- Use same level of detail as surrounding code
- Maintain consistent spacing and formatting

## Common Implementation Patterns

### Adding CRUD Operations
When adding CRUD, find existing CRUD examples:
1. Copy the structure exactly
2. Adjust entity/model names
3. Keep same validation patterns
4. Use same repository patterns
5. Follow same endpoint/API structure

### Adding API Endpoints
When adding endpoints, find similar endpoints:
1. Copy routing pattern
2. Match request/response DTOs structure
3. Use same validation approach
4. Follow same error response format
5. Apply same authentication/authorization

### Adding Business Logic
When adding logic, study similar use cases:
1. Follow same service/use case structure
2. Use existing domain models
3. Apply same transaction patterns
4. Reuse existing validation
5. Match logging and error handling

## Integration Best Practices

### Use Existing Utilities
```
✅ Always: Reuse project utilities and helpers
❌ Never: Reimplement existing functionality
```

### Follow Architectural Boundaries
```
✅ Always: Respect layer dependencies (API → Service → Repository)
❌ Never: Skip layers or create circular dependencies
```

### Match Technology Choices
```
✅ Always: Use same libraries as existing code
❌ Never: Introduce new frameworks without strong justification
```

## Quality Checklist

Before considering implementation complete:
- [ ] Does code match naming conventions of surrounding files?
- [ ] Are imports organized like existing files?
- [ ] Does error handling follow project patterns?
- [ ] Are same libraries/utilities used?
- [ ] Do comments match existing style?
- [ ] Does code structure align with similar features?
- [ ] All existing tests still pass?
- [ ] New code follows discovered patterns?
- [ ] No architectural boundaries violated?
- [ ] No unnecessary dependencies added?

## Detailed Examples

For comprehensive code examples demonstrating each pattern, see:
- **examples.md** - Detailed code samples for all matching strategies

---

**Remember**: The best implementation is invisible - it looks like it was always part of the codebase. Use [codebase-analysis] to understand the codebase's voice, then write in that voice.
