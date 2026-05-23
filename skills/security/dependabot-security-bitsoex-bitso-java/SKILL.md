---
name: dependabot-security
description: >
  Fix Dependabot security vulnerabilities in Java/Gradle projects using severity-based
  processing, dependency substitution strategies, and dependency graph verification.
  Use when Dependabot alerts need resolution with proper CI validation.
compatibility: Java projects using Gradle with dependency-graph plugin
metadata:
  version: "1.0.0"
  technology: java
  category: security
  tags:
    - java
    - gradle
    - security
    - dependabot
    - vulnerabilities
    - cve
---

# Dependabot Security

Fix Dependabot security vulnerabilities in Java/Gradle projects with proper verification.

## When to use this skill

- Resolving Dependabot security alerts
- Fixing CVE vulnerabilities in dependencies
- Verifying dependency graph for CI compliance
- Choosing the right fix strategy for transitive dependencies
- Understanding why `dependency-review` CI check fails

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L25-L32)
- [Quick Start](#quick-start) (L54-L91)
- [Key Concepts](#key-concepts) (L92-L118)
- [References](#references) (L119-L127)
- [Related Rules](#related-rules) (L128-L132)
- [Related Skills](#related-skills) (L133-L138)

### Available Resources

**📚 references/** - Detailed documentation
- [dependency graph](references/dependency-graph.md)
- [fix strategies](references/fix-strategies.md)
- [severity processing](references/severity-processing.md)
- [troubleshooting](references/troubleshooting.md)

---

## Quick Start

### 1. Create Jira ticket first

See `global/rules/jira-ticket-workflow.md` for ticket creation.

### 2. Get alerts by severity

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
gh api --paginate repos/$REPO/dependabot/alerts --jq '.[] | select(.state == "open") | {
  number, severity: .security_advisory.severity, package: .dependency.package.name,
  patched_version: .security_vulnerability.first_patched_version.identifier,
  cve: .security_advisory.cve_id
}'
```

### 3. Fix by severity (CRITICAL first, then HIGH, MEDIUM, LOW)

See [references/fix-strategies.md](references/fix-strategies.md) for strategy hierarchy.

### 4. Verify with dependency graph

```bash
./gradlew -I gradle/dependency-graph-init.gradle \
    --dependency-verification=off \
    :ForceDependencyResolutionPlugin_resolveAllDependencies

# Check ONLY patched versions appear
grep -i "package-name" build/reports/dependency-graph-snapshots/dependency-list.txt
```

### 5. Commit and create PR

```bash
git commit -m "🤖 🛡️ fix(security): [JIRA-KEY] resolve CRITICAL vulnerabilities"
```

## Key Concepts

### Severity-Based Processing

Process ONE severity level at a time, creating separate PRs for each:

| Priority | Severity | When to Process |
|----------|----------|-----------------|
| 1 | CRITICAL | Always first |
| 2 | HIGH | After no CRITICAL |
| 3 | MEDIUM | After no HIGH |
| 4 | LOW | After no MEDIUM |

### Dependency Graph vs Runtime Resolution

The dependency graph plugin reports ALL versions to GitHub, not just the resolved version.
Force rules alone won't fix `dependency-review` failures - use substitution to remove old versions.

### Fix Strategy Hierarchy

1. **BOM Update** - Update Spring Boot, gRPC, Protobuf BOM versions
2. **Version Catalog** - Update direct dependencies in `libs.versions.toml`
3. **Dependency Substitution** - Replace transitive dependencies
4. **Constraints** - Set minimum version floors
5. **Force Rules** - Quick fix (combine with substitution)
6. **Exclude + Add** - Last resort

## References

| Reference | Description |
|-----------|-------------|
| [references/fix-strategies.md](references/fix-strategies.md) | Detailed fix strategies with examples |
| [references/severity-processing.md](references/severity-processing.md) | Severity-based workflow |
| [references/dependency-graph.md](references/dependency-graph.md) | Dependency graph plugin setup and verification |
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Rules

- `.cursor/rules/java-vulnerability-golden-paths.mdc` - Proven fix patterns for common CVEs
- `.cursor/rules/java-versions-and-dependencies.mdc` - Version management policies

## Related Skills

| Skill | Purpose |
|-------|---------|
| [gradle-standards](../gradle-standards/SKILL.md) | Gradle configuration |
| [sonarqube-integration](../sonarqube-integration/SKILL.md) | Code quality checks |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/dependabot-security/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

