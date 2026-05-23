---
name: atmos-auth
description: >-
  Use when authenticating with AWS via Atmos. Covers ATMOS_PROFILE setup, SSO login, and how Atmos automatically assumes
  the correct identity per stack. Use for authentication setup, SSO login issues, and permission errors.
---

# Atmos Auth

Atmos Auth handles AWS authentication automatically based on your profile and the target stack.

## Quick Start

```bash
# Set your profile (required for all atmos commands)
# Use your assigned profile: devops, developers, or managers
export ATMOS_PROFILE=<your-profile>

# Authenticate via SSO provider (preferred - triggers browser SSO)
atmos auth login --provider acme-sso

# Alternative: authenticate by specifying any identity (also triggers browser SSO)
atmos auth login --identity core-auto/terraform

# Run commands - Atmos auto-selects the correct identity per stack
atmos terraform plan vpc -s plat-use2-dev
```

## How It Works

1. **Set your profile**: `export ATMOS_PROFILE=<profile-name>` (or prefix each command)
2. **Authenticate when needed**: Atmos authenticates per-stack automatically. If credentials are expired, it will
   launch the IDP to sign in, or you can manually trigger SSO login.
3. **Run commands**: Atmos automatically assumes the correct identity for each stack based on the stack name.

When you run `atmos terraform plan <component> -s <stack>`, Atmos:

1. Renders all stack config, then determines the default identity for the stack
2. If there's a single default identity (e.g., `plat-dev/terraform`), it's selected automatically
3. Looks up that identity name in your profile to get the actual credentials
4. Assumes the configured Permission Set in the target account
5. Runs the Terraform command with those credentials

## Identity Configuration

Each stack defines its default identity in its `_defaults.yaml` file:

```yaml
# stacks/orgs/acme/plat/dev/_defaults.yaml
auth:
  identities:
    plat-dev/terraform:
      default: true
```

The identity name (`plat-dev/terraform`) is resolved by your profile to determine the actual AWS credentials to use.

## Profiles

Profiles are defined in `profiles/<profile-name>/atmos.yaml`. Each maps identities to Permission Sets:

| Profile      | Core Accounts        | Platform Dev/Sandbox | Platform Staging/Prod |
| ------------ | -------------------- | -------------------- | --------------------- |
| `devops`     | TerraformApplyAccess | TerraformApplyAccess | TerraformApplyAccess  |
| `developers` | TerraformStateAccess | TerraformApplyAccess | TerraformPlanAccess   |
| `managers`   | TerraformStateAccess | TerraformPlanAccess  | TerraformPlanAccess   |

**Permission Set capabilities:**

- `TerraformApplyAccess` - Full plan and apply
- `TerraformPlanAccess` - Plan only (no apply)
- `TerraformStateAccess` - Read state only (for cross-account references)

## Identity Naming Convention

Identities follow the pattern: `<tenant>-<stage>/terraform`

Examples:

- `plat-dev/terraform` - Platform dev account
- `core-auto/terraform` - Core automation account
- `plat-prod/terraform` - Platform production account

## Special Cases

**superadmin profile**: IAM user with MFA for breakglass access. Avoid unless SSO is unavailable.

**github-plan profile**: OIDC-based authentication for CI/CD plan operations. Uses planner roles with read-only access.

**github-apply profile**: OIDC-based authentication for CI/CD apply operations. Uses terraform roles with full access.
Only used from main branch after PR merge.

## Troubleshooting

If authentication fails:

1. Verify `ATMOS_PROFILE` is set: `echo $ATMOS_PROFILE`
2. Re-authenticate: `atmos auth login --provider acme-sso` (or `--identity core-auto/terraform`)
3. Check you have the required Permission Set in AWS IAM Identity Center
4. Verify the identity exists in `profiles/$ATMOS_PROFILE/atmos.yaml`

## Debugging Authentication Issues

For authentication-specific debugging:

```bash
# Enable debug logging to see auth flow
ATMOS_LOGS_LEVEL=debug atmos terraform plan <component> -s <stack>
```

Look for:

- Identity resolution (`<tenant>-<stage>/terraform`)
- SSO token retrieval
- Role assumption errors

For general Atmos debugging (configuration, variables, stack resolution), see the `debugging-atmos` skill.
