---
name: alibaba-cloud
description: Provides comprehensive Alibaba Cloud (Aliyun) guidance including ECS, ApsaraDB, OSS, SLB, VPC, RAM, ACK (Kubernetes), Function Compute, API Gateway, CDN, and monitoring services. Covers infrastructure provisioning with Terraform/ROS, cloud architecture design, security best practices, cost optimization, and migration strategies. Produces infrastructure code, deployment scripts, architecture diagrams, and operational procedures. Use when working with Alibaba Cloud services, designing cloud architecture on Aliyun, migrating to Alibaba Cloud, setting up Chinese cloud infrastructure, implementing multi-region deployments in China, or when users mention Alibaba Cloud, Aliyun, ECS, OSS, ApsaraDB, ACK, RDS, SLB, or Chinese cloud computing.
---

# Alibaba Cloud

## Core Capabilities

Provides expert guidance across Alibaba Cloud ecosystem:

1. **Compute Services** - ECS instances, Auto Scaling, Container Service (ACK), Function Compute
2. **Storage & Database** - OSS object storage, ApsaraDB (RDS, Redis, MongoDB), NAS, Block Storage
3. **Networking** - VPC, SLB (Server Load Balancer), VPN Gateway, CEN, NAT Gateway
4. **Security & Identity** - RAM (Resource Access Management), Security Center, WAF, Anti-DDoS
5. **Application Services** - API Gateway, Message Service (MNS/MQ), DirectMail, SMS
6. **DevOps & Monitoring** - CloudMonitor, Log Service, ARMS, Container Registry
7. **CDN & Edge** - Alibaba Cloud CDN, DCDN, Global Accelerator
8. **Data & Analytics** - DataWorks, MaxCompute, AnalyticDB, E-MapReduce

## Best Practices

## Architecture

- Deploy across multiple zones for high availability
- Use SLB for load balancing with health checks
- Implement Auto Scaling for dynamic capacity
- Configure CloudMonitor with actionable alerts

### Security

- Enable RAM with least privilege access control
- Use Security Groups and Network ACLs for filtering
- Enable encryption at rest and in transit
- Implement WAF and Anti-DDoS for protection
- Enable ActionTrail for audit logging

### Cost Optimization

- Use Reserved Instances for predictable workloads (up to 70% savings)
- Leverage Preemptible Instances for batch jobs
- Configure Auto Scaling to match demand
- Use OSS lifecycle policies for cold data
- Monitor with Cost Management dashboards

### Performance

- Choose appropriate instance families and sizes
- Implement Redis/Memcache for caching
- Use CDN for static content delivery
- Configure read replicas for databases
- Enable ESSD disks for high IOPS workloads

## Infrastructure as Code

### Terraform for Alibaba Cloud

```hcl
terraform {
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.200"
    }
  }
}

provider "alicloud" {
  region = "cn-hangzhou"
}

# VPC with multi-zone deployment
resource "alicloud_vpc" "main" {
  vpc_name   = "production-vpc"
  cidr_block = "10.0.0.0/16"
}

resource "alicloud_vswitch" "app" {
  vpc_id     = alicloud_vpc.main.id
  cidr_block = "10.0.1.0/24"
  zone_id    = "cn-hangzhou-h"
}

resource "alicloud_security_group" "app" {
  vpc_id = alicloud_vpc.main.id
  name   = "application-sg"
}

resource "alicloud_instance" "app" {
  instance_name              = "app-server"
  instance_type              = "ecs.g6.large"
  image_id                   = "ubuntu_20_04_x64"
  vswitch_id                 = alicloud_vswitch.app.id
  security_groups            = [alicloud_security_group.app.id]
  internet_max_bandwidth_out = 10
}
```

### ROS (Resource Orchestration Service)

```yaml
ROSTemplateFormatVersion: '2015-09-01'
Description: High availability web application
Parameters:
  InstanceType:
    Type: String
    Default: ecs.g6.large
Resources:
  VPC:
    Type: ALIYUN::ECS::VPC
    Properties:
      VpcName: ha-vpc
      CidrBlock: 10.0.0.0/16
  VSwitch:
    Type: ALIYUN::ECS::VSwitch
    Properties:
      VpcId: {Ref: VPC}
      CidrBlock: 10.0.1.0/24
      ZoneId: cn-hangzhou-h
  SLB:
    Type: ALIYUN::SLB::LoadBalancer
    Properties:
      LoadBalancerName: web-lb
      AddressType: internet
      VpcId: {Ref: VPC}
      VSwitchId: {Ref: VSwitch}
```

## China-Specific Considerations

### ICP Filing

- Required for websites hosted in mainland China
- Obtain before pointing domain to Alibaba Cloud
- Allow 20-30 business days for approval
- Different requirements for personal vs corporate

### Data Residency & Compliance

- Data localization laws require China region storage
- Use: cn-hangzhou, cn-shanghai, cn-beijing, cn-shenzhen
- Understand Cybersecurity Law and Data Security Law
- Cross-border transfer requires security assessment

### Network & Performance

- Great Wall Firewall impacts international connectivity
- Use China CDN for domestic users
- Use Global Accelerator for cross-border access
- Test from within China for accurate results

## Migration to Alibaba Cloud

### Assessment

1. Inventory infrastructure, applications, and dependencies
2. Analyze regulatory requirements (ICP, data residency)
3. Map services to Alibaba Cloud equivalents
4. Estimate costs with pricing calculator
5. Plan connectivity (VPN Gateway, Express Connect)

### Strategies

- **Rehost** - Lift and shift with minimal changes
- **Replatform** - Optimize with managed services (RDS, OSS, Redis)
- **Refactor** - Rebuild with cloud-native services (Function Compute, ACK)
- **Hybrid** - Partial migration with on-premises connectivity

### Execution

1. Set up account and configure RAM
2. Establish network connectivity
3. Create VPC, VSwitches, security groups
4. Migrate data to OSS/RDS
5. Deploy applications to ECS/ACK
6. Configure SLB and DNS
7. Set up CloudMonitor and Log Service
8. Test and execute cutover

See [cloud-migration.md](references/cloud-migration.md) for detailed procedures

## Reference Files

Load detailed documentation when needed:

- **Compute Services**: See [compute-services.md](references/compute-services.md) for ECS instance families, specifications, custom images, Auto Scaling configuration, and optimization techniques

- **Storage Solutions**: See [storage-solutions.md](references/storage-solutions.md) for OSS bucket policies, encryption, lifecycle rules, NAS setup, and storage optimization strategies

- **Database Services**: See [database-services.md](references/database-services.md) for ApsaraDB RDS, PolarDB, Redis, MongoDB configuration, tuning, backup, and high availability setup

- **Infrastructure as Code**: See [infrastructure-as-code.md](references/infrastructure-as-code.md) for Terraform modules, ROS templates, multi-environment patterns, and deployment automation

- **Cloud Migration**: See [cloud-migration.md](references/cloud-migration.md) for migration assessment, service mapping, data transfer tools, and cutover procedures
