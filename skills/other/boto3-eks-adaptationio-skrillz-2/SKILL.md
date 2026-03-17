---
name: boto3-eks
description: AWS Boto3 SDK patterns for Amazon EKS cluster management, node groups, authentication tokens, and Kubernetes client integration. Use when working with EKS clusters, managing node groups, generating kubeconfig, creating authentication tokens, integrating Kubernetes Python client, managing Fargate profiles, or implementing IRSA authentication.
---

# AWS Boto3 EKS Integration

Complete patterns for managing Amazon EKS clusters using AWS Boto3 SDK, including authentication token generation for Kubernetes client integration.

## Quick Reference

### Client Initialization

```python
import boto3
from typing import Optional

def get_eks_client(region_name: str = 'us-east-1',
                   profile_name: Optional[str] = None):
    """Initialize EKS client with optional profile"""
    session = boto3.Session(
        region_name=region_name,
        profile_name=profile_name
    )
    return session.client('eks')

# Usage
eks = get_eks_client(region_name='us-west-2')
```

### Essential Cluster Operations

```python
# Describe cluster
cluster = eks.describe_cluster(name='my-cluster')
print(f"Status: {cluster['cluster']['status']}")
print(f"Endpoint: {cluster['cluster']['endpoint']}")
print(f"Version: {cluster['cluster']['version']}")

# List clusters
clusters = eks.list_clusters()
for cluster_name in clusters['clusters']:
    print(cluster_name)

# Check cluster status
waiter = eks.get_waiter('cluster_active')
waiter.wait(name='my-cluster')
```

### Authentication Token Generation

```python
import base64
from botocore.signers import RequestSigner

def get_eks_token(cluster_name: str, region_name: str = 'us-east-1') -> str:
    """Generate EKS authentication token (k8s-aws-v1.*)"""
    session = boto3.Session(region_name=region_name)
    client = session.client('sts')

    service_id = client.meta.service_model.service_id
    signer = RequestSigner(
        service_id,
        region_name,
        'sts',
        'v4',
        session.get_credentials(),
        session.events
    )

    params = {
        'method': 'GET',
        'url': f'https://sts.{region_name}.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15',
        'body': {},
        'headers': {
            'x-k8s-aws-id': cluster_name
        },
        'context': {}
    }

    signed_url = signer.generate_presigned_url(
        params,
        region_name=region_name,
        expires_in=60,
        operation_name=''
    )

    token = 'k8s-aws-v1.' + base64.urlsafe_b64encode(
        signed_url.encode('utf-8')
    ).decode('utf-8').rstrip('=')

    return token

# Usage with Kubernetes client
from kubernetes import client as k8s_client

token = get_eks_token('my-cluster', 'us-west-2')
configuration = k8s_client.Configuration()
configuration.host = cluster['cluster']['endpoint']
configuration.api_key = {"authorization": f"Bearer {token}"}
configuration.ssl_ca_cert = '/tmp/ca.crt'  # Cluster CA certificate
```

### Kubeconfig Generation

```python
import yaml
from pathlib import Path

def generate_kubeconfig(cluster_name: str,
                        region_name: str,
                        output_path: str = '~/.kube/config') -> dict:
    """Generate kubeconfig for EKS cluster"""
    eks = get_eks_client(region_name)
    cluster_info = eks.describe_cluster(name=cluster_name)['cluster']

    kubeconfig = {
        'apiVersion': 'v1',
        'kind': 'Config',
        'clusters': [{
            'cluster': {
                'certificate-authority-data': cluster_info['certificateAuthority']['data'],
                'server': cluster_info['endpoint']
            },
            'name': cluster_info['arn']
        }],
        'contexts': [{
            'context': {
                'cluster': cluster_info['arn'],
                'user': cluster_info['arn']
            },
            'name': cluster_info['arn']
        }],
        'current-context': cluster_info['arn'],
        'users': [{
            'name': cluster_info['arn'],
            'user': {
                'exec': {
                    'apiVersion': 'client.authentication.k8s.io/v1beta1',
                    'command': 'aws',
                    'args': [
                        'eks',
                        'get-token',
                        '--cluster-name',
                        cluster_name,
                        '--region',
                        region_name
                    ],
                    'env': None,
                    'interactiveMode': 'IfAvailable',
                    'provideClusterInfo': False
                }
            }
        }]
    }

    # Write to file
    output = Path(output_path).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w') as f:
        yaml.dump(kubeconfig, f, default_flow_style=False)

    return kubeconfig
```

### Node Group Management

```python
# List node groups
nodegroups = eks.list_nodegroups(clusterName='my-cluster')
for ng in nodegroups['nodegroups']:
    print(ng)

# Describe node group
ng_info = eks.describe_nodegroup(
    clusterName='my-cluster',
    nodegroupName='my-nodegroup'
)
print(f"Status: {ng_info['nodegroup']['status']}")
print(f"Capacity: {ng_info['nodegroup']['scalingConfig']}")

# Update node group scaling
eks.update_nodegroup_config(
    clusterName='my-cluster',
    nodegroupName='my-nodegroup',
    scalingConfig={
        'minSize': 2,
        'maxSize': 10,
        'desiredSize': 4
    }
)
```

### Fargate Profiles

```python
# List Fargate profiles
profiles = eks.list_fargate_profiles(clusterName='my-cluster')

# Describe Fargate profile
profile_info = eks.describe_fargate_profile(
    clusterName='my-cluster',
    fargateProfileName='my-fargate-profile'
)
print(f"Status: {profile_info['fargateProfile']['status']}")
print(f"Selectors: {profile_info['fargateProfile']['selectors']}")
```

## Common Patterns

### Error Handling

```python
from botocore.exceptions import ClientError, BotoCoreError

try:
    cluster = eks.describe_cluster(name='my-cluster')
except eks.exceptions.ResourceNotFoundException:
    print("Cluster not found")
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'AccessDeniedException':
        print("Insufficient permissions")
    else:
        print(f"AWS Error: {error_code}")
except BotoCoreError as e:
    print(f"Connection error: {e}")
```

### Async Operations with Waiters

```python
# Wait for cluster to be active
waiter = eks.get_waiter('cluster_active')
waiter.wait(
    name='my-cluster',
    WaiterConfig={
        'Delay': 30,  # Poll every 30 seconds
        'MaxAttempts': 40  # Max 20 minutes
    }
)

# Wait for cluster deletion
waiter = eks.get_waiter('cluster_deleted')
waiter.wait(name='my-cluster')

# Wait for nodegroup active
waiter = eks.get_waiter('nodegroup_active')
waiter.wait(
    clusterName='my-cluster',
    nodegroupName='my-nodegroup'
)
```

### IRSA (IAM Roles for Service Accounts)

```python
# Get OIDC provider for cluster
cluster = eks.describe_cluster(name='my-cluster')['cluster']
oidc_issuer = cluster['identity']['oidc']['issuer']
print(f"OIDC Issuer: {oidc_issuer}")

# OIDC issuer URL (without https://)
oidc_provider = oidc_issuer.replace('https://', '')

# Use with IAM to create trust relationship
# (See references/auth-tokens.md for complete IRSA setup)
```

## Progressive Disclosure

### Quick Start (This File)
- Client initialization
- Essential cluster operations
- Token generation for K8s client
- Kubeconfig generation
- Basic node group operations

### Detailed References
- **[Cluster Operations](references/cluster-operations.md)**: Complete cluster lifecycle management, version updates, configuration changes, and advanced waiter patterns
- **[Authentication & Tokens](references/auth-tokens.md)**: Token generation, refresh patterns, cross-account access, IRSA setup, and Kubernetes client integration
- **[Node Groups & Fargate](references/nodegroups-fargate.md)**: Managed node groups, Fargate profiles, add-ons, scaling operations, and update workflows

## When to Use This Skill

Use this skill when:
- Managing EKS clusters programmatically
- Generating authentication tokens for Kubernetes Python client
- Creating or updating kubeconfig files
- Automating node group scaling
- Setting up Fargate profiles
- Implementing IRSA for pod-level permissions
- Cross-account cluster access
- Integrating EKS with Python applications

## Dependencies

```bash
pip install boto3 botocore kubernetes pyyaml
```

## Related Skills

- **anthropic-expert**: Claude API patterns for agent-based EKS management
- **claude-cost-optimization**: Cost tracking for EKS automation workflows
- **railway-deployment**: Container deployment patterns

## Best Practices

1. **Credentials**: Use IAM roles or profiles, never hardcode credentials
2. **Token Refresh**: EKS tokens expire in 15 minutes, implement refresh logic
3. **Error Handling**: Always handle ResourceNotFoundException and throttling
4. **Waiters**: Use built-in waiters for async operations instead of polling
5. **Region Awareness**: Always specify region explicitly
6. **IRSA**: Use IRSA for pod-level permissions instead of node IAM roles
7. **Pagination**: Use paginators for list operations in large environments
8. **Type Hints**: Include type hints for better IDE support and validation
