---
name: kafka-iac-deployment
description: Terraform deployment expert for Apache Kafka, AWS MSK, and Azure Event Hubs. Use when provisioning Kafka infrastructure with IaC, comparing managed vs self-hosted platforms, or automating cluster deployments.
---

# Kafka Infrastructure as Code (IaC) Deployment

Expert guidance for deploying Apache Kafka using Terraform across multiple platforms.

## When to Use This Skill

I activate when you need help with:
- **Terraform deployments**: "Deploy Kafka with Terraform", "provision Kafka cluster"
- **Platform selection**: "Should I use AWS MSK or self-hosted Kafka?", "compare Kafka platforms"
- **Infrastructure planning**: "How to size Kafka infrastructure", "Kafka on AWS vs Azure"
- **IaC automation**: "Automate Kafka deployment", "CI/CD for Kafka infrastructure"

## What I Know

### Available Terraform Modules

This plugin provides 3 production-ready Terraform modules:

#### 1. **Apache Kafka (Self-Hosted, KRaft Mode)**
- **Location**: `plugins/specweave-kafka/terraform/apache-kafka/`
- **Platform**: AWS EC2 (can adapt to other clouds)
- **Architecture**: KRaft mode (no ZooKeeper dependency)
- **Features**:
  - Multi-broker cluster (3-5 brokers recommended)
  - Security groups with SASL_SSL
  - IAM roles for S3 backups
  - CloudWatch metrics and alarms
  - Auto-scaling group support
  - Custom VPC and subnet configuration
- **Use When**:
  - ✅ You need full control over Kafka configuration
  - ✅ Running Kafka 3.6+ (KRaft mode)
  - ✅ Want to avoid ZooKeeper operational overhead
  - ✅ Multi-cloud or hybrid deployments
- **Variables**:
  ```hcl
  module "kafka" {
    source = "../../plugins/specweave-kafka/terraform/apache-kafka"

    environment         = "production"
    broker_count        = 3
    kafka_version       = "3.7.0"
    instance_type       = "m5.xlarge"
    vpc_id              = var.vpc_id
    subnet_ids          = var.subnet_ids
    domain              = "example.com"
    enable_s3_backups   = true
    enable_monitoring   = true
  }
  ```

#### 2. **AWS MSK (Managed Streaming for Kafka)**
- **Location**: `plugins/specweave-kafka/terraform/aws-msk/`
- **Platform**: AWS Managed Service
- **Features**:
  - Fully managed Kafka service
  - IAM authentication + SASL/SCRAM
  - Auto-scaling (provisioned throughput)
  - Built-in monitoring (CloudWatch)
  - Multi-AZ deployment
  - Encryption in transit and at rest
- **Use When**:
  - ✅ You want AWS to manage Kafka operations
  - ✅ Need tight AWS integration (IAM, KMS, CloudWatch)
  - ✅ Prefer operational simplicity over cost
  - ✅ Running in AWS VPC
- **Variables**:
  ```hcl
  module "msk" {
    source = "../../plugins/specweave-kafka/terraform/aws-msk"

    cluster_name           = "my-kafka-cluster"
    kafka_version          = "3.6.0"
    number_of_broker_nodes = 3
    broker_node_instance_type = "kafka.m5.large"

    vpc_id     = var.vpc_id
    subnet_ids = var.private_subnet_ids

    enable_iam_auth      = true
    enable_scram_auth    = false
    enable_auto_scaling  = true
  }
  ```

#### 3. **Azure Event Hubs (Kafka API)**
- **Location**: `plugins/specweave-kafka/terraform/azure-event-hubs/`
- **Platform**: Azure Managed Service
- **Features**:
  - Kafka 1.0+ protocol support
  - Auto-inflate (elastic scaling)
  - Premium SKU for high throughput
  - Zone redundancy
  - Private endpoints (VNet integration)
  - Event capture to Azure Storage
- **Use When**:
  - ✅ Running on Azure cloud
  - ✅ Need Kafka-compatible API without Kafka operations
  - ✅ Want serverless scaling (auto-inflate)
  - ✅ Integrating with Azure ecosystem
- **Variables**:
  ```hcl
  module "event_hubs" {
    source = "../../plugins/specweave-kafka/terraform/azure-event-hubs"

    namespace_name        = "my-event-hub-ns"
    resource_group_name   = var.resource_group_name
    location              = "eastus"

    sku                   = "Premium"
    capacity              = 1
    kafka_enabled         = true
    auto_inflate_enabled  = true
    maximum_throughput_units = 20
  }
  ```

## Platform Selection Decision Tree

```
Need Kafka deployment? START HERE:

├─ Running on AWS?
│  ├─ YES → Want managed service?
│  │  ├─ YES → Use AWS MSK module (terraform/aws-msk)
│  │  └─ NO → Use Apache Kafka module (terraform/apache-kafka)
│  └─ NO → Continue...
│
├─ Running on Azure?
│  ├─ YES → Use Azure Event Hubs module (terraform/azure-event-hubs)
│  └─ NO → Continue...
│
├─ Multi-cloud or hybrid?
│  └─ YES → Use Apache Kafka module (most portable)
│
├─ Need maximum control?
│  └─ YES → Use Apache Kafka module
│
└─ Default → Use Apache Kafka module (self-hosted, KRaft mode)
```

## Deployment Workflows

### Workflow 1: Deploy Self-Hosted Kafka (Apache Kafka Module)

**Scenario**: You want full control over Kafka on AWS EC2

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "kafka_cluster" {
  source = "../../plugins/specweave-kafka/terraform/apache-kafka"

  environment         = "production"
  broker_count        = 3
  kafka_version       = "3.7.0"
  instance_type       = "m5.xlarge"

  vpc_id     = "vpc-12345678"
  subnet_ids = ["subnet-abc", "subnet-def", "subnet-ghi"]
  domain     = "kafka.example.com"

  enable_s3_backups = true
  enable_monitoring = true

  tags = {
    Project     = "MyApp"
    Environment = "Production"
  }
}

output "broker_endpoints" {
  value = module.kafka_cluster.broker_endpoints
}
EOF

# 2. Initialize Terraform
terraform init

# 3. Plan deployment (review what will be created)
terraform plan

# 4. Apply (create infrastructure)
terraform apply

# 5. Get broker endpoints
terraform output broker_endpoints
# Output: ["kafka-0.kafka.example.com:9093", "kafka-1.kafka.example.com:9093", ...]
```

### Workflow 2: Deploy AWS MSK (Managed Service)

**Scenario**: You want AWS to manage Kafka operations

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "msk_cluster" {
  source = "../../plugins/specweave-kafka/terraform/aws-msk"

  cluster_name           = "my-msk-cluster"
  kafka_version          = "3.6.0"
  number_of_broker_nodes = 3
  broker_node_instance_type = "kafka.m5.large"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_iam_auth     = true
  enable_auto_scaling = true

  tags = {
    Project = "MyApp"
  }
}

output "bootstrap_brokers" {
  value = module.msk_cluster.bootstrap_brokers_sasl_iam
}
EOF

# 2. Deploy
terraform init && terraform apply

# 3. Configure IAM authentication
# (module outputs IAM policy, attach to your application role)
```

### Workflow 3: Deploy Azure Event Hubs (Kafka API)

**Scenario**: You're on Azure and want Kafka-compatible API

```bash
# 1. Create Terraform configuration
cat > main.tf <<EOF
module "event_hubs" {
  source = "../../plugins/specweave-kafka/terraform/azure-event-hubs"

  namespace_name      = "my-kafka-namespace"
  resource_group_name = "my-resource-group"
  location            = "eastus"

  sku                  = "Premium"
  capacity             = 1
  kafka_enabled        = true
  auto_inflate_enabled = true
  maximum_throughput_units = 20

  # Create hubs (topics) for your use case
  hubs = [
    { name = "user-events",    partitions = 12 },
    { name = "order-events",   partitions = 6 },
    { name = "payment-events", partitions = 3 }
  ]
}

output "connection_string" {
  value = module.event_hubs.connection_string
  sensitive = true
}
EOF

# 2. Deploy
terraform init && terraform apply

# 3. Get connection details
terraform output connection_string
```

## Infrastructure Sizing Recommendations

### Small Environment (Dev/Test)
```hcl
# Self-hosted: 1 broker, m5.large
broker_count  = 1
instance_type = "m5.large"

# AWS MSK: 1 broker per AZ, kafka.m5.large
number_of_broker_nodes = 3
broker_node_instance_type = "kafka.m5.large"

# Azure Event Hubs: Basic SKU
sku = "Basic"
capacity = 1
```

### Medium Environment (Staging/Production)
```hcl
# Self-hosted: 3 brokers, m5.xlarge
broker_count  = 3
instance_type = "m5.xlarge"

# AWS MSK: 3 brokers, kafka.m5.xlarge
number_of_broker_nodes = 3
broker_node_instance_type = "kafka.m5.xlarge"

# Azure Event Hubs: Standard SKU with auto-inflate
sku = "Standard"
capacity = 2
auto_inflate_enabled = true
maximum_throughput_units = 10
```

### Large Environment (High-Throughput Production)
```hcl
# Self-hosted: 5+ brokers, m5.2xlarge or m5.4xlarge
broker_count  = 5
instance_type = "m5.2xlarge"

# AWS MSK: 6+ brokers, kafka.m5.2xlarge, auto-scaling
number_of_broker_nodes = 6
broker_node_instance_type = "kafka.m5.2xlarge"
enable_auto_scaling = true

# Azure Event Hubs: Premium SKU with zone redundancy
sku = "Premium"
capacity = 4
zone_redundant = true
maximum_throughput_units = 20
```

## Best Practices

### Security Best Practices
1. **Always use encryption in transit**
   - Self-hosted: Enable SASL_SSL listener
   - AWS MSK: Set `encryption_in_transit_client_broker = "TLS"`
   - Azure Event Hubs: HTTPS/TLS enabled by default

2. **Use IAM authentication (when possible)**
   - AWS MSK: `enable_iam_auth = true`
   - Azure Event Hubs: Managed identities

3. **Network isolation**
   - Deploy in private subnets
   - Use security groups/NSGs restrictively
   - Azure: Enable private endpoints for Premium SKU

### High Availability Best Practices
1. **Multi-AZ deployment**
   - Self-hosted: Distribute brokers across 3+ AZs
   - AWS MSK: Automatically multi-AZ
   - Azure Event Hubs: Enable `zone_redundant = true` (Premium)

2. **Replication factor = 3**
   - Self-hosted: `default.replication.factor=3`
   - AWS MSK: Configured automatically
   - Azure Event Hubs: N/A (fully managed)

3. **min.insync.replicas = 2**
   - Ensures durability even if 1 broker fails

### Cost Optimization
1. **Right-size instances**
   - Use ClusterSizingCalculator utility (in kafka-architecture skill)
   - Start small, scale up based on metrics

2. **Auto-scaling (where available)**
   - AWS MSK: `enable_auto_scaling = true`
   - Azure Event Hubs: `auto_inflate_enabled = true`

3. **Retention policies**
   - Set `log.retention.hours` based on actual needs (default: 168 hours = 7 days)
   - Shorter retention = lower storage costs

## Monitoring Integration

All modules integrate with monitoring:

### Self-Hosted Kafka
- CloudWatch metrics (via JMX Exporter)
- Prometheus + Grafana dashboards (see kafka-observability skill)
- Custom CloudWatch alarms

### AWS MSK
- Built-in CloudWatch metrics
- Enhanced monitoring available
- Integration with CloudWatch Alarms

### Azure Event Hubs
- Built-in Azure Monitor metrics
- Diagnostic logs to Log Analytics
- Integration with Azure Alerts

## Troubleshooting

### "Terraform destroy fails on security groups"
**Cause**: Resources using security groups still exist
**Fix**:
```bash
# 1. Find dependent resources
aws ec2 describe-network-interfaces --filters "Name=group-id,Values=sg-12345678"

# 2. Delete dependent resources first
# 3. Retry terraform destroy
```

### "AWS MSK cluster takes 20+ minutes to create"
**Cause**: MSK provisioning is inherently slow (AWS behavior)
**Fix**: This is normal. Use `--auto-approve` for automation:
```bash
terraform apply -auto-approve
```

### "Azure Event Hubs: Connection refused"
**Cause**: Kafka protocol not enabled OR incorrect connection string
**Fix**:
1. Verify `kafka_enabled = true` in Terraform
2. Use Kafka connection string (not Event Hubs connection string)
3. Check firewall rules (Premium SKU supports private endpoints)

## Integration with Other Skills

- **kafka-architecture**: For cluster sizing and partitioning strategy
- **kafka-observability**: For Prometheus + Grafana setup after deployment
- **kafka-kubernetes**: For deploying Kafka on Kubernetes (alternative to Terraform)
- **kafka-cli-tools**: For testing deployed clusters with kcat

## Quick Reference Commands

```bash
# Terraform workflow
terraform init          # Initialize modules
terraform plan          # Preview changes
terraform apply         # Create infrastructure
terraform output        # Get outputs (endpoints, etc.)
terraform destroy       # Delete infrastructure

# AWS MSK specific
aws kafka list-clusters # List MSK clusters
aws kafka describe-cluster --cluster-arn <arn> # Get cluster details

# Azure Event Hubs specific
az eventhubs namespace list # List namespaces
az eventhubs eventhub list --namespace-name <name> --resource-group <rg> # List hubs
```

---

**Next Steps After Deployment**:
1. Use **kafka-observability** skill to set up Prometheus + Grafana monitoring
2. Use **kafka-cli-tools** skill to test cluster with kcat
3. Deploy your producer/consumer applications
4. Monitor cluster health and performance
