---
name: multi-cloud-architecture
description: Design multi-cloud and hybrid architectures across AWS, Azure, and GCP — covering service selection, networking, cost optimization, and migration strategy. Use when building multi-cloud systems, planning hybrid connectivity, optimizing cloud spend, or avoiding vendor lock-in.
---

# Multi-Cloud Architecture

## Service Comparison

### Compute
| AWS | Azure | GCP | Use Case |
|-----|-------|-----|----------|
| EC2 | Virtual Machines | Compute Engine | IaaS VMs |
| ECS | Container Instances | Cloud Run | Containers |
| EKS | AKS | GKE | Kubernetes |
| Lambda | Functions | Cloud Functions | Serverless |

### Storage
| AWS | Azure | GCP | Use Case |
|-----|-------|-----|----------|
| S3 | Blob Storage | Cloud Storage | Object |
| EBS | Managed Disks | Persistent Disk | Block |
| EFS | Azure Files | Filestore | File |

### Database
| AWS | Azure | GCP | Use Case |
|-----|-------|-----|----------|
| RDS | SQL Database | Cloud SQL | Managed SQL |
| DynamoDB | Cosmos DB | Firestore | NoSQL |
| Aurora | PostgreSQL/MySQL | Cloud Spanner | Distributed SQL |
| ElastiCache | Cache for Redis | Memorystore | Caching |

## Architecture Patterns

**Single Provider with DR** -- Primary workload in one cloud, DR in another. Database replication + automated failover.

**Best-of-Breed** -- AI/ML on GCP, Enterprise apps on Azure, General compute on AWS. Pick strengths per provider.

**Geographic Distribution** -- Serve from nearest region, data sovereignty compliance, global load balancing.

**Cloud-Agnostic Abstraction** -- Portable stack to reduce lock-in:
| Layer | Portable Choice |
|-------|----------------|
| Compute | Kubernetes (EKS/AKS/GKE) |
| Database | PostgreSQL/MySQL |
| Messaging | Apache Kafka |
| Cache | Redis |
| Object Storage | S3-compatible API (MinIO) |
| Monitoring | Prometheus/Grafana |
| Service Mesh | Istio/Linkerd |
| IaC | Terraform/OpenTofu |

## Networking

### Connection Options
| Provider | VPN | Dedicated |
|----------|-----|-----------|
| AWS | Site-to-Site VPN (1.25 Gbps/tunnel) | Direct Connect (1-100 Gbps) |
| Azure | VPN Gateway (varies by SKU) | ExpressRoute (up to 100 Gbps) |
| GCP | Cloud VPN HA (3 Gbps/tunnel, 99.99% SLA) | Cloud Interconnect (10-100 Gbps) |

### VPN vs Dedicated Connection Decision
| Factor | VPN | Dedicated (DC/ER/Interconnect) |
|--------|-----|-------------------------------|
| Bandwidth need | < 1.25 Gbps | > 1 Gbps or consistent throughput |
| Latency tolerance | Variable OK | Predictable required |
| Setup time | Hours | Weeks-months |
| Cost | Low (pay per hour) | Higher (port + data) |
| Encryption | Built-in IPsec | Must add if needed (MACsec or overlay) |

**Default:** Start with VPN, upgrade to dedicated when bandwidth or latency demands it.

### Hub-and-Spoke Topology
```
On-Premises Datacenter
         |
    VPN / Direct Connect
         |
    Transit Gateway (AWS) / vWAN (Azure) / Cloud Router (GCP)
    +-- Production VPC/VNet
    +-- Staging VPC/VNet
    +-- Development VPC/VNet
```

### BGP Essentials
- On-prem router advertises internal CIDRs (e.g., 10.0.0.0/8) with private ASN (64512-65534)
- Cloud-side ASNs: AWS default 64512, Azure fixed 65515, GCP configurable
- Always run dual tunnels for HA -- active/active with ECMP or active/passive
- Monitor: tunnel status, BGP session state, packet loss, latency, bytes in/out

## Cost Optimization

### Pricing Models
| Model | AWS | Azure | GCP |
|-------|-----|-------|-----|
| Reserved | RI + Savings Plans (30-72%) | Reserved VMs (up to 72%) | Committed Use (up to 57%) |
| Spot/Preemptible | Spot (up to 90% off, 2-min notice) | Spot VMs | Preemptible (80% off, 24h max) |
| Auto-discount | None | Hybrid Benefit (existing licenses) | Sustained Use (auto 30%) |

### Tagging Strategy (Required Tags)
| Tag | Purpose | Example |
|-----|---------|---------|
| Environment | Env separation | production, staging, dev |
| Project | Cost allocation | my-project |
| CostCenter | Chargeback | engineering |
| Owner | Accountability | team@example.com |
| ManagedBy | Drift detection | terraform |

### Cost Optimization Checklist
- [ ] Tag all resources with required tags above
- [ ] Delete unused resources (unattached disks, idle LBs, old snapshots, unassociated EIPs)
- [ ] Right-size instances based on utilization (use provider advisors/recommenders)
- [ ] Reserved capacity for steady-state workloads; spot/preemptible for fault-tolerant
- [ ] Implement auto-scaling with appropriate cooldowns
- [ ] Storage lifecycle policies: hot -> warm -> cold -> archive
- [ ] Set budget alerts at 50%, 80%, 100% thresholds
- [ ] Enable cost anomaly detection
- [ ] Optimize data transfer (same-AZ where possible, VPC endpoints, CDN)
- [ ] Add caching layers to reduce compute/DB load

### Cost Tools
- **AWS:** Cost Explorer, Compute Optimizer, Cost Anomaly Detection
- **Azure:** Cost Management, Advisor
- **GCP:** Cost Management, Recommender
- **Multi-cloud:** CloudHealth, Cloudability, Kubecost

## Migration Strategy

1. **Assessment** -- Inventory workloads, map dependencies, estimate costs, identify compliance constraints
2. **Pilot** -- Select low-risk workload, implement, validate, document lessons
3. **Migration** -- Incremental moves, dual-run period, automated testing, rollback plan per workload
4. **Optimization** -- Right-size, adopt cloud-native services, implement cost governance

## Gotchas and Anti-Patterns

- **Lift-and-shift everything** -- Re-platform or re-architect where ROI justifies it
- **Ignoring egress costs** -- Data transfer between clouds/regions adds up fast; design data gravity around primary provider
- **Multi-cloud for the sake of it** -- Real multi-cloud adds operational complexity; have a concrete reason (DR, best-of-breed, compliance)
- **No abstraction layer** -- Without Terraform/K8s, multi-cloud becomes multi-headache
- **Skipping tagging** -- Impossible to optimize costs or enforce governance without consistent tags
- **Single tunnel** -- Always deploy redundant VPN tunnels; single tunnel = single point of failure
- **Overlapping CIDRs** -- Plan IP address space across all environments upfront; retrofitting is painful
- **No network monitoring** -- Hybrid connectivity issues are invisible without proactive tunnel/BGP monitoring
