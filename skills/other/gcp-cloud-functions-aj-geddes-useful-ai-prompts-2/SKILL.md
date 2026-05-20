---
name: gcp-cloud-functions
description: Deploy serverless functions on Google Cloud Platform with triggers, IAM roles, environment variables, and monitoring. Use for event-driven computing on GCP.
---

# GCP Cloud Functions

## Overview

Google Cloud Functions enables event-driven serverless computing on Google Cloud Platform. Build functions with automatic scaling, integrated security, and seamless integration with Google Cloud services for rapid development.

## When to Use

- HTTP APIs and webhooks
- Pub/Sub message processing
- Storage bucket events
- Firestore database triggers
- Cloud Scheduler jobs
- Real-time data processing
- Image and video processing
- Data pipeline orchestration

## Implementation Examples

### 1. **Cloud Function Creation with gcloud CLI**

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize and authenticate
gcloud init
gcloud auth application-default login

# Set project
gcloud config set project MY_PROJECT_ID

# Create service account
gcloud iam service-accounts create cloud-function-sa \
  --display-name "Cloud Function Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding MY_PROJECT_ID \
  --member="serviceAccount:cloud-function-sa@MY_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"

# Deploy HTTP function
gcloud functions deploy my-http-function \
  --gen2 \
  --runtime nodejs18 \
  --region us-central1 \
  --source ./src \
  --entry-point httpHandler \
  --trigger-http \
  --allow-unauthenticated \
  --timeout 60 \
  --memory 256MB \
  --max-instances 100 \
  --set-env-vars NODE_ENV=production,API_KEY=xxx \
  --service-account cloud-function-sa@MY_PROJECT_ID.iam.gserviceaccount.com

# Deploy Pub/Sub function
gcloud functions deploy my-pubsub-function \
  --gen2 \
  --runtime nodejs18 \
  --region us-central1 \
  --source ./src \
  --entry-point pubsubHandler \
  --trigger-topic my-topic \
  --memory 256MB \
  --timeout 300 \
  --service-account cloud-function-sa@MY_PROJECT_ID.iam.gserviceaccount.com

# Deploy Cloud Storage function
gcloud functions deploy my-storage-function \
  --gen2 \
  --runtime nodejs18 \
  --region us-central1 \
  --source ./src \
  --entry-point storageHandler \
  --trigger-bucket my-bucket \
  --trigger-location us-central1 \
  --timeout 60 \
  --service-account cloud-function-sa@MY_PROJECT_ID.iam.gserviceaccount.com

# List functions
gcloud functions list

# Get function details
gcloud functions describe my-http-function --gen2 --region us-central1

# Call function
gcloud functions call my-http-function \
  --region us-central1 \
  --data '{"name":"John"}'

# View logs
gcloud functions logs read my-http-function --limit 50 --gen2 --region us-central1

# Delete function
gcloud functions delete my-http-function --gen2 --region us-central1
```

### 2. **Cloud Functions Implementation (Node.js)**

```javascript
// HTTP Trigger Function
exports.httpHandler = async (req, res) => {
  try {
    // Enable CORS
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');

    if (req.method === 'OPTIONS') {
      res.status(204).send('');
      return;
    }

    // Parse request
    const { name } = req.query;

    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }

    // Log with Cloud Logging
    console.log(JSON.stringify({
      severity: 'INFO',
      message: 'Processing request',
      name: name,
      requestId: req.id
    }));

    // Business logic
    const response = {
      message: `Hello ${name}!`,
      timestamp: new Date().toISOString()
    };

    res.status(200).json(response);
  } catch (error) {
    console.error(JSON.stringify({
      severity: 'ERROR',
      message: error.message,
      stack: error.stack
    }));

    res.status(500).json({ error: 'Internal server error' });
  }
};

// Pub/Sub Trigger Function
exports.pubsubHandler = async (message, context) => {
  try {
    // Decode Pub/Sub message
    const pubsubMessage = message.data
      ? Buffer.from(message.data, 'base64').toString()
      : null;

    console.log('Received message:', pubsubMessage);

    // Parse message
    const data = JSON.parse(pubsubMessage);

    // Process message asynchronously
    await processMessage(data);

    console.log('Message processed successfully');
  } catch (error) {
    console.error('Error processing message:', error);
    throw error; // Function will retry
  }
};

// Cloud Storage Trigger Function
exports.storageHandler = async (file, context) => {
  try {
    const { name, bucket } = file;

    console.log(JSON.stringify({
      message: 'Processing storage event',
      bucket: bucket,
      file: name,
      eventId: context.eventId,
      eventType: context.eventType
    }));

    // Check file type
    if (!name.endsWith('.jpg') && !name.endsWith('.png')) {
      console.log('Skipping non-image file');
      return;
    }

    // Process image
    await processImage(bucket, name);

    console.log('Image processed successfully');
  } catch (error) {
    console.error('Error processing file:', error);
    throw error;
  }
};

// Cloud Scheduler (CRON) Function
exports.cronHandler = async (req, res) => {
  try {
    console.log('Scheduled job started');

    // Run batch processing
    await performBatchJob();

    res.status(200).json({ message: 'Batch job completed' });
  } catch (error) {
    console.error('Error in batch job:', error);
    res.status(500).json({ error: error.message });
  }
};

// Helper functions
async function processMessage(data) {
  // Business logic
  return new Promise(resolve => {
    setTimeout(() => resolve(), 1000);
  });
}

async function processImage(bucket, filename) {
  // Use Cloud Vision API or similar
  return true;
}

async function performBatchJob() {
  // Batch processing logic
  return true;
}
```

### 3. **Terraform Cloud Functions Configuration**

```hcl
# cloud-functions.tf
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

# Service account for functions
resource "google_service_account" "function_sa" {
  account_id   = "cloud-function-sa"
  display_name = "Cloud Function Service Account"
}

# Grant invoker role
resource "google_project_iam_member" "function_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# Grant Cloud Logging role
resource "google_project_iam_member" "function_logs" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# Source archive bucket
resource "google_storage_bucket" "function_source" {
  name     = "${var.project_id}-function-source"
  location = var.region
}

# Upload function code
resource "google_storage_bucket_object" "function_zip" {
  name   = "function-${data.archive_file.function.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function.output_path
}

# Archive function code
data "archive_file" "function" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/function.zip"
}

# HTTP Cloud Function
resource "google_cloudfunctions2_function" "http_function" {
  name        = "my-http-function"
  location    = var.region
  description = "HTTP trigger function"

  build_config {
    runtime           = "nodejs18"
    entry_point       = "httpHandler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 100
    available_memory_mb = 256
    timeout_seconds = 60
    service_account_email = google_service_account.function_sa.email

    environment_variables = {
      NODE_ENV = "production"
      API_KEY  = "your-api-key"
    }
  }

  labels = {
    env = "production"
  }
}

# Allow public HTTP access
resource "google_cloudfunctions2_function_iam_member" "http_public" {
  cloud_function = google_cloudfunctions2_function.http_function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}

# Pub/Sub topic
resource "google_pubsub_topic" "messages" {
  name = "message-topic"
}

# Pub/Sub Cloud Function
resource "google_cloudfunctions2_function" "pubsub_function" {
  name        = "my-pubsub-function"
  location    = var.region
  description = "Pub/Sub trigger function"

  build_config {
    runtime           = "nodejs18"
    entry_point       = "pubsubHandler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 100
    available_memory_mb = 256
    timeout_seconds = 300
    service_account_email = google_service_account.function_sa.email
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.publish"
    pubsub_topic   = google_pubsub_topic.messages.id
  }
}

# Cloud Storage bucket
resource "google_storage_bucket" "uploads" {
  name     = "${var.project_id}-uploads"
  location = var.region
}

# Cloud Storage trigger function
resource "google_cloudfunctions2_function" "storage_function" {
  name        = "my-storage-function"
  location    = var.region
  description = "Cloud Storage trigger function"

  build_config {
    runtime           = "nodejs18"
    entry_point       = "storageHandler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 50
    available_memory_mb = 256
    timeout_seconds = 60
    service_account_email = google_service_account.function_sa.email
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.storage.object.finalize"
    resource       = google_storage_bucket.uploads.name
  }
}

# Cloud Scheduler job (CRON)
resource "google_cloud_scheduler_job" "batch_job" {
  name             = "batch-job-scheduler"
  description      = "Scheduled batch job"
  schedule         = "0 2 * * *" # Daily at 2 AM
  time_zone        = "UTC"
  attempt_deadline = "320s"
  region           = var.region

  retry_config {
    retry_count = 1
  }

  http_target {
    uri        = google_cloudfunctions2_function.http_function.service_config[0].uri
    http_method = "POST"

    headers = {
      "Content-Type" = "application/json"
    }

    body = base64encode(jsonencode({
      job_type = "batch"
    }))

    oidc_token {
      service_account_email = google_service_account.function_sa.email
    }
  }
}

# Cloud Logging sink
resource "google_logging_project_sink" "function_logs" {
  name        = "cloud-function-logs"
  destination = "logging.googleapis.com/projects/${var.project_id}/logs/my-http-function"

  filter = "resource.type=\"cloud_function\" AND resource.labels.function_name=\"my-http-function\""
}

# Monitoring alert
resource "google_monitoring_alert_policy" "function_errors" {
  display_name = "Cloud Function Error Rate"
  combiner     = "OR"

  conditions {
    display_name = "Error rate threshold"

    condition_threshold {
      filter          = "metric.type=\"cloudfunctions.googleapis.com/function/error_count\" AND resource.type=\"cloud_function\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 10
      aggregations {
        alignment_period    = "60s"
        per_series_aligner  = "ALIGN_RATE"
      }
    }
  }
}

output "http_function_url" {
  value = google_cloudfunctions2_function.http_function.service_config[0].uri
}
```

## Best Practices

### ✅ DO
- Use service accounts with least privilege
- Store secrets in Secret Manager
- Implement proper error handling
- Use environment variables for configuration
- Monitor with Cloud Logging and Cloud Monitoring
- Set appropriate memory and timeout
- Use event filters to reduce invocations
- Implement idempotent functions

### ❌ DON'T
- Store secrets in code
- Use default service account
- Create long-running functions
- Ignore error handling
- Deploy without testing
- Use unauthenticated access for sensitive functions

## Monitoring

- Cloud Logging for application logs
- Cloud Monitoring for metrics
- Error Reporting for error tracking
- Cloud Trace for distributed tracing
- Cloud Profiler for performance analysis

## Resources

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Cloud Functions Best Practices](https://cloud.google.com/functions/docs/bestpractices/retries)
- [Cloud Functions Terraform Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions2_function)
