---
name: kcl-composition-validator
description: Validates KCL Crossplane compositions with comprehensive checks including formatting, syntax validation, and rendering tests. Automatically activates when working with KCL files, Crossplane compositions, or before commits touching infrastructure/base/crossplane/configuration/. Prevents CI failures and catches critical bugs like the mutation pattern.
allowed-tools: Read, Bash, Grep, Glob
---

# KCL Composition Validator

## When This Skill Activates

This skill automatically activates when:
- Modifying files in `infrastructure/base/crossplane/configuration/kcl/`
- Working with KCL compositions or Crossplane resources
- User mentions "kcl", "crossplane", "composition", or "validate"
- Before committing changes that include `.k` files
- When running pre-commit validation

## Critical: Why This Matters

**The CI enforces strict KCL formatting and will fail your commit if validation doesn't pass.**

Common issues this skill prevents:
- Formatting violations that fail CI
- Syntax errors in KCL code
- Resource mutation causing duplicate resources (issue #285)
- Rendering failures in composition pipeline

## Three-Stage Validation Process

### Stage 1: KCL Formatting (CRITICAL - CI Enforced)

**Purpose**: Ensure code follows strict formatting standards that CI will check.

**What to check**:
- Single-line list comprehensions (NOT multi-line)
- No trailing blank lines between sections
- Proper indentation and spacing

**How to validate**:
```bash
cd infrastructure/base/crossplane/configuration/kcl/<module>
kcl fmt .
```

**Check for changes**:
```bash
git diff --quiet . || echo "Files were reformatted - review changes"
```

If `kcl fmt` made changes, the formatting was incorrect. Review the diff and commit the formatted version.

### Stage 2: KCL Syntax and Logic Validation

**Purpose**: Test KCL code executes without errors using example settings.

**How to validate**:
```bash
cd infrastructure/base/crossplane/configuration/kcl/<module>
kcl run . -Y settings-example.yaml
```

**What this catches**:
- Syntax errors in KCL code
- Logic errors in conditionals
- Type mismatches
- Reference errors

### Stage 3: Crossplane Render Validation

**Purpose**: Test the complete composition pipeline end-to-end.

**Comprehensive validation script**:
```bash
# From repository root
./scripts/validate-kcl-compositions.sh
```

This script validates ALL compositions through all three stages automatically.

**Manual validation** (for specific compositions):
```bash
cd infrastructure/base/crossplane/configuration

# Test basic example
crossplane render examples/app-basic.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/rendered.yaml

# Test complete example
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/rendered.yaml
```

**Tested compositions**:
- `app`: app-basic.yaml, app-complete.yaml
- `cloudnativepg` (SQLInstance): sqlinstance-basic.yaml, sqlinstance-complete.yaml
- `eks-pod-identity`: epi.yaml

## Critical KCL Rules

### Rule 1: NEVER MUTATE RESOURCES (Issue #285)

**Background**: https://github.com/crossplane-contrib/function-kcl/issues/285

Mutating dictionaries/resources after creation causes function-kcl to create duplicate resources. This is a known bug in function-kcl's duplicate detection mechanism.

**WRONG - Mutation Pattern**:
```kcl
# ❌ Creating resource then modifying it later
_deployment = {
    apiVersion = "apps/v1"
    kind = "Deployment"
    metadata = {
        name = _name
        annotations = {
            "base-annotation" = "value"
        }
    }
}

# ❌ MUTATION! This causes duplicates
if _deploymentReady:
    _deployment.metadata.annotations["krm.kcl.dev/ready"] = "True"

_items += [_deployment]
```

**CORRECT - Inline Conditional Pattern**:
```kcl
# ✅ Using inline conditionals
_deployment = {
    apiVersion = "apps/v1"
    kind = "Deployment"
    metadata = {
        name = _name
        annotations = {
            "base-annotation" = "value"
            if _deploymentReady:
                "krm.kcl.dev/ready" = "True"  # ✅ Inline conditional
        }
    }
}
_items += [_deployment]
```

**CORRECT - List Comprehension Pattern**:
```kcl
# ✅ List comprehensions with inline definitions
_items += [{
    apiVersion = "apps/v1"
    kind = "Deployment"
    metadata = {
        name = _name + "-" + db.name
        annotations = {
            "base-annotation" = "value"
            if _ready:
                "krm.kcl.dev/ready" = "True"
        }
    }
} for db in databases]
```

**Safe patterns**:
- Inline conditionals within dictionary literals
- List comprehensions with inline definitions
- Ternary operators returning complete dictionaries

**Unsafe patterns** (NEVER use):
- Post-creation field assignment: `resource.field = value`
- Post-creation nested assignment: `resource.metadata.annotations["key"] = "value"`
- Any mutation of resource variables after initial creation

### Rule 2: Single-Line List Comprehensions

**WRONG**:
```kcl
# ❌ Multi-line comprehension (will fail CI)
_ready = any_true([
    c.get("type") == "Available" and c.get("status") == "True"
    for c in conditions or []
])
```

**CORRECT**:
```kcl
# ✅ Single-line comprehension
_ready = any_true([c.get("type") == "Available" and c.get("status") == "True" for c in conditions or []])
```

### Rule 3: No Trailing Blank Lines

Remove extra blank lines between logical sections. The `kcl fmt` tool will catch these.

## Pre-Commit Workflow

**ALWAYS run before committing KCL changes**:

```bash
# From repository root
./scripts/validate-kcl-compositions.sh
```

**Expected output**:
```
╔════════════════════════════════════════════════════════════════╗
║  KCL Crossplane Composition Validation                        ║
╚════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Validating: app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 [1/3] Checking KCL formatting...
   ✅ Formatting is correct

🧪 [2/3] Validating KCL syntax and logic...
   ✅ KCL syntax valid

🎨 [3/3] Testing crossplane render...
   Testing: app-basic.yaml
   ✅ app-basic.yaml renders successfully
   Testing: app-complete.yaml
   ✅ app-complete.yaml renders successfully

✅ All checks passed for app
```

**Target**: Zero errors, minimal warnings.

## Common Issues and Fixes

### Issue: Code Reformatted by kcl fmt

**Symptom**: `kcl fmt` makes changes to your code

**Fix**:
1. Review the changes with `git diff`
2. Commit the formatted version
3. The formatting is now correct for CI

### Issue: Syntax Errors

**Symptom**: `kcl run` fails with syntax error

**Fix**:
1. Read the error message carefully
2. Check the line number indicated
3. Common causes: missing commas, incorrect indentation, typos
4. Fix the syntax and re-run validation

### Issue: Render Failures

**Symptom**: `crossplane render` fails

**Fix**:
1. Check that example files match composition schema
2. Verify `functions.yaml` is correctly configured
3. Ensure `environmentconfig.yaml` exists
4. Check function-kcl version compatibility

### Issue: Duplicate Resources Created

**Symptom**: Multiple identical resources in rendered output

**Fix**:
1. Search for resource mutation patterns in code
2. Look for lines like: `_resource.field = value`
3. Refactor to use inline conditionals
4. See Rule 1 above for correct patterns

## Quick Checklist

Before committing KCL changes, ensure:

- [ ] Run `./scripts/validate-kcl-compositions.sh` from repo root
- [ ] All formatting checks pass (Stage 1)
- [ ] All syntax validations pass (Stage 2)
- [ ] All render tests pass (Stage 3)
- [ ] No resource mutation patterns in code
- [ ] List comprehensions are single-line
- [ ] No trailing blank lines

## Additional Resources

- Mutation bug details: See `reference.md` in this skill folder
- Code patterns: See `examples.md` in this skill folder
- Quick reference: See `quick-reference.md` in this skill folder

## Validation Targets

**Modules validated**:
- `app` - Application composition with progressive complexity
- `cloudnativepg` - PostgreSQL database instances
- `eks-pod-identity` - EKS Pod Identity for IAM roles

**Example files tested**:
- Basic examples (minimal configuration)
- Complete examples (production-ready with all features)

## Success Criteria

Validation is successful when:
1. `kcl fmt` makes no changes (formatting correct)
2. `kcl run` executes without errors (syntax valid)
3. `crossplane render` succeeds for all examples (composition valid)
4. Zero errors reported by validation script
5. Minimal warnings (Docker availability only)
