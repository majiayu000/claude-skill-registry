---
name: aws-sam-bootstrap
description: "Provides AWS SAM bootstrap patterns: generates `template.yaml` and `samconfig.toml` for new projects via `sam init`, creates SAM templates for existing Lambda/CloudFormation code migration, validates build/package/deploy workflows, and configures local testing with `sam local invoke`. Use when the user asks about SAM projects, `sam init`, `sam deploy`, serverless deployments, or needs to bootstrap/migrate Lambda functions with SAM templates."
allowed-tools: Read, Write, Bash
---

# AWS SAM Bootstrap

## Overview

Generates SAM project artifacts for greenfield and migration scenarios. Creates the minimum required files (`template.yaml`, `samconfig.toml`, `events/`), validates with `sam build`, and configures `sam deploy` workflows following AWS SAM conventions.

## When to Use

- User needs to start a new AWS SAM project (`sam init`, `sam deploy`)
- User wants to migrate existing Lambda functions or CloudFormation resources to SAM templates
- User asks about SAM CLI commands (`sam init`, `sam build`, `sam local invoke`, `sam deploy`)
- User needs to create or update `template.yaml` or `samconfig.toml` for serverless deployments
- User wants to configure local testing with `sam local invoke` for Lambda functions

## Instructions

### 1) Classify Scenario

- **New project**: no Lambda structure exists. Run `sam init` to scaffold.
- **Existing project migration**: Lambda/CloudFormation resources exist. Create `template.yaml` manually.

### 2) Select Runtime and Package Type

Use current non-deprecated runtimes. Package type: **Zip** (default) or **Image** (container/native deps).

### 3) Bootstrap New Projects

```bash
sam init
sam build
sam local invoke <LogicalFunctionId> -e events/event.json
sam deploy --guided
```

### 4) Bootstrap Existing Projects

1. Inspect current Lambda handlers, runtime, and dependency layout
2. Create `template.yaml` with `Transform: AWS::Serverless-2016-10-31`
3. Map existing resources to `AWS::Serverless::Function` and related SAM resources
4. Create `samconfig.toml` with deploy defaults and environment overrides
5. Add `events/event.json` payload samples for local invocation
6. Validate with `sam validate` and `sam build` before deploy

### 5) Required Artifacts

```
.
├── template.yaml
├── samconfig.toml
└── events/
    └── event.json
```

See reference templates: [examples.md](references/examples.md), [migration-checklist.md](references/migration-checklist.md)

### 6) Validation Checklist

- `sam validate` succeeds
- `sam build` succeeds
- `template.yaml` has correct logical IDs and handlers
- `samconfig.toml` contains deploy parameters for target environments

## Examples

### New SAM Project

```bash
sam init  # Interactive scaffold
sam build
sam local invoke HelloFunction -e events/event.json
sam deploy --guided
```

### Migrate Existing Lambda

1. Detect handler/runtime → create `template.yaml` with SAM transform
2. Add `samconfig.toml` with `stack_name`, `capabilities`, `resolve_s3`
3. Add `events/event.json` → validate with `sam build`

Full templates in [references/examples.md](references/examples.md).

## Best Practices

- One deployable function first, then expand; keep migration-first PRs minimal
- Keep `samconfig.toml` committed for deterministic deployments
- Use environment-specific sections (`[default]`, `[prod]`) instead of CLI flags
- Map existing handler paths to SAM conventions during migration

## Constraints and Warnings

- SAM CLI must be installed locally for command execution
- `CAPABILITY_IAM` is required when IAM resources are created
- Container image packaging requires Docker availability
- Existing projects may require refactoring handler paths to match SAM conventions
- `sam deploy --guided` writes local configuration; review before committing
