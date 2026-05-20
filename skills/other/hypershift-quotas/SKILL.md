---
name: hypershift:quotas
description: Check AWS service quotas and usage before creating HyperShift clusters. Shows capacity for VPCs, NAT gateways, Elastic IPs, and more.
---

# AWS Quotas Check Skill

Check AWS service quotas and current usage to plan HyperShift cluster capacity.

## When to Use

- Before creating new HyperShift clusters
- Capacity planning for parallel CI runs
- Debugging "quota exceeded" errors
- User asks "check quotas" or "can I create more clusters"

## Quick Check

```bash
# Check all quotas and usage
./.github/scripts/hypershift/check-quotas.sh
```

Output shows:
- VPC Resources (VPCs, Internet Gateways, NAT Gateways, Elastic IPs)
- EC2 Resources (Running instances, Security Groups, Launch Templates)
- Load Balancer Resources (NLBs, Target Groups)
- S3 Resources (Buckets)
- IAM Resources (Roles, Instance Profiles)
- Route53 Resources (Hosted Zones)

## Request Quota Increases

```bash
# Request increases for quotas below recommended levels
./.github/scripts/hypershift/check-quotas.sh --request-increases
```

## Key Quotas for HyperShift

Each HyperShift cluster typically requires:

| Resource | Per Cluster | Default Quota | Recommended |
|----------|-------------|---------------|-------------|
| VPCs | 1 | 5 | 5+ |
| NAT Gateways | 3 (per AZ) | 5 | 15+ |
| Elastic IPs | 3 (for NATs) | 5 | 15+ |
| Security Groups | ~10 | 500 | 50+ |
| NLBs | 1-2 | 50 | 10+ |
| IAM Roles | ~5 | 300 | 50+ |
| Route53 Zones | 1-2 | 500 | 10+ |

## Quota Status Interpretation

Output colors:
- **Green**: <60% used (healthy)
- **Yellow**: 60-80% used (monitor)
- **Red**: >80% used (action needed)

Recommended warnings show when quota is below suggested minimum.

## Manual Quota Check

```bash
# VPCs
aws ec2 describe-vpcs --query 'Vpcs | length(@)'

# NAT Gateways (active only)
aws ec2 describe-nat-gateways \
    --filter "Name=state,Values=available,pending" \
    --query 'NatGateways | length(@)'

# Elastic IPs
aws ec2 describe-addresses --query 'Addresses | length(@)'

# Security Groups
aws ec2 describe-security-groups --query 'SecurityGroups | length(@)'

# Running Instances
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running,pending" \
    --query 'Reservations[*].Instances | length(@)'
```

## Service Quota API

```bash
# Get specific quota
aws service-quotas get-service-quota \
    --service-code vpc \
    --quota-code L-F678F1CE \
    --query 'Quota.Value'

# Common quota codes:
# VPCs:              vpc / L-F678F1CE
# NAT Gateways:      vpc / L-FE5A380F
# Elastic IPs:       ec2 / L-0263D0A3
# Security Groups:   ec2 / L-0EA8095F
# NLBs:              elasticloadbalancing / L-69A177A2
```

## Request Quota Increase Manually

```bash
# Request quota increase
aws service-quotas request-service-quota-increase \
    --service-code vpc \
    --quota-code L-FE5A380F \
    --desired-value 20 \
    --region us-east-1
```

## Troubleshooting Quota Issues

### "VpcLimitExceeded"

```bash
# Check VPC count and limit
aws ec2 describe-vpcs --query 'Vpcs | length(@)'
./.github/scripts/hypershift/check-quotas.sh | grep -A2 "VPC Resources"

# Delete unused VPCs (carefully!)
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,Tags[?Key==`Name`].Value|[0]]' --output table
```

### "AddressLimitExceeded"

```bash
# Find unused Elastic IPs
aws ec2 describe-addresses \
    --query 'Addresses[?AssociationId==`null`].[AllocationId,PublicIp]' \
    --output table

# Release unused EIPs
aws ec2 release-address --allocation-id <allocation-id>
```

### "NatGatewayLimitExceeded"

```bash
# Find orphaned NAT Gateways
aws ec2 describe-nat-gateways \
    --filter "Name=state,Values=available" \
    --query 'NatGateways[*].[NatGatewayId,State,VpcId]' \
    --output table
```

## CI Parallel Run Capacity

For CI with parallel HyperShift runs, plan quotas:

| Parallel Runs | NAT Gateways | Elastic IPs | VPCs |
|---------------|--------------|-------------|------|
| 1 | 5 | 5 | 2 |
| 2 | 8 | 8 | 3 |
| 3 | 12 | 12 | 4 |
| 4 | 15 | 15 | 5 |

Add buffer for failed cleanups that may leave orphaned resources.

## Related Skills

- **hypershift:cluster**: Create and destroy clusters
- **hypershift:debug**: Debug stuck resources
- **hypershift:preflight**: Full pre-flight check

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
