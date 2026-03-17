---
name: maven-tools
description: "JVM dependency intelligence via Maven Tools MCP server. Use when user asks about Java/Kotlin/Scala dependencies, versions, upgrades, CVEs, or licenses. Use when analyzing pom.xml, build.gradle, or any Maven Central dependency. Use when user says 'check my dependencies', 'should I upgrade X', 'is this version safe', or 'what's the latest version of Y'."
allowed-tools: mcp__maven-tools__*
---

# Maven Tools

Dependency intelligence for JVM projects via Maven Tools MCP server.

## Prerequisites

Requires [Maven Tools MCP server](https://github.com/arvindand/maven-tools-mcp) configured in your MCP client.

**Recommended setup (Claude Desktop):**

```json
{
  "mcpServers": {
    "maven-tools": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "arvindand/maven-tools-mcp:latest-noc7"]
    }
  }
}
```

**Why `-noc7`?** The `latest-noc7` variant focuses purely on dependency intelligence. For documentation lookup, use the separate [context7 skill](../context7/) which provides broader coverage and works independently. This modular approach means dependency tools work even if Context7 is blocked.

## When to Use

**Activate automatically when:**

- User asks about Java/Kotlin/Scala/JVM dependencies
- User mentions Maven, Gradle, pom.xml, build.gradle
- User asks "what's the latest version of X"
- User wants to check for updates, CVEs, or license issues
- User says "analyze my dependencies" or "check my pom.xml"
- User asks "should I upgrade X" or "is this version safe"

## Tool Selection

Pick the right tool for the task (8 tools available):

| User Intent | Tool | Key Parameters |
|-------------|------|----------------|
| "Latest version of X" | `get_latest_version` | `stabilityFilter`: PREFER_STABLE (default) |
| "Does version X.Y.Z exist?" | `check_version_exists` | — |
| "Check these dependencies" (no versions) | `check_multiple_dependencies` | `stabilityFilter` |
| "Should I upgrade from X to Y?" | `compare_dependency_versions` | `includeSecurityScan`: true |
| "How old are my dependencies?" | `analyze_dependency_age` | `maxAgeInDays` threshold |
| "Is this library maintained?" | `analyze_release_patterns` | `monthsToAnalyze`: 24 |
| "Show version history" | `get_version_timeline` | `versionCount`: 20 |
| "Full health check" | `analyze_project_health` | `includeSecurityScan`, `includeLicenseScan` |

**Default choice:** When user says "check my dependencies" or pastes a pom.xml → use `analyze_project_health` for comprehensive analysis.

## Stability Filters

Control which versions are returned:

| Filter | Use When |
|--------|----------|
| `PREFER_STABLE` | Default for recommendations — prioritizes stable, includes others |
| `STABLE_ONLY` | Production upgrades — no RC/beta/alpha |
| `ALL` | Research — see everything including snapshots |

## Common Workflows

### "Check my dependencies"

1. Extract dependencies from pom.xml or user input
2. Call `analyze_project_health` with:
   - `includeSecurityScan: true`
   - `includeLicenseScan: true`
3. Report: outdated deps, CVEs, license risks, health score

### "Should I upgrade Spring Boot?"

1. Call `compare_dependency_versions` with current and target versions
2. If major upgrade detected, note breaking changes likely
3. Use context7 skill for migration documentation:
   - `scripts/context7.py search "spring boot"`
   - `scripts/context7.py docs "<library-id>" "migration guide"`

### "Is this dependency safe?"

1. Call `get_latest_version` to check if user's version is current
2. Call `analyze_release_patterns` to verify active maintenance
3. Security scan is included by default — report any CVEs

### "What libraries should I use for X?"

1. This tool doesn't recommend new libraries — it analyzes existing ones
2. Suggest user specify candidate libraries
3. Then use `analyze_project_health` to compare candidates

## Dependency Format

All tools expect Maven coordinates:

```
groupId:artifactId
```

**Examples:**

- `org.springframework.boot:spring-boot-starter`
- `com.fasterxml.jackson.core:jackson-databind`
- `org.junit.jupiter:junit-jupiter`

**From Gradle:** Convert `implementation("group:artifact:version")` → `group:artifact`

## Documentation Lookup (Guided Delegation)

Maven Tools provides version intelligence. For migration guides and API documentation, delegate to the [context7 skill](../context7/).

**Workflow:**

1. Maven analysis reveals upgrade needed (e.g., Spring Boot 2→3)
2. Load context7 skill for documentation lookup
3. Query: "spring boot 3 migration guide" or "hibernate 6 breaking changes"
4. Combine version data + documentation for complete upgrade plan

**Example chain:**

```
User: "Should I upgrade Spring Boot from 2.7 to 3.2?"

→ maven-tools: compare_dependency_versions
  Result: Major upgrade, 3.2.1 available, no CVEs

→ context7: scripts/context7.py search "spring boot"
→ context7: scripts/context7.py docs "/spring-projects/spring-boot" "2.7 to 3 migration"
  Result: javax→jakarta migration steps, config changes

→ Combined response: Version analysis + migration steps
```

This separation means:

- Dependency tools work even if Context7 is unreachable
- Context7 skill is reusable for any library, not just JVM
- Each skill stays focused and maintainable

## Response Interpretation

### Health Scores

| Score | Meaning |
|-------|---------|
| 80-100 | Healthy — recent releases, no CVEs |
| 60-79 | Good — minor concerns |
| 40-59 | Aging — consider updates |
| 0-39 | Stale — maintenance risk |

### Age Classification

| Class | Age | Action |
|-------|-----|--------|
| fresh | <6 months | No action needed |
| current | 6-12 months | Monitor |
| aging | 1-2 years | Plan upgrade |
| stale | >2 years | Upgrade or replace |

### Version Types

| Type | Production Safe? |
|------|-----------------|
| stable | ✅ Yes |
| rc | ⚠️ Test thoroughly |
| beta | ⚠️ Non-critical only |
| alpha | ❌ Development only |
| milestone | ⚠️ Early adopters |
| snapshot | ❌ Never in production |

## Examples

### Example 1: Quick version check

**User:** "What's the latest stable Spring Boot?"

```
→ get_latest_version
  groupId: org.springframework.boot
  artifactId: spring-boot-starter
  stabilityFilter: STABLE_ONLY
```

### Example 2: Upgrade analysis

**User:** "I'm on Spring Boot 2.7.18, should I upgrade?"

```
→ compare_dependency_versions
  dependencies: ["org.springframework.boot:spring-boot-starter:2.7.18"]
  includeSecurityScan: true

→ If major upgrade available, delegate to context7 skill:
  scripts/context7.py search "spring boot"
  scripts/context7.py docs "/spring-projects/spring-boot" "2.7 to 3 migration"
```

### Example 3: Full project audit

**User:** "Analyze my pom.xml" (pastes file)

```
→ Extract all dependencies from pom.xml
→ analyze_project_health
  dependencies: [extracted list]
  includeSecurityScan: true
  includeLicenseScan: true
```

## Recovery

| Issue | Action |
|-------|--------|
| MCP tools unavailable | Inform user: "Maven Tools MCP server not configured. Install from <https://github.com/arvindand/maven-tools-mcp> — use `latest-noc7` image since we have context7 skill for docs." |
| Dependency not found | Verify groupId:artifactId format, check Maven Central |
| Context7 skill unavailable | Fall back to web search for documentation |
| Security scan slow | Results still return, CVE data may be partial |
| Unknown version type | Treat as unstable, recommend stable alternative |

---

> **License:** MIT
> **Requires:** [Maven Tools MCP server](https://github.com/arvindand/maven-tools-mcp) (`latest-noc7` recommended)
> **Pairs with:** [context7 skill](../context7/) for documentation lookup
