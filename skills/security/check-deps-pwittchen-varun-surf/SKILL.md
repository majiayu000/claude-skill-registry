---
name: check-deps
description: Analyze Gradle dependencies for outdated versions, known CVEs, unnecessary transitive dependencies, and version conflicts
---

# Check Dependencies Skill

Analyze the project's Gradle dependencies for security vulnerabilities, version issues, and optimization opportunities.

## Instructions

### 1. Gather Dependency Information

Run the following commands to collect dependency data:

```bash
# Full dependency tree
./gradlew dependencies --configuration runtimeClasspath

# Check for dependency updates (if plugin available)
./gradlew dependencyUpdates 2>/dev/null || echo "Plugin not available"

# Build file for direct dependencies
cat build.gradle
```

### 2. Analyze Direct Dependencies

Read `build.gradle` and extract:
- All declared dependencies with versions
- Dependency management/BOM imports
- Plugin versions

Create a table of direct dependencies:

| Group | Artifact | Declared Version | Type |
|-------|----------|------------------|------|
| org.springframework.boot | spring-boot-starter-webflux | 3.5.x | implementation |

### 3. Check for Outdated Versions

For each major dependency, check current latest versions:

**Spring Ecosystem** (check spring.io):
- spring-boot-starter-* → Current stable: 3.5.x
- spring-ai-* → Current stable: 1.x

**HTTP Clients**:
- okhttp → Current stable: 4.12.x
- (check square.github.io/okhttp)

**JSON Processing**:
- gson → Current stable: 2.11.x

**Testing**:
- junit-jupiter → Current stable: 5.11.x
- truth → Current stable: 1.4.x
- mockwebserver → matches okhttp version
- playwright → Current stable: 1.49.x

**Build Plugins**:
- com.github.ben-manes.versions → for dependency updates
- org.owasp.dependencycheck → for CVE scanning

### 4. CVE Cross-Reference

Check for known vulnerabilities in dependencies:

**High-Risk Libraries to Verify**:
- Spring Framework (check spring.io/security)
- OkHttp (check GitHub security advisories)
- Gson (check GitHub security advisories)
- Netty (transitive from WebFlux)
- Jackson (if present, frequent CVEs)
- Log4j/Logback (logging frameworks)

**Use WebSearch** to check:
```
"[library-name] [version] CVE" site:nvd.nist.gov
"[library-name] security advisory" site:github.com
```

**Known Historical Issues**:
- Log4j < 2.17.0: Log4Shell (CVE-2021-44228)
- Spring4Shell: Spring Framework < 5.3.18
- Jackson-databind: Multiple CVEs in older versions
- Netty < 4.1.86: Various CVEs

### 5. Transitive Dependency Analysis

From the dependency tree output, identify:

**Unnecessary Transitive Dependencies**:
- Duplicate functionality (multiple JSON parsers, HTTP clients)
- Test dependencies leaking to runtime
- Optional dependencies pulled in

**Large Transitive Trees**:
- Dependencies bringing in many sub-dependencies
- Candidates for exclusion if not needed

**Example exclusion**:
```gradle
implementation('org.example:library') {
    exclude group: 'commons-logging', module: 'commons-logging'
}
```

### 6. Version Conflict Detection

Look for in the dependency tree:
- `->` indicators showing version resolution
- `(*)` indicating dependency was evicted
- Multiple versions of same artifact

**Example conflict**:
```
+--- com.squareup.okhttp3:okhttp:4.12.0
|    \--- org.jetbrains.kotlin:kotlin-stdlib:1.9.10 -> 1.9.22 (*)
```

**Resolution strategies**:
```gradle
configurations.all {
    resolutionStrategy {
        force 'org.example:library:1.2.3'
        failOnVersionConflict()
    }
}
```

### 7. Dependency Health Metrics

Calculate and report:
- Total direct dependencies
- Total transitive dependencies
- Average dependency tree depth
- Number of version conflicts
- Number of outdated dependencies

## Output Format

```markdown
## Dependency Analysis Report

### Summary
| Metric | Count |
|--------|-------|
| Direct dependencies | X |
| Transitive dependencies | Y |
| Outdated dependencies | Z |
| Version conflicts | N |
| Potential CVEs | M |

### Outdated Dependencies

| Dependency | Current | Latest | Severity | Notes |
|------------|---------|--------|----------|-------|
| org.springframework.boot:* | 3.4.0 | 3.5.0 | Medium | Minor version behind |
| com.squareup.okhttp3:okhttp | 4.11.0 | 4.12.0 | Low | Patch update |

### Security Vulnerabilities (CVEs)

#### Critical

| Dependency | Version | CVE | Description | Fix |
|------------|---------|-----|-------------|-----|
| (none found or list issues) |

#### High

| Dependency | Version | CVE | Description | Fix |
|------------|---------|-----|-------------|-----|

### Version Conflicts

| Artifact | Requested Versions | Resolved | Risk |
|----------|-------------------|----------|------|
| kotlin-stdlib | 1.9.10, 1.9.22 | 1.9.22 | Low |

### Unnecessary Transitive Dependencies

| Dependency | Pulled By | Reason to Exclude | Savings |
|------------|-----------|-------------------|---------|
| commons-logging | spring-* | Using SLF4J | ~60KB |

### Dependency Tree Highlights

```
// Notable branches from dependency tree
+--- org.springframework.boot:spring-boot-starter-webflux
|    +--- io.projectreactor:reactor-core:3.6.x
|    +--- io.projectreactor.netty:reactor-netty-http:1.1.x
```

### Recommendations

#### Immediate Actions (Security)
1. Upgrade X to version Y (CVE-XXXX-XXXXX)

#### Short-term (Maintenance)
1. Update spring-boot to latest 3.5.x
2. Add version constraints for transitive dependencies

#### Long-term (Optimization)
1. Consider adding OWASP dependency-check plugin
2. Set up Dependabot for automated updates

### Suggested build.gradle Additions

```gradle
// Add dependency update checking
plugins {
    id 'com.github.ben-manes.versions' version '0.51.0'
}

// Add OWASP CVE scanning
plugins {
    id 'org.owasp.dependencycheck' version '9.0.9'
}

// Force consistent versions
configurations.all {
    resolutionStrategy {
        // Add any necessary version forcing
    }
}
```
```

## Execution Steps

1. Run `./gradlew dependencies --configuration runtimeClasspath` via Bash
2. Read `build.gradle` to identify direct dependencies
3. Parse dependency tree for conflicts and transitive deps
4. Use WebSearch to check for recent CVEs on major dependencies
5. Compare versions against latest stable releases
6. Generate comprehensive report with actionable recommendations

## Notes

- Spring Boot manages many dependency versions via BOM - check parent version
- Focus on runtime dependencies; test scope is lower priority
- Some "conflicts" are normal (Gradle picks highest compatible version)
- CVE databases may have false positives for non-applicable vulnerabilities
- Consider dependency scope when evaluating necessity
