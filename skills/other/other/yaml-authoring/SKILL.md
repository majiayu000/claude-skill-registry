---
name: yaml-authoring
description: Create and validate YAML diagram files. Use when writing new diagrams or troubleshooting YAML syntax.
---

# YAML Diagram Authoring

## Basic Structure

```yaml
version: 1
docId: unique-document-id
title: "My Architecture Diagram"  # optional

nodes:
  - id: unique-id
    provider: aws  # Provider name (e.g., aws, gcp, azure)
    kind: compute.lambda  # Service category.type
    label: "Display Name"  # optional
    parent: container-id  # optional, for nesting in VPC/Subnet
    layout:  # optional for child nodes (auto-positioned)
      x: 100  # optional for child nodes
      y: 200  # optional for child nodes
      w: 200  # required for containers (VPC/Subnet)
      h: 150  # required for containers

edges:
  - id: edge-1
    from: source-node-id
    to: target-node-id
    label: "optional label"  # optional
```

## Auto-Layout

Child nodes (with `parent`) can omit `layout` entirely for automatic positioning:

```yaml
nodes:
  - id: vpc
    provider: aws
    kind: network.vpc
    layout: { x: 0, y: 0, w: 800, h: 600 }  # Container: explicit layout

  - id: ec2_1
    provider: aws
    kind: compute.ec2
    parent: vpc
    # No layout - auto-positioned at (40, 40)

  - id: ec2_2
    provider: aws
    kind: compute.ec2
    parent: vpc
    # No layout - auto-positioned at (200, 40)
```

**Auto-layout rules:**
- 3 columns per row
- 60px padding, 160px horizontal spacing, 140px vertical spacing
- Explicit `x`/`y` overrides auto-positioning
- Cannot specify only `x` or only `y` (both or neither)

## Node Kind Categories

The `kind` field uses a hierarchical format: `category.type` or `category.subcategory.type`

### Container Types (require w/h in layout)
| Kind | Description |
|------|-------------|
| `network.vpc` | Virtual Private Cloud |
| `network.subnet` | Subnet within VPC |

### Resource Types
| Category | Kind Examples |
|----------|---------------|
| `compute` | `compute.lambda`, `compute.ec2`, `compute.ecs`, `compute.eks` |
| `compute.lb` | `compute.lb.alb`, `compute.lb.nlb`, `compute.lb.elb` |
| `database` | `database.dynamodb`, `database.rds`, `database.aurora` |
| `storage` | `storage.s3`, `storage.efs`, `storage.ebs` |
| `integration` | `integration.apiGateway`, `integration.sns`, `integration.sqs`, `integration.eventBridge` |
| `security` | `security.iam`, `security.cognito`, `security.waf` |
| `analytics` | `analytics.kinesis`, `analytics.athena`, `analytics.glue` |

## Examples

### Simple Lambda + S3

```yaml
version: 1
docId: lambda-s3-example
title: "Lambda S3 Integration"

nodes:
  - id: fn
    provider: aws
    kind: compute.lambda
    label: "Process Upload"
    layout:
      x: 100
      y: 100
  - id: bucket
    provider: aws
    kind: storage.s3
    label: "uploads-bucket"
    layout:
      x: 300
      y: 100

edges:
  - id: fn-to-bucket
    from: fn
    to: bucket
```

### API with Database

```yaml
version: 1
docId: api-db-example
title: "REST API Architecture"

nodes:
  - id: api
    provider: aws
    kind: integration.apiGateway
    label: "REST API"
    layout:
      x: 100
      y: 200
  - id: handler
    provider: aws
    kind: compute.lambda
    label: "Handler"
    layout:
      x: 300
      y: 200
  - id: db
    provider: aws
    kind: database.dynamodb
    label: "Users Table"
    layout:
      x: 500
      y: 200

edges:
  - id: api-to-handler
    from: api
    to: handler
    label: "invoke"
  - id: handler-to-db
    from: handler
    to: db
    label: "read/write"
```

### VPC with Nested Resources

```yaml
version: 1
docId: vpc-example
title: "VPC Architecture"

nodes:
  - id: vpc
    provider: aws
    kind: network.vpc
    label: "Production VPC"
    layout:
      x: 50
      y: 50
      w: 600
      h: 400
  - id: public-subnet
    provider: aws
    kind: network.subnet
    label: "Public Subnet"
    parent: vpc
    layout:
      x: 70
      y: 100
      w: 250
      h: 300
  - id: alb
    provider: aws
    kind: compute.lb.alb
    label: "Application LB"
    parent: public-subnet
    layout:
      x: 100
      y: 150
  - id: lambda
    provider: aws
    kind: compute.lambda
    label: "API Handler"
    parent: public-subnet
    layout:
      x: 100
      y: 280

edges:
  - id: alb-to-lambda
    from: alb
    to: lambda
```

## Validation

```bash
# Validate and build to JSON
bun run packages/cli/src/index.ts build diagram.yaml

# Serve with live reload (default port: 3456)
bun run packages/cli/src/index.ts serve diagram.yaml
```

## Common Errors

### Missing Required Fields
```
Error: Missing required field "version"
Error: Missing required field "docId"
```
Ensure `version` and `docId` are at the document root.

### Duplicate IDs
```
Error: Duplicate node id: "my-node"
```
Each node and edge must have a unique `id`.

### Missing Edge ID
```
Error: Edge must have an id
```
All edges require an `id` field.

### Missing Layout
```
Error: layout is required for top-level nodes
Error: layout.x is required for top-level nodes
```
Top-level nodes (without `parent`) must have a `layout` with `x` and `y`. Child nodes can omit layout for auto-positioning.

### Partial Coordinates
```
Error: layout.x and layout.y must be both specified or both omitted
```
You cannot specify only `x` or only `y`. Either provide both, or omit both for auto-layout.

### Invalid Parent Reference
```
Error: Node "child" references unknown parent: "missing-vpc"
```
Ensure `parent` references an existing container node.

### Missing Edge Target
```
Error: Edge references unknown node: "missing-id"
```
Ensure `from` and `to` reference existing node IDs.

### YAML Syntax Error
```
Error: YAML parse error at line 5
```
Check indentation (2 spaces) and proper quoting.

## Tips

- Use descriptive IDs: `user-api` not `n1`
- Labels can include spaces and special characters (use quotes)
- Use `parent` to nest resources inside VPC/Subnet containers
- Container nodes (VPC, Subnet) require `w` and `h` in layout
- Child nodes can omit `layout` entirely for automatic grid positioning
- Use comments with `#` for documentation
- The `kind` field is flexible - use any string that makes sense for your architecture
