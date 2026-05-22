---
name: crossplane-renderer
description: Renders and validates Crossplane compositions with security and policy checks. Automatically activates when testing compositions, rendering examples, or validating resources with Polaris, kube-linter, and Datree. Works standalone or as part of complete KCL validation workflow.
allowed-tools: Read, Bash, Grep, Glob, Write
---

# Crossplane Renderer & Validator

## When This Skill Activates

This skill automatically activates when:
- Rendering Crossplane compositions for testing
- Validating composition security and policies
- Previewing resources before deployment
- User mentions "render", "crossplane", "polaris", "validate", "security"
- Testing composition changes during development
- Debugging composition issues

## Relationship with KCL Validator

**Standalone Use**: Quick composition testing and security validation during development

**Integrated Use**: Part of the complete validation workflow with `kcl-composition-validator` skill
- Stage 1: KCL Formatting (`kcl fmt`)
- Stage 2: KCL Syntax Validation (`kcl run`)
- **Stage 3: Composition Rendering** (this skill)
- **Stage 4: Security/Policy Validation** (this skill)

For complete pre-commit validation, use `kcl-composition-validator` which runs all stages.

## Core Rendering Workflow

### Basic Rendering

**Purpose**: Test that composition renders successfully and preview resources

**Command Pattern**:
```bash
cd infrastructure/base/crossplane/configuration

crossplane render \
  examples/<claim-file>.yaml \
  <composition-file>.yaml \
  functions.yaml \
  --extra-resources examples/environmentconfig.yaml \
  > /tmp/rendered.yaml
```

**Available Compositions**:

1. **App Composition** (`app-composition.yaml`)
   - Examples: `app-basic.yaml`, `app-complete.yaml`
   - Progressive complexity: minimal to production-ready
   - Features: deployment, database, cache, storage, autoscaling, HA

2. **SQLInstance Composition** (`sql-instance-composition.yaml`)
   - Examples: `sqlinstance-basic.yaml`, `sqlinstance-complete.yaml`
   - PostgreSQL via CloudNativePG
   - Features: backup, HA, migrations

3. **EKS Pod Identity** (`epi-composition.yaml`)
   - Example: `epi.yaml`
   - IAM roles for service accounts

### Rendering Examples

**Test basic App configuration**:
```bash
cd infrastructure/base/crossplane/configuration

crossplane render \
  examples/app-basic.yaml \
  app-composition.yaml \
  functions.yaml \
  --extra-resources examples/environmentconfig.yaml \
  > /tmp/app-basic-rendered.yaml
```

**Test complete App configuration**:
```bash
crossplane render \
  examples/app-complete.yaml \
  app-composition.yaml \
  functions.yaml \
  --extra-resources examples/environmentconfig.yaml \
  > /tmp/app-complete-rendered.yaml
```

**Test SQLInstance**:
```bash
crossplane render \
  examples/sqlinstance-complete.yaml \
  sql-instance-composition.yaml \
  functions.yaml \
  --extra-resources examples/environmentconfig.yaml \
  > /tmp/sqlinstance-rendered.yaml
```

## Security & Policy Validation

**CRITICAL**: Every composition change must pass security and policy validation before committing.

### Validation Targets

- **Polaris**: Security & best practices - Target score: **85+**
- **kube-linter**: Kubernetes best practices - Target: **No errors**
- **Datree**: Policy enforcement - Target: **No violations** (warnings acceptable if documented)

### Step-by-Step Validation

**Step 1: Render the Composition**
```bash
cd infrastructure/base/crossplane/configuration
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/rendered.yaml
```

**Step 2: Polaris Security Audit**
```bash
polaris audit --audit-path /tmp/rendered.yaml --format=pretty
```

**Expected output**:
- Overall score: 85+ (Green/Yellow acceptable)
- No critical security issues
- Resource limits defined
- Health checks configured

**Common Polaris Issues**:
- Missing resource limits → Add requests/limits in composition
- No health checks → Add liveness/readiness probes
- Running as root → Add securityContext with non-root user
- Privileged containers → Remove privileged: true unless required

**Step 3: kube-linter Validation**
```bash
kube-linter lint /tmp/rendered.yaml
```

**Expected**: Clean output with no errors

**Common kube-linter Issues**:
- Missing liveness/readiness probes
- No resource limits
- Incorrect label schemas
- Deprecated API versions

**Step 4: Datree Policy Check**
```bash
datree test /tmp/rendered.yaml --ignore-missing-schemas
```

**Expected**: No policy violations (warnings acceptable if documented)

**Common Datree Issues**:
- Missing labels (app.kubernetes.io/*)
- Incorrect image tags (using 'latest')
- Missing owner references
- Network policy gaps

### Security Validation Checklist

Before committing composition changes:

- [ ] Composition renders successfully without errors
- [ ] Polaris score is 85+ with no critical issues
- [ ] kube-linter passes with no errors
- [ ] Datree policy check passes (or warnings documented)
- [ ] Resource limits are defined for all containers
- [ ] Health checks (liveness/readiness) are configured
- [ ] Security contexts are properly set
- [ ] No privileged containers (unless justified)
- [ ] Images use specific tags (not 'latest')
- [ ] Network policies are defined (where applicable)

## Rendered Output Analysis

### Inspect Resources

**Count resources by kind**:
```bash
grep "^kind:" /tmp/rendered.yaml | sort | uniq -c
```

**Extract specific resource**:
```bash
# Get Deployment
yq 'select(.kind == "Deployment")' /tmp/rendered.yaml

# Get Service
yq 'select(.kind == "Service")' /tmp/rendered.yaml

# Get HTTPRoute
yq 'select(.kind == "HTTPRoute")' /tmp/rendered.yaml
```

**Check readiness annotations**:
```bash
# Find resources marked as ready
grep -B 5 'krm.kcl.dev/ready: "True"' /tmp/rendered.yaml
```

### Verify Resource Correctness

**Deployment checks**:
```bash
# Check replicas
yq 'select(.kind == "Deployment") | .spec.replicas' /tmp/rendered.yaml

# Check image
yq 'select(.kind == "Deployment") | .spec.template.spec.containers[0].image' /tmp/rendered.yaml

# Check resource limits
yq 'select(.kind == "Deployment") | .spec.template.spec.containers[0].resources' /tmp/rendered.yaml
```

**Service checks**:
```bash
# Check service type
yq 'select(.kind == "Service") | .spec.type' /tmp/rendered.yaml

# Check ports
yq 'select(.kind == "Service") | .spec.ports' /tmp/rendered.yaml
```

**HTTPRoute checks**:
```bash
# Check hostnames
yq 'select(.kind == "HTTPRoute") | .spec.hostnames' /tmp/rendered.yaml

# Check backend refs
yq 'select(.kind == "HTTPRoute") | .spec.rules[0].backendRefs' /tmp/rendered.yaml
```

## Detecting Duplicate Resources

**Issue**: KCL mutation patterns can cause duplicate resources (see `kcl-composition-validator` skill)

**Detection**:
```bash
# Count Deployments (should match expected count)
grep -c "kind: Deployment" /tmp/rendered.yaml

# Count Services
grep -c "kind: Service" /tmp/rendered.yaml

# Find duplicate resource names
grep "name:" /tmp/rendered.yaml | sort | uniq -d
```

**If duplicates found**:
1. Check KCL code for mutation patterns
2. Use `kcl-composition-validator` skill for detailed guidance
3. Refactor to use inline conditionals
4. Re-render and verify

## Development Workflow

### Quick Iteration Cycle

**When developing new composition features**:

```bash
# 1. Make changes to KCL composition
vim infrastructure/base/crossplane/configuration/kcl/app/main.k

# 2. Quick render test
cd infrastructure/base/crossplane/configuration
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/test.yaml

# 3. Check output
less /tmp/test.yaml

# 4. Iterate until correct
```

**When changes look good**:

```bash
# 5. Run security validation
polaris audit --audit-path /tmp/test.yaml --format=pretty
kube-linter lint /tmp/test.yaml
datree test /tmp/test.yaml --ignore-missing-schemas

# 6. Run complete validation (includes KCL formatting/syntax)
./scripts/validate-kcl-compositions.sh
```

### Testing Different Scenarios

**Test with minimal configuration**:
```bash
crossplane render examples/app-basic.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/minimal.yaml
```

**Test with complete configuration**:
```bash
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/complete.yaml
```

**Compare outputs**:
```bash
diff -u /tmp/minimal.yaml /tmp/complete.yaml | less
```

### Creating Custom Test Examples

**Create a custom claim for testing**:

```yaml
# /tmp/my-test-app.yaml
apiVersion: cloud.ogenki.io/v1alpha1
kind: App
metadata:
  name: test-app
  namespace: apps
spec:
  image: nginx:1.25
  replicas: 3
  database:
    enabled: true
    size: small
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
```

**Render custom claim**:
```bash
cd infrastructure/base/crossplane/configuration
crossplane render /tmp/my-test-app.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/my-test-rendered.yaml
```

## Troubleshooting Rendering Issues

### Issue: Composition Not Found

**Symptom**: `Error: composition not found`

**Fix**:
- Ensure you're in `infrastructure/base/crossplane/configuration/` directory
- Verify composition file exists and path is correct
- Check composition file syntax with `yq` or `kubectl`

### Issue: Function Not Found

**Symptom**: `Error: function not found` or `unknown function`

**Fix**:
- Verify `functions.yaml` exists in the same directory
- Check function images are accessible
- Ensure Docker is running (required for `crossplane render`)

### Issue: EnvironmentConfig Missing

**Symptom**: References to environment config fail

**Fix**:
- Always include `--extra-resources examples/environmentconfig.yaml`
- Verify the EnvironmentConfig file exists
- Check the EnvironmentConfig spec matches composition expectations

### Issue: Render Succeeds but Resources Are Wrong

**Symptom**: Render completes but output doesn't match expectations

**Debug steps**:
1. Check the claim file matches the composition schema
2. Verify EnvironmentConfig has required fields
3. Review KCL code in `infrastructure/base/crossplane/configuration/kcl/<module>/`
4. Check for conditional logic that might affect output
5. Use `kcl-composition-validator` skill to validate KCL syntax

### Issue: Docker Not Available

**Symptom**: `Error: cannot connect to Docker daemon`

**Fix**:
```bash
# Start Docker
sudo systemctl start docker

# Or use podman with docker alias
alias docker=podman
```

## Integration with Complete Validation

**For pre-commit validation**, use the comprehensive script:
```bash
./scripts/validate-kcl-compositions.sh
```

This runs:
1. KCL formatting (`kcl fmt`)
2. KCL syntax validation (`kcl run`)
3. **Crossplane rendering** (this skill)

**For security validation** (additional step):
```bash
# After rendering
polaris audit --audit-path /tmp/rendered.yaml --format=pretty
kube-linter lint /tmp/rendered.yaml
datree test /tmp/rendered.yaml --ignore-missing-schemas
```

## Common Validation Scenarios

### Scenario 1: Testing New Feature in Composition

```bash
# 1. Modify composition KCL
vim infrastructure/base/crossplane/configuration/kcl/app/main.k

# 2. Render with feature enabled
cd infrastructure/base/crossplane/configuration
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/test.yaml

# 3. Verify feature resources exist
grep "kind:" /tmp/test.yaml | sort | uniq -c

# 4. Security validation
polaris audit --audit-path /tmp/test.yaml --format=pretty
```

### Scenario 2: Validating Database Integration

```bash
# Render SQLInstance
crossplane render examples/sqlinstance-complete.yaml sql-instance-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml > /tmp/db.yaml

# Check generated resources
yq 'select(.kind == "Cluster")' /tmp/db.yaml  # CloudNativePG Cluster
yq 'select(.kind == "ScheduledBackup")' /tmp/db.yaml  # Backup config
yq 'select(.kind == "AtlasMigration")' /tmp/db.yaml  # Migrations

# Validate security
polaris audit --audit-path /tmp/db.yaml --format=pretty
```

### Scenario 3: Testing Environment-Specific Configuration

```bash
# Create test EnvironmentConfig
cat > /tmp/test-env.yaml <<EOF
apiVersion: cloud.ogenki.io/v1alpha1
kind: EnvironmentConfig
metadata:
  name: test-env
data:
  environment: prod
  region: us-west-2
EOF

# Render with custom environment
crossplane render examples/app-complete.yaml app-composition.yaml functions.yaml \
  --extra-resources /tmp/test-env.yaml > /tmp/prod-app.yaml

# Verify environment-specific settings
yq 'select(.kind == "Deployment") | .spec.replicas' /tmp/prod-app.yaml
```

## Performance Optimization

### Faster Rendering

**Render specific composition only** (skip others):
```bash
# Instead of running full validation script
crossplane render examples/app-basic.yaml app-composition.yaml functions.yaml \
  --extra-resources examples/environmentconfig.yaml
```

**Use local function images** (if available):
```bash
# Pull function images once
docker pull xpkg.upbound.io/crossplane-contrib/function-kcl:latest

# Subsequent renders will use cached image
```

### Selective Validation

**During development**, validate only what changed:
```bash
# Skip Polaris/kube-linter/Datree during rapid iteration
# Only run these before commit
```

**Before commit**, run all validations:
```bash
# Complete validation
./scripts/validate-kcl-compositions.sh

# Security validation
polaris audit --audit-path /tmp/rendered.yaml --format=pretty
kube-linter lint /tmp/rendered.yaml
datree test /tmp/rendered.yaml --ignore-missing-schemas
```

## Additional Resources

- Security validation details: See `security-validation.md` in this skill folder
- Rendering examples and scenarios: See `examples.md` in this skill folder
- Quick command reference: See `quick-reference.md` in this skill folder
- KCL-specific validation: Use `kcl-composition-validator` skill

## Success Criteria

Validation is successful when:
1. ✅ Composition renders without errors
2. ✅ No duplicate resources in output
3. ✅ Polaris score is 85+ with no critical issues
4. ✅ kube-linter reports no errors
5. ✅ Datree policy check passes (or warnings documented)
6. ✅ Resources match expected count and structure
7. ✅ All required fields are populated correctly
