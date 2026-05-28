---
name: sop-maintenance
description: Use when updating, versioning, deprecating, or maintaining existing Standard Operating Procedures. Covers keeping SOPs accurate, relevant, and synchronized with implementation changes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# SOP Maintenance

SOPs require ongoing maintenance to remain accurate and useful. This skill covers strategies for keeping SOPs current, managing versions, and ensuring SOPs evolve with your systems.

## Key Concepts

### SOP Lifecycle

1. **Creation**: Initial SOP development
2. **Active Use**: SOP is being executed regularly
3. **Update**: Modifications to reflect changes
4. **Deprecation**: SOP is outdated but referenced
5. **Archive/Removal**: SOP is no longer needed

### Why SOPs Become Outdated

- **Technology Changes**: Tools, frameworks, or languages updated
- **Process Evolution**: Workflows improve or change
- **Environment Changes**: Infrastructure or deployment changes
- **Discovery**: Better approaches found through experience
- **External Dependencies**: Third-party services change APIs

## Best Practices

### Version Control for SOPs

Treat SOPs as code:

```bash
# Store SOPs in git repository
my-sops/
├── .git/
├── deployment/
│   ├── deploy-web-app.sop.md
│   └── rollback-deployment.sop.md
├── development/
│   ├── code-review.sop.md
│   └── feature-implementation.sop.md
└── README.md
```

**Commit Messages:**

```bash
git commit -m "feat(deployment): add health check step to deploy-web-app.sop"
git commit -m "fix(code-review): correct security checklist items"
git commit -m "docs(development): update feature-implementation with new test framework"
```

### SOP Versioning

Include version information in SOP metadata:

```markdown
# Deploy Application to Production

**Version**: 2.1.0
**Last Updated**: 2025-12-05
**Author**: DevOps Team
**Status**: Active

## Changelog

### v2.1.0 (2025-12-05)
- Added automated rollback triggers
- Updated health check thresholds

### v2.0.0 (2025-11-15)
- Migrated to Kubernetes from Docker Swarm
- Added canary deployment steps

### v1.0.0 (2025-09-01)
- Initial deployment SOP
```

### Keeping SOPs Current

**Regular Review Schedule:**

```markdown
## SOP Maintenance Schedule

- **Monthly**: Review frequently-used SOPs (deployment, incident response)
- **Quarterly**: Review all active SOPs for accuracy
- **After Major Changes**: Update SOPs when systems change
- **Post-Incident**: Update SOPs based on lessons learned
```

**Maintenance Checklist:**

```markdown
## SOP Review Checklist

- [ ] Prerequisites are still accurate
- [ ] Tools/versions are current
- [ ] Steps reflect actual process
- [ ] Parameters are still relevant
- [ ] Success criteria are measurable
- [ ] Error handling covers common issues
- [ ] Related SOPs are still valid
- [ ] Examples use current syntax
```

### Deprecating SOPs

When an SOP is outdated:

```markdown
# ⚠️ DEPRECATED: Deploy Using Docker Swarm

**Status**: DEPRECATED as of 2025-11-15
**Replaced By**: deploy-kubernetes.sop.md
**Reason**: Migrated infrastructure from Docker Swarm to Kubernetes

## Migration Guide

If you need to migrate from this SOP:
1. Review new Kubernetes deployment SOP
2. Understand key differences in deployment process
3. Update CI/CD pipelines to use new SOP
4. Archive Docker Swarm configurations

## Original SOP (for reference only)

[Keep original content for historical reference]
```

### Managing SOP Collections

**Directory Organization:**

```bash
sops/
├── active/              # Currently used SOPs
│   ├── deployment/
│   ├── development/
│   └── operations/
├── deprecated/          # Outdated but may be referenced
│   └── legacy-deployments/
└── templates/           # SOP templates for creating new SOPs
    ├── analysis.template.sop.md
    ├── implementation.template.sop.md
    └── deployment.template.sop.md
```

**Index File:**

```markdown
# SOP Index

## Active SOPs

### Deployment
- [deploy-web-app.sop.md](active/deployment/deploy-web-app.sop.md) - v2.1.0 - Deploy web application to production
- [rollback-deployment.sop.md](active/deployment/rollback-deployment.sop.md) - v1.5.0 - Rollback failed deployment

### Development
- [code-review.sop.md](active/development/code-review.sop.md) - v3.0.0 - Review code changes
- [tdd-implementation.sop.md](active/development/tdd-implementation.sop.md) - v2.2.0 - Implement features with TDD

## Deprecated SOPs

- [deploy-docker-swarm.sop.md](deprecated/deploy-docker-swarm.sop.md) - DEPRECATED - Use deploy-web-app.sop.md instead
```

## Examples

### Example 1: Updating SOP for Tool Change

**Before (using old test framework):**

```markdown
# Run Test Suite

## Steps

1. Run tests with Mocha

   ```bash
   npm run test
   ```

1. Check coverage with Istanbul

   ```bash
   npm run coverage
   ```

```

**After (updated for Vitest):**

```markdown
# Run Test Suite

**Version**: 2.0.0
**Last Updated**: 2025-12-05
**Changes**: Migrated from Mocha to Vitest

## Steps

1. Run tests with Vitest

   ```bash
   npm run test
   ```

1. Check coverage (built into Vitest)

   ```bash
   npm run test:coverage
   ```

## Migration Notes

If migrating from v1.x (Mocha):

- Vitest uses same syntax for most assertions
- Coverage is built-in (no separate Istanbul step)
- Tests run significantly faster

```

### Example 2: Adding Environment Variable Support

**Updated SOP with env var support:**

```markdown
# Configure SOP Paths

## Overview

Configure custom SOP paths using environment variable or configuration file.
This allows teams to maintain organization-specific SOPs alongside built-in ones.

## Parameters

- **SOP Paths**: {sop_paths} - Colon-separated directory paths

## Methods

### Method 1: Environment Variable (Recommended)

Set `AGENT_SOP_PATHS` environment variable:

```bash
# In ~/.zshrc or ~/.bashrc
export AGENT_SOP_PATHS="~/my-team-sops:~/project-sops"

# Or inline for single use
AGENT_SOP_PATHS="~/my-sops" strands-agents-sops mcp
```

### Method 2: Command Line Argument

Pass paths directly to MCP server:

```bash
strands-agents-sops mcp --sop-paths ~/my-sops:~/team-sops
```

### Method 3: Configuration File

Add to Claude Code settings:

```json
{
  "mcpServers": {
    "agent-sops": {
      "command": "strands-agents-sops",
      "args": ["mcp"],
      "env": {
        "AGENT_SOP_PATHS": "~/my-sops:~/team-sops"
      }
    }
  }
}
```

## Precedence

1. Command line `--sop-paths` (highest priority)
2. `AGENT_SOP_PATHS` environment variable
3. Default paths (built-in SOPs only)

Custom SOPs override built-in SOPs with matching names.

```

### Example 3: Post-Incident SOP Update

**Adding error handling based on production incident:**

```markdown
# Deploy Application to Production

**Version**: 2.2.0
**Last Updated**: 2025-12-05
**Changes**: Added database connection pool check after incident #1234

## Changelog

### v2.2.0 (2025-12-05)
- Added database connection pool verification step
- Updated error handling for connection failures
- Added monitoring alert validation

*Reason: Production incident #1234 caused by connection pool exhaustion*

## Steps

1. Pre-deployment verification
   - Verify staging deployment healthy
   - Check database migrations ready
   - **NEW**: Verify database connection pool configuration
     ```bash
     # Check pool settings
     kubectl get configmap db-config -o yaml | grep -A5 pool

     # Validate pool size matches expected load
     # MUST be ≥ (expected_connections * 1.5)
     ```

2. Deploy application
   [... existing steps ...]

3. Post-deployment verification
   - Run smoke tests
   - Monitor error rates
   - **NEW**: Verify database connection pool metrics
     ```bash
     # Check active connections
     # MUST be < 80% of pool size
     curl https://monitoring.example.com/metrics/db-pool
     ```

## Error Handling

### NEW: Error: Database Connection Pool Exhausted

**Symptoms**: Application unable to acquire database connections, requests timing out

**Cause**: Pool size insufficient for load, connection leaks, or slow queries

**Resolution**:

1. Immediate: Scale up connection pool size

   ```bash
   kubectl patch configmap db-config --patch '{"data":{"pool_size":"100"}}'
   kubectl rollout restart deployment app
   ```

1. Monitor connection usage for 5 minutes
1. If issue persists, execute rollback
1. Post-incident: Review slow query logs and optimize

```

## Common Patterns

### Template for SOP Update

```markdown
# {SOP Title}

**Version**: {new_version}
**Last Updated**: {date}
**Changes**: {summary of changes}

## Changelog

### v{new_version} ({date})
- {change 1}
- {change 2}
- {change 3}

*Reason: {why these changes were made}*

### v{previous_version} ({date})
[Previous changes]

## [Rest of SOP content]
```

### Template for Deprecation Notice

```markdown
# ⚠️ DEPRECATED: {Old SOP Title}

**Status**: DEPRECATED as of {date}
**Replaced By**: {new-sop-file.sop.md}
**Reason**: {why deprecated}
**Support End Date**: {when will this be removed}

## Migration Guide

To migrate from this SOP to {new SOP}:

1. **Key Differences**:
   - {difference 1}
   - {difference 2}

2. **Migration Steps**:
   - {step 1}
   - {step 2}

3. **Breaking Changes**:
   - {breaking change 1}
   - {breaking change 2}

## References

- New SOP: [{new-sop-title}]({new-sop-file.sop.md})
- Migration Guide: [link]
- Announcement: [link to announcement]

---

## Original SOP (for historical reference)

[Keep original content below this line]
```

## Anti-Patterns

**Avoid These Maintenance Mistakes:**

1. **No Version Tracking**
   - ❌ Updating SOPs without tracking changes
   - ✅ Use version numbers and changelog

2. **Ignoring Deprecated SOPs**
   - ❌ Leaving outdated SOPs without deprecation notice
   - ✅ Clearly mark deprecated SOPs and provide alternatives

3. **Breaking Changes Without Notice**
   - ❌ Silently changing SOP behavior
   - ✅ Version bump and migration guide for breaking changes

4. **No Review Schedule**
   - ❌ Only updating SOPs when they break
   - ✅ Regular review schedule for all SOPs

5. **Poor Change Communication**
   - ❌ Updating SOPs without notifying users
   - ✅ Announce significant SOP changes to team

## Maintenance Workflow

### Regular Maintenance

```markdown
## Monthly SOP Maintenance

1. Review high-frequency SOPs
   - Check execution logs for failures
   - Review any reported issues
   - Update based on user feedback

2. Validate SOP accuracy
   - Run through critical SOPs manually
   - Verify tools/versions are current
   - Test examples still work

3. Update documentation
   - Fix any inaccuracies found
   - Add clarifications where needed
   - Update related SOPs

4. Commit and communicate changes
   - Commit updates with descriptive messages
   - Announce changes in team channel
   - Update SOP index
```

### Post-Change Maintenance

```markdown
## After System Changes

When infrastructure, tools, or processes change:

1. Identify affected SOPs

   ```bash
   # Search for SOPs mentioning changed component
   grep -r "docker" sops/*.sop.md
   ```

1. Update each affected SOP
   - Update version number
   - Add changelog entry
   - Modify affected steps
   - Update examples

1. Test updated SOPs
   - Run through new workflow
   - Verify all steps work
   - Check success criteria still valid

1. Review dependencies
   - Check related SOPs need updates
   - Update SOP index
   - Notify team of changes

```

## Related Skills

- **sop-authoring**: Create new SOPs with quality
- **sop-structure**: Organize SOPs effectively
- **sop-rfc2119**: Use precise requirement keywords
