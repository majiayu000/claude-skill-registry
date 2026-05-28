---
name: start-new-sdk-project
description: Use when you have an OpenAPI spec and want to generate an SDK, or asking "how do I get started with Speakeasy"
---

# start-new-sdk-project

Use `speakeasy quickstart` to initialize a new project with a workflow configuration.

## Prerequisites

For non-interactive environments (CI/CD, AI agents), set:
```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```
See `configure-authentication` skill for details.

## Command

```bash
speakeasy quickstart -s <path-to-openapi-spec> -t <target-language>
```

## Supported Targets

| Language | Target Flag |
|----------|-------------|
| TypeScript | `typescript` |
| Python | `python` |
| Go | `go` |
| Java | `java` |
| C# | `csharp` |
| PHP | `php` |
| Ruby | `ruby` |
| Kotlin | `kotlin` |
| Terraform | `terraform` |

## Example

```bash
# Initialize TypeScript SDK project
speakeasy quickstart -s ./api/openapi.yaml -t typescript

# With custom output directory
speakeasy quickstart -s ./api/openapi.yaml -t python -o ./sdks/python
```

## What It Creates

```
.speakeasy/
└── workflow.yaml    # Workflow configuration
```

## Next Steps After Quickstart

1. Run `speakeasy run` to generate the SDK
2. Review the generated SDK in the output directory
3. Add more targets to workflow.yaml for multi-language support
