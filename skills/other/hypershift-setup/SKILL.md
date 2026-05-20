---
name: hypershift:setup
description: Setup local environment for HyperShift testing. Installs hcp CLI, ansible collections, and configures credentials.
---

# HyperShift Local Setup Skill

Setup the local development environment for HyperShift cluster provisioning.

## When to Use

- First time setting up HyperShift testing
- After reinstalling tools or machine
- Missing hcp CLI or ansible collections
- User asks "setup hypershift" or "configure hypershift"

## Prerequisites

Before running setup:

1. **AWS CLI**: Configured with admin credentials
2. **OpenShift CLI (oc)**: Installed and logged into management cluster
3. **Ansible**: `pip install ansible-core`
4. **Credentials file**: Created by setup-hypershift-ci-credentials.sh

## Quick Setup Workflow

```bash
# 1. Run preflight check first
./.github/scripts/hypershift/preflight-check.sh

# 2. Setup credentials (requires IAM admin - first time only)
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh

# 3. Setup local tools
./.github/scripts/hypershift/local-setup.sh
```

## What local-setup.sh Does

1. **Loads credentials** from `.env.kagenti-hypershift-custom` or `.env.hypershift-ci`
2. **Installs hcp CLI** from OpenShift console to `~/.local/bin`
3. **Clones hypershift-automation** repository (Ladas fork with additional-tags support)
4. **Installs ansible collections**: kubernetes.core, amazon.aws, community.general
5. **Installs Python dependencies**: boto3, botocore, kubernetes, openshift
6. **Saves pull secret** to `~/.pullsecret.json`
7. **Verifies kubeconfig** for management cluster

## Running local-setup.sh

```bash
# Run the setup script
./.github/scripts/hypershift/local-setup.sh
```

Expected output:
```
✓ Loaded credentials from .env.kagenti-hypershift-custom
✓ hcp CLI installed to ~/.local/bin
✓ Cloned to .../hypershift-automation
✓ Ansible collections installed
✓ Python dependencies installed
✓ Pull secret saved to ~/.pullsecret.json
✓ Management kubeconfig verified
```

## After Setup

```bash
# Create your first cluster
./.github/scripts/hypershift/create-cluster.sh

# Or run full test workflow
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy
```

## Manual Steps

### Install hcp CLI Manually

If automatic download fails:

```bash
# 1. Get the console downloads URL
oc get consoleclidownloads hcp-cli-download -o jsonpath='{.spec.links}'

# 2. Download from OpenShift console
# Go to: ? → Command Line Tools → Download hcp CLI

# 3. Extract to ~/.local/bin
tar -xzf hcp-*.tar.gz && mv hcp ~/.local/bin/
chmod +x ~/.local/bin/hcp

# 4. Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.local/bin:$PATH"
```

### Install Ansible Collections Manually

```bash
ansible-galaxy collection install kubernetes.core amazon.aws community.general --force-with-deps
pip install boto3 botocore kubernetes openshift PyYAML
```

### Clone hypershift-automation Manually

```bash
cd ..
git clone -b add-additional-tags-support https://github.com/Ladas/hypershift-automation.git
```

## Credentials File Structure

The setup creates `.env.kagenti-hypershift-custom` (or `.env.hypershift-ci`):

```bash
# AWS credentials (scoped to MANAGED_BY_TAG)
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"

# Cluster configuration
export MANAGED_BY_TAG="kagenti-hypershift-custom"
export BASE_DOMAIN="octo-emerging.redhataicoe.com"
export HCP_ROLE_NAME="kagenti-hypershift-custom-hcp-role"

# Management cluster access
export KUBECONFIG="$HOME/.kube/kagenti-hypershift-ci-mgmt.kubeconfig"

# Pull secret (for accessing Red Hat registries)
export PULL_SECRET='{"auths":{...}}'
```

## Verify Setup

```bash
# Check hcp CLI
hcp version

# Check ansible
ansible-playbook --version
ansible-galaxy collection list | grep -E "kubernetes|amazon|community"

# Check AWS credentials
aws sts get-caller-identity

# Check management cluster access
source .env.kagenti-hypershift-custom
oc get hostedclusters -n clusters
```

## Troubleshooting

### hcp CLI Not Found

```bash
# Add ~/.local/bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Check if installed
ls -la ~/.local/bin/hcp
```

### Ansible Collection Errors

```bash
# Reinstall collections
ansible-galaxy collection install kubernetes.core amazon.aws community.general --force
```

### hypershift-automation Not Found

```bash
# Check sibling directory
ls -la ../hypershift-automation

# Re-run setup
./.github/scripts/hypershift/local-setup.sh
```

### AWS Credentials Invalid

```bash
# Verify credentials work
source .env.kagenti-hypershift-custom
aws sts get-caller-identity

# If using wrong credentials (e.g., CI instead of admin)
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
```

### Management Cluster Access Denied

```bash
# Re-login to management cluster
oc login <management-cluster-url>

# Re-run credentials setup
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh
```

## Related Skills

- **hypershift:preflight**: Run full pre-flight checks
- **hypershift:cluster**: Create and destroy clusters
- **hypershift:quotas**: Check AWS quotas

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
