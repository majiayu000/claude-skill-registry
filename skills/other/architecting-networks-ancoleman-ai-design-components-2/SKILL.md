---
name: architecting-networks
description: Design cloud network architectures with VPC patterns, subnet strategies, zero trust principles, and hybrid connectivity. Use when planning VPC topology, implementing multi-cloud networking, or establishing secure network segmentation for cloud workloads.
---

# Network Architecture

Design secure, scalable cloud network architectures using proven patterns across AWS, GCP, and Azure. This skill provides decision frameworks for VPC design, subnet strategy, zero trust implementation, and hybrid connectivity.

## When to Use This Skill

Invoke this skill when:
- Designing VPC/VNet topology for new cloud environments
- Implementing network segmentation and security controls
- Planning multi-VPC or multi-cloud connectivity
- Establishing hybrid cloud connectivity (on-premises to cloud)
- Migrating from flat network to sophisticated architecture
- Implementing zero trust network principles
- Optimizing network costs and performance

## Core Network Architecture Patterns

### Pattern 1: Flat (Single VPC) Architecture

**Use When:** Small applications, single environment, simple security requirements, team < 10 engineers

**Characteristics:**
- All resources in one VPC with subnet-level segmentation
- Public, private, and database subnet tiers
- Simplest to understand and manage
- No inter-VPC routing complexity

**Tradeoffs:**
- ✓ Lowest cost, fastest to set up
- ✗ Poor isolation, difficult to scale, entire VPC is blast radius

### Pattern 2: Multi-VPC (Isolated) Architecture

**Use When:** Multiple environments (dev/staging/prod), strong isolation requirements, compliance mandates separation

**Characteristics:**
- Separate VPCs per environment or workload
- No direct connectivity without explicit setup
- Independent CIDR ranges

**Tradeoffs:**
- ✓ Strong blast radius containment, clear security boundaries
- ✗ Management overhead, duplicate infrastructure, higher costs

### Pattern 3: Hub-and-Spoke (Transit Gateway) Architecture

**Use When:** 5+ VPCs need communication, centralized security inspection required, hybrid connectivity, multi-account setup

**Characteristics:**
- Central hub VPC/Transit Gateway
- Spoke VPCs connect to hub
- All inter-VPC traffic routes through hub

**Tradeoffs:**
- ✓ Simplified routing, centralized security, scales easily (100+ VPCs)
- ✗ Transit Gateway costs (~$0.05/hour + $0.02/GB), increased latency (hub hop)

### Pattern 4: Full Mesh (VPC Peering) Architecture

**Use When:** Small number of VPCs (< 5), low latency critical, no centralized inspection needed

**Characteristics:**
- Every VPC directly connected via peering
- Direct VPC-to-VPC communication

**Tradeoffs:**
- ✓ Lowest latency, no Transit Gateway costs
- ✗ Management complexity scales as O(n²), doesn't scale beyond ~10 VPCs

### Pattern 5: Hybrid (Multi-Pattern) Architecture

**Use When:** Large enterprise with diverse requirements, balancing cost/performance/security

**Characteristics:**
- Hub-spoke for most VPCs + direct peering for latency-sensitive pairs
- Combination based on workload requirements

**Tradeoffs:**
- ✓ Optimized for specific needs
- ✗ More complex to design and manage

## Pattern Selection Framework

```
Number of VPCs?
│
├─► 1 VPC → Flat (Single VPC)
├─► 2-4 VPCs + No inter-VPC communication → Multi-VPC (Isolated)
├─► 2-5 VPCs + Low latency critical → Full Mesh (VPC Peering)
├─► 5+ VPCs + Centralized inspection → Hub-and-Spoke (Transit Gateway)
└─► 10+ VPCs + Mixed requirements → Hybrid (Multi-Pattern)

Additional Considerations:
├─► Hybrid connectivity required? → Hub-and-Spoke preferred
├─► Centralized egress/inspection? → Hub-and-Spoke with Inspection VPC
├─► Multi-account environment? → Hub-and-Spoke with AWS RAM sharing
└─► Cost optimization priority? → Flat or Multi-VPC (avoid TGW fees)
```

## Subnet Strategy

### Standard Three-Tier Design

**Public Subnets:**
- Route to Internet Gateway
- Use for load balancers, bastion hosts, NAT Gateways
- CIDR: /24 to /27 (256 to 32 IPs)

**Private Subnets:**
- Route to NAT Gateway for outbound
- Use for application servers, containers, compute workloads
- CIDR: /20 to /22 (4,096 to 1,024 IPs)

**Database Subnets:**
- No direct internet route
- Use for RDS, ElastiCache, managed databases
- CIDR: /24 to /26 (256 to 64 IPs)

### Multi-AZ Distribution

**Production:** Distribute each tier across 3 Availability Zones minimum
**Dev/Test:** 1-2 AZs acceptable for cost savings

### CIDR Block Planning

**VPC Sizing:**
- /16 (65,536 IPs) - Large production environments
- /20 (4,096 IPs) - Medium environments
- /24 (256 IPs) - Small/dev environments

**Critical Rules:**
- Non-overlapping CIDR ranges across VPCs
- Coordinate with on-premises network team for hybrid connectivity
- Reserve address space for future expansion

For detailed subnet planning, see `references/subnet-strategy.md`

## NAT Gateway Strategy

### Decision Framework

```
Cost vs Resilience?
│
├─► Cost Priority (Dev/Test)
│   └─► Single NAT Gateway (~$32/month)
│       └─► Risk: Single point of failure
│
├─► Balanced (Most Production)
│   └─► One NAT Gateway per AZ (~$96/month for 3 AZs)
│       └─► Resilience: AZ failure doesn't break connectivity
│
└─► Maximum Resilience
    └─► Multiple NAT Gateways per AZ + monitoring
        └─► Critical workloads, SLA-dependent

Alternative: Centralized Egress Pattern
└─► Hub-and-Spoke: Single egress VPC with NAT
    └─► Reduces NAT Gateway count, centralized logging
```

**No Outbound Internet Needed?**
- Skip NAT Gateway entirely (cost savings)
- Use VPC Endpoints for AWS service access

## Security Controls

### Security Groups (Recommended)

**Characteristics:**
- Stateful (return traffic auto-allowed)
- Instance-level control
- Allow rules only (implicit deny)
- Can reference other security groups

**Use For:**
- Service-to-service communication
- Instance-level security
- Most common use case

**Best Practices:**
- Use descriptive names (app-alb-sg, app-backend-sg)
- Reference other security groups instead of CIDR blocks
- Keep rules minimal and specific

### Network ACLs (Optional)

**Characteristics:**
- Stateless (must allow both request and response)
- Subnet-level control
- Allow and deny rules
- Processes rules in order (lowest number first)

**Use For:**
- Explicit deny rules (block specific IPs)
- Compliance requirements (defense in depth)
- Additional layer beyond security groups

**Best Practices:**
- Use sparingly (complex to manage)
- Remember to allow ephemeral ports (1024-65535)
- Test thoroughly (stateless nature causes issues)

For security group architecture patterns, see `references/security-controls.md`

## Zero Trust Principles

### Core Tenets

1. **Never Trust, Always Verify**
   - Authenticate every request regardless of source
   - No implicit trust based on network location

2. **Least Privilege Access**
   - Grant minimum necessary permissions
   - Time-bound access (just-in-time)

3. **Assume Breach**
   - Segment network aggressively
   - Monitor all traffic
   - Rapid detection and response

### Implementation Patterns

**Microsegmentation:**
- Isolate every workload with granular security group rules
- Service-to-service communication only between specific services
- Reduce blast radius

**Identity-Based Access:**
- Use IAM roles instead of IP addresses for authorization
- VPC Endpoints with IAM policies
- Service-to-service identity verification

**Continuous Verification:**
- VPC Flow Logs for traffic analysis
- Monitor rejected connections
- Alert on anomalies

For zero trust architecture patterns, see `references/zero-trust-networking.md`

## Hybrid Connectivity

### VPN (Virtual Private Network)

**Use When:** Dev/test environments, backup connectivity, temporary connections

**Characteristics:**
- Encrypted tunnel over public internet
- Throughput: ~1.25 Gbps per tunnel
- Latency: Variable (internet-dependent)
- Cost: Low (~$0.05/hour + data transfer)
- Setup: Quick (no contracts)

### Direct Connect / ExpressRoute / Cloud Interconnect

**Use When:** Production workloads, large data transfers, real-time applications

**Characteristics:**
- Dedicated network connection (bypasses public internet)
- Throughput: Up to 100 Gbps
- Latency: Low and consistent
- Cost: Higher (port fees + data transfer)
- Setup: Slower (contracts, coordination)

### Transit Gateway + Direct Connect

**Use When:** Multiple VPCs need on-premises connectivity

**Benefits:**
- Single Direct Connect connection → Transit Gateway → Multiple VPCs
- Cost efficient and scalable
- Centralized hybrid connectivity

For hybrid connectivity patterns and examples, see `references/hybrid-connectivity.md`

## Multi-Cloud Networking

### Unified Concepts Across Providers

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Virtual Network | VPC | VPC | Virtual Network (VNet) |
| Subnets | Subnets (AZ-scoped) | Subnets (Regional) | Subnets |
| NAT | NAT Gateway | Cloud NAT | NAT Gateway |
| Peering | VPC Peering | VPC Peering | VNet Peering |
| Hub-Spoke | Transit Gateway | Cloud Router | Virtual WAN |
| Private Endpoints | PrivateLink | Private Service Connect | Private Link |
| Hybrid VPN | VPN | Cloud VPN | VPN Gateway |
| Hybrid Dedicated | Direct Connect | Cloud Interconnect | ExpressRoute |

### Provider-Specific Best Practices

**AWS:**
- Multi-AZ baseline for production
- Prefer Transit Gateway for 5+ VPCs
- Use VPC Endpoints to avoid NAT charges

**GCP:**
- Custom mode VPC (not auto-mode)
- Start with single VPC, use Shared VPC for multi-project
- Grant network user role at subnet level

**Azure:**
- Hub-and-spoke network topology as standard
- Few large VNets vs many small VNets
- Private endpoints for Azure services

For multi-cloud implementations, see `references/multi-cloud-networking.md`

## Network Observability

### VPC Flow Logs

**Enable Flow Logs for:**
- Traffic analysis and troubleshooting
- Security monitoring (detect unauthorized access)
- Cost attribution by network path
- Compliance requirements

**Configuration:**
- Traffic type: ALL (capture accepted and rejected)
- Aggregation interval: 1-10 minutes
- Destination: CloudWatch Logs or S3

### Monitoring Patterns

**Monitor:**
- Rejected connections (security anomalies)
- Traffic volume spikes
- Cross-VPC communication patterns
- NAT Gateway utilization

**Alert On:**
- Spike in rejected connections
- Unusual traffic patterns
- High data transfer costs
- Network errors

For observability patterns and flow log analysis, see `references/network-observability.md`

## Cost Optimization

### Common Cost Drivers

1. **NAT Gateway:** $0.045/hour + $0.045/GB data processed
2. **Transit Gateway:** $0.05/hour/attachment + $0.02/GB
3. **Data Transfer:** Egress charges vary by destination
4. **VPN/Direct Connect:** Port fees + data transfer

### Optimization Strategies

**Reduce NAT Gateway Costs:**
- Use VPC Endpoints for AWS services (S3, DynamoDB)
- Centralized egress VPC pattern
- Single NAT Gateway for dev/test (accept availability risk)

**Reduce Data Transfer Costs:**
- Keep traffic within same region
- Use VPC Endpoints instead of public internet
- Private connectivity for high-volume transfers

**Avoid Transit Gateway Costs:**
- Use VPC Peering for small number of VPCs (< 5)
- Direct peering for latency-sensitive pairs

For detailed cost optimization strategies, see `references/cost-optimization.md`

## Implementation Workflow

### Step 1: Analyze Requirements

- How many VPCs/environments needed?
- Hybrid connectivity required?
- Latency requirements?
- Security/compliance requirements?
- Budget constraints?

### Step 2: Select Pattern

Use pattern selection framework above to choose:
- Flat, Multi-VPC, Hub-Spoke, Mesh, or Hybrid

### Step 3: Design Subnets

- Calculate CIDR blocks (non-overlapping)
- Plan multi-AZ distribution
- Determine public/private/database tiers

### Step 4: Configure Security

- Design security group architecture
- Plan microsegmentation
- Configure Network ACLs if needed

### Step 5: Implement with IaC

Use `infrastructure-as-code` skill to implement with Terraform/Pulumi

### Step 6: Enable Observability

- Configure VPC Flow Logs
- Set up monitoring and alerting
- Cost tracking

## Quick Reference

### VPC Pattern Selection

| Requirement | Recommended Pattern |
|-------------|---------------------|
| Single environment | Flat (Single VPC) |
| Multiple isolated environments | Multi-VPC (Isolated) |
| 2-5 VPCs, low latency | Full Mesh (Peering) |
| 5+ VPCs, centralized security | Hub-and-Spoke (TGW) |
| Hybrid connectivity | Hub-and-Spoke (TGW) |
| Cost optimization | Flat or Multi-VPC |

### NAT Gateway Configuration

| Scenario | Configuration | Monthly Cost (3 AZs) |
|----------|---------------|----------------------|
| Dev/Test | Single NAT | ~$32 |
| Production | NAT per AZ | ~$96 |
| Centralized Egress | Hub VPC NAT | ~$32-96 |

### Hybrid Connectivity

| Requirement | Solution | Throughput | Latency |
|-------------|----------|------------|---------|
| Dev/Test | VPN | ~1.25 Gbps | Variable |
| Production | Direct Connect | Up to 100 Gbps | Low, consistent |
| Backup | VPN (backup to DX) | ~1.25 Gbps | Variable |

## Reference Documentation

**Detailed Guides:**
- `references/vpc-design-patterns.md` - Comprehensive pattern descriptions with diagrams
- `references/subnet-strategy.md` - CIDR planning, IPAM, multi-AZ best practices
- `references/zero-trust-networking.md` - Microsegmentation, IAM integration, continuous verification
- `references/hybrid-connectivity.md` - VPN, Direct Connect, Transit Gateway patterns
- `references/multi-cloud-networking.md` - AWS, GCP, Azure implementations
- `references/security-controls.md` - Security groups, NACLs, firewall patterns
- `references/private-networking.md` - VPC Endpoints, PrivateLink, Private Service Connect
- `references/multi-region-networking.md` - Cross-region peering, global load balancing
- `references/network-observability.md` - Flow logs, monitoring, troubleshooting
- `references/cost-optimization.md` - Egress reduction, NAT strategies

**Code Examples:**
- `examples/aws/` - AWS VPC patterns (flat, hub-spoke, peering, VPN, Direct Connect)
- `examples/gcp/` - GCP VPC patterns (custom VPC, Shared VPC, Cloud Interconnect)
- `examples/azure/` - Azure VNet patterns (hub-spoke, peering, ExpressRoute)
- `examples/multi-cloud/` - Cross-cloud connectivity examples

**Utility Scripts:**
- `scripts/cidr-calculator.py` - Calculate CIDR blocks and plan IP addressing
- `scripts/cost-estimator.sh` - Estimate network infrastructure costs
- `scripts/validate-sg-rules.py` - Validate security group rule configurations
- `scripts/flow-log-analyzer.py` - Analyze VPC flow logs for security and cost

## Integration with Other Skills

**Use `infrastructure-as-code` skill to:**
- Implement network architectures with Terraform/Pulumi
- Version control network configurations
- Automate network provisioning

**Use `kubernetes-operations` skill to:**
- Configure Kubernetes networking (CNI) on top of VPC design
- Implement pod networking and service meshes

**Use `security-hardening` skill to:**
- Implement firewall rules and WAF configurations
- Configure network-level DDoS protection
- Set up intrusion detection systems

**Use `observability` skill to:**
- Implement comprehensive network monitoring
- Set up distributed tracing across network boundaries
- Configure performance dashboards

**Use `disaster-recovery` skill to:**
- Design multi-region failover networking
- Implement cross-region backup connectivity
- Plan network recovery procedures
