---
name: gradle-troubleshooting
description: |
  Analyzes and resolves common Gradle build issues including OutOfMemory errors,
  dependency conflicts, build cache problems, configuration cache failures, and slow builds.
  Use when asked to "debug Gradle build", "fix build failure", "troubleshoot Gradle",
  or "resolve dependency conflicts".
  Works with build.gradle.kts, gradle.properties, and build logs.
---

# Gradle Troubleshooting

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Commands Reference](#commands-reference)
- [See Also](#see-also)

## When to Use This Skill

Use this skill when you need to:
- Debug OutOfMemoryError or heap space issues
- Resolve dependency conflicts and version mismatches
- Fix build cache or configuration cache problems
- Diagnose slow build performance
- Troubleshoot daemon or wrapper issues
- Debug plugin loading failures
- Resolve TestContainers or Docker connectivity issues
- Investigate test failures in CI but not locally

## Quick Start

When a build fails, run in order:

```bash
# 1. Stop daemon and clean
./gradlew --stop
./gradlew clean

# 2. Run with diagnostics
./gradlew build --stacktrace --info

# 3. If still failing, generate build scan
./gradlew build --scan

# 4. If slow, profile
./gradlew build --profile
```

## Instructions

### Step 1: Diagnose with Debug Output

Run with increasing verbosity to identify the issue:

```bash
# Stack trace (shows where error occurred)
./gradlew build --stacktrace

# Full stack trace (complete call stack)
./gradlew build --full-stacktrace

# Info logging (what Gradle is doing)
./gradlew build --info

# Debug logging (very detailed, generates lots of output)
./gradlew build --debug

# Use grep to filter
./gradlew build --info 2>&1 | grep -i error
./gradlew build --info 2>&1 | grep cache
```

### Step 2: Identify the Issue Category

**OutOfMemoryError**:
```bash
./gradlew build 2>&1 | grep -i "outofmemory\|java heap\|metaspace"
```

**Dependency resolution**:
```bash
./gradlew dependencies --info 2>&1 | grep -i "could not\|failed\|error"
./gradlew dependencyInsight --dependency spring-core
```

**Build cache problems**:
```bash
./gradlew build --no-build-cache --info 2>&1 | grep cache
```

**Configuration cache**:
```bash
./gradlew build --no-configuration-cache --info
```

**Plugin issues**:
```bash
./gradlew build --stacktrace 2>&1 | grep -A 5 "plugin"
```

### Step 3: Fix OutOfMemoryError

**Immediate fix** - Increase heap size:

```bash
# For this build only
./gradlew build -Dorg.gradle.jvmargs="-Xmx8g"

# Or stop daemon and increase persistent memory
./gradlew --stop
```

**Permanent fix** - Update `gradle.properties`:

```properties
# For standard projects (10-30 modules)
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# For large projects (30+ modules)
org.gradle.jvmargs=-Xmx8g -XX:MaxMetaspaceSize=2g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# For very large projects
org.gradle.jvmargs=-Xmx12g -XX:MaxMetaspaceSize=3g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

**Verify fix**:

```bash
./gradlew --stop  # Must restart daemon
./gradlew build --info 2>&1 | grep "XX:Xmx"
```

### Step 4: Debug Dependency Resolution

Understand why dependencies aren't resolving:

```bash
# Show full dependency tree
./gradlew dependencies

# Show specific configuration
./gradlew dependencies --configuration implementation

# Find where a dependency comes from
./gradlew dependencyInsight --dependency spring-core

# Show dependency insights for specific config
./gradlew dependencyInsight --dependency jackson-databind --configuration implementation

# Refresh and re-download
./gradlew build --refresh-dependencies
```

**Common solutions**:

**Option 1: Force specific version**:

```kotlin
// build.gradle.kts
configurations.all {
    resolutionStrategy {
        force("com.google.guava:guava:32.1.3-jre")
    }
}
```

**Option 2: Exclude problematic transitive dependency**:

```kotlin
dependencies {
    implementation("com.example:library:1.0") {
        exclude(group = "commons-logging", module = "commons-logging")
    }
}
```

**Option 3: Use dependency constraints**:

```kotlin
dependencies {
    constraints {
        implementation("org.apache.commons:commons-lang3:3.18.0")
    }
}
```

### Step 5: Debug Build Cache Issues

Test if build cache is causing problems:

```bash
# Disable cache for this build
./gradlew build --no-build-cache

# If this fixes it, cache is the problem
# Clean cache
rm -rf ~/.gradle/caches/build-cache-*

# Check cache status
./gradlew build --build-cache --info | grep cache

# Verify task is cacheable
./gradlew build --info 2>&1 | grep "Cache key"
```

**Common build cache issues**:

**Issue**: Build slower with cache enabled

```bash
# Check for non-cacheable tasks
./gradlew build --info 2>&1 | grep -i "non-cacheable"
```

**Issue**: Incorrect cached results

```bash
# Clean entire cache
rm -rf ~/.gradle/caches

# Rebuild
./gradlew build
```

### Step 6: Debug Configuration Cache

Test if configuration cache is compatible:

```bash
# Start with warnings (not errors)
./gradlew build --configuration-cache-problems=warn

# Check report
# build/reports/configuration-cache/<hash>/configuration-cache-report.html

# Once issues fixed, enable strict mode
./gradlew build --configuration-cache-problems=fail
```

**Common configuration cache issues**:

**Issue**: Build fails with configuration cache

```bash
# Disable temporarily
./gradlew build --no-configuration-cache

# Check for incompatible plugins
./gradlew build --configuration-cache-problems=warn --info

# View detailed report
open build/reports/configuration-cache/report.html
```

**Issue**: Plugins not compatible

```bash
# Update plugins to latest versions
./gradlew wrapper --gradle-version 9.2
./gradlew build -x test  # Skip tests temporarily
```

For advanced troubleshooting including slow build analysis, daemon management, wrapper issues, and plugin resolution, see [references/advanced-troubleshooting.md](references/advanced-troubleshooting.md).

## Examples

### Example 1: Complete Troubleshooting Workflow

```bash
# 1. Initial failure
./gradlew build
# BUILD FAILED

# 2. Get details
./gradlew build --stacktrace
# Shows: OutOfMemoryError: Java heap space

# 3. Fix: Update gradle.properties
echo "org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g" >> gradle.properties

# 4. Stop daemon and retry
./gradlew --stop
./gradlew build

# BUILD SUCCESSFUL
```

### Example 2: Dependency Conflict Resolution

```bash
# Build fails with version conflict
./gradlew build
# ERROR: Could not resolve dependency: conflicting versions

# Investigate
./gradlew dependencyInsight --dependency commons-lang3

# You see:
# commons-lang3:3.8.1 <- old-library
# commons-lang3:3.18.0 <- new-library

# Solution: Force newer version
# In build.gradle.kts:
configurations.all {
    resolutionStrategy {
        force("org.apache.commons:commons-lang3:3.18.0")
    }
}

./gradlew build
# BUILD SUCCESSFUL
```


For advanced examples including slow build analysis, configuration cache debugging, and Docker troubleshooting, see [references/advanced-examples.md](references/advanced-examples.md).



## Commands Reference

See [references/commands-and-checklists.md](references/commands-and-checklists.md) for complete command reference, troubleshooting checklist, and quick reference table.

## See Also

- [gradle-testing-setup](../gradle-testing-setup/SKILL.md) - Configure testing infrastructure
- [gradle-performance-optimization](../gradle-performance-optimization/SKILL.md) - Optimize build performance
- [gradle-ci-cd-integration](../gradle-ci-cd-integration/SKILL.md) - CI/CD integration patterns
- [Gradle Documentation](https://docs.gradle.org/)
- [Gradle Build Scans](https://scans.gradle.com/)

