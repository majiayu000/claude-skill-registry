---
name: librel
description: >
  librel - Release management tools. VersionBumper handles semver version
  bumping for packages. ChangeDetector identifies changed packages between git
  commits. StackQuery retrieves CloudFormation stack outputs for deployments.
  Use for release automation, CI/CD pipelines, and deployment orchestration.
---

# librel Skill

## When to Use

- Bumping package versions (major/minor/patch)
- Detecting which packages changed between commits
- Retrieving CloudFormation outputs for deployment
- Automating release workflows

## Key Concepts

**VersionBumper**: Updates package.json version following semver rules.

**ChangeDetector**: Compares git refs to identify modified packages.

**StackQuery**: Retrieves AWS CloudFormation stack outputs for deployment
config.

## Usage Patterns

### Pattern 1: Bump version

```javascript
import { VersionBumper } from "@copilot-ld/librel";

const bumper = new VersionBumper("./packages/libagent");
await bumper.bump("minor"); // 1.0.0 -> 1.1.0
```

### Pattern 2: Detect changes

```javascript
import { ChangeDetector } from "@copilot-ld/librel";

const detector = new ChangeDetector(".");
const changed = await detector.getChangedPackages("main", "HEAD");
// ["libagent", "libmemory"]
```

## Integration

Used by CI/CD scripts for release automation and change detection.
