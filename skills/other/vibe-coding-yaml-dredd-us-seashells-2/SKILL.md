---
name: vibe-coding-yaml
description: AI outputs YAML descriptors instead of code, CLI executes deterministically for 100% auditable behavior with zero slop. Use when auditability is critical, generated code review needed, or deterministic execution required. YAML serves as intermediate representation. Triggers on "auditable generation", "YAML output", "deterministic execution", "code review", "vibe coding".
---

# Vibe Coding YAML

## Purpose

AI generates YAML descriptors instead of code, CLI executes deterministically for 100% auditable behavior with zero slop.

## When to Use

- Auditable code generation
- Deterministic outputs required
- Generated code review needed
- UI component generation
- Infrastructure as code
- Compliance requirements

## Core Instructions

### Pattern

AI outputs YAML:
```yaml
component:
  type: Button
  props:
    text: "Submit"
    variant: "primary"
    onClick: "handleSubmit"
  styles:
    padding: "12px 24px"
    borderRadius: "8px"
    backgroundColor: "#007bff"
```

CLI executes deterministically:
```bash
generate-component component.yaml > Button.tsx
```

### Benefits

- **100% auditable**: Review YAML, not generated code
- **Zero slop**: Deterministic execution
- **Versionable**: YAML in Git
- **Reproducible**: Same YAML = same output
- **Reviewable**: Easier to review descriptors than code

### Example Workflow

```python
# 1. AI generates descriptor
descriptor = {
    'type': 'api_endpoint',
    'method': 'POST',
    'path': '/users',
    'handler': 'createUser',
    'validation': {
        'email': 'required|email',
        'name': 'required|string'
    }
}

# 2. Save as YAML
with open('endpoint.yaml', 'w') as f:
    yaml.dump(descriptor, f)

# 3. Execute deterministically
$ generate-endpoint endpoint.yaml > routes/users.ts

# 4. Review YAML (not generated code)
$ git diff endpoint.yaml
```

## Performance

- **100% auditable**
- **0% slop rate**
- Deterministic behavior
- Easy review process

## Version

v1.0.0 (2025-10-23)

