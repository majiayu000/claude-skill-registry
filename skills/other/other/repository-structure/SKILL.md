---
name: repository-structure
description: Monorepo structure, subpackage organization, and dependency rules. Use when creating new packages, understanding project layout, or organizing code.
---

# Repository Structure

This is a **CDK monorepo** using npm workspaces. All packages share a synchronized `aws-cdk-lib` version.

## Directory Structure

```
cdk-constructs-library/
├── package.json              # Root package (@cdk-constructs/cdk) - core utilities, types, enums
├── tsconfig.json             # Root TypeScript config (builds src/)
├── tsconfig.app.json         # CDK app TypeScript config (builds bin/, lib/)
├── tsconfig.build.json       # Workspace build references
├── packages/
│   ├── aws/                  # @cdk-constructs/aws - AWS account, region, environment enums
│   ├── codeartifact/         # @cdk-constructs/codeartifact - CodeArtifact constructs
│   ├── api-gateway/          # @cdk-constructs/api-gateway - API Gateway & Lambda constructs
│   ├── aurora/               # @cdk-constructs/aurora - Aurora database constructs
│   ├── cloudwatch/           # @cdk-constructs/cloudwatch - CloudWatch monitoring
│   ├── eks/                  # @cdk-constructs/eks - EKS utilities and VPC constants
│   └── waf/                  # @cdk-constructs/waf - WAF configurations
├── src/                      # Root package source (type-driven development)
│   ├── constructs/           # Shared base constructs and utilities
│   ├── enums/                # Shared enums
│   ├── types/                # Shared types (types, not interfaces)
│   └── util/                 # Shared utilities
├── bin/                      # CDK app entry point
│   ├── app.ts                # Main CDK application
│   └── environment.ts        # Environment configurations
├── lib/                      # CDK stack implementations
│   └── stacks/               # Stack classes for testing
├── docs/                     # Documentation
├── scripts/                  # Build and maintenance scripts
└── test/                     # Test files
```

## Architecture Decisions

- **Monorepo Strategy**: This is a monorepo containing multiple subpackages, each independently versioned
- **Type-Driven Development**: All data structures use `type` declarations, not `interface`
- **Subpackage Structure**: Each subpackage follows `src/types`, `src/enums`, `src/constructs`, etc.
- **Root Package Purpose**: Provides shared types, enums, and utilities used across subpackages
- **New Feature Placement**: Domain-specific constructs go in dedicated subpackages (e.g., `@cdk-constructs/api-gateway`)
- **CDK Version Sync**: All packages must use the same `aws-cdk-lib` version
- **No Circular Dependencies**: Packages are structured to prevent dependency loops

## Subpackage Structure

Each subpackage follows this standard structure for full organization:

```
packages/{package-name}/
├── package.json              # Package config with workspace dependencies
├── tsconfig.json             # Extends ../../tsconfig-strict.json
├── src/
│   ├── index.ts              # Public exports
│   ├── types/                # Package-specific types (type-driven development)
│   ├── enums/                # Package-specific enums
│   ├── constructs/           # CDK construct implementations
│   └── util/                 # Package-specific utilities
├── test/                     # Test files and example stacks
├── docs/                     # Package documentation (optional)
└── README.md                 # Package documentation
```

**Organization Principles:**

- `src/types/` - All data structures using `type` declarations (not `interface`)
- `src/enums/` - Enumeration definitions (e.g., AWS regions, accounts)
- `src/constructs/` - CDK construct factory functions
- `src/util/` - Helper functions and utilities

## Dependency Structure

```
@cdk-constructs/cdk (root)
├── @cdk-constructs/aws (no dependencies on other packages)
├── @cdk-constructs/codeartifact (depends on: aws)
├── @cdk-constructs/api-gateway (depends on: cdk)
├── @cdk-constructs/aurora (depends on: cdk)
├── @cdk-constructs/eks (depends on: cdk)
├── @cdk-constructs/waf (depends on: cdk)
└── @cdk-constructs/cloudwatch (depends on: cdk, api-gateway)
```

**Rules:**

- Root package never depends on subpackages
- Subpackages can depend on root package
- Subpackages can depend on other subpackages only if no cycle is created
- Always build in dependency order
