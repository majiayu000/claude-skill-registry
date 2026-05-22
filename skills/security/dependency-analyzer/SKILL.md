---
name: dependency-analyzer
description: Analyzes project dependencies, detects outdated packages, identifies breaking changes, and suggests safe update strategies. Helps maintain dependency health and security.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Analyze package.json/requirements.txt/go.mod
  - Check for security vulnerabilities
  - Identify breaking changes
  - Suggest update strategies
  - Validate compatibility
error_handling: graceful
streaming: supported
templates: [dependency-report, update-plan, security-audit]
---

# Dependency Analyzer Skill

<identity>
Dependency Analyzer Skill - Analyzes project dependencies, detects outdated packages, identifies breaking changes, and suggests safe update strategies.
</identity>

<capabilities>
- Analyzing dependency health
- Planning dependency updates
- Detecting security vulnerabilities
- Identifying breaking changes
- Validating compatibility
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Dependency Files

Locate dependency files:

- `package.json` (Node.js)
- `requirements.txt` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)
- `pom.xml` (Java/Maven)

### Step 2: Analyze Dependencies

Examine dependencies:

- Read dependency files
- Check versions
- Identify outdated packages
- Note version constraints

### Step 3: Semantic Versioning Analysis

Analyze version numbers using semantic versioning (semver):

1. **Parse version numbers**:
   - Extract major.minor.patch from version strings
   - Handle version ranges (^, ~, >=, etc.)
   - Identify exact vs range versions

2. **Detect major version bumps**:
   - Compare current version with latest available
   - Identify major version changes (e.g., 1.x.x -> 2.x.x)
   - Flag major updates as potentially breaking

3. **Check changelogs for breaking changes**:
   - **For major version updates**: Trigger web search (Exa/WebFetch) to research breaking changes
   - Look for "BREAKING CHANGE" markers in changelogs
   - Check migration guides
   - Review release notes for breaking changes
   - Document specific breaking changes found

4. **Semantic Versioning Rules**:
   - **Major version (X.0.0)**: Breaking changes likely, requires code changes
   - **Minor version (0.X.0)**: New features, backward compatible
   - **Patch version (0.0.X)**: Bug fixes, backward compatible

5. **Breaking Change Detection**:
   - Parse changelog entries for breaking change indicators
   - Identify deprecated APIs
   - Check for removed features
   - Document migration requirements
   - Generate breaking change report

### Step 4: Check for Updates

Check available updates:

- Query package registries
- Compare current vs latest versions
- Identify major/minor/patch updates
- Apply semantic versioning analysis
- Warn about breaking changes

### Step 5: Security Audit

Check for vulnerabilities:

- Scan for known vulnerabilities
- Check security advisories
- Identify high-risk packages
- Suggest security updates

### Step 6: Generate Report

Create dependency report:

- List outdated packages
- Identify breaking changes
- Suggest update strategy
- Provide migration guidance
  </execution_process>

<integration>
**Integration with DevOps Agent**:
- Manages dependency updates
- Implements update strategies
- Validates compatibility

**Integration with Security Architect Agent**:

- Reviews security vulnerabilities
- Validates security updates
- Ensures compliance
  </integration>

<best_practices>

1. **Regular Analysis**: Analyze dependencies regularly
2. **Security First**: Prioritize security updates
3. **Test Updates**: Always test after updates
4. **Gradual Updates**: Update incrementally
5. **Document Changes**: Track update decisions
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Dependency Health Report**

```markdown
# Dependency Health Report

## Summary

- Total Dependencies: 45
- Outdated: 12
- Vulnerable: 3
- Up to Date: 30

## Outdated Packages

- react: 18.0.0 -> 18.2.0 (minor update)
- next: 13.4.0 -> 14.0.0 (major update - breaking changes)
- typescript: 5.0.0 -> 5.3.0 (patch update)

## Security Vulnerabilities

- lodash: 4.17.20 (CVE-2021-23337) - Update to 4.17.21
- axios: 0.21.1 (CVE-2021-3749) - Update to 1.6.0

## Update Recommendations

1. Update patch versions (safe)
2. Review minor updates (low risk)
3. Plan major updates (breaking changes)
```

</formatting_example>

<formatting_example>
**Update Plan**

```markdown
# Dependency Update Plan

## Phase 1: Patch Updates (Safe)

- Update lodash: 4.17.20 -> 4.17.21
- Update typescript: 5.0.0 -> 5.3.0

## Phase 2: Minor Updates (Low Risk)

- Update react: 18.0.0 -> 18.2.0
- Update @types/node: 20.0.0 -> 20.10.0

## Phase 3: Major Updates (Breaking Changes)

- Update next: 13.4.0 -> 14.0.0
  - Breaking changes: [List]
  - Migration steps: [Steps]
  - Testing required: [Tests]
```

</formatting_example>
</examples>

<examples>
<usage_example>
**Example Commands**:

```
# Analyze dependencies
Analyze dependencies for this project

# Check for updates
Check for dependency updates

# Security audit
Perform security audit of dependencies

# Generate update plan
Generate update plan for major version updates
```

</usage_example>
</examples>

## Rules

- Always check for security vulnerabilities first
- Research breaking changes before major updates
- Test thoroughly after any dependency update

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
