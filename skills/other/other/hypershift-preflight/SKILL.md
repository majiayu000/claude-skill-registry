---
name: hypershift:preflight
description: Run pre-flight checks for HyperShift CI. Verifies tools, AWS auth, OpenShift permissions, and configuration.
---

# HyperShift Pre-flight Check Skill

Verify all prerequisites for HyperShift cluster provisioning before running setup or creating clusters.

## When to Use

- Before first-time HyperShift setup
- Troubleshooting failed cluster creation
- Verifying environment after changes
- User asks "check hypershift prereqs" or "why won't cluster create"

## Quick Check

```bash
# Run all pre-flight checks
./.github/scripts/hypershift/preflight-check.sh
```

## What It Checks

### 1. Tools for Setup
- `jq` - JSON processor
- `aws` - AWS CLI
- `oc` - OpenShift CLI

### 2. Tools for Cluster Creation
- `hcp` - HyperShift CLI (optional, installed by local-setup.sh)
- `ansible-playbook` - Ansible automation
- `ansible-galaxy` - Ansible collection manager

### 3. AWS Authentication
- AWS credentials configured
- Identity accessible

### 4. AWS IAM Permissions
- Can create IAM policies
- Can create IAM roles
- Not using CI credentials (needs admin for setup)

### 5. OpenShift Authentication
- Logged into management cluster
- Server accessible

### 6. OpenShift Permissions
- Can create ClusterRoles
- Can create ClusterRoleBindings
- Can read secrets in openshift-config namespace

### 7. HyperShift Installation
- HyperShift CRD exists on management cluster

### 8. HyperShift Operator OIDC
- Operator has OIDC S3 configuration
- Required for AWS hosted clusters

### 9. Pull Secret
- Can access pull secret in openshift-config
- Pull secret is valid JSON
- Registry count verified

### 10. Base Domain
- Auto-detects from ingress config
- Falls back to existing hosted clusters

### 11. Route53 Hosted Zone
- Public hosted zone exists for base domain
- Required for DNS resolution

## Expected Output (Success)

```
╔════════════════════════════════════════════════════════════════╗
║           HyperShift CI Pre-flight Check                       ║
╚════════════════════════════════════════════════════════════════╝

→ Checking tools for setup...
✓ jq: jq-1.7.1
✓ aws: aws-cli/2.x.x
✓ oc: Client Version: 4.x.x

→ Checking tools for cluster creation...
✓ hcp: v4.x.x
✓ ansible-playbook: ansible-playbook 2.x.x
✓ ansible-galaxy: available

→ Checking AWS authentication...
✓ AWS authenticated: arn:aws:iam::xxx:user/xxx

→ Checking AWS IAM permissions for setup...
✓ AWS identity: arn:aws:iam::xxx:user/xxx
✓ AWS IAM: Can create policies
✓ AWS IAM: Can create roles

→ Checking OpenShift authentication...
✓ OpenShift authenticated: xxx @ https://xxx

→ Checking OpenShift permissions...
✓ Can create ClusterRoles
✓ Can create ClusterRoleBindings
✓ Can read secrets in openshift-config namespace

→ Checking HyperShift installation...
✓ HyperShift CRD found - HyperShift is installed

→ Checking HyperShift operator OIDC configuration...
✓ HyperShift operator has OIDC S3 configured

→ Checking pull secret accessibility...
✓ Pull secret valid (5 registries configured)

→ Checking base domain discovery...
✓ Base domain: octo-emerging.redhataicoe.com

→ Checking Route53 public hosted zone...
✓ Route53 public hosted zone found

╔════════════════════════════════════════════════════════════════╗
║  All checks passed! Ready to run setup script.                 ║
╚════════════════════════════════════════════════════════════════╝
```

## Common Errors and Fixes

### Missing Tools

```bash
# Install jq
brew install jq  # macOS
sudo apt install jq  # Ubuntu

# Install AWS CLI
# https://aws.amazon.com/cli/

# Install oc
# https://mirror.openshift.com/pub/openshift-v4/clients/ocp/

# Install ansible
pip install ansible-core
```

### AWS Not Authenticated

```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="us-east-1"
```

### Using CI Credentials Instead of Admin

```bash
# Error: Logged in as CI user. Setup requires IAM admin.

# Fix: Unset CI credentials
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

# Use your admin profile
aws configure list
```

### OpenShift Not Logged In

```bash
# Login to management cluster
oc login https://api.<management-cluster>:6443

# Verify
oc whoami
oc whoami --show-server
```

### HyperShift Not Installed

```
Error: HyperShift CRD not found.
```

This means the management cluster doesn't have HyperShift installed. Contact cluster admin or use a different management cluster.

### HyperShift Operator Missing OIDC

```
Error: HyperShift operator MISSING OIDC S3 configuration!
```

The operator was upgraded and lost OIDC config. Follow the fix instructions in the preflight output (requires cluster-admin).

### No Public Route53 Zone

```
Error: No PUBLIC Route53 hosted zone found for xxx
```

HyperShift requires a public hosted zone for DNS. Either:
1. Create a public hosted zone in Route53
2. Update BASE_DOMAIN in .env file to match an existing zone

## Manual Checks

### Check AWS Identity

```bash
aws sts get-caller-identity
```

### Check OpenShift Permissions

```bash
oc auth can-i create clusterroles
oc auth can-i create clusterrolebindings
oc auth can-i get secrets -n openshift-config
```

### Check HyperShift CRD

```bash
oc get crd hostedclusters.hypershift.openshift.io
```

### Check Operator OIDC Args

```bash
oc get deployment operator -n hypershift \
    -o jsonpath='{.spec.template.spec.containers[0].args}' | tr ',' '\n' | grep oidc
```

### Check Route53 Zones

```bash
aws route53 list-hosted-zones \
    --query "HostedZones[?Config.PrivateZone==\`false\`].Name" \
    --output table
```

## Next Steps After Preflight

If all checks pass:

```bash
# Setup credentials (first time only)
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh

# Setup local tools
./.github/scripts/hypershift/local-setup.sh

# Create cluster
./.github/scripts/hypershift/create-cluster.sh
```

## Related Skills

- **hypershift:setup**: Setup local environment
- **hypershift:cluster**: Create and destroy clusters
- **hypershift:quotas**: Check AWS quotas

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
