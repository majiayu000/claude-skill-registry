---
name: gcp-architecture
description: "Google Cloud Platform architecture patterns and best practices. Use when designing, deploying, or reviewing GCP infrastructure including GKE, Cloud Run, Cloud Functions, BigQuery, and IAM."
---

# Google Cloud Platform Architecture

Comprehensive guide for building secure, scalable infrastructure on Google Cloud Platform.

## When to Use

- Designing GCP architecture for new projects
- Deploying applications to GCP services
- Setting up networking (VPC, firewall rules)
- Configuring IAM policies and service accounts
- Working with GKE (Google Kubernetes Engine)
- Optimizing costs and performance

## Core Services Overview

### Compute

| Service | Use Case | Key Features |
|---------|----------|--------------|
| Compute Engine | Virtual machines | Full control, custom images |
| GKE | Managed Kubernetes | Autopilot mode, node auto-provisioning |
| Cloud Run | Serverless containers | Scale to zero, any container |
| Cloud Functions | Serverless functions | Event-driven, 2nd gen |
| App Engine | PaaS | Standard/Flexible environments |

### Storage

| Service | Use Case | Key Features |
|---------|----------|--------------|
| Cloud Storage | Object storage | Multi-regional, lifecycle |
| Persistent Disk | Block storage (GCE) | SSD/HDD, snapshots |
| Filestore | Managed NFS | High performance |
| Cloud SQL | Managed SQL | MySQL, PostgreSQL, SQL Server |
| Firestore | NoSQL document | Serverless, realtime |
| BigQuery | Data warehouse | Serverless, petabyte-scale |
| Cloud Spanner | Global SQL | Horizontal scaling |
| Memorystore | Managed Redis | In-memory cache |

### Networking

| Service | Use Case | Key Features |
|---------|----------|--------------|
| VPC | Virtual network | Global, shared VPC |
| Cloud Load Balancing | Global LB | Layer 4/7, anycast IPs |
| Cloud CDN | Content delivery | Edge caching |
| Cloud DNS | DNS management | 100% SLA |
| Cloud NAT | Outbound NAT | No external IPs needed |

## VPC Architecture

### Shared VPC Pattern

```
┌──────────────────────────────────────────────────────────────────┐
│ Host Project (Shared VPC)                                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ VPC Network: shared-vpc                                    │  │
│  │                                                            │  │
│  │  ┌─────────────────────┐    ┌─────────────────────┐       │  │
│  │  │ Subnet: prod-app    │    │ Subnet: prod-data   │       │  │
│  │  │ 10.0.0.0/20         │    │ 10.0.16.0/20        │       │  │
│  │  │ us-central1         │    │ us-central1         │       │  │
│  │  └─────────────────────┘    └─────────────────────┘       │  │
│  │                                                            │  │
│  │  ┌─────────────────────┐    ┌─────────────────────┐       │  │
│  │  │ Subnet: staging-app │    │ Subnet: staging-data│       │  │
│  │  │ 10.1.0.0/20         │    │ 10.1.16.0/20        │       │  │
│  │  │ us-central1         │    │ us-central1         │       │  │
│  │  └─────────────────────┘    └─────────────────────┘       │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│ Service Project A   │      │ Service Project B   │
│ (Production)        │      │ (Staging)           │
│                     │      │                     │
│ GKE, Cloud Run      │      │ GKE, Cloud Run      │
│ Cloud SQL           │      │ Cloud SQL           │
└─────────────────────┘      └─────────────────────┘
```

### Terraform VPC

```hcl
# VPC Network
resource "google_compute_network" "main" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

# Subnets
resource "google_compute_subnetwork" "app" {
  name          = "${var.project_id}-app-subnet"
  ip_cidr_range = "10.0.0.0/20"
  region        = var.region
  network       = google_compute_network.main.id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.100.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.200.0.0/20"
  }

  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud NAT
resource "google_compute_router" "main" {
  name    = "${var.project_id}-router"
  region  = var.region
  network = google_compute_network.main.id
}

resource "google_compute_router_nat" "main" {
  name                               = "${var.project_id}-nat"
  router                             = google_compute_router.main.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# Firewall Rules
resource "google_compute_firewall" "allow_internal" {
  name    = "${var.project_id}-allow-internal"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
  }
  allow {
    protocol = "udp"
  }
  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/8"]
}

resource "google_compute_firewall" "allow_health_checks" {
  name    = "${var.project_id}-allow-health-checks"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
  }

  source_ranges = [
    "35.191.0.0/16",   # GCP Health Checks
    "130.211.0.0/22",  # GCP Health Checks
  ]

  target_tags = ["allow-health-checks"]
}
```

## IAM & Service Accounts

### Service Account Best Practices

```hcl
# Application Service Account
resource "google_service_account" "app" {
  account_id   = "${var.project_id}-app-sa"
  display_name = "Application Service Account"
}

# Workload Identity for GKE
resource "google_service_account_iam_binding" "workload_identity" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[${var.namespace}/${var.k8s_service_account}]"
  ]
}

# Grant specific permissions
resource "google_project_iam_member" "app_storage" {
  project = var.project_id
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_service_account.app.email}"

  condition {
    title      = "Only app bucket"
    expression = "resource.name.startsWith('projects/_/buckets/${var.project_id}-app-data')"
  }
}

resource "google_project_iam_member" "app_secretmanager" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.app.email}"
}

resource "google_project_iam_member" "app_cloudsql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

### Custom IAM Role

```hcl
resource "google_project_iam_custom_role" "app_deployer" {
  role_id     = "appDeployer"
  title       = "Application Deployer"
  description = "Can deploy applications to Cloud Run and GKE"

  permissions = [
    "run.services.create",
    "run.services.update",
    "run.services.delete",
    "run.services.get",
    "container.deployments.create",
    "container.deployments.update",
    "container.services.create",
    "container.services.update",
  ]
}
```

## GKE (Google Kubernetes Engine)

### GKE Autopilot Cluster

```hcl
resource "google_container_cluster" "main" {
  name     = "${var.project_id}-gke"
  location = var.region

  # Autopilot mode
  enable_autopilot = true

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.app.name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.authorized_network
      display_name = "Authorized Network"
    }
  }

  release_channel {
    channel = "REGULAR"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Security
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  deletion_protection = var.environment == "prod"
}
```

### GKE Standard Cluster

```hcl
resource "google_container_cluster" "standard" {
  name     = "${var.project_id}-gke-standard"
  location = var.region

  # Remove default node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.app.name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
  }
}

resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  cluster    = google_container_cluster.standard.name
  location   = var.region

  node_count = var.environment == "prod" ? 3 : 1

  autoscaling {
    min_node_count = var.environment == "prod" ? 3 : 1
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    service_account = google_service_account.gke_nodes.email

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    labels = {
      environment = var.environment
    }

    tags = ["gke-node", var.environment]
  }
}
```

## Cloud Run

### Cloud Run Service

```hcl
resource "google_cloud_run_v2_service" "app" {
  name     = "${var.project_id}-app"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = google_service_account.app.email

    scaling {
      min_instance_count = var.environment == "prod" ? 1 : 0
      max_instance_count = 100
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/app/myapp:${var.image_tag}"

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
        }
        cpu_idle = true  # Scale to zero
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_url.secret_id
            version = "latest"
          }
        }
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 10
        period_seconds        = 3
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    vpc_access {
      network_interfaces {
        network    = google_compute_network.main.name
        subnetwork = google_compute_subnetwork.app.name
      }
      egress = "PRIVATE_RANGES_ONLY"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# IAM - Allow unauthenticated (public API)
resource "google_cloud_run_v2_service_iam_member" "public" {
  count    = var.public_access ? 1 : 0
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Custom domain
resource "google_cloud_run_domain_mapping" "app" {
  location = var.region
  name     = var.domain

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_v2_service.app.name
  }
}
```

## Cloud SQL

### PostgreSQL Instance

```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project_id}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier              = var.environment == "prod" ? "db-custom-4-16384" : "db-f1-micro"
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_size         = 100
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = var.environment == "prod"
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = var.environment == "prod" ? 30 : 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
    database_flags {
      name  = "log_connections"
      value = "on"
    }
    database_flags {
      name  = "log_disconnections"
      value = "on"
    }

    maintenance_window {
      day          = 7  # Sunday
      hour         = 3
      update_track = "stable"
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }
  }

  deletion_protection = var.environment == "prod"
}

resource "google_sql_database" "main" {
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "app"
  instance = google_sql_database_instance.main.name
  password = random_password.db.result
}
```

## Cloud Storage

### Secure Bucket

```hcl
resource "google_storage_bucket" "data" {
  name          = "${var.project_id}-data"
  location      = var.region
  force_destroy = var.environment != "prod"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.storage.id
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }

  cors {
    origin          = ["https://${var.domain}"]
    method          = ["GET", "PUT", "POST"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  labels = local.common_labels
}

# Prevent public access
resource "google_storage_bucket_iam_binding" "prevent_public" {
  bucket = google_storage_bucket.data.name
  role   = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.app.email}",
  ]
}
```

## Cost Optimization

### Committed Use Discounts

| Commitment | Discount |
|------------|----------|
| 1-year CUD | 37% |
| 3-year CUD | 55% |
| Spot VMs | 60-91% |

### Budget Alerts

```hcl
resource "google_billing_budget" "main" {
  billing_account = var.billing_account_id
  display_name    = "${var.project_id} Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = var.monthly_budget
    }
  }

  threshold_rules {
    threshold_percent = 0.5
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.8
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    pubsub_topic = google_pubsub_topic.budget_alerts.id
  }
}
```

## CLI Reference

```bash
# Auth
gcloud auth login
gcloud auth application-default login
gcloud config set project PROJECT_ID

# Compute
gcloud compute instances list
gcloud compute instances start INSTANCE
gcloud compute ssh INSTANCE --zone ZONE

# GKE
gcloud container clusters get-credentials CLUSTER --region REGION
gcloud container clusters list

# Cloud Run
gcloud run services list
gcloud run deploy SERVICE --image IMAGE --region REGION
gcloud run services update-traffic SERVICE --to-latest

# Cloud SQL
gcloud sql instances list
gcloud sql connect INSTANCE --user USER

# Storage
gsutil ls gs://BUCKET/
gsutil cp FILE gs://BUCKET/
gsutil rsync -r ./folder gs://BUCKET/folder

# Secrets
gcloud secrets list
gcloud secrets versions access latest --secret SECRET_NAME

# Logs
gcloud logging read "resource.type=cloud_run_revision" --limit 100
```

## Security Checklist

- [ ] VPC Service Controls enabled
- [ ] Private Google Access enabled
- [ ] Cloud NAT for outbound traffic
- [ ] Workload Identity for GKE
- [ ] Binary Authorization enabled
- [ ] Cloud Armor for DDoS protection
- [ ] Secret Manager for credentials
- [ ] Cloud Audit Logs enabled
- [ ] Security Command Center enabled

## Integration

Works with:
- `/terraform` - GCP provider configuration
- `/k8s` - GKE deployments
- `/devops` - GCP deployment pipelines
- `/security` - GCP security review
