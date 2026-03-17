---
name: terraform-infrastructure
description: Terraform and GCP infrastructure patterns for gh-pr-linear-issue-linker. Use when creating/modifying Terraform, provisioning GCP resources, configuring IAM, Cloud Run, Artifact Registry, or working with infrastructure as code.
---

# Terraform Infrastructure Patterns

## Project Structure

```
infra/
├── main.tf              # Primary resources (Cloud Run, Artifact Registry)
├── variables.tf         # Input variables (project_id, region, etc.)
├── outputs.tf           # Exported values (service_url, etc.)
├── secrets.tf           # Secret Manager resources
├── iam.tf               # IAM policies and service accounts
├── terraform.tfvars.example  # Example configuration
└── terraform.tfvars     # Actual secrets (gitignored)
```

## Core Resources

### Cloud Run Service

```hcl
resource "google_cloud_run_service" "app" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.image_url

        env {
          name = "GITHUB_APP_ID"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.github_app_id.secret_id
              key  = "latest"
            }
          }
        }
      }

      service_account_name = google_service_account.app.email
    }
  }
}
```

### Artifact Registry

```hcl
resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = var.service_name
  format        = "DOCKER"
  description   = "Container images for ${var.service_name}"
}
```

### Secret Manager

```hcl
resource "google_secret_manager_secret" "github_app_id" {
  secret_id = "${var.service_name}-github-app-id"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "github_app_id" {
  secret      = google_secret_manager_secret.github_app_id.id
  secret_data = var.github_app_id
}
```

## IAM Patterns

### Service Account (Least Privilege)

```hcl
resource "google_service_account" "app" {
  account_id   = "${var.service_name}-sa"
  display_name = "Service account for ${var.service_name}"
}

# Grant only necessary permissions
resource "google_secret_manager_secret_iam_member" "app_secrets" {
  secret_id = google_secret_manager_secret.github_app_id.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

### Public Access (for GitHub webhooks)

```hcl
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

## Cloud Build Integration

```hcl
# Trigger build when Dockerfile changes
resource "null_resource" "build_image" {
  triggers = {
    dockerfile_hash = filemd5("${path.module}/../Dockerfile")
  }

  provisioner "local-exec" {
    command = <<-EOT
      gcloud builds submit ../. \
        --config=cloudbuild.yaml \
        --substitutions=_IMAGE_URL=${local.image_url}
    EOT
  }
}
```

## Variable Patterns

```hcl
# variables.tf
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "github_app_id" {
  description = "GitHub App ID"
  type        = string
  sensitive   = true
}
```

## Output Patterns

```hcl
# outputs.tf
output "service_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_service.app.status[0].url
}

output "artifact_registry_url" {
  description = "Artifact Registry repository URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app.repository_id}"
}
```

## Commands

**Initialize Terraform:**
```bash
cd infra && terraform init
```

**Plan changes:**
```bash
cd infra && terraform plan
```

**Apply changes:**
```bash
cd infra && terraform apply
```

**View outputs:**
```bash
cd infra && terraform output
```

**Destroy resources (careful!):**
```bash
cd infra && terraform destroy
```

## State Management

**Backend configuration (use GCS for team):**

```hcl
terraform {
  backend "gcs" {
    bucket = "your-terraform-state-bucket"
    prefix = "gh-pr-linear-issue-linker"
  }
}
```

**Local state (for personal projects):**
- State stored in `infra/terraform.tfstate`
- Gitignored automatically

## Best Practices

### 1. Never Commit Secrets

```bash
# terraform.tfvars is gitignored
# Use terraform.tfvars.example as template

cp infra/terraform.tfvars.example infra/terraform.tfvars
# Edit terraform.tfvars with actual secrets
```

### 2. Use Variables for Everything

```hcl
# ❌ BAD - Hardcoded values
resource "google_cloud_run_service" "app" {
  name     = "gh-pr-linear-issue-linker"
  location = "us-central1"
}

# ✅ GOOD - Use variables
resource "google_cloud_run_service" "app" {
  name     = var.service_name
  location = var.region
}
```

### 3. Document Outputs

```hcl
output "service_url" {
  description = "Cloud Run service URL for GitHub webhook configuration"
  value       = google_cloud_run_service.app.status[0].url
}
```

### 4. Use Modules for Reusability

```hcl
# For larger projects, extract common patterns
module "secrets" {
  source = "./modules/secrets"

  service_name = var.service_name
  secrets      = var.secrets
}
```

## Common Resources Checklist

When setting up new infrastructure:

- [ ] Cloud Run service configured
- [ ] Artifact Registry repository created
- [ ] Secret Manager secrets defined
- [ ] Service account with least privilege
- [ ] IAM policies for secrets access
- [ ] Public access configured (if needed)
- [ ] Outputs defined for service URL
- [ ] Variables use `sensitive = true` for secrets
- [ ] terraform.tfvars.example provided
- [ ] .gitignore includes terraform.tfvars
