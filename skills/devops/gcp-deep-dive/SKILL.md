---
description: GCP deep dive expert for GKE, Cloud Run, Cloud Functions, networking, IAM, and data services. Designs production-grade architectures using Terraform, gcloud CLI, and Google Cloud best practices. Generates infrastructure ONE COMPONENT AT A TIME.
allowed-tools: Read, Write, Edit, Bash
model: opus
context: fork
---

# GCP Deep Dive Expert

## Purpose

Design and implement production-grade Google Cloud infrastructure with deep expertise in GKE, Cloud Run, networking, IAM, and data services. Produces well-structured Terraform configurations and gcloud workflows following the Google Cloud Architecture Framework.

## When to Use

- Designing GKE clusters with Workload Identity
- Building serverless architectures with Cloud Run or Cloud Functions
- VPC design, Cloud Load Balancing, and Cloud CDN
- IAM policy engineering and organization policies
- Cloud SQL, Cloud Spanner, Firestore, BigQuery architectures
- Terraform GCP provider patterns
- Cloud Build CI/CD pipelines
- Cloud Monitoring, Logging, and Trace setup

## Triggers

GCP, Google Cloud, GKE, Cloud Run, Cloud Functions, BigQuery, Cloud SQL, Firestore, Cloud Spanner, Cloud Build, Artifact Registry, Cloud Armor, Cloud CDN

## Generation Rules

```
CHUNKING RULE: Generate ONE COMPONENT AT A TIME.
Do NOT produce a complete infrastructure in one response.

Order:
1. Networking (VPC, subnets, firewall rules)
2. IAM (service accounts, Workload Identity)
3. Compute (GKE, Cloud Run, Cloud Functions)
4. Data (Cloud SQL, Spanner, Firestore, BigQuery)
5. Load Balancing & CDN
6. CI/CD (Cloud Build, Artifact Registry, Cloud Deploy)
7. Observability (Monitoring, Logging, Trace)

Each chunk: explain decisions, show Terraform + gcloud equivalent, note costs.
```

## GKE (Google Kubernetes Engine)

### Cluster with Terraform

```hcl
# modules/gke/main.tf
resource "google_container_cluster" "primary" {
  name     = "gke-${var.project_name}-${var.environment}"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.vpc_id
  subnetwork = var.subnet_id

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = var.environment == "production"
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  master_authorized_networks_config {
    dynamic "cidr_blocks" {
      for_each = var.authorized_networks
      content {
        cidr_block   = cidr_blocks.value.cidr
        display_name = cidr_blocks.value.name
      }
    }
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  binary_authorization {
    evaluation_mode = var.environment == "production" ? "PROJECT_SINGLETON_POLICY_ENFORCE" : "DISABLED"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=TU,WE,TH"
    }
  }

  release_channel {
    channel = var.environment == "production" ? "REGULAR" : "RAPID"
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS", "DAEMONSET", "DEPLOYMENT", "STATEFULSET"]
    managed_prometheus { enabled = true }
  }

  addons_config {
    gce_persistent_disk_csi_driver_config { enabled = true }
    gcs_fuse_csi_driver_config            { enabled = true }
    dns_cache_config                       { enabled = true }
    http_load_balancing                    { disabled = false }
    horizontal_pod_autoscaling             { disabled = false }
  }

  cluster_autoscaling {
    autoscaling_profile = "OPTIMIZE_UTILIZATION"
  }
}

# General-purpose node pool
resource "google_container_node_pool" "general" {
  name     = "general"
  cluster  = google_container_cluster.primary.id
  location = var.region

  initial_node_count = var.environment == "production" ? 3 : 1
  autoscaling {
    min_node_count = var.environment == "production" ? 3 : 1
    max_node_count = 20
  }

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    workload_metadata_config { mode = "GKE_METADATA" }
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
    labels   = { workload-type = "general", environment = var.environment }
    metadata = { disable-legacy-endpoints = "true" }
  }

  management { auto_repair = true; auto_upgrade = true }
  upgrade_settings { max_surge = 1; max_unavailable = 0; strategy = "SURGE" }
}

# Spot node pool (cost optimization)
resource "google_container_node_pool" "spot" {
  name     = "spot"
  cluster  = google_container_cluster.primary.id
  location = var.region

  initial_node_count = 0
  autoscaling { min_node_count = 0; max_node_count = 30 }

  node_config {
    machine_type = "e2-standard-4"
    spot         = true
    disk_size_gb = 100
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    workload_metadata_config { mode = "GKE_METADATA" }
    labels = { workload-type = "spot" }
    taint {
      key = "cloud.google.com/gke-spot"; value = "true"; effect = "NO_SCHEDULE"
    }
  }
  management { auto_repair = true; auto_upgrade = true }
}
```

### GKE with gcloud CLI

```bash
# Autopilot cluster (recommended for most workloads)
gcloud container clusters create-auto "gke-myapp-production" \
  --region="us-central1" --project="my-project-id" \
  --network="vpc-myapp" --subnetwork="subnet-gke" \
  --cluster-secondary-range-name="pods" \
  --services-secondary-range-name="services" \
  --enable-private-nodes --master-ipv4-cidr="172.16.0.0/28" \
  --release-channel="regular" \
  --enable-master-authorized-networks --master-authorized-networks="10.0.0.0/8"

# Standard cluster (full node control)
gcloud container clusters create "gke-myapp-production" \
  --region="us-central1" --num-nodes=3 --machine-type="e2-standard-4" \
  --enable-autoscaling --min-nodes=3 --max-nodes=20 \
  --enable-ip-alias --network="vpc-myapp" --subnetwork="subnet-gke" \
  --workload-pool="my-project-id.svc.id.goog" \
  --enable-shielded-nodes --enable-private-nodes \
  --master-ipv4-cidr="172.16.0.0/28" --release-channel="regular"
```

### Workload Identity Federation (GKE)

```hcl
resource "google_service_account" "app_sa" {
  account_id   = "myapp-workload"
  display_name = "MyApp Workload Service Account"
}

resource "google_service_account_iam_binding" "workload_identity" {
  service_account_id = google_service_account.app_sa.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[production/myapp-sa]"
  ]
}

resource "google_project_iam_member" "app_storage" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}
```

```yaml
# Kubernetes ServiceAccount linked to GCP SA
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
  annotations:
    iam.gke.io/gcp-service-account: myapp-workload@my-project-id.iam.gserviceaccount.com
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: myapp-sa
      nodeSelector:
        iam.gke.io/gke-metadata-server-enabled: "true"
      containers:
        - name: myapp
          image: us-central1-docker.pkg.dev/my-project-id/myapp/api:latest
```

### GKE Standard vs Autopilot

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria             │ GKE Standard         │ GKE Autopilot        │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Node management      │ You manage           │ Google manages       │
│ Pricing              │ Pay for nodes        │ Pay for pods         │
│ GPU / TPU            │ Full support         │ Supported            │
│ DaemonSets           │ Full control         │ Restricted           │
│ Privileged pods      │ Allowed              │ Not allowed          │
│ Security posture     │ You harden           │ Pre-hardened         │
│ Scale to zero        │ Manual               │ Built-in             │
│ Best for             │ Complex workloads    │ Most workloads       │
└──────────────────────┴──────────────────────┴──────────────────────┘

RULE: Default → Autopilot. Use Standard for DaemonSets, privileged pods,
      custom node images, GPU/ML with specific node configs.
```

## Cloud Run

### Service Deployment with Terraform

```hcl
resource "google_cloud_run_v2_service" "api" {
  name     = "api-${var.environment}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = google_service_account.run_sa.email
    scaling {
      min_instance_count = var.environment == "production" ? 2 : 0
      max_instance_count = 100
    }
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repo}/api:${var.image_tag}"
      ports { container_port = 8080 }
      resources {
        limits            = { cpu = "2", memory = "1Gi" }
        cpu_idle          = var.environment != "production"
        startup_cpu_boost = true
      }
      env {
        name  = "DB_HOST"
        value = "/cloudsql/${google_sql_database_instance.main.connection_name}"
      }
      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }
      startup_probe {
        http_get { path = "/healthz" }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }
      liveness_probe {
        http_get { path = "/healthz" }
        period_seconds = 30
      }
    }
    vpc_access {
      network_interfaces { network = var.vpc_id; subnetwork = var.subnet_id }
      egress = "PRIVATE_RANGES_ONLY"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_member" "invoker" {
  name     = google_cloud_run_v2_service.api.name
  location = var.region
  role     = "roles/run.invoker"
  member   = var.public_api ? "allUsers" : "serviceAccount:${var.invoker_sa_email}"
}
```

### Cloud Run with gcloud

```bash
gcloud run deploy api-production \
  --image="us-central1-docker.pkg.dev/my-project/myapp/api:v1.2.3" \
  --region="us-central1" \
  --service-account="api-runner@my-project.iam.gserviceaccount.com" \
  --min-instances=2 --max-instances=100 --cpu=2 --memory=1Gi \
  --set-env-vars="ENV=production" --set-secrets="DB_PASS=db-password:latest" \
  --vpc-connector="projects/my-project/locations/us-central1/connectors/run-vpc" \
  --vpc-egress=private-ranges-only \
  --ingress=internal-and-cloud-load-balancing --no-allow-unauthenticated

# Traffic splitting (canary)
gcloud run services update-traffic api-production --region="us-central1" \
  --to-revisions="api-production-v2=10,api-production-v1=90"
```

## Cloud Functions (2nd Gen)

```hcl
resource "google_cloudfunctions2_function" "processor" {
  name     = "order-processor-${var.environment}"
  location = var.region

  build_config {
    runtime     = "nodejs22"
    entry_point = "processOrder"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_source.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    min_instance_count    = 0
    max_instance_count    = 100
    available_memory      = "512Mi"
    timeout_seconds       = 60
    service_account_email = google_service_account.fn_sa.email
    ingress_settings      = "ALLOW_INTERNAL_ONLY"

    environment_variables = { PROJECT_ID = var.project_id }

    secret_environment_variables {
      key     = "API_KEY"
      secret  = google_secret_manager_secret.api_key.secret_id
      version = "latest"
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.orders.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}
```

## Networking

### VPC Design with Terraform

```hcl
resource "google_compute_network" "vpc" {
  name                    = "vpc-${var.project_name}-${var.environment}"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

# Primary subnet with secondary ranges for GKE
resource "google_compute_subnetwork" "gke" {
  name          = "subnet-gke-${var.environment}"
  ip_cidr_range = "10.0.0.0/20"
  region        = var.region
  network       = google_compute_network.vpc.id

  secondary_ip_range { range_name = "pods";     ip_cidr_range = "10.4.0.0/14" }
  secondary_ip_range { range_name = "services"; ip_cidr_range = "10.8.0.0/20" }

  private_ip_google_access = true
  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Serverless and data subnets
resource "google_compute_subnetwork" "serverless" {
  name = "subnet-serverless-${var.environment}"
  ip_cidr_range = "10.1.0.0/24"; region = var.region
  network = google_compute_network.vpc.id
  private_ip_google_access = true
}

resource "google_compute_subnetwork" "data" {
  name = "subnet-data-${var.environment}"
  ip_cidr_range = "10.2.0.0/24"; region = var.region
  network = google_compute_network.vpc.id
  private_ip_google_access = true
}

# Cloud NAT
resource "google_compute_router" "router" {
  name = "router-${var.environment}"; region = var.region
  network = google_compute_network.vpc.id
}

resource "google_compute_router_nat" "nat" {
  name   = "nat-${var.environment}"
  router = google_compute_router.router.name
  region = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  log_config { enable = true; filter = "ERRORS_ONLY" }
}

# Private Service Access (Cloud SQL, Memorystore, etc.)
resource "google_compute_global_address" "private_services" {
  name = "private-services-${var.environment}"
  purpose = "VPC_PEERING"; address_type = "INTERNAL"; prefix_length = 20
  network = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_services.name]
}
```

### Firewall Rules

```hcl
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal-${var.environment}"
  network = google_compute_network.vpc.id
  allow { protocol = "tcp"; ports = ["0-65535"] }
  allow { protocol = "udp"; ports = ["0-65535"] }
  allow { protocol = "icmp" }
  source_ranges = ["10.0.0.0/8"]
}

resource "google_compute_firewall" "allow_health_checks" {
  name    = "allow-health-checks-${var.environment}"
  network = google_compute_network.vpc.id
  allow { protocol = "tcp"; ports = ["80", "443", "8080"] }
  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]  # GCP health check ranges
  target_tags   = ["allow-health-check"]
}
```

### Cloud Load Balancing (External HTTPS with CDN)

```hcl
resource "google_compute_global_address" "lb_ip" { name = "lb-ip-${var.environment}" }

resource "google_compute_managed_ssl_certificate" "cert" {
  name = "cert-${var.environment}"
  managed { domains = [var.domain] }
}

resource "google_compute_backend_service" "api" {
  name                  = "backend-api-${var.environment}"
  protocol              = "HTTPS"
  timeout_sec           = 30
  load_balancing_scheme = "EXTERNAL_MANAGED"
  health_checks         = [google_compute_health_check.api.id]
  backend { group = google_compute_region_network_endpoint_group.run_neg.id }

  enable_cdn = true
  cdn_policy {
    cache_mode  = "CACHE_ALL_STATIC"
    default_ttl = 3600
    max_ttl     = 86400
  }

  security_policy = google_compute_security_policy.armor.id
  log_config { enable = true; sample_rate = 1.0 }
}

resource "google_compute_url_map" "lb" {
  name            = "lb-${var.environment}"
  default_service = google_compute_backend_service.api.id
}

resource "google_compute_target_https_proxy" "lb" {
  name             = "lb-proxy-${var.environment}"
  url_map          = google_compute_url_map.lb.id
  ssl_certificates = [google_compute_managed_ssl_certificate.cert.id]
}

resource "google_compute_global_forwarding_rule" "lb" {
  name       = "lb-rule-${var.environment}"
  target     = google_compute_target_https_proxy.lb.id
  port_range = "443"
  ip_address = google_compute_global_address.lb_ip.id
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

# Serverless NEG for Cloud Run
resource "google_compute_region_network_endpoint_group" "run_neg" {
  name   = "neg-run-${var.environment}"
  region = var.region
  network_endpoint_type = "SERVERLESS"
  cloud_run { service = google_cloud_run_v2_service.api.name }
}
```

### Cloud Armor (WAF / DDoS)

```hcl
resource "google_compute_security_policy" "armor" {
  name = "armor-${var.environment}"

  rule {
    action = "allow"; priority = 2147483647
    match { versioned_expr = "SRC_IPS_V1"; config { src_ip_ranges = ["*"] } }
    description = "Default allow"
  }

  rule {
    action = "deny(403)"; priority = 1000
    match { versioned_expr = "SRC_IPS_V1"; config { src_ip_ranges = var.blocked_ip_ranges } }
    description = "Block known malicious IPs"
  }

  rule {
    action = "rate_based_ban"; priority = 2000
    match { versioned_expr = "SRC_IPS_V1"; config { src_ip_ranges = ["*"] } }
    rate_limit_options {
      conform_action = "allow"; exceed_action = "deny(429)"
      rate_limit_threshold { count = 100; interval_sec = 60 }
      ban_duration_sec = 300
    }
    description = "Rate limit: 100 req/min"
  }

  # OWASP CRS preconfigured rules
  rule {
    action = "deny(403)"; priority = 3000
    match { expr { expression = "evaluatePreconfiguredExpr('sqli-v33-stable')" } }
    description = "SQL injection protection"
  }

  rule {
    action = "deny(403)"; priority = 3100
    match { expr { expression = "evaluatePreconfiguredExpr('xss-v33-stable')" } }
    description = "XSS protection"
  }

  adaptive_protection_config {
    layer_7_ddos_defense_config { enable = var.environment == "production" }
  }
}
```

## Identity & Security

### IAM Best Practices

```hcl
# Principle: Grant roles to groups, not individuals.
# Principle: Use custom roles when predefined roles are too broad.

resource "google_project_iam_custom_role" "app_reader" {
  role_id     = "appDataReader"
  title       = "Application Data Reader"
  permissions = [
    "cloudsql.instances.connect", "cloudsql.instances.get",
    "storage.objects.get", "storage.objects.list",
    "secretmanager.versions.access",
  ]
}

# Conditional IAM binding (time-limited)
resource "google_project_iam_binding" "conditional" {
  project = var.project_id
  role    = "roles/cloudsql.admin"
  members = ["group:dba-team@company.com"]
  condition {
    title      = "weekday_only"
    expression = "request.time.getDayOfWeek('America/New_York') >= 1 && request.time.getDayOfWeek('America/New_York') <= 5"
  }
}
```

### Service Accounts with Least Privilege

```hcl
# Dedicated SA per workload (never use default compute SA)
resource "google_service_account" "api_sa" {
  account_id   = "api-${var.environment}"
  display_name = "API Service Account (${var.environment})"
}

resource "google_project_iam_member" "api_roles" {
  for_each = toset([
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/cloudtrace.agent",
  ])
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.api_sa.email}"
}

# Disable SA key creation (enforce Workload Identity)
resource "google_project_organization_policy" "disable_sa_keys" {
  project    = var.project_id
  constraint = "iam.disableServiceAccountKeyCreation"
  boolean_policy { enforced = true }
}
```

### Secret Manager

```hcl
resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password-${var.environment}"
  replication { auto {} }
  labels = { environment = var.environment, managed_by = "terraform" }
  rotation {
    rotation_period    = "7776000s" # 90 days
    next_rotation_time = timeadd(timestamp(), "24h")
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = var.db_password
}

resource "google_secret_manager_secret_iam_member" "accessor" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.api_sa.email}"
}
```

### Organization Policies

```hcl
resource "google_project_organization_policy" "no_external_ip" {
  project    = var.project_id
  constraint = "compute.vmExternalIpAccess"
  list_policy { deny { all = true } }
}

resource "google_project_organization_policy" "location_restriction" {
  project    = var.project_id
  constraint = "gcp.resourceLocations"
  list_policy { allow { values = ["in:us-locations"] } }
}

resource "google_project_organization_policy" "uniform_bucket" {
  project    = var.project_id
  constraint = "storage.uniformBucketLevelAccess"
  boolean_policy { enforced = true }
}
```

## Data Services

### Cloud SQL (PostgreSQL)

```hcl
resource "google_sql_database_instance" "main" {
  name                = "sql-${var.project_name}-${var.environment}"
  database_version    = "POSTGRES_16"
  region              = var.region
  deletion_protection = var.environment == "production"

  settings {
    tier              = var.environment == "production" ? "db-custom-4-16384" : "db-f1-micro"
    availability_type = var.environment == "production" ? "REGIONAL" : "ZONAL"
    disk_size = 100; disk_type = "PD_SSD"; disk_autoresize = true

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = var.environment == "production" ? 30 : 7
      }
    }

    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = var.vpc_id
      enable_private_path_for_google_cloud_services = true
    }

    database_flags { name = "log_checkpoints";            value = "on" }
    database_flags { name = "log_connections";             value = "on" }
    database_flags { name = "log_min_duration_statement";  value = "1000" }

    maintenance_window { day = 7; hour = 3; update_track = "stable" }

    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      record_application_tags = true
      record_client_address   = true
    }
  }

  depends_on = [google_service_networking_connection.private_vpc]
}
```

### Cloud Spanner

```hcl
resource "google_spanner_instance" "main" {
  name         = "spanner-${var.project_name}-${var.environment}"
  config       = "regional-${var.region}"
  display_name = "${var.project_name} ${var.environment}"

  autoscaling_config {
    autoscaling_limits {
      min_processing_units = var.environment == "production" ? 1000 : 100
      max_processing_units = var.environment == "production" ? 10000 : 1000
    }
    autoscaling_targets {
      high_priority_cpu_utilization_percent = 65
      storage_utilization_percent           = 90
    }
  }
}

resource "google_spanner_database" "app" {
  instance = google_spanner_instance.main.name
  name     = "app-db"
  ddl = [
    "CREATE TABLE Users (UserId STRING(36) NOT NULL, Email STRING(255) NOT NULL, CreatedAt TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true)) PRIMARY KEY (UserId)",
    "CREATE UNIQUE INDEX UsersByEmail ON Users(Email)",
  ]
  deletion_protection = var.environment == "production"
}
```

### Firestore

```hcl
resource "google_firestore_database" "main" {
  name        = "(default)"
  project     = var.project_id
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  concurrency_mode = "OPTIMISTIC"
  point_in_time_recovery_enablement = var.environment == "production" ? "POINT_IN_TIME_RECOVERY_ENABLED" : "POINT_IN_TIME_RECOVERY_DISABLED"
}

resource "google_firestore_index" "orders_by_user" {
  project    = var.project_id
  database   = google_firestore_database.main.name
  collection = "orders"
  fields { field_path = "userId";    order = "ASCENDING" }
  fields { field_path = "createdAt"; order = "DESCENDING" }
}
```

### BigQuery

```hcl
resource "google_bigquery_dataset" "analytics" {
  dataset_id  = "analytics_${var.environment}"
  location    = var.region
  labels      = { environment = var.environment }

  access { role = "OWNER"; special_group = "projectOwners" }
  access { role = "READER"; group_by_email = "analysts@company.com" }
}

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "events"
  time_partitioning { type = "DAY"; field = "event_timestamp" }
  clustering = ["event_name", "user_id"]
  schema = jsonencode([
    { name = "event_id",        type = "STRING",    mode = "REQUIRED" },
    { name = "event_name",      type = "STRING",    mode = "REQUIRED" },
    { name = "event_timestamp", type = "TIMESTAMP", mode = "REQUIRED" },
    { name = "user_id",         type = "STRING",    mode = "NULLABLE" },
    { name = "properties",      type = "JSON",      mode = "NULLABLE" },
  ])
}
```

### Cloud Storage Patterns

```hcl
resource "google_storage_bucket" "data_lake" {
  name     = "${var.project_id}-data-lake-${var.environment}"
  location = var.region
  force_destroy               = var.environment != "production"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning { enabled = var.environment == "production" }

  lifecycle_rule { condition { age = 30 };  action { type = "SetStorageClass"; storage_class = "NEARLINE" } }
  lifecycle_rule { condition { age = 90 };  action { type = "SetStorageClass"; storage_class = "COLDLINE" } }
  lifecycle_rule { condition { age = 365 }; action { type = "SetStorageClass"; storage_class = "ARCHIVE" } }

  encryption { default_kms_key_name = var.kms_key_id }
}
```

### Data Service Decision Framework

```
┌──────────────────┬───────────────┬───────────────┬───────────────────┐
│ Need             │ Service       │ Strengths     │ Limits            │
├──────────────────┼───────────────┼───────────────┼───────────────────┤
│ Relational OLTP  │ Cloud SQL     │ Managed PG/MY │ Single region     │
│ Global relational│ Cloud Spanner │ Strong consis.│ Cost (min ~$65/mo)│
│ Document / mobile│ Firestore     │ Realtime sync │ 1 write/sec/doc   │
│ Analytics / OLAP │ BigQuery      │ Serverless    │ Not for OLTP      │
│ Key-value cache  │ Memorystore   │ Redis compat. │ No persistence opt│
│ Wide-column      │ Bigtable      │ Low latency   │ No SQL, no joins  │
│ Object storage   │ Cloud Storage │ Unlimited     │ Eventual consist. │
└──────────────────┴───────────────┴───────────────┴───────────────────┘

GUIDANCE:
- Default OLTP -> Cloud SQL (PostgreSQL)
- Need global consistency -> Cloud Spanner
- Mobile/web realtime -> Firestore
- Analytics warehouse -> BigQuery
- High-throughput time-series -> Bigtable
```

## Infrastructure as Code

### Terraform GCP Provider Setup

```hcl
terraform {
  required_version = ">= 1.7"
  required_providers {
    google      = { source = "hashicorp/google";      version = "~> 6.0" }
    google-beta = { source = "hashicorp/google-beta"; version = "~> 6.0" }
  }
  backend "gcs" { bucket = "my-project-terraform-state"; prefix = "terraform/state" }
}

provider "google"      { project = var.project_id; region = var.region }
provider "google-beta" { project = var.project_id; region = var.region }
```

### Terraform Module Structure

```
infra/
├── environments/
│   ├── dev/           # main.tf, variables.tf, terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── network/       # VPC, subnets, firewall, NAT
│   ├── gke/           # GKE cluster + node pools
│   ├── cloud-run/     # Cloud Run services
│   ├── database/      # Cloud SQL, Spanner
│   ├── observability/ # Monitoring, logging, alerting
│   └── security/      # IAM, org policies, KMS
└── shared/
    └── state-bucket/  # Bootstrap: create state bucket
```

### Pulumi GCP Pattern (TypeScript)

```typescript
import * as gcp from "@pulumi/gcp";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const environment = config.require("environment");

const vpc = new gcp.compute.Network("vpc", {
  name: `vpc-myapp-${environment}`,
  autoCreateSubnetworks: false,
});

const cluster = new gcp.container.Cluster("gke", {
  name: `gke-myapp-${environment}`,
  location: "us-central1",
  network: vpc.id,
  removeDefaultNodePool: true,
  initialNodeCount: 1,
  workloadIdentityConfig: { workloadPool: `${gcp.config.project}.svc.id.goog` },
  releaseChannel: { channel: "REGULAR" },
});

export const clusterName = cluster.name;
```

## CI/CD

### Cloud Build Pipeline

```yaml
# cloudbuild.yaml
steps:
  - name: 'node:22-slim'
    entrypoint: 'npm'
    args: ['ci']
    id: install

  - name: 'node:22-slim'
    entrypoint: 'npm'
    args: ['test']
    id: test
    waitFor: ['install']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}', '.']
    id: build
    waitFor: ['test']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}']
    id: push
    waitFor: ['build']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args: ['run', 'deploy', '${_SERVICE}',
           '--image=${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}',
           '--region=${_REGION}', '--platform=managed', '--quiet']
    id: deploy
    waitFor: ['push']

substitutions:
  _REGION: us-central1
  _REPO: myapp
  _SERVICE: api
options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'E2_HIGHCPU_8'
```

### Artifact Registry

```hcl
resource "google_artifact_registry_repository" "docker" {
  repository_id = "myapp"
  location      = var.region
  format        = "DOCKER"

  cleanup_policies {
    id = "keep-recent"; action = "KEEP"
    most_recent_versions { keep_count = 10 }
  }
  cleanup_policies {
    id = "delete-old-untagged"; action = "DELETE"
    condition { tag_state = "UNTAGGED"; older_than = "604800s" }
  }
}

resource "google_artifact_registry_repository_iam_member" "cloudbuild" {
  repository = google_artifact_registry_repository.docker.name
  location   = var.region
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}
```

### Cloud Deploy (GKE Delivery Pipeline)

```bash
# Create a release
gcloud deploy releases create "v1.2.3" \
  --delivery-pipeline="myapp-pipeline" --region="us-central1" \
  --images="api=${REGION}-docker.pkg.dev/${PROJECT_ID}/myapp/api:v1.2.3"

# Approve promotion to production
gcloud deploy rollouts approve "v1.2.3-to-production-0001" \
  --delivery-pipeline="myapp-pipeline" --release="v1.2.3" --region="us-central1"
```

## Observability

### Cloud Monitoring (Alerting)

```hcl
resource "google_monitoring_notification_channel" "pagerduty" {
  display_name = "PagerDuty - ${var.environment}"
  type         = "pagerduty"
  labels       = { service_key = var.pagerduty_service_key }
}

resource "google_monitoring_uptime_check_config" "api" {
  display_name = "API Health - ${var.environment}"
  timeout = "10s"; period = "60s"
  http_check { path = "/healthz"; port = 443; use_ssl = true; validate_ssl = true }
  monitored_resource {
    type   = "uptime_url"
    labels = { project_id = var.project_id; host = var.api_domain }
  }
}

# Alert: High error rate (MQL)
resource "google_monitoring_alert_policy" "error_rate" {
  display_name = "High Error Rate - ${var.environment}"
  combiner     = "OR"
  conditions {
    display_name = "Error rate > 1%"
    condition_monitoring_query_language {
      query = <<-MQL
        fetch cloud_run_revision
        | metric 'run.googleapis.com/request_count'
        | filter resource.service_name == 'api-${var.environment}'
        | align rate(1m)
        | group_by [metric.response_code_class],
            [value_request_count_aggregate: aggregate(value.request_count)]
        | outer_join 0
        | value [error_rate:
            sum(if(metric.response_code_class = '5xx', value_request_count_aggregate, 0))
            / sum(value_request_count_aggregate) * 100]
        | condition error_rate > 1
      MQL
      duration = "300s"
    }
  }
  notification_channels = [google_monitoring_notification_channel.pagerduty.id]
  alert_strategy { auto_close = "1800s" }
}
```

### Cloud Logging

```bash
# Query logs
gcloud logging read \
  'resource.type="cloud_run_revision" AND severity>=ERROR AND resource.labels.service_name="api-production"' \
  --limit=50 --format=json --freshness=1h

# Log-based metric
gcloud logging metrics create api-errors \
  --description="Count of API 5xx errors" \
  --log-filter='resource.type="cloud_run_revision" AND httpRequest.status>=500'

# Log sink to BigQuery
gcloud logging sinks create audit-to-bq \
  "bigquery.googleapis.com/projects/my-project/datasets/audit_logs" \
  --log-filter='logName:"cloudaudit.googleapis.com"'
```

```hcl
resource "google_logging_project_sink" "audit_bq" {
  name        = "audit-to-bigquery"
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/${google_bigquery_dataset.audit.dataset_id}"
  filter      = "logName:\"cloudaudit.googleapis.com\""
  unique_writer_identity = true
  bigquery_options { use_partitioned_tables = true }
}

resource "google_bigquery_dataset_iam_member" "sink_writer" {
  dataset_id = google_bigquery_dataset.audit.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = google_logging_project_sink.audit_bq.writer_identity
}
```

### Cloud Trace and Error Reporting

```bash
gcloud services enable cloudtrace.googleapis.com \
  clouderrorreporting.googleapis.com cloudprofiler.googleapis.com

# Cloud Trace is automatic for Cloud Run and GKE with the trace agent.
# For custom instrumentation, use OpenTelemetry with the GCP exporter.
# See the opentelemetry skill (sw-infra:opentelemetry) for full setup.
```

### SLO Monitoring

```hcl
resource "google_monitoring_slo" "api_availability" {
  service      = google_monitoring_custom_service.api.service_id
  display_name = "API Availability SLO"
  goal         = 0.999
  rolling_period_days = 28
  request_based_sli {
    good_total_ratio {
      good_service_filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"api-${var.environment}\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.labels.response_code_class!=\"5xx\""
      total_service_filter = "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"api-${var.environment}\" AND metric.type=\"run.googleapis.com/request_count\""
    }
  }
}

resource "google_monitoring_alert_policy" "slo_burn" {
  display_name = "SLO Burn Rate Alert - ${var.environment}"
  combiner     = "OR"
  conditions {
    display_name = "SLO burn rate high"
    condition_threshold {
      filter          = "select_slo_burn_rate(\"${google_monitoring_slo.api_availability.id}\", \"60m\")"
      comparison      = "COMPARISON_GT"
      threshold_value = 10
      duration        = "0s"
    }
  }
  notification_channels = [google_monitoring_notification_channel.pagerduty.id]
}
```

## Cost Optimization Quick Reference

```
┌─────────────────────────────┬──────────────────────────────────────┐
│ Strategy                    │ Implementation                       │
├─────────────────────────────┼──────────────────────────────────────┤
│ Committed Use Discounts     │ 1yr: ~20% off, 3yr: ~50% off        │
│ Spot VMs                    │ Up to 91% off (can be preempted)     │
│ Cloud Run min=0             │ Scale to zero in non-prod            │
│ Cloud SQL shared-core       │ db-f1-micro for dev/staging          │
│ GKE Autopilot               │ Pay per pod, not per node            │
│ Storage lifecycle            │ Standard->Nearline->Coldline->Archive│
│ BigQuery flat-rate           │ Predictable cost at scale            │
│ Cloud NAT per-VM pricing    │ Reduce NAT by using Private Google   │
│ Rightsizing recommendations  │ gcloud recommender insights list     │
│ Budget alerts                │ Set billing budgets + Pub/Sub alerts │
└─────────────────────────────┴──────────────────────────────────────┘
```
