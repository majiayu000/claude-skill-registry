---
name: aws-sam-bootstrap
description: Provides AWS Serverless Application Model (SAM) bootstrap patterns for new and existing projects. Use when initializing SAM projects with `sam init`, migrating existing Lambda/CloudFormation projects to SAM, generating `template.yaml` and `samconfig.toml`, preparing local test events, and configuring build/package/deploy workflows with `sam build`, `sam package`, `sam deploy --guided`, and `sam local invoke`.
allowed-tools: Read, Write, Bash
---

# AWS SAM Bootstrap

## Overview

Bootstrap AWS SAM projects end-to-end for both greenfield and migration scenarios. Generate the minimum required artifacts for reliable `sam build` and `sam deploy` workflows while following AWS SAM conventions.

## When to Use

Use this skill when:
- Configuring AWS SAM for an existing Lambda or CloudFormation-based project
- Creating a new serverless project with AWS SAM from scratch
- Adding `template.yaml` and `samconfig.toml` to standardize deployments
- Setting up local testing with `sam local invoke` and sample event payloads
- Defining environment-aware deploy settings (for example `default` and `prod`)

Trigger phrases:
- "Configure AWS SAM for this project"
- "Create a new SAM project"
- "Add template.yaml for SAM"
- "Initialize SAM for existing Lambda function"
- "Generate samconfig.toml"

## Instructions

### 1) Classify the Scenario

Identify one path before writing files:
- **New project**: no deployable Lambda structure exists yet.
- **Existing project migration**: Lambda code and/or CloudFormation resources already exist.

### 2) Choose Runtime and Package Type

Select runtime and package mode first, then keep all generated files consistent.

Supported runtime families:
- Python: `python3.10` to `python3.14` (avoid 3.8/3.9, deprecated)
- Node.js: `nodejs20.x`, `nodejs22.x`, `nodejs24.x` (avoid 18.x, deprecated)
- Java: `java8.al2`, `java11`, `java17`, `java21`, `java25`
- Go: `provided.al2`, `provided.al2023`
- .NET: `dotnet8`, `dotnet9`, `dotnet10` (avoid dotnet6, deprecated)
- Ruby: `ruby3.2`, `ruby3.3`, `ruby3.4`

Package type:
- **Zip**: default for most functions
- **Image**: choose when container packaging or native dependencies are needed

### 3) Bootstrap New Projects

For new projects:
1. Run `sam init` with explicit runtime, architecture, and package type.
2. Keep the generated structure minimal and production-oriented.
3. Add/adjust `samconfig.toml` with environment-specific deploy settings.
4. Add `events/` payloads for local test commands.

Recommended command sequence:

```bash
sam init
sam build
sam local invoke <LogicalFunctionId> -e events/event.json
sam deploy --guided
```

### 4) Bootstrap Existing Projects

For existing projects:
1. Inspect current Lambda handlers, runtime, and dependency layout.
2. Create `template.yaml` with `Transform: AWS::Serverless-2016-10-31`.
3. Map existing resources into `AWS::Serverless::Function` and related SAM resources.
4. Create `samconfig.toml` with deploy defaults and environment overrides.
5. Add `events/` payload samples for local invocation.
6. Validate with `sam validate` and `sam build` before deploy.

Migration sequence:

```bash
sam validate
sam build
sam local invoke <LogicalFunctionId> -e events/event.json
sam deploy --guided
```

### 5) Ensure Required Artifacts Exist

Always produce and verify these artifacts:

```text
.
├── template.yaml
├── samconfig.toml
└── events/
    └── event.json
```

Use reference templates from:
- [SAM Template Examples](references/examples.md)
- [Migration Checklist](references/migration-checklist.md)

### 6) Configure samconfig.toml Correctly

At minimum:
- `stack_name`
- `capabilities` (typically `CAPABILITY_IAM`)
- `resolve_s3 = true`
- environment separation (`default`, optional `prod`)
- optional build acceleration (`cached = true`, `parallel = true`)

Baseline example:

```toml
version = 0.1

[default.global.parameters]
stack_name = "my-sam-app"

[default.build.parameters]
cached = true
parallel = true

[default.deploy.parameters]
capabilities = "CAPABILITY_IAM"
confirm_changeset = true
resolve_s3 = true

[prod.deploy.parameters]
confirm_changeset = false
```

### 7) Standard Command Coverage

Use these commands according to task phase:
- `sam init` for new projects
- `sam build` to compile/package artifacts
- `sam deploy --guided` for first deployment configuration
- `sam package` when explicit packaging step is required
- `sam local invoke` for local function execution with event payloads

### 8) Validate Before Finalizing

Run this verification checklist:
- `sam validate` succeeds
- `sam build` succeeds
- `template.yaml` has correct logical IDs and handlers
- `samconfig.toml` contains deploy parameters for target environments
- `events/event.json` matches handler input expectations

## Examples

### Example A: Create a New SAM App

User request: "Create a new SAM project for a Python Lambda API"

Response approach:
1. Initialize with `sam init` and Python runtime.
2. Confirm package type (`Zip` by default).
3. Generate `samconfig.toml` with `default` and `prod` deploy parameters.
4. Add `events/event.json`.
5. Validate with `sam build` and `sam local invoke`.

Input:

```text
Create a new SAM project for a Python Lambda API with a /hello endpoint.
```

Output:

```text
Generated files:
- template.yaml (AWS::Serverless::Function + API event)
- samconfig.toml (default/prod deploy settings)
- events/event.json

Commands to run:
sam build
sam local invoke HelloFunction -e events/event.json
sam deploy --guided
```

### Example B: Migrate Existing Lambda Project

User request: "Configure AWS SAM for this existing Lambda project"

Response approach:
1. Detect current handler/runtime from the codebase.
2. Create `template.yaml` with SAM transform and function definition.
3. Generate `samconfig.toml` including `stack_name`, `capabilities`, and `resolve_s3`.
4. Add local test events.
5. Run validate/build/deploy workflow commands.

Input:

```text
Configure AWS SAM for this existing Lambda project and prepare deployment artifacts.
```

Output:

```text
Migration result:
- Added template.yaml with Transform AWS::Serverless-2016-10-31
- Added samconfig.toml with deployment parameters
- Added events/event.json for local testing
- Validation workflow prepared:
  sam validate
  sam build
  sam deploy --guided
```

## Best Practices

- Keep template resources explicit and minimal; avoid unrelated infrastructure in migration-first PRs
- Prefer one deployable function flow first, then expand to multiple functions
- Keep `samconfig.toml` committed for deterministic deployments
- Use environment-specific sections instead of ad-hoc CLI flags
- Define IAM permissions with least privilege
- Add local events that reflect real payloads used in production integrations

## Constraints and Warnings

- SAM CLI must be installed locally for command execution
- `CAPABILITY_IAM` is required when IAM resources are created
- Container image packaging requires Docker availability
- Existing projects may require refactoring handler paths to match SAM conventions
- `sam deploy --guided` writes local configuration; review before committing
