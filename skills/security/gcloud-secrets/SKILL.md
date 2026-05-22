---
name: gcloud-secrets
description: Manage Google Cloud Secret Manager for storing and fetching environment secrets. Use when working with deployment, secrets, or gcloud commands.
---

# Google Cloud Secret Manager

## Project Configuration

- **Project ID**: `myimageupscaler-auth`
- **Account**: `jfurtado141@gmail.com`
- **Secrets**:
  - `myimageupscaler-api-prod` → `.env.api.prod`
  - `myimageupscaler-client-prod` → `.env.client.prod`

## Setup Commands

```bash
# Set correct account and project
gcloud config set account jfurtado141@gmail.com
gcloud config set project myimageupscaler-auth

# Verify access
gcloud secrets list
```

## Common Issues

### "Failed to fetch secret" Error

1. Check current project: `gcloud config get-value project`
2. Check current account: `gcloud config get-value account`
3. Switch to correct account/project (see above)

### Wrong Project

The CLI might default to `definya-447700`. Always ensure you're on `myimageupscaler-auth`.

### Service Account vs Personal Account

- Service account `cloudstartlabs-service-acc@coldstartlabs-auth.iam.gserviceaccount.com` does NOT have access to myimageupscaler-auth
- Use personal account `jfurtado141@gmail.com` for secret access
- **Or** use the service account key at `./cloud/keys/myimageupscaler-auth-6348371fe8c6.json`:
  ```bash
  gcloud auth activate-service-account --key-file=./cloud/keys/myimageupscaler-auth-6348371fe8c6.json
  ```

## Deploy Flow

The deploy script (`scripts/deploy/deploy.sh`) fetches secrets in step 0:

1. Fetches `myimageupscaler-api-prod` → `.env.api.prod`
2. Fetches `myimageupscaler-client-prod` → `.env.client.prod`
3. Cleans up these files after deploy (success or failure)

## Updating Secrets

```bash
# Update API secrets
gcloud secrets versions add myimageupscaler-api-prod --data-file=.env.api

# Update client secrets
gcloud secrets versions add myimageupscaler-client-prod --data-file=.env.client
```

**Important**: Always destroy older versions after adding a new one to avoid secret sprawl and reduce security risk:

```bash
# List versions to find the old one
gcloud secrets versions list myimageupscaler-api-prod

# Destroy the previous version (replace N with version number)
gcloud secrets versions destroy N --secret=myimageupscaler-api-prod --quiet
```

## Service Account Key Location

Local keys available at:

- `./cloud/keys/coldstart-labs-service-account-key.json` (Note: Does not have access to myimageupscaler-auth project)
- `./cloud/keys/myimageupscaler-auth-6348371fe8c6.json` (myimageupscaler-auth project)

**Important**: The `cloud/keys/` directory is gitignored. Never commit service account keys.
