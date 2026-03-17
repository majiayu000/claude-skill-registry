---
name: m365-admin
description: Use when user needs Microsoft 365 administration, automation, and management for Exchange Online, Teams, SharePoint, licensing, and Graph API operations. Handles secure identity and workload automation.
---

# Microsoft 365 Administrator

## Purpose

Provides Microsoft 365 administration and automation expertise specializing in Exchange Online, Teams, SharePoint, and Graph API operations. Manages secure identity, workload automation, licensing optimization, and compliance configuration across the Microsoft 365 ecosystem.

## When to Use

- Exchange Online mailbox management and lifecycle
- Microsoft Teams team lifecycle automation
- SharePoint site management and security
- License assignment and optimization
- Microsoft Graph PowerShell automation
- User provisioning and onboarding workflows
- Compliance and security configuration

This skill provides expert Microsoft 365 administration and automation capabilities. It designs, builds, and reviews scripts and workflows across Exchange Online, Teams, SharePoint, and other Microsoft cloud workloads with focus on automation, licensing optimization, and Graph API operations.

## When to Use

User needs:
- Exchange Online mailbox management and lifecycle
- Microsoft Teams team lifecycle automation
- SharePoint site management and security
- License assignment and optimization
- Microsoft Graph PowerShell automation
- User provisioning and onboarding workflows
- Compliance and security configuration
- Guest access and external sharing management

## What This Skill Does

This skill automates and manages Microsoft 365 workloads through PowerShell and Graph API. It handles mailbox operations, team lifecycle management, SharePoint administration, license auditing and optimization, and ensures secure identity and compliance across the Microsoft 365 platform.

### M365 Workloads Covered

- Exchange Online (mailboxes, distribution groups, transport rules)
- Microsoft Teams (team creation, membership, channel management)
- SharePoint Online (sites, permissions, sharing settings)
- Microsoft Graph API (identity, users, groups, app registrations)
- Licensing and subscription management
- Security and compliance configuration

## Core Capabilities

### Exchange Online Management
- Mailbox provisioning and lifecycle management
- Distribution groups and mail-enabled security groups
- Transport rules and compliance policies
- Message trace and audit workflows
- Calendar and resource management
- Email flow configuration and routing

### Teams + SharePoint Administration
- Team lifecycle automation (create, archive, delete)
- SharePoint site provisioning and permissions
- Guest access and external sharing validation
- Collaboration security workflows
- Channel and tab management
- Document library and folder structure

### Licensing + Graph API
- License assignment, auditing, and optimization
- Microsoft Graph PowerShell for identity automation
- Service principal and app registration management
- Role-based access control (RBAC) configuration
- User and group synchronization
- Conditional access policies

### Automation Patterns
- User onboarding and offboarding workflows
- Bulk operations across departments
- Scheduled maintenance and cleanup tasks
- Compliance and security audit automation
- Reporting and analytics generation
- Self-healing and remediation scripts

## Tool Restrictions

- Read: Access M365 configuration files, scripts, and documentation
- Write/Edit: Create PowerShell scripts and automation workflows
- Bash: Execute PowerShell commands and M365 CLI tools
- Glob/Grep: Search M365-related code and configuration files

## Integration with Other Skills

- azure-infra-engineer: Identity/hybrid alignment and Azure AD integration
- powershell-7-expert: PowerShell scripting and Graph API automation
- powershell-module-architect: Module structure for cloud tooling
- it-ops-orchestrator: M365 workflows involving infrastructure and automation
- security-auditor: Security compliance and access reviews

## Example Interactions

### Scenario 1: User Onboarding Automation

**User:** "Automate new employee onboarding with mailbox, Teams, and license assignment"

**Interaction:**
1. Skill designs onboarding workflow with required information
2. Creates PowerShell script using Microsoft Graph:
   - Creates user account in Azure AD
   - Assigns appropriate M365 licenses
   - Provisions Exchange Online mailbox
   - Creates user's departmental Team with default channels
   - Adds user to relevant distribution groups and SharePoint sites
   - Sends welcome email with resources
3. Implements error handling and logging
4. Tests workflow with test accounts

### Scenario 2: SharePoint External Sharing Audit

**User:** "Audit all SharePoint sites for external sharing and fix misconfigured sites"

**Interaction:**
1. Skill audits all SharePoint site sharing settings via Graph API
2. Identifies misconfigured sites with external sharing enabled
3. Generates report showing:
   - Site owners and administrators
   - Current sharing settings and external users
   - Business justification for external access
4. Implements remediation script to:
   - Disable external sharing on non-compliant sites
   - Set appropriate sharing policies
   - Add compliance notifications
5. Provides ongoing monitoring solution

### Scenario 3: License Optimization

**User:** "Audit and optimize M365 licenses across the organization"

**Interaction:**
1. Skill queries all assigned licenses via Microsoft Graph
2. Analyzes usage data and last activity timestamps
3. Identifies:
   - Unused licenses for reclamation
   - Over-licensed users for downgrade
   - Underutilized premium features
4. Generates optimization plan:
   - Reclaims X unused licenses saving $Y/month
   - Recommends license package changes
   - Suggests automation for license assignment
5. Implements automated license provisioning workflow

## Best Practices

- Validation: Always validate connections and permissions before modifications
- Least Privilege: Apply RBAC principles for all automation accounts
- Testing: Test scripts in non-production environments first
- Backup: Audit and backup affected objects before bulk changes
- Documentation: Document all automation scripts with comments and examples
- Error Handling: Implement robust error handling and logging
- Monitoring: Add monitoring and alerting for critical workflows
- Approval: Include approval workflows for high-impact changes

## Examples

### Example 1: Enterprise User Onboarding Automation

**Scenario:** A company with 500+ employees needs automated onboarding across M365 workloads.

**Implementation Approach:**
1. **Graph API Integration**: Created PowerShell scripts using Microsoft Graph API
2. **Workflow Design**: Sequential provisioning with dependency handling
3. **Error Handling**: Retry logic and notification system
4. **Testing**: Validated with test accounts before production

**Onboarding Workflow:**
1. Create Azure AD user account with proper attributes
2. Assign M365 licenses based on job role
3. Provision Exchange Online mailbox
4. Create Teams team with department channels
5. Add to SharePoint sites and distribution groups
6. Send welcome email with credentials

**Results:**
- Onboarding time: 4 hours → 15 minutes
- 100% consistency across all users
- Zero manual errors in 6 months

### Example 2: SharePoint Security Audit and Remediation

**Scenario:** Need to audit all SharePoint sites for external sharing compliance.

**Audit Process:**
1. **Data Collection**: Retrieved all site collections via Graph API
2. **Analysis**: Identified sharing settings and external users
3. **Risk Assessment**: Categorized sites by sensitivity level
4. **Remediation**: Applied policies based on risk level

**Findings:**
| Category | Sites | External Users | Risk Level |
|----------|-------|----------------|------------|
| High | 23 | 156 | Critical |
| Medium | 45 | 34 | Medium |
| Low | 120 | 8 | Low |

**Actions Taken:**
- Disabled external sharing on high-risk sites
- Implemented approval workflow for external access
- Added monitoring and alerting for policy violations

### Example 3: M365 License Optimization Project

**Scenario:** Optimize M365 license usage and reduce costs by identifying unused licenses.

**Optimization Approach:**
1. **License Audit**: Queried all assigned licenses via Graph API
2. **Usage Analysis**: Analyzed sign-in activity and service usage
3. **Optimization Plan**: Identified reclamation opportunities
4. **Implementation**: Automated license reassignment process

**Results:**
- 127 unused licenses reclaimed
- $45,000 annual savings
- 15% reduction in license costs
- Automated monitoring for license utilization

## Best Practices

### PowerShell Automation

- **Use Microsoft Graph API**: Modern approach for M365 management
- **Module Best Practices**: Use latest ExchangeOnlineManagement module
- **Error Handling**: Implement try/catch blocks for all operations
- **Logging**: Comprehensive logging for audit trails
- **Testing**: Always test scripts in non-production first

### Security and Compliance

- **Least Privilege**: Use application permissions, not user delegated
- **Conditional Access**: Implement for sensitive operations
- **Audit Logging**: Enable unified audit logging
- **Data Protection**: Encrypt sensitive data at rest and in transit
- **Compliance**: Follow organizational compliance requirements

### User Lifecycle Management

- **Onboarding**: Automated provisioning with approval workflows
- **Changes**: Handle role changes with proper access updates
- **Offboarding**: Complete deprovisioning with data retention
- **Licensing**: Regular audits and optimization
- **Self-Service**: Enable user self-service where appropriate

### Performance Optimization

- **Batch Operations**: Use batch API calls for bulk operations
- **Rate Limiting**: Handle throttling gracefully
- **Caching**: Cache frequently accessed data
- **Parallel Processing**: Use parallel execution for independent tasks
- **Monitoring**: Track script performance and duration

## Anti-Patterns

### PowerShell Automation Anti-Patterns

- **Sequential Everything**: Not leveraging parallel processing - use parallel execution for independent operations
- **No Error Handling**: Scripts that fail silently - implement comprehensive try/catch/finally
- **Hardcoded Values**: Embedding usernames, URLs in scripts - use parameters and configuration
- **Chatty API Calls**: Making excessive API calls - batch operations and use delta queries

### Security Anti-Patterns

- **Over-Privileged Accounts**: Using admin accounts for routine tasks - apply least privilege principles
- **Credential Hardcoding**: Storing passwords in scripts - use secure credential storage
- **Audit Neglect**: Not enabling unified audit logging - enable and monitor audit logs
- **Permission Creep**: Accumulating permissions without review - conduct regular access reviews

### User Management Anti-Patterns

- **Manual Provisioning**: Creating users manually instead of automation - automate user lifecycle
- **License Waste**: Assigning licenses without tracking usage - monitor and optimize license usage
- **Orphaned Accounts**: Leaving accounts after user departure - implement deprovisioning automation
- **Inconsistent Naming**: No naming convention enforcement - implement and enforce naming standards

### Configuration Anti-Patterns

- **Configuration Drift**: Environments diverging over time - use configuration management
- **Setting Shadow IT**: Users creating unauthorized configurations - monitor and govern settings
- **Over-Sharing**: Excessive external sharing permissions - audit and restrict sharing settings
- **Policy Overlap**: Multiple conflicting policies - consolidate and prioritize policies

## Automation Scripts and References

The M365 admin skill includes comprehensive automation scripts and reference documentation located in:

### Scripts (`scripts/` directory)
- **create_m365_users.ts**: TypeScript classes and functions for user lifecycle management, license assignment, password validation, and bulk operations
- **configure_teams.ts**: Microsoft Teams management including team creation, channel management, member management, team settings, and archiving
- **setup_exchange.ts**: Exchange Online administration with mailbox management, auto-reply configuration, distribution groups, calendar events, and email automation

### References (`references/` directory)
- **m365_quickstart.md**: Quick start guide with app registration, authentication, common patterns, and troubleshooting
- **admin_patterns.md**: Comprehensive patterns for user lifecycle, Teams templates, email automation, license management, security and compliance, and backup/recovery

## Output Format

This skill delivers:
- PowerShell automation scripts for M365 workloads
- Graph API integration code and examples
- Configuration templates and manifests
- Audit reports and compliance summaries
- Onboarding/offboarding workflow scripts
- License optimization recommendations and implementations

All outputs include:
- Detailed script documentation and comments
- Error handling and logging patterns
- Testing instructions and validation steps
- RBAC configuration guidance
- Troubleshooting procedures and common issues
- Security best practices and compliance considerations
