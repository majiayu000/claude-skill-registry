---
name: identity-review
description: Review identity and access management across all platforms
user-invocable: true
---

You are helping the team review identity and access management (IAM) across Jocko Fuel platforms.

Follow these steps:

### Step 1: Define Review Scope

Ask the user which platforms to review:
- **GCP**: IAM roles, service accounts, API keys
- **Shopify**: Staff accounts, API access, app permissions
- **Snowflake**: Roles, grants, warehouse access
- **SaaS platforms**: User accounts across third-party tools
- **All**: Comprehensive IAM review

### Step 2: Audit Accounts and Permissions

Delegate to the `identity-access-reviewer` agent to:
- List all user and service accounts per platform
- Map role assignments and permission grants
- Check MFA status for all human accounts
- Identify service accounts and their privilege scope
- Review API key and token ages and rotation schedules

### Step 3: Identify Issues

Flag these common IAM problems:
- **Over-privileged accounts**: Users or services with more access than needed
- **Stale accounts**: Inactive accounts from former employees or unused services
- **Missing MFA**: Human accounts without multi-factor authentication
- **Shared credentials**: Accounts used by multiple people
- **Excessive admin roles**: Too many accounts with admin-level access
- **No rotation**: API keys or tokens that haven't been rotated

### Step 4: Recommend Changes

For each issue, provide:
- **Finding**: What's wrong
- **Risk**: What could happen
- **Fix**: Specific remediation action
- **Priority**: Critical / High / Medium / Low

Present as a prioritized action list.

### Error Handling

- If platform access is insufficient for a complete audit, note what's missing
- If the organization lacks an identity inventory, recommend creating one
- If accounts span personal and business use, flag for policy clarification
