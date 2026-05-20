---
name: hypershift:debug
description: Debug AWS resources for HyperShift clusters - identify stuck resources, orphaned infrastructure, and deletion blockers
---

# AWS HyperShift Debug Skill

This skill helps debug AWS resources related to HyperShift clusters, identifying resources that may be blocking cluster deletion or orphaned infrastructure.

## When to Use

- Cluster deletion is stuck (finalizer not removed)
- Need to identify orphaned AWS resources
- Debugging IAM permission issues during cluster operations
- Verifying cleanup after cluster destruction
- User asks "debug hypershift" or "why is cluster stuck"

## Arguments

- `cluster-name`: The HyperShift cluster name or suffix to debug (optional, defaults to local)
- `--check`: Quiet mode - returns exit code only (0=no resources, 1=resources exist)

## Quick Debug Commands

### Prerequisites

Ensure credentials are loaded:
```bash
# Load HyperShift credentials (from kagenti repo root)
source .env.kagenti-hypershift-custom  # or .env.hypershift-ci
```

### Run Full Debug Script

```bash
# Run comprehensive AWS debug
./.github/scripts/hypershift/debug-aws-hypershift.sh [cluster-name]

# Examples:
./.github/scripts/hypershift/debug-aws-hypershift.sh              # defaults to username
./.github/scripts/hypershift/debug-aws-hypershift.sh ladas        # suffix only
./.github/scripts/hypershift/debug-aws-hypershift.sh kagenti-hypershift-custom-ladas  # full name
./.github/scripts/hypershift/debug-aws-hypershift.sh pr529

# Check mode (quiet, returns exit code only)
./.github/scripts/hypershift/debug-aws-hypershift.sh --check ladas
echo $?  # 0 = no resources, 1 = resources exist
```

## Manual Debug Commands

### Check HostedCluster Status

```bash
# Set management cluster kubeconfig
source .env.kagenti-hypershift-custom  # loads KUBECONFIG

# Get HostedCluster status
oc get hostedcluster -n clusters <cluster-name> -o yaml

# Check deletion timestamp and finalizers
oc get hostedcluster -n clusters <cluster-name> -o jsonpath='{.metadata.deletionTimestamp}{"\n"}{.metadata.finalizers}'

# Check conditions
oc get hostedcluster -n clusters <cluster-name> -o jsonpath='{range .status.conditions[*]}{.type}{": "}{.status}{" - "}{.message}{"\n"}{end}'
```

### Check HyperShift Operator Logs

```bash
# Operator logs (filtered for cluster)
oc logs -n hypershift -l app=operator --tail=200 | grep -i "<cluster-name>\|error\|failed\|denied"

# All operator logs
oc logs -n hypershift -l app=operator --tail=500
```

### EC2 Resources

```bash
# EC2 Instances
aws ec2 describe-instances \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,Tags[?Key==`Name`].Value|[0]]' \
    --output table

# VPCs
aws ec2 describe-vpcs \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'Vpcs[*].[VpcId,State,CidrBlock]' \
    --output table

# Subnets
aws ec2 describe-subnets \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'Subnets[*].[SubnetId,State,CidrBlock,AvailabilityZone]' \
    --output table

# Security Groups
aws ec2 describe-security-groups \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'SecurityGroups[*].[GroupId,GroupName,VpcId]' \
    --output table

# NAT Gateways
aws ec2 describe-nat-gateways \
    --filter "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'NatGateways[*].[NatGatewayId,State,VpcId]' \
    --output table

# Internet Gateways
aws ec2 describe-internet-gateways \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'InternetGateways[*].[InternetGatewayId,Attachments[0].VpcId]' \
    --output table

# Elastic IPs
aws ec2 describe-addresses \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'Addresses[*].[AllocationId,PublicIp]' \
    --output table
```

### Load Balancers

```bash
# Classic ELBs
aws elb describe-load-balancers \
    --query "LoadBalancerDescriptions[?contains(LoadBalancerName, '<cluster-name>')].[LoadBalancerName,Scheme]" \
    --output table

# ALB/NLBs
aws elbv2 describe-load-balancers \
    --query "LoadBalancers[?contains(LoadBalancerName, '<cluster-name>')].[LoadBalancerName,Type,State.Code]" \
    --output table
```

### S3 Buckets

```bash
# List S3 buckets for cluster
aws s3api list-buckets --query "Buckets[?contains(Name, '<cluster-name>')].Name" --output text

# Check bucket contents (if exists)
aws s3 ls s3://<bucket-name>/ --recursive
```

### IAM Resources

```bash
# IAM Roles
aws iam list-roles --query "Roles[?contains(RoleName, '<cluster-name>')].RoleName" --output text

# Instance Profiles
aws iam list-instance-profiles --query "InstanceProfiles[?contains(InstanceProfileName, '<cluster-name>')].InstanceProfileName" --output text

# OIDC Providers
aws iam list-open-id-connect-providers --query 'OpenIDConnectProviderList[*].Arn' --output text | tr '\t' '\n' | grep "<cluster-name>"
```

### Route53

```bash
# Hosted zones
aws route53 list-hosted-zones --query "HostedZones[?contains(Name, '<cluster-name>')].[Name,Id,Config.PrivateZone]" --output table

# All zones (for reference)
aws route53 list-hosted-zones --query 'HostedZones[*].[Name,Id,Config.PrivateZone]' --output table
```

## Cleanup Commands (Use with Caution)

### Force Remove HostedCluster Finalizer

**Warning**: This orphans AWS resources. Only use if resources are already deleted or you will clean them manually.

```bash
oc patch hostedcluster -n clusters <cluster-name> \
    -p '{"metadata":{"finalizers":null}}' --type=merge
```

### Manual Resource Cleanup Order

If you need to manually delete AWS resources, delete in this order:

1. **EC2 Instances** - Terminate worker nodes
2. **NAT Gateways** - Delete and wait for deletion
3. **Elastic IPs** - Release after NAT gateways deleted
4. **Load Balancers** - Delete ELBs/ALBs/NLBs
5. **Security Groups** - Delete (may need multiple passes for dependencies)
6. **Subnets** - Delete all subnets
7. **Internet Gateways** - Detach and delete
8. **VPCs** - Delete VPC
9. **Route53** - Delete private hosted zone
10. **S3 Buckets** - Empty and delete OIDC bucket
11. **IAM Roles** - Delete roles and instance profiles
12. **OIDC Provider** - Delete OIDC provider

```bash
# Example: Delete all EC2 instances for a cluster
INSTANCE_IDS=$(aws ec2 describe-instances \
    --filters "Name=tag-key,Values=kubernetes.io/cluster/<cluster-name>" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text)
aws ec2 terminate-instances --instance-ids $INSTANCE_IDS
```

## Find Orphaned Resources

```bash
# Find orphaned resources across all clusters
./.github/scripts/hypershift/find-orphaned-resources.sh
```

## Common Issues

### Issue: Cluster stuck in deletion

**Symptoms**: HostedCluster has deletionTimestamp but finalizer remains

**Debug Steps**:
1. Check HyperShift operator logs for errors
2. Check AWS resources still exist (VPCs, subnets, etc.)
3. Verify IAM permissions for resource deletion
4. Check if resources have dependencies blocking deletion

**Common Causes**:
- Security group has dependencies
- ENIs attached to resources
- Load balancer still has targets
- IAM policy doesn't allow deletion

### Issue: Permission denied during deletion

**Symptoms**: Operator logs show "Access Denied" or "UnauthorizedOperation"

**Debug Steps**:
1. Check which resource deletion is failing
2. Verify IAM policy has permission for that resource type
3. Check if tag conditions match (kubernetes.io/cluster/<cluster-name>)

**Fix**: Update IAM policies and re-run setup script:
```bash
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh
```

### Issue: AWS resources orphaned

**Symptoms**: HostedCluster deleted but AWS resources remain

**Debug Steps**:
1. Run this debug skill to find remaining resources
2. Note all resource IDs
3. Follow manual cleanup order above

## Integration with Other Skills

- **hypershift:cluster**: Create and destroy clusters
- **hypershift:quotas**: Check AWS quotas before debugging
- **k8s:health**: Check overall cluster health after debugging
- **k8s:logs**: Examine HyperShift operator logs in detail
- **k8s:pods**: Debug control plane pods on management cluster

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
