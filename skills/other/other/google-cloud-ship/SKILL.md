---
name: google-cloud-ship
description: Google Cloud shipping gate for Cloud Run, GKE, GCE, App Engine, Cloud Functions, IAM, Secret Manager, load balancers, and rollout safety. Use when releasing to GCP and you want a provider-specific read on service accounts, config drift, scaling traps, or rollback realism.
user-invocable: true
argument-hint: "[Cloud Run service, GKE deploy, or GCP release]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Wrong IAM is production breakage with paperwork.
- If the secret path is wrong, your health checks are fiction.
- A rollout without rollback is just optimism with YAML.
- Autoscaling hides mistakes until traffic arrives.

## What to interrogate

### 1. Release surface

State what is shipping:
- Cloud Run
- GKE
- App Engine
- Cloud Functions
- load balancer or IAM change
- secrets, networking, or env config

### 2. Runtime and identity

Check:
- service account assumptions
- IAM bindings
- secret access
- environment parity
- network reachability and ingress expectations

### 3. Scale and startup risks

Review:
- cold start sensitivity
- request timeout assumptions
- concurrency and memory settings
- health probe realism
- autoscaling behavior under burst load

### 4. Rollout and rollback

Ask:
- is this canary, gradual, or instant?
- what happens if new revision is bad?
- can traffic shift back cleanly?
- do data or config changes make rollback fake?

## Output format

### GCP release surface

What actually changes in the platform.

### Platform blockers

IAM, secret, network, startup, or scaling blockers.

### Rollout risk

What fails during deploy, scale-up, or rollback.

### Mitigation and rollback plan

Concrete safer rollout steps.

### Verdict

- **Safe to release**
- **Fix before release**
- **GCP release red flag**
