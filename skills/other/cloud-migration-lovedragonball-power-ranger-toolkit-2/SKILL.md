---
name: cloud-migration
description: Cloud migration strategies for AWS, GCP, and Azure. Use for lift-and-shift, replatforming, and cloud-native architecture design.
---

# ☁️ Cloud Migration Skill

## Migration Strategies (6 Rs)

| Strategy | Description | Use When |
|----------|-------------|----------|
| Rehost | Lift-and-shift | Quick migration, no changes |
| Replatform | Minor optimizations | Need some cloud benefits |
| Repurchase | Switch to SaaS | Commercial alternative exists |
| Refactor | Full redesign | Need cloud-native features |
| Retire | Decommission | App no longer needed |
| Retain | Keep on-premises | Not ready to migrate |

---

## AWS Migration

### Common Services Mapping
| On-Premises | AWS Equivalent |
|-------------|----------------|
| Web Server | EC2, ECS, Lambda |
| Database | RDS, DynamoDB, Aurora |
| File Storage | S3, EFS |
| Load Balancer | ELB, ALB |
| DNS | Route 53 |
| CDN | CloudFront |

### Infrastructure as Code (Terraform)
```hcl
# AWS EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name = "web-server"
    Environment = "production"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "assets" {
  bucket = "my-app-assets"
}
```

---

## GCP Migration

### Services Mapping
| Concept | GCP Service |
|---------|-------------|
| Compute | Compute Engine, Cloud Run |
| Database | Cloud SQL, Firestore |
| Storage | Cloud Storage |
| Serverless | Cloud Functions |
| Kubernetes | GKE |

---

## Azure Migration

### Services Mapping
| Concept | Azure Service |
|---------|---------------|
| Compute | Virtual Machines, App Service |
| Database | Azure SQL, Cosmos DB |
| Storage | Blob Storage |
| Serverless | Azure Functions |
| Kubernetes | AKS |

---

## Migration Checklist

### Pre-Migration
- [ ] Inventory all applications
- [ ] Assess dependencies
- [ ] Choose migration strategy
- [ ] Estimate costs (TCO calculator)
- [ ] Plan network architecture
- [ ] Security compliance review

### During Migration
- [ ] Set up landing zone
- [ ] Configure networking (VPC, VPN)
- [ ] Migrate databases
- [ ] Migrate applications
- [ ] Update DNS records
- [ ] Test thoroughly

### Post-Migration
- [ ] Monitor performance
- [ ] Optimize costs
- [ ] Implement auto-scaling
- [ ] Set up backups
- [ ] Document architecture
