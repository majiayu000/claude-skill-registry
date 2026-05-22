---
name: android-gradle
description: Automate Gradle tasks for Android projects - build, test, coverage, clean. Use when building APKs, running unit tests, generating coverage reports, or checking dependencies.
license: MIT
version: 1.0.0
---

# Android Gradle Skill

Automate Gradle tasks for Android projects: build, test, coverage, clean.

## When to Use

- Building debug/release APK
- Running unit tests
- Generating coverage reports
- Cleaning build cache
- Checking dependencies

## Commands

### Build Commands

| Command | Description | Gradle Task |
|---------|-------------|-------------|
| `build` | Build debug APK | `./gradlew assembleDebug` |
| `build:release` | Build release APK | `./gradlew assembleRelease` |
| `install` | Install to device | `./gradlew installDebug` |
| `clean` | Clean build cache | `./gradlew clean` |
| `rebuild` | Clean + build | `./gradlew clean assembleDebug` |

### Test Commands

| Command | Description | Gradle Task |
|---------|-------------|-------------|
| `test` | Run all unit tests | `./gradlew testDebugUnitTest` |
| `test:class` | Run single class | `./gradlew test --tests "*.ClassName"` |
| `test:method` | Run single test | `./gradlew test --tests "*.Class.method"` |

### Coverage Commands

| Command | Description | Gradle Task |
|---------|-------------|-------------|
| `coverage` | Full coverage report | `./gradlew jacocoTestDebugUnitTestReport` |
| `coverage:verify` | Enforce 80% minimum | `./gradlew jacocoVerification` |

### Dependency Commands

| Command | Description | Gradle Task |
|---------|-------------|-------------|
| `deps` | Show dependency tree | `./gradlew dependencies` |
| `deps:app` | App module only | `./gradlew :app:dependencies` |
| `outdated` | Check outdated deps | `./gradlew dependencyUpdates` |

## Usage Examples

```bash
# Build and install debug APK
./gradlew assembleDebug && ./gradlew installDebug

# Run specific test class
./gradlew test --tests "*.GameManagerImplTest"

# Generate coverage report
./gradlew jacocoTestDebugUnitTestReport
# Report at: app/build/reports/jacoco/jacocoTestDebugUnitTestReport/html/index.html

# Clean rebuild
./gradlew clean assembleDebug
```

## Timeout Configuration

| Task Type | Timeout |
|-----------|---------|
| assembleDebug | 2 min |
| testDebugUnitTest | 3 min |
| jacocoTestDebugUnitTestReport | 2 min |
| clean | 30 sec |
| dependencies | 30 sec |

## Version Compatibility

| Gradle | AGP | Kotlin | JDK |
|--------|-----|--------|-----|
| 8.10+ | 8.8+ | 2.1+ | 17+ |
| 8.5+ | 8.5+ | 2.0+ | 17+ |
| 8.0+ | 8.0+ | 1.9+ | 17+ |

## Error Handling

```kotlin
// Handle build failures in scripts
fun handleGradleResult(exitCode: Int, output: String) {
    when {
        exitCode != 0 && output.contains("Compilation failed") ->
            println("Fix compilation errors in: ${extractErrorFiles(output)}")
        exitCode != 0 && output.contains("AAPT") ->
            println("Resource error - check XML files")
        exitCode != 0 && output.contains("OutOfMemoryError") ->
            println("Increase heap: org.gradle.jvmargs=-Xmx4g")
    }
}
```

**Common Errors:**
- **Build failure**: Parse error message, check file:line references
- **Test failure**: Run with `--info` for stack traces
- **Coverage below threshold**: Check `app/build/reports/jacoco/*/html/index.html`
- **OOM**: Increase heap in `gradle.properties`

## Test Result Validation

```bash
# Run tests and validate results
./gradlew testDebugUnitTest && echo "✓ All tests passed" || echo "✗ Tests failed"

# Check coverage threshold
./gradlew jacocoTestDebugUnitTestReport
# Verify: app/build/reports/jacoco/jacocoTestDebugUnitTestReport/html/index.html
# Target: 80%+ line coverage

# Parse test results programmatically
cat app/build/test-results/testDebugUnitTest/*.xml | grep -E "(tests=|failures=)"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build hangs | Kill daemon: `./gradlew --stop` |
| Cache issues | Clean: `./gradlew clean cleanBuildCache` |
| OOM errors | Add to gradle.properties: `org.gradle.jvmargs=-Xmx4g` |
| Version conflict | Force resolution in build.gradle.kts |
| Slow builds | Enable: `org.gradle.parallel=true` |

## Command Workflows

```bash
# Full CI workflow
./gradlew clean testDebugUnitTest jacocoTestDebugUnitTestReport assembleDebug

# Quick iteration
./gradlew assembleDebug -x lint -x test && ./gradlew installDebug

# Pre-commit check
./gradlew ktlintCheck testDebugUnitTest
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Build & Test
  run: |
    ./gradlew testDebugUnitTest
    ./gradlew jacocoTestDebugUnitTestReport
    ./gradlew assembleDebug

- name: Upload Coverage
  uses: codecov/codecov-action@v4
  with:
    files: app/build/reports/jacoco/*/jacoco*.xml
```

## Best Practices

- Always use Gradle wrapper (`./gradlew`), never system Gradle
- Use `--parallel` for multi-module projects
- Enable configuration cache for faster builds
- Skip lint with `-x lint` if not needed for quick iterations

## References

- [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html)
- [Android Gradle Plugin](https://developer.android.com/build)
- [JaCoCo Coverage](https://docs.gradle.org/current/userguide/jacoco_plugin.html)
