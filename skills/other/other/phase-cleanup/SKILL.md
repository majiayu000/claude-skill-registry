---
name: phase-cleanup
description: "Refactor and finalize code after parallel phases complete, addressing technical debt. Use in cleanup phase to polish code before merge."
mcp_fallback: none
category: phase
phase: Cleanup
user-invocable: false
---

# Cleanup Phase Coordination Skill

Refactor and finalize code after all parallel phases (Test, Implementation, Package) are complete.

## When to Use

- After Test, Implementation, and Package phases complete
- Addressing technical debt and code quality issues
- Finalizing code before merge to main
- Consolidating and polishing parallel phase outputs

## Quick Reference

```bash
# Check for code quality issues
grep -r "TODO\|FIXME\|HACK" src/
just pre-commit-all
pixi run mojo test -I . tests/

# Format and clean
pixi run mojo format src/**/*.mojo
pixi run mojo format tests/**/*.mojo

# Verify no warnings
pixi run mojo build -I . shared/ 2>&1 | grep -i "warning" && echo "⚠️ Warnings found" || echo "✅ No warnings"
```

## Workflow

1. **Collect issues** - Gather TODOs, FIXMEs, and bugs from parallel phases
2. **Refactor code** - Remove duplication, simplify complexity, improve naming
3. **Update documentation** - Ensure all docs match implementation
4. **Final quality checks** - Format, lint, test, coverage
5. **Verify ready for merge** - All quality gates passing

## Refactoring Principles

**KISS - Keep It Simple**:

```mojo
# Before: Over-engineered
fn process(data: Tensor) -> Tensor:
    let step1 = stage1(data)
    let step2 = stage2(step1)
    let step3 = stage3(step2)
    return finalize(step3)

# After: Simple pipeline
fn process(data: Tensor) -> Tensor:
    return pipeline(data)
```

**DRY - Don't Repeat Yourself**:

```mojo
# Before: Duplication
fn add_f32(a: Float32, b: Float32) -> Float32:
    return a + b
fn add_f64(a: Float64, b: Float64) -> Float64:
    return a + b

# After: Generic
fn add[dtype: DType](a: Scalar[dtype], b: Scalar[dtype]) -> Scalar[dtype]:
    return a + b
```

**SOLID - Single Responsibility**:

```mojo
# Before: Mixed responsibilities
fn load_and_process(path: String) -> Tensor:
    let raw = load_file(path)
    let cleaned = remove_outliers(raw)
    return normalize(cleaned)

# After: Separate
fn load_data(path: String) -> RawData:
    return load_file(path)

fn preprocess_data(data: RawData) -> Tensor:
    return normalize(remove_outliers(data))
```

## Quality Checklist

- [ ] No TODOs/FIXMEs (or documented in issue)
- [ ] Code duplication removed (DRY)
- [ ] Complex functions simplified (KISS)
- [ ] Naming clear and consistent
- [ ] Documentation updated
- [ ] All tests passing
- [ ] Code formatted (`mojo format`)
- [ ] No compiler warnings (zero-warnings policy)
- [ ] Test coverage ≥ 80%
- [ ] Ready for review

## Common Cleanup Tasks

1. **Remove dead code** - Unused functions, imports, variables
2. **Consolidate imports** - Organize by module
3. **Standardize errors** - Consistent error handling patterns
4. **Add missing tests** - Cover gaps in coverage
5. **Update comments** - Ensure accuracy after changes
6. **Review variable names** - Use clear, descriptive names

## Phase Dependencies

- **Input from**: Test, Implementation, and Package phases (all parallel outputs)
- **Precedes**: Merge to main (final polishing gate)
- **Must complete before**: PR approval and merge

## Output Location

- **Refactored code**: Same locations as implementation (in-place)
- **Updated docs**: GitHub issue comments
- **Final artifacts**: Ready for merge to `main` branch

## Error Handling

| Issue | Action |
|-------|--------|
| TODOs remain | Document in issue or remove code |
| Tests fail | Revert changes, debug, try again |
| Coverage low | Add tests for uncovered lines |
| Warnings | Fix immediately (zero-warnings policy) |
| Merge conflicts | Resolve with implementation team |

## Verification Checklist

Before marking cleanup complete:

```bash
# 1. Format
pixi run mojo format src/**/*.mojo tests/**/*.mojo

# 2. Test
pixi run mojo test -I . tests/

# 3. No warnings
pixi run mojo build -I . shared/ 2>&1 | tee /tmp/build.log
grep -i "warning" /tmp/build.log && echo "❌ Warnings found" || echo "✅ Clean"

# 4. No TODOs
grep -r "TODO\|FIXME" src/ && echo "❌ TODOs found" || echo "✅ Clean"

# 5. Pre-commit
just pre-commit-all

# 6. Final confirmation
git status  # No uncommitted changes
```

## References

- `CLAUDE.md` - "Key Development Principles" (KISS, DRY, SOLID, YAGNI)
- `CLAUDE.md` - "Zero-Warnings Policy" (enforcement guidelines)
- `CLAUDE.md` - "Common Mistakes to Avoid" (patterns from 64+ test failures)

---

**Key Principle**: Cleanup completes the 5-phase workflow. Code must be merge-ready.
