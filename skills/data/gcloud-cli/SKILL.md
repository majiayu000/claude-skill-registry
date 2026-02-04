---
name: gcloud-cli
description: Google Cloud CLI operations and resource management
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Never expose service account keys
  - Resource deletion requires confirmation
  - Verify project before operations
error_handling: graceful
streaming: supported
---

# Google Cloud CLI Skill

## Installation

The skill invokes the `gcloud` CLI. Install and initialize:

- **Linux/macOS**: `curl https://sdk.cloud.google.com | bash` then restart shell and run `gcloud init`
- **Windows**: Download [Google Cloud SDK installer](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe) or use PowerShell to download and run

Verify: `gcloud --version`. Configure: `gcloud init`

## Cheat Sheet & Best Practices

**Config:** `gcloud config set project <id>`; `gcloud config list`; `gcloud config configurations create/activate <name>` — switch projects.

**Auth:** `gcloud auth login`; use `--impersonate-service-account` for SA; `--access-token-file` for CI.

**Hacks:** Use `--format="table(name,zone,status)"` or `--format=json` + jq to cut output. Use `--flags-file=file.yaml` for long or repeated flags. Use named configurations for dev/staging/prod. Run `gcloud components update` periodically.

## Certifications & Training

**Free:** [Google Cloud Learn](https://cloud.google.com/learn) and [Google Skills](https://www.cloudskillsboost.google/) — Innovators Program (35 credits/month). **Certs:** Cloud Digital Leader, Cloud Engineer (associate), Cloud Architect/DevOps (professional). **Skill data:** Config, auth, compute/storage/IAM; no exposed service-account keys.

## Hooks & Workflows

**Suggested hooks:** Pre-deploy: `gcloud config get-value project`. Use when **devops** is routed for GCP tasks (contextual: `gcp_project`).

**Workflows:** Use with **devops** (contextual: `gcp_project`). Flow: detect GCP → load gcloud-cli → run CLI via skill script.

## Overview

Google Cloud Platform CLI operations. 90%+ context savings.

## Requirements

- gcloud CLI installed
- GOOGLE_PROJECT_ID environment variable
- Authenticated via gcloud auth

## Tools (Progressive Disclosure)

### Compute

| Tool             | Description       | Confirmation |
| ---------------- | ----------------- | ------------ |
| instances-list   | List VM instances | No           |
| instances-create | Create VM         | Yes          |
| instances-delete | Delete VM         | **REQUIRED** |

### Storage

| Tool       | Description          | Confirmation |
| ---------- | -------------------- | ------------ |
| storage-ls | List buckets/objects | No           |
| storage-cp | Copy objects         | Yes          |
| storage-rm | Delete objects       | Yes          |

### IAM

| Tool             | Description           |
| ---------------- | --------------------- |
| iam-list         | List IAM policies     |
| service-accounts | List service accounts |

### Logging

| Tool      | Description            |
| --------- | ---------------------- |
| logs-read | Read logs              |
| logs-tail | Tail logs in real-time |

### BLOCKED

| Tool              | Status      |
| ----------------- | ----------- |
| projects delete   | **BLOCKED** |
| iam-policy delete | **BLOCKED** |

## Agent Integration

- **devops** (primary): Cloud operations
- **gcp-cloud-agent** (primary): GCP specific
- **cloud-integrator** (secondary): Multi-cloud

## Security

⚠️ Never expose service account keys
⚠️ Resource deletion requires confirmation

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
