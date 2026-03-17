---
name: gcp
description: Google Cloud Platform services including GKE, Cloud Run, Cloud Storage, BigQuery, and Pub/Sub. Activate for GCP infrastructure, Google Cloud deployment, and GCP integration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# GCP Skill

Provides comprehensive Google Cloud Platform capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- GKE cluster management
- Cloud Run deployments
- Cloud Storage operations
- BigQuery data analytics
- Pub/Sub messaging

## gcloud CLI Quick Reference

### Configuration
\`\`\`bash
# Initialize
gcloud init

# Authenticate
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project PROJECT_ID

# Check config
gcloud config list
gcloud info
\`\`\`

### GKE (Google Kubernetes Engine)
\`\`\`bash
# Create cluster
gcloud container clusters create golden-armada-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-standard-4 \
  --enable-autoscaling --min-nodes 1 --max-nodes 10

# Get credentials
gcloud container clusters get-credentials golden-armada-cluster --zone us-central1-a

# List clusters
gcloud container clusters list

# Resize cluster
gcloud container clusters resize golden-armada-cluster --num-nodes 5 --zone us-central1-a

# Delete cluster
gcloud container clusters delete golden-armada-cluster --zone us-central1-a
\`\`\`

### Cloud Run
\`\`\`bash
# Deploy service
gcloud run deploy golden-armada-api \
  --image gcr.io/PROJECT_ID/agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "ENV=production"

# List services
gcloud run services list

# Get service URL
gcloud run services describe golden-armada-api --platform managed --region us-central1 --format 'value(status.url)'

# Update traffic
gcloud run services update-traffic golden-armada-api \
  --to-revisions REVISION=100
\`\`\`

### Cloud Storage
\`\`\`bash
# Create bucket
gsutil mb -l us-central1 gs://golden-armada-data

# Copy files
gsutil cp local-file.txt gs://bucket-name/
gsutil cp gs://bucket-name/file.txt .
gsutil -m cp -r ./local-dir gs://bucket-name/

# List
gsutil ls gs://bucket-name/

# Sync
gsutil rsync -r ./local-dir gs://bucket-name/dir/

# Set permissions
gsutil iam ch allUsers:objectViewer gs://bucket-name
\`\`\`

### BigQuery
\`\`\`bash
# Create dataset
bq mk --dataset PROJECT_ID:agents_dataset

# Create table
bq mk --table agents_dataset.agent_logs schema.json

# Query
bq query --use_legacy_sql=false \
  'SELECT * FROM `project.dataset.table` LIMIT 10'

# Load data
bq load --source_format=NEWLINE_DELIMITED_JSON \
  agents_dataset.logs gs://bucket/logs/*.json

# Export
bq extract --destination_format NEWLINE_DELIMITED_JSON \
  agents_dataset.logs gs://bucket/export/logs-*.json
\`\`\`

### Pub/Sub
\`\`\`bash
# Create topic
gcloud pubsub topics create agent-events

# Create subscription
gcloud pubsub subscriptions create agent-events-sub \
  --topic agent-events

# Publish message
gcloud pubsub topics publish agent-events \
  --message '{"event": "agent_started", "agent_id": "123"}'

# Pull messages
gcloud pubsub subscriptions pull agent-events-sub --auto-ack
\`\`\`

## Python SDK

\`\`\`python
from google.cloud import storage, bigquery, pubsub_v1

# Cloud Storage
storage_client = storage.Client()
bucket = storage_client.bucket('golden-armada-data')

# Upload
blob = bucket.blob('agents/config.json')
blob.upload_from_string(json.dumps(config))

# Download
blob = bucket.blob('agents/config.json')
content = blob.download_as_string()

# BigQuery
bq_client = bigquery.Client()

query = """
    SELECT agent_id, COUNT(*) as task_count
    FROM `project.dataset.tasks`
    GROUP BY agent_id
    ORDER BY task_count DESC
"""
results = bq_client.query(query)
for row in results:
    print(f"{row.agent_id}: {row.task_count}")

# Insert rows
table_ref = bq_client.dataset('agents_dataset').table('logs')
errors = bq_client.insert_rows_json(table_ref, rows)

# Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'agent-events')

future = publisher.publish(
    topic_path,
    json.dumps({"event": "task_completed"}).encode(),
    agent_id="123"
)
message_id = future.result()

# Pub/Sub Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('project-id', 'agent-events-sub')

def callback(message):
    print(f"Received: {message.data}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
\`\`\`

## Terraform GCP Resources

\`\`\`hcl
provider "google" {
  project = var.project_id
  region  = var.region
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "golden-armada-cluster"
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    machine_type = "e2-standard-4"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }
}

# Cloud Run Service
resource "google_cloud_run_service" "agent_api" {
  name     = "golden-armada-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/agent:latest"
        env {
          name  = "ENV"
          value = "production"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Storage Bucket
resource "google_storage_bucket" "data" {
  name     = "golden-armada-data"
  location = var.region

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}
\`\`\`
