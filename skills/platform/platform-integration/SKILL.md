---
name: platform-integration
description: Use when implementing CMMI processes in GitHub or Azure DevOps, migrating between platforms, or establishing traceability/compliance on GitHub/Azure - platform-specific process guidance
---

# Platform Integration

## Overview

This skill provides concrete implementation guidance for mapping CMMI process areas to GitHub and Azure DevOps platform features.

**Core principle**: CMMI defines WHAT processes are required. This skill shows HOW to implement them in your platform with production-ready configurations.

**Platforms covered**:
- **GitHub** - Issues, PRs, Actions, Projects for CMMI implementation
- **Azure DevOps** - Work Items, Repos, Pipelines, Boards for CMMI implementation

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` for CMMI process area definitions.

---

## When to Use

Use this skill when:
- Implementing requirements traceability in GitHub/Azure DevOps
- Setting up CI/CD pipelines with CMMI quality gates
- Configuring branch protection and code review policies
- Automating metrics collection for measurement
- Creating audit trails for compliance
- Migrating between platforms (GitHub ↔ Azure DevOps)
- Setting up risk tracking in work items
- Integrating CMMI processes with platform automation

**Do NOT use for**:
- CMMI process definitions → Use sdlc-prescription document
- Process-agnostic guidance → Use requirements-lifecycle, design-and-build, etc.
- Non-GitHub/Azure DevOps platforms → Adapt principles to your platform

---

## Quick Reference: CMMI → Platform Mapping

| CMMI Process Area | GitHub Feature | Azure DevOps Feature | Reference Sheet |
|-------------------|----------------|----------------------|-----------------|
| **REQM (Requirements Management)** | Issues, Projects, Labels | Work Items, Queries, Backlogs | github-requirements.md, azdo-requirements.md |
| **CM (Configuration Management)** | Branch Protection, CODEOWNERS | Branch Policies, Required Reviewers | github-config-mgmt.md, azdo-config-mgmt.md |
| **VER + VAL + PI (Quality)** | Actions, Status Checks, PRs | Pipelines, Gates, Test Plans | github-quality-gates.md, azdo-quality-gates.md |
| **MA (Measurement)** | Insights, API, Actions | Analytics, Dashboards, OData | github-measurement.md, azdo-measurement.md |
| **DAR + RSKM (Governance)** | Discussions, Wiki, Issues | Wiki, Custom Work Items | github-audit-trail.md, azdo-audit-trail.md |

---

## Platform Selection Criteria

### When to Use GitHub

**Best for**:
- Open source projects (public repositories)
- Developer-centric workflows (PRs, code review focus)
- Lightweight process (startups, small teams)
- Git-native workflows (GitFlow, GitHub Flow, trunk-based)
- Strong Actions ecosystem for automation
- Integration with third-party dev tools

**Strengths**:
- ✅ Excellent developer experience
- ✅ Free for public repositories
- ✅ Strong community and marketplace
- ✅ Simple, intuitive UI
- ✅ Best-in-class code review
- ✅ Actions for flexible automation

**Limitations**:
- ❌ Limited work item hierarchy (no built-in epic → feature → story)
- ❌ Basic project management features
- ❌ Limited reporting/analytics (compared to Azure DevOps)
- ❌ No built-in test management
- ❌ Weaker audit logging (for compliance)

**CMMI Maturity**:
- **Level 2**: Fully capable
- **Level 3**: Fully capable with third-party tools
- **Level 4**: Limited (external analytics tools needed)

### When to Use Azure DevOps

**Best for**:
- Enterprise projects (regulated industries)
- Complex work item hierarchies (epic → feature → story)
- Integrated ALM (requirements → design → test → deploy)
- Advanced reporting and analytics
- Compliance and audit requirements
- Microsoft stack integration (.NET, Azure)

**Strengths**:
- ✅ Rich work item management
- ✅ Built-in test management
- ✅ Advanced analytics and reporting
- ✅ Audit logging for compliance
- ✅ Integrated CI/CD with environments
- ✅ Customizable processes

**Limitations**:
- ❌ Steeper learning curve
- ❌ More complex to configure
- ❌ Less developer-friendly UX
- ❌ Weaker community/marketplace
- ❌ Limited free tier

**CMMI Maturity**:
- **Level 2**: Fully capable
- **Level 3**: Fully capable (native features)
- **Level 4**: Fully capable (native analytics, baselines)

### Hybrid Scenarios

**Common patterns**:
- **GitHub + Azure DevOps Boards**: Code in GitHub, work tracking in Azure DevOps
- **Azure DevOps + GitHub Actions**: Work items in Azure DevOps, CI/CD in GitHub
- **Multi-Platform**: Microservices split across platforms

**Integration options**:
- Azure Boards + GitHub integration (official)
- Zapier/Make for workflow automation
- API-based synchronization
- Third-party tools (Unito, Workato)

---

## Reference Sheets

The following reference sheets provide detailed, production-ready implementation guidance for each platform.

### GitHub Integration (5 Sheets)

#### 1. Requirements Management in GitHub

**When to use**: Implementing REQM (Requirements Management) in GitHub

→ See [github-requirements.md](./github-requirements.md)

**Covers**:
- Issue templates for requirements with traceability IDs
- Label strategy for requirement types and states
- Projects/Milestones for requirement organization
- PR linking patterns (`Implements #123`, `Closes #456`)
- Traceability matrix automation
- Requirement change management workflow
- Level 2/3/4 scaling requirements
- Audit trail for requirements changes

#### 2. Configuration Management in GitHub

**When to use**: Implementing CM (Configuration Management) in GitHub

→ See [github-config-mgmt.md](./github-config-mgmt.md)

**Covers**:
- Branch protection rules (required reviewers, status checks)
- CODEOWNERS file format and enforcement
- Git workflow comparison (GitFlow, GitHub Flow, trunk-based)
- Merge strategies (squash, merge, rebase) trade-offs
- Baseline management (tags, releases)
- Release management automation
- Emergency hotfix procedures
- Configuration as code (settings.yml, Terraform)

#### 3. Quality Gates in GitHub

**When to use**: Implementing VER, VAL, PI (Verification, Validation, Integration) in GitHub

→ See [github-quality-gates.md](./github-quality-gates.md)

**Covers**:
- GitHub Actions workflows for CI/CD
- Multi-stage pipelines (build → test → deploy)
- Required status checks configuration
- Test execution and coverage enforcement
- Deployment environments and protection rules
- Approval workflows for production
- Quality metrics collection
- Integration testing strategies

#### 4. Measurement in GitHub

**When to use**: Implementing MA (Measurement & Analysis) in GitHub

→ See [github-measurement.md](./github-measurement.md)

**Covers**:
- GitHub Insights and API for metrics
- DORA metrics implementation (all 4 metrics)
- Metrics collection automation (Actions)
- Dashboard creation (external tools integration)
- Historical baseline tracking
- Statistical process control (Level 4)
- Alerting on metric thresholds
- Custom metrics for project needs

#### 5. Audit Trail in GitHub

**When to use**: Compliance and audit requirements in GitHub

→ See [github-audit-trail.md](./github-audit-trail.md)

**Covers**:
- Commit history as audit log
- PR review history retention
- Issue comment trails
- Action logs and artifact retention
- Compliance mappings (SOC 2, ISO, GDPR)
- Audit report generation
- Data retention policies
- Access control for sensitive data

### Azure DevOps Integration (5 Sheets)

#### 6. Requirements Management in Azure DevOps

**When to use**: Implementing REQM (Requirements Management) in Azure DevOps

→ See [azdo-requirements.md](./azdo-requirements.md)

**Covers**:
- Work item types (Epic, Feature, User Story, Requirement)
- Custom fields for traceability
- Backlogs and boards configuration
- Queries for requirement reporting
- Multi-level hierarchy management
- Change request workflow
- Requirement baseline management
- Integration with test plans

#### 7. Configuration Management in Azure DevOps

**When to use**: Implementing CM (Configuration Management) in Azure DevOps

→ See [azdo-config-mgmt.md](./azdo-config-mgmt.md)

**Covers**:
- Azure Repos branch policies
- Required reviewers and CODEOWNERS
- Linked work items enforcement
- Merge strategies and build validation
- Release management with environments
- Baseline tagging automation
- TFVC migration (if needed)
- Configuration as code (YAML pipelines)

#### 8. Quality Gates in Azure DevOps

**When to use**: Implementing VER, VAL, PI (Verification, Validation, Integration) in Azure DevOps

→ See [azdo-quality-gates.md](./azdo-quality-gates.md)

**Covers**:
- Azure Pipelines multi-stage YAML
- Quality gates between stages
- Test Plans integration
- Approval workflows and gates
- Deployment environments
- Release management strategies
- Test execution and reporting
- Quality metrics tracking

#### 9. Measurement in Azure DevOps

**When to use**: Implementing MA (Measurement & Analysis) in Azure DevOps

→ See [azdo-measurement.md](./azdo-measurement.md)

**Covers**:
- Analytics views and widgets
- Dashboard creation and customization
- OData queries for custom reports
- PowerBI integration
- DORA metrics implementation
- Process baselines (Level 3/4)
- Historical data analysis
- Statistical process control

#### 10. Audit Trail in Azure DevOps

**When to use**: Compliance and audit requirements in Azure DevOps

→ See [azdo-audit-trail.md](./azdo-audit-trail.md)

**Covers**:
- Work item history and revisions
- Audit logs (admin actions, permission changes)
- Pipeline run history retention
- Compliance features (data residency, encryption)
- Audit report generation
- Retention policies configuration
- Access control and permissions
- Regulatory compliance (FDA, ISO, SOC 2)

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| **Treating platform as CMMI-aware** | Platforms don't enforce CMMI; you configure enforcement | Map each CMMI practice to platform feature explicitly |
| **Using platform defaults** | Defaults are permissive (no quality gates, no reviews) | Configure branch protection, required checks, policies |
| **Manual traceability** | Spreadsheet traceability becomes stale immediately | Automate with issue/PR links, work item queries, API |
| **Skipping audit trail setup** | Compliance failures discovered during audit | Configure retention, access logs, history from project start |
| **One-size-fits-all configuration** | Level 2 project gets Level 4 overhead (or vice versa) | Scale configuration based on CMMI target level |
| **Forgetting baselines** | No way to freeze requirements or code for releases | Implement baseline tagging, release branches, milestone freezes |
| **Ignoring platform limitations** | GitHub weak at test management; Azure DevOps weak at code review | Use hybrid approach or third-party tools for gaps |
| **No verification automation** | Traceability breaks without detection | Scheduled checks for orphaned requirements, missing links |
| **Generic metrics** | Collecting data nobody uses | GQM approach: Goal → Question → Metric (actionable only) |
| **Missing cross-process links** | Requirements don't link to risks; tests don't link to design | Document integration patterns in configuration |

---

## Integration with Other Skills

| When You're Doing | Also Use | For |
|-------------------|----------|-----|
| Platform setup for requirements | `requirements-lifecycle` | REQM/RD process definitions |
| Platform setup for CI/CD | `design-and-build` | TS/PI process definitions |
| Platform setup for testing | `quality-assurance` | VER/VAL process definitions |
| Platform setup for metrics | `quantitative-management` | MA/QPM metrics definitions |
| Platform selection decision | `governance-and-risk` | Decision analysis for platform choice |
| Initial platform adoption | `lifecycle-adoption` | Incremental rollout strategy |

---

## Next Steps

1. **Determine your platform**: GitHub, Azure DevOps, or hybrid
2. **Identify CMMI process area**: Which process (REQM, CM, VER, etc.) are you implementing?
3. **Check target maturity level**: Level 2, 3, or 4 (from CLAUDE.md or user)
4. **Load reference sheet**: Read platform-specific implementation guide
5. **Apply configuration**: Use production-ready examples from reference sheet
6. **Verify setup**: Run verification checks for traceability, quality gates, audit trail
7. **Integrate processes**: Link requirements → code → tests → metrics

**Remember**: Platforms don't enforce CMMI compliance automatically. You must configure them to implement CMMI practices. This skill provides the configuration patterns to bridge CMMI policy to platform reality.
