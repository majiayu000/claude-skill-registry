---
name: gcloud
description: "Google Cloud Platform CLI - manage GCP resources including Compute Engine, Cloud Run, GKE, Cloud Functions, Storage, BigQuery, and more."
---

# GCloud Skill

Use the `gcloud` CLI to manage Google Cloud Platform resources and services.

## Authentication

Check current auth:
```bash
gcloud auth list
```

Login interactively:
```bash
gcloud auth login
```

Login with service account:
```bash
gcloud auth activate-service-account --key-file=key.json
```

Application default credentials:
```bash
gcloud auth application-default login
```

## Project & Configuration

List projects:
```bash
gcloud projects list
```

Set default project:
```bash
gcloud config set project PROJECT_ID
```

Show current config:
```bash
gcloud config list
```

Create named configuration:
```bash
gcloud config configurations create my-config
gcloud config configurations activate my-config
```

Set default region/zone:
```bash
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

## Compute Engine (VMs)

List instances:
```bash
gcloud compute instances list
```

Create instance:
```bash
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

SSH to instance:
```bash
gcloud compute ssh my-vm --zone=us-central1-a
```

Stop/start instance:
```bash
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
```

Delete instance:
```bash
gcloud compute instances delete my-vm --zone=us-central1-a
```

## Cloud Run

List services:
```bash
gcloud run services list
```

Deploy from source:
```bash
gcloud run deploy my-service --source . --region=us-central1
```

Deploy container:
```bash
gcloud run deploy my-service \
  --image=gcr.io/PROJECT/IMAGE \
  --region=us-central1 \
  --allow-unauthenticated
```

View logs:
```bash
gcloud run services logs read my-service --region=us-central1
```

Update traffic split:
```bash
gcloud run services update-traffic my-service \
  --to-revisions=LATEST=100 \
  --region=us-central1
```

## Cloud Functions

List functions:
```bash
gcloud functions list
```

Deploy function (2nd gen):
```bash
gcloud functions deploy my-function \
  --gen2 \
  --runtime=nodejs20 \
  --region=us-central1 \
  --trigger-http \
  --entry-point=handler \
  --source=.
```

View logs:
```bash
gcloud functions logs read my-function --region=us-central1
```

Delete function:
```bash
gcloud functions delete my-function --region=us-central1
```

## Google Kubernetes Engine (GKE)

List clusters:
```bash
gcloud container clusters list
```

Get credentials for kubectl:
```bash
gcloud container clusters get-credentials my-cluster \
  --zone=us-central1-a
```

Create cluster:
```bash
gcloud container clusters create my-cluster \
  --zone=us-central1-a \
  --num-nodes=3
```

Resize node pool:
```bash
gcloud container clusters resize my-cluster \
  --node-pool=default-pool \
  --num-nodes=5 \
  --zone=us-central1-a
```

## Cloud Storage

List buckets:
```bash
gcloud storage buckets list
```

Create bucket:
```bash
gcloud storage buckets create gs://my-bucket --location=us-central1
```

List objects:
```bash
gcloud storage ls gs://my-bucket/
```

Copy files:
```bash
# Upload
gcloud storage cp local-file.txt gs://my-bucket/

# Download
gcloud storage cp gs://my-bucket/file.txt ./

# Recursive
gcloud storage cp -r ./local-dir gs://my-bucket/
```

Sync directory:
```bash
gcloud storage rsync -r ./local-dir gs://my-bucket/remote-dir
```

## Cloud SQL

List instances:
```bash
gcloud sql instances list
```

Create instance:
```bash
gcloud sql instances create my-instance \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

Connect via proxy:
```bash
gcloud sql connect my-instance --user=postgres
```

Create database:
```bash
gcloud sql databases create mydb --instance=my-instance
```

## BigQuery

List datasets:
```bash
bq ls
```

Run query:
```bash
bq query --use_legacy_sql=false 'SELECT * FROM dataset.table LIMIT 10'
```

Create dataset:
```bash
bq mk --dataset my_dataset
```

Load data:
```bash
bq load --source_format=CSV my_dataset.my_table gs://bucket/data.csv
```

## Pub/Sub

List topics:
```bash
gcloud pubsub topics list
```

Create topic:
```bash
gcloud pubsub topics create my-topic
```

Publish message:
```bash
gcloud pubsub topics publish my-topic --message="Hello"
```

Create subscription:
```bash
gcloud pubsub subscriptions create my-sub --topic=my-topic
```

Pull messages:
```bash
gcloud pubsub subscriptions pull my-sub --auto-ack
```

## Secret Manager

List secrets:
```bash
gcloud secrets list
```

Create secret:
```bash
echo -n "my-secret-value" | gcloud secrets create my-secret --data-file=-
```

Access secret:
```bash
gcloud secrets versions access latest --secret=my-secret
```

Add new version:
```bash
echo -n "new-value" | gcloud secrets versions add my-secret --data-file=-
```

## IAM

List service accounts:
```bash
gcloud iam service-accounts list
```

Create service account:
```bash
gcloud iam service-accounts create my-sa \
  --display-name="My Service Account"
```

Create key:
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=my-sa@PROJECT.iam.gserviceaccount.com
```

Add IAM binding:
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

## Cloud Build

Submit build:
```bash
gcloud builds submit --tag gcr.io/PROJECT/IMAGE
```

List builds:
```bash
gcloud builds list
```

View build logs:
```bash
gcloud builds log BUILD_ID
```

## Artifact Registry

List repositories:
```bash
gcloud artifacts repositories list
```

Configure Docker:
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

## Logging

Read logs:
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

Tail logs:
```bash
gcloud logging tail "resource.type=gce_instance"
```

## App Engine

Deploy app:
```bash
gcloud app deploy
```

View logs:
```bash
gcloud app logs tail
```

Browse app:
```bash
gcloud app browse
```

## Useful Flags

Format as JSON:
```bash
gcloud compute instances list --format=json
```

Format as table with specific columns:
```bash
gcloud compute instances list --format="table(name,zone,status)"
```

Filter results:
```bash
gcloud compute instances list --filter="status=RUNNING"
```

Quiet mode (no prompts):
```bash
gcloud compute instances delete my-vm --quiet
```

## Cheat Sheet

Quick reference:
```bash
gcloud cheat-sheet
```

Interactive shell:
```bash
gcloud interactive
```
