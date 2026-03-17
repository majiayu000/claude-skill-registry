---
name: create-review-checklist
description: "Generate review checklists for different change types. Use to customize review focus based on what was changed."
category: review
mcp_fallback: none
agent: test-engineer
user-invocable: false
---

# Create Review Checklists

Generate customized review checklists based on type of change.

## When to Use

- Starting PR review for unfamiliar change type
- Need specific checklist for Mojo vs Python code
- Reviewing test changes
- Documenting-focused changes
- Large multi-type changes needing organized review

## Quick Reference

```bash
# Detect change type from PR
gh pr diff <pr> --name-only | grep -E "\\.mojo$|\\.py$|\\.md$|test_"

# Categorize changes
gh pr diff <pr> | head -100 | grep "^[+-]" | wc -l  # Changed lines

# Get file counts by type
gh pr diff <pr> --name-only | sed 's/.*\.//' | sort | uniq -c
```

## Change Type Detection

**Mojo Implementation**:

- Files: `*.mojo` or `*.🔥`
- Focus: Syntax, patterns, memory safety, performance
- Extra checks: SIMD, ownership, zero-warnings

**Python Code**:

- Files: `*.py`
- Focus: Style (PEP 8), type hints, error handling
- Extra checks: Security, test coverage

**Tests**:

- Files: `test_*.py`, `test_*.mojo`
- Focus: Coverage, assertions, edge cases, clarity
- Extra checks: Flakiness, isolation

**Documentation**:

- Files: `*.md`, docstrings, comments
- Focus: Clarity, accuracy, completeness
- Extra checks: Links work, examples valid

**Configuration**:

- Files: `*.toml`, `*.yaml`, `.yaml`, `*.json`
- Focus: Correctness, consistency, validation
- Extra checks: No secrets, proper syntax

## Checklist Templates

**Mojo Implementation Checklist**:

- [ ] v0.26.1+ syntax (no inout, @value, DynamicVector)
- [ ] All `__init__` use `out self`
- [ ] Non-copyable returns use `^`
- [ ] Traits conformance correct (Copyable, Movable)
- [ ] Memory safety validated
- [ ] Zero compiler warnings
- [ ] SIMD used in hot paths
- [ ] Tests present and passing
- [ ] Documentation updated

**Python Code Checklist**:

- [ ] Follows PEP 8 style guide
- [ ] Type hints on all functions
- [ ] Docstrings present and clear
- [ ] Error handling appropriate
- [ ] No security vulnerabilities
- [ ] Tests cover new code
- [ ] Edge cases handled
- [ ] No code duplication

**Test Code Checklist**:

- [ ] Test name describes what's tested
- [ ] Assertions are clear and specific
- [ ] Edge cases covered (boundaries, empty, null, large)
- [ ] Setup/teardown clean (no side effects)
- [ ] Not dependent on other tests
- [ ] Reasonable timeout (not too long)
- [ ] Mocking/isolation appropriate
- [ ] Deterministic (no randomness/flakiness)

**Documentation Checklist**:

- [ ] Spelling and grammar correct
- [ ] Links validated and working
- [ ] Code examples are complete and correct
- [ ] Instructions tested and accurate
- [ ] Structure is logical and easy to follow
- [ ] Markdown formatting valid
- [ ] No broken references
- [ ] Up to date with code changes

**Configuration Checklist**:

- [ ] Syntax is valid (YAML, TOML, JSON)
- [ ] No hardcoded secrets
- [ ] Consistent with project standards
- [ ] Required fields present
- [ ] Default values sensible
- [ ] Documentation matches config
- [ ] Backward compatible (if applicable)
- [ ] Performance impact acceptable

## Checklist Generation Workflow

1. **Analyze PR**: Determine file types changed
2. **Categorize**: Group changes by type
3. **Select templates**: Pick appropriate checklists
4. **Customize**: Adjust based on complexity/scope
5. **Prioritize**: Mark critical vs optional items
6. **Document**: Create checklist with explanations
7. **Use**: Apply during code review

## Output Format

Report checklist with:

1. **Change Summary** - What types of changes detected
2. **Primary Focus** - Main review area
3. **Checklist Items** - Organized by category
4. **Deep Dives** - Detailed items for complex changes
5. **Quick Wins** - Easy items to verify first
6. **Risks** - High-risk areas to focus on
7. **Notes** - Special considerations

## Multi-Type Example

**PR changing Mojo code + Tests + Docs**:

1. Start with Mojo checklist (primary)
2. Apply test checklist to test changes
3. Apply documentation checklist to docs
4. Verify consistency across all types
5. Check integration between parts

## Customization Rules

- Critical items must PASS before approval
- High items SHOULD pass unless justified
- Medium items are NICE to have
- Low items are OPTIONAL suggestions

**Critical** (must fix):

- Syntax errors
- Test failures
- Security issues
- Breaking changes

**High** (should fix):

- Code style issues
- Missing tests
- Performance regression
- Incomplete documentation

**Medium** (nice to have):

- Code cleanup
- Example improvements
- Comment refinements

**Low** (optional):

- Formatting polish
- Minor optimizations
- Documentation color

## Error Handling

| Problem | Solution |
|---------|----------|
| Mixed change types | Create separate checklists for each type |
| Unclear type | Inspect files to determine type |
| Complex change | Break into multiple checklists |
| Specialized domain | Add domain-specific items to template |
| New pattern | Create new checklist template |

## References

- See review-pr-changes for full review workflow
- See CLAUDE.md for code standards
- See individual skill docs for detailed requirements
