---
name: google-cloud
description: Manage Google Cloud resources via gcloud CLI. Compute, storage, and cloud functions.
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["gcloud"]}}}
---
# Google Cloud Platform
Cloud infrastructure and services.
## Auth
```bash
gcloud auth login
gcloud config set project PROJECT_ID
```
## Compute Engine
```bash
gcloud compute instances list
gcloud compute instances create vm-name --zone=us-central1-a --machine-type=e2-micro
gcloud compute instances stop vm-name --zone=us-central1-a
```
## Cloud Functions
```bash
gcloud functions list
gcloud functions deploy myFunction --runtime nodejs18 --trigger-http --allow-unauthenticated
gcloud functions call myFunction --data '{"name": "test"}'
```
## Cloud Storage
```bash
gsutil ls gs://bucket-name/
gsutil cp file.txt gs://bucket-name/
gsutil cp gs://bucket-name/file.txt ./
```
## Cloud Run
```bash
gcloud run services list
gcloud run deploy service-name --image gcr.io/project/image --platform managed
```
## Links
- Console: https://console.cloud.google.com
- Docs: https://cloud.google.com/sdk/gcloud/reference
