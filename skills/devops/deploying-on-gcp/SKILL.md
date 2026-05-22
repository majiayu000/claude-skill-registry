---
name: deploying-on-gcp
description: Implement applications using Google Cloud Platform (GCP) services. Use when building on GCP infrastructure, selecting compute/storage/database services, designing data analytics pipelines, implementing ML workflows, or architecting cloud-native applications with BigQuery, Cloud Run, GKE, Vertex AI, and other GCP services.
---

# GCP Patterns

Build applications and infrastructure using Google Cloud Platform services with appropriate service selection, architecture patterns, and best practices.

## Purpose

This skill provides decision frameworks and implementation patterns for Google Cloud Platform (GCP) services across compute, storage, databases, data analytics, machine learning, networking, and security. It guides service selection based on workload requirements and demonstrates production-ready patterns using Terraform, Python SDKs, and gcloud CLI.

## When to Use

Use this skill when:

- Selecting GCP compute services (Cloud Run, GKE, Cloud Functions, Compute Engine, App Engine)
- Choosing storage or database services (Cloud Storage, Cloud SQL, Spanner, Firestore, Bigtable, BigQuery)
- Designing data analytics pipelines (BigQuery, Pub/Sub, Dataflow, Dataproc, Composer)
- Implementing ML workflows (Vertex AI, AutoML, pre-trained APIs)
- Architecting network infrastructure (VPC, Load Balancing, CDN, Cloud Armor)
- Setting up IAM, security, and cost optimization
- Migrating from AWS or Azure to GCP
- Building multi-cloud or GCP-first architectures

## Core Concepts

### GCP Service Categories

**Compute Options:**
- **Cloud Run:** Serverless containers for stateless HTTP services (auto-scale to zero)
- **GKE (Google Kubernetes Engine):** Managed Kubernetes for complex orchestration
- **Cloud Functions:** Event-driven functions for simple processing
- **Compute Engine:** Virtual machines for full OS control
- **App Engine:** Platform-as-a-Service for web applications

**Storage & Databases:**
- **Cloud Storage:** Object storage with Standard/Nearline/Coldline/Archive tiers
- **Cloud SQL:** Managed PostgreSQL/MySQL/SQL Server (up to 96TB)
- **Cloud Spanner:** Global distributed SQL with 99.999% SLA
- **Firestore:** NoSQL document database with real-time sync
- **Bigtable:** Wide-column NoSQL for time-series and IoT (petabyte scale)
- **AlloyDB:** PostgreSQL-compatible with 4x performance improvement

**Data & Analytics:**
- **BigQuery:** Serverless data warehouse (petabyte-scale SQL analytics)
- **Pub/Sub:** Global messaging and event streaming
- **Dataflow:** Apache Beam for stream and batch processing
- **Dataproc:** Managed Spark and Hadoop clusters
- **Cloud Composer:** Managed Apache Airflow for workflows

**AI/ML Services:**
- **Vertex AI:** Unified ML platform (training, deployment, monitoring)
- **AutoML:** No-code ML for standard tasks
- **Pre-trained APIs:** Vision, Natural Language, Speech, Translation
- **TPUs:** Tensor Processing Units for large model training

### Decision Framework: Compute Service Selection

```
Need to run code in GCP?
├─ HTTP service?
│  ├─ YES → Stateless?
│  │  ├─ YES → Cloud Run (auto-scale to zero)
│  │  └─ NO → Need Kubernetes? → GKE | Compute Engine
│  └─ NO (Event-driven)
│     ├─ Simple function? → Cloud Functions
│     └─ Complex orchestration? → GKE | Cloud Run Jobs
```

**Selection Guide:**
- **First choice:** Cloud Run (unless state or Kubernetes required)
- **Need Kubernetes:** GKE Autopilot (managed) or Standard (full control)
- **Simple events:** Cloud Functions (60-min max execution)
- **Full control:** Compute Engine (VMs with custom configuration)

### Decision Framework: Database Selection

```
Choose database type:
├─ Relational (SQL)
│  ├─ Multi-region required? → Cloud Spanner
│  ├─ PostgreSQL + high performance? → AlloyDB
│  └─ Standard RDBMS → Cloud SQL (PostgreSQL/MySQL/SQL Server)
│
├─ Document (NoSQL)
│  ├─ Mobile/web with offline sync? → Firestore
│  └─ Flexible schema, no offline? → MongoDB Atlas (Marketplace)
│
├─ Key-Value
│  ├─ Time-series or IoT data? → Bigtable
│  └─ Caching layer? → Memorystore (Redis/Memcached)
│
└─ Analytics
   └─ Petabyte-scale SQL analytics → BigQuery
```

### Decision Framework: Storage Selection

```
Storage type needed?
├─ Objects/Files
│  ├─ Frequent access → Cloud Storage (Standard)
│  ├─ Monthly access → Cloud Storage (Nearline)
│  ├─ Quarterly access → Cloud Storage (Coldline)
│  └─ Yearly access → Cloud Storage (Archive)
│
├─ Block storage → Persistent Disk (SSD/Standard/Extreme)
└─ Shared filesystem → Filestore (NFS)
```

### GCP vs AWS vs Azure Service Mapping

| Category | GCP | AWS | Azure |
|----------|-----|-----|-------|
| **Serverless Containers** | Cloud Run | Fargate | Container Instances |
| **Kubernetes** | GKE | EKS | AKS |
| **Functions** | Cloud Functions | Lambda | Functions |
| **VMs** | Compute Engine | EC2 | Virtual Machines |
| **Object Storage** | Cloud Storage | S3 | Blob Storage |
| **SQL Database** | Cloud SQL | RDS | SQL Database |
| **NoSQL Document** | Firestore | DynamoDB | Cosmos DB |
| **Data Warehouse** | BigQuery | Redshift | Synapse |
| **Messaging** | Pub/Sub | SNS/SQS | Service Bus |
| **ML Platform** | Vertex AI | SageMaker | Machine Learning |

## Architecture Patterns

### Pattern 1: Serverless Web Application

**Use Case:** Stateless HTTP API with database and caching

**Architecture:**
```
Internet → Cloud Load Balancer → Cloud Run → Cloud SQL (PostgreSQL)
                                            → Memorystore (Redis)
                                            → Cloud Storage
```

**Key Services:**
- Cloud Run for API service (auto-scaling containers)
- Cloud SQL for transactional data
- Memorystore for caching
- Cloud Storage for file uploads

For detailed Terraform configuration, see `references/compute-services.md`.

### Pattern 2: Data Analytics Platform

**Use Case:** Real-time event processing and analytics

**Architecture:**
```
Data Sources → Pub/Sub → Dataflow → BigQuery → Looker/Tableau
                          ↓
                     Cloud Storage (staging)
```

**Key Services:**
- Pub/Sub for event ingestion (at-least-once delivery)
- Dataflow for stream processing (Apache Beam)
- BigQuery for analytics (partitioned tables, clustering)
- Cloud Storage for staging and backups

For BigQuery optimization patterns, see `references/data-analytics.md`.

### Pattern 3: ML Pipeline

**Use Case:** End-to-end machine learning workflow

**Architecture:**
```
Training Data (GCS) → Vertex AI Training → Model Registry → Vertex AI Endpoints
                                                              ↓
                                                         Predictions
```

**Key Services:**
- Vertex AI Workbench for notebook development
- Vertex AI Training for custom models (GPU/TPU support)
- Vertex AI Endpoints for model serving (auto-scaling)
- Vertex AI Pipelines for orchestration (Kubeflow)

For ML implementation examples, see `references/ml-ai-services.md`.

### Pattern 4: GKE Microservices Platform

**Use Case:** Complex orchestration with multiple services

**Architecture:**
```
Internet → Cloud Load Balancer → GKE Cluster
                                   ├─ Ingress Controller
                                   ├─ Service Mesh (optional)
                                   ├─ Microservice A
                                   ├─ Microservice B
                                   └─ Microservice C
```

**Key Features:**
- GKE Autopilot (fully managed nodes) or Standard (custom configuration)
- Workload Identity for secure GCP service access
- Private cluster with Private Google Access
- Config Connector for managing GCP resources via Kubernetes

For GKE setup and best practices, see `references/compute-services.md`.

## Best Practices

### Cost Optimization

**Compute:**
- Use Committed Use Discounts for predictable workloads (57% off)
- Use Spot VMs for fault-tolerant workloads (60-91% off)
- Cloud Run scales to zero when idle (no charges)
- GKE Autopilot charges only for pod resources, not nodes

**Storage:**
- Use appropriate Cloud Storage classes (Standard/Nearline/Coldline/Archive)
- Enable Object Lifecycle Management to transition cold data
- Archive backups with Coldline or Archive (99% cheaper than Standard)

**Data:**
- BigQuery: Use partitioned and clustered tables
- Query only needed columns (avoid `SELECT *`)
- Use BI Engine for caching (up to 10TB free)
- Consider flat-rate pricing for heavy BigQuery usage

For detailed cost strategies, see `references/cost-optimization.md`.

### Security Fundamentals

**IAM Best Practices:**
- Follow principle of least privilege
- Use service accounts, not user accounts for applications
- Enable Workload Identity for GKE workloads (no service account keys)
- Use Secret Manager for secrets, not environment variables

**Network Security:**
- Use Private Google Access (access GCP services without public IPs)
- Enable Cloud NAT for outbound internet from private instances
- Implement VPC Service Controls for data exfiltration protection
- Use Identity-Aware Proxy (IAP) for zero-trust access

**Data Security:**
- Enable encryption at rest (default) and in transit
- Use Customer-Managed Encryption Keys (CMEK) for sensitive data
- Implement VPC Service Controls perimeter for data protection
- Enable audit logging for all projects

For comprehensive security patterns, see `references/security-iam.md`.

### High Availability

**Multi-Region Strategy:**
- Cloud Storage: Use multi-region locations (US, EU, ASIA)
- Cloud SQL: Enable Regional HA (automatic failover)
- Cloud Spanner: Use multi-region configurations (99.999% SLA)
- Global Load Balancing: Route traffic to nearest healthy backend

**Backup and Disaster Recovery:**
- Cloud SQL: Enable automated backups and point-in-time recovery
- Persistent Disk: Schedule snapshot backups
- Cloud Storage: Enable versioning for critical data
- BigQuery: Use table snapshots for time travel

For networking and HA patterns, see `references/networking.md`.

## Quick Reference

### Common gcloud Commands

```bash
# Project management
gcloud projects list
gcloud config set project PROJECT_ID

# Cloud Run
gcloud run deploy SERVICE_NAME --image IMAGE_URL --region REGION
gcloud run services list

# GKE
gcloud container clusters create-auto CLUSTER_NAME --region REGION
gcloud container clusters get-credentials CLUSTER_NAME --region REGION

# Cloud Storage
gsutil mb gs://BUCKET_NAME
gsutil cp FILE gs://BUCKET_NAME/

# BigQuery
bq mk DATASET_NAME
bq query --use_legacy_sql=false 'SELECT * FROM dataset.table LIMIT 10'

# Cloud SQL
gcloud sql instances create INSTANCE_NAME --database-version=POSTGRES_15 --region=REGION
gcloud sql connect INSTANCE_NAME --user=postgres
```

For complete command reference, see `examples/gcloud/common-commands.sh`.

### Python SDK Quick Start

```python
# Cloud Storage
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('file.txt')
blob.upload_from_filename('local-file.txt')

# BigQuery
from google.cloud import bigquery
client = bigquery.Client()
query = "SELECT * FROM `project.dataset.table` LIMIT 10"
results = client.query(query).result()

# Pub/Sub
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project', 'topic-name')
future = publisher.publish(topic_path, b'message data')
```

For complete Python examples, see `examples/python/`.

### Terraform Quick Start

```hcl
# Provider configuration
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = "api-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project/api:latest"
      }
    }
  }
}
```

For complete Terraform examples, see `examples/terraform/`.

## Service Selection Cheatsheet

| Requirement | Recommended Service | Alternative |
|-------------|---------------------|-------------|
| Stateless HTTP API | Cloud Run | App Engine |
| Complex orchestration | GKE Autopilot | GKE Standard |
| Event processing | Cloud Functions | Cloud Run Jobs |
| Object storage | Cloud Storage | N/A |
| Relational database | Cloud SQL | AlloyDB, Spanner |
| NoSQL document | Firestore | MongoDB Atlas |
| Time-series data | Bigtable | N/A |
| Data warehouse | BigQuery | N/A |
| Message queue | Pub/Sub | N/A |
| Stream processing | Dataflow | Dataproc |
| Batch processing | Dataflow | Dataproc |
| ML training | Vertex AI | Custom on GKE |
| Caching | Memorystore Redis | N/A |

## Integration with Other Skills

**Related Skills:**

- **infrastructure-as-code:** Use Terraform to provision GCP resources (see `examples/terraform/`)
- **kubernetes-operations:** Deploy and manage applications on GKE
- **building-ci-pipelines:** Use Cloud Build for CI/CD to Cloud Run or GKE
- **secret-management:** Use Secret Manager for sensitive configuration
- **observability:** Use Cloud Monitoring and Cloud Logging for metrics and logs
- **data-architecture:** Design data lakes and warehouses using BigQuery and Cloud Storage
- **mlops-patterns:** Implement ML pipelines using Vertex AI
- **aws-patterns:** Compare AWS and GCP service equivalents for multi-cloud
- **azure-patterns:** Compare Azure and GCP service equivalents

## Progressive Disclosure

For detailed documentation:

- **Compute services:** See `references/compute-services.md` for Cloud Run, GKE, Cloud Functions, Compute Engine, and App Engine patterns
- **Storage & databases:** See `references/storage-databases.md` for detailed service selection and configuration
- **Data analytics:** See `references/data-analytics.md` for BigQuery, Pub/Sub, Dataflow, and Dataproc patterns
- **ML/AI services:** See `references/ml-ai-services.md` for Vertex AI, AutoML, and pre-trained API usage
- **Networking:** See `references/networking.md` for VPC, Load Balancing, CDN, and Cloud Armor patterns
- **Security & IAM:** See `references/security-iam.md` for IAM patterns, Workload Identity, and Secret Manager
- **Cost optimization:** See `references/cost-optimization.md` for detailed cost reduction strategies

For working examples:

- **Terraform configurations:** See `examples/terraform/` for infrastructure templates
- **Python SDK usage:** See `examples/python/` for client library examples
- **gcloud CLI commands:** See `examples/gcloud/common-commands.sh` for command reference

## Key Decisions Summary

**When choosing GCP:**
- Data analytics workloads (BigQuery is best-in-class)
- ML/AI applications (Vertex AI, TPUs, Google Research backing)
- Kubernetes-native applications (GKE invented by Kubernetes creators)
- Serverless containers (Cloud Run is mature and cost-effective)
- Real-time streaming (Pub/Sub + Dataflow)

**GCP's unique advantages:**
- BigQuery: Serverless, petabyte-scale, fastest data warehouse
- Cloud Run: Most mature serverless container platform
- GKE: Most advanced managed Kubernetes (Autopilot mode)
- Vertex AI: Unified ML platform (training, deployment, monitoring)
- Per-second billing and sustained use discounts (automatic cost savings)

**Multi-region recommendations:**
- Production workloads: Use multi-region for 99.95%+ SLA
- Cloud Storage: Multi-region for global access
- Cloud Spanner: Multi-region for global transactions
- Global Load Balancing: Route to nearest healthy backend
