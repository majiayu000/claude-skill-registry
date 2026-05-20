---
name: gcp-cloud-run
description: Deploy containerized applications on Google Cloud Run with automatic scaling, traffic management, and service mesh integration. Use for container-based serverless computing.
---

# GCP Cloud Run

## Overview

Google Cloud Run enables deployment of containerized applications at scale without managing infrastructure. Run stateless HTTP containers with automatic scaling from zero to thousands of instances, paying only for compute time consumed.

## When to Use

- Microservices and APIs
- Web applications and backends
- Batch processing jobs
- Long-running background workers
- CI/CD pipeline integration
- Data processing pipelines
- WebSocket applications
- Multi-language services

## Implementation Examples

### 1. **Cloud Run Deployment with gcloud CLI**

```bash
# Build container image
gcloud builds submit --tag gcr.io/MY_PROJECT_ID/my-app:latest

# Deploy to Cloud Run
gcloud run deploy my-app \
  --image gcr.io/MY_PROJECT_ID/my-app:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --max-instances 100 \
  --min-instances 1 \
  --no-allow-unauthenticated \
  --set-env-vars NODE_ENV=production,DATABASE_URL=postgresql://...

# Allow public access
gcloud run services add-iam-policy-binding my-app \
  --platform managed \
  --region us-central1 \
  --member=allUsers \
  --role=roles/run.invoker

# Get service URL
gcloud run services describe my-app \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'

# View logs
gcloud run services logs read my-app --limit 50

# Update service with new image
gcloud run deploy my-app \
  --image gcr.io/MY_PROJECT_ID/my-app:v2 \
  --platform managed \
  --region us-central1 \
  --update-env-vars VERSION=2
```

### 2. **Containerized Application (Node.js)**

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Expose port (Cloud Run uses 8080 by default)
EXPOSE 8080

# Run application
CMD ["node", "server.js"]
```

```javascript
// server.js
const express = require('express');
const app = express();

const PORT = process.env.PORT || 8080;

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Liveness probe
app.get('/live', (req, res) => {
  res.status(200).send('alive');
});

// Readiness probe
app.get('/ready', (req, res) => {
  res.status(200).send('ready');
});

// API endpoints
app.get('/api/data', async (req, res) => {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Graceful shutdown
let isShuttingDown = false;

process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  isShuttingDown = true;

  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });

  // Force close after 30 seconds
  setTimeout(() => {
    console.error('Forced shutdown due to timeout');
    process.exit(1);
  }, 30000);
});

const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

async function fetchData() {
  return { items: [] };
}
```

### 3. **Terraform Cloud Run Configuration**

```hcl
# cloud-run.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "GCP Project ID"
}

variable "region" {
  default = "us-central1"
}

variable "image" {
  description = "Container image URI"
}

# Service account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}

# Grant Cloud Logging role
resource "google_project_iam_member" "cloud_run_logs" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Cloud SQL Client role (if using Cloud SQL)
resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Cloud Run service
resource "google_cloud_run_service" "app" {
  name     = "my-app"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.cloud_run_sa.email

      containers {
        image = var.image

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }

        env {
          name  = "NODE_ENV"
          value = "production"
        }

        env {
          name  = "PORT"
          value = "8080"
        }

        ports {
          container_port = 8080
        }

        # Startup probe
        startup_probe {
          http_get {
            path = "/ready"
            port = 8080
          }
          failure_threshold = 3
          period_seconds    = 10
        }

        # Liveness probe
        liveness_probe {
          http_get {
            path = "/live"
            port = 8080
          }
          failure_threshold     = 3
          period_seconds        = 10
          initial_delay_seconds = 10
        }
      }

      timeout_seconds       = 3600
      service_account_name  = google_service_account.cloud_run_sa.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "100"
        "autoscaling.knative.dev/minScale" = "1"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_iam_member.cloud_run_logs]
}

# Allow public access
resource "google_cloud_run_service_iam_binding" "public" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# Cloud Load Balancer for global access
resource "google_compute_backend_service" "app" {
  name            = "my-app-backend"
  protocol        = "HTTPS"
  security_policy = google_compute_security_policy.app.id

  backend {
    group = google_compute_network_endpoint_group.app.id
  }

  health_checks = [google_compute_health_check.app.id]

  log_config {
    enable      = true
    sample_rate = 1.0
  }
}

# Network Endpoint Group for Cloud Run
resource "google_compute_network_endpoint_group" "app" {
  name                  = "my-app-neg"
  network_endpoint_type = "SERVERLESS"
  cloud_run_config {
    service = google_cloud_run_service.app.name
  }
  location = var.region
}

# Health check
resource "google_compute_health_check" "app" {
  name = "my-app-health-check"

  https_health_check {
    port         = "8080"
    request_path = "/health"
  }
}

# Cloud Armor security policy
resource "google_compute_security_policy" "app" {
  name = "my-app-policy"

  rules {
    action   = "deny(403)"
    priority = "100"
    match {
      versioned_expr = "CEL_V1"
      expression     = "origin.country_code in ['CN', 'RU']"
    }
  }

  rules {
    action   = "rate_based_ban"
    priority = "200"
    match {
      versioned_expr = "CEL_V1"
      expression     = "true"
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      enforce_on_key = "IP"
      ban_duration_sec = 600
      rate_limit_threshold {
        count        = 100
        interval_sec = 60
      }
      ban_threshold_rule {
        count        = 1000
        interval_sec = 60
      }
    }
  }

  rules {
    action   = "allow"
    priority = "65535"
    match {
      versioned_expr = "CEL_V1"
      expression     = "true"
    }
  }
}

# Global address
resource "google_compute_global_address" "app" {
  name = "my-app-address"
}

# HTTPS redirect
resource "google_compute_url_map" "https_redirect" {
  name = "my-app-https-redirect"

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "301"
    strip_query            = false
  }
}

# HTTPS target proxy
resource "google_compute_target_https_proxy" "app" {
  name            = "my-app-proxy"
  url_map         = google_compute_url_map.app.id
  ssl_certificates = [google_compute_managed_ssl_certificate.app.id]
}

# Managed SSL certificate
resource "google_compute_managed_ssl_certificate" "app" {
  name = "my-app-cert"

  managed {
    domains = ["example.com"]
  }
}

# URL map
resource "google_compute_url_map" "app" {
  name            = "my-app-url-map"
  default_service = google_compute_backend_service.app.id
}

# Forwarding rule
resource "google_compute_global_forwarding_rule" "app" {
  name                  = "my-app-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL"
  port_range            = "443"
  target                = google_compute_target_https_proxy.app.id
  address               = google_compute_global_address.app.address
}

# Monitoring alert
resource "google_monitoring_alert_policy" "cloud_run_errors" {
  display_name = "Cloud Run High Error Rate"
  combiner     = "OR"

  conditions {
    display_name = "Error rate threshold"

    condition_threshold {
      filter          = "metric.type=\"run.googleapis.com/request_count\" AND resource.label.service_name=\"my-app\" AND metric.label.response_code_class=\"5xx\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 10
      aggregations {
        alignment_period    = "60s"
        per_series_aligner  = "ALIGN_RATE"
      }
    }
  }

  notification_channels = []
}

# Cloud Run job for batch processing
resource "google_cloud_run_v2_job" "batch" {
  name     = "batch-processor"
  location = var.region

  template {
    containers {
      image = var.image
      env {
        name  = "JOB_TYPE"
        value = "batch"
      }
    }
    timeout       = "3600s"
    service_account = google_service_account.cloud_run_sa.email
  }
}

# Cloud Scheduler to trigger job
resource "google_cloud_scheduler_job" "batch_trigger" {
  name             = "batch-processor-trigger"
  schedule         = "0 2 * * *"
  time_zone        = "UTC"
  attempt_deadline = "320s"
  region           = var.region

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/jobs/batch-processor:run"

    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = google_service_account.cloud_run_sa.email
    }
  }
}

output "cloud_run_url" {
  value = google_cloud_run_service.app.status[0].url
}

output "load_balancer_ip" {
  value = google_compute_global_address.app.address
}
```

### 4. **Docker Build and Push**

```bash
# Build image locally
docker build -t my-app:latest .

# Tag for Container Registry
docker tag my-app:latest gcr.io/MY_PROJECT_ID/my-app:latest

# Push to Container Registry
docker push gcr.io/MY_PROJECT_ID/my-app:latest

# Or use Cloud Build
gcloud builds submit \
  --tag gcr.io/MY_PROJECT_ID/my-app:latest \
  --source-dir . \
  --no-cache
```

## Best Practices

### ✅ DO
- Use container health checks
- Set appropriate CPU and memory
- Implement graceful shutdown
- Use service accounts with least privilege
- Monitor with Cloud Logging
- Enable Cloud Armor for protection
- Use revision management for blue-green deployments
- Implement startup and liveness probes

### ❌ DON'T
- Store secrets in code
- Use default service account
- Create stateful applications
- Ignore health checks
- Deploy without testing
- Use excessive resource limits
- Store files in container filesystem

## Monitoring

- Cloud Logging for application logs
- Cloud Monitoring for metrics
- Error Reporting for error tracking
- Cloud Trace for distributed tracing
- Revision metrics and analytics

## Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/tips/general-tips)
- [Container Lifecycle and Graceful Shutdown](https://cloud.google.com/run/docs/terminating-instances)
