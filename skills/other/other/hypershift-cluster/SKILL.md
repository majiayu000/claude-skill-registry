---
name: hypershift:cluster
description: Create and destroy HyperShift clusters on AWS for testing Kagenti platform. Manages ephemeral OpenShift clusters.
---

# HyperShift Cluster Management Skill

Create, destroy, and manage HyperShift clusters on AWS for testing.

## When to Use

- Need to create a test OpenShift cluster on AWS
- Destroying a cluster after testing
- User asks "create hypershift cluster" or "destroy cluster"
- Testing Kagenti on real OpenShift (not Kind)

## Prerequisites

Before creating clusters, ensure setup is complete:

```bash
# 1. Run preflight check
./.github/scripts/hypershift/preflight-check.sh

# 2. Setup credentials (first time only, requires IAM admin)
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh

# 3. Setup local tools (hcp CLI, ansible, etc.)
./.github/scripts/hypershift/local-setup.sh
```

## Create Cluster

### Quick Create (Default Suffix)

```bash
# Creates: kagenti-hypershift-custom-<username>
./.github/scripts/hypershift/create-cluster.sh
```

### Create with Custom Suffix

```bash
# Creates: kagenti-hypershift-custom-pr529
./.github/scripts/hypershift/create-cluster.sh pr529

# Creates: kagenti-hypershift-custom-mytest
./.github/scripts/hypershift/create-cluster.sh mytest
```

### Create with Custom Configuration

```bash
# More worker nodes and larger instances
REPLICAS=3 INSTANCE_TYPE=m5.2xlarge ./.github/scripts/hypershift/create-cluster.sh

# Specific OCP version
OCP_VERSION=4.19.5 ./.github/scripts/hypershift/create-cluster.sh
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REPLICAS` | 2 | Number of worker nodes |
| `INSTANCE_TYPE` | m5.xlarge | AWS instance type |
| `OCP_VERSION` | 4.20.11 | OpenShift version |
| `CLUSTER_SUFFIX` | username | Suffix for cluster name |
| `MANAGED_BY_TAG` | kagenti-hypershift-custom | IAM scope prefix |

## Destroy Cluster

### Quick Destroy

```bash
# Destroy by suffix
./.github/scripts/hypershift/destroy-cluster.sh <suffix>

# Examples:
./.github/scripts/hypershift/destroy-cluster.sh pr529
./.github/scripts/hypershift/destroy-cluster.sh ladas
```

### Destroy by Full Name

```bash
./.github/scripts/hypershift/destroy-cluster.sh kagenti-hypershift-custom-pr529
```

## After Cluster Creation

The create script outputs next steps. Typical workflow:

```bash
# 1. Set kubeconfig to new cluster
export KUBECONFIG=~/clusters/hcp/<cluster-name>/auth/kubeconfig

# 2. Verify cluster access
oc get nodes
oc get clusterversion

# 3. Deploy Kagenti platform
./.github/scripts/kagenti-operator/30-run-installer.sh --env ocp
./.github/scripts/kagenti-operator/41-wait-crds.sh
./.github/scripts/kagenti-operator/42-apply-pipeline-template.sh

# 4. Deploy demo agents
./.github/scripts/kagenti-operator/71-build-weather-tool.sh
./.github/scripts/kagenti-operator/72-deploy-weather-tool.sh
./.github/scripts/kagenti-operator/73-patch-weather-tool.sh
./.github/scripts/kagenti-operator/74-deploy-weather-agent.sh

# 5. Run E2E tests
export AGENT_URL="https://$(oc get route -n team1 weather-service -o jsonpath='{.spec.host}')"
export KAGENTI_CONFIG_FILE=deployments/envs/ocp_values.yaml
./.github/scripts/kagenti-operator/90-run-e2e-tests.sh
```

## Full Test Workflow

Use the full test script for complete workflow:

```bash
# Full test: create cluster -> deploy -> test -> keep cluster
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy

# With custom suffix
./.github/scripts/local-setup/hypershift-full-test.sh pr123 --skip-cluster-destroy

# Include cleanup after test
./.github/scripts/local-setup/hypershift-full-test.sh --include-cluster-destroy
```

## Cluster Naming

Clusters are named: `${MANAGED_BY_TAG}-${CLUSTER_SUFFIX}`

| MANAGED_BY_TAG | Use Case | Example |
|----------------|----------|---------|
| `kagenti-hypershift-custom` | Local development (default) | kagenti-hypershift-custom-ladas |
| `kagenti-hypershift-ci` | CI/CD pipelines | kagenti-hypershift-ci-pr529 |

## Troubleshooting

### Cluster Creation Stuck

```bash
# Check HostedCluster status (use management cluster kubeconfig)
source .env.kagenti-hypershift-custom  # or .env.hypershift-ci
oc get hostedcluster -n clusters

# Check conditions
oc get hostedcluster -n clusters <cluster-name> -o jsonpath='{range .status.conditions[*]}{.type}{": "}{.status}{" - "}{.message}{"\n"}{end}'

# Check NodePool
oc get nodepool -n clusters <cluster-name>
```

### Cluster Deletion Stuck

```bash
# Debug AWS resources
./.github/scripts/hypershift/debug-aws-hypershift.sh <cluster-name>

# Force remove finalizer (only if AWS resources are cleaned)
oc patch hostedcluster -n clusters <cluster-name> -p '{"metadata":{"finalizers":null}}' --type=merge
```

### Control Plane Namespace Issues

```bash
# If namespace is stuck terminating
oc delete ns clusters-<cluster-name> --wait=false
oc patch ns clusters-<cluster-name> -p '{"metadata":{"finalizers":null}}' --type=merge
```

### Check AWS Quotas

```bash
# Before creating clusters, check capacity
./.github/scripts/hypershift/check-quotas.sh
```

## Related Skills

- **hypershift:setup**: Setup local environment for HyperShift
- **hypershift:preflight**: Run pre-flight checks
- **hypershift:quotas**: Check AWS quotas
- **hypershift:debug**: Debug AWS resources for stuck clusters

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
- `docs/hypershift-hcp-research.md` - HyperShift research and architecture
