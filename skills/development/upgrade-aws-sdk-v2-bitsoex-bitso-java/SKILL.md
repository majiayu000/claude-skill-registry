---
name: upgrade-aws-sdk-v2
description: >
  Migrate from AWS SDK for Java v1 (com.amazonaws) to v2 (software.amazon.awssdk).
  Use when projects need to move away from deprecated AWS SDK v1 to the modern v2 API.
compatibility: Java projects using Gradle with AWS SDK dependencies
metadata:
  version: "2.0.0"
  technology: java
  category: modernization
  tags:
    - aws
    - sdk
    - migration
    - dependencies
    - upgrade
---

# Upgrade AWS SDK v2

Migrate Java projects from AWS SDK v1 (`com.amazonaws`) to v2 (`software.amazon.awssdk`).

## When to Use

- Project uses deprecated AWS SDK v1 (`com.amazonaws.*` imports)
- Dependabot/security scans flag v1 vulnerabilities
- Need features only available in v2 (async clients, HTTP/2, etc.)
- When asked to "upgrade to aws sdk v2"

## Skill Contents

### Sections

- [When to Use](#when-to-use) (L23-L29)
- [Critical: MSK IAM Authentication](#critical-msk-iam-authentication) (L49-L61)
- [Migration Strategy (Priority Order)](#migration-strategy-priority-order) (L62-L70)
- [Quick Start](#quick-start) (L71-L110)
- [References](#references) (L111-L116)
- [Related Command](#related-command) (L117-L120)
- [Related Resources](#related-resources) (L121-L124)

### Available Resources

**📚 references/** - Detailed documentation
- [migration patterns](references/migration-patterns.md)

---

## Critical: MSK IAM Authentication

When migrating to AWS SDK v2, also update `aws-msk-iam-auth` if using Kafka with MSK IAM.

**Error after migration:**
```
NoClassDefFoundError: com/amazonaws/auth/AWSCredentialsProvider
```

**Fix:** Update `aws-msk-iam-auth` to `2.3.5` (AWS SDK v2 compatible).

See [references/migration-patterns.md](references/migration-patterns.md) for details.

## Migration Strategy (Priority Order)

| Priority | Strategy | When to Use |
|----------|----------|-------------|
| 1 | **Update library** | A newer version of the library uses v2 |
| 2 | **Update BOM** | v1 comes from Spring Boot or other BOM |
| 3 | **Dependency substitution** | Replace v1 artifact with v2 equivalent |
| 4 | **Direct code migration** | Only if no library update available |

## Quick Start

### 1. Identify v1 Usages

```bash
# Find all files with v1 imports
grep -r "import com.amazonaws" --include="*.java" . | grep -v "/build/"

# Check dependency tree
./gradlew dependencies --configuration runtimeClasspath | grep -B5 "com.amazonaws"
```

### 2. Apply Migration

See `references/migration-patterns.md` for detailed code migration patterns.

**Dependency Substitution (in root build.gradle):**

```groovy
allprojects {
    configurations.configureEach {
        resolutionStrategy.dependencySubstitution {
            substitute module("com.amazonaws:aws-java-sdk-s3")
                using module("software.amazon.awssdk:s3:${libs.versions.aws.sdk.v2.get()}")
                because "Migrate to AWS SDK v2"
        }
    }
}
```

### 3. Validate

```bash
# Verify no v1 imports remain
grep -r "import com.amazonaws" --include="*.java" . | grep -v "/build/"

# Build and test
./gradlew clean build test
```

## References

| Reference | Content |
|-----------|---------|
| [references/migration-patterns.md](references/migration-patterns.md) | Code migration patterns for S3, SQS, SNS, Lambda |

## Related Command

This skill is referenced by: `/upgrade-to-aws-sdk-v2` (see `java/commands/`)

## Related Resources

- [AWS SDK v2 Developer Guide](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/)
- [AWS SDK v2 Migration Guide](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/migration.html)
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/upgrade-aws-sdk-v2/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

