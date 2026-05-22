---
name: deployment-gcp-canary-setup
description: "Set up progressive canary deployments on GCP Cloud Run with traffic splitting, monitoring alerts, and automated rollback."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - LS
---

# Skill: GCP Canary Deployment Setup

This skill teaches you how to implement production-ready canary deployments for GCP Cloud Run. You'll configure progressive traffic shifting between revisions, Cloud Monitoring alerts for error rate and latency, and automated rollback mechanisms.

Canary deployments reduce blast radius by gradually shifting traffic to new revisions. If metrics indicate problems, traffic routes back to the stable revision automatically.

## Prerequisites

- GCP project with Cloud Run API enabled
- Terraform 1.5+ installed and configured
- gcloud CLI authenticated with appropriate permissions
- Cloud Monitoring API enabled
- Service already deployed to Cloud Run (at least one revision exists)

## Overview

You will:
1. Set up Cloud Run with revision naming for traffic splitting
2. Configure initial traffic split (90/10)
3. Create Cloud Monitoring alert policies
4. Implement rollback automation script
5. Create canary deployment Makefile targets
6. Test rollback scenarios

## Step 1: Cloud Run Terraform with Traffic Splitting

```hcl
# infra/terraform/modules/cloud-run-canary/variables.tf

variable "project_id" { type = string }
variable "service_name" { type = string }
variable "image" { type = string }
variable "region" { type = string; default = "us-central1" }
variable "environment" { type = string }
variable "min_instances" { type = number; default = 0 }
variable "max_instances" { type = number; default = 100 }

variable "traffic_split" {
  type = list(object({
    revision_name = string
    percent       = number
    latest        = bool
  }))
  default = [{ revision_name = null, percent = 100, latest = true }]
}

variable "enable_canary_alerts" { type = bool; default = true }
variable "error_rate_threshold" { type = number; default = 0.01 }
variable "latency_threshold_ms" { type = number; default = 2000 }
```

```hcl
# infra/terraform/modules/cloud-run-canary/main.tf

resource "google_cloud_run_v2_service" "service" {
  name     = "${var.service_name}-${var.environment}"
  location = var.region
  project  = var.project_id

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }
    containers {
      image = var.image
      resources {
        limits = { cpu = "2", memory = "1Gi" }
        cpu_idle = true
      }
      startup_probe {
        http_get { path = "/health"; port = 8080 }
        initial_delay_seconds = 5
        period_seconds = 10
        failure_threshold = 3
      }
      liveness_probe {
        http_get { path = "/health"; port = 8080 }
        period_seconds = 30
        failure_threshold = 3
      }
    }
  }

  dynamic "traffic" {
    for_each = var.traffic_split
    content {
      type     = traffic.value.latest ? "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST" : "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"
      revision = traffic.value.latest ? null : traffic.value.revision_name
      percent  = traffic.value.percent
    }
  }

  lifecycle { ignore_changes = [traffic, client, client_version] }
}

output "service_url" { value = google_cloud_run_v2_service.service.uri }
output "latest_revision" { value = google_cloud_run_v2_service.service.latest_ready_revision }
```

## Step 2: Configure Initial Traffic Split (90/10)

```hcl
# services/my-service/deploy/terraform/main.tf

variable "canary_percent" { type = number; default = 100 }

data "terraform_remote_state" "current" {
  count   = var.canary_percent < 100 ? 1 : 0
  backend = "gcs"
  config = {
    bucket = "myorg-terraform-state"
    prefix = "services/my-service/${var.environment}"
  }
}

module "service" {
  source = "../../../../infra/terraform/modules/cloud-run-canary"

  project_id   = var.project_id
  service_name = "my-service"
  image        = "gcr.io/${var.project_id}/my-service:${var.image_tag}"
  region       = var.region
  environment  = var.environment

  traffic_split = var.canary_percent < 100 ? [
    { revision_name = null, percent = var.canary_percent, latest = true },
    { revision_name = try(data.terraform_remote_state.current[0].outputs.stable_revision, null),
      percent = 100 - var.canary_percent, latest = false }
  ] : [{ revision_name = null, percent = 100, latest = true }]

  enable_canary_alerts = var.environment == "prod"
}

output "stable_revision" { value = module.service.latest_revision }
```

## Step 3: Create Cloud Monitoring Alert Policies

```hcl
# infra/terraform/modules/cloud-run-canary/alerts.tf

resource "google_monitoring_alert_policy" "error_rate" {
  count        = var.enable_canary_alerts ? 1 : 0
  project      = var.project_id
  display_name = "${var.service_name}-${var.environment}-error-rate"
  combiner     = "OR"

  conditions {
    display_name = "Error Rate > ${var.error_rate_threshold * 100}%"
    condition_monitoring_query_language {
      query = <<-EOT
        fetch cloud_run_revision
        | filter resource.service_name == '${var.service_name}-${var.environment}'
        | { t_0: metric 'run.googleapis.com/request_count' | filter metric.response_code_class == '5xx'
          ; t_1: metric 'run.googleapis.com/request_count' }
        | ratio | every 1m | condition val() > ${var.error_rate_threshold}
      EOT
      duration = "120s"
      trigger { count = 1 }
    }
  }
  alert_strategy { auto_close = "1800s" }
}

resource "google_monitoring_alert_policy" "latency" {
  count        = var.enable_canary_alerts ? 1 : 0
  project      = var.project_id
  display_name = "${var.service_name}-${var.environment}-latency"
  combiner     = "OR"

  conditions {
    display_name = "P99 Latency > ${var.latency_threshold_ms}ms"
    condition_monitoring_query_language {
      query = <<-EOT
        fetch cloud_run_revision
        | filter resource.service_name == '${var.service_name}-${var.environment}'
        | metric 'run.googleapis.com/request_latencies'
        | align delta(1m) | every 1m
        | group_by [], [value: percentile(value.request_latencies, 99)]
        | condition val() > ${var.latency_threshold_ms}
      EOT
      duration = "120s"
      trigger { count = 1 }
    }
  }
  alert_strategy { auto_close = "1800s" }
}
```

## Step 4: Implement Rollback Automation Script

```bash
#!/bin/bash
# tools/scripts/check-canary-metrics.sh
set -euo pipefail

SERVICE="${1:?Service name required}"
ENVIRONMENT="${2:?Environment required}"
PROJECT_ID="${3:-${PROJECT_ID:?PROJECT_ID not set}}"

ERROR_RATE_THRESHOLD=0.01
LATENCY_THRESHOLD_MS=2000
SERVICE_FULL="${SERVICE}-${ENVIRONMENT}"

query_metric() {
  gcloud monitoring time-series query --project="${PROJECT_ID}" --start-time="-5m" \
    --query="$1" --format="value(pointData.values[0].doubleValue)" 2>/dev/null || echo "0"
}

ERROR_RATE=$(query_metric "
  fetch cloud_run_revision | filter resource.service_name == '${SERVICE_FULL}'
  | { t_0: metric 'run.googleapis.com/request_count' | filter metric.response_code_class == '5xx'
    ; t_1: metric 'run.googleapis.com/request_count' } | ratio")

LATENCY_P99=$(query_metric "
  fetch cloud_run_revision | filter resource.service_name == '${SERVICE_FULL}'
  | metric 'run.googleapis.com/request_latencies' | align delta(1m) | every 1m
  | group_by [], [value: percentile(value.request_latencies, 99)]")

echo "Error rate: ${ERROR_RATE} | P99 latency: ${LATENCY_P99}ms"

FAILED=0
(( $(echo "${ERROR_RATE} > ${ERROR_RATE_THRESHOLD}" | bc -l) )) && FAILED=1
(( $(echo "${LATENCY_P99} > ${LATENCY_THRESHOLD_MS}" | bc -l) )) && FAILED=1

[[ ${FAILED} -eq 1 ]] && { echo "CANARY VALIDATION FAILED"; exit 1; }
echo "CANARY VALIDATION PASSED"
```

```bash
#!/bin/bash
# tools/scripts/rollback.sh
set -euo pipefail

SERVICE="${1:?Service name required}"
ENVIRONMENT="${2: prod}"
PROJECT_ID="${3:-${PROJECT_ID:?}}"
REGION="${4: us-central1}"

PREV_REVISION=$(gcloud run revisions list --service="${SERVICE}-${ENVIRONMENT}" \
  --region="${REGION}" --project="${PROJECT_ID}" \
  --format='value(name)' --sort-by='~metadata.creationTimestamp' --limit=2 | tail -1)

gcloud run services update-traffic "${SERVICE}-${ENVIRONMENT}" \
  --region="${REGION}" --project="${PROJECT_ID}" --to-revisions="${PREV_REVISION}=100"

echo "Rolled back to ${PREV_REVISION}"
```

## Step 5: Create Canary Deployment Makefile Targets

```makefile
# services/my-service/Makefile

SERVICE_NAME := my-service
VERSION ?= $(shell git describe --tags --always --dirty)
STAGE ?= prod
PROJECT_ID ?= myorg-platform
REGION ?= us-central1
IAC_DIR := deploy/terraform
SCRIPTS_DIR := ../../../tools/scripts
IMAGE := gcr.io/$(PROJECT_ID)/$(SERVICE_NAME):$(VERSION)

.PHONY: build package push deploy deploy-canary promote rollback

build:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o bin/server ./cmd/api

package: build
	docker build --platform linux/amd64 -t $(IMAGE) -f Dockerfile ../..

push:
	docker push $(IMAGE)

deploy: package push
	@cd $(IAC_DIR) && terraform init -backend-config="bucket=$(PROJECT_ID)-terraform-state" \
		-backend-config="prefix=services/$(SERVICE_NAME)/$(STAGE)" && \
	terraform apply -var="project_id=$(PROJECT_ID)" -var="environment=$(STAGE)" \
		-var="image_tag=$(VERSION)" -var="canary_percent=100" -auto-approve

deploy-canary: package push
ifndef PERCENT
	$(error PERCENT required. Usage: make deploy-canary PERCENT=10)
endif
	@cd $(IAC_DIR) && terraform init -backend-config="bucket=$(PROJECT_ID)-terraform-state" \
		-backend-config="prefix=services/$(SERVICE_NAME)/$(STAGE)" && \
	terraform apply -var="project_id=$(PROJECT_ID)" -var="environment=$(STAGE)" \
		-var="image_tag=$(VERSION)" -var="canary_percent=$(PERCENT)" -auto-approve
	@sleep 30
	@$(SCRIPTS_DIR)/check-canary-metrics.sh $(SERVICE_NAME) $(STAGE) $(PROJECT_ID)

promote:
	@$(MAKE) deploy STAGE=$(STAGE)

rollback:
	@$(SCRIPTS_DIR)/rollback.sh $(SERVICE_NAME) $(STAGE) $(PROJECT_ID) $(REGION)

canary-10:
	@$(MAKE) deploy-canary PERCENT=10

canary-50:
	@$(MAKE) deploy-canary PERCENT=50

canary-full:
	@$(MAKE) promote

traffic-status:
	@gcloud run services describe $(SERVICE_NAME)-$(STAGE) --region=$(REGION) \
		--project=$(PROJECT_ID) --format='table(status.traffic.revisionName,status.traffic.percent)'

list-revisions:
	@gcloud run revisions list --service=$(SERVICE_NAME)-$(STAGE) --region=$(REGION) \
		--project=$(PROJECT_ID) --format='table(name,metadata.creationTimestamp)' --limit=10
```

## Step 6: Test Rollback Scenarios

```bash
#!/bin/bash
# tools/scripts/test-rollback.sh
set -euo pipefail

SERVICE="${1:?Service name required}"
ENVIRONMENT="${2: staging}"
PROJECT_ID="${3:-${PROJECT_ID:?}}"
REGION="${4: us-central1}"
SERVICE_FULL="${SERVICE}-${ENVIRONMENT}"

REVISIONS=$(gcloud run revisions list --service="${SERVICE_FULL}" --region="${REGION}" \
  --project="${PROJECT_ID}" --format='value(name)' --sort-by='~metadata.creationTimestamp' --limit=5)

CURRENT=$(echo "${REVISIONS}" | head -1)
PREVIOUS=$(echo "${REVISIONS}" | head -2 | tail -1)

echo "Testing rollback: ${CURRENT} -> ${PREVIOUS}"
gcloud run services update-traffic "${SERVICE_FULL}" --region="${REGION}" \
  --project="${PROJECT_ID}" --to-revisions="${PREVIOUS}=100"

sleep 5
SERVICE_URL=$(gcloud run services describe "${SERVICE_FULL}" --region="${REGION}" \
  --project="${PROJECT_ID}" --format='value(status.url)')
curl -s -o /dev/null -w "Health: HTTP %{http_code}\n" "${SERVICE_URL}/health"

echo "Restoring: ${PREVIOUS} -> ${CURRENT}"
gcloud run services update-traffic "${SERVICE_FULL}" --region="${REGION}" \
  --project="${PROJECT_ID}" --to-revisions="${CURRENT}=100"
```

## GitHub Actions CI/CD Workflow

```yaml
# .github/workflows/deploy-canary-gcp.yaml
name: GCP Canary Deployment

on:
  workflow_dispatch:
    inputs:
      service:
        description: 'Service to deploy'
        required: true
        type: choice
        options: [my-service, other-service]
      version:
        description: 'Version/tag to deploy'
        required: true
        type: string

env:
  PROJECT_ID: myorg-platform
  REGION: us-central1
  WORKLOAD_IDENTITY_PROVIDER: projects/123456789/locations/global/workloadIdentityPools/github/providers/github-actions
  SERVICE_ACCOUNT: github-actions@myorg-platform.iam.gserviceaccount.com

jobs:
  deploy-canary-10:
    name: Deploy Canary (10%)
    runs-on: ubuntu-latest
    environment: prod-canary-start
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.version }}

      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ env.WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ env.SERVICE_ACCOUNT }}

      - uses: google-github-actions/setup-gcloud@v2

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Deploy canary 10%
        run: |
          cd services/go/${{ inputs.service }}
          make deploy-canary PERCENT=10 VERSION=${{ inputs.version }} STAGE=prod

      - name: Validate metrics
        run: |
          sleep 180
          ./tools/scripts/check-canary-metrics.sh ${{ inputs.service }} prod ${{ env.PROJECT_ID }}

      - name: Rollback on failure
        if: failure()
        run: |
          cd services/go/${{ inputs.service }}
          make rollback STAGE=prod

  deploy-canary-50:
    name: Deploy Canary (50%)
    needs: deploy-canary-10
    runs-on: ubuntu-latest
    environment: prod-canary-50
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.version }}

      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ env.WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ env.SERVICE_ACCOUNT }}

      - uses: google-github-actions/setup-gcloud@v2
      - uses: hashicorp/setup-terraform@v3

      - name: Deploy canary 50%
        run: |
          cd services/go/${{ inputs.service }}
          make deploy-canary PERCENT=50 VERSION=${{ inputs.version }} STAGE=prod

      - name: Validate metrics
        run: |
          sleep 180
          ./tools/scripts/check-canary-metrics.sh ${{ inputs.service }} prod ${{ env.PROJECT_ID }}

      - name: Rollback on failure
        if: failure()
        run: make rollback STAGE=prod
        working-directory: services/go/${{ inputs.service }}

  promote-100:
    name: Promote to 100%
    needs: deploy-canary-50
    runs-on: ubuntu-latest
    environment: prod-canary-100
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.version }}

      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ env.WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ env.SERVICE_ACCOUNT }}

      - uses: google-github-actions/setup-gcloud@v2
      - uses: hashicorp/setup-terraform@v3

      - name: Promote to 100%
        run: |
          cd services/go/${{ inputs.service }}
          make promote VERSION=${{ inputs.version }} STAGE=prod

      - name: Final validation
        run: |
          sleep 60
          ./tools/scripts/check-canary-metrics.sh ${{ inputs.service }} prod ${{ env.PROJECT_ID }}
```

## Usage Examples

```bash
# Progressive canary deployment
make canary-10      # Deploy at 10%
make canary-50      # Increase to 50%
make canary-full    # Promote to 100%

# Check traffic distribution
make traffic-status

# Emergency rollback
make rollback STAGE=prod
```

### gcloud CLI Quick Commands

```bash
# View traffic split
gcloud run services describe my-service-prod --region=us-central1 --format='yaml(status.traffic)'

# Instant rollback to specific revision
gcloud run services update-traffic my-service-prod --region=us-central1 \
  --to-revisions=my-service-prod-00042-abc=100

# Split traffic 90/10
gcloud run services update-traffic my-service-prod --region=us-central1 \
  --to-revisions=my-service-prod-00042-abc=90,my-service-prod-00043-xyz=10
```

## Verification Checklist

- [ ] Cloud Run module supports `traffic_split` variable
- [ ] Service Terraform reads previous revision from remote state
- [ ] Cloud Monitoring alerts created for error rate and latency
- [ ] Metrics validation script exits with code 1 on threshold breach
- [ ] Makefile has `deploy-canary`, `promote`, and `rollback` targets
- [ ] Rollback routes 100% traffic to previous revision
- [ ] Health probes configured for startup and liveness
- [ ] Minimum 2 revisions maintained for rollback capability
- [ ] Traffic status shows correct percentage distribution
- [ ] Rollback test passes in staging environment
