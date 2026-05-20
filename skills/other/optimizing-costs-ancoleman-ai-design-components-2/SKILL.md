---
name: optimizing-costs
description: Optimize cloud infrastructure costs through FinOps practices, commitment discounts, right-sizing, and automated cost management. Use when reducing cloud spend, implementing budget controls, or establishing cost visibility across AWS, Azure, GCP, and Kubernetes environments.
---

# Cost Optimization

## Purpose

Cloud cost optimization transforms uncontrolled spending into strategic resource allocation through the FinOps lifecycle: Inform, Optimize, and Operate. This skill provides decision frameworks for commitment-based discounts (Reserved Instances, Savings Plans), right-sizing strategies, Kubernetes cost management, and automated cost governance across multi-cloud environments.

## When to Use This Skill

Invoke cost-optimization when:
- Reducing cloud spend by 15-40% through systematic optimization
- Implementing cost visibility dashboards and allocation tracking
- Establishing budget alerts and anomaly detection
- Optimizing Kubernetes resource requests and cluster efficiency
- Managing Reserved Instances, Savings Plans, or Committed Use Discounts
- Automating idle resource cleanup and right-sizing recommendations
- Setting up showback/chargeback models for internal teams
- Preventing cost overruns through CI/CD cost estimation (Infracost)
- Responding to finance team requests for cloud cost reduction

## FinOps Principles

### The FinOps Lifecycle

```
┌─────────────────────────────────────────────────────┐
│  INFORM → OPTIMIZE → OPERATE (continuous loop)      │
│    ↓         ↓           ↓                          │
│ Visibility  Action   Automation                     │
└─────────────────────────────────────────────────────┘
```

**Inform Phase:** Establish cost visibility
- Enable cost allocation tags (Owner, Project, Environment)
- Deploy real-time cost dashboards for engineering teams
- Integrate cloud billing data (AWS CUR, Azure Consumption API, GCP BigQuery)
- Set up Kubernetes cost monitoring (Kubecost, OpenCost)

**Optimize Phase:** Take action on cost drivers
- Purchase commitment-based discounts (40-72% savings)
- Right-size over-provisioned resources (target 60-80% utilization)
- Implement spot/preemptible instances for fault-tolerant workloads
- Clean up idle resources (unattached volumes, old snapshots)

**Operate Phase:** Automate and govern
- Budget alerts with cascading notifications (50%, 75%, 90%, 100%)
- Automated cleanup scripts for idle resources
- CI/CD cost estimation to prevent surprise increases
- Continuous monitoring with anomaly detection

### Core FinOps Principles

1. **Collaboration:** Cross-functional teams (finance, engineering, operations, product)
2. **Accountability:** Teams own the cost of their services
3. **Transparency:** All costs visible and understandable to stakeholders
4. **Optimization:** Continuous improvement of cost efficiency

For detailed FinOps maturity models and organizational structures, see `references/finops-foundations.md`.

## Cost Optimization Strategies

### 1. Commitment-Based Discounts

**Reserved Instances (RIs):** 40-72% discount for 1-3 year commitments
- **Standard RI:** Instance type locked, highest discount (60% for 3-year)
- **Convertible RI:** Flexible instance types, moderate discount (54% for 3-year)
- **Use for:** Databases (RDS, ElastiCache), stable production EC2 workloads

**Savings Plans:** Flexible compute commitments
- **Compute Savings Plans:** Applies to EC2, Fargate, Lambda (54% discount for 3-year)
- **EC2 Instance Savings Plans:** Tied to instance family (66% discount for 3-year)
- **Use for:** Workloads that change instance types or regions

**GCP Committed Use Discounts (CUDs):** 25-70% discount
- **Resource-based CUDs:** Commit to vCPU, memory, GPUs
- **Spend-based CUDs:** Commit to dollar amount (flexible)
- **Sustained Use Discounts:** Automatic 20-30% discount for sustained usage (no commitment)

**Decision Framework:**
```
Reserve when:
├─ Workload is production-critical (24/7 uptime required)
├─ Usage is predictable (stable baseline over 6+ months)
├─ Architecture is stable (unlikely to change instance types)
└─ Financial commitment acceptable (1-3 year lock-in)

Use On-Demand when:
├─ Development/testing environments
├─ Unpredictable spiky workloads
├─ Short-term projects (<6 months)
└─ Evaluating new instance types
```

For detailed commitment strategies and RI coverage analysis, see `references/commitment-strategies.md`.

### 2. Spot and Preemptible Instances

**Discount:** 70-90% off on-demand pricing (interruptible with 2-minute warning)

**Use Spot For:** CI/CD workers, batch jobs, ML training (with checkpointing), Kubernetes workers, data analytics
**Avoid Spot For:** Stateful databases, real-time services, long-running jobs without checkpointing

**Best Practices:**
- Diversify instance types and spread across Availability Zones
- Implement graceful shutdown handlers
- Auto-fallback to on-demand when capacity unavailable
- Kubernetes: Mix 70% spot + 30% on-demand nodes with taints/tolerations

### 3. Right-Sizing Strategies

**Target Utilization:** 60-80% average (leave headroom for spikes)

**Compute Right-Sizing:**
- Analyze actual CPU/memory utilization over 30+ days
- Downsize instances with <40% average utilization
- Consolidate underutilized workloads
- Switch instance families (compute-optimized vs. memory-optimized)

**Database Right-Sizing:**
- Analyze connection pool usage (max connections vs. allocated)
- Downgrade storage IOPS if utilization <50%
- Evaluate read replica necessity (can caching replace it?)
- Consider serverless options (Aurora Serverless, Azure SQL Serverless)

**Kubernetes Right-Sizing:**
- Set requests = average usage (not peak)
- Set limits = 2-3x requests (allow bursting)
- Use Vertical Pod Autoscaler (VPA) for automated recommendations
- Identify pods with 0% CPU usage (candidates for consolidation)

**Storage Right-Sizing:**
- Delete unattached volumes (EBS, Azure Disks, GCP Persistent Disks)
- Delete old snapshots (>90 days, retention policy not required)
- Implement lifecycle policies (S3 Intelligent-Tiering, Azure Blob Lifecycle)
- Compress/deduplicate data

**Right-Sizing Tools:**
- **AWS Compute Optimizer:** ML-based EC2, Lambda, EBS recommendations
- **Azure Advisor:** VM rightsizing, reserved instance advice
- **GCP Recommender:** VM, disk, commitment recommendations
- **VPA (Vertical Pod Autoscaler):** Automated container resource requests

### 4. Kubernetes Cost Management

**Resource Requests and Limits:**
```yaml
# Set requests = average usage (enables efficient bin-packing)
resources:
  requests:
    cpu: 500m        # 0.5 CPU cores (average usage)
    memory: 1Gi      # 1 GiB memory (average usage)
  limits:
    cpu: 1500m       # 1.5 CPU cores (3x requests, allows bursting)
    memory: 3Gi      # 3 GiB memory (3x requests)
```

**Namespace Quotas:** Prevent runaway resource consumption
- ResourceQuota: Limit total CPU/memory per namespace
- LimitRange: Default/max requests per pod
- PriorityClass: Ensure critical pods get resources

**Cluster Autoscaling:**
- Scale down idle nodes to reduce costs
- Scale-to-zero for dev clusters during off-hours
- Use multiple node pools (spot + on-demand mix)
- Set max node limits to prevent overspend

**Cost Visibility:**
- Deploy Kubecost or OpenCost for namespace-level cost tracking
- Allocate costs by labels (team, project, environment)
- Track idle cost (cluster capacity not allocated to workloads)
- Generate showback/chargeback reports

For detailed Kubernetes cost optimization patterns, see `references/kubernetes-cost-optimization.md`.

## Cost Visibility and Monitoring

### Tagging for Cost Allocation

**Required Tags:**
- `Owner` or `Team` - Responsible team/department
- `Project` or `Application` - Business unit or application name
- `Environment` - prod, staging, dev, test
- `CostCenter` - Finance cost center code

**Enable Cost Allocation Tags:**
- **AWS:** Activate tags in Cost Allocation Tags console
- **Azure:** Apply tags via Azure Policy enforcement
- **GCP:** Use labels on all resources, export to BigQuery

For comprehensive tagging strategies, see `references/tagging-for-cost-allocation.md`.

### Monitoring and Dashboards

**Native Cloud Tools:**
- **AWS Cost Explorer:** Analyze spending patterns, forecast costs
- **Azure Cost Management + Billing:** Budget tracking, cost analysis
- **GCP Cloud Billing:** BigQuery export for custom analysis

**Third-Party Platforms:**
- **Kubecost:** Kubernetes cost visibility and optimization
- **CloudZero:** Unit cost economics, anomaly detection
- **CloudHealth:** Multi-cloud cost management
- **Infracost:** Terraform cost estimation in CI/CD

**Key Metrics to Track:**
- Total monthly cloud spend (trend over time)
- Cost per service/team/project (allocation accuracy)
- Unit cost metrics (cost per customer, cost per transaction)
- Reserved Instance/Savings Plan utilization (target >95%)
- Idle resource waste (target <5% of total spend)
- Budget variance (forecasted vs. actual)

### Budget Alerts and Anomaly Detection

**Cascading Budget Alerts:**
```
50% of budget  → Email to team lead (informational)
75% of budget  → Email + Slack to team (warning)
90% of budget  → Email + Slack + PagerDuty (urgent)
100% of budget → Automated shutdown (non-prod only) or escalation
```

**Anomaly Detection:** Alert on unexpected cost spikes
- >20% cost increase week-over-week
- >$500 unexpected daily cost spike
- New resource types (unusual spend patterns)

**Budget Granularity:**
- Organization-level (total cloud spend)
- Department-level (engineering, data, marketing)
- Project-level (per application/service)
- Environment-level (prod vs. dev/staging)

## Decision Frameworks

### Framework 1: Commitment Discount Decision Tree

```
Should we purchase Reserved Instances / Savings Plans?

STEP 1: Analyze Historical Usage (6-12 months)
├─ Identify steady-state baseline (minimum usage)
├─ Exclude spiky/seasonal workloads
└─ Calculate: (baseline usage) / (total usage) = commitment %

STEP 2: Choose Commitment Type
├─ RESERVED INSTANCES
│   ├─ Pros: Highest discount (up to 72%)
│   ├─ Cons: Instance type locked (unless convertible)
│   └─ Use for: Databases, stable production workloads
│
├─ SAVINGS PLANS
│   ├─ Pros: Flexible (across instance types, regions)
│   ├─ Cons: Slightly lower discount than RI
│   └─ Use for: Compute workloads, Lambda, Fargate
│
└─ COMMITTED USE DISCOUNTS (GCP)
    ├─ Resource-based: vCPU/memory commitments
    └─ Spend-based: Dollar amount commitments

STEP 3: Determine Commitment Period
├─ 1-year commitment
│   ├─ Lower discount (40-50%)
│   └─ Less risk if architecture changes
│
└─ 3-year commitment
    ├─ Higher discount (60-72%)
    └─ Only for mature, stable workloads

STEP 4: Monitor and Optimize
├─ Target >95% RI/Savings Plan utilization
├─ Sell unused RIs on AWS Reserved Instance Marketplace
└─ Adjust commitments quarterly based on usage trends
```

### Framework 2: Right-Sizing Priority Matrix

**Cost Impact vs. Effort:**

**High Impact, Low Effort (DO FIRST):**
- Idle resources (100% waste): Stopped instances, unattached volumes, old snapshots
- Unused NAT Gateways ($32/month each)
- Over-provisioned databases (<20% CPU for 30 days)
- Kubernetes pods with no resource requests set

**High Impact, Medium Effort (DO SECOND):**
- Over-provisioned compute (<40% CPU/memory for 30 days)
- Lambda functions with max memory >2x used memory
- Storage optimization (S3 Intelligent-Tiering, gp3 vs. gp2)

**Low Impact, High Effort (DO LAST):**
- Application code optimization (requires profiling, refactoring)
- Architecture redesign (serverless migration, multi-region optimization)

**Weekly Optimization Routine:**
1. Delete idle resources (automated script)
2. Review top 10 cost drivers (manual analysis)
3. Right-size 3-5 instances/week (incremental approach)
4. Monitor impact (cost trend over 4 weeks)

### Framework 3: Spot vs. On-Demand Decision

```
Should this workload use Spot/Preemptible instances?

├─ Is the workload fault-tolerant?
│   ├─ NO → Use On-Demand
│   └─ YES → Continue
│
├─ Is the workload stateless (or has checkpointing)?
│   ├─ NO → Use On-Demand (data loss risk)
│   └─ YES → Continue
│
├─ Can the workload handle interruptions gracefully?
│   ├─ NO → Use On-Demand
│   └─ YES → Continue
│
└─ Workload Type Assessment:
    ├─ Batch Jobs / CI/CD → ✅ Use Spot (70-90% savings)
    ├─ ML Training → ✅ Use Spot (with checkpointing)
    ├─ Kubernetes Workers → ✅ Use Spot (mixed with on-demand)
    ├─ Production API Servers → ⚠️ Mixed fleet (70% spot, 30% on-demand)
    ├─ Databases → ❌ Use On-Demand (or Reserved)
    └─ Real-time Services → ❌ Use On-Demand (or Reserved)
```

## Tool Selection Guide

### By Platform

| Platform | Cost Visibility | Right-Sizing | Automation |
|----------|----------------|--------------|------------|
| **AWS** | Cost Explorer, CUR | Compute Optimizer | AWS Budgets, Lambda cleanup |
| **Azure** | Cost Management | Azure Advisor | Azure Policy, Automation |
| **GCP** | Cloud Billing | Recommender | Budget Alerts, Cloud Functions |
| **Kubernetes** | Kubecost, OpenCost | VPA | Cluster Autoscaler |
| **Multi-Cloud** | CloudZero, CloudHealth | Densify | ParkMyCloud |

### By Use Case

| Use Case | Recommended Tool | Key Feature |
|----------|------------------|-------------|
| K8s cost visibility | Kubecost | Real-time namespace cost allocation |
| Terraform cost estimation | Infracost | PR comments with cost diffs |
| Multi-cloud aggregation | CloudHealth | Unified cost view across AWS/Azure/GCP |
| Automated optimization | nOps (AWS), CAST AI (K8s) | ML-based automation |
| Unit cost economics | CloudZero | Cost per customer/transaction tracking |
| Spot instance management | Spot.io | Automated spot orchestration |

For detailed tool comparisons and selection criteria, see `references/tools-comparison.md`.

## Cloud-Specific Tactics

### AWS Optimization Tactics

1. **Enable Cost & Usage Reports (CUR):** Export detailed billing to S3
2. **Use AWS Compute Optimizer:** ML-based EC2 rightsizing recommendations
3. **Implement Savings Plans:** More flexible than Reserved Instances
4. **S3 Intelligent-Tiering:** Automatic storage class optimization
5. **Lambda Right-Sizing:** Adjust memory allocation (CPU scales proportionally)
6. **EBS gp3 Migration:** 20% cheaper than gp2 with same performance

### Azure Optimization Tactics

1. **Enable Azure Advisor:** VM rightsizing and reserved instance recommendations
2. **Azure Hybrid Benefit:** Bring Windows Server licenses for discounts
3. **Dev/Test Pricing:** Reduced rates for non-production workloads
4. **Azure Spot VMs:** Up to 90% discount for interruptible workloads
5. **Storage Lifecycle Management:** Auto-tier blobs to cool/archive tiers

### GCP Optimization Tactics

1. **Export Billing to BigQuery:** Custom cost analysis with SQL
2. **Sustained Use Discounts:** Automatic 20-30% discount (no commitment)
3. **Committed Use Discounts:** 52-70% savings for 3-year commitments
4. **Preemptible VMs:** Up to 91% discount for batch workloads
5. **GCP Recommender:** Idle VM detection and rightsizing advice

For cloud-specific deep dives, see `references/cloud-specific-tactics.md`.

## Implementation Checklist

### Phase 1: Establish Visibility (Week 1-2)
- [ ] Enable cost allocation tags (Owner, Project, Environment)
- [ ] Activate cost allocation tags in cloud billing console
- [ ] Deploy Kubecost for Kubernetes cost visibility (if using K8s)
- [ ] Create cost dashboards (Grafana, CloudWatch, Azure Monitor, GCP)
- [ ] Set up weekly cost reports (emailed to team leads)

### Phase 2: Set Up Governance (Week 2-3)
- [ ] Create budget alerts (50%, 75%, 90%, 100% thresholds)
- [ ] Enable anomaly detection (>20% WoW increase)
- [ ] Implement tagging policy enforcement (Azure Policy, AWS Config, GCP Org Policy)
- [ ] Establish showback reports (cost by team/project)
- [ ] Document cost ownership (who owns which services)

### Phase 3: Quick Wins (Week 3-4)
- [ ] Delete idle resources (unattached volumes, old snapshots)
- [ ] Stop/terminate unused development instances
- [ ] Right-size top 10 over-provisioned instances (<40% utilization)
- [ ] Implement S3 Intelligent-Tiering or lifecycle policies
- [ ] Evaluate Reserved Instance/Savings Plan coverage

### Phase 4: Commitment Discounts (Month 2)
- [ ] Analyze 6-12 months usage history
- [ ] Calculate baseline usage for commitment sizing
- [ ] Purchase Reserved Instances for databases
- [ ] Purchase Savings Plans for compute workloads
- [ ] Monitor RI/SP utilization (target >95%)

### Phase 5: Automation (Month 2-3)
- [ ] Deploy automated cleanup scripts (weekly schedule)
- [ ] Integrate Infracost into CI/CD pipelines
- [ ] Implement auto-shutdown for dev/test environments (off-hours)
- [ ] Enable Vertical Pod Autoscaler (VPA) for K8s rightsizing
- [ ] Set up Spot instance automation (Spot.io, CAST AI, or native)

### Phase 6: Continuous Optimization (Ongoing)
- [ ] Weekly cost reviews with engineering teams
- [ ] Monthly optimization sprints (top cost drivers)
- [ ] Quarterly commitment adjustments (RI/SP coverage)
- [ ] Annual FinOps maturity assessment

## Common Pitfalls

### Pitfall 1: No Cost Visibility
❌ **Problem:** Finance team sees cloud bill at end of month, surprises everywhere
✅ **Solution:** Deploy real-time cost dashboards, daily Slack reports to engineering teams

### Pitfall 2: Reserved Instance Underutilization
❌ **Problem:** Purchased 100 RIs, only using 60 (40% wasted commitment)
✅ **Solution:** Monitor RI utilization weekly (target >95%), sell unused RIs on marketplace

### Pitfall 3: Missing Kubernetes Resource Requests
❌ **Problem:** Pods with no requests set → inefficient bin-packing → wasted nodes
✅ **Solution:** Use VPA to auto-generate recommendations, enforce via admission control

### Pitfall 4: Idle Resources Not Cleaned Up
❌ **Problem:** 50 stopped EC2 instances (still paying for EBS), 200 unattached volumes
✅ **Solution:** Weekly automated cleanup of idle resources >7 days old

### Pitfall 5: No Budget Alerts
❌ **Problem:** Accidentally left test cluster running, $10K bill surprise
✅ **Solution:** Budget alerts at 50%, 75%, 90%, 100% with Slack/PagerDuty notifications

## Related Skills

- **resource-tagging:** Cost allocation tags enable showback/chargeback models
- **kubernetes-operations:** K8s rightsizing, VPA, cluster autoscaling for cost optimization
- **infrastructure-as-code:** Infracost for Terraform cost estimation and policy-as-code
- **aws-patterns:** AWS-specific cost optimization tactics (EC2, RDS, S3, Lambda)
- **gcp-patterns:** GCP-specific optimizations (Compute Engine, BigQuery, Cloud Storage)
- **azure-patterns:** Azure-specific optimizations (VMs, Storage, App Service, Functions)
- **platform-engineering:** Internal FinOps platforms and self-service cost dashboards
- **disaster-recovery:** Balance cost vs. RTO/RPO (warm standby vs. cold standby)

## Examples

See `examples/` directory for:
- **terraform/**: AWS, Azure, GCP cost optimization infrastructure (budgets, alerts)
- **kubernetes/**: Kubecost deployment, resource quotas, VPA configurations
- **ci-cd/**: Infracost GitHub Actions, cost approval workflows
- **dashboards/**: Grafana cost dashboards, CloudWatch alarms

## Scripts

See `scripts/` directory for:
- **cleanup_idle_resources.py:** Automated AWS/Azure/GCP idle resource cleanup
- **ri_coverage_report.py:** Reserved Instance coverage analysis
- **cost_allocation_report.py:** Generate showback/chargeback reports
- **spot_savings_calculator.py:** Estimate savings from spot instances
- **k8s_rightsizing_audit.py:** Find K8s pods with missing resource requests

## Key Takeaways

1. **FinOps is a Culture:** Collaboration between finance, engineering, and operations
2. **Visibility First:** Can't optimize what can't measure (tags + dashboards mandatory)
3. **Commitment = Savings:** Reserved Instances/Savings Plans provide 40-72% discounts
4. **Right-Size Continuously:** Target 60-80% utilization (leave headroom for spikes)
5. **Automate Cleanup:** Idle resources are 100% waste (weekly automated deletion)
6. **Kubernetes Costs Hidden:** Use Kubecost/OpenCost for namespace-level visibility
7. **Shift-Left Cost Awareness:** Infracost in CI/CD prevents surprise cost increases
8. **Budget Alerts Prevent Overspend:** Cascading notifications at 50%, 75%, 90%, 100%
9. **Spot for Fault-Tolerant Workloads:** 70-90% discount (CI/CD, batch jobs, ML training)
10. **Unit Cost Metrics Drive Value:** Track cost per customer, cost per transaction
