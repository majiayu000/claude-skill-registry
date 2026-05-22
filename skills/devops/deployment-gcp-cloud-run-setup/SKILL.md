---
name: deployment-gcp-cloud-run-setup
description: "Step-by-step guide for setting up GCP Cloud Run infrastructure with Terraform, Firestore, Pub/Sub, and Workflows."
---

# Skill: GCP Cloud Run Deployment Setup

This skill teaches you how to set up a complete GCP Cloud Run deployment infrastructure using Terraform. You'll create production-ready infrastructure for containerized services, Firestore database, Pub/Sub messaging, and Workflows following  architectural patterns.

A well-structured Cloud Run deployment ensures scalability, cost-efficiency, and maintainability. Cloud Run provides serverless container execution with automatic scaling to zero, HTTPS endpoints, and built-in traffic splitting for canary deployments. Following consistent Terraform patterns across services enables team members to quickly understand and deploy any service with confidence.

This skill uses Terraform as the infrastructure language, which provides excellent provider support and state management. The patterns work across Go, TypeScript, and Python services deployed as Docker containers.

## Prerequisites

- Google Cloud CLI (`gcloud`) configured with appropriate credentials
- Terraform 1.5+ installed
- Docker installed for building container images
- Go 1.25+ (or Node.js/Python for other runtimes)
- Understanding of containerization and Cloud Run concepts
- A bounded context or service to deploy
- GCP project with billing enabled

## Overview

In this skill, you will:
1. Initialize the Terraform project with GCS backend
2. Create the Cloud Run service module with traffic splitting
3. Configure Firestore database
4. Set up Pub/Sub topics and subscriptions
5. Add Workflows for orchestration (GCP's Step Functions equivalent)
6. Create a Makefile for build and deployment automation

## Step 1: Initialize Terraform Project

Create the Terraform project structure within your service's deploy directory. This keeps infrastructure code close to the service it deploys.

### Directory Structure

```text
services/my-service/
├── cmd/
│   └── api/
│       └── main.go              # HTTP server for Cloud Run
├── core/
│   ├── domain/
│   └── application/
├── adapters/
│   ├── inbound/                 # HTTP handlers
│   └── outbound/                # Firestore, Pub/Sub clients
├── deploy/
│   └── terraform/
│       ├── main.tf              # Main configuration
│       ├── cloud-run.tf         # Cloud Run service
│       ├── firestore.tf         # Firestore database
│       ├── pubsub.tf            # Pub/Sub topics
│       ├── workflows.tf         # Workflows orchestration
│       ├── variables.tf         # Input variables
│       ├── outputs.tf           # Output values
│       └── versions.tf          # Provider versions
├── Dockerfile                   # Cloud Run container
├── Makefile                     # GCP-specific targets
└── go.mod
```

### Provider Configuration

```hcl
# deploy/terraform/versions.tf

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }

  # Backend configured via CLI: terraform init -backend-config="..."
  backend "gcs" {}
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
```

### Variables Configuration

```hcl
# deploy/terraform/variables.tf

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "GCP region for resources"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
}

variable "canary_percent" {
  type        = number
  default     = 100
  description = "Percentage of traffic to route to latest revision (for canary)"
}

# Service-specific configuration per environment
locals {
  service_name = "my-service"
  image        = "gcr.io/${var.project_id}/${local.service_name}:${var.image_tag}"

  env_config = {
    dev = {
      min_instances = 0
      max_instances = 2
      cpu           = "1"
      memory        = "512Mi"
    }
    staging = {
      min_instances = 1
      max_instances = 5
      cpu           = "1"
      memory        = "512Mi"
    }
    prod = {
      min_instances = 2
      max_instances = 50
      cpu           = "2"
      memory        = "1Gi"
    }
  }

  config = local.env_config[var.environment]
}
```

This configuration provides environment-specific settings for scaling, memory, and CPU. Production uses higher minimums for consistent performance, while dev scales to zero for cost savings.

## Step 2: Create Cloud Run Service Module

Define the Cloud Run service with proper scaling, health checks, and traffic splitting for canary deployments.

### Cloud Run Service

```hcl
# deploy/terraform/cloud-run.tf

# Get current revision for canary deployments
data "terraform_remote_state" "current" {
  count   = var.canary_percent < 100 ? 1 : 0
  backend = "gcs"
  config = {
    bucket = "myorg-terraform-state"
    prefix = "services/${local.service_name}/${var.environment}"
  }
}

# Cloud Run service
resource "google_cloud_run_v2_service" "service" {
  name     = "${local.service_name}-${var.environment}"
  location = var.region

  # Deletion protection for production
  deletion_protection = var.environment == "prod"

  template {
    # Scaling configuration
    scaling {
      min_instance_count = local.config.min_instances
      max_instance_count = local.config.max_instances
    }

    # Service account for the container
    service_account = google_service_account.service.email

    containers {
      image = local.image

      # Resource limits
      resources {
        limits = {
          cpu    = local.config.cpu
          memory = local.config.memory
        }
        cpu_idle = var.environment != "prod"  # Allow CPU throttling in non-prod
      }

      # Environment variables
      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "SERVICE_NAME"
        value = local.service_name
      }
      env {
        name  = "FIRESTORE_PROJECT"
        value = var.project_id
      }
      env {
        name  = "PUBSUB_TOPIC"
        value = google_pubsub_topic.events.name
      }

      # Port configuration
      ports {
        container_port = 8080
      }

      # Health check
      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 5
        period_seconds        = 10
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

    # Request timeout
    timeout = "60s"

    # Concurrency per instance
    max_instance_request_concurrency = 80
  }

  # Traffic splitting for canary deployments
  dynamic "traffic" {
    for_each = var.canary_percent < 100 ? [1] : []
    content {
      type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
      percent = var.canary_percent
    }
  }

  dynamic "traffic" {
    for_each = var.canary_percent < 100 ? [1] : []
    content {
      type     = "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"
      revision = data.terraform_remote_state.current[0].outputs.stable_revision
      percent  = 100 - var.canary_percent
    }
  }

  dynamic "traffic" {
    for_each = var.canary_percent >= 100 ? [1] : []
    content {
      type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
      percent = 100
    }
  }

  depends_on = [
    google_project_service.run,
  ]
}

# Service account for Cloud Run
resource "google_service_account" "service" {
  account_id   = "${local.service_name}-${var.environment}"
  display_name = "${local.service_name} service account (${var.environment})"
}

# IAM - Allow unauthenticated access (adjust for prod)
resource "google_cloud_run_v2_service_iam_member" "invoker" {
  count    = var.environment == "prod" ? 0 : 1
  location = google_cloud_run_v2_service.service.location
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Enable required APIs
resource "google_project_service" "run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}
```

### Cloud Run Key Concepts

Cloud Run provides serverless container execution with these characteristics:

| Feature | Description |
|---------|-------------|
| Auto-scaling | Scales from 0 to max based on traffic |
| Traffic splitting | Route percentage of traffic to revisions |
| Revisions | Immutable snapshots of deployments |
| Concurrency | Multiple requests per instance |
| Cold starts | Minimize with min instances > 0 |

## Step 3: Configure Firestore Database

Set up Firestore in Native mode for document storage with proper indexes and security.

### Firestore Configuration

```hcl
# deploy/terraform/firestore.tf

# Enable Firestore API
resource "google_project_service" "firestore" {
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

# Firestore database (one per project)
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  # Enable delete protection for prod
  delete_protection_state = var.environment == "prod" ? "DELETE_PROTECTION_ENABLED" : "DELETE_PROTECTION_DISABLED"

  depends_on = [google_project_service.firestore]
}

# Composite indexes for query patterns
resource "google_firestore_index" "facility_by_tenant" {
  project    = var.project_id
  database   = google_firestore_database.database.name
  collection = "facilities"

  fields {
    field_path = "tenant_id"
    order      = "ASCENDING"
  }

  fields {
    field_path = "created_at"
    order      = "DESCENDING"
  }
}

resource "google_firestore_index" "asset_by_facility" {
  project    = var.project_id
  database   = google_firestore_database.database.name
  collection = "assets"

  fields {
    field_path = "facility_id"
    order      = "ASCENDING"
  }

  fields {
    field_path = "state"
    order      = "ASCENDING"
  }
}

# Grant Firestore access to service account
resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.service.email}"
}
```

### Firestore Go Client Example

```go
// adapters/outbound/firestore/repository.go
package firestore

import (
    "context"
    "fmt"
    "time"

    "cloud.google.com/go/firestore"
    "google.golang.org/api/iterator"
)

// FacilityRepository implements outports.FacilityRepository with Firestore.
type FacilityRepository struct {
    client     *firestore.Client
    collection string
}

// NewFacilityRepository creates a Firestore repository.
func NewFacilityRepository(client *firestore.Client) *FacilityRepository {
    return &FacilityRepository{
        client:     client,
        collection: "facilities",
    }
}

// facilityDoc is the Firestore document representation.
type facilityDoc struct {
    ID        string    `firestore:"id"`
    TenantID  string    `firestore:"tenant_id"`
    Name      string    `firestore:"name"`
    Address   string    `firestore:"address"`
    State     string    `firestore:"state"`
    CreatedAt time.Time `firestore:"created_at"`
    UpdatedAt time.Time `firestore:"updated_at"`
}

// Save persists the facility to Firestore.
func (r *FacilityRepository) Save(ctx context.Context, facility *domain.Facility) error {
    doc := facilityDoc{
        ID:        facility.ID(),
        TenantID:  facility.TenantID(),
        Name:      facility.Name(),
        Address:   facility.Address().String(),
        State:     string(facility.State()),
        CreatedAt: facility.CreatedAt(),
        UpdatedAt: time.Now().UTC(),
    }

    _, err := r.client.Collection(r.collection).Doc(facility.ID()).Set(ctx, doc)
    if err != nil {
        return fmt.Errorf("failed to save facility: %w", err)
    }

    return nil
}

// FindByID retrieves a facility by ID.
func (r *FacilityRepository) FindByID(ctx context.Context, id string) (*domain.Facility, error) {
    docSnap, err := r.client.Collection(r.collection).Doc(id).Get(ctx)
    if err != nil {
        if status.Code(err) == codes.NotFound {
            return nil, domain.ErrFacilityNotFound
        }
        return nil, fmt.Errorf("failed to get facility: %w", err)
    }

    var doc facilityDoc
    if err := docSnap.DataTo(&doc); err != nil {
        return nil, fmt.Errorf("failed to unmarshal facility: %w", err)
    }

    return r.toDomain(doc)
}

// FindByTenant retrieves all facilities for a tenant.
func (r *FacilityRepository) FindByTenant(ctx context.Context, tenantID string) ([]*domain.Facility, error) {
    iter := r.client.Collection(r.collection).
        Where("tenant_id", "==", tenantID).
        OrderBy("created_at", firestore.Desc).
        Documents(ctx)
    defer iter.Stop()

    var facilities []*domain.Facility
    for {
        docSnap, err := iter.Next()
        if err == iterator.Done {
            break
        }
        if err != nil {
            return nil, fmt.Errorf("failed to iterate facilities: %w", err)
        }

        var doc facilityDoc
        if err := docSnap.DataTo(&doc); err != nil {
            return nil, fmt.Errorf("failed to unmarshal facility: %w", err)
        }

        facility, err := r.toDomain(doc)
        if err != nil {
            return nil, err
        }
        facilities = append(facilities, facility)
    }

    return facilities, nil
}
```

Firestore provides automatic scaling, strong consistency, and real-time subscriptions. Use collection hierarchies to model relationships and composite indexes for complex queries.

## Step 4: Set Up Pub/Sub

Configure Pub/Sub topics and subscriptions for domain event publishing.

### Pub/Sub Configuration

```hcl
# deploy/terraform/pubsub.tf

# Enable Pub/Sub API
resource "google_project_service" "pubsub" {
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

# Domain events topic
resource "google_pubsub_topic" "events" {
  name = "${local.service_name}-events-${var.environment}"

  # Message retention for replay
  message_retention_duration = var.environment == "prod" ? "604800s" : "86400s"  # 7 days / 1 day

  depends_on = [google_project_service.pubsub]
}

# Dead letter topic for failed messages
resource "google_pubsub_topic" "dlq" {
  name = "${local.service_name}-dlq-${var.environment}"

  depends_on = [google_project_service.pubsub]
}

# Subscription for event handlers
resource "google_pubsub_subscription" "event_handler" {
  name  = "${local.service_name}-event-handler-${var.environment}"
  topic = google_pubsub_topic.events.name

  # Acknowledge deadline
  ack_deadline_seconds = 60

  # Message retention
  message_retention_duration = "604800s"  # 7 days

  # Retry policy with exponential backoff
  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }

  # Dead letter policy
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }

  # Enable exactly-once delivery for idempotency
  enable_exactly_once_delivery = true

  depends_on = [google_project_service.pubsub]
}

# Push subscription to Cloud Run (alternative to pull)
resource "google_pubsub_subscription" "push_handler" {
  count = var.environment != "dev" ? 1 : 0  # Only in staging/prod
  name  = "${local.service_name}-push-handler-${var.environment}"
  topic = google_pubsub_topic.events.name

  ack_deadline_seconds = 60

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.service.uri}/events"

    oidc_token {
      service_account_email = google_service_account.pubsub_invoker.email
    }

    attributes = {
      x-goog-version = "v1"
    }
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }

  depends_on = [google_cloud_run_v2_service.service]
}

# Service account for Pub/Sub push
resource "google_service_account" "pubsub_invoker" {
  account_id   = "pubsub-invoker-${var.environment}"
  display_name = "Pub/Sub invoker for Cloud Run"
}

# Allow Pub/Sub to invoke Cloud Run
resource "google_cloud_run_v2_service_iam_member" "pubsub_invoker" {
  count    = var.environment != "dev" ? 1 : 0
  location = google_cloud_run_v2_service.service.location
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub_invoker.email}"
}

# Grant Pub/Sub publisher role to service
resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.service.email}"
}
```

### Pub/Sub Go Publisher Example

```go
// adapters/outbound/pubsub/publisher.go
package pubsub

import (
    "context"
    "encoding/json"
    "fmt"

    "cloud.google.com/go/pubsub"
)

// EventPublisher publishes domain events to Pub/Sub.
type EventPublisher struct {
    client *pubsub.Client
    topic  *pubsub.Topic
}

// NewEventPublisher creates a Pub/Sub publisher.
func NewEventPublisher(client *pubsub.Client, topicName string) *EventPublisher {
    topic := client.Topic(topicName)
    // Enable message ordering for aggregate consistency
    topic.EnableMessageOrdering = true

    return &EventPublisher{
        client: client,
        topic:  topic,
    }
}

// Publish sends domain events to Pub/Sub.
func (p *EventPublisher) Publish(ctx context.Context, events []domain.Event) error {
    for _, event := range events {
        data, err := json.Marshal(event)
        if err != nil {
            return fmt.Errorf("failed to marshal event: %w", err)
        }

        msg := &pubsub.Message{
            Data: data,
            Attributes: map[string]string{
                "event_type":     event.EventType(),
                "aggregate_id":   event.AggregateID(),
                "schema_version": event.SchemaVersion(),
            },
            OrderingKey: event.AggregateID(),  // Ensure ordering per aggregate
        }

        result := p.topic.Publish(ctx, msg)
        if _, err := result.Get(ctx); err != nil {
            return fmt.Errorf("failed to publish event %s: %w", event.EventID(), err)
        }
    }

    return nil
}

// Close releases publisher resources.
func (p *EventPublisher) Close() {
    p.topic.Stop()
}
```

## Step 5: Add Workflows Orchestration

Configure GCP Workflows for multi-step processes (equivalent to AWS Step Functions).

### Workflows Configuration

```hcl
# deploy/terraform/workflows.tf

# Enable Workflows API
resource "google_project_service" "workflows" {
  service            = "workflows.googleapis.com"
  disable_on_destroy = false
}

# Workflow definition
resource "google_workflows_workflow" "process" {
  count           = var.environment != "dev" ? 1 : 0
  name            = "${local.service_name}-process-${var.environment}"
  region          = var.region
  service_account = google_service_account.workflow.email

  source_contents = <<-YAML
    main:
      params: [input]
      steps:
        - init:
            assign:
              - correlationId: $${input.correlation_id}
              - aggregateId: $${input.aggregate_id}
              - baseUrl: "${google_cloud_run_v2_service.service.uri}"

        - validate:
            call: http.post
            args:
              url: $${baseUrl + "/workflow/validate"}
              body:
                correlation_id: $${correlationId}
                aggregate_id: $${aggregateId}
                payload: $${input.payload}
              auth:
                type: OIDC
            result: validateResult

        - checkValidation:
            switch:
              - condition: $${validateResult.body.valid == false}
                raise: $${validateResult.body.error}

        - process:
            try:
              call: http.post
              args:
                url: $${baseUrl + "/workflow/process"}
                body:
                  correlation_id: $${correlationId}
                  aggregate_id: $${aggregateId}
                  validated_data: $${validateResult.body.data}
                auth:
                  type: OIDC
              result: processResult
            except:
              as: e
              steps:
                - compensate:
                    call: http.post
                    args:
                      url: $${baseUrl + "/workflow/compensate"}
                      body:
                        correlation_id: $${correlationId}
                        aggregate_id: $${aggregateId}
                        error: $${e.message}
                      auth:
                        type: OIDC
                - raiseError:
                    raise: $${e}

        - finalize:
            call: http.post
            args:
              url: $${baseUrl + "/workflow/finalize"}
              body:
                correlation_id: $${correlationId}
                aggregate_id: $${aggregateId}
                result: $${processResult.body}
              auth:
                type: OIDC
            result: finalResult

        - returnResult:
            return: $${finalResult.body}
  YAML

  depends_on = [google_project_service.workflows]
}

# Service account for Workflows
resource "google_service_account" "workflow" {
  account_id   = "workflow-${var.environment}"
  display_name = "Workflows service account (${var.environment})"
}

# Allow Workflows to invoke Cloud Run
resource "google_cloud_run_v2_service_iam_member" "workflow_invoker" {
  count    = var.environment != "dev" ? 1 : 0
  location = google_cloud_run_v2_service.service.location
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.workflow.email}"
}

# Allow service to execute workflows
resource "google_project_iam_member" "workflow_invoker" {
  count   = var.environment != "dev" ? 1 : 0
  project = var.project_id
  role    = "roles/workflows.invoker"
  member  = "serviceAccount:${google_service_account.service.email}"
}
```

### Workflow Handler in Go

```go
// adapters/inbound/http/workflow_handlers.go
package http

import (
    "encoding/json"
    "net/http"
)

// WorkflowValidateRequest is the request for validation step.
type WorkflowValidateRequest struct {
    CorrelationID string          `json:"correlation_id"`
    AggregateID   string          `json:"aggregate_id"`
    Payload       json.RawMessage `json:"payload"`
}

// HandleWorkflowValidate handles the validation step.
func (h *Handler) HandleWorkflowValidate(w http.ResponseWriter, r *http.Request) {
    var req WorkflowValidateRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        h.respondError(w, http.StatusBadRequest, "invalid request")
        return
    }

    // Validate the payload
    result, err := h.validateUseCase.Execute(r.Context(), usecases.ValidateCommand{
        CorrelationID: req.CorrelationID,
        AggregateID:   req.AggregateID,
        Payload:       req.Payload,
    })
    if err != nil {
        h.respondJSON(w, http.StatusOK, map[string]interface{}{
            "valid": false,
            "error": err.Error(),
        })
        return
    }

    h.respondJSON(w, http.StatusOK, map[string]interface{}{
        "valid": true,
        "data":  result.ValidatedData,
    })
}

// HandleWorkflowCompensate handles the compensation step.
func (h *Handler) HandleWorkflowCompensate(w http.ResponseWriter, r *http.Request) {
    var req struct {
        CorrelationID string `json:"correlation_id"`
        AggregateID   string `json:"aggregate_id"`
        Error         string `json:"error"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        h.respondError(w, http.StatusBadRequest, "invalid request")
        return
    }

    // Execute compensation logic
    if err := h.compensateUseCase.Execute(r.Context(), usecases.CompensateCommand{
        CorrelationID: req.CorrelationID,
        AggregateID:   req.AggregateID,
        Reason:        req.Error,
    }); err != nil {
        h.respondError(w, http.StatusInternalServerError, "compensation failed")
        return
    }

    h.respondJSON(w, http.StatusOK, map[string]string{
        "status": "compensated",
    })
}
```

## Step 6: Create Outputs and Makefile

Define Terraform outputs and create a comprehensive Makefile.

### Terraform Outputs

```hcl
# deploy/terraform/outputs.tf

output "service_url" {
  value       = google_cloud_run_v2_service.service.uri
  description = "Cloud Run service URL"
}

output "stable_revision" {
  value       = google_cloud_run_v2_service.service.latest_ready_revision
  description = "Latest ready revision name (for canary)"
}

output "events_topic" {
  value       = google_pubsub_topic.events.name
  description = "Pub/Sub events topic name"
}

output "service_account" {
  value       = google_service_account.service.email
  description = "Service account email"
}
```

### Makefile

```makefile
# services/my-service/Makefile

SERVICE_NAME := my-service
VERSION ?= $(shell git describe --tags --always --dirty)

# GCP settings
PROJECT_ID ?= myorg-platform
REGION ?= us-central1
REGISTRY := gcr.io/$(PROJECT_ID)
IMAGE := $(REGISTRY)/$(SERVICE_NAME)
STAGE ?= dev

IAC_DIR := deploy/terraform

.PHONY: build package push deploy deploy-canary promote rollback test clean help

##@ Building

# Build Go binary
build:
	@echo "Building $(SERVICE_NAME)..."
	@CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
		-ldflags="-s -w -X main.Version=$(VERSION)" \
		-o bin/server ./cmd/api

##@ Testing

test: test-unit test-integration

test-unit:
	@echo "Running unit tests..."
	@go test -v -race -coverprofile=coverage.out ./core/...

test-integration:
	@echo "Running integration tests..."
	@go test -v -race ./tests/integration/...

lint:
	@echo "Running linter..."
	@golangci-lint run ./...

##@ Packaging

# Build Docker image
package:
	@echo "Building $(IMAGE):$(VERSION)..."
	@docker build \
		-f Dockerfile \
		-t $(IMAGE):$(VERSION) \
		-t $(IMAGE):latest \
		../../../

# Push to GCR
push:
	@echo "Pushing $(IMAGE):$(VERSION)..."
	@docker push $(IMAGE):$(VERSION)
	@docker push $(IMAGE):latest

##@ Deployment

# Deploy to environment
deploy: package push
ifndef STAGE
	$(error STAGE is required: make deploy STAGE=dev)
endif
	@echo "Deploying $(SERVICE_NAME) to $(STAGE)..."
	@cd $(IAC_DIR) && \
		terraform init \
			-backend-config="bucket=myorg-terraform-state" \
			-backend-config="prefix=services/$(SERVICE_NAME)/$(STAGE)" && \
		terraform apply \
			-var="environment=$(STAGE)" \
			-var="image_tag=$(VERSION)" \
			-var="project_id=$(PROJECT_ID)" \
			-auto-approve

# Deploy canary
deploy-canary: package push
ifndef PERCENT
	PERCENT=10
endif
	@echo "Deploying canary at $(PERCENT)%..."
	@cd $(IAC_DIR) && \
		terraform init \
			-backend-config="bucket=myorg-terraform-state" \
			-backend-config="prefix=services/$(SERVICE_NAME)/prod" && \
		terraform apply \
			-var="environment=prod" \
			-var="image_tag=$(VERSION)" \
			-var="project_id=$(PROJECT_ID)" \
			-var="canary_percent=$(PERCENT)" \
			-auto-approve

# Promote canary to 100%
promote:
	@$(MAKE) deploy-canary PERCENT=100

# Rollback to previous revision
rollback:
ifndef STAGE
	$(error STAGE is required)
endif
	@echo "Rolling back $(SERVICE_NAME) in $(STAGE)..."
	@gcloud run services update-traffic $(SERVICE_NAME)-$(STAGE) \
		--region=$(REGION) \
		--to-revisions=$$(gcloud run revisions list \
			--service=$(SERVICE_NAME)-$(STAGE) \
			--region=$(REGION) \
			--format='value(name)' \
			--limit=2 | tail -1)=100

##@ Utilities

# Tail Cloud Run logs
logs:
ifndef STAGE
	$(error STAGE is required)
endif
	@gcloud logging tail \
		"resource.type=cloud_run_revision AND resource.labels.service_name=$(SERVICE_NAME)-$(STAGE)" \
		--format="value(textPayload)"

# Clean build artifacts
clean:
	@rm -rf bin coverage.out

# Show help
help:
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
```

### Dockerfile

```dockerfile
# Dockerfile

FROM golang:1.25-alpine AS builder

WORKDIR /app

# Copy workspace files from monorepo root
COPY go.work go.work.sum ./
COPY go-core/ go-core/
COPY go-services/my-service/ go-services/my-service/

WORKDIR /app/go-services/my-service

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-w -s" \
    -o /server ./cmd/api

# Runtime stage
FROM gcr.io/distroless/static-debian12:nonroot

COPY --from=builder /server /server

EXPOSE 8080

ENTRYPOINT ["/server"]
```

## Usage

### Local Development

```bash
# Build binary
make build

# Run tests
make test

# Build Docker image
make package
```

### Deployment

```bash
# Configure Docker for GCR
gcloud auth configure-docker gcr.io

# Deploy to dev
make deploy STAGE=dev

# Deploy to staging
make deploy STAGE=staging

# Deploy to prod (with canary)
make deploy-canary PERCENT=10
# ... wait, check metrics ...
make deploy-canary PERCENT=50
# ... wait, check metrics ...
make promote
```

### Rollback

```bash
# Rollback to previous revision
make rollback STAGE=prod
```

## Verification Checklist

After setting up your Cloud Run deployment, verify:

- [ ] Terraform initializes with GCS backend configured
- [ ] Cloud Run service deploys successfully with health checks
- [ ] Service scales to zero in dev, maintains min instances in prod
- [ ] Firestore database created with appropriate indexes
- [ ] Pub/Sub topics have dead letter queues configured
- [ ] Push subscriptions can invoke Cloud Run (staging/prod)
- [ ] Workflows can orchestrate multi-step processes
- [ ] Service account has least-privilege IAM roles
- [ ] Traffic splitting works for canary deployments
- [ ] Makefile has build, package, deploy, rollback targets
- [ ] Environment-specific configuration (dev/staging/prod) works
- [ ] Docker builds with multi-stage for minimal image size
