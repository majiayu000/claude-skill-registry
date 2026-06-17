---
name: gcloud
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Google Cloud Platform CLI - manage GCP resources. Use when working with Compute
  Engine, Cloud Run, GKE, Cloud Functions, Storage, BigQuery, or other GCP services.
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | THE EXACT PROMPT | Services | Output Formatting | AGENTS.md Blurb | When to Use | References -->

# GCloud CLI

> **Core Capability:** Manage Google Cloud Platform resources and services from the command line.

## Quick Start

```bash
# Install
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Verify
gcloud version

# Check auth
gcloud auth list

# Set project
gcloud config set project PROJECT_ID

# Show current config
gcloud config list
```

---

## THE EXACT PROMPT — Auth & Config

```
# Login interactively
gcloud auth login

# Service account auth
gcloud auth activate-service-account --key-file=key.json

# Application default credentials
gcloud auth application-default login

# Set project
gcloud config set project PROJECT_ID

# Set region/zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Named configurations
gcloud config configurations create my-config
gcloud config configurations activate my-config
```

---

## THE EXACT PROMPT — Compute Engine

```
# List VMs
gcloud compute instances list

# Create VM
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-12 \
  --image-project=debian-cloud

# SSH to VM
gcloud compute ssh my-vm --zone=us-central1-a

# Stop/start
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
```

---

## THE EXACT PROMPT — Cloud Run

```
# List services
gcloud run services list

# Deploy from source
gcloud run deploy my-service --source . --region=us-central1

# Deploy container
gcloud run deploy my-service \
  --image=gcr.io/PROJECT/IMAGE \
  --region=us-central1 \
  --allow-unauthenticated

# View logs
gcloud run services logs read my-service --region=us-central1
```

---

## THE EXACT PROMPT — Cloud Storage

```
# List buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://my-bucket --location=us-central1

# Upload/download
gcloud storage cp local-file.txt gs://my-bucket/
gcloud storage cp gs://my-bucket/file.txt ./

# Sync directory
gcloud storage rsync -r ./local-dir gs://my-bucket/remote-dir
```

---

## Essential Commands

| Service | List | Create | Delete |
|---------|------|--------|--------|
| Compute | `gcloud compute instances list` | `gcloud compute instances create` | `gcloud compute instances delete` |
| Cloud Run | `gcloud run services list` | `gcloud run deploy` | `gcloud run services delete` |
| Functions | `gcloud functions list` | `gcloud functions deploy` | `gcloud functions delete` |
| GKE | `gcloud container clusters list` | `gcloud container clusters create` | `gcloud container clusters delete` |
| Storage | `gcloud storage buckets list` | `gcloud storage buckets create` | `gcloud storage rm` |

---

## Output Formatting

```bash
# JSON output
gcloud compute instances list --format=json

# Table with specific columns
gcloud compute instances list --format="table(name,zone,status)"

# Filter results
gcloud compute instances list --filter="status=RUNNING"

# Quiet mode (no prompts)
gcloud compute instances delete my-vm --quiet
```

---

## Quick Reference

```bash
gcloud cheat-sheet      # Built-in cheat sheet
gcloud interactive      # Interactive shell
gcloud --help           # General help
gcloud compute --help   # Service-specific help
```

---

## AGENTS.md Blurb

Copy this to your project's AGENTS.md:

```markdown
### Google Cloud CLI (gcloud)

`gcloud` is installed and authenticated.

Auth:

\`\`\`bash
gcloud auth login
gcloud auth application-default login  # For API libraries
\`\`\`

Project:

\`\`\`bash
gcloud config set project <PROJECT_ID>
\`\`\`

Enable APIs:

\`\`\`bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable analyticsdata.googleapis.com
\`\`\`

Useful commands:

\`\`\`bash
gcloud projects list
gcloud services list --enabled
gcloud beta billing accounts list
\`\`\`
```

---

## When to Use

- Enabling APIs for Gemini, Vertex AI, or other Google services
- Managing billing and cost alerts
- Creating service accounts for CI/CD
- Deploying containers to Cloud Run
- Managing GKE clusters

---

## References

| Topic | Reference |
|-------|-----------|
| All services | [SERVICES.md](references/SERVICES.md) |
| IAM & Security | [IAM.md](references/IAM.md) |
